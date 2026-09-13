#!/usr/bin/env python3
"""Read-only fixed scanner-stage failure and resource diagnosis; never activate services."""
import hashlib
import json
import os
from pathlib import Path
import re
import resource
import signal
import stat
import subprocess
import time

BASE = Path('/opt/cyf/output-scanner')
ENV = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'HOME': '/root', 'LC_ALL': 'C', 'LANG': 'C',
       'LD_LIBRARY_PATH': str(BASE/'usr/lib64')}


def read(path, limit):
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as stream:
        info = os.fstat(stream.fileno())
        if not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or stat.S_IMODE(info.st_mode)&0o022:
            raise RuntimeError('untrusted_file')
        data = stream.read(limit+1)
    if len(data)>limit:
        raise RuntimeError('file_limit')
    return data


def limit_child():
    resource.setrlimit(resource.RLIMIT_AS, (256*1024**2, 256*1024**2))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def diagnostics(data):
    text = data.decode('utf-8', errors='replace')
    return {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data),
            'libraryNames': sorted(set(re.findall(r'\blib[A-Za-z0-9_+.-]+\.so(?:\.[0-9]+)*', text))),
            'missingLibraries': sorted(set(re.findall(r'(lib[A-Za-z0-9_+.-]+\.so(?:\.[0-9]+)*)\s*(?:=>\s*not found|:\s*cannot open shared object file)', text))),
            'undefinedSymbols': sorted(set(re.findall(r'undefined symbol:\s*([A-Za-z0-9_]+)', text))),
            'versionMissing': sorted(set(re.findall(r'version [`\x27]([A-Za-z0-9_.]+)[\x27]\s+not found', text))),
            'allocationFailure': bool(re.search(r'Cannot allocate memory|memory allocation failed', text, re.I)),
            'configurationFailure': bool(re.search(r'config.*(?:error|fail)|(?:error|fail).*config', text, re.I))}


def main():
    result = {'observedAtEpoch': int(time.time()), 'readOnly': True, 'status': 'UNKNOWN'}
    def expired(signum, frame):
        raise RuntimeError('diagnostic_deadline')
    signal.signal(signal.SIGALRM, expired)
    signal.alarm(90)
    try:
        if os.geteuid()!=0 or os.uname().machine!='x86_64':
            raise RuntimeError('host_identity')
        result['lastStageCommand'] = diagnostics(read(BASE/'command-output', 65536))
        loader = Path('/lib64/ld-linux-x86-64.so.2')
        info = loader.stat()
        if info.st_uid!=0 or not stat.S_ISREG(info.st_mode) or stat.S_IMODE(info.st_mode)&0o022:
            raise RuntimeError('untrusted_loader')
        result['loaders'] = []
        for relative in ['usr/bin/freshclam', 'usr/sbin/clamd']:
            data = read(BASE/relative, 16*1024**2)
            expected = {'usr/bin/freshclam': '91029892d3ce03a17cf2c56bf273fe12d3c800cf6bc2e6bf75d58d9de758dbab',
                        'usr/sbin/clamd': '4af6f9bfab10e9b18f051e7ba8e299766a6eeae9bead3c482678b55afdae2b8a'}
            if hashlib.sha256(data).hexdigest()!=expected[relative]:
                raise RuntimeError('staged_binary_hash')
            p = subprocess.run([str(loader), '--list', str(BASE/relative)], env=ENV,
                stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                timeout=20, check=False, preexec_fn=limit_child)
            if len(p.stdout)>65536:
                raise RuntimeError('loader_output_limit')
            result['loaders'].append(dict(path=relative, exitCode=p.returncode, **diagnostics(p.stdout)))
        mem = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
        result['memory'] = {k+'Bytes': int(mem[k].split()[0])*1024 for k in ['MemTotal','MemAvailable','SwapTotal','SwapFree']}
        v = os.statvfs('/opt')
        result['diskAvailableBytes'] = v.f_bavail*v.f_frsize
        helper = read(Path('/usr/local/sbin/cyf-api-kit'), 128*1024)
        result['apiHelperSha256'] = hashlib.sha256(helper).hexdigest()
        result['literalResourceConstants'] = [{'name': m[0], 'value': int(m[2])} for m in re.findall(
            rb'(?m)^([A-Z_]*(?:DISK|MEM|SPACE)[A-Z_]*)=([\x22\x27]?)([0-9]+)\2(?:\s*#.*)?$',helper)]
        for row in result['literalResourceConstants']:
            row['name'] = row['name'].decode('ascii')
        result['status'] = 'READ_ONLY_DIAGNOSED'
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        result['errorType'] = type(exc).__name__
    finally:
        signal.alarm(0)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status']=='READ_ONLY_DIAGNOSED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
