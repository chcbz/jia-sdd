import importlib.util,unittest,json,os,time,subprocess
from pathlib import Path
base=Path(__file__).parent;root=Path('/home/isp/wsps/cyf');ev=root/'docs/implementation/evidence/runtime-footprint-20261109'
env=dict(os.environ,TMPDIR=str(base/'tmp'),TMP=str(base/'tmp'),TEMP=str(base/'tmp'),PYTHONDONTWRITEBYTECODE='1')
results=[]
cmd=['/usr/bin/python3','-B','/home/isp/wsps/chcbz/isp-install/tests/test_runtime_python_freeze.py','-v']
with (ev/'real-freeze-tests.log').open('wb') as log:
 start=time.monotonic();r=subprocess.run(cmd,env=dict(env,CYF_TEST_FREEZE_PYTHON='/home/isp/apps/cyf-agent-runtime-v1/app/codex-bridge/.toolchain/bin/python',CYF_PYTHON_DEBUG_OUTPUT=str(base/'freeze-debug-symbols-final')),stdout=log,stderr=subprocess.STDOUT,timeout=120)
 results.append({'command':cmd,'seconds':time.monotonic()-start,'exitCode':r.returncode})
assert r.returncode==0,'real freeze regression failed; preserve evidence'
cmd=['/usr/bin/python3','-I','-B','/usr/local/libexec/cyf/runtime_backup_cleanup.py','plan-state']
with (ev/'installed-state-inventory.json').open('wb') as output:
 start=time.monotonic();r=subprocess.run(cmd,stdout=output,env=env,timeout=60);os.chmod(str(ev/'installed-state-inventory.json'),0o600)
 results.append({'command':cmd,'seconds':time.monotonic()-start,'exitCode':r.returncode,'category':'read-only-inventory'})
assert r.returncode==0
# Execute the source-bound test module against the actual installed bytes.
os.environ.update({key:env[key] for key in ('TMPDIR','TMP','TEMP','PYTHONDONTWRITEBYTECODE')})
spec=importlib.util.spec_from_file_location('installed_scope_tests',str(root/'ops/maintenance/tests/test_runtime_backup_scope.py'));test=importlib.util.module_from_spec(spec);spec.loader.exec_module(test)
scope=Path('/usr/local/libexec/cyf/runtime_backup_scope.py');spec=importlib.util.spec_from_file_location('installed_scope',str(scope));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);test.m=m;test.SCRIPT=scope
with (ev/'installed-scope-fixtures.log').open('w') as log:
 start=time.monotonic();r=unittest.TextTestRunner(stream=log,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(test))
 results.append({'category':'installed-isolated-fixtures','tests':r.testsRun,'seconds':time.monotonic()-start,'success':r.wasSuccessful()})
(ev/'final-probes.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results))
