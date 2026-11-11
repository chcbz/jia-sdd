from pathlib import Path,PurePosixPath
import json,hashlib,tarfile,datetime,sys
D=Path(__file__).resolve().parent;name=sys.argv[1];a=json.loads((D/(name+'-artifact.json')).read_text())
def digest(f):
 h=hashlib.sha256()
 for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
with open(a['path'],'rb') as f:assert digest(f)==a['sha256']
files={};docs={};seen=set();jar=None
with tarfile.open(a['path'],'r|gz') as t:
 for m in t:
  p=str(PurePosixPath(m.name));assert not p.startswith('/') and '..' not in PurePosixPath(p).parts and p not in seen;seen.add(p)
  if m.isdir():continue
  assert m.isfile();f=t.extractfile(m)
  if name=='api' and p=='application.jar':jar=digest(f)
  elif name=='web' and p.startswith('dist/'):files[p[5:]]={'size':m.size,'sha256':digest(f)}
  elif p in ('receipt.json','test-results/summary.json','release.json','source-commit.txt','source-tree.txt','mochawesome-report/mochawesome.json'):
   docs[p]=f.read();(D/(name+'-'+Path(p).name)).write_bytes(docs[p])
if name=='api':
 r=json.loads(docs['receipt.json']);s=json.loads(docs['test-results/summary.json']);assert r['source']['commit_sha']==a['commit'] and r['source']['tree_sha']==a['tree'] and r['flow']['run_id']==a['run'];assert r['source']['clean_before'] and r['source']['clean_after'];assert r['status']=='success' and r['gradle_exit_code']==r['bridge_exit_code']==0
 assert jar=='5b8a202fc0ffa44bcdba44e725bf13d3803b77e0e928e77656f4b94ac8e16979' and hashlib.sha256(docs['receipt.json']).hexdigest()=='b4d4cd874fc098f6252dfe10fafb4c51572e3fe51a62c98a12a109d0d3e71006'
 assert s['counts']['failures']==s['counts']['errors']==0
 extra={'jarSha256':jar,'tests':s['counts']}
else:
 r=json.loads(docs['release.json']);assert r['commit']==a['commit']==docs['source-commit.txt'].decode().strip();assert a['tree']==docs['source-tree.txt'].decode().strip();assert r['run_id']==a['run'] and r['package_version']==a['version'];assert files=={x['path']:{'size':x['size'],'sha256':x['sha256']} for x in r['files']}
 stats=json.loads(docs['mochawesome-report/mochawesome.json'])['stats'];assert stats['failures']==0 and stats['passes']==3672
 (D/'web-release-manifest.json').write_bytes(docs['release.json']);extra={'files':len(files),'tests':stats}
out=dict(a,status='verified_not_deployed',**extra);(D/(name+'-verified.json')).write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
