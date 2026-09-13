#!/usr/bin/env python3
"""Stage pinned signed ClamAV payloads; no RPM transaction or service activation."""
import gzip
import hashlib
import io
import json
import lzma
import os
from pathlib import Path
import re
import resource
import shutil
import signal
import stat
import struct
import subprocess
import time
import urllib.request

PACKAGES = [{'name': 'clamav', 'arch': 'x86_64', 'version': {'epoch': '0', 'ver': '1.4.6', 'rel': '1.el8'}, 'rpm': 'Packages/c/clamav-1.4.6-1.el8.x86_64.rpm', 'sha256': '26c0d752dde2bce847c4c482a45faf3c154509d0db42cad8eafa38b673741485', 'bytes': '7303280'}, {'name': 'clamav-lib', 'arch': 'x86_64', 'version': {'epoch': '0', 'ver': '1.4.6', 'rel': '1.el8'}, 'rpm': 'Packages/c/clamav-lib-1.4.6-1.el8.x86_64.rpm', 'sha256': '750a489e2da29989cbf5690fea84ae7dd5ccf70ae464ed03b2a68d0e43ba2afe', 'bytes': '4257924'}, {'name': 'clamd', 'arch': 'x86_64', 'version': {'epoch': '0', 'ver': '1.4.6', 'rel': '1.el8'}, 'rpm': 'Packages/c/clamd-1.4.6-1.el8.x86_64.rpm', 'sha256': '98900509e74e6b989770bf6dc06485ad1286994fb36fb1299ef44eee00e0f061', 'bytes': '134244'}, {'name': 'clamav-freshclam', 'arch': 'x86_64', 'version': {'epoch': '0', 'ver': '1.4.6', 'rel': '1.el8'}, 'rpm': 'Packages/c/clamav-freshclam-1.4.6-1.el8.x86_64.rpm', 'sha256': 'ebdcd6cc94391fc05a2565237f4f34c6d029944db2558e9427b2a65aaf2230d6', 'bytes': '3566940', 'providesLegacyName': True}]
MANIFEST = [{'package': 'clamav', 'rpmSha256': '26c0d752dde2bce847c4c482a45faf3c154509d0db42cad8eafa38b673741485', 'payloadCodec': 'xz', 'payloadBytesRead': 20552672, 'members': [{'path': 'usr/bin/clamscan', 'mode': '0o755', 'bytes': 193984, 'sha256': '4c662ebca789e371eb97fcd6ec2ff44b3445211bd6f5f87808c4a396bbed3989', 'type': 'regular'}, {'path': 'usr/bin/sigtool', 'mode': '0o755', 'bytes': 9587448, 'sha256': '1a6010478d9361b3bf27fc700ba87447b7fcbfa12358251f9c0160ddd201fe15', 'type': 'regular'}]}, {'package': 'clamav-lib', 'rpmSha256': '750a489e2da29989cbf5690fea84ae7dd5ccf70ae464ed03b2a68d0e43ba2afe', 'payloadCodec': 'xz', 'payloadBytesRead': 11507080, 'members': [{'path': 'usr/lib64/libclamav.so.12', 'mode': '0o777', 'bytes': 19, 'sha256': '3c9b7fb194d079740744d66a329096b72c522ada5dc2ea566b8e3c87471dcb17', 'type': 'symlink', 'target': 'libclamav.so.12.0.3'}, {'path': 'usr/lib64/libclamav.so.12.0.3', 'mode': '0o755', 'bytes': 11421696, 'sha256': 'f2eb53c3b86f2f01449ef57d5970efd47f36fd3c33c6e027e342493c6c6d748e', 'type': 'regular'}, {'path': 'usr/lib64/libclammspack.so.0', 'mode': '0o777', 'bytes': 22, 'sha256': '462d1f655fb5c241ac8b821dfa923d8cd0274df9f634fe86e0b4d8455092a6bd', 'type': 'symlink', 'target': 'libclammspack.so.0.8.0'}, {'path': 'usr/lib64/libclammspack.so.0.8.0', 'mode': '0o755', 'bytes': 78840, 'sha256': 'cdebda20f8fbe3f64341a60fa12b3282d412becc95f8e9c197cae4f538bb277b', 'type': 'regular'}]}, {'package': 'clamd', 'rpmSha256': '98900509e74e6b989770bf6dc06485ad1286994fb36fb1299ef44eee00e0f061', 'payloadCodec': 'xz', 'payloadBytesRead': 268320, 'members': [{'path': 'usr/sbin/clamd', 'mode': '0o755', 'bytes': 223024, 'sha256': '4af6f9bfab10e9b18f051e7ba8e299766a6eeae9bead3c482678b55afdae2b8a', 'type': 'regular'}]}, {'package': 'clamav-freshclam', 'rpmSha256': 'ebdcd6cc94391fc05a2565237f4f34c6d029944db2558e9427b2a65aaf2230d6', 'payloadCodec': 'xz', 'payloadBytesRead': 9690824, 'members': [{'path': 'usr/bin/freshclam', 'mode': '0o755', 'bytes': 83568, 'sha256': '91029892d3ce03a17cf2c56bf273fe12d3c800cf6bc2e6bf75d58d9de758dbab', 'type': 'regular'}, {'path': 'usr/lib64/libfreshclam.so.3', 'mode': '0o777', 'bytes': 21, 'sha256': '3297218ef05a4dd3ec638b4fc3be8426f26a5b2d9de9032c1aa99d617e1eb4cf', 'type': 'symlink', 'target': 'libfreshclam.so.3.0.2'}, {'path': 'usr/lib64/libfreshclam.so.3.0.2', 'mode': '0o755', 'bytes': 9591216, 'sha256': '9f90f21ddb393ac49773a862c88baadebc2d72dc54675b322ffef90ea33ed0b3', 'type': 'regular'}]}]

