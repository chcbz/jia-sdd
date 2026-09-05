#!/usr/bin/env bash
set -Eeuo pipefail
IFS=$'\n\t'
umask 077

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd -P)"
RELEASE="$ROOT/ops/release"
SELECTOR=all
if [[ "${1:-}" == --selector && -n "${2:-}" && $# == 2 ]]; then SELECTOR="$2"; elif (($#)); then echo 'usage: test-api-host-adaptation.sh [--selector build-contract|locks|transactions|activation-installer-nginx|all]' >&2; exit 2; fi
case "$SELECTOR" in build-contract|locks|transactions|activation-installer-nginx|all) ;; *) echo "unknown selector: $SELECTOR" >&2; exit 2 ;; esac

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
pass() { printf 'PASS: %s\n' "$*"; }
expect_fail() { local output; set +e; output="$("$@" 2>&1)"; local rc=$?; set -e; ((rc != 0)) || fail "expected failure: $*"; printf '%s' "$output"; }

TMP="$(mktemp -d /tmp/cyf-host-adapt-test.XXXXXX)"
trap 'rm -rf -- "$TMP"' EXIT
TEST_ROOT="$TMP/root"
HEAD=34b67fed96061bf9c3132106ca219fc6f5f6ba05
TREE=fb42c46c1f63299a37b44d7e55c6a303ddf016f1

make_fake_lifecycle() {
  mkdir -p "$TEST_ROOT/usr/local/sbin" "$TEST_ROOT/opt/cyf/service/api/backups" \
    "$TEST_ROOT/opt/cyf/service/api/release-records" "$TEST_ROOT/tmp" "$TEST_ROOT/control"
  : > "$TEST_ROOT/tmp/cyf-release-api.lock"; chmod 0660 "$TEST_ROOT/tmp/cyf-release-api.lock"
  : > "$TEST_ROOT/tmp/cyf-api-lifecycle.lock"; chmod 0600 "$TEST_ROOT/tmp/cyf-api-lifecycle.lock"
  cat > "$TEST_ROOT/usr/local/sbin/cyf-api-kit" <<'SH'
#!/bin/bash -p
set -Eeuo pipefail
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
root="${CYF_RELEASE_TEST_ROOT:?}"
exec 9<>"$root/tmp/cyf-api-lifecycle.lock"; flock -n 9 || exit 36
printf 'lifecycle-held:%s\n' "$1" >> "$root/control/lifecycle.log"
if [[ "$1" == stop && -e "$root/control/partial-stop-next" ]]; then
  rm -f -- "$root/control/partial-stop-next"
  printf 'partial-stop:%s\n' "$1" >> "$root/control/lifecycle.log"
  exit 40
fi
if [[ "$1" == stop && -e "$root/control/fail-stop" ]]; then exit 41; fi
if [[ "$1" == start && -e "$root/control/fail-next-start" ]]; then rm -f "$root/control/fail-next-start"; exit 42; fi
case "$1" in stop|start|status) ;; *) exit 43 ;; esac
SH
  chmod 0755 "$TEST_ROOT/usr/local/sbin/cyf-api-kit"
}

