"""Complete the same batch's post-install smoke; never repeat its installation."""
import datetime,hashlib,json,time,urllib.request,urllib.error
from pathlib import Path
D=Path(__file__).resolve().parent;path=D/'api-08-release.json';r=json.loads(path.read_text());(D/'api-08-release-smoke-parser-failure.json').write_text(json.dumps(r,indent=2)+'\n');t=time.monotonic()
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
checks=[]
for route in ['/actuator/health','/oauth2/jwks','/agent/scenes/liangshan-hall/snapshot']:
 request=urllib.request.Request('http://127.0.0.1:10018'+route,headers={'Accept':'application/json'})
 try:
  with urllib.request.urlopen(request,timeout=15) as response:status=response.status;data=response.read(1048576)
 except urllib.error.HTTPError as e:status=e.code;data=e.read(1048576)
 if route=='/actuator/health':assert status==200 and json.loads(data)['status']['code']=='UP' # actual Boot 4 Status object, not invented string shape
 elif route=='/oauth2/jwks':assert status==200 and bool(json.loads(data)['keys'])
 else:assert status==401
 checks.append(dict(path=route,httpStatus=status,bodySha256=hashlib.sha256(data).hexdigest()))
b=json.loads((D/'api-08-result.json').read_text());record=json.loads(Path('/home/isp/state/cyf-api-flow/record.json').read_text());p=b['package']
assert record['status']=='installed' and record['source_kind']=='LOCAL' and record['source']==p['identity']
assert sha('/home/isp/hosts/cyf/api/cyf-api-kit.jar')==p['applicationJarSha256'] and sha(record['backup'])==r['previousJarSha256']
assert not Path('/proc/1750937').exists()
status=(D/'api-08-lifecycle-status.log').read_text();assert 'HEALTH=UP' in status and 'ARTIFACT_ATTESTATION=MATCH' in status
now=datetime.datetime.now(datetime.timezone.utc);wall=(now-datetime.datetime.fromisoformat(r['startedAt'])).total_seconds()
old=r['wallSeconds'];r['priorAttempts'].append(dict(status=r['status'],error=r['error'],wallSeconds=old))
r['stages'].append(dict(name='smoke-parser-repair-and-wait',seconds=round(wall-old-(time.monotonic()-t),3)))
r['stages'].append(dict(name='health-and-security-smoke',seconds=round(time.monotonic()-t,3)))
r.pop('error',None);r.update(status='RELEASED',endedAt=now.isoformat(),wallSeconds=round(wall,3),checks=checks,installRecord=record,backupVerified=True,healthVerified=True,under600Seconds=wall<=600,businessSmokeScope='real protected scene endpoint unauthorized refusal; JWKS nonempty; no authenticated user mutation',temporaryDiagnostics='CYF_API_STARTUP_DIAGNOSTICS also enables lifecycle startup debug flags; remove on next normal measured release')
path.write_text(json.dumps(r,indent=2)+'\n');(D/'api-08-install-record.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k not in ('buildResult','installRecord')},indent=2))
