from pathlib import Path
import os,sys,time,json,hashlib,base64,urllib.request,urllib.error,re
run=Path(sys.argv[1]).resolve(); assert str(run)=='/tmp/cyf-aam-resume-20261007/runtime'
ready=json.loads((run/'io/ready.json').read_text());origin=ready['origin'];assert origin=='http://127.0.0.1:18121'
token=(run/'io/admin.jwt').read_text().strip();assert re.fullmatch(r'[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+',token)
c={'agentId':sys.argv[2]}
opener=urllib.request.build_opener(urllib.request.ProxyHandler({}));records=[]
def call(method,path,body=None,key=None,revision=None,auth=True,extra=None,expected=None):
 assert path.startswith('/') and not path.startswith('//')
 headers={'Accept':'application/json'}
 if auth:headers['Authorization']='Bearer '+token
 if body is not None:headers['Content-Type']='application/json'
 if key:headers['Idempotency-Key']=key
 if revision is not None:headers['If-Match']='"v'+str(revision)+'"'
 if extra:headers.update(extra)
 payload=None if body is None else json.dumps(body,ensure_ascii=False,separators=(',',':')).encode()
 try:response=opener.open(urllib.request.Request(origin+path,data=payload,headers=headers,method=method),timeout=60)
 except urllib.error.HTTPError as e:response=e
 raw=response.read();status=response.status
 try:decoded=json.loads(raw)
 except (UnicodeDecodeError,json.JSONDecodeError):decoded=None
 record={'method':method,'path':path,'status':status}
 if isinstance(decoded,dict) and isinstance(decoded.get('code'),str):record['businessCode']=decoded['code']
 records.append(record);(run/'evidence/http-observations.json').write_text(json.dumps({'componentMode':'shared-production-wiring','records':records},indent=2)+'\n');print(json.dumps(record),flush=True)
 if expected is not None:
  assert status==expected,(status,decoded);return decoded
 if status>=400 or isinstance(decoded,dict) and 'data' in decoded and decoded.get('code')!='E0':raise RuntimeError(f'HTTP/business failure {status} {method} {path}: {decoded.get("code") if isinstance(decoded,dict) else "not_json"}')
 return decoded.get('data',decoded) if isinstance(decoded,dict) else decoded
# Authentication denial is observed over actual HTTP before mutations.
call('GET','/archive/admin/v1/collections/platform-classics/slot',auth=False,expected=401)
for n in range(40):
 observed=call('GET','/agent/'+c['agentId'])
 if observed.get('agentId')==c['agentId'] and observed.get('status') in ('idle','online','active','busy'):break
 time.sleep(2)
else:raise RuntimeError('real Client registration did not become online')
catalog=call('GET','/agent/platform-skills/catalog');assert catalog[0]['packageSha256']=='8894d96341067dd7f9e2f45696eef44057dc61346255a0323b2d713a3c7ea081'
stateFile=run/'io/driver-state.json'
state=json.loads(stateFile.read_text()) if stateFile.exists() else {}
def save(): stateFile.write_text(json.dumps(state,indent=2,ensure_ascii=False)+'\n')
def observe(value,fields): print(json.dumps({k:value.get(k) for k in fields}),flush=True)
def wait_install(i):
 for n in range(40):
  result=call('GET','/agent/platform-skills/installations/'+i)
  if result['state']=='SUCCEEDED': return result
  if result['state'] in ['FAILED','REVOKED']: observe(result,['state','errorCode']); raise RuntimeError('installation terminal failure')
  time.sleep(3)
 raise RuntimeError('installation not complete within observation window')
if 'installationId' not in state:
 installed=call('POST','/agent/platform-skills/installations',{'agentId':c['agentId'],'bindingVersion':os.environ['CYF_FIXTURE_BINDING_VERSION'],'skillKey':'archive-maintainer','skillVersion':'1.0.0'},'resume20261007-install')
 state['installationId']=installed['installationId'];save();observe(installed,['installationId','state','errorCode'])
installed=wait_install(state['installationId']);state['installation']=installed;save();print('REAL_CLIENT_INSTALLATION_RECEIPT_PASS',flush=True)
if 'appointment' not in state:
 slot=call('GET','/archive/admin/v1/collections/platform-classics/slot')
 appointment=call('POST','/archive/admin/v1/collections/platform-classics/appointments',{'agentId':c['agentId'],'expectedBindingVersion':os.environ['CYF_FIXTURE_BINDING_VERSION'],'workScopeMode':'COLLECTION','workIds':[],'permissionProfile':'PUBLISH_VALIDATED','requiredSkill':{'key':'archive-maintainer','version':'1.0.0','packageSha256':'8894d96341067dd7f9e2f45696eef44057dc61346255a0323b2d713a3c7ea081'}},'resume20261007-appointment',slot['revision'])
 state['appointment']=appointment;save();observe(appointment,['appointmentId','status','readiness'])
