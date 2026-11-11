from pathlib import Path,PurePosixPath
import os,fcntl,json,hashlib,subprocess,shutil,stat
D=Path(__file__).resolve().parent;ROOT=Path('/home/isp/state/cyf-web-flow');SITE=Path('/home/isp/hosts/cyf/web/kit');BACK=Path('/home/isp/baks/cyf-web-flow/20261102-task-agent-filter')
lock=os.open(str(ROOT/'deploy.lock'),os.O_RDWR|os.O_NOFOLLOW);fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
old=(ROOT/'record.json').read_bytes();r=json.loads(old);assert r['run_id']=='401' and r['commit']=='5470363fc33d7689890763a54eb0ee23ac8d84d2'
BACK.mkdir(mode=0o700,parents=True,exist_ok=False);(BACK/'record.json').write_bytes(old)
names=[]
for e in r['files']:
 p=PurePosixPath(e['path']);assert not p.is_absolute() and '..' not in p.parts and '\x00' not in e['path'];actual=SITE/e['path'];assert actual.is_file() and not actual.is_symlink();names.append(e['path'])
assert 'index.html' in names
(BACK/'files.list').write_bytes(b'\0'.join(n.encode() for n in names)+b'\0')
subprocess.run(['tar','--acls','--xattrs','-I','gzip -1','-cf',str(BACK/'site.tar.gz'),'-C',str(SITE),'--null','-T',str(BACK/'files.list')],check=True)
subprocess.run(['tar','--acls','--xattrs','--compare','-zf',str(BACK/'site.tar.gz'),'-C',str(SITE)],check=True)
h=hashlib.sha256()
with (BACK/'site.tar.gz').open('rb') as f:
 for b in iter(lambda:f.read(1048576),b''):h.update(b)
result={'backup':str(BACK),'archiveSha256':h.hexdigest(),'previousRun':r['run_id'],'previousCommit':r['commit'],'files':len(names),'recordSha256':hashlib.sha256(old).hexdigest()};(D/'backup.json').write_text(json.dumps(result,indent=2)+'\n')
(BACK/'RECOVERY.md').write_text('Retain this verified prior site and record. Under existing deploy.lock, preserve new hashed assets and restore prior files assets first and index.html last only after checking API compatibility; Do not roll back API or business state automatically. This archive is not a newly built release.\n')
print(json.dumps(result))
