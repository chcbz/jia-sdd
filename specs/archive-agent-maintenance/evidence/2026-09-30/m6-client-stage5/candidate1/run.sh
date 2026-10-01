set -eu
root=/dev/shm/cyf-aam-m6-test-20260930
[ -f "$root/etc/alpine-release" ]
work="$root/workspaces/candidate1"
[ ! -e "$work" ] || { echo 'fresh snapshot directory required'; exit 1; }
mkdir -p "$work"
tar -xf /mnt/host/c/tmp/aam-client-evidence-20260930/m6-runtime/candidate1/source.tar -C "$work"
chroot "$root" /bin/sh -c 'cd /workspaces/candidate1 && bash -n shell/codex_ws_agent_install.sh shell/common.sh && cd conf/codex-ws-agent && node --version && npm ci --ignore-scripts'
set +e
chroot "$root" /bin/sh -c 'cd /workspaces/candidate1/conf/codex-ws-agent && npm test'
code=$?
printf '%s\n' "$code" > /mnt/host/c/tmp/aam-client-evidence-20260930/m6-runtime/candidate1/tests.exit-code.txt
exit "$code"
