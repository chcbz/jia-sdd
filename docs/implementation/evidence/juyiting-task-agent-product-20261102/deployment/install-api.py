from pathlib import Path
import json,hashlib,subprocess,os,datetime
D=Path(__file__).resolve().parent
r=json.loads((D/'api-verified.json').read_text());assert r['status']=='verified_not_deployed' and r['run']=='441'
old=(D/'api-previous-record.json').read_bytes();assert Path('/home/isp/state/cyf-api-flow/record.json').read_bytes()==old,'production changed'
for p,h in json.loads((D/'installer-baseline.json').read_text())['helpers'].items():assert hashlib.sha256(Path(p).read_bytes()).hexdigest()==h,'installer changed'
h=hashlib.sha256()
with open('/home/isp/hosts/cyf/api/cyf-api-kit.jar','rb') as f:
 for b in iter(lambda:f.read(1048576),b''):h.update(b)
assert h.hexdigest()==json.loads(old)['candidate_sha256']
with (D/'api-install.log').open('ab') as log:
 p=subprocess.run(['/usr/local/sbin/cyf-api-flow-deploy',r['pipeline'],r['run'],r['commit'],r['version'],r['sha256']],stdout=log,stderr=subprocess.STDOUT)
(D/'api-install-result.json').write_text(json.dumps({'finishedAt':datetime.datetime.now().isoformat(),'exitCode':p.returncode,'run':r['run']}))
raise SystemExit(p.returncode)
