from pathlib import Path
import json,hashlib,subprocess,datetime,os
D=Path(__file__).resolve().parent
v=json.loads((D/'api-verified.json').read_text());r=json.loads(Path('/home/isp/state/cyf-api-flow/record.json').read_text());assert r['status']=='installed' and r['run_id']==v['run'] and r['source_commit_sha']==v['commit'] and r['source_tree_sha']==v['tree']
h=hashlib.sha256()
with open('/home/isp/hosts/cyf/api/cyf-api-kit.jar','rb') as f:
 for b in iter(lambda:f.read(1048576),b''):h.update(b)
assert h.hexdigest()==v['jarSha256']
s=subprocess.check_output(['/usr/local/sbin/cyf-api-kit','status']).decode();assert 'ARTIFACT_ATTESTATION=MATCH' in s and 'HEALTH=UP' in s
pid=next(x.split('=',1)[1] for x in s.splitlines() if x.startswith('PID='));assert os.readlink('/proc/'+pid+'/cwd')=='/home/isp/hosts/cyf/api'
with (D/'canonical-after.log').open('w') as log:subprocess.run(['/usr/bin/python3','-I','-B','/home/isp/bin/tests/test_cyf_api_canonical_path.py'],stdout=log,stderr=subprocess.STDOUT,check=True)
f06=json.loads(Path('/home/isp/state/cyf-api-flow/schema-results/run-441.json').read_text()) if Path('/home/isp/state/cyf-api-flow/schema-results/run-441.json').exists() else None
out={'verifiedAt':datetime.datetime.now().isoformat(),'run':v['run'],'commit':v['commit'],'tree':v['tree'],'version':v['version'],'jarSha256':h.hexdigest(),'health':'UP','attestation':'MATCH','pid':pid,'canonicalPath':'PASS','backup':r['backup'],'businessAcceptance':'not exercised with a real authenticated user in this deployment'}
(D/'api-installed-verification.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
