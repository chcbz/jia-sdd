"""Invoke the existing host LOCAL Web transaction for the authorized fixed candidate."""
import datetime,hashlib,json,os,pathlib,subprocess,time,shutil
P=pathlib.Path;T=time.monotonic();os.umask(0o077)
E=P(__file__).resolve().parent;ROOT=P('/home/isp/state/cyf-local-build/tasks/JUYITING-HELP-20261109');B=ROOT/'deploy-build';record=P('/home/isp/state/cyf-web-flow/record.json');site=P('/home/isp/hosts/cyf/web/kit');R={'startedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PREPARING','authorization':'User: 部署','component':'web','apiOrRuntimeChanged':False}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
try:
 result=json.loads((B/'result.json').read_text());manifest=json.loads((B/'manifest.json').read_text())
 assert result['status']=='BUILT' and result['source']['commit']=='af8fe8542bb0c93f0561ce4599bf8dd6829fbc0e'
 assert result['source']==manifest['source'] and manifest['tests']['stats']['failures']==0
 assert record.read_bytes()==(E/'record-before.json').read_bytes(),'Production changed since preflight; do not overwrite'
 pkg=P(result['artifact']['path']);assert sha(pkg)==result['artifact']['sha256']
 dest=ROOT/'package/web-1.16.133.tgz';assert not dest.exists();shutil.move(str(pkg),str(dest));os.chmod(dest,0o600)
 descriptor={'schema_version':1,'source_kind':'LOCAL','source':dict(manifest['source'],version=manifest['version'],buildId=manifest['buildId']),'package':{'path':str(dest),'sha256':sha(dest),'size':dest.stat().st_size},'previousIndexSha256':sha(site/'index.html'),'previousRecordSha256':sha(record)}
 d=E/'install-descriptor.json';d.write_text(json.dumps(descriptor,indent=2));os.chmod(d,0o600)
 R.update(source=descriptor['source'],artifact=descriptor['package'],helperSha256=sha(P('/usr/local/sbin/cyf-web-flow-deploy')))
 with (E/'install.log').open('w') as log:
  rc=subprocess.call(['/usr/bin/python3','-I','-B','/usr/local/sbin/cyf-web-flow-deploy','--source-local',str(d)],stdout=log,stderr=subprocess.STDOUT)
 R['exitCode']=rc
 shutil.copy2(record,E/'record-after.json');after=json.loads(record.read_text())
 assert rc==0 and after['status']=='online_verified' and after['source']==descriptor['source'] and after['artifact_sha256']==descriptor['package']['sha256']
 for n,item in manifest['files'].items():assert sha(site/n)==item['sha256'],n
 backup=P(after['backup']);assert sha(backup/'record-before.json')==descriptor['previousRecordSha256']
 R.update(status='DEPLOYED_ONLINE_VERIFIED',installedFiles=len(manifest['files']),onlineVerifiedFiles=after['onlineVerifiedFiles'],backup=str(backup),backupVerified=True,businessAcceptance='Production static integrity verified; authenticated help UI smoke recorded separately')
except Exception as e:R.update(status='FAIL',error=repr(e));raise
finally:
 R['wallSeconds']=round(time.monotonic()-T,3);(E/'result.json').write_text(json.dumps(R,indent=2,ensure_ascii=False));print(json.dumps(R,indent=2,ensure_ascii=False))
