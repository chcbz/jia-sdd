set -eu
export CYF_EXPERIMENT="$(mktemp -d /tmp/cyf-backend-flow-ci.XXXXXX)"
printf 'CYF_FLOW_PHASE runtime.begin wall=%s monotonic=' "$(date -u +%FT%TZ)"; cut -d' ' -f1 /proc/uptime
python3 - <<'CYFTOOLS'
import io,base64,gzip,hashlib,json,os,pathlib
raw=base64.b64decode('@CYF_TOOL_BUNDLE_BASE64@',validate=True)
assert hashlib.sha256(raw).hexdigest()=='@CYF_TOOL_BUNDLE_SHA256@', 'tool bundle hash mismatch'
root=pathlib.Path(os.environ['CYF_EXPERIMENT'])
for name,text in json.loads(gzip.decompress(raw).decode()).items():
 p=root/name
 p.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
 p.write_text(text)
 p.chmod(0o600)
CYFTOOLS
python3 "$CYF_EXPERIMENT/prepare-backend-jdk.py" --cache "$HOME/.cache/cyf-backend-jdk-archives" --destination "$CYF_EXPERIMENT/jdk" > "$CYF_EXPERIMENT/jdk-result.txt"
cat "$CYF_EXPERIMENT/jdk-result.txt"
export JAVA_HOME="$(tail -1 "$CYF_EXPERIMENT/jdk-result.txt")"
export PATH="$JAVA_HOME/bin:$PATH"
java -version
printf 'CYF_FLOW_PHASE runtime.end wall=%s monotonic=' "$(date -u +%FT%TZ)"; cut -d' ' -f1 /proc/uptime

export CYF_REVIEW_MYSQL_ARCHIVE_SHA=e6503f2ca665dbd4524a0109fa15969453f02b69c20f42d3fe8ba0d0b0ca1a1f
mysql_cache="$HOME/.cache/cyf-backend-mysql-archives"
mkdir -p "$mysql_cache"
mysql_archive="$mysql_cache/mysql-$CYF_REVIEW_MYSQL_ARCHIVE_SHA.tar.xz"
if [ ! -e "$mysql_archive" ]; then
  mysql_temporary="$(mktemp "$mysql_cache/.download.XXXXXX")"
  curl --fail --silent --show-error --location --proto '=https' --proto-redir '=https' 'https://cdn.mysql.com/archives/mysql-8.0/mysql-8.0.21-linux-glibc2.17-x86_64-minimal.tar.xz' -o "$mysql_temporary"
  printf '%s  %s\n' "$CYF_REVIEW_MYSQL_ARCHIVE_SHA" "$mysql_temporary" | sha256sum -c -
  mv "$mysql_temporary" "$mysql_archive"
fi
printf '%s  %s\n' "$CYF_REVIEW_MYSQL_ARCHIVE_SHA" "$mysql_archive" | sha256sum -c -
mkdir "$CYF_EXPERIMENT/mysql-runtime"
tar -xJf "$mysql_archive" -C "$CYF_EXPERIMENT/mysql-runtime" --strip-components=1
export CYF_REVIEW_MYSQLD="$CYF_EXPERIMENT/mysql-runtime/bin/mysqld"
libaio_archive="$mysql_cache/libaio-d1476e4beab3d85f8a7d31de94c27472711ed3ef399ce70708e24b259426125b.deb"
if [ ! -e "$libaio_archive" ]; then
  libaio_temporary="$(mktemp "$mysql_cache/.libaio.XXXXXX")"
  curl --fail --silent --show-error --location --proto '=https' --proto-redir '=https' 'https://deb.debian.org/debian/pool/main/liba/libaio/libaio1_0.3.113-4_amd64.deb' -o "$libaio_temporary"
  printf '%s  %s\n' d1476e4beab3d85f8a7d31de94c27472711ed3ef399ce70708e24b259426125b "$libaio_temporary" | sha256sum -c -
  mv "$libaio_temporary" "$libaio_archive"
