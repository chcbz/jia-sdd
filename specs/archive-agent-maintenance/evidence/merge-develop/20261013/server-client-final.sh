#!/usr/bin/env bash
set -euo pipefail
# Adapted from the existing 20261008/server-node-final.sh: Client-only, no Web build/Gradle/production.
umask 077
base=/tmp/cyf-aam-merge-develop-20261013
repo="$base/isp-install"
out="$base/evidence/client-final"
[ ! -e "$out" ]; mkdir -p "$out" "$base/tmp-node"
exec > >(tee "$out/control.log") 2>&1
export CODEX_BIN=/bin/false AGENT_LLM_EXECUTION_ENABLED=false TMPDIR="$base/tmp-node"
unset CYF_CI_BOOTSTRAP CI PIPELINE_ID
[ "$(git -C "$repo" rev-parse HEAD)" = 5bec7d2f2dee597e8acb15f004c5a5abe6bd8004 ]
[ "$(git -C "$repo" rev-parse 'HEAD^{tree}')" = a36a452dc5666f3661d304cc3c3c229cac3efd5c ]
[ -z "$(git -C "$repo" status --porcelain)" ]
git -C "$repo" rev-parse HEAD 'HEAD^{tree}' > "$out/source-before.txt"
node --version > "$out/node-version.txt"
df -Pk "$base" > "$out/disk-before.txt"
cd "$repo/conf/codex-ws-agent"
npm ci --ignore-scripts --no-audit --no-fund > "$out/npm-ci.log" 2>&1
set +e
(umask 022; npm test -- --test-concurrency=1) > "$out/client-full.log" 2>&1
code=$?;set -e;echo "$code" > "$out/client.exit.txt"
cd "$repo/conf/cyf-agent-runtime-v1"
set +e
(umask 022; node --test --test-concurrency=1 test/runtime-host.test.mjs test/runtime-v1.test.mjs test/canonical-dispatch-r2.test.mjs) > "$out/runtime-targeted.log" 2>&1
code=$?;set -e;echo "$code" > "$out/runtime.exit.txt"
python3 - "$repo" "$out" <<'PY'
import pathlib,json,subprocess,sys,re,datetime
repo=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2])
def g(*args):return subprocess.check_output(['git','-C',str(repo)]+list(args),universal_newlines=True).strip()
result={'commit':g('rev-parse','HEAD'),'tree':g('rev-parse','HEAD^{tree}'),'status':g('status','--porcelain'),'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'production_changes':False,'real_runtime_e2e':False}
for name,filename in [('client','client-full.log'),('runtime','runtime-targeted.log')]:
 text=(out/filename).read_text();result[name]={'exit':int((out/(name+'.exit.txt')).read_text()),'counts':dict(re.findall(r'^# (tests|pass|fail|skipped|cancelled) (\d+)',text,re.M)),'failure_titles':re.findall(r'^not ok \d+ - (.*)$',text,re.M)}
result['source_unchanged']=result['commit']=='5bec7d2f2dee597e8acb15f004c5a5abe6bd8004' and result['tree']=='a36a452dc5666f3661d304cc3c3c229cac3efd5c' and not result['status']
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
PY
df -Pk "$base" > "$out/disk-after.txt"
