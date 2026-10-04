set -eu
root=/dev/shm/cyf-aam-m6-test-20260930
dest=/fixtures/lifecycle-client-attempt2/source
[ -x "$root/usr/bin/node" ]
[ ! -e "$root$dest" ]
mkdir -p "$root$dest"
tar -xf /mnt/host/c/tmp/aam-real-runtime-20261003/lifecycle-client-attempt2/source.tar -C "$root$dest"
chroot "$root" /bin/sh -c 'set -eu; cd /fixtures/lifecycle-client-attempt2/source/conf/codex-ws-agent; node --version; npm ci --ignore-scripts; sha256sum test/fixtures/archive-maintainer-1.0.0-approved.zip; mkdir -p /tmp/lifecycle-client-attempt2; TMPDIR=/tmp/lifecycle-client-attempt2 node --test test/platform-skill-manager.test.mjs test/platform-skill-native.test.mjs test/archive-maintenance-runner.test.mjs'
