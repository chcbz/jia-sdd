import json,pathlib,datetime,collections,hashlib
p=pathlib.Path(__file__).parent
rows=[json.loads(l) for l in (p/'business-responses.jsonl').open()]
net=[json.loads(l) for l in (p/'network.jsonl').open()]
req=[r for r in net if r.get('event')=='request']
points=[r for r in rows if '/429/point-and-deliberate' in r['request']['url']]
create=[r for r in rows if r['request']['url'].endswith('/tasks/creation-operations/v2') and r['request']['method']=='POST']
pointposts=[r for r in points if r['request']['method']=='POST']
assert len(create)==1 and len(pointposts)==1
for task in ['429','426','424']:
 exact=[x for x in rows if x['request']['url'].endswith('/agent/tasks/'+task)]
 if exact:(p/('task-'+task+'-readback.json')).write_text(json.dumps(exact[-1],ensure_ascii=False,indent=2))
for name,obj in [('task-429-create-receipt',create[0]),('task-429-point-receipt',pointposts[0]),('task-429-last-bootstrap',points[-1])]:
 (p/(name+'.json')).write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def dt(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00')) if hasattr(datetime.datetime,'fromisoformat') else datetime.datetime.strptime(s,'%Y-%m-%dT%H:%M:%S.%fZ').replace(tzinfo=datetime.timezone.utc)
def local(s):return dt(s).astimezone(datetime.timezone(datetime.timedelta(hours=8))).isoformat()
last=points[-1]['data']['data'];assert last['bootstrapState']=='PENDING' and last['conversationId'] is None and last['initialRequestId'] is None
writeCounts={
'createPOST':sum(r['method']=='POST' and r['url'].endswith('/agent/tasks/creation-operations/v2') for r in req),
'pointPOST':sum(r['method']=='POST' and r['url'].endswith('/agent/tasks/429/point-and-deliberate') for r in req),
'finalizationPOST':sum(r['method']=='POST' and '/finalizations' in r['url'] for r in req),
'chatStreamPOST':sum(r['method']=='POST' and r['url'].endswith('/chat/stream') for r in req),
'interactionPOST':sum(r['method']=='POST' and '/interactions' in r['url'] for r in req),
'bootstrapGETCapturedResponses':sum(r['request']['method']=='GET' for r in points)}
s={'status':'FAIL_NEW_PLAINTEXT_FLOW_BOOTSTRAP_BLOCKED','observedDate':'2026-10-08','timezone':'Asia/Shanghai','method':'Owned Chromium 133, normal account login and native UI clicks, mobile viewport 390x844, real production; no mocks or direct API business writes','actor':'chcbz (profile UI verified)','newTaskId':'429','createdAt':local(create[0]['at']),'pointedAt':local(pointposts[0]['at']),'lastBootstrapObservedAt':local(points[-1]['at']),'elapsedPointToLastReadSeconds':(dt(points[-1]['at'])-dt(pointposts[0]['at'])).total_seconds(),'newTaskStatus':'assigned','newTaskVersion':'1','bootstrap':last,'networkCounts':writeCounts,'results':[
{'id':'NEW01','status':'REPRODUCED','finding':'Creation/assignment accepted; bootstrap stays PENDING, no conversationId/initialRequestId; existing relay startup failure and stop in same live API PID logs'},
{'id':'SF01','status':'NOT_RETESTED_ORIGINAL_PATH','finding':'Automatic post-assignment discussion never opened. Manual task-detail discussion return reaches detail, but that is not the original auto-entry path.'},
{'id':'SF02','status':'REPRODUCED_ASSIGNMENT_ONLY','finding':'New task assigned to Gongsun Sheng but homepage still open/unassigned until full reload; acceptance refresh subcase blocked'},
{'id':'SF03','status':'REPRODUCED','finding':'98-character submitted draft remains after COMMITTED creation; cleared only after full reload'},
{'id':'SF04','status':'REPRODUCED_EXISTING_COMPLETED_RECORD','finding':'Current GET task426 completed/version4; reopened results enable Confirm acceptance/Continue modification. Composer/attachments/voice remain enabled. No repeat acceptance or send attempted.'},
{'id':'SF05','status':'REPRODUCED_EXISTING_MESSAGE','finding':'Task426 same USER bubble visibly repeats request twice; not proof of duplicate backend execution'},
{'id':'R01','status':'REPRODUCED_EXISTING_MIXED_PROJECTION','finding':'Task424 chat still shows image and text, results says delivery scope unclear and has no accept button; no new image/edit/acceptance run'},
{'id':'new-delivery-acceptance','status':'BLOCKED_UPSTREAM','finding':'Not reached; do not substitute old completed task for new business pass'}],
'notRun':['new Agent response/delivery/acceptance','new mixed-image generation/edit/acceptance','attachment-only and natural clarification','real microphone/audio','cross-account isolation','real-device keyboard','fault injection'],
'boundaries':['No code/config/deploy/service restart/direct DB write','No task cleanup/archive/cancel; 429 remains assigned/pending','Only one new task; old 424/426 read-only viewing','Fresh browser credentials used only for normal login; no credentials persisted in scripts/reports','Owned browser closed and temporary profile cleanup requested by driver; no other browser/service touched']}
(p/'summary.json').write_text(json.dumps(s,ensure_ascii=False,indent=2))
print(json.dumps({k:s[k] for k in ['status','createdAt','pointedAt','lastBootstrapObservedAt','elapsedPointToLastReadSeconds','networkCounts']},ensure_ascii=False,indent=2))
