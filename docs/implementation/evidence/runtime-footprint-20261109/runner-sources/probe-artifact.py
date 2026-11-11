from pathlib import Path
import importlib.util,subprocess,os,json,time,hashlib
base=Path(__file__).parent;ev=Path('/home/isp/wsps/cyf/docs/implementation/evidence/runtime-footprint-20261109');script=Path('/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/python-artifact.py')
spec=importlib.util.spec_from_file_location('artifact',str(script));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
start=time.monotonic();source=base/'probe-stage/codex-bridge/.toolchain';archive=base/'python-slim-probe.tgz';manifest=base/'python-slim-probe.json';target=base/'recovered-python'
with (ev/'python-artifact.log').open('wb') as log:
 m.pack(source,archive,manifest);digest=m.extract(archive,manifest,target)
 code='import json,sys,ssl,sqlite3,zlib,ctypes,docx,openpyxl,pptx,pypdf,reportlab,lxml.etree; from PIL import Image; print(json.dumps({"prefix":sys.prefix,"imports":"ok"}))'
 subprocess.run([str(target/'bin/python'),'-I','-B','-c',code],check=True,stdout=log,stderr=subprocess.STDOUT,timeout=120,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(base/'tmp')))
 assert len({(target/'bin'/n).stat().st_ino for n in ('python','python3','python3.11')})==1
 assert (target/'lib/libpython3.11.so').stat().st_ino==(target/'lib/libpython3.11.so.1.0').stat().st_ino
 result={'seconds':time.monotonic()-start,'archiveSha256':digest,'scriptSha256':hashlib.sha256(script.read_bytes()).hexdigest(),'archiveBytes':archive.stat().st_size,'restoredAliasesShareInodes':True,'productionChanged':False,'probeOnlyNotReleaseArtifact':True}
 (ev/'python-artifact-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
