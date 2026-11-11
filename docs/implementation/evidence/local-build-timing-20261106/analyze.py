import pathlib,json,datetime,collections,xml.etree.ElementTree as ET
D=pathlib.Path(__file__).resolve().parent;log=(D/'api-gradle.log').read_text(errors='replace');tasks=[];phases=[];execution=None
for line in log.splitlines():
 for prefix,output in [('CYF_TASK_TIMING ',tasks),('CYF_GRADLE_PHASE ',phases)]:
  if line.startswith(prefix):
   try:output.append(json.loads(line[len(prefix):]))
   except ValueError:pass
 if line.startswith('GRADLE_EXECUTION_TIMING '):execution=json.loads(line.split(' ',1)[1])
roots=[t for t in tasks if t['rootBuild']];nested=[t for t in tasks if not t['rootBuild']];cat=collections.defaultdict(float)
for t in roots:
 n=t['task'].split(':')[-1]
 if n.startswith('compile') and n.endswith(('Java','Groovy','Kotlin')):kind='compile'
 elif n in ['test','jytUxB02','publicArtifactVerifierTest','poiProductionRuntimeClasspathTest'] or n.startswith(('mmd','skillManagement')):kind='test'
 elif n=='bootJar':kind='finalBootJar'
 elif n=='validateLayering':kind='layering'
 elif n.endswith('jar') or n.endswith('Jar'):kind='libraryJar'
 elif 'Resources' in n:kind='resources'
 else:kind='other'
 cat[kind]+=t['seconds']
counts=dict(suites=0,tests=0,failures=0,errors=0,skipped=0);failures=[];junitSeconds=0.0
source=D/'api-junit'
if not source.exists() or not any(source.rglob('TEST-*.xml')):source=pathlib.Path('/var/tmp/cyf-local-build-timing-20261106/api-build')
for p in source.rglob('TEST-*.xml'):
 try:s=ET.parse(str(p)).getroot()
 except ET.ParseError:continue
 if s.tag!='testsuite':continue
 counts['suites']+=1;junitSeconds+=float(s.get('time','0'))
 for k in ['tests','failures','errors','skipped']:counts[k]+=int(s.get(k,'0'))
 for t in s.findall('testcase'):
  for f in list(t.findall('failure'))+list(t.findall('error')):failures.append({'suite':s.get('name'),'class':t.get('classname'),'test':t.get('name'),'message':f.get('message','')[:400]})
counts['passed']=counts['tests']-counts['failures']-counts['errors']-counts['skipped']
rootPhases=[p for p in phases if p['rootBuild']];graph=next((p['elapsedSeconds'] for p in rootPhases if p['phase']=='taskGraphReady'),None)
r={'snapshotAt':datetime.datetime.now().isoformat(),'gradleExecution':execution,'rootPhases':rootPhases,'nestedPhases':[p for p in phases if not p['rootBuild']],'categoryTaskSeconds':dict(cat),'rootTaskCount':len(roots),'nestedTaskCount':len(nested),'compileCacheHitCount':sum(t.get('skipMessage')=='FROM-CACHE' for t in tasks),'slowestRootTasks':sorted(roots,key=lambda t:t['seconds'],reverse=True)[:25],'slowestNestedTasks':sorted(nested,key=lambda t:t['seconds'],reverse=True)[:8],'junitRecords':counts,'junitSuiteRecordedSeconds':junitSeconds,'failures':failures,'notes':'Nested plugin tasks occur inside root configuration and are NOT added again to root totals. XML counts are execution records, not deduplicated cases. Test task time includes fork/startup/reporting; compile task time may include dependency resolution.'}
if execution and graph is not None:r['startupShutdownDispatchAndOtherResidualSeconds']=execution['elapsed_seconds']-graph-sum(cat.values())
(D/'api-analysis.json').write_text(json.dumps(r,ensure_ascii=False,indent=2));print(json.dumps({k:r[k] for k in ['gradleExecution','categoryTaskSeconds','rootTaskCount','compileCacheHitCount','junitRecords']},ensure_ascii=False,indent=2))
