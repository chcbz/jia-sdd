import json,pathlib,hashlib,re,urllib.request,datetime
D=pathlib.Path(__file__).parent; SITE=pathlib.Path('/home/isp/hosts/cyf/web/kit');m=json.loads((D/'web-release-manifest.json').read_text());files={x['path']:x for x in m['files']}
record=json.loads(pathlib.Path('/home/isp/state/cyf-web-flow/record.json').read_text())
assert record['status']=='online_verified' and record['run_id']==m['run_id'] and record['commit']==m['commit']
for name,e in files.items():
 p=SITE/name
 assert p.is_file() and not p.is_symlink() and p.stat().st_size==e['size']
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 assert h.hexdigest()==e['sha256'],name
index=(SITE/'index.html').read_text();paths={'index.html'}
paths.update(p.lstrip('/') for p in re.findall(r'(?:src|href)="([^"]+\.(?:js|css))"',index))
paths.update(p for p in files if 'JuyiHallEntry-' in p or 'OAuthCallback-' in p)
# Verify feature chunks are actually reachable from the current built JS import graph.
js=[SITE/p for p in paths if p.endswith('.js') and 'JuyiHallEntry-' not in p and 'OAuthCallback-' not in p]
reachable='\n'.join(p.read_text() for p in js)
for p in paths:
 if 'JuyiHallEntry-' in p or 'OAuthCallback-' in p: assert p.split('/')[-1] in reachable,'FEATURE_NOT_REFERENCED'
results=[]
for p in sorted(paths):
 e=files[p];req=urllib.request.Request('https://kit.chaoyoufan.cn/'+p,headers={'Cache-Control':'no-cache, no-store','Accept-Encoding':'identity'})
 with urllib.request.urlopen(req,timeout=60) as r:b=r.read();status=r.status
 h=hashlib.sha256(b).hexdigest();assert status==200 and len(b)==e['size'] and h==e['sha256'],p
 results.append({'path':p,'status':status,'size':len(b),'sha256':h,'match':True})
result={'verifiedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pipeline':'4403172','run':m['run_id'],'commit':m['commit'],'installedFilesVerified':len(files),'featureReferencedByCurrentEntry':True,'resources':results}
(D/'web-public-resources.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
