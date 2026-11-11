import pathlib,json,subprocess,hashlib,tempfile,time,os
P=pathlib.Path; S=P('/home/isp/wsps/worktrees/beta-wen-billing-runtime');B=P('/home/isp/state/cyf-local-build/tasks/cyf-beta-wen-cutover-20261107/runtime');F=B/'followup2';F.mkdir();tmp=P(tempfile.mkdtemp(prefix='cyf-wen-',dir='/tmp'));(tmp/'home').mkdir()
sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
git=lambda *a:subprocess.check_output(['git',*a],cwd=S,text=True).strip()
assert not git('status','--porcelain');assert git('rev-parse','HEAD')=='d7e51840f2cfc3cea6afda5a7e7e8d1b07d3f776'
assert git('diff','--name-only','6c8fc27314a17bdb778aaa5d69b9945837380a4a','HEAD')=='conf/codex-bridge/test/typed-inspection-runtime.test.mjs'
cmd=['/home/isp/apps/cyf-agent-runtime-v1/app/node/bin/node','--test','--test-concurrency=2','conf/codex-bridge/test/typed-inspection-runtime.test.mjs','conf/cyf-agent-runtime-v1/test/hosting-control.test.mjs']
start=time.time()
with (F/'tests.log').open('wb') as log:r=subprocess.run(cmd,cwd=S,env={'PATH':'/home/isp/apps/cyf-agent-runtime-v1/app/node/bin:/usr/bin:/bin','HOME':str(tmp/'home'),'TMPDIR':str(tmp),'LANG':'C.UTF-8'},stdout=log,stderr=subprocess.STDOUT)
record={'sourceCommit':git('rev-parse','HEAD'),'sourceTree':git('rev-parse','HEAD^{tree}'),'command':cmd,'tmpdir':str(tmp),'exitCode':r.returncode,'wallSeconds':round(time.time()-start,3),'testsLogSha256':sha(F/'tests.log'),'baseResults':{'path':str(B/'result.json'),'sha256':sha(B/'result.json'),'pass':1508,'fail':3,'skip':18},'reuseScope':'All production code and all other test files identical to 6c8fc27; failed hosting suite rerun with short Unix-socket fixture root; inspection stale assertion corrected per 79e08b1, all inspection tests rerun','sourceUnchanged':not git('status','--porcelain')}
(F/'result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2));raise SystemExit(r.returncode)
