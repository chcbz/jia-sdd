import datetime,json,pathlib,subprocess,time,hashlib,urllib.request,urllib.error,shutil
P=pathlib.Path; E=P(__file__).parent; O=P('/dev/shm/cyf-full-local-20261107-01');r=json.loads((E/'release.json').read_text());start=datetime.datetime.fromisoformat(r['startedAt']).timestamp()
def elapsed():return time.time()-start
def sha(p):return hashlib.sha256(P(p).read_bytes()).hexdigest()
r['priorFailure']={'error':r['error'],'wallSeconds':r['wallSeconds'],'reason':'controller Python3.11 CA trust missing; fixed by original installed helper system Python; verified TLS retained'}
r['stages'].append({'name':'repair-and-resume-gap','seconds':round(elapsed()-r['wallSeconds'],3)})
t=time.monotonic();budget=600-elapsed(); assert budget>0
cmd=['/usr/bin/python3','-I','-B','-c',"import runpy,sys; m=runpy.run_path('/usr/local/sbin/cyf-web-flow-deploy',run_name='cyf_local_release'); m['deploy_local'](sys.argv[1],float(sys.argv[2]))",str(O/'web/install-descriptor.json'),str(budget)]
with (E/'web-install-resume.log').open('w') as f: subprocess.check_call(cmd,stdout=f,stderr=subprocess.STDOUT)
r['stages'].append({'name':'web-install-resume','seconds':round(time.monotonic()-t,3),'exitCode':0,'argv':cmd})
a=json.loads((O/'api/result.json').read_text());w=json.loads((O/'web/result.json').read_text()); ar=json.loads(P('/home/isp/state/cyf-api-flow/record.json').read_text());wr=json.loads(P('/home/isp/state/cyf-web-flow/record.json').read_text()); p=a['package'];d=json.loads((O/'web/install-descriptor.json').read_text())
assert ar['status']=='installed' and ar['source_kind']=='LOCAL' and ar['source']==p['identity'] and sha('/home/isp/hosts/cyf/api/cyf-api-kit.jar')==p['applicationJarSha256']
assert sha(ar['backup'])==json.loads((O/'api/install-descriptor.json').read_text())['expected_previous_sha256']
assert wr['status']=='online_verified' and wr['source_kind']=='LOCAL' and wr['source']==d['source'] and wr['artifact_sha256']==w['artifact']['sha256']
t=time.monotonic();checks=[]
for route in ['/actuator/health','/oauth2/jwks','/agent/scenes/liangshan-hall/snapshot']:
 try:
  with urllib.request.urlopen('http://127.0.0.1:10018'+route,timeout=10) as resp:code,data=resp.status,resp.read()
 except urllib.error.HTTPError as e:code,data=e.code,e.read()
 if route=='/actuator/health':assert code==200 and json.loads(data)['status']['code']=='UP'
 elif route=='/oauth2/jwks':assert code==200 and json.loads(data)['keys']
 else:assert code==401
 checks.append({'path':route,'status':code,'bodySha256':hashlib.sha256(data).hexdigest()})
status=subprocess.check_output(['/usr/local/sbin/cyf-api-kit','status'],text=True);(E/'api-status-final.log').write_text(status);assert 'HEALTH=UP' in status and 'ARTIFACT_ATTESTATION=MATCH' in status
import re
pid=int(re.search(r'^PID=(\d+)$',status,re.M).group(1));cmdline=P('/proc/'+str(pid)+'/cmdline').read_bytes();assert b'=DEBUG' not in cmdline and b'=TRACE' not in cmdline and b'--cyf.startup-tracing.enabled=true' not in cmdline
for component,path in [('api','/root/.codex/worktrees/cyf-local-timing-api/api'),('web','/dev/shm/cyf-local-stable-web')]:
 assert not subprocess.check_output(['git','-C',path,'status','--porcelain'])
 assert subprocess.check_output(['git','-C',path,'rev-parse','HEAD'],text=True).strip()==r['source'][component]['commit']
r['stages'].append({'name':'final-smoke','seconds':round(time.monotonic()-t,3)})
r.update(apiBuild=a,webBuild=w,apiInstallRecord=ar,webInstallRecord=wr,checks=checks,apiPid=pid,startupDiagnostics=False,businessSmokeScope='real scene auth refusal + signing readiness; no authenticated business mutation',status='RELEASED',endedAt=datetime.datetime.now(datetime.timezone.utc).isoformat());r.pop('error',None)
for name,path in [('api-install-record.json','/home/isp/state/cyf-api-flow/record.json'),('web-install-record.json','/home/isp/state/cyf-web-flow/record.json')]:shutil.copyfile(path,E/name)
r['wallSeconds']=round(elapsed(),3);r['under600Seconds']=r['wallSeconds']<=600
for path in [O/'release.json',E/'release.json']:path.write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({'status':r['status'],'wallSeconds':r['wallSeconds'],'under600Seconds':r['under600Seconds'],'onlineFiles':wr.get('onlineVerifiedFiles')}))
