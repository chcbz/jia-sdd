#!/usr/bin/env bash
set -u
ctl=/tmp/aam-merge-develop-control-20261008
printf 'CONTROL_START %s\n' "$(date -Iseconds)"
bash "$ctl/server-verify-merged-source.sh" "$@"
result=$?
printf '%s\n' "$result" > "$ctl/server-control.exit.txt"
printf 'CONTROL_EXIT %s %s\n' "$result" "$(date -Iseconds)"
exit "$result"
