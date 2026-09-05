#!/bin/bash -p
set -Eeuo pipefail
IFS=$'\n\t'
umask 077
export PATH='/usr/sbin:/usr/bin:/sbin:/bin'
export LC_ALL='C'
export HOME='/var/empty' CURL_HOME='/var/empty' GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL='/dev/null'
unset BASH_ENV ENV CDPATH GLOBIGNORE PYTHONPATH PYTHONHOME PYTHONSTARTUP LD_PRELOAD LD_LIBRARY_PATH \
  HTTP_PROXY HTTPS_PROXY ALL_PROXY NO_PROXY http_proxy https_proxy all_proxy no_proxy \
  CURL_CA_BUNDLE REQUESTS_CA_BUNDLE SSL_CERT_FILE SSL_CERT_DIR GIT_SSL_CAINFO GIT_SSL_CAPATH \
  GIT_CONFIG_COUNT GIT_SSL_NO_VERIFY GIT_PROXY_COMMAND OPENSSL_CONF OPENSSL_MODULES \
  AWS_CA_BUNDLE NODE_EXTRA_CA_CERTS

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
# shellcheck source=lib/web-deploy-adapter.sh
source "$SCRIPT_DIR/lib/web-deploy-adapter.sh"

usage() {
  cat <<'USAGE'
Usage: deploy-web.sh [--input PATH] [--dry-run|--execute]

Default is read-only dry-run. --execute requires the SHA-bound CYF release
approval variables. The accepted JVC-OAI archive and a genuine external API
activation proof must match an immutable Web guard before same-filesystem
staging, backup, rename cutover, health verification, and durable recording.
No process, database, RabbitMQ, or API activation operation is performed.
USAGE
}

