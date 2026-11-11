from pathlib import Path
import os,subprocess,json
R=Path('/home/isp/wsps/cyf'); E=R/'docs/implementation/evidence/local-release-closure-20261107'; index=E/'scoped.index';env=dict(os.environ,GIT_INDEX_FILE=str(index))
def git(*args,**kw):return subprocess.check_output(['git',*args],cwd=R,env=env,**kw)
base=git('rev-parse','HEAD',text=True).strip();git('read-tree',base)
files=['ops/orchestration/'+n for n in ['local_build.py','local_release.py','local_web_build.py','local-build.init.gradle','local-web-build.mjs','tests/test_local_build.py','tests/test_local_release_runner.py']]
files+=['ops/ci/aliyun-flow/'+n for n in ['auto/package-api-local.py','tests/test_api_local_package.py','tests/test_native_local_api.py','tests/test_web_native_local.py']]
files+=['ops/maintenance/'+n for n in ['flow_host_cleanup.py','rebuildable_cache_cleanup.py','clear_disk.host.sh','host_cleanup_log.py','host_cleanup_processes.py','runtime_backup_cleanup.py','LOCAL_ARTIFACT_RETENTION.md','RUNTIME_BACKUP_RETENTION.md','tests/test_flow_host_cleanup.py','tests/test_rebuildable_cache_cleanup.py','tests/test_runtime_backup_cleanup.py','tests/test_clear_disk.sh']]
files+=['docs/implementation/handoffs/'+n for n in ['LOCAL-BUILD-TIMING-20261106.md','LOCAL-BUILD-RETENTION-10M-20261106.md']]
git('add','--',*files)
for n in ['cyf-api-flow-deploy','cyf-api-flow-install','cyf-web-flow-deploy']:
 blob=git('hash-object','-w','--stdin',input=(E/'candidate-helpers'/n).read_bytes()).decode().strip()
 git('update-index','--add','--cacheinfo','100755',blob,'ops/ci/aliyun-flow/host/'+n)
def put(path,text):
 blob=git('hash-object','-w','--stdin',input=text.encode()).decode().strip();git('update-index','--add','--cacheinfo','100644',blob,path)
for name in ['docs/aliyun-flow-cicd-strategy.md','docs/DEPLOYMENT.md','ops/orchestration/README.md']:
 current=(R/name).read_text();old=git('show',base+':'+name).decode();header=current.split('\n',1)[0]+'\n\n'
 if name.endswith('aliyun-flow-cicd-strategy.md'):
  start=current.index('## 本地快速构建发布长期策略');end=current.index('## 2026-11-06 本地完整发布耗时',start);new=header+current[start:end]+'> 以下为历史策略，冲突时以上方2026-11-07规则为准。\n\n'+old
 elif name.endswith('DEPLOYMENT.md'):
  start=current.index('## 当前默认快速发布入口');end=current.index('> **2026-09-30',start);new=header+current[start:end]+'> 以下为历史部署说明，冲突时以上方现行策略为准。\n\n'+old
 else:
  start=current.index('## 本地快速构建与受控发布');new=header+'> 下方旧Flow-only说明保留作历史；当前入口见本文末节。\n\n'+old+'\n'+current[start:]
 put(name,new)
result={'base':base,'index':str(index),'stagedFiles':git('diff','--cached','--name-only',text=True).splitlines()};(E/'scoped-stage.json').write_text(json.dumps(result,indent=2)+'\n');print(git('diff','--cached','--stat',text=True));print('BASE',base)
