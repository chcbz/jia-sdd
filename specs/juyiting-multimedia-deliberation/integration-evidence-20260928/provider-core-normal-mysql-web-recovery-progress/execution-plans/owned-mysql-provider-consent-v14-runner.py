import sys,json,pathlib,hashlib,subprocess,os
plan=json.loads(pathlib.Path(sys.argv[1]).read_text());inputs=json.loads(pathlib.Path(plan['inputs']).read_text())
d=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
assert d(plan['matrix'])==plan['matrix_sha256'] and d(plan['inputs'])==plan['fixture_digest']
assert plan['environment']==inputs['fixture_environment']
environment=os.environ.copy();environment.update(plan['environment'])
assert set(plan['environment'])=={'MMD_U1_REFERENCE_MYSQL_URL','MMD_U1_REFERENCE_MYSQL_USER','MMD_U1_REFERENCE_MYSQL_PASSWORD','MMD_U1_REFERENCE_MYSQL_DATABASE_PREFIX','MMD_U1_REFERENCE_MYSQL_ISOLATED_FIXTURE'}
out=pathlib.Path(inputs['logs']['gradle_stdout_stderr'])
command=['/usr/bin/python3','/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py']+plan['argv']
with out.open('xb') as log:
 p=subprocess.Popen(command,cwd='/home/isp/wsps/cyf',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0,env=environment)
 print('ACTUAL_STREAM_CAPTURE launcher_pid={} orchestrator_pid={} file={}'.format(os.getpid(),p.pid,out),flush=True)
 for b in iter(p.stdout.readline,b''):
  log.write(b);log.flush();sys.stdout.buffer.write(b);sys.stdout.buffer.flush()
 code=p.wait()
print('ACTUAL_STREAM_EXIT={}'.format(code),flush=True);sys.exit(code)
