#!/usr/bin/env python3
"""Isolated real-MinIO protocol probe; does not prove the Java adapter or SQL quota."""
import argparse
import concurrent.futures
import datetime
import hashlib
import http.client
import io
import json
from pathlib import Path
import socket
import time
from urllib.parse import urlsplit
import uuid

from minio import Minio


def response_headers(stream):
    line = stream.readline(8192)
    if not line.startswith(b"HTTP/"):
        raise RuntimeError("Missing HTTP response status")
    status = int(line.split(b" ", 2)[1])
    headers = {}
    for _ in range(100):
        line = stream.readline(8192)
        if line in (b"\r\n", b"\n"):
            return status, headers
        name, value = line.decode("latin-1").split(":", 1)
        headers[name.lower()] = value.strip()
    raise RuntimeError("Too many response headers")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--credentials", required=True)
    parser.add_argument("--endpoint", default="127.0.0.1:19000")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    credentials = json.loads(Path(args.credentials).read_text())
    client = Minio(args.endpoint, access_key=credentials["access_key"],
                   secret_key=credentials["secret_key"], secure=False,
                   region="us-east-1")
    bucket = "cyf-od02-fence-probe-" + uuid.uuid4().hex[:16]
    client.make_bucket(bucket)
    report = {"kind": "real_minio_protocol_probe", "bucket": bucket,
              "started_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "limitations": ["Python protocol probe, not production Java adapter",
                              "No SQL quota, HTTP application auth, scan or READY proof",
                              "Isolated zero-byte tombstones retained after probe"],
              "checks": []}
    data = b"cyf-storage-fence-probe\n" * 48000

    def signed(key):
        return client.get_presigned_url("PUT", bucket, key,
                                        expires=datetime.timedelta(minutes=5))

    def conditional_put(url, body):
        parsed = urlsplit(url)
        conn = http.client.HTTPConnection(parsed.hostname, parsed.port, timeout=20)
        try:
            conn.request("PUT", parsed.path + "?" + parsed.query, body=body,
                         headers={"If-None-Match": "*",
                                  "Content-Type": "application/octet-stream"})
            response = conn.getresponse()
            status = response.status
            response.read()
            return status
        finally:
            conn.close()

    def tombstone(key, token):
        client.put_object(bucket, key, io.BytesIO(b""), 0,
                          content_type="application/x-cyf-output-tombstone",
                          metadata={"cleanup-token": token})
        head = client.stat_object(bucket, key)
        observed = {k.lower(): v for k, v in head.metadata.items()}
        assert head.size == 0, "Tombstone length mismatch"
        assert observed.get("x-amz-meta-cleanup-token") == token, "Tombstone identity mismatch"

    try:
        versioning = client.get_bucket_versioning(bucket)
        assert versioning.status is None, "Fresh bucket unexpectedly has versioning"
        report["versioning"] = "never_enabled"

        # Obtain 100 Continue from the actual MinIO server before installing a marker.
        # This avoids mistaking SDK signing/pre-reading for an in-flight request.
        key = "slow-epoch"
        token = hashlib.sha256((bucket + "/" + key).encode()).hexdigest()
        url = signed(key)
        parsed = urlsplit(url)
        sock = socket.create_connection((parsed.hostname, parsed.port), timeout=20)
        stream = sock.makefile("rb")
        try:
            request = ("PUT " + parsed.path + "?" + parsed.query + " HTTP/1.1\r\n"
                       "Host: " + parsed.netloc + "\r\n"
                       "Content-Length: " + str(len(data)) + "\r\n"
                       "Content-Type: application/octet-stream\r\n"
                       "If-None-Match: *\r\nExpect: 100-continue\r\n"
                       "Connection: close\r\n\r\n")
            sock.sendall(request.encode("ascii"))
            interim, _ = response_headers(stream)
            assert interim == 100, "MinIO did not accept the streaming PUT body"
            sock.sendall(data[:65536])
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                marker = pool.submit(tombstone, key, token)
                marker_before_resume = False
                try:
                    marker.result(timeout=2)
                    marker_before_resume = True
                except concurrent.futures.TimeoutError:
                    pass
                sock.sendall(data[65536:])
                status, _ = response_headers(stream)
                stream.read()
                marker.result(timeout=20)
            assert status in (200, 409, 412), "Unexpected in-flight PUT result"
            if marker_before_resume:
                assert status in (409, 412), "Late PUT replaced an installed tombstone"
            head = client.stat_object(bucket, key)
            assert head.size == 0, "In-flight PUT recreated nonzero data"
            assert head.metadata.get("x-amz-meta-cleanup-token") == token
            report["checks"].append({"name": "in_flight_create_only_vs_tombstone",
                                     "server_100_continue_observed": True,
                                     "bytes_sent_before_marker": 65536,
                                     "marker_completed_before_body_resumed": marker_before_resume,
                                     "old_put_status": status, "result": "PASS"})
        finally:
            stream.close()
            sock.close()

        status = conditional_put(url, data)
        assert status in (409, 412), "Old signed PUT recreated cleaned bytes"
        report["checks"].append({"name": "replay_old_signed_put_after_fence",
                                 "status": status, "result": "PASS"})

        key = "old-put-wins-first"
        token = hashlib.sha256((bucket + "/" + key).encode()).hexdigest()
        assert conditional_put(signed(key), data) == 200
        assert client.stat_object(bucket, key).size == len(data)
        tombstone(key, token)
        # Repeating after an uncertain acknowledgement must preserve the same marker.
        tombstone(key, token)
        assert conditional_put(signed(key), data) in (409, 412)
        report["checks"].append({"name": "completed_put_then_idempotent_tombstone",
                                 "result": "PASS"})
        report["result"] = "PASS"
    except BaseException as error:
        report["result"] = "FAIL"
        # Never serialize network exception strings: they may include signed URLs.
        report["error_type"] = type(error).__name__
        raise
    finally:
        report["finished_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(report, indent=2) + "\n")
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    try:
        main()
    except BaseException as error:
        print("Probe failed; redacted exception class: " + type(error).__name__)
        raise SystemExit(1)
