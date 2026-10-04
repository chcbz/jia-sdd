set -eu
pid=16631
expected=/dev/shm/cyf-aam-m6-test-20260930/fixtures/chapters-client-attempt1/source/conf/codex-ws-agent
[ "$(readlink /proc/$pid/cwd)" = "$expected" ]
[ "$(readlink /proc/$pid/exe)" = /dev/shm/cyf-aam-m6-test-20260930/usr/bin/node ]
[ "$(tr '\000' ' ' < /proc/$pid/cmdline)" = '/usr/bin/node test/archive-maintenance-runner.test.mjs ' ]
kill -TERM "$pid"
printf 'TERM owned runner PID %s after three recorded checkpoint failures and leaked test HTTP fixture; not a complete natural suite result\n' "$pid"
