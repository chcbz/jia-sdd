import pathlib,json,hashlib,shutil,datetime
D=pathlib.Path(__file__).parent; E=pathlib.Path('/home/isp/wsps/cyf/specs/juyiting-skill-execution/evidence/current-installation-20261025/authorized-release');E.mkdir(exist_ok=True)
def load(p):return json.loads(p.read_text())
def save(n,x):(E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def cp(src,n=None):shutil.copyfile(str(src),str(E/(n or src.name)))
state=load(D/'5260799-watch-status.json');assert state['run']['status']=='SUCCESS' and state['elapsed']<600
restore=load(D/'5260799-restore.json');assert restore['state']=='APPLIED'
release=load(D/'online/versioned-release-308.json'); assert release['commit']=='347dff304123a031a6d0f5e27d2cb3df58555eaf' and release['status']=='verified'
summary=load(next((D/'artifact-evidence').glob('*summary*')));assert summary['counts']==dict(tests=3261,failures=0,errors=0,skipped=164)
receipt=load(next((D/'artifact-evidence').glob('*receipt*')));assert receipt['source']['commit_sha']==release['commit'] and receipt['source']['tree_sha']==release['tree']
cp(next((D/'artifact-evidence').glob('*summary*')),'api-test-summary.json');cp(next((D/'artifact-evidence').glob('*receipt*')),'same-run-receipt.json')
for n in ['5260799-start-context.json','5260799-start-result.json','5260799-update.json','5260799-restore.json','tested-policy.json','runtime-baseline.json','runtime-test-log.txt','deploy-order.json','canonical-path-check.txt']:cp(D/n)
for p in (D/'online').iterdir():cp(p)
# Store only safe Run status/identity/times/actions; job runtime parameters are not evidence.
safeRun={'createTime':state['run']['createTime'],'updateTime':state['run']['updateTime'],'pipeline':5260799,'run':308,'status':'SUCCESS','observedTerminalSeconds':state['elapsed'],'stages':[]}
for s in state['run']['stages']:
 info=s['stageInfo'];safeRun['stages'].append({k:info[k] for k in ['name','startTime','endTime','status'] if k in info});safeRun['stages'][-1]['jobs']=[{'id':j['id'],'name':j['name'],'status':j['status']} for j in info['jobs']]
save('run-status.json',safeRun)
B=D/'browser'; latest={}; samples={}; snapshots=[]
for f in sorted(B.glob('response-*.json')):
 d=load(f);latest[d['path']]=d
 if d['path'].endswith('/skills') and 'wuyong' in d['path']:
  for item in d['body'].get('data',{}).get('items',[]):
   if item['skillKey']=='text-file' and item.get('latestChange',{}):
    c=item['latestChange']
    if c.get('status')=='SUCCEEDED' and c.get('runtimeSynced'):
     samples[c['skillChangeId']]={'at':d['at'],'httpStatus':d['status'],'skillKey':'text-file','installation':item['installed'],'desiredEnabled':item['desiredEnabled'],'admissionEnabled':item['admissionEnabled'],'runtime':item['runtime'],'change':{k:v for k,v in c.items() if k!='actorLabel'}}
profile=next(v for k,v in latest.items() if k.endswith('/profile-capabilities') and 'wuyong' in k);skills=next(v for k,v in latest.items() if k.endswith('/skills') and 'wuyong' in k);records=next(v for k,v in latest.items() if k.endswith('/skill-changes') and 'wuyong' in k)
profileItems=profile['body']['data']['skills']['items'];assert len(profileItems)==4 and len(set(x['skillKey'] for x in profileItems))==4
assert [x['skillVersion'] for x in profileItems if x['skillKey'] in ['image-edit','image-generate']]==['1.2.0','1.2.0']
for c in records['body']['data']['items']:c.pop('actorLabel',None)
save('live-profile-current.json',{'at':profile['at'],'status':profile['status'],'skills':profile['body']['data']['skills']});save('live-records.json',records)
ids=['sc_6e40f859069b49af8e8e48483c9b9305','sc_009935d8bc6d4b6991720c84400815bf','sc_547871b1b6a04ae093ae9d9f8e77ca7a','sc_906df800c34c403ea33674b45811e6cf','sc_13c926f1518a47d3a87021b066bfb655'];assert all(i in samples for i in ids)
selected=[samples[i] for i in ids];assert len(set(x['installation']['skillInstallationId'] for x in selected))==1
assert [x['admissionEnabled'] for x in selected]==[True,False,True,False,True]
assert selected[0]['change']['price']['amountMinor']=='0' or selected[0]['change']['price']['amountMinor']==0
save('live-install-and-policy.json',selected)
ui=load(B/'post-browser-result.json');final=load(B/'post-refresh-final-result.json');assert all(x['pass'] for x in final['checks']);passed=[x for x in ui['checks'] if x['pass']]+final['checks'];assert len(passed)==28
save('browser-regression.json',{'at':final['at'],'scope':final['scope'],'passedChecks':passed,'count':28,'harnessNotes':['Earlier diagnostics used whole panel text instead of button text, preserved expanded state, and programmatic clicks without focus; corrected harness without changing product or dropping assertions.','Page reload was initially clicked before application bootstrap settled; continued after bootstrap and re-ran actual reload with explicit readiness plus 1.5s diagnostic settling; final refresh/records/outside-close six checks passed.','Original harness attempts retained separately; no claim all attempts passed.']})
for f in B.glob('post-browser-harness-*.json'):cp(f)
cp(B/'post-browser-result.json','browser-initial-diagnostic.json');cp(B/'post-refresh-final-result.json');cp(D/'post-browser.cjs');cp(D/'final-browser.cjs')
for n in ['before-profile-duplicate.png','after-profile-current-only.png','live-free-install-success.png','live-disable-success.png','live-enable-success.png','post-management-390x844.png','post-management-320x740.png','post-management-390x480.png','post-offline-read-error.png','post-network-recovered.png','post-deploy-disable-success.png','post-deploy-enable-success.png','post-refresh-records.png','post-final-manager.png']:cp(B/n)
network=load(B/'readonly-network.json');writes=[x for x in network if x['method']=='POST' and ('/skill-changes' in x['path'] or '/skill-orders/' in x['path'])];assert len(writes)==6 and all(x['explicitPermit'] and x['allowed'] for x in writes);save('skill-write-audit.json',writes)
names=['SkillManagement','InstalledSkillDescriptorServiceTest','ChatActionCapabilityServiceTest','AgentProfileCapabilitiesServiceTest'];target=[s for s in summary['suites'] if any(n in s['name'] for n in names)]
result={'verifiedAt':datetime.datetime.now().isoformat(),'taskId':'SKILL-MANAGEMENT-API-20261023','owner':'codex-skill-full-owner','scope':'Skill management regression, authorized API release, real login post-release verification','fix':'Current skills use activeInstallationId; history/exact old-task references retained. No Web, Runtime or DB schema change in this release.','api':{'version':'1.17.6','pipeline':5260799,'run':308,'source':receipt['source'],'artifactSha256':release['artifact_sha256'],'jarSha256':release['jar_sha256'],'receiptSha256':release['receipt_sha256'],'passed':3097,'skipped':164,'failures':0,'errors':0,'targetedPassed':90,'targetedSuites':target,'observedTerminalSeconds':state['elapsed'],'lastStageEndMinusRunCreateSeconds':(max(s['stageInfo'].get('endTime',0) for s in state['run']['stages'])-state['run']['createTime'])/1000,'deployOrder':71766552,'installation':'verified','health':'UP','readiness':'UP','configRestored':True},'web':{'commit':'075c0c28a7cf7410d915dc15ca5eb5ff50ace01d','tree':'752e9bccdf3e2bda5506f28424e6e214e8010518','existingOnlineRun':317,'exactSourceVerificationRun':318,'passed':3339,'pending':2,'redeployed':False},'runtime':dict(load(D/'runtime-baseline.json'),passedCurrentSourceManagementTests=119,failed=0,skipped=0,redeployed=False),'browser':{'realProductionChecksPassed':28,'beforeReleaseWrites':['free text-file INSTALL','DISABLE','ENABLE'],'afterReleaseWrites':['DISABLE','ENABLE'],'finalInstallationId':'si_1ced6eb5aca34793a05ca3698ba04a10','finalEnabled':True,'finalRuntimeSynced':True,'profileCurrentSkills':4,'managementRows':5,'operationRecords':8,'paidModelInvocations':0,'paymentAmount':0,'paidUpgradeExecuted':False},'limits':['No naturally upgradeable owned installed SKU remained; real existing upgrade records checked, new upgrade/failure/old-task retention covered by current-source MySQL and Node fixtures, not a new production upgrade execution.','Real charging/refunds, provider-model invocation, physical mobile devices and destructive Runtime outage not performed; offlining is limited to this dedicated browser.','API restart required re-login; this verifies restored facts after authentication, not seamless survival of the prior login session.','Skipped/pending tests are not counted as passes; browser-bootstrap harness attempts are retained, not relabeled successes.'],'recovery':'Previous JAR backup SHA verified; existing controlled versioned installation required for rollback; no restore of business state.'}
save('summary.json',result)
with (E/'SHA256SUMS.txt').open('w') as out:
 for p in sorted(E.iterdir()):
  if p.is_file() and p.name!='SHA256SUMS.txt':out.write(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n')
print('Evidence',E);print('Real checks',len(passed),'writes',len(writes))
