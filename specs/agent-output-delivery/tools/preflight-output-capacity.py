#!/usr/bin/env python3
"""Fixed read-only capacity and deployment-layout probe; no subprocess or raw configs."""
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import time

HELPERS = {
    '/usr/local/sbin/cyf-api-flow-deploy': 'f262aba1d9031baf6d97abe763581c8cf5a5f6ad9df7a8aba20bb010b1a34f35',
    '/usr/local/sbin/cyf-web-flow-deploy': '53070ba8cf924852744e38c232d0b5d5b3fd432e0d05c90b8f9a877af21b9bb6',
}
PREFIXES = ('/home/isp/hosts/cyf/', '/var/lib/cyf-api-flow/', '/var/lib/cyf-web-flow/', '/home/isp/apps/', '/etc/systemd/system/')


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
    report['limits'] = ['Only OS ID/version and selected numeric meminfo fields are exported.',
                        'Helper contents and bounded Java arguments are inspected in memory; raw text is not exported.',
                        'No application config/environment, network connection, subprocess, installation or restart.',
                        'No service readiness, backup, storage/scanner or release gate is closed.']
    print(json.dumps(report, sort_keys=True))


if __name__ == '__main__':
    main()
