#!/usr/bin/env bash
set -euo pipefail
ctl=/tmp/aam-merge-develop-control-20261008
b=/tmp/cyf-aam-merge-develop-20261008
while [ ! -f "$ctl/server-api-attempt4-control.exit.txt" ];do sleep 20;done
[ "$(cat "$ctl/server-api-attempt4-control.exit.txt")" = 0 ]
python3 - "$b" <<'PY'
import pathlib,json,sys
b=pathlib.Path(sys.argv[1]);p=b/'evidence/attempt4'
x=json.loads((p/'api-result.json').read_text());s=json.loads((p/'final-source-snapshot.json').read_text())
assert x['all_requested_suites_have_fresh_xml'] and x['source_unchanged']
assert s['own_mysql_port34061_closed'] and all(v['source_unchanged'] for v in s['repos'].values())
assert s['repos']['root']['commit']=='46c905cde88ef4262c97679bcd6c56485c8c6220'
print('API4_FRESH_COMPLETE_BEFORE_NODE',x['gradle_exit'])
PY
bash "$ctl/server-node-final.sh"