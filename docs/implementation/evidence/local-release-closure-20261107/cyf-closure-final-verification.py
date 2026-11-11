from pathlib import Path
import json,hashlib,os,urllib.request,urllib.error,datetime,subprocess
r=Path('/home/isp/wsps/cyf');e=r/'docs/implementation/evidence/local-release-closure-20261107'
def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
a=json.loads(Path('/home/isp/state/cyf-api-flow/record.json').read_text());w=json.loads(Path('/home/isp/state/cyf-web-flow/record.json').read_text());reg=json.loads(Path('/home/isp/state/cyf-host-cleanup/completed-tasks.json').read_text());assert a['status']=='installed' and a['schema_version']==4 and w['status']=='online_verified' and w['schema_version']==2
assert sha('/home/isp/hosts/cyf/api/cyf-api-kit.jar')==a['candidate_sha256'];assert sha(a['backup'])==a['previous_sha256'];os.kill(2168125,0)
checks=[]
for route in ['/actuator/health','/oauth2/jwks','/agent/scenes/liangshan-hall/snapshot']:
 try:
  with urllib.request.urlopen('http://127.0.0.1:10018'+route,timeout=15) as resp:code=resp.status;data=resp.read(1048576)
 except urllib.error.HTTPError as ex:code=ex.code;data=ex.read(1048576)
 if route=='/actuator/health':assert code==200 and json.loads(data)['status']['code']=='UP'
 elif route=='/oauth2/jwks':assert code==200 and json.loads(data)['keys']
 else:assert code==401
 checks.append({'route':route,'code':code,'sha256':hashlib.sha256(data).hexdigest()})
idx=next(x for x in w['files'] if x['path']=='index.html');assert sha('/home/isp/hosts/cyf/web/kit/index.html')==idx['sha256']
# Use the host's original TLS-capable interpreter through curl without disabling trust.
online=subprocess.check_output(['curl','--fail','--silent','--show-error','--max-time','20','https://kit.chaoyoufan.cn/']);assert hashlib.sha256(online).hexdigest()==idx['sha256']
archives=[]
for t in reg['tasks']:
 for f in t.get('artifacts',{}).get('files',[]):
  p=Path(t['task_root'])/f['relative_path'];assert sha(p)==f['sha256'];archives.append({'path':str(p),'sha256':f['sha256']})
installed=[]
for s,d in [('ops/maintenance/flow_host_cleanup.py','/usr/local/libexec/cyf/flow_host_cleanup.py'),('ops/maintenance/rebuildable_cache_cleanup.py','/usr/local/libexec/cyf/rebuildable_cache_cleanup.py'),('ops/maintenance/clear_disk.host.sh','/home/isp/bin/clear_disk.sh')]:
 assert sha(r/s)==sha(d);installed.append({'source':s,'installed':d,'sha256':sha(d)})
jdk=Path('/opt/cyf/toolchains/dragonwell-21.0.11.0.11+10-GA');v=subprocess.check_output([str(jdk/'bin/java'),'-version'],stderr=subprocess.STDOUT).decode();assert '21.0.11' in v
cache=Path('/home/isp/state/cyf-local-build/gradle-home');assert cache.is_dir() and not Path('/var/tmp/cyf-local-build-timing-20261106/gradle-home').exists()
free=os.statvfs('/').f_bavail*os.statvfs('/').f_frsize
summary=dict(verifiedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),cleanupAllocatedBytes=1591824384,cleanupBreakdown={'apiHistoricalBackups':503287808,'abandonedBuildIntermediates':755277824,'webHistoryAndOrphanStage':333258752},rootFreeBytes=free,capacityWarning='Below 5GiB cleanup trigger; protected files preserved; target not reached',maintenanceTests=253,apiPid=2168125,apiJarSha256=a['candidate_sha256'],apiRollbackSha256=a['previous_sha256'],apiRecordSha256=sha('/home/isp/state/cyf-api-flow/record.json'),webRecordSha256=sha('/home/isp/state/cyf-web-flow/record.json'),webIndexSha256=idx['sha256'],checks=checks,installed=installed,registeredTasks=len(reg['tasks']),artifacts=archives,jdk=str(jdk),javaVersion=v,gradleHome=str(cache),cron='*/30 * * * * root /home/isp/bin/clear_disk.sh clean',actualCleanupExitCode=3,noNewApplicationBuildOrRestart=True,measuredReleaseSeconds=435.314,scope='Web/API warm-cache selected baseline; not cold-build/full-regression guarantee; no authenticated mutation')
(e/'closure-summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