fi
printf '%s  %s\n' d1476e4beab3d85f8a7d31de94c27472711ed3ef399ce70708e24b259426125b "$libaio_archive" | sha256sum -c -
export CYF_REVIEW_LIBAIO_ARCHIVE="$libaio_archive"
python3 - <<'LIBAIO'
import io,os,pathlib,tarfile
raw=pathlib.Path(os.environ['CYF_REVIEW_LIBAIO_ARCHIVE']).read_bytes()
assert raw[:8]==b'!<arch>\n'
offset=8;found=[]
while offset<len(raw):
 header=raw[offset:offset+60];assert len(header)==60 and header[58:60]==b'`\n'
 size=int(header[48:58]);name=header[:16].decode().strip().rstrip('/')
 payload=raw[offset+60:offset+60+size];assert len(payload)==size
 if name=='data.tar.xz':found.append(payload)
 offset+=60+size+(size%2)
assert len(found)==1
with tarfile.open(fileobj=io.BytesIO(found[0]),mode='r:xz') as archive:
 data=archive.extractfile('./usr/lib/x86_64-linux-gnu/libaio.so.1.0.2').read()
destination=pathlib.Path(os.environ['CYF_EXPERIMENT'])/'mysql-libs'
destination.mkdir(mode=0o700)
(destination/'libaio.so.1').write_bytes(data)
LIBAIO
libnuma_archive="$mysql_cache/libnuma-ab2277a2af54056f7c2b01f98c0ac9ea546753a35de00e74285b7a0f667ea7e7.deb"
if [ ! -e "$libnuma_archive" ]; then
  libnuma_temporary="$(mktemp "$mysql_cache/.libnuma.XXXXXX")"
  curl --fail --silent --show-error --location --proto '=https' --proto-redir '=https' 'https://archive.debian.org/debian/pool/main/n/numactl/libnuma1_2.0.12-1_amd64.deb' -o "$libnuma_temporary"
  printf '%s  %s\n' ab2277a2af54056f7c2b01f98c0ac9ea546753a35de00e74285b7a0f667ea7e7 "$libnuma_temporary" | sha256sum -c -
  mv "$libnuma_temporary" "$libnuma_archive"
fi
printf '%s  %s\n' ab2277a2af54056f7c2b01f98c0ac9ea546753a35de00e74285b7a0f667ea7e7 "$libnuma_archive" | sha256sum -c -
export CYF_REVIEW_LIBNUMA_ARCHIVE="$libnuma_archive"
python3 - <<'LIBNUMA'
import io,os,pathlib,tarfile
raw=pathlib.Path(os.environ['CYF_REVIEW_LIBNUMA_ARCHIVE']).read_bytes()
assert raw[:8]==b'!<arch>\n'
offset=8;found=[]
while offset<len(raw):
 header=raw[offset:offset+60];assert len(header)==60 and header[58:60]==b'`\n'
 size=int(header[48:58]);name=header[:16].decode().strip().rstrip('/')
 payload=raw[offset+60:offset+60+size];assert len(payload)==size
 if name=='data.tar.xz':found.append(payload)
 offset+=60+size+(size%2)
assert len(found)==1
with tarfile.open(fileobj=io.BytesIO(found[0]),mode='r:xz') as archive:
 data=archive.extractfile('./usr/lib/x86_64-linux-gnu/libnuma.so.1.0.0').read()
destination=pathlib.Path(os.environ['CYF_EXPERIMENT'])/'mysql-libs'
destination.mkdir(mode=0o700,exist_ok=True)
(destination/'libnuma.so.1').write_bytes(data)
LIBNUMA
export LD_LIBRARY_PATH="$CYF_EXPERIMENT/mysql-libs${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

ldd "$CYF_REVIEW_MYSQLD" > "$CYF_EXPERIMENT/mysql-ldd.txt"
cat "$CYF_EXPERIMENT/mysql-ldd.txt"
if grep -q 'not found' "$CYF_EXPERIMENT/mysql-ldd.txt"; then echo 'MySQL runtime dependency missing' >&2; exit 1; fi

"$CYF_REVIEW_MYSQLD" --no-defaults --version

