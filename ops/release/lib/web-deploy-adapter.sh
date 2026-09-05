#!/bin/bash
# Fail-closed adapter for the immutable JVC-OAI Web artifact and API activation proof.

readonly WEB_ADAPTER_SCHEMA='cyf-jvc-oai-web-deploy-adapter-v1'
readonly WEB_ACTIVATION_PROOF_SCHEMA='cyf-jvc-oai-api-activation-proof-v1'
readonly WEB_GUARD_SCHEMA='cyf-jvc-oai-web-deploy-guard-v1'
readonly WEB_ADAPTER_PRODUCTION_TRUST_ROOT='/var/lib/cyf-jvc-release-controller'
readonly WEB_ADAPTER_EXPECTED_WEB_HEAD='6d88a3419d894c0abd0c9c3e96ea2e732890922b'
readonly WEB_ADAPTER_EXPECTED_WEB_TREE='c2a6a192199c702ef3be9d48c8c4b4f4c86e51ba'
readonly WEB_ADAPTER_EXPECTED_API_HEAD='34b67fed96061bf9c3132106ca219fc6f5f6ba05'
readonly WEB_ADAPTER_EXPECTED_API_TREE='fb42c46c1f63299a37b44d7e55c6a303ddf016f1'
readonly WEB_ADAPTER_EXPECTED_JAR_SHA='fa808e633e985551e66168b1d70c488d8cf01361662f630e9f48ccab265038d5'
readonly WEB_ADAPTER_EXPECTED_ARCHIVE='/tmp/jvc-oai-web-artifact-r1.B9dEVE/jvc-oai-web-dist.tar.gz'
readonly WEB_ADAPTER_EXPECTED_ARCHIVE_SHA='86d3fd759cdf95050ff7520c4bdccf762eaca1f0be2a58c03f5a9970914df93f'
readonly WEB_ADAPTER_DEFAULT_INPUT="$CYF_RELEASE_SCRIPT_DIR/jvc-oai-web-deploy-r1-input.json"
readonly WEB_ADAPTER_TOOL_FILES=(
  'lib/web-deploy-adapter.sh'
  'verify-web-deploy-adapter.sh'
  'deploy-web.sh'
  'rollback-web.sh'
)

web_adapter_fixture_mode() {
  [[ -n "${CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT:-}" ]]
}

web_adapter_select_default_input() {
  if [[ "$INPUT_FILE" == "$CYF_RELEASE_DEFAULT_INPUT" ]]; then
    INPUT_FILE="$WEB_ADAPTER_DEFAULT_INPUT"
  fi
}

web_adapter_stable_sha256() {
  python3 -B - "$1" <<'PY'
import hashlib, os, stat, sys
path = sys.argv[1]
fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
try:
    before = os.fstat(fd)
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise SystemExit('file must be a regular nlink1 object')
    digest = hashlib.sha256()
    while True:
        block = os.read(fd, 1024 * 1024)
        if not block:
            break
        digest.update(block)
    after = os.fstat(fd)
    path_after = os.stat(path, follow_symlinks=False)
    identity = lambda value: (value.st_dev, value.st_ino, value.st_size,
                              value.st_mtime_ns, value.st_ctime_ns, value.st_nlink)
    if identity(before) != identity(after) or (after.st_dev, after.st_ino) != (path_after.st_dev, path_after.st_ino):
        raise SystemExit('file changed while it was held open')
    print(digest.hexdigest())
finally:
    os.close(fd)
PY
}

web_adapter_tool_sha256() {
  (
    cd -- "$CYF_RELEASE_SCRIPT_DIR"
    local file
    for file in "${WEB_ADAPTER_TOOL_FILES[@]}"; do
      [[ -f "$file" && ! -L "$file" && "$(stat -Lc %h -- "$file")" == 1 ]] \
        || die "Web adapter tool file is missing or unsafe: $file"
      printf '%s\0' "$file"
      web_adapter_stable_sha256 "$file"
    done
  ) | sha256sum | awk '{print $1}'
}

web_adapter_secure_root() {
  local label="$1" path="$2" expected_uid
  [[ -d "$path" && ! -L "$path" ]] || die "$label must be one physical directory: $path"
  if web_adapter_fixture_mode; then expected_uid="$(id -u)"; else expected_uid=0; fi
  [[ "$(stat -Lc '%a:%u' -- "$path")" == "700:$expected_uid" ]] \
    || die "$label must be mode 0700 and owned by the trusted controller: $path"
}

