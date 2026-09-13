#!/usr/bin/env python3
import hashlib,json,re,sys
from pathlib import Path
prompt=sys.argv[-1] if len(sys.argv)>1 else ''
m=re.search(r'outputs/([0-9a-f]{32})',prompt)
if not m: raise SystemExit('No trusted output run path supplied')
run=m.group(1);root=Path.cwd()/'outputs'/run;root.mkdir(parents=True,exist_ok=True)
items=[]
for i in range(60):
 name=f'page-{i:03d}.md';body=f'# OD11 pagination file {i}\n\nTrusted conversation run {run}.\n'
 (root/name).write_text(body)
 items.append({'outputId':hashlib.sha256(f'{run}:{name}'.encode()).hexdigest()[:32],
 'title':f'OD11 paging {i:03d}','relativePath':name,'artifactType':'document','publishToOwner':True})
(root/'manifest.json').write_text(json.dumps({'schemaVersion':1,'items':items}))
print(json.dumps({'type':'item.completed','item':{'type':'agent_message','text':'已生成60份分页验证文件。'}}),flush=True)