SHOW_HELP=0
parse_common_args "$@"
if (( SHOW_HELP == 1 )); then usage; exit 0; fi
((${#POSITIONAL[@]} == 0)) || die "unexpected positional arguments"
web_adapter_select_default_input
for command in git /usr/bin/python3 sha256sum curl realpath stat grep mv flock mktemp sync find id; do require_command "$command"; done
web_adapter_load_input "$INPUT_FILE"
web_adapter_verify_guard 1
APPROVED_GUARD_SHA="$WEB_GUARD_SHA"
APPROVED_PROOF_SHA="$ACTIVATION_PROOF_SHA"
web_adapter_require_execute_approval
print_mode
web_adapter_acquire_execution_lock
assert_clean_candidate 'Web' "$WEB_REPO" "$WEB_REF" "$WEB_HEAD" "$WEB_TREE"
web_adapter_verify_guard 1
[[ "$WEB_GUARD_SHA" == "$APPROVED_GUARD_SHA" && "$ACTIVATION_PROOF_SHA" == "$APPROVED_PROOF_SHA" ]] \
  || die "Web guard or API activation proof changed before the execution lock"
ARCHIVE_SHA="$(web_adapter_archive_operation)"
[[ "$ARCHIVE_SHA" == "$WEB_ARCHIVE_SHA_EXPECTED" ]] || die "Web archive digest changed after validation"

[[ -d "$WEB_LIVE_DIR" && ! -L "$WEB_LIVE_DIR" ]] \
  || die "live Web kit must be one physical directory: $WEB_LIVE_DIR"
WEB_LIVE_PARENT="$(dirname -- "$WEB_LIVE_DIR")"
[[ -d "$WEB_LIVE_PARENT" && ! -L "$WEB_LIVE_PARENT" ]] || die "Web live parent is unavailable or symlinked"
web_adapter_assert_path_within 'Web backup root' "$WEB_BACKUP_ROOT" "$WEB_LIVE_PARENT"
web_adapter_assert_path_within 'Web record root' "$WEB_RECORD_ROOT" "$WEB_BACKUP_ROOT"
assert_disk_gate "$WEB_LIVE_PARENT" 'Web deploy filesystem'
assert_disk_gate "$WEB_BACKUP_ROOT" 'Web backup filesystem'

CURRENT_TREE_SHA="$(hash_tree "$WEB_LIVE_DIR")"
CANDIDATE_TREE_SHA="$WEB_EXTRACTED_TREE_SHA"
log "Web dry-run evidence: current_tree_sha256=$CURRENT_TREE_SHA candidate_tree_sha256=$CANDIDATE_TREE_SHA archive_sha256=$ARCHIVE_SHA guard_sha256=$WEB_GUARD_SHA activation_proof_sha256=$ACTIVATION_PROOF_SHA"

if (( EXECUTE == 0 )); then
  printf 'DRY_RUN=PASS\nCOMPONENT=web\nCURRENT_TREE_SHA256=%s\nCANDIDATE_TREE_SHA256=%s\nARCHIVE_SHA256=%s\nWEB_GUARD_SHA256=%s\nACTIVATION_PROOF_SHA256=%s\n' \
    "$CURRENT_TREE_SHA" "$CANDIDATE_TREE_SHA" "$ARCHIVE_SHA" "$WEB_GUARD_SHA" "$ACTIVATION_PROOF_SHA"
  exit 0
fi

STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
CHANGE_ID="$CYF_RELEASE_APPROVAL_ID"
STAGE_DIR="$WEB_LIVE_PARENT/.kit-stage-${STAMP}-${WEB_HEAD}-${WEB_TREE}-${CHANGE_ID}"
BACKUP_DIR="$WEB_BACKUP_ROOT/kit-backup-${STAMP}-${WEB_HEAD}-${WEB_TREE}-${CHANGE_ID}"
FAILED_DIR="$WEB_BACKUP_ROOT/kit-failed-${STAMP}-${WEB_HEAD}-${WEB_TREE}-${CHANGE_ID}"
DEPLOY_RECORD="$WEB_RECORD_ROOT/web-deploy-${STAMP}-${WEB_HEAD}-${WEB_TREE}-${CHANGE_ID}.json"
RECOVERY_RECORD="$WEB_RECORD_ROOT/web-recovery-deploy-${STAMP}-${WEB_HEAD}-${WEB_TREE}-${CHANGE_ID}.json"
RECORD_TEMP=''
BACKED_UP=0
INSTALLED=0
WEB_ADAPTER_RECORD_PRESERVE_LIVE=0
WEB_ADAPTER_RECORD_COMMIT_ATTEMPTED=0
WEB_ADAPTER_RECORD_EXPECTED_SHA=''
WEB_ADAPTER_PUBLICATION_FINAL_STATE=NOT_APPLICABLE
WEB_ADAPTER_PUBLICATION_SIDECAR_STATE=NOT_APPLICABLE
WEB_ADAPTER_PUBLICATION_SOURCE_STATE=NOT_APPLICABLE
WEB_ADAPTER_PUBLICATION_INTEGRITY=NOT_APPLICABLE
WEB_ADAPTER_PUBLICATION_LIVE_VALIDATION=NOT_APPLICABLE

restore_web_on_error() {
  local exit_code=$? recovery_failed=0 reason='' move_rc=0 restored_entry='' observed_tree=''
  trap - EXIT
  set +e
  if (( WEB_ADAPTER_RECORD_COMMIT_ATTEMPTED == 1 )); then
    web_adapter_reconcile_publication_failure "$RECORD_TEMP" "$DEPLOY_RECORD" \
      "$WEB_ADAPTER_RECORD_EXPECTED_SHA"
    WEB_ADAPTER_PUBLICATION_LIVE_VALIDATION=MISSING_OR_UNSAFE
    if [[ -d "$WEB_LIVE_DIR" && ! -L "$WEB_LIVE_DIR" ]]; then
      observed_tree="$(hash_tree "$WEB_LIVE_DIR" 2>/dev/null)"
      if [[ "$observed_tree" == "$CANDIDATE_TREE_SHA" ]]; then
        if restored_entry="$(web_adapter_health "$WEB_LIVE_DIR" "$WEB_HEALTH_TIMEOUT" "${WEB_HEALTH_URLS[@]}")"; then
          WEB_ADAPTER_PUBLICATION_LIVE_VALIDATION=MATCHING_HEALTHY
        else
          WEB_ADAPTER_PUBLICATION_LIVE_VALIDATION=MATCHING_UNHEALTHY
        fi
      else
        WEB_ADAPTER_PUBLICATION_LIVE_VALIDATION=TREE_MISMATCH
      fi
    fi
    reason="publication-uncertain-${WEB_ADAPTER_PUBLICATION_INTEGRITY}-${WEB_ADAPTER_PUBLICATION_LIVE_VALIDATION}"
    if web_adapter_publish_recovery_failure deploy "$RECOVERY_RECORD" "$CHANGE_ID" "$exit_code" \
      "$reason" "$WEB_LIVE_DIR" "$BACKUP_DIR" '' "$FAILED_DIR"; then
      log "FAILED_MANUAL_RECOVERY_REQUIRED: durable evidence=$RECOVERY_RECORD"
    else
      log "CRITICAL: FAILED_MANUAL_RECOVERY_REQUIRED evidence publication failed: $RECOVERY_RECORD"
    fi
    log "CRITICAL: publication failed after the parent commit-attempt boundary; preserving Web live state without reverse rollback: live_validation=$WEB_ADAPTER_PUBLICATION_LIVE_VALIDATION"
    exit "$exit_code"
  fi
  if (( INSTALLED == 1 )) && [[ -d "$WEB_LIVE_DIR" ]]; then
    if [[ -e "$FAILED_DIR" ]]; then
      recovery_failed=1; reason="${reason:+$reason,}failed-candidate-path-occupied"
      log 'CRITICAL: Web failed-candidate path already exists'
    elif web_adapter_move recovery-failed "$WEB_LIVE_DIR" "$FAILED_DIR"; then
      INSTALLED=0
    else
      move_rc=$?; recovery_failed=1
      reason="${reason:+$reason,}candidate-removal-rc${move_rc}"
      log "CRITICAL: failed to move the rejected Web candidate aside: rc=$move_rc"
    fi
  fi
  if (( BACKED_UP == 1 )); then
    if [[ -d "$BACKUP_DIR" && ! -e "$WEB_LIVE_DIR" ]]; then
      if web_adapter_move recovery-restore "$BACKUP_DIR" "$WEB_LIVE_DIR"; then
        BACKED_UP=0
        if restored_entry="$(web_adapter_health "$WEB_LIVE_DIR" "$WEB_HEALTH_TIMEOUT" "${WEB_HEALTH_URLS[@]}")"; then
          log "automatic Web restore health check PASS: entry_asset=$restored_entry"
        else
          recovery_failed=1; reason="${reason:+$reason,}restored-health"
          log 'CRITICAL: automatic Web restore health check failed'
        fi
      else
        move_rc=$?; recovery_failed=1
        reason="${reason:+$reason,}backup-restore-rc${move_rc}"
        log "CRITICAL: automatic Web backup restore failed: rc=$move_rc"
      fi
    elif [[ ! -e "$WEB_LIVE_DIR" ]]; then
      recovery_failed=1; reason="${reason:+$reason,}backup-missing"
      log 'CRITICAL: automatic Web restore cannot find the backup directory'
    elif (( INSTALLED == 0 )); then
      recovery_failed=1; reason="${reason:+$reason,}live-path-occupied"
      log 'CRITICAL: automatic Web restore found an unexpected live path'
    else
      recovery_failed=1
    fi
  fi
  [[ -z "$RECORD_TEMP" || ! -e "$RECORD_TEMP" ]] || rm -f -- "$RECORD_TEMP"
  [[ ! -e "$STAGE_DIR" ]] || rm -rf --one-file-system -- "$STAGE_DIR"
  if (( recovery_failed == 1 )); then
    if web_adapter_publish_recovery_failure deploy "$RECOVERY_RECORD" "$CHANGE_ID" "$exit_code" \
      "$reason" "$WEB_LIVE_DIR" "$BACKUP_DIR" '' "$FAILED_DIR"; then
      log "FAILED_MANUAL_RECOVERY_REQUIRED: durable evidence=$RECOVERY_RECORD"
    else
      log "CRITICAL: FAILED_MANUAL_RECOVERY_REQUIRED evidence publication failed: $RECOVERY_RECORD"
    fi
  fi
  exit "$exit_code"
}
trap restore_web_on_error EXIT

mkdir -p -- "$WEB_BACKUP_ROOT" "$WEB_RECORD_ROOT"
assert_not_symlink 'Web backup root' "$WEB_BACKUP_ROOT"
assert_not_symlink 'Web record root' "$WEB_RECORD_ROOT"
[[ "$(stat -c %d -- "$WEB_LIVE_PARENT")" == "$(stat -c %d -- "$WEB_BACKUP_ROOT")" ]] \
  || die "Web live, staging and backup paths must share one filesystem"
[[ ! -e "$STAGE_DIR" && ! -e "$BACKUP_DIR" && ! -e "$FAILED_DIR" \
   && ! -e "$DEPLOY_RECORD" && ! -e "${DEPLOY_RECORD}.sha256" \
   && ! -e "$RECOVERY_RECORD" && ! -e "${RECOVERY_RECORD}.sha256" ]] \
  || die "Web staging, backup, or record path already exists"
mkdir -- "$STAGE_DIR"
web_adapter_archive_operation "$STAGE_DIR" >/dev/null
find "$STAGE_DIR" -type d -exec chmod 0755 {} +
find "$STAGE_DIR" -type f -exec chmod 0644 {} +
[[ -f "$STAGE_DIR/index.html" ]] || die "staged Web release has no index.html"
web_adapter_maybe_fault staged-tree
STAGED_TREE_SHA="$(hash_tree "$STAGE_DIR")"
[[ "$STAGED_TREE_SHA" == "$CANDIDATE_TREE_SHA" ]] || die "staged Web tree checksum mismatch"
sync -f "$STAGE_DIR" 2>/dev/null || true

web_adapter_move backup-rename "$WEB_LIVE_DIR" "$BACKUP_DIR"
BACKED_UP=1
[[ "$(hash_tree "$BACKUP_DIR")" == "$CURRENT_TREE_SHA" ]] || die "Web backup tree checksum mismatch"
web_adapter_move cutover-rename "$STAGE_DIR" "$WEB_LIVE_DIR"
INSTALLED=1
sync -f "$WEB_LIVE_PARENT" 2>/dev/null || true
[[ "$(hash_tree "$WEB_LIVE_DIR")" == "$CANDIDATE_TREE_SHA" ]] || die "deployed Web tree checksum mismatch"

ENTRY_ASSET="$(web_adapter_health "$WEB_LIVE_DIR" "$WEB_HEALTH_TIMEOUT" "${WEB_HEALTH_URLS[@]}")" \
  || die "Web health check failed"

RECORD_TEMP="$(mktemp "$WEB_RECORD_ROOT/.web-deploy-record.XXXXXX")"
/usr/bin/python3 -I -B - "$RECORD_TEMP" "$RELEASE_ID" "$CHANGE_ID" "$API_HEAD" "$API_TREE" "$WEB_HEAD" \
  "$WEB_TREE" "$WEB_ARTIFACT" "$ARCHIVE_SHA" "$CANDIDATE_TREE_SHA" \
  "$CURRENT_TREE_SHA" "$WEB_LIVE_DIR" "$BACKUP_DIR" "$ENTRY_ASSET" \
  "$RELEASE_INPUT_SHA" "$WEB_ADAPTER_TOOL_SHA" "$WEB_GUARD" "$WEB_GUARD_SHA" \
  "$ACTIVATION_PROOF_SHA" "$ACTIVATION_HOST_IDENTITY_SHA" "$ACTIVATION_LIFECYCLE_SHA" \
  "$ACTIVATION_RECORD_SHA" "${WEB_HEALTH_URLS[@]}" <<'PY'
import datetime, json, os, sys
(path, release_id, change_id, api_head, api_tree, web_head, web_tree, artifact,
 artifact_sha, candidate_tree_sha, previous_tree_sha, live_dir, backup_dir,
 entry_asset, input_sha, tool_sha, guard, guard_sha, proof_sha, host_sha,
 lifecycle_sha, activation_record_sha, *health_urls) = sys.argv[1:]
record = {
  'schema': 'cyf-web-deploy-record-v2', 'status': 'DEPLOYED_HEALTHY',
  'releaseId': release_id, 'changeId': change_id,
  'completedAt': datetime.datetime.now(datetime.timezone.utc).isoformat(),
  'apiHead': api_head, 'apiTree': api_tree, 'webHead': web_head, 'webTree': web_tree,
  'artifact': artifact, 'artifactSha256': artifact_sha,
  'candidateTreeSha256': candidate_tree_sha, 'previousLiveTreeSha256': previous_tree_sha,
  'liveDir': live_dir, 'backupDir': backup_dir, 'entryAsset': entry_asset,
  'healthUrls': health_urls, 'releaseInputSha256': input_sha,
  'adapterToolSha256': tool_sha, 'webGuard': guard, 'webGuardSha256': guard_sha,
  'activationProofSha256': proof_sha, 'finalAcceptedHostIdentitySha256': host_sha,
  'finalAcceptedLifecycleSha256': lifecycle_sha, 'activationRecordSha256': activation_record_sha,
  'databaseOperation': 'NOT_PERFORMED', 'rabbitMqOperation': 'NOT_PERFORMED',
  'apiActivationOperation': 'NOT_PERFORMED'
}
with open(path, 'w', encoding='utf-8') as stream:
    json.dump(record, stream, sort_keys=True, indent=2); stream.write('\n')
    stream.flush(); os.fsync(stream.fileno())
PY
WEB_ADAPTER_RECORD_EXPECTED_SHA="$(web_adapter_stable_sha256 "$RECORD_TEMP")"
WEB_ADAPTER_RECORD_COMMIT_ATTEMPTED=1
web_adapter_publish_immutable_with_sidecar "$RECORD_TEMP" "$DEPLOY_RECORD" >/dev/null
RECORD_TEMP=''
trap - EXIT
BACKED_UP=0
INSTALLED=0
printf 'DEPLOY_WEB=PASS\nBACKUP_DIR=%s\nDEPLOY_RECORD=%s\nTREE_SHA256=%s\nENTRY_ASSET=%s\nWEB_GUARD_SHA256=%s\nACTIVATION_PROOF_SHA256=%s\n' \
  "$BACKUP_DIR" "$DEPLOY_RECORD" "$CANDIDATE_TREE_SHA" "$ENTRY_ASSET" \
  "$WEB_GUARD_SHA" "$ACTIVATION_PROOF_SHA"
