"""One measured stable API build/package/transaction/health release, no Flow."""
import datetime,hashlib,json,os,shutil,subprocess,time,urllib.request,urllib.error
from pathlib import Path
D=Path(__file__).resolve().parent; B=Path('/dev/shm/cyf-local-fast-api-20261107-08'); T=time.monotonic()
previous_result=json.loads((D/'api-08-release.json').read_text())
(D/'api-08-release-first-failure.json').write_text(json.dumps(previous_result,indent=2)+'\n')
T=time.monotonic()-(datetime.datetime.now(datetime.timezone.utc)-datetime.datetime.fromisoformat(previous_result['startedAt'])).total_seconds()
R=previous_result
R['priorAttempts']=[{'status':R['status'],'error':R.get('error'),'wallSeconds':R['wallSeconds']}]
R['stages'].append(dict(name='helper-path-repair-and-wait',seconds=round(time.monotonic()-T-R['wallSeconds'],3)))
R['status']='RUNNING';R.pop('error',None)

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def save():
 R['wallSeconds']=round(time.monotonic()-T,3);p=D/'api-08-release.tmp';p.write_text(json.dumps(R,indent=2)+'\n');os.replace(p,D/'api-08-release.json')
def run(name,cmd,env=None):
 t=time.monotonic();s=dict(name=name,startedAfterSeconds=round(t-T,3));R['stages'].append(s);save()
 with (D/('api-08-'+name+'.log')).open('w') as f:rc=subprocess.call(cmd,stdout=f,stderr=subprocess.STDOUT,env=env)
 s.update(seconds=round(time.monotonic()-t,3),exitCode=rc);save()
 if rc:raise RuntimeError(name+' exit '+str(rc))
try:
 canonical=Path('/home/isp/hosts/cyf/api/cyf-api-kit.jar'); before=sha(canonical)
 previous=json.loads(Path('/home/isp/state/cyf-api-flow/record.json').read_text())
 assert previous['status']=='installed' and previous['candidate_sha256']==before and previous['source_commit_sha']=='7bb82c526e4ba4345ca8e88711067ed23dfcdbbc'
 R['previousJarSha256']=before
 built=json.loads((B/'result.json').read_text());assert built['status']=='BUILT' and built['exitCode']==0;R['buildResult']=built;save()
 assert time.monotonic()-T<600,'build exhausted release budget; do not start installation'
 assert sha(canonical)==before,'production candidate changed during build'
 p=built['package']; approval=dict(schema_version=4,source_kind='LOCAL',source=p['identity'],package=p['package'],receipt_sha256=p['receiptSha256'],jar_sha256=p['applicationJarSha256'],expected_previous_sha256=before,consumed=False)
 descriptor=B/'install-descriptor.json';descriptor.write_text(json.dumps(approval,sort_keys=True)+'\n');descriptor.chmod(0o600)
 env=os.environ.copy();env['CYF_API_STARTUP_DIAGNOSTICS']='1'
 # Normal coordinator outside the timed build cgroup, retaining locks, backup,
 # real lifecycle health checks and recoverable state. No schema-changing hooks.
 run('install',['/usr/local/sbin/cyf-api-flow-deploy','--source-local',str(descriptor)],env)
 run('lifecycle-status',['/usr/local/sbin/cyf-api-kit','status'])
 t=time.monotonic();checks=[]
 for path in ['/actuator/health','/oauth2/jwks','/agent/scenes/liangshan-hall/snapshot']:
  request=urllib.request.Request('http://127.0.0.1:10018'+path,headers={'Accept':'application/json'})
  try:
   with urllib.request.urlopen(request,timeout=15) as response:status=response.status; data=response.read(1048576)
  except urllib.error.HTTPError as e:status=e.code;data=e.read(1048576)
  if path=='/actuator/health':assert status==200 and json.loads(data)['status']=='UP'
  elif path=='/oauth2/jwks':assert status==200 and bool(json.loads(data)['keys'])
  else:assert status==401 # Real protected business route remains denied without credentials.
  checks.append(dict(path=path,httpStatus=status,bodySha256=hashlib.sha256(data).hexdigest()))
 record=json.loads(Path('/home/isp/state/cyf-api-flow/record.json').read_text());assert record['status']=='installed' and record['source_kind']=='LOCAL' and record['source']==p['identity'] and sha(canonical)==p['applicationJarSha256']
 assert sha(record['backup'])==before
 status=(D/'api-08-lifecycle-status.log').read_text();assert 'HEALTH=UP' in status and 'ARTIFACT_ATTESTATION=MATCH' in status
 R['stages'].append(dict(name='health-and-security-smoke',seconds=round(time.monotonic()-t,3)))
 R.update(status='RELEASED',checks=checks,installRecord=record,backupVerified=True,healthVerified=True,securityReadinessVerified=True,businessSmokeScope='protected scene endpoint rejects unauthenticated GET; no authenticated user mutation',under600Seconds=time.monotonic()-T<=600,endedAt=datetime.datetime.now(datetime.timezone.utc).isoformat())
except BaseException as e:
 R.update(status='FAIL',error=type(e).__name__+': '+str(e));raise
finally:
 if B.exists():
  for name in ['result.json','inputs.json','gradle.log']:
   if (B/name).exists():shutil.copyfile(B/name,D/('api-08-'+name))
 save()
 print(json.dumps({k:v for k,v in R.items() if k not in ('buildResult','installRecord')},indent=2))
