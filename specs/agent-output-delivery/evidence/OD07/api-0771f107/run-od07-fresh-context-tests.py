#!/usr/bin/env python3
import base64
import json
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path


credentials = json.loads(Path(
    "/home/chc/.local/share/cyf-output-tools/services/rabbitmq/state/credentials.json"
).read_text())
username = credentials["user"]
password = credentials["password"]
vhost = f"cyf_od07_fresh_{os.getpid()}_{time.time_ns()}"
base_url = "http://127.0.0.1:15674/api"
authorization = "Basic " + base64.b64encode(
    f"{username}:{password}".encode("utf-8")
).decode("ascii")


def request(method, path, body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        base_url + path,
        method=method,
        data=data,
        headers={
            "Authorization": authorization,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=10) as response:
        return response.status


encoded_vhost = urllib.parse.quote(vhost, safe="")
encoded_user = urllib.parse.quote(username, safe="")
created = False
try:
    request("PUT", f"/vhosts/{encoded_vhost}", {})
    created = True
    request("PUT", f"/permissions/{encoded_vhost}/{encoded_user}", {
        "configure": ".*",
        "write": ".*",
        "read": ".*",
    })
    environment = os.environ.copy()
    environment.update({
        "OD07_RABBIT_HOST": "127.0.0.1",
        "OD07_RABBIT_PORT": "15673",
        "OD07_RABBIT_VHOST": vhost,
        "OD07_RABBIT_USER": username,
        "OD07_RABBIT_PASSWORD": password,
        "OD07_RABBIT_FRESH_VHOST": "true",
    })
    command = [
        sys.executable,
        "/tmp/cyf-od02-evidence/run-gradle-with-od-env.py",
        *sys.argv[1:],
    ]
    log_path = os.environ.get("OD07_TEST_LOG")
    if log_path:
        with Path(log_path).open("w", encoding="utf-8") as log_file:
            process = subprocess.Popen(
                command,
                env=environment,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            assert process.stdout is not None
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                log_file.write(line)
                log_file.flush()
            return_code = process.wait()
    else:
        return_code = subprocess.run(
            command,
            env=environment,
            check=False,
        ).returncode
    raise SystemExit(return_code)
finally:
    if created:
        try:
            request("DELETE", f"/vhosts/{encoded_vhost}")
        except Exception as cleanup_failure:
            print("OD07 fresh-vhost cleanup failed: "
                  + cleanup_failure.__class__.__name__, file=sys.stderr)
