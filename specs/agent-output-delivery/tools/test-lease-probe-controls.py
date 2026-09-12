#!/usr/bin/env python3
"""Synthetic controls for the lease probe. Never contacts any CYF service."""
import importlib.util
import io
import json
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("lease_probe", Path(__file__).with_name("smoke-output-lease.py"))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class FakeTransport:
    def __init__(self, fault=None):
        self.calls = []
        self.receipts = {}
        self.fault = fault
        self.state = {"workItemId": "work-example", "status": "ready", "version": "9007199254740993"}

    def request(self, method, path, body=None, key=None):
        self.calls.append((method, path, dict(body) if body else body, key))
        if method == "GET":
            value = dict(self.state)
            if self.fault == "wrong-initial-item":
                value["workItemId"] = "other-work"
            return value
        action = path.rsplit("/", 1)[1]
        if key in self.receipts:
            prior_body, value = self.receipts[key]
            assert body == prior_body
            if self.fault == "changed-receipt":
                value = {**value, "version": str(int(value["version"]) + 1)}
            return dict(value)
        assert body["expectedVersion"] == self.state["version"]
        if action != "claim":
            assert body["leaseToken"] == self.state["leaseToken"]
        value = {"workItemId": "work-example", "status": {
            "claim": "claimed", "start": "running", "heartbeat": "running", "release": "ready"
        }[action], "version": str(int(self.state["version"]) + 1)}
        if action != "release":
            value["leaseToken"] = "SYNTHETIC-LEASE-TOKEN-NOT-FOR-REPORTS"
            value["leaseUntil"] = (str(int(self.state["leaseUntil"]) + 1000)
                                   if action == "heartbeat" else "1789239999000")
        if self.fault == "missing-active-token":
            value.pop("leaseToken", None)
        elif self.fault == "wrong-result-item":
            value["workItemId"] = "other-work"
        elif self.fault == "numeric-version":
            value["version"] = int(value["version"])
        elif self.fault == "retained-release-token" and action == "release":
            value["leaseToken"] = self.state["leaseToken"]
        elif self.fault == "backward-version":
            value["version"] = str(int(self.state["version"]) - 1)
        elif self.fault == "unchanged-version":
            value["version"] = self.state["version"]
        elif self.fault == "missing-active-expiry":
            value.pop("leaseUntil", None)
        elif self.fault == "duplicate-version-step":
            value["version"] = str(int(self.state["version"]) + 2)
        elif self.fault == "unchanged-heartbeat-expiry" and action == "heartbeat":
            value["leaseUntil"] = self.state["leaseUntil"]
        self.state = value
        self.receipts[key] = (dict(body), dict(value))
        return dict(value)


