#!/usr/bin/env python3
"""Bounded, plugin-free, cache-only scanner dependency planning; no RPM transaction."""
import configparser
import glob
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

REQUESTED = ('clamav', 'clamd', 'clamav-update')
# Only these distro/EPEL cache IDs may participate. No network metadata refresh.
REPO_IDS = ('alinux3-os', 'alinux3-updates', 'alinux3-plus', 'alinux3-powertools', 'epel')
ENVIRONMENT = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'HOME': '/root', 'LC_ALL': 'C', 'LANG': 'C'}
LIMIT = 2 * 1024 * 1024


def repo_ids():
    ids = set()
    directory = os.lstat('/etc/yum.repos.d')
    if not stat.S_ISDIR(directory.st_mode) or directory.st_uid != 0 or directory.st_mode & 0o022:
        raise ValueError('repository_directory_identity')
    files = sorted(glob.glob('/etc/yum.repos.d/*.repo'))
    if len(files) > 40:
        raise ValueError('repository_file_limit')
    for name in files:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, 'rb') as f:
            info = os.fstat(f.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_uid != 0 or info.st_mode & 0o022:
                raise ValueError('repository_not_regular')
            data = f.read(65537)
        if len(data) > 65536:
            raise ValueError('repository_size_limit')
        parser = configparser.ConfigParser(interpolation=None, strict=True)
        parser.read_string(data.decode('utf-8'))
        for item in parser.sections():
            if item in ids and item in REPO_IDS:
                raise ValueError('duplicate_allowlisted_repository')
            if re.fullmatch(r'[A-Za-z0-9_.-]{1,100}', item):
                ids.add(item)
    return sorted(ids)


def bounded_run(command):
    output = bytearray()
    process = subprocess.Popen(command, env=ENVIRONMENT, stdin=subprocess.DEVNULL,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
    status = 'exited'
    selector = selectors.DefaultSelector()
    selector.register(process.stdout, selectors.EVENT_READ)
    deadline = time.monotonic() + 120
    try:
        while selector.get_map():
            if time.monotonic() >= deadline:
                status = 'query_timed_out'
                break
            for key, _ in selector.select(min(0.25, max(0, deadline-time.monotonic()))):
                data = os.read(key.fileobj.fileno(), 65536)
                if not data:
                    selector.unregister(key.fileobj)
                    continue
                if len(output) + len(data) > LIMIT:
                    status = 'output_limit_exceeded'
                    break
                output.extend(data)
            if status != 'exited':
                break
        # A process can close stdout and still continue running.
        if status == 'exited':
            try:
                process.wait(timeout=max(0.01, deadline-time.monotonic()))
            except subprocess.TimeoutExpired:
                status = 'query_timed_out'
    finally:
        # Kill any child left in this dedicated group, even when its parent exited.
        try:
            os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        process.wait(timeout=10)
        selector.close()
        process.stdout.close()
    return status, process.returncode, bytes(output)


def main():
    result = {'observedAtEpoch': int(time.time()), 'status': 'UNKNOWN',
              'packageInstallRequested': False, 'networkMetadataRefresh': False,
              'packages': [], 'messages': [], 'pluginsEnabled': False}
    started = time.monotonic()
    try:
        space = os.statvfs('/var/cache/dnf')
        result['diskAvailableBefore'] = space.f_bavail * space.f_frsize
        if result['diskAvailableBefore'] < 4 * 1024**3:
            result['reason'] = 'disk_space_gate'
            return result
        temp_space = os.statvfs('/var/tmp')
        result['temporaryDiskAvailableBefore'] = temp_space.f_bavail * temp_space.f_frsize
        memory = dict(line.split(':', 1) for line in Path('/proc/meminfo').read_text().splitlines())
        result['memAvailableBefore'] = int(memory['MemAvailable'].split()[0]) * 1024
        if result['temporaryDiskAvailableBefore'] < 4 * 1024**3 or result['memAvailableBefore'] < 1536 * 1024**2:
            result['reason'] = 'temporary_disk_or_memory_gate'
            return result
        inventory = repo_ids()
        result['repositoryIds'] = inventory
        selected = [x for x in REPO_IDS if x in inventory]
        result['enabledCacheRepositoryIds'] = selected
        if not selected:
            result['reason'] = 'no_allowlisted_repository_cache'
            return result
        with tempfile.TemporaryDirectory(prefix='cyf-output-dnf-plan-', dir='/var/tmp') as temp:
            config = Path(temp) / 'dnf.conf'
            config.write_text('[main]\nplugins=0\nreposdir=/etc/yum.repos.d\n'
                              'cachedir=/var/cache/dnf\nsystem_cachedir=/var/cache/dnf\n'
                              'skip_if_unavailable=False\ngpgcheck=1\nsslverify=1\n'
                              'install_weak_deps=False\nlogdir='+temp+'\npersistdir='+temp+'\n')
            command = ['/usr/bin/dnf', '--config='+str(config), '--noplugins', '--cacheonly', '--assumeno',
                       '--disablerepo=*'] + ['--enablerepo='+x for x in selected] + [
                       '--setopt=install_weak_deps=False', '--setopt=*.skip_if_unavailable=False',
                       '--setopt=logdir='+temp,
                       '--setopt=persistdir='+temp, '--setopt=log_size=1048576',
                       '--setopt=log_rotate=0', '--setopt=timeout=15', '--setopt=retries=0',
                       'install', *REQUESTED]
            state, code, raw = bounded_run(command)
            result['processStatus'] = state
            result['exitCode'] = code
            if state != 'exited':
                return result
            aborted = 0
            failed = False
            in_table = False
            table_finished = False
            malformed_table = False
            pending = ''
            seen = set()
            for line in raw.decode('utf-8', errors='replace').splitlines():
                line = line.strip()
                if line == 'Operation aborted.':
                    aborted += 1
                if re.search(r'(?i)(error:|failed|no match for argument|cannot |could not |unable to|problem:|ignoring repositories|skip.*repositor)', line):
                    failed = True
                if line in ('Installing:', 'Installing dependencies:'):
                    if pending:
                        malformed_table = True
                    in_table = True
                    continue
                if line == 'Transaction Summary':
                    if pending or not in_table:
                        malformed_table = True
                    in_table = False
                    table_finished = True
                    continue
                if in_table:
                    if not line or re.fullmatch(r'=+', line):
                        continue
                    pending = (pending + ' ' + line).strip()
                    parts = pending.split()
                    if len(parts) < 6 and len(pending) < 500:
                        continue
                    if (len(parts) == 6 and re.fullmatch(r'[A-Za-z0-9_.+-]{1,100}', parts[0])
                            and parts[1] in ('x86_64', 'noarch')
                            and re.fullmatch(r'[A-Za-z0-9:_.+~^-]{1,100}', parts[2])
                            and parts[3] in selected and re.fullmatch(r'[0-9.]+', parts[4])
                            and parts[5] in ('k', 'M', 'G', 'T')):
                        key = tuple(parts[:4])
                        if key in seen or len(seen) >= 256:
                            malformed_table = True
                        else:
                            seen.add(key)
                            result['packages'].append(dict(zip(('name', 'arch', 'version', 'repository'), parts[:4])))
                    else:
                        malformed_table = True
                    pending = ''
                if re.fullmatch(r'(Total download size|Installed size): [0-9.]+ [kMGT]?', line):
                    result['messages'].append(line)
            complete = set(REQUESTED).issubset({x['name'] for x in result['packages']})
            result.update(automaticRefusalCount=aborted, errorMarkerObserved=failed,
                          requestedPackagesComplete=complete, transactionTableComplete=table_finished,
                          unparsedTransactionRows=malformed_table or bool(pending) or in_table)
            if (code == 1 and aborted == 1 and not failed and complete and table_finished
                    and not result['unparsedTransactionRows']):
                result['status'] = 'complete_cached_plan'
            else:
                result['reason'] = 'incomplete_or_unrecognized_cached_transaction'
    except (OSError, ValueError, KeyError, configparser.Error, subprocess.SubprocessError):
        result['reason'] = 'bounded_cache_query_unavailable'
    finally:
        try:
            space = os.statvfs('/var/cache/dnf')
            result['diskAvailableAfter'] = space.f_bavail * space.f_frsize
        except OSError:
            pass
        result['elapsedSeconds'] = round(time.monotonic()-started, 3)
        result['limits'] = [
            'No plugins; fixed minimal environment; cache-only mode forbids metadata network refresh.',
            'Only allowlisted local cache repositories; no installation confirmation or service command.',
            'Private temporary DNF logs/state are deleted; raw output never exported.',
            'Complete cached plan is not package signature verification, installation, or readiness.']
    return result


if __name__ == '__main__':
    observation = main()
    print(json.dumps(observation, sort_keys=True))
    sys.exit(0 if observation['status'] == 'complete_cached_plan' else 1)
