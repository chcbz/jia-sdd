import re,json,pathlib
w=pathlib.Path('/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/api-v3-wire-jackson3-source-owner-20261001'); src=(w/'chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatTypedDeliberationSchemaInitializer.java').read_text();exp=dict(re.findall(r'Map.entry\("(chk_[^"]+)","([^"]+)"\)',src))
rows=json.load(open('/var/tmp/cyf-mmd-api-da047-catalog-diagnostic-20261001/actual-check-catalog.json'))['raw_rows'];act={r.split('\t')[0]:r.split('\t',2)[2] for r in rows}
def canonical(s):
 s=s.replace("\\'", "'");s=re.sub(r"(?i)_utf8mb4(?=\s*')",'',s);out='';q=False
 for c in s:
  if c=="'":q=not q;out+=c
  elif q:out+=c
  elif not c.isspace() and c!='`':out+=c.lower()
 return out

def covers(s):
 d=0;q=False
 for i,c in enumerate(s):
  if c=="'":q=not q
  elif not q and c=='(':d+=1
  elif not q and c==')':
   d-=1
   if (d==0 and i<len(s)-1) or d<0:return False
 return d==0 and not q

def boolean(s,a,b):
 d=0;q=False
 for i in range(a,b):
  c=s[i]
  if c=="'":q=not q;continue
  if q:continue
  if c=='(':d+=1
  elif c==')':d-=1
  elif d==0 and (s.startswith('and',i) or s.startswith('or',i)):return True
 return False

def norm(s):
 s=canonical(s)
 while len(s)>=2 and s[0]=='(' and s[-1]==')' and covers(s):s=s[1:-1]
 while True:
  stack=[];i=0;changed=False
  while i<len(s):
   c=s[i]
   if c=="'":
    while i+1<len(s) and s[i+1]!="'":i+=1
    # Mirrors Java loop's actual quote traversal, including its retained closing quote behaviour.
   elif c=='(':stack.append(i)
   elif c==')' and stack:
    o=stack.pop();group=o==0 or not(s[o-1].isalnum() or s[o-1]=='_')
    if group and not boolean(s,o+1,i):s=s[:o]+s[o+1:i]+s[i+1:];changed=True;break
   i+=1
  if not changed:return s
out=[]
for k in sorted(exp):
 e=norm(exp[k]);a=norm(act[k]);out.append({'name':k,'equal':e==a,'expected':exp[k],'actual':act[k],'normalized_expected':e,'normalized_actual':a})
p=pathlib.Path('/var/tmp/cyf-mmd-main-controlled-bridge-progress/api-da047-check-rendering-diagnostic.json');p.write_text(json.dumps({'kind':'Static Python transcription diagnostic, not Java/runtime proof','comparisons':out},indent=2)+'\n')
for r in out:
 if not r['equal']:print(r['name'],'\n expected:',r['normalized_expected'],'\n actual:  ',r['normalized_actual'])
