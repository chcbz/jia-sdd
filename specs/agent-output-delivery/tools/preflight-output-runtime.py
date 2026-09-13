#!/usr/bin/env python3
"""Bounded read-only /opt CYF runtime identification; never exports configuration values."""
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import time

ROOT = '/opt/cyf/service/api'
FILES = [ROOT, ROOT+'/config', '/run/cyf-api', '/usr/local/sbin/cyf-api-kit',
         ROOT+'/cyf-api-kit.jar', '/run/cyf-api/cyf-api-kit.pid',
         '/run/cyf-api/cyf-api-kit.runtime']
CONFIGS = [ROOT+'/'+name for name in ('application.properties', 'application-prod.properties',
                                      'config/application.properties', 'config/application-prod.properties')]
HISTORICAL_HELPER_SHA = 'b333df940a58640a59b46ebd29d301fe2a82e22b3745598693179a004e74d525'


def read_small(path, limit):
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    with os.fdopen(fd, 'rb') as f:
        data = f.read(limit+1)
    if len(data) > limit:
        raise ValueError('oversize')
    return data


def metadata(path, max_hash_bytes=0):
    row = {'path': path}
    try:
        info = os.lstat(path)
        row.update(exists=True, uid=info.st_uid, gid=info.st_gid,
                   mode=oct(stat.S_IMODE(info.st_mode)), size=info.st_size,
                   symlink=stat.S_ISLNK(info.st_mode), regular=stat.S_ISREG(info.st_mode))
        if max_hash_bytes and stat.S_ISREG(info.st_mode) and info.st_size <= max_hash_bytes:
            fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
            h = hashlib.sha256()
            count = 0
            with os.fdopen(fd,'rb') as f:
                before = os.fstat(f.fileno())
                while count <= max_hash_bytes:
                    chunk = f.read(min(1024*1024, max_hash_bytes+1-count))
                    if not chunk:
                        break
                    count += len(chunk)
                    h.update(chunk)
                after = os.fstat(f.fileno())
            identity = lambda x: (x.st_dev,x.st_ino,x.st_mtime_ns,x.st_size)
            if count <= max_hash_bytes and identity(info) == identity(before) == identity(after):
                row['sha256'] = h.hexdigest()
            else:
                row['hashStatus'] = 'changed_or_oversize'
    except FileNotFoundError:
        row['exists'] = False
    except OSError:
        row['status'] = 'unreadable'
    return row


def main():
    rows = [metadata(p, 300*1024*1024 if p.endswith('.jar') else 1024*1024 if p.endswith('/cyf-api-kit') else 0) for p in FILES]
    helper = next(x for x in rows if x['path'].endswith('/cyf-api-kit'))
    helper['matchesHistoricalSourceBe41be7'] = helper.get('sha256') == HISTORICAL_HELPER_SHA
    configs=[]
    for path in CONFIGS:
        row=metadata(path)
        if row.get('regular') and not row.get('symlink'):
            try:
                source=read_small(path,65536).decode('utf-8')
                keys=[]
                for line in source.splitlines():
                    key=line.strip().split('=',1)[0].strip()
                    if re.fullmatch(r'(?:agent\.(?:output-delivery|rabbit-broker|rabbit-dispatch|rabbit-topology|rabbit-publish|rabbit-consume|command-outbox)|spring\.config)[A-Za-z0-9_.\[\]-]*', key):
                        keys.append(key)
                row['relevantKeys']=sorted(set(keys))[:100]
                row['keysTruncated']=len(set(keys))>100
            except (OSError,ValueError,UnicodeError):
                row['keyInspectionStatus']='unreadable_or_oversize'
        configs.append(row)
    processes=[]
    for p in Path('/proc').iterdir():
        if not p.name.isdecimal():continue
        try:
            if read_small(p/'comm',17).rstrip(b'\n')!=b'java':continue
            args=[v.decode('utf-8') for v in read_small(p/'cmdline',65536).split(b'\0') if v]
            if ROOT+'/cyf-api-kit.jar' not in args:continue
            ticks=read_small(p/'stat',16384).decode().split(') ',1)[1].split()[19]
            processes.append({'pid':int(p.name),'startTicks':ticks,'exactJarArgument':ROOT+'/cyf-api-kit.jar',
                              'cwdIsServiceRoot':os.readlink(p/'cwd')==ROOT,
                              'prodProfileArgument':'--spring.profiles.active=prod' in args})
        except (OSError,ValueError,UnicodeError,IndexError):continue
    print(json.dumps({'observedAtEpoch':int(time.time()),'readOnly':True,'files':rows,'configs':configs,'processes':processes,
                      'limits':['Only fixed paths, metadata, jar/helper digests and allowlisted property names are exported.',
                                'Existing bounded configuration contents and Java arguments may be inspected in memory; no values/raw arguments are exported.',
                                'No network, SQL, process environment, subprocess, service command, install or file mutation.',
                                'Historical helper correspondence does not itself prove the current Flow delegation or a working backup/rollback.']},sort_keys=True))


if __name__=='__main__':main()
