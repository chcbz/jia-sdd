#!/usr/bin/env python3
"""Configure signed staged ClamAV, validate full databases, then activate a bounded scanner."""
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
    data = command(['/usr/bin/systemctl','show',name,'--property=ActiveState,SubState,Result,ExecMainStatus,MainPID,MemoryCurrent,MemoryMax,User,Group,UnitFileState,ExecMainStartTimestampMonotonic,ExecMainExitTimestampMonotonic','--no-pager'])
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


def main():
    result = {'startedAtEpoch':int(time.time()),'status':'UNKNOWN','apiRestartRequested':False,
              'rpmTransactionRequested':False,'scheduledUpdaterEnabled':False}
    phase = 'preflight'
    units_created = False
    def expired(signum,frame):
        raise RuntimeError('installer_deadline')
    signal.signal(signal.SIGALRM,expired)
    signal.alarm(1200)
    try:
        require(os.geteuid()==0 and os.uname().machine=='x86_64','host_identity')
        for parent in [Path('/opt'),Path('/opt/cyf'),BASE,BASE/'usr',BASE/'usr/bin',BASE/'usr/sbin',BASE/'usr/lib64',Path('/etc'),Path('/var'),Path('/var/lib'),UNITDIR]:
            info=parent.lstat()
            require(stat.S_ISDIR(info.st_mode) and info.st_uid==0 and not stat.S_IMODE(info.st_mode)&0o022,'untrusted_parent')
        for path in [CONFIG,STATE,UNITDIR/DAEMON,UNITDIR/UPDATER,BASE/'configure-intent.json']:
            require(not os.path.lexists(path),'existing_configuration')
        try:pwd.getpwnam(USER)
        except KeyError:pass
        else:raise RuntimeError('existing_user')
        try:grp.getgrnam(USER)
        except KeyError:pass
        else:raise RuntimeError('existing_group')
        identities={}
        for row in MANIFEST:
            path=BASE/row['path']
            if row['type']=='regular':identities[row['path']]=read_hash(path,row)
            else:
                info=path.lstat()
                require(stat.S_ISLNK(info.st_mode) and info.st_uid==0 and os.readlink(path)==row['target'],'staged_link_identity')
        with socket.socket() as s:s.bind(('127.0.0.1',13310))
        result.update(diskAvailableBefore=disk(),memAvailableBefore=memory(),diskReserveBytes=DISK_RESERVE,
                      knownDatabasePeakBytes=DATABASE_PEAK,serviceMemoryLimitBytes=SERVICE_MEMORY,memoryReserveBytes=MEMORY_RESERVE)
        require(disk()>=DISK_RESERVE+DATABASE_PEAK and memory()>=SERVICE_MEMORY+MEMORY_RESERVE,'resource_gate')
        phase='configure_new_service'
        exclusive(BASE/'configure-intent.json',(json.dumps(result)+'\n').encode())
        command(['/usr/sbin/useradd','--system','--user-group','--no-create-home','--home-dir',str(STATE),'--shell','/sbin/nologin',USER])
        user=pwd.getpwnam(USER)
        require(user.pw_uid!=0 and grp.getgrnam(USER).gr_gid==user.pw_gid and user.pw_dir==str(STATE) and user.pw_shell=='/sbin/nologin','created_identity')
        CONFIG.mkdir(mode=0o755)
        STATE.mkdir(mode=0o750)
        (STATE/'db').mkdir(mode=0o750)
        for path in [STATE,STATE/'db']:os.chown(path,user.pw_uid,user.pw_gid)
        for path in [BASE,BASE/'usr',BASE/'usr/bin',BASE/'usr/sbin',BASE/'usr/lib64']:os.chmod(path,0o755)
        fresh=f'''DatabaseDirectory {STATE}/db
DatabaseOwner {USER}
DatabaseMirror database.clamav.net
Foreground yes
MaxAttempts 2
ConnectTimeout 20
ReceiveTimeout 60
TestDatabases yes
ScriptedUpdates no
'''
        clam=f'''DatabaseDirectory {STATE}/db
TCPSocket 13310
TCPAddr 127.0.0.1
Foreground yes
MaxThreads 1
MaxQueue 2
StreamMaxLength 60M
MaxFileSize 60M
MaxScanSize 100M
AlertExceedsMax yes
ConcurrentDatabaseReload no
ReadTimeout 120
CommandReadTimeout 10
'''
        exclusive(CONFIG/'freshclam.conf',fresh.encode(),0o644)
        exclusive(CONFIG/'clamd.conf',clam.encode(),0o644)
        for binary,conf in [('usr/bin/freshclam','freshclam.conf'),('usr/sbin/clamd','clamd.conf')]:
            version=command([str(BASE/binary),'--config-file='+str(CONFIG/conf),'--version'],private_libs=True).strip()
            require(version=='ClamAV 1.4.6','configured_version')
        result['configuredVersionsVerified']=True
        exclusive(UNITDIR/UPDATER,unit_text('CYF initial full signed antivirus database validation',str(BASE/'usr/bin/freshclam')+' --config-file='+str(CONFIG/'freshclam.conf'),True).encode(),0o644)
        exclusive(UNITDIR/DAEMON,unit_text('CYF Agent output antivirus scanner',str(BASE/'usr/sbin/clamd')+' --config-file='+str(CONFIG/'clamd.conf')).encode(),0o644)
        units_created=True
        command(['/usr/bin/systemctl','daemon-reload'])
        phase='signed_database_bootstrap'
        require(memory()>=SERVICE_MEMORY+MEMORY_RESERVE,'bootstrap_resource_gate')
        command(['/usr/bin/systemctl','start','--no-block',UPDATER])
        deadline=time.monotonic()+620
        while True:
            state=unit_values(UPDATER)
            require(time.monotonic()<deadline,'bootstrap_deadline')
            require(state['ActiveState']!='failed','bootstrap_service_failed')
            if state['ActiveState']=='inactive' and int(state.get('ExecMainStartTimestampMonotonic','0'))>0:
                require(int(state.get('ExecMainExitTimestampMonotonic','0'))>=int(state['ExecMainStartTimestampMonotonic']) and state['Result']=='success' and state['ExecMainStatus']=='0','bootstrap_exit_failed')
                break
            time.sleep(2)
        require(memory()>=SERVICE_MEMORY+MEMORY_RESERVE,'daemon_resource_gate')
        result['databases']=[]
        for name in ['main.cvd','daily.cvd','bytecode.cvd']:
            path=STATE/'db'/name
            info=path.lstat()
            require(stat.S_ISREG(info.st_mode) and info.st_uid==user.pw_uid and 512<=info.st_size<=256*1024**2,'database_identity')
            output=command([str(BASE/'usr/bin/sigtool'),'--info',str(path)],private_libs=True)
            require('Verification OK.' in output,'database_signature_invalid')
            digest=hashlib.sha256()
            with path.open('rb') as f:
                for data in iter(lambda:f.read(1024*1024),b''):digest.update(data)
            result['databases'].append({'name':name,'bytes':info.st_size,'sha256':digest.hexdigest(),'signatureVerified':True})
        require(sum(x['bytes'] for x in result['databases'])<=512*1024**2 and disk()>=DISK_RESERVE,'database_disk_budget')
        phase='activate_scanner'
        command(['/usr/bin/systemctl','enable','--now',DAEMON],timeout=30)
        deadline=time.monotonic()+120
        while True:
            try:
                if protocol(b'zPING\0')=='PONG':break
            except OSError:pass
            require(time.monotonic()<deadline,'scanner_readiness_deadline')
            time.sleep(2)
        state=unit_values(DAEMON)
        pid=int(state['MainPID'])
        require(pid>1 and state['User']==USER and state['Group']==USER and int(state['MemoryMax'])==SERVICE_MEMORY,'unit_identity')
        proc=Path('/proc')/str(pid)
        start=(proc/'stat').read_text().rsplit(')',1)[1].split()[19]
        status=dict(line.split(':',1) for line in (proc/'status').read_text().splitlines() if ':' in line)
        require([int(x) for x in status['Uid'].split()]==[user.pw_uid]*4 and [int(x) for x in status['Gid'].split()]==[user.pw_gid]*4,'process_identity')
        exe=os.stat(proc/'exe');identity=identities['usr/sbin/clamd']
        require(os.readlink(proc/'exe')==str(BASE/'usr/sbin/clamd') and (exe.st_dev,exe.st_ino)==(identity['device'],identity['inode']),'running_binary_identity')
        result['scans']=[]
        phase='real_scan_validation'
        for name,content,expected in [('clean',b'CYF output scanner production probe\n','stream: OK'),('eicar',EICAR,' FOUND'),('member_61_mib',archive([61]),'Heuristics.Limits.Exceeded'),('aggregate_110_mib',archive([55,55]),'Heuristics.Limits.Exceeded')]:
            began=time.monotonic();response=protocol(b'zINSTREAM\0',content)
            require(response==expected if name=='clean' else expected in response,'scan_result_mismatch')
            result['scans'].append({'case':name,'inputBytes':len(content),'sha256':hashlib.sha256(content).hexdigest(),'expectedMatched':True,'elapsedSeconds':round(time.monotonic()-began,3)})
        require((proc/'stat').read_text().rsplit(')',1)[1].split()[19]==start,'process_changed')
        state=unit_values(DAEMON)
        result.update(runtimeIdentity={'pid':pid,'startTicks':start,'uid':user.pw_uid,'gid':user.pw_gid,'exeSha256':identity['sha256'],'memoryCurrentBytes':int(state['MemoryCurrent'])},
                      memAvailableAfter=memory(),diskAvailableAfter=disk(),version=protocol(b'zVERSION\0'))
        require(int(state['MainPID'])==pid and state['ActiveState']=='active' and int(state['MemoryCurrent'])<=SERVICE_MEMORY and memory()>=MEMORY_RESERVE and disk()>=DISK_RESERVE,'runtime_resource_gate')
        result['status']='SCANNER_INSTALLED_AND_SCAN_VERIFIED'
        exclusive(BASE/'configure-result.json',(json.dumps(result,sort_keys=True)+'\n').encode())
    except (OSError,ValueError,KeyError,RuntimeError,MemoryError,subprocess.SubprocessError) as exc:
        signal.alarm(0)
        result.update(status='UNKNOWN',failedPhase=phase,errorType=type(exc).__name__)
        if type(exc) is RuntimeError and re.fullmatch('[a-z_]+',str(exc)):result['errorCode']=str(exc)
        if units_created:
            try:
                command(['/usr/bin/systemctl','disable','--now',DAEMON,UPDATER],timeout=45)
                states=[unit_values(x) for x in [DAEMON,UPDATER]]
                result['failureServicesStoppedAndDisabled']=all(x['ActiveState'] in ['inactive','failed'] and x['UnitFileState']=='disabled' for x in states)
            except (OSError,ValueError,RuntimeError,subprocess.SubprocessError):result['failureServicesStoppedAndDisabled']=False
    finally:signal.alarm(0)
    result['diskAvailableAfter']=disk()
    print(json.dumps(result,sort_keys=True))
    return 0 if result['status']=='SCANNER_INSTALLED_AND_SCAN_VERIFIED' else 1


if __name__=='__main__':
    raise SystemExit(main())
