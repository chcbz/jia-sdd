#!/usr/bin/env python3
"""Development-only live output probe; never prints credentials or response bodies.

Requires an already authenticated, active server-created run, OUTPUT_SMOKE_RUN_TICKET
and OUTPUT_SMOKE_USER_TOKEN in the environment. --read-only needs only the user token
and an existing --output-id; use it after independently stopping the Agent to collect
offline-retrieval evidence. This tool does not stop an Agent or prove client/UI flows.
Only numeric loopback HTTP(S) origins are accepted, and redirects are never followed.
Requires PyYAML and jsonschema >= 4. Writes a small synthetic file in publish mode.
"""
import argparse
import hashlib
import ipaddress
import json
import os
from pathlib import Path
import re
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlsplit
from urllib.request import HTTPRedirectHandler, ProxyHandler, Request, build_opener
import uuid

from jsonschema import Draft202012Validator
import yaml


class ProbeFailure(Exception):
    pass


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def require(condition, message):
    if not condition:
        raise ProbeFailure(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--source-type", choices=["TASK", "CONVERSATION"], required=True)
    parser.add_argument("--source-id", required=True)
    parser.add_argument("--run-id")
    parser.add_argument("--output-id")
    parser.add_argument("--read-only", action="store_true")
    args = parser.parse_args()
    origin = urlsplit(args.base_url)
    require(origin.scheme in ("http", "https") and origin.hostname is not None
            and origin.username is None and origin.password is None
            and origin.path in ("", "/") and not origin.query and not origin.fragment,
            "An origin without a path prefix is required")
    require(ipaddress.ip_address(origin.hostname).is_loopback, "Only numeric loopback origins are allowed")
    require(args.source_id and args.source_id == args.source_id.strip(), "Exact source ID required")
    require(not args.read_only or args.output_id is not None, "Read-only mode needs an existing output ID")
    require(args.read_only or args.run_id is not None, "Publication needs a trusted run ID")
    owner = os.environ.get("OUTPUT_SMOKE_USER_TOKEN", "")
    ticket = os.environ.get("OUTPUT_SMOKE_RUN_TICKET", "")
    require(bool(owner) and (args.read_only or bool(ticket)), "Required credentials missing from environment")
    base = args.base_url.rstrip("/")
    spec_root = Path(__file__).resolve().parents[1]
    contract_raw = (spec_root / "openapi.yaml").read_bytes()
    contract = yaml.safe_load(contract_raw)
    operations = {}
    for template, methods in contract["paths"].items():
        pattern = "".join("[^/]+" if piece.startswith("{") else re.escape(piece)
                          for piece in re.split(r"(\{[^{}]+\})", template))
        for method, operation in methods.items():
            if isinstance(operation, dict) and "operationId" in operation:
                require(operation["operationId"] not in operations, "Duplicate operation ID")
                operations[operation["operationId"]] = (method.upper(), pattern, operation)
    fixture = json.loads((spec_root / "fixtures.json").read_text())["sampleFile"]
    payload = fixture["utf8"].encode("utf-8")
    expected_hash = hashlib.sha256(payload).hexdigest()
    require(expected_hash == fixture["sha256"] and str(len(payload)) == fixture["byteLength"],
            "Frozen fixture hash/size mismatch")
    opener = build_opener(ProxyHandler({}), NoRedirect())
    observations = []

    def request(operation, method, path, token, body=None, key=None, binary=False):
        expected_method, pattern, operation_schema = operations[operation]
        require(method == expected_method and re.fullmatch(pattern, path) is not None,
                "Probe method/path does not match the frozen operation")
        headers = {"Authorization": "Bearer " + token, "Accept": "application/json"}
        if key:
            headers["Idempotency-Key"] = key
        if body is not None:
            headers["Content-Type"] = "application/octet-stream" if isinstance(body, bytes) else "application/json"
            data = body if isinstance(body, bytes) else json.dumps(body).encode()
        else:
            data = None
        req = Request(base + path, data=data, headers=headers, method=method)
        try:
            response = opener.open(req, timeout=15)
        except HTTPError as error:
            response = error
        with response:
            status = response.status
            # This probe handles only the tiny synthetic file and bounded JSON.
            raw = response.read(1024 * 1024 + 1)
            require(len(raw) <= 1024 * 1024, "Probe response exceeded one MiB")
            observations.append({"operationId": operation, "httpStatus": status,
                                 "responseSha256": hashlib.sha256(raw).hexdigest()})
            if binary and status == 200:
                require(response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
                        == "application/octet-stream", "Download media type differs from the contract")
                require(response.headers.get("Cache-Control", "").lower() == "private, no-store",
                        "Download Cache-Control mismatch")
                require(response.headers.get("Content-Disposition", "").lower().startswith("attachment;"),
                        "Download must be an attachment")
                require(response.headers.get("X-Content-Type-Options", "").lower() == "nosniff",
                        "Download must disable MIME sniffing")
                require(raw == payload, "Downloaded bytes differ from frozen fixture")
                return raw
            require(response.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
                    == "application/json", "Expected JSON response media type")
            require("no-store" in {part.strip().lower() for part in response.headers.get("Cache-Control", "").split(",")},
                    "JSON response must disable caching")
            schema = operation_schema["responses"].get(str(status), {}).get("content", {}).get("application/json")
            require(schema is not None, "Undocumented JSON status")
            envelope = json.loads(raw)
            validator = Draft202012Validator(dict(schema["schema"], components=contract["components"]))
            require(validator.is_valid(envelope), "Response violates frozen JSON schema")
            require(status in (200, 202), "HTTP operation failed; response body withheld")
            return envelope["data"], raw

    output_id = args.output_id or uuid.uuid4().hex
    source = {"type": args.source_type, "id": args.source_id}
    sid, oid = quote(args.source_id, safe=""), quote(output_id, safe="")
    task = args.source_type == "TASK"
    prefix = f"/agent/tasks/{sid}/artifacts" if task else f"/chat/conversations/{sid}/outputs"
    kind = "Task" if task else "Chat"
    try:
        if not args.read_only:
            create_body = {"runId": args.run_id, "source": source, "name": fixture["name"],
                           "size": str(len(payload)), "sha256": expected_hash, "mime": "text/markdown"}
            create_key = "probe-create-" + uuid.uuid4().hex
            created, create_raw = request("createUpload", "POST", "/agent/output-uploads", ticket,
                                          create_body, create_key)
            create_status = observations[-1]["httpStatus"]
            _, replay = request("createUpload", "POST", "/agent/output-uploads", ticket, create_body, create_key)
            require(create_raw == replay and observations[-1]["httpStatus"] == create_status,
                    "Create did not replay its original status and response bytes")
            uid = quote(created["uploadId"], safe="")
            upload_path = f"/agent/output-uploads/{uid}"
            request("putUploadBytes", "PUT", upload_path + "/content", ticket, payload)
            complete_key = "probe-complete-" + uuid.uuid4().hex
            _, complete_raw = request("completeUpload", "POST", upload_path + "/complete", ticket, key=complete_key)
            complete_status = observations[-1]["httpStatus"]
            deadline = time.monotonic() + 60
            while True:
                current, _ = request("getUpload", "GET", upload_path, ticket)
                if current["state"] == "READY":
                    break
                require(current["state"] == "VERIFYING" and time.monotonic() < deadline,
                        "Upload did not reach READY within the probe deadline")
                time.sleep(1)
            _, replay = request("completeUpload", "POST", upload_path + "/complete", ticket, key=complete_key)
            require(complete_raw == replay and observations[-1]["httpStatus"] == complete_status,
                    "Complete did not replay its original status and response bytes")
            body = {"runId": args.run_id, "expectedPreviousVersion": "0", "title": "Output delivery probe",
                    "artifactType": "analysis", "objectId": current["objectId"]}
            if task:
                body.update(artifactId=output_id, artifactVersion="1", publishToOwner=True)
            else:
                body.update(outputId=output_id, version="1")
            publish_key = "probe-publish-" + uuid.uuid4().hex
            published, original = request("publish" + kind + "Output", "POST", prefix, ticket, body, publish_key)
            require(published["outputId"] == output_id and published["version"] == "1",
                    "Publication returned a different output version")
            _, replay = request("publish" + kind + "Output", "POST", prefix, ticket, body, publish_key)
            require(original == replay, "Publication did not replay its original response bytes")
        detail_path = prefix + f"/{oid}/versions/1"
        detail, _ = request("get" + kind + "OutputVersion", "GET", detail_path, owner)
        item = detail["item"]
        require(item["outputId"] == output_id and item["version"] == "1" and item["source"] == source,
                "Owner received a different source/output/version")
        require(item["canDownload"] and item["state"] == "AVAILABLE", "Output is not downloadable")
        require(item.get("sha256") == expected_hash and item.get("size") == str(len(payload))
                and item.get("mime") == "text/markdown", "Published file metadata differs from the fixture")
        require(item["publicationKind"] == ("OWNER_SHARE" if task else "CONVERSATION_OUTPUT"),
                "Output lacks the expected explicit owner publication")
        request("download" + kind + "OutputVersion", "GET", detail_path + "/download", owner, binary=True)
        print(json.dumps({"passed": True, "mode": "read_only" if args.read_only else "publish_and_read",
                          "outputId": output_id, "version": "1", "byteLength": len(payload),
                          "sha256": expected_hash, "contractSha256": hashlib.sha256(contract_raw).hexdigest(),
                          "observations": observations,
                          "limit": "Synthetic live HTTP only; Agent offline state, ACL/conflict negatives, pagination and UI require separate evidence."},
                         indent=2))
        return 0
    except (ProbeFailure, URLError, ValueError, KeyError, TimeoutError, OSError):
        print(json.dumps({"passed": False, "completedObservations": observations,
                          "error": "Probe failed; response values and credentials withheld."}, indent=2))
        return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ProbeFailure, ValueError, KeyError, OSError):
        print("Probe setup failed; input values and credentials withheld.", file=sys.stderr)
        sys.exit(2)
