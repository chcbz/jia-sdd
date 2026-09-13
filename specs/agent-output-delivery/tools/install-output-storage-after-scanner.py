#!/usr/bin/env python3
"""Install a pinned MinIO in new task-specific paths; never touches an existing API runtime."""
import hashlib
import grp
import json
import os
from pathlib import Path
import pwd
import secrets
import signal
import shutil
import socket
import stat
import subprocess
import tarfile
import tempfile
import time
import urllib.request
import urllib.parse
import urllib.error

BASE = Path('/opt/cyf/output-storage')
CONFIG = Path('/etc/cyf-output-storage')
STATE = Path('/var/lib/cyf-output-storage')
UNIT = Path('/etc/systemd/system/cyf-output-storage.service')
USER = 'cyf-output-store'
LAYER = 'f9c0805c25ee5c0d375a9c16810eafb57cf658d7b6814c179d52496272bec8a4'
BINARY = '7c5bd8512c6e966455b1d198209358b2d191c77a83ab377c4073281065fb855f'
DISK_RESERVE = 2560 * 1024**2
MEMORY_RESERVE = 256 * 1024**2
KNOWN_INSTALL_PEAK = 110989496 + 64 * 1024**2
ENV = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'HOME': '/root', 'LC_ALL': 'C', 'LANG': 'C'}


def run(args, timeout=30):
    p = subprocess.run(args, env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL, timeout=timeout, check=False)
    if p.returncode != 0:
        raise RuntimeError('command_failed')


