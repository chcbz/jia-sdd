#!/bin/sh
set -eu
umask 077
PATH=/usr/sbin:/usr/bin:/sbin:/bin
export PATH

ACTION=${1-}
SELF=$(readlink -f -- "$0")
BASE=$(dirname -- "$SELF")
MONITOR=/usr/local/libexec/cyf-juyiting-health.py
CONFIG=/etc/cyf-juyiting-health.json
STATE_DIR=/var/lib/cyf-juyiting-health
CRON=/etc/cron.d/cyf-juyiting-health
CANONICAL=/usr/local/sbin/cyf-api-kit
CANONICAL_SHA=56537824cd33f6333f199ea1cebda90b127b39c079e08daad6d164607f788ef5
CANDIDATE_MONITOR_SHA=657deab366401a07d50ed1acb05fa3cc274b93b1b340ffade06db83a07735d79

fail() { echo "ERROR: $*" >&2; exit 2; }

install_monitor_atomically() {
  /usr/bin/python3 -I - "$BASE/cyf-juyiting-health.py" "$MONITOR" "$CANDIDATE_MONITOR_SHA" <<'PY'
import hashlib, os, stat, sys, tempfile
source, target, expected_sha = sys.argv[1:]
target_dir = os.path.dirname(target)
source_flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
source_fd = os.open(source, source_flags)
temporary_fd = None
temporary = None
try:
    source_info = os.fstat(source_fd)
    if not stat.S_ISREG(source_info.st_mode) or source_info.st_uid != 0 \
            or source_info.st_gid != 0 or source_info.st_nlink != 1 \
            or stat.S_IMODE(source_info.st_mode) != 0o755:
        raise SystemExit(1)
    directory_info = os.lstat(target_dir)
    if not stat.S_ISDIR(directory_info.st_mode) or stat.S_ISLNK(directory_info.st_mode) \
            or directory_info.st_uid != 0 or directory_info.st_gid != 0 \
            or stat.S_IMODE(directory_info.st_mode) != 0o755:
        raise SystemExit(1)
    temporary_fd, temporary = tempfile.mkstemp(
        prefix=".cyf-juyiting-health.py.", dir=target_dir)
    os.fchmod(temporary_fd, 0o755)
    os.fchown(temporary_fd, 0, 0)
    digest = hashlib.sha256()
    while True:
        chunk = os.read(source_fd, 65536)
        if not chunk:
            break
        digest.update(chunk)
        offset = 0
        while offset < len(chunk):
            offset += os.write(temporary_fd, chunk[offset:])
    if digest.hexdigest() != expected_sha:
        raise SystemExit(1)
    os.fsync(temporary_fd)
    os.close(temporary_fd)
    temporary_fd = None
    os.replace(temporary, target)
    temporary = None
    directory_fd = os.open(target_dir, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)
    target_info = os.lstat(target)
    if not stat.S_ISREG(target_info.st_mode) or stat.S_ISLNK(target_info.st_mode) \
            or target_info.st_uid != 0 or target_info.st_gid != 0 \
            or target_info.st_nlink != 1 or stat.S_IMODE(target_info.st_mode) != 0o755:
        raise SystemExit(1)
finally:
    os.close(source_fd)
    if temporary_fd is not None:
        os.close(temporary_fd)
    if temporary is not None:
        try:
            os.unlink(temporary)
        except OSError:
            pass
PY
}

