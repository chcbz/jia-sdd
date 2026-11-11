from pathlib import Path
import json,subprocess,shutil,hashlib,datetime,os
B=Path(__file__).parent;E=Path('/home/isp/wsps/cyf/docs/implementation/evidence/runtime-footprint-20261109');S=Path('/home/isp/wsps/worktrees/runtime-footprint-20261109');A=Path('/home/isp/apps/cyf-agent-runtime-v1/app');R=A.parent/'release-records';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
current=json.loads((R/'current.json').read_text());assert current['status']=='verified-active' and current['runtimeVersion']=='1.3.69'
health=json.loads(Path('/home/isp/state/cyf-agent-runtime-v1/unified/host/runtime-health.json').read_text());assert health['pid']==int(subprocess.check_output(['systemctl','show','cyf-agent-runtime-v1@unified.service','-p','MainPID','--value']))==3821968 and all(a['ready'] and a['registered'] and a['connected'] and a.get('lastPresenceAckAt') for a in health['agents'])
(B/'acceptance/heartbeat-ack-readback.json').write_text(json.dumps(health,indent=2)+'\n')
release=E/'release';release.mkdir(mode=0o700)
for p in B.glob('*.json'):shutil.copy2(p,release/p.name)
for p in B.glob('*.py'):shutil.copy2(p,release/p.name)
shutil.copytree(B/'acceptance',release/'acceptance')
for name in ('tests-0.log','tests-1.log','tests-2.log','tests-3.log','verification.log'):shutil.copy2(B/name,release/name)
shutil.copytree(B/'install',release/'install',ignore=shutil.ignore_patterns('extracted','host-probes'))
# Preserve payload metadata outside the reconstructible extracted package input.
shutil.copy2(B/'install/extracted/release.json',release/'release.json')
subprocess.run(['git','-C',str(S),'diff','--binary','92df9eb8de9abf523dd7224e575c43329139a98b','HEAD'],stdout=(release/'release-source.patch').open('wb'),check=True)
assert not subprocess.check_output(['git','-C',str(S),'status','--porcelain']).strip()
subprocess.run(['git','-C','/home/isp/wsps/chcbz/isp-install','worktree','remove',str(S)],check=True)
shutil.rmtree(B/'install/extracted')
# The current-bound artifact is intentionally retained, not declared reclaimable.
d={'status':'DEPLOYED_VERIFIED_ACTIVE','at':datetime.datetime.now().astimezone().isoformat(),'currentRecordSha256':sha(R/'current.json'),'sourceCommit':current['sourceCommit'],'sourceTree':current['sourceTree'],'runtimeVersion':current['runtimeVersion'],'evidence':str(release),'privateWorktreeRemoved':str(S),'privateExtractedInputRemoved':str(B/'install/extracted'),'retainedArtifact':str(B/'package/runtime.tgz'),'artifactRetentionRegistration':'not declared reclaimable: current-bound artifact retained; no arbitrary nested task-root registration or new cleanup exception','retentionPlan':str(B/'retention-plan-final.json'),'retentionDeletedBytes':0,'retentionBoundary':'newest two and current pin unchanged; no eligible known historical payload. Unsafe/missing-evidence batches preserved, not normalized or deleted. Current archived runtime directory inherits baseline 0775 and remains skipped by future cleanup until separately reconciled.','testBuildPackageSeconds':json.loads((B/'build-budget.json').read_text())['seconds'],'wallSecondsObservedFromBatchSetup':(datetime.datetime.now().timestamp()-(B/'source.json').stat().st_mtime),'freeBytesAfterOwnedCleanup':shutil.disk_usage(B).free,'sourceIntegration':'task branch codex/runtime-footprint-20261109, clean commit retained. Original dirty workspace and old local develop unchanged; no remote latest or develop merge claimed.','files':{str(p.relative_to(release)):sha(p) for p in sorted(release.rglob('*')) if p.is_file()}}
(E/'release-closeout.json').write_text(json.dumps(d,indent=2)+'\n');(B/'closeout.json').write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items() if k!='files'},indent=2))
