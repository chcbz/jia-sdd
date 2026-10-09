#!/usr/bin/env python3
"""Root artifact admission and read-only revalidation; no build/install/service control.

A protected independent controller observation authenticates the batch decision.
Producer JSON/logs/checksums alone are consistency, NOT execution authentication.
No offline trust bypass exists. Private synthetic units are not release evidence.
"""
import argparse
import ctypes
import errno
import hashlib
import io
import json
import os
from pathlib import Path
import re
import secrets
import stat
import tarfile
import xml.etree.ElementTree as ET
import zipfile

MEMBERS = ('application.jar', 'application.metadata.json', 'application.sidecar.json',
           'dependency.provenance.json', 'receipt.json')
MAIL_CLASSES = frozenset(('javax/mail/MessagingException.class', 'javax/mail/Session.class',
    'javax/mail/Transport.class', 'com/sun/mail/smtp/SMTPTransport.class', 'javax/activation/DataHandler.class'))
OPENCV_SHA = '323d40119548134b0966d3735e97a78d1edbc79bd91e7fb1074e5152392095f4'
OPENCV_SIZE = 722802
AUTHORITY_ID = 'cyf-local-release-controller-v1'
SCOPE = 'artifact-admission-only'
SAFE_CODES = frozenset(('INPUT_INVALID', 'ROOT_REQUIRED', 'PATH_UNSAFE', 'AUTHORITY_INVALID',
    'IDENTITY_MISMATCH', 'DIGEST_MISMATCH', 'EVIDENCE_INVALID', 'PACKAGE_INVALID', 'JAR_INVALID',
    'MAIL_RUNTIME_INVALID', 'PROVENANCE_INVALID', 'OUTPUT_EXISTS', 'IO_FAILURE'))
META_KEYS = ('CYF-Release-Version', 'CYF-Source-Commit', 'CYF-Source-Tree', 'CYF-Local-Build-Id')
OBSERVATIONS = {'sourceCleanBefore': True, 'sourceCleanAfter': True, 'gradleExitCode': 0,
                'freshBootJar': True, 'validateLayering': True, 'publicArtifactVerifier': True}


class Rejected(Exception):
    def __init__(self, code):
        assert code in SAFE_CODES
        self.code = code
        super().__init__(code)


def need(ok, code='EVIDENCE_INVALID'):
    if not ok:
        raise Rejected(code)


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False) + '\n').encode()


def sha(data):
    return hashlib.sha256(data).hexdigest()


def exact(obj, keys, code='EVIDENCE_INVALID'):
    need(type(obj) is dict and set(obj) == set(keys), code)
    return obj


def strict_json(data, code='EVIDENCE_INVALID'):
    def pairs(items):
        out = {}
        for key, value in items:
            need(key not in out, code)
            out[key] = value
        return out
    try:
        return json.loads(data, object_pairs_hook=pairs,
            # Frozen schemas have no floating-point fields. Reject exponent
            # overflow as well as NaN/Infinity, and avoid float == int confusion.
            parse_float=lambda unused: (_ for _ in ()).throw(Rejected(code)),
            parse_constant=lambda unused: (_ for _ in ()).throw(Rejected(code)))
    except (ValueError, UnicodeError, RecursionError):
        raise Rejected(code) from None


def token(value, code='INPUT_INVALID'):
    need(type(value) is str and re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', value), code)
    return value


def hex_value(value, length=64, code='INPUT_INVALID'):
    need(type(value) is str and re.fullmatch('[0-9a-f]{%d}' % length, value), code)
    return value


def identity(obj):
    exact(obj, ('version', 'buildId', 'commit', 'tree'), 'IDENTITY_MISMATCH')
    token(obj['version'], 'IDENTITY_MISMATCH')
    token(obj['buildId'], 'IDENTITY_MISMATCH')
    hex_value(obj['commit'], 40, 'IDENTITY_MISMATCH')
    hex_value(obj['tree'], 40, 'IDENTITY_MISMATCH')
    return obj


def digest(obj, code='DIGEST_MISMATCH'):
    exact(obj, ('sha256', 'size'), code)
    hex_value(obj['sha256'], code=code)
    need(type(obj['size']) is int and obj['size'] > 0, code)
    return obj


def file_ref(obj, code='EVIDENCE_INVALID'):
    exact(obj, ('path', 'sha256', 'size'), code)
    normalized(obj['path'])
    digest({k: obj[k] for k in ('sha256', 'size')}, code)
    return obj


def binding(data):
    return {'sha256': sha(data), 'size': len(data)}


def normalized(value):
    need(type(value) is str and value.startswith('/') and not value.startswith('//') and '\x00' not in value and '\\' not in value,
         'PATH_UNSAFE')
    path = Path(value)
    need(str(path) == value and all(x not in ('.', '..') for x in path.parts), 'PATH_UNSAFE')
    return path


def below(path, root):
    need(path != root and root in path.parents, 'PATH_UNSAFE')
    return path


def disjoint(*paths):
    for i, path in enumerate(paths):
        for other in paths[i + 1:]:
            need(path != other and path not in other.parents and other not in path.parents, 'PATH_UNSAFE')


def signature(s):
    return (s.st_dev, s.st_ino, s.st_mode, s.st_uid, s.st_gid, s.st_nlink,
            s.st_size, s.st_mtime_ns, s.st_ctime_ns)


def directory_signature(s):
    # Our own staging changes directory mtime; immutable ownership/inode remain.
    return (s.st_dev, s.st_ino, s.st_mode, s.st_uid, s.st_gid)


def root_directory(s, private=False):
    need(stat.S_ISDIR(s.st_mode) and s.st_uid == s.st_gid == 0 and
         not s.st_mode & 0o022 and (not private or stat.S_IMODE(s.st_mode) == 0o700), 'PATH_UNSAFE')


def open_directory(path, protected=False, anchor=None):
    """Walk from / using NOFOLLOW dirfds; no resolve-then-open symlink race."""
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC)
    trail = []
    try:
        current = Path('/')
        for part in ('',) + path.parts[1:]:
            if part:
                new = os.open(part, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=fd)
                os.close(fd)
                fd = new
                current /= part
            s = os.fstat(fd)
            if protected:
                root_directory(s, anchor is not None and (current == anchor or anchor in current.parents))
            trail.append((current, directory_signature(s)))
        return fd, trail
    except BaseException:
        os.close(fd)
        raise


