#!/usr/bin/env python3
"""Resolve three approved distro caches in a private capped mount namespace; no RPM install."""
import configparser
import contextlib
import ctypes
import glob
import hashlib
import json
import os
from pathlib import Path
import re
import selectors
import signal
import stat
import subprocess
import sys
import tempfile
import time
from urllib.parse import urlsplit

REPOS = ('alinux3-os', 'alinux3-updates', 'epel')
HOSTS = ('mirrors.cloud.aliyuncs.com', 'mirrors.aliyun.com')
ENV = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'HOME': '/root', 'LC_ALL': 'C', 'LANG': 'C'}


def read_trusted(path, limit):
    fd = os.open(str(path), os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        st = os.fstat(f.fileno())
        if not stat.S_ISREG(st.st_mode) or st.st_uid != 0 or st.st_mode & 0o022:
            raise ValueError('file_identity')
        data = f.read(limit+1)
    if len(data) > limit:
        raise ValueError('file_size')
    return data


def approved_repos():
    # Public vendor endpoints observed from this development host; no host repo config is read.
    os_path = os.path.realpath('/etc/os-release')
    if os_path not in ('/etc/os-release', '/usr/lib/os-release'):
        raise ValueError('os_release_path')
    os_release = read_trusted(os_path, 8192).decode()
    values = dict(line.split('=', 1) for line in os_release.splitlines() if '=' in line and not line.startswith('#'))
    if values.get('ID', '').strip('"') != 'alinux' or values.get('VERSION_ID', '').strip('"') != '3' or os.uname().machine != 'x86_64':
        raise ValueError('distribution_identity')
    return {
        'alinux3-os': {'baseurl': 'https://mirrors.aliyun.com/alinux/3/os/x86_64/', 'host': 'mirrors.aliyun.com'},
        'alinux3-updates': {'baseurl': 'https://mirrors.aliyun.com/alinux/3/updates/x86_64/', 'host': 'mirrors.aliyun.com'},
        'epel': {'baseurl': 'https://mirrors.aliyun.com/epel/8/Everything/x86_64/', 'host': 'mirrors.aliyun.com'},
    }


@contextlib.contextmanager
def capped_workspace():
    libc = ctypes.CDLL(None, use_errno=True)
    libc.mount.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_ulong, ctypes.c_char_p]
    libc.umount2.argtypes = [ctypes.c_char_p, ctypes.c_int]
    if libc.unshare(0x00020000) != 0: # CLONE_NEWNS
        raise ValueError('mount_namespace_unavailable')
    if libc.mount(None, b'/', None, (1 << 18) | 16384, None) != 0: # MS_PRIVATE | MS_REC
        raise ValueError('mount_namespace_not_private')
    with tempfile.TemporaryDirectory(prefix='cyf-scanner-plan-', dir='/var/tmp') as temp:
        target = os.fsencode(temp)
        if libc.mount(b'tmpfs', target, b'tmpfs', 2 | 4 | 8, b'size=256m,mode=0700') != 0:
            raise ValueError('bounded_tmpfs_unavailable')
        try:
            yield Path(temp)
        finally:
            if libc.umount2(target, 0) != 0:
                raise ValueError('bounded_tmpfs_cleanup_failed')


