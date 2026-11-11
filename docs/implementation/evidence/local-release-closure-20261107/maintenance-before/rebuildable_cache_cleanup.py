#!/usr/bin/python3
"""Bounded inactive Gradle caches and explicitly completed task dependencies.
No source/database/release scanning. Completion is declared, never inferred from idle.
"""
import argparse, fcntl, hashlib, importlib.util, json, os, re, stat, sys, time, uuid
from pathlib import Path

def module(name, file):
 s=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
proc=module('cache_processes','/usr/local/libexec/cyf/host_cleanup_processes.py')
logger=module('cache_audit_logger','/usr/local/libexec/cyf/host_cleanup_log.py')
MAX_ENTRIES=200000
class Unsafe(RuntimeError):pass
class Paths:
 def __init__(self):
  self.cache=Path('/root/.gradle/caches')
  self.state=Path('/home/isp/state/cyf-host-cleanup')
  self.registry=self.state/'completed-tasks.json'
  self.audit=Path('/home/isp/baks/host-cleanup/rebuildable-cache/audit.jsonl')
  self.lock=Path('/run/lock/cyf-host-cleanup.lock')
  self.mountinfo=Path('/proc/self/mountinfo')
  self.proc=Path('/proc')
  self.task_bases=[Path(x) for x in ['/tmp','/var/tmp','/home/isp/wsps/worktrees','/home/isp/wsps/private-maintenance','/home/isp/wsps/cyf/.worktrees']]
  self.root_device=os.stat('/').st_dev
  self._mount_text=None;self._mounts=[]
def signature(s):return (s.st_dev,s.st_ino,s.st_mode,s.st_uid,s.st_gid,s.st_nlink,s.st_size,s.st_mtime_ns,s.st_ctime_ns)
def physical(p, write=False):
 s=p.lstat()
 if not stat.S_ISDIR(s.st_mode) or s.st_uid!=0 or s.st_mode&0o002 or (s.st_mode&0o020 and s.st_gid!=0):raise Unsafe('unsafe directory: '+str(p))
 return s
def regular(p):
 s=p.lstat()
 if not stat.S_ISREG(s.st_mode) or s.st_uid!=0 or s.st_mode&0o022 or s.st_nlink!=1:raise Unsafe('unsafe regular file: '+str(p))
 return s
def digest(p,expected,directory=None):
 fd=os.open(str(p) if directory is None else p.name,os.O_RDONLY|os.O_NOFOLLOW,dir_fd=directory)
 with os.fdopen(fd,'rb') as f:
  if signature(os.fstat(f.fileno()))!=tuple(expected):raise Unsafe('file changed before content verification')
  h=hashlib.sha256();remaining=expected[6]
  while remaining:
   b=f.read(min(1024*1024,remaining))
   if not b:raise Unsafe('file shortened while hashing')
   h.update(b);remaining-=len(b)
  if f.read(1) or signature(os.fstat(f.fileno()))!=tuple(expected):raise Unsafe('file changed while hashing')
  return h.hexdigest()
def read_registry(paths):
 if not os.path.lexists(str(paths.registry)):return []
 physical(paths.state);s=regular(paths.registry)
 if s.st_size>1024*1024:raise Unsafe('oversized completion registry')
 fd=os.open(str(paths.registry),os.O_RDONLY|os.O_NOFOLLOW)
 with os.fdopen(fd) as f:
  if signature(os.fstat(f.fileno()))!=signature(s):raise Unsafe('registry replaced')
  v=json.load(f)
  if signature(os.fstat(f.fileno()))!=signature(s) or signature(paths.registry.lstat())!=signature(s):raise Unsafe('registry changed')
 if not isinstance(v,dict) or v.get('version')!=1 or not isinstance(v.get('tasks'),list) or len(v['tasks'])>256:raise Unsafe('invalid completion registry')
 if any(not isinstance(e,dict) for e in v['tasks']):raise Unsafe('invalid registry entry')
 return v['tasks']
def atomic_json(p,v):
 d=logger.open_parent(p);temp='.'+p.name+'.'+uuid.uuid4().hex
 try:
  try:before=os.stat(p.name,dir_fd=d,follow_symlinks=False);logger.safe_log_stat(before);identity=(before.st_dev,before.st_ino)
  except FileNotFoundError:identity=None
  fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600,dir_fd=d)
  with os.fdopen(fd,'w') as f:json.dump(v,f);f.flush();os.fsync(f.fileno())
  try:s=os.stat(p.name,dir_fd=d,follow_symlinks=False);logger.safe_log_stat(s);now=(s.st_dev,s.st_ino)
  except FileNotFoundError:now=None
  if now!=identity:raise Unsafe('registry/status replaced')
  os.replace(temp,p.name,src_dir_fd=d,dst_dir_fd=d);os.fsync(d)
 finally:
  try:os.unlink(temp,dir_fd=d)
  except FileNotFoundError:pass
  os.close(d)
