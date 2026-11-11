from pathlib import Path
import os,stat,fcntl,hashlib,json,importlib.util,subprocess,datetime
R=Path('/home/isp/wsps/cyf');E=R/'docs/implementation/evidence/local-release-closure-20261107';B=E/'directory-layout-before';B.mkdir(exist_ok=False)
old=Path('/home/isp/wsps/private-maintenance');packages=Path('/home/isp/pkgs/cyf');archive=Path('/home/isp/baks/private-maintenance');empty=Path('/home/isp/wsps/cyf-worktrees')
assert old.resolve()==old and old.is_dir() and not packages.exists() and not archive.exists()
spec=importlib.util.spec_from_file_location('layout_cleanup',str(R/'ops/maintenance/rebuildable_cache_cleanup.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
sha=lambda b:hashlib.sha256(b).hexdigest()
def manifest(root):
 rows={}
 for p in sorted(root.rglob('*')):
  s=p.lstat();rel=str(p.relative_to(root));assert '.git' not in p.relative_to(root).parts and not stat.S_ISLNK(s.st_mode)
  row={'mode':stat.S_IMODE(s.st_mode),'uid':s.st_uid,'gid':s.st_gid,'device':s.st_dev,'inode':s.st_ino,'links':s.st_nlink}
  if stat.S_ISDIR(s.st_mode):row['type']='directory'
  else:
   assert stat.S_ISREG(s.st_mode);row.update(type='file',size=s.st_size,sha256=sha(p.read_bytes()))
  rows[rel]=row
 return rows
fds=[]
try:
 for name in ['/run/lock/cyf-host-cleanup.lock','/tmp/cyf-api-flow-auto-approval-v2.lock','/tmp/cyf-release-api.lock','/home/isp/state/cyf-web-flow/deploy.lock']:
  fd=os.open(name,os.O_RDWR|os.O_NOFOLLOW);s=os.fstat(fd);assert stat.S_ISREG(s.st_mode) and s.st_uid==0 and s.st_nlink==1;fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);assert os.stat(name).st_ino==s.st_ino;fds.append(fd)
 paths=m.Paths();assert not m.mounted(paths,old) and not m.mounted(paths,empty)
 assert not m.proc.snapshot().used(old) and not m.proc.snapshot().used(empty)
 before=manifest(old);(E/'directory-layout-inventory.json').write_text(json.dumps(before,sort_keys=True,indent=2)+'\n')
 registry=paths.registry;raw=registry.read_bytes();entries=m.read_registry(paths);newentries=json.loads(json.dumps(entries));moves=[]
 for name in ['cyf-local-archive-20261107-api-current','cyf-local-archive-20261107-api-rollback','cyf-local-archive-20261107-web-current']:
  src=old/name;dst=packages/name;matching=[x for x in newentries if x['task_root']==str(src)];assert len(matching)==1
  entry=matching[0];s=src.lstat();assert (s.st_dev,s.st_ino)==(entry['device'],entry['inode'])
  for f in entry['artifacts']['files']:
   p=src/f['relative_path'];assert m.signature(p.lstat())==tuple(f['signature']) and sha(p.read_bytes())==f['sha256']
  entry['task_root']=str(dst);moves.append({'from':str(src),'to':str(dst)})
 assert registry.read_bytes()==raw and not m.proc.snapshot().used(old)
 helper=Path('/usr/local/libexec/cyf/rebuildable_cache_cleanup.py');beforehelper=helper.read_bytes();source=(R/'ops/maintenance/rebuildable_cache_cleanup.py').read_bytes();assert beforehelper!=source
 (B/'rebuildable_cache_cleanup.py').write_bytes(beforehelper);(B/'completed-tasks.json').write_bytes(raw)
 for p in B.iterdir():p.chmod(0o600)
 record={'status':'prepared','startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'packageMoves':moves,'historyMove':{'from':str(old),'to':str(archive)},'emptyLegacyWorktrees':str(empty),'inventorySha256':sha(json.dumps(before,sort_keys=True).encode()),'originalEntries':len(before),'sourceHelperSha256':sha(source),'installedBeforeSha256':sha(beforehelper),'registryBeforeSha256':sha(raw),'preserveCompletionTimes':True,'productionRecordsBefore':{n:sha(Path(n).read_bytes()) for n in ['/home/isp/state/cyf-api-flow/record.json','/home/isp/state/cyf-web-flow/record.json']}}
 proof=E/'directory-layout-migration.json';proof.write_text(json.dumps(record,indent=2)+'\n')
 packages.mkdir(mode=0o700);assert packages.lstat().st_dev==old.lstat().st_dev and archive.parent.stat().st_dev==old.lstat().st_dev
 for move in moves:os.rename(move['from'],move['to'])
 remaining=sorted(p.name for p in old.iterdir());os.rename(old,archive)
 # Reassemble the original manifest by original relative names; all bytes, modes,
 # owners and inodes must survive the same-filesystem directory renames.
 after=manifest(archive)
 for move in moves:
  task=Path(move['to']);taskrow=before[task.name];s=task.lstat();assert (s.st_dev,s.st_ino)==(taskrow['device'],taskrow['inode']);after[task.name]=taskrow
  after.update({task.name+'/'+k:v for k,v in manifest(task).items()})
 assert after==before
 for entry in newentries:
  if str(packages)+'/' in entry['task_root']:
   task=m.task_root(paths,Path(entry['task_root']));assert (task.stat().st_dev,task.stat().st_ino)==(entry['device'],entry['inode'])
 assert registry.read_bytes()==raw;m.atomic_json(registry,{'version':1,'tasks':newentries})
 temp=helper.with_name('.rebuildable_cache_cleanup.layout');fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o755)
 with os.fdopen(fd,'wb') as out:out.write(source);out.flush();os.fsync(out.fileno())
 assert helper.read_bytes()==beforehelper;os.replace(temp,helper);assert helper.read_bytes()==source
 assert empty.exists() and not list(empty.iterdir());empty.rmdir()
 for n,h in record['productionRecordsBefore'].items():assert sha(Path(n).read_bytes())==h
 record.update(status='verified',completedAt=datetime.datetime.now(datetime.timezone.utc).isoformat(),allOriginalFilesAndInodesVerified=True,historyTasksPreserved=remaining,registeredTasks=len(newentries),registryAfterSha256=sha(registry.read_bytes()),oldPrivatePathAbsent=not old.exists(),emptyWorktreesRemoved=not empty.exists(),productionRecordsUnchanged=True,noWorktreeMoved=True)
 proof.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
finally:
 for fd in reversed(fds):os.close(fd)
