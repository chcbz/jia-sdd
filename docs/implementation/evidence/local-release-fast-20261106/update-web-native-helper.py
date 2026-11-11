"""Prepare/test-exact or install LOCAL support without changing live state aliases."""
import fcntl,hashlib,json,os,stat,subprocess,sys,tempfile
from pathlib import Path
D=Path(__file__).resolve().parent;folder=D/'web-native-helpers';folder.mkdir(mode=0o700,exist_ok=True)
target=Path('/usr/local/sbin/cyf-web-flow-deploy');candidate=folder/target.name;backup=folder/(target.name+'.before')
sha=lambda b:hashlib.sha256(b).hexdigest()
if sys.argv[1:]==['--prepare']:
 old=target.read_bytes();assert not backup.exists() or backup.read_bytes()==old
 backup.write_bytes(old);backup.chmod(0o600)
 source=Path('/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-web-flow-deploy').read_bytes()
 # Keep the installed state root. Relocating the legacy bind alias is separate work.
 root_line=next(line for line in old.splitlines() if line.startswith(b'ROOT = Path('))
 source=source.replace(b"ROOT = Path('/home/isp/state/cyf-web-flow')",root_line)
 compile(source,str(candidate),'exec');candidate.write_bytes(source);candidate.chmod(0o755)
 (D/'web-native-helper-inputs.json').write_text(json.dumps(dict(target=str(target),beforeSha256=sha(old),candidateSha256=sha(source),candidate=str(candidate),backup=str(backup)),indent=2)+'\n')
else:
 assert sys.argv[1:]==['--install'];record=json.loads((D/'web-native-helper-inputs.json').read_text())
 locks=[]
 try:
  for p in ['/home/isp/state/cyf-web-flow/helper-upgrade.lock','/home/isp/state/cyf-web-flow/deploy.lock']:
   fd=os.open(p,os.O_RDWR|os.O_CREAT|os.O_NOFOLLOW,0o600);locks.append(fd);s=os.fstat(fd);assert stat.S_ISREG(s.st_mode) and s.st_uid==0 and stat.S_IMODE(s.st_mode)==0o600 and s.st_nlink==1;fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
  s=target.lstat();assert stat.S_ISREG(s.st_mode) and s.st_uid==0 and s.st_nlink==1 and stat.S_IMODE(s.st_mode)==0o755
  assert sha(target.read_bytes())==record['beforeSha256'] and sha(backup.read_bytes())==record['beforeSha256'] and sha(candidate.read_bytes())==record['candidateSha256']
  current=json.loads(Path('/home/isp/state/cyf-web-flow/record.json').read_text());assert current['status'] in ['installed','online_verified']
  fd,tmp=tempfile.mkstemp(prefix='.local-helper-',dir=str(target.parent))
  with os.fdopen(fd,'wb') as f:os.fchmod(f.fileno(),0o755);f.write(candidate.read_bytes());f.flush();os.fsync(f.fileno())
  os.replace(tmp,target);fd=os.open(str(target.parent),os.O_DIRECTORY);os.fsync(fd);os.close(fd)
  assert sha(target.read_bytes())==record['candidateSha256'];record.update(status='INSTALLED_VERIFIED',applicationTouched=False)
  (D/'web-native-helper-installation.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
 finally:
  for fd in locks:os.close(fd)
