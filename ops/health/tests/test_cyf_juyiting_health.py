import importlib.util
import json
import os
import shutil
import stat
import tempfile
import unittest

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODULE_PATH = os.path.join(HERE, "cyf-juyiting-health.py")
SPEC = importlib.util.spec_from_file_location("cyf_juyiting_health", MODULE_PATH)
health = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(health)


def stopped():
    return {"healthy": False, "classification": "stopped", "recovery_safe": True,
            "returncode": 3, "pid": None, "elapsed_seconds": None}


def up():
    return {"healthy": True, "classification": "up", "recovery_safe": False,
            "returncode": 0, "pid": 123, "elapsed_seconds": 2000}


def busy():
    return {"healthy": False, "classification": "canonical_busy_or_error",
            "recovery_safe": False, "returncode": 1, "pid": None, "elapsed_seconds": None}


def unsafe():
    return {"healthy": False, "classification": "canonical_unsafe_identity_or_listener",
            "recovery_safe": False, "returncode": 5, "pid": None, "elapsed_seconds": None}


def not_ready(age=1600, safe=True):
    return {"healthy": False,
            "classification": "not_ready_trusted" if safe else "not_ready_identity_incomplete",
            "recovery_safe": safe, "returncode": 4, "pid": 123,
            "elapsed_seconds": age}


class FakeEffects(object):
    def __init__(self, statuses=None):
        self.statuses = list(statuses or [up()])
        self.recoveries = []
        self.recovery_rc = 0
        self.web_result = {"healthy": True, "classification": "web_ok"}
        self.public_api_result = {"healthy": True, "classification": "auth_boundary_ok"}
        self.mysql_result = {"healthy": True, "classification": "mysql_reachable"}
        self.redis_result = {"healthy": True, "classification": "redis_reachable"}
        self.agent_result = {"healthy": True, "classification": "agent_active"}
        self.resource_result = {"healthy": True, "classification": "resources_ok"}
        self.mail_results = []
        self.mail_calls = []
        self.events = []

    def canonical_status(self):
        self.events.append("status")
        if len(self.statuses) > 1:
            return self.statuses.pop(0)
        return self.statuses[0]

    def recover(self, action):
        self.events.append("recover:" + action)
        self.recoveries.append(action)
        return {"returncode": self.recovery_rc, "classification": "exit_%d" % self.recovery_rc}

    def web(self, marker):
        self.events.append("web")
        return dict(self.web_result)

    def public_api(self):
        self.events.append("public_api")
        return dict(self.public_api_result)

    def mysql(self):
        self.events.append("mysql")
        return dict(self.mysql_result)

    def redis(self):
        self.events.append("redis")
        return dict(self.redis_result)

    def agent(self):
        self.events.append("agent")
        return dict(self.agent_result)

    def resources(self):
        self.events.append("resources")
        return dict(self.resource_result)

    def send_email(self, subject, body):
        self.events.append("mail")
        self.mail_calls.append((subject, body))
        if self.mail_results:
            return self.mail_results.pop(0)
        return True, "helper_accepted"


class Clock(object):
    def __init__(self, now=2000000000):
        self.now = now

    def __call__(self):
        return self.now


