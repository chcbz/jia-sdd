#!/usr/bin/python3
"""Retire only historical Runtime recovery payloads; never live state/programs.
Keep newest two payload-bearing batches AND current release's pinned backup.
Run on every host cleanup, independent of disk pressure. No tree retirement.
"""
import argparse
import fcntl
import json
import os
import pwd
from pathlib import Path
import re
import stat
import sys
import time
import importlib.util


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


safe = module('runtime_cache_safety', '/usr/local/libexec/cyf/rebuildable_cache_cleanup.py')
Unsafe = safe.Unsafe
PAYLOADS = ('state.tar', 'state.tar.gz', 'old-program.tar.gz')
MAX_FILES = 100000


class Paths(safe.Paths):
    def __init__(self):
        super().__init__()
        self.base = Path('/home/isp/baks/cyf-agent-runtime-v1')
        self.current = Path('/home/isp/apps/cyf-agent-runtime-v1/release-records/current.json')
        self.release_lock = Path('/run/lock/cyf-wuyong-versioned-release.lock')
        self.audit = Path('/home/isp/baks/host-cleanup/runtime-backups/audit.jsonl')


def directory(paths, p, runtime_record=False):
    # Check every physical ancestor, not just the final component.
    for d in reversed((p,) + tuple(p.parents)):
        st = d.lstat()
        legacy_apps = runtime_record and str(d) == '/home/isp/apps' and st.st_uid == pwd.getpwnam('isp').pw_uid
        if not stat.S_ISDIR(st.st_mode) or (st.st_uid != 0 and not legacy_apps) or st.st_mode & 0o022:
            raise Unsafe('unsafe directory: ' + str(d))
        if os.path.lexists(d / '.keep'):
            raise Unsafe('keep marker: ' + str(d))
    if p.stat().st_dev != paths.root_device or safe.mounted(paths, p):
        raise Unsafe('mounted/wrong device: ' + str(p))
    return p.stat()


def read_current(paths):
    directory(paths, paths.current.parent, runtime_record=True)
    ancestors = [(d, d.lstat().st_dev, d.lstat().st_ino) for d in paths.current.parents]
    st = safe.regular(paths.current)
    if st.st_size > 1024 * 1024:
        raise Unsafe('oversized release record')
    fd = os.open(paths.current, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd) as f:
        if safe.signature(os.fstat(f.fileno())) != safe.signature(st):
            raise Unsafe('release record replaced')
        data = json.load(f)
        if safe.signature(os.fstat(f.fileno())) != safe.signature(st):
            raise Unsafe('release record changed')
    if safe.signature(paths.current.lstat()) != safe.signature(st):
        raise Unsafe('release record replaced')
    for d, dev, ino in ancestors:
        current = d.lstat()
        if not stat.S_ISDIR(current.st_mode) or (current.st_dev, current.st_ino) != (dev, ino):
            raise Unsafe('release record ancestor replaced')
    # Unknown/unverified activation fails closed. No inferred success from idle.
    if data.get('status') != 'verified-active':
        raise Unsafe('current Runtime release is not verified-active')
    pin = Path(data.get('backup', ''))
    if pin.parent != paths.base or not re.fullmatch(r'20\d{6}-[A-Za-z0-9_.-]+', pin.name):
        raise Unsafe('missing/invalid pinned Runtime recovery batch')
    directory(paths, pin)
    return pin, safe.signature(st)


def leaf(paths, p, shared=False):
    directory(paths, p.parent)
    st = p.lstat()
    if not (stat.S_ISREG(st.st_mode) or stat.S_ISLNK(st.st_mode)):
        raise Unsafe('non-payload file type')
    if st.st_uid != 0 or (st.st_nlink != 1 and not (shared and stat.S_ISREG(st.st_mode))) or (not stat.S_ISLNK(st.st_mode) and st.st_mode & 0o022):
        raise Unsafe('unsafe payload ownership/links/mode')
    if st.st_dev != paths.root_device or safe.mounted(paths, p):
        raise Unsafe('mounted payload')
    return st


