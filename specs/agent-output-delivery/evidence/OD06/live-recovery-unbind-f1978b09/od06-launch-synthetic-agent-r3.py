#!/usr/bin/env python3
import json
import os
from pathlib import Path

secrets = json.loads(Path("/tmp/od06-live-fixture-secrets.json").read_text())
environment = os.environ.copy()
profile = [{
    "profileId": "od06-synthetic",
    "agentId": secrets["agent_id"],
    "agentName": "OD06 Synthetic Agent",
    "personaName": "OD06 Synthetic Agent",
    "codexBin": "/tmp/od06-synthetic-codex-counted-r3.py",
    "codexHome": "/tmp/od06-synthetic-home-r1",
    "codexWorkdir": "/tmp/od06-synthetic-workspace-r2",
    "codexSandbox": "workspace-write",
    "codexApproval": "never",
    "codexSessionMode": "new",
    "codexTimeoutMs": 60000,
    "workspacePolicyId": "od06-synthetic",
    "isDefault": True,
}]
workspace_policies = {
    "od06-synthetic": {
        "root": "/tmp/od06-managed-workspaces-r1",
        "repository": "/tmp/od06-managed-repository-r1.git",
        "baseRef": "refs/heads/master",
        "trustedRemoteUrl": "https://example.invalid/od06-synthetic.git",
        "trustedRemoteRef": "refs/heads/master",
    }
}
environment.update({
    "WS_URL": "ws://127.0.0.1:10018/ws/agent/channel",
    "OPENCLAW_API_KEY": secrets["api_key"],
    "DEFAULT_CODEX_PROFILE": "od06-synthetic",
    "CODEX_PROFILES": json.dumps(profile, separators=(",", ":")),
    "CODEX_WORKSPACE_POLICIES": json.dumps(workspace_policies, separators=(",", ":")),
    "OUTPUT_API_URL": "http://127.0.0.1:10019",
    "OUTPUT_QUEUE_DIR": "/tmp/od06-synthetic-agent-r2/data/output-queue",
    "COMMAND_INBOX_DIR": "/tmp/od06-synthetic-agent-r2/data/inbox",
    "CODEX_PROFILE_RELOAD_MS": "60000",
    "HEARTBEAT_MS": "10000",
    "RECONNECT_MAX_MS": "120000",
})
command = ["/usr/bin/node", "/tmp/od06-synthetic-agent-r2/agent-client.mjs"]
os.execvpe(command[0], command, environment)
