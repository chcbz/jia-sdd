from pathlib import Path
import json, hashlib, re, sys
from urllib.parse import urlsplit,unquote
R=Path('/home/isp/wsps/cyf'); E=R/'docs/implementation/evidence/spec-full-refresh-20261107'
sys.path.insert(0,str(R/'ops/orchestration'))
from sdd_docs import without_fences, LINK
h=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
base=json.loads((E/'before-inventory.json').read_text())
changed=[]
for p in (E/'originals').rglob('*.txt'):
 n=str(p.relative_to(E/'originals'))[:-4]; target=R/n
 if target.exists() and h(p)!=h(target):changed.append({'path':n,'before_sha256':h(p),'after_sha256':h(target),'new':False})
# Include additions listed by previous scripts (no original exists for new files).
names={x['path'] for x in changed}
for log in ['primary-changes.json','navigation-changes.json','detail-changes.json']:
 for x in json.loads((E/log).read_text()):
  if isinstance(x,dict) and x.get('before_sha256','not-null') is None and x['path'] not in names:
   p=R/x['path'];changed.append({'path':x['path'],'before_sha256':None,'after_sha256':h(p),'new':True});names.add(x['path'])
checks=0; missing=[]; new_missing=[]
def targets(text):
 return set(m.group(1) for m in LINK.finditer(without_fences(text)))
for x in changed:
 p=R/x['path']
 if p.suffix!='.md':continue
 old=E/'originals'/(x['path']+'.txt'); olds=targets(old.read_text()) if old.exists() else set()
 for t in targets(p.read_text()):
  u=urlsplit(t)
  if u.scheme or u.netloc or not u.path:continue
  checks+=1
  if not (p.parent/unquote(u.path)).exists():
   v={'path':x['path'],'target':t,'preexisting':t in olds};missing.append(v)
   if t not in olds:new_missing.append(v)
protected=[x for x in base if Path(x['path']).suffix in ['.json','.yaml','.yml']]
drift=[dict(x,current_sha256=h(R/x['path']) if (R/x['path']).exists() else None) for x in protected if not (R/x['path']).exists() or h(R/x['path'])!=x['sha256']]
non_owned=[]
for x in base:
 p=R/x['path']
 if x['path'] not in names and (not p.exists() or h(p)!=x['sha256']):non_owned.append(x['path'])
result={'changed_files':len(changed),'changed_markdown':sum(x['path'].endswith('.md') for x in changed),'local_link_targets_checked':checks,'missing_local_links':missing,'new_missing_local_links':new_missing,'preexisting_machine_readable_files_checked':len(protected),'machine_readable_drift':drift,'changes_outside_task_owned_paths':non_owned,'scope':'Current document navigation and frozen data byte preservation only; not source/production verification'}
(E/'final-changes.json').write_text(json.dumps(changed,ensure_ascii=False,indent=2)+'\n')
(E/'final-integrity-and-links.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