def mounted(paths,p):
 text=paths.mountinfo.read_text()
 if text!=paths._mount_text:
  paths._mount_text=text;paths._mounts=[]
  for line in text.splitlines():
   fields=line.split()
   if len(fields)<6:raise Unsafe('invalid mount metadata')
   paths._mounts.append(re.sub(r'\\([0-7]{3})',lambda m:chr(int(m.group(1),8)),fields[4]))
 name=str(p)
 return any(m!='/' and (name==m or name.startswith(m.rstrip('/')+'/')) for m in paths._mounts)
def guard(paths,p,root):
 if root not in p.parents:raise Unsafe('outside artifact root')
 if mounted(paths,p):raise Unsafe('mounted artifact')
 for d in p.parents:
  s=d.lstat()
  if not stat.S_ISDIR(s.st_mode):raise Unsafe('symlink/non-directory ancestor')
  if os.path.lexists(str(d/'.keep')):raise Unsafe('keep marker')
  if d==root or root in d.parents:physical(d)
 s=regular(p)
 if s.st_dev!=paths.root_device:raise Unsafe('wrong device')
 return s
def used(u,p):
 s=p.stat()
 if not hasattr(u,'ancestor_names'):
  u.ancestor_names=set(u.paths)
  for n in u.paths:u.ancestor_names.update(str(parent) for parent in Path(n).parents)
 return (s.st_dev,s.st_ino) in u.inodes or str(p) in u.ancestor_names

def task_root(paths,p):
 if not p.is_absolute() or '..' in p.parts or p.parent not in paths.task_bases:raise Unsafe('task outside explicit bases')
 if p.parent in paths.task_bases[:2] and not re.fullmatch(r'cyf-[A-Za-z0-9_.-]+',p.name):raise Unsafe('unrecognized temporary task')
 if str(p.resolve())!=str(p):raise Unsafe('symlink task path')
 physical(p)
 if mounted(paths,p):raise Unsafe('mounted task')
 if os.path.lexists(str(p/'.keep')):raise Unsafe('task keep marker')
 return p

def dependency_root(task,rel):
 if not isinstance(rel,str):raise Unsafe('invalid dependency declaration')
 p=Path(rel)
 if p.is_absolute() or any(x in ('..','.','') for x in rel.split('/')) or len(p.parts)>3 or p.name!='node_modules' or any(x=='node_modules' or x.startswith('.') for x in p.parts[:-1]):raise Unsafe('only explicit node_modules roots supported')
 root=task/p;physical(root)
 # Require reproducible NPM project evidence, never infer completion from inactivity.
 regular(root.parent/'package-lock.json');regular(root.parent/'package.json')
 return root

def mark_complete(paths,task,rels):
 task=task_root(paths,task);u=proc.snapshot(paths.proc)
 if used(u,task):raise Unsafe('task still active')
 if not rels or len(rels)>8:raise Unsafe('declare 1..8 dependency roots')
 roots=[dependency_root(task,r) for r in sorted(set(rels))]
 for root in roots:
  if os.path.lexists(str(root/'.keep')):raise Unsafe('dependency keep marker')
 st=task.lstat();entries=read_registry(paths)
 entries=[e for e in entries if e.get('task_root')!=str(task)]
 if len(entries)>=256:raise Unsafe('completion registry full')
 entries.append({'task_root':str(task),'device':st.st_dev,'inode':st.st_ino,'completed_at':time.time(),'dependencies':[str(r.relative_to(task)) for r in roots]})
 if not paths.state.exists():paths.state.mkdir(mode=0o700)
 physical(paths.state);atomic_json(paths.registry,{'version':1,'tasks':entries})
 return {'registered':str(task),'dependency_roots':[str(r) for r in roots]}

