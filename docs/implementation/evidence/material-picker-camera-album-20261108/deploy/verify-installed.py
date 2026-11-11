import hashlib,json,pathlib,urllib.request,datetime
E=pathlib.Path(__file__).resolve().parent
P=pathlib.Path('/home/isp/hosts/cyf/web/kit')
r=json.loads(pathlib.Path('/home/isp/state/cyf-web-flow/record.json').read_text());c=json.loads((E/'candidate.json').read_text());build=json.loads((E/'result.json').read_text())
assert r['status']=='online_verified' and r['source_kind']=='LOCAL'
assert r['source']['commit']==c['commit'] and r['source']['tree']==c['tree'] and r['source']['version']==c['version']
assert r['artifact_sha256']==build['artifact']['sha256']
sha=lambda b:hashlib.sha256(b).hexdigest()
for item in r['files']:
 data=(P/item['path']).read_bytes();assert len(data)==item['size'] and sha(data)==item['sha256'],item['path']
js=[];css=[]
for item in r['files']:
 path=item['path']
 if not path.endswith(('.js','.css')):continue
 text=(P/path).read_text()
 if path.endswith('.js') and '从相册选择' in text and 'capture:"environment"' in text:
  assert 'image/*' in text and '拍照' in text
  js.append(item)
 if path.endswith('.css') and '.quick-material-upload' in text:
  assert 'background:transparent' in text
  css.append(item)
assert js and css
online=[]
for item in [next(f for f in r['files'] if f['path']=='index.html'),*js,*css]:
 req=urllib.request.Request('https://kit.chaoyoufan.cn/'+item['path']+'?camera_album_verify='+c['commit'],headers={'Accept-Encoding':'identity','Cache-Control':'no-cache'})
 with urllib.request.urlopen(req,timeout=30) as response:
  data=response.read();assert response.status==200 and sha(data)==item['sha256']
 online.append({'path':item['path'],'sha256':sha(data),'status':200})
backup=pathlib.Path(r['backup']);before=json.loads((E/'before-record.json').read_text());snapshot=json.loads((backup/'before.json').read_text())
assert (backup/'record-before.json').read_bytes()==(E/'before-record.json').read_bytes()
assert sha((backup/'files/index.html').read_bytes())==c['beforeIndexSha256']
(E/'installed-record.json').write_text(json.dumps(r,indent=2))
(E/'acceptance.json').write_text(json.dumps({'verifiedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','source':r['source'],'packageSha256':r['artifact_sha256'],'installedFilesVerified':len(r['files']),'installerOnlineVerifiedFiles':r['onlineVerifiedFiles'],'targetedOnline':online,'backup':str(backup),'previousVersion':before['source']['version'],'businessScope':'published compiled picker has rear-camera and multi-image album inputs; fixed-source mounted regressions passed; no authenticated production upload or real mobile camera/album interaction performed','apiRuntimeChanges':False,'buildSeconds':build['wallSeconds'],'installSeconds':r['wallSeconds'],'fullDeliveryWallSeconds':None},indent=2))
print(json.dumps({'status':'PASS','version':r['source']['version'],'diskFiles':len(r['files']),'onlineFiles':r['onlineVerifiedFiles'],'targetedAssets':len(online),'backup':str(backup)},indent=2))
