#!/usr/bin/env python3
"""Bounded OD07 development probe; never creates a task/run or runs a model.

Requires OUTPUT_SMOKE_RUN_TICKET and an existing trusted, ready policy1 work item
on the isolated API10018. Mutates that work item's lease and releases it. Only
numeric loopback10018 is allowed; no redirects/proxies. Reports contain hashes,
states and versions, never the bearer or returned leaseToken. This is not submit,
review, concurrency, runtime-restart or production acceptance.
"""
import argparse
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener
import uuid

from jsonschema import Draft202012Validator
import yaml


class ProbeFailure(Exception):
    pass


def require(condition, message):
    if not condition:
        raise ProbeFailure(message)


def origin(value):
    parsed = urlsplit(value)
    try:
        loopback = ipaddress.ip_address(parsed.hostname or "").is_loopback
        port = parsed.port
    except ValueError:
        raise ProbeFailure("Numeric loopback API10018 required") from None
    require(parsed.scheme == "http" and loopback and port == 10018
            and parsed.username is None and parsed.password is None
            and parsed.path in ("", "/") and not parsed.query and not parsed.fragment,
            "Only the isolated HTTP loopback API10018 origin is supported")
    return value.rstrip("/")


def identifier(value):
    require(isinstance(value, str) and 0 < len(value) <= 100
            and value == value.strip()
            and value not in (".", "..")
            and not any(c in value for c in ("/", "\\", "%"))
            and not any(ord(c) < 32 or ord(c) == 127 for c in value),
            "Exact nonempty identifier required")
    return value


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def sha(value):
    return hashlib.sha256(value).hexdigest()


def unique_object(pairs):
    value = {}
    for key, item in pairs:
        require(key not in value, "Duplicate JSON member in lease response")
        value[key] = item
    return value


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


class Transport:
    def __init__(self, base, bearer, observations):
        self.base = origin(base)
        require(isinstance(bearer, str) and bool(bearer) and not any(c.isspace() for c in bearer),
                "OUTPUT_SMOKE_RUN_TICKET is required")
        self.bearer = bearer
        self.observations = observations
        self.opener = build_opener(ProxyHandler({}), NoRedirect())
        contract = yaml.safe_load((Path(__file__).resolve().parents[1] / "openapi.yaml").read_text())
        self.validator = Draft202012Validator({
            "$ref": "#/components/schemas/LeaseResponse", "components": contract["components"]})

    def request(self, method, path, body=None, key=None):
        headers = {"Authorization": "Bearer " + self.bearer,
                   "Accept": "application/json", "Cache-Control": "no-store"}
        payload = None if body is None else canonical(body)
        if payload is not None:
            headers["Content-Type"] = "application/json"
        if key:
            headers["Idempotency-Key"] = key
        request = Request(self.base + path, data=payload, headers=headers, method=method)
        row = {"method": method, "path": path, "attempted": True,
               "requestSha256": sha(payload) if payload is not None else None,
               "responseReceived": False}
        # Once a POST enters transport, timeout can mean a committed unknown result.
        self.observations.append(row)
        try:
            response = self.opener.open(request, timeout=20)
        except HTTPError as error:
            response = error
        with response:
            row.update({"status": response.status, "responseReceived": True})
            raw = response.read(65537)
            row.update({"responseSha256": sha(raw), "responseBytes": len(raw)})
            require(len(raw) <= 65536, "Lease response exceeded64KiB")
            require(response.status == 200, "Lease request did not return HTTP200")
            try:
                parsed = json.loads(raw, object_pairs_hook=unique_object)
            except (ValueError, UnicodeError):
                raise ProbeFailure("Lease response was not JSON") from None
            require(not list(self.validator.iter_errors(parsed)), "Lease response schema mismatch")
            data = parsed["data"]
            row.update({"state": data["status"], "version": data["version"],
                        "workItemId": data["workItemId"], "hasLeaseToken": bool(data.get("leaseToken"))})
            return data