def scopes(paths,now,cache_days,task_hours):
 out=[];skips=[]
 if paths.cache.exists():
  try:physical(paths.cache);out.append((paths.cache,paths.cache,now-(cache_days+1)*86400,None))
  except (OSError,Unsafe) as e:skips.append({'path':str(paths.cache),'reason':str(e)})
 for e in read_registry(paths):
  try:
   if not isinstance(e,dict):raise Unsafe('invalid task entry')
   task=task_root(paths,Path(e['task_root']));st=task.lstat()
   if (st.st_dev,st.st_ino)!=(e['device'],e['inode']):raise Unsafe('task identity changed')
   completed=e['completed_at']
   if not isinstance(completed,(int,float)) or not 0<completed<=now:raise Unsafe('invalid completion time')
   if now-completed<task_hours*3600:continue
   rels=e['dependencies']
   if not isinstance(rels,list) or not 1<=len(rels)<=8:raise Unsafe('invalid dependency roots')
   for rel in rels:
    root=dependency_root(task,rel)
    if any((root.parent/n).lstat().st_ctime>completed for n in ('package-lock.json','package.json')):raise Unsafe('project changed after completion')
    out.append((root,task,completed,completed))
  except (OSError,Unsafe,KeyError,TypeError,ValueError) as exc:skips.append({'path':e.get('task_root','invalid') if isinstance(e,dict) else 'invalid','reason':str(exc)})
 return out,skips

def collect(paths,u,now,cache_days=2,task_hours=24):
 rows=[];roots,skips=scopes(paths,now,cache_days,task_hours);scanned=0
 for root,task,cutoff,completed in roots:
  if used(u,task):skips.append({'path':str(root),'reason':'scope active'});continue
  for d,ds,fs in os.walk(str(root),followlinks=False):
   depth=len(Path(d).relative_to(root).parts)
   ds[:]=[n for n in ds if depth<16 and not os.path.islink(os.path.join(d,n)) and not os.path.lexists(os.path.join(d,n,'.keep'))]
   for name in fs:
    scanned+=1
    if scanned>MAX_ENTRIES:raise Unsafe('bounded scan limit exceeded; no partial plan')
    if name.endswith('.lock') or name in ('.keep','gc.properties'):continue
    p=Path(d)/name
    try:
     s=guard(paths,p,root)
     if max(s.st_mtime,s.st_ctime)>cutoff or used(u,p):continue
     rows.append({'path':str(p),'root':str(root),'task':str(task),'signature':signature(s),'sha256':digest(p,signature(s)),'allocated':s.st_blocks*512,'cutoff':cutoff,'completed_at':completed,'root_identity':(root.stat().st_dev,root.stat().st_ino),'task_identity':(task.stat().st_dev,task.stat().st_ino)})
    except (OSError,Unsafe) as exc:skips.append({'path':str(p),'reason':str(exc)})
 return rows,skips

def unlink_row(paths,r,u):
 p=Path(r['path']);root=Path(r['root']);task=Path(r['task'])
 if used(u,task) or used(u,p):raise Unsafe('active before unlink')
 if (root.stat().st_dev,root.stat().st_ino)!=tuple(r['root_identity']) or (task.stat().st_dev,task.stat().st_ino)!=tuple(r['task_identity']):raise Unsafe('scope identity changed')
 if r['completed_at'] and any((root.parent/n).lstat().st_ctime>r['completed_at'] for n in ('package-lock.json','package.json')):raise Unsafe('project changed after completion')
 s=guard(paths,p,root)
 if signature(s)!=tuple(r['signature']) or max(s.st_mtime,s.st_ctime)>r['cutoff']:raise Unsafe('file identity/age changed')
 fd=os.open('/',os.O_RDONLY|os.O_DIRECTORY);chain=[];part=Path('/')
 try:
  for name in p.parent.parts[1:]:
   child=os.open(name,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW,dir_fd=fd);os.close(fd);fd=child;part=part/name;st=os.fstat(fd);chain.append((part,st.st_dev,st.st_ino))
  for parent,dev,ino in chain:
   st=parent.lstat()
   if not stat.S_ISDIR(st.st_mode) or (st.st_dev,st.st_ino)!=(dev,ino):raise Unsafe('parent replaced')
  if signature(os.stat(p.name,dir_fd=fd,follow_symlinks=False))!=tuple(r['signature']):raise Unsafe('anchored file changed')
  if digest(p,r['signature'],fd)!=r['sha256']:raise Unsafe('cache content changed')
  if signature(os.stat(p.name,dir_fd=fd,follow_symlinks=False))!=tuple(r['signature']):raise Unsafe('file changed after content verification')
  guard(paths,p,root);os.unlink(p.name,dir_fd=fd)
 finally:os.close(fd)

def free_bytes():
 s=os.statvfs('/');return s.f_bavail*s.f_frsize

