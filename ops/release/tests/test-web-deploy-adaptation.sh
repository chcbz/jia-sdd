#!/bin/bash -p
set -Eeuo pipefail
IFS=$'\n\t'
umask 077
export PATH='/usr/sbin:/usr/bin:/sbin:/bin'
export LC_ALL='C'
unset BASH_ENV ENV CDPATH GLOBIGNORE PYTHONPATH PYTHONHOME PYTHONSTARTUP LD_PRELOAD LD_LIBRARY_PATH \
  HTTP_PROXY HTTPS_PROXY ALL_PROXY NO_PROXY http_proxy https_proxy all_proxy no_proxy \
  CURL_CA_BUNDLE REQUESTS_CA_BUNDLE SSL_CERT_FILE SSL_CERT_DIR GIT_SSL_CAINFO GIT_SSL_CAPATH \
  GIT_CONFIG_COUNT GIT_SSL_NO_VERIFY GIT_PROXY_COMMAND OPENSSL_CONF OPENSSL_MODULES \
  AWS_CA_BUNDLE NODE_EXTRA_CA_CERTS

ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../../.." && pwd -P)"
VERIFY="$ROOT/ops/release/verify-web-deploy-adapter.sh"
DEPLOY="$ROOT/ops/release/deploy-web.sh"
ROLLBACK="$ROOT/ops/release/rollback-web.sh"
# shellcheck source=../common.sh
source "$ROOT/ops/release/common.sh"

