import json,pathlib,xml.etree.ElementTree as E
b=pathlib.Path('/tmp/cyf-aam-merge-develop-20261008');d=json.loads((b/'evidence/attempt2/api-result.json').read_text());suite=next(x for x in d['suites'] if x['task']=='archiveRegression')
for f in sorted((b/'evidence/attempt2/archiveRegression').glob('TEST-*.xml')):
 r=E.parse(f).getroot()
 for t in r.findall('testcase'):
  fail=t.find('failure')
  if fail is None:continue
  cls=t.get('classname')
  if cls.endswith(('ArchiveMaintenanceConcurrencyMySqlTest','ArchiveBusinessOutboxMySqlTest','ArchiveQuestionWorkerTest','ArchiveRootProfileWiringTest')):continue
  print(cls+'#'+t.get('name'));print(fail.get('message'))
print('source unchanged',d['source_unchanged'],'fresh',d['all_requested_suites_have_fresh_xml'])
