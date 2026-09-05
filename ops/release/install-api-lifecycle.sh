#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/common.sh"
source "$SCRIPT_DIR/lib/api-host-transaction.sh"

INPUT_FILE="$SCRIPT_DIR/jvc-oai-r1-input.json"
CANDIDATE="$SCRIPT_DIR/host/cyf-api-kit"
PROOF=''
while (($#)); do
  case "$1" in
    --input) (($# >= 2)) || die "--input requires a path"; INPUT_FILE="$2"; shift 2 ;;
    --candidate) (($# >= 2)) || die "--candidate requires a path"; CANDIDATE="$2"; shift 2 ;;
    --local-consumer-proof) (($# >= 2)) || die "--local-consumer-proof requires a path"; PROOF="$2"; shift 2 ;;
    --help|-h) printf 'Usage: %s --input FILE --candidate FILE --local-consumer-proof FILE\n' "$0"; exit 0 ;;
    *) die "unknown installer option: $1" ;;
  esac
done
host_load_input "$INPUT_FILE"
if ! host_offline; then (( EUID == 0 )) || die "lifecycle installation requires root"; fi
if ! host_offline; then
  for path in /usr /usr/local /usr/local/sbin; do
    [[ -d "$path" && ! -L "$path" && "$(stat -Lc %U "$path")" == root ]] \
      || die "lifecycle destination path is not trusted: $path"
    (( (8#$(stat -Lc %a "$path") & 8#022) == 0 )) \
      || die "lifecycle destination path is writable by group/other: $path"
  done
fi
[[ -n "$PROOF" ]] || die "local-consumer proof is required"
[[ ! -L "$CANDIDATE" && ! -L "$PROOF" ]] || die "installer inputs must not be symlinks"
CANDIDATE="$(normalize_absolute_path 'lifecycle candidate' "$CANDIDATE")"
PROOF="$(normalize_absolute_path 'local-consumer proof' "$PROOF")"
[[ -f "$CANDIDATE" && ! -L "$CANDIDATE" && "$(stat -Lc %h "$CANDIDATE")" == 1 ]] \
  || die "candidate must be regular nlink1"
[[ "$(host_sha_regular "$CANDIDATE")" == "$CANDIDATE_LIFECYCLE_SHA" ]] \
  || die "reviewed lifecycle candidate digest mismatch"
if host_offline; then PROOF_EXPECTED="444:$(id -u):$(id -g):1"; INSTALLED_EXPECTED="755:$(id -u):$(id -g):1"; else PROOF_EXPECTED=444:0:0:1; INSTALLED_EXPECTED=755:0:0:1; fi
[[ -f "$PROOF" && ! -L "$PROOF" && "$(stat -Lc '%a:%u:%g:%h' "$PROOF")" == "$PROOF_EXPECTED" ]] \
  || die "consumer proof must be immutable root-owned nlink1"
python3 -B - "$PROOF" "$CANDIDATE_LIFECYCLE_SHA" <<'PY'
import json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as stream: data=json.load(stream)
expected = {'schema':'cyf-api-local-consumer-proof-v1', 'status':'ACCEPTED',
            'bindAddress':'127.0.0.1', 'consumer':'nginx-loopback',
            'candidateLifecycleSha256':sys.argv[2]}
if data != expected: raise SystemExit('local-consumer proof mismatch')
PY
host_validate_lock "$RELEASE_LOCK"
host_validate_lock "$LIFECYCLE_LOCK"
exec 8<>"$RELEASE_LOCK"; flock -n 8 || die "release lock is held"
[[ "$(stat -Lc '%d:%i' "$RELEASE_LOCK")" == "$(stat -Lc '%d:%i' /proc/$$/fd/8)" ]] || die "release lock replaced"
exec 9<>"$LIFECYCLE_LOCK"; flock -n 9 || die "lifecycle lock is held"
[[ "$(stat -Lc '%d:%i' "$LIFECYCLE_LOCK")" == "$(stat -Lc '%d:%i' /proc/$$/fd/9)" ]] || die "lifecycle lock replaced"
[[ -f "$LIFECYCLE" && ! -L "$LIFECYCLE" && "$(stat -Lc '%a:%u:%g:%h' "$LIFECYCLE")" == "$INSTALLED_EXPECTED" ]] \
  || die "installed lifecycle path is unsafe"
[[ "$(host_sha_regular "$LIFECYCLE")" == "$INSTALLED_LIFECYCLE_SHA" ]] \
  || die "installed lifecycle does not match exact prior SHA"
TEMP="$(dirname -- "$LIFECYCLE")/.cyf-api-kit.install.$$"
[[ ! -e "$TEMP" ]] || die "installer staging path exists"
python3 -B - "$CANDIDATE" "$TEMP" "$CANDIDATE_LIFECYCLE_SHA" <<'PY'
import hashlib, os, stat, sys
source, target, expected = sys.argv[1:]
sfd=os.open(source, os.O_RDONLY|getattr(os,'O_NOFOLLOW',0)); dfd=None
try:
    before=os.fstat(sfd)
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1: raise SystemExit('unsafe candidate')
    dfd=os.open(target, os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0), 0o700)
    digest=hashlib.sha256()
    while True:
        block=os.read(sfd, 1024*1024)
        if not block: break
        digest.update(block); view=memoryview(block)
        while view: view=view[os.write(dfd, view):]
    after=os.fstat(sfd)
    if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns)!=(after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns):
        raise SystemExit('candidate changed during copy')
    if digest.hexdigest()!=expected: raise SystemExit('candidate digest changed')
    os.fchown(dfd,os.geteuid(),os.getegid()); os.fchmod(dfd,0o755); os.fsync(dfd)
finally:
    os.close(sfd)
    if dfd is not None: os.close(dfd)
PY
trap 'rm -f -- "$TEMP"' EXIT
host_replace_durable "$TEMP" "$LIFECYCLE"
trap - EXIT
[[ "$(host_sha_regular "$LIFECYCLE")" == "$CANDIDATE_LIFECYCLE_SHA" ]] || die "installed digest verification failed"
printf 'INSTALL_API_LIFECYCLE=PASS\nSHA256=%s\n' "$CANDIDATE_LIFECYCLE_SHA"
