#!/usr/bin/env python3
import json
import os
import subprocess
from pathlib import Path

credentials = json.loads(Path(
    "/home/chc/.local/share/cyf-output-tools/services/mysql/state/credentials.json"
).read_text())
environment = os.environ.copy()
environment["MYSQL_PWD"] = credentials["password"]
mysql = "/home/chc/.local/share/cyf-output-tools/services/mysql/bin/mysql"
base = [mysql, "--protocol=TCP", "--host=127.0.0.1", "--port=13306",
        "--user=" + credentials["user"], "--database=cyf_od06_live_r1_20260912",
        "--batch", "--skip-column-names"]
run_id = "4326fd3446e4469dbc1e0c3221846ce5"
queries = {
    "task": "SELECT task_id,reward_status,assigned_agent_id,task_version,current_event_version FROM agent_task_meta WHERE task_id='4'",
    "member": "SELECT task_id,agent_id,member_status,version FROM agent_task_member WHERE task_id='4'",
    "events": "SELECT event_version,event_type,aggregate_type,aggregate_id FROM agent_task_event WHERE task_id='4' ORDER BY event_version",
    "artifact_counts": "SELECT COUNT(*),COUNT(DISTINCT artifact_id),MIN(artifact_version),MAX(artifact_version) FROM agent_task_artifact WHERE task_id='4'",
    "artifacts": f"SELECT artifact_id,artifact_version,run_id,file_name,content_byte_length,mime_type,content_hash FROM agent_task_artifact WHERE task_id='4' ORDER BY created_at",
    "upload_counts": f"SELECT COUNT(*),COUNT(DISTINCT upload_id),COUNT(DISTINCT object_id),SUM(file_name='report.md') FROM output_upload_session WHERE run_id='{run_id}'",
    "uploads": f"SELECT upload_id,file_name,state,expected_size,HEX(expected_sha256),slot_released,verification_attempts,COALESCE(error_code,'') FROM output_upload_session WHERE run_id='{run_id}' ORDER BY created_at",
    "objects": f"SELECT object_id,lifecycle_status,verification_status,actual_size,HEX(actual_sha256),actual_mime,COALESCE(error_code,'') FROM output_object WHERE run_id='{run_id}' ORDER BY created_at",
    "owner_refs": "SELECT output_id,output_version,reference_kind,state FROM output_object_reference WHERE source_type='TASK' AND source_id='4' AND reference_kind='OWNER_SHARE' ORDER BY created_at",
}
result = {}
for label, query in queries.items():
    process = subprocess.run(base + ["--execute=" + query], env=environment,
                             check=True, capture_output=True, text=True)
    result[label] = process.stdout.splitlines()
path = Path("/tmp/od06-bounty-task4-recovery-db-r1.observation.json")
path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
