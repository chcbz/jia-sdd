#!/usr/bin/env bash
set -euo pipefail
umask 077
base=/tmp/cyf-aam-merge-develop-20261008
out="$base/evidence/node-final"
[ ! -e "$out" ];[ -f "$base/evidence/attempt4/final-source-snapshot.json" ];mkdir -p "$out"
exec > >(tee "$out/control.log") 2>&1
export CODEX_BIN=/bin/false AGENT_LLM_EXECUTION_ENABLED=false
unset CYF_CI_BOOTSTRAP CI PIPELINE_ID
python3 - "$base" <<'PY'
import pathlib,json,subprocess,sys
b=pathlib.Path(sys.argv[1]);s=json.loads((b/'evidence/attempt4/final-source-snapshot.json').read_text())
for k,p in [('root',b/'root'),('api',b/'root/api'),('web',b/'root/web'),('client',b/'isp-install')]:
 def g(*a):return subprocess.check_output(['git','-C',str(p),*a],universal_newlines=True).strip()
 assert not g('status','--porcelain')
 assert g('rev-parse','HEAD')==s['repos'][k]['commit']
 assert g('rev-parse','HEAD^{tree}')==s['repos'][k]['tree']
(b/'evidence/node-final/source-before.json').write_text(json.dumps(s['repos'],indent=2)+'\n')
PY
cd "$base/isp-install/conf/codex-ws-agent"
set +e
(umask 022;npm test -- --test-concurrency=1) > "$out/client-full.log" 2>&1
result=$?;set -e;echo "$result" > "$out/client.exit.txt"
cd "$base/root/web"
set +e
(umask 022;npm test) > "$out/web-full.log" 2>&1
result=$?;set -e;echo "$result" > "$out/web.exit.txt"
mkdir "$out/web-report";cp -p mochawesome-report/mochawesome.json "$out/web-report/"
set +e
npm run build > "$out/web-build.log" 2>&1
result=$?;set -e;echo "$result" > "$out/web-build.exit.txt"
git diff -- src/auto-imports.d.ts src/components.d.ts > "$out/web-generated-typing-noise.diff"
git restore --source=HEAD --worktree -- src/auto-imports.d.ts src/components.d.ts
python3 - "$base" <<'PY'
import pathlib,json,sys,subprocess,re,datetime,hashlib
b=pathlib.Path(sys.argv[1]);p=b/'evidence/node-final';repos={}
for k,d in [('root',b/'root'),('api',b/'root/api'),('web',b/'root/web'),('client',b/'isp-install')]:
 def g(*a):return subprocess.check_output(['git','-C',str(d),*a],universal_newlines=True).strip()
 repos[k]={'commit':g('rev-parse','HEAD'),'tree':g('rev-parse','HEAD^{tree}'),'status':g('status','--porcelain'),'source_unchanged':not g('status','--porcelain')}
old=json.loads((p/'source-before.json').read_text());assert all(repos[k]['commit']==v['commit'] and repos[k]['tree']==v['tree'] and repos[k]['source_unchanged'] for k,v in old.items())
d=json.loads((p/'web-report/mochawesome.json').read_text());fails=[]
def walk(x):
 if isinstance(x,list):
  for v in x:walk(v)
 elif isinstance(x,dict):
  if x.get('state')=='failed':fails.append({k:x.get(k) for k in ('title','fullTitle','err')})
  for v in x.values():
   if isinstance(v,(dict,list)):walk(v)
walk(d)
baseline=json.loads((b/'evidence/node-develop-baseline/comparison.json').read_text());bs=set(baseline['web']['baseline_failures']);fs=set(f['fullTitle'] for f in fails);text=(p/'client-full.log').read_text()
r={'finished_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'repos':repos,'web':{'stats':d['stats'],'failures':fails,'introduced_vs_develop_four_files':sorted(fs-bs),'removed_vs_develop_four_files':sorted(bs-fs),'raw_report_sha256':hashlib.sha256((p/'web-report/mochawesome.json').read_bytes()).hexdigest(),'build_exit':int((p/'web-build.exit.txt').read_text())},'client':{'counts':dict(re.findall(r'^# (tests|pass|fail|skipped) (\d+)',text,re.M)),'failures':re.findall(r'^not ok \d+ - (.*)$',text,re.M),'exit':int((p/'client.exit.txt').read_text())},'node_suites_umask':'022','historical_failed_node_suites_umask':'077','production_operation':False,'business_acceptance':False}
(p/'result.json').write_text(json.dumps(r,indent=2)+'\n')
print('WEB',r['web']['stats'],'BUILD',r['web']['build_exit'],'INTRODUCED',r['web']['introduced_vs_develop_four_files']);print('CLIENT',r['client'])
PY