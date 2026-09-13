#!/usr/bin/env python3
"""Activate the exact compensated scanner using independently verified existing full databases."""
import grp
import hashlib
import io
import json
import os
from pathlib import Path
import pwd
import re
import signal
import socket
import stat
import struct
import subprocess
import time
import zipfile

MANIFEST = [{'path': 'usr/bin/clamscan', 'mode': '0o755', 'bytes': 193984, 'sha256': '4c662ebca789e371eb97fcd6ec2ff44b3445211bd6f5f87808c4a396bbed3989', 'type': 'regular'}, {'path': 'usr/bin/sigtool', 'mode': '0o755', 'bytes': 9587448, 'sha256': '1a6010478d9361b3bf27fc700ba87447b7fcbfa12358251f9c0160ddd201fe15', 'type': 'regular'}, {'path': 'usr/lib64/libclamav.so.12', 'mode': '0o777', 'bytes': 19, 'sha256': '3c9b7fb194d079740744d66a329096b72c522ada5dc2ea566b8e3c87471dcb17', 'type': 'symlink', 'target': 'libclamav.so.12.0.3'}, {'path': 'usr/lib64/libclamav.so.12.0.3', 'mode': '0o755', 'bytes': 11421696, 'sha256': 'f2eb53c3b86f2f01449ef57d5970efd47f36fd3c33c6e027e342493c6c6d748e', 'type': 'regular'}, {'path': 'usr/lib64/libclammspack.so.0', 'mode': '0o777', 'bytes': 22, 'sha256': '462d1f655fb5c241ac8b821dfa923d8cd0274df9f634fe86e0b4d8455092a6bd', 'type': 'symlink', 'target': 'libclammspack.so.0.8.0'}, {'path': 'usr/lib64/libclammspack.so.0.8.0', 'mode': '0o755', 'bytes': 78840, 'sha256': 'cdebda20f8fbe3f64341a60fa12b3282d412becc95f8e9c197cae4f538bb277b', 'type': 'regular'}, {'path': 'usr/sbin/clamd', 'mode': '0o755', 'bytes': 223024, 'sha256': '4af6f9bfab10e9b18f051e7ba8e299766a6eeae9bead3c482678b55afdae2b8a', 'type': 'regular'}, {'path': 'usr/bin/freshclam', 'mode': '0o755', 'bytes': 83568, 'sha256': '91029892d3ce03a17cf2c56bf273fe12d3c800cf6bc2e6bf75d58d9de758dbab', 'type': 'regular'}, {'path': 'usr/lib64/libfreshclam.so.3', 'mode': '0o777', 'bytes': 21, 'sha256': '3297218ef05a4dd3ec638b4fc3be8426f26a5b2d9de9032c1aa99d617e1eb4cf', 'type': 'symlink', 'target': 'libfreshclam.so.3.0.2'}, {'path': 'usr/lib64/libfreshclam.so.3.0.2', 'mode': '0o755', 'bytes': 9591216, 'sha256': '9f90f21ddb393ac49773a862c88baadebc2d72dc54675b322ffef90ea33ed0b3', 'type': 'regular'}]

BASE = Path('/opt/cyf/output-scanner')
CONFIG = Path('/etc/cyf-output-scanner')
STATE = Path('/var/lib/cyf-output-scanner')
USER = 'cyf-output-scan'
DAEMON = 'cyf-output-scanner.service'
UPDATER = 'cyf-output-scanner-bootstrap.service'
UNITDIR = Path('/etc/systemd/system')
ENV = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'HOME': '/root', 'LC_ALL': 'C', 'LANG': 'C'}
DISK_RESERVE = 2560 * 1024**2
DATABASE_PEAK = 768 * 1024**2
SERVICE_MEMORY = 1200 * 1024**2
MEMORY_RESERVE = 256 * 1024**2
EICAR = b'X5O!P%@AP[4\\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*'


def require(value, code):
    if not value:
        raise RuntimeError(code)


