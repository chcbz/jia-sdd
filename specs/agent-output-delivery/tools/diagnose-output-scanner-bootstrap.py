#!/usr/bin/env python3
"""Read-only diagnosis of the fixed failed scanner bootstrap; no service mutations."""
import hashlib
import json
import os
from pathlib import Path
import re
import signal
import stat
import subprocess
import time

UNITS = ['cyf-output-scanner-bootstrap.service', 'cyf-output-scanner.service']
ENV = {'PATH': '/usr/bin:/usr/sbin:/bin:/sbin', 'LC_ALL': 'C'}


def command(args):
    p = subprocess.run(args, env=ENV, stdin=subprocess.DEVNULL,
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=20)
    if p.returncode or len(p.stdout) > 262144:
        raise RuntimeError('diagnostic_command_failed')
    return p.stdout.decode('utf-8', errors='strict')


def main():
    result = {'observedAtEpoch': int(time.time()), 'readOnly': True, 'status': 'UNKNOWN'}
    def expired(signum, frame):
        raise RuntimeError('deadline')
    signal.signal(signal.SIGALRM, expired)
    signal.alarm(90)
    try:
        if os.geteuid() != 0:
            raise RuntimeError('host_identity')
        result['units'] = []
        for unit in UNITS:
            state = command(['/usr/bin/systemctl', 'show', unit, '--no-pager',
                '--property=ActiveState,SubState,Result,ExecMainStatus,MainPID,MemoryCurrent,MemoryMax,UnitFileState,ExecMainStartTimestampMonotonic,ExecMainExitTimestampMonotonic'])
            raw = command(['/usr/bin/journalctl', '--no-pager', '-u', unit,
                           '--since', '2026-09-13 16:30:00', '-n', '100', '-o', 'json'])
            messages = []
            for line in raw.splitlines():
                row = json.loads(line)
                message = row.get('MESSAGE', '')
                if not isinstance(message, str):
                    continue
                message = re.sub(r'https?://\S+', '<url>', message)
                if re.search(r'password|secret|token|authorization|bearer', message, re.I):
                    message = '<sensitive line excluded>'
                messages.append({'time': row.get('__REALTIME_TIMESTAMP'), 'message': message[:600]})
            result['units'].append({'unit': unit,
                'state': dict(x.split('=', 1) for x in state.splitlines()),
                'journalSha256': hashlib.sha256(raw.encode()).hexdigest(),
                'journalBytes': len(raw.encode()), 'lastMessages': messages})
        db = Path('/var/lib/cyf-output-scanner/db')
        info = db.lstat()
        if not stat.S_ISDIR(info.st_mode) or info.st_uid == 0:
            raise RuntimeError('database_directory_identity')
        entries = list(db.iterdir())
        if len(entries) > 32:
            raise RuntimeError('entry_limit')
        result['databaseEntries'] = []
        for entry in entries:
            i = entry.lstat()
            result['databaseEntries'].append({'name': entry.name, 'bytes': i.st_size,
                'uid': i.st_uid, 'mode': oct(stat.S_IMODE(i.st_mode)),
                'regular': stat.S_ISREG(i.st_mode), 'mtimeEpoch': i.st_mtime})
        m = dict(x.split(':', 1) for x in Path('/proc/meminfo').read_text().splitlines())
        result['memAvailableBytes'] = int(m['MemAvailable'].split()[0]) * 1024
        v = os.statvfs('/opt')
        result['diskAvailableBytes'] = v.f_bavail * v.f_frsize
        result['status'] = 'READ_ONLY_DIAGNOSED'
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        result['errorType'] = type(exc).__name__
    finally:
        signal.alarm(0)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] == 'READ_ONLY_DIAGNOSED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
