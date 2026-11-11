import json,hashlib,tarfile,datetime,urllib.request,re
from pathlib import Path
out=Path(__file__).resolve().parent
start=json.loads((out/'web-start.json').read_text());run=str(start.get('run',{}).get('id') or start.get('runId') or start['returnedRunId'])
commit='69175b99f9b8a4c36194d2b4edf22a26e4e027f1';tree='699a56f071d4e80b9535caef87f45fe846ebbd14'
archive=Path('/home/isp/state/cyf-web-flow/downloads')/run/'package.tgz';site=Path('/home/isp/hosts/cyf/web/kit')
def sha_file(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
sha=sha_file(archive);record=json.load(open('/home/isp/state/cyf-web-flow/record.json'))
assert record['run_id']==run and record['commit']==commit and record['release_version']=='1.16.65' and record['artifact_sha256']==sha and record['status']=='online_verified'
archiveFiles={};captured={}
with tarfile.open(str(archive),'r|gz') as t:
 for m in t:
  name=m.name[2:] if m.name.startswith('./') else m.name
  if not m.isfile():continue
  if name in ['release.json','source-commit.txt','source-tree.txt','mochawesome-report/mochawesome.json','mochawesome-report/ci-profile.json']:
   captured[name]=t.extractfile(m).read()
  elif name.startswith('dist/'):
   h=hashlib.sha256();size=0
   f=t.extractfile(m)
   for b in iter(lambda:f.read(1024*1024),b''):h.update(b);size+=len(b)
   archiveFiles[name[5:]]={'sha256':h.hexdigest(),'size':size}

manifest=json.loads(captured['release.json']);stats=json.loads(captured['mochawesome-report/mochawesome.json'])['stats']
assert manifest['commit']==commit and str(manifest['run_id'])==run and manifest['package_version']=='1.16.65'
assert captured['source-commit.txt'].decode().strip()==commit and captured['source-tree.txt'].decode().strip()==tree
assert stats['failures']==0 and stats['passes']==3480 and stats['pending']==2
expected={x['path']:x for x in manifest['files']};assert len(archiveFiles)==len(expected)
for p,x in expected.items():
 assert archiveFiles[p]['sha256']==x['sha256'] and archiveFiles[p]['size']==x['size']
 assert (site/p).stat().st_size==x['size'] and sha_file(site/p)==x['sha256']
old={x['path']:x for x in json.loads((out/'installed-before.json').read_text())['files']}
changed=[p for p,x in expected.items() if p in old and old[p]['sha256']!=x['sha256']]
assert changed==['index.html']
index=(site/'index.html').read_text();paths=['','juyiting']
paths+=sorted(p for p in expected if re.match(r'static/(JuyiHallEntry-[^/]+\.(?:js|css))$',p) or ('/'+p in index))
checks=[]
for p in paths:
 req=urllib.request.Request('https://kit.chaoyoufan.cn/'+p+'?verify=discussion-material-'+run,headers={'Cache-Control':'no-cache','Accept-Encoding':'identity'})
 with urllib.request.urlopen(req,timeout=30) as response:
  body=response.read();status=response.status
 digest=hashlib.sha256(body).hexdigest();assert status==200 and digest==expected[p if p in expected else 'index.html']['sha256']
 checks.append({'path':p,'status':status,'sha256':digest})
for name in ['release.json','source-commit.txt','source-tree.txt','mochawesome-report/ci-profile.json']:(out/('artifact-'+name.split('/')[-1])).write_bytes(captured[name])
(out/'installed-after.json').write_text(json.dumps(record,indent=2)+'\n')
result={'verifiedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pipeline':'4403172','run':run,'version':'1.16.65','commit':commit,'tree':tree,'artifactSha256':sha,'artifactBytes':archive.stat().st_size,'stats':stats,'installedFileCount':len(expected),'changedExistingPaths':changed,'onlineChecks':checks,'backup':'/home/isp/baks/cyf-web-discussion-material-20261027-'+run,'scope':'same-Run artifact, installed files, public entries and Juyiting JS/CSS; not authenticated interaction or real phone camera permissions','apiRuntimeChanged':False}
(out/'verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['onlineChecks','stats']},ensure_ascii=False))