def collect_batch(paths, batch):
    directory(paths, batch)
    # Known recovery layout only. Preserve RECOVERY, manifests, records, evidence.
    for n in ('RECOVERY.md', 'current.json'):
        safe.regular(batch / n)
    selected = [batch / n for n in PAYLOADS if os.path.lexists(batch / n)]
    old = batch / 'old-program'
    if os.path.lexists(old):
        directory(paths, old)
        def fail(error):
            raise error
        for d, dirs, files in os.walk(old, followlinks=False, onerror=fail):
            d = Path(d)
            directory(paths, d)
            if len(d.relative_to(old).parts) > 20:
                raise Unsafe('payload depth limit')
            links = [n for n in dirs if (d / n).is_symlink()]
            dirs[:] = [n for n in dirs if n not in links]
            selected.extend(d / n for n in files + links)
            if len(selected) > MAX_FILES:
                raise Unsafe('payload entry limit; no partial batch')
    rows, groups = [], {}
    for p in selected:
        # Sharing is only supported inside one retired installation, never for
        # state archives or aliases into another release/live program.
        st = leaf(paths, p, old in p.parents)
        row = {'path': str(p), 'signature': safe.signature(st), 'allocated': st.st_blocks * 512}
        rows.append(row)
        if stat.S_ISREG(st.st_mode):
            groups.setdefault((st.st_dev, st.st_ino), []).append(row)
    for aliases in groups.values():
        if len(aliases) != aliases[0]['signature'][5]:
            raise Unsafe('payload hardlink escapes old-program')
        if len(aliases) > 1:
            for row in aliases:
                if old not in Path(row['path']).parents or row['signature'] != aliases[0]['signature']:
                    raise Unsafe('payload hardlink changed/outside old-program')
                row['shared'] = True
                row['allocated'] = 0
            # Space is reclaimed only when the last directory entry is removed.
            aliases[-1]['allocated'] = Path(aliases[-1]['path']).lstat().st_blocks * 512
    return rows


def retirement_record(batch):
    """Completed retirement records are immutable tombstones, never reused roots.
    Ignore any later additions to such roots (preserve, do not auto-delete them).
    """
    marker = batch / 'PAYLOAD_RETIRED.json'
    if not os.path.lexists(marker):
        return {}
    st = safe.regular(marker)
    if st.st_size > 4096:
        raise Unsafe('oversized retirement marker')
    fd = os.open(marker, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd) as f:
        if safe.signature(os.fstat(f.fileno())) != safe.signature(st):
            raise Unsafe('retirement marker replaced')
        value = json.load(f)
        if safe.signature(os.fstat(f.fileno())) != safe.signature(st):
            raise Unsafe('retirement marker changed')
    if safe.signature(marker.lstat()) != safe.signature(st):
        raise Unsafe('retirement marker replaced')
    return value


def retired_batch(batch):
    value = retirement_record(batch)
    return (value.get('status') == 'retired-not-a-complete-recovery'
            and value.get('policy') == 'newest-two-plus-current-pin')


