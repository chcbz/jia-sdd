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

usage() { printf 'Usage: %s --input <jvc-oai-web-deploy-r1-input.json>\n' "$0"; }
SHOW_HELP=0
parse_common_args "$@"
(( SHOW_HELP == 0 )) || { usage; exit 0; }
(( EXECUTE == 0 && ${#POSITIONAL[@]} == 0 )) || die "Web adapter verifier accepts only --input"
web_adapter_select_default_input
for command in git /usr/bin/python3 sha256sum realpath stat find id; do require_command "$command"; done
web_adapter_load_input "$INPUT_FILE"
assert_clean_candidate 'Web' "$WEB_REPO" "$WEB_REF" "$WEB_HEAD" "$WEB_TREE"
web_adapter_validate_activation_proof
VERIFY_DIR="$(mktemp -d "$WEB_GUARD_ROOT/.web-adapter-verify.XXXXXX")"
trap 'rm -rf --one-file-system -- "$VERIFY_DIR"' EXIT
web_adapter_archive_operation "$VERIFY_DIR" >/dev/null
find "$VERIFY_DIR" -type d -exec chmod 0755 {} +
find "$VERIFY_DIR" -type f -exec chmod 0644 {} +
EXTRACTED_TREE_SHA="$(hash_tree "$VERIFY_DIR")"
GUARD_SHA="$(web_adapter_write_guard "$EXTRACTED_TREE_SHA")"
web_adapter_verify_guard 1
[[ "$GUARD_SHA" == "$WEB_GUARD_SHA" && "$EXTRACTED_TREE_SHA" == "$WEB_EXTRACTED_TREE_SHA" ]] \
  || die "published Web guard failed exact self-verification"
printf 'VERIFY_WEB_DEPLOY_ADAPTER=PASS\nWEB_GUARD=%s\nWEB_GUARD_SHA256=%s\nARCHIVE_SHA256=%s\nEXTRACTED_TREE_SHA256=%s\nACTIVATION_PROOF_SHA256=%s\nDEPLOYMENT=NOT_PERFORMED\n' \
  "$WEB_GUARD" "$WEB_GUARD_SHA" "$WEB_ARCHIVE_SHA_EXPECTED" "$WEB_EXTRACTED_TREE_SHA" \
  "$ACTIVATION_PROOF_SHA"
