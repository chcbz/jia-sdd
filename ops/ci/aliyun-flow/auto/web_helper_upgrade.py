#!/usr/bin/python3
"""Install a frozen web deploy helper from the same Flow artifact.

This bootstrap deliberately has no source-checkout dependency on the deployment
host.  It verifies an artifact-local helper manifest, serializes upgrades, and
keeps a root-only predecessor copy for rollback if the newly installed helper
returns a non-zero exit status.
"""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile

CHUNK_SIZE = 1024 * 1024
EXPECTED_MEMBERS = {
    'installer/cyf-web-flow-deploy',
    'installer/helper-release.json',
    'source-tree.txt',
}
IDENTITY_RE = re.compile(r'^[0-9a-f]{40,64}$')
TREE_RE = re.compile(r'^[0-9a-f]{40}$')
SHA256_RE = re.compile(r'^[0-9a-f]{64}$')


def fail(message):
    raise SystemExit('cyf-web-helper-upgrade: ' + message)


def safe_dir(path):
    info = path.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
        fail('unsafe directory ' + str(path))


def read_regular(path):
    try:
        fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
    except OSError:
        fail('unsafe regular file ' + str(path))
    try:
        before = os.fstat(fd)
        if not stat.S_ISREG(before.st_mode) or before.st_uid != 0 or before.st_nlink != 1:
            fail('unsafe regular file ' + str(path))
        digest = hashlib.sha256()
        chunks = []
        while True:
            block = os.read(fd, CHUNK_SIZE)
            if not block:
                break
            chunks.append(block)
            digest.update(block)
        after = os.fstat(fd)
        if (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) != (
                after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns):
            fail('regular file changed while reading ' + str(path))
        return b''.join(chunks), digest.hexdigest(), stat.S_IMODE(before.st_mode)
    finally:
        os.close(fd)


def write_regular(path, data, mode, exclusive=False):
    name = None
    if exclusive:
        fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    else:
        fd, name = tempfile.mkstemp(prefix='.cyf-web-helper-', dir=str(path.parent))
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, 'wb') as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
        if name is not None:
            os.replace(name, str(path))
            name = None
        directory = os.open(str(path.parent), os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory)
        finally:
            os.close(directory)
    finally:
        if name is not None:
            try:
                os.unlink(name)
            except FileNotFoundError:
                pass


def unique_json(pairs):
    value = {}
    for key, item in pairs:
        if key in value:
            raise ValueError('duplicate JSON key')
        value[key] = item
    return value


def copy_member(archive, member, destination=None):
    extracted = archive.extractfile(member)
    if extracted is None:
        fail('invalid helper artifact member')
    digest = hashlib.sha256()
    chunks = [] if destination is None else None
    size = 0
    output = None
    try:
        if destination is not None:
            try:
                fd = os.open(str(destination), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o700)
                output = os.fdopen(fd, 'wb')
            except OSError:
                fail('unsafe helper staging file')
        while True:
            block = extracted.read(CHUNK_SIZE)
            if not block:
                break
            size += len(block)
            if size > member.size:
                fail('helper artifact member exceeds declared size')
            digest.update(block)
            if output is None:
                chunks.append(block)
            else:
                output.write(block)
        if size != member.size:
            fail('helper artifact member size mismatch')
        if output is not None:
            output.flush()
            os.fsync(output.fileno())
    finally:
        if output is not None:
            output.close()
        extracted.close()
    return size, digest.hexdigest(), b''.join(chunks) if chunks is not None else None


def extract_candidate(archive_path, staging):
    try:
        fd = os.open(str(archive_path), os.O_RDONLY | os.O_NOFOLLOW)
    except OSError:
        fail('unsafe same-run artifact')
    try:
        artifact = os.fstat(fd)
        if not stat.S_ISREG(artifact.st_mode) or artifact.st_uid != 0 or artifact.st_nlink != 1 or artifact.st_size <= 0:
            fail('unsafe same-run artifact')
        seen = set()
        found = {}
        helper_path = staging / 'candidate-helper'
        with os.fdopen(fd, 'rb') as source:
            fd = None
            try:
                with tarfile.open(fileobj=source, mode='r|gz') as archive:
                    for member in archive:
                        if member.name not in EXPECTED_MEMBERS:
                            continue
                        if member.name in seen or not member.isfile() or member.size < 0:
                            fail('unsafe helper artifact member')
                        seen.add(member.name)
                        found[member.name] = copy_member(
                            archive, member,
                            helper_path if member.name == 'installer/cyf-web-flow-deploy' else None)
            except (tarfile.TarError, EOFError, OSError):
                fail('invalid same-run helper artifact')
        if set(found) != EXPECTED_MEMBERS:
            fail('missing same-run helper artifact member')
        return helper_path, found
    finally:
        if fd is not None:
            os.close(fd)


