#!/usr/bin/env bash
set -euo pipefail
umask 077
base=/tmp/cyf-aam-merge-develop-20261008
out="$base/evidence/node-develop-baseline"
[ ! -e "$out" ];mkdir -p "$out"
exec > >(tee "$out/control.log") 2>&1
export CODEX_BIN=/bin/false AGENT_LLM_EXECUTION_ENABLED=false
unset CYF_CI_BOOTSTRAP CI PIPELINE_ID
for pair in client:isp-install:0d80e588be271891348e38b8892d9b9a9b0bb436 web:root/web:dbfe20bca65d1939b37198bb55b5b95fd5fa2775;do
 key=${pair%%:*};tail=${pair#*:};src=${tail%%:*};sha=${tail#*:};dst="$base/${key}-develop-baseline"
 [ ! -e "$dst" ];git clone --no-checkout --shared "$base/$src" "$dst"
 git -C "$dst" checkout --detach "$sha"
 git -C "$dst" rev-parse HEAD HEAD^{tree} > "$out/$key-source-before.txt"
 git -C "$dst" status --porcelain >> "$out/$key-source-before.txt"
 if [ "$key" = client ];then cd "$dst/conf/codex-ws-agent";prior="$base/isp-install/conf/codex-ws-agent";else cd "$dst";prior="$base/root/web";fi
 if cmp -s package-lock.json "$prior/package-lock.json";then cp -a "$prior/node_modules" .;else npm ci > "$out/$key-install.log" 2>&1;fi
 set +e
 if [ "$key" = client ];then
  npm test -- --test-concurrency=1 > "$out/client-full.log" 2>&1
 else
  CYF_MERGE_WEB_RESULT="$out/web-affected-result.json" node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --timeout 10000 --exit --reporter /tmp/aam-merge-develop-control-20261008/merge-web-reporter.cjs tests/juyiting-bounty-inline-results.test.js tests/juyiting-occlusion-atlas-e9b.test.js tests/juyiting-occlusion-fragment-ownership.test.js tests/juyiting-occlusion-prop-sort.test.js > "$out/web-affected.log" 2>&1
 fi
 result=$?;set -e;echo "$result" > "$out/$key.exit.txt"
 git -C "$dst" rev-parse HEAD HEAD^{tree} > "$out/$key-source-after.txt"
 git -C "$dst" status --porcelain >> "$out/$key-source-after.txt"
done
cd "$base/isp-install/conf/codex-ws-agent"
set +e
(umask 022;node --test test/controlled-image-http-ledger.test.mjs) > "$out/merged-ledger-umask022.log" 2>&1
result=$?;set -e;echo "$result" > "$out/merged-ledger-umask022.exit.txt"
python3 - "$out" <<'PY'
import pathlib,json,re,sys,hashlib,datetime
p=pathlib.Path(sys.argv[1]);x=json.loads((p/'web-affected-result.json').read_text());text=(p/'client-full.log').read_text();old=json.loads((p.parent/'attempt2/node-full-result-summary.json').read_text());cur=set(f['title'] for f in x['failures']);merged=set(f['fullTitle'] for f in old['failures'])
r={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'web':{'scope':'four failing files only; not full develop regression','baseline_stats':x['stats'],'baseline_failures':sorted(cur),'merged_full_failures':sorted(merged),'introduced':sorted(merged-cur),'removed':sorted(cur-merged)},'client':{'baseline_counts':dict(re.findall(r'^# (tests|pass|fail|skipped) (\d+)',text,re.M)),'baseline_failures':re.findall(r'^not ok \d+ - (.*)$',text,re.M),'merged':old['client']['merged']},'production_operation':False,'business_acceptance':False}
(p/'comparison.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
PY