#!/usr/bin/env python3
"""Remove five exact off-host-backed-up download caches, under the Web deploy lock."""
import fcntl
import hashlib
import json
import os
from pathlib import Path
import signal
import stat
import time

PLAN = [{'bytes': 104222372, 'complete': True, 'device': 64769, 'gid': 0, 'inode': 394846, 'mode': '0o644', 'mtimeNs': 1789214540000000000, 'nlink': 1, 'path': '/var/lib/cyf-web-flow/downloads/93/package.tgz', 'run': 93, 'sha256': '0ece2d5e0d2e333cfe5259ea654689fcc878b7f06ff91c49b81d5851dbcb1600', 'uid': 0}, {'bytes': 104244925, 'complete': True, 'device': 64769, 'gid': 0, 'inode': 454305, 'mode': '0o644', 'mtimeNs': 1789227576000000000, 'nlink': 1, 'path': '/var/lib/cyf-web-flow/downloads/95/package.tgz', 'run': 95, 'sha256': '6f0f6913f11b288f45d346fb575f4f6f867fb9d57d5564896c1a63f5766c27c0', 'uid': 0}, {'bytes': 104243370, 'complete': True, 'device': 64769, 'gid': 0, 'inode': 394667, 'mode': '0o644', 'mtimeNs': 1789263102000000000, 'nlink': 1, 'path': '/var/lib/cyf-web-flow/downloads/96/package.tgz', 'run': 96, 'sha256': '3b68e16aedd732c473147e4e0ff691117571bec7af3f9498b00e8d038b3aa253', 'uid': 0}, {'bytes': 104251760, 'complete': True, 'device': 64769, 'gid': 0, 'inode': 394783, 'mode': '0o644', 'mtimeNs': 1789266385000000000, 'nlink': 1, 'path': '/var/lib/cyf-web-flow/downloads/98/package.tgz', 'run': 98, 'sha256': '10781a487cae29e80a92641b7313f355f1ac4849201638291f562177aece8cd6', 'uid': 0}, {'bytes': 104273152, 'complete': True, 'device': 64769, 'gid': 0, 'inode': 395235, 'mode': '0o644', 'mtimeNs': 1789269693000000000, 'nlink': 1, 'path': '/var/lib/cyf-web-flow/downloads/99/package.tgz', 'run': 99, 'sha256': 'b57049c1c0d4772b187cdfa41d4ebca659a24357ee18d66a25f073106fe1d5a9', 'uid': 0}]
BASE = Path('/var/lib/cyf-web-flow')
SITE = Path('/home/isp/hosts/cyf/web/kit')
INTENT = Path('/opt/cyf/output-cache-prune-intent.json')
RECEIPT = Path('/opt/cyf/output-cache-prune-result.json')
FAILURE = Path('/opt/cyf/output-cache-prune-failure.json')
JOURNAL = Path('/opt/cyf/output-cache-prune-journal.jsonl')
HELPER_SHA = '53070ba8cf924852744e38c232d0b5d5b3fd432e0d05c90b8f9a877af21b9bb6'


def require(ok, code):
    if not ok:
        raise RuntimeError(code)


def safe_dir(path):
    info = path.lstat()
    require(stat.S_ISDIR(info.st_mode) and info.st_uid == 0 and info.st_gid == 0
            and not stat.S_IMODE(info.st_mode) & 0o022, 'directory_identity')
    return os.open(str(path), os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW)


def identity(info):
    return (info.st_dev, info.st_ino, info.st_size, info.st_mtime_ns,
            info.st_uid, info.st_gid, stat.S_IMODE(info.st_mode), info.st_nlink)


def parent_identity(info):
    return (info.st_dev,info.st_ino,info.st_uid,info.st_gid,stat.S_IMODE(info.st_mode))


def digest(fd, maximum):
    os.lseek(fd, 0, os.SEEK_SET)
    h = hashlib.sha256()
    size = 0
    while True:
        chunk = os.read(fd, 1024*1024)
        if not chunk:
            break
        size += len(chunk)
        require(size <= maximum, 'hash_bound')
        h.update(chunk)
    return h.hexdigest()


def protected_fingerprint(path, maximum):
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
    try:
        before = os.fstat(fd)
        require(stat.S_ISREG(before.st_mode) and before.st_uid == 0
                and before.st_size <= maximum, 'protected_file_identity')
        h = digest(fd, maximum)
        require(identity(before) == identity(path.lstat()), 'protected_file_changed')
        return {'identity': identity(before), 'sha256': h}
    finally:
        os.close(fd)


