#!/bin/bash -p
set -Eeuo pipefail
IFS=$'\n\t'
umask 077
export PATH='/usr/sbin:/usr/bin:/sbin:/bin'
export LC_ALL='C'
unset BASH_ENV ENV CDPATH GLOBIGNORE

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
  python3 -B - "$archive" "$variant" <<'PY'
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
  python3 -B - "$PROOF" "$RELEASE_ID" "$API_HEAD" "$API_TREE" "$JAR_SHA" \
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
  python3 -B - "$INPUT" "$RELEASE_ID" "$ARCHIVE" "$archive_sha" "$REPO" "$WEB_REF" \
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

new_case() {
  CASE_INDEX=$((CASE_INDEX+1)); CASE="$RUN/case-$CASE_INDEX"; mkdir -m 0700 "$CASE"
  export CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE"
  unset CYF_WEB_DEPLOY_ADAPTER_FAULT
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
  CANDIDATE_TREE="$(python3 -B - "$GUARD" <<'PY'
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

run_static() {
  local script
  for script in "$VERIFY" "$DEPLOY" "$ROLLBACK" "$ROOT/ops/release/lib/web-deploy-adapter.sh" "$0"; do
    head -1 "$script" | grep -Eq '^#!/bin/bash( -p)?$' || fail "non-absolute Bash entrypoint: $script"
  done
  python3 -B - "$ROOT/ops/release/tests/test-web-deploy-adaptation.sh" <<'PY'
import pathlib,sys
text=pathlib.Path(sys.argv[1]).read_text(encoding='utf-8')
for token in ('/dev/'+'shm', 'ev'+'al ', 'npm'+' ', 'gra'+'dle', 'system'+'ctl', 'p'+'kill'):
    if token in text: raise SystemExit('forbidden fixture-test token: {}'.format(token))
PY
  grep -Fq "MINIMUM_FREE_BYTES=0" "$ROOT/ops/release/lib/web-deploy-adapter.sh" \
    || fail 'cancelled legacy resource threshold was reactivated'
  pass 'static privileged-entrypoint and forbidden-mechanism fences'
}

run_proof() {
  new_case; rm "$PROOF"; expect_fail 'compiler flag without external proof' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
  local field value
  for field in status stt tts routes deny loopback; do
    new_case; rm "$PROOF"
    case "$field" in
      status) write_proof UNHEALTHY;; stt) write_proof ACTIVATED_HEALTHY FAIL;;
      tts) write_proof ACTIVATED_HEALTHY PASS FAIL;; routes) write_proof ACTIVATED_HEALTHY PASS PASS FAIL;;
      deny) write_proof ACTIVATED_HEALTHY PASS PASS PASS FAIL;;
      loopback) write_proof ACTIVATED_HEALTHY PASS PASS PASS PASS 0.0.0.0;;
    esac
    expect_fail "wrong activation proof $field" env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
  done
  new_case; chmod 0600 "$PROOF"; expect_fail 'mutable proof mode' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
  new_case; ln "$PROOF" "$CASE/proof-hardlink"; expect_fail 'hardlinked proof' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
  new_case; mv "$PROOF" "$CASE/proof-real"; ln -s ../proof-real "$PROOF"; expect_fail 'symlinked proof' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" "$VERIFY" --input "$INPUT"
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
  ( sleep 0.05; touch "$ARCHIVE" ) & mutator=$!
  expect_fail 'archive mutation while held open' env CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$CASE" \
    CYF_WEB_DEPLOY_ADAPTER_FAULT=archive-mutation-window "$VERIFY" --input "$INPUT"
  wait "$mutator"
}

run_guard() {
  new_case; verify_case
  [[ "$(stat -Lc '%a:%h' "$GUARD")" == '400:1' && "$(stat -Lc '%a:%h' "${GUARD}.sha256")" == '400:1' ]] \
    || fail 'guard publication is not immutable complete nlink1'
  chmod 0600 "$GUARD"
  expect_fail 'mutable guard' approval_env "$DEPLOY" --input "$INPUT" --dry-run
  new_case; verify_case; printf '\n' >> "$INPUT"
  expect_fail 'input changed after guard' approval_env "$DEPLOY" --input "$INPUT" --dry-run
  new_case; verify_case; chmod 0600 "$ARCHIVE"; printf x >> "$ARCHIVE"; chmod 0444 "$ARCHIVE"
  expect_fail 'archive changed after guard' approval_env "$DEPLOY" --input "$INPUT" --dry-run
}

run_deploy() {
  new_case; verify_case
  local binding
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

  local fault
  for fault in extraction staged-tree backup-rename cutover-rename health record-write; do
    new_case; verify_case
    expect_fail "deploy recovery $fault" approval_env env CYF_WEB_DEPLOY_ADAPTER_FAULT="$fault" "$DEPLOY" --input "$INPUT" --execute
    assert_live_tree "$OLD_TREE"
    [[ -z "$(find "$RECORDS" -maxdepth 1 -name 'web-deploy-*.json' -print -quit)" ]] || fail "failed deploy $fault left a committed record"
  done
}

run_rollback() {
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

  local fault
  for fault in rollback-staged-tree rollback-rescue-rename rollback-cutover-rename health record-write; do
    new_case; verify_case; deploy_case
    expect_fail "rollback rescue $fault" approval_env env CYF_WEB_DEPLOY_ADAPTER_FAULT="$fault" \
      "$ROLLBACK" --input "$INPUT" --execute "$DEPLOY_RECORD"
    assert_live_tree "$CANDIDATE_TREE"
    [[ -z "$(find "$RECORDS" -maxdepth 1 -name 'web-rollback-*.json' -print -quit)" ]] || fail "failed rollback $fault left a committed record"
  done
}

case "$SELECTOR" in
  static) run_static;; proof) run_proof;; archive) run_archive;; guard) run_guard;;
  deploy) run_deploy;; rollback) run_rollback;;
  all) run_static; run_proof; run_archive; run_guard; run_deploy; run_rollback;;
esac
printf 'WEB_DEPLOY_ADAPTATION_TESTS=PASS\n'
