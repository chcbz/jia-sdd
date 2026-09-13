#!/usr/bin/env python3
"""Fixed read-only capacity and deployment-layout probe; no subprocess or raw configs; bounded metadata sizes."""
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import stat
import time

HELPERS = {
    '/usr/local/sbin/cyf-api-flow-deploy': '22d078b96c55b8a053cee8756323e18dc06bef6ea609ade81eaaf2d16726f5c9',
    '/usr/local/sbin/cyf-web-flow-deploy': '53070ba8cf924852744e38c232d0b5d5b3fd432e0d05c90b8f9a877af21b9bb6',
}
PREFIXES = ('/home/isp/hosts/cyf/', '/var/lib/cyf-api-flow/', '/var/lib/cyf-web-flow/', '/home/isp/apps/', '/etc/systemd/system/', '/opt/cyf/', '/opt/cyf-api/', '/opt/cyf-web/', '/usr/local/libexec/')


def bounded(path, limit):
    with open(path, 'rb') as f:
        data = f.read(limit + 1)
    if len(data) > limit:
        raise ValueError('oversize')
    return data


def safe_path(value):
    return (bool(re.fullmatch(r'/[A-Za-z0-9_./-]+', value))
            and os.path.normpath(value) == value
            and not any(part in ('.', '..') for part in value.split('/'))
            and value.startswith(PREFIXES)
            and not re.search(r'password|secret|token|credential|\.pass', value, re.I))



def allocated_tree(path, deadline):
    total = 0
    count = 0
    stack = [Path(path)]
    device = os.lstat(path).st_dev
    while stack:
        if time.monotonic() > deadline or count >= 50000:
            return {'allocatedBytes': total, 'entries': count, 'complete': False}
        item = stack.pop()
        info = item.lstat()
        count += 1
        if info.st_dev != device:
            continue
        total += info.st_blocks * 512
        if stat.S_ISDIR(info.st_mode):
            with os.scandir(item) as entries:
                for entry in entries:
                    if time.monotonic() > deadline or len(stack) + count >= 50000:
                        return {'allocatedBytes': total, 'entries': count, 'complete': False}
                    stack.append(Path(entry.path))
    return {'allocatedBytes': total, 'entries': count, 'complete': True}


def deployment_disk():
    report = []
    deadline = time.monotonic() + 30
    for path in ['/var/lib/cyf-api-flow/downloads', '/var/lib/cyf-api-flow/releases',
                 '/var/lib/cyf-web-flow/downloads', '/var/lib/cyf-web-flow/releases',
                 '/home/isp/hosts/cyf/api', '/opt/cyf/output-scanner',
                 '/var/lib/cyf-output-scanner', '/opt/cyf', '/var/lib/cyf-api-flow',
                 '/var/lib/cyf-web-flow', '/home/isp/hosts/cyf/web/kit']:
        row = {'path': path}
        if time.monotonic() > deadline:
            report.append({'path': path, 'status': 'scan_budget_exhausted', 'truncated': True})
            break
        try:
            info = os.lstat(path)
            if not stat.S_ISDIR(info.st_mode):
                row['directory'] = False
                report.append(row)
                continue
            disk = os.statvfs(path)
            row.update(device=info.st_dev, totalBytes=disk.f_blocks*disk.f_frsize,
                       availableBytes=disk.f_bavail*disk.f_frsize)
            row['children'] = []
            with os.scandir(path) as entries:
                for entry in entries:
                    if len(row['children']) >= 80 or time.monotonic() > deadline:
                        row['truncated'] = True
                        break
                    if not re.fullmatch('[A-Za-z0-9_.-]{1,100}', entry.name) or re.search(
                            'password|secret|token|credential|config|properties|yaml|yml', entry.name, re.I):
                        continue
                    i = entry.stat(follow_symlinks=False)
                    item = {'name': entry.name, 'uid': i.st_uid, 'mode': oct(stat.S_IMODE(i.st_mode)),
                            'mtimeEpoch': int(i.st_mtime), 'symlink': stat.S_ISLNK(i.st_mode)}
                    if stat.S_ISDIR(i.st_mode):
                        item.update(allocated_tree(entry.path, deadline))
                    elif stat.S_ISREG(i.st_mode):
                        item.update(allocatedBytes=i.st_blocks*512, bytes=i.st_size)
                    row['children'].append(item)
        except (OSError, ValueError):
            row['status'] = 'missing_or_unreadable'
        report.append(row)
    return report