SELECTOR='all'
if (($#)); then
  [[ "$1" == --selector && $# == 2 ]] || { printf 'Usage: %s [--selector all|proof|archive|guard|deploy|rollback|static]\n' "$0" >&2; exit 2; }
  SELECTOR="$2"
fi
case "$SELECTOR" in all|proof|archive|guard|deploy|rollback|static) ;; *) printf 'unknown selector: %s\n' "$SELECTOR" >&2; exit 2 ;; esac

fail() { printf 'FAIL: %s\n' "$*" >&2; exit 1; }
pass() { printf 'PASS: %s\n' "$*"; }
expect_fail() {
  local label="$1"; shift
  if "$@" >"$CASE/out" 2>"$CASE/err"; then fail "$label unexpectedly succeeded"; fi
  pass "$label fails closed"
}

RUN="$(mktemp -d /tmp/cyf-web-adapter-test.XXXXXX)"
chmod 0700 "$RUN"
trap 'rm -rf --one-file-system -- "$RUN"' EXIT
export HOME="$RUN/home" GIT_CONFIG_NOSYSTEM=1
mkdir -m 0700 "$HOME"
CASE_INDEX=0

write_archive() {
  local archive="$1" variant="${2:-safe}"
  /usr/bin/python3 -I -B - "$archive" "$variant" <<'PY'
import io, os, tarfile, sys
path, variant = sys.argv[1:]
def add_file(bundle, name, content=b'x', kind=None, link=''):
    item=tarfile.TarInfo(name); item.mtime=1; item.mode=0o644
    if kind is not None:
        item.type=kind; item.linkname=link; item.size=0; bundle.addfile(item); return
    item.size=len(content); bundle.addfile(item,io.BytesIO(content))
with tarfile.open(path,'w:gz',format=tarfile.PAX_FORMAT) as bundle:
    if variant != 'missing-index':
        add_file(bundle,'./index.html',b'<script type="module" src="/static/index-fixture.js"></script>')
    add_file(bundle,'./static/index-fixture.js',b'console.log("fixture")')
    if variant == 'traversal': add_file(bundle,'../escape',b'bad')
    elif variant == 'duplicate':
        add_file(bundle,'./dup',b'a'); add_file(bundle,'dup',b'b')
    elif variant == 'symlink': add_file(bundle,'./link',kind=tarfile.SYMTYPE,link='index.html')
    elif variant == 'hardlink': add_file(bundle,'./hard',kind=tarfile.LNKTYPE,link='index.html')
    elif variant == 'device': add_file(bundle,'./device',kind=tarfile.CHRTYPE)
    elif variant == 'fifo': add_file(bundle,'./fifo',kind=tarfile.FIFOTYPE)
os.chmod(path,0o444)
PY
}

write_proof() {
  local status="${1:-ACTIVATED_HEALTHY}" stt="${2:-PASS}" tts="${3:-PASS}"
  local routes="${4:-PASS}" deny="${5:-PASS}" loopback="${6:-127.0.0.1}"
  /usr/bin/python3 -I -B - "$PROOF" "$RELEASE_ID" "$API_HEAD" "$API_TREE" "$JAR_SHA" \
    "$status" "$stt" "$tts" "$routes" "$deny" "$loopback" <<'PY'
import json,os,sys
(path,release_id,api_head,api_tree,jar_sha,status,stt,tts,routes,deny,loopback)=sys.argv[1:]
data={'schema':'cyf-jvc-oai-api-activation-proof-v1','releaseId':release_id,
      'finalAcceptedHostIdentitySha256':'1'*64,'finalAcceptedLifecycleSha256':'2'*64,
      'apiHead':api_head,'apiTree':api_tree,'deployedJarSha256':jar_sha,'status':status,
      'authenticatedStt':stt,'authenticatedTts':tts,'nginxRoutes':routes,
      'nginxDenyClosed':deny,'loopbackBinding':loopback,'activationRecordSha256':'3'*64}
with open(path,'x',encoding='utf-8') as stream: json.dump(data,stream,sort_keys=True,indent=2); stream.write('\n')
os.chmod(path,0o400)
PY
}

write_input() {
  local archive_sha
  archive_sha="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
  /usr/bin/python3 -I -B - "$INPUT" "$RELEASE_ID" "$ARCHIVE" "$archive_sha" "$REPO" "$WEB_REF" \
    "$WEB_HEAD" "$WEB_TREE" "$LIVE" "$BACKUP" "$RECORDS" "$API_HEAD" "$API_TREE" \
    "$JAR_SHA" "$CONTROLLER" <<'PY'
import json,sys
(path,release_id,archive,archive_sha,repo,ref,web_head,web_tree,live,backup,records,
 api_head,api_tree,jar_sha,controller)=sys.argv[1:]
data={'schema':'cyf-jvc-oai-web-deploy-adapter-v1','releaseId':release_id,'compileVoiceEnabled':True,
 'archive':{'path':archive,'sha256':archive_sha},
 'web':{'repo':repo,'ref':ref,'head':web_head,'tree':web_tree,
        'deploy':{'liveDir':live,'backupRoot':backup,'recordRoot':records,
                  'healthUrls':['https://fixture.invalid/','https://fixture.invalid/juyiting'],
                  'healthTimeoutSeconds':1}},
 'api':{'head':api_head,'tree':api_tree,'deployedJarSha256':jar_sha},
 'activationProof':{'schema':'cyf-jvc-oai-api-activation-proof-v1','trustedRoot':controller},
 'webGuardRoot':controller}
with open(path,'x',encoding='utf-8') as stream: json.dump(data,stream,sort_keys=True,indent=2); stream.write('\n')
PY
}

rewrite_json_field() {
  local path="$1" field="$2" value="$3" sidecar="${4:-}"
  /usr/bin/python3 -I -B - "$path" "$field" "$value" "$sidecar" <<'PY'
import hashlib, json, os, sys
path, field, value, sidecar = sys.argv[1:]
os.chmod(path, 0o600)
with open(path, encoding='utf-8') as stream:
    data = json.load(stream)
data[field] = value
with open(path, 'w', encoding='utf-8') as stream:
    json.dump(data, stream, sort_keys=True, indent=2); stream.write('\n')
    stream.flush(); os.fsync(stream.fileno())
os.chmod(path, 0o400)
if sidecar:
    content = open(path, 'rb').read()
    payload = '{}  {}\n'.format(hashlib.sha256(content).hexdigest(), os.path.basename(path))
    os.chmod(sidecar, 0o600)
    with open(sidecar, 'w', encoding='ascii') as stream:
        stream.write(payload); stream.flush(); os.fsync(stream.fileno())
    os.chmod(sidecar, 0o400)
PY
}

assert_no_success_record() {
  local prefix="$1"
  [[ -z "$(find "$RECORDS" -maxdepth 1 -name "${prefix}-*.json" -print -quit)" ]] \
    || fail "failed operation left a committed $prefix record"
}

assert_manual_recovery_record() {
  local operation="$1" expected_integrity="${2:-}" expected_live="${3:-}"
  local expected_final="${4:-}" expected_sidecar="${5:-}" expected_source="${6:-}"
  local record digest
  record="$(find "$RECORDS" -maxdepth 1 -name "web-recovery-${operation}-*.json" -print -quit)"
  [[ -n "$record" && -f "$record" && -f "${record}.sha256" ]] \
    || fail "missing durable manual recovery record for $operation"
  [[ "$(stat -Lc '%a:%h' "$record")" == '400:1' \
     && "$(stat -Lc '%a:%h' "${record}.sha256")" == '400:1' ]] \
    || fail "manual recovery record is not immutable nlink1 for $operation"
  digest="$(sha256sum "$record" | awk '{print $1}')"
  [[ "$(cat -- "${record}.sha256")" == "$digest  $(basename -- "$record")" ]] \
    || fail "manual recovery record sidecar mismatch for $operation"
  /usr/bin/python3 -I -B - "$record" "$operation" "$expected_integrity" "$expected_live" \
    "$expected_final" "$expected_sidecar" "$expected_source" <<'PY'
import json, sys
with open(sys.argv[1], encoding='utf-8') as stream:
    data = json.load(stream)
if data.get('schema') != 'cyf-web-recovery-record-v1':
    raise SystemExit('wrong recovery record schema')
if data.get('status') != 'FAILED_MANUAL_RECOVERY_REQUIRED':
    raise SystemExit('wrong recovery record status')
if data.get('operation') != sys.argv[2]:
    raise SystemExit('wrong recovery operation')
checks = {
    'publicationIntegrity': sys.argv[3],
    'publicationLiveValidation': sys.argv[4],
    'publicationFinalState': sys.argv[5],
    'publicationSidecarState': sys.argv[6],
    'publicationSourceState': sys.argv[7],
}
for key, expected in checks.items():
    if expected and data.get(key) != expected:
        raise SystemExit('{} mismatch: {} != {}'.format(key, data.get(key), expected))
PY
}

new_case() {
  CASE_INDEX=$((CASE_INDEX+1)); CASE="$RUN/case-$CASE_INDEX"; mkdir -m 0700 "$CASE"
  export CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE"
  unset CYF_WEB_DEPLOY_ADAPTER_FAULT CYF_WEB_DEPLOY_ADAPTER_TEST_COMMON_SH
  CONTROLLER="$CASE/controller"; REPO="$CASE/repo"; LIVE_PARENT="$CASE/host/web"
  LIVE="$LIVE_PARENT/kit"; BACKUP="$LIVE_PARENT/bak"; RECORDS="$BACKUP/release-records"
  ARCHIVE="$CASE/web.tar.gz"; INPUT="$CASE/input.json"
  RELEASE_ID="fixture-$CASE_INDEX"; API_HEAD="$(printf 'a%.0s' {1..40})"; API_TREE="$(printf 'b%.0s' {1..40})"
  JAR_SHA="$(printf 'c%.0s' {1..64})"
  mkdir -m 0700 "$CONTROLLER" "$REPO" "$LIVE_PARENT" "$LIVE" "$BACKUP" "$RECORDS"
  git -C "$REPO" init -q
  git -C "$REPO" config user.name fixture
  git -C "$REPO" config user.email fixture@example.invalid
  mkdir -p "$REPO/static"
  printf '<script type="module" src="/static/index-source.js"></script>\n' > "$REPO/index.html"
  printf 'source\n' > "$REPO/static/index-source.js"
  git -C "$REPO" add .; git -C "$REPO" commit -qm fixture
  WEB_HEAD="$(git -C "$REPO" rev-parse HEAD)"; WEB_TREE="$(git -C "$REPO" rev-parse 'HEAD^{tree}')"
  WEB_REF="$(git -C "$REPO" symbolic-ref --short HEAD)"
  mkdir -p "$LIVE/static"
  printf '<script type="module" src="/static/index-old.js"></script>\n' > "$LIVE/index.html"
  printf 'old\n' > "$LIVE/static/index-old.js"
  OLD_TREE="$(hash_tree "$LIVE")"
  write_archive "$ARCHIVE" safe
  PROOF="$CONTROLLER/cyf-jvc-oai-api-activation-proof-v1.json"
  write_proof
  write_input
  GUARD="$CONTROLLER/web-guard-${RELEASE_ID}-${WEB_HEAD}-${WEB_TREE}.json"
}

verify_case() {
  env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT" >"$CASE/verify.out"
  [[ -f "$GUARD" && -f "${GUARD}.sha256" ]] || fail 'verifier did not publish complete guard'
  GUARD_SHA="$(sha256sum "$GUARD" | awk '{print $1}')"
  PROOF_SHA="$(sha256sum "$PROOF" | awk '{print $1}')"
  CANDIDATE_TREE="$(/usr/bin/python3 -I -B - "$GUARD" <<'PY'
import json,sys
with open(sys.argv[1],encoding='utf-8') as stream: print(json.load(stream)['extractedTreeSha256'])
PY
)"
}

approval_env() {
  env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" \
    CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID="$RELEASE_ID" \
    CYF_RELEASE_APPROVED_API_HEAD="$API_HEAD" CYF_RELEASE_APPROVED_API_TREE="$API_TREE" \
    CYF_RELEASE_APPROVED_WEB_HEAD="$WEB_HEAD" CYF_RELEASE_APPROVED_WEB_TREE="$WEB_TREE" \
    CYF_RELEASE_APPROVED_WEB_ARTIFACT_SHA256="$(sha256sum "$ARCHIVE" | awk '{print $1}')" \
    CYF_RELEASE_APPROVED_WEB_GUARD_SHA256="$GUARD_SHA" \
    CYF_RELEASE_APPROVED_API_ACTIVATION_PROOF_SHA256="$PROOF_SHA" "$@"
}

deploy_case() {
  approval_env "$DEPLOY" --input "$INPUT" --execute >"$CASE/deploy.out"
  DEPLOY_RECORD="$(sed -n 's/^DEPLOY_RECORD=//p' "$CASE/deploy.out")"
  [[ -n "$DEPLOY_RECORD" && -f "$DEPLOY_RECORD" ]] || fail 'deploy record missing'
}

assert_live_tree() {
  [[ "$(hash_tree "$LIVE")" == "$1" ]] || fail "unexpected live tree: expected=$1"
}

assert_path_tree() {
  local path="$1" expected="$2" label="$3"
  [[ -d "$path" && ! -L "$path" ]] || fail "$label path is unavailable: $path"
  [[ "$(hash_tree "$path")" == "$expected" ]] || fail "$label tree mismatch: $path"
}

run_static() {
  local script
  for script in "$VERIFY" "$DEPLOY" "$ROLLBACK" "$ROOT/ops/release/lib/web-deploy-adapter.sh" "$0"; do
    head -1 "$script" | grep -Eq '^#!/bin/bash( -p)?$' || fail "non-absolute Bash entrypoint: $script"
  done
  /usr/bin/python3 -I -B - "$ROOT/ops/release/tests/test-web-deploy-adaptation.sh" <<'PY'
import pathlib,sys
text=pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
for token in ('/dev/'+'shm', 'ev'+'al ', 'npm'+' ', 'gra'+'dle', 'system'+'ctl', 'p'+'kill'):
    if token in text: raise SystemExit('forbidden fixture-test token: {}'.format(token))
PY
  for script in "$VERIFY" "$DEPLOY" "$ROLLBACK"; do
    grep -Fq 'HTTP_PROXY HTTPS_PROXY ALL_PROXY NO_PROXY http_proxy https_proxy all_proxy no_proxy' "$script" \
      || fail "proxy environment is not cleared by $script"
    grep -Fq 'CURL_CA_BUNDLE REQUESTS_CA_BUNDLE SSL_CERT_FILE SSL_CERT_DIR GIT_SSL_CAINFO GIT_SSL_CAPATH' "$script" \
      || fail "CA override environment is not cleared by $script"
  done
  grep -Fq "'common.sh'" "$ROOT/ops/release/lib/web-deploy-adapter.sh" \
    || fail 'common.sh is absent from the Web adapter tool digest'
  grep -Fq "MINIMUM_FREE_BYTES=0" "$ROOT/ops/release/lib/web-deploy-adapter.sh" \
    || fail 'cancelled legacy resource threshold was reactivated'
  pass 'static privileged-entrypoint and forbidden-mechanism fences'
}

run_proof() {
  new_case; rm "$PROOF"; expect_fail 'compiler flag without external proof' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
  local field value hostile marker
  for field in schema releaseId apiHead apiTree deployedJarSha256 status authenticatedStt \
    authenticatedTts nginxRoutes nginxDenyClosed loopbackBinding; do
    new_case
    case "$field" in
      schema) value=wrong-schema;; releaseId) value=wrong-release;;
      apiHead|apiTree) value="$(printf 'd%.0s' {1..40})";;
      deployedJarSha256) value="$(printf 'e%.0s' {1..64})";;
      status) value=UNHEALTHY;; loopbackBinding) value=0.0.0.0;;
      *) value=FAIL;;
    esac
    rewrite_json_field "$PROOF" "$field" "$value"
    expect_fail "wrong activation proof $field" env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" \
      "$VERIFY" --input "$INPUT"
  done
  for field in finalAcceptedHostIdentitySha256 finalAcceptedLifecycleSha256 activationRecordSha256; do
    new_case; rewrite_json_field "$PROOF" "$field" invalid
    expect_fail "invalid activation proof digest $field" env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" \
      "$VERIFY" --input "$INPUT"
  done
  new_case; chmod 0600 "$PROOF"; expect_fail 'mutable proof mode' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
  new_case; ln "$PROOF" "$CASE/proof-hardlink"; expect_fail 'hardlinked proof' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
  new_case; mv "$PROOF" "$CASE/proof-real"; ln -s ../proof-real "$PROOF"; expect_fail 'symlinked proof' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"

  new_case
  hostile="$CASE/hostile"; marker="$CASE/injected"; mkdir -m 0700 "$hostile"
  printf 'import os\nopen(os.environ["INJECT_MARKER"], "w").write("python")\n' > "$hostile/json.py"
  cp -- "$hostile/json.py" "$hostile/tarfile.py"
  printf 'printf shell > "$INJECT_MARKER"\n' > "$hostile/bash-env"
  (cd -- "$hostile" && env INJECT_MARKER="$marker" PYTHONPATH="$hostile" PYTHONHOME="$hostile" \
    HOME="$hostile" BASH_ENV="$hostile/bash-env" ENV="$hostile/bash-env" \
    HTTP_PROXY=http://127.0.0.1:9 HTTPS_PROXY=http://127.0.0.1:9 ALL_PROXY=http://127.0.0.1:9 \
    NO_PROXY='*' http_proxy=http://127.0.0.1:9 https_proxy=http://127.0.0.1:9 \
    all_proxy=http://127.0.0.1:9 no_proxy='*' CURL_CA_BUNDLE="$hostile/ca.pem" \
    REQUESTS_CA_BUNDLE="$hostile/ca.pem" SSL_CERT_FILE="$hostile/ca.pem" \
    SSL_CERT_DIR="$hostile" GIT_SSL_CAINFO="$hostile/ca.pem" GIT_SSL_CAPATH="$hostile" \
    GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=http.proxy GIT_CONFIG_VALUE_0=http://127.0.0.1:9 \
    GIT_SSL_NO_VERIFY=true GIT_PROXY_COMMAND="$hostile/proxy" OPENSSL_CONF="$hostile/openssl.cnf" \
    OPENSSL_MODULES="$hostile" \
    "$VERIFY" --input "$INPUT" > "$CASE/hostile.out")
  [[ ! -e "$marker" ]] || fail 'hostile shell/Python startup injection executed'
  [[ -f "$GUARD" ]] || fail 'isolated hostile-environment verification did not publish a guard'
  pass 'entrypoint clears proxy/CA injection and isolates Python imports from HOME/PYTHONPATH/CWD'
}