class MonitorTests(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        self.config = {"schema_version": 1, "web_marker": '<div id="app"></div>',
                       "email_enabled": True, "reminder_interval_seconds": 21600}
        self.persisted = []

    def monitor(self, effects):
        return health.Monitor(effects, lambda state: self.persisted.append(json.loads(json.dumps(state))), self.clock)

    def test_stopped_threshold_starts_on_third_failure(self):
        effects = FakeEffects([stopped(), stopped(), stopped(), up()])
        state = health.initial_state(self.clock.now)
        monitor = self.monitor(effects)
        monitor.check_once(state, self.config)
        monitor.check_once(state, self.config)
        self.assertEqual([], effects.recoveries)
        result = monitor.check_once(state, self.config)
        self.assertEqual(["start"], effects.recoveries)
        self.assertEqual("success_health_up", result["recovery"]["result"])
        recovery_index = effects.events.index("recover:start")
        self.assertIn("mail", effects.events[:recovery_index])
        fenced = [item for item in self.persisted if item["recovery"]["in_flight"]]
        self.assertEqual(1, fenced[-1]["recovery"]["attempts"])

    def test_rc1_busy_never_recovers(self):
        effects = FakeEffects([busy()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        result = self.monitor(effects).check_once(state, self.config)
        self.assertEqual([], effects.recoveries)
        self.assertEqual("identity_or_status_not_recovery_safe", result["recovery"]["decision"])

    def test_rc5_foreign_identity_never_recovers(self):
        effects = FakeEffects([unsafe()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        self.monitor(effects).check_once(state, self.config)
        self.assertEqual([], effects.recoveries)

    def test_external_only_failure_never_recovers_healthy_api(self):
        effects = FakeEffects([up()])
        effects.public_api_result = {"healthy": False, "classification": "auth_boundary_invalid"}
        state = health.initial_state(self.clock.now)
        monitor = self.monitor(effects)
        for _ in range(3):
            monitor.check_once(state, self.config)
        self.assertEqual([], effects.recoveries)
        self.assertEqual("local_api_up", state["last_snapshot"]["recovery"]["decision"])
        self.assertEqual(["public_api"], state["incident"]["components"])

    def test_maintenance_reports_but_pauses_recovery(self):
        effects = FakeEffects([stopped()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        result = self.monitor(effects).check_once(state, self.config, maintenance=True)
        self.assertEqual([], effects.recoveries)
        self.assertTrue(result["maintenance"])
        self.assertEqual("maintenance_paused", result["recovery"]["decision"])
        self.assertFalse(state["last_snapshot"]["checks"]["local_api"]["healthy"])

    def test_cooldown_blocks_second_attempt(self):
        effects = FakeEffects([stopped()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        state["recovery"]["attempts"] = 1
        state["recovery"]["last_attempt_at"] = self.clock.now - 100
        result = self.monitor(effects).check_once(state, self.config)
        self.assertEqual([], effects.recoveries)
        self.assertEqual("cooldown", result["recovery"]["decision"])

    def test_interrupted_attempt_is_fenced(self):
        effects = FakeEffects([stopped()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        state["recovery"]["attempts"] = 1
        state["recovery"]["last_attempt_at"] = self.clock.now - 10
        state["recovery"]["in_flight"] = {"action": "start", "attempt": 1,
                                            "at": self.clock.now - 10}
        self.monitor(effects).check_once(state, self.config)
        self.assertEqual([], effects.recoveries)
        self.assertEqual(1, state["recovery"]["attempts"])
        self.assertIsNotNone(state["recovery"]["in_flight"])

    def test_second_failure_latches_circuit(self):
        effects = FakeEffects([stopped(), stopped()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        state["recovery"]["attempts"] = 1
        state["recovery"]["last_attempt_at"] = self.clock.now - health.COOLDOWN_SECONDS
        self.monitor(effects).check_once(state, self.config)
        self.assertEqual(["start"], effects.recoveries)
        self.assertEqual(2, state["recovery"]["attempts"])
        self.assertTrue(state["recovery"]["circuit_latched"])

    def test_second_success_still_latches_until_three_up_observations(self):
        effects = FakeEffects([stopped(), up()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        state["recovery"]["attempts"] = 1
        state["recovery"]["last_attempt_at"] = self.clock.now - health.COOLDOWN_SECONDS
        self.monitor(effects).check_once(state, self.config)
        self.assertTrue(state["recovery"]["circuit_latched"])
        self.assertEqual(1, state["api_healthy_streak"])

    def test_three_healthy_checks_reset_circuit(self):
        effects = FakeEffects([up()])
        state = health.initial_state(self.clock.now)
        state["recovery"].update({"attempts": 2, "circuit_latched": True,
                                  "last_attempt_at": self.clock.now - 100,
                                  "in_flight": {"action": "start", "attempt": 2,
                                                "at": self.clock.now - 100}})
        monitor = self.monitor(effects)
        for _ in range(3):
            monitor.check_once(state, self.config)
        self.assertEqual(0, state["recovery"]["attempts"])
        self.assertFalse(state["recovery"]["circuit_latched"])
        self.assertIsNone(state["recovery"]["in_flight"])

    def test_dependency_down_blocks_recovery(self):
        effects = FakeEffects([stopped()])
        effects.mysql_result = {"healthy": False, "classification": "mysql_refused"}
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        result = self.monitor(effects).check_once(state, self.config)
        self.assertEqual([], effects.recoveries)
        self.assertEqual("dependencies_unreachable", result["recovery"]["decision"])

    def test_not_ready_requires_grace_and_full_identity(self):
        effects = FakeEffects([not_ready(1499)])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        result = self.monitor(effects).check_once(state, self.config)
        self.assertEqual("startup_grace", result["recovery"]["decision"])
        self.assertEqual([], effects.recoveries)

        effects = FakeEffects([not_ready(1500), up()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        self.monitor(effects).check_once(state, self.config)
        self.assertEqual(["restart"], effects.recoveries)

    def test_rc4_without_runtime_identity_is_alert_only(self):
        effects = FakeEffects([not_ready(5000, safe=False)])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        result = self.monitor(effects).check_once(state, self.config)
        self.assertEqual([], effects.recoveries)
        self.assertEqual("identity_or_status_not_recovery_safe", result["recovery"]["decision"])

    def test_exit_zero_without_fresh_up_is_failure(self):
        effects = FakeEffects([stopped(), not_ready(1700)])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        result = self.monitor(effects).check_once(state, self.config)
        self.assertEqual("failed_fresh_health_not_up", result["recovery"]["result"])
        self.assertIsNone(state["recovery"]["last_success_at"])

    def test_resource_gate_does_not_consume_attempt(self):
        effects = FakeEffects([stopped()])
        effects.resource_result = {"healthy": False,
                                   "classification": "resources_below_canonical_minimum"}
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        result = self.monitor(effects).check_once(state, self.config)
        self.assertEqual([], effects.recoveries)
        self.assertEqual(0, state["recovery"]["attempts"])
        self.assertEqual("resources_blocked", result["recovery"]["decision"])


class MailQueueTests(unittest.TestCase):
    def test_email_retry_and_dedup(self):
        now = 2000000000
        state = health.initial_state(now)
        added = health.enqueue_notice(state, "same", "incident_confirmed", "subject", "body", now)
        duplicate = health.enqueue_notice(state, "same", "incident_confirmed", "subject", "body", now)
        self.assertTrue(added)
        self.assertFalse(duplicate)
        effects = FakeEffects()
        effects.mail_results = [(False, "helper_failed")]
        config = {"email_enabled": True}
        self.assertEqual(0, health.flush_outbox(state, effects, config, now, 2))
        self.assertEqual(1, len(state["outbox"]))
        self.assertGreater(state["outbox"][0]["next_attempt_at"], now)
        effects.mail_results = [(True, "helper_accepted")]
        retry_at = state["outbox"][0]["next_attempt_at"]
        self.assertEqual(1, health.flush_outbox(state, effects, config, retry_at, 2))
        self.assertEqual([], state["outbox"])

    def test_outbox_is_bounded_and_coalesces(self):
        state = health.initial_state(1)
        for number in range(health.MAX_OUTBOX + 10):
            health.enqueue_notice(state, "n%d" % number, "recovery_result", "subject", "body", number + 1)
        self.assertLessEqual(len(state["outbox"]), health.MAX_OUTBOX)
        self.assertTrue(any(item["event"] == "digest" for item in state["outbox"]))


class StateStoreSecurityTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="cyf-health-test-")
        self.state_dir = os.path.join(self.root, "state")
        self.store = health.StateStore(self.state_dir, expected_uid=os.getuid(), validate_parents=False)
        self.store.prepare_init()
        self.store.acquire()

    def tearDown(self):
        self.store.release()
        shutil.rmtree(self.root)

    def test_round_trip_atomic_state(self):
        state = health.initial_state(10)
        self.store.write(state)
        self.assertEqual(state, self.store.read())
        self.assertEqual(0o600, stat.S_IMODE(os.lstat(self.store.state_path).st_mode))

    def test_fail_closed_missing_and_corrupt_state(self):
        with self.assertRaises(health.MonitorError):
            self.store.read()
        with open(self.store.state_path, "w") as stream:
            stream.write("not-json")
        os.chmod(self.store.state_path, 0o600)
        with self.assertRaises(health.MonitorError):
            self.store.read()

    def test_fail_closed_insecure_state_mode(self):
        self.store.write(health.initial_state(10))
        os.chmod(self.store.state_path, 0o644)
        with self.assertRaises(health.MonitorError):
            self.store.read()

    def test_nonblocking_singleton_lock(self):
        second = health.StateStore(self.state_dir, expected_uid=os.getuid(), validate_parents=False)
        with self.assertRaises(health.BusyError):
            second.acquire()
        second.release()

    def test_pause_resume_marker(self):
        self.store.write(health.initial_state(10))
        self.store.pause(10)
        self.assertTrue(self.store.maintenance())
        self.store.resume()
        self.assertFalse(self.store.maintenance())


class ConfigSecurityTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="cyf-health-config-")
        self.path = os.path.join(self.root, "config.json")
        self.valid = {"schema_version": 1, "web_marker": '<div id="app"></div>',
                      "email_enabled": True, "reminder_interval_seconds": 21600}

    def tearDown(self):
        shutil.rmtree(self.root)

    def write(self, data, mode=0o600):
        with open(self.path, "w") as stream:
            json.dump(data, stream)
        os.chmod(self.path, mode)

    def test_valid_config(self):
        self.write(self.valid)
        self.assertEqual(self.valid, health.load_config(self.path, os.getuid(), False))

    def test_rejects_command_or_url_configuration(self):
        data = dict(self.valid)
        data["recovery_command"] = "/bin/true"
        self.write(data)
        with self.assertRaises(health.MonitorError):
            health.load_config(self.path, os.getuid(), False)

    def test_rejects_insecure_mode(self):
        self.write(self.valid, 0o644)
        with self.assertRaises(health.MonitorError):
            health.load_config(self.path, os.getuid(), False)

    def test_rejects_symlink(self):
        target = self.path + ".target"
        with open(target, "w") as stream:
            json.dump(self.valid, stream)
        os.chmod(target, 0o600)
        os.symlink(target, self.path)
        with self.assertRaises(health.MonitorError):
            health.load_config(self.path, os.getuid(), False)

    def test_rejects_duplicate_json_key(self):
        with open(self.path, "w") as stream:
            stream.write('{"schema_version":1,"schema_version":1,"web_marker":"x","email_enabled":true,"reminder_interval_seconds":21600}')
        os.chmod(self.path, 0o600)
        with self.assertRaises(health.MonitorError):
            health.load_config(self.path, os.getuid(), False)


class ProbeContractTests(unittest.TestCase):
    def canonical_output(self, health_value="UP", identity=True, listener=True, elapsed="25:01"):
        lines = ["STATUS=RUNNING", "PID=123",
                 "  PID  PPID                  STARTED     ELAPSED STAT %CPU %MEM   RSS CMD",
                 "  123     1 Sat Sep  5 12:00:00 2026       %s Sl    0.0  1.0 1 java" % elapsed,
                 "ARTIFACT_ATTESTATION=MATCH"]
        if listener:
            lines.append("PORT_10018=LISTENING_BY_PID")
        if identity:
            lines.append("RUNTIME_IDENTITY=" + health.EXPECTED_RUNTIME_IDENTITY)
        lines.append("HEALTH=" + health_value)
        return "\n".join(lines) + "\n"

    def test_canonical_parser_requires_full_up_identity(self):
        parsed = health.parse_canonical_status(0, self.canonical_output())
        self.assertTrue(parsed["healthy"])
        self.assertEqual(1501, parsed["elapsed_seconds"])
        incomplete = health.parse_canonical_status(0, self.canonical_output(identity=False))
        self.assertFalse(incomplete["healthy"])

    def test_canonical_rc4_no_listener_is_not_recovery_safe(self):
        parsed = health.parse_canonical_status(4, self.canonical_output("NOT_READY", identity=False, listener=False))
        self.assertFalse(parsed["recovery_safe"])
        self.assertEqual("not_ready_identity_incomplete", parsed["classification"])

    def test_public_api_requires_json_auth_denial(self):
        effects = health.Effects()
        effects._http = lambda url: (403, "text/html", b"nginx forbidden", "completed")
        self.assertFalse(effects.public_api()["healthy"])
        effects._http = lambda url: (403, "application/json", b'{"message":"Forbidden"}', "completed")
        self.assertTrue(effects.public_api()["healthy"])

    def test_web_requires_html_marker(self):
        effects = health.Effects()
        effects._http = lambda url: (200, "text/html", b'<div id="app"></div>', "completed")
        self.assertTrue(effects.web('<div id="app"></div>')["healthy"])
        effects._http = lambda url: (200, "application/json", b'<div id="app"></div>', "completed")
        self.assertFalse(effects.web('<div id="app"></div>')["healthy"])


class StaticContractTests(unittest.TestCase):
    def test_fixed_recovery_and_mail_commands(self):
        with open(MODULE_PATH, "r") as stream:
            source = stream.read()
        self.assertIn('[CANONICAL, "status"]', source)
        self.assertIn('[CANONICAL, action]', source)
        self.assertIn('[MAIL_PYTHON, "-I", MAIL_HELPER', source)
        self.assertNotIn("shell=True", source)
        self.assertNotIn("/home/isp/bin", source)

    def test_cron_syntax_contract(self):
        path = os.path.join(HERE, "cyf-juyiting-health.cron")
        with open(path, "r") as stream:
            text = stream.read()
        command = "* * * * * root /usr/bin/python3 -I /usr/local/libexec/cyf-juyiting-health.py --check-once"
        self.assertIn(command, text)
        self.assertNotIn("systemd-run", text)
        self.assertNotIn("curl", text)


if __name__ == "__main__":
    unittest.main()
