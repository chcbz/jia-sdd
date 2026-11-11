"""Minimal, conservative Runtime state selection; no live cleanup or activation.

Unknown files are included. Only ephemeral startup probes and schema-confirmed
Codex diagnostic logs are excluded. Requests/conversations/SQLite state, locks,
authorization and task bindings remain included. Caller owns quiescing writers.
"""
import hashlib
import json
import os
from pathlib import Path
import re
import sqlite3
import stat
import subprocess

LOG_COLUMNS = {'id', 'ts', 'ts_nanos', 'level', 'target', 'feedback_log_body',
               'module_path', 'file', 'line', 'thread_id', 'process_uuid', 'estimated_bytes'}


def diagnostic_database(path):
    # Name alone never authorizes omission. Unknown schema is recovery data.
    if path.name != 'logs_2.sqlite' or path.is_symlink() or not path.is_file():
        return False
    connection = None
    try:
        connection = sqlite3.connect(path.as_uri() + '?mode=ro', uri=True, timeout=0)
        tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        columns = {row[1] for row in connection.execute('PRAGMA table_info(logs)')}
        views = list(connection.execute("SELECT name FROM sqlite_master WHERE type='view'"))
        return tables == {'logs', '_sqlx_migrations', 'sqlite_sequence'} and columns == LOG_COLUMNS and not views
    except (sqlite3.Error, OSError):
        return False
    finally:
        if connection is not None: connection.close()


def signature(path):
    s = path.lstat()
    return [s.st_dev, s.st_ino, s.st_mode, s.st_uid, s.st_gid, s.st_size, s.st_mtime_ns, s.st_ctime_ns]


def probe_directory(relative):
    parts = relative.parts
    # Only the exact runtime-managed agent layout, not a generic folder name.
    return (len(parts) == 7 and parts[:2] == ('unified', 'agents') and
            parts[3] == 'inspection-state' and re.fullmatch('[0-9a-f]+', parts[4]) and
            parts[5] == 'measurement' and re.fullmatch(r'\.(isolated|execution)-[A-Za-z0-9]+', parts[6]))


def plan(roots):
    roots = [Path(p) for p in roots]
    if len(set(roots)) != len(roots): raise ValueError('DUPLICATE_STATE_ROOT')
    for root in roots:
        if not root.is_absolute() or root.resolve() != root or not root.is_dir():
            raise ValueError('STATE_ROOT_NOT_CANONICAL_DIRECTORY')
        if any(root != other and other in root.parents for other in roots):
            raise ValueError('OVERLAPPING_STATE_ROOTS')
    included, excluded = [], []
    for root in roots:
        device = root.stat().st_dev
        def visit(path):
            st = path.lstat()
            if st.st_dev != device or os.path.ismount(str(path)) and path != root:
                raise ValueError('STATE_MOUNT_REQUIRES_EXPLICIT_SCOPE: ' + str(path))
            relative = path.relative_to(root)
            if stat.S_ISDIR(st.st_mode):
                if probe_directory(relative):
                    excluded.append({'path': str(path), 'reason': 'ephemeral-startup-probe'})
                    return
                included.append({'path': str(path), 'signature': signature(path)})
                children = sorted(path.iterdir())
                log = path / 'logs_2.sqlite'
                is_home = path.name == 'codex-home'  # never omit unrelated business logs
                omit_log = is_home and diagnostic_database(log)
                for child in children:
                    if omit_log and child.name in ('logs_2.sqlite', 'logs_2.sqlite-wal', 'logs_2.sqlite-shm') and child.is_file() and not child.is_symlink():
                        excluded.append({'path': str(child), 'reason': 'schema-confirmed-diagnostic-log'})
                    else: visit(child)
            elif stat.S_ISREG(st.st_mode) or stat.S_ISLNK(st.st_mode):
                included.append({'path': str(path), 'signature': signature(path)})
            elif stat.S_ISSOCK(st.st_mode):
                # A socket is not persisted recovery state. Fail until its owner
                # explicitly retires it; don't silently skip an unknown endpoint.
                raise ValueError('STATE_SOCKET_STILL_PRESENT: ' + str(path))
            else:
                raise ValueError('UNSUPPORTED_STATE_FILE: ' + str(path))
        visit(root)
    return {'policy': 'runtime-essential-state-v1', 'roots': list(map(str, roots)),
            'included': included, 'excluded': excluded,
            'includedRegularBytes': sum(r['signature'][5] for r in included if stat.S_ISREG(r['signature'][2]))}