run_archive() {
  local variant
  for variant in traversal duplicate symlink hardlink device fifo missing-index; do
    new_case; chmod 0600 "$ARCHIVE"; rm "$ARCHIVE"; write_archive "$ARCHIVE" "$variant"; rm "$INPUT"; write_input
    expect_fail "unsafe archive $variant" env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
  done
  new_case; chmod 0600 "$ARCHIVE"; printf mutation >> "$ARCHIVE"; chmod 0444 "$ARCHIVE"
  expect_fail 'archive hash mismatch' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
  new_case; ln "$ARCHIVE" "$CASE/archive-hardlink"
  expect_fail 'hardlinked archive' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
  new_case; mv "$ARCHIVE" "$CASE/archive-real"; ln -s archive-real "$ARCHIVE"
  expect_fail 'symlinked archive' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
  new_case
  env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" CYF_WEB_DEPLOY_ADAPTER_FAULT=archive-mutation-window \
    "$VERIFY" --input "$INPUT" > "$CASE/out" 2> "$CASE/err" & verifier_pid=$!
  deadline=$((SECONDS + 10))
  until [[ -f "$CASE/archive-mutation.ready" ]]; do
    (( SECONDS < deadline )) || { wait "$verifier_pid" || true; fail 'mutation ready handshake timed out'; }
  done
  touch "$ARCHIVE"
  (umask 077; printf 'CONTINUE\n' > "$CASE/archive-mutation.continue")
  if wait "$verifier_pid"; then fail 'archive mutation while held open unexpectedly succeeded'; fi
  pass 'archive mutation while held open fails through deterministic handshake'
}

