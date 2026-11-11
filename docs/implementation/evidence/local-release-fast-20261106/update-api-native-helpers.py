"""Reversible, digest-bound local update; no application lifecycle operations."""
import contextlib,fcntl,hashlib,json,os,stat,tempfile,time
from pathlib import Path
D=Path(__file__).resolve().parent
rows=json.loads((D/'api-native-helper-update-inputs.json').read_text())
sha=lambda data:hashlib.sha256(data).hexdigest()
def read(p):
 p=Path(p);st=p.lstat();assert stat.S_ISREG(st.st_mode) and st.st_uid==0 and st.st_nlink==1 and not st.st_mode&0o022;return p.read_bytes()
def atomic(p,b):
 fd,n=tempfile.mkstemp(prefix='.native-local-update-',dir=str(p.parent))
 try:
  with os.fdopen(fd,'wb') as f:os.fchmod(f.fileno(),0o755);f.write(b);f.flush();os.fsync(f.fileno())
  os.replace(n,p);fd=os.open(str(p.parent),os.O_DIRECTORY);os.fsync(fd);os.close(fd)
 finally:
  if os.path.exists(n):os.unlink(n)
report={'status':'PREPARING','sourceKind':'LOCAL','applicationTouched':False,'targets':rows}
with contextlib.ExitStack() as stack:
 for path in ['/tmp/cyf-api-flow-auto-approval-v2.lock','/tmp/cyf-release-api.lock']:
  fd=os.open(path,os.O_RDWR|os.O_NOFOLLOW);stack.callback(os.close,fd);st=os.fstat(fd);assert stat.S_ISREG(st.st_mode) and st.st_uid==0 and st.st_nlink==1
  # Do not wait behind an unrelated active release; retry only after reinspection.
  fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
 current=json.loads(Path('/home/isp/state/cyf-api-flow/record.json').read_text());assert current['status']=='installed'
 for r in rows:
  assert sha(read(r['path']))==r['beforeSha256'];assert sha(read(r['candidate']))==r['candidateSha256'];assert sha(Path(r['backup']).read_bytes())==r['beforeSha256']
 done=[]
 try:
  for r in rows:
   atomic(Path(r['path']),read(r['candidate']));done.append(r);assert sha(read(r['path']))==r['candidateSha256']
 except BaseException:
  for r in reversed(done):atomic(Path(r['path']),Path(r['backup']).read_bytes())
  raise
 report.update(status='INSTALLED_VERIFIED',verifiedAt=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()))
 (D/'api-native-helper-installation.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