class LeaseProbeControls(unittest.TestCase):
    def run_fixture(self, transport):
        return probe.run_probe(transport.request, "task-example", "work-example", "2" * 32)

    def test_lifecycle_uses_returned_exact_versions_and_receipts(self):
        transport = FakeTransport()
        result = self.run_fixture(transport)
        self.assertEqual(result["finalVersion"], "9007199254740997")
        self.assertEqual(result["finalState"], "ready")
        self.assertEqual(len(transport.calls), 9)
        self.assertEqual(len(transport.receipts), 4)
        for index in (1, 3, 5, 7):
            self.assertEqual(transport.calls[index], transport.calls[index + 1])
        self.assertNotIn("leaseToken", result)
        self.assertNotIn("SYNTHETIC-LEASE", str(result))

    def test_invalid_or_changed_results_stop_the_sequence(self):
        for fault in ("wrong-initial-item", "changed-receipt", "missing-active-token",
                      "wrong-result-item", "numeric-version", "backward-version",
                      "retained-release-token", "unchanged-version", "missing-active-expiry",
                      "duplicate-version-step", "unchanged-heartbeat-expiry"):
            with self.subTest(fault=fault), self.assertRaises(probe.ProbeFailure):
                self.run_fixture(FakeTransport(fault))

    def test_non_ready_work_item_is_not_mutated(self):
        transport = FakeTransport()
        transport.state["status"] = "running"
        with self.assertRaises(probe.ProbeFailure):
            self.run_fixture(transport)
        self.assertEqual([call[0] for call in transport.calls], ["GET"])

    def test_failure_does_not_guess_a_new_version_or_release(self):
        transport = FakeTransport()

        def interrupted(method, path, body=None, key=None):
            if path.endswith("/start"):
                raise probe.ProbeFailure("Injected409")
            return transport.request(method, path, body, key)

        with self.assertRaises(probe.ProbeFailure):
            probe.run_probe(interrupted, "task-example", "work-example", "2" * 32)
        self.assertEqual(len(transport.calls), 3)
        self.assertFalse(any(call[1].endswith("/release") for call in transport.calls))

    def test_origins_and_identifiers_fail_before_a_request(self):
        for value in ("https://example.com", "http://localhost:10018", "http://127.0.0.1:10019",
                      "http://user:secret@127.0.0.1:10018", "http://@127.0.0.1:10018",
                      "http://127.0.0.1:10018/path",
                      "http://127.0.0.1:10018/?token=example", "http://127.0.0.1:10018/#x"):
            with self.subTest(origin=value), self.assertRaises(probe.ProbeFailure):
                probe.origin(value)
        self.assertEqual(probe.origin("http://127.0.0.1:10018/"), "http://127.0.0.1:10018")
        transport = FakeTransport()
        with self.assertRaises(probe.ProbeFailure):
            probe.run_probe(transport.request, "task-example", "work-example", "invalid-run")
        self.assertEqual(transport.calls, [])
        for value in (".", "..", "a/b", "a\\b", "%2e%2e", "a" * 101, "a b", "a\u2003b"):
            with self.subTest(identifier=value), self.assertRaises(probe.ProbeFailure):
                probe.run_probe(transport.request, value, "work-example", "2" * 32)
            self.assertEqual(transport.calls, [])

    def test_first_claim_timeout_is_an_unknown_mutation(self):
        observations = []
        transport = probe.Transport("http://127.0.0.1:10018", "synthetic-bearer", observations)

        class TimeoutOpener:
            def open(self, request, timeout):
                raise TimeoutError("Synthetic transport timeout")

        transport.opener = TimeoutOpener()
        with self.assertRaises(TimeoutError):
            transport.request("POST", "/agent/tasks/task-example/work-items/work-example/lease/claim",
                              {"runId": "2" * 32, "expectedVersion": "0", "leaseDurationMillis": "120000"},
                              "synthetic-timeout-key")
        self.assertTrue(any(row["method"] == "POST" for row in observations))
        self.assertFalse(observations[0]["responseReceived"])

    def test_transport_schema_bounds_and_redaction(self):
        secret = "SYNTHETIC-SECRET-NEVER-IN-OBSERVATIONS"
        data = {"code": "E0", "data": {"workItemId": "work-example", "status": "claimed",
                "version": "1", "leaseToken": secret, "leaseUntil": "1789239999000"}}

        class Response(io.BytesIO):
            status = 200

        class Opener:
            def __init__(self, raw, status=200):
                self.raw, self.status = raw, status

            def open(self, request, timeout):
                value = Response(self.raw)
                value.status = self.status
                return value

        for raw, status, success in ((json.dumps(data).encode(), 200, True),
                                     (json.dumps(data).encode(), 409, False),
                                     (b'{"code":"E0","data":{}}', 200, False),
                                     (b'{"code":"E0","code":"E0","data":{}}', 200, False),
                                     (b'x' * 65537, 200, False)):
            with self.subTest(status=status, success=success, size=len(raw)):
                observations = []
                transport = probe.Transport("http://127.0.0.1:10018", secret, observations)
                transport.opener = Opener(raw, status)
                if success:
                    self.assertEqual(transport.request("GET", "/example")["leaseToken"], secret)
                else:
                    with self.assertRaises(probe.ProbeFailure):
                        transport.request("GET", "/example")
                self.assertNotIn(secret, json.dumps(observations))
                self.assertEqual(len(observations), 1)


if __name__ == "__main__":
    unittest.main()