run_guard() {
  new_case; verify_case
  [[ "$(stat -Lc '%a:%h' "$GUARD")" == '400:1' && "$(stat -Lc '%a:%h' "${GUARD}.sha256")" == '400:1' ]] \
    || fail 'guard publication is not immutable complete nlink1'
  chmod 0600 "$GUARD"
  expect_fail 'mutable guard' approval_env "$DEPLOY" --input "$INPUT" --dry-run
  new_case; verify_case; ln "$GUARD" "$CASE/guard-hardlink"
  expect_fail 'hardlinked guard' approval_env "$DEPLOY" --input "$INPUT" --dry-run
  new_case; verify_case; rewrite_json_field "$GUARD" schema wrong-schema "${GUARD}.sha256"
  expect_fail 'guard semantic mismatch' approval_env "$DEPLOY" --input "$INPUT" --dry-run
  new_case; verify_case; chmod 0600 "${GUARD}.sha256"
  expect_fail 'mutable guard sidecar' approval_env "$DEPLOY" --input "$INPUT" --dry-run
  new_case; verify_case; ln "${GUARD}.sha256" "$CASE/guard-sidecar-hardlink"
  expect_fail 'hardlinked guard sidecar' approval_env "$DEPLOY" --input "$INPUT" --dry-run
  new_case; verify_case; chmod 0600 "${GUARD}.sha256"; printf '0  wrong\n' > "${GUARD}.sha256"; chmod 0400 "${GUARD}.sha256"
  expect_fail 'guard sidecar hash mismatch' approval_env "$DEPLOY" --input "$INPUT" --dry-run
  new_case; verify_case; chmod 0600 "$GUARD"; printf '\n' >> "$GUARD"; chmod 0400 "$GUARD"
  expect_fail 'guard content hash mismatch' approval_env "$DEPLOY" --input "$INPUT" --dry-run
  new_case; verify_case; printf '\n' >> "$INPUT"
  expect_fail 'input changed after guard' approval_env "$DEPLOY" --input "$INPUT" --dry-run
  new_case; verify_case; chmod 0600 "$ARCHIVE"; printf x >> "$ARCHIVE"; chmod 0444 "$ARCHIVE"
  expect_fail 'archive changed after guard' approval_env "$DEPLOY" --input "$INPUT" --dry-run
  for field in finalAcceptedHostIdentitySha256 finalAcceptedLifecycleSha256 activationRecordSha256; do
    new_case; verify_case; rewrite_json_field "$PROOF" "$field" "$(printf '9%.0s' {1..64})"
    expect_fail "activation proof guard mismatch $field" approval_env "$DEPLOY" --input "$INPUT" --dry-run
  done
  new_case
  cp -- "$ROOT/ops/release/common.sh" "$CASE/common.sh"; chmod 0400 "$CASE/common.sh"
  export CYF_WEB_DEPLOY_ADAPTER_TEST_COMMON_SH="$CASE/common.sh"
  verify_case
  chmod 0600 "$CASE/common.sh"; printf '\n# fixture mutation\n' >> "$CASE/common.sh"; chmod 0400 "$CASE/common.sh"
  expect_fail 'common.sh tool digest mutation' approval_env "$DEPLOY" --input "$INPUT" --dry-run
}

