import tarfile,json,hashlib,os,posixpath
from datetime import datetime,timezone
p='/var/lib/cyf-web-flow/downloads/170/package.tgz'
t=tarfile.open(p);members=t.getmembers();names=[m.name for m in members]
assert len(names)==len(set(names)),'duplicate archive entries'
assert not any(m.name.startswith('/') or '..' in m.name.split('/') or '\\' in m.name or m.issym() or m.islnk() or m.isdev() for m in members),'unsafe archive'
files=[m for m in members if m.isfile()]
release=[m for m in files if posixpath.basename(m.name)=='release.json'];assert len(release)==1
manifest=json.load(t.extractfile(release[0]));assert manifest['pipeline_id']=='4403172' and manifest['run_id']=='170' and manifest['branch']=='develop' and manifest['commit']=='6117332543cb551a1388865b6075b39901ecff2b'
base=posixpath.dirname(release[0].name);prefix=base+'/dist/'
actual={m.name[len(prefix):]:m for m in files if m.name.startswith(prefix)};expected={row['path']:row for row in manifest['files']};assert len(expected)==len(manifest['files']) and set(actual)==set(expected) and 'index.html' in actual
for name,m in actual.items():
 h=hashlib.sha256();f=t.extractfile(m)
 for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 assert m.size==expected[name]['size'] and h.hexdigest()==expected[name]['sha256'],'dist integrity mismatch'
reports=[m for m in files if posixpath.basename(m.name)=='mochawesome.json'];assert len(reports)==1
report=json.load(t.extractfile(reports[0]));stats=report['stats'];assert stats['failures']==0 and stats['passes']>0
h=hashlib.sha256()
with open(p,'rb') as f:
 for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
x={'verifiedAt':datetime.now(timezone.utc).isoformat(),'pipeline':4403172,'run':170,'commit':manifest['commit'],'archiveSafety':'PASS no extraction performed','artifactBytes':os.path.getsize(p),'artifactSha256':h.hexdigest(),'distFilesVerified':len(actual),'distCoverageExact':True,'testStats':stats,'packageVersion':manifest.get('package_version'),'buildOrigin':'aliyun_flow','deployment':'FLOW_SUCCESS_ONLINE_BYTES_PENDING','productAcceptance':'NOT_RUN'}
out='/home/isp/wsps/cyf/docs/implementation/evidence/t05-t09-business-closure-20261006/web170-artifact-verification.json';open(out,'w').write(json.dumps(x,indent=2)+'\n');print(json.dumps(x));print(json.dumps({'non_dist_non_report_files':[m.name for m in files if not m.name.startswith(prefix) and 'mochawesome' not in m.name]},ensure_ascii=False))


