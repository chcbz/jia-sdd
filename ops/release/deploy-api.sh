#!/bin/bash -p
set -Eeuo pipefail
IFS=$'\n\t'
umask 077
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
export LC_ALL=C

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/common.sh"
source "$SCRIPT_DIR/lib/api-host-transaction.sh"

usage() { printf 'Usage: %s --input <jvc-oai-r1-input.json> [--dry-run|--execute]\n' "$0"; }
parse_common_args "$@"
(( SHOW_HELP == 0 )) || { usage; exit 0; }
((${#POSITIONAL[@]} == 0)) || die "deploy-api accepts no positional arguments"
host_load_input "$INPUT_FILE"
host_require_execute_approval
verify_sha256_sidecar "$API_ARTIFACT"
verify_sha256_sidecar "$API_METADATA"
NEW_SHA="$(host_sha_regular "$API_ARTIFACT")"
host_validate_boot_jar "$API_ARTIFACT" || die "candidate is not an executable Spring Boot JAR"
host_verify_artifact_metadata

if (( EXECUTE == 0 )); then
  printf 'DRY_RUN=PASS\nCOMPONENT=api\nCANONICAL_LIFECYCLE=%s\nLIVE_JAR=%s\nCANDIDATE_SHA256=%s\n' \
    "$CYF_HOST_LIFECYCLE" "$CYF_HOST_LIVE_JAR" "$NEW_SHA"
  exit 0
fi

host_prepare_transaction_dirs
host_acquire_release_lock
host_validate_live_jar
host_validate_boot_jar "$LIVE_JAR" || die "current live JAR is not a valid Spring Boot rescue candidate"
OLD_SHA="$(host_sha_regular "$LIVE_JAR")"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
CHANGE_ID="$CYF_RELEASE_APPROVAL_ID"
BACKUP_DIR="$BACKUP_ROOT/api-${STAMP}-${API_HEAD}-${CHANGE_ID}"
BACKUP_JAR="$BACKUP_DIR/cyf-api-kit-${OLD_SHA}.jar"
STAGE_JAR="$(dirname -- "$LIVE_JAR")/.cyf-api-stage-${CHANGE_ID}"
RESTORE_STAGE="$(dirname -- "$LIVE_JAR")/.cyf-api-restore-${CHANGE_ID}"
RECORD="$RECORD_ROOT/api-deploy-${STAMP}-${API_HEAD}-${CHANGE_ID}.json"
[[ ! -e "$BACKUP_DIR" && ! -e "$STAGE_JAR" && ! -e "$RESTORE_STAGE" && ! -e "$RECORD" ]] \
  || die "transaction destination already exists"
mkdir -m 0750 -- "$BACKUP_DIR"
if ! host_offline; then chown root:isp "$BACKUP_DIR"; fi
host_fsync_dir "$BACKUP_ROOT"
host_copy_exclusive "$LIVE_JAR" "$BACKUP_JAR" 0440 "$OLD_SHA"
host_copy_exclusive "$API_ARTIFACT" "$STAGE_JAR" 0640 "$NEW_SHA"
host_record_init "$RECORD" deploy "$CHANGE_ID" "$API_HEAD" "$API_TREE" "$BACKUP_JAR" "$OLD_SHA" "$NEW_SHA"

PHASE=PREPARED
deploy_failure() {
  local rc=$?
  trap - EXIT
  set +e
  case "$PHASE" in
    PREPARED)
      host_record_state "$RECORD" ABORTED_BEFORE_STOP 2>/dev/null || true
      host_finalize_record "$RECORD" 2>/dev/null || true
      ;;
    STOP_ATTEMPTED|STOPPED|CANDIDATE_INSTALLED)
      if host_call_lifecycle stop >/dev/null 2>&1 \
          && host_copy_exclusive "$BACKUP_JAR" "$RESTORE_STAGE" 0640 "$OLD_SHA" \
          && host_replace_durable "$RESTORE_STAGE" "$LIVE_JAR" \
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
  [[ ! -e "$STAGE_JAR" ]] || rm -f -- "$STAGE_JAR"
  [[ ! -e "$RESTORE_STAGE" ]] || rm -f -- "$RESTORE_STAGE"
  exit "$rc"
}
trap deploy_failure EXIT

host_record_state "$RECORD" STOP_ATTEMPTED
PHASE=STOP_ATTEMPTED
host_call_lifecycle stop
PHASE=STOPPED
host_record_state "$RECORD" STOPPED
host_replace_durable "$STAGE_JAR" "$LIVE_JAR"
PHASE=CANDIDATE_INSTALLED
host_record_state "$RECORD" CANDIDATE_INSTALLED
[[ "$(host_sha_regular "$LIVE_JAR")" == "$NEW_SHA" ]] || die "installed candidate digest mismatch"
host_call_lifecycle start
PHASE=STARTED_HEALTHY
host_record_state "$RECORD" STARTED_HEALTHY
PHASE=COMMITTING
host_record_state "$RECORD" COMMITTED
PHASE=COMMITTED
host_finalize_record "$RECORD"
trap - EXIT
printf 'DEPLOY_API=PASS\nSTATUS=COMMITTED\nCANDIDATE_SHA256=%s\nRECORD=%s\n' "$NEW_SHA" "$RECORD"