def verify_trail(trail):
    for path, expected in trail:
        need(directory_signature(os.lstat(str(path))) == expected, 'PATH_UNSAFE')


class StableReader:
    """Keep bytes + stable descriptor proofs and recheck all inputs at publication."""
    def __init__(self):
        self.saved = {}
        self.inodes = {}

    def read(self, path, anchor=None):
        path = normalized(str(path))
        if anchor:
            below(path, anchor)
        fd, trail = open_directory(path.parent, anchor is not None, anchor)
        try:
            leaf = os.open(path.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_NONBLOCK | os.O_CLOEXEC, dir_fd=fd)
            with os.fdopen(leaf, 'rb') as handle:
                before = os.fstat(handle.fileno())
                need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1, 'PATH_UNSAFE')
                if anchor:
                    need(before.st_uid == before.st_gid == 0 and stat.S_IMODE(before.st_mode) == 0o600,
                         'PATH_UNSAFE')
                data = handle.read()
                after = os.fstat(handle.fileno())
            current = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
            need(signature(before) == signature(after) == signature(current), 'DIGEST_MISMATCH')
            verify_trail(trail)
        finally:
            os.close(fd)
        inode = (before.st_dev, before.st_ino)
        need(inode not in self.inodes or self.inodes[inode] == path, 'PATH_UNSAFE')
        previous = self.saved.get(path)
        need(previous is None or previous[0:2] == (data, signature(before)), 'DIGEST_MISMATCH')
        self.saved[path] = (data, signature(before), anchor)
        self.inodes[inode] = path
        return data

    def checked(self, ref, anchor, code='DIGEST_MISMATCH'):
        file_ref(ref, code)
        data = self.read(normalized(ref['path']), anchor)
        need(binding(data) == {k: ref[k] for k in ('sha256', 'size')}, code)
        return data

    def recheck(self):
        for path, (data, unused, anchor) in list(self.saved.items()):
            need(self.read(path, anchor) == data, 'DIGEST_MISMATCH')


def payload_archive(data):
    out = {}
    try:
        with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
            for member in archive:
                need(member.name in MEMBERS and member.name not in out and member.isreg() and
                     member.size > 0 and not member.sparse and not member.pax_headers, 'PACKAGE_INVALID')
                handle = archive.extractfile(member)
                need(handle is not None, 'PACKAGE_INVALID')
                with handle:
                    out[member.name] = handle.read()
                need(len(out[member.name]) == member.size, 'PACKAGE_INVALID')
    except (tarfile.TarError, EOFError, ValueError):
        raise Rejected('PACKAGE_INVALID') from None
    need(set(out) == set(MEMBERS), 'PACKAGE_INVALID')
    return out


def manifest_and_mail(data):
    def safe_zip(z):
        names = z.namelist()
        need(len(names) == len(set(names)) and all(not n.startswith('/') and '\\' not in n and
             '\x00' not in n and '..' not in n.split('/') for n in names), 'JAR_INVALID')
        need(all(not stat.S_ISLNK(x.external_attr >> 16) for x in z.infolist()), 'JAR_INVALID')
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as boot:
            safe_zip(boot)
            text = boot.read('META-INF/MANIFEST.MF').decode('utf-8')
            lines = []
            for line in text.replace('\r\n', '\n').split('\n'):
                if not line:
                    break  # main attributes only
                if line.startswith(' '):
                    need(bool(lines), 'JAR_INVALID')
                    lines[-1] += line[1:]
                else:
                    lines.append(line)
            mf = {}
            for line in lines:
                k, sep, v = line.partition(': ')
                need(bool(sep) and k and k.lower() not in {n.lower() for n in mf}, 'JAR_INVALID')
                mf[k] = v
            need(mf.get('Start-Class') == 'cn.jia.JiaApplication' and
                 mf.get('Main-Class', '').startswith('org.springframework.boot.loader.'), 'JAR_INVALID')
            missing = set(MAIL_CLASSES)
            # Same actual nested shipped runtime check as original verify_mail_runtime;
            # self-contained stdlib implementation, no builder/repository code import.
            for name in boot.namelist():
                if name.startswith('BOOT-INF/lib/') and name.endswith('.jar'):
                    with zipfile.ZipFile(io.BytesIO(boot.read(name))) as nested:
                        safe_zip(nested)
                        missing.difference_update(nested.namelist())
            need(not missing, 'MAIL_RUNTIME_INVALID')
        return mf, sorted(MAIL_CLASSES)
    except (zipfile.BadZipFile, KeyError, UnicodeError, RuntimeError):
        raise Rejected('JAR_INVALID') from None


def xml_summary(data):
    try:
        need(b'<!DOCTYPE' not in data and b'<!ENTITY' not in data)
        class NoDTD(ET.TreeBuilder):
            def doctype(self, name, pubid, system):
                raise Rejected('EVIDENCE_INVALID')
        root = ET.fromstring(data, parser=ET.XMLParser(target=NoDTD()))
        need(root.tag in ('testsuite', 'testsuites'))
        suites = [root] if root.tag == 'testsuite' else list(root)
        result = dict(tests=0, failures=0, errors=0, skipped=0)
        names = set()
        for suite in suites:
            need(suite.tag == 'testsuite')
            counts = {}
            for k in result:
                value = suite.get(k, '0')
                need(re.fullmatch(r'[0-9]+', value))
                counts[k] = int(value)
            cases = suite.findall('testcase')
            need(counts['tests'] == len(cases) and counts['failures'] == counts['errors'] == 0)
            for case in cases:
                label = (case.get('classname'), case.get('name'))
                need(all(label) and label not in names and not case.findall('failure') and not case.findall('error'))
                names.add(label)
            need(counts['skipped'] == sum(bool(c.findall('skipped')) for c in cases))
            for k in result:
                result[k] += counts[k]
        need(result['tests'] >= result['skipped'])
        return result
    except (ET.ParseError, ValueError):
        raise Rejected('EVIDENCE_INVALID') from None


def task_executed(log, task):
    need(type(task) is str and re.fullmatch(r':[A-Za-z0-9_:-]+', task))
    matches = re.findall(r'^> Task ' + re.escape(task) + r'(?=\s|$)(.*)$', log, flags=re.MULTILINE)
    need(len(matches) == 1 and not matches[0].strip())