export CYF_FLOW_COMPILE_CACHE_OPT_IN=1
export CYF_FLOW_SHORT_LIVED_TEST_JVM=1
case "${CI_COMMIT_REF_NAME:-}" in develop|codex/v1-6-voice-api-readiness-20260917|codex/mmd-unified-materials-api-20261003) ;; *) echo 'unexpected CI branch' >&2; exit 1 ;; esac
test -n "${CI_COMMIT_SHA:-}"
test "$(git rev-parse HEAD)" = "$CI_COMMIT_SHA"
export CYF_FLOW_GRADLE_ACTIVE=1
export CYF_FLOW_BUILD_ROOT="$CYF_EXPERIMENT/build"
test ! -e "$CYF_FLOW_BUILD_ROOT"
mkdir -p "$CYF_FLOW_BUILD_ROOT"
git diff --exit-code HEAD --
export CYF_SOURCE_CLEAN_BEFORE=1
# Preserve complete compiler diagnostics and per-task timing.
cat > "$CYF_EXPERIMENT/owner-fixture-diagnostics.gradle" <<'OWNERDIAGNOSTICS'
allprojects {
    tasks.withType(org.gradle.api.tasks.compile.JavaCompile).configureEach {
        options.compilerArgs += ['-Xmaxerrs', '1000']
    }
}
def cyfTaskStarts = new java.util.concurrent.ConcurrentHashMap()
gradle.taskGraph.beforeTask { task -> cyfTaskStarts[task.path] = System.nanoTime() }
gradle.taskGraph.afterTask { task, state ->
    def started = cyfTaskStarts.remove(task.path)
    if (started != null) {
        println('CYF_TASK_TIMING ' + groovy.json.JsonOutput.toJson([
            task: task.path, seconds: (System.nanoTime() - started) / 1000000000.0,
            skipped: state.skipped, skipMessage: state.skipMessage, failed: state.failure != null]))
    }
}

OWNERDIAGNOSTICS
set +e
printf 'CYF_FLOW_PHASE gradle.begin wall=%s monotonic=' "$(date -u +%FT%TZ)"; cut -d' ' -f1 /proc/uptime
python3 - > "$CYF_FLOW_BUILD_ROOT/gradle-output.log" 2>&1 <<'CYFGRADLE'
import hashlib,json,os,pathlib,subprocess,sys
root=pathlib.Path(os.environ['CYF_EXPERIMENT'])
raw=(root/'ops/ci/aliyun-flow/backend-ci-policy.json').read_bytes()
policy=json.loads(raw)
for name in ('build.gradle', 'settings.gradle'):
    path=pathlib.Path(name)
    print('CYF_BUILD_INPUT '+name+' '+hashlib.sha256(path.read_bytes()).hexdigest(),flush=True)
argv=[value.replace('$CYF_EXPERIMENT',str(root)).replace(
    '$CYF_FLOW_BUILD_ROOT',os.environ['CYF_FLOW_BUILD_ROOT']) for value in policy['argv']]
tree=subprocess.check_output(['git','rev-parse','HEAD^{tree}'],text=True).strip()
sys.exit(subprocess.run([sys.executable,str(root/'ops/orchestration/cyf_orchestrator.py'),
    'gradle','--flow-ci','--cwd',str(pathlib.Path.cwd()),'--tree-sha',tree,
    '--selector',policy['selector'],'--fixture-digest',hashlib.sha256(raw).hexdigest(),
    'FLOW-CI-5260799','--']+argv,check=False).returncode)
CYFGRADLE
gradle_rc=$?
printf 'CYF_FLOW_PHASE gradle.end wall=%s monotonic=' "$(date -u +%FT%TZ)"; cut -d' ' -f1 /proc/uptime
set -e
cat "$CYF_FLOW_BUILD_ROOT/gradle-output.log"
python3 - <<'PYDIAGNOSTICS'
import base64, gzip, hashlib, json, os, re, xml.etree.ElementTree as ET
from pathlib import Path
root = Path(os.environ['CYF_FLOW_BUILD_ROOT'])
lines = (root / 'gradle-output.log').read_text(errors='replace').splitlines()
errors = []
current = None
for line in lines:
    if re.search(r'\.java:\d+: (?:error:|错误:)', line):
        current = {'diagnostic': line, 'details': []}
        errors.append(current)
    elif current is not None and re.match(r'\s*(?:required:|found:|reason:|symbol:|location:|需要:|找到:|原因:|符号:|位置:)', line):
        current['details'].append(line.strip())
def safe_failure_text(value):
    value = value or ''
    for name, secret in os.environ.items():
        if len(secret) >= 8 and re.search(r'(?i)secret|token|password|credential|access.?key', name):
            value = value.replace(secret, '[REDACTED]')
    value = re.sub(r'(?i)(authorization|api[_-]?key|password|secret|token)\s*[:=]\s*[^\s,;]+', r'\1=[REDACTED]', value)
    value = re.sub(r'https?://[^\s<>]+', '[URL]', value)
    return value[:3000]
