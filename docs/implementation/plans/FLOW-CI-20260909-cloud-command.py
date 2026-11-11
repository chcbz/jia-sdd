"""Reviewed control-plane template; executed only inside cloud JavaBuild.
Payload constants are prepended by the controller. No credentials or deployment.
"""
import base64
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import zlib


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def git(*args, **kwargs):
    return subprocess.check_output(['git'] + list(args), **kwargs).decode().strip()


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


platform_cwd = pathlib.Path.cwd().resolve()
need(os.environ.get('PIPELINE_ID') == '5256653', 'Unexpected platform pipeline')
run_id = os.environ.get('BUILD_NUMBER', '')
need(re.fullmatch('[1-9][0-9]*', run_id) is not None, 'Missing platform run number')
tip = git('rev-parse', 'HEAD')
need(os.environ.get('CI_COMMIT_SHA') == tip, 'Platform source SHA differs from checkout')
need(os.environ.get('CI_COMMIT_REF_NAME') == 'develop', 'Unexpected platform source branch')
need(git('rev-parse', '--is-shallow-repository') == 'false', 'Full source history required')

payload = json.loads(zlib.decompress(base64.b64decode(PAYLOAD_B64)).decode('utf-8'))
need(set(payload) == {'ticket', 'tools'}, 'Unknown payload fields')
ticket_bytes = base64.b64decode(payload['ticket'])
need(hashlib.sha256(ticket_bytes).hexdigest() == TICKET_SHA256, 'Ticket transport mismatch')
ticket = json.loads(ticket_bytes.decode('utf-8'))
api = pathlib.Path(ticket['execution']['cwd'])
tools = pathlib.Path(ticket['execution']['tool_root'])
receipt_path = pathlib.Path(ticket['execution']['receipt_path'])
run_root = receipt_path.parent
need(not api.exists() and not tools.exists() and not run_root.exists(), 'Fresh paths required')
allowed = {
    'ops/orchestration/cyf_orchestrator.py',
    'ops/orchestration/flow_remote.py',
    'ops/ci/aliyun-flow/run-cloud.sh',
    'ops/ci/aliyun-flow/cold-init.gradle',
}
need(set(payload['tools']) == allowed, 'Unexpected tool transport paths')
for relative in sorted(allowed):
    dest = tools / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    with dest.open('xb') as f:
        f.write(base64.b64decode(payload['tools'][relative]))
    dest.chmod(0o555 if relative.endswith('.sh') else 0o444)
ticket_path = pathlib.Path('/tmp/cyf-flow-tickets') / (ticket['nonce'] + '.json')
ticket_path.parent.mkdir(parents=True, exist_ok=True)
with ticket_path.open('xb') as f:
    f.write(ticket_bytes)
ticket_path.chmod(0o444)

# Clone the authenticated Flow checkout locally on the CLOUD worker. Never refetch
# a moving remote branch; retain the exact Flow source-tip ancestry separately.
api.parent.mkdir(parents=True, exist_ok=True)
subprocess.check_call(['git', 'clone', '--no-hardlinks', '--no-checkout', str(platform_cwd), str(api)])
git('-C', str(api), 'remote', 'set-url', 'origin', ticket['source']['repo_url'])
git('-C', str(api), 'update-ref', 'refs/remotes/origin/develop', tip)
git('-C', str(api), 'checkout', '--detach', ticket['source']['commit_sha'])
need(git('-C', str(api), 'rev-parse', 'HEAD^{tree}') == ticket['source']['tree_sha'], 'Pinned tree differs')

os.environ['CYF_FLOW_ORGANIZATION_ID'] = '5fb7d76ee6f9d07f148529c7'
os.environ['CYF_FLOW_PIPELINE_ID'] = os.environ['PIPELINE_ID']
os.environ['CYF_FLOW_RUN_ID'] = run_id
# Logical YAML job id, NOT a fabricated numeric Flow API job id. The controller
# must bind this logical name to the authenticated same-run numeric job later.
os.environ['CYF_FLOW_JOB_ID'] = 'cloud_ci.api_ci'
os.environ['CYF_FLOW_SOURCE_TIP_SHA'] = tip
print('FLOW_CI_CONTEXT ' + json.dumps({'pipeline': '5256653', 'run': run_id,
      'logical_job': 'cloud_ci.api_ci', 'source_tip': tip,
      'built_commit': ticket['source']['commit_sha'], 'ticket_sha256': TICKET_SHA256}), flush=True)
rc = subprocess.call([str(tools / 'ops/ci/aliyun-flow/run-cloud.sh'), str(ticket_path),
                      TICKET_SHA256, str(api), str(receipt_path)])

# Export ONLY receipt-referenced files, XML and their hashes; no Gradle/HOME/cache
# directories. The separate REQUIRED final gate returns the recorded native rc.
export = platform_cwd / '_flow_ci_export'
export.mkdir(exist_ok=False)
shutil.copyfile(str(ticket_path), str(export / 'ticket.json'))
manifest = []
if receipt_path.is_file() and not receipt_path.is_symlink():
    receipt = json.loads(receipt_path.read_text())
    shutil.copyfile(str(receipt_path), str(export / 'receipt.json'))
    for record in receipt['files']:
        relative = pathlib.Path(record['path'])
        need(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe export path')
        src = run_root / relative
        need(src.is_file() and not src.is_symlink(), 'Invalid export member')
        need(run_root.resolve() in src.resolve().parents, 'Export escapes run root')
        need(digest(src) == record['sha256'], 'Export hash mismatch')
        dest = export / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(src), str(dest))
    for src in sorted((run_root / 'build').rglob('TEST-*.xml')):
        if 'test-results' not in src.parts:
            continue
        need(src.is_file() and not src.is_symlink(), 'Invalid XML member')
        relative = pathlib.Path('test-xml') / src.relative_to(run_root / 'build')
        dest = export / relative
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(str(src), str(dest))
        manifest.append({'path': str(relative), 'sha256': digest(dest), 'size': dest.stat().st_size})
result = {'native_runner_rc': rc, 'ticket_sha256': TICKET_SHA256,
          'platform_run': run_id, 'source_tip': tip, 'logical_job': 'cloud_ci.api_ci',
          'xml_files': manifest, 'receipt_present': (export / 'receipt.json').is_file()}
(export / 'result.json').write_text(json.dumps(result, sort_keys=True, indent=2) + '\n')
print('FLOW_CI_RECORDED_RC=' + str(rc), flush=True)
# Evidence collection step intentionally completes; final_gate MUST NOT be removed.