def validate_argv(argv, tasks, inputs):
    need(type(argv) is list and argv and all(type(x) is str for x in argv))
    need(Path(argv[0]).name in ('gradle', 'gradlew'))
    i, previous, metadata_seen = 1, None, False
    simple = {'--no-daemon', '--no-build-cache', '--build-cache', '--rerun-tasks', '--console=plain', '--stacktrace', '--info'}
    while i < len(argv):
        arg = argv[i]
        if arg in ('-I', '--init-script'):
            need(i + 1 < len(argv) and argv[i + 1] in inputs)
            metadata_seen |= Path(argv[i + 1]).name == 'local-release-metadata.init.gradle'
            i += 2
        elif arg == '--tests':
            need(previous in tasks - {':starter:bootJar', ':validateLayering'} and i + 1 < len(argv) and
                 re.fullmatch(r'[A-Za-z0-9_.*$-]+', argv[i + 1]))
            i += 2
        else:
            is_task = bool(re.fullmatch(r':[A-Za-z0-9_:-]+', arg))
            need(arg in simple or is_task)
            if is_task:
                previous = arg
            i += 1
    need(tasks.issubset(argv) and '--console=plain' in argv and metadata_seen)


def clean_state(obj, ident):
    exact(obj, ('commit', 'tree', 'clean'))
    need(obj['clean'] is True and obj['commit'] == ident['commit'] and obj['tree'] == ident['tree'])


def verify_evidence(record, verification, payloads, reader, trusted_root):
    evidence_data = reader.checked(record['buildEvidence'], trusted_root)
    need(sha(evidence_data) == verification['buildEvidenceSha256'])
    ev = strict_json(evidence_data)
    exact(ev, ('format', 'identity', 'sourceRoot', 'buildRoot', 'sourceBefore', 'sourceAfter',
               'invocation', 'tests', 'validateLayering', 'bootJar', 'opencv'))
    ident = record['identity']
    need(ev['format'] == 'cyf-api-local-build-evidence-v1' and ev['identity'] == ident)
    source, build = normalized(ev['sourceRoot']), normalized(ev['buildRoot'])
    disjoint(source, build, trusted_root)
    clean_state(ev['sourceBefore'], ident)
    clean_state(ev['sourceAfter'], ident)
    need(type(record['snapshots']) is list and record['snapshots'])
    saved = {}
    protected_files = set()
    for item in record['snapshots']:
        exact(item, ('role', 'originalPath', 'file'))
        need(item['role'] in ('build-evidence', 'invocation-log', 'bootjar-proof', 'input', 'test-report', 'opencv-jar'))
        original = str(normalized(item['originalPath']))
        need(original not in saved)
        file_ref(item['file'])
        need(item['file']['path'] not in protected_files, 'PATH_UNSAFE')
        protected_files.add(item['file']['path'])
        data = reader.checked(item['file'], trusted_root)
        saved[original] = (item['role'], data, item['file'])
    own = [p for p, (role, data, ref) in saved.items() if role == 'build-evidence']
    need(len(own) == 1 and saved[own[0]][2] == record['buildEvidence'])
    below(normalized(own[0]), build)
    used = {own[0]}

    def reference(ref, role, root=None):
        file_ref(ref)
        original = ref['path']
        if root:
            below(normalized(original), root)
        need(original not in used and original in saved)
        found_role, data, unused = saved[original]
        need(found_role == role and binding(data) == {k: ref[k] for k in ('sha256', 'size')})
        used.add(original)
        return data

    inv = exact(ev['invocation'], ('argv', 'exitCode', 'cacheHit', 'log', 'selector', 'fixtureSha256', 'inputs'))
    need(type(inv['exitCode']) is int and inv['exitCode'] == 0 and inv['cacheHit'] is False)
    token(inv['selector'], 'EVIDENCE_INVALID')
    hex_value(inv['fixtureSha256'], code='EVIDENCE_INVALID')
    log_data = reference(inv['log'], 'invocation-log', build)
    log = log_data.decode('utf-8')
    need('GRADLE_LOCK_ACQUIRED task=' in log and 'EVIDENCE_HIT' not in log and
         re.search(r'^BUILD SUCCESSFUL(?:\s|$)', log, re.MULTILINE))
    need(sha(log_data) == verification['invocationLogSha256'])
    need(type(inv['inputs']) is list and inv['inputs'])
    input_paths = []
    for ref in inv['inputs']:
        reference(ref, 'input')
        input_paths.append(ref['path'])
    need(str(source / 'settings.gradle') in input_paths and str(source / 'starter/build.gradle') in input_paths)
    need(type(ev['tests']) is list and ev['tests'])
    tests, tasks = [], set()
    for test in ev['tests']:
        exact(test, ('task', 'selector', 'fixtureSha256', 'reports'))
        task_executed(log, test['task'])
        need(test['task'] not in tasks and test['task'] not in (':validateLayering', ':starter:bootJar'))
        tasks.add(test['task'])
        token(test['selector'], 'EVIDENCE_INVALID')
        hex_value(test['fixtureSha256'], code='EVIDENCE_INVALID')
        need(type(test['reports']) is list and test['reports'])
        summaries = []
        for ref in test['reports']:
            data = reference(ref, 'test-report', build)
            summaries.append({**binding(data), **xml_summary(data)})
        need(sum(s['tests'] - s['skipped'] for s in summaries) > 0)
        tests.append(dict({k: test[k] for k in ('task', 'selector', 'fixtureSha256')}, reports=summaries))
    need({':starter:publicArtifactVerifierTest', ':starter:poiProductionRuntimeClasspathTest'}.issubset(tasks))
    # Type-safe equality: bool is not accepted as an XML count/exit code.
    controller_tests = verification['requiredTests']
    need(type(controller_tests) is list and controller_tests)
    for test in controller_tests:
        exact(test, ('task', 'selector', 'fixtureSha256', 'reports'), 'AUTHORITY_INVALID')
        need(type(test['reports']) is list and test['reports'], 'AUTHORITY_INVALID')
        for report in test['reports']:
            exact(report, ('sha256', 'size', 'tests', 'failures', 'errors', 'skipped'), 'AUTHORITY_INVALID')
            need(all(type(report[k]) is int for k in ('size', 'tests', 'failures', 'errors', 'skipped')), 'AUTHORITY_INVALID')
    need(controller_tests == tests)
    need(ev['validateLayering'] == {'task': ':validateLayering'})
    task_executed(log, ':validateLayering')
    boot = exact(ev['bootJar'], ('task', 'proof'))
    need(boot['task'] == ':starter:bootJar')
    task_executed(log, boot['task'])
    validate_argv(inv['argv'], tasks | {':validateLayering', boot['task']}, input_paths)
    proof_data = reference(boot['proof'], 'bootjar-proof', build)
    need(boot['proof']['path'] == str(build / 'local-bootjar-proof.json') and
         sha(proof_data) == verification['bootJarProofSha256'])
    proof = strict_json(proof_data)
    exact(proof, ('format', 'identity', 'sourceRoot', 'buildRoot', 'sourceBefore', 'sourceAfter',
                 'task', 'metadata', 'moduleVersion', 'implementationVersion', 'jar', 'publicArtifactVerifier'))
    clean_state(proof['sourceBefore'], ident)
    clean_state(proof['sourceAfter'], ident)
    metadata = dict(zip(META_KEYS, [ident[k] for k in ('version', 'commit', 'tree', 'buildId')]))
    need(proof['format'] == 'cyf-api-local-bootjar-proof-v1' and proof['identity'] == ident and
         proof['sourceRoot'] == str(source) and proof['buildRoot'] == str(build) and proof['task'] == boot['task'] and
         proof['metadata'] == metadata and proof['publicArtifactVerifier'] == 'bootJar-original-doLast-completed')
    token(proof['moduleVersion'], 'EVIDENCE_INVALID')
    need(proof['implementationVersion'] is None or (type(proof['implementationVersion']) is str and
         re.fullmatch(r'[A-Za-z0-9_.-]+', proof['implementationVersion'])))
    begin = 'CYF_LOCAL_BOOTJAR_BEGIN ' + ident['buildId'] + '\n'
    end = 'CYF_LOCAL_BOOTJAR_END ' + sha(proof_data) + '\n'
    need(log.count(begin) == log.count(end) == 1 and log.index(begin) < log.index(end) < log.index('BUILD SUCCESSFUL'))
    file_ref(proof['jar'])
    below(normalized(proof['jar']['path']), build)
    need(binding(payloads['application.jar']) == {k: proof['jar'][k] for k in ('sha256', 'size')})
    # JAR's logical original reference may not alias any evidence reference.
    need(proof['jar']['path'] not in saved)
    prov_data = reference(ev['opencv'], 'input', build)
    need(prov_data == payloads['dependency.provenance.json'])
    prov = strict_json(prov_data)
    exact(prov, ('coordinate', 'jar_sha256', 'jar_size', 'resolved_file'), 'PROVENANCE_INVALID')
    need(prov['coordinate'] == 'org.opencv:opencv:4.5.5' and prov['jar_sha256'] == OPENCV_SHA and
         type(prov['jar_size']) is int and prov['jar_size'] == OPENCV_SIZE, 'PROVENANCE_INVALID')
    dependency = reference({'path': prov['resolved_file'], 'sha256': OPENCV_SHA, 'size': OPENCV_SIZE}, 'opencv-jar')
    need(binding(dependency) == {'sha256': OPENCV_SHA, 'size': OPENCV_SIZE}, 'PROVENANCE_INVALID')
    need(used == set(saved))
    return ev, proof, tests


