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
import tempfile
import time

REQUESTED = ('clamav', 'clamd', 'clamav-update')
# Only these distro/EPEL cache IDs may participate. No network metadata refresh.
REPO_IDS = ('alinux3-os', 'alinux3-updates', 'alinux3-plus', 'alinux3-powertools', 'epel')
ENVIRONMENT = {'PATH': '/usr/sbin:/usr/bin:/sbin:/bin', 'HOME': '/root', 'LC_ALL': 'C', 'LANG': 'C'}
LIMIT = 2 * 1024 * 1024


def repo_ids():
    ids = set()
    files = sorted(glob.glob('/etc/yum.repos.d/*.repo'))
    if len(files) > 40:
        raise ValueError('repository_file_limit')
    for name in files:
        fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW)
        with os.fdopen(fd, 'rb') as f:
            if not stat.S_ISREG(os.fstat(f.fileno()).st_mode):
                raise ValueError('repository_not_regular')
            data = f.read(65537)
        if len(data) > 65536:
            raise ValueError('repository_size_limit')
        parser = configparser.ConfigParser(interpolation=None, strict=True)
        parser.read_string(data.decode('utf-8'))
        ids.update(x for x in parser.sections() if re.fullmatch(r'[A-Za-z0-9_.-]{1,100}', x))
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
        inventory = repo_ids()
        result['repositoryIds'] = inventory
        selected = [x for x in REPO_IDS if x in inventory]
        result['enabledCacheRepositoryIds'] = selected
        if not selected:
            result['reason'] = 'no_allowlisted_repository_cache'
            return result
        with tempfile.TemporaryDirectory(prefix='cyf-output-dnf-plan-') as temp:
            command = ['/usr/bin/dnf', '--noplugins', '--cacheonly', '--assumeno',
                       '--disablerepo=*'] + ['--enablerepo='+x for x in selected] + [
                       '--setopt=install_weak_deps=False', '--setopt=logdir='+temp,
                       '--setopt=persistdir='+temp, '--setopt=log_size=1048576',
                       '--setopt=log_rotate=0', '--setopt=timeout=15', '--setopt=retries=0',
                       'install', *REQUESTED]
            state, code, raw = bounded_run(command)
            result['processStatus'] = state
            result['exitCode'] = code
            if state != 'exited':
                return result
            aborted = False
            failed = False
            for line in raw.decode('utf-8', errors='replace').splitlines():
                line = line.strip()
                parts = line.split()
                if (len(parts) >= 4 and re.fullmatch(r'[A-Za-z0-9_.+-]{1,100}', parts[0])
                        and parts[1] in ('x86_64', 'noarch')
                        and re.fullmatch(r'[A-Za-z0-9:_.+~^-]{1,100}', parts[2])
                        and parts[3] in selected):
                    result['packages'].append(dict(zip(('name', 'arch', 'version', 'repository'), parts[:4])))
                if line == 'Operation aborted.':
                    aborted = True
                if re.search(r'(?i)(error:|failed|no match for argument|cannot |could not |unable to)', line):
                    failed = True
                if re.fullmatch(r'(Total download size|Installed size): [0-9.]+ [kMGT]?', line):
                    result['messages'].append(line)
            complete = set(REQUESTED).issubset({x['name'] for x in result['packages']})
            result.update(automaticRefusalObserved=aborted, errorMarkerObserved=failed,
                          requestedPackagesComplete=complete)
            if code == 1 and aborted and not failed and complete:
                result['status'] = 'complete_cached_plan'
            else:
                result['reason'] = 'incomplete_or_unrecognized_cached_transaction'
    except (OSError, ValueError, configparser.Error, subprocess.SubprocessError):
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
    print(json.dumps(main(), sort_keys=True))