def run(command):
    p = subprocess.Popen(command, env=ENV, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT, start_new_session=True)
    selector = selectors.DefaultSelector()
    selector.register(p.stdout, selectors.EVENT_READ)
    result = bytearray()
    deadline = time.monotonic()+120
    try:
        while selector.get_map():
            if time.monotonic() >= deadline:
                raise ValueError('dnf_timeout')
            for key, _ in selector.select(0.2):
                data = os.read(key.fileobj.fileno(), 65536)
                if not data:
                    selector.unregister(key.fileobj)
                    continue
                if len(result)+len(data) > 2*1024**2:
                    raise ValueError('dnf_output_limit')
                result.extend(data)
        p.wait(timeout=max(0.01, deadline-time.monotonic()))
        return p.returncode, result.decode('utf-8', errors='replace')
    finally:
        try:
            os.killpg(p.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        p.wait(timeout=10)
        selector.close()
        p.stdout.close()


def parse(code, raw):
    rows = []
    pending = ''
    in_table = False
    finished = False
    bad = False
    aborted = 0
    seen = set()
    for line in raw.splitlines():
        line = line.strip()
        if line == 'Operation aborted.':
            aborted += 1
        if re.search(r'(?i)(error:|failed|no match for argument|cannot |could not |unable to|problem:|ignoring repositories|skip.*repositor)', line):
            bad = True
        if line in ('Installing:', 'Installing dependencies:'):
            bad |= bool(pending)
            in_table = True
            continue
        if line == 'Transaction Summary':
            bad |= bool(pending) or not in_table
            in_table = False
            finished = True
            continue
        if in_table:
            if not line or re.fullmatch(r'=+', line):
                continue
            pending = (pending+' '+line).strip()
            parts = pending.split()
            if len(parts)<6 and len(pending)<500:
                continue
            if (len(parts)==6 and re.fullmatch(r'[A-Za-z0-9_.+-]{1,100}',parts[0])
                    and parts[1] in ('x86_64','noarch') and re.fullmatch(r'[A-Za-z0-9:_.+~^-]{1,100}',parts[2])
                    and parts[3] in REPOS and re.fullmatch(r'[0-9.]+',parts[4]) and parts[5] in ('k','M','G','T')
                    and tuple(parts[:4]) not in seen and len(seen)<256):
                seen.add(tuple(parts[:4]))
                rows.append(dict(zip(('name','arch','version','repository'),parts[:4])))
            else:
                bad = True
            pending = ''
    complete = ({'clamav','clamd','clamav-freshclam'}.issubset({r['name'] for r in rows})
                and code==1 and aborted==1 and finished and not (bad or pending or in_table))
    return {'status': 'complete_network_plan' if complete else 'UNKNOWN', 'packages': rows,
            'dnfExitCode':code,'automaticRefusalCount':aborted,'parseProblem':bool(bad or pending or in_table)}


def main():
    out = {'observedAtEpoch':int(time.time()),'status':'UNKNOWN','packageInstallRequested':False,
           'cacheLimitBytes':256*1024**2,'privateMountNamespaceRequested':True}
    phase = 'preflight'
    try:
        if os.geteuid()!=0:
            raise ValueError('root_required')
        st=os.statvfs('/var/tmp');out['diskAvailableBefore']=st.f_bavail*st.f_frsize
        memory=dict(line.split(':',1) for line in Path('/proc/meminfo').read_text().splitlines())
        out['memAvailableBefore']=int(memory['MemAvailable'].split()[0])*1024
        if out['diskAvailableBefore']<4*1024**3 or out['memAvailableBefore']<1536*1024**2:
            raise ValueError('resource_gate')
        repos=approved_repos()
        out['repositories']=[{'id':rid,'scheme':'https','host':repos[rid]['host']} for rid in REPOS]
        phase='bounded_metadata_plan'
        with capped_workspace() as temp:
            out['privateMountNamespaceCreated'] = True
            repo_dir=temp/'repos';repo_dir.mkdir()
            text=''.join('['+rid+']\nname='+rid+'\nbaseurl='+repos[rid]['baseurl']+'\nenabled=1\ngpgcheck=1\nsslverify=1\nskip_if_unavailable=False\n\n' for rid in REPOS)
            (repo_dir/'approved.repo').write_text(text)
            config=temp/'dnf.conf'
            config.write_text('[main]\nplugins=0\nreposdir='+str(repo_dir)+'\ncachedir='+str(temp/'cache')+'\nsystem_cachedir='+str(temp/'cache')+'\nlogdir='+str(temp/'logs')+'\npersistdir='+str(temp/'state')+'\nvarsdir='+str(temp/'vars')+'\ninstall_weak_deps=False\ngpgcheck=1\nsslverify=1\nskip_if_unavailable=False\nlog_size=1048576\nlog_rotate=0\n')
            command=['/usr/bin/dnf','--config='+str(config),'--noplugins','--assumeno','--disablerepo=*']+['--enablerepo='+x for x in REPOS]+['--setopt=timeout=15','--setopt=retries=0','install','clamav-1.4.6-1.el8.x86_64','clamd-1.4.6-1.el8.x86_64','clamav-freshclam-1.4.6-1.el8.x86_64']
            code,raw=run(command)
            out.update(parse(code,raw))
            out['rpmDownloaded']=any(temp.rglob('*.rpm'))
            cache=os.statvfs(temp);out['temporaryUsedBytes']=(cache.f_blocks-cache.f_bfree)*cache.f_frsize
            if out['rpmDownloaded']:
                out['status']='UNKNOWN'
        out['privateMountRemoved']=True
    except (OSError,ValueError,KeyError,configparser.Error,subprocess.SubprocessError):
        out.update(status='UNKNOWN',failedPhase=phase)
    finally:
        st=os.statvfs('/var/tmp');out['diskAvailableAfter']=st.f_bavail*st.f_frsize
        if out.get('diskAvailableBefore',0)-out['diskAvailableAfter']>16*1024**2:
            out.update(status='UNKNOWN',diskDriftExceeded=True)
    print(json.dumps(out,sort_keys=True))
    return 0 if out['status']=='complete_network_plan' else 1


if __name__=='__main__':
    raise SystemExit(main())