def verify_payloads(record, verification, payloads, reader, root):
    ident = record['identity']
    exact(record['payloads'], MEMBERS, 'DIGEST_MISMATCH')
    for name in MEMBERS:
        need(digest(record['payloads'][name]) == binding(payloads[name]), 'DIGEST_MISMATCH')
    receipt = strict_json(payloads['receipt.json'])
    exact(receipt, ('format', 'status', 'producer', 'identity', 'source', 'evidence',
                    'applicationJar', 'dependencyProvenance', 'verification'))
    need(receipt['format'] == 'cyf-api-local-release-receipt-v1' and receipt['status'] == 'packaged' and
         receipt['producer'] == {'kind': 'local-build-v1'} and receipt['identity'] == ident)
    exact(receipt['source'], ('commit', 'tree', 'cleanBefore', 'cleanAfter'))
    need(receipt['source']['cleanBefore'] is True and receipt['source']['cleanAfter'] is True and
         receipt['source']['commit'] == ident['commit'] and receipt['source']['tree'] == ident['tree'])
    jar_ref = {'path': 'application.jar', **binding(payloads['application.jar'])}
    prov_ref = {'path': 'dependency.provenance.json', **binding(payloads['dependency.provenance.json'])}
    need(receipt['applicationJar'] == jar_ref and receipt['dependencyProvenance'] == prov_ref)
    meta = strict_json(payloads['application.metadata.json'])
    side = strict_json(payloads['application.sidecar.json'])
    exact(meta, ('format', 'identity', 'receiptSha256', 'applicationJar', 'dependencyProvenance',
                 'moduleVersion', 'implementationVersion'))
    exact(side, ('format', 'identity', 'receiptSha256', 'applicationJar', 'dependencyProvenance'))
    need(meta['format'] == 'cyf-api-local-application-metadata-v1' and
         side['format'] == 'cyf-api-local-application-sidecar-v1')
    for obj in (meta, side):
        need(obj['identity'] == ident and obj['receiptSha256'] == sha(payloads['receipt.json']) and
             obj['applicationJar'] == jar_ref and obj['dependencyProvenance'] == prov_ref)
    ev, proof, tests = verify_evidence(record, verification, payloads, reader, root)
    evidence = exact(receipt['evidence'], ('sha256', 'invocationLogSha256', 'selector', 'fixtureSha256',
                                         'inputs', 'tests', 'bootJarProofSha256'))
    expected = {'sha256': record['buildEvidence']['sha256'],
        'invocationLogSha256': ev['invocation']['log']['sha256'], 'selector': ev['invocation']['selector'],
        'fixtureSha256': ev['invocation']['fixtureSha256'], 'inputs': ev['invocation']['inputs'],
        'tests': tests, 'bootJarProofSha256': ev['bootJar']['proof']['sha256']}
    need(evidence == expected)
    # Check counts/size types even if malicious producer used JSON true == 1.
    need(type(evidence['tests']) is list)
    for item in evidence['tests']:
        exact(item, ('task', 'selector', 'fixtureSha256', 'reports'))
        for summary in item['reports']:
            exact(summary, ('sha256', 'size', 'tests', 'failures', 'errors', 'skipped'))
            need(all(type(summary[k]) is int for k in ('size', 'tests', 'failures', 'errors', 'skipped')))
    need(meta['moduleVersion'] == proof['moduleVersion'] and meta['implementationVersion'] == proof['implementationVersion'])
    mf, classes = manifest_and_mail(payloads['application.jar'])
    need(all(mf.get(k) == v for k, v in proof['metadata'].items()) and
         mf.get('Implementation-Version') == proof['implementationVersion'], 'JAR_INVALID')
    need(receipt['verification'] == {'mailRuntimeClasses': classes,
                                   'publicArtifactVerifier': 'bootJar-original-doLast-completed'})