def collect(paths, usage, now=None):
    now = time.time() if now is None else now
    directory(paths, paths.base)
    pin, current_sig = read_current(paths)
    batches = []
    skips = []
    entries = list(paths.base.iterdir())
    if len(entries) > 10000:
        raise Unsafe('metadata entry limit exceeded')
    unretired = 0
    for batch in entries:
        if not re.fullmatch(r'20\d{6}-[A-Za-z0-9_.-]+', batch.name):
            continue
        try:
            directory(paths, batch)
            retirement = retirement_record(batch)
            if (retirement.get('status') == 'retired-not-a-complete-recovery'
                    and retirement.get('policy') == 'newest-two-plus-current-pin'):
                continue
            unretired += 1
            if unretired > 512:
                raise Unsafe('unretired batch limit exceeded')
            rows = collect_batch(paths, batch)
            if rows:
                # File times, never directory mtime (deletion changes directory mtime).
                stamp = max(r['signature'][8] / 1e9 for r in rows)
                # Our own hardlink unlinks change survivor ctime. An interrupted
                # retirement must not become a newer-than-pin recovery forever.
                # Reuse only this directory's original, protected intent stamp.
                if (retirement.get('status') == 'retiring-not-a-complete-recovery'
                        and retirement.get('policy') == 'newest-two-plus-current-pin'
                        and retirement.get('batchIdentity') == list(safe.signature(batch.lstat())[:2])
                        and isinstance(retirement.get('payloadStamp'), (int, float))
                        and 0 < retirement['payloadStamp'] <= stamp
                        and all(r['signature'][7] / 1e9 <= retirement['payloadStamp'] for r in rows)):
                    stamp = retirement['payloadStamp']
                batches.append({'batch': str(batch), 'stamp': stamp, 'rows': rows,
                                'identity': safe.signature(batch.lstat())[:2]})
        except (OSError, Unsafe) as e:
            if unretired > 512:
                raise Unsafe('unretired batch limit exceeded')
            # Unsafe batches still reserve a newest slot, so failures cannot evict
            # the real newest recoveries. Use top-level metadata conservatively.
            skips.append({'batch': str(batch), 'reason': str(e)})
            stamp = max(batch.lstat().st_ctime, batch.lstat().st_mtime)
            batches.append({'batch': str(batch), 'stamp': stamp, 'rows': [], 'unsafe': True})
    batches.sort(key=lambda x: (x['stamp'], x['batch']), reverse=True)
    protected = {b['batch'] for b in batches[:2]} | {str(pin)}
    # Never prune newer-than-current backup attempts, even beyond newest two.
    pin_stamp = next((b['stamp'] for b in batches if b['batch'] == str(pin)), None)
    if pin_stamp is None:
        raise Unsafe('pinned recovery payload is missing')
    eligible = []
    for b in batches:
        if b.get('unsafe') or b['batch'] in protected:
            continue
        if b['stamp'] > pin_stamp or now - b['stamp'] < 3600:
            skips.append({'batch': b['batch'], 'reason': 'recent/newer-than-current recovery'})
            continue
        if usage.used(Path(b['batch'])) or any(tuple(r['signature'][:2]) in usage.inodes for r in b['rows']):
            skips.append({'batch': b['batch'], 'reason': 'active recovery'})
            continue
        eligible.append(b)
    return eligible, sorted(protected), skips, current_sig


def unlink(paths, row, remaining=None):
    p = Path(row['path'])
    shared = row.get('shared', False)
    aliases = (remaining or {}).get(tuple(row['signature'][:2]), []) if shared else []
    if shared and (len(aliases) != row['signature'][5] or row not in aliases):
        raise Unsafe('missing payload hardlink closure')
    if safe.signature(leaf(paths, p, shared)) != tuple(row['signature']):
        raise Unsafe('payload changed before unlink')
    # Anchor every parent with O_NOFOLLOW. Never follow archived symlinks.
    fd = os.open('/', os.O_RDONLY | os.O_DIRECTORY)
    chain = []
    try:
        parent = Path('/')
        for name in p.parent.parts[1:]:
            child = os.open(name, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW, dir_fd=fd)
            os.close(fd)
            fd = child
            parent /= name
            st = os.fstat(fd)
            chain.append((parent, st.st_dev, st.st_ino))
        for parent, dev, ino in chain:
            st = parent.lstat()
            if not stat.S_ISDIR(st.st_mode) or (st.st_dev, st.st_ino) != (dev, ino):
                raise Unsafe('parent replaced')
        if safe.signature(os.stat(p.name, dir_fd=fd, follow_symlinks=False)) != tuple(row['signature']):
            raise Unsafe('anchored payload changed')
        if shared:
            # Hold the inode while unlink changes nlink/ctime. Advance only
            # those expected fields on our remaining aliases, not arbitrary
            # replacement metadata. External links/writes still fail closed.
            held = os.open(p.name, os.O_RDONLY | os.O_NOFOLLOW, dir_fd=fd)
            try:
                before = tuple(row['signature'])
                if safe.signature(os.fstat(held)) != before:
                    raise Unsafe('shared payload changed')
                os.unlink(p.name, dir_fd=fd)
                after = safe.signature(os.fstat(held))
                if after[5] != before[5] - 1 or after[:5] != before[:5] or after[6:8] != before[6:8]:
                    raise Unsafe('shared payload changed while unlinking')
                aliases.remove(row)
                for alias in aliases:
                    alias['signature'] = after
            finally:
                os.close(held)
        else:
            os.unlink(p.name, dir_fd=fd)
    finally:
        os.close(fd)