def run(paths,mode,cache_days=2,task_hours=24,target_gib=8,inherited=None,min_free_gib=5):
 before=regular(paths.lock)
 fd=os.dup(inherited) if inherited is not None else os.open(str(paths.lock),os.O_RDWR|os.O_NOFOLLOW)
 auditfd=None
 try:
  if signature(os.fstat(fd))!=signature(before):raise Unsafe('lock changed')
  fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
  if signature(paths.lock.lstat())!=signature(before):raise Unsafe('lock replaced')
  u=proc.snapshot(paths.proc);rows,skips=collect(paths,u,time.time(),cache_days,task_hours)
  result={'stage':'rebuildable_caches','mode':mode,'eligible_files':len(rows),'estimated_reclaim_bytes':sum(r['allocated'] for r in rows),'skipped_count':len(skips),'scope_skips':[r for r in skips if r.get('reason') in ('scope active','task identity changed','dependencies changed after completion')],'removed_files':0,'reclaimed_allocated_bytes':0}
  if mode=='plan' or free_bytes()>=min_free_gib*1024**3 or not rows:return result
  if not paths.audit.parent.exists():paths.audit.parent.mkdir(mode=0o700)
  physical(paths.audit.parent);logger.LOG=paths.audit;auditfd=logger.rotate_log(logger.open_log(paths.audit))
  def audit(v):
   logger.validate_log(auditfd);b=(json.dumps(v)+'\n').encode();view=memoryview(b)
   while view:
    n=os.write(auditfd,view)
    if n<=0:raise OSError('audit write made no progress')
    view=view[n:]
   os.fsync(auditfd)
  for i in range(0,len(rows),50):
   if free_bytes()>=target_gib*1024**3:break
   batch=rows[i:i+50];auditfd=logger.rotate_log(auditfd);audit({'intent':batch})
   for r in batch:
    if free_bytes()>=target_gib*1024**3:break
    # Fresh FD/cwd/mmap snapshot for every mutation. Incomplete scans abort, not skip silently.
    fresh=proc.snapshot(paths.proc)
    try:unlink_row(paths,r,fresh)
    except (OSError,Unsafe):result['skipped_count']+=1;continue
    result['removed_files']+=1;result['reclaimed_allocated_bytes']+=r['allocated']
    audit({'removed':r['path']})
  return result
 finally:
  if auditfd is not None:os.close(auditfd)
  os.close(fd)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['plan','clean','mark-complete','mark-active']);p.add_argument('--host-lock-fd',type=int);p.add_argument('--cache-keep-days',type=int,default=2);p.add_argument('--task-keep-hours',type=int,default=24);p.add_argument('--target-gib',type=int,default=8);p.add_argument('--min-free-gib',type=int,default=5);p.add_argument('--task-root',type=Path);p.add_argument('--node-modules',action='append',default=[]);a=p.parse_args()
 if any(v<0 or v>999999999 for v in (a.cache_keep_days,a.task_keep_hours,a.target_gib,a.min_free_gib)) or a.host_lock_fd is not None and a.host_lock_fd<3:p.error('invalid bounded settings')
 if a.target_gib<a.min_free_gib:p.error('target must be at least trigger')
 paths=Paths()
 try:
  if a.mode in ('mark-complete','mark-active'):
   if os.geteuid()!=0 or a.task_root is None:p.error('task registration requires root and --task-root')
   fd=os.open(str(paths.lock),os.O_RDWR|os.O_NOFOLLOW)
   try:
    st=regular(paths.lock)
    if signature(os.fstat(fd))!=signature(st):raise Unsafe('lock changed')
    fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB)
    if signature(paths.lock.lstat())!=signature(st):raise Unsafe('lock replaced')
    if a.mode=='mark-complete':result=mark_complete(paths,a.task_root,a.node_modules)
    else:
     task=task_root(paths,a.task_root);entries=read_registry(paths)
     if not paths.state.exists():paths.state.mkdir(mode=0o700)
     physical(paths.state);atomic_json(paths.registry,{'version':1,'tasks':[e for e in entries if e.get('task_root')!=str(task)]});result={'active':str(task)}
   finally:os.close(fd)
  else:
   if a.mode=='clean' and os.geteuid()!=0:p.error('clean requires root')
   result=run(paths,a.mode,a.cache_keep_days,a.task_keep_hours,a.target_gib,a.host_lock_fd,a.min_free_gib)
  print(json.dumps(result));return 0
 except (OSError,Unsafe,ValueError,TypeError) as e:print('WARNING: rebuildable cleanup stopped safely: '+str(e),file=sys.stderr);return 1
if __name__=='__main__':sys.exit(main())
