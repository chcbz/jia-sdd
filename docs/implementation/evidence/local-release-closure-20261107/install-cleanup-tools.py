import pathlib,os,fcntl,hashlib,json,stat
R=pathlib.Path('/home/isp/wsps/cyf');E=pathlib.Path(__file__).parent;B=E/'maintenance-before';B.mkdir(exist_ok=True)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
lock=pathlib.Path('/run/lock/cyf-host-cleanup.lock');fd=os.open(lock,os.O_RDWR|os.O_NOFOLLOW)
fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
assert os.fstat(fd).st_ino==lock.stat().st_ino
rows=[]
for src,dst in [('ops/maintenance/flow_host_cleanup.py','/usr/local/libexec/cyf/flow_host_cleanup.py'),('ops/maintenance/rebuildable_cache_cleanup.py','/usr/local/libexec/cyf/rebuildable_cache_cleanup.py'),('ops/maintenance/clear_disk.host.sh','/home/isp/bin/clear_disk.sh')]:
 s=R/src;d=pathlib.Path(dst);st=d.lstat();assert stat.S_ISREG(st.st_mode) and st.st_uid==0 and st.st_nlink==1
 before=sha(d);backup=B/d.name;assert not backup.exists();backup.write_bytes(d.read_bytes());backup.chmod(0o600)
 temp=d.with_name('.'+d.name+'.local-closure');f=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o755)
 with os.fdopen(f,'wb') as stream:stream.write(s.read_bytes());stream.flush();os.fchmod(stream.fileno(),0o755);os.fsync(stream.fileno())
 assert sha(d)==before;os.replace(temp,d);assert sha(d)==sha(s)
 rows.append({'source':str(s),'installed':str(d),'beforeSha256':before,'afterSha256':sha(d),'backup':str(backup)})
(E/'maintenance-installation.json').write_text(json.dumps(rows,indent=2)+'\n');os.close(fd);print(json.dumps(rows,indent=2))