def parse_batch_authority(auth_data, expected_sha256):
    """Shared original root batch authority checks; never an install authorization."""
    need(sha(auth_data) == expected_sha256, 'AUTHORITY_INVALID')
    auth = strict_json(auth_data, 'AUTHORITY_INVALID')
    exact(auth, ('format', 'authorityId', 'scope', 'batchId', 'identity', 'trustedRecordSha256',
                 'verificationRecord'), 'AUTHORITY_INVALID')
    need(auth['format'] == 'cyf-api-local-batch-authority-v1' and auth['authorityId'] == AUTHORITY_ID and
         auth['scope'] == SCOPE, 'AUTHORITY_INVALID')
    identity(auth['identity'])
    token(auth['batchId'], 'AUTHORITY_INVALID')
    return auth


def parse_controller_verification(auth, verification_data):
    """Validate the same independent observations for ingress and published copies."""
    file_ref(auth['verificationRecord'], 'AUTHORITY_INVALID')
    need(binding(verification_data) == {k: auth['verificationRecord'][k] for k in ('sha256', 'size')},
         'AUTHORITY_INVALID')
    verification = strict_json(verification_data, 'AUTHORITY_INVALID')
    exact(verification, ('format', 'authorityId', 'batchId', 'identity', 'buildEvidenceSha256',
        'package', 'payloads', 'invocationLogSha256', 'bootJarProofSha256', 'requiredTests', 'observations'), 'AUTHORITY_INVALID')
    need(verification['format'] == 'cyf-api-local-controller-verification-v1' and
         verification['authorityId'] == AUTHORITY_ID and verification['identity'] == auth['identity'] and
         verification['batchId'] == auth['batchId'], 'AUTHORITY_INVALID')
    digest(verification['package'], 'AUTHORITY_INVALID')
    exact(verification['payloads'], MEMBERS, 'AUTHORITY_INVALID')
    for member in MEMBERS:
        digest(verification['payloads'][member], 'AUTHORITY_INVALID')
    observations = exact(verification['observations'], OBSERVATIONS, 'AUTHORITY_INVALID')
    for k, expected in OBSERVATIONS.items():
        need(type(observations[k]) is type(expected) and observations[k] == expected, 'AUTHORITY_INVALID')
    # An empty controller test observation is not authority for a batch,
    # irrespective of any internally consistent producer log/receipt.
    observed_tests = verification['requiredTests']
    need(type(observed_tests) is list and observed_tests, 'AUTHORITY_INVALID')
    observed_tasks = set()
    for test in observed_tests:
        exact(test, ('task', 'selector', 'fixtureSha256', 'reports'), 'AUTHORITY_INVALID')
        need(type(test['task']) is str and re.fullmatch(r':[A-Za-z0-9_:-]+', test['task']) and
             test['task'] not in observed_tasks, 'AUTHORITY_INVALID')
        observed_tasks.add(test['task'])
        token(test['selector'], 'AUTHORITY_INVALID')
        hex_value(test['fixtureSha256'], code='AUTHORITY_INVALID')
        need(type(test['reports']) is list and test['reports'], 'AUTHORITY_INVALID')
        for report in test['reports']:
            exact(report, ('sha256', 'size', 'tests', 'failures', 'errors', 'skipped'), 'AUTHORITY_INVALID')
            digest({k: report[k] for k in ('sha256', 'size')}, 'AUTHORITY_INVALID')
            need(all(type(report[k]) is int for k in ('tests', 'failures', 'errors', 'skipped')) and
                 report['tests'] >= report['skipped'] >= 0 and
                 report['failures'] == report['errors'] == 0, 'AUTHORITY_INVALID')
        need(sum(r['tests'] - r['skipped'] for r in test['reports']) > 0, 'AUTHORITY_INVALID')
    need({':starter:publicArtifactVerifierTest', ':starter:poiProductionRuntimeClasspathTest'}.issubset(observed_tasks),
         'AUTHORITY_INVALID')
    return verification


def parse_trusted_record(auth, verification, record_data, expected_sha256):
    """Validate the exact original trusted-record bytes, not projected JSON claims."""
    need(sha(record_data) == expected_sha256 == auth['trustedRecordSha256'], 'AUTHORITY_INVALID')
    record = strict_json(record_data)
    exact(record, ('format', 'scope', 'batchId', 'identity', 'package', 'payloads', 'buildEvidence',
                   'snapshots', 'installPrecondition'))
    need(record['format'] == 'cyf-api-local-trusted-record-v1' and record['scope'] == SCOPE)
    identity(record['identity'])
    need(record['identity'] == auth['identity'] and record['batchId'] == auth['batchId'], 'IDENTITY_MISMATCH')
    need(digest(record['package']) == digest(verification['package'], 'AUTHORITY_INVALID') and
         record['payloads'] == verification['payloads'], 'AUTHORITY_INVALID')
    exact(record['installPrecondition'], ('canonicalJarSha256',))
    hex_value(record['installPrecondition']['canonicalJarSha256'], code='EVIDENCE_INVALID')
    for k in ('buildEvidenceSha256', 'invocationLogSha256', 'bootJarProofSha256'):
        hex_value(verification[k], code='AUTHORITY_INVALID')
    return record


def load_authority(args, reader, root, authority_root):
    """Authenticate the root decision BEFORE inspecting a producer's claimed PASS."""
    authority_path = below(normalized(args.batch_authority), authority_root)
    record_path = below(normalized(args.trusted_record), root)
    try:
        auth_data = reader.read(authority_path, authority_root)
        auth = parse_batch_authority(auth_data, args.batch_authority_sha256)
        verification_data = reader.checked(auth['verificationRecord'], authority_root, 'AUTHORITY_INVALID')
        verification = parse_controller_verification(auth, verification_data)
    except FileNotFoundError:
        raise Rejected('AUTHORITY_INVALID') from None
    record_data = reader.read(record_path, root)
    record = parse_trusted_record(auth, verification, record_data, args.trusted_record_sha256)
    return record, auth, verification, record_data, auth_data, verification_data


