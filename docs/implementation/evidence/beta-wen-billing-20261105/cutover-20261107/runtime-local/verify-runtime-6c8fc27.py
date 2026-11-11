import pathlib,tarfile,json,hashlib,subprocess,time,os
P=pathlib.Path
src=P('/home/isp/wsps/worktrees/beta-wen-billing-runtime'); out=P('/home/isp/state/cyf-local-build/tasks/cyf-beta-wen-cutover-20261107/runtime');out.mkdir(parents=True,exist_ok=True)
archive=P('/tmp/cyf-beta-retirement-20261106/runtime165.tgz'); assert hashlib.sha256(archive.read_bytes()).hexdigest()=='8d60753e69004073cfe801f68508377f39b796dc321c691fb0cefc5f78a969ad'
with tarfile.open(archive) as t:
 old=json.load(t.extractfile('./payload/codex-bridge/package-lock.json'));new=json.loads((src/'conf/codex-bridge/package-lock.json').read_text())
 for d in (old,new):
  d.pop('version',None);d.pop('name',None);d['packages'][''].pop('version',None);d['packages'][''].pop('name',None)
 assert old==new
 deps=src/'conf/codex-bridge/node_modules'; oldlink='/home/isp/wsps/chcbz/isp-install/conf/codex-bridge/node_modules'
 if deps.is_symlink():
  assert os.readlink(deps)==oldlink;deps.unlink();deps.mkdir()
 else:assert deps.is_dir()
 for m in t.getmembers():
  prefix='./payload/codex-bridge/node_modules/'
  if not m.name.startswith(prefix):continue
  rel=m.name[len(prefix):]
  if not rel:continue
  assert '..' not in P(rel).parts and (m.isfile() or m.isdir())
  dest=deps/rel
  if m.isdir():dest.mkdir(parents=True,exist_ok=True)
  else:
   dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(t.extractfile(m).read());dest.chmod(m.mode)
 tests=sorted(str(p.relative_to(src)) for base in ('conf/codex-bridge/test','conf/cyf-agent-runtime-v1/test','conf/skills/native-image/test') for p in (src/base).glob('*.test.mjs'))
 node='/home/isp/apps/cyf-agent-runtime-v1/app/node/bin/node';cmd=[node,'--test','--test-concurrency=2',*tests]
 for n in ('home','tmp'):(out/n).mkdir(exist_ok=True)
 env={'PATH':str(P(node).parent)+':/usr/bin:/bin','HOME':str(out/'home'),'TMPDIR':str(out/'tmp'),'LANG':'C.UTF-8'}
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=src,text=True).strip();assert head=='6c8fc27314a17bdb778aaa5d69b9945837380a4a'
 start=time.time(); record={'sourceCommit':head,'sourceTree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],cwd=src,text=True).strip(),'command':cmd,'startedAt':start,'dependencyProvenance':{'method':'reuse verified Flow165 locked node_modules; normalized lock identical except root package metadata','archiveSha256':hashlib.sha256(archive.read_bytes()).hexdigest(),'previousSymlink':oldlink},'nodeVersion':subprocess.check_output([node,'--version'],text=True).strip()}
 (out/'inputs.json').write_text(json.dumps(record,indent=2)+'\n')
 with (out/'tests.log').open('wb') as log:r=subprocess.run(cmd,cwd=src,env=env,stdout=log,stderr=subprocess.STDOUT)
 record.update(exitCode=r.returncode,wallSeconds=round(time.time()-start,3),sourceUnchanged=subprocess.check_output(['git','rev-parse','HEAD'],cwd=src,text=True).strip()==head,testsLogSha256=hashlib.sha256((out/'tests.log').read_bytes()).hexdigest())
 (out/'result.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({k:v for k,v in record.items() if k!='command'},indent=2));raise SystemExit(r.returncode)
