from pathlib import Path
import os,fcntl,json,hashlib,tempfile,subprocess,datetime
root=Path('/home/isp/wsps/cyf');ev=root/'docs/implementation/evidence/runtime-footprint-20261109';base=Path('/usr/local/libexec/cyf')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old='0952197912885ffa697808fc8a36dec6e781b5e4061fc8105614056baeb0717d'
tested=json.loads((ev/'batch05-result.json').read_text());assert tested['inputUnchanged'] and all(x['exitCode']==0 for x in tested['commands'])
record=Path('/home/isp/apps/cyf-agent-runtime-v1/release-records/current.json')
unit='cyf-agent-runtime-v1@unified.service'
def observe():
 return {'recordSha256':sha(record),'service':subprocess.check_output(['systemctl','show',unit,'-p','MainPID','-p','ActiveState','-p','NRestarts']).decode()}
before=observe();fds=[];changes=[]
try:
 for lock in ('/run/lock/cyf-host-cleanup.lock','/run/lock/cyf-wuyong-versioned-release.lock'):
  fd=os.open(lock,os.O_RDWR|os.O_NOFOLLOW);fds.append(fd);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
  assert os.fstat(fd).st_ino==os.lstat(lock).st_ino
 assert sha(base/'runtime_backup_cleanup.py')==old,'installed helper changed by another owner'
 assert sha(base/'runtime_backup_scope.py')=='496da8c079eeadc598914af1bfe56822e78d5b44c1c977d1b7c74eb2ee1bb735','scope module changed; reconcile'
 saved=ev/'installed-helper.intermediate.py';saved.write_bytes((base/'runtime_backup_cleanup.py').read_bytes());saved.chmod(0o600)
 for name in ('runtime_backup_scope.py','runtime_backup_cleanup.py'):
  src=root/'ops/maintenance'/name;dest=base/name
  assert sha(src)==tested['inputHashes'][str(src)]
  fd,tmp=tempfile.mkstemp(prefix='.'+name+'-',dir=str(base))
  with os.fdopen(fd,'wb') as f:f.write(src.read_bytes());f.flush();os.fchmod(f.fileno(),0o755 if name.endswith('cleanup.py') else 0o644);os.fchown(f.fileno(),0,0);os.fsync(f.fileno())
  os.replace(tmp,str(dest));assert sha(dest)==sha(src)
  changes.append({'path':str(dest),'sha256':sha(dest)})
 fd=os.open(str(base),os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
finally:
 for fd in reversed(fds):os.close(fd)
after=observe();result={'installedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'changes':changes,'before':before,'after':after,'productionRecordAndServiceUnchanged':before==after,'automaticBackupSelectionChanged':False}
(ev/'helper-installation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
