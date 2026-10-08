import pathlib,subprocess,json,hashlib,datetime,sys
root=pathlib.Path(r'C:\Users\Think\.codex\worktrees\archive-agent-maintenance\cyf-web-kit')
relative='specs/archive-agent-maintenance/evidence/merge-develop/20261008'
output='staged-evidence-byte-proof-final-validation.json'
def g(*a,**kw):return subprocess.check_output(['git','-c','core.longpaths=true','-C',str(root),*a],**kw)
paths=[x for x in g('diff','--cached','--name-only','-z','--diff-filter=ACM','--',relative).decode().split('\0') if x and not x.endswith('/'+output)]
raw=g('cat-file','--batch',input=(''.join(':'+p+'\n' for p in paths)).encode());offset=0;proof=[]
for p in paths:
 end=raw.index(b'\n',offset);header=raw[offset:end].decode().split();assert len(header)==3 and header[1]=='blob',header
 size=int(header[2]);offset=end+1;blob=raw[offset:offset+size];offset+=size+1;disk=(root/p).read_bytes();assert blob==disk,p
 proof.append({'file':p,'bytes':size,'blob':header[0],'sha256':hashlib.sha256(blob).hexdigest(),'disk_index_equal':True})
assert offset==len(raw)
r={'at':datetime.datetime.now().astimezone().isoformat(),'scope':'Only newly staged or modified merge evidence; excludes this proof itself to avoid self-binding. Previous proof files remain historical.','files':proof,'count':len(proof),'all_preserved':True}
(root/relative/output).write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8')
print('RAW_EVIDENCE_BYTE_PROOF',len(proof))