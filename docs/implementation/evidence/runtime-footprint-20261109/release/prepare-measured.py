from pathlib import Path
import json,subprocess,time,os,hashlib
B=Path(__file__).parent;budget_path=B/'build-budget.json';budget=json.loads(budget_path.read_text());start=time.monotonic();code=1
try:
 with (B/'install/integration-final.log').open('wb') as log:
  subprocess.run(['/root/.local/bin/python3.11','-B',str(B/'install/test-install-integration.py')],env=dict(os.environ,TMPDIR=str(B/'tmp')),stdout=log,stderr=subprocess.STDOUT,check=True,timeout=600-budget['seconds'])
 with (B/'install/prepare.log').open('wb') as log:
  p=subprocess.run(['/root/.local/bin/python3.11','-B','-u',str(B/'install/prepare-runtime.py')],env=dict(os.environ,TMPDIR=str(B/'tmp'),TMP=str(B/'tmp'),TEMP=str(B/'tmp'),PYTHONDONTWRITEBYTECODE='1'),stdout=log,stderr=subprocess.STDOUT,timeout=600-budget['seconds']-(time.monotonic()-start));code=p.returncode
finally:
 elapsed=time.monotonic()-start;budget['seconds']+=elapsed;budget['phases'].append({'phase':'final installer regression and private candidate preparation/probes','seconds':elapsed,'exitCode':code});budget_path.write_text(json.dumps(budget,indent=2)+'\n');print(json.dumps({'exitCode':code,'seconds':elapsed,'cumulativeSeconds':budget['seconds']}),flush=True)
raise SystemExit(code)