make_input_and_artifact() {
  local artifact_root="$TMP/artifacts"
  mkdir -p "$artifact_root/api"
  INPUT="$TMP/input.json"
  python3 -B - "$RELEASE/jvc-oai-r1-input.json" "$INPUT" "$artifact_root" <<'PY'
import json,sys
source,target,artifact=sys.argv[1:]
with open(source,encoding='utf-8') as stream: data=json.load(stream)
data['artifactRoot']=artifact
with open(target,'w',encoding='utf-8') as stream: json.dump(data,stream,indent=2); stream.write('\n')
PY
  ARTIFACT="$artifact_root/api/cyf-api-$HEAD-$TREE.jar"
  python3 -B - "$ARTIFACT" <<'PY'
import sys,zipfile
with zipfile.ZipFile(sys.argv[1],'x',zipfile.ZIP_STORED) as jar:
    jar.writestr('META-INF/MANIFEST.MF','Manifest-Version: 1.0\nMain-Class: org.springframework.boot.loader.launch.JarLauncher\nStart-Class: cn.jia.Application\n\n')
    jar.writestr('org/springframework/boot/loader/launch/JarLauncher.class',b'fixture')
    jar.writestr('BOOT-INF/classes/application.properties',b'fixture=true\n')
PY
  chmod 0444 "$ARTIFACT"
  SHA="$(sha256sum "$ARTIFACT" | awk '{print $1}')"
  INPUT_SHA="$(sha256sum "$INPUT" | awk '{print $1}')"
  TOOL_SHA="$(bash -c 'source "$1/common.sh"; source "$1/lib/api-host-transaction.sh"; host_tool_digest' _ "$RELEASE")"
  cat > "$ARTIFACT.json" <<EOF
{
  "apiHead": "$HEAD",
  "apiTree": "$TREE",
  "artifact": "$(basename "$ARTIFACT")",
  "artifactSha256": "$SHA",
  "deployment": "NOT_PERFORMED",
  "fixtureDigest": "N/A",
  "gradleTask": ":starter:bootJar",
  "orchestratorTaskId": "JVC-OAI-ARTIFACT-API",
  "releaseId": "jvc-oai-host-adapt-r1",
  "releaseInputSha256": "$INPUT_SHA",
  "releaseToolSha256": "$TOOL_SHA",
  "schema": "cyf-api-host-artifact-v1",
  "sourceRef": "codex/juyiting-voice-release-api",
  "selector": "JVC-OAI-HOST-ADAPT-api-bootJar"
}
EOF
  chmod 0444 "$ARTIFACT.json"
  printf '%s  %s\n' "$SHA" "$(basename "$ARTIFACT")" > "$ARTIFACT.sha256"; chmod 0444 "$ARTIFACT.sha256"
  local meta_sha; meta_sha="$(sha256sum "$ARTIFACT.json"|awk '{print $1}')"
  printf '%s  %s\n' "$meta_sha" "$(basename "$ARTIFACT.json")" > "$ARTIFACT.json.sha256"; chmod 0444 "$ARTIFACT.json.sha256"
  python3 -B - "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar" <<'PY'
import sys,zipfile
with zipfile.ZipFile(sys.argv[1],'x',zipfile.ZIP_STORED) as jar:
    jar.writestr('META-INF/MANIFEST.MF','Manifest-Version: 1.0\nMain-Class: org.springframework.boot.loader.launch.JarLauncher\nStart-Class: cn.jia.Application\n\n')
    jar.writestr('org/springframework/boot/loader/launch/JarLauncher.class',b'prior-fixture')
    jar.writestr('BOOT-INF/classes/application.properties',b'fixture=prior\n')
PY
  chmod 0640 "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"
}

run_release() {
  env CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES \
    CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 \
    CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" "$@"
}

reset_fixture() { rm -rf -- "$TEST_ROOT" "$TMP/artifacts"; make_fake_lifecycle; make_input_and_artifact; }

make_canonical_lock_fixture() {
  CANONICAL_LOCK_ROOT="$TMP/canonical-locks"
  rm -rf -- "$CANONICAL_LOCK_ROOT"
  mkdir -m 0700 -- "$CANONICAL_LOCK_ROOT"
  : > "$CANONICAL_LOCK_ROOT/cyf-release-api.lock"; chmod 0660 "$CANONICAL_LOCK_ROOT/cyf-release-api.lock"
  : > "$CANONICAL_LOCK_ROOT/cyf-api-lifecycle.lock"; chmod 0600 "$CANONICAL_LOCK_ROOT/cyf-api-lifecycle.lock"
}

run_canonical_lock_validation() {
  env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" \
    "$RELEASE/host/cyf-api-kit" validate-lock-contract
}