[ "$(id -u)" = 0 ] || fail "root required"
case "$SELF" in /home/isp/*) fail "copy this bundle to a root-owned staging directory before root execution";; esac

/usr/bin/python3 -I - "$BASE" "$SELF" \
  "$BASE/cyf-juyiting-health.py" "$BASE/cyf-juyiting-health.json.example" \
  "$BASE/cyf-juyiting-health.cron" <<'PY' || fail "staging chain or payload metadata unsafe"
import os, stat, sys
base = os.path.abspath(sys.argv[1])
expected = {
    os.path.abspath(sys.argv[2]): 0o755,
    os.path.abspath(sys.argv[3]): 0o755,
    os.path.abspath(sys.argv[4]): 0o600,
    os.path.abspath(sys.argv[5]): 0o644,
}
current = base
while True:
    info = os.lstat(current)
    if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode) \
            or info.st_uid != 0 or info.st_gid != 0 or stat.S_IMODE(info.st_mode) & 0o022:
        raise SystemExit(1)
    if current == '/':
        break
    current = os.path.dirname(current)
for path, mode in expected.items():
    info = os.lstat(path)
    if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode) \
            or info.st_uid != 0 or info.st_gid != 0 or info.st_nlink != 1 \
            or stat.S_IMODE(info.st_mode) != mode:
        raise SystemExit(1)
PY

[ "$(sha256sum "$BASE/cyf-juyiting-health.py" | awk '{print $1}')" = "$CANDIDATE_MONITOR_SHA" ] \
  || fail "monitor candidate digest is not the reviewed digest"
[ "$(sha256sum "$CANONICAL" | awk '{print $1}')" = "$CANONICAL_SHA" ] \
  || fail "canonical API lifecycle hash mismatch"

case "$ACTION" in
  install)
    [ -d /usr/local/libexec ] && [ ! -L /usr/local/libexec ] || fail "/usr/local/libexec missing/unsafe"
    [ "$(stat -Lc '%a:%u:%g' /usr/local/libexec)" = "755:0:0" ] || fail "/usr/local/libexec metadata mismatch"
    install_monitor_atomically || fail "atomic monitor activation failed"
    [ "$(stat -Lc '%a:%u:%g:%h' "$MONITOR")" = "755:0:0:1" ] || fail "installed monitor metadata mismatch"
    [ "$(sha256sum "$MONITOR" | awk '{print $1}')" = "$CANDIDATE_MONITOR_SHA" ] || fail "installed monitor digest mismatch"
    if [ ! -e "$STATE_DIR" ]; then
      install -d -o root -g root -m 0700 "$STATE_DIR"
    else
      [ -d "$STATE_DIR" ] && [ ! -L "$STATE_DIR" ] || fail "existing state directory unsafe"
      [ "$(stat -Lc '%a:%u:%g' "$STATE_DIR")" = "700:0:0" ] || fail "existing state directory must already be 700 root:root"
    fi
    if [ ! -e "$CONFIG" ]; then
      install -o root -g root -m 0600 "$BASE/cyf-juyiting-health.json.example" "$CONFIG"
    else
      [ -f "$CONFIG" ] && [ ! -L "$CONFIG" ] || fail "existing config unsafe"
      [ "$(stat -Lc '%a:%u:%g:%h' "$CONFIG")" = "600:0:0:1" ] || fail "existing config must be 600 root:root one-link"
    fi
    if [ ! -e "$STATE_DIR/state.json" ]; then
      /usr/bin/python3 -I "$MONITOR" --init
    else
      [ -f "$STATE_DIR/state.json" ] && [ ! -L "$STATE_DIR/state.json" ] || fail "existing state unsafe"
      [ "$(stat -Lc '%a:%u:%g:%h' "$STATE_DIR/state.json")" = "600:0:0:1" ] || fail "existing state must be 600 root:root one-link"
    fi
    echo "installed without cron activation or service restart"
    ;;
  install-cron)
    [ -f "$MONITOR" ] && [ ! -L "$MONITOR" ] || fail "install monitor first"
    [ "$(stat -Lc '%a:%u:%g:%h' "$MONITOR")" = "755:0:0:1" ] || fail "installed monitor metadata mismatch"
    [ "$(sha256sum "$MONITOR" | awk '{print $1}')" = "$CANDIDATE_MONITOR_SHA" ] || fail "installed monitor is not the reviewed candidate"
    [ -f "$CONFIG" ] && [ ! -L "$CONFIG" ] || fail "install config first"
    [ "$(stat -Lc '%a:%u:%g:%h' "$CONFIG")" = "600:0:0:1" ] || fail "config metadata mismatch"
    [ -f "$STATE_DIR/state.json" ] && [ ! -L "$STATE_DIR/state.json" ] || fail "initialize state first"
    [ "$(stat -Lc '%a:%u:%g:%h' "$STATE_DIR/state.json")" = "600:0:0:1" ] || fail "state metadata mismatch"
    cron_sha=$(sha256sum "$BASE/cyf-juyiting-health.cron" | awk '{print $1}')
    install -o root -g root -m 0644 "$BASE/cyf-juyiting-health.cron" "$CRON"
    [ "$(stat -Lc '%a:%u:%g:%h' "$CRON")" = "644:0:0:1" ] || fail "installed cron metadata mismatch"
    [ "$(sha256sum "$CRON" | awk '{print $1}')" = "$cron_sha" ] || fail "installed cron digest mismatch"
    echo "cron file installed; no daemon restart and no immediate check executed"
    ;;
  verify)
    [ -f "$MONITOR" ] && [ ! -L "$MONITOR" ] || fail "monitor missing/unsafe"
    [ "$(stat -Lc '%a:%u:%g:%h' "$MONITOR")" = "755:0:0:1" ] || fail "monitor metadata mismatch"
    [ "$(sha256sum "$MONITOR" | awk '{print $1}')" = "$CANDIDATE_MONITOR_SHA" ] || fail "monitor digest mismatch"
    [ -f "$CONFIG" ] && [ "$(stat -Lc '%a:%u:%g:%h' "$CONFIG")" = "600:0:0:1" ] || fail "config metadata mismatch"
    /usr/bin/python3 -I "$MONITOR" --status
    ;;
  *)
    echo "Usage: $0 {install|install-cron|verify}" >&2
    exit 2
    ;;
esac
