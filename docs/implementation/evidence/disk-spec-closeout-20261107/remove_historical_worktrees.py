"""One-off explicit historical worktree removal; branches and commits retained."""
import sys,json,pathlib,subprocess,os,fcntl,time
sys.path.insert(0,'/usr/local/libexec/cyf')
from host_cleanup_processes import snapshot
base=pathlib.Path(__file__).resolve().parent
inventory=json.loads((base/'worktrees-before.json').read_text())
selected={
'/home/isp/wsps/worktrees/api-startup-60s-20261022',
'/home/isp/wsps/worktrees/cyf-workspace-audit-completion-20261016',
'/home/isp/wsps/worktrees/skill-adoption-api-20261024',
'/root/.codex/worktrees/archive-agent-maintenance-20261020/cyf/api',
'/var/tmp/cyf-external-chat-20261021',
'/var/tmp/cyf-external-contract-tests-20261021',
'/home/isp/wsps/worktrees/skill-management-web-20261023',
'/root/.codex/worktrees/archive-agent-maintenance-20261020/cyf/web',
}
lock=open('/run/lock/cyf-host-cleanup.lock','r+')
fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
results=[]
for d in inventory:
 p=d['worktree']
 if p not in selected:continue
 rec={'path':p,'head':d['HEAD'],'branch':d['branch'],'at':time.time()}
 def git(*a):return subprocess.check_output(['git','-C',p,*a],text=True).strip()
 if git('status','--porcelain') or git('rev-parse','HEAD')!=d['HEAD']:raise RuntimeError('changed worktree '+p)
 if subprocess.check_output(['git','-C',d['repo'],'rev-parse',d['branch']],text=True).strip()!=d['HEAD']:raise RuntimeError('branch changed')
 root=pathlib.Path(p)
 if snapshot().used(root):rec['result']='protected-process';results.append(rec);continue
 if any(root.rglob('.keep')) or os.path.ismount(p):raise RuntimeError('protected path '+p)
 ignored=git('ls-files','--others','--ignored','--exclude-standard').splitlines()
 for item in ignored:
  q=root/item
  if item=='node_modules' and q.is_symlink():continue
  if not (item.startswith('.gradle/') or item.startswith('plugin/.gradle/')):raise RuntimeError('unique ignored content '+str(q))
 rec['ignored_disposable']=ignored
 rec['allocated_bytes']=int(subprocess.check_output(['du','-sx','--block-size=1',p],text=True).split()[0])
 # Retain pre-delete identity; do not remove the branch or force a dirty worktree.
 with (base/'worktree-removal-audit.jsonl').open('a') as f:f.write(json.dumps(rec)+'\n');f.flush();os.fsync(f.fileno())
 subprocess.run(['git','-C',d['repo'],'worktree','remove',p],check=True)
 rec['result']='removed';results.append(rec)
 (base/'worktrees-removed.json').write_text(json.dumps(results,indent=2))
 print(rec['result'],p,flush=True)