test_build_contract() {
  python3 -B - "$RELEASE/build-api.sh" <<'PY'
import pathlib, sys

text = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
start = text.index('"$ORCHESTRATOR_PATH" gradle \\\n')
end = text.index('\n\nBUILT_JAR=', start)
call = text[start:end]
required_options = (
    '--cwd "$API_REPO"',
    '--tree-sha "$API_TREE"',
    '--selector "$ORCHESTRATOR_SELECTOR"',
    '--fixture-digest "$ORCHESTRATOR_FIXTURE"',
    '--artifact "$API_REPO/$API_JAR_RELATIVE_PATH"',
)
task = '"$ORCHESTRATOR_TASK" -- \\n'
gradlew = '"$API_REPO/gradlew"'
task_at = call.index(task)
if any(call.index(option) > task_at for option in required_options):
    raise SystemExit('orchestrator admission option appears after task ID')
if call.index(gradlew) < task_at:
    raise SystemExit('Gradle argv appears before orchestrator task/separator')
for argument in ('--max-workers=1', '--no-build-cache',
                 '-PrepoUsername=unused', '-PrepoPassword=unused'):
    if argument not in call:
        raise SystemExit('missing bounded nonpublishing build argument: ' + argument)
if 'TEMP_METADATA="$(mktemp ' not in text:
    raise SystemExit('metadata does not use a secure pre-created temporary file')
if "with open(path, 'w', encoding='utf-8')" not in text:
    raise SystemExit('metadata writer does not open the pre-created file')
if "with open(path, 'x', encoding='utf-8')" in text:
    raise SystemExit('metadata writer incorrectly exclusive-opens an existing mktemp file')
PY
  hostile="$TMP/hostile-bin"; mkdir -m 0700 -- "$hostile"
  marker="$TMP/hostile-environment-executed"
  cat > "$TMP/hostile-bash-env" <<EOF
printf injected > "$marker"
EOF
  cat > "$hostile/dirname" <<EOF
#!/bin/bash -p
printf injected > "$marker"
exit 70
EOF
  chmod 0700 "$TMP/hostile-bash-env" "$hostile/dirname"
  for script in deploy-api.sh rollback-api.sh activate-api-voice.sh install-api-lifecycle.sh; do
    env -i PATH="$hostile" BASH_ENV="$TMP/hostile-bash-env" "$RELEASE/$script" --help >/dev/null
  done
  [[ ! -e "$marker" ]] || fail "privileged entrypoint accepted hostile PATH/BASH_ENV"
  pass build-contract
}

test_locks() {
  make_canonical_lock_fixture
  output="$(run_canonical_lock_validation)"
  [[ "$output" == *'LOCK_CONTRACT=PASS'* && "$output" == *'LOCK_ORDER=FD8,FD9'* ]] || fail "canonical direct lock order"
  (
    exec 8<>"$CANONICAL_LOCK_ROOT/cyf-release-api.lock"; flock -n 8
    d="$(stat -Lc %d /proc/$$/fd/8)"; i="$(stat -Lc %i /proc/$$/fd/8)"
    env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" \
      CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE="$i" \
      CYF_RELEASE_LOCK_HELD=1 "$RELEASE/host/cyf-api-kit" validate-lock-contract >/dev/null
    expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=7 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE="$i" CYF_RELEASE_LOCK_HELD=1 "$RELEASE/host/cyf-api-kit" validate-lock-contract >/dev/null
    expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE=1 CYF_RELEASE_LOCK_HELD=1 "$RELEASE/host/cyf-api-kit" validate-lock-contract >/dev/null
    expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 "$RELEASE/host/cyf-api-kit" validate-lock-contract >/dev/null
  )
  (exec 8<>"$CANONICAL_LOCK_ROOT/cyf-release-api.lock"; d="$(stat -Lc %d /proc/$$/fd/8)"; i="$(stat -Lc %i /proc/$$/fd/8)"; expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE="$i" CYF_RELEASE_LOCK_HELD=1 "$RELEASE/host/cyf-api-kit" validate-lock-contract >/dev/null)
  (
    exec 7<>"$CANONICAL_LOCK_ROOT/cyf-release-api.lock"; flock -n 7
    exec 8<>"$CANONICAL_LOCK_ROOT/cyf-release-api.lock"
    d="$(stat -Lc %d /proc/$$/fd/8)"; i="$(stat -Lc %i /proc/$$/fd/8)"
    expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE="$i" CYF_RELEASE_LOCK_HELD=1 "$RELEASE/host/cyf-api-kit" validate-lock-contract >/dev/null
  )
  (
    exec 8<>"$CANONICAL_LOCK_ROOT/cyf-release-api.lock"; flock -n 8; d="$(stat -Lc %d /proc/$$/fd/8)"; i="$(stat -Lc %i /proc/$$/fd/8)"
    mv "$CANONICAL_LOCK_ROOT/cyf-release-api.lock" "$CANONICAL_LOCK_ROOT/replaced.lock"; : > "$CANONICAL_LOCK_ROOT/cyf-release-api.lock"; chmod 0660 "$CANONICAL_LOCK_ROOT/cyf-release-api.lock"
    expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE="$i" CYF_RELEASE_LOCK_HELD=1 "$RELEASE/host/cyf-api-kit" validate-lock-contract >/dev/null
  )
  make_canonical_lock_fixture
  (exec 7<>"$CANONICAL_LOCK_ROOT/cyf-release-api.lock"; flock 7; : > "$CANONICAL_LOCK_ROOT/holder-ready"; sleep 1) & holder=$!
  while [[ ! -e "$CANONICAL_LOCK_ROOT/holder-ready" ]]; do sleep 0.01; done
  expect_fail run_canonical_lock_validation >/dev/null
  wait "$holder"
  python3 -B - "$RELEASE/host/cyf-api-kit" <<'PY'
from pathlib import Path
import sys
text=Path(sys.argv[1]).read_text(encoding='utf-8')
branch=text[text.index('acquire_release_lock_contract() {'):text.index('acquire_lifecycle_lock_contract() {')]
inherited=branch.split('else',1)[0]
if 'exec 8<>' in inherited: raise SystemExit('inherited FD8 is reopened')
if text.count('--server.address=127.0.0.1') != 1 or '--server.address=0.0.0.0' in text:
    raise SystemExit('canonical source bind is not exact loopback')
if text.count('8>&- 9>&-') != 1: raise SystemExit('Java does not close both release descriptors')
PY
  pass locks
}

