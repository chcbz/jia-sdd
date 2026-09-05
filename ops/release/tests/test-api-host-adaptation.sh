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
OWNED_LOOPBACK_PIDS=()
cleanup() {
  local pid
  set +e
  for pid in "${OWNED_LOOPBACK_PIDS[@]}"; do
    wait "$pid" 2>/dev/null
  done
  rm -rf -- "$TMP"
}
trap cleanup EXIT
TEST_ROOT="$TMP/root"
HEAD=34b67fed96061bf9c3132106ca219fc6f5f6ba05
TREE=fb42c46c1f63299a37b44d7e55c6a303ddf016f1

make_fake_lifecycle() {
  mkdir -p "$TEST_ROOT/usr/local/sbin" "$TEST_ROOT/opt/cyf/service/api/backups" \
    "$TEST_ROOT/opt/cyf/service/api/release-records" "$TEST_ROOT/tmp" "$TEST_ROOT/control"
  : > "$TEST_ROOT/control/running"
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
  rm -f -- "$root/control/running"
  printf 'partial-stop:%s\n' "$1" >> "$root/control/lifecycle.log"
  exit 40
fi
if [[ "$1" == stop && -e "$root/control/fail-stop" ]]; then exit 41; fi
if [[ "$1" == start && -e "$root/control/fail-next-start" ]]; then rm -f "$root/control/fail-next-start"; exit 42; fi
case "$1" in
  stop) rm -f -- "$root/control/running" ;;
  start) : > "$root/control/running" ;;
  status) ;;
  *) exit 43 ;;
esac
SH
  chmod 0755 "$TEST_ROOT/usr/local/sbin/cyf-api-kit"
}

make_input_and_artifact() {
  local artifact_root="$TMP/artifacts"
  mkdir -p "$artifact_root/api"
  INPUT="$TMP/input.json"
  /usr/bin/python3 -I -B - "$RELEASE/jvc-oai-r1-input.json" "$INPUT" "$artifact_root" <<'PY'
import json,sys
source,target,artifact=sys.argv[1:]
with open(source,encoding='utf-8') as stream: data=json.load(stream)
data['artifactRoot']=artifact
with open(target,'w',encoding='utf-8') as stream: json.dump(data,stream,indent=2); stream.write('\n')
PY
  ARTIFACT="$artifact_root/api/cyf-api-$HEAD-$TREE.jar"
  /usr/bin/python3 -I -B - "$ARTIFACT" <<'PY'
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
  /usr/bin/python3 -I -B - "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar" <<'PY'
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

make_hostile_python_fixture() {
  HOSTILE_PYTHON="$TMP/hostile-python"
  HOSTILE_PYTHON_MARKER="$TMP/hostile-python-executed"
  rm -rf -- "$HOSTILE_PYTHON"; rm -f -- "$HOSTILE_PYTHON_MARKER"
  mkdir -m 0700 -- "$HOSTILE_PYTHON"
  local module
  for module in json pathlib hashlib tempfile sitecustomize; do
    cat > "$HOSTILE_PYTHON/$module.py" <<EOF
with open('$HOSTILE_PYTHON_MARKER', 'a') as stream:
    stream.write('$module\\n')
raise RuntimeError('ambient Python module executed')
EOF
    chmod 0600 "$HOSTILE_PYTHON/$module.py"
  done
}

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
  /usr/bin/python3 -I -B - "$RELEASE/build-api.sh" <<'PY'
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

  reset_fixture; make_valid_config; printf 'audio' > "$TMP/python-audio.webm"; chmod 0444 "$TMP/python-audio.webm"
  make_hostile_python_fixture
  (
    cd -- "$HOSTILE_PYTHON"
    export PYTHONPATH="$HOSTILE_PYTHON" PYTHONHOME="$HOSTILE_PYTHON" PYTHONSTARTUP="$HOSTILE_PYTHON/sitecustomize.py"
    run_release "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" \
      --audio-fixture "$TMP/python-audio.webm" \
      --expected-transcript-sha256 "$(printf ok | sha256sum | awk '{print $1}')" --dry-run >/dev/null
  )
  [[ ! -e "$HOSTILE_PYTHON_MARKER" ]] || fail "actual host validation imported ambient Python code"
  pass build-contract
}

