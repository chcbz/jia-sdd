import os,sys,subprocess,time,json,hashlib
from pathlib import Path
root=Path('/home/isp/wsps/cyf'); ext=Path('/home/isp/wsps/chcbz/isp-install')
ev=root/'docs/implementation/evidence/runtime-footprint-20261109'
batch=sys.argv[1]
commands=[['/usr/bin/python3','-B',str(ext/'tests/test_runtime_python_artifact.py'),'-v'],['/usr/bin/python3','-B',str(ext/'tests/test_runtime_python_freeze.py'),'-v'],['/usr/bin/python3','-B','-m','unittest','discover','-s','ops/maintenance/tests','-p','test_runtime_backup_scope.py','-v'],['/usr/bin/python3','-B','-m','unittest','discover','-s','ops/maintenance/tests','-p','test_runtime*py','-v']]
inputs=[ext/'conf/cyf-agent-runtime-v1/lib/python-artifact.py',ext/'tests/test_runtime_python_artifact.py',ext/'conf/cyf-agent-runtime-v1/lib/freeze-python.py',ext/'tests/test_runtime_python_freeze.py',root/'ops/maintenance/runtime_backup_scope.py',root/'ops/maintenance/runtime_backup_cleanup.py',root/'ops/maintenance/tests/test_runtime_backup_scope.py']
hashes={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs}
env=dict(os.environ,TMPDIR='/home/isp/state/cyf-local-build/tasks/runtime-footprint-20261109/tmp',TMP='/home/isp/state/cyf-local-build/tasks/runtime-footprint-20261109/tmp',TEMP='/home/isp/state/cyf-local-build/tasks/runtime-footprint-20261109/tmp',PYTHONDONTWRITEBYTECODE='1')
results=[]
with (ev/(batch+'-tests.log')).open('wb') as log:
 for cmd in commands:
  start=time.monotonic(); log.write(('COMMAND '+repr(cmd)+'\n').encode()); log.flush()
  try:r=subprocess.run(cmd,cwd=str(root),env=env,stdout=log,stderr=subprocess.STDOUT,timeout=600-sum(x['seconds'] for x in results)); code=r.returncode
  except subprocess.TimeoutExpired:code=124
  results.append(dict(command=cmd,seconds=time.monotonic()-start,exitCode=code))
  if code:break
result={'commands':results,'inputHashes':hashes,'inputUnchanged':hashes=={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in inputs},'seconds':sum(x['seconds'] for x in results)}
(ev/(batch+'-result.json')).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
