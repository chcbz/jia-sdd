import os,sys,json,pathlib,subprocess,time,datetime,fcntl,hashlib,shutil,importlib.util,traceback
os.umask(0o077)
R=pathlib.Path('/home/isp/wsps/cyf');D=pathlib.Path(__file__).resolve().parent;B=pathlib.Path('/var/tmp/cyf-local-build-timing-20261106');TASK='LOCAL-BUILD-TIMING-20261106'
REQ=json.loads((D/'request.json').read_text());T=time.monotonic();results={'batchStartedAt':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'scope':'local tests/build/package only; production install NOT_MEASURED','components':{}}
def now():return datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
def save():
 results['observedAt']=now();results['batchWallSeconds']=round(time.monotonic()-T,3);(D/'result.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
def digest(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for x in iter(lambda:f.read(1024*1024),b''):h.update(x)
 return h.hexdigest()
def step(comp,name,argv,cwd,env):
 rec={'name':name,'startedAt':now(),'argv':list(map(str,argv))};comp['stages'].append(rec);save();t=time.monotonic()
 with open(D/(comp['name']+'-'+name+'.log'),'w') as f:
  rc=subprocess.call(list(map(str,argv)),cwd=str(cwd),env=env,stdout=f,stderr=subprocess.STDOUT)
 rec.update(endedAt=now(),seconds=round(time.monotonic()-t,3),exitCode=rc);save();print(comp['name'],name,rc,rec['seconds'],flush=True);return rc
baseenv=os.environ.copy()
for k in list(baseenv):
 if k.startswith(('PIPELINE_','CI_COMMIT','CYF_FLOW_')) or k in ['CI','BUILD_NUMBER','GRADLE_USER_HOME']:baseenv.pop(k,None)
baseenv['PATH']='/home/isp/apps/node/bin:/home/isp/apps/jdk21/bin:'+baseenv.get('PATH','');baseenv['JAVA_HOME']='/home/isp/apps/jdk21'
if '--api-resume' in sys.argv:
 results=json.loads((D/'result.json').read_text());results['status']='RUNNING';results.pop('endedAt',None)
 T=time.monotonic()-(time.time()-datetime.datetime.fromisoformat(results['batchStartedAt']).timestamp())
for name in (['api'] if '--api-resume' in sys.argv else ['web','api']):
 S=pathlib.Path(REQ[name]['source']);previous=results['components'].get(name);C={'name':name,'commit':REQ[name]['commit'],'tree':REQ[name]['tree'],'startedAt':now(),'stages':[]};results['components'][name]=C;ct=time.monotonic()
 if previous:
  C['priorAttempts']=[previous];C['startedAt']=previous['startedAt'];ct=time.monotonic()-(time.time()-datetime.datetime.fromisoformat(C['startedAt']).timestamp())
 save()
 try:
  assert subprocess.check_output(['git','-C',str(S),'rev-parse','HEAD']).decode().strip()==C['commit']
  assert not subprocess.check_output(['git','-C',str(S),'status','--porcelain']).strip()
  env=baseenv.copy()
  if name=='web':
   # All memory-intensive work shares the existing Gradle scheduling lock; no new lock/limits.
   q=time.monotonic();C['status']='QUEUED_ON_EXISTING_BUILD_LOCK';save()
   with open('/tmp/cyf-gradle.lock','a+') as lock:
    fcntl.flock(lock,fcntl.LOCK_EX);C['queueSeconds']=round(time.monotonic()-q,3);C['status']='RUNNING';save()
    rc=step(C,'dependencies',['npm','ci','--no-audit','--no-fund'],S,env)
    if rc==0:rc=step(C,'tests',['npm','run','test:run','--','--profile=release','--reporter-options','reportDir='+str(D/'web-tests')+',reportFilename=mochawesome.json,consoleReporter=dot'],S,env)
    # Build for diagnostic timing even if tests fail; never classify failed tests as publishable.
    brc=step(C,'build',['npm','run','build','--','--outDir',str(B/'web-dist')],S,env) if (S/'node_modules/.bin/vite').exists() else 1
    C['testsPassed']=rc==0;C['buildPassed']=brc==0
    if brc==0:
     (B/'package').mkdir(exist_ok=True);pkg=B/'package/web.tgz'
     prc=step(C,'package',['tar','-czf',str(pkg),'-C',str(B/'web-dist'),'.'],S,env);C['artifact']={'path':str(pkg),'sha256':digest(pkg),'publishable':rc==0 and prc==0};C['packagePassed']=prc==0
    C['status']='PASS' if C.get('testsPassed') and C.get('buildPassed') and C.get('packagePassed') else 'FAIL'
   # Keep reports outside disposable dependencies/worktree.
   if (S/'mochawesome-report').exists():shutil.copytree(S/'mochawesome-report',D/'web-default-reports',dirs_exist_ok=True)
  else:
   home=B/'gradle-home';home.mkdir(mode=0o700,exist_ok=True);(home/'caches').mkdir(exist_ok=True)
   seed=time.monotonic()
   for folder in ['modules-2','build-cache-1']:
    src=pathlib.Path('/var/cache/cyf-gradle-local/caches')/folder
    if src.exists() and not (home/'caches'/folder).exists():subprocess.run(['cp','-a',str(src),str(home/'caches'/folder)],check=True)
   C['stages'].append({'name':'dependency-cache-seed','seconds':round(time.monotonic()-seed,3),'source':'existing intended local cache modules-2 and content-keyed compile cache only; no transforms/test results/JAR'})
   build=B/'api-build';build.mkdir(mode=0o700,exist_ok=True)
   def load(n,p):
    spec=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
   h=load('hist',R/'ops/orchestration/execution_history_check.py')
   env.update(h.credentials(type('Args',(),{'credentials_init':pathlib.Path('/root/.gradle/init.gradle')})()))
   env.update(CYF_LOCAL_GRADLE_ACTIVE='1',CYF_LOCAL_BUILD_ROOT=str(build),CYF_LOCAL_RELEASE_OPT_IN='1',CYF_LOCAL_RELEASE_SOURCE_ROOT=str(S),CYF_LOCAL_RELEASE_BUILD_ROOT=str(build),CYF_LOCAL_RELEASE_VERSION='timing-20261106',CYF_LOCAL_RELEASE_BUILD_ID='local-build-timing-20261106',CYF_LOCAL_RELEASE_COMMIT=C['commit'],CYF_LOCAL_RELEASE_TREE=C['tree'],CYF_REVIEW_MYSQLD='/home/isp/apps/mysql/bin/mysqld',CYF_SM_NODE_BIN='/home/isp/apps/node/bin/node',CYF_SM_NODE_PEER='/home/isp/wsps/chcbz/isp-install/conf/codex-bridge/test/fixtures/skill-management-node-peer.mjs')
   policy=json.loads((D/'backend-policy.json').read_text());tasks=policy['argv'][policy['argv'].index(':agent:jia-agent-mapper:test'):]
   argv=['/home/isp/apps/gradle/9.3.1/bin/gradle','--continue','--no-daemon','--max-workers=2','--build-cache','--console=plain','--stacktrace','-Dorg.gradle.jvmargs=-Xmx768m -XX:MaxMetaspaceSize=384m -XX:ActiveProcessorCount=2','--init-script',str(D/'local.init.gradle'),'--init-script',str(D/'local-release-metadata.init.gradle'),'--init-script',str(D/'timing.init.gradle'),'--project-cache-dir',str(B/'project-cache')]+tasks
   fixture={'argv':argv,'commit':C['commit'],'tree':C['tree'],'localBatch':'local-build-timing-20261106','policySha256':digest(D/'backend-policy.json'),'toolHashes':{p.name:digest(p) for p in [D/'local.init.gradle',D/'local-release-metadata.init.gradle',D/'timing.init.gradle',R/'ops/orchestration/cyf_orchestrator.py']},'nodePeerSha256':digest(pathlib.Path(env['CYF_SM_NODE_PEER'])),'cache':'private home, existing dependency and compile-only cache seed; fresh outputs'}
   (D/'api-inputs.json').write_text(json.dumps(fixture,indent=2));fd=digest(D/'api-inputs.json');C['fixtureDigest']=fd;C['status']='QUEUED_OR_RUNNING_GRADLE';save()
   cmd=['python3','-u',str(R/'ops/orchestration/cyf_orchestrator.py'),'gradle','--heavy','--cwd',str(S),'--tree-sha',C['tree'],'--selector','local-release-policy-timing-20261106-v1','--fixture-digest',fd,'--dependency-cache-home',str(home),'--artifact',str(D/'api-gradle.log'),TASK,'--']+argv
   rc=step(C,'gradle',cmd,S,env);C['status']='PASS' if rc==0 else 'FAIL'
   (D/'api-junit').mkdir(exist_ok=True)
   for xml in build.rglob('TEST-*.xml'):
    dest=D/'api-junit'/xml.relative_to(build);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(xml,dest)
   if (build/'local-bootjar-proof.json').exists():shutil.copy2(build/'local-bootjar-proof.json',D/'local-bootjar-proof.json')
   jars=list(build.glob('**/starter/libs/*.jar'))+list(build.glob('**/jia/starter/libs/*.jar'))
   if not jars:jars=list(build.glob('**/starter/*.jar'))+list(build.glob('**/*starter*/libs/*.jar'))
   if jars:
    (B/'package').mkdir(exist_ok=True);jar=max(jars,key=lambda p:p.stat().st_size);dst=B/'package/api.jar';t=time.monotonic();shutil.copy2(jar,dst);C['stages'].append({'name':'package-copy-and-hash','seconds':round(time.monotonic()-t,3)});C['artifact']={'path':str(dst),'sha256':digest(dst),'publishable':rc==0}
 except Exception as exc:
  C['status']='ERROR';C['error']=type(exc).__name__+': '+str(exc);(D/(name+'-exception.txt')).write_text(traceback.format_exc());print(C['error'],flush=True)
 finally:
  C.update(endedAt=now(),wallSeconds=round(time.monotonic()-ct,3));save()
results['endedAt']=now();results['status']='FINISHED';save();print('FINISHED',flush=True)
