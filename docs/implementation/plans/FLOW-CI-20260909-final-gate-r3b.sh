set -eu
python3 - <<'PYGATE'
import json, pathlib, subprocess, sys
p=pathlib.Path('_flow_ci_export')
r=json.loads((p/'result.json').read_text())
rc=r['native_runner_rc']
if type(rc) is not int or not 0 <= rc <= 255:
    raise SystemExit(70)
if rc != 0:
    raise SystemExit(rc)
if not r['receipt_present']:
    raise SystemExit(70)
ticket=json.loads((p/'ticket.json').read_text())
expected='04fb38e1d81ade959f2e0dc8b9f3464d16a51805064c2dc84548e3098528d22f'
check=subprocess.call(['python3',ticket['execution']['tool_root']+'/ops/orchestration/cyf_orchestrator.py',
    'flow-remote','inspect','--ticket',str(p/'ticket.json'),'--expected-ticket-sha256',expected,
    '--receipt',str(p/'receipt.json')])
if check != 0:
    raise SystemExit(check)
receipt=json.loads((p/'receipt.json').read_text())
if receipt['status'] != 'success' or receipt['gradle_exit_code'] != 0 or receipt['bridge_exit_code'] != 0:
    raise SystemExit(70)
print('FLOW_CI_TARGETED_COLD_GATE_PASS; production/full-suite acceptance NOT granted')
PYGATE