latest_record() { find "$TEST_ROOT/opt/cyf/service/api/release-records" -type f -name "$1" -print | sort | tail -1; }
record_status() { python3 -B -c 'import json,sys;print(json.load(open(sys.argv[1]))["status"])' "$1"; }

run_release_fault() {
  local name="$1" value="$2"; shift 2
  env "$name=$value" CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" \
    CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 \
    CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" "$@"
}

test_transactions() {
  reset_fixture; old_sha="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"
  run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "candidate swap"
  deploy_record="$(latest_record 'api-deploy-*.json')"
  [[ "$(python3 -B -c 'import json,sys;print(json.load(open(sys.argv[1]))["status"])' "$deploy_record")" == COMMITTED ]] || fail "deploy commit state"
  run_release "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$old_sha" ]] || fail "rollback old artifact"

  reset_fixture; run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; deploy_record="$(latest_record 'api-deploy-*.json')"; : > "$TEST_ROOT/control/fail-next-start"
  expect_fail run_release "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "failed rollback did not restore rescue candidate"

  reset_fixture; run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; deploy_record="$(latest_record 'api-deploy-*.json')"
  expect_fail env CYF_RELEASE_FAULT_REPLACE_MATCH=.cyf-api-rollback CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "rollback rename fault lost rescue candidate"

  reset_fixture; prior="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; : > "$TEST_ROOT/control/fail-stop"
  expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$prior" ]] || fail "stop fault changed artifact"
  [[ "$(record_status "$(latest_record 'api-deploy-*.json')")" == FAILED_MANUAL_RECOVERY_REQUIRED ]] || fail "unrecovered stop fault claimed health"

  reset_fixture; prior="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; : > "$TEST_ROOT/control/partial-stop-next"
  expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$prior" ]] || fail "partial stop did not restore prior artifact"
  partial_record="$(latest_record 'api-deploy-*.json')"
  [[ "$(record_status "$partial_record")" == ROLLED_BACK_HEALTHY ]] || fail "partial stop recovery lacks truthful terminal receipt"
  [[ "$(rg -c '^lifecycle-held:stop$' "$TEST_ROOT/control/lifecycle.log")" == 2 \
      && "$(rg -c '^lifecycle-held:start$' "$TEST_ROOT/control/lifecycle.log")" == 1 ]] \
    || fail "partial stop recovery did not canonical stop/restore/start"

  reset_fixture; prior="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; : > "$TEST_ROOT/control/fail-next-start"
  expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$prior" ]] || fail "start fault did not restore"

  reset_fixture; prior="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"
  expect_fail env CYF_RELEASE_FAULT_REPLACE_MATCH=.cyf-api-stage CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$prior" ]] || fail "rename fault changed artifact"

  for terminal_state in STARTED_HEALTHY COMMITTED; do
    reset_fixture
    expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE "$terminal_state" "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "terminal receipt fault rolled back healthy candidate"
    [[ "$(record_status "$(latest_record 'api-deploy-*.json')")" == FAILED_MANUAL_RECOVERY_REQUIRED ]] || fail "terminal receipt fault has stale state"
  done
  reset_fixture
  expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE_AFTER_REPLACE STARTED_HEALTHY "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "post-replace healthy receipt fault rolled back selected candidate"
  [[ "$(record_status "$(latest_record 'api-deploy-*.json')")" == FAILED_MANUAL_RECOVERY_REQUIRED ]] || fail "post-replace healthy receipt fault has stale state"

  reset_fixture
  expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE_AFTER_REPLACE COMMITTED "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "post-replace commit receipt fault rolled back selected candidate"
  [[ "$(record_status "$(latest_record 'api-deploy-*.json')")" == COMMITTED ]] || fail "post-replace commit receipt fault obscured durable commit"

  for finalize_fault in before-chmod file-fsync dir-fsync; do
    reset_fixture
    expect_fail run_release_fault CYF_RELEASE_FAULT_FINALIZE "$finalize_fault" "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "finalize fault rolled back committed candidate"
    [[ "$(record_status "$(latest_record 'api-deploy-*.json')")" == COMMITTED ]] || fail "finalize fault left stale committed selection"
  done

  reset_fixture; final_old_sha="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; deploy_record="$(latest_record 'api-deploy-*.json')"
  expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE STARTED_HEALTHY "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$final_old_sha" ]] || fail "rollback terminal receipt fault restored rescue candidate"
  [[ "$(record_status "$(latest_record 'api-rollback-*.json')")" == FAILED_MANUAL_RECOVERY_REQUIRED ]] || fail "rollback terminal receipt fault has stale state"

  reset_fixture; final_old_sha="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; deploy_record="$(latest_record 'api-deploy-*.json')"
  expect_fail run_release_fault CYF_RELEASE_FAULT_FINALIZE dir-fsync "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$final_old_sha" ]] || fail "rollback finalize fault restored stale rescue candidate"
  [[ "$(record_status "$(latest_record 'api-rollback-*.json')")" == COMMITTED ]] || fail "rollback finalize fault obscured committed selection"

  reset_fixture; ln "$ARTIFACT" "$TMP/artifact-hardlink"; expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; rm "$TMP/artifact-hardlink"
  chmod 0644 "$ARTIFACT"; expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; chmod 0444 "$ARTIFACT"
  mv "$ARTIFACT" "$ARTIFACT.real"; ln -s "$ARTIFACT.real" "$ARTIFACT"; expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  if [[ -d /dev/shm && "$(stat -Lc %d /dev/shm)" != "$(stat -Lc %d "$(dirname "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar")")" ]]; then
    (
      cross_root="$(mktemp -d /dev/shm/cyf-host-cross-device.XXXXXX)"
      chmod 0700 "$cross_root"
      cross_stage="$(mktemp "$cross_root/stage.XXXXXX")"
      trap 'rm -f -- "$cross_stage"; rmdir -- "$cross_root"' EXIT
      chmod 0600 "$cross_stage"; printf stage > "$cross_stage"
      expect_fail bash -c 'source "$1/common.sh"; source "$1/lib/api-host-transaction.sh"; CYF_RELEASE_OFFLINE_TEST=YES; CYF_RELEASE_TEST_ROOT="$2"; host_replace_durable "$3" "$4"' _ "$RELEASE" "$TEST_ROOT" "$cross_stage" "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar" >/dev/null
    )
  fi
  ! rg -n '\b(kill|pkill|pgrep|ps|java|nohup|setsid)\b' "$RELEASE/deploy-api.sh" "$RELEASE/rollback-api.sh" || fail "direct process control in transaction drivers"
  pass transactions
}

