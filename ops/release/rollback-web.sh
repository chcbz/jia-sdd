#!/bin/bash -p
set -Eeuo pipefail
IFS=$'\n\t'
umask 077
export PATH='/usr/sbin:/usr/bin:/sbin:/bin'
export LC_ALL='C'
export HOME='/var/empty' CURL_HOME='/var/empty' GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL='/dev/null'
unset BASH_ENV ENV CDPATH GLOBIGNORE PYTHONPATH PYTHONHOME PYTHONSTARTUP LD_PRELOAD LD_LIBRARY_PATH

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
# shellcheck source=lib/web-deploy-adapter.sh
source "$SCRIPT_DIR/lib/web-deploy-adapter.sh"

usage() {
  cat <<'USAGE'
Usage: rollback-web.sh [--input PATH] [--dry-run|--execute] DEPLOY_RECORD.json

Default is read-only dry-run. Execution requires the same SHA-bound approval as
deploy-web.sh. The immutable deploy record, Web guard, candidate tree, restore
tree, approval ID, and all artifact/proof bindings are validated. Emergency
rollback uses the recorded genuine activation-proof digest and does not require
the external proof file to remain present. No process or API operation occurs.
USAGE
}

SHOW_HELP=0
parse_common_args "$@"
if (( SHOW_HELP == 1 )); then usage; exit 0; fi
((${#POSITIONAL[@]} == 1)) || die "one Web deploy record path is required"
web_adapter_select_default_input
for command in python3 sha256sum realpath stat grep mv cp flock mktemp sync find id; do require_command "$command"; done
web_adapter_load_input "$INPUT_FILE"
web_adapter_verify_guard 0
APPROVED_GUARD_SHA="$WEB_GUARD_SHA"
APPROVED_PROOF_SHA="$ACTIVATION_PROOF_SHA"
web_adapter_require_execute_approval
print_mode
web_adapter_acquire_execution_lock
web_adapter_verify_guard 0
[[ "$WEB_GUARD_SHA" == "$APPROVED_GUARD_SHA" && "$ACTIVATION_PROOF_SHA" == "$APPROVED_PROOF_SHA" ]] \
  || die "Web guard binding changed before the execution lock"

DEPLOY_RECORD="$(normalize_absolute_path 'Web deploy record' "${POSITIONAL[0]}")"
assert_path_within 'Web deploy record' "$DEPLOY_RECORD" "$WEB_RECORD_ROOT"
web_adapter_verify_immutable_with_sidecar "$DEPLOY_RECORD" >/dev/null
mapfile -d '' -t DEPLOY_FACTS < <(web_adapter_read_deploy_record "$DEPLOY_RECORD")
((${#DEPLOY_FACTS[@]} == 6)) || die "Web deploy record facts are incomplete"
BACKUP_DIR="$(normalize_absolute_path 'Web backup directory' "${DEPLOY_FACTS[0]}")"
RECORDED_LIVE_DIR="$(normalize_absolute_path 'recorded Web live directory' "${DEPLOY_FACTS[1]}")"
EXPECTED_CURRENT_TREE="${DEPLOY_FACTS[2]}"
EXPECTED_OLD_TREE="${DEPLOY_FACTS[3]}"
EXPECTED_ARCHIVE_SHA="${DEPLOY_FACTS[4]}"
RECORD_CHANGE_ID="${DEPLOY_FACTS[5]}"
require_sha256 'current Web tree' "$EXPECTED_CURRENT_TREE"
require_sha256 'old Web tree' "$EXPECTED_OLD_TREE"
require_sha256 'deployed Web archive' "$EXPECTED_ARCHIVE_SHA"
[[ "$EXPECTED_CURRENT_TREE" == "$WEB_EXTRACTED_TREE_SHA" ]] \
  || die "Web deploy record tree does not match the immutable Web guard"
[[ "$EXPECTED_ARCHIVE_SHA" == "$WEB_ARCHIVE_SHA_EXPECTED" ]] \
  || die "Web deploy record archive does not match the approved artifact digest"
[[ "$RECORDED_LIVE_DIR" == "$WEB_LIVE_DIR" ]] || die "Web deploy record live directory mismatch"
require_safe_id 'Web deploy record changeId' "$RECORD_CHANGE_ID"
if (( EXECUTE == 1 )); then
  [[ "$CYF_RELEASE_APPROVAL_ID" == "$RECORD_CHANGE_ID" ]] \
    || die "rollback approval ID must match the original deploy record changeId"
fi
assert_path_within 'Web backup directory' "$BACKUP_DIR" "$WEB_BACKUP_ROOT"
[[ -d "$BACKUP_DIR" && ! -L "$BACKUP_DIR" ]] || die "Web backup directory is unavailable or symlinked"
[[ -d "$WEB_LIVE_DIR" && ! -L "$WEB_LIVE_DIR" ]] || die "live Web kit is unavailable or symlinked"
[[ "$(hash_tree "$WEB_LIVE_DIR")" == "$EXPECTED_CURRENT_TREE" ]] \
  || die "current Web tree does not match the deployment being rolled back"
[[ "$(hash_tree "$BACKUP_DIR")" == "$EXPECTED_OLD_TREE" ]] \
  || die "Web backup tree checksum mismatch"
WEB_LIVE_PARENT="$(dirname -- "$WEB_LIVE_DIR")"
[[ -d "$WEB_LIVE_PARENT" && ! -L "$WEB_LIVE_PARENT" ]] || die "Web live parent is unavailable or symlinked"
assert_path_within 'Web backup root' "$WEB_BACKUP_ROOT" "$WEB_LIVE_PARENT"
assert_path_within 'Web record root' "$WEB_RECORD_ROOT" "$WEB_BACKUP_ROOT"
assert_disk_gate "$WEB_LIVE_PARENT" 'Web rollback filesystem'
assert_disk_gate "$WEB_BACKUP_ROOT" 'Web rollback backup filesystem'
[[ "$(stat -c %d -- "$WEB_LIVE_PARENT")" == "$(stat -c %d -- "$WEB_BACKUP_ROOT")" ]] \
  || die "Web live, staging and backup paths must share one filesystem"

log "Web rollback dry-run evidence: current_tree_sha256=$EXPECTED_CURRENT_TREE restore_tree_sha256=$EXPECTED_OLD_TREE guard_sha256=$WEB_GUARD_SHA activation_proof_sha256=$ACTIVATION_PROOF_SHA"
if (( EXECUTE == 0 )); then
  printf 'DRY_RUN=PASS\nCOMPONENT=web-rollback\nCURRENT_TREE_SHA256=%s\nRESTORE_TREE_SHA256=%s\nBACKUP_DIR=%s\nWEB_GUARD_SHA256=%s\nACTIVATION_PROOF_SHA256=%s\n' \
    "$EXPECTED_CURRENT_TREE" "$EXPECTED_OLD_TREE" "$BACKUP_DIR" "$WEB_GUARD_SHA" "$ACTIVATION_PROOF_SHA"
  exit 0
fi

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
CHANGE_ID="$CYF_RELEASE_APPROVAL_ID"
STAGE_DIR="$WEB_LIVE_PARENT/.kit-rollback-stage-${STAMP}-${WEB_HEAD}-${WEB_TREE}-${CHANGE_ID}"
RESCUE_DIR="$WEB_BACKUP_ROOT/kit-rescue-${STAMP}-${WEB_HEAD}-${WEB_TREE}-${CHANGE_ID}"
ROLLBACK_RECORD="$WEB_RECORD_ROOT/web-rollback-${STAMP}-${WEB_HEAD}-${WEB_TREE}-${CHANGE_ID}.json"
RECORD_TEMP=''
CURRENT_MOVED=0
RESTORED_INSTALLED=0

restore_candidate_on_error() {
  local exit_code=$?
  trap - EXIT
  set +e
  if (( RESTORED_INSTALLED == 1 )) && [[ -d "$WEB_LIVE_DIR" ]]; then
    local failed="$WEB_BACKUP_ROOT/kit-rollback-failed-${STAMP}-${WEB_HEAD}-${CHANGE_ID}"
    [[ -e "$failed" ]] || web_adapter_move recovery-rollback-failed "$WEB_LIVE_DIR" "$failed"
  fi
  if (( CURRENT_MOVED == 1 )) && [[ -d "$RESCUE_DIR" && ! -e "$WEB_LIVE_DIR" ]]; then
    web_adapter_move recovery-rescue "$RESCUE_DIR" "$WEB_LIVE_DIR"
    if rescued_entry="$(web_adapter_health "$WEB_LIVE_DIR" "$WEB_HEALTH_TIMEOUT" "${WEB_HEALTH_URLS[@]}")"; then
      log "pre-rollback Web candidate restore health check PASS: entry_asset=$rescued_entry"
    else
      log 'CRITICAL: pre-rollback Web candidate restore health check failed'
    fi
  fi
  [[ -z "$RECORD_TEMP" || ! -e "$RECORD_TEMP" ]] || rm -f -- "$RECORD_TEMP"
  [[ ! -e "$STAGE_DIR" ]] || rm -rf --one-file-system -- "$STAGE_DIR"
  exit "$exit_code"
}
trap restore_candidate_on_error EXIT

[[ ! -e "$STAGE_DIR" && ! -e "$RESCUE_DIR" && ! -e "$ROLLBACK_RECORD" \
   && ! -e "${ROLLBACK_RECORD}.sha256" ]] \
  || die "Web rollback staging, rescue, or record path already exists"
mkdir -- "$STAGE_DIR"
cp -a -- "$BACKUP_DIR/." "$STAGE_DIR/"
web_adapter_maybe_fault rollback-staged-tree
[[ "$(hash_tree "$STAGE_DIR")" == "$EXPECTED_OLD_TREE" ]] || die "staged Web rollback checksum mismatch"
sync -f "$STAGE_DIR" 2>/dev/null || true
web_adapter_move rollback-rescue-rename "$WEB_LIVE_DIR" "$RESCUE_DIR"
CURRENT_MOVED=1
[[ "$(hash_tree "$RESCUE_DIR")" == "$EXPECTED_CURRENT_TREE" ]] || die "Web rescue backup checksum mismatch"
web_adapter_move rollback-cutover-rename "$STAGE_DIR" "$WEB_LIVE_DIR"
RESTORED_INSTALLED=1
sync -f "$WEB_LIVE_PARENT" 2>/dev/null || true
[[ "$(hash_tree "$WEB_LIVE_DIR")" == "$EXPECTED_OLD_TREE" ]] || die "restored Web tree checksum mismatch"

ENTRY_ASSET="$(web_adapter_health "$WEB_LIVE_DIR" "$WEB_HEALTH_TIMEOUT" "${WEB_HEALTH_URLS[@]}")" \
  || die "Web rollback health check failed"

RECORD_TEMP="$(mktemp "$WEB_RECORD_ROOT/.web-rollback-record.XXXXXX")"
python3 -B - "$RECORD_TEMP" "$RELEASE_ID" "$CHANGE_ID" "$API_HEAD" "$API_TREE" "$WEB_HEAD" "$WEB_TREE" \
  "$DEPLOY_RECORD" "$EXPECTED_OLD_TREE" "$EXPECTED_CURRENT_TREE" "$BACKUP_DIR" \
  "$RESCUE_DIR" "$ENTRY_ASSET" "$RELEASE_INPUT_SHA" "$WEB_ADAPTER_TOOL_SHA" \
  "$WEB_GUARD" "$WEB_GUARD_SHA" "$ACTIVATION_PROOF_SHA" <<'PY'
import datetime, json, os, sys
(path, release_id, change_id, api_head, api_tree, web_head, web_tree, deploy_record,
 restored_tree, replaced_tree, source_backup, rescue_backup, entry_asset, input_sha,
 tool_sha, guard, guard_sha, proof_sha) = sys.argv[1:]
record = {
  'schema': 'cyf-web-rollback-record-v2', 'status': 'ROLLED_BACK_HEALTHY',
  'releaseId': release_id, 'changeId': change_id,
  'completedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'apiHead': api_head, 'apiTree': api_tree, 'webHead': web_head, 'webTree': web_tree,
  'rolledBackDeployRecord': deploy_record, 'restoredTreeSha256': restored_tree,
  'replacedTreeSha256': replaced_tree, 'sourceBackupDir': source_backup,
  'rescueBackupDir': rescue_backup, 'entryAsset': entry_asset,
  'releaseInputSha256': input_sha, 'adapterToolSha256': tool_sha,
  'webGuard': guard, 'webGuardSha256': guard_sha,
  'activationProofSha256': proof_sha, 'databaseOperation': 'NOT_PERFORMED',
  'rabbitMqOperation': 'NOT_PERFORMED', 'apiActivationOperation': 'NOT_PERFORMED'
}
with open(path, 'w', encoding='utf-8') as stream:
    json.dump(record, stream, sort_keys=True, indent=2); stream.write('\n')
    stream.flush(); os.fsync(stream.fileno())
PY
web_adapter_publish_immutable_with_sidecar "$RECORD_TEMP" "$ROLLBACK_RECORD" >/dev/null
RECORD_TEMP=''
trap - EXIT
CURRENT_MOVED=0
RESTORED_INSTALLED=0
printf 'ROLLBACK_WEB=PASS\nRESTORED_TREE_SHA256=%s\nRESCUE_DIR=%s\nROLLBACK_RECORD=%s\nENTRY_ASSET=%s\nWEB_GUARD_SHA256=%s\nACTIVATION_PROOF_SHA256=%s\n' \
  "$EXPECTED_OLD_TREE" "$RESCUE_DIR" "$ROLLBACK_RECORD" "$ENTRY_ASSET" \
  "$WEB_GUARD_SHA" "$ACTIVATION_PROOF_SHA"