web_adapter_load_input() {
  local requested="$1" count index
  local -a fields=()
  RELEASE_INPUT="$(normalize_absolute_path 'Web adapter input' "$requested")"
  [[ -f "$RELEASE_INPUT" && ! -L "$RELEASE_INPUT" && "$(stat -Lc %h -- "$RELEASE_INPUT")" == 1 ]] \
    || die "Web adapter input must be a regular nlink1 file: $RELEASE_INPUT"
  mapfile -d '' -t fields < <(python3 -B - "$RELEASE_INPUT" <<'PY'
import hashlib, json, os, re, stat, sys
path = sys.argv[1]
fd = os.open(path, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
try:
    before = os.fstat(fd)
    if not stat.S_ISREG(before.st_mode) or before.st_nlink != 1:
        raise SystemExit('input must be regular nlink1')
    content = bytearray(); digest = hashlib.sha256()
    while True:
        block = os.read(fd, 1024 * 1024)
        if not block: break
        content.extend(block); digest.update(block)
    after = os.fstat(fd); current = os.stat(path, follow_symlinks=False)
    identity = lambda value: (value.st_dev, value.st_ino, value.st_size,
                              value.st_mtime_ns, value.st_ctime_ns, value.st_nlink)
    if identity(before) != identity(after) or (after.st_dev, after.st_ino) != (current.st_dev, current.st_ino):
        raise SystemExit('input changed while held open')
finally:
    os.close(fd)
def unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError('duplicate JSON key: {}'.format(key))
        result[key] = value
    return result
data = json.loads(content.decode('utf-8'), object_pairs_hook=unique)
def exact(obj, keys, label):
    if not isinstance(obj, dict) or set(obj) != set(keys):
        raise SystemExit('{} has unexpected or missing fields'.format(label))
def text(value, label):
    if not isinstance(value, str) or not value or any(ord(ch) < 32 or ord(ch) == 127 for ch in value):
        raise SystemExit('{} must be a non-empty control-free string'.format(label))
    return value
exact(data, ('schema','releaseId','compileVoiceEnabled','archive','web','api','activationProof','webGuardRoot'), 'input')
exact(data['archive'], ('path','sha256'), 'archive')
exact(data['web'], ('repo','ref','head','tree','deploy'), 'web')
exact(data['web']['deploy'], ('liveDir','backupRoot','recordRoot','healthUrls','healthTimeoutSeconds'), 'web.deploy')
exact(data['api'], ('head','tree','deployedJarSha256'), 'api')
exact(data['activationProof'], ('schema','trustedRoot'), 'activationProof')
if data['schema'] != 'cyf-jvc-oai-web-deploy-adapter-v1':
    raise SystemExit('unsupported Web adapter schema')
if data['compileVoiceEnabled'] is not True:
    raise SystemExit('compileVoiceEnabled must be true')
values = [
    text(data['releaseId'], 'releaseId'), text(data['archive']['path'], 'archive.path'),
    text(data['archive']['sha256'], 'archive.sha256'), text(data['web']['repo'], 'web.repo'),
    text(data['web']['ref'], 'web.ref'), text(data['web']['head'], 'web.head'),
    text(data['web']['tree'], 'web.tree'), text(data['web']['deploy']['liveDir'], 'web.deploy.liveDir'),
    text(data['web']['deploy']['backupRoot'], 'web.deploy.backupRoot'),
    text(data['web']['deploy']['recordRoot'], 'web.deploy.recordRoot'),
    str(data['web']['deploy']['healthTimeoutSeconds']), text(data['api']['head'], 'api.head'),
    text(data['api']['tree'], 'api.tree'), text(data['api']['deployedJarSha256'], 'api.deployedJarSha256'),
    text(data['activationProof']['schema'], 'activationProof.schema'),
    text(data['activationProof']['trustedRoot'], 'activationProof.trustedRoot'),
    text(data['webGuardRoot'], 'webGuardRoot')]
urls = data['web']['deploy']['healthUrls']
if (not isinstance(data['web']['deploy']['healthTimeoutSeconds'], int)
        or isinstance(data['web']['deploy']['healthTimeoutSeconds'], bool)):
    raise SystemExit('healthTimeoutSeconds must be an integer')
if not isinstance(urls, list) or not urls:
    raise SystemExit('healthUrls must be a non-empty array')
values.append(digest.hexdigest())
values.append(str(len(urls)))
values.extend(text(value, 'healthUrls') for value in urls)
for value in values:
    sys.stdout.buffer.write(value.encode('utf-8') + b'\0')
PY
  )
  ((${#fields[@]} >= 20)) || die "invalid Web adapter input: $RELEASE_INPUT"
  RELEASE_ID="${fields[0]}"
  WEB_ARTIFACT="$(normalize_absolute_path 'Web archive' "${fields[1]}")"
  WEB_ARCHIVE_SHA_EXPECTED="${fields[2]}"
  WEB_REPO="$(normalize_absolute_path 'Web candidate repo' "${fields[3]}")"
  WEB_REF="${fields[4]}"; WEB_HEAD="${fields[5]}"; WEB_TREE="${fields[6]}"
  WEB_LIVE_DIR="$(normalize_absolute_path 'Web live directory' "${fields[7]}")"
  WEB_BACKUP_ROOT="$(normalize_absolute_path 'Web backup root' "${fields[8]}")"
  WEB_RECORD_ROOT="$(normalize_absolute_path 'Web record root' "${fields[9]}")"
  WEB_HEALTH_TIMEOUT="${fields[10]}"
  API_HEAD="${fields[11]}"; API_TREE="${fields[12]}"; API_DEPLOYED_JAR_SHA="${fields[13]}"
  ACTIVATION_PROOF_SCHEMA="${fields[14]}"
  ACTIVATION_PROOF_ROOT="$(normalize_absolute_path 'API activation proof root' "${fields[15]}")"
  WEB_GUARD_ROOT="$(normalize_absolute_path 'Web guard root' "${fields[16]}")"
  RELEASE_INPUT_SHA="${fields[17]}"
  count="${fields[18]}"
  [[ "$count" =~ ^[1-9][0-9]{0,2}$ && ${#fields[@]} -eq $((19 + count)) ]] \
    || die "invalid Web health URL list"
  WEB_HEALTH_URLS=()
  for ((index=0; index<count; index++)); do WEB_HEALTH_URLS+=("${fields[$((19 + index))]}"); done

  require_safe_id 'releaseId' "$RELEASE_ID"
  require_full_git_oid 'web.head' "$WEB_HEAD"; require_full_git_oid 'web.tree' "$WEB_TREE"
  require_full_git_oid 'api.head' "$API_HEAD"; require_full_git_oid 'api.tree' "$API_TREE"
  require_sha256 'Web archive' "$WEB_ARCHIVE_SHA_EXPECTED"
  require_sha256 'deployed API JAR' "$API_DEPLOYED_JAR_SHA"
  [[ "$ACTIVATION_PROOF_SCHEMA" == "$WEB_ACTIVATION_PROOF_SCHEMA" ]] \
    || die "unsupported API activation proof schema"
  [[ "$WEB_HEALTH_TIMEOUT" =~ ^[1-9][0-9]{0,3}$ ]] || die "Web health timeout is invalid"
  local url
  for url in "${WEB_HEALTH_URLS[@]}"; do
    [[ "$url" =~ ^https://[^[:space:]]+$ ]] || die "Web health URL must use HTTPS: $url"
  done
  require_sha256 'release input' "$RELEASE_INPUT_SHA"
  WEB_ADAPTER_TOOL_SHA="$(web_adapter_tool_sha256)"
  ACTIVATION_PROOF="$ACTIVATION_PROOF_ROOT/${ACTIVATION_PROOF_SCHEMA}.json"
  WEB_GUARD="$WEB_GUARD_ROOT/web-guard-${RELEASE_ID}-${WEB_HEAD}-${WEB_TREE}.json"
  # Historical M1 capacity thresholds are cancelled; common.sh records observation only.
  MINIMUM_FREE_BYTES=0

  if web_adapter_fixture_mode; then
    CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT="$(normalize_absolute_path 'Web adapter fixture root' "$CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT")"
    web_adapter_secure_root 'Web adapter fixture root' "$CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT"
    local path
    for path in "$RELEASE_INPUT" "$WEB_ARTIFACT" "$WEB_REPO" "$WEB_LIVE_DIR" \
      "$WEB_BACKUP_ROOT" "$WEB_RECORD_ROOT" "$ACTIVATION_PROOF_ROOT" "$WEB_GUARD_ROOT"; do
      assert_path_within 'fixture-owned Web adapter path' "$path" "$CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT"
    done
  else
    [[ -z "${CYF_WEB_DEPLOY_ADAPTER_FAULT:-}" ]] || die "Web adapter fault injection is test-only"
    [[ "$ACTIVATION_PROOF_ROOT" == "$WEB_ADAPTER_PRODUCTION_TRUST_ROOT" \
       && "$WEB_GUARD_ROOT" == "$WEB_ADAPTER_PRODUCTION_TRUST_ROOT" ]] \
      || die "production proof and guard root must be $WEB_ADAPTER_PRODUCTION_TRUST_ROOT"
    [[ "$WEB_HEAD" == "$WEB_ADAPTER_EXPECTED_WEB_HEAD" && "$WEB_TREE" == "$WEB_ADAPTER_EXPECTED_WEB_TREE" ]] \
      || die "Web source pin does not match the accepted JVC-OAI artifact"
    [[ "$API_HEAD" == "$WEB_ADAPTER_EXPECTED_API_HEAD" && "$API_TREE" == "$WEB_ADAPTER_EXPECTED_API_TREE" \
       && "$API_DEPLOYED_JAR_SHA" == "$WEB_ADAPTER_EXPECTED_JAR_SHA" ]] \
      || die "API identity does not match the accepted JVC-OAI artifact"
    [[ "$WEB_ARTIFACT" == "$WEB_ADAPTER_EXPECTED_ARCHIVE" \
       && "$WEB_ARCHIVE_SHA_EXPECTED" == "$WEB_ADAPTER_EXPECTED_ARCHIVE_SHA" ]] \
      || die "Web archive does not match the accepted immutable artifact"
    [[ "$WEB_LIVE_DIR" == '/home/isp/hosts/cyf/web/kit' \
       && "$WEB_BACKUP_ROOT" == '/home/isp/hosts/cyf/web/bak' \
       && "$WEB_RECORD_ROOT" == '/home/isp/hosts/cyf/web/bak/release-records' ]] \
      || die "Web deployment roots do not match the retained production layout"
  fi
  web_adapter_secure_root 'API activation proof root' "$ACTIVATION_PROOF_ROOT"
  [[ "$WEB_GUARD_ROOT" == "$ACTIVATION_PROOF_ROOT" ]] \
    || die "Web guard and activation proof must share the trusted controller root"
}

web_adapter_validate_activation_proof() {
  local -a facts=()
  mapfile -d '' -t facts < <(python3 -B - "$ACTIVATION_PROOF_ROOT" \
    "$(basename -- "$ACTIVATION_PROOF")" "$RELEASE_ID" "$API_HEAD" "$API_TREE" \
    "$API_DEPLOYED_JAR_SHA" "$(web_adapter_fixture_mode && id -u || printf 0)" <<'PY'
import hashlib, json, os, re, stat, sys
root, name, release_id, api_head, api_tree, jar_sha, expected_uid = sys.argv[1:]
rootfd = os.open(root, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0))
fd = None
try:
    rinfo = os.fstat(rootfd)
    if not stat.S_ISDIR(rinfo.st_mode) or stat.S_IMODE(rinfo.st_mode) != 0o700 or rinfo.st_uid != int(expected_uid):
        raise SystemExit('unsafe activation proof root')
    fd = os.open(name, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0), dir_fd=rootfd)
    before = os.fstat(fd)
    if (not stat.S_ISREG(before.st_mode) or stat.S_IMODE(before.st_mode) != 0o400
            or before.st_uid != int(expected_uid) or before.st_nlink != 1):
        raise SystemExit('activation proof must be owner 0400 regular nlink1')
    content = bytearray()
    digest = hashlib.sha256()
    while True:
        block = os.read(fd, 1024 * 1024)
        if not block:
            break
        content.extend(block); digest.update(block)
    after = os.fstat(fd)
    current = os.stat(name, dir_fd=rootfd, follow_symlinks=False)
    identity = lambda value: (value.st_dev, value.st_ino, value.st_size,
                              value.st_mtime_ns, value.st_ctime_ns, value.st_nlink)
    if identity(before) != identity(after) or (after.st_dev, after.st_ino) != (current.st_dev, current.st_ino):
        raise SystemExit('activation proof changed while held open')
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result: raise ValueError('duplicate proof key')
            result[key] = value
        return result
    data = json.loads(content.decode('utf-8'), object_pairs_hook=unique)
    keys = {'schema','releaseId','finalAcceptedHostIdentitySha256','finalAcceptedLifecycleSha256',
            'apiHead','apiTree','deployedJarSha256','status','authenticatedStt','authenticatedTts',
            'nginxRoutes','nginxDenyClosed','loopbackBinding','activationRecordSha256'}
    if not isinstance(data, dict) or set(data) != keys:
        raise SystemExit('activation proof has unexpected or missing fields')
    expected = {'schema':'cyf-jvc-oai-api-activation-proof-v1','releaseId':release_id,
                'apiHead':api_head,'apiTree':api_tree,'deployedJarSha256':jar_sha,
                'status':'ACTIVATED_HEALTHY','authenticatedStt':'PASS','authenticatedTts':'PASS',
                'nginxRoutes':'PASS','nginxDenyClosed':'PASS','loopbackBinding':'127.0.0.1'}
    for key, value in expected.items():
        if data.get(key) != value: raise SystemExit('activation proof mismatch for {}'.format(key))
    for key in ('finalAcceptedHostIdentitySha256','finalAcceptedLifecycleSha256','activationRecordSha256'):
        if not isinstance(data.get(key), str) or not re.fullmatch(r'[0-9a-f]{64}', data[key]):
            raise SystemExit('activation proof digest is invalid: {}'.format(key))
    for value in (digest.hexdigest(), data['finalAcceptedHostIdentitySha256'],
                  data['finalAcceptedLifecycleSha256'], data['activationRecordSha256']):
        sys.stdout.buffer.write(value.encode('ascii') + b'\0')
finally:
    if fd is not None: os.close(fd)
    os.close(rootfd)
PY
  )
  ((${#facts[@]} == 4)) || die "invalid or missing genuine API activation proof: $ACTIVATION_PROOF"
  ACTIVATION_PROOF_SHA="${facts[0]}"
  ACTIVATION_HOST_IDENTITY_SHA="${facts[1]}"
  ACTIVATION_LIFECYCLE_SHA="${facts[2]}"
  ACTIVATION_RECORD_SHA="${facts[3]}"
}

web_adapter_archive_operation() {
  local destination="${1:-}" mode='validate'
  [[ -z "$destination" ]] || mode='extract'
  if [[ "$mode" == extract ]]; then
    [[ -d "$destination" && ! -L "$destination" ]] || die "Web extraction root is unsafe: $destination"
    [[ -z "$(find "$destination" -mindepth 1 -print -quit)" ]] || die "Web extraction root is not empty"
  fi
  [[ "${CYF_WEB_DEPLOY_ADAPTER_FAULT:-}" != archive-read ]] || die "injected Web archive read failure"
  local mutation_window=0
  if web_adapter_fixture_mode && [[ "${CYF_WEB_DEPLOY_ADAPTER_FAULT:-}" == archive-mutation-window ]]; then mutation_window=1; fi
  python3 -B - "$WEB_ARTIFACT" "$WEB_ARCHIVE_SHA_EXPECTED" "$mode" "$destination" "$mutation_window" <<'PY'
import hashlib, os, posixpath, stat, sys, tarfile, time
archive, expected, mode, destination, mutation_window = sys.argv[1:]
fd = os.open(archive, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0))
try:
    before = os.fstat(fd)
    if mutation_window == '1': time.sleep(0.25)
    if (not stat.S_ISREG(before.st_mode) or stat.S_IMODE(before.st_mode) != 0o444
            or before.st_nlink != 1):
        raise SystemExit('Web archive must be immutable 0444 regular nlink1')
    digest = hashlib.sha256()
    while True:
        block = os.read(fd, 1024 * 1024)
        if not block: break
        digest.update(block)
    if digest.hexdigest() != expected:
        raise SystemExit('Web archive SHA-256 mismatch')
    os.lseek(fd, 0, os.SEEK_SET)
    seen = set(); entries = []; has_index = False
    with os.fdopen(os.dup(fd), 'rb') as held:
        with tarfile.open(fileobj=held, mode='r:gz') as bundle:
            for item in bundle:
                raw = item.name
                while raw.startswith('./'): raw = raw[2:]
                raw = raw.rstrip('/')
                if not raw: continue
                try: raw.encode('utf-8', 'strict')
                except UnicodeError: raise SystemExit('archive member is not UTF-8')
                parts = raw.split('/')
                normalized = posixpath.normpath(raw)
                if (raw.startswith('/') or any(part in ('','.','..') for part in parts)
                        or normalized in ('','.','..') or normalized.startswith('../')):
                    raise SystemExit('unsafe archive path: {}'.format(item.name))
                if normalized in seen:
                    raise SystemExit('duplicate normalized archive path: {}'.format(item.name))
                seen.add(normalized)
                if not (item.isdir() or item.isfile()):
                    raise SystemExit('unsupported archive entry type: {}'.format(item.name))
                entries.append((normalized, item.isdir(), item))
                if normalized == 'index.html' and item.isfile(): has_index = True
            if not has_index: raise SystemExit('Web archive has no root index.html')
            if mode == 'extract':
                for normalized, is_dir, item in entries:
                    target = os.path.join(destination, *normalized.split('/'))
                    if is_dir:
                        os.makedirs(target, mode=0o700, exist_ok=True)
                        continue
                    parent = os.path.dirname(target)
                    os.makedirs(parent, mode=0o700, exist_ok=True)
                    outfd = os.open(target, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o600)
                    source = bundle.extractfile(item)
                    if source is None: raise SystemExit('archive file payload is unavailable')
                    remaining = item.size
                    try:
                        while remaining:
                            block = source.read(min(1024 * 1024, remaining))
                            if not block: raise SystemExit('short archive file payload')
                            view = memoryview(block)
                            while view:
                                written = os.write(outfd, view); view = view[written:]
                            remaining -= len(block)
                        if source.read(1): raise SystemExit('oversized archive file payload')
                        os.fsync(outfd)
                    finally:
                        source.close(); os.close(outfd)
            else:
                for normalized, is_dir, item in entries:
                    if is_dir: continue
                    source = bundle.extractfile(item)
                    if source is None: raise SystemExit('archive file payload is unavailable')
                    remaining = item.size
                    try:
                        while remaining:
                            block = source.read(min(1024 * 1024, remaining))
                            if not block: raise SystemExit('short archive file payload')
                            remaining -= len(block)
                        if source.read(1): raise SystemExit('oversized archive file payload')
                    finally: source.close()
    after = os.fstat(fd)
    current = os.stat(archive, follow_symlinks=False)
    identity = lambda value: (value.st_dev, value.st_ino, value.st_size,
                              value.st_mtime_ns, value.st_ctime_ns, value.st_nlink)
    if identity(before) != identity(after) or (after.st_dev, after.st_ino) != (current.st_dev, current.st_ino):
        raise SystemExit('Web archive changed while held open')
    print(digest.hexdigest())
finally:
    os.close(fd)
PY
  [[ "${CYF_WEB_DEPLOY_ADAPTER_FAULT:-}" != extraction || "$mode" != extract ]] \
    || die "injected Web extraction failure"
}

web_adapter_write_guard() {
  local extracted_tree="$1"
  require_sha256 'extracted Web tree' "$extracted_tree"
  python3 -B - "$WEB_GUARD_ROOT" "$(basename -- "$WEB_GUARD")" "$RELEASE_ID" \
    "$RELEASE_INPUT_SHA" "$WEB_ADAPTER_TOOL_SHA" "$WEB_ARTIFACT" "$WEB_ARCHIVE_SHA_EXPECTED" \
    "$extracted_tree" "$WEB_HEAD" "$WEB_TREE" "$ACTIVATION_PROOF_SCHEMA" \
    "$ACTIVATION_PROOF_SHA" "$API_HEAD" "$API_TREE" "$API_DEPLOYED_JAR_SHA" \
    "$ACTIVATION_HOST_IDENTITY_SHA" "$ACTIVATION_LIFECYCLE_SHA" "$ACTIVATION_RECORD_SHA" <<'PY'
import hashlib, json, os, stat, sys
(root, name, release_id, input_sha, tool_sha, archive, archive_sha, tree_sha,
 web_head, web_tree, proof_schema, proof_sha, api_head, api_tree, jar_sha,
 host_sha, lifecycle_sha, activation_record_sha) = sys.argv[1:]
record = {'schema':'cyf-jvc-oai-web-deploy-guard-v1','releaseId':release_id,
          'status':'VERIFIED','verification':'PASS','deployment':'NOT_PERFORMED',
          'compileVoiceEnabled':True,'releaseInputSha256':input_sha,
          'adapterToolSha256':tool_sha,'archivePath':archive,'archiveSha256':archive_sha,
          'extractedTreeSha256':tree_sha,'webHead':web_head,'webTree':web_tree,
          'activationProofSchema':proof_schema,'activationProofSha256':proof_sha,
          'apiHead':api_head,'apiTree':api_tree,'apiDeployedJarSha256':jar_sha,
          'finalAcceptedHostIdentitySha256':host_sha,
          'finalAcceptedLifecycleSha256':lifecycle_sha,
          'activationRecordSha256':activation_record_sha}
content = (json.dumps(record, sort_keys=True, indent=2) + '\n').encode('utf-8')
digest = hashlib.sha256(content).hexdigest()
side_content = '{}  {}\n'.format(digest, name).encode('ascii')
rootfd = os.open(root, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0))
def publish(filename, payload):
    try:
        fd = os.open(filename, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o400, dir_fd=rootfd)
    except FileExistsError:
        fd = os.open(filename, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0), dir_fd=rootfd)
        try:
            info = os.fstat(fd)
            if (not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode) != 0o400
                    or info.st_nlink != 1 or os.read(fd, len(payload) + 1) != payload):
                raise SystemExit('immutable guard object already differs: {}'.format(filename))
        finally: os.close(fd)
        return
    try:
        view = memoryview(payload)
        while view:
            written = os.write(fd, view); view = view[written:]
        os.fchmod(fd, 0o400); os.fsync(fd)
    finally: os.close(fd)
try:
    publish(name, content); publish(name + '.sha256', side_content); os.fsync(rootfd)
finally: os.close(rootfd)
print(digest)
PY
}

web_adapter_verify_guard() {
  local require_external_proof="${1:-1}" current_tool
  local -a values=()
  current_tool="$(web_adapter_tool_sha256)"
  [[ "$current_tool" == "$WEB_ADAPTER_TOOL_SHA" ]] || die "Web adapter tool changed after input load"
  mapfile -d '' -t values < <(python3 -B - "$WEB_GUARD_ROOT" "$(basename -- "$WEB_GUARD")" \
    "$RELEASE_ID" "$RELEASE_INPUT_SHA" "$WEB_ADAPTER_TOOL_SHA" "$WEB_ARTIFACT" \
    "$WEB_ARCHIVE_SHA_EXPECTED" "$WEB_HEAD" "$WEB_TREE" "$ACTIVATION_PROOF_SCHEMA" \
    "$API_HEAD" "$API_TREE" "$API_DEPLOYED_JAR_SHA" <<'PY'
import hashlib, json, os, re, stat, sys
(root, name, release_id, input_sha, tool_sha, archive, archive_sha, web_head, web_tree,
 proof_schema, api_head, api_tree, jar_sha) = sys.argv[1:]
rootfd = os.open(root, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0))
def read_immutable(filename):
    fd = os.open(filename, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0), dir_fd=rootfd)
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or stat.S_IMODE(before.st_mode) != 0o400 or before.st_nlink != 1:
            raise SystemExit('unsafe immutable guard object: {}'.format(filename))
        content = bytearray()
        while True:
            block = os.read(fd, 1024 * 1024)
            if not block: break
            content.extend(block)
        after = os.fstat(fd); current = os.stat(filename, dir_fd=rootfd, follow_symlinks=False)
        if ((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns,before.st_nlink)
                != (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns,after.st_nlink)
                or (after.st_dev,after.st_ino) != (current.st_dev,current.st_ino)):
            raise SystemExit('guard object changed while held open')
        return bytes(content)
    finally: os.close(fd)
try:
    content = read_immutable(name); side = read_immutable(name + '.sha256')
finally: os.close(rootfd)
digest = hashlib.sha256(content).hexdigest()
if side != '{}  {}\n'.format(digest, name).encode('ascii'):
    raise SystemExit('Web guard sidecar mismatch')
def unique(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise ValueError('duplicate guard key')
        result[key]=value
    return result
data=json.loads(content.decode('utf-8'), object_pairs_hook=unique)
keys={'schema','releaseId','status','verification','deployment','compileVoiceEnabled',
      'releaseInputSha256','adapterToolSha256','archivePath','archiveSha256','extractedTreeSha256',
      'webHead','webTree','activationProofSchema','activationProofSha256','apiHead','apiTree',
      'apiDeployedJarSha256','finalAcceptedHostIdentitySha256','finalAcceptedLifecycleSha256',
      'activationRecordSha256'}
if not isinstance(data,dict) or set(data)!=keys: raise SystemExit('Web guard shape mismatch')
expected={'schema':'cyf-jvc-oai-web-deploy-guard-v1','releaseId':release_id,'status':'VERIFIED',
          'verification':'PASS','deployment':'NOT_PERFORMED','compileVoiceEnabled':True,
          'releaseInputSha256':input_sha,'adapterToolSha256':tool_sha,'archivePath':archive,
          'archiveSha256':archive_sha,'webHead':web_head,'webTree':web_tree,
          'activationProofSchema':proof_schema,'apiHead':api_head,'apiTree':api_tree,
          'apiDeployedJarSha256':jar_sha}
for key,value in expected.items():
    if data.get(key)!=value: raise SystemExit('Web guard mismatch for {}'.format(key))
for key in ('extractedTreeSha256','activationProofSha256','finalAcceptedHostIdentitySha256',
            'finalAcceptedLifecycleSha256','activationRecordSha256'):
    if not isinstance(data.get(key),str) or not re.fullmatch(r'[0-9a-f]{64}',data[key]):
        raise SystemExit('invalid Web guard digest: {}'.format(key))
for value in (digest,data['extractedTreeSha256'],data['activationProofSha256'],
              data['finalAcceptedHostIdentitySha256'],data['finalAcceptedLifecycleSha256'],
              data['activationRecordSha256']):
    sys.stdout.buffer.write(value.encode('ascii')+b'\0')
PY
  )
  ((${#values[@]} == 6)) || die "invalid or incomplete Web deployment guard: $WEB_GUARD"
  WEB_GUARD_SHA="${values[0]}"; WEB_EXTRACTED_TREE_SHA="${values[1]}"
  ACTIVATION_PROOF_SHA="${values[2]}"; ACTIVATION_HOST_IDENTITY_SHA="${values[3]}"
  ACTIVATION_LIFECYCLE_SHA="${values[4]}"; ACTIVATION_RECORD_SHA="${values[5]}"
  if [[ "$require_external_proof" == 1 ]]; then
    local expected_proof="$ACTIVATION_PROOF_SHA" expected_host="$ACTIVATION_HOST_IDENTITY_SHA"
    local expected_lifecycle="$ACTIVATION_LIFECYCLE_SHA" expected_record="$ACTIVATION_RECORD_SHA"
    web_adapter_validate_activation_proof
    [[ "$ACTIVATION_PROOF_SHA" == "$expected_proof" \
       && "$ACTIVATION_HOST_IDENTITY_SHA" == "$expected_host" \
       && "$ACTIVATION_LIFECYCLE_SHA" == "$expected_lifecycle" \
       && "$ACTIVATION_RECORD_SHA" == "$expected_record" ]] \
      || die "external API activation proof no longer matches the immutable Web guard"
  fi
}

web_adapter_require_execute_approval() {
  require_execute_approval
  (( EXECUTE == 1 )) || return 0
  [[ "${CYF_RELEASE_APPROVED_WEB_ARTIFACT_SHA256:-}" == "$WEB_ARCHIVE_SHA_EXPECTED" ]] \
    || die "approved Web artifact SHA-256 mismatch"
  [[ "${CYF_RELEASE_APPROVED_WEB_GUARD_SHA256:-}" == "$WEB_GUARD_SHA" ]] \
    || die "approved Web guard SHA-256 mismatch"
  [[ "${CYF_RELEASE_APPROVED_API_ACTIVATION_PROOF_SHA256:-}" == "$ACTIVATION_PROOF_SHA" ]] \
    || die "approved API activation proof SHA-256 mismatch"
  web_adapter_fixture_mode || (( EUID == 0 )) || die "Web deployment execution requires root"
}

web_adapter_health() {
  local live_dir="$1" timeout="$2"; shift 2
  if web_adapter_fixture_mode; then
    [[ -z "${CYF_WEB_DEPLOY_ADAPTER_FAULT:-}" || "${CYF_WEB_DEPLOY_ADAPTER_FAULT:-}" != health ]] || return 1
    [[ -d "$live_dir" && ! -L "$live_dir" && -f "$live_dir/index.html" && ! -e "$live_dir/.health-fail" ]] || return 1
    local entry
    entry="$(grep -oE '/static/index-[A-Za-z0-9_-]+\.js' "$live_dir/index.html" | head -1)"
    [[ -n "$entry" ]] || return 1
    printf '%s\n' "$entry"
    return 0
  fi
  verify_web_health "$live_dir" "$timeout" "$@"
}

web_adapter_move() {
  local operation="$1" source="$2" destination="$3"
  if web_adapter_fixture_mode && [[ "${CYF_WEB_DEPLOY_ADAPTER_FAULT:-}" == "$operation" ]]; then
    return 91
  fi
  mv -T -- "$source" "$destination"
}

web_adapter_maybe_fault() {
  local point="$1"
  if web_adapter_fixture_mode && [[ "${CYF_WEB_DEPLOY_ADAPTER_FAULT:-}" == "$point" ]]; then
    die "injected Web adapter fault: $point"
  fi
}

web_adapter_read_deploy_record() {
  local deploy_record="$1"
  python3 -B - "$deploy_record" "$RELEASE_ID" "$RELEASE_INPUT_SHA" "$WEB_ADAPTER_TOOL_SHA" \
    "$WEB_ARCHIVE_SHA_EXPECTED" "$WEB_GUARD" "$WEB_GUARD_SHA" "$ACTIVATION_PROOF_SHA" \
    "$API_HEAD" "$API_TREE" "$WEB_HEAD" "$WEB_TREE" <<'PY'
import json,os,re,stat,sys
(path,release_id,input_sha,tool_sha,archive_sha,guard,guard_sha,proof_sha,
 api_head,api_tree,web_head,web_tree)=sys.argv[1:]
fd=os.open(path,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0))
try:
    before=os.fstat(fd)
    if not stat.S_ISREG(before.st_mode) or stat.S_IMODE(before.st_mode)!=0o400 or before.st_nlink!=1:
        raise SystemExit('deploy record is not immutable regular nlink1')
    content=bytearray()
    while True:
        block=os.read(fd,1024*1024)
        if not block: break
        content.extend(block)
    after=os.fstat(fd); current=os.stat(path,follow_symlinks=False)
    if ((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns,before.st_nlink)
            != (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns,after.st_nlink)
            or (after.st_dev,after.st_ino)!=(current.st_dev,current.st_ino)):
        raise SystemExit('deploy record changed while held open')
finally: os.close(fd)
def unique(pairs):
    result={}
    for key,value in pairs:
        if key in result: raise ValueError('duplicate deploy record key')
        result[key]=value
    return result
data=json.loads(content.decode('utf-8'),object_pairs_hook=unique)
expected={'schema':'cyf-web-deploy-record-v2','status':'DEPLOYED_HEALTHY','releaseId':release_id,
          'releaseInputSha256':input_sha,'adapterToolSha256':tool_sha,'artifactSha256':archive_sha,
          'webGuard':guard,'webGuardSha256':guard_sha,'activationProofSha256':proof_sha,
          'apiHead':api_head,'apiTree':api_tree,'webHead':web_head,'webTree':web_tree,
          'databaseOperation':'NOT_PERFORMED','rabbitMqOperation':'NOT_PERFORMED',
          'apiActivationOperation':'NOT_PERFORMED'}
for key,value in expected.items():
    if data.get(key)!=value: raise SystemExit('deploy record binding mismatch for {}'.format(key))
for key in ('candidateTreeSha256','previousLiveTreeSha256'):
    if not isinstance(data.get(key),str) or not re.fullmatch(r'[0-9a-f]{64}',data[key]):
        raise SystemExit('deploy record tree digest is invalid')
for key in ('backupDir','liveDir','changeId'):
    value=data.get(key)
    if not isinstance(value,str) or not value or any(ord(ch)<32 or ord(ch)==127 for ch in value):
        raise SystemExit('invalid deploy record scalar: {}'.format(key))
for value in (data['backupDir'],data['liveDir'],data['candidateTreeSha256'],
              data['previousLiveTreeSha256'],data['artifactSha256'],data['changeId']):
    sys.stdout.buffer.write(value.encode('utf-8')+b'\0')
PY
}

web_adapter_publish_immutable_with_sidecar() {
  local source="$1" destination="$2"
  web_adapter_maybe_fault record-write
  python3 -B - "$source" "$destination" <<'PY'
import hashlib, os, stat, sys
source, destination = sys.argv[1:]
parent = os.path.dirname(destination)
if os.path.dirname(source) != parent:
    raise SystemExit('record staging and destination must share one directory')
rootfd = os.open(parent, os.O_RDONLY | getattr(os, 'O_DIRECTORY', 0) | getattr(os, 'O_NOFOLLOW', 0))
sname, dname = os.path.basename(source), os.path.basename(destination)
fd = os.open(sname, os.O_RDWR | getattr(os, 'O_NOFOLLOW', 0), dir_fd=rootfd)
try:
    info = os.fstat(fd)
    if not stat.S_ISREG(info.st_mode) or info.st_nlink != 1:
        raise SystemExit('record staging file is unsafe')
    digest = hashlib.sha256()
    while True:
        block = os.read(fd, 1024 * 1024)
        if not block: break
        digest.update(block)
    os.fchmod(fd, 0o400); os.fsync(fd)
finally: os.close(fd)
side_name = dname + '.sha256'
side_content = '{}  {}\n'.format(digest.hexdigest(), dname).encode('ascii')
try:
    sidefd = os.open(side_name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0), 0o400, dir_fd=rootfd)
except FileExistsError:
    sidefd = os.open(side_name, os.O_RDONLY | getattr(os, 'O_NOFOLLOW', 0), dir_fd=rootfd)
    try:
        sinfo = os.fstat(sidefd)
        if (not stat.S_ISREG(sinfo.st_mode) or stat.S_IMODE(sinfo.st_mode) != 0o400
                or sinfo.st_nlink != 1 or os.read(sidefd, len(side_content) + 1) != side_content):
            raise SystemExit('existing record sidecar is unsafe or mismatched')
    finally: os.close(sidefd)
else:
    try:
        view=memoryview(side_content)
        while view:
            written=os.write(sidefd,view); view=view[written:]
        os.fchmod(sidefd,0o400); os.fsync(sidefd)
    finally: os.close(sidefd)
if os.path.lexists(destination):
    raise SystemExit('immutable record destination already exists')
os.link(sname, dname, src_dir_fd=rootfd, dst_dir_fd=rootfd, follow_symlinks=False)
os.unlink(sname, dir_fd=rootfd)
os.fsync(rootfd); os.close(rootfd)
print(digest.hexdigest())
PY
}

web_adapter_verify_immutable_with_sidecar() {
  local path="$1"
  python3 -B - "$path" <<'PY'
import hashlib, os, stat, sys
path=sys.argv[1]; parent=os.path.dirname(path); name=os.path.basename(path)
rootfd=os.open(parent,os.O_RDONLY|getattr(os,'O_DIRECTORY',0)|getattr(os,'O_NOFOLLOW',0))
def read(name):
    fd=os.open(name,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0),dir_fd=rootfd)
    try:
        before=os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or stat.S_IMODE(before.st_mode)!=0o400 or before.st_nlink!=1:
            raise SystemExit('immutable record object is unsafe')
        content=bytearray()
        while True:
            block=os.read(fd,1024*1024)
            if not block: break
            content.extend(block)
        after=os.fstat(fd); current=os.stat(name,dir_fd=rootfd,follow_symlinks=False)
        if ((before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns,before.st_ctime_ns,before.st_nlink)
                != (after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns,after.st_ctime_ns,after.st_nlink)
                or (after.st_dev,after.st_ino)!=(current.st_dev,current.st_ino)):
            raise SystemExit('immutable record changed while held open')
        return bytes(content)
    finally: os.close(fd)
try:
    content=read(name); side=read(name+'.sha256')
finally: os.close(rootfd)
digest=hashlib.sha256(content).hexdigest()
if side!='{}  {}\n'.format(digest,name).encode('ascii'):
    raise SystemExit('immutable record sidecar mismatch')
print(digest)
PY
}

web_adapter_acquire_execution_lock() {
  (( EXECUTE == 1 )) || return 0
  if ! web_adapter_fixture_mode; then
    acquire_execution_lock web
    return 0
  fi
  local lock_path="$CYF_WEB_DEPLOY_ADAPTER_TEST_ROOT/controller/web-execution.lock"
  mkdir -p -- "$(dirname -- "$lock_path")"
  if [[ ! -e "$lock_path" ]]; then
    (umask 077; : > "$lock_path")
  fi
  [[ -f "$lock_path" && ! -L "$lock_path" && "$(stat -Lc '%a:%u:%h' -- "$lock_path")" == "600:$(id -u):1" ]] \
    || die "fixture Web execution lock is unsafe"
  exec {CYF_RELEASE_EXECUTION_LOCK_FD}>"$lock_path"
  flock -n "$CYF_RELEASE_EXECUTION_LOCK_FD" || die "another fixture Web operation holds the execution lock"
  log "exclusive fixture Web execution lock acquired: $lock_path"
}