def validate_release(members, pipeline, run, commit, expected_new):
    helper_size, helper_sha, _ = members['installer/cyf-web-flow-deploy']
    if helper_sha != expected_new:
        fail('candidate helper digest mismatch')
    _, _, manifest_bytes = members['installer/helper-release.json']
    _, _, tree_bytes = members['source-tree.txt']
    try:
        tree = tree_bytes.decode('ascii')
        release = json.loads(manifest_bytes.decode('utf-8'), object_pairs_hook=unique_json)
    except (UnicodeDecodeError, ValueError):
        fail('invalid helper release manifest')
    if not tree.endswith('\n') or tree.count('\n') != 1 or not TREE_RE.fullmatch(tree[:-1]):
        fail('invalid source tree binding')
    expected = dict(
        schema_version=1, pipeline_id=pipeline, run_id=run, branch='develop', commit=commit,
        tree=tree[:-1], helper=dict(path='installer/cyf-web-flow-deploy', size=helper_size,
                                   sha256=helper_sha, mode='0700'))
    if release != expected:
        fail('helper release manifest does not match this Flow run')


def emit(reporter, name, **fields):
    reporter(name + ' ' + json.dumps(fields, sort_keys=True))


def rollback(target, backup, expected_old, expected_new, target_mode, run, reporter):
    installed_bytes, installed_digest, _ = read_regular(target)
    backup_bytes, backup_digest, _ = read_regular(backup)
    if installed_digest == expected_new and backup_digest == expected_old:
        write_regular(target, backup_bytes, target_mode)
        emit(reporter, 'CYF_WEB_HELPER_UPGRADE=ROLLED_BACK', run_id=run,
             restored_sha256=expected_old, failed_candidate_sha256=expected_new,
             rollback_path=str(backup))
        return
    emit(lambda value: print(value, file=sys.stderr, flush=True), 'CYF_WEB_HELPER_UPGRADE=ROLLBACK_SKIPPED',
         run_id=run, expected_candidate_sha256=expected_new,
         actual_installed_sha256=installed_digest, rollback_sha256=backup_digest)


def upgrade_and_run(pipeline, run, commit, archive, target, expected_old, expected_new, state_root,
                    runner=subprocess.run, reporter=lambda value: print(value, flush=True)):
    if (pipeline != '4403172' or not run.isdigit() or int(run) <= 0 or not IDENTITY_RE.fullmatch(commit)
            or not SHA256_RE.fullmatch(expected_old) or not SHA256_RE.fullmatch(expected_new)):
        fail('invalid Flow identity or helper digest')
    root = Path(state_root)
    archive = Path(archive)
    target = Path(target)
    safe_dir(root)
    safe_dir(target.parent)
    lock_path = root / 'helper-upgrade.lock'
    try:
        lock_fd = os.open(str(lock_path), os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
    except OSError:
        fail('unsafe helper upgrade lock')
    staging = None
    try:
        lock_info = os.fstat(lock_fd)
        if not stat.S_ISREG(lock_info.st_mode) or lock_info.st_uid != 0 or lock_info.st_nlink != 1:
            fail('unsafe helper upgrade lock')
        fcntl.flock(lock_fd, fcntl.LOCK_EX)
        staging = Path(tempfile.mkdtemp(prefix='.cyf-web-helper-', dir=str(root)))
        os.chmod(str(staging), 0o700)
        safe_dir(staging)
        candidate_path, members = extract_candidate(archive, staging)
        validate_release(members, pipeline, run, commit, expected_new)
        candidate_bytes, candidate_digest, candidate_mode = read_regular(candidate_path)
        if candidate_digest != expected_new or candidate_mode != 0o700:
            fail('staged helper changed')
        current_bytes, current_digest, current_mode = read_regular(target)
        upgraded = False
        backup = None
        if current_digest == expected_new:
            pass
        elif current_digest == expected_old:
            rollback_root = root / 'helper-rollbacks'
            rollback_root.mkdir(mode=0o700, exist_ok=True)
            safe_dir(rollback_root)
            backup = rollback_root / (pipeline + '-' + run + '-' + expected_old + '-to-' + expected_new)
            if backup.exists():
                backup_bytes, backup_digest, _ = read_regular(backup)
                if backup_digest != expected_old or backup_bytes != current_bytes:
                    fail('existing helper rollback does not match installed helper')
            else:
                write_regular(backup, current_bytes, 0o600, exclusive=True)
            refreshed_bytes, refreshed_digest, refreshed_mode = read_regular(target)
            if refreshed_digest != expected_old or refreshed_bytes != current_bytes or refreshed_mode != current_mode:
                fail('installed helper changed before compare-and-swap')
            write_regular(target, candidate_bytes, 0o755)
            upgraded = True
            emit(reporter, 'CYF_WEB_HELPER_UPGRADE=INSTALLED', run_id=run,
                 previous_sha256=expected_old, candidate_sha256=expected_new,
                 rollback_path=str(backup))
        else:
            fail('installed helper digest is neither expected predecessor nor candidate')
        try:
            result = runner([str(target), pipeline, run, commit], check=False)
        except BaseException:
            if upgraded:
                rollback(target, backup, expected_old, expected_new, current_mode, run, reporter)
            raise
        code = result.returncode
        if code != 0 and upgraded:
            rollback(target, backup, expected_old, expected_new, current_mode, run, reporter)
        return code
    finally:
        try:
            if staging is not None:
                shutil.rmtree(str(staging))
        finally:
            os.close(lock_fd)


def main(argv):
    if len(argv) != 9:
        fail('expected pipeline run commit archive target old_sha256 new_sha256 state_root')
    return upgrade_and_run(*argv[1:])


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
