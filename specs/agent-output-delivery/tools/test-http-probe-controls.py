#!/usr/bin/env python3
"""Synthetic controls for the probe itself; these never exercise the CYF API."""
import contextlib
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("probe", Path(__file__).with_name("smoke-output-http.py"))
probe = importlib.util.module_from_spec(spec)
spec.loader.exec_module(probe)


class Response(io.BytesIO):
    def __init__(self, body, status=200, binary=False):
        super().__init__(body if binary else json.dumps({"code": "E0", "data": body}).encode())
        self.status = status
        self.headers = {"Content-Type": "application/octet-stream" if binary else "application/json",
                        "Cache-Control": "private, no-store", "Content-Disposition": "attachment; filename=report.md",
                        "X-Content-Type-Options": "nosniff"}


class Transport:
    def __init__(self, source_type, fault=None):
        self.source = {"type": source_type, "id": "source-test"}
        self.fault = fault
        self.completes = 0
        self.calls = []

    def open(self, request, timeout):
        self.calls.append(request)
        path = probe.urlsplit(request.full_url).path
        if path.endswith("/download"):
            response = Response(b"wrong" if self.fault == "bytes" else b"hello world!\n", binary=True)
        elif "/output-uploads" in path:
            state, status = "CREATED", 200
            if path.endswith("/content"):
                state = "UPLOADING"
            elif path.endswith("/complete"):
                self.completes += 1
                state, status = "VERIFYING", 202
                if self.fault == "replay_status" and self.completes > 1:
                    status = 200
            elif request.method == "GET":
                state = "READY"
            response = Response({"uploadId": "upload-test", "state": state, "expiresAt": "1800000000000",
                                 "objectId": "object-test"}, status)
        else:
            item = {"source": self.source, "outputId": "output-test", "version": "1", "title": "Synthetic",
                    "createdAt": "1800000000000", "state": "AVAILABLE", "previewKind": "TEXT", "canDownload": True,
                    "publicationKind": "OWNER_SHARE" if self.source["type"] == "TASK" else "CONVERSATION_OUTPUT",
                    "size": "13", "mime": "text/markdown", "sha256": hashlib.sha256(b"hello world!\n").hexdigest()}
            if self.fault == "metadata":
                item["size"] = "14"
            response = Response(item if request.method == "POST" else {"item": item})
        if self.fault == "cache":
            response.headers.pop("Cache-Control")
        return response


class Controls(unittest.TestCase):
    def run_case(self, source_type="TASK", fault=None, read_only=False, base="http://127.0.0.1:18080"):
        transport = Transport(source_type, fault)
        args = ["probe", "--base-url", base, "--source-type", source_type, "--source-id", "source-test",
                "--output-id", "output-test"] + (["--read-only"] if read_only else ["--run-id", "run-test"])
        captured = io.StringIO()
        with patch("sys.argv", args), patch.dict("os.environ", {"OUTPUT_SMOKE_USER_TOKEN": "synthetic-user-secret",
                "OUTPUT_SMOKE_RUN_TICKET": "synthetic-run-secret"}), patch.object(probe, "build_opener", return_value=transport), contextlib.redirect_stdout(captured):
            result = probe.main()
        self.assertNotIn("synthetic-user-secret", captured.getvalue())
        self.assertNotIn("synthetic-run-secret", captured.getvalue())
        return result, transport

    def test_publish_both_sources_and_read_only(self):
        for kind, readonly in [("TASK", False), ("CONVERSATION", False), ("TASK", True)]:
            with self.subTest(kind=kind, readonly=readonly):
                result, transport = self.run_case(kind, read_only=readonly)
                self.assertEqual(0, result)
                if readonly:
                    self.assertTrue(all(r.method == "GET" for r in transport.calls))

    def test_status_bytes_metadata_and_cache_faults_fail(self):
        for fault in ("replay_status", "bytes", "metadata", "cache"):
            with self.subTest(fault=fault):
                self.assertEqual(1, self.run_case(fault=fault)[0])

    def test_path_prefix_and_remote_origin_fail_before_transport(self):
        for origin in ("http://127.0.0.1/api", "https://192.0.2.1"):
            with self.subTest(origin=origin), self.assertRaises(probe.ProbeFailure):
                self.run_case(base=origin)


if __name__ == "__main__":
    unittest.main()