reports = []
for path in sorted(root.rglob('TEST-*.xml')):
    suite = ET.parse(str(path)).getroot()
    failures = []
    for case in suite.findall('testcase'):
        for failure in list(case.findall('failure')) + list(case.findall('error')):
            failures.append({'class': case.get('classname'), 'test': case.get('name'), 'type': failure.get('type'), 'message': safe_failure_text(failure.get('message')), 'projectFrames': [line.strip() for line in (failure.text or '').splitlines() if re.match(r'\s*at (?:app//)?cn\.jia\.[\w.$]+\([^)]*\)', line)][:16]})
    reports.append({'path': str(path.relative_to(root)), 'name': suite.get('name'),
        'counts': {k: int(suite.get(k, 0)) for k in ('tests', 'failures', 'errors', 'skipped')}, 'failures': failures})
data = json.dumps({'commit': os.environ.get('CI_COMMIT_SHA'), 'run': os.environ.get('BUILD_NUMBER'),
    'compilerDiagnostics': errors, 'junitReports': reports}, separators=(',', ':'), ensure_ascii=False).encode()
compressed = base64.b64encode(gzip.compress(data)).decode()
print('CYF_DIAGNOSTIC_SUMMARY ' + json.dumps({'compilerErrors': len(errors), 'junitSuites': len(reports),
    'sha256': hashlib.sha256(data).hexdigest(), 'encoding': 'gzip+base64', 'base64Bytes': len(compressed)}))