def exclusive(path, data, mode=0o600):
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    with os.fdopen(fd, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def memory():
    rows = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    return int(rows['MemAvailable'].split()[0])*1024


def disk():
    v = os.statvfs('/opt')
    return v.f_bavail*v.f_frsize


def read_hash(path, row):
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        before = os.fstat(f.fileno())
        require(stat.S_ISREG(before.st_mode) and before.st_uid==0 and before.st_gid==0 and
                stat.S_IMODE(before.st_mode)==0o755 and before.st_size==row['bytes'], 'staged_file_identity')
        digest = hashlib.sha256()
        for chunk in iter(lambda:f.read(1024*1024), b''):
            digest.update(chunk)
        after = os.fstat(f.fileno())
        require((before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns), 'staged_file_changed')
        require(digest.hexdigest()==row['sha256'], 'staged_file_hash')
        return {'device':before.st_dev,'inode':before.st_ino,'sha256':digest.hexdigest()}


def command(args, timeout=15, private_libs=False):
    env = dict(ENV)
    if private_libs:
        env['LD_LIBRARY_PATH'] = str(BASE/'usr/lib64')
    p = subprocess.run(args, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                       stderr=subprocess.DEVNULL, timeout=timeout, check=False)
    require(p.returncode==0 and len(p.stdout)<=65536, 'command_failed')
    return p.stdout.decode('utf-8', errors='strict')


def unit_values(name):
    data = command(['/usr/bin/systemctl','show',name,'--property=ActiveState,SubState,Result,ExecMainStatus,MainPID,MemoryCurrent,MemoryMax,User,Group,UnitFileState,ExecMainStartTimestampMonotonic,ExecMainExitTimestampMonotonic,NRestarts','--no-pager'])
    return dict(line.split('=',1) for line in data.splitlines())


def unit_text(description, executable, oneshot=False):
    return f'''[Unit]
Description={description}
After=network-online.target
Wants=network-online.target
StartLimitIntervalSec=300
StartLimitBurst=2

[Service]
Type={'oneshot' if oneshot else 'simple'}
User={USER}
Group={USER}
Environment=LD_LIBRARY_PATH={BASE}/usr/lib64
ExecStart={executable}
TimeoutStartSec={'600' if oneshot else '120'}
TimeoutStopSec=20
MemoryAccounting=true
MemoryMax=1200M
MemorySwapMax=128M
TasksMax=64
LimitFSIZE=256M
LimitCORE=0
UMask=0077
NoNewPrivileges=true
PrivateTmp=true
ProtectHome=true
ProtectSystem=strict
ReadWritePaths={STATE}
RestrictAddressFamilies=AF_INET AF_INET6 AF_UNIX
{'' if oneshot else 'Restart=on-failure' + chr(10) + 'RestartSec=15'}

[Install]
WantedBy=multi-user.target
'''


def protocol(command_bytes, content=None):
    with socket.create_connection(('127.0.0.1',13310), timeout=5) as s:
        s.settimeout(180)
        s.sendall(command_bytes)
        if content is not None:
            for start in range(0,len(content),65536):
                part = content[start:start+65536]
                s.sendall(struct.pack('!I',len(part))+part)
            s.sendall(struct.pack('!I',0))
        response = bytearray()
        while len(response)<1024:
            data = s.recv(1024-len(response))
            if not data:
                break
            response.extend(data)
            if b'\0' in data:
                break
        require(len(response)<1024, 'scanner_response_limit')
        return response.split(b'\0',1)[0].decode('ascii', errors='strict')


def archive(sizes):
    output = io.BytesIO()
    with zipfile.ZipFile(output,'w',compression=zipfile.ZIP_DEFLATED) as z:
        block = bytes(1024*1024)
        for i,size in enumerate(sizes):
            with z.open('padding'+str(i)+'.bin','w') as member:
                for _ in range(size):
                    member.write(block)
    return output.getvalue()


def trusted_file(path, mode, maximum):
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        info = os.fstat(f.fileno())
        require(stat.S_ISREG(info.st_mode) and info.st_uid == 0 and info.st_gid == 0
                and stat.S_IMODE(info.st_mode) == mode and info.st_size <= maximum,
                'configuration_identity')
        content = f.read(maximum + 1)
        require(len(content) <= maximum, 'configuration_limit')
        return content


def readiness_ping():
    with socket.create_connection(('127.0.0.1', 13310), timeout=2) as connection:
        connection.settimeout(2)
        connection.sendall(b'zPING\0')
        response = bytearray()
        while len(response) < 64 and b'\0' not in response:
            part = connection.recv(64-len(response))
            if not part:
                break
            response.extend(part)
        return bytes(response) == b'PONG\0'


def startup_progress():
    values = unit_values(DAEMON)
    require(int(values['NRestarts']) == 0, 'startup_process_restarted')
    row = {'kind': 'SCANNER_STARTUP_PROGRESS', 'observedAtEpoch': int(time.time()),
           'unitState': values['ActiveState'], 'pid': int(values['MainPID']),
           'memoryCurrent': values.get('MemoryCurrent'), 'memAvailableBytes': memory()}
    if row['pid'] > 1:
        proc = Path('/proc')/str(row['pid'])
        status = dict(x.split(':', 1) for x in (proc/'status').read_text().splitlines() if ':' in x)
        require([int(x) for x in status['Uid'].split()] == [986]*4, 'progress_process_identity')
        info = (proc/'stat').read_text().rsplit(')', 1)[1].split()
        row.update(startTicks=info[19], userTicks=int(info[11]), systemTicks=int(info[12]))
        for key in ['VmRSS', 'VmSwap']:
            row[key+'Bytes'] = int(status[key].split()[0])*1024
    print(json.dumps(row, sort_keys=True), flush=True)
    return row


def main():
    result = {'startedAtEpoch': int(time.time()), 'status': 'UNKNOWN',
              'apiRestartRequested': False, 'rpmTransactionRequested': False,
              'scheduledUpdaterEnabled': False, 'databaseDownloadRequested': False,
              'priorBootstrapStartedAtEpoch': 1789288473,
              'serviceMemoryLimitBytes': SERVICE_MEMORY, 'memoryReserveBytes': MEMORY_RESERVE,
              'diskReserveBytes': DISK_RESERVE}
    phase = 'existing_configuration_verification'
    activation_attempted = False
    def expired(signum, frame):
        raise RuntimeError('activation_deadline')
    signal.signal(signal.SIGALRM, expired)
    signal.alarm(1200)
    try:
        require(os.geteuid() == 0 and os.uname().machine == 'x86_64', 'host_identity')
        for parent in [Path('/opt'), Path('/opt/cyf'), BASE, BASE/'usr', BASE/'usr/bin',
                       BASE/'usr/sbin', BASE/'usr/lib64', Path('/etc'), CONFIG,
                       Path('/var'), Path('/var/lib'), UNITDIR]:
            info = parent.lstat()
            require(stat.S_ISDIR(info.st_mode) and info.st_uid == 0 and info.st_gid == 0
                    and not stat.S_IMODE(info.st_mode) & 0o022, 'untrusted_parent')
        for path in [BASE/'observe-activation-intent.json', BASE/'configure-result.json',
                     CONFIG/'clamd.conf.pre-observation', CONFIG/'clamd.conf.observe-new']:
            require(not os.path.lexists(path), 'existing_activation')
        previous = json.loads(trusted_file(BASE/'activate-intent.json', 0o600, 65536))
        require(previous.get('startedAtEpoch') == 1789290118
                and previous.get('status') == 'UNKNOWN'
                and previous.get('databaseDownloadRequested') is False, 'prior_activation_mismatch')
        prior = json.loads(trusted_file(BASE/'configure-intent.json', 0o600, 65536))
        require(prior.get('startedAtEpoch') == 1789288473 and prior.get('status') == 'UNKNOWN'
                and prior.get('apiRestartRequested') is False, 'prior_intent_mismatch')
        user = pwd.getpwnam(USER)
        require(user.pw_uid == 986 and user.pw_gid == grp.getgrnam(USER).gr_gid
                and user.pw_dir == str(STATE) and user.pw_shell == '/sbin/nologin', 'existing_user')
        for parent in [STATE, STATE/'db']:
            info = parent.lstat()
            require(stat.S_ISDIR(info.st_mode) and info.st_uid == user.pw_uid
                    and info.st_gid == user.pw_gid and stat.S_IMODE(info.st_mode) == 0o750,
                    'database_directory_identity')
        identities = {}
        for row in MANIFEST:
            path = BASE/row['path']
            if row['type'] == 'regular':
                identities[row['path']] = read_hash(path, row)
            else:
                info = path.lstat()
                require(stat.S_ISLNK(info.st_mode) and info.st_uid == 0
                        and os.readlink(path) == row['target'], 'staged_link_identity')
        expected = {
            UNITDIR/DAEMON: '8f6d10bebfa2df5832a824001826f42887fdb77c918955656aa3e2b5f271e3b7',
            UNITDIR/UPDATER: '3b86c587e083c21fd040b065862ecb430dbaa8f8311992b93140089d28c4433c',
            CONFIG/'clamd.conf': 'bbd6c053c9029e10a6f43d101907433fe2c62650c7cb3f8f64ac9fcd80f3cea8',
        }
        for path, digest in expected.items():
            require(hashlib.sha256(trusted_file(path, 0o644, 16384)).hexdigest() == digest,
                    'configuration_digest')
        for unit in [DAEMON, UPDATER]:
            state = unit_values(unit)
            require(state['ActiveState'] == 'inactive' and state['UnitFileState'] == 'disabled'
                    and state['MainPID'] == '0', 'existing_service_active')
            require(int(state['NRestarts']) == 0, 'prior_service_restarts')
        with socket.socket() as s:
            s.bind(('127.0.0.1', 13310))
        result.update(memAvailableBefore=memory(), diskAvailableBefore=disk())
        require(memory() >= SERVICE_MEMORY + MEMORY_RESERVE and disk() >= DISK_RESERVE,
                'resource_gate')
        phase = 'existing_database_signatures'
        require({x.name for x in (STATE/'db').iterdir()} ==
                {'main.cvd', 'daily.cvd', 'bytecode.cvd', 'freshclam.dat'}, 'database_set')
        result['databases'] = []
        for name, size in [('main.cvd', 89072577), ('daily.cvd', 23432361), ('bytecode.cvd', 281702)]:
            path = STATE/'db'/name
            fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(fd, 'rb') as f:
                before = os.fstat(f.fileno())
                require(stat.S_ISREG(before.st_mode) and before.st_uid == user.pw_uid
                        and before.st_gid == user.pw_gid and stat.S_IMODE(before.st_mode) == 0o600
                        and before.st_size == size, 'database_identity')
                digest = hashlib.sha256()
                for data in iter(lambda: f.read(1024*1024), b''):
                    digest.update(data)
                output = command([str(BASE/'usr/bin/sigtool'), '--info', str(path)], private_libs=True)
                require('Verification OK.' in output, 'database_signature_invalid')
                after = path.lstat()
                require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
                        (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), 'database_changed')
            result['databases'].append({'name': name, 'bytes': size,
                'sha256': digest.hexdigest(), 'signatureVerified': True})
        require(command([str(BASE/'usr/sbin/clamd'), '--config-file='+str(CONFIG/'clamd.conf'),
                         '--version'], private_libs=True).strip().split('/', 1)[0] == 'ClamAV 1.4.6',
                'configured_version')
        require(memory() >= SERVICE_MEMORY + MEMORY_RESERVE and disk() >= DISK_RESERVE,
                'activation_resource_gate')
        exclusive(BASE/'observe-activation-intent.json', (json.dumps(result, sort_keys=True)+'\n').encode())
        phase = 'enable_engine_logging'
        original_config = trusted_file(CONFIG/'clamd.conf', 0o644, 16384)
        require(hashlib.sha256(original_config).hexdigest() == expected[CONFIG/'clamd.conf'],
                'configuration_changed')
        new_config = original_config + b'LogSyslog yes\nLogTime yes\nLogVerbose yes\n'
        exclusive(CONFIG/'clamd.conf.pre-observation', original_config)
        exclusive(CONFIG/'clamd.conf.observe-new', new_config, 0o644)
        os.replace(CONFIG/'clamd.conf.observe-new', CONFIG/'clamd.conf')
        directory_fd = os.open(str(CONFIG), os.O_RDONLY | os.O_DIRECTORY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
        result['configurationSha256'] = hashlib.sha256(new_config).hexdigest()
        phase = 'activate_scanner'
        activation_attempted = True
        command(['/usr/bin/systemctl', 'enable', '--now', DAEMON], timeout=30)
        activation_began = time.monotonic()
        deadline = activation_began+600
        next_progress = 0
        initial_state = unit_values(DAEMON)
        initial_pid = int(initial_state['MainPID'])
        require(initial_pid > 1 and int(initial_state['NRestarts']) == 0, 'initial_process_identity')
        initial_start = (Path('/proc')/str(initial_pid)/'stat').read_text().rsplit(')', 1)[1].split()[19]
        startup_identity = (initial_pid, initial_start)
        while True:
            pending_state = unit_values(DAEMON)
            require(int(pending_state['NRestarts']) == 0
                    and int(pending_state['MainPID']) == startup_identity[0], 'startup_process_restarted')
            try:
                if readiness_ping():
                    break
            except OSError:
                pass
            require(time.monotonic() < deadline, 'scanner_readiness_deadline')
            require(unit_values(DAEMON)['ActiveState'] != 'failed', 'scanner_failed')
            if time.monotonic() >= next_progress:
                row = startup_progress()
                require(row['memAvailableBytes'] >= MEMORY_RESERVE, 'startup_memory_reserve')
                if row['pid'] > 1:
                    current_identity = (row['pid'], row['startTicks'])
                    require(startup_identity == current_identity, 'startup_process_restarted')
                next_progress = time.monotonic()+15
            time.sleep(2)
        result['startupElapsedSeconds'] = round(time.monotonic()-activation_began, 3)
        state = unit_values(DAEMON)
        pid = int(state['MainPID'])
        require(int(state['NRestarts']) == 0, 'startup_process_restarted')
        require(pid > 1 and state['User'] == USER and state['Group'] == USER
                and int(state['MemoryMax']) == SERVICE_MEMORY, 'unit_identity')
        proc = Path('/proc')/str(pid)
        start = (proc/'stat').read_text().rsplit(')', 1)[1].split()[19]
        require((pid, start) == startup_identity, 'startup_process_restarted')
        status = dict(x.split(':', 1) for x in (proc/'status').read_text().splitlines() if ':' in x)
        require([int(x) for x in status['Uid'].split()] == [user.pw_uid]*4
                and [int(x) for x in status['Gid'].split()] == [user.pw_gid]*4, 'process_identity')
        exe = os.stat(proc/'exe')
        identity = identities['usr/sbin/clamd']
        require(os.readlink(proc/'exe') == str(BASE/'usr/sbin/clamd')
                and (exe.st_dev, exe.st_ino) == (identity['device'], identity['inode']),
                'running_binary_identity')
        phase = 'real_scan_validation'
        result['scans'] = []
        for name, content, expected in [
                ('clean', b'CYF output scanner production probe\n', 'stream: OK'),
                ('eicar', EICAR, ' FOUND'),
                ('member_61_mib', archive([61]), 'Heuristics.Limits.Exceeded'),
                ('aggregate_110_mib', archive([55, 55]), 'Heuristics.Limits.Exceeded')]:
            began = time.monotonic()
            response = protocol(b'zINSTREAM\0', content)
            require(response == expected if name == 'clean' else expected in response, 'scan_result_mismatch')
            result['scans'].append({'case': name, 'inputBytes': len(content),
                'sha256': hashlib.sha256(content).hexdigest(), 'expectedMatched': True,
                'elapsedSeconds': round(time.monotonic()-began, 3)})
        require((proc/'stat').read_text().rsplit(')', 1)[1].split()[19] == start, 'process_changed')
        state = unit_values(DAEMON)
        result.update(runtimeIdentity={'pid': pid, 'startTicks': start, 'uid': user.pw_uid,
            'gid': user.pw_gid, 'exeSha256': identity['sha256'],
            'memoryCurrentBytes': int(state['MemoryCurrent'])},
            memAvailableAfter=memory(), diskAvailableAfter=disk(), version=protocol(b'zVERSION\0'))
        require(int(state['MainPID']) == pid and state['ActiveState'] == 'active'
                and int(state['NRestarts']) == 0
                and int(state['MemoryCurrent']) <= SERVICE_MEMORY and memory() >= MEMORY_RESERVE
                and disk() >= DISK_RESERVE, 'runtime_resource_gate')
        require(unit_values(UPDATER)['ActiveState'] == 'inactive', 'updater_active')
        result['status'] = 'SCANNER_INSTALLED_AND_SCAN_VERIFIED'
        exclusive(BASE/'configure-result.json', (json.dumps(result, sort_keys=True)+'\n').encode())
    except (OSError, ValueError, KeyError, RuntimeError, MemoryError, subprocess.SubprocessError) as exc:
        signal.alarm(0)
        result.update(status='UNKNOWN', failedPhase=phase, errorType=type(exc).__name__)
        if type(exc) is RuntimeError and re.fullmatch('[a-z_]+', str(exc)):
            result['errorCode'] = str(exc)
        if activation_attempted:
            try:
                command(['/usr/bin/systemctl', 'disable', '--now', DAEMON], timeout=45)
                state = unit_values(DAEMON)
                result['failureScannerStoppedAndDisabled'] = (
                    state['ActiveState'] in ['inactive', 'failed'] and state['UnitFileState'] == 'disabled')
            except (OSError, ValueError, RuntimeError, subprocess.SubprocessError):
                result['failureScannerStoppedAndDisabled'] = False
    finally:
        signal.alarm(0)
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status'] == 'SCANNER_INSTALLED_AND_SCAN_VERIFIED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