test_locks() {
  make_canonical_lock_fixture
  output="$(run_canonical_lock_validation)"
  [[ "$output" == *'LOCK_CONTRACT=PASS'* && "$output" == *'LOCK_ORDER=FD8,FD9'* ]] || fail "canonical direct lock order"
  make_hostile_python_fixture
  (
    cd -- "$HOSTILE_PYTHON"
    export PYTHONPATH="$HOSTILE_PYTHON" PYTHONHOME="$HOSTILE_PYTHON" PYTHONSTARTUP="$HOSTILE_PYTHON/sitecustomize.py"
    exec 8<>"$CANONICAL_LOCK_ROOT/cyf-release-api.lock"; flock -n 8
    d="$(stat -Lc %d /proc/$$/fd/8)"; i="$(stat -Lc %i /proc/$$/fd/8)"
    env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" \
      CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE="$i" \
      CYF_RELEASE_LOCK_HELD=1 "$RELEASE/host/cyf-api-kit" validate-lock-contract >/dev/null
    expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=7 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE="$i" CYF_RELEASE_LOCK_HELD=1 "$RELEASE/host/cyf-api-kit" validate-lock-contract >/dev/null
    expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE=1 CYF_RELEASE_LOCK_HELD=1 "$RELEASE/host/cyf-api-kit" validate-lock-contract >/dev/null
    expect_fail env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$CANONICAL_LOCK_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 "$RELEASE/host/cyf-api-kit" validate-lock-contract >/dev/null
  )
  [[ ! -e "$HOSTILE_PYTHON_MARKER" ]] || fail "canonical lock validation imported ambient Python code"
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
  /usr/bin/python3 -I -B - "$RELEASE/host/cyf-api-kit" <<'PY'
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
record_status() { /usr/bin/python3 -I -B -c 'import json,sys;print(json.load(open(sys.argv[1]))["status"])' "$1"; }
assert_fixture_running() { [[ -f "$TEST_ROOT/control/running" ]] || fail "$1 left fixture runtime stopped"; }
assert_no_lifecycle_calls() { [[ ! -s "$TEST_ROOT/control/lifecycle.log" ]] || fail "$1 unexpectedly called canonical lifecycle"; }

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
  assert_fixture_running "successful deploy"
  deploy_record="$(latest_record 'api-deploy-*.json')"
  [[ "$(/usr/bin/python3 -I -B -c 'import json,sys;print(json.load(open(sys.argv[1]))["status"])' "$deploy_record")" == COMMITTED ]] || fail "deploy commit state"
  run_release "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$old_sha" ]] || fail "rollback old artifact"
  assert_fixture_running "successful rollback"

  for fault_variable in CYF_RELEASE_FAULT_RECORD_STATE CYF_RELEASE_FAULT_RECORD_STATE_AFTER_REPLACE; do
    reset_fixture; prior="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"
    if [[ "$fault_variable" == CYF_RELEASE_FAULT_RECORD_STATE ]]; then window=before-replace; else window=after-replace; fi
    expect_fail run_release_fault "$fault_variable" STOP_ATTEMPTED "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
    boundary_record="$(latest_record 'api-deploy-*.json')"
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$prior" ]] || fail "deploy STOP_ATTEMPTED $window fault changed selected artifact"
    [[ "$(record_status "$boundary_record")" == ABORTED_BEFORE_STOP && "$(stat -Lc %a "$boundary_record")" == 444 ]] \
      || fail "deploy STOP_ATTEMPTED $window fault lacks immutable terminal receipt"
    assert_no_lifecycle_calls "deploy STOP_ATTEMPTED $window fault"
    assert_fixture_running "deploy STOP_ATTEMPTED $window fault"
  done

  reset_fixture; run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; deploy_record="$(latest_record 'api-deploy-*.json')"; : > "$TEST_ROOT/control/fail-next-start"
  expect_fail run_release "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "failed rollback did not restore rescue candidate"
  assert_fixture_running "rollback start-fault recovery"

  reset_fixture; run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; deploy_record="$(latest_record 'api-deploy-*.json')"
  expect_fail env CYF_RELEASE_FAULT_REPLACE_MATCH=.cyf-api-rollback CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "rollback rename fault lost rescue candidate"
  assert_fixture_running "rollback replace-fault recovery"

  for fault_variable in CYF_RELEASE_FAULT_RECORD_STATE CYF_RELEASE_FAULT_RECORD_STATE_AFTER_REPLACE; do
    reset_fixture; run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
    deploy_record="$(latest_record 'api-deploy-*.json')"; : > "$TEST_ROOT/control/lifecycle.log"
    if [[ "$fault_variable" == CYF_RELEASE_FAULT_RECORD_STATE ]]; then window=before-replace; else window=after-replace; fi
    expect_fail run_release_fault "$fault_variable" STOP_ATTEMPTED "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
    boundary_record="$(latest_record 'api-rollback-*.json')"
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "rollback STOP_ATTEMPTED $window fault changed selected artifact"
    [[ "$(record_status "$boundary_record")" == ABORTED_BEFORE_STOP && "$(stat -Lc %a "$boundary_record")" == 444 ]] \
      || fail "rollback STOP_ATTEMPTED $window fault lacks immutable terminal receipt"
    assert_no_lifecycle_calls "rollback STOP_ATTEMPTED $window fault"
    assert_fixture_running "rollback STOP_ATTEMPTED $window fault"
  done

  reset_fixture; prior="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; : > "$TEST_ROOT/control/fail-stop"
  expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$prior" ]] || fail "stop fault changed artifact"
  [[ "$(record_status "$(latest_record 'api-deploy-*.json')")" == FAILED_MANUAL_RECOVERY_REQUIRED ]] || fail "unrecovered stop fault claimed health"
  assert_fixture_running "deploy stop-fault state"

  reset_fixture; prior="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; : > "$TEST_ROOT/control/partial-stop-next"
  expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$prior" ]] || fail "partial stop did not restore prior artifact"
  partial_record="$(latest_record 'api-deploy-*.json')"
  [[ "$(record_status "$partial_record")" == ROLLED_BACK_HEALTHY ]] || fail "partial stop recovery lacks truthful terminal receipt"
  [[ "$(rg -c '^lifecycle-held:stop$' "$TEST_ROOT/control/lifecycle.log")" == 2 \
      && "$(rg -c '^lifecycle-held:start$' "$TEST_ROOT/control/lifecycle.log")" == 1 ]] \
    || fail "partial stop recovery did not canonical stop/restore/start"
  assert_fixture_running "deploy partial-stop recovery"

  reset_fixture; prior="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; : > "$TEST_ROOT/control/fail-next-start"
  expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$prior" ]] || fail "start fault did not restore"
  assert_fixture_running "deploy start-fault recovery"

  reset_fixture; prior="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"
  expect_fail env CYF_RELEASE_FAULT_REPLACE_MATCH=.cyf-api-stage CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$prior" ]] || fail "rename fault changed artifact"
  assert_fixture_running "deploy replace-fault recovery"

  for terminal_state in STARTED_HEALTHY COMMITTED; do
    reset_fixture
    expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE "$terminal_state" "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "terminal receipt fault rolled back healthy candidate"
    [[ "$(record_status "$(latest_record 'api-deploy-*.json')")" == FAILED_MANUAL_RECOVERY_REQUIRED ]] || fail "terminal receipt fault has stale state"
    assert_fixture_running "deploy $terminal_state pre-replace receipt fault"
  done
  reset_fixture
  expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE_AFTER_REPLACE STARTED_HEALTHY "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "post-replace healthy receipt fault rolled back selected candidate"
  [[ "$(record_status "$(latest_record 'api-deploy-*.json')")" == FAILED_MANUAL_RECOVERY_REQUIRED ]] || fail "post-replace healthy receipt fault has stale state"
  assert_fixture_running "deploy STARTED_HEALTHY post-replace receipt fault"

  reset_fixture
  expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE_AFTER_REPLACE COMMITTED "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "post-replace commit receipt fault rolled back selected candidate"
  [[ "$(record_status "$(latest_record 'api-deploy-*.json')")" == COMMITTED ]] || fail "post-replace commit receipt fault obscured durable commit"
  assert_fixture_running "deploy COMMITTED post-replace receipt fault"

  for finalize_fault in before-chmod file-fsync dir-fsync; do
    reset_fixture
    expect_fail run_release_fault CYF_RELEASE_FAULT_FINALIZE "$finalize_fault" "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "finalize fault rolled back committed candidate"
    [[ "$(record_status "$(latest_record 'api-deploy-*.json')")" == COMMITTED ]] || fail "finalize fault left stale committed selection"
    assert_fixture_running "deploy $finalize_fault finalize fault"
  done

  reset_fixture; run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; deploy_record="$(latest_record 'api-deploy-*.json')"
  : > "$TEST_ROOT/control/lifecycle.log"; : > "$TEST_ROOT/control/partial-stop-next"
  expect_fail run_release "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$SHA" ]] || fail "rollback partial stop did not retain rescue candidate"
  [[ "$(record_status "$(latest_record 'api-rollback-*.json')")" == ROLLED_BACK_HEALTHY ]] || fail "rollback partial stop lacks truthful recovery receipt"
  [[ "$(rg -c '^lifecycle-held:stop$' "$TEST_ROOT/control/lifecycle.log")" == 2 \
      && "$(rg -c '^lifecycle-held:start$' "$TEST_ROOT/control/lifecycle.log")" == 1 ]] \
    || fail "rollback partial stop recovery did not canonical stop/restore/start"
  assert_fixture_running "rollback partial-stop recovery"

  for terminal_state in STARTED_HEALTHY COMMITTED; do
    reset_fixture; final_old_sha="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; deploy_record="$(latest_record 'api-deploy-*.json')"
    expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE "$terminal_state" "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$final_old_sha" ]] || fail "rollback terminal receipt fault restored stale rescue candidate"
    [[ "$(record_status "$(latest_record 'api-rollback-*.json')")" == FAILED_MANUAL_RECOVERY_REQUIRED ]] || fail "rollback terminal receipt fault has stale state"
    assert_fixture_running "rollback $terminal_state pre-replace receipt fault"
  done

  for terminal_state in STARTED_HEALTHY COMMITTED; do
    reset_fixture; final_old_sha="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; deploy_record="$(latest_record 'api-deploy-*.json')"
    expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE_AFTER_REPLACE "$terminal_state" "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$final_old_sha" ]] || fail "rollback post-replace receipt fault restored stale rescue candidate"
    if [[ "$terminal_state" == STARTED_HEALTHY ]]; then expected_status=FAILED_MANUAL_RECOVERY_REQUIRED; else expected_status=COMMITTED; fi
    [[ "$(record_status "$(latest_record 'api-rollback-*.json')")" == "$expected_status" ]] || fail "rollback post-replace receipt fault obscured selected state"
    assert_fixture_running "rollback $terminal_state post-replace receipt fault"
  done

  for finalize_fault in before-chmod file-fsync dir-fsync; do
    reset_fixture; final_old_sha="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; deploy_record="$(latest_record 'api-deploy-*.json')"
    expect_fail run_release_fault CYF_RELEASE_FAULT_FINALIZE "$finalize_fault" "$RELEASE/rollback-api.sh" --input "$INPUT" --execute "$deploy_record" >/dev/null
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$final_old_sha" ]] || fail "rollback finalize fault restored stale rescue candidate"
    [[ "$(record_status "$(latest_record 'api-rollback-*.json')")" == COMMITTED ]] || fail "rollback finalize fault obscured committed selection"
    assert_fixture_running "rollback $finalize_fault finalize fault"
  done

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
  cache="$(/usr/bin/python3 -I -B -c 'import base64;print(base64.b64encode(b"C"*32).decode())')"
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
[[ "${1:-}" == -q ]] || exit 59
shift
[[ "${1:-}" == --noproxy && "${2:-}" == '*' ]] || exit 60
shift 2
for name in CURL_CA_BUNDLE SSL_CERT_FILE SSL_CERT_DIR http_proxy https_proxy ftp_proxy all_proxy no_proxy HTTP_PROXY HTTPS_PROXY FTP_PROXY ALL_PROXY NO_PROXY; do
  [[ -z "${!name+x}" ]] || exit 58
