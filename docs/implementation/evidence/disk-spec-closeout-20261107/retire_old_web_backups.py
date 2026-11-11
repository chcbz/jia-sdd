"""Retire only three explicitly reviewed obsolete Web payloads; retain records."""
import pathlib,json,hashlib,os,fcntl,sys,stat
sys.path.insert(0,'/usr/local/libexec/cyf')
from host_cleanup_processes import snapshot
base=pathlib.Path(__file__).resolve().parent
locks=[]
for p in ['/run/lock/cyf-host-cleanup.lock','/home/isp/state/cyf-web-flow/deploy.lock']:
 f=open(p,'r+');fcntl.flock(f,fcntl.LOCK_EX|fcntl.LOCK_NB);locks.append(f)
current=pathlib.Path('/home/isp/state/cyf-web-flow/record.json');current_bytes=current.read_bytes();record=json.loads(current_bytes)
assert record['phase']=='online_verified'
pin=pathlib.Path(record['backup']).resolve();assert pin.is_dir()
names=['cyf-archive-reader-icons-release-20261106','cyf-reader-icons-narrow-release-20261106','cyf-reader-toolbar-alignment-release-20261106']
results=[]
for name in names:
 root=pathlib.Path('/home/isp/baks')/name
 assert root.resolve()==root and root!=pin and not root.is_symlink()
 assert not list(root.rglob('.keep')) and not snapshot().used(root)
 manifest=root/('backup.json' if (root/'backup.json').exists() else 'record.json')
 data=json.loads(manifest.read_bytes());payload=root/'site' if manifest.name=='backup.json' else root
 plan=[]
 for entry in data['files']:
  rel=pathlib.PurePosixPath(entry['path']);assert not rel.is_absolute() and '..' not in rel.parts
  p=payload/rel
  st=p.lstat();assert stat.S_ISREG(st.st_mode) and st.st_nlink==1 and not os.path.ismount(p)
  assert p.resolve()==p and hashlib.sha256(p.read_bytes()).hexdigest()==entry['sha256']
  plan.append((p,st,entry['sha256']))
 assert current.read_bytes()==current_bytes
 audit={'root':str(root),'manifest_sha256':hashlib.sha256(manifest.read_bytes()).hexdigest(),'files':len(plan),'allocated_bytes':sum(s.st_blocks*512 for _,s,_ in plan),'protected_current_backup':str(pin)}
 with (base/'backup-removal-audit.jsonl').open('a') as f:f.write(json.dumps(audit)+'\n');f.flush();os.fsync(f.fileno())
 usage=snapshot();assert not usage.used(root)
 for p,st,sha in plan:
  now=p.lstat();assert (now.st_ino,now.st_size,now.st_mtime_ns,now.st_nlink)==(st.st_ino,st.st_size,st.st_mtime_ns,st.st_nlink)
  assert not usage.used(p)
  p.unlink()
 audit['result']='payload-retired';results.append(audit)
 (root/'PAYLOAD_RETIRED.json').write_text(json.dumps(audit,indent=2)+'\n')
 (base/'backups-retired.json').write_text(json.dumps(results,indent=2)+'\n')
 print(name,len(plan),audit['allocated_bytes'],flush=True)
assert current.read_bytes()==current_bytes
