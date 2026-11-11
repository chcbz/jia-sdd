import os,json,gzip,hashlib,re,uuid,time,stat
from pathlib import Path
ROOT=Path('/home/isp/apps/codex-ws-agent/data/inbox/6a79742d6a69616665776e6e763538656332333739632d7775796f6e67')
HW=ROOT/'ack-sequence-high-water'; CONFIG=Path('/home/isp/apps/codex-ws-agent/codex-profiles.conf')
AGENT='jyt-jiafewnnv58ec2379c-wuyong'
BACKUP=Path('/home/isp/baks/ack-high-water')/('retired-wuyong-'+time.strftime('%Y%m%dT%H%M%S')+'-'+uuid.uuid4().hex[:8]+'.jsonl.gz')
EVIDENCE=Path('/home/isp/wsps/cyf/docs/implementation/evidence/AGENT-ACK-CHECKPOINT-20261008/reclaim-20261009/result.json')
def syncdir(p):
 fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY)
 try:os.fsync(fd)
 finally:os.close(fd)
def sha(b):return hashlib.sha256(b).hexdigest()
def guard():
 assert CONFIG.read_bytes()==config_bytes,'shared profile config changed'
 # Old profile must remain absent, not merely disabled.
 assert AGENT not in config_bytes.decode(),'old Agent identity still configured'
 assert ROOT.resolve()==ROOT and HW.resolve()==HW,'unexpected symlink'
 assert (ROOT/'ack-sequence.json').read_bytes()==counter_bytes,'counter changed'
config_bytes=CONFIG.read_bytes();counter_bytes=(ROOT/'ack-sequence.json').read_bytes();guard()
lock=ROOT/'ack-sequence.lock';token=uuid.uuid4().hex
os.mkdir(lock,0o700);syncdir(ROOT)
owner={'formatVersion':1,'pid':os.getpid(),'runtimeInstanceId':token,'operation':'authorized-retired-high-water-backup-prune','acquiredAt':int(time.time()*1000)}
with open(lock/'owner.json','x') as f:json.dump(owner,f);f.flush();os.fsync(f.fileno())
syncdir(lock)
try:
 guard()
 seq=json.loads(counter_bytes);init=json.loads((HW/'initialized.json').read_bytes())
 assert seq['formatVersion']==1 and init['formatVersion']==1 and init['agentId']==AGENT
 names=sorted(os.listdir(HW));markers=[n for n in names if re.fullmatch(r'\d{20}\.json',n)]
 assert set(names)==set(markers)|{'initialized.json'},'unexpected evidence or intent'
 assert markers,'no old markers'
 maximum=max(int(n[:-5]) for n in markers); fence=seq['lastSequence']
 keep={'initialized.json'}|{n for n in markers if int(n[:-5])>=fence}|{f'{maximum:020}.json'}
 before=sum(os.stat(HW/n,follow_symlinks=False).st_blocks*512 for n in names)+os.stat(HW).st_blocks*512
 BACKUP.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
 records={};digest=hashlib.sha256()
 header={'kind':'header','formatVersion':1,'purpose':'retired-high-water-prune-not-migration','agentId':AGENT,'root':str(ROOT),'counterContents':counter_bytes.decode(),'maximum':maximum,'retain':sorted(keep)}
 with open(BACKUP,'xb') as raw:
  os.chmod(BACKUP,0o600)
  with gzip.GzipFile(fileobj=raw,mode='wb') as gz:
   line=(json.dumps(header,separators=(',',':'))+'\n').encode();gz.write(line);digest.update(line)
   for n in names:
    p=HW/n;s=p.lstat();assert stat.S_ISREG(s.st_mode),'nonregular evidence'
    data=p.read_bytes();o=json.loads(data)
    if n!='initialized.json':assert o['formatVersion']==1 and o['agentId']==AGENT and o['queueSequence']==int(n[:-5]),'invalid marker'
    records[n]=sha(data)
    row={'kind':'file','name':n,'contents':data.decode(),'sha256':records[n],'mode':stat.S_IMODE(s.st_mode)}
    line=(json.dumps(row,separators=(',',':'))+'\n').encode();gz.write(line);digest.update(line)
   footer={'kind':'footer','count':len(names),'digest':digest.hexdigest()};gz.write((json.dumps(footer)+'\n').encode())
  raw.flush();os.fsync(raw.fileno())
 syncdir(BACKUP.parent)
 print('Backup durable',str(BACKUP),BACKUP.stat().st_size,flush=True)
 check=hashlib.sha256();seen=set();verified=False
 with gzip.open(BACKUP,'rb') as f:
  for line in f:
   row=json.loads(line)
   if row['kind']=='footer':
    assert row['count']==len(seen) and row['digest']==check.hexdigest();verified=True
    assert not f.read(1),'trailing data';break
   check.update(line)
   if row['kind']=='file':
    n=row['name'];assert n in records and n not in seen;seen.add(n)
    assert sha(row['contents'].encode())==row['sha256']==records[n]
    assert sha((HW/n).read_bytes())==records[n],'source changed'
 assert verified and seen==set(names),'backup incomplete'
 guard();assert sorted(os.listdir(HW))==names,'directory changed'
 print('Backup verified; pruning',len(names)-len(keep),'historical files; retained',sorted(keep),flush=True)
 removed=0
 for n in names:
  if n in keep:continue
  guard() if removed%10000==0 else None
  assert sha((HW/n).read_bytes())==records[n],'source changed before deletion'
  (HW/n).unlink();removed+=1
 syncdir(HW);guard()
 assert set(os.listdir(HW))==keep
 for n in keep:assert sha((HW/n).read_bytes())==records[n]
 after=sum(os.stat(HW/n).st_blocks*512 for n in keep)+os.stat(HW).st_blocks*512
 result={'timestamp':time.strftime('%Y-%m-%dT%H:%M:%S%z'),'status':'reclaimed','operation':'backup-verified-retired-legacy-prune-not-format-migration','root':str(ROOT),'backup':str(BACKUP),'backupBytes':BACKUP.stat().st_size,'backupSha256':sha(BACKUP.read_bytes()),'sourceFileCount':len(names),'removedFileCount':removed,'retainedFiles':sorted(keep),'counterSequenceUnchanged':fence,'highWaterMaximumUnchanged':maximum,'preexistingConflictPreserved':maximum!=fence,'allocatedBeforeBytes':before,'allocatedAfterBytes':after,'netReclaimedBytes':before-after-BACKUP.stat().st_blocks*512,'pendingAckModified':False,'servicesRestarted':False}
 with open(EVIDENCE,'x') as f:json.dump(result,f,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
 print(json.dumps(result,indent=2),flush=True)
finally:
 actual=json.loads((lock/'owner.json').read_bytes());assert actual['pid']==os.getpid() and actual['runtimeInstanceId']==token
 (lock/'owner.json').unlink();syncdir(lock);lock.rmdir();syncdir(ROOT)