done
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
  request_id="$(/usr/bin/python3 -I -B - "${data#@}" "$root/control/stt-request-id" <<'PY'
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

start_owned_loopback_server() {
  local name="$1" mode="$2" requests="$3" control="$4"
  /usr/bin/python3 -I -B - "$mode" "$requests" "$control/$name.port" "$control/trap-hit" <<'PY' &
from http.server import BaseHTTPRequestHandler, HTTPServer
import os, sys, time

mode, maximum, port_path, trap_path = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.server.served += 1
        if mode == 'target' and self.path == '/health':
            body = b'{"status":"UP"}\n'
            self.send_response(200)
        else:
            fd = os.open(trap_path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
            with os.fdopen(fd, 'ab') as stream:
                stream.write((self.path + '\n').encode('ascii', 'backslashreplace'))
            body = b'trap\n'
            self.send_response(502)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, format, *args):
        pass

server = HTTPServer(('127.0.0.1', 0), Handler)
server.served = 0
fd = os.open(port_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
with os.fdopen(fd, 'w', encoding='ascii') as stream:
    stream.write(str(server.server_port) + '\n')
    stream.flush()
    os.fsync(stream.fileno())
deadline = time.monotonic() + 5
while server.served < maximum and time.monotonic() < deadline:
    server.timeout = max(0.05, deadline - time.monotonic())
    server.handle_request()
server.server_close()
PY
  printf -v "${name}_pid" '%s' "$!"
  OWNED_LOOPBACK_PIDS+=("$!")
  local attempt
  for attempt in $(seq 1 200); do
    [[ -s "$control/$name.port" ]] && return 0
    sleep 0.01
  done
  fail "owned loopback $name server did not publish a port"
}

test_real_curl_contract() {
  local control="$TMP/real-curl"
  mkdir -m 0700 -- "$control"
  start_owned_loopback_server target target 3 "$control"
  start_owned_loopback_server trap trap 1 "$control"
  local target_port trap_port target_pid_value trap_pid_value
  target_port="$(cat "$control/target.port")"; trap_port="$(cat "$control/trap.port")"
  target_pid_value="$target_pid"; trap_pid_value="$trap_pid"
  cat > "$control/.curlrc" <<EOF
url = "http://127.0.0.1:$trap_port/trap"
proxy = "http://127.0.0.1:$trap_port"
EOF
  chmod 0600 "$control/.curlrc"
  (
    cd -- "$control"
    export HOME="$control" CURL_HOME="$control" XDG_CONFIG_HOME="$control"
    proxy_url="http://127.0.0.1:$trap_port"
    export http_proxy="$proxy_url" HTTP_PROXY="$proxy_url"
    export https_proxy="$proxy_url" HTTPS_PROXY="$proxy_url"
    export all_proxy="$proxy_url" ALL_PROXY="$proxy_url" no_proxy='' NO_PROXY=''
    export CURL_CA_BUNDLE="$control/untrusted-ca.pem"
    export SSL_CERT_FILE="$control/untrusted-cert.pem" SSL_CERT_DIR="$control/untrusted-certs"
    source "$RELEASE/common.sh"
    source "$RELEASE/lib/api-host-transaction.sh"
    wait_for_health "http://127.0.0.1:$target_port/health" '"status":"UP"' 2 \
      || fail "common wait_for_health missed owned loopback target"
    host_loopback_curl /usr/bin/curl --proto '=http' --silent --show-error --max-time 5 \
      "http://127.0.0.1:$target_port/health" > "$control/helper.body"
    env CYF_RELEASE_OFFLINE_TEST=YES CYF_API_KIT_VALIDATION_ROOT="$control" \
      CYF_API_KIT_VALIDATION_URL="http://127.0.0.1:$target_port/health" \
      "$RELEASE/host/cyf-api-kit" validate-curl-contract > "$control/canonical.out"
  )
  wait "$target_pid_value"
  wait "$trap_pid_value"
  OWNED_LOOPBACK_PIDS=()
  grep -qx '{"status":"UP"}' "$control/helper.body" || fail "shared real curl missed owned loopback target"
  rg -q '^CURL_CONTRACT=PASS$' "$control/canonical.out" || fail "canonical real curl contract failed"
  [[ ! -e "$control/trap-hit" ]] || fail "curl config/proxy remapped an owned loopback request"
}

assert_nginx_contract() {
  /usr/bin/python3 -I -B - "$RELEASE/nginx/juyiting-voice-http.conf" \
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
  env CYF_RELEASE_FAKE_CURL="$TMP/fake-curl" CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" \
    CURL_CA_BUNDLE="$TMP/untrusted-ca.pem" SSL_CERT_FILE="$TMP/untrusted-cert.pem" SSL_CERT_DIR="$TMP/untrusted-certs" \
    http_proxy=http://127.0.0.1:9 https_proxy=http://127.0.0.1:9 all_proxy=http://127.0.0.1:9 no_proxy='' \
    HTTP_PROXY=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 ALL_PROXY=http://127.0.0.1:9 NO_PROXY='' \
    "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
  [[ -f "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env" ]] || fail "activation config missing"
  assert_fixture_running "successful activation"

  for fault_variable in CYF_RELEASE_FAULT_RECORD_STATE CYF_RELEASE_FAULT_RECORD_STATE_AFTER_REPLACE; do
    reset_fixture; printf 'prior-config\n' > "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"; chmod 0600 "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"
    prior_config_sha="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')"; make_valid_config
    if [[ "$fault_variable" == CYF_RELEASE_FAULT_RECORD_STATE ]]; then window=before-replace; else window=after-replace; fi
    expect_fail run_release_fault "$fault_variable" STOP_ATTEMPTED "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
    boundary_record="$(latest_record 'voice-activation-*.json')"
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')" == "$prior_config_sha" ]] || fail "activation STOP_ATTEMPTED $window fault changed selected config"
    [[ "$(record_status "$boundary_record")" == ABORTED_BEFORE_STOP && "$(stat -Lc %a "$boundary_record")" == 444 ]] \
      || fail "activation STOP_ATTEMPTED $window fault lacks immutable terminal receipt"
    assert_no_lifecycle_calls "activation STOP_ATTEMPTED $window fault"
    assert_fixture_running "activation STOP_ATTEMPTED $window fault"
  done

  reset_fixture; printf 'prior-config\n' > "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"; chmod 0600 "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"
  prior_config_sha="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')"; make_valid_config
  : > "$TEST_ROOT/control/partial-stop-next"
  expect_fail run_release "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')" == "$prior_config_sha" ]] || fail "activation partial stop did not restore prior config"
  [[ "$(record_status "$(latest_record 'voice-activation-*.json')")" == ROLLED_BACK_HEALTHY ]] || fail "activation partial stop lacks truthful recovery receipt"
  [[ "$(rg -c '^lifecycle-held:stop$' "$TEST_ROOT/control/lifecycle.log")" == 2 \
      && "$(rg -c '^lifecycle-held:start$' "$TEST_ROOT/control/lifecycle.log")" == 1 ]] \
    || fail "activation partial stop recovery did not canonical stop/restore/start"
  assert_fixture_running "activation partial-stop recovery"

  for terminal_state in STARTED_HEALTHY COMMITTED; do
    reset_fixture; make_valid_config; make_fake_curl
    config_sha="$(sha256sum "$TMP/voice.env"|awk '{print $1}')"
    export CYF_RELEASE_FAKE_CURL="$TMP/fake-curl"
    expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE "$terminal_state" "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
    unset CYF_RELEASE_FAKE_CURL
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')" == "$config_sha" ]] || fail "activation terminal receipt fault rolled back healthy config"
    [[ "$(record_status "$(latest_record 'voice-activation-*.json')")" == FAILED_MANUAL_RECOVERY_REQUIRED ]] || fail "activation terminal receipt fault has stale state"
    assert_fixture_running "activation $terminal_state pre-replace receipt fault"
  done

  for terminal_state in STARTED_HEALTHY COMMITTED; do
    reset_fixture; make_valid_config; make_fake_curl
    config_sha="$(sha256sum "$TMP/voice.env"|awk '{print $1}')"
    export CYF_RELEASE_FAKE_CURL="$TMP/fake-curl"
    expect_fail run_release_fault CYF_RELEASE_FAULT_RECORD_STATE_AFTER_REPLACE "$terminal_state" "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
    unset CYF_RELEASE_FAKE_CURL
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')" == "$config_sha" ]] || fail "activation post-replace receipt fault rolled back healthy config"
    if [[ "$terminal_state" == STARTED_HEALTHY ]]; then expected_status=FAILED_MANUAL_RECOVERY_REQUIRED; else expected_status=COMMITTED; fi
    [[ "$(record_status "$(latest_record 'voice-activation-*.json')")" == "$expected_status" ]] || fail "activation post-replace receipt fault obscured selected state"
    assert_fixture_running "activation $terminal_state post-replace receipt fault"
  done

  for finalize_fault in before-chmod file-fsync dir-fsync; do
    reset_fixture; make_valid_config; make_fake_curl
    config_sha="$(sha256sum "$TMP/voice.env"|awk '{print $1}')"
    export CYF_RELEASE_FAKE_CURL="$TMP/fake-curl"
    expect_fail run_release_fault CYF_RELEASE_FAULT_FINALIZE "$finalize_fault" "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
    unset CYF_RELEASE_FAKE_CURL
    [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')" == "$config_sha" ]] || fail "activation finalize fault rolled back committed config"
    [[ "$(record_status "$(latest_record 'voice-activation-*.json')")" == COMMITTED ]] || fail "activation finalize fault obscured committed selection"
    assert_fixture_running "activation $finalize_fault finalize fault"
  done

  reset_fixture; printf 'prior-config\n' > "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"; chmod 0600 "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"; prior_config_sha="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')"; : > "$TEST_ROOT/control/fail-smoke"
  expect_fail env CYF_RELEASE_FAKE_CURL="$TMP/fake-curl" CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')" == "$prior_config_sha" ]] || fail "activation fault did not restore prior config"
  assert_fixture_running "activation smoke-fault recovery"

  test_real_curl_contract
  assert_nginx_contract
  rg -q 'ops/orchestration/cyf_orchestrator.py' "$RELEASE/build-api.sh" || fail "orchestrator delegation"
  ! rg -n '(^|[^A-Z_])OPENAI_API_KEY' "$RELEASE/activate-api-voice.sh" "$RELEASE/host/cyf-api-kit" || fail "custom OPENAI_API_KEY"

  make_fake_lifecycle
  installed_sha="$(sha256sum "$TEST_ROOT/usr/local/sbin/cyf-api-kit"|awk '{print $1}')"; candidate_sha="$(sha256sum "$RELEASE/host/cyf-api-kit"|awk '{print $1}')"
  /usr/bin/python3 -I -B - "$INPUT" "$installed_sha" "$candidate_sha" <<'PY'
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
