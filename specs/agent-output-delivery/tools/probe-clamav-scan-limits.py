#!/usr/bin/env python3
"""Check local ClamAV archive scan limits with the standard EICAR test string."""
import argparse
import datetime
import hashlib
import io
import json
from pathlib import Path
import socket
import struct
import time
import zipfile

EICAR = b"X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"


def archive(member_mib):
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as package:
        block = bytes(1024 * 1024)
        for index, size in enumerate(member_mib):
            with package.open("padding" + str(index) + ".bin", "w") as entry:
                for _ in range(size):
                    entry.write(block)
    return output.getvalue()


def scan(host, port, content, timeout):
    with socket.create_connection((host, port), timeout=5) as connection:
        connection.settimeout(timeout)
        connection.sendall(b"zINSTREAM\0")
        for start in range(0, len(content), 65536):
            chunk = content[start:start + 65536]
            connection.sendall(struct.pack("!I", len(chunk)) + chunk)
        connection.sendall(struct.pack("!I", 0))
        response = bytearray()
        while len(response) < 1024:
            part = connection.recv(1024 - len(response))
            if not part:
                break
            response.extend(part)
            if b"\0" in part:
                break
        return response.split(b"\0", 1)[0].decode("utf-8", errors="strict")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=13310)
    parser.add_argument("--output", required=True)
    parser.add_argument("--timeout", type=float, default=180)
    args = parser.parse_args()
    report = {"observed_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              "kind": "clamav_scan_limit_probe", "checks": [],
              "timeout_seconds": args.timeout,
              "scope": "Real local ClamAV INSTREAM protocol; not application upload/READY evidence"}
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    def save():
        target.write_text(json.dumps(report, indent=2) + "\n")
    cases = [("clean", lambda: b"hello output\n", " OK"),
             ("eicar", lambda: EICAR, " FOUND"),
             ("member_61_mib", lambda: archive([61]), "Heuristics.Limits.Exceeded"),
             ("aggregate_110_mib", lambda: archive([55, 55]), "Heuristics.Limits.Exceeded")]
    report["result"] = "RUNNING"
    save()
    for name, make_content, expected in cases:
        item = {"case": name, "expected_response_contains": expected, "status": "RUNNING"}
        report["checks"].append(item)
        save()
        print("Scanning " + name, flush=True)
        started = time.monotonic()
        try:
            content = make_content()
            item.update({"input_bytes": len(content), "sha256": hashlib.sha256(content).hexdigest()})
            response = scan(args.host, args.port, content, args.timeout)
            item["response"] = response
            item["status"] = "PASS" if expected in response else "FAIL"
        except (OSError, UnicodeError) as error:
            item.update({"status": "INCONCLUSIVE", "error_type": type(error).__name__})
        item["elapsed_seconds"] = round(time.monotonic() - started, 3)
        save()
        print(json.dumps(item), flush=True)
    report["result"] = "PASS" if all(x["status"] == "PASS" for x in report["checks"]) else "NOT_PASSED"
    save()
    raise SystemExit(0 if report["result"] == "PASS" else 1)


if __name__ == "__main__":
    main()