def run_probe(request, task_id, work_item_id, run_id):
    """Consumes actual response versions; injectable only for helper control tests."""
    task_id, work_item_id, run_id = map(identifier, (task_id, work_item_id, run_id))
    require(re.fullmatch(r"[a-f0-9]{32}", run_id) is not None, "Trusted32hex runId required")
    path = f"/agent/tasks/{quote(task_id, safe='')}/work-items/{quote(work_item_id, safe='')}/lease"

    def checked(value, states):
        require(isinstance(value, dict) and value.get("workItemId") == work_item_id,
                "Lease response refers to another work item")
        require(value.get("status") in states, "Unexpected lease lifecycle state")
        require(isinstance(value.get("version"), str)
                and re.fullmatch(r"0|[1-9][0-9]*", value["version"]) is not None,
                "Canonical string lease version required")
        return value

    current = checked(request("GET", path), {"ready"})
    require(not current.get("leaseToken"), "Ready work item unexpectedly has a lease")
    initial_version = current["version"]
    for action, states in (("claim", {"claimed"}), ("start", {"running"}),
                           ("heartbeat", {"running"}), ("release", {"ready", "failed"})):
        body = {"runId": run_id, "expectedVersion": current["version"]}
        if action != "claim":
            require(isinstance(current.get("leaseToken"), str) and bool(current["leaseToken"]),
                    "Active response omitted the lease token")
            body["leaseToken"] = current["leaseToken"]
        if action in ("claim", "heartbeat"):
            body["leaseDurationMillis"] = "120000"
        key = "od07-lease-" + uuid.uuid4().hex
        result = checked(request("POST", path + "/" + action, body, key), states)
        replay = checked(request("POST", path + "/" + action, body, key), states)
        require(result == replay, "Exact lease receipt replay changed the result")
        require(int(result["version"]) == int(current["version"]) + 1,
                "Lease mutation did not advance the version exactly once")
        if action != "release":
            require(isinstance(result.get("leaseToken"), str) and bool(result["leaseToken"]),
                    "Active lease token missing")
            require(isinstance(result.get("leaseUntil"), str)
                    and re.fullmatch(r"[1-9][0-9]{0,18}", result["leaseUntil"]) is not None,
                    "Active lease expiry missing or noncanonical")
        else:
            require(not result.get("leaseToken"), "Released response retained an active lease token")
        current = result
    return {"taskId": task_id, "workItemId": work_item_id, "runId": run_id,
            "initialVersion": initial_version, "finalVersion": current["version"],
            "finalState": current["status"], "exactReplays": 4}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", default="http://127.0.0.1:10018")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--work-item-id", required=True)
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-directory", required=True, type=Path)
    args = parser.parse_args()
    observations = []
    result = {"succeeded": False, "network": observations,
              "scope": "Lease HTTP lifecycle/exact receipts only; no model/submit/review/concurrency test"}
    transport = Transport(args.base_url, os.environ.get("OUTPUT_SMOKE_RUN_TICKET", ""), observations)
    args.output_directory.mkdir(mode=0o700, parents=True, exist_ok=False)
    try:
        result["lifecycle"] = run_probe(transport.request, args.task_id, args.work_item_id, args.run_id)
        result["succeeded"] = True
    except Exception as error:
        # HTTP/schema exceptions may carry credentialed bodies; never stringify them.
        result["failure"] = str(error) if isinstance(error, ProbeFailure) else type(error).__name__
        result["mayHaveActiveLease"] = any(row["method"] == "POST" for row in observations)
    report = args.output_directory / "observation.json"
    report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    report.chmod(0o600)
    print(json.dumps({"succeeded": result["succeeded"], "observation": str(report)}))
    return 0 if result["succeeded"] else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as error:
        print(json.dumps({"succeeded": False, "failure": type(error).__name__}))
        raise SystemExit(2)