def cache_fingerprints():
    rows = []
    deadline = time.monotonic() + 120
    for run in [93, 95, 96, 98, 99]:
        path = Path('/var/lib/cyf-web-flow/downloads')/str(run)/'package.tgz'
        row = {'run': run, 'path': str(path), 'complete': False}
        try:
            for parent in [path.parent.parent, path.parent]:
                info = parent.lstat()
                if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or stat.S_IMODE(info.st_mode)&0o022:
                    raise ValueError('cache_parent_identity')
            fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(fd, 'rb') as f:
                before = os.fstat(f.fileno())
                if not stat.S_ISREG(before.st_mode) or before.st_uid != 0 or before.st_size > 128*1024**2:
                    raise ValueError('cache_file_identity')
                h = hashlib.sha256()
                while True:
                    if time.monotonic() > deadline:
                        raise ValueError('cache_hash_budget')
                    chunk = f.read(1024*1024)
                    if not chunk:
                        break
                    h.update(chunk)
                after = path.lstat()
                if (before.st_dev,before.st_ino,before.st_size,before.st_mtime_ns) != (
                        after.st_dev,after.st_ino,after.st_size,after.st_mtime_ns):
                    raise ValueError('cache_file_changed')
            row.update(complete=True,sha256=h.hexdigest(),bytes=before.st_size,
                       device=before.st_dev,inode=before.st_ino,nlink=before.st_nlink,
                       mode=oct(stat.S_IMODE(before.st_mode)),uid=before.st_uid,gid=before.st_gid,
                       mtimeNs=before.st_mtime_ns)
        except (OSError,ValueError):
            row['status'] = 'not_fingerprinted'
        rows.append(row)
    return rows


def main():
    report = {'observedAtEpoch': int(time.time()), 'architecture': platform.machine(), 'readOnly': True}
    try:
        fields = {}
        for line in bounded('/etc/os-release', 16384).decode().splitlines():
            key, sep, value = line.partition('=')
            value = value.strip('"')
            if sep and key in ('ID', 'VERSION_ID', 'ID_LIKE') and re.fullmatch(r'[A-Za-z0-9_. -]{1,100}', value):
                fields[key] = value
        report['os'] = fields
    except (OSError, ValueError, UnicodeError):
        report['os'] = {'status': 'unreadable'}
    try:
        fields = {}
        for line in bounded('/proc/meminfo', 16384).decode().splitlines():
            match = re.fullmatch(r'(MemTotal|MemAvailable|SwapTotal|SwapFree):\s+(\d+) kB', line)
            if match:
                fields[match[1] + 'Bytes'] = int(match[2]) * 1024
        report['memory'] = fields
    except (OSError, ValueError, UnicodeError):
        report['memory'] = {'status': 'unreadable'}
    report['helpers'] = []
    for name, expected in HELPERS.items():
        row = {'path': name}
        try:
            data = bounded(name, 1024 * 1024)
            digest = hashlib.sha256(data).hexdigest()
            row.update(sha256=digest, expectedHashMatches=digest == expected)
            if digest != expected:
                row['status'] = 'changed_since_prior_probe'
            else:
                source = data.decode('utf-8')
                paths = sorted(set(p for p in re.findall(r'/[A-Za-z0-9_./-]+', source) if safe_path(p)))
                row['literalPaths'] = paths[:60]
                row['pathsTruncated'] = len(paths) > 60
                row['uses'] = {word: bool(re.search(r'\b' + re.escape(word) + r'\b', source)) for word in
                               ('systemctl', 'nohup', 'java', 'spring.config', 'rollback', 'backup')}
        except (OSError, ValueError, UnicodeError):
            row['status'] = 'unreadable'
        report['helpers'].append(row)
    report['javaJars'] = []
    for pid in Path('/proc').iterdir():
        if not pid.name.isdecimal():
            continue
        try:
            if bounded(pid / 'comm', 17).rstrip(b'\n') != b'java':
                continue
            args = [part.decode('utf-8') for part in bounded(pid / 'cmdline', 65536).split(b'\0') if part]
            if not args or Path(args[0]).name != 'java':
                continue
            for index, arg in enumerate(args):
                if index == 0 or args[index-1] != '-jar' or not re.fullmatch(r'[A-Za-z0-9_./-]+\.jar', arg):
                    continue
                if any(part in ('.', '..') for part in arg.split('/')):
                    continue
                candidate = arg if arg.startswith('/') else str(Path(os.readlink(pid / 'cwd')) / arg)
                if not safe_path(candidate):
                    continue
                info = os.lstat(candidate)
                ticks = bounded(pid / 'stat', 16384).decode().split(') ', 1)[1].split()[19]
                report['javaJars'].append({'pid': int(pid.name), 'startTicks': ticks,
                                           'jarPath': candidate, 'sizeBytes': info.st_size})
        except (OSError, ValueError, UnicodeError, IndexError):
            continue
    report['deploymentDisk'] = deployment_disk()
    report['cacheFingerprints'] = cache_fingerprints()
    report['limits'] = ['Only OS ID/version and selected numeric meminfo fields are exported.',
                        'Helper contents and bounded Java arguments are inspected in memory; raw text is not exported.',
                        'No application config/environment, network connection, subprocess, installation or restart.',
                        'No service readiness, backup, storage/scanner or release gate is closed.']
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