def rename_no_replace(parent_fd, old, new):
    """Linux atomic directory publication; no check-then-rename overwrite fallback."""
    libc = ctypes.CDLL(None, use_errno=True)
    function = getattr(libc, 'renameat2', None)
    need(function is not None, 'IO_FAILURE')
    function.argtypes = (ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_uint)
    function.restype = ctypes.c_int
    if function(parent_fd, os.fsencode(old), parent_fd, os.fsencode(new), 1):  # RENAME_NOREPLACE
        error = ctypes.get_errno()
        raise Rejected('OUTPUT_EXISTS' if error in (errno.EEXIST, errno.ENOTEMPTY) else 'IO_FAILURE')


class OwnedStage:
    """Track every created inode; cleanup only this exact unpublished snapshot."""
    def __init__(self, parent_fd):
        self.parent_fd = parent_fd
        self.name = '.admit-' + secrets.token_hex(16)
        os.mkdir(self.name, mode=0o700, dir_fd=parent_fd)
        self.fd = os.open(self.name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=parent_fd)
        self.dirs = {'': self.fd}
        self.nodes = {'': directory_signature(os.fstat(self.fd))}
        self.files = {}
        self.published = False

    def directory(self, name):
        os.mkdir(name, mode=0o700, dir_fd=self.fd)
        fd = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=self.fd)
        self.dirs[name] = fd
        self.nodes[name] = directory_signature(os.fstat(fd))

    def write(self, name, data):
        path = Path(name)
        directory = '' if str(path.parent) == '.' else str(path.parent)
        fd = os.open(path.name, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW | os.O_CLOEXEC,
                     0o600, dir_fd=self.dirs[directory])
        with os.fdopen(fd, 'wb') as handle:
            # Track inode before any potentially failing chmod/write/fsync.
            self.files[name] = (os.fstat(handle.fileno()).st_dev, os.fstat(handle.fileno()).st_ino)
            os.fchmod(handle.fileno(), 0o600)
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        return binding(data)

    def verify(self):
        need(directory_signature(os.stat(self.name, dir_fd=self.parent_fd, follow_symlinks=False)) ==
             self.nodes[''], 'PATH_UNSAFE')
        for directory, fd in self.dirs.items():
            need(directory_signature(os.fstat(fd)) == self.nodes[directory], 'PATH_UNSAFE')
            if directory:
                need(directory_signature(os.stat(directory, dir_fd=self.fd, follow_symlinks=False)) ==
                     self.nodes[directory], 'PATH_UNSAFE')
            expected = {Path(n).name for n in self.files if ('' if str(Path(n).parent) == '.' else str(Path(n).parent)) == directory}
            if not directory:
                expected |= set(self.dirs) - {''}
            need(set(os.listdir(fd)) == expected, 'PATH_UNSAFE')
        for name, inode in self.files.items():
            path = Path(name)
            fd = self.dirs['' if str(path.parent) == '.' else str(path.parent)]
            s = os.stat(path.name, dir_fd=fd, follow_symlinks=False)
            need(stat.S_ISREG(s.st_mode) and s.st_uid == s.st_gid == 0 and s.st_nlink == 1 and
                 stat.S_IMODE(s.st_mode) == 0o600 and (s.st_dev, s.st_ino) == inode, 'PATH_UNSAFE')

    def cleanup(self):
        # Published outputs are never deleted, including uncertain fsync outcomes.
        if not self.published:
            self.verify()
            for name in reversed(list(self.files)):
                path = Path(name)
                os.unlink(path.name, dir_fd=self.dirs['' if str(path.parent) == '.' else str(path.parent)])
            for name in reversed(list(self.dirs)):
                if name:
                    os.rmdir(name, dir_fd=self.fd)
            os.rmdir(self.name, dir_fd=self.parent_fd)
            os.fsync(self.parent_fd)

    def close(self):
        for fd in self.dirs.values():
            os.close(fd)


def publish(args, reader, record, auth, raw_records, payloads, parent_fd, trail):
    output = normalized(args.output)
    stage = OwnedStage(parent_fd)
    try:
        for name in ('payload', 'authority', 'evidence'):
            stage.directory(name)
        def write(name, data):
            return {'path': str(output / name), **stage.write(name, data)}
        package = write('package.tgz', reader.saved[normalized(args.package)][0])
        payload_refs = {name: write('payload/' + name, payloads[name]) for name in MEMBERS}
        record_data, auth_data, verification_data = raw_records
        authority = {'authorityId': AUTHORITY_ID, 'batchId': auth['batchId'],
            'batchAuthority': write('authority/batch-authority.json', auth_data),
            'trustedRecord': write('authority/trusted-record.json', record_data),
            'verificationRecord': write('authority/controller-verification.json', verification_data)}
        snapshots = []
        build_evidence_ref = None
        for i, item in enumerate(record['snapshots']):
            data = reader.saved[normalized(item['file']['path'])][0]
            ref = write('evidence/%06d.bin' % i, data)
            snapshots.append({'role': item['role'], 'originalPath': item['originalPath'], 'file': ref})
            if item['role'] == 'build-evidence':
                build_evidence_ref = ref
        admitted = {'format': 'cyf-api-local-admitted-input-v1', 'status': 'admitted',
            'source': {'kind': 'local-build-v1', 'identity': record['identity']}, 'authority': authority,
            'package': package, 'payloads': payload_refs,
            'evidence': {'buildEvidence': build_evidence_ref, 'snapshots': snapshots},
            'installPrecondition': record['installPrecondition'], 'scope': SCOPE, 'productionAuthorized': False}
        admission_ref = write('admission.json', canonical(admitted))
        stage.verify()
        # Re-read every staged byte, not merely each inode, before trusting publication.
        for name in stage.files:
            p = Path(name)
            directory = stage.dirs['' if str(p.parent) == '.' else str(p.parent)]
            fd = os.open(p.name, os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC, dir_fd=directory)
            with os.fdopen(fd, 'rb') as f:
                actual = f.read()
            if name == 'admission.json':
                need(binding(actual) == {k: admission_ref[k] for k in ('sha256', 'size')}, 'DIGEST_MISMATCH')
            elif name == 'package.tgz':
                need(binding(actual) == record['package'], 'DIGEST_MISMATCH')
            elif name.startswith('payload/'):
                need(binding(actual) == record['payloads'][p.name], 'DIGEST_MISMATCH')
            elif name.startswith('authority/'):
                source = {'batch-authority.json': auth_data, 'trusted-record.json': record_data,
                          'controller-verification.json': verification_data}[p.name]
                need(actual == source, 'DIGEST_MISMATCH')
            else:
                ref = record['snapshots'][int(p.stem)]['file']
                need(binding(actual) == {k: ref[k] for k in ('sha256', 'size')}, 'DIGEST_MISMATCH')
        reader.recheck()
        verify_trail(trail)
        # Child contents first, then root directory entries, then final parent.
        for name in reversed(list(stage.dirs)):
            os.fsync(stage.dirs[name])
        rename_no_replace(parent_fd, stage.name, output.name)
        stage.published = True
        os.fsync(parent_fd)
        verify_trail(trail)
        need(directory_signature(os.stat(output.name, dir_fd=parent_fd, follow_symlinks=False)) ==
             stage.nodes[''], 'PATH_UNSAFE')
        return {'format': 'cyf-api-local-admission-result-v1', 'status': 'admitted',
                'admission': admission_ref, 'productionAuthorized': False}
    finally:
        try:
            stage.cleanup()
        finally:
            stage.close()