def no_open_references(targets):
    checked = 0
    for process in Path('/proc').iterdir():
        if not process.name.isdecimal() or int(process.name) == os.getpid():
            continue
        try:
            with os.scandir(process/'fd') as entries:
                for entry in entries:
                    checked += 1
                    require(checked <= 100000, 'fd_scan_bound')
                    try:
                        info = os.stat(entry.path)
                    except FileNotFoundError:
                        continue
                    require((info.st_dev, info.st_ino) not in targets, 'cache_open_elsewhere')
        except FileNotFoundError:
            continue
    return checked


def no_site_references(targets):
    stack = [SITE]
    count = 0
    while stack:
        path = stack.pop()
        info = path.lstat()
        count += 1
        require(count <= 20000, 'site_scan_bound')
        if stat.S_ISLNK(info.st_mode):
            resolved = os.path.realpath(path)
            require(not any(x['path'] == resolved or x['path'].startswith(resolved.rstrip('/')+'/')
                            for x in PLAN), 'cache_site_reference')
            try:
                followed = path.stat()
            except FileNotFoundError:
                continue
            require((followed.st_dev, followed.st_ino) not in targets, 'cache_site_reference')
        elif stat.S_ISDIR(info.st_mode):
            with os.scandir(path) as entries:
                for entry in entries:
                    require(len(stack)+count < 20000, 'site_scan_bound')
                    stack.append(Path(entry.path))
        else:
            require((info.st_dev, info.st_ino) not in targets, 'cache_site_reference')
    return count


def exclusive(path, value):
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'w') as f:
        json.dump(value, f, sort_keys=True)
        f.write('\n')
        f.flush()
        os.fsync(f.fileno())
    parent = safe_dir(path.parent)
    try:
        os.fsync(parent)
    finally:
        os.close(parent)


def journal(fd, value):
    data = (json.dumps(value, sort_keys=True)+'\n').encode()
    while data:
        n = os.write(fd, data)
        require(n > 0, 'journal_short_write')
        data = data[n:]
    os.fsync(fd)


