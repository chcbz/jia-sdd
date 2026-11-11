from pathlib import Path
import os,subprocess,json,hashlib,time,shutil,tarfile,sys,stat
B=Path(__file__).parent;S=Path('/home/isp/wsps/worktrees/runtime-footprint-20261109');I=B/'install';A=Path('/home/isp/apps/cyf-agent-runtime-v1/app');OLD=Path('/home/isp/state/cyf-local-build/tasks/cyf-native-readiness-20261108/runtime');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();source=json.loads((B/'source.json').read_text());budget_path=B/'build-budget.json'
env=dict(os.environ,TMPDIR=str(B/'tmp'),TMP=str(B/'tmp'),TEMP=str(B/'tmp'),PYTHONDONTWRITEBYTECODE='1',CYF_TEST_FREEZE_PYTHON=str(A/'codex-bridge/.toolchain/bin/python'))
assert subprocess.check_output(['stat','-f','-c','%T',str(B)]).strip() not in (b'tmpfs',b'ramfs')
assert not subprocess.check_output(['git','-C',str(S),'status','--porcelain']).strip()
def measured(label,fn):
 budget=json.loads(budget_path.read_text());remaining=budget['limit']-budget['seconds'];assert remaining>0
 start=time.monotonic()
 try:return fn(remaining)
 finally:
  seconds=time.monotonic()-start;budget['seconds']+=seconds;budget['phases'].append({'phase':label,'seconds':seconds});budget_path.write_text(json.dumps(budget,indent=2)+'\n');print(label,seconds,flush=True)
tests=[]
commands=[['/usr/bin/python3','-B',str(S/'tests/test_runtime_python_freeze.py'),'-v'],['/usr/bin/python3','-B',str(S/'tests/test_runtime_python_artifact.py'),'-v'],['/usr/bin/python3','-B','-m','unittest','discover','-s','ops/maintenance/tests','-p','test_runtime*py','-v'],['/root/.local/bin/python3.11','-B',str(I/'test-install-integration.py')]]
for idx,cmd in enumerate(commands):
 log=B/('tests-%s.log'%idx)
 def test(remaining):
  with log.open('wb') as f:r=subprocess.run(cmd,cwd='/home/isp/wsps/cyf',env=env,stdout=f,stderr=subprocess.STDOUT,timeout=remaining)
  item={'command':cmd,'log':str(log),'sha256':sha(log),'exitCode':r.returncode};tests.append(item);(B/'tests.json').write_text(json.dumps(tests,indent=2)+'\n');assert r.returncode==0,log
 measured('test-'+str(idx),test)
def package(remaining):
 old_archive=OLD/'package/runtime.tgz';assert sha(old_archive)=='172ebdfa3019d748cacf93b9bcb33f88b88ea14849c22250dd1088d625e31274'
 package=B/'package';staging=package/'input';staging.mkdir()
 with tarfile.open(old_archive) as t:
  assert all(not Path(m.name).is_absolute() and '..' not in Path(m.name).parts and (m.isfile() or m.isdir()) for m in t.getmembers());t.extractall(staging)
 meta=json.loads((staging/'release.json').read_text());payload=staging/'payload'
 for e in meta['files']:assert sha(payload/e['path'])==e['sha256']
 mapping={'runtime/lib/freeze-python.py':'conf/cyf-agent-runtime-v1/lib/freeze-python.py','runtime/lib/python-artifact.py':'conf/cyf-agent-runtime-v1/lib/python-artifact.py','runtime/package.json':'conf/cyf-agent-runtime-v1/package.json'}
 for dst,src in mapping.items():shutil.copy2(S/src,payload/dst)
 baseline=OLD/'build-evidence.json'
 # Keep original successful/failing history without relabelling; unchanged consumers reuse exact bytes.
 proof=json.loads(baseline.read_text())
 for key in ('base','followup'):assert sha(Path(proof[key]['log']))==proof[key]['sha256']
 evidence={'format':'cyf-runtime-local-evidence-v1','status':'VERIFIED_WITH_EXACT_INPUT_REUSE','source':{k:source[k] for k in ('commit','tree')},'tests':tests,'baselineEvidence':{'path':str(baseline),'sha256':sha(baseline)},'changedFiles':subprocess.check_output(['git','-C',str(S),'diff','--name-only',source['baseline'],source['commit']]).decode().splitlines(),'reuseBasis':'Only Python freeze/extraction adapters, their tests and Runtime version changed. Runtime/bridge execution source, node lock, Python/browser inputs unchanged; installed target probes independently repeated. Python payload remains byte-identical; only aliases deduplicated before manifest.'}
 (B/'build-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n');shutil.copy2(B/'build-evidence.json',staging/'build-evidence.json')
 meta.update(sourceKind='LOCAL',buildId='runtime-footprint-20261109-runtime',commit=source['commit'],tree=source['tree'],version=source['version'],buildEvidenceSha256=sha(B/'build-evidence.json'))
 current=json.loads((A.parent/'release-records/current.json').read_text())
 meta['dependencyProvenance'].update(method='reuse byte-identical locked dependencies from verified Runtime1.3.68; internal Python hardlink deduplication only',baselineRecordSha256=sha(A.parent/'release-records/current.json'),baselineManifestSha256=current['artifactManifestSha256'])
 meta['files']=[{'path':str(p.relative_to(payload)),'sha256':sha(p),'mode':stat.S_IMODE(p.stat().st_mode)} for p in sorted(payload.rglob('*')) if p.is_file()]
 (staging/'release.json').write_text(json.dumps(meta,indent=2)+'\n')
 archive=package/'runtime.tgz'
 with tarfile.open(archive,'w:gz',compresslevel=1) as t:
  for n in ('release.json','build-evidence.json','payload'):t.add(staging/n,arcname=n)
 descriptor={'sourceKind':'LOCAL','buildId':meta['buildId'],'commit':source['commit'],'tree':source['tree'],'version':source['version'],'buildEvidencePath':str(B/'build-evidence.json'),'buildEvidenceSha256':sha(B/'build-evidence.json'),'artifactPath':str(archive),'artifactSha256':sha(archive),'expectedPreviousRecordSha256':sha(A.parent/'release-records/current.json')}
 (I/'local-release-input.json').write_text(json.dumps(descriptor,indent=2)+'\n');(I/'local-release-input.json').chmod(0o600)
 (B/'package-result.json').write_text(json.dumps({'status':'PACKAGED','source':source,'artifact':{'path':str(archive),'sha256':sha(archive),'bytes':archive.stat().st_size}},indent=2)+'\n')
 shutil.rmtree(staging)
measured('package',package)
