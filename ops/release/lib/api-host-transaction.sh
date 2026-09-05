#!/usr/bin/env bash
# Narrow, canonical-only host transaction helpers for JVC-OAI-HOST-ADAPT R1.

readonly CYF_HOST_SCHEMA=cyf-jvc-oai-host-release-v1
readonly CYF_HOST_LIVE_JAR=/opt/cyf/service/api/cyf-api-kit.jar
readonly CYF_HOST_LIFECYCLE=/usr/local/sbin/cyf-api-kit
readonly CYF_HOST_RELEASE_LOCK=/tmp/cyf-release-api.lock
readonly CYF_HOST_LIFECYCLE_LOCK=/tmp/cyf-api-lifecycle.lock

host_offline() {
  [[ "${CYF_RELEASE_OFFLINE_TEST:-}" == YES ]]
}

host_path() {
  local path="$1"
  if host_offline; then
    [[ -n "${CYF_RELEASE_TEST_ROOT:-}" && "$CYF_RELEASE_TEST_ROOT" == /* ]] \
      || die "offline fixture root is missing or unsafe"
    printf '%s%s\n' "${CYF_RELEASE_TEST_ROOT%/}" "$path"
  else
    printf '%s\n' "$path"
  fi
}

host_validate_input() {
  python3 -B - "$1" <<'PY'
import json, os, re, sys

def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: {}'.format(key))
        result[key] = value
    return result

with open(sys.argv[1], 'r', encoding='utf-8') as stream:
    data = json.load(stream, object_pairs_hook=unique)
if set(data) != {'schema', 'releaseId', 'artifactRoot', 'api', 'web', 'host'}:
    raise SystemExit('unexpected top-level release input fields')
if data['schema'] != 'cyf-jvc-oai-host-release-v1':
    raise SystemExit('unsupported host release schema')
if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,79}', data['releaseId']):
    raise SystemExit('unsafe releaseId')
if not os.path.isabs(data['artifactRoot']):
    raise SystemExit('artifactRoot must be absolute')
api = data['api']
if set(api) != {'repo', 'ref', 'head', 'tree', 'gradleTask', 'jarRelativePath', 'orchestrator'}:
    raise SystemExit('unexpected api fields')
for key in ('repo', 'ref', 'head', 'tree', 'gradleTask', 'jarRelativePath', 'orchestrator'):
    if not isinstance(api[key], (str, dict)):
        raise SystemExit('invalid api field: {}'.format(key))
if not os.path.isabs(api['repo']) or not re.fullmatch(r'[0-9a-f]{40}', api['head']) \
        or not re.fullmatch(r'[0-9a-f]{40}', api['tree']):
    raise SystemExit('invalid pinned API identity')
if not re.fullmatch(r':[A-Za-z0-9:_-]+', api['gradleTask']):
    raise SystemExit('unsafe Gradle task')
if api['jarRelativePath'].startswith('/') or '..' in api['jarRelativePath'].split('/'):
    raise SystemExit('unsafe JAR relative path')
orch = api['orchestrator']
if set(orch) != {'path', 'taskId', 'selector', 'fixtureDigest'}:
    raise SystemExit('unexpected orchestrator fields')
if orch['path'] != '/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py':
    raise SystemExit('orchestrator path is not canonical')
if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._-]{0,127}', orch['taskId']):
    raise SystemExit('unsafe orchestrator taskId')
if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9._:-]{0,159}', orch['selector']):
    raise SystemExit('unsafe orchestrator selector')
if not re.fullmatch(r'(N/A|[0-9a-f]{64})', orch['fixtureDigest']):
    raise SystemExit('unsafe orchestrator fixture digest')
web = data['web']
if set(web) != {'repo', 'ref', 'head', 'tree', 'npmBin', 'distRelativePath', 'admission'}:
    raise SystemExit('unexpected web fields')
if not os.path.isabs(web['repo']) or not re.fullmatch(r'[0-9a-f]{40}', web['head']) \
        or not re.fullmatch(r'[0-9a-f]{40}', web['tree']):
    raise SystemExit('invalid pinned Web identity')
if web['npmBin'] != '/home/isp/apps/node/lib/node_modules/npm/bin/npm-cli.js':
    raise SystemExit('Web npm path must be the real canonical npm-cli.js')
if web['distRelativePath'] != 'dist':
    raise SystemExit('unexpected Web dist path')
if web['admission'] != 'PROVISIONAL_DO_NOT_BUILD_OR_DEPLOY':
    raise SystemExit('Web pin is not fail-closed provisional input')
host = data['host']
expected_host = {
    'liveJar': '/opt/cyf/service/api/cyf-api-kit.jar',
    'lifecycle': '/usr/local/sbin/cyf-api-kit',
    'releaseLock': '/tmp/cyf-release-api.lock',
    'lifecycleLock': '/tmp/cyf-api-lifecycle.lock',
    'backupRoot': '/opt/cyf/service/api/backups',
    'recordRoot': '/opt/cyf/service/api/release-records',
}
if set(host) != set(expected_host) | {'installedLifecycleSha256', 'candidateLifecycleSha256'}:
    raise SystemExit('unexpected host fields')
for key, expected in expected_host.items():
    if host[key] != expected:
        raise SystemExit('non-canonical host path: {}'.format(key))
for key in ('installedLifecycleSha256', 'candidateLifecycleSha256'):
    if not re.fullmatch(r'[0-9a-f]{64}', host[key]):
        raise SystemExit('invalid lifecycle digest: {}'.format(key))
PY
}

host_load_input() {
  [[ ! -L "$1" ]] || die "release input must not be a symlink"
  load_release_input_path="$(normalize_absolute_path 'release input' "$1")"
  [[ -f "$load_release_input_path" && ! -L "$load_release_input_path" ]] \
    || die "host release input must be a physical regular file"
  host_validate_input "$load_release_input_path" || die "invalid host release input"
  RELEASE_INPUT="$load_release_input_path"
  RELEASE_ID="$(json_get "$RELEASE_INPUT" releaseId)"
  ARTIFACT_ROOT="$(normalize_absolute_path 'artifact root' "$(json_get "$RELEASE_INPUT" artifactRoot)")"
  API_REPO="$(normalize_absolute_path 'API repo' "$(json_get "$RELEASE_INPUT" api.repo)")"
  API_REF="$(json_get "$RELEASE_INPUT" api.ref)"
  API_HEAD="$(json_get "$RELEASE_INPUT" api.head)"
  API_TREE="$(json_get "$RELEASE_INPUT" api.tree)"
  API_GRADLE_TASK="$(json_get "$RELEASE_INPUT" api.gradleTask)"
  API_JAR_RELATIVE_PATH="$(json_get "$RELEASE_INPUT" api.jarRelativePath)"
  ORCHESTRATOR_PATH="$(json_get "$RELEASE_INPUT" api.orchestrator.path)"
  ORCHESTRATOR_TASK="$(json_get "$RELEASE_INPUT" api.orchestrator.taskId)"
  ORCHESTRATOR_SELECTOR="$(json_get "$RELEASE_INPUT" api.orchestrator.selector)"
  ORCHESTRATOR_FIXTURE="$(json_get "$RELEASE_INPUT" api.orchestrator.fixtureDigest)"
  API_ARTIFACT="$ARTIFACT_ROOT/api/cyf-api-${API_HEAD}-${API_TREE}.jar"
  API_METADATA="${API_ARTIFACT}.json"
  LIVE_JAR="$(host_path "$CYF_HOST_LIVE_JAR")"
  LIFECYCLE="$(host_path "$CYF_HOST_LIFECYCLE")"
  RELEASE_LOCK="$(host_path "$CYF_HOST_RELEASE_LOCK")"
  LIFECYCLE_LOCK="$(host_path "$CYF_HOST_LIFECYCLE_LOCK")"
  BACKUP_ROOT="$(host_path /opt/cyf/service/api/backups)"
  RECORD_ROOT="$(host_path /opt/cyf/service/api/release-records)"
  INSTALLED_LIFECYCLE_SHA="$(json_get "$RELEASE_INPUT" host.installedLifecycleSha256)"
  CANDIDATE_LIFECYCLE_SHA="$(json_get "$RELEASE_INPUT" host.candidateLifecycleSha256)"
  case "$ARTIFACT_ROOT" in "$API_REPO"|"$API_REPO"/*) die "artifact root must be outside API worktree" ;; esac
}

host_tool_digest() {
  (
    cd -- "$CYF_RELEASE_SCRIPT_DIR"
    for file in common.sh build-api.sh verify-release.sh deploy-api.sh rollback-api.sh \
      install-api-lifecycle.sh activate-api-voice.sh lib/api-host-transaction.sh host/cyf-api-kit \
      nginx/juyiting-voice-http.conf nginx/juyiting-voice-server.conf nginx/juyiting-voice-deny.conf; do
      [[ -f "$file" && ! -L "$file" ]] || die "host release source is missing or symlinked: $file"
      printf '%s\0' "$file"; sha256sum -- "$file"
    done
  ) | sha256sum | awk '{print $1}'
}

host_verify_artifact_metadata() {
  local digest input_sha tool_sha
  digest="$(host_sha_regular "$API_ARTIFACT")"
  input_sha="$(host_sha_regular "$RELEASE_INPUT")"
  tool_sha="$(host_tool_digest)"
  for path in "$API_ARTIFACT" "$API_METADATA" "${API_ARTIFACT}.sha256" "${API_METADATA}.sha256"; do
    [[ -f "$path" && ! -L "$path" && "$(stat -Lc '%a:%h' "$path")" == 444:1 ]] \
      || die "immutable artifact publication is unsafe: $path"
  done
  python3 -B - "$API_METADATA" "$RELEASE_ID" "$API_REF" "$API_HEAD" "$API_TREE" \
    "$(basename -- "$API_ARTIFACT")" "$digest" "$input_sha" "$tool_sha" \
    "$ORCHESTRATOR_TASK" "$ORCHESTRATOR_SELECTOR" "$ORCHESTRATOR_FIXTURE" "$API_GRADLE_TASK" <<'PY'
import json, sys
(path, release_id, source_ref, head, tree, artifact, digest, input_sha, tool_sha,
 task, selector, fixture, gradle_task) = sys.argv[1:]
def unique(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise ValueError('duplicate metadata key')
        result[key]=value
    return result
with open(path,'r',encoding='utf-8') as stream: data=json.load(stream,object_pairs_hook=unique)
expected={'schema':'cyf-api-host-artifact-v1','releaseId':release_id,'sourceRef':source_ref,
 'apiHead':head,'apiTree':tree,'artifact':artifact,'artifactSha256':digest,
 'releaseInputSha256':input_sha,'releaseToolSha256':tool_sha,'orchestratorTaskId':task,
 'selector':selector,'fixtureDigest':fixture,'gradleTask':gradle_task,'deployment':'NOT_PERFORMED'}
if data != expected: raise SystemExit('artifact metadata mismatch')
PY
}

host_require_execute_approval() {
  (( EXECUTE == 1 )) || return 0
  [[ "${CYF_RELEASE_APPROVED:-}" == YES ]] || die "--execute requires CYF_RELEASE_APPROVED=YES"
  require_safe_id "CYF_RELEASE_APPROVAL_ID" "${CYF_RELEASE_APPROVAL_ID:-}"
  [[ "${CYF_RELEASE_APPROVED_API_HEAD:-}" == "$API_HEAD" ]] || die "approved API HEAD mismatch"
  [[ "${CYF_RELEASE_APPROVED_API_TREE:-}" == "$API_TREE" ]] || die "approved API tree mismatch"
  if host_offline; then
    [[ "${CYF_RELEASE_ALLOW_OFFLINE_EXECUTE:-}" == YES ]] || die "offline execute is test-only and not admitted"
  else
    [[ -z "${CYF_RELEASE_TEST_ROOT:-}${CYF_RELEASE_ALLOW_OFFLINE_EXECUTE:-}" ]] \
      || die "test overrides are forbidden for host execution"
    (( EUID == 0 )) || die "host execution requires root"
  fi
}

host_expected_lock_tuple() {
  if host_offline; then
    printf '%s:%s:%s:%s\n' "$(stat -Lc %a "$1")" "$(id -u)" "$(id -g)" 1
  elif [[ "$1" == "$RELEASE_LOCK" ]]; then
    printf '660:0:%s:1\n' "$(id -g isp)"
  else
    printf '600:0:0:1\n'
  fi
}

host_validate_lock() {
  local path="$1" expected actual
  [[ -f "$path" && ! -L "$path" ]] || die "lock is missing or unsafe: $path"
  expected="$(host_expected_lock_tuple "$path")"
  actual="$(stat -Lc '%a:%u:%g:%h' "$path")"
  [[ "$actual" == "$expected" ]] || die "unsafe lock metadata: $path"
}

host_acquire_release_lock() {
  host_validate_lock "$RELEASE_LOCK"
  exec 8<>"$RELEASE_LOCK"
  [[ "$(stat -Lc '%d:%i' "$RELEASE_LOCK")" == "$(stat -Lc '%d:%i' /proc/$$/fd/8)" ]] \
    || die "release lock path changed while opening FD8"
  flock -n 8 || die "another API release transaction is active"
  CYF_RELEASE_LOCK_DEVICE="$(stat -Lc %d /proc/$$/fd/8)"
  CYF_RELEASE_LOCK_INODE="$(stat -Lc %i /proc/$$/fd/8)"
  export CYF_RELEASE_LOCK_INHERITED_FD=8 CYF_RELEASE_LOCK_DEVICE CYF_RELEASE_LOCK_INODE
  export CYF_RELEASE_LOCK_HELD=1
}

host_call_lifecycle() {
  [[ -x "$LIFECYCLE" && ! -L "$LIFECYCLE" ]] || die "canonical lifecycle is missing or unsafe"
  CYF_RELEASE_LOCK_INHERITED_FD=8 \
  CYF_RELEASE_LOCK_DEVICE="$CYF_RELEASE_LOCK_DEVICE" \
  CYF_RELEASE_LOCK_INODE="$CYF_RELEASE_LOCK_INODE" \
  CYF_RELEASE_LOCK_HELD=1 \
    "$LIFECYCLE" "$1"
}

host_sha_regular() {
  python3 -B - "$1" <<'PY'
import hashlib, os, stat, sys
fd = os.open(sys.argv[1], os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
try:
    before = os.fstat(fd)
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise SystemExit('unsafe regular file')
    digest = hashlib.sha256()
    while True:
        block = os.read(fd, 1024 * 1024)
        if not block:
            break
        digest.update(block)
    after = os.fstat(fd)
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != \
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise SystemExit('file changed while hashing')
    print(digest.hexdigest())
finally:
    os.close(fd)
PY
}

host_validate_boot_jar() {
  python3 -B - "$1" <<'PY'
import pathlib, stat, sys, zipfile
path=sys.argv[1]
with zipfile.ZipFile(path) as archive:
    names=set()
    for item in archive.infolist():
        pure=pathlib.PurePosixPath(item.filename)
        if pure.is_absolute() or '..' in pure.parts or item.filename in names:
            raise SystemExit('unsafe or duplicate JAR member')
        names.add(item.filename)
        mode=(item.external_attr >> 16) & 0xffff
        if stat.S_ISLNK(mode): raise SystemExit('symlink JAR member is forbidden')
    required={'META-INF/MANIFEST.MF','org/springframework/boot/loader/launch/JarLauncher.class'}
    if not required.issubset(names) or not any(name.startswith('BOOT-INF/classes/') for name in names):
        raise SystemExit('JAR is not the expected Spring Boot layout')
    manifest=archive.read('META-INF/MANIFEST.MF').decode('utf-8','strict')
    if 'Main-Class: org.springframework.boot.loader.launch.JarLauncher' not in manifest \
            or '\nStart-Class: ' not in manifest:
        raise SystemExit('JAR manifest is not executable Spring Boot metadata')
PY
}

host_validate_live_jar() {
  local expected
  [[ -f "$LIVE_JAR" && ! -L "$LIVE_JAR" ]] || die "live JAR is missing or unsafe"
  if host_offline; then
    expected="640:$(id -u):$(id -g):1"
  else
    expected="640:0:$(id -g isp):1"
  fi
  [[ "$(stat -Lc '%a:%u:%g:%h' "$LIVE_JAR")" == "$expected" ]] \
    || die "live JAR must be canonical 0640 regular nlink1"
}

host_prepare_transaction_dirs() {
  local path mode owner group
  if host_offline; then
    for path in "$(dirname -- "$LIVE_JAR")" "$BACKUP_ROOT" "$RECORD_ROOT"; do
      [[ -d "$path" && ! -L "$path" ]] || die "offline transaction directory is missing"
    done
    return 0
  fi
  owner=root; group=isp; mode=0750
  for path in /opt /opt/cyf /opt/cyf/service /opt/cyf/service/api; do
    [[ -d "$path" && ! -L "$path" ]] || die "trusted deployment path is missing: $path"
    [[ "$(stat -Lc '%U:%a' "$path")" == root:* ]] || die "deployment path is not root-owned: $path"
    (( (8#$(stat -Lc %a "$path") & 8#022) == 0 )) || die "deployment path is group/other writable: $path"
  done
  install -d -m "$mode" -o "$owner" -g "$group" -- "$BACKUP_ROOT" "$RECORD_ROOT"
  [[ "$(stat -Lc '%a:%U:%G' "$BACKUP_ROOT")" == 750:root:isp ]] || die "unsafe backup root"
  [[ "$(stat -Lc '%a:%U:%G' "$RECORD_ROOT")" == 750:root:isp ]] || die "unsafe record root"
}

host_validate_lifecycle_destination_chain() {
  local root expected_uid path
  if host_offline; then
    root="${CYF_RELEASE_TEST_ROOT%/}"
    expected_uid="$(id -u)"
  else
    root=''
    expected_uid=0
  fi
  for path in "$root/usr" "$root/usr/local" "$root/usr/local/sbin"; do
    [[ -d "$path" && ! -L "$path" && "$(stat -Lc %u "$path")" == "$expected_uid" ]] \
      || die "lifecycle destination path is not trusted: $path"
    (( (8#$(stat -Lc %a "$path") & 8#022) == 0 )) \
      || die "lifecycle destination path is writable by group/other: $path"
  done
}

host_copy_exclusive() {
  local source="$1" destination="$2" mode="$3" expected_sha="$4"
  local uid gid
  if [[ -n "${5:-}" && -n "${6:-}" ]]; then
    uid="$5"; gid="$6"
  elif host_offline; then
    uid="$(id -u)"; gid="$(id -g)"
  else
    uid=0; gid="$(id -g isp)"
  fi
  python3 -B - "$source" "$destination" "$mode" "$uid" "$gid" "$expected_sha" <<'PY'
import hashlib, os, stat, sys
source, destination, mode_text, uid_text, gid_text, expected = sys.argv[1:]
sfd = os.open(source, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
dfd = None
try:
    before = os.fstat(sfd)
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise SystemExit('source is not an exclusive regular file')
    parent = os.path.dirname(destination)
    parent_info = os.stat(parent, follow_symlinks=False)
    if not stat.S_ISDIR(parent_info.st_mode):
        raise SystemExit('destination parent is unsafe')
    dfd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
    if os.fstat(dfd).st_dev != parent_info.st_dev:
        raise SystemExit('cross-device artifact transaction is forbidden')
    digest = hashlib.sha256()
    while True:
        block = os.read(sfd, 1024 * 1024)
        if not block:
            break
        digest.update(block)
        view = memoryview(block)
        while view:
            written = os.write(dfd, view)
            view = view[written:]
    after = os.fstat(sfd)
    if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != \
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
        raise SystemExit('source changed during stable copy')
    if digest.hexdigest() != expected:
        raise SystemExit('source digest mismatch')
    os.fchown(dfd, int(uid_text), int(gid_text))
    os.fchmod(dfd, int(mode_text, 8))
    os.fsync(dfd)
    pfd = os.open(parent, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
    try:
        os.fsync(pfd)
    finally:
        os.close(pfd)
finally:
    os.close(sfd)
    if dfd is not None:
        os.close(dfd)
PY
}

host_replace_durable() {
  if host_offline && [[ -n "${CYF_RELEASE_FAULT_REPLACE_MATCH:-}" \
      && "$(basename -- "$1")" == *"$CYF_RELEASE_FAULT_REPLACE_MATCH"* ]]; then
    return 91
  fi
  python3 -B - "$1" "$2" <<'PY'
import os, sys
source, destination = sys.argv[1:]
if os.stat(source, follow_symlinks=False).st_dev != os.stat(os.path.dirname(destination), follow_symlinks=False).st_dev:
    raise SystemExit('cross-device replace is forbidden')
os.replace(source, destination)
fd = os.open(os.path.dirname(destination), os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
try:
    os.fsync(fd)
finally:
    os.close(fd)
PY
}

host_fsync_dir() {
  python3 -B - "$1" <<'PY'
import os,sys
fd=os.open(sys.argv[1], os.O_RDONLY|getattr(os,'O_DIRECTORY',0))
try: os.fsync(fd)
finally: os.close(fd)
PY
}

host_remove_durable() {
  python3 -B - "$1" <<'PY'
import os, sys
path=sys.argv[1]
if os.path.lexists(path):
    info=os.lstat(path)
    if not os.path.isfile(path) or os.path.islink(path) or info.st_nlink != 1:
        raise SystemExit('refusing unsafe durable removal')
    os.unlink(path)
fd=os.open(os.path.dirname(path), os.O_RDONLY|getattr(os,'O_DIRECTORY',0))
try: os.fsync(fd)
finally: os.close(fd)
PY
}

host_record_init() {
  python3 -B - "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" <<'PY'
import json, os, sys
path, kind, change_id, api_head, api_tree, backup, previous_sha, candidate_sha = sys.argv[1:]
record = {'schema': 'cyf-api-host-transaction-v1', 'kind': kind, 'changeId': change_id,
          'apiHead': api_head, 'apiTree': api_tree, 'backupArtifact': backup,
          'previousJarSha256': previous_sha, 'candidateJarSha256': candidate_sha,
          'transitions': ['PREPARED'], 'status': 'PREPARED',
          'databaseOperation': 'NOT_PERFORMED', 'rabbitMqOperation': 'NOT_PERFORMED'}
fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
with os.fdopen(fd, 'w', encoding='utf-8') as stream:
    json.dump(record, stream, sort_keys=True, indent=2); stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
parent = os.open(os.path.dirname(path), os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
try: os.fsync(parent)
finally: os.close(parent)
PY
}

host_record_state() {
  local after_replace_fault=''
  if host_offline && [[ "${CYF_RELEASE_FAULT_RECORD_STATE:-}" == "$2" ]]; then
    return 92
  fi
  if host_offline; then after_replace_fault="${CYF_RELEASE_FAULT_RECORD_STATE_AFTER_REPLACE:-}"; fi
  python3 -B - "$1" "$2" "$after_replace_fault" <<'PY'
import json, os, sys, tempfile
path, state, after_replace_fault = sys.argv[1:]
with open(path, 'r', encoding='utf-8') as stream:
    record = json.load(stream)
allowed = {
 'PREPARED': {'STOP_ATTEMPTED', 'ABORTED_BEFORE_STOP', 'FAILED_MANUAL_RECOVERY_REQUIRED'},
 'STOP_ATTEMPTED': {'STOPPED', 'ROLLED_BACK_HEALTHY', 'FAILED_MANUAL_RECOVERY_REQUIRED'},
 'STOPPED': {'CANDIDATE_INSTALLED', 'ROLLED_BACK_HEALTHY', 'FAILED_MANUAL_RECOVERY_REQUIRED'},
 'CANDIDATE_INSTALLED': {'STARTED_HEALTHY', 'ROLLED_BACK_HEALTHY', 'FAILED_MANUAL_RECOVERY_REQUIRED'},
 'STARTED_HEALTHY': {'COMMITTED', 'FAILED_MANUAL_RECOVERY_REQUIRED'},
}
if state not in allowed.get(record['status'], set()):
    raise SystemExit('invalid transaction transition')
record['transitions'].append(state); record['status'] = state
fd, temp = tempfile.mkstemp(prefix='.txn.', dir=os.path.dirname(path))
try:
    with os.fdopen(fd, 'w', encoding='utf-8') as stream:
        json.dump(record, stream, sort_keys=True, indent=2); stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
    os.chmod(temp, 0o600)
    os.replace(temp, path)
    if after_replace_fault == state:
        raise SystemExit(96)
    parent = os.open(os.path.dirname(path), os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
    try: os.fsync(parent)
    finally: os.close(parent)
finally:
    if os.path.exists(temp): os.unlink(temp)
PY
}

host_finalize_record() {
  local fault=''
  if host_offline; then fault="${CYF_RELEASE_FAULT_FINALIZE:-}"; fi
  if [[ "$fault" == before-chmod ]]; then
    return 93
  fi
  chmod 0444 "$1"
  if [[ "$fault" == file-fsync ]]; then
    return 94
  fi
  python3 -B - "$1" "$fault" <<'PY'
import os, sys
fd = os.open(sys.argv[1], os.O_RDONLY)
try: os.fsync(fd)
finally: os.close(fd)
if sys.argv[2] == 'dir-fsync':
    raise SystemExit(95)
parent = os.open(os.path.dirname(sys.argv[1]), os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0))
try: os.fsync(parent)
finally: os.close(parent)
PY
}

host_parse_voice_config() {
  python3 -B - "$1" "${2:-java}" <<'PY'
from pathlib import Path
from urllib.parse import urlsplit
import base64, hmac, re, sys
path, output_mode = Path(sys.argv[1]), sys.argv[2]
java_names = {
 'JIA_CHAT_VOICE_ENABLED', 'JIA_CHAT_VOICE_IDENTITY_HMAC_SECRET',
 'JIA_CHAT_VOICE_CACHE_ENCRYPTION_KEY', 'JIA_CHAT_VOICE_COMPATIBILITY_GATEWAY_ALLOWLIST',
 'JIA_CHAT_VOICE_TRANSCRIPTION_ENABLED', 'JIA_CHAT_VOICE_TRANSCRIPTION_PROVIDER',
 'JIA_CHAT_VOICE_TRANSCRIPTION_MODEL', 'JIA_CHAT_VOICE_SYNTHESIS_ENABLED',
 'JIA_CHAT_VOICE_SYNTHESIS_PROVIDER', 'JIA_CHAT_VOICE_SYNTHESIS_MODEL',
 'JIA_CHAT_VOICE_SYNTHESIS_PROVIDER_VOICE', 'SPRING_AI_OPENAI_API_KEY',
 'SPRING_AI_OPENAI_BASE_URL', 'SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_API_KEY',
 'SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_BASE_URL', 'SPRING_AI_OPENAI_AUDIO_SPEECH_API_KEY',
 'SPRING_AI_OPENAI_AUDIO_SPEECH_BASE_URL'}
allowed = java_names | {'CYF_VOICE_SMOKE_BEARER_TOKEN'}
values = {}
for number, raw in enumerate(path.read_bytes().splitlines(), 1):
    if not raw or raw.startswith(b'#'): continue
    if b'\0' in raw or any(byte < 32 or byte == 127 for byte in raw):
        raise SystemExit('invalid control byte at line {}'.format(number))
    try: line = raw.decode('utf-8')
    except UnicodeDecodeError: raise SystemExit('configuration must be UTF-8')
    name, separator, value = line.partition('=')
    if not separator or not re.fullmatch(r'[A-Z][A-Z0-9_]*', name) or name not in allowed or name in values:
        raise SystemExit('unknown, duplicate or invalid name at line {}'.format(number))
    values[name] = value
required = {'JIA_CHAT_VOICE_ENABLED':'true', 'JIA_CHAT_VOICE_TRANSCRIPTION_ENABLED':'true',
 'JIA_CHAT_VOICE_TRANSCRIPTION_PROVIDER':'openai-compatible',
 'JIA_CHAT_VOICE_TRANSCRIPTION_MODEL':'whisper-1', 'JIA_CHAT_VOICE_SYNTHESIS_ENABLED':'true',
 'JIA_CHAT_VOICE_SYNTHESIS_PROVIDER':'openai-compatible',
 'JIA_CHAT_VOICE_SYNTHESIS_MODEL':'gpt-4o-mini-tts',
 'JIA_CHAT_VOICE_SYNTHESIS_PROVIDER_VOICE':'alloy'}
for name, expected in required.items():
    if values.get(name) != expected: raise SystemExit('invalid activation setting: {}'.format(name))
identity = values.get('JIA_CHAT_VOICE_IDENTITY_HMAC_SECRET','').encode('utf-8')
if len(identity) < 32: raise SystemExit('invalid identity key')
try: cache = base64.b64decode(values.get('JIA_CHAT_VOICE_CACHE_ENCRYPTION_KEY',''), validate=True)
except (ValueError, TypeError): cache = b''
if len(cache) != 32: raise SystemExit('invalid cache key')
common_key = values.get('SPRING_AI_OPENAI_API_KEY','')
tkey = values.get('SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_API_KEY', common_key)
skey = values.get('SPRING_AI_OPENAI_AUDIO_SPEECH_API_KEY', common_key)
if not tkey or not skey: raise SystemExit('provider API keys are missing')
for secret in (tkey.encode(), skey.encode(), cache, values.get('JIA_CHAT_VOICE_CACHE_ENCRYPTION_KEY','').encode()):
    if hmac.compare_digest(identity, secret): raise SystemExit('credentials must be independent')
common_url = values.get('SPRING_AI_OPENAI_BASE_URL','')
urls = [values.get('SPRING_AI_OPENAI_AUDIO_TRANSCRIPTION_BASE_URL', common_url),
        values.get('SPRING_AI_OPENAI_AUDIO_SPEECH_BASE_URL', common_url)]
for url in urls:
    parsed=urlsplit(url); segments=parsed.path[1:].split('/') if parsed.path.startswith('/') else []
    if (parsed.scheme.lower()!='https' or not parsed.hostname or parsed.username or parsed.password
            or parsed.query or parsed.fragment or parsed.path=='/' or not segments
            or any(part in ('','.','..') for part in segments) or url.endswith('/')
            or any(ch in url for ch in ('%','\\',';')) or parsed.geturl()!=url):
        raise SystemExit('unsafe provider gateway')
allowlist = set(filter(None, values.get('JIA_CHAT_VOICE_COMPATIBILITY_GATEWAY_ALLOWLIST',
                                        'https://api.openai.com/v1').split(',')))
if not set(urls).issubset(allowlist): raise SystemExit('provider gateway is not allowlisted')
if not values.get('CYF_VOICE_SMOKE_BEARER_TOKEN'): raise SystemExit('smoke credential is missing')
names = sorted(values if output_mode == 'all' else java_names & set(values))
for name in names:
    print(base64.b64encode((name+'='+values[name]).encode('utf-8')).decode('ascii'))
PY
}
