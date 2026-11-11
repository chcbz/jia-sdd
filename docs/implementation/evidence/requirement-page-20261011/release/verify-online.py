from pathlib import Path,PurePosixPath
import json,tarfile,hashlib,datetime,urllib.request,re
D=Path(__file__).resolve().parent;archive=Path('/var/lib/cyf-web-flow/downloads/202/package.tgz');recordPath=Path('/var/lib/cyf-web-flow/record.json');record=json.loads(recordPath.read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
assert (record['run_id'],record['commit'],record['release_version'],record['status'])==('202','d079c548947a24ae9d2affcb41f97bbb9108e469','1.14.9','online_verified')
assert sha(archive.read_bytes())==record['artifact_sha256'];metadata={};files={}
with tarfile.open(str(archive),'r|gz') as t:
 for m in t:
  n=m.name[2:] if m.name.startswith('./') else m.name;p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and not m.issym() and not m.islnk()
  if not m.isfile():continue
  assert n not in files;data=t.extractfile(m).read();files[n]={'size':len(data),'sha256':sha(data)}
  if n in ('release.json','installer/helper-release.json','source-commit.txt','source-tree.txt','dist/index.html'):metadata[n]=data
m=json.loads(metadata['release.json']);assert m['run_id']=='202' and m['commit']==record['commit'] and m['package_version']==record['release_version'];assert metadata['source-tree.txt'].decode().strip()=='b19c302211fa2e6aa572d331723ed08d998cc06f';assert metadata['source-commit.txt'].decode().strip()==record['commit']
entries={e['path']:e for e in m['files']};assert set(entries)=={n[5:] for n in files if n.startswith('dist/')}
root=Path('/home/isp/hosts/cyf/web/kit')
for p,e in entries.items():
 assert files['dist/'+p]=={k:e[k] for k in ('size','sha256')};local=root/p;assert local.is_file();assert {'size':local.stat().st_size,'sha256':sha(local.read_bytes())}==files['dist/'+p]
selected={'index.html'}
for ref in re.findall(r'(?:src|href)=["\']([^"\']+)["\']',metadata['dist/index.html'].decode()):
 ref=ref.lstrip('/')
 if ref in entries:selected.add(ref)
for p in entries:
 if p.startswith('static/') and any(x in p for x in ('JuyiHall','BountyPanel','HallDraftEditor','AgentDetail','HostingRent','Login')) and p.endswith(('.js','.css')):selected.add(p)
checks=[]
for p in sorted(selected):
 req=urllib.request.Request('https://kit.chaoyoufan.cn/'+p+'?verify_run=202',headers={'Cache-Control':'no-cache','Pragma':'no-cache','Accept-Encoding':'identity'})
 with urllib.request.urlopen(req,timeout=45) as r:data=r.read();status=r.status
 actual=sha(data);match=actual==entries[p]['sha256'];checks.append({'path':p,'status':status,'sha256':actual,'match':match});assert status==200 and match,p
report={'verifiedAt':datetime.datetime.now().astimezone().isoformat(),'pipeline':4403172,'run':202,'commit':record['commit'],'tree':'b19c302211fa2e6aa572d331723ed08d998cc06f','version':record['release_version'],'artifactSHA256':record['artifact_sha256'],'artifactBytes':archive.stat().st_size,'distFilesVerified':len(entries),'installedFilesMatch':len(entries),'httpChecks':checks,'status':'SOURCE_ARTIFACT_INSTALLED_FILES_AND_PUBLIC_HTTP_MATCH','businessInteractions':'NOT_YET_TESTED','recordSHA256':sha(recordPath.read_bytes())}
(D/'online-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='httpChecks'}));print('PUBLIC_HTTP_FILES_MATCH',len(checks))