current=call('GET','/archive/admin/v1/collections/platform-classics/appointments')['items']
assigned=[value for value in current if value['appointmentId']==state['appointment']['appointmentId']]
assert len(assigned)==1
observedAppointment=assigned[0]; observedCapabilities=call('GET','/archive/admin/v1/collections/platform-classics/capabilities')
assert observedAppointment['readiness']=='READY' and observedCapabilities['readiness']=='READY'
assert observedAppointment['skillReadiness']['state']=='VERIFIED' and observedAppointment['skillReadiness']['executable'] is True and observedAppointment['skillReadiness']['blocker'] is None
assert observedAppointment['skillReadiness']['proof']['installationRef']==state['installationId']
state['readyObservation']={'appointmentReadiness':observedAppointment['readiness'],'capabilitiesReadiness':observedCapabilities['readiness'],'skillReadiness':observedAppointment['skillReadiness']};save();print('ACTUAL_CURRENT_READY_PROJECTION_PASS',flush=True)
source='第一章\n这是隔离开发验证使用的原创测试文本。\n第二章\n此文本不是公开典籍，不用于生产发布。\n'.encode()
if 'sourceId' not in state:
 accepted=call('POST','/archive/admin/v1/collections/platform-classics/source-snapshots',{'sourceName':'isolated-original-fixture','sourceVersion':'v15','rightsBasis':'Main-authored synthetic test-only text; not a real publication','declaredSha256':hashlib.sha256(source).hexdigest(),'contentBase64':base64.b64encode(source).decode()},'resume20261007-source')
 operation=call('GET','/archive/admin/v1/operations/'+accepted['operationId']);assert operation['state']=='COMMITTED'
 state['sourceId']=operation['result']['sourceId'];state['sourceSha256']=hashlib.sha256(source).hexdigest();save()
for mode in ('manual','auto'):
 if mode not in state:
  job=call('POST','/archive/admin/v1/collections/platform-classics/jobs',{'operation':'ADD_WORK','newWork':{'canonicalKey':'aam-resume20261007-'+mode,'title':'隔离验证 '+mode.upper(),'language':'zh-CN'},'workId':None,'sourceId':state['sourceId'],'publicationMode':mode.upper(),'requestIntentId':'aam-resume20261007-intent-'+mode},'resume20261007-job-'+mode)
  state[mode]={'job':job};save();observe(job,['jobId','state','waitReason','revision'])
 if 'execution' not in state[mode]:
  job=call('GET','/archive/admin/v1/jobs/'+state[mode]['job']['jobId'])
  execution=call('POST','/archive/admin/v1/jobs/'+job['jobId']+'/execute',None,'resume20261007-execute-'+mode,job['revision']);state[mode]['execution']=execution;save();observe(execution,['state','readiness','commandId','runId'])
 for n in range(50):
  job=call('GET','/archive/admin/v1/jobs/'+state[mode]['job']['jobId']);state[mode]['job']=job;save()
  observe(job,['jobId','state','waitReason','revision','draftId','publicationId'])
  if job['state'] in ('AWAITING_PUBLISH','PUBLISHED'): break
  if job['state'] in ('FAILED','CANCELLED'): raise RuntimeError('job terminal failure')
  time.sleep(3)
 else: raise RuntimeError('execution incomplete within observation window')
 if mode=='manual' and job['state']!='PUBLISHED':
  draft=call('GET','/archive/admin/v1/jobs/'+job['jobId']+'/draft')
  validation=call('GET','/archive/admin/v1/drafts/'+draft['draftId']+'/validation');assert validation['outcome']=='PASSED'
  body={'validationId':validation['validationId'],'expectedActiveEditionId':None,'expectedWorkRevision':'0'}
  publication=call('POST','/archive/admin/v1/jobs/'+job['jobId']+'/publish',body,'resume20261007-manual-publish',draft['revision'])
  state[mode]['publication']=publication;save();observe(publication,['publicationId','editionId','readbackState'])
 job=call('GET','/archive/admin/v1/jobs/'+job['jobId']);state[mode]['job']=job;save();assert job['state']=='PUBLISHED'
 print('REAL_'+mode.upper()+'_PUBLISHED_PASS',flush=True)
print('REAL_RUNTIME_MANUAL_AUTO_DRIVER_PASS',flush=True)

for mode in ('manual','auto'):
 job=state[mode]['job'];editions=call('GET','/archive/admin/v1/works/'+job['workId']+'/editions')
 state[mode]['editions']=editions
 selected=next(e for e in (editions if isinstance(editions,list) else editions.get('editions',[])) if e.get('state')=='PUBLISHED')
 edition=selected['editionId']
 catalog=call('GET','/archive/v1/editions/'+edition+'/catalog',auth=False)
 chapters=catalog.get('activeEdition',{}).get('chapters',[]) if isinstance(catalog,dict) else []
 assert chapters,'published catalog must have chapters'
 for chapter in chapters:
  chapterId=chapter.get('blockId',chapter.get('chapterId',chapter.get('id')))
  content=call('GET','/archive/v1/editions/'+edition+'/chapters/'+chapterId,auth=False)
  assert content,'actual Reader chapter is empty'
 state[mode]['readerObserved']=True
save()
(run/'evidence/runtime-result.json').write_text(json.dumps({'status':'passed','runtimeEvidence':'REAL_SHARED_RUNTIME_HTTP_CLIENT_OBSERVED','manualPublished':True,'autoPublished':True,'readerReadback':True,'realClientInstalledApprovedPackage':True,'syntheticFixtureIdentity':True,'productionOperation':False,'paidModel':False,'business84Cases':'not_run'},indent=2)+'\n')