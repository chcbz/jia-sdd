"""One-off Owner retirement of exactly three abandoned generated JARs.
Not a final-package retention bypass: no package/ archives or backups are removed.
"""
from pathlib import Path
import importlib.util,json,os,fcntl,time,shutil
E=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('cleanup','/usr/local/libexec/cyf/rebuildable_cache_cleanup.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);p=m.Paths()
s=importlib.util.spec_from_file_location('flow','/usr/local/libexec/cyf/flow_host_cleanup.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
items=[('/var/tmp/cyf-local-build-timing-20261106','api-build/jia/starter/libs/starter-1.1.37-SNAPSHOT.jar'),('/var/tmp/cyf-local-fast-api-20261107-04','build/jia/starter/libs/starter-1.1.37-SNAPSHOT.jar'),('/var/tmp/cyf-local-fast-api-20261107-06','build/jia/starter/libs/starter-1.1.37-SNAPSHOT.jar')]
fd=os.open(p.lock,os.O_RDWR|os.O_NOFOLLOW);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
with f.locked(f.Paths()):
 api,api_sig=f.read_state(f.Paths());web,web_sig=f.read_web_state(f.Paths());protected={api['candidate_sha256'],api['previous_sha256']}
 rows=[]
 for task_name,rel in items:
  task=Path(task_name);file=task/rel;build=task/rel.split('/')[0];dst=E/'retired-intermediate-evidence'/task.name;dst.mkdir(parents=True,exist_ok=True)
  for name in ['result.json','inputs.json','gradle.log']:
   if (task/name).is_file():shutil.copyfile(task/name,dst/name)
  for pattern in ['local-bootjar-proof.json','opencv-resolved.json','jia/*/test-results/*/TEST-*.xml']:
   for src in build.glob(pattern):
    dest=dst/src.relative_to(build);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
  st=m.guard(p,file,task);digest=m.digest(file,m.signature(st));assert digest not in protected
  assert not m.used(m.proc.snapshot(p.proc),task)
  rows.append(dict(path=str(file),root=str(task),task=str(task),signature=m.signature(st),sha256=digest,allocated=st.st_blocks*512,cutoff=time.time()+1,completed_at=None,root_identity=(task.stat().st_dev,task.stat().st_ino),task_identity=(task.stat().st_dev,task.stat().st_ino)))
 intent=E/'retired-build-intermediates.json';m.atomic_json(intent,{'status':'INTENT','scope':'exact Owner-abandoned build intermediates; packages/backups protected','rows':rows})
 for row in rows:
  assert f.read_state(f.Paths())[1]==api_sig and f.read_web_state(f.Paths())[1]==web_sig
  m.unlink_row(p,row,m.proc.snapshot(p.proc))
 m.atomic_json(intent,{'status':'REMOVED','allocatedBytes':sum(r['allocated'] for r in rows),'rows':rows,'protectedRollback':api['backup']})
os.close(fd);print('Retired intermediates bytes:',sum(r['allocated'] for r in rows))
