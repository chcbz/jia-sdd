import os,json,hashlib,time,subprocess
from pathlib import Path
E=Path('/home/isp/wsps/cyf/docs/implementation/evidence/AGENT-ACK-CHECKPOINT-20261008/reclaim-20261009')
root=Path('/home/isp/apps/codex-ws-agent/data/inbox/6a79742d6a69616665776e6e763538656332333739632d7775796f6e67');hw=root/'ack-sequence-high-water'
before=json.loads((E/'before.json').read_text());files={}
for d,dirs,names in os.walk(root):
 dirs[:]=[x for x in dirs if x!='ack-sequence-high-water']
 for n in names:
  p=Path(d)/n
  if p==root/'ack-sequence.json':continue
  files[str(p.relative_to(root))]=hashlib.sha256(p.read_bytes()).hexdigest()
assert files==before['unaffectedFiles'],'non-high-water files changed'
assert set(os.listdir(hw))=={'initialized.json','checkpoint.json'}
init=json.loads((hw/'initialized.json').read_bytes());state=json.loads((root/'ack-sequence.json').read_bytes());checkpoint=json.loads((hw/'checkpoint.json').read_bytes())
assert state==checkpoint and state['lastSequence']==292658 and init['formatVersion']==2
assert init['storageId']==state['storageId'] and init['agentId']==state['agentId']
assert not (root/'ack-sequence.lock').exists()
backup=Path((E/'backup-path.txt').read_text().strip());after=sum(p.stat().st_blocks*512 for p in hw.iterdir())+hw.stat().st_blocks*512
services={}
for service,pid in [('codex-ws-agent.service',2237),('codex-ws-agent@wuyong-local.service',324415)]:
 s=dict(l.split('=',1) for l in subprocess.check_output(['systemctl','show',service,'-p','MainPID','-p','ActiveState'],universal_newlines=True).splitlines())
 assert s['ActiveState']=='active' and int(s['MainPID'])==pid
 services[service]=s
result={'timestamp':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'status':'migration-and-reclaim-verified','toolSourceCommit':'5b71067f7bcbc7ca7f1076f5a9e10321b400785a','targetRoot':str(root),'retiredProfileNotConfiguredOnSharedAgent':True,'lastSequence':state['lastSequence'],'highWaterFiles':2,'unaffectedFilesVerified':len(files),'services':services,'backup':str(backup),'backupBytes':backup.stat().st_size,'backupSha256':hashlib.sha256(backup.read_bytes()).hexdigest(),'allocatedBeforeBytes':before['highWaterAllocatedBytes'],'allocatedAfterBytes':after,'netReclaimedBytes':before['highWaterAllocatedBytes']-after-backup.stat().st_blocks*512,'runtimeDeploymentPerformed':False,'serviceRestartPerformed':False}
(E/'result.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
