#!/usr/bin/env python3
import hashlib
import json
import urllib.error
import urllib.request
from pathlib import Path

BASE = "http://127.0.0.1:10018"
TASK_ID = "4"
RUN_ID = "4326fd3446e4469dbc1e0c3221846ce5"
QUEUE_ROOT = Path("/tmp/od06-synthetic-agent-r2/data/output-queue/6167745f6335383936316561663330393433613661663933306566653335306534353761")
token_doc = json.loads(Path("/tmp/od06-user-token-r1.json").read_text())
token = token_doc.get("access_token") or token_doc.get("token")
if not isinstance(token, str) or not token:
    raise SystemExit("access token unavailable")

def request(path, binary=False):
    req = urllib.request.Request(BASE + path, headers={"Authorization": "Bearer " + token})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            body = response.read()
            return response.status, dict(response.headers.items()), body if binary else json.loads(body)
    except urllib.error.HTTPError as error:
        body = error.read()
        try:
            parsed = json.loads(body)
        except Exception:
            parsed = {"bodyBytes": len(body)}
        return error.code, dict(error.headers.items()), parsed

queue = json.loads((QUEUE_ROOT / "queue" / f"{RUN_ID}.json").read_text())
result = {
    "taskId": TASK_ID,
    "runId": RUN_ID,
    "queueState": queue.get("state"),
    "queueRetryCount": queue.get("retryCount"),
    "terminalNotified": queue.get("terminalNotified"),
    "modelInvocationCount": len(Path("/tmp/od06-synthetic-codex-r3.invocations.log").read_text().splitlines()),
}
status, _, body = request(f"/agent/tasks/{TASK_ID}/artifacts?limit=20")
items = ((body.get("data") or {}).get("items") or []) if isinstance(body, dict) else []
result["list"] = {"status": status, "code": body.get("code"), "count": len(items), "items": []}
for item in items:
    oid = item["outputId"]
    version = str(item["version"])
    versions_status, _, versions_body = request(
        f"/agent/tasks/{TASK_ID}/artifacts/{oid}/versions?limit=20")
    detail_status, _, detail_body = request(
        f"/agent/tasks/{TASK_ID}/artifacts/{oid}/versions/{version}")
    download_status, headers, payload = request(
        f"/agent/tasks/{TASK_ID}/artifacts/{oid}/versions/{version}/download", binary=True)
    snapshot = next((QUEUE_ROOT / "snapshots" / RUN_ID).glob(oid + ".*"))
    safe = {key: item.get(key) for key in (
        "outputId", "version", "title", "name", "mime", "size", "sha256", "state",
        "publicationKind", "previewKind", "canDownload"
    )}
    safe["versions"] = {
        "status": versions_status,
        "code": versions_body.get("code"),
        "count": len(((versions_body.get("data") or {}).get("items") or [])),
    }
    detail_data = detail_body.get("data") or {}
    safe["detail"] = {
        "status": detail_status,
        "code": detail_body.get("code"),
        "itemMatchesList": detail_data.get("item") == item,
    }
    safe["download"] = {
        "status": download_status,
        "contentLength": headers.get("Content-Length"),
        "size": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "matchesSnapshot": payload == snapshot.read_bytes(),
        "matchesMetadata": str(len(payload)) == str(item.get("size"))
            and hashlib.sha256(payload).hexdigest() == item.get("sha256"),
    }
    result["list"]["items"].append(safe)

path = Path("/tmp/od06-bounty-task4-recovery-read-r1.observation.json")
path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
