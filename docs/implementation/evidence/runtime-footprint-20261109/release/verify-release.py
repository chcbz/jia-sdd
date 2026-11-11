from pathlib import Path
import json,subprocess,hashlib,time,datetime,os,fcntl,shutil
B=Path(__file__).parent;I=B/'install';A=Path('/home/isp/apps/cyf-agent-runtime-v1/app');R=A.parent/'release-records';source=json.loads((B/'source.json').read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
report=json.loads((I/'installation.json').read_text());assert report['phase']=='installed-service-started'
unit='cyf-agent-runtime-v1@unified.service';pid=int(subprocess.check_output(['systemctl','show',unit,'-p','MainPID','--value']));assert pid==report['pid'] and pid>0
# Observe readiness; do not interrupt running requests or impose application deadlines.
health_path=Path('/home/isp/state/cyf-agent-runtime-v1/unified/host/runtime-health.json')
for attempt in range(36):
 health=json.loads(health_path.read_text())
 if health['pid']==pid and len(health['agents'])==3 and all(a['connected'] and a['registered'] and a['ready'] and a['channelState']=='ready' for a in health['agents']):break
 time.sleep(5)
else:raise RuntimeError('READINESS_NOT_YET_VERIFIED_SERVICE_LEFT_RUNNING')
assert time.time()*1000-health['observedAt']<2*health['heartbeatIntervalMs'],'STALE_CHANNEL_HEALTH'
assert subprocess.check_output(['systemctl','is-active',unit]).strip()==b'active'
accept=B/'acceptance';accept.mkdir(mode=0o700,exist_ok=True)
with (accept/'lujunyi-native-readiness.log').open('wb') as log:
 subprocess.run([str(A/'node/bin/node'),str(I/'verify-startup-readiness.mjs'),str(A),str(accept),'/home/isp/conf/cyf-agent-runtime-v1/unified-profiles/lujunyi.json'],env=dict(os.environ,TMPDIR=str(B/'tmp'),TMP=str(B/'tmp'),TEMP=str(B/'tmp'),PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=subprocess.STDOUT,check=True)
assert json.loads((accept/'host-startup-readiness.json').read_text())['passed'] is True
carriers=json.loads((I/'installed-carrier-readback.json').read_text());assert len(carriers['results'])==2 and all(r['contractReady'] and len(r['supportedInputs'])==10 for r in carriers['results'])
# Close only the current release record under the same host->release lock order.
locks=[]
try:
 for path in ('/run/lock/cyf-host-cleanup.lock','/run/lock/cyf-wuyong-versioned-release.lock'):
  fd=os.open(path,os.O_RDWR|os.O_NOFOLLOW);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);locks.append(fd)
 health=json.loads(health_path.read_text());assert int(subprocess.check_output(['systemctl','show',unit,'-p','MainPID','--value']))==pid and health['pid']==pid and len(health['agents'])==3 and all(a['connected'] and a['registered'] and a['ready'] and a['channelState']=='ready' for a in health['agents']),'POST_PROBE_CHANNEL_DRIFT'
 current=json.loads((R/'current.json').read_text());assert current['status']=='installed-channel-verification-pending' and current['runtimeVersion']==source['version'] and current['sourceCommit']==source['commit'] and current['sourceTree']==source['tree'];assert sha(Path(current['artifactManifestPath']))==current['artifactManifestSha256']
 ns={'__file__':str(I/'install-local-artifact.py')};text=(I/'install-local-artifact.py').read_text();exec(compile(text[:text.index('assert len(sys.argv)==3')],'installer-prefix','exec'),ns)
 assert ns['critical']()==json.loads((I/'prepared.json').read_text())['before'],'CONFIG_OR_IDENTITY_DRIFT'
 actual=ns['manifest'](A);expected=json.loads((R/'current.manifest.json').read_text());e={x['path']:x for x in expected};a={x['path']:x for x in actual};diff=[{'path':k,'expected':e.get(k),'actual':a.get(k)} for k in sorted(e.keys()|a.keys()) if e.get(k)!=a.get(k)]
 if diff:
  (accept/'derived-cache-drift.json').write_text(json.dumps(diff,indent=2)+'\n')
  proof=subprocess.check_output([str(A/'codex-bridge/.toolchain/bin/python'),'-I','-B',str(I/'verify-derived-pycache.py'),str(A),str(R/'current.manifest.json'),str(accept/'derived-cache-drift.json')]);(accept/'derived-cache-proof.json').write_bytes(proof);assert json.loads(proof)['status']=='PASS'
 backup=Path(current['backup']);scope=json.loads((backup/'state-scope.json').read_text());assert scope['archiveSha256']==current['stateBackupSha256'] and scope['releaseBinding']['commit']==source['commit'];assert sha(backup/'state.tar.gz')==scope['archiveSha256']
 for rels in (('bin/python','bin/python3','bin/python3.11'),('lib/libpython3.11.so','lib/libpython3.11.so.1.0')):
  files=[A/'codex-bridge/.toolchain'/r for r in rels];assert len({p.stat().st_ino for p in files})==1
  for p in files:assert sha(p)==sha(backup/'old-program'/p.relative_to(A)),'PYTHON_BYTES_CHANGED'
 after=int(subprocess.check_output(['du','-s','-B1',str(A)]).split()[0]);before=json.loads((B/'before-install.json').read_text())['baselineProgramAllocatedBytes']
 result={'status':'VERIFIED_ACTIVE','at':datetime.datetime.now().astimezone().isoformat(),'source':source,'pid':pid,'health':health,'programBeforeAllocatedBytes':before,'programAfterAllocatedBytes':after,'programSavedAllocatedBytes':before-after,'stateBackup':{'path':str(backup/'state.tar.gz'),'sha256':scope['archiveSha256'],'archiveBytes':scope['archiveBytes'],'includedRegularBytes':scope['includedRegularBytes'],'excludedCount':len(scope['excluded']),'policy':scope['policy']},'backupScopeReceipt':str(backup/'state-scope.json'),'identityAndConfigUnchanged':True,'carrierReadbackProfiles':2,'nativeFinalPathProbe':'lujunyi passed; no model turns','paidModelTurns':0,'debugSymbolsStripped':False,'testBuildPackageSeconds':json.loads((B/'build-budget.json').read_text())['seconds'],'freeBytesAfter':shutil.disk_usage(B).free,'hostNetSavingsClaimed':False,'caveat':'Old program retained for rollback; new consistent state snapshot consumes space. Raw excluded member bytes are not compressed savings.'}
 (accept/'verified-release.json').write_text(json.dumps(result,indent=2)+'\n');(accept/'verified-release.json').chmod(0o600)
 current.update(status='verified-active',businessAcceptance='PASS: both existing materials carrier bindings retain 10 inputs; lujunyi actual final-path native document/browser/PDF/script readiness; all 3 channels connected/registered/ready. No paid model turns.',channelVerification={'at':result['at'],'pid':pid,'healthObservedAt':health['observedAt'],'allConnectedRegisteredReady':True},footprintVerification=str(accept/'verified-release.json'),pythonLayoutTransformation={'mode':'internal-hardlink-deduplication-only','fileBytesUnchanged':True,'debugSymbolsStripped':False,'evidence':str(I/'python-deduplication.json')},stateBackupPolicy=scope['policy'])
 ns['atomic'](R/'current.json',current)
 with (A.parent/'RELEASES.md').open('a') as f:f.write('\n2026-11-09 Runtime1.3.69 verified-active '+source['commit']+'; byte-identical Python alias deduplication; essential-state-v1 snapshot; actual channel/materials/native readiness passed; no paid model turns. Evidence '+str(accept/'verified-release.json')+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='health'},indent=2))
finally:
 for fd in reversed(locks):os.close(fd)
