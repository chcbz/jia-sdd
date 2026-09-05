import importlib.util
import json
import os
import shutil
import stat
import tempfile
import unittest
from unittest import mock

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


def not_ready(age=1600, safe=True, pid=123):
    return {"healthy": False,
            "classification": "not_ready_trusted" if safe else "not_ready_identity_incomplete",
            "recovery_safe": safe, "returncode": 4, "pid": pid,
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
        self.mail_observer = None

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
        if self.mail_observer is not None:
            self.mail_observer(subject, body)
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
        effects = FakeEffects([stopped(), stopped(), stopped(), stopped(), up()])
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
        effects = FakeEffects([stopped(), stopped(), stopped()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        state["recovery"]["attempts"] = 1
        state["recovery"]["last_attempt_at"] = self.clock.now - health.COOLDOWN_SECONDS
        self.monitor(effects).check_once(state, self.config)
        self.assertEqual(["start"], effects.recoveries)
        self.assertEqual(2, state["recovery"]["attempts"])
        self.assertTrue(state["recovery"]["circuit_latched"])

    def test_second_success_still_latches_until_three_up_observations(self):
        effects = FakeEffects([stopped(), stopped(), up()])
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

        effects = FakeEffects([not_ready(1500), not_ready(1600), up()])
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
        effects = FakeEffects([stopped(), stopped(), not_ready(1700)])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        result = self.monitor(effects).check_once(state, self.config)
        self.assertEqual("failed_fresh_health_not_up", result["recovery"]["result"])
        self.assertIsNone(state["recovery"]["last_success_at"])

    def test_post_mail_restart_revalidation_healthy_skips_command(self):
        effects = FakeEffects([not_ready(1600), up()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        result = self.monitor(effects).check_once(state, self.config)
        self.assertEqual([], effects.recoveries)
        self.assertEqual(0, state["recovery"]["attempts"])
        self.assertEqual("revalidation_became_healthy", result["recovery"]["decision"])

    def test_post_mail_restart_revalidation_pid_change_skips_command(self):
        effects = FakeEffects([not_ready(1600, pid=123), not_ready(1700, pid=124)])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        result = self.monitor(effects).check_once(state, self.config)
        self.assertEqual([], effects.recoveries)
        self.assertEqual(0, state["recovery"]["attempts"])
        self.assertEqual("revalidation_restart_pid_changed", result["recovery"]["decision"])

    def test_post_mail_restart_same_identity_executes(self):
        effects = FakeEffects([not_ready(1600, pid=123), not_ready(1700, pid=123), up()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        self.monitor(effects).check_once(state, self.config)
        self.assertEqual(["restart"], effects.recoveries)
        first_mail = effects.events.index("mail")
        second_status = effects.events.index("status", effects.events.index("status") + 1)
        self.assertLess(first_mail, second_status)
        self.assertLess(second_status, effects.events.index("recover:restart"))

    def test_current_attempt_mail_is_durable_and_prioritized(self):
        effects = FakeEffects([stopped(), stopped(), up()])
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        health.enqueue_notice(state, "old-1", "incident_confirmed", "old one", "body", self.clock.now)
        health.enqueue_notice(state, "old-2", "incident_confirmed", "old two", "body", self.clock.now)
        def observe(subject, body):
            self.assertTrue(any(
                any(item["event"] == "recovery_attempted" for item in snapshot["outbox"])
                for snapshot in self.persisted))
        effects.mail_observer = observe
        self.monitor(effects).check_once(state, self.config)
        self.assertTrue(effects.mail_calls[0][0].startswith("CYF API recovery attempt selected"))
        self.assertEqual(["start"], effects.recoveries)

    def test_full_outbox_preserves_failed_priority_recovery_notice(self):
        effects = FakeEffects([stopped(), stopped(), up()])
        effects.mail_results = [(False, "helper_failed")]
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        for number in range(health.MAX_OUTBOX):
            health.enqueue_notice(
                state, "old-%d" % number, "recovery_result",
                "old recovery result", "old body", self.clock.now)

        def observe(subject, body):
            if subject.startswith("CYF API recovery attempt selected"):
                durable = self.persisted[-1]["outbox"]
                self.assertTrue(any(item["event"] == "digest" for item in durable))
                self.assertTrue(any(item["event"] == "recovery_attempted"
                                    for item in durable))
        effects.mail_observer = observe
        self.monitor(effects).check_once(state, self.config)

        self.assertEqual(["start"], effects.recoveries)
        self.assertTrue(effects.mail_calls[0][0].startswith(
            "CYF API recovery attempt selected"))
        current = [item for item in state["outbox"]
                   if item["event"] == "recovery_attempted"]
        self.assertEqual(1, len(current))
        self.assertIn("action=start attempt=1", current[0]["body"])
        self.assertEqual(1, current[0]["attempts"])
        self.assertGreater(current[0]["next_attempt_at"], self.clock.now)
        self.assertEqual("helper_failed", current[0]["last_error"])
        self.assertTrue(any(subject == "CYF health monitor pending event digest"
                            for subject, _ in effects.mail_calls[1:]))
        self.assertLessEqual(len(state["outbox"]), health.MAX_OUTBOX)

    def test_resource_deferred_notice_persisted_before_delivery(self):
        effects = FakeEffects([stopped()])
        effects.resource_result = {"healthy": False,
                                   "classification": "resources_below_canonical_minimum"}
        state = health.initial_state(self.clock.now)
        state["component_streaks"]["local_api"] = 2
        def observe(subject, body):
            if subject == "CYF API recovery deferred by resources":
                self.assertTrue(any(
                    any(item["event"] == "recovery_deferred" for item in snapshot["outbox"])
                    for snapshot in self.persisted))
        effects.mail_observer = observe
        self.monitor(effects).check_once(state, self.config)
        self.assertTrue(any(subject == "CYF API recovery deferred by resources"
                            for subject, _ in effects.mail_calls))

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

    def test_pause_resume_marker_and_directory_fsync(self):
        self.store.write(health.initial_state(10))
        with mock.patch.object(health.os, "fsync", wraps=health.os.fsync) as fsync:
            self.store.pause(10)
        self.assertGreaterEqual(fsync.call_count, 2)
        self.assertTrue(self.store.maintenance())
        self.store.resume()
        self.assertFalse(self.store.maintenance())


class TrustedExecutableTests(unittest.TestCase):
    def setUp(self):
        self.root = tempfile.mkdtemp(prefix="cyf-health-exec-")
        self.target = os.path.join(self.root, "python-real")
        self.link = os.path.join(self.root, "python3")
        with open(self.target, "w") as stream:
            stream.write("#!/bin/sh\n")
        os.chmod(self.target, 0o755)
        os.symlink("python-real", self.link)

    def tearDown(self):
        shutil.rmtree(self.root)

    def test_root_owned_safe_python_symlink_chain_allowed(self):
        resolved = health.validate_trusted_executable(
            self.link, expected_uid=os.getuid(), validate_parents=False)
        self.assertEqual(self.target, resolved)

    def test_python_symlink_writable_final_executable_rejected(self):
        os.chmod(self.target, 0o775)
        with self.assertRaises(health.MonitorError):
            health.validate_trusted_executable(
                self.link, expected_uid=os.getuid(), validate_parents=False)


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

    def test_public_api_allows_exact_empty_401_boundary(self):
        effects = health.Effects()
        effects._http = lambda url: (401, "", b"", "completed")
        result = effects.public_api()
        self.assertTrue(result["healthy"])
        self.assertEqual("auth_boundary_empty_401", result["classification"])

    def test_public_api_rejects_html_403_502_and_spa_200(self):
        effects = health.Effects()
        for response in ((403, "text/html", b"nginx forbidden", "completed"),
                         (502, "text/html", b"bad gateway", "completed"),
                         (200, "text/html", b'<div id="app"></div>', "completed")):
            effects._http = lambda url, value=response: value
            self.assertFalse(effects.public_api()["healthy"])

    def test_public_api_accepts_json_auth_denial(self):
        effects = health.Effects()
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
        self.assertIn("validate_trusted_executable(MAIL_PYTHON", source)
        self.assertNotIn("shell=True", source)
        self.assertNotIn("/home/isp/bin", source)

    def test_guard_logging_uses_fixed_sanitized_syslog_command(self):
        captured = []
        validated = []
        self.assertTrue(health.guard_log(
            "unsafe\npayload", validator=lambda *args: validated.append(args),
            executor=lambda argv: captured.append(argv)))
        self.assertEqual(health.LOGGER, validated[0][0])
        self.assertEqual([health.LOGGER, "-p", "daemon.err", "-t", "cyf-juyiting-health",
                          "fail_closed reason=unsafe_payload"], captured[0])

    def test_installer_trust_and_activation_contract(self):
        path = os.path.join(HERE, "install.sh")
        with open(path, "r") as stream:
            text = stream.read()
        self.assertIn("stat.S_ISLNK", text)
        self.assertIn("info.st_uid != 0 or info.st_gid != 0", text)
        self.assertIn("stat.S_IMODE(info.st_mode) & 0o022", text)
        self.assertIn("info.st_nlink != 1", text)
        monitor_digest = health.sha256_file(MODULE_PATH)
        self.assertIn("CANDIDATE_MONITOR_SHA=" + monitor_digest, text)
        self.assertIn("installed monitor is not the reviewed candidate", text)
        self.assertIn("755:0:0:1", text)

    def test_cron_syntax_contract(self):
        path = os.path.join(HERE, "cyf-juyiting-health.cron")
        with open(path, "r") as stream:
            text = stream.read()
        command = "* * * * * root /usr/bin/python3 -I /usr/local/libexec/cyf-juyiting-health.py --check-once"
        self.assertIn(command, text)
        self.assertNotIn("systemd-run", text)
        self.assertNotIn("curl", text)
        with open(MODULE_PATH, "r") as stream:
            source = stream.read()
        self.assertEqual(2, source.count("guard_log(reason)"))


if __name__ == "__main__":
    unittest.main()
