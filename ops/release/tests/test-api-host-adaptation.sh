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
#!/usr/bin/env bash
set -Eeuo pipefail
root="${CYF_RELEASE_TEST_ROOT:?}"
lock="$root/tmp/cyf-release-api.lock"; lifecycle_lock="$root/tmp/cyf-api-lifecycle.lock"
[[ "${CYF_RELEASE_LOCK_INHERITED_FD:-}" == 8 && "${CYF_RELEASE_LOCK_HELD:-}" == 1 ]] || exit 31
[[ -e /proc/$$/fd/8 ]] || exit 32
[[ "$(stat -Lc '%d:%i' /proc/$$/fd/8)" == "$(stat -Lc '%d:%i' "$lock")" ]] || exit 33
[[ "$(stat -Lc '%d:%i' /proc/$$/fd/8)" == "${CYF_RELEASE_LOCK_DEVICE:-}:${CYF_RELEASE_LOCK_INODE:-}" ]] || exit 34
python3 -B - "$lock" <<'PY' || exit 35
import os,sys
st=os.stat(sys.argv[1]); fd=os.fstat(8)
if (st.st_dev,st.st_ino)!=(fd.st_dev,fd.st_ino): raise SystemExit(1)
expected=(os.major(fd.st_dev),os.minor(fd.st_dev),fd.st_ino); found=False
for line in open('/proc/self/fdinfo/8',encoding='ascii'):
    fields=line.split()
    if len(fields)>=9 and fields[0]=='lock:' and fields[2:5]==['FLOCK','ADVISORY','WRITE']:
        try: a,b,c=fields[6].split(':'); actual=(int(a,16),int(b,16),int(c))
        except ValueError: continue
        if actual==expected: found=True; break
raise SystemExit(0 if found else 1)
PY
printf 'release-held:%s\n' "$1" >> "$root/control/lifecycle.log"
exec 9<>"$lifecycle_lock"; flock -n 9 || exit 36
printf 'lifecycle-held:%s\n' "$1" >> "$root/control/lifecycle.log"
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
  pass build-contract
}

test_locks() {
  reset_fixture
  (
    source "$RELEASE/common.sh"; source "$RELEASE/lib/api-host-transaction.sh"
    CYF_RELEASE_OFFLINE_TEST=YES; CYF_RELEASE_TEST_ROOT="$TEST_ROOT"; export CYF_RELEASE_OFFLINE_TEST CYF_RELEASE_TEST_ROOT
    host_load_input "$INPUT"; host_acquire_release_lock; host_call_lifecycle status
  )
  mapfile -t order < "$TEST_ROOT/control/lifecycle.log"
  [[ "${order[0]}" == release-held:status && "${order[1]}" == lifecycle-held:status ]] || fail "lock order"
  (
    exec 8<>"$TEST_ROOT/tmp/cyf-release-api.lock"; flock -n 8
    d="$(stat -Lc %d /proc/$$/fd/8)"; i="$(stat -Lc %i /proc/$$/fd/8)"
    expect_fail env CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=7 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE="$i" CYF_RELEASE_LOCK_HELD=1 "$TEST_ROOT/usr/local/sbin/cyf-api-kit" status >/dev/null
    expect_fail env CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE=1 CYF_RELEASE_LOCK_HELD=1 "$TEST_ROOT/usr/local/sbin/cyf-api-kit" status >/dev/null
    expect_fail env CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 "$TEST_ROOT/usr/local/sbin/cyf-api-kit" status >/dev/null
  )
  (exec 8<>"$TEST_ROOT/tmp/cyf-release-api.lock"; d="$(stat -Lc %d /proc/$$/fd/8)"; i="$(stat -Lc %i /proc/$$/fd/8)"; expect_fail env CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE="$i" CYF_RELEASE_LOCK_HELD=1 "$TEST_ROOT/usr/local/sbin/cyf-api-kit" status >/dev/null)
  (
    exec 7<>"$TEST_ROOT/tmp/cyf-release-api.lock"; flock -n 7
    exec 8<>"$TEST_ROOT/tmp/cyf-release-api.lock"
    d="$(stat -Lc %d /proc/$$/fd/8)"; i="$(stat -Lc %i /proc/$$/fd/8)"
    expect_fail env CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE="$i" CYF_RELEASE_LOCK_HELD=1 "$TEST_ROOT/usr/local/sbin/cyf-api-kit" status >/dev/null
  )
  (
    exec 8<>"$TEST_ROOT/tmp/cyf-release-api.lock"; flock -n 8; d="$(stat -Lc %d /proc/$$/fd/8)"; i="$(stat -Lc %i /proc/$$/fd/8)"
    mv "$TEST_ROOT/tmp/cyf-release-api.lock" "$TEST_ROOT/tmp/replaced.lock"; : > "$TEST_ROOT/tmp/cyf-release-api.lock"; chmod 0660 "$TEST_ROOT/tmp/cyf-release-api.lock"
    expect_fail env CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE="$d" CYF_RELEASE_LOCK_INODE="$i" CYF_RELEASE_LOCK_HELD=1 "$TEST_ROOT/usr/local/sbin/cyf-api-kit" status >/dev/null
  )
  reset_fixture
  (exec 7<>"$TEST_ROOT/tmp/cyf-release-api.lock"; flock 7; : > "$TEST_ROOT/control/holder-ready"; sleep 1) & holder=$!
  while [[ ! -e "$TEST_ROOT/control/holder-ready" ]]; do sleep 0.01; done
  expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  wait "$holder"
  rg -q 'CYF_RELEASE_LOCK_INHERITED_FD=8' "$RELEASE/host/cyf-api-kit" || fail "canonical inherited FD contract missing"
  pass locks
}