def reconcile(rows):
    states = []
    for row in rows:
        state = {'run': row['run'], 'path': row['path'], 'state': 'UNKNOWN'}
        try:
            directory = row['_directoryFd']
            require(parent_identity(os.fstat(directory)) == row['_parentIdentity'], 'parent_changed')
            try:
                info = os.stat('package.tgz', dir_fd=directory, follow_symlinks=False)
            except FileNotFoundError:
                state['state'] = 'MISSING'
            else:
                expected = (row['device'],row['inode'],row['bytes'],row['mtimeNs'],0,0,0o644,1)
                if stat.S_ISREG(info.st_mode) and identity(info) == expected:
                    fd = os.open('package.tgz', os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
                    try:
                        state['state'] = 'ORIGINAL' if identity(os.fstat(fd)) == expected and digest(fd,128*1024**2) == row['sha256'] else 'CHANGED'
                    finally:
                        os.close(fd)
                else:
                    state['state'] = 'CHANGED'
            os.fsync(directory)
            state['parentFsynced'] = True
        except (OSError,RuntimeError,KeyError) as exc:
            state['reconciliationError'] = type(exc).__name__
            state['parentFsynced'] = False
        states.append(state)
    return states


def available():
    s = os.statvfs(BASE)
    return s.f_bavail*s.f_frsize


def main():
    result = {'startedAtEpoch': int(time.time()), 'status': 'UNKNOWN',
              'removed': [], 'apiRestartRequested': False,
              'scope': 'Five backed-up Web download cache files only; no runtime/backup deletion'}
    handles = []
    lock = None
    journal_fd = None
    intent_created = False
    def expired(signum, frame):
        raise RuntimeError('cleanup_deadline')
    for sig in (signal.SIGALRM, signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, expired)
    signal.alarm(240)
    try:
        require(os.geteuid() == 0 and [x['run'] for x in PLAN] == [93,95,96,98,99], 'fixed_scope')
        for parent in [Path('/var'), Path('/var/lib'), BASE, BASE/'downloads',
                       Path('/opt'), Path('/opt/cyf')]:
            fd = safe_dir(parent)
            os.close(fd)
        si = SITE.lstat()
        require(stat.S_ISDIR(si.st_mode) and si.st_uid in (0,1000)
                and not stat.S_IMODE(si.st_mode)&0o002, 'site_directory_identity')
        require(not any(os.path.lexists(p) for p in (INTENT,RECEIPT,FAILURE,JOURNAL)), 'prior_cleanup_intent')
        helper = protected_fingerprint(Path('/usr/local/sbin/cyf-web-flow-deploy'), 1024*1024)
        require(helper['sha256'] == HELPER_SHA, 'deploy_helper_changed')
        lock = os.open(str(BASE/'deploy.lock'), os.O_RDONLY | os.O_NOFOLLOW)
        li = os.fstat(lock)
        require(stat.S_ISREG(li.st_mode) and li.st_uid == 0 and li.st_gid == 0
                and stat.S_IMODE(li.st_mode) == 0o600 and li.st_nlink == 1, 'deploy_lock_identity')
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        protected_paths = [(SITE/'index.html', 1024*1024), (BASE/'record.json', 1024*1024),
                           (BASE/'downloads/100/package.tgz', 128*1024**2),
                           (BASE/'downloads/102/package.tgz', 128*1024**2)]
        before_protected = {str(p): protected_fingerprint(p, limit) for p,limit in protected_paths}
        targets = set()
        for row in PLAN:
            parent = BASE/'downloads'/str(row['run'])
            require(row['path'] == str(parent/'package.tgz'), 'plan_path')
            directory = safe_dir(parent)
            handles.append(directory)
            fd = os.open('package.tgz', os.O_RDONLY | os.O_NOFOLLOW, dir_fd=directory)
            handles.append(fd)
            info = os.fstat(fd)
            expected = (row['device'],row['inode'],row['bytes'],row['mtimeNs'],0,0,0o644,1)
            require(stat.S_ISREG(info.st_mode) and identity(info) == expected, 'cache_identity_changed')
            require(digest(fd, 128*1024**2) == row['sha256'], 'cache_hash_changed')
            targets.add((info.st_dev,info.st_ino))
            row['_directoryFd'], row['_fileFd'] = directory, fd
            row['_parentIdentity'] = parent_identity(os.fstat(directory))
        result['checkedOpenDescriptors'] = no_open_references(targets)
        result['checkedSiteEntries'] = no_site_references(targets)
        result['availableBefore'] = available()
        result['protectedBefore'] = before_protected
        result['targets'] = [{**{k:v for k,v in row.items() if not k.startswith('_')},
                              'parentIdentity':row['_parentIdentity']} for row in PLAN]
        exclusive(INTENT, result)
        intent_created = True
        journal_fd = os.open(JOURNAL, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        journal(journal_fd, {'phase':'PREPARED','targets':result['targets']})
        parent = safe_dir(JOURNAL.parent)
        try:
            os.fsync(parent)
        finally:
            os.close(parent)
        for row in PLAN:
            expected = (row['device'],row['inode'],row['bytes'],row['mtimeNs'],0,0,0o644,1)
            require(identity(os.fstat(row['_fileFd'])) == expected
                    and identity(os.stat('package.tgz', dir_fd=row['_directoryFd'],
                                         follow_symlinks=False)) == expected, 'cache_replaced')
            journal(journal_fd, {'run':row['run'],'phase':'BEFORE_UNLINK'})
            os.unlink('package.tgz', dir_fd=row['_directoryFd'])
            os.fsync(row['_directoryFd'])
            journal(journal_fd, {'run':row['run'],'phase':'AFTER_UNLINK_PARENT_FSYNC'})
        after_protected = {str(p): protected_fingerprint(p, limit) for p,limit in protected_paths}
        require(after_protected == before_protected, 'protected_file_changed')
        result['protectedUnchanged'] = True
        result['operationChecksPassed'] = True
    except (OSError, ValueError, RuntimeError) as exc:
        result['errorType'] = type(exc).__name__
        if isinstance(exc, OSError):
            result['errno'] = exc.errno
        if type(exc) is RuntimeError:
            result['errorCode'] = str(exc)
    finally:
        signal.alarm(0)
        signal.pthread_sigmask(signal.SIG_BLOCK, {signal.SIGALRM,signal.SIGTERM,signal.SIGINT})
        if intent_created:
            result['reconciledTargets'] = reconcile(PLAN)
            result['removed'] = [{k:row[k] for k in ('run','bytes','sha256')} for row,state in zip(PLAN,result['reconciledTargets']) if state['state'] == 'MISSING']
            result['allMissingDurable'] = all(x['state'] == 'MISSING' and x.get('parentFsynced') for x in result['reconciledTargets'])
        for fd in handles:
            os.close(fd)
        result['availableAfter'] = available()
        if intent_created:
            try:
                if result.get('operationChecksPassed') and result['allMissingDurable'] and not result.get('errorType'):
                    result['status'] = 'BACKED_UP_CACHE_FILES_REMOVED'
                if journal_fd is not None:
                    journal(journal_fd, {'phase':'FINAL_RECONCILIATION','status':result['status'],'targets':result['reconciledTargets']})
                exclusive(RECEIPT if result['status'] == 'BACKED_UP_CACHE_FILES_REMOVED' else FAILURE, result)
                result['durableResultWritten'] = True
            except (OSError,RuntimeError) as exc:
                result['status'] = 'UNKNOWN'
                result['durableResultWritten'] = False
                result['finalizationError'] = type(exc).__name__
        if journal_fd is not None:
            os.close(journal_fd)
        if lock is not None:
            os.close(lock)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] == 'BACKED_UP_CACHE_FILES_REMOVED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
