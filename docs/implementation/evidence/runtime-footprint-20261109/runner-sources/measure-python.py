import importlib.util,json,os,subprocess,time,hashlib,shutil
from pathlib import Path
base=Path(__file__).parent;ev=Path('/home/isp/wsps/cyf/docs/implementation/evidence/runtime-footprint-20261109')
source=Path('/home/isp/apps/cyf-agent-runtime-v1/app/codex-bridge/.toolchain')
script=Path('/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/freeze-python.py')
stage=base/'probe-stage/codex-bridge/.toolchain'; stage.parent.mkdir(parents=True)
assert not stage.exists()
env=dict(os.environ,TMPDIR=str(base/'tmp'),TMP=str(base/'tmp'),TEMP=str(base/'tmp'),PYTHONDONTWRITEBYTECODE='1')
start=time.monotonic()
subprocess.run(['cp','-a','--reflink=never',str(source),str(stage)],check=True,env=env)
spec=importlib.util.spec_from_file_location('slim',str(script));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
with (ev/'real-python.log').open('wb') as log:
 before=int(subprocess.check_output(['du','-s','-B1',str(stage)]).split()[0])
 result=m.slim_staged_python(stage,base/'python-debug-symbols')
 code='''import json,sys,ssl,sqlite3,zlib,ctypes
import docx,openpyxl,pptx,pypdf,reportlab,lxml.etree
from PIL import Image
from reportlab.pdfgen import canvas
from pathlib import Path
p=Path(sys.argv[1]); c=canvas.Canvas(str(p/'probe.pdf')); c.drawString(10,10,'runtime slim probe'); c.save()
assert len(pypdf.PdfReader(str(p/'probe.pdf')).pages)==1
Image.new('RGB',(8,8),'white').save(str(p/'probe.png'))
assert Image.open(str(p/'probe.png')).size==(8,8)
print(json.dumps({'prefix':sys.prefix,'imports':'ok','pdf':'ok','image':'ok'}))
'''
 subprocess.run([str(stage/'bin/python'),'-I','-B','-c',code,str(base)],env=env,stdout=log,stderr=subprocess.STDOUT,check=True,timeout=120)
 after=int(subprocess.check_output(['du','-s','-B1',str(stage)]).split()[0])
 result.update(stageBeforeAllocatedBytes=before,stageAfterAllocatedBytes=after,stageSavedAllocatedBytes=before-after,seconds=time.monotonic()-start,scriptSha256=hashlib.sha256(script.read_bytes()).hexdigest(),productionChanged=False)
 (ev/'real-python-result.json').write_text(json.dumps(result,indent=2)+'\n')
 shutil.copy2(str(base/'python-debug-symbols/symbols.json'),str(ev/'python-symbols.json'))
 print(json.dumps(result))
