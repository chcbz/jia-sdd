set -eu
root=/dev/shm/cyf-aam-m6-test-20260930
dest=/fixtures/lifecycle-resume-20261007-candidate5/source
[ -x "$root/usr/bin/node" ]
[ ! -e "$root$dest" ]
mkdir -p "$root$dest"
tar -xf /mnt/host/c/tmp/aam-real-runtime-20261003/lifecycle-resume-20261007-candidate5/source.tar -C "$root$dest"
chroot "$root" /bin/sh -c 'set -eu; cd /fixtures/lifecycle-resume-20261007-candidate5/source/conf/codex-ws-agent; node --version; npm ci --ignore-scripts; sha256sum test/fixtures/archive-maintainer-1.0.0-approved.zip; mkdir -p /tmp/lifecycle-resume-20261007-candidate5; TMPDIR=/tmp/lifecycle-resume-20261007-candidate5 node --test test/platform-skill-manager.test.mjs test/platform-skill-native.test.mjs test/archive-maintenance-runner.test.mjs'
