# Controller-only rendering, not a build. Exact output requires independent review.
import ast, base64, hashlib, json, pathlib, zlib
root=pathlib.Path('/home/isp/wsps/cyf')
plans=root/'docs/implementation/plans'
tp=pathlib.Path('/tmp/cyf-flow-tickets/FLOW-CI-COLD-01-r3b.json')
tb=tp.read_bytes();ticket=json.loads(tb.decode());th=hashlib.sha256(tb).hexdigest()
paths=['ops/orchestration/cyf_orchestrator.py','ops/orchestration/flow_remote.py','ops/ci/aliyun-flow/run-cloud.sh','ops/ci/aliyun-flow/cold-init.gradle']
payload={'ticket':base64.b64encode(tb).decode(),'tools':{p:base64.b64encode((root/p).read_bytes()).decode() for p in paths}}
b64=base64.b64encode(zlib.compress(json.dumps(payload,sort_keys=True).encode(),9)).decode()
command='PAYLOAD_B64 = '+repr(b64)+'\nTICKET_SHA256 = '+repr(th)+'\n'+(plans/'FLOW-CI-20260909-cloud-command-r3.py').read_text()
ast.parse(command)
# This gate is mandatory after artifact upload; preserve runner exit code, and
# independently inspect success receipts without importing evidence on the worker.
gate='''set -eu
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
expected='''+repr(th)+'''
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
'''
start='set -eu\npython3 - <<\'PYCLOUD\'\n'+command+'\nPYCLOUD\n'
def indent(s):return '\n'.join('                '+line if line else '                ' for line in s.rstrip().splitlines())+'\n'
yaml='''# Manual cloud-only targeted cold validation; mandatory final native-exit gate.
# No automatic triggers, deployment or production DB; private consumer auth via encrypted group.
name: cyf-api-kit-ci
variableGroups: ["q37x7n8snxqq744z"]
sources:
  cyf_api:
    type: git
    name: CYF API develop
    endpoint: https://gitee.com/chcbz/jia.git
    branch: develop
    cloneDepth: 0
defaultWorkspace: cyf_api
stages:
  cloud_ci:
    name: Pinned backend cold validation - NO DEPLOY
    jobs:
      api_ci:
        name: Targeted tests and bootJar with final required gate
        runsOn: public/cn-beijing
        timeoutMinutes: 60
        steps:
          cold_build:
            step: JavaBuild
            name: Execute cold validation and record native status
            with:
              jdkVersion: "21"
              run: |
'''+indent(start)+'''          upload_evidence:
            step: ArtifactUpload
            name: Preserve same-run evidence including failed build logs
            with:
              uploadType: flowPublic
              artifact: Artifacts_${PIPELINE_ID}
              filePath:
                - _flow_ci_export/
              includePathInArtifact: false
          final_gate:
            step: Command
            name: REQUIRED native exit and receipt gate - never skip
            with:
              run: |
'''+indent(gate)
p=plans/'FLOW-CI-20260909-cold-r3b.yaml';p.write_text(yaml)
(plans/'FLOW-CI-20260909-final-gate-r3b.sh').write_text(gate)
(plans/'FLOW-CI-20260909-build-step-r3b.sh').write_text(start)
meta={'config_path':str(p),'config_sha256':hashlib.sha256(yaml.encode()).hexdigest(),'ticket_sha256':th,
 'ticket_path':str(tp),'tool_bundle_sha256':ticket['tools']['bundle_sha256'],'fixture_digest':ticket['fixture']['digest'],
 'source':ticket['source'],'expires_at':ticket.get('expires_at'),'logical_job_key':'cloud_ci.api_ci',
 'required_final_gate':True,'production_deployment':False,'trigger_events':[],'encrypted_variable_group':'q37x7n8snxqq744z','legacy_numeric_variable_group':44254}
(plans/'FLOW-CI-20260909-cold-r3b-context.json').write_text(json.dumps(meta,indent=2)+'\n');print(json.dumps(meta,indent=2))
