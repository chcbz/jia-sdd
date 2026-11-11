"""Verify only observed derived CPython caches against exact baseline source bytes.
No source/program writes; executed with the baseline's exact Python -I -B.
"""
from pathlib import Path
import json,marshal,importlib.util,re,sys,hashlib,stat
root=Path(sys.argv[1]);expected={x['path']:x for x in json.loads(Path(sys.argv[2]).read_text())};diff=json.loads(Path(sys.argv[3]).read_text());verified=[]
for item in diff:
 n=item['path'];e=item['expected'];a=item['actual'];p=root/n
 assert n.startswith('codex-bridge/.toolchain/') and a is not None,'NON_DERIVED_DRIFT'
 assert a['uid']==0 and a['gid']==0 and not int(a['mode'],8)&0o022,'UNSAFE_CACHE'
 if a['type']=='directory':
  assert e is None and p.name=='__pycache__','NON_CACHE_DIRECTORY';continue
 assert a['type']=='file' and p.parent.name=='__pycache__','NON_CACHE_FILE'
 if e is not None:assert {k:v for k,v in e.items() if k!='sha256'}=={k:v for k,v in a.items() if k!='sha256'},'CACHE_METADATA_CHANGED'
 m=re.fullmatch(r'(.+)\.cpython-311(?:\.opt-([12]))?\.pyc',p.name);assert m,'UNKNOWN_CACHE_FORMAT'
 src=p.parent.parent/(m[1]+'.py');sn=str(src.relative_to(root));se=expected.get(sn);assert se and se['type']=='file','UNVERIFIED_CACHE_SOURCE'
 raw=p.read_bytes();sb=src.read_bytes();assert hashlib.sha256(sb).hexdigest()==se['sha256'],'SOURCE_CHANGED'
 assert hashlib.sha256(raw).hexdigest()==a['sha256'] and raw[:4]==importlib.util.MAGIC_NUMBER,'CACHE_CHANGED'
 code=marshal.loads(raw[16:]);assert code==compile(sb,code.co_filename,'exec',dont_inherit=True,optimize=int(m[2] or 0)),'CACHE_NOT_DERIVED'
 verified.append({'path':n,'source':sn,'sha256':a['sha256'],'sourceSha256':se['sha256']})
print(json.dumps({'status':'PASS','python':sys.version,'verifiedCaches':verified,'changes':len(diff)}))
