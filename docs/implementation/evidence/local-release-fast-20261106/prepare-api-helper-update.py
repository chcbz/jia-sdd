"""Prepare only native LOCAL adapter delta; preserve unrelated installed behavior."""
import hashlib,json,os,py_compile,subprocess
from pathlib import Path
D=Path(__file__).resolve().parent; S=Path('/home/isp/wsps/cyf/ops/ci/aliyun-flow/host'); C=D/'api-native-helpers'
C.mkdir(mode=0o700,exist_ok=True)
records=[]
for name in ['cyf-api-flow-deploy','cyf-api-flow-install']:
 target=Path('/usr/local/sbin')/name; before=target.read_bytes(); source=(S/name).read_text()
 if name=='cyf-api-flow-deploy':
  installed=before.decode(); assert '# BEGIN NATIVE_LOCAL_SOURCE_V1' not in installed
  block=source[source.index('# BEGIN NATIVE_LOCAL_SOURCE_V1'):source.index('# END NATIVE_LOCAL_SOURCE_V1')+len('# END NATIVE_LOCAL_SOURCE_V1')]
  installed=installed.replace('/var/lib/cyf-api-flow','/home/isp/state/cyf-api-flow')
  needle='def main():\n'; assert installed.count(needle)==1
  installed=installed.replace(needle,block+'\n\n\n'+needle+"    if sys.argv[1:2] == ['--source-local']:\n        raise SystemExit(native_api_main(sys.argv[2:]))\n")
  content=installed.encode()
 else: content=source.encode()
 candidate=C/name; candidate.write_bytes(content);candidate.chmod(0o755)
 backup=C/(name+'.before');assert not backup.exists() or backup.read_bytes()==before;backup.write_bytes(before);backup.chmod(0o600)
 if name.endswith('install'):subprocess.check_call(['bash','-n',str(candidate)])
 else:compile(content,str(candidate),'exec')
 records.append(dict(path=str(target),candidate=str(candidate),beforeSha256=hashlib.sha256(before).hexdigest(),candidateSha256=hashlib.sha256(content).hexdigest(),backup=str(backup)))
(D/'api-native-helper-update-inputs.json').write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
