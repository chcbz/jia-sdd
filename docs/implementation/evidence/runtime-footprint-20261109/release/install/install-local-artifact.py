# Scoped reuse of prior Runtime same-Run activation contract (runtime-release/install-flow-artifact.py; explicit LOCAL-source adaptation): no state adoption/migration, native startup gate and cleaned RPC timeout recovery; no profile or identity migration.
import os, sys, json, pathlib, hashlib, shutil, subprocess, tarfile, stat, fcntl, signal, time, datetime
P=pathlib.Path
TASK=P(__file__).resolve().parent
APP=P('/home/isp/apps/cyf-agent-runtime-v1/app'); RECORDS=APP.parent/'release-records'
BACK=P('/home/isp/baks/cyf-agent-runtime-v1/20261109-runtime-footprint-local')
UNIT='cyf-agent-runtime-v1@unified.service'; CONFIG=P('/home/isp/conf/cyf-agent-runtime-v1/unified.host.json')
COMMIT='fb9aafbd4c334efe7633f147d5b986de084f45df'; TREE='9cd28d72987b671c3be942563b4b9260d306bdca'
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def phase_log(phase,stage,started=None):
 try:
  print(json.dumps({'event':'installer-phase','phase':phase,'stage':stage,'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),**({'durationSeconds':round(time.monotonic()-started,3)} if started is not None else {})}),flush=True)
 except OSError:pass
def run(args,**kw):
 started=time.monotonic();phase_log(str(args[0]),'start')
 try:return subprocess.run(list(map(str,args)),check=True,**kw)
 finally:phase_log(str(args[0]),'finish',started)
def write_state_archive(destination, paths, log):
 import importlib.util
 module_path=P('/usr/local/libexec/cyf/runtime_backup_scope.py')
 assert sha(module_path)=='b05d63e386f056e99ec71d0162f68c8fe5f6f7c9b8f1ae147f6cef7de9b59a98','STATE_SCOPE_ADAPTER_CHANGED'
 spec=importlib.util.spec_from_file_location('runtime_backup_scope',str(module_path));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 receipt=module.write_state_archive(destination,paths,log,release_binding={'sourceKind':'LOCAL','buildId':build_id,'commit':COMMIT,'tree':TREE,'artifactSha256':artifact_sha,'predecessorRecordSha256':local_source['expectedPreviousRecordSha256']})
 atomic(TASK/'state-scope.json',receipt)
 return receipt['archiveSha256']
def assert_state_quiescent(paths):
 import importlib.util
 helper=P('/usr/local/libexec/cyf/runtime_backup_cleanup.py')
 assert sha(helper)=='07d80fa5a8d38066d347d89bb3b1bcb3c3e9a510373d750c505e81649f9f988b','STATE_SAFETY_HELPER_CHANGED'
 spec=importlib.util.spec_from_file_location('runtime_backup_safety',str(helper));module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 usage=module.safe.proc.snapshot(module.Paths().proc)
 assert not any(usage.used(p) for p in paths),'STATE_ROOT_STILL_IN_USE'
 assert subprocess.check_output(['systemctl','show',UNIT,'-p','MainPID','--value']).strip()==b'0'
 assert subprocess.check_output(['systemctl','show',UNIT,'-p','ActiveState','--value']).strip() in (b'inactive',b'failed')
def atomic(p,v):
 q=p.with_name(p.name+'.conversation-continuity.tmp');q.write_text(json.dumps(v,indent=2)+'\n');q.chmod(0o600);os.replace(q,p)
def persist_recovery_report():
 # A full disk must not prevent recovery of the unchanged prior service.
 # Failure remains a failure even when durable diagnostics are unavailable.
 try:
  atomic(TASK/'installation.json',report)
 except OSError as error:
  try:
   print('RECOVERY_REPORT_WRITE_FAILED '+type(error).__name__,file=sys.stderr,flush=True)
  except OSError:
   pass
def critical():
 paths=list(CONFIG.parent.rglob('*.json'))+list(CONFIG.parent.glob('*.conf'))
 for a in ('linchong','lujunyi','wuyong'):
  paths+=list((APP.parent/a).glob('*.json'))+list((APP.parent/a/'runtime-state').glob('runtime-authorization.json'))
 return {str(p):sha(p) for p in paths if p.is_file() and not p.is_symlink()}
def validate(root):
 with (TASK/'installation-validate.log').open('ab') as f:
  run(['/bin/bash','-c','set -a; . /home/isp/conf/cyf-agent-runtime-v1/unified.conf; set +a; export PYTHONDONTWRITEBYTECODE=1; exec bash "$1/runtime/validate.sh" --root "$1" --config "$2"','validate',root,CONFIG],stdout=f,stderr=subprocess.STDOUT)
def manifest(root):
 entries=[]
 for p in sorted(root.rglob('*')):
  s=p.lstat();e={'path':str(p.relative_to(root)),'mode':oct(stat.S_IMODE(s.st_mode)),'uid':s.st_uid,'gid':s.st_gid}
  if p.is_symlink():e.update(type='symlink',target=os.readlink(p))
  elif p.is_dir():e['type']='directory'
  elif p.is_file():e.update(type='file',sha256=sha(p))
  else:raise RuntimeError('UNSAFE_PROGRAM_FILE')
  entries.append(e)
 return entries
def verify_baseline_program():
 expected_path=RECORDS/'current.manifest.json';expected=json.loads(expected_path.read_text());actual=manifest(APP)
 e={x['path']:x for x in expected};a={x['path']:x for x in actual}
 diff=[{'path':k,'expected':e.get(k),'actual':a.get(k)} for k in sorted(a.keys()|e.keys()) if a.get(k)!=e.get(k)]
 if diff:
  atomic(TASK/'derived-cache-drift.json',diff)
  proof=subprocess.check_output([str(APP/'codex-bridge/.toolchain/bin/python'),'-I','-B',str(TASK/'verify-derived-pycache.py'),str(APP),str(expected_path),str(TASK/'derived-cache-drift.json')])
  result=json.loads(proof);assert result['status']=='PASS'
  atomic(TASK/'derived-cache-proof.json',result)
  assert manifest(APP)==actual,'BASELINE_CHANGED_DURING_VERIFICATION'
 atomic(TASK/'baseline-observed.manifest.json',actual)
 return actual
def capture_writer_objects(config,pid):
 roots=[P(config['stateRoot']),*[P(a['stateRoot']) for a in config['agents']]]; socket_fact=None
 if config.get('hostingControlPath'):
  hosting=json.loads(P(config['hostingControlPath']).read_text());managed=P(hosting['managedRoot'])
  roots += [managed,*[p.parent for p in managed.glob('*/state/.runtime-writer.lock')]]
  socket=P(hosting['socketPath']);st=socket.lstat()
  assert stat.S_ISSOCK(st.st_mode) and st.st_uid==0 and st.st_gid==hosting['socketGid'] and stat.S_IMODE(st.st_mode)==0o660
  socket_fact={'path':str(socket),'dev':st.st_dev,'ino':st.st_ino}
 records=[]
 for root in roots:
  path=root/'.runtime-writer.lock';st=path.lstat();assert stat.S_ISDIR(st.st_mode) and st.st_uid==0 and stat.S_IMODE(st.st_mode)==0o700
  assert set(p.name for p in path.iterdir())=={'owner.json'} and not (path/'owner.json').is_symlink()
  raw=(path/'owner.json').read_bytes();owner=json.loads(raw)
  assert owner['pid']==pid and owner['hostId']==config['hostId'] and owner.get('nonce')
  records.append({'path':str(path),'dev':st.st_dev,'ino':st.st_ino,'raw':raw})
 assert len({json.loads(r['raw'])['instanceId'] for r in records})==1
 return records,socket_fact

def retire_stopped_writer_objects(records,socket_fact,pid):
 # Called under the release lock only after exact unit MainPID=0 and cgroup-empty checks.
 assert not P('/proc/'+str(pid)).exists(),'OLD_WRITER_STILL_LIVE'
 pending=[]
 for r in records:
  path=P(r['path'])
  if not path.exists():continue
  st=path.lstat();assert stat.S_ISDIR(st.st_mode) and st.st_dev==r['dev'] and st.st_ino==r['ino'],'WRITER_LOCK_OWNERSHIP_CHANGED'
  assert (path/'owner.json').read_bytes()==r['raw'] and set(p.name for p in path.iterdir())=={'owner.json'},'WRITER_LOCK_CONTENT_CHANGED'
  pending.append(r)
 sock=None
 if socket_fact:
  sock=P(socket_fact['path'])
  if sock.exists():
   st=sock.lstat();assert stat.S_ISSOCK(st.st_mode) and st.st_dev==socket_fact['dev'] and st.st_ino==socket_fact['ino'],'SOCKET_OWNERSHIP_CHANGED'
   assert not any(line.split()[-1]==str(sock) for line in P('/proc/net/unix').read_text().splitlines() if line.split()),'SOCKET_STILL_LISTENING'
  else:sock=None
 if not pending and sock is None:return
 out=BACK/'stopped-writer-locks';out.mkdir(mode=0o700)
 atomic(BACK/'stopped-writer-recovery.json',{'oldPid':pid,'oldProcessAbsent':True,'locks':[{'path':r['path'],'ownerSha256':hashlib.sha256(r['raw']).hexdigest()} for r in pending],'socket':socket_fact if sock else None,'businessStateRestored':False})
 for i,r in enumerate(pending):os.rename(r['path'],out/str(i))
 if sock:sock.unlink()

def load_local_source(input_path, expected_input_sha):
 path=P(input_path);st=path.lstat()
 assert path.is_absolute() and stat.S_ISREG(st.st_mode) and st.st_uid==os.geteuid() and stat.S_IMODE(st.st_mode)==0o600
 assert sha(path)==expected_input_sha,'LOCAL_INPUT_CHANGED'
 local=json.loads(path.read_text())
 assert local['sourceKind']=='LOCAL' and not any(k in local for k in ('pipeline','run','flowStatus','buildJobId')),'GENUINE_LOCAL_SOURCE_REQUIRED'
 assert local['commit']==COMMIT and local['tree']==TREE and local['version']=='1.3.69'
 assert local['buildId']=='runtime-footprint-20261109-runtime'
 evidence=P(local['buildEvidencePath']);assert sha(evidence)==local['buildEvidenceSha256'],'SOURCE_EVIDENCE_CHANGED'
 proof=json.loads(evidence.read_text())
 assert proof['format']=='cyf-runtime-local-evidence-v1' and proof['status']=='VERIFIED_WITH_EXACT_INPUT_REUSE'
 assert proof['source']=={'commit':COMMIT,'tree':TREE},'SOURCE_MISMATCH'
 for item in proof['tests']:
  assert item['exitCode']==0 and sha(P(item['log']))==item['sha256'],'TEST_EVIDENCE_CHANGED'
 baseline=P(proof['baselineEvidence']['path']);assert sha(baseline)==proof['baselineEvidence']['sha256'],'BASELINE_EVIDENCE_CHANGED'
 assert json.loads(baseline.read_text())['source']=={'commit':'92df9eb8de9abf523dd7224e575c43329139a98b','tree':'31d4d7e0899f1692e924c248702fb3f19e2e48fd'}
 changed=subprocess.check_output(['git','-C','/home/isp/wsps/chcbz/isp-install','diff','--name-only','92df9eb8de9abf523dd7224e575c43329139a98b',COMMIT]).decode().splitlines()
 assert changed==proof['changedFiles'] and set(changed)=={'conf/cyf-agent-runtime-v1/lib/freeze-python.py','conf/cyf-agent-runtime-v1/lib/python-artifact.py','conf/cyf-agent-runtime-v1/package.json','tests/test_runtime_python_artifact.py','tests/test_runtime_python_freeze.py'},'REUSE_INPUT_CHANGED'
 assert sha(P(local['artifactPath']))==local['artifactSha256'],'ARTIFACT_CHANGED'
 assert sha(RECORDS/'current.json')==local['expectedPreviousRecordSha256'],'PREDECESSOR_CHANGED'
 return local
assert len(sys.argv)==3,'expected local-release-input.json input-sha256; not a Flow command'
local_source=load_local_source(sys.argv[1],sys.argv[2]);build_id=local_source['buildId']
lockpath=P('/run/lock/cyf-wuyong-versioned-release.lock');info=lockpath.lstat();assert stat.S_ISREG(info.st_mode) and info.st_uid==0 and not info.st_mode&0o077
lock=os.fdopen(os.open(str(lockpath),os.O_RDWR|os.O_NOFOLLOW),'r+');fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB);assert os.fstat(lock.fileno()).st_ino==lockpath.lstat().st_ino
assert not BACK.exists();BACK.mkdir(mode=0o700)
archive=P(local_source['artifactPath']);artifact_sha=sha(archive);assert artifact_sha==local_source['artifactSha256']
extract=TASK/'extracted';extract.mkdir(mode=0o700)
with tarfile.open(archive,'r:gz') as t:
 for m in t.getmembers():
  p=P(m.name);assert not p.is_absolute() and '..' not in p.parts and (m.isdir() or m.isfile()),'UNSAFE_LOCAL_ARTIFACT'
 t.extractall(extract)
meta=json.loads((extract/'release.json').read_text());assert meta['commit']==COMMIT and meta['tree']==TREE and meta['version']=='1.3.69'
assert meta['sourceKind']=='LOCAL' and meta['buildId']==build_id and meta['buildEvidenceSha256']==local_source['buildEvidenceSha256']
assert sha(extract/'build-evidence.json')==local_source['buildEvidenceSha256']
payload=extract/'payload';listed=set()
for e in meta['files']:
 p=payload/e['path'];assert str(p.resolve()).startswith(str(payload.resolve())+'/') and p.is_file() and not p.is_symlink()
 assert sha(p)==e['sha256'] and stat.S_IMODE(p.stat().st_mode)==e['mode'];listed.add(e['path'])
assert listed=={str(p.relative_to(payload)) for p in payload.rglob('*') if p.is_file()}
old=json.loads((RECORDS/'current.json').read_text());assert old['runtimeVersion']=='1.3.68' and old['sourceCommit']=='92df9eb8de9abf523dd7224e575c43329139a98b' and old['sourceKind']=='LOCAL'
phase_started=time.monotonic();phase_log('baseline-manifest','start')
old_manifest=json.loads((RECORDS/'current.manifest.json').read_text());verify_baseline_program()
phase_log('baseline-manifest','finish',phase_started)
# This fixed LOCAL artifact explicitly retains the unchanged verified host toolchains.
assert sha(payload/'codex-bridge/toolchain/requirements.txt')==meta['dependencyProvenance']['retainedPythonRequirementsSha256']
for relative in ('toolchain/requirements.txt','toolchain/browser/package-lock.json','toolchain/browser/sources.json'):
 assert sha(payload/'codex-bridge'/relative)==sha(APP/'codex-bridge'/relative),'RETAINED_TOOLCHAIN_INPUT_CHANGED'
# Only root package-name/version metadata changed. All locked dependency entries remain identical.
assert sha(payload/'codex-bridge/package-lock.json')==meta['dependencyProvenance']['lockSha256']
old_lock=json.loads((APP/'codex-bridge/package-lock.json').read_text())
new_lock=json.loads((payload/'codex-bridge/package-lock.json').read_text())
assert old_lock==new_lock and new_lock['version']=='1.1.57'
for lock_doc in (old_lock,new_lock):
 lock_doc.pop('version');lock_doc['packages'][''].pop('version');lock_doc.pop('name');lock_doc['packages'][''].pop('name')
assert old_lock==new_lock,'DEPENDENCY_CHANGE_REQUIRES_NEW_TOOLCHAIN_REVIEW'
assert subprocess.check_output([str(APP/'node/bin/node'),'--version']).decode().strip()=='v24.22.1'
config=json.loads(CONFIG.read_text());before=critical()
for temp_key in ('TMPDIR','TMP','TEMP'):os.environ[temp_key]='/home/isp/state/cyf-local-build/tasks/runtime-footprint-20261109/release/tmp'
assert P('/home/isp/state/cyf-local-build/tasks/runtime-footprint-20261109/release/tmp').is_dir()
for name in ('linchong','wuyong'):
 shutil.copy2(CONFIG.parent/'unified-profiles'/(name+'.json'),BACK/(name+'.profile.json'))
def inbox_roots():
 roots=[P(a['stateRoot']) for a in config['agents']]
 if config.get('hostingControlPath'):
  hosting=json.loads(P(config['hostingControlPath']).read_text())
  roots.extend(P(hosting['managedRoot']).glob('*/state'))
 return roots
# Queued work is left in place; any actual in-flight record blocks this installation.
for root in inbox_roots():
 for p in (root/'inbox').glob('**/processing/*'):
  if p.is_file():raise RuntimeError('IN_FLIGHT_WORK_REQUIRES_COORDINATION')
stage=APP.parent/'.cyf-agent-runtime.stage.footprint-20261109';assert not stage.exists();stage.mkdir(mode=0o700)
phase_started=time.monotonic();phase_log('candidate-copy','start')
run(['cp','--archive','--reflink=never','--',payload/'runtime',stage/'runtime']);run(['cp','--archive','--reflink=never','--',payload/'codex-bridge',stage/'codex-bridge'])
run(['cp','--archive','--reflink=never','--',APP/'node',stage/'node'])
(stage/'runtime/node-version.txt').write_text('24.22.1\n')
for folder in ('.toolchain','.browser-toolchain'):
 run(['cp','--archive','--reflink=never','--',APP/'codex-bridge'/folder,stage/'codex-bridge'/folder])
# Reused toolchain files remain byte/mode identical to the verified baseline manifest.
for folder in ('.toolchain','.browser-toolchain'):
 assert manifest(stage/'codex-bridge'/folder)==manifest(APP/'codex-bridge'/folder),'RETAINED_TOOLCHAIN_COPY_CHANGED'
# Verify prefix resolution after extraction; no installed venv or host base reuse.
run([stage/'codex-bridge/.toolchain/bin/python','-I','-B','-c','import sys; assert sys.prefix == sys.base_prefix == sys.argv[1]',stage/'codex-bridge/.toolchain'])
phase_log('candidate-copy','finish',phase_started)
# Deduplicate only: certification pins bytes, so no debug stripping in this release.
import importlib.util
spec=importlib.util.spec_from_file_location('freeze_python',str(stage/'runtime/lib/freeze-python.py'));slim=importlib.util.module_from_spec(spec);spec.loader.exec_module(slim)
assert 'CYF_PYTHON_DEBUG_OUTPUT' not in os.environ,'UNEXPECTED_SYMBOL_REWRITE_REQUEST'
slim_result=slim.slim_staged_python(stage/'codex-bridge/.toolchain')
atomic(TASK/'python-deduplication.json',slim_result)
with (TASK/'toolchain-image-preparation.log').open('wb') as log:
 run([stage/'node/bin/node',stage/'runtime/lib/prepare-toolchain-image.mjs','--root',stage],stdout=log,stderr=subprocess.STDOUT)
assert sha(stage/'codex-bridge/.sandbox-toolchain/manifest.json')==sha(APP/'codex-bridge/.sandbox-toolchain/manifest.json'),'TOOLCHAIN_VIEW_CHANGED_REQUIRES_REVIEW'
validate(stage)
# The worker cannot exercise UID namespaces. Run the exact same lightweight
# source test against this fixed artifact before stopping any production writer.
probes=json.loads((TASK/'host-probe-source.json').read_text())['probes']
assert {p['file'] for p in probes}=={'native-document-toolchain.test.mjs','native-browser-toolchain.test.mjs','native-browser-execution-profile.test.mjs'}
probe_dir=stage/'codex-bridge/test';assert not probe_dir.exists();probe_dir.mkdir(mode=0o700)
probe_files=[]
try:
 for probe in probes:
  assert sha(TASK/'host-probes'/probe['file'])==probe['sha256'],'HOST_PROBE_CHANGED'
  path=probe_dir/probe['file'];shutil.copy2(TASK/'host-probes'/probe['file'],path);probe_files.append(path)
 with (TASK/'host-capability-probe.log').open('wb') as log:
  env={'PATH':'/usr/bin:/bin','LANG':'C.UTF-8','TMPDIR':'/home/isp/state/cyf-local-build/tasks/runtime-footprint-20261109/release/tmp','TMP':'/home/isp/state/cyf-local-build/tasks/runtime-footprint-20261109/release/tmp','TEMP':'/home/isp/state/cyf-local-build/tasks/runtime-footprint-20261109/release/tmp','CYF_NATIVE_DOCUMENT_PROBE_PYTHON':str(stage/'codex-bridge/.toolchain/bin/python'),
       'CYF_NATIVE_BROWSER_PROBE_ROOT':str(stage/'codex-bridge/.browser-toolchain'),
       'CYF_NATIVE_BROWSER_PROFILE_PROBE_ROOT':str(stage/'codex-bridge/.browser-toolchain')}
  run([stage/'node/bin/node','--test','--test-concurrency=1','--test-name-pattern=pinned Python actually|real browser|real app-server',*probe_files],env=env,stdout=log,stderr=subprocess.STDOUT)
 proof=(TASK/'host-capability-probe.log').read_text()
 assert 'pass 3' in proof and 'fail 0' in proof and 'skipped 0' in proof,'HOST_PROBE_INCOMPLETE'
finally:
 for path in probe_files:path.unlink()
 probe_dir.rmdir()
# Exercise the actual startup declaration with this artifact, not a browser test
# that supplies a different command timeout. No model turn/business write.
with (TASK/'host-startup-readiness.log').open('wb') as log:
 run([stage/'node/bin/node',TASK/'verify-startup-readiness.mjs',stage,TASK],stdout=log,stderr=subprocess.STDOUT)
for n in ('current.json','current.manifest.json'):shutil.copy2(RECORDS/n,BACK/n)
shutil.copy2(APP.parent/'RELEASES.md',BACK/'RELEASES.md')
# The exact verified prior program is archived by atomic rename below, not compressed twice.
state_paths=[P('/home/isp/state/cyf-agent-runtime-v1'),P('/home/isp/state/cyf-agent-runtime-v1-managed'),CONFIG.parent,*[APP.parent/a for a in ('linchong','lujunyi','wuyong')]]
state_paths=[p for p in state_paths if p.exists()]
(BACK/'RECOVERY.md').write_text('This task deduplicates byte-identical Python aliases and selects necessary recovery state; no identity migration; Python/browser toolchains retain the current verified production baseline, with identical source inputs and copied bytes. Preserve all current journals and uninstall tombstones. Never replay or automatically translate legacy tasks. Program restoration before any new process starts is installation recovery only; any later rollback requires explicit state-compatibility assessment. Under the same release lock and with the exact unified unit stopped, verify old-program against current.manifest.json, then restore that archived program into canonical app and validate before restarting. Never start the archive path. Do not start backup paths or restore state.tar.gz over new session/ACK/business facts. Retain current facts and assess compatibility before rollback. installation.json records exact completed phase.\n')
report={'executionLocation':'host-local','sourceKind':'LOCAL','buildId':build_id,'commit':COMMIT,'tree':TREE,'version':'1.3.69','artifactSha256':artifact_sha,'phase':'candidate-validated','backup':str(BACK),'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
atomic(TASK/'installation.json',report)
def terminated(signum,frame):raise RuntimeError('CONTROLLED_INSTALL_INTERRUPTION')
signal.signal(signal.SIGTERM,terminated);signal.signal(signal.SIGINT,terminated)
stopped=False;switched=False;new_started=False
try:
 for root in inbox_roots():
  assert not any(p.is_file() for p in (root/'inbox').glob('**/processing/*')),'NEW_IN_FLIGHT_WORK'
 old_pid=int(subprocess.check_output(['systemctl','show',UNIT,'-p','MainPID','--value']))
 assert old_pid>0,'BASELINE_NOT_RUNNING_RECONCILE_OWNERSHIP'
 writer_objects,socket_fact=capture_writer_objects(config,old_pid)
 stopped=True;run(['systemctl','stop',UNIT])
 assert subprocess.check_output(['systemctl','show',UNIT,'-p','MainPID','--value']).strip()==b'0'
 cg=subprocess.check_output(['systemctl','show',UNIT,'-p','ControlGroup','--value']).decode().strip()
 for cp in [P('/sys/fs/cgroup'+cg+'/cgroup.procs'),P('/sys/fs/cgroup/systemd'+cg+'/cgroup.procs')]:
  if cg and cp.exists():assert not cp.read_text().strip(),'OWNED_CHILD_STILL_RUNNING'
 retire_stopped_writer_objects(writer_objects,socket_fact,old_pid)
 assert critical()==before,'CONFIG_OR_IDENTITY_CHANGED'
 assert_state_quiescent(state_paths)
 report['phase']='stopped';atomic(TASK/'installation.json',report)
 with (TASK/'state-backup.log').open('wb') as f:
  phase_started=time.monotonic();phase_log('state-backup','start')
  backup_digest=write_state_archive(BACK/'state.tar.gz',state_paths,f)
  phase_log('state-backup','finish',phase_started)
  run(['tar','--acls','--xattrs','--compare','-z','-f',BACK/'state.tar.gz','-C','/'],stdout=f,stderr=f)
 assert_state_quiescent(state_paths)
 report['stateBackupSha256']=backup_digest;report['oldProgramManifestSha256']=sha(BACK/'current.manifest.json');report['phase']='state-backed-up';atomic(TASK/'installation.json',report)
 retired=BACK/'old-program';os.rename(APP,retired);switched=True
 report['phase']='old-program-archived';atomic(TASK/'installation.json',report)
 os.rename(stage,APP)
 validate(APP);assert critical()==before,'IDENTITY_CHANGED'
 with (TASK/'installed-carrier-readback.log').open('wb') as log:
  run([APP/'node/bin/node',TASK/'verify-installed-carriers.mjs'],stdout=log,stderr=subprocess.STDOUT)
 assert critical()==before,'CONFIG_OR_IDENTITY_CHANGED'
 m=manifest(APP);atomic(RECORDS/'1.3.69.manifest.json',m);atomic(RECORDS/'current.manifest.json',m)
 current={'schemaVersion':1,'status':'installed-channel-verification-pending','runtimeVersion':'1.3.69','artifactPath':str(APP),'sourceCommit':COMMIT,'sourceTree':TREE,'artifactManifestPath':str(RECORDS/'1.3.69.manifest.json'),'artifactManifestSha256':sha(RECORDS/'1.3.69.manifest.json'),'artifactEntryCount':len(m),'sourceKind':'LOCAL','buildId':build_id,'artifactSha256':artifact_sha,'dependencyReuse':{'baselineManifestSha256':old['artifactManifestSha256'],'nodeVersion':'24.22.1','pythonFromSameRun':False,'retainedToolchainSourceRun':old['dependencyReuse']['retainedToolchainSourceRun'],'retainedToolchainSourceCommit':old['dependencyReuse']['retainedToolchainSourceCommit'],'retainedProgramSourceCommit':old['sourceCommit'],'pythonArtifactSha256':old['dependencyReuse']['pythonArtifactSha256'],'npmLockedDependencies':meta['dependencyProvenance']},'backup':str(BACK),'stateBackupSha256':report['stateBackupSha256'],'installationEvidence':str(TASK/'installation.json'),'businessAcceptance':'PENDING','priorBusinessIssue':old.get('businessAcceptance'),'identityUnchanged':True,'configChange':'none; Python file bytes and existing carrier evidence preserved; aliases use internal hardlinks','executionMode':'system-codex-no-program-snapshot','executionLocation':'host-local','installedAt':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 atomic(RECORDS/'current.json',current)
 new_started=True;run(['systemctl','start',UNIT])
 report['phase']='installed-service-started';report['pid']=int(subprocess.check_output(['systemctl','show',UNIT,'-p','MainPID','--value']));atomic(TASK/'installation.json',report)
 # Retain the exact retired program as the recovery archive; no redundant recompression/deletion.
 with (APP.parent/'RELEASES.md').open('a') as f:f.write('\n2026-11-09 Runtime1.3.69 '+COMMIT+' LOCAL '+build_id+': installed at fixed app; byte-identical Python deduplication and essential state backup; channel and skill business verification pending; previous version preserved in '+str(BACK)+'/old-program/.\n')
 print('RUNTIME_INSTALL_COMPLETE version=1.3.69 build='+build_id+' pid='+str(report['pid']),flush=True)
except BaseException:
 report['phase']='installation-interrupted-reconcile-required';persist_recovery_report()
 # Restore only program/records before any new executable has started. Never restore state.
 if stopped and not new_started:
  for name in ('linchong','wuyong'):
   saved=BACK/(name+'.profile.json')
   if saved.exists():shutil.copy2(saved,CONFIG.parent/'unified-profiles'/(name+'.json'))
  if switched:
   failed=BACK/'failed-candidate'
   if APP.exists():os.rename(APP,failed)
   os.rename(BACK/'old-program',APP)
   for n in ('current.json','current.manifest.json'):shutil.copy2(BACK/n,RECORDS/n)
   shutil.copy2(BACK/'RELEASES.md',APP.parent/'RELEASES.md')
  run(['systemctl','start',UNIT]);report['oldServiceRecovered']=True;persist_recovery_report()
 raise
