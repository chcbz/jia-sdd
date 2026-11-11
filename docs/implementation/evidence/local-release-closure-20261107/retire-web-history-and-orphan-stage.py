from pathlib import Path
import os,json,hashlib,fcntl,importlib.util,tarfile,time
E=Path(__file__).resolve().parent

def load(n):
 s=importlib.util.spec_from_file_location(n,'/usr/local/libexec/cyf/'+n+'.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
r=load('release_payload_cleanup');f=load('flow_host_cleanup');rt=load('runtime_backup_cleanup');safe=load('rebuildable_cache_cleanup')
fd=r.locked_fd(r.Paths().host_lock,(0o600,0o644));report={'scope':'explicit user historical cleanup; existing exact-file safety adapters reused','groups':[]}
with f.locked(f.Paths()):
 api,asig=f.read_state(f.Paths());web,wsig=f.read_web_state(f.Paths());current=json.loads(Path('/home/isp/state/cyf-web-flow/record.json').read_text())
 base=Path('/home/isp/baks/cyf-web-flow');payloads=[]
 for d in base.iterdir():
  if not d.is_dir() or d.is_symlink():continue
  files=[d/n for n in ('site.tar','site.tar.gz','prior-flow-package.tgz') if (d/n).is_file()]
  if files:payloads.append((max(p.stat().st_mtime for p in files),d,files))
 keep={str(d) for _,d,_ in sorted(payloads,reverse=True)[:2]};report['protectedWebBackups']=sorted(keep)
 exact=[base/'20261104-single-reply-445/site.tar.gz',base/'20261104-ephemeral-preview-web422/prior-flow-package.tgz']
 for p in exact:
  assert str(p.parent) not in keep
  for name in ('record.json','RECOVERY.md'):safe.regular(p.parent/name)
  st=rt.leaf(rt.Paths(),p);dest=E/'retired-web-metadata'/p.parent.name;dest.mkdir(parents=True,exist_ok=True)
  for name in ('record.json','RECOVERY.md','files.list'):
   if (p.parent/name).is_file():(dest/name).write_bytes((p.parent/name).read_bytes())
  names=[]
  with tarfile.open(p,'r:*') as tar:
   for member in tar:
    names.append({'name':member.name,'size':member.size})
    if member.isfile() and Path(member.name).name in {'version.json','manifest.json','cyf-flow-build.json','cyf-local-build.json','receipt.json','application.metadata.json','build-info.json'} and member.size<3*1024*1024:
     (dest/(hashlib.sha256(member.name.encode()).hexdigest()[:12]+'-'+Path(member.name).name)).write_bytes(tar.extractfile(member).read())
  (dest/'archive-members.json').write_text(json.dumps(names))
  report['groups'].append({'root':str(p.parent),'reason':'older than two newest Web recovery payloads; current LOCAL binding separate','files':[{'path':str(p),'signature':safe.signature(st),'sha256':r.digest(p),'allocated':st.st_blocks*512}]})
 stage=Path('/home/isp/state/cyf-web-flow/.cyf-web-stage-zwiqf2vw');expected={x['path']:x for x in current['files']};rows=[]
 for p in stage.rglob('*'):
  if p.is_dir():rt.directory(rt.Paths(),p);continue
  name=str(p.relative_to(stage/'dist'));assert name in expected
  st=rt.leaf(rt.Paths(),p);digest=r.digest(p);assert st.st_size==expected[name]['size'] and digest==expected[name]['sha256']
  rows.append({'path':str(p),'signature':safe.signature(st),'sha256':digest,'allocated':st.st_blocks*512})
 assert rows
 report['groups'].append({'root':str(stage),'reason':'orphan staging from terminated same-batch TLS verifier; every file matches verified current Web manifest','files':rows})
 safe.atomic_json(E/'web-history-cleanup.json',dict(report,status='INTENT'))
 for group in report['groups']:
  root=Path(group['root']);assert not safe.proc.snapshot(Path('/proc')).used(root)
  for i,row in enumerate(group['files']):
   if i%50==0:
    usage=safe.proc.snapshot(Path('/proc'));assert not usage.used(root)
    assert f.read_state(f.Paths())[1]==asig and f.read_web_state(f.Paths())[1]==wsig
   p=Path(row['path']);assert not usage.used(p);assert r.digest(p)==row['sha256'];rt.unlink(rt.Paths(),row)
  if root!=stage:safe.atomic_json(root/'PAYLOAD_RETIRED.json',{'schemaVersion':1,'status':'retired-not-a-complete-recovery','reason':'2026-11-07 explicit historical cleanup; newest two/current protected','audit':str(E),'at':time.time()})
 for d in sorted([p for p in stage.rglob('*') if p.is_dir()],key=lambda p:len(p.parts),reverse=True):d.rmdir()
 stage.rmdir()
 report['status']='REMOVED';report['allocatedBytes']=sum(row['allocated'] for g in report['groups'] for row in g['files']);safe.atomic_json(E/'web-history-cleanup.json',report)
os.close(fd);print('Removed Web history/orphan staging bytes:',report['allocatedBytes'])