run_deploy() {
  new_case; verify_case
  local binding var fault record backup failed
  for binding in approved id api-head api-tree web-head web-tree artifact guard proof; do
    case "$binding" in
      approved) expect_fail 'approval YES binding' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$DEPLOY" --input "$INPUT" --execute;;
      id) expect_fail 'approval ID safety binding' approval_env env CYF_RELEASE_APPROVAL_ID='bad/id' "$DEPLOY" --input "$INPUT" --execute;;
      *)
        # A complete environment is supplied, then exactly one immutable binding is replaced.
        var="CYF_RELEASE_APPROVED_${binding^^}"; var="${var//-/_}"
        case "$binding" in api-head) var=CYF_RELEASE_APPROVED_API_HEAD;; api-tree) var=CYF_RELEASE_APPROVED_API_TREE;;
          web-head) var=CYF_RELEASE_APPROVED_WEB_HEAD;; web-tree) var=CYF_RELEASE_APPROVED_WEB_TREE;;
          artifact) var=CYF_RELEASE_APPROVED_WEB_ARTIFACT_SHA256;; guard) var=CYF_RELEASE_APPROVED_WEB_GUARD_SHA256;;
          proof) var=CYF_RELEASE_APPROVED_API_ACTIVATION_PROOF_SHA256;; esac
        expect_fail "approval $binding binding" approval_env env "$var=wrong" "$DEPLOY" --input "$INPUT" --execute
        ;;
    esac
    assert_live_tree "$OLD_TREE"
  done
  new_case; verify_case; deploy_case; assert_live_tree "$CANDIDATE_TREE"
  pass 'actual deploy entrypoint preserves exact candidate tree and immutable record'

  for fault in extraction staged-tree backup-rename cutover-rename health; do
    new_case; verify_case
    expect_fail "deploy recovery $fault" approval_env env CYF_WEB_DEPLOY_ADAPTER_FAULT="$fault" "$DEPLOY" --input "$INPUT" --execute
    assert_live_tree "$OLD_TREE"
    assert_no_success_record web-deploy
  done

  for fault in record-write record-sidecar record-final-link record-post-link-unlink; do
    new_case; verify_case
    expect_fail "deploy conservative publication boundary $fault" approval_env env \
      CYF_WEB_DEPLOY_ADAPTER_FAULT="$fault" "$DEPLOY" --input "$INPUT" --execute
    assert_live_tree "$CANDIDATE_TREE"
    assert_no_success_record web-deploy
    [[ -z "$(find "$RECORDS" -maxdepth 1 -name 'web-deploy-*.json.sha256' -print -quit)" ]] \
      || fail "failed deploy $fault left a success sidecar"
    backup="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-backup-*' -print -quit)"
    assert_path_tree "$backup" "$OLD_TREE" "publication boundary $fault backup"
    [[ -n "$(find "$RECORDS" -maxdepth 1 -name '.web-deploy-record.*' -print -quit)" ]] \
      || fail "publication boundary $fault did not retain the source record"
    assert_manual_recovery_record deploy ABSENT_UNCONFIRMED MATCHING_HEALTHY ABSENT ABSENT PRESENT
  done

  new_case; verify_case
  expect_fail 'deploy record directory fsync preserves matching live state' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=record-directory-fsync "$DEPLOY" --input "$INPUT" --execute
  assert_live_tree "$CANDIDATE_TREE"
  record="$(find "$RECORDS" -maxdepth 1 -name 'web-deploy-*.json' -print -quit)"
  [[ -n "$record" && -f "$record" && -f "${record}.sha256" ]] \
    || fail 'directory-fsync terminal deploy did not preserve complete matching evidence'
  approval_env "$ROLLBACK" --input "$INPUT" --dry-run "$record" > "$CASE/terminal-deploy-record.out"
  backup="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-backup-*' -print -quit)"
  assert_path_tree "$backup" "$OLD_TREE" 'terminal deploy backup'
  assert_manual_recovery_record deploy COMPLETE_EXPECTED MATCHING_HEALTHY PRESENT PRESENT ABSENT

  new_case; verify_case
  expect_fail 'deploy link success before child feedback' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=record-link-no-feedback "$DEPLOY" --input "$INPUT" --execute
  assert_live_tree "$CANDIDATE_TREE"
  record="$(find "$RECORDS" -maxdepth 1 -name 'web-deploy-*.json' -print -quit)"
  [[ -n "$record" && -f "$record" && ! -e "${record}.sha256" ]] \
    || fail 'link-no-feedback deploy did not retain the expected final-only record state'
  [[ "$(stat -Lc %h "$record")" == 2 ]] || fail 'link-no-feedback deploy final record is not nlink2'
  [[ -n "$(find "$RECORDS" -maxdepth 1 -name '.web-deploy-record.*' -print -quit)" ]] \
    || fail 'link-no-feedback deploy did not retain the linked source record'
  backup="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-backup-*' -print -quit)"
  assert_path_tree "$backup" "$OLD_TREE" 'link-no-feedback deploy backup'
  [[ -z "$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-failed-*' -print -quit)" ]] \
    || fail 'link-no-feedback deploy attempted reverse rollback'
  assert_manual_recovery_record deploy PARTIAL_OR_INVALID MATCHING_HEALTHY PRESENT ABSENT PRESENT

  new_case; verify_case
  expect_fail 'deploy cleanup final unlink failure' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=record-post-link-unlink,record-cleanup-final-unlink \
    "$DEPLOY" --input "$INPUT" --execute
  assert_live_tree "$CANDIDATE_TREE"
  record="$(find "$RECORDS" -maxdepth 1 -name 'web-deploy-*.json' -print -quit)"
  [[ -n "$record" && -f "${record}.sha256" && "$(stat -Lc %h "$record")" == 1 ]] \
    || fail 'cleanup-final-unlink deploy did not preserve complete nlink1 evidence'
  [[ -z "$(find "$RECORDS" -maxdepth 1 -name '.web-deploy-record.*' -print -quit)" ]] \
    || fail 'cleanup-final-unlink deploy unexpectedly retained the source record'
  backup="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-backup-*' -print -quit)"
  assert_path_tree "$backup" "$OLD_TREE" 'cleanup-final-unlink deploy backup'
  [[ -z "$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-failed-*' -print -quit)" ]] \
    || fail 'cleanup-final-unlink deploy attempted reverse rollback'
  assert_manual_recovery_record deploy COMPLETE_EXPECTED MATCHING_HEALTHY PRESENT PRESENT ABSENT

  new_case; verify_case
  expect_fail 'deploy cleanup sidecar unlink failure' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=record-final-link,record-cleanup-sidecar-unlink \
    "$DEPLOY" --input "$INPUT" --execute
  assert_live_tree "$CANDIDATE_TREE"
  [[ -z "$(find "$RECORDS" -maxdepth 1 -name 'web-deploy-*.json' -print -quit)" ]] \
    || fail 'cleanup-sidecar-unlink deploy unexpectedly retained a final record'
  [[ -n "$(find "$RECORDS" -maxdepth 1 -name 'web-deploy-*.json.sha256' -print -quit)" ]] \
    || fail 'cleanup-sidecar-unlink deploy did not retain the sidecar'
  [[ -n "$(find "$RECORDS" -maxdepth 1 -name '.web-deploy-record.*' -print -quit)" ]] \
    || fail 'cleanup-sidecar-unlink deploy did not retain the source record'
  backup="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-backup-*' -print -quit)"
  assert_path_tree "$backup" "$OLD_TREE" 'cleanup-sidecar-unlink deploy backup'
  [[ -z "$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-failed-*' -print -quit)" ]] \
    || fail 'cleanup-sidecar-unlink deploy attempted reverse rollback'
  assert_manual_recovery_record deploy PARTIAL_OR_INVALID MATCHING_HEALTHY ABSENT PRESENT PRESENT

  new_case; verify_case
  expect_fail 'deploy cleanup directory fsync failure' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=record-post-link-unlink,record-cleanup-directory-fsync \
    "$DEPLOY" --input "$INPUT" --execute
  assert_live_tree "$CANDIDATE_TREE"
  assert_no_success_record web-deploy
  [[ -z "$(find "$RECORDS" -maxdepth 1 -name 'web-deploy-*.json.sha256' -print -quit)" ]] \
    || fail 'cleanup-directory-fsync deploy retained a visible sidecar'
  [[ -n "$(find "$RECORDS" -maxdepth 1 -name '.web-deploy-record.*' -print -quit)" ]] \
    || fail 'cleanup-directory-fsync deploy did not retain the source record'
  backup="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-backup-*' -print -quit)"
  assert_path_tree "$backup" "$OLD_TREE" 'cleanup-directory-fsync deploy backup'
  [[ -z "$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-failed-*' -print -quit)" ]] \
    || fail 'cleanup-directory-fsync deploy attempted reverse rollback'
  assert_manual_recovery_record deploy ABSENT_UNCONFIRMED MATCHING_HEALTHY ABSENT ABSENT PRESENT

  new_case; verify_case
  expect_fail 'compound deploy candidate removal failure' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=health,recovery-failed "$DEPLOY" --input "$INPUT" --execute
  assert_live_tree "$CANDIDATE_TREE"
  backup="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-backup-*' -print -quit)"
  assert_path_tree "$backup" "$OLD_TREE" 'compound deploy backup'
  [[ -z "$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-failed-*' -print -quit)" ]] \
    || fail 'candidate-removal failure unexpectedly created a failed-candidate directory'
  assert_no_success_record web-deploy
  assert_manual_recovery_record deploy

  new_case; verify_case
  expect_fail 'compound deploy backup restore failure' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=health,recovery-restore "$DEPLOY" --input "$INPUT" --execute
  [[ ! -e "$LIVE" ]] || fail 'backup-restore failure unexpectedly left a live directory'
  backup="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-backup-*' -print -quit)"
  failed="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-failed-*' -print -quit)"
  assert_path_tree "$backup" "$OLD_TREE" 'compound deploy retained backup'
  assert_path_tree "$failed" "$CANDIDATE_TREE" 'compound deploy failed candidate'
  assert_no_success_record web-deploy
  assert_manual_recovery_record deploy
}