BASE = Path('/opt/cyf/output-scanner')
KEY_SHA = 'cd1db21a863185127f2e3b264c97fb1c6c44c316385707999041ea475c110d1c'
KEY_FINGERPRINT = '94E279EB8D8F25B21810ADF121EA45AB2F86D6A1'
ENV = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'HOME': '/root', 'LC_ALL': 'C', 'LANG': 'C'}
RESERVE = 3584 * 1024**2
PEAK = 128 * 1024**2


def require(condition, code):
    if not condition:
        raise RuntimeError(code)


def exclusive(path, data, mode=0o600):
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, mode)
    with os.fdopen(fd, 'wb') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())


def memory():
    values = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
    return {key+'Bytes': int(values[key].split()[0])*1024 for key in
            ['MemTotal', 'MemAvailable', 'SwapTotal', 'SwapFree']}


def download(url, path, size, digest):
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    deadline = time.monotonic()+90
    value = hashlib.sha256()
    count = 0
    fd = os.open(str(path), os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
    with os.fdopen(fd, 'wb') as target, opener.open(url, timeout=20) as source:
        while True:
            require(time.monotonic() < deadline, 'download_deadline')
            data = source.read(1024*1024)
            if not data:
                break
            count += len(data)
            require(count <= size, 'download_size_limit')
            value.update(data)
            target.write(data)
        target.flush()
        os.fsync(target.fileno())
    require(count == size and value.hexdigest() == digest, 'download_integrity')


def child_limits():
    resource.setrlimit(resource.RLIMIT_AS, (256*1024**2, 256*1024**2))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
    resource.setrlimit(resource.RLIMIT_FSIZE, (16*1024**2, 16*1024**2))


def command(args, private_libs=False):
    env = dict(ENV)
    if private_libs:
        env['LD_LIBRARY_PATH'] = str(BASE/'usr/lib64')
    # Output is local and bounded by a regular file + RLIMIT_FSIZE; never exported raw.
    with (BASE/'command-output').open('w+b') as output:
        p = subprocess.run(args, stdin=subprocess.DEVNULL, stdout=output, stderr=subprocess.STDOUT,
                           env=env, timeout=25, check=False, preexec_fn=child_limits)
        output.seek(0)
        data = output.read(65537)
    require(len(data) <= 65536, 'command_output_limit')
    require(p.returncode == 0, 'command_exit_nonzero')
    return data.decode('utf-8', errors='strict')


def fingerprint(data):
    import base64
    lines = data.decode('ascii').splitlines()
    start = lines.index('-----BEGIN PGP PUBLIC KEY BLOCK-----')+1
    while lines[start].strip():
        start += 1
    start += 1
    raw = base64.b64decode(''.join(line for line in lines[start:] if line and not line.startswith(('=', '-'))), validate=True)
    require(raw[0]&0x80 and not raw[0]&0x40 and (raw[0]>>2)&15 == 6, 'key_packet_type')
    length_kind = raw[0]&3
    require(length_kind in (0, 1, 2), 'key_packet_length')
    n = 1 << length_kind
    length = int.from_bytes(raw[1:1+n], 'big')
    body = raw[1+n:1+n+length]
    require(len(body) == length and body[0] == 4 and length < 65536, 'key_packet_version')
    return hashlib.sha1(b'\x99'+length.to_bytes(2, 'big')+body).hexdigest().upper()


def extract(rpm, expected):
    data = rpm.read_bytes()
    require(len(data)<16*1024**2 and data[:4] == b'\xed\xab\xee\xdb', 'rpm_format')
    def header(offset):
        require(offset+16<=len(data) and data[offset:offset+4] == b'\x8e\xad\xe8\x01', 'rpm_header')
        n, size = struct.unpack('>II', data[offset+8:offset+16])
        require(n<10000 and size<16*1024**2, 'rpm_header_limit')
        start = offset+16+n*16
        require(start+size<=len(data), 'rpm_header_bounds')
        return start+size
    sigend = header(96)
    start = header((sigend+7)//8*8)
    f = lzma.LZMAFile(io.BytesIO(data[start:]))
    total, count = 0, 0
    wanted = {row['path']: row for row in expected}
    seen = set()
    def read(n):
        nonlocal total
        require(0<=n<=64*1024**2, 'payload_member_limit')
        total += n
        require(total<=256*1024**2, 'payload_total_limit')
        result = f.read(n)
        require(len(result)==n, 'payload_truncated')
        return result
    while True:
        h = read(110)
        require(h[:6] == b'070701', 'cpio_format')
        values = [int(h[6+i*8:14+i*8], 16) for i in range(13)]
        mode, size, namesize = values[1], values[6], values[11]
        require(1<=namesize<=4096 and size<=64*1024**2, 'cpio_member_limit')
        name = read(namesize)
        require(name.endswith(b'\0'), 'cpio_name')
        name = name[:-1].decode()
        read((-(110+namesize))%4)
        if name == 'TRAILER!!!':
            require(size == 0, 'cpio_trailer')
            break
        count += 1
        require(count<=20000, 'cpio_count')
        payload = read(size)
        read((-size)%4)
        path = name[2:] if name.startswith('./') else name
        if path not in wanted:
            continue
        require(path not in seen, 'duplicate_payload')
        seen.add(path)
        row = wanted[path]
        require(size == row['bytes'] and hashlib.sha256(payload).hexdigest() == row['sha256'], 'payload_integrity')
        destination = BASE/path
        require(not os.path.lexists(destination), 'existing_payload')
        if row['type'] == 'regular':
            require(stat.S_ISREG(mode) and stat.S_IMODE(mode)==0o755 and
                    payload[:5]==b'\x7fELF\x02' and payload[18:20]==b'\x3e\x00', 'elf_identity')
            exclusive(destination, payload, 0o755)
        else:
            require(stat.S_ISLNK(mode) and payload.decode()==row['target'] and
                    '/' not in row['target'] and row['target'] not in ('.', '..'), 'payload_link')
            os.symlink(row['target'], destination)
    f.close()
    require(seen == set(wanted), 'missing_payload')
    return {'membersVerified': len(seen), 'payloadBytesRead': total}


def expired(signum, frame):
    raise RuntimeError('stage_deadline')


def main():
    result = {'startedAtEpoch': int(time.time()), 'status': 'UNKNOWN', 'rpmTransactionRequested': False,
              'serviceActivationRequested': False, 'signaturesDatabaseDownloaded': False,
              'apiRestartRequested': False}
    phase = 'preflight'
    signal.signal(signal.SIGALRM, expired)
    signal.alarm(450)
    try:
        require(os.geteuid()==0 and os.uname().machine=='x86_64', 'host_identity')
        require(not os.path.lexists(BASE), 'existing_stage')
        for ancestor in [Path('/opt'), Path('/opt/cyf')]:
            info = ancestor.lstat()
            require(stat.S_ISDIR(info.st_mode) and info.st_uid==0 and not stat.S_IMODE(info.st_mode)&0o022, 'untrusted_parent')
        for program in [Path('/usr/bin/rpm'), Path('/lib64/ld-linux-x86-64.so.2')]:
            info = program.stat()
            require(stat.S_ISREG(info.st_mode) and info.st_uid==0 and not stat.S_IMODE(info.st_mode)&0o022, 'untrusted_host_tool')
        result.update(memoryBefore=memory(), diskAvailableBefore=shutil.disk_usage('/opt').free,
                      diskReserveBytes=RESERVE, knownStagePeakBytes=PEAK)
        require(result['diskAvailableBefore']>=RESERVE+PEAK and result['memoryBefore']['MemAvailableBytes']>=768*1024**2, 'resource_gate')
        BASE.mkdir(mode=0o700)
        exclusive(BASE/'stage-intent.json', (json.dumps(result)+'\n').encode())
        for name in ['rpmdb', 'packages', 'usr', 'usr/bin', 'usr/sbin', 'usr/lib64']:
            (BASE/name).mkdir(mode=0o700)
        phase = 'download_signing_key'
        key = BASE/'RPM-GPG-KEY-EPEL-8'
        download('https://dl.fedoraproject.org/pub/epel/RPM-GPG-KEY-EPEL-8', key, 1627, KEY_SHA)
        require(fingerprint(key.read_bytes())==KEY_FINGERPRINT, 'key_fingerprint')
        phase = 'private_key_import'
        dbargs = ['/usr/bin/rpm', '--dbpath', str(BASE/'rpmdb')]
        command(dbargs+['--initdb'])
        command(dbargs+['--import', str(key)])
        result['keyFingerprint'] = KEY_FINGERPRINT
        result['packages'] = []
        for package in PACKAGES:
            phase = 'download_'+package['name']
            path = BASE/'packages'/Path(package['rpm']).name
            download('https://mirrors.aliyun.com/epel/8/Everything/x86_64/'+package['rpm'], path,
                     int(package['bytes']), package['sha256'])
            phase = 'verify_'+package['name']
            output = command(dbargs+['--checksig', '--verbose', str(path)])
            require(re.search(r'Signature, key ID 2f86d6a1: OK', output, re.I) is not None and
                    not re.search(r'NOT OK|NOKEY|NOTTRUSTED|BAD|UNSIGNED', output, re.I), 'rpm_signature_invalid')
            selected = next(row for row in MANIFEST if row['package']==package['name'])
            require(selected['rpmSha256']==package['sha256'], 'manifest_rpm_identity')
            phase = 'extract_'+package['name']
            row = extract(path, selected['members'])
            result['packages'].append(dict(name=package['name'], rpmSha256=package['sha256'], signatureVerified=True, **row))
        phase = 'dynamic_dependencies'
        result['executables'] = []
        for rel in ['usr/bin/clamscan', 'usr/bin/sigtool', 'usr/bin/freshclam', 'usr/sbin/clamd']:
            path = BASE/rel
            dependencies = command(['/lib64/ld-linux-x86-64.so.2', '--list', str(path)], private_libs=True)
            require('not found' not in dependencies, 'missing_library')
            libraries = []
            for match in re.finditer(r'=> (/[^\s]+)', dependencies):
                library = Path(match.group(1))
                require(library.is_absolute() and '..' not in library.parts, 'loader_path')
                info = library.stat()
                require(stat.S_ISREG(info.st_mode) and info.st_uid==0 and not stat.S_IMODE(info.st_mode)&0o022, 'untrusted_library')
                libraries.append(str(library))
            require(libraries, 'no_loader_dependencies')
            version = command([str(path), '--version'], private_libs=True).strip()
            require(re.fullmatch(r'ClamAV 1\.4\.6', version) is not None, 'executable_version')
            result['executables'].append({'path': rel, 'version': version, 'libraries': libraries})
        result.update(status='SCANNER_BINARIES_STAGED', memoryAfter=memory(), diskAvailableAfter=shutil.disk_usage('/opt').free)
        require(result['diskAvailableAfter']>=RESERVE, 'final_disk_reserve')
        exclusive(BASE/'stage-result.json', (json.dumps(result,sort_keys=True)+'\n').encode())
    except (OSError, ValueError, KeyError, RuntimeError, subprocess.SubprocessError, lzma.LZMAError) as exc:
        result.update(status='UNKNOWN', failedPhase=phase,
                      errorCode=str(exc) if type(exc) is RuntimeError and re.fullmatch(r'[a-z_]+',str(exc)) else type(exc).__name__)
    finally:
        signal.alarm(0)
    result['diskAvailableAfter'] = shutil.disk_usage('/opt').free
    print(json.dumps(result, sort_keys=True))
    return 0 if result['status']=='SCANNER_BINARIES_STAGED' else 1


if __name__ == '__main__':
    raise SystemExit(main())
