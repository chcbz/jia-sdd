from pathlib import Path
import os,subprocess,tempfile,json
R=Path('/home/isp/wsps/cyf');E=R/'docs/implementation/evidence/local-release-closure-20261107';base='cc1b56ad109d30f6b94d07e21759dba5bfd5baeb';branch='refs/heads/codex/local-release-strategy-20261107'
fd,index=tempfile.mkstemp(prefix='cyf-layout-index-');os.close(fd);os.unlink(index);env=dict(os.environ,GIT_INDEX_FILE=index)
def git(*args,input=None):return subprocess.check_output(['git',*args],cwd=str(R),env=env,input=input)
def put(p,data):
 blob=git('hash-object','-w','--stdin',input=data).decode().strip();git('update-index','--add','--cacheinfo','100644',blob,p)
try:
 git('read-tree',base)
 for p in ['ops/maintenance/rebuildable_cache_cleanup.py','ops/maintenance/tests/test_rebuildable_cache_cleanup.py','ops/maintenance/HOST_DIRECTORY_LAYOUT.md']:
  put(p,(R/p).read_bytes())
 for p,marker in [('docs/aliyun-flow-cicd-strategy.md','\n### 主机目录职责归位（2026-11-07后续更新）'),('ops/orchestration/README.md','\n主机目录职责：构建任务及缓存归state'),('ops/maintenance/LOCAL_ARTIFACT_RETENTION.md','\n## 2026-11-07目录归位更新')]:
  s=git('show',base+':'+p).decode();w=(R/p).read_text();assert w.count(marker)==1
  if 'cicd-strategy' in p:
   a=s.index('### 已验证范围及持久化/清理状态');b=s.index('\n操作参数见',a);s=s[:a]+s[a:b].replace('/home/isp/wsps/private-maintenance/','/home/isp/pkgs/cyf/')+s[b:]
  if p=='ops/orchestration/README.md':s=s.replace('/home/isp/wsps/private-maintenance/cyf-NEW_BATCH','/home/isp/state/cyf-local-build/tasks/cyf-NEW_BATCH')
  s+=w[w.index(marker):];put(p,s.encode())
 for name in ['directory-layout-migration.json','directory-layout-docs.json','directory-layout-verification.json','directory-layout-plan.json','directory-layout-rebuildable-tests.log','directory-layout-runtime-tests.log','directory-layout-flow-tests.log','directory-layout-shell-tests.log']:
  p=str((E/name).relative_to(R));put(p,(R/p).read_bytes())
 print(subprocess.run(['git','diff','--cached','--check',base],cwd=str(R),env=env,stdout=subprocess.PIPE).stdout.decode()); git('diff','--cached','--check',base)
 print(git('diff','--cached','--stat',base).decode())
 print(git('diff','--cached',base,'--','ops/maintenance/rebuildable_cache_cleanup.py','ops/maintenance/tests/test_rebuildable_cache_cleanup.py','ops/orchestration/README.md').decode())
 tree=git('write-tree').decode().strip();commit=git('commit-tree',tree,'-p',base,input=b'ops: align local release archives and worktree policy with host layout\n').decode().strip()
 git('update-ref',branch,commit,base)
 (E/'directory-layout-version-control.json').write_text(json.dumps({'branch':branch,'parent':base,'commit':commit,'pushVerified':False},indent=2)+'\n')
 print('COMMIT='+commit)
finally:
 if os.path.exists(index):os.unlink(index)