latest_record() { find "$TEST_ROOT/opt/cyf/service/api/release-records" -type f -name "$1" -print | sort | tail -1; }

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

  reset_fixture; prior="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"; : > "$TEST_ROOT/control/fail-next-start"
  expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$prior" ]] || fail "start fault did not restore"

  reset_fixture; prior="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')"
  expect_fail env CYF_RELEASE_FAULT_REPLACE_MATCH=.cyf-api-stage CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar"|awk '{print $1}')" == "$prior" ]] || fail "rename fault changed artifact"

  reset_fixture; ln "$ARTIFACT" "$TMP/artifact-hardlink"; expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; rm "$TMP/artifact-hardlink"
  chmod 0644 "$ARTIFACT"; expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null; chmod 0444 "$ARTIFACT"
  mv "$ARTIFACT" "$ARTIFACT.real"; ln -s "$ARTIFACT.real" "$ARTIFACT"; expect_fail run_release "$RELEASE/deploy-api.sh" --input "$INPUT" --execute >/dev/null
  if [[ -d /dev/shm && "$(stat -Lc %d /dev/shm)" != "$(stat -Lc %d "$(dirname "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar")")" ]]; then
    printf stage > /dev/shm/cyf-host-cross-device-stage.$$
    expect_fail bash -c 'source "$1/common.sh"; source "$1/lib/api-host-transaction.sh"; CYF_RELEASE_OFFLINE_TEST=YES; CYF_RELEASE_TEST_ROOT="$2"; host_replace_durable "$3" "$4"' _ "$RELEASE" "$TEST_ROOT" "/dev/shm/cyf-host-cross-device-stage.$$" "$TEST_ROOT/opt/cyf/service/api/cyf-api-kit.jar" >/dev/null
    rm -f -- "/dev/shm/cyf-host-cross-device-stage.$$"
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
#!/usr/bin/env bash
set -eu
body=''; headers=''; url=''
while (($#)); do
 case "$1" in --output) body="$2"; shift 2;; --dump-header) headers="$2"; shift 2;; --write-out|--request|--header|--data|--form) shift 2;; --silent|--show-error) shift;; http://*) url="$1"; shift;; *) shift;; esac
done
if [[ -e "${CYF_RELEASE_TEST_ROOT:-}/control/fail-smoke" ]]; then printf 500; exit 0; fi
if [[ "$url" == */transcriptions ]]; then printf '{"data":{"transcript":"ok"}}\n' > "$body"; else printf 'ID3fake' > "$body"; printf 'HTTP/1.1 200 OK\r\nContent-Type: audio/mpeg\r\n\r\n' > "$headers"; fi
printf 200
SH
  chmod 0755 "$TMP/fake-curl"
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

  reset_fixture; printf 'prior-config\n' > "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"; chmod 0600 "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"; prior_config_sha="$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')"; : > "$TEST_ROOT/control/fail-smoke"
  expect_fail env CYF_RELEASE_FAKE_CURL="$TMP/fake-curl" CYF_RELEASE_OFFLINE_TEST=YES CYF_RELEASE_TEST_ROOT="$TEST_ROOT" CYF_RELEASE_ALLOW_OFFLINE_EXECUTE=YES CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=test-r1 CYF_RELEASE_APPROVED_API_HEAD="$HEAD" CYF_RELEASE_APPROVED_API_TREE="$TREE" "$RELEASE/activate-api-voice.sh" --input "$INPUT" --config "$TMP/voice.env" --audio-fixture "$TMP/audio.webm" --expected-transcript-sha256 "$ok_sha" --execute >/dev/null
  [[ "$(sha256sum "$TEST_ROOT/opt/cyf/service/api/.voice-runtime.env"|awk '{print $1}')" == "$prior_config_sha" ]] || fail "activation fault did not restore prior config"

  [[ "$(rg -c '^location = /api/chat/speech/transcriptions \{' "$RELEASE/nginx/juyiting-voice-server.conf")" == 1 ]] || fail "STT route"
  [[ "$(rg -c '^location = /api/chat/speech/synthesis \{' "$RELEASE/nginx/juyiting-voice-server.conf")" == 1 ]] || fail "TTS route"
  rg -q '^location \^~ /api/chat/speech/' "$RELEASE/nginx/juyiting-voice-deny.conf" || fail "deny closure"
  rg -q 'server 127\.0\.0\.1:10018' "$RELEASE/nginx/juyiting-voice-http.conf" || fail "loopback upstream"
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
