from pathlib import Path
import os,fcntl,hashlib,json,shutil,stat,subprocess
E=Path(__file__).resolve().parent

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def inventory(root):
 out={}
 for p in sorted(root.rglob('*')):
  st=p.lstat();row={'mode':stat.S_IMODE(st.st_mode)}
  if p.is_symlink():row['symlink']=os.readlink(p)
  elif p.is_file():row.update(size=st.st_size,sha256=sha(p))
  elif p.is_dir():row['directory']=True
  else:raise ValueError('unexpected toolchain node')
  out[str(p.relative_to(root))]=row
 return out
fd=os.open('/run/lock/cyf-host-cleanup.lock',os.O_RDWR|os.O_NOFOLLOW);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
source=Path('/dev/shm/cyf-local-toolchain/dragonwell-21.0.11.0.11+10-GA');dest=Path('/opt/cyf/toolchains')/source.name
assert source.is_dir() and not dest.exists()
dest.parent.mkdir(parents=True,exist_ok=True,mode=0o755);before=inventory(source);stage=dest.with_name(dest.name+'.staging');assert not stage.exists();shutil.copytree(str(source),str(stage),symlinks=True);assert inventory(stage)==before;os.rename(stage,dest)
subprocess.check_call([str(dest/'bin/java'),'-version'])
record={'jdk':{'from':str(source),'to':str(dest),'files':before},'packages':[]}
# Exact immutable package mirrors; original installation records are not rewritten.
for label,origin,result_path,component in [
 ('api-current','/dev/shm/cyf-full-local-20261107-01/api/package/api.tgz','/dev/shm/cyf-full-local-20261107-01/api/result.json','api'),
 ('api-rollback','/dev/shm/cyf-local-fast-api-20261107-08/package/api.tgz','/dev/shm/cyf-local-fast-api-20261107-08/result.json','api'),
 ('web-current','/dev/shm/cyf-full-local-20261107-01/web/package/web.tgz','/dev/shm/cyf-full-local-20261107-01/web/result.json','web')]:
 original=Path(origin);task=Path('/var/tmp/cyf-local-archive-20261107-'+label);assert not task.exists();(task/'package').mkdir(parents=True,mode=0o700);task.chmod(0o700)
 target=task/'package'/original.name;shutil.copyfile(str(original),str(target));target.chmod(0o600);assert sha(original)==sha(target)
 result=json.loads(Path(result_path).read_text());(task/'result.json').write_text(json.dumps(result,indent=2)+'\n');source_identity=result['source']
 item={'component':component,'from':str(original),'path':str(target),'size':target.stat().st_size,'sha256':sha(target),'source':source_identity,'sourceResult':result_path}
 if component=='api':item['payloadSha256']=result['package']['applicationJarSha256']
 record['packages'].append(item)
 (task/'archive.json').write_text(json.dumps(item,indent=2)+'\n')
# Retain a durable move receipt before retiring the verified cache duplicate.
(E/'persistent-inputs.json').write_text(json.dumps(record,indent=2)+'\n');assert inventory(source)==before;shutil.rmtree(str(source));source.parent.rmdir()
cache=Path('/var/tmp/cyf-local-build-timing-20261106/gradle-home');newcache=Path('/home/isp/state/cyf-local-build/gradle-home');assert not newcache.exists();newcache.parent.mkdir(mode=0o700,parents=True,exist_ok=True);os.rename(cache,newcache)
record['gradleCache']={'from':str(cache),'to':str(newcache),'method':'same-filesystem atomic directory rename; bytes/inodes preserved'}
(E/'persistent-inputs.json').write_text(json.dumps(record,indent=2)+'\n');os.close(fd)
print(json.dumps({'jdk':str(dest),'gradleCache':str(newcache),'archives':[x['path'] for x in record['packages']]},indent=2))
