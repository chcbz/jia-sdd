"""Task-only recovery of interrupted stream using the existing v2 manifest; never installs."""
import datetime,fcntl,gzip,hashlib,json,os,pathlib,shutil,subprocess,sys,tarfile,time
P=pathlib.Path; T=time.monotonic()
ROOT=P('/home/isp/state/cyf-local-build/tasks/JUYITING-HELP-20261109'); S=ROOT/'source'; B=ROOT/'build-final'; O=ROOT/'finish-package'
sys.path.insert(0,'/home/isp/wsps/cyf/ops/orchestration')
from build_storage import require_disk
from web_dependencies import verify
O.mkdir(mode=0o700); R={'status':'RUNNING','startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authorization':'User: 继续完成; previously requested additional 180 seconds','priorResult':str(B/'result.json'),'deploymentPerformed':False}
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''): h.update(b)
 return h.hexdigest()
def git(*a):return subprocess.check_output(['git','-C',str(S),*a],text=True).strip()
try:
 for p in (S,B,O):require_disk(p)
 old=json.loads((B/'result.json').read_text()); m=json.loads((B/'manifest.json').read_text())
 assert old['source']==m['source']=={'commit':'1c942b0a822392a78df582949d6a07032d0d9e0f','tree':'8048bc8d1466a91033fd064db81a19252a7ae5d6'}
 assert git('rev-parse','HEAD')==m['source']['commit'] and git('rev-parse','HEAD^{tree}')==m['source']['tree'] and not git('status','--porcelain')
 assert sha(S/'package-lock.json')==old['lockSha256']
 for p,h in old['tools'].items():assert sha(P('/home/isp/wsps/cyf')/p)==h,p
 assert sha(P('/home/isp/apps/node/bin/node').resolve())==old['nodeBinarySha256']
 assert sha(B/'test-reports/mochawesome.json')==m['tests']['reportSha256']
 assert m['tests']['stats']['failures']==0 and m['tests']['stats']['passes']==87
 assert all(any(s['name']==n and s.get('exitCode')==0 for s in old['stages']) for n in ('tests','build'))
 R.update(source=m['source'],version=m['version'],tests=m['tests'],priorResultSha256=sha(B/'result.json'),manifestSha256=sha(B/'manifest.json'),recoveryScriptSha256=sha(P(__file__)))
 with open('/tmp/cyf-gradle.lock','a+') as lock:
  t=time.monotonic();fcntl.flock(lock,fcntl.LOCK_EX);R['queueSeconds']=round(time.monotonic()-t,3)
  verify(P(old['dependencies']['path']),old['dependencies']['inputs'])
  recovered=O/'recovered';recovered.mkdir();files={};seen=set()
  # No extractall: accept only manifest-listed regular members and verify each byte.
  try:
   with tarfile.open(B/'package/web.tgz','r|gz') as tar:
    for item in tar:
     assert item.isfile() and item.name not in seen;seen.add(item.name)
     if item.name=='cyf-local-build.json':continue
     assert item.name in m['files'] and not P(item.name).is_absolute() and '..' not in P(item.name).parts
     p=recovered/item.name;p.parent.mkdir(parents=True,exist_ok=True)
     with tar.extractfile(item) as src,p.open('wb') as dst:shutil.copyfileobj(src,dst)
     assert {'sha256':sha(p),'size':p.stat().st_size}==m['files'][item.name]
     files[item.name]=p
  except (EOFError,tarfile.ReadError) as e:
   R['interruptedArchiveRead']=str(e)
  R['recoveredVerifiedMembers']=len(files)
  # Public files remain in the fixed clean source and can fill an interrupted tail.
  for n,meta in m['files'].items():
   if n not in files:
    p=S/'public'/n
    assert p.is_file() and not p.is_symlink(), 'missing built output: '+n
    assert {'sha256':sha(p),'size':p.stat().st_size}==meta,n
    files[n]=p
  assert set(files)==set(m['files'])
  R['sourcePublicMembers']=len(files)-R['recoveredVerifiedMembers']
  pkg=O/'web.tgz'
  with pkg.open('wb') as raw,gzip.GzipFile(fileobj=raw,mode='wb',compresslevel=1,mtime=0) as gz,tarfile.open(fileobj=gz,mode='w|') as tar:
   for n,p in sorted(files.items()):tar.add(p,arcname=n,recursive=False)
   tar.add(B/'manifest.json',arcname='cyf-local-build.json',recursive=False)
  with tarfile.open(pkg,'r:gz') as tar:
   seen=set()
   for item in tar:
    assert item.isfile() and item.name not in seen;seen.add(item.name)
    h=hashlib.sha256();length=0
    with tar.extractfile(item) as f:
     for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk);length+=len(chunk)
    if item.name=='cyf-local-build.json':assert h.hexdigest()==R['manifestSha256']
    else:assert {'sha256':h.hexdigest(),'size':length}==m['files'][item.name]
   assert seen==set(m['files'])|{'cyf-local-build.json'}
  assert not git('status','--porcelain')
  R.update(status='BUILT',artifact={'path':str(pkg),'sha256':sha(pkg)},sourceUnchanged=True,integrityVerifiedFiles=len(files),reusedStages=['tests','build'],scope=old['scope'])
except Exception as e:
 R.update(status='FAIL',error=repr(e));raise
finally:
 R['additionalSeconds']=round(time.monotonic()-T,3)
 (O/'result.json').write_text(json.dumps(R,indent=2,ensure_ascii=False))
 print(json.dumps(R,indent=2,ensure_ascii=False))
