from pathlib import Path
import subprocess,json,hashlib,shutil
B=Path(__file__).parent; I=B/'install';S=Path('/home/isp/wsps/worktrees/runtime-footprint-20261109');OLD=Path('/home/isp/state/cyf-local-build/tasks/cyf-native-readiness-20261108/runtime/install');R=Path('/home/isp/apps/cyf-agent-runtime-v1/release-records')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
commit=subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD']).decode().strip();tree=subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD^{tree}']).decode().strip()
(B/'source.json').write_text(json.dumps(dict(commit=commit,tree=tree,baseline='92df9eb8de9abf523dd7224e575c43329139a98b',version='1.3.69',mode='deduplicate-only-byte-identical'),indent=2)+'\n')
(B/'build-budget.json').write_text(json.dumps(dict(limit=600,seconds=172.120,phases=[dict(phase='previous-implementation-conservative-upper-bound',seconds=172.120)]),indent=2)+'\n')
for n in ('prepare-runtime.py','apply-prepared-runtime.py','verify-derived-pycache.py','verify-startup-readiness.mjs','verify-installed-carriers.mjs'):
 shutil.copy2(OLD/n,I/n)
shutil.copytree(OLD/'host-probes',I/'host-probes');probes=json.loads((OLD/'host-probe-source.json').read_text());probes['source']={'commit':commit,'tree':tree};(I/'host-probe-source.json').write_text(json.dumps(probes,indent=2)+'\n')
s=(OLD/'install-local-artifact.py').read_text()
s=s.replace("20261109-native-readiness-local","20261109-runtime-footprint-local").replace("92df9eb8de9abf523dd7224e575c43329139a98b",commit).replace("31d4d7e0899f1692e924c248702fb3f19e2e48fd",tree).replace("native-readiness-20261109-runtime","runtime-footprint-20261109-runtime").replace("1.3.68","1.3.69").replace(".native-readiness-local-candidate",".cyf-agent-runtime.stage.footprint-20261109").replace("/home/isp/state/cyf-nr-20261109/tmp",str(B/'tmp'))
a=s.index('def run(args,**kw):');b=s.index('def atomic(',a)
s=s[:a]+'''def run(args,**kw):
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
'''+s[b:]
a=s.index(" assert proof['format']==");b=s.index(" assert sha(P(local['artifactPath']))",a)
s=s[:a]+''' assert proof['format']=='cyf-runtime-local-evidence-v1' and proof['status']=='VERIFIED_WITH_EXACT_INPUT_REUSE'
 assert proof['source']=={'commit':COMMIT,'tree':TREE},'SOURCE_MISMATCH'
 for item in proof['tests']:
  assert item['exitCode']==0 and sha(P(item['log']))==item['sha256'],'TEST_EVIDENCE_CHANGED'
 baseline=P(proof['baselineEvidence']['path']);assert sha(baseline)==proof['baselineEvidence']['sha256'],'BASELINE_EVIDENCE_CHANGED'
 assert json.loads(baseline.read_text())['source']=={'commit':'92df9eb8de9abf523dd7224e575c43329139a98b','tree':'31d4d7e0899f1692e924c248702fb3f19e2e48fd'}
 changed=subprocess.check_output(['git','-C','/home/isp/wsps/chcbz/isp-install','diff','--name-only','92df9eb8de9abf523dd7224e575c43329139a98b',COMMIT]).decode().splitlines()
 assert changed==proof['changedFiles'] and set(changed)=={'conf/cyf-agent-runtime-v1/lib/freeze-python.py','conf/cyf-agent-runtime-v1/lib/python-artifact.py','conf/cyf-agent-runtime-v1/package.json','tests/test_runtime_python_artifact.py','tests/test_runtime_python_freeze.py'},'REUSE_INPUT_CHANGED'
'''+s[b:]
s=s.replace("old['runtimeVersion']=='1.3.67' and old['sourceCommit']=='5dc596c9721000bcbca3c9dcb38d7b8e1c8d3a1e'", "old['runtimeVersion']=='1.3.68' and old['sourceCommit']=='92df9eb8de9abf523dd7224e575c43329139a98b'")
s=s.replace("old_lock['version']=='1.1.56' and new_lock['version']=='1.1.57'","old_lock==new_lock and new_lock['version']=='1.1.57'")
# A separate copy, never hardlink a candidate to the running installation.
s=s.replace("'--reflink=auto'","'--reflink=never'")
marker="with (TASK/'toolchain-image-preparation.log').open('wb') as log:"
s=s.replace(marker,'''# Deduplicate only: certification pins bytes, so no debug stripping in this release.
import importlib.util
spec=importlib.util.spec_from_file_location('freeze_python',str(stage/'runtime/lib/freeze-python.py'));slim=importlib.util.module_from_spec(spec);spec.loader.exec_module(slim)
assert 'CYF_PYTHON_DEBUG_OUTPUT' not in os.environ,'UNEXPECTED_SYMBOL_REWRITE_REQUEST'
slim_result=slim.slim_staged_python(stage/'codex-bridge/.toolchain')
atomic(TASK/'python-deduplication.json',slim_result)
'''+marker)
s=s.replace('This task decouples native readiness from materials with retained production startup recovery;', 'This task deduplicates byte-identical Python aliases and selects necessary recovery state;')
s=s.replace('independent native execution readiness;', 'byte-identical Python deduplication and essential state backup;')
s=s.replace("'none; existing carrier evidence verified at unchanged final toolchain paths'", "'none; Python file bytes and existing carrier evidence preserved; aliases use internal hardlinks'")
# Caller holds host cleanup lock before release lock across preparation/application.
(I/'install-local-artifact.py').write_text(s)
# prospective scripts own lock ordering; historical scripts remain unchanged
for n in ('prepare-runtime.py','apply-prepared-runtime.py'):
 p=I/n;x=p.read_text(); anchor="I=Path(__file__).resolve().parent;"
 lock="import os,fcntl\ncleanup_lock=os.open('/run/lock/cyf-host-cleanup.lock',os.O_RDWR|os.O_NOFOLLOW);fcntl.flock(cleanup_lock,fcntl.LOCK_EX|fcntl.LOCK_NB)\n"
 x=x.replace(anchor,lock+anchor);p.write_text(x)
print(commit,tree)
