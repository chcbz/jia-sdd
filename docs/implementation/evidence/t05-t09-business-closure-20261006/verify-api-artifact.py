import tarfile,json,hashlib,posixpath,xml.etree.ElementTree as ET
from datetime import datetime,timezone
p='/var/lib/cyf-api-flow/incoming/package.tgz'
t=tarfile.open(p);members=t.getmembers();bad=[m.name for m in members if m.name.startswith('/') or '..' in m.name.split('/') or m.issym() or m.islnk() or m.isdev()]
assert not bad
print(json.dumps({'non_report_files':[m.name for m in members if m.isfile() and 'test-results' not in m.name]},ensure_ascii=False))
receipt=next(m for m in members if m.isfile() and posixpath.basename(m.name)=='receipt.json');r=json.loads(t.extractfile(receipt).read());assert r['flow']['run_id']=='112' and r['source']['commit_sha']=='329d44fd7f8d0b2402853f5eac4cf47c99fcbed9' and r['source']['tree_sha']=='69d2cb5448aa165b35ead9794bac0971736f1a7d' and r['gradle_exit_code']==r['bridge_exit_code']==0
counts=dict(suites=0,tests=0,failures=0,errors=0,skipped=0);groups={}
for m in members:
 if m.isfile() and '/test-results/' in m.name and m.name.endswith('.xml'):
  x=ET.fromstring(t.extractfile(m).read());assert x.tag=='testsuite'
  group=m.name.split('/test-results/')[-1].split('/')[0];g=groups.setdefault(group,dict(suites=0,tests=0,failures=0,errors=0,skipped=0));counts['suites']+=1;g['suites']+=1
  for key in ['tests','failures','errors','skipped']:
   n=int(x.get(key,'0'));counts[key]+=n;g[key]+=n
assert counts['suites']>0 and counts['failures']==counts['errors']==0
h=hashlib.sha256()
with open(p,'rb') as f:
 for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
jar=next(m for m in members if m.isfile() and posixpath.basename(m.name)=='application.jar');jh=hashlib.sha256();f=t.extractfile(jar)
for b in iter(lambda:f.read(1024*1024),b''):jh.update(b)
result={'verifiedAt':datetime.now(timezone.utc).isoformat(),'pipeline':5260799,'run':112,'commit':'329d44fd7f8d0b2402853f5eac4cf47c99fcbed9','sourceEvidence':'Flow run source first commit','archiveSafety':'PASS no extraction performed','artifactBytes':__import__('os').path.getsize(p),'artifactSha256':h.hexdigest(),'applicationJarSha256':jh.hexdigest(),'suiteEntryCountsMayOverlap':True,'testStats':counts,'testGroups':groups,'buildOrigin':'aliyun_flow','deployment':'SEE_SEPARATE_LIVE_FLOW_AND_HOST_VERIFICATION','productAcceptance':'NOT_RUN'}
out='/home/isp/wsps/cyf/docs/implementation/evidence/t05-t09-business-closure-20261006/api112-artifact-verification.json';open(out,'w').write(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

