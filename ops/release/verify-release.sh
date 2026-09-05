#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/common.sh"
source "$SCRIPT_DIR/lib/api-host-transaction.sh"

usage() { printf 'Usage: %s --input <jvc-oai-r1-input.json>\n' "$0"; }
parse_common_args "$@"
(( SHOW_HELP == 0 )) || { usage; exit 0; }
(( EXECUTE == 0 && ${#POSITIONAL[@]} == 0 )) || die "verify-release accepts only --input"
host_load_input "$INPUT_FILE"
assert_clean_candidate api "$API_REPO" "$API_REF" "$API_HEAD" "$API_TREE"
verify_sha256_sidecar "$API_ARTIFACT"
verify_sha256_sidecar "$API_METADATA"
API_SHA="$(host_sha_regular "$API_ARTIFACT")"
host_validate_boot_jar "$API_ARTIFACT" || die "API artifact is not the expected executable Spring Boot JAR"
host_verify_artifact_metadata
printf 'VERIFY_RELEASE=PASS\nAPI_HEAD=%s\nAPI_TREE=%s\nAPI_SHA256=%s\nDEPLOYMENT=NOT_PERFORMED\n' \
  "$API_HEAD" "$API_TREE" "$API_SHA"