make_valid_config() {
  cache="$(python3 -B -c 'import base64;print(base64.b64encode(b"C"*32).decode())')"
  cat > "$TMP/voice.env" <<EOF
JIA_CHAT_VOICE_ENABLED=true
JIA_CHAT_VOICE_IDENTITY_HMAC_SECRET=IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
JIA_CHAT_VOICE_CACHE_ENCRYPTION_KEY=$cache
JIA_CHAT_VOICE_COMPATIBILITY_GATEWAY_ALLOWLIST=https://api.openai.com/v1
JIA_CHAT_VOICE_TRANSCRIPTION_ENABLED=true
JIA_CHAT_VOICE_TRANSCRIPTION_PROVIDER=openai-compatible
JIA_CHAT_VOICE_TRANSCRIPTION_MODEL=whisper-1
JIA_CHAT_VOICE_SYNTHESIS_ENABLED=true
JIA_CHAT_VOICE_SYNTHESIS_PROVIDER=openai-compatible
JIA_CHAT_VOICE_SYNTHESIS_MODEL=gpt-4o-mini-tts
JIA_CHAT_VOICE_SYNTHESIS_PROVIDER_VOICE=alloy
SPRING_AI_OPENAI_API_KEY=provider-sentinel-secret
SPRING_AI_OPENAI_BASE_URL=https://api.openai.com/v1
CYF_VOICE_SMOKE_BEARER_TOKEN=smoke-sentinel-secret
EOF
  chmod 0600 "$TMP/voice.env"
}

