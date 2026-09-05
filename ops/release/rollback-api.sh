#!/bin/bash -p
set -Eeuo pipefail
IFS=$'\n\t'
umask 077
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
export LC_ALL=C

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/common.sh"
source "$SCRIPT_DIR/lib/api-host-transaction.sh"

usage() { printf 'Usage: %s --input <jvc-oai-r1-input.json> [--dry-run|--execute] <deploy-record.json>\n' "$0"; }
parse_common_args "$@"
(( SHOW_HELP == 0 )) || { usage; exit 0; }
((${#POSITIONAL[@]} == 1)) || die "rollback-api requires one deploy record"
host_load_input "$INPUT_FILE"
host_require_execute_approval
[[ ! -L "${POSITIONAL[0]}" ]] || die "deploy record must not be a symlink"
DEPLOY_RECORD="$(normalize_absolute_path 'deploy record' "${POSITIONAL[0]}")"
case "$DEPLOY_RECORD" in
  "$RECORD_ROOT"/api-deploy-*.json) ;;
  *) die "deploy record is outside canonical record root" ;;
esac
if host_offline; then RECORD_UID="$(id -u)"; else RECORD_UID=0; fi
mapfile -t RECORD_FIELDS < <(python3 -B - "$DEPLOY_RECORD" "$API_HEAD" "$API_TREE" "$RECORD_UID" <<'PY'
import json, os, stat, sys
path, head, tree, expected_uid = sys.argv[1:]
info = os.lstat(path)
if (not stat.S_ISREG(info.st_mode) or info.st_nlink != 1
        or stat.S_IMODE(info.st_mode) != 0o444 or info.st_uid != int(expected_uid)):
    raise SystemExit('deploy record is not immutable')
with open(path, 'r', encoding='utf-8') as stream: data = json.load(stream)
if data.get('schema') != 'cyf-api-host-transaction-v1' or data.get('kind') != 'deploy' \
        or data.get('status') != 'COMMITTED' or data.get('apiHead') != head or data.get('apiTree') != tree:
    raise SystemExit('deploy record is not an exact committed candidate')
for key in ('backupArtifact', 'previousJarSha256', 'candidateJarSha256'):
    if not isinstance(data.get(key), str) or not data[key]: raise SystemExit('deploy record field missing')
print(data['backupArtifact']); print(data['previousJarSha256']); print(data['candidateJarSha256'])
PY
)
((${#RECORD_FIELDS[@]} == 3)) || die "deploy record validation failed"
BACKUP_JAR="${RECORD_FIELDS[0]}"; OLD_SHA="${RECORD_FIELDS[1]}"; EXPECTED_CURRENT_SHA="${RECORD_FIELDS[2]}"
[[ "$BACKUP_JAR" == "$BACKUP_ROOT"/* ]] || die "backup artifact is outside canonical backup root"
require_sha256 "previous JAR SHA" "$OLD_SHA"
require_sha256 "candidate JAR SHA" "$EXPECTED_CURRENT_SHA"
if host_offline; then BACKUP_EXPECTED="440:$(id -u):$(id -g):1"; else BACKUP_EXPECTED="440:0:$(id -g isp):1"; fi
[[ -f "$BACKUP_JAR" && ! -L "$BACKUP_JAR" && "$(stat -Lc '%a:%u:%g:%h' "$BACKUP_JAR")" == "$BACKUP_EXPECTED" ]] \
  || die "backup artifact metadata is unsafe"
[[ "$(host_sha_regular "$BACKUP_JAR")" == "$OLD_SHA" ]] || die "backup artifact digest mismatch"
host_validate_boot_jar "$BACKUP_JAR" || die "backup artifact is not a Spring Boot JAR"
if (( EXECUTE == 0 )); then
  printf 'DRY_RUN=PASS\nCOMPONENT=api-rollback\nRESTORE_SHA256=%s\n' "$OLD_SHA"
  exit 0
fi

host_prepare_transaction_dirs
host_acquire_release_lock
host_validate_live_jar
host_validate_boot_jar "$LIVE_JAR" || die "current rescue JAR is not a valid Spring Boot artifact"
CURRENT_SHA="$(host_sha_regular "$LIVE_JAR")"
[[ "$CURRENT_SHA" == "$EXPECTED_CURRENT_SHA" ]] || die "live JAR no longer matches deploy record"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"; CHANGE_ID="$CYF_RELEASE_APPROVAL_ID"
RESCUE_DIR="$BACKUP_ROOT/rescue-${STAMP}-${API_HEAD}-${CHANGE_ID}"
RESCUE_JAR="$RESCUE_DIR/cyf-api-kit-${CURRENT_SHA}.jar"
OLD_STAGE="$(dirname -- "$LIVE_JAR")/.cyf-api-rollback-${CHANGE_ID}"
RESCUE_STAGE="$(dirname -- "$LIVE_JAR")/.cyf-api-rescue-${CHANGE_ID}"
RECORD="$RECORD_ROOT/api-rollback-${STAMP}-${API_HEAD}-${CHANGE_ID}.json"
[[ ! -e "$RESCUE_DIR" && ! -e "$OLD_STAGE" && ! -e "$RESCUE_STAGE" && ! -e "$RECORD" ]] \
  || die "rollback destination already exists"
mkdir -m 0750 -- "$RESCUE_DIR"; if ! host_offline; then chown root:isp "$RESCUE_DIR"; fi
host_fsync_dir "$BACKUP_ROOT"
host_copy_exclusive "$LIVE_JAR" "$RESCUE_JAR" 0440 "$CURRENT_SHA"
host_copy_exclusive "$BACKUP_JAR" "$OLD_STAGE" 0640 "$OLD_SHA"
host_record_init "$RECORD" rollback "$CHANGE_ID" "$API_HEAD" "$API_TREE" "$RESCUE_JAR" "$CURRENT_SHA" "$OLD_SHA"
PHASE=PREPARED
rollback_failure() {
  local rc=$?; trap - EXIT; set +e
  case "$PHASE" in
    PREPARED)
      host_record_state "$RECORD" ABORTED_BEFORE_STOP 2>/dev/null || true
      host_finalize_record "$RECORD" 2>/dev/null || true
      ;;
    STOP_ATTEMPTED|STOPPED|CANDIDATE_INSTALLED)
      if host_call_lifecycle stop >/dev/null 2>&1 \
          && host_copy_exclusive "$RESCUE_JAR" "$RESCUE_STAGE" 0640 "$CURRENT_SHA" \
          && host_replace_durable "$RESCUE_STAGE" "$LIVE_JAR" \
          && host_call_lifecycle start >/dev/null 2>&1; then
        if ! host_record_state "$RECORD" ROLLED_BACK_HEALTHY 2>/dev/null; then
          host_record_state "$RECORD" FAILED_MANUAL_RECOVERY_REQUIRED 2>/dev/null || true
        fi
      else
        host_record_state "$RECORD" FAILED_MANUAL_RECOVERY_REQUIRED 2>/dev/null || true
      fi
      host_finalize_record "$RECORD" 2>/dev/null || true
      ;;
    STARTED_HEALTHY|COMMITTING)
      host_record_state "$RECORD" FAILED_MANUAL_RECOVERY_REQUIRED 2>/dev/null || true
      host_finalize_record "$RECORD" 2>/dev/null || true
      ;;
    COMMITTED)
      host_finalize_record "$RECORD" 2>/dev/null || true
      ;;
  esac
  [[ ! -e "$OLD_STAGE" ]] || rm -f -- "$OLD_STAGE"
  [[ ! -e "$RESCUE_STAGE" ]] || rm -f -- "$RESCUE_STAGE"
  exit "$rc"
}
trap rollback_failure EXIT
host_record_state "$RECORD" STOP_ATTEMPTED
PHASE=STOP_ATTEMPTED
host_call_lifecycle stop
PHASE=STOPPED
host_record_state "$RECORD" STOPPED
host_replace_durable "$OLD_STAGE" "$LIVE_JAR"
PHASE=CANDIDATE_INSTALLED
host_record_state "$RECORD" CANDIDATE_INSTALLED
[[ "$(host_sha_regular "$LIVE_JAR")" == "$OLD_SHA" ]] || die "restored JAR digest mismatch"
host_call_lifecycle start
PHASE=STARTED_HEALTHY
host_record_state "$RECORD" STARTED_HEALTHY
PHASE=COMMITTING
host_record_state "$RECORD" COMMITTED
PHASE=COMMITTED
host_finalize_record "$RECORD"
trap - EXIT
printf 'ROLLBACK_API=PASS\nSTATUS=COMMITTED\nRESTORED_SHA256=%s\nRECORD=%s\n' "$OLD_SHA" "$RECORD"
