#!/usr/bin/env bash
set -u
ctl=/tmp/aam-merge-develop-control-20261008
printf 'CONTROL_START %s\n' "$(date -Iseconds)"
bash "$ctl/server-verify-attempt2.sh" "$@"
result=$?
printf '%s\n' "$result" > "$ctl/server-attempt2-control.exit.txt"
printf 'CONTROL_EXIT %s %s\n' "$result" "$(date -Iseconds)"
exit "$result"
