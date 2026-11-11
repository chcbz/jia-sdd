from pathlib import Path,PurePosixPath
import json,tarfile,hashlib,datetime,urllib.request,re
D=Path(__file__).resolve().parent;archive=Path('/var/lib/cyf-web-flow/downloads/215/package.tgz');recordPath=Path('/var/lib/cyf-web-flow/record.json');record=json.loads(recordPath.read_text());sha=lambda b:hashlib.sha256(b).hexdigest()
assert (record['run_id'],record['commit'],record['release_version'],record['status'])==('215','828460c9c1ce90d083ef9f82f9ce7622bdf4830d','1.16.2','online_verified')
assert sha(archive.read_bytes())==record['artifact_sha256'];metadata={};files={}
with tarfile.open(str(archive),'r|gz') as t:
 for m in t:
  n=m.name[2:] if m.name.startswith('./') else m.name;p=PurePosixPath(n);assert not p.is_absolute() and '..' not in p.parts and not m.issym() and not m.islnk()
  if not m.isfile():continue
  assert n not in files;data=t.extractfile(m).read();files[n]={'size':len(data),'sha256':sha(data)}
  if n in ('release.json','installer/helper-release.json','source-commit.txt','source-tree.txt','dist/index.html','mochawesome-report/mochawesome.json','mochawesome-report/ci-profile.json') or (n.endswith(('.js','.css')) and any(x in n for x in ('JuyiHall','PersonalWorkspace','usePersonalWorkspace','HallDraftEditor','TaskMaterialLinks'))):metadata[n]=data
m=json.loads(metadata['release.json']);assert m['run_id']=='215' and m['commit']==record['commit'] and m['package_version']==record['release_version'];assert metadata['source-tree.txt'].decode().strip()=='47b212675e478b9d0fb8f0c4fd849b706dab188c';assert metadata['source-commit.txt'].decode().strip()==record['commit']
entries={e['path']:e for e in m['files']};assert set(entries)=={n[5:] for n in files if n.startswith('dist/')}
root=Path('/home/isp/hosts/cyf/web/kit')
for p,e in entries.items():
 assert files['dist/'+p]=={k:e[k] for k in ('size','sha256')};local=root/p;assert local.is_file();assert {'size':local.stat().st_size,'sha256':sha(local.read_bytes())}==files['dist/'+p]
selected={'index.html'}
for ref in re.findall(r'(?:src|href)=["\']([^"\']+)["\']',metadata['dist/index.html'].decode()):
 ref=ref.lstrip('/')
 if ref in entries:selected.add(ref)
for p in entries:
 if p.startswith('static/') and any(x in p for x in ('JuyiHall','PersonalWorkspace','usePersonalWorkspace','HallDraftEditor','TaskMaterialLinks','Login')) and p.endswith(('.js','.css')):selected.add(p)
checks=[]
for p in sorted(selected):
 req=urllib.request.Request('https://kit.chaoyoufan.cn/'+p+'?verify_run=215',headers={'Cache-Control':'no-cache','Pragma':'no-cache','Accept-Encoding':'identity'})
 with urllib.request.urlopen(req,timeout=45) as r:data=r.read();status=r.status
 actual=sha(data);match=actual==entries[p]['sha256'];checks.append({'path':p,'status':status,'sha256':actual,'match':match});assert status==200 and match,p
report={'verifiedAt':datetime.datetime.now().astimezone().isoformat(),'pipeline':4403172,'run':215,'commit':record['commit'],'tree':'47b212675e478b9d0fb8f0c4fd849b706dab188c','version':record['release_version'],'artifactSHA256':record['artifact_sha256'],'artifactBytes':archive.stat().st_size,'distFilesVerified':len(entries),'installedFilesMatch':len(entries),'httpChecks':checks,'status':'SOURCE_ARTIFACT_INSTALLED_FILES_AND_PUBLIC_HTTP_MATCH','businessInteractions':'NOT_YET_TESTED','recordSHA256':sha(recordPath.read_bytes())}
(D/'online-verification.json').write_text(json.dumps(report,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='httpChecks'}));print('PUBLIC_HTTP_FILES_MATCH',len(checks))

# Read the full same-run report, not an excerpt of the Flow console log.
tests=json.loads(metadata['mochawesome-report/mochawesome.json'])['stats']
assert tests['failures']==0 and tests['passes']>0
(D/'formal-test-report.json').write_text(json.dumps({'run':215,'commit':record['commit'],'stats':tests},indent=2))
js='\n'.join(v.decode() for k,v in metadata.items() if k.endswith('.js'))
css='\n'.join(v.decode() for k,v in metadata.items() if k.endswith('.css'))
assert '读取更早版本' in js
assert '详情读取失败；请重读详情，不要重复提交。' in js
request=urllib.request.Request('https://kit.chaoyoufan.cn/juyiting?verify_run=215',headers={'Cache-Control':'no-cache','Accept-Encoding':'identity'})
with urllib.request.urlopen(request,timeout=45) as response:
 assert response.status==200 and sha(response.read())==entries['index.html']['sha256']
(D/'ui-artifact-smoke.json').write_text(json.dumps({'run':215,'commit':record['commit'],'status':'PASS','workspaceHistoryControl':True,'savedButDetailFailedNotice':True,'hallRouteMatchesIndex':True,'scope':'Exact Flow artifact assets matched against installed and public bytes; authenticated browser clicks not performed'},indent=2))
print('FORMAL_TEST_STATS',json.dumps(tests))
print('UI_ARTIFACT_AND_HALL_ROUTE_SMOKE PASS')
