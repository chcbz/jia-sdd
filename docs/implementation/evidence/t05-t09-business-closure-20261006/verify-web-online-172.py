import pathlib,json,hashlib,tarfile,posixpath,concurrent.futures,urllib.request,urllib.parse,time
from datetime import datetime,timezone
E=pathlib.Path('/home/isp/wsps/cyf/docs/implementation/evidence/t05-t09-business-closure-20261006');p=pathlib.Path('/var/lib/cyf-web-flow/record.json');raw=p.read_bytes();r=json.loads(raw);assert r['run_id']=='172' and r['status']==r['phase']=='online_verified' and r['commit']=='fe6d4d542079bdf07f5b5fcf2ff96e7f217be33e'
a=json.loads((E/'web172-artifact-verification.json').read_text());assert a['run']==172 and a['distFilesVerified']==len(r['files'])
with tarfile.open('/var/lib/cyf-web-flow/downloads/172/package.tgz') as t:
 def text(base):
  entries=[m for m in t.getmembers() if m.isfile() and posixpath.basename(m.name)==base];assert len(entries)==1;return t.extractfile(entries[0]).read().decode().strip()
 assert text('source-commit.txt')==r['commit'];tree=text('source-tree.txt');assert tree=='a8e42ded0fbec8a26d6e4aa9f719473cc165e524'
site=pathlib.Path('/home/isp/hosts/cyf/web/kit');out=[]
def verify(f):
 path=f['path'];assert not path.startswith('/') and '..' not in path.split('/') and '\\' not in path
 local=site/path;assert local.is_file() and not local.is_symlink();b=local.read_bytes();assert len(b)==f['size'] and hashlib.sha256(b).hexdigest()==f['sha256']
 url='https://kit.chaoyoufan.cn/'+urllib.parse.quote(path,safe='/')+'?flow_verify=4403172-172'
 req=urllib.request.Request(url,headers={'Accept-Encoding':'identity','Cache-Control':'no-cache, no-store, max-age=0','Pragma':'no-cache','User-Agent':'cyf-mmd-release-verification/172'})
 h=hashlib.sha256();size=0
 with urllib.request.urlopen(req,timeout=30) as response:
  assert response.getcode()==200
  while True:
   block=response.read(1024*1024)
   if not block:break
   size+=len(block);assert size<=f['size'];h.update(block)
 assert size==f['size'] and h.hexdigest()==f['sha256'],('PUBLIC_BYTES_MISMATCH',path)
 return {'path':path,'size':size,'sha256':h.hexdigest(),'installedBytesMatch':True,'publicHttpsBytesMatch':True}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for x in pool.map(verify,r['files']):out.append(x)
assert p.read_bytes()==raw
result={'verifiedAt':datetime.now(timezone.utc).isoformat(),'pipeline':4403172,'run':172,'commit':r['commit'],'tree':tree,'recordStatus':r['status'],'packageVersion':r['package_version'],'sameRunArtifactSha256':a['artifactSha256'],'files':len(out),'fullManifestPublicCoverage':True,'installedBytesVerified':True,'publicHttpsBytesVerified':True,'recordUnchanged':True,'productAcceptance':'NOT_RUN'}
(E/'web172-online-files-private.json').write_text(json.dumps(out,indent=2));(E/'web172-online-verification.json').write_text(json.dumps(result,indent=2));print(json.dumps(result))
