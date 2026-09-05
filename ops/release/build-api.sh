#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
umask 077

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
# shellcheck source=common.sh
source "$SCRIPT_DIR/common.sh"
# shellcheck source=lib/api-host-transaction.sh
source "$SCRIPT_DIR/lib/api-host-transaction.sh"

usage() { printf 'Usage: %s --input <jvc-oai-r1-input.json>\n' "$0"; }
parse_common_args "$@"
(( SHOW_HELP == 0 )) || { usage; exit 0; }
(( EXECUTE == 0 && ${#POSITIONAL[@]} == 0 )) || die "build-api accepts only --input"
host_load_input "$INPUT_FILE"
assert_clean_candidate api "$API_REPO" "$API_REF" "$API_HEAD" "$API_TREE"
[[ -x "$ORCHESTRATOR_PATH" && ! -L "$ORCHESTRATOR_PATH" ]] || die "canonical orchestrator is unavailable"
[[ -x "$API_REPO/gradlew" && ! -L "$API_REPO/gradlew" ]] || die "pinned Gradle wrapper is unavailable"

"$ORCHESTRATOR_PATH" gradle \
  --cwd "$API_REPO" \
  --tree-sha "$API_TREE" \
  --selector "$ORCHESTRATOR_SELECTOR" \
  --fixture-digest "$ORCHESTRATOR_FIXTURE" \
  --artifact "$API_REPO/$API_JAR_RELATIVE_PATH" \
  "$ORCHESTRATOR_TASK" -- \
  "$API_REPO/gradlew" --no-daemon --max-workers=1 --no-build-cache \
  -PrepoUsername=unused -PrepoPassword=unused "$API_GRADLE_TASK"

assert_clean_candidate api-after-build "$API_REPO" "$API_REF" "$API_HEAD" "$API_TREE"
BUILT_JAR="$API_REPO/$API_JAR_RELATIVE_PATH"
[[ -f "$BUILT_JAR" && ! -L "$BUILT_JAR" ]] || die "Gradle did not create the pinned JAR"
host_validate_boot_jar "$BUILT_JAR" || die "Gradle output is not the expected executable Spring Boot JAR"
mkdir -p -- "$(dirname -- "$API_ARTIFACT")"
install_immutable_file "$BUILT_JAR" "$API_ARTIFACT" 0444
API_SHA="$(host_sha_regular "$API_ARTIFACT")"
INPUT_SHA="$(host_sha_regular "$RELEASE_INPUT")"
TOOL_SHA="$(host_tool_digest)"
TEMP_METADATA="$(mktemp "$(dirname -- "$API_METADATA")/.metadata.XXXXXX")"
python3 -B - "$TEMP_METADATA" "$RELEASE_ID" "$API_REF" "$API_HEAD" "$API_TREE" \
  "$(basename -- "$API_ARTIFACT")" "$API_SHA" "$INPUT_SHA" "$TOOL_SHA" "$ORCHESTRATOR_TASK" \
  "$ORCHESTRATOR_SELECTOR" "$ORCHESTRATOR_FIXTURE" "$API_GRADLE_TASK" <<'PY'
import json, os, sys
(path, release_id, source_ref, head, tree, artifact, digest, input_sha, tool_sha,
 task, selector, fixture, gradle_task) = sys.argv[1:]
data = {'schema': 'cyf-api-host-artifact-v1', 'releaseId': release_id, 'sourceRef': source_ref,
        'apiHead': head, 'apiTree': tree, 'artifact': artifact, 'artifactSha256': digest,
        'releaseInputSha256': input_sha, 'releaseToolSha256': tool_sha, 'orchestratorTaskId': task,
        'selector': selector, 'fixtureDigest': fixture, 'gradleTask': gradle_task,
        'deployment': 'NOT_PERFORMED'}
with open(path, 'w', encoding='utf-8') as stream:
    json.dump(data, stream, sort_keys=True, indent=2); stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
PY
chmod 0444 "$TEMP_METADATA"
if ! ln -- "$TEMP_METADATA" "$API_METADATA" 2>/dev/null; then
  rm -f -- "$TEMP_METADATA"
  die "artifact metadata already exists"
fi
rm -f -- "$TEMP_METADATA"
write_sha256_sidecar "$API_ARTIFACT" >/dev/null
write_sha256_sidecar "$API_METADATA" >/dev/null
printf 'BUILD_API=PASS\nARTIFACT=%s\nSHA256=%s\n' "$API_ARTIFACT" "$API_SHA"
