import pathlib,glob,xml.etree.ElementTree as E,collections,datetime
b=pathlib.Path('/tmp/cyf-aam-merge-develop-20261008');start=datetime.datetime.strptime((b/'evidence/attempt4/api-started-utc.txt').read_text().strip(),'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=datetime.timezone.utc).timestamp()
for suite in ['archiveMaintenanceMvp','archiveRegression']:
 p=b/'root/api/chat/jia-chat-service/build/test-results'/suite;counts=collections.Counter();tests=fail=0;files=0
 for f in p.glob('TEST-*.xml'):
  if f.stat().st_mtime<start:continue
  x=E.parse(str(f)).getroot();files+=1;tests+=int(x.get('tests',0));fail+=int(x.get('failures',0))
  for t in x.iter('testcase'):
   e=t.find('failure')
   if e is not None:counts[e.get('message','')[:550]]+=1
 print(suite,'freshFiles',files,'tests',tests,'fail',fail,'categories',dict(counts))