def exclusive(path, data, mode=0o600):
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    with os.fdopen(fd, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def installed_identity():
    fd = os.open(str(BASE/'minio'), os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        info = os.fstat(f.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_gid != 0
                or stat.S_IMODE(info.st_mode) != 0o755 or info.st_size != 110989496):
            raise RuntimeError('installed_binary_identity')
        digest = hashlib.sha256()
        for data in iter(lambda: f.read(1024*1024), b''):
            digest.update(data)
        os.fsync(f.fileno())
        after = os.fstat(f.fileno())
        if (after.st_ino, after.st_size, after.st_mtime_ns) != (info.st_ino, info.st_size, info.st_mtime_ns):
            raise RuntimeError('installed_binary_changed')
        if digest.hexdigest() != BINARY:
            raise RuntimeError('installed_binary_digest')
    return {'sha256': digest.hexdigest(), 'bytes': info.st_size, 'device': info.st_dev,
            'inode': info.st_ino, 'uid': info.st_uid, 'gid': info.st_gid, 'mode': '0755'}


def available_memory():
    mem = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    return int(mem['MemAvailable'].split()[0])*1024


def runtime_identity(user, installed):
    completed = subprocess.run(['/usr/bin/systemctl', 'show', 'cyf-output-storage.service',
        '--property=MainPID,MemoryCurrent,User,Group', '--no-pager'], env=ENV,
        stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10, check=False)
    if completed.returncode != 0 or len(completed.stdout) > 4096:
        raise RuntimeError('unit_identity_unavailable')
    values = dict(line.split('=', 1) for line in completed.stdout.decode().splitlines())
    pid = int(values['MainPID'])
    if pid < 2 or values['User'] != USER or values['Group'] != USER:
        raise RuntimeError('unit_identity_mismatch')
    proc = Path('/proc')/str(pid)
    before = (proc/'stat').read_text().rsplit(')', 1)[1].split()[19]
    status = dict(line.split(':', 1) for line in (proc/'status').read_text().splitlines() if ':' in line)
    if ([int(x) for x in status['Uid'].split()] != [user.pw_uid]*4
            or [int(x) for x in status['Gid'].split()] != [user.pw_gid]*4
            or os.readlink(proc/'exe') != str(BASE/'minio')):
        raise RuntimeError('process_identity_mismatch')
    exe = os.stat(proc/'exe')
    if (exe.st_dev, exe.st_ino) != (installed['device'], installed['inode']):
        raise RuntimeError('process_executable_mismatch')
    after = (proc/'stat').read_text().rsplit(')', 1)[1].split()[19]
    if before != after:
        raise RuntimeError('process_changed')
    memory = int(values['MemoryCurrent'])
    if memory > 384*1024**2:
        raise RuntimeError('unit_memory_budget')
    return {'pid': pid, 'startTicks': before, 'uid': user.pw_uid, 'gid': user.pw_gid,
            'exeSha256': installed['sha256'], 'unitMemoryBytes': memory}


class PinnedLayerStream:
    def __init__(self, source, result):
        self.source = source
        self.result = result
        self.digest = hashlib.sha256()
        self.size = 0
        self.deadline = time.monotonic()+120

    def read(self, size):
        if not 0 <= size <= 1024*1024:
            raise RuntimeError('layer_read_bound')
        if time.monotonic() > self.deadline:
            raise RuntimeError('download_timeout')
        data = self.source.read(size)
        self.size += len(data)
        self.result['downloadedLayerBytes'] = self.size
        if self.size > 39450432:
            raise RuntimeError('layer_size_exceeded')
        self.digest.update(data)
        return data

    def verify_complete(self):
        while self.read(1024*1024):
            pass
        if self.size != 39450432 or self.digest.hexdigest() != LAYER:
            raise RuntimeError('layer_integrity')


def extract_verified_layer(response, candidate, result):
    stream = PinnedLayerStream(response, result)
    matches = 0
    with tarfile.open(fileobj=stream, mode='r|gz') as archive:
        for index, member in enumerate(archive, 1):
            if index > 2048:
                raise RuntimeError('layer_member_count')
            if member.name.lstrip('./') != 'usr/bin/minio':
                continue
            matches += 1
            if matches != 1 or not member.isfile() or member.size != 110989496:
                raise RuntimeError('binary_member_integrity')
            digest = hashlib.sha256()
            written = 0
            with archive.extractfile(member) as src, candidate.open('xb') as dst:
                while True:
                    data = src.read(1024*1024)
                    if not data:
                        break
                    written += len(data)
                    if written > 110989496:
                        raise RuntimeError('binary_size_exceeded')
                    digest.update(data)
                    dst.write(data)
                dst.flush()
                os.fsync(dst.fileno())
            if written != 110989496 or digest.hexdigest() != BINARY:
                raise RuntimeError('binary_integrity')
    stream.verify_complete()
    if matches != 1:
        raise RuntimeError('binary_not_unique')
    result['streamedLayerSha256'] = stream.digest.hexdigest()


def expired(signum, frame):
    raise RuntimeError('installer_deadline')


def scanner_plan_cleanup_state():
    deadline = time.monotonic()+15
    prefix = b'/var/tmp/cyf-scanner-plan-'
    with os.scandir('/var/tmp') as entries:
        for entry in entries:
            if time.monotonic() > deadline:
                raise RuntimeError('scanner_plan_cleanup_scan_limit')
            if entry.name.startswith('cyf-scanner-plan-'):
                raise RuntimeError('scanner_plan_directory_remaining')
    checked = 0
    for proc in Path('/proc').iterdir():
        if not proc.name.isdecimal():
            continue
        checked += 1
        if checked > 8192 or time.monotonic() > deadline:
            raise RuntimeError('scanner_plan_cleanup_scan_limit')
        for name, limit in [('cmdline', 65536), ('mountinfo', 512*1024)]:
            try:
                fd = os.open(str(proc/name), os.O_RDONLY | os.O_NOFOLLOW)
                with os.fdopen(fd, 'rb') as f:
                    data = f.read(limit+1)
            except (FileNotFoundError, ProcessLookupError):
                continue
            if len(data)>limit:
                raise RuntimeError('scanner_plan_cleanup_record_limit')
            if prefix in data:
                raise RuntimeError('scanner_plan_process_or_mount_remaining')
    return {'observedAtEpoch': int(time.time()), 'checkedProcesses': checked,
            'residualTaskDirectories': 0, 'taskProcessReferences': 0, 'taskMountReferences': 0,
            'readOnly': True, 'priorPrivateCacheAccessible': False}


SCANNER_BINARY = '4af6f9bfab10e9b18f051e7ba8e299766a6eeae9bead3c482678b55afdae2b8a'
SCANNER_UNIT_SHA = '8f6d10bebfa2df5832a824001826f42887fdb77c918955656aa3e2b5f271e3b7'
SCANNER_CONFIG_SHA = 'a005a0936da56ce957850e65af4dbd8a75e0296894fd9bf18c20e1f3d58fee9a'


def scanner_prerequisite():
    receipt_path = Path('/opt/cyf/output-scanner/configure-result.json')
    fd = os.open(str(receipt_path), os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        info = os.fstat(f.fileno())
        if (not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_gid != 0
                or stat.S_IMODE(info.st_mode) != 0o600 or info.st_size > 65536):
            raise RuntimeError('scanner_receipt_identity')
        receipt = json.loads(f.read(65537))
    if (receipt.get('status') != 'SCANNER_INSTALLED_AND_SCAN_VERIFIED'
            or receipt.get('serviceMemoryLimitBytes') != 1200*1024**2
            or receipt.get('runtimeIdentity', {}).get('exeSha256') != SCANNER_BINARY
            or {x.get('case') for x in receipt.get('scans', [])} !=
                {'clean', 'eicar', 'member_61_mib', 'aggregate_110_mib'}
            or not all(x.get('expectedMatched') is True for x in receipt.get('scans', []))):
        raise RuntimeError('scanner_receipt_unaccepted')
    for path, expected, expected_mode in [
            (Path('/etc/systemd/system/cyf-output-scanner.service'), SCANNER_UNIT_SHA, 0o644),
            (Path('/etc/cyf-output-scanner/clamd.conf'), SCANNER_CONFIG_SHA, 0o644),
            (Path('/opt/cyf/output-scanner/usr/sbin/clamd'), SCANNER_BINARY, 0o755)]:
        fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, 'rb') as f:
            info = os.fstat(f.fileno())
            if (not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_gid != 0
                    or stat.S_IMODE(info.st_mode) != expected_mode or info.st_size > 256*1024):
                raise RuntimeError('scanner_file_identity')
            content = f.read(256*1024+1)
            if len(content) > 256*1024 or hashlib.sha256(content).hexdigest() != expected:
                raise RuntimeError('scanner_file_digest')
            if path.name == 'clamd':
                executable = info
    completed = subprocess.run(['/usr/bin/systemctl', 'show', 'cyf-output-scanner.service',
        '--property=MainPID,ActiveState,User,Group,MemoryCurrent,MemoryMax', '--no-pager'],
        env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
        timeout=10, check=False)
    if completed.returncode != 0 or len(completed.stdout) > 4096:
        raise RuntimeError('scanner_unit_unavailable')
    values = dict(line.split('=', 1) for line in completed.stdout.decode().splitlines())
    pid = int(values['MainPID'])
    if (pid < 2 or values['ActiveState'] != 'active' or values['User'] != 'cyf-output-scan'
            or values['Group'] != 'cyf-output-scan' or int(values['MemoryMax']) != 1200*1024**2
            or int(values['MemoryCurrent']) > 1200*1024**2):
        raise RuntimeError('scanner_unit_identity')
    user = pwd.getpwnam('cyf-output-scan')
    proc = Path('/proc')/str(pid)
    start = (proc/'stat').read_text().rsplit(')', 1)[1].split()[19]
    status = dict(line.split(':', 1) for line in (proc/'status').read_text().splitlines() if ':' in line)
    exe = os.stat(proc/'exe')
    if ([int(x) for x in status['Uid'].split()] != [user.pw_uid]*4
            or [int(x) for x in status['Gid'].split()] != [user.pw_gid]*4
            or os.readlink(proc/'exe') != '/opt/cyf/output-scanner/usr/sbin/clamd'
            or (exe.st_dev, exe.st_ino) != (executable.st_dev, executable.st_ino)):
        raise RuntimeError('scanner_process_identity')
    with socket.create_connection(('127.0.0.1', 13310), timeout=3) as connection:
        connection.settimeout(3)
        connection.sendall(b'zPING\0')
        reply = bytearray()
        while len(reply) < 64:
            part = connection.recv(64-len(reply))
            if not part:
                break
            reply.extend(part)
            if b'\0' in part:
                break
        if bytes(reply) != b'PONG\0':
            raise RuntimeError('scanner_not_ready')
    if (proc/'stat').read_text().rsplit(')', 1)[1].split()[19] != start:
        raise RuntimeError('scanner_process_changed')
    return {'pid': pid, 'startTicks': start, 'unitMemoryBytes': int(values['MemoryCurrent']),
            'exeSha256': SCANNER_BINARY, 'unitSha256': SCANNER_UNIT_SHA,
            'configSha256': SCANNER_CONFIG_SHA, 'ping': 'PONG'}


def main():
    result = {'startedAtEpoch': int(time.time()), 'status': 'UNKNOWN', 'apiRestartRequested': False}
    phase = 'preflight'
    activation_attempted = False
    signal.signal(signal.SIGALRM, expired)
    signal.alarm(420)
    try:
        if os.geteuid() != 0 or os.uname().machine != 'x86_64':
            raise RuntimeError('host_identity_gate')
        status = dict(line.split(':', 1) for line in (Path('/proc')/str(os.getpid())/'status').read_text().splitlines() if ':' in line)
        result['installerInitialMemory'] = {key+'Bytes': int(status[key].split()[0])*1024
            for key in ['VmSize', 'VmRSS', 'VmData']}
        result['scannerPlanCleanup'] = scanner_plan_cleanup_state()
        result['scannerBefore'] = scanner_prerequisite()
        for p in [BASE, CONFIG, STATE, UNIT]:
            if os.path.lexists(p):
                raise RuntimeError('existing_task_path')
        try:
            pwd.getpwnam(USER)
        except KeyError:
            pass
        else:
            raise RuntimeError('existing_task_user')
        try:
            grp.getgrnam(USER)
        except KeyError:
            pass
        else:
            raise RuntimeError('existing_task_group')
        for ancestor in [Path('/opt'), Path('/opt/cyf'), Path('/etc'), Path('/var'), Path('/var/lib'), UNIT.parent]:
            info = ancestor.lstat()
            if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or stat.S_IMODE(info.st_mode) & 0o022:
                raise RuntimeError('untrusted_parent')
        result['diskAvailableBefore'] = shutil.disk_usage('/opt').free
        result['memAvailableBefore'] = available_memory()
        result.update(diskReserveBytes=DISK_RESERVE, memoryReserveBytes=MEMORY_RESERVE,
                      knownInstallPeakBytes=KNOWN_INSTALL_PEAK)
        if (result['diskAvailableBefore'] < DISK_RESERVE+KNOWN_INSTALL_PEAK
                or result['memAvailableBefore'] < MEMORY_RESERVE+384*1024**2+64*1024**2):
            raise RuntimeError('resource_gate')
        for port in [19000, 19001]:
            with socket.socket() as s:
                s.bind(('127.0.0.1', port))
        phase = 'download_pinned_layer'
        with tempfile.TemporaryDirectory(prefix='cyf-output-storage-install-', dir='/opt/cyf') as temp:
            mirror = 'https://m.daocloud.io'
            url = mirror + '/v2/quay.io/minio/minio/blobs/sha256:' + LAYER
            # Anonymous public mirror token; no user/Flow credential or inherited proxy.
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            opener.addheaders = [('User-Agent', 'docker/27.0'), ('Cache-Control', 'no-cache')]
            query = urllib.parse.urlencode({'service': 'm.daocloud.io',
                'scope': 'repository:quay.io/minio/minio:pull', 'client_id': 'cyf-output-probe'})
            with opener.open(mirror+'/auth/token?'+query, timeout=20) as response:
                data = response.read(65537)
                if len(data) > 65536:
                    raise RuntimeError('public_token_response_limit')
                token = json.loads(data)['token']
                if not isinstance(token, str) or not token or len(token)>16384:
                    raise RuntimeError('public_token_invalid')
            request = urllib.request.Request(url, headers={'Authorization': 'Bearer '+token})
            result['downloadMirror'] = 'm.daocloud.io'
            result['downloadedLayerBytes'] = 0
            candidate = Path(temp) / 'minio'
            with opener.open(request, timeout=30) as response:
                extract_verified_layer(response, candidate, result)
            phase = 'install_new_paths'
            BASE.mkdir(mode=0o755)
            CONFIG.mkdir(mode=0o700)
            STATE.mkdir(mode=0o750)
            receipt = BASE / 'install-intent.json'
            exclusive(receipt, (json.dumps(dict(result, layerSha256=LAYER, binarySha256=BINARY))+'\n').encode())
            run(['/usr/sbin/useradd', '--system', '--user-group', '--no-create-home', '--home-dir', str(STATE), '--shell', '/sbin/nologin', USER])
            user = pwd.getpwnam(USER)
            group = grp.getgrnam(USER)
            if (user.pw_uid == 0 or user.pw_gid != group.gr_gid or user.pw_dir != str(STATE)
                    or user.pw_shell != '/sbin/nologin'):
                raise RuntimeError('created_identity_mismatch')
            result['serviceIdentity'] = {'uid': user.pw_uid, 'gid': user.pw_gid, 'home': user.pw_dir, 'shell': user.pw_shell}
            os.chown(STATE, user.pw_uid, user.pw_gid)
            if candidate.stat().st_dev != BASE.stat().st_dev:
                raise RuntimeError('binary_filesystem_mismatch')
            # Exclusive hard link shares existing blocks, then remove the staging name.
            os.link(candidate, BASE/'minio', follow_symlinks=False)
            candidate.unlink()
            os.chmod(BASE/'minio', 0o755)
            installed = installed_identity()
            result['installedBinary'] = installed
            credential = {'accessKey': 'cyf-output-'+secrets.token_hex(8), 'secretKey': secrets.token_hex(32)}
            exclusive(CONFIG/'credentials.json', (json.dumps(credential)+'\n').encode())
            exclusive(CONFIG/'minio.env', ('MINIO_ROOT_USER='+credential['accessKey']+'\nMINIO_ROOT_PASSWORD='+credential['secretKey']+'\nMINIO_BROWSER=off\nMINIO_API_REQUESTS_MAX=8\nGOMEMLIMIT=256MiB\n').encode())
            unit = '''[Unit]
Description=CYF Agent output object storage
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=300
StartLimitBurst=3

[Service]
User=cyf-output-store
Group=cyf-output-store
EnvironmentFile=/etc/cyf-output-storage/minio.env
ExecStart=/opt/cyf/output-storage/minio server /var/lib/cyf-output-storage --address 127.0.0.1:19000 --console-address 127.0.0.1:19001
Restart=on-failure
RestartSec=10
UMask=0077
LimitNOFILE=4096
MemoryAccounting=true
MemoryMax=384M
TasksMax=128
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=/var/lib/cyf-output-storage
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX

[Install]
WantedBy=multi-user.target
'''
            exclusive(UNIT, unit.encode(), 0o644)
        phase = 'activate_new_service'
        if shutil.disk_usage('/opt').free < DISK_RESERVE or available_memory() < MEMORY_RESERVE+384*1024**2:
            raise RuntimeError('activation_resource_gate')
        activation_attempted = True
        run(['/usr/bin/systemctl', 'daemon-reload'])
        run(['/usr/bin/systemctl', 'enable', '--now', 'cyf-output-storage.service'], timeout=60)
        phase = 'readiness'
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        ready = False
        for _ in range(20):
            try:
                with opener.open('http://127.0.0.1:19000/minio/health/ready', timeout=3) as response:
                    ready = response.status == 200
            except OSError:
                pass
            if ready:
                break
            time.sleep(1)
        if not ready:
            raise RuntimeError('readiness_failed')
        result['runtimeIdentity'] = runtime_identity(user, installed)
        result['scannerAfter'] = scanner_prerequisite()
        if any(result['scannerBefore'][key] != result['scannerAfter'][key] for key in ['pid','startTicks']):
            raise RuntimeError('existing_scanner_restarted')
        result['memAvailableAfter'] = available_memory()
        if shutil.disk_usage('/opt').free < DISK_RESERVE or result['memAvailableAfter'] < MEMORY_RESERVE:
            raise RuntimeError('runtime_resource_gate')
        result.update(status='STORAGE_SERVICE_INSTALLED', binarySha256=installed['sha256'],
                      service='cyf-output-storage.service', endpoint='http://127.0.0.1:19000',
                      bucketCreated=False, applicationConfigured=False)
        exclusive(BASE/'install-result.json', (json.dumps(result,sort_keys=True)+'\n').encode())
    except (OSError, ValueError, KeyError, RuntimeError, MemoryError, subprocess.SubprocessError, tarfile.TarError) as exc:
        signal.alarm(0)
        result.update(status='UNKNOWN', failedPhase=phase, errorType=type(exc).__name__)
        if isinstance(exc, urllib.error.HTTPError):
            result['httpStatus'] = exc.code
        if type(exc) is RuntimeError and str(exc).replace('_', '').isalpha():
            result['errorCode'] = str(exc)
        if activation_attempted:
            try:
                run(['/usr/bin/systemctl', 'disable', '--now', 'cyf-output-storage.service'], timeout=45)
                check = subprocess.run(['/usr/bin/systemctl', 'show', 'cyf-output-storage.service',
                    '--property=ActiveState,UnitFileState', '--no-pager'], env=ENV, stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=10, check=False)
                states = dict(line.split('=', 1) for line in check.stdout.decode().splitlines())
                result['failureServiceDisabledAndStopped'] = (check.returncode == 0
                    and states.get('ActiveState') in ('inactive', 'failed')
                    and states.get('UnitFileState') == 'disabled')
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
                result['failureServiceDisabledAndStopped'] = False
    finally:
        signal.alarm(0)
    result['diskAvailableAfter'] = shutil.disk_usage('/opt').free
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] == 'STORAGE_SERVICE_INSTALLED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