def admit(args):
    need(args.opt_in is True, 'INPUT_INVALID')
    need(os.geteuid() == 0, 'ROOT_REQUIRED')
    need(not any(os.environ.get(k) for k in ('PIPELINE_ID', 'BUILD_NUMBER', 'CYF_FLOW_GRADLE_ACTIVE')), 'INPUT_INVALID')
    hex_value(args.batch_authority_sha256)
    hex_value(args.trusted_record_sha256)
    root, authority_root = normalized(args.trusted_root), normalized(args.authority_root)
    ingress, output = normalized(args.package), normalized(args.output)
    disjoint(root, authority_root, ingress)
    need(output.parent == root / 'admitted', 'PATH_UNSAFE')
    for anchor in (root, authority_root):
        fd, trail = open_directory(anchor, True, anchor)
        try:
            verify_trail(trail)
        finally:
            os.close(fd)
    parent_fd, trail = open_directory(output.parent, True, root)
    try:
        need(not os.path.lexists(str(output)), 'OUTPUT_EXISTS')
        reader = StableReader()
        record, auth, verification, record_data, auth_data, verification_data = load_authority(args, reader, root, authority_root)
        # The ingress package never gets to provide or authorize root authority.
        package_data = reader.read(ingress)
        need(binding(package_data) == record['package'], 'DIGEST_MISMATCH')
        payloads = payload_archive(package_data)
        verify_payloads(record, verification, payloads, reader, root)
        return publish(args, reader, record, auth, (record_data, auth_data, verification_data), payloads, parent_fd, trail)
    finally:
        os.close(parent_fd)


class CopiedProofReader:
    """Pure label-to-bytes map for the original trusted record's File identities.

    No filesystem capability exists here. Old protected file paths, like original
    builder paths inside evidence, are labels only. Shared verify_payloads checks
    their exact identities/roles/reference closure against already-read copies.
    """
    def __init__(self):
        self.copies = {}

    def add(self, original, data):
        file_ref(original)
        path = normalized(original['path'])
        need(path not in self.copies, 'EVIDENCE_INVALID')
        need(binding(data) == {k: original[k] for k in ('sha256', 'size')}, 'DIGEST_MISMATCH')
        self.copies[path] = (dict(original), data)

    def checked(self, ref, unused_anchor, code='DIGEST_MISMATCH'):
        file_ref(ref, code)
        item = self.copies.get(normalized(ref['path']))
        need(item is not None and item[0] == ref, code)
        return item[1]


def published_inventory(reader, root, output):
    """Read-only exact original publication layout; no extra or aliased nodes."""
    expected = {}
    for path in reader.saved:
        below(path, output)
        expected.setdefault(path.parent, set()).add(path.name)
    directories = (output, output / 'payload', output / 'authority', output / 'evidence')
    need(set(expected) == set(directories), 'EVIDENCE_INVALID')
    expected[output] |= {'payload', 'authority', 'evidence'}
    for directory in directories:
        fd, trail = open_directory(directory, True, root)
        try:
            need(set(os.listdir(fd)) == expected[directory], 'EVIDENCE_INVALID')
            verify_trail(trail)
        finally:
            os.close(fd)