def run(paths, mode, inherited=None):
    fds = []
    auditfd = None
    result = {'stage': 'runtime_backups', 'mode': mode, 'removed_files': 0,
              'reclaimed_allocated_bytes': 0, 'retired_batches': []}
    try:
        for lock, inherit in ((paths.lock, inherited), (paths.release_lock, None)):
            before = safe.regular(lock)
            fd = os.dup(inherit) if inherit is not None else os.open(lock, os.O_RDWR | os.O_NOFOLLOW)
            fds.append(fd)
            if safe.signature(os.fstat(fd)) != safe.signature(before):
                raise Unsafe('lock identity changed')
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                return dict(result, skipped='cleanup/release in progress')
            if safe.signature(lock.lstat()) != safe.signature(before):
                raise Unsafe('lock replaced')
        batches, protected, skips, current_sig = collect(paths, safe.proc.snapshot(paths.proc))
        result.update(protected=protected, skipped=skips, eligible_batches=[b['batch'] for b in batches],
                      estimated_reclaim_bytes=sum(r['allocated'] for b in batches for r in b['rows']))
        if mode == 'plan' or not batches:
            return result
        if not paths.audit.parent.exists():
            paths.audit.parent.mkdir(mode=0o700)
        directory(paths, paths.audit.parent)
        safe.logger.LOG = paths.audit
        auditfd = safe.logger.rotate_log(safe.logger.open_log(paths.audit))
        def audit(value):
            nonlocal auditfd
            auditfd = safe.logger.rotate_log(auditfd)
            safe.logger.validate_log(auditfd)
            data = memoryview((json.dumps(value) + '\n').encode())
            while data:
                n = os.write(auditfd, data)
                if n <= 0:
                    raise OSError('audit write failed')
                data = data[n:]
            os.fsync(auditfd)
        for b in batches:
            batch = Path(b['batch'])
            directory(paths, batch)
            if safe.signature(batch.lstat())[:2] != tuple(b['identity']):
                raise Unsafe('backup batch replaced')
            # Durable marker BEFORE first deletion: interrupted runs must not
            # advertise a partially retired archive as a usable recovery point.
            audit({'retirement_intent': str(batch), 'time': time.time()})
            safe.atomic_json(batch / 'PAYLOAD_RETIRED.json', {
                'status': 'retiring-not-a-complete-recovery', 'time': time.time(),
                'payloadStamp': b['stamp'], 'batchIdentity': list(b['identity']),
                'policy': 'newest-two-plus-current-pin', 'audit': str(paths.audit)})
            remaining = {}
            for row in b['rows']:
                if row.get('shared'):
                    remaining.setdefault(tuple(row['signature'][:2]), []).append(row)
            for i in range(0, len(b['rows']), 100):
                fresh = safe.proc.snapshot(paths.proc)
                if fresh.used(batch):
                    raise Unsafe('backup became active')
                if read_current(paths)[1] != current_sig:
                    raise Unsafe('current release changed')
                chunk = b['rows'][i:i + 100]
                if any(tuple(r['signature'][:2]) in fresh.inodes for r in chunk):
                    raise Unsafe('payload inode became active')
                audit({'intent': chunk})
                done = []
                try:
                    for row in chunk:
                        unlink(paths, row, remaining)
                        result['removed_files'] += 1
                        result['reclaimed_allocated_bytes'] += row['allocated']
                        done.append(row['path'])
                finally:
                    audit({'removed': done})
            safe.atomic_json(batch / 'PAYLOAD_RETIRED.json', {
                'status': 'retired-not-a-complete-recovery', 'time': time.time(),
                'policy': 'newest-two-plus-current-pin', 'audit': str(paths.audit)})
            result['retired_batches'].append(str(batch))
            audit({'batch_complete': str(batch)})
        return result
    finally:
        if auditfd is not None:
            os.close(auditfd)
        for fd in reversed(fds):
            os.close(fd)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('mode', choices=['plan', 'clean'])
    p.add_argument('--host-lock-fd', type=int)
    args = p.parse_args()
    if os.geteuid() != 0 or (args.host_lock_fd is not None and args.host_lock_fd < 3):
        p.error('root and a valid inherited lock FD required')
    try:
        print(json.dumps(run(Paths(), args.mode, args.host_lock_fd)))
        return 0
    except (OSError, Unsafe, ValueError, KeyError, TypeError) as e:
        print('Runtime backup cleanup stopped safely: ' + str(e), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
