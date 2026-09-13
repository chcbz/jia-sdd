#!/usr/bin/env python3
"""Install a pinned MinIO in new task-specific paths; never touches an existing API runtime."""
import hashlib
import json
import os
from pathlib import Path
import pwd
import secrets
import shutil
import socket
import stat
import subprocess
import tarfile
import tempfile
import time
import urllib.request

BASE = Path('/opt/cyf/output-storage')
CONFIG = Path('/etc/cyf-output-storage')
STATE = Path('/var/lib/cyf-output-storage')
UNIT = Path('/etc/systemd/system/cyf-output-storage.service')
USER = 'cyf-output-store'
LAYER = 'f9c0805c25ee5c0d375a9c16810eafb57cf658d7b6814c179d52496272bec8a4'
BINARY = '7c5bd8512c6e966455b1d198209358b2d191c77a83ab377c4073281065fb855f'
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


def main():
    result = {'startedAtEpoch': int(time.time()), 'status': 'UNKNOWN', 'apiRestartRequested': False}
    phase = 'preflight'
    try:
        if os.geteuid() != 0 or os.uname().machine != 'x86_64':
            raise RuntimeError('host_identity_gate')
        for p in [BASE, CONFIG, STATE, UNIT]:
            if os.path.lexists(p):
                raise RuntimeError('existing_task_path')
        try:
            pwd.getpwnam(USER)
        except KeyError:
            pass
        else:
            raise RuntimeError('existing_task_user')
        for ancestor in [Path('/opt'), Path('/opt/cyf'), Path('/etc'), Path('/var'), Path('/var/lib'), UNIT.parent]:
            info = ancestor.lstat()
            if not stat.S_ISDIR(info.st_mode) or info.st_uid != 0 or stat.S_IMODE(info.st_mode) & 0o022:
                raise RuntimeError('untrusted_parent')
        result['diskAvailableBefore'] = shutil.disk_usage('/opt').free
        mem = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
        result['memAvailableBefore'] = int(mem['MemAvailable'].split()[0]) * 1024
        if result['diskAvailableBefore'] < 4 * 1024**3 or result['memAvailableBefore'] < 1536 * 1024**2:
            raise RuntimeError('resource_gate')
        for port in [19000, 19001]:
            with socket.socket() as s:
                s.bind(('127.0.0.1', port))
        phase = 'download_pinned_layer'
        with tempfile.TemporaryDirectory(prefix='cyf-output-storage-install-', dir='/opt/cyf') as temp:
            layer_path = Path(temp) / 'layer.tar.gz'
            url = 'https://quay.io/v2/minio/minio/blobs/sha256:' + LAYER
            # Public immutable layer; no registry/Flow credentials or proxy inherited.
            opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
            digest = hashlib.sha256()
            size = 0
            with opener.open(url, timeout=30) as response, layer_path.open('xb') as f:
                deadline = time.monotonic()+120
                while True:
                    if time.monotonic() > deadline:
                        raise RuntimeError('download_timeout')
                    data = response.read(1024*1024)
                    if not data:
                        break
                    size += len(data)
                    if size > 39450432:
                        raise RuntimeError('layer_size_exceeded')
                    digest.update(data)
                    f.write(data)
            if size != 39450432 or digest.hexdigest() != LAYER:
                raise RuntimeError('layer_integrity')
            candidate = Path(temp) / 'minio'
            matches = 0
            with tarfile.open(layer_path, 'r|gz') as archive:
                for member in archive:
                    if member.name.lstrip('./') != 'usr/bin/minio':
                        continue
                    matches += 1
                    if matches != 1 or not member.isfile() or member.size != 110989496:
                        raise RuntimeError('binary_member_integrity')
                    digest = hashlib.sha256()
                    with archive.extractfile(member) as src, candidate.open('xb') as dst:
                        while True:
                            data = src.read(1024*1024)
                            if not data:
                                break
                            digest.update(data)
                            dst.write(data)
                    if digest.hexdigest() != BINARY:
                        raise RuntimeError('binary_integrity')
            if matches != 1:
                raise RuntimeError('binary_not_unique')
            phase = 'install_new_paths'
            BASE.mkdir(mode=0o755)
            CONFIG.mkdir(mode=0o700)
            STATE.mkdir(mode=0o750)
            receipt = BASE / 'install-intent.json'
            exclusive(receipt, (json.dumps(dict(result, layerSha256=LAYER, binarySha256=BINARY))+'\n').encode())
            run(['/usr/sbin/useradd', '--system', '--user-group', '--no-create-home', '--home-dir', str(STATE), '--shell', '/sbin/nologin', USER])
            user = pwd.getpwnam(USER)
            os.chown(STATE, user.pw_uid, user.pw_gid)
            shutil.copyfile(candidate, BASE/'minio')
            os.chmod(BASE/'minio', 0o755)
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
        result.update(status='STORAGE_SERVICE_INSTALLED', binarySha256=BINARY,
                      service='cyf-output-storage.service', endpoint='http://127.0.0.1:19000',
                      bucketCreated=False, applicationConfigured=False)
        exclusive(BASE/'install-result.json', (json.dumps(result,sort_keys=True)+'\n').encode())
    except (OSError, RuntimeError, subprocess.SubprocessError, tarfile.TarError):
        result.update(status='UNKNOWN', failedPhase=phase)
    result['diskAvailableAfter'] = shutil.disk_usage('/opt').free
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] == 'STORAGE_SERVICE_INSTALLED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