run_rollback() {
  local fault record rescue failed
  new_case; verify_case; deploy_case; assert_live_tree "$CANDIDATE_TREE"
  rm "$PROOF"
  approval_env "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD" >"$CASE/rollback.out"
  assert_live_tree "$OLD_TREE"
  grep -q '^ROLLBACK_WEB=PASS$' "$CASE/rollback.out" || fail 'actual rollback did not pass without external proof file'
  pass 'actual rollback uses recorded proof digest and restores exact old tree'

  new_case; verify_case; deploy_case
  expect_fail 'rollback approval ID binding' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" \
    CYF_RELEASE_APPROVED=YES CYF_RELEASE_APPROVAL_ID=wrong \
    CYF_RELEASE_APPROVED_API_HEAD="$API_HEAD" CYF_RELEASE_APPROVED_API_TREE="$API_TREE" \
    CYF_RELEASE_APPROVED_WEB_HEAD="$WEB_HEAD" CYF_RELEASE_APPROVED_WEB_TREE="$WEB_TREE" \
    CYF_RELEASE_APPROVED_WEB_ARTIFACT_SHA256="$(sha256sum "$ARCHIVE" | awk '{print $1}')" \
    CYF_RELEASE_APPROVED_WEB_GUARD_SHA256="$GUARD_SHA" \
    CYF_RELEASE_APPROVED_API_ACTIVATION_PROOF_SHA256="$PROOF_SHA" \
    "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD"
  assert_live_tree "$CANDIDATE_TREE"

  for fault in rollback-staged-tree rollback-rescue-rename rollback-cutover-rename health; do
    new_case; verify_case; deploy_case
    expect_fail "rollback rescue $fault" approval_env env CYF_WEB_DEPLOY_ADAPTER_FAULT="$fault" \
      "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD"
    assert_live_tree "$CANDIDATE_TREE"
    assert_no_success_record web-rollback
  done

  for fault in record-write record-sidecar record-final-link record-post-link-unlink; do
    new_case; verify_case; deploy_case
    expect_fail "rollback conservative publication boundary $fault" approval_env env \
      CYF_WEB_DEPLOY_ADAPTER_FAULT="$fault" "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD"
    assert_live_tree "$OLD_TREE"
    assert_no_success_record web-rollback
    [[ -z "$(find "$RECORDS" -maxdepth 1 -name 'web-rollback-*.json.sha256' -print -quit)" ]] \
      || fail "failed rollback $fault left a success sidecar"
    rescue="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rescue-*' -print -quit)"
    assert_path_tree "$rescue" "$CANDIDATE_TREE" "publication boundary $fault rescue"
    [[ -n "$(find "$RECORDS" -maxdepth 1 -name '.web-rollback-record.*' -print -quit)" ]] \
      || fail "publication boundary $fault did not retain the source rollback record"
    [[ -z "$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rollback-failed-*' -print -quit)" ]] \
      || fail "publication boundary $fault attempted reverse rollback"
    assert_manual_recovery_record rollback ABSENT_UNCONFIRMED MATCHING_HEALTHY ABSENT ABSENT PRESENT
  done

  new_case; verify_case; deploy_case
  expect_fail 'rollback record directory fsync preserves matching live state' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=record-directory-fsync \
    "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD"
  assert_live_tree "$OLD_TREE"
  record="$(find "$RECORDS" -maxdepth 1 -name 'web-rollback-*.json' -print -quit)"
  [[ -n "$record" && -f "$record" && -f "${record}.sha256" ]] \
    || fail 'directory-fsync terminal rollback did not preserve complete matching evidence'
  rescue="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rescue-*' -print -quit)"
  assert_path_tree "$rescue" "$CANDIDATE_TREE" 'terminal rollback rescue'
  assert_manual_recovery_record rollback COMPLETE_EXPECTED MATCHING_HEALTHY PRESENT PRESENT ABSENT

  new_case; verify_case; deploy_case
  expect_fail 'rollback link success before child feedback' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=record-link-no-feedback \
    "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD"
  assert_live_tree "$OLD_TREE"
  record="$(find "$RECORDS" -maxdepth 1 -name 'web-rollback-*.json' -print -quit)"
  [[ -n "$record" && -f "$record" && ! -e "${record}.sha256" ]] \
    || fail 'link-no-feedback rollback did not retain the expected final-only record state'
  [[ "$(stat -Lc %h "$record")" == 2 ]] || fail 'link-no-feedback rollback final record is not nlink2'
  [[ -n "$(find "$RECORDS" -maxdepth 1 -name '.web-rollback-record.*' -print -quit)" ]] \
    || fail 'link-no-feedback rollback did not retain the linked source record'
  rescue="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rescue-*' -print -quit)"
  assert_path_tree "$rescue" "$CANDIDATE_TREE" 'link-no-feedback rollback rescue'
  [[ -z "$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rollback-failed-*' -print -quit)" ]] \
    || fail 'link-no-feedback rollback attempted reverse rollback'
  assert_manual_recovery_record rollback PARTIAL_OR_INVALID MATCHING_HEALTHY PRESENT ABSENT PRESENT

  new_case; verify_case; deploy_case
  expect_fail 'rollback cleanup final unlink failure' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=record-post-link-unlink,record-cleanup-final-unlink \
    "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD"
  assert_live_tree "$OLD_TREE"
  record="$(find "$RECORDS" -maxdepth 1 -name 'web-rollback-*.json' -print -quit)"
  [[ -n "$record" && -f "${record}.sha256" && "$(stat -Lc %h "$record")" == 1 ]] \
    || fail 'cleanup-final-unlink rollback did not preserve complete nlink1 evidence'
  [[ -z "$(find "$RECORDS" -maxdepth 1 -name '.web-rollback-record.*' -print -quit)" ]] \
    || fail 'cleanup-final-unlink rollback unexpectedly retained the source record'
  rescue="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rescue-*' -print -quit)"
  assert_path_tree "$rescue" "$CANDIDATE_TREE" 'cleanup-final-unlink rollback rescue'
  [[ -z "$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rollback-failed-*' -print -quit)" ]] \
    || fail 'cleanup-final-unlink rollback attempted reverse rollback'
  assert_manual_recovery_record rollback COMPLETE_EXPECTED MATCHING_HEALTHY PRESENT PRESENT ABSENT

  new_case; verify_case; deploy_case
  expect_fail 'rollback cleanup sidecar unlink failure' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=record-final-link,record-cleanup-sidecar-unlink \
    "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD"
  assert_live_tree "$OLD_TREE"
  [[ -z "$(find "$RECORDS" -maxdepth 1 -name 'web-rollback-*.json' -print -quit)" ]] \
    || fail 'cleanup-sidecar-unlink rollback unexpectedly retained a final record'
  [[ -n "$(find "$RECORDS" -maxdepth 1 -name 'web-rollback-*.json.sha256' -print -quit)" ]] \
    || fail 'cleanup-sidecar-unlink rollback did not retain the sidecar'
  [[ -n "$(find "$RECORDS" -maxdepth 1 -name '.web-rollback-record.*' -print -quit)" ]] \
    || fail 'cleanup-sidecar-unlink rollback did not retain the source record'
  rescue="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rescue-*' -print -quit)"
  assert_path_tree "$rescue" "$CANDIDATE_TREE" 'cleanup-sidecar-unlink rollback rescue'
  [[ -z "$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rollback-failed-*' -print -quit)" ]] \
    || fail 'cleanup-sidecar-unlink rollback attempted reverse rollback'
  assert_manual_recovery_record rollback PARTIAL_OR_INVALID MATCHING_HEALTHY ABSENT PRESENT PRESENT

  new_case; verify_case; deploy_case
  expect_fail 'rollback cleanup directory fsync failure' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=record-post-link-unlink,record-cleanup-directory-fsync \
    "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD"
  assert_live_tree "$OLD_TREE"
  assert_no_success_record web-rollback
  [[ -z "$(find "$RECORDS" -maxdepth 1 -name 'web-rollback-*.json.sha256' -print -quit)" ]] \
    || fail 'cleanup-directory-fsync rollback retained a visible sidecar'
  [[ -n "$(find "$RECORDS" -maxdepth 1 -name '.web-rollback-record.*' -print -quit)" ]] \
    || fail 'cleanup-directory-fsync rollback did not retain the source record'
  rescue="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rescue-*' -print -quit)"
  assert_path_tree "$rescue" "$CANDIDATE_TREE" 'cleanup-directory-fsync rollback rescue'
  [[ -z "$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rollback-failed-*' -print -quit)" ]] \
    || fail 'cleanup-directory-fsync rollback attempted reverse rollback'
  assert_manual_recovery_record rollback ABSENT_UNCONFIRMED MATCHING_HEALTHY ABSENT ABSENT PRESENT

  new_case; verify_case; deploy_case
  expect_fail 'compound rollback restored-tree removal failure' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=health,recovery-rollback-failed \
    "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD"
  assert_live_tree "$OLD_TREE"
  rescue="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rescue-*' -print -quit)"
  assert_path_tree "$rescue" "$CANDIDATE_TREE" 'compound rollback rescue'
  [[ -z "$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rollback-failed-*' -print -quit)" ]] \
    || fail 'restored-tree removal failure unexpectedly created a rollback-failed directory'
  assert_no_success_record web-rollback
  assert_manual_recovery_record rollback

  new_case; verify_case; deploy_case
  expect_fail 'compound rollback rescue restore failure' approval_env env \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=health,recovery-rescue \
    "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD"
  [[ ! -e "$LIVE" ]] || fail 'rescue-restore failure unexpectedly left a live directory'
  rescue="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rescue-*' -print -quit)"
  failed="$(find "$BACKUP" -maxdepth 1 -type d -name 'kit-rollback-failed-*' -print -quit)"
  assert_path_tree "$rescue" "$CANDIDATE_TREE" 'compound rollback retained rescue'
  assert_path_tree "$failed" "$OLD_TREE" 'compound rollback failed restored tree'
  assert_no_success_record web-rollback
  assert_manual_recovery_record rollback
}

case "$SELECTOR" in
  static) run_static;; proof) run_proof;; archive) run_archive;; guard) run_guard;;
  deploy) run_deploy;; rollback) run_rollback;;
  all) run_static; run_proof; run_archive; run_guard; run_deploy; run_rollback;;
esac
printf 'WEB_DEPLOY_ADAPTATION_TESTS=PASS\n'
