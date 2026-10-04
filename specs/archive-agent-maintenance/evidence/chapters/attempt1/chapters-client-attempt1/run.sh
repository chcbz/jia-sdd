set -eu
root=/dev/shm/cyf-aam-m6-test-20260930
dest=/fixtures/chapters-client-attempt1/source
[ -x "$root/usr/bin/node" ]
[ ! -e "$root$dest" ]
mkdir -p "$root$dest"
tar -xf /mnt/host/c/tmp/aam-real-runtime-20261003/chapters-client-attempt1/source.tar -C "$root$dest"
chroot "$root" /bin/sh -c 'set -eu; cd /fixtures/chapters-client-attempt1/source/conf/codex-ws-agent; node --version; npm ci --ignore-scripts; sha256sum test/fixtures/archive-maintainer-1.0.0-approved.zip; mkdir -p /tmp/chapters-client-attempt1; TMPDIR=/tmp/chapters-client-attempt1 node --test test/archive-maintenance-runner.test.mjs test/platform-skill-runtime.test.mjs test/workspace-manager.test.mjs'
