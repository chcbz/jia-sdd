import pathlib,json,hashlib,subprocess,os,sys
sha=lambda p:hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
plan=json.loads(pathlib.Path(sys.argv[1]).read_text())
inputs=json.loads(pathlib.Path(plan['inputs']).read_text())
assert sha(plan['inputs'])==plan['fixture_digest']
assert sha(plan['matrix'])==plan['matrix_sha256']
assert sha(inputs['init']['path'])==inputs['init']['sha256']
assert sha(inputs['runner']['path'])==inputs['runner']['sha256']
w=inputs['worktree']
def git(*a):return subprocess.check_output(['git','-C',w]+list(a),universal_newlines=True).strip()
assert git('rev-parse','HEAD')==inputs['commit']
assert git('rev-parse','HEAD^{tree}')==inputs['tree']
assert not git('status','--porcelain')
for p,h in inputs['source_file_hashes'].items():assert sha(pathlib.Path(w)/p)==h
for x in inputs['contracts']:assert sha(x['path'])==x['sha256']
log=pathlib.Path(inputs['log']);assert not log.exists()
if len(sys.argv)==3 and sys.argv[2]=='--check-plan':
 print('STATIC_PLAN_PASS no Gradle/process/DB started');sys.exit(0)
assert len(sys.argv)==2
command=['/usr/bin/python3','/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py']+plan['argv']
with log.open('xb') as f:
 p=subprocess.Popen(command,cwd='/home/isp/wsps/cyf',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,bufsize=0)
 print('ACTUAL_RUN orchestrator_pid=%d rawlog=%s'%(p.pid,log),flush=True)
 for line in iter(p.stdout.readline,b''):
  f.write(line);f.flush();sys.stdout.buffer.write(line);sys.stdout.buffer.flush()
 code=p.wait()
print('ACTUAL_EXIT=%d'%code,flush=True);sys.exit(code)