def summary(snapshot):
    result = {key: value for key, value in snapshot.items() if key != 'included'}
    result['includedCount'] = len(snapshot['included'])
    result['selectionSha256'] = hashlib.sha256(json.dumps(snapshot['included'], sort_keys=True).encode()).hexdigest()
    return result


def write_state_archive(destination, roots, log, release_binding=None):
    """Use from the stopped, release-locked installer, BEFORE program switch.

    Keep the caller's existing tar/tar.gz format: savings come from selecting
    fewer members, never recompressing old backups. No
    automatic restore; a later state rollback needs compatibility assessment.
    Explicit member list prevents tar re-including omitted descendants.
    """
    destination = Path(destination)
    if destination.name not in ('state.tar', 'state.tar.gz') or destination.exists() or destination.is_symlink():
        raise ValueError('NEW_STATE_ARCHIVE_REQUIRED')
    for path in [destination.parent] + [Path(p) for p in roots]:
        if subprocess.check_output(['stat', '-f', '-c', '%T', str(path)]).decode().strip() in ('tmpfs', 'ramfs'):
            raise ValueError('STATE_BACKUP_REQUIRES_DISK')
    snapshot = plan(roots)
    if any(Path(root) == destination.parent or Path(root) in destination.parents for root in snapshot['roots']):
        raise ValueError('BACKUP_DESTINATION_INSIDE_SOURCE')
    receipt = destination.with_name('state-scope.json')
    if receipt.exists() or receipt.is_symlink(): raise ValueError('STATE_SCOPE_RECEIPT_EXISTS')
    names = b''.join(os.fsencode(row['path'].lstrip('/')) + b'\0' for row in snapshot['included'])
    try:
        compression = ['-I', 'gzip -1'] if destination.name.endswith('.gz') else []
        with destination.open('xb') as stream:
            os.chmod(str(destination), 0o600)
            subprocess.run(['tar', '--format=pax', '--acls', '--xattrs', '--sparse', '--no-recursion', '--null',
                            '--verbatim-files-from'] + compression + ['-cf', '-', '-C', '/', '-T', '-'],
                           input=names, stdout=stream, stderr=log, check=True)
            stream.flush(); os.fsync(stream.fileno())
        subprocess.run(['tar', '--acls', '--xattrs', '--compare'] + (['-z'] if compression else []) + ['-f', str(destination), '-C', '/'],
                       stdout=log, stderr=log, check=True)
        if snapshot != plan(roots): raise ValueError('STATE_CHANGED_DURING_BACKUP')
        digest = hashlib.sha256()
        with destination.open('rb') as stream:
            for chunk in iter(lambda: stream.read(1048576), b''): digest.update(chunk)
        snapshot['releaseBinding'] = release_binding or {}
        snapshot['archiveSha256'] = digest.hexdigest()
        snapshot['archiveBytes'] = destination.stat().st_size
        snapshot = summary(snapshot)
        # The archive SHA binds its full self-describing member list; don't
        # duplicate all per-file stat records in every backup's receipt.
        # Existing batch evidence, not a global registry. Never contains file data.
        with receipt.open('x') as stream:
            os.chmod(str(receipt), 0o600)
            json.dump(snapshot, stream, indent=2); stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
        fd = os.open(str(destination.parent), os.O_RDONLY | os.O_DIRECTORY)
        try: os.fsync(fd)
        finally: os.close(fd)
        return snapshot
    except BaseException:
        # Retain failed payload/evidence for the Owner. Never delete source data.
        raise