def verify_published(args):
    """Revalidate artifact-only copied publication without writes or old-path reads."""
    need(args.verify_published is True, 'INPUT_INVALID')
    need(os.geteuid() == 0, 'ROOT_REQUIRED')
    need(not any(os.environ.get(k) for k in ('PIPELINE_ID', 'BUILD_NUMBER', 'CYF_FLOW_GRADLE_ACTIVE')), 'INPUT_INVALID')
    hex_value(args.admission_sha256)
    root, admission_path = normalized(args.trusted_root), normalized(args.admission)
    output = admission_path.parent
    need(output.parent == root / 'admitted' and admission_path.name == 'admission.json', 'PATH_UNSAFE')
    reader = StableReader()
    admission_data = reader.read(admission_path, root)
    need(sha(admission_data) == args.admission_sha256, 'DIGEST_MISMATCH')
    admitted = strict_json(admission_data)
    exact(admitted, ('format', 'status', 'source', 'authority', 'package', 'payloads',
                     'evidence', 'installPrecondition', 'scope', 'productionAuthorized'))
    need(admitted['format'] == 'cyf-api-local-admitted-input-v1' and admitted['status'] == 'admitted' and
         admitted['scope'] == SCOPE and admitted['productionAuthorized'] is False, 'AUTHORITY_INVALID')
    source = exact(admitted['source'], ('kind', 'identity'), 'IDENTITY_MISMATCH')
    need(source['kind'] == 'local-build-v1', 'IDENTITY_MISMATCH')
    identity(source['identity'])

    def copied(ref, relative, code='DIGEST_MISMATCH'):
        file_ref(ref, code)
        need(ref['path'] == str(output / relative), 'PATH_UNSAFE')
        return reader.checked(ref, root, code)

    authority = exact(admitted['authority'], ('authorityId', 'batchId', 'batchAuthority',
                                             'trustedRecord', 'verificationRecord'), 'AUTHORITY_INVALID')
    auth_data = copied(authority['batchAuthority'], 'authority/batch-authority.json', 'AUTHORITY_INVALID')
    auth = parse_batch_authority(auth_data, authority['batchAuthority']['sha256'])
    verification_data = copied(authority['verificationRecord'], 'authority/controller-verification.json', 'AUTHORITY_INVALID')
    verification = parse_controller_verification(auth, verification_data)
    record_data = copied(authority['trustedRecord'], 'authority/trusted-record.json', 'AUTHORITY_INVALID')
    record = parse_trusted_record(auth, verification, record_data, authority['trustedRecord']['sha256'])
    need(authority['authorityId'] == auth['authorityId'] and authority['batchId'] == auth['batchId'], 'AUTHORITY_INVALID')
    need(source['identity'] == record['identity'], 'IDENTITY_MISMATCH')
    need(admitted['installPrecondition'] == record['installPrecondition'], 'EVIDENCE_INVALID')

    # Original raw proof identities bijectively map to copies. Do not transform
    # or reload the original controller record/evidence, even if still present.
    evidence = exact(admitted['evidence'], ('buildEvidence', 'snapshots'))
    snapshots = evidence['snapshots']
    need(type(record['snapshots']) is list and record['snapshots'] and
         type(snapshots) is list and len(snapshots) == len(record['snapshots']))
    proof_reader = CopiedProofReader()
    build_ref = None
    for i, (original, snapshot) in enumerate(zip(record['snapshots'], snapshots)):
        exact(original, ('role', 'originalPath', 'file'))
        exact(snapshot, ('role', 'originalPath', 'file'))
        need(snapshot['role'] == original['role'] and snapshot['originalPath'] == original['originalPath'])
        data = copied(snapshot['file'], 'evidence/%06d.bin' % i)
        proof_reader.add(original['file'], data)
        if original['role'] == 'build-evidence':
            need(build_ref is None and original['file'] == record['buildEvidence'])
            build_ref = snapshot['file']
    need(build_ref is not None and evidence['buildEvidence'] == build_ref)
    need(normalized(auth['verificationRecord']['path']) not in proof_reader.copies, 'EVIDENCE_INVALID')

    package_data = copied(admitted['package'], 'package.tgz')
    need(binding(package_data) == record['package'], 'DIGEST_MISMATCH')
    payloads = payload_archive(package_data)
    exact(admitted['payloads'], MEMBERS, 'PACKAGE_INVALID')
    for name in MEMBERS:
        data = copied(admitted['payloads'][name], 'payload/' + name)
        need(data == payloads[name], 'DIGEST_MISMATCH')
    verify_payloads(record, verification, payloads, proof_reader, root)
    # Reads are protected throughout; final re-read detects replacement/tamper.
    published_inventory(reader, root, output)
    reader.recheck()
    published_inventory(reader, root, output)
    return {'format': 'cyf-api-local-published-verification-v1', 'status': 'verified',
            'scope': SCOPE, 'productionAuthorized': False,
            'admission': {'path': str(admission_path), **binding(admission_data)}, 'source': source}


def describe():
    return {'format': 'cyf-api-local-admission-interface-v1', 'scope': SCOPE,
        'trustedRecord': 'cyf-api-local-trusted-record-v1', 'batchAuthority': 'cyf-api-local-batch-authority-v1',
        'controllerVerification': 'cyf-api-local-controller-verification-v1',
        'admittedInput': 'cyf-api-local-admitted-input-v1', 'result': 'cyf-api-local-admission-result-v1',
        'safeCodes': sorted(SAFE_CODES), 'productionAuthorized': False,
        'trust': 'independent root controller observations required; producer consistency is not authentication',
        'publishedVerifier': {'mode': '--verify-published',
            'flags': ['--verify-published', '--trusted-root', '--admission', '--admission-sha256'],
            'result': 'cyf-api-local-published-verification-v1', 'readOnly': True}}


class SafeParser(argparse.ArgumentParser):
    def error(self, message):
        raise Rejected('INPUT_INVALID')


def parse(argv):
    p = SafeParser(add_help=False, allow_abbrev=False)
    p.add_argument('--opt-in', action='store_true', required=True)
    for name in ('trusted-root', 'authority-root', 'trusted-record', 'trusted-record-sha256',
                 'batch-authority', 'batch-authority-sha256', 'package', 'output'):
        p.add_argument('--' + name, required=True)
    need(len([v for v in argv if v.startswith('--')]) == 9 and
         len({v.split('=')[0] for v in argv if v.startswith('--')}) == 9, 'INPUT_INVALID')
    return p.parse_args(argv)


def parse_verification(argv):
    p = SafeParser(add_help=False, allow_abbrev=False)
    p.add_argument('--verify-published', action='store_true', required=True)
    for name in ('trusted-root', 'admission', 'admission-sha256'):
        p.add_argument('--' + name, required=True)
    flags = [v.split('=')[0] for v in argv if v.startswith('--')]
    need(len(flags) == 4 and len(set(flags)) == 4, 'INPUT_INVALID')
    return p.parse_args(argv)


def main(argv=None):
    import sys
    argv = sys.argv[1:] if argv is None else argv
    verification_mode = any(v.split('=')[0] == '--verify-published' for v in argv)
    result_format = ('cyf-api-local-published-verification-v1' if verification_mode
                     else 'cyf-api-local-admission-result-v1')
    try:
        if argv == ['--describe']:
            print(canonical(describe()).decode(), end='')
            return 0
        if verification_mode:
            result = verify_published(parse_verification(argv))
        else:
            args = parse(argv)
            previous = os.umask(0o077)
            try:
                result = admit(args)
            finally:
                os.umask(previous)
        print(canonical(result).decode(), end='')
        return 0
    except Rejected as exc:
        code = exc.code
    except (OSError, EOFError):
        code = 'IO_FAILURE'
    except (KeyError, TypeError, AttributeError, UnicodeError, ValueError, RecursionError, OverflowError):
        code = 'EVIDENCE_INVALID'
    except Exception:
        # Unexpected parser/filesystem faults must not leak raw input or paths.
        # Publication/cleanup still run in their own finally blocks.
        code = 'IO_FAILURE'
    print(canonical({'format': result_format, 'status': 'rejected', 'code': code}).decode(), end='')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
