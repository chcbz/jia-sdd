#!/usr/bin/env python3
"""Resolve a scanner install transaction without installing; suppress raw repository output."""
import json
import os
import re
import subprocess
import time


def main():
    command=['/usr/bin/dnf','--assumeno','--setopt=install_weak_deps=False',
             '--setopt=timeout=15','--setopt=retries=0','install','clamav','clamd','clamav-update']
    environment=dict(os.environ, LC_ALL='C', LANG='C')
    started=int(time.time())
    result={'observedAtEpoch':started,'packageInstallRequested':False,
            'metadataCacheMayChange':True,'command':command,'packages':[],'messages':[]}
    try:
        completed=subprocess.run(command,env=environment,stdin=subprocess.DEVNULL,
                                 stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120,check=False)
        result['exitCode']=completed.returncode
        raw=completed.stdout
        if len(raw)>2*1024*1024:
            result['status']='output_limit_exceeded'
        else:
            for line in raw.decode('utf-8',errors='replace').splitlines():
                parts=line.strip().split()
                if (len(parts)>=4 and re.fullmatch(r'[A-Za-z0-9_.+-]{1,100}',parts[0])
                        and parts[1] in ('x86_64','noarch')
                        and re.fullmatch(r'[A-Za-z0-9:_.+~^-]{1,100}',parts[2])
                        and re.fullmatch(r'[A-Za-z0-9_.:-]{1,100}',parts[3])):
                    result['packages'].append({'name':parts[0],'arch':parts[1],'version':parts[2],'repository':parts[3]})
                for package in ('clamav','clamd','clamav-update'):
                    if line.strip()=='No match for argument: '+package:
                        result['messages'].append('No match for argument: '+package)
                if re.fullmatch(r'(Total download size|Installed size): [0-9.]+ [kMGT]?',line.strip()):
                    result['messages'].append(line.strip())
                if line.strip() in ('Operation aborted.','Nothing to do.','Complete!'):
                    result['messages'].append(line.strip())
            result['status']='plan_observed' if result['packages'] else 'no_package_plan'
    except subprocess.TimeoutExpired:
        result['status']='query_timed_out'
    except OSError:
        result['status']='dnf_unavailable'
    result['elapsedSeconds']=int(time.time())-started
    result['limits']=['DNF --assumeno cannot confirm an installation and no service command is invoked.',
                      'Repository metadata/cache may be downloaded or refreshed by DNF; raw output is never exported.',
                      'Package signatures and dependency compatibility are not proven by this plan alone.']
    print(json.dumps(result,sort_keys=True))


if __name__=='__main__':main()