make_fake_curl() {
  cat > "$TMP/fake-curl" <<'SH'
#!/bin/bash -p
set -Eeuo pipefail
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
auth=''; IFS= read -r auth || true
body=''; dump_headers=''; url=''; data=''; forms=(); request_headers=()
while (($#)); do
 case "$1" in
   --output) body="$2"; shift 2 ;;
   --dump-header) dump_headers="$2"; shift 2 ;;
   --write-out|--request) shift 2 ;;
   --header) request_headers+=("$2"); shift 2 ;;
   --data) data="$2"; shift 2 ;;
   --form) forms+=("$2"); shift 2 ;;
   --silent|--show-error) shift ;;
   http://*) url="$1"; shift ;;
   *) exit 61 ;;
 esac
done
root="${CYF_RELEASE_TEST_ROOT:?}"
[[ "$auth" == 'Authorization: Bearer smoke-sentinel-secret' ]] || exit 62
[[ "${request_headers[0]:-}" == @- ]] || exit 63
if [[ -e "$root/control/fail-smoke" ]]; then printf 500; exit 0; fi
if [[ "$url" == http://127.0.0.1:10018/chat/speech/transcriptions ]]; then
  [[ ${#forms[@]} == 3 && "${forms[0]}" == audio=@* && -f "${forms[0]#audio=@}" \
      && "${forms[1]}" == requestId=* && "${forms[2]}" == language=zh-CN \
      && -z "$data" && -z "$dump_headers" ]] || exit 64
  request_id="${forms[1]#requestId=}"
  [[ "$request_id" =~ ^[A-Za-z0-9][A-Za-z0-9._:-]{15,127}$ ]] || exit 65
  printf '%s\n' "$request_id" > "$root/control/stt-request-id"
  printf '{"data":{"requestId":"%s","text":"ok","detectedLanguage":"zh-CN","durationMs":1}}\n' "$request_id" > "$body"
elif [[ "$url" == http://127.0.0.1:10018/chat/speech/synthesis ]]; then
  [[ ${#forms[@]} == 0 && "${request_headers[1]:-}" == 'Content-Type: application/json' \
      && "$data" == @* && -f "${data#@}" && -n "$dump_headers" ]] || exit 66
  request_id="$(python3 -B - "${data#@}" "$root/control/stt-request-id" <<'PY'
import json,re,sys
with open(sys.argv[1],encoding='utf-8') as stream: data=json.load(stream)
if set(data) != {'requestId','text','voice','format'}: raise SystemExit(1)
if data['text']!='聚义厅语音验收' or data['voice']!='juyiting-default' or data['format']!='mp3': raise SystemExit(1)
if not isinstance(data['requestId'],str) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:-]{15,127}',data['requestId']): raise SystemExit(1)
with open(sys.argv[2],encoding='utf-8') as stream: prior=stream.read().strip()
if data['requestId']==prior: raise SystemExit(1)
print(data['requestId'])
PY
)" || exit 67
  printf 'ID3fakeaudio' > "$body"
  printf 'HTTP/1.1 200 OK\r\nContent-Type: audio/mpeg\r\nCache-Control: no-store\r\nX-Voice-Request-Id: %s\r\nContent-Length: 12\r\n\r\n' "$request_id" > "$dump_headers"
else
  exit 68
fi
printf 200
SH
  chmod 0755 "$TMP/fake-curl"
}

assert_nginx_contract() {
  python3 -B - "$RELEASE/nginx/juyiting-voice-http.conf" \
    "$RELEASE/nginx/juyiting-voice-server.conf" "$RELEASE/nginx/juyiting-voice-deny.conf" <<'PY'
from pathlib import Path
import sys

def blocks(path):
    result=[]; outside=[]; current=[]; depth=0
    for raw in Path(path).read_text(encoding='utf-8').splitlines():
        line=raw.strip()
        if not line or line.startswith('#'): continue
        if depth == 0:
            if '{' not in line:
                outside.append(line); continue
            current=[line]
        else:
            current.append(line)
        depth += line.count('{') - line.count('}')
        if depth < 0: raise SystemExit('unbalanced Nginx block')
        if depth == 0:
            result.append((current[0][:-1].strip(), current[1:-1])); current=[]
    if depth or outside: raise SystemExit('unexpected Nginx top-level directive')
    return result

http=blocks(sys.argv[1]); server=blocks(sys.argv[2]); deny=blocks(sys.argv[3])
if http != [('upstream cyf_juyiting_voice_loopback', [
        'server 127.0.0.1:10018 max_fails=1 fail_timeout=5s;', 'keepalive 8;'])]:
    raise SystemExit('Nginx loopback upstream is not exact')
expected_common=[
    'proxy_request_buffering on;', 'proxy_buffering off;', 'proxy_http_version 1.1;',
    'proxy_set_header Connection "";', 'proxy_set_header Host 127.0.0.1;',
    'proxy_set_header Authorization $http_authorization;',
    'proxy_set_header X-Forwarded-Proto https;', 'proxy_set_header X-Forwarded-Host $host;']
expected={
 'location = /api/chat/speech/transcriptions': [
    'if ($request_method != POST) { return 405; }', 'client_max_body_size 10m;',
    *expected_common,
    'proxy_pass http://cyf_juyiting_voice_loopback/chat/speech/transcriptions;'],
 'location = /api/chat/speech/synthesis': [
    'if ($request_method != POST) { return 405; }', 'client_max_body_size 64k;',
    *expected_common,
    'proxy_pass http://cyf_juyiting_voice_loopback/chat/speech/synthesis;'],
}
if len(server) != 2 or {name for name,_ in server} != set(expected):
    raise SystemExit('Nginx voice route set is not exact')
for name, body in server:
    if body != expected[name]: raise SystemExit('Nginx route directives are not exact: '+name)
if deny != [('location ^~ /api/chat/speech/', ['return 404;'])]:
    raise SystemExit('Nginx deny closure is not exact')
PY
}

test_activation_installer_nginx() {
  reset_fixture; make_valid_config; printf 'audio' > "$TMP/audio.webm"; chmod 0444 "$TMP/audio.webm"
  ok_sha="$(printf ok | sha256sum | awk '{print $1}')"
  output="$(run_release "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --dry-run 2>&1)"
  [[ "$output" != *sentinel* ]] || fail "dry-run disclosed a secret"
  cp "$TMP/voice.env" "$TMP/bad.env"; printf 'UNKNOWN_SECRET=sentinel-never-print\n' >> "$TMP/bad.env"; chmod 0600 "$TMP/bad.env"
  output="$(expect_fail run_release "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/bad.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --dry-run)"
  [[ "$output" != *sentinel-never-print* ]] || fail "parser disclosed unknown secret"
  cp "$TMP/voice.env" "$TMP/duplicate.env"; printf 'JIA_CHAT_VOICE_ENABLED=true\n' >> "$TMP/duplicate.env"; chmod 0600 "$TMP/duplicate.env"
  expect_fail run_release "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/duplicate.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --dry-run >/dev/null
  make_fake_curl
  env CYF_RELEASE_FAKE_CURL="$TMP/fake-curl" CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
  [[ -f "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env" ]] || fail "activation config missing"

  reset_fixture; make_valid_config; make_fake_curl
  config_sha="$(sha256sum "$TMP/voice.env"|awk '{print $1}')"
  export CYF_RELEASE_FAKE_CURL="$TMP/fake-curl"
  expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE STARTED_HEALTHY "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
  unset CYF_RELEASE_FAKE_CURL
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')" == "$config_sha" ]] || fail "activation terminal receipt fault rolled back healthy config"
  [[ "$(record_status "$(latest_record 'voice-activation-*.json')")" == FAILED_MANUAL_RECOVERY_REQUIRED ]] || fail "activation terminal receipt fault has stale state"

  reset_fixture; make_valid_config; make_fake_curl
  config_sha="$(sha256sum "$TMP/voice.env"|awk '{print $1}')"
  export CYF_RELEASE_FAKE_CURL="$TMP/fake-curl"
  expect_fail run_release_fault CYF_RELEASE_FAULT_FINALIZE dir-fsync "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
  unset CYF_RELEASE_FAKE_CURL
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')" == "$config_sha" ]] || fail "activation finalize fault rolled back committed config"
  [[ "$(record_status "$(latest_record 'voice-activation-*.json')")" == COMMITTED ]] || fail "activation finalize fault obscured committed selection"

  reset_fixture; printf 'prior-config\n' > "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"; chmod 0600 "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"; prior_config_sha="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')"; : > "$TEST_ROOT/control/fail-smoke"
  expect_fail env CYF_RELEASE_FAKE_CURL="$TMP/fake-curl" CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')" == "$prior_config_sha" ]] || fail "activation fault did not restore prior config"

  assert_nginx_contract
  rg -q 'ops/orchestration/cyf_orchestrator.py' "$RELEASE/build-api.sh" || fail "orchestrator delegation"
  ! rg -n '(^|[^A-Z_])OPENAI_API_KEY' "$RELEASE/activate-api-voice.sh" "$RELEASE/host/cyf-api-kit" || fail "custom OPENAI_API_KEY"

  make_fake_lifecycle
  installed_sha="$(sha256sum "$TEST_ROOT/usr/local/sbin/cyf-api-kit"|awk '{print $1}')"; candidate_sha="$(sha256sum "$RELEASE/host/cyf-api-kit"|awk '{print $1}')"
  python3 -B - "$INPUT" "$installed_sha" "$candidate_sha" <<'PY'
import json,sys
path,installed,candidate=sys.argv[1:]
data=json.load(open(path)); data['host']['installedLifecycleSha256']=installed; data['host']['candidateLifecycleSha256']=candidate
json.dump(data,open(path,'w'),indent=2); open(path,'a').write('\n')
PY
  cat > "$TMP/proof.json" <<EOF
{"schema":"cyf-api-local-consumer-proof-v1","status":"ACCEPTED","bindAddress":"127.0.0.1","consumer":"nginx-loopback","candidateLifecycleSha256":"$candidate_sha"}
EOF
  chmod 0444 "$TMP/proof.json"
  chmod 0770 "$TEST_ROOT/usr/local"
  expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" "$RELEASE/install-api-lifecycle.sh" --input "$INPUT" --candidate "$RELEASE/host/cyf-api-kit" --local-consumer-proof "$TMP/proof.json" >/dev/null
  chmod 0700 "$TEST_ROOT/usr/local"
  mv "$TEST_ROOT/usr/local" "$TEST_ROOT/usr/local.real"; ln -s local.real "$TEST_ROOT/usr/local"
  expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" "$RELEASE/install-api-lifecycle.sh" --input "$INPUT" --candidate "$RELEASE/host/cyf-api-kit" --local-consumer-proof "$TMP/proof.json" >/dev/null
  rm -f -- "$TEST_ROOT/usr/local"; mv "$TEST_ROOT/usr/local.real" "$TEST_ROOT/usr/local"
  cp "$INPUT" "$TMP/wrong-input.json"; sed -i "s/$installed_sha/$(printf '0%.0s' {1..64})/" "$TMP/wrong-input.json"
  expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" "$RELEASE/install-api-lifecycle.sh" --input "$TMP/wrong-input.json" --candidate "$RELEASE/host/cyf-api-kit" --local-consumer-proof "$TMP/proof.json" >/dev/null
  env CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" "$RELEASE/install-api-lifecycle.sh" --input "$INPUT" --candidate "$RELEASE/host/cyf-api-kit" --local-consumer-proof "$TMP/proof.json" >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/usr/local/sbin/cyf-api-kit"|awk '{print $1}')" == "$candidate_sha" ]] || fail "installer digest"
  pass activation-installer-nginx
}

[[ "$SELECTOR" == build-contract || "$SELECTOR" == all ]] && test_build_contract
[[ "$SELECTOR" == locks || "$SELECTOR" == all ]] && test_locks
[[ "$SELECTOR" == transactions || "$SELECTOR" == all ]] && test_transactions
[[ "$SELECTOR" == activation-installer-nginx || "$SELECTOR" == all ]] && test_activation_installer_nginx
printf 'HOST_ADAPTATION_TESTS=PASS selector=%s\n' "$SELECTOR"
