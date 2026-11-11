import runpy,json,hashlib,tarfile,tempfile,time,shutil,os
from pathlib import Path
root=Path('/dev/shm/cyf-local-fast-api-20261107-07')
out=Path('/home/isp/wsps/cyf/docs/implementation/evidence/local-release-fast-20261106')
m=runpy.run_path('/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy',run_name='read_only_validator')
r=json.loads((root/'result.json').read_text());p=r['package']; t=time.monotonic()
a=dict(schema_version=4,source_kind='LOCAL',source=p['identity'],package=p['package'],receipt_sha256=p['receiptSha256'],jar_sha256=p['applicationJarSha256'],expected_previous_sha256=hashlib.sha256(Path('/home/isp/hosts/cyf/api/cyf-api-kit.jar').read_bytes()).hexdigest(),consumed=False)
# This descriptor is for read-only validation only: never write production approval.
m['native_approval'](a);m['native_package'](a)
extract=Path(tempfile.mkdtemp(prefix='cyf-local-real-validate-',dir='/dev/shm'))
try:
 with tarfile.open(a['package']['path'],'r:gz') as tar:
  members=tar.getmembers(); expected={'application.jar','receipt.json','application.metadata.json','application.sidecar.json','dependency.provenance.json'}
  assert len(members)==5 and {x.name for x in members}==expected and all(x.isfile() for x in members)
  for member in members:
   with tar.extractfile(member) as src,(extract/member.name).open('wb') as dst:shutil.copyfileobj(src,dst)
 m['native_validate_payloads'](a,extract)
 receipt=json.loads((extract/'receipt.json').read_text())
 result=dict(status='PASS',scope='real stable LOCAL package accepted by original installer payload validator; no installation',source=a['source'],package=a['package'],applicationJarSha256=a['jar_sha256'],validationSeconds=round(time.monotonic()-t,3),tests=receipt['evidence']['tests'],installedHelpersUpdated=False,productionTouched=False)
 (out/'api-07-package-validation.json').write_text(json.dumps(result,indent=2)+'\n')
 for name in ['result.json','inputs.json','gradle.log'] :shutil.copyfile(root/name,out/('api-07-'+name))
 shutil.copyfile(extract/'receipt.json',out/'api-07-receipt.json')
 print(json.dumps({k:v for k,v in result.items() if k!='tests'},indent=2))
finally:shutil.rmtree(extract)
