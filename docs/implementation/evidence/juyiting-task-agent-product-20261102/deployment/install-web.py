from pathlib import Path
import json,hashlib,subprocess,os
D=Path(__file__).resolve().parent
r=json.loads((D/'web-verified.json').read_text());a=json.loads((D/'api-install-result.json').read_text());assert a['exitCode']==0 and a['run']=='441'
assert json.loads(Path('/home/isp/state/cyf-api-flow/record.json').read_text())['source_commit_sha']=='aa6ecf935343caed76f6d0c657f9847025de4600'
b=json.loads((D/'backup.json').read_text());assert hashlib.sha256(Path('/home/isp/state/cyf-web-flow/record.json').read_bytes()).hexdigest()==b['recordSha256']
env=dict(os.environ,SSL_CERT_FILE='/etc/pki/tls/certs/ca-bundle.crt')
with (D/'web-install.log').open('ab') as log:
 p=subprocess.run(['/usr/local/sbin/cyf-web-flow-deploy',r['pipeline'],r['run'],r['commit'],r['version'],r['sha256']],stdout=log,stderr=subprocess.STDOUT,env=env)
(D/'web-install-result.json').write_text(json.dumps({'exitCode':p.returncode,'run':r['run']}));print('web install exit',p.returncode);raise SystemExit(p.returncode)
