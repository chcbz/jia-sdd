set -eu
expected=/dev/shm/cyf-aam-m6-test-20260930/fixtures/chapters-client-attempt1/source/conf/codex-ws-agent
for dir in /proc/[0-9]*; do
 cwd=$(readlink "$dir/cwd" 2>/dev/null || true)
 [ "$cwd" = "$expected" ] || continue
 exe=$(readlink "$dir/exe" 2>/dev/null || true)
 case "$exe" in */usr/bin/node) ;; *) continue ;; esac
 printf 'OWNED_NODE_PID=%s CWD=%s EXE=%s\n' "${dir##*/}" "$cwd" "$exe"
 tr '\000' ' ' < "$dir/cmdline"; printf '\n'
done
