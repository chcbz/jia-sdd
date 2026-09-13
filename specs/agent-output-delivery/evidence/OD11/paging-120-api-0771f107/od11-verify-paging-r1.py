import json,hashlib,urllib.parse,requests
from pathlib import Path
expected={}
for manifest in Path('/tmp/od11-paging-workspace-r1/outputs').glob('*/manifest.json'):
 for item in json.loads(manifest.read_text())['items']:
  body=(manifest.parent/item['relativePath']).read_bytes()
  expected[item['outputId']]={'sha256':hashlib.sha256(body).hexdigest(),'size':len(body)}
assert len(expected)==120
s=requests.Session();s.trust_env=False
s.headers['Authorization']='Bearer '+json.loads(Path('/tmp/od06-user-token-r1.json').read_text())['access_token']
base='http://127.0.0.1:10018/chat/conversations/4/outputs'
result={'sourceCommit':'0771f1072d3d79eabde0757f254634427a7e0746','clientCommit':'7c6a273d242d7c61050d76f26bf09cea901992fc','conversationId':'4','expectedCount':120,'pages':[],'downloads':[],'overallPass':False}
items=[];cursor=None;seen=set()
try:
 for page in range(8):
  q={'limit':20}
  if cursor:q['cursor']=cursor
  r=s.get(base,params=q,timeout=30);d=r.json()
  assert r.status_code==200 and d['code']=='E0'
  data=d['data'];batch=data['items'];next_cursor=data.get('nextCursor')
  result['pages'].append({'page':page+1,'status':r.status_code,'count':len(batch),'nextCursorPresent':bool(next_cursor),'bodySha256':hashlib.sha256(r.content).hexdigest()})
  for x in batch:
   assert x['outputId'] not in seen;seen.add(x['outputId'])
   assert str(x['version'])=='1' and x['canDownload'] is True
   assert x['sha256']==expected[x['outputId']]['sha256'] and int(x['size'])==expected[x['outputId']]['size']
  items.extend(batch)
  if not next_cursor:break
  assert next_cursor!=cursor;cursor=next_cursor
 assert len(items)==120 and seen==set(expected)
 for i in [0,19,20,99,100,119]:
  x=items[i];path=base+'/'+x['outputId']+'/versions/1'
  detail=s.get(path,timeout=30);assert detail.status_code==200 and detail.json()['code']=='E0'
  download=s.get(path+'/download',timeout=30);digest=hashlib.sha256(download.content).hexdigest()
  ok=download.status_code==200 and digest==x['sha256'] and len(download.content)==int(x['size'])
  result['downloads'].append({'index':i,'outputId':x['outputId'],'status':download.status_code,'bytes':len(download.content),'sha256':digest,'matchesSnapshot':ok});assert ok
 result['overallPass']=True
except (AssertionError,ValueError,KeyError,requests.RequestException) as e:
 result['errorType']=type(e).__name__
finally:
 result['actualCount']=len(items)
 out=Path('/tmp/od11-paging-r1.observation.json')
 with out.open('x') as f:json.dump(result,f,indent=2);f.write('\n')
 print(json.dumps(result))