for index in range(0, len(compressed), 3000):
    print('CYF_DIAGNOSTIC_CHUNK %d %s' % (index // 3000, compressed[index:index + 3000]))
PYDIAGNOSTICS
if [ "$gradle_rc" -ne 0 ]; then exit "$gradle_rc"; fi
python3 - <<'PYARTIFACT'
#!/usr/bin/env python3
"""Package this successful Flow build for the existing transactional installer.

Call only after the required Gradle command exits zero. ticket_sha256 is a
legacy wire-field for a deterministic run identity, not an approval ticket.
"""
import hashlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import zipfile


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


REQUIRED_MAIL_RUNTIME_CLASSES = frozenset((
    'javax/mail/MessagingException.class',
    'javax/mail/Session.class',
    'javax/mail/Transport.class',
    'com/sun/mail/smtp/SMTPTransport.class',
    'javax/activation/DataHandler.class',
))


def verify_mail_runtime(jar):
    """Check the shipped bootJar, not the broader Gradle test classpath."""
    missing = set(REQUIRED_MAIL_RUNTIME_CLASSES)
    try:
        with zipfile.ZipFile(str(jar)) as boot:
            for member in boot.infolist():
                if not member.filename.startswith('BOOT-INF/lib/') or not member.filename.endswith('.jar'):
                    continue
                with zipfile.ZipFile(io.BytesIO(boot.read(member))) as dependency:
                    missing.difference_update(dependency.namelist())
                if not missing:
                    break
    except (OSError, zipfile.BadZipFile, RuntimeError) as exc:
        raise SystemExit('invalid bootJar runtime archive: ' + type(exc).__name__)
    if missing:
        raise SystemExit('bootJar missing required mail runtime classes: ' + ', '.join(sorted(missing)))
    return sorted(REQUIRED_MAIL_RUNTIME_CLASSES)


def main():
    root = Path.cwd()
    env = os.environ
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD']).decode().strip()
    tree = subprocess.check_output(['git', 'rev-parse', 'HEAD^{tree}']).decode().strip()
    if (env.get('PIPELINE_ID') != '5260799' or env.get('CI_COMMIT_REF_NAME') not in ('develop', 'codex/v1-6-voice-api-readiness-20260917', 'codex/mmd-unified-materials-api-20261003')
            or commit != env.get('CI_COMMIT_SHA') or not re.fullmatch('[0-9a-f]{40,64}', commit)
            or not re.fullmatch('[1-9][0-9]*', env.get('BUILD_NUMBER', ''))):
        raise SystemExit('unexpected Flow source/run identity')
    # Both checks are enforced in the shell, before and after Gradle; repeat the
    # latter here. Untracked build outputs are not part of the tracked source.
    if env.get('CYF_SOURCE_CLEAN_BEFORE') != '1':
        raise SystemExit('missing successful pre-build source check')
    subprocess.check_call(['git', 'diff', '--exit-code', 'HEAD', '--'])
    build = Path(env['CYF_FLOW_BUILD_ROOT'])
    jars = [p for p in (build / 'jia/starter/libs').glob('*.jar') if not p.name.endswith('-plain.jar')]
    provenance = build / 'opencv-resolved.json'
    if len(jars) != 1 or any(p.is_symlink() or not p.is_file() for p in jars + [provenance]):
        raise SystemExit('expected one bootJar and OpenCV provenance')
    prov = json.loads(provenance.read_text())
    if (prov.get('jar_sha256') != '323d40119548134b0966d3735e97a78d1edbc79bd91e7fb1074e5152392095f4'
            or prov.get('jar_size') != 722802):
        raise SystemExit('unexpected private OpenCV artifact')
    mail_runtime = verify_mail_runtime(jars[0])
    print('CYF_BOOTJAR_MAIL_RUNTIME ' + json.dumps(mail_runtime))
    out = root / '_cyf_api_flow_export'
    out.mkdir(mode=0o700)  # fail rather than reuse stale output
    flow = dict(organization_id='5fb7d76ee6f9d07f148529c7', pipeline_id='5260799',
                job_id='cloud_ci.api_ci', run_id=env['BUILD_NUMBER'], source_tip_sha=commit)
    source = dict(branch=env.get('CI_COMMIT_REF_NAME'), commit_sha=commit, tree_sha=tree, clean_before=True, clean_after=True)
    records = []
    for kind, src, name in [('application_jar', jars[0], 'application.jar'),
                             ('dependency_provenance', provenance, 'dependency.provenance.json')]:
        target = out / name
        shutil.copyfile(str(src), str(target))
        records.append(dict(kind=kind, path=name, sha256=digest(target), size=target.stat().st_size))
    identity = hashlib.sha256(canonical(dict(flow=flow, source=source))).hexdigest()
    receipt = dict(schema_version=1, status='success', gradle_exit_code=0, bridge_exit_code=0,
                   ticket_sha256=identity, flow=flow, source=source, files=records)
    data = canonical(receipt)
    (out / 'receipt.json').write_bytes(data)
    receipt_sha = hashlib.sha256(data).hexdigest()
    (out / 'application.metadata.json').write_bytes(canonical(dict(
        schema_version=1, receipt_sha256=receipt_sha, flow=flow, source=source,
        application_jar=records[0], dependency_provenance=records[1])))
    (out / 'application.sidecar.json').write_bytes(canonical(dict(
        schema_version=1, receipt_sha256=receipt_sha, flow=flow,
        sha256=records[0]['sha256'], size=records[0]['size'])))
    print('CYF_API_ARTIFACT ' + json.dumps(dict(flow=flow, source=source,
          jar_sha256=records[0]['sha256'], receipt_sha256=receipt_sha), sort_keys=True))


if __name__ == '__main__':
    main()
PYARTIFACT
python3 - <<'PYTESTREPORT'
import json, os, shutil, xml.etree.ElementTree as ET
from pathlib import Path
root = Path(os.environ['CYF_FLOW_BUILD_ROOT'])
dest = Path('_cyf_api_flow_export/test-results')
records = []
for xml in sorted(root.rglob('TEST-*.xml')):
    suite = ET.parse(str(xml)).getroot()
    relative = xml.relative_to(root)
    target = dest / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(str(xml), str(target))
    records.append(dict(path=str(relative), name=suite.attrib.get('name'), **{
        k:int(suite.attrib.get(k,0)) for k in ('tests','failures','errors','skipped')}))
if not records:
    raise RuntimeError('No actual JUnit reports')
counts = {k:sum(r[k] for r in records) for k in ('tests','failures','errors','skipped')}
if counts['failures'] or counts['errors']:
    raise RuntimeError('Actual failing JUnit report')
summary = dict(pipeline=os.environ.get('PIPELINE_ID'), run=os.environ.get('BUILD_NUMBER'),
    commit=os.environ.get('CI_COMMIT_SHA'), counts=counts, suites=records,
    countNote='Test executions; source sets can overlap. Skips remain explicit.')
(dest / 'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print('CYF_API_TEST_SUMMARY '+json.dumps(dict(counts=counts,suites=len(records))))
PYTESTREPORT
printf 'CYF_FLOW_PHASE package.end wall=%s monotonic=' "$(date -u +%FT%TZ)"; cut -d' ' -f1 /proc/uptime
