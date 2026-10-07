#!/usr/bin/env python3
"""Read-only, targeted document/evidence checks; no build, deploy or business write."""
import hashlib,json,pathlib,re,subprocess
ROOT=pathlib.Path('/home/isp/wsps/cyf')
FEATURE=ROOT/'specs/juyiting-multimedia-deliberation'
EVIDENCE=ROOT/'docs/implementation/evidence/mmd-shortest-flow-20261007'

def check():
    required=['spec.md','design.md','tasks.md','acceptance.md','integration.yaml','delivery-status.md','remaining-tasks-20261007.md','shortest-flow-test-20261007.md','cleanup-status-20261007.md']
    for name in required: assert (FEATURE/name).is_file(),name
    selected=[FEATURE/n for n in ['delivery-status.md','remaining-tasks-20261007.md','shortest-flow-test-20261007.md','cleanup-status-20261007.md']]+[EVIDENCE/'report.md']
    links=0
    for f in selected:
        for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
            if target.startswith(('https:','http:','#')):continue
            target=target.split('#')[0]
            assert (f.parent/target).exists(),(str(f),target)
            links+=1
    json_count=0
    for f in EVIDENCE.glob('*.json'):
        if f.name=='validation.json':continue
        json.loads(f.read_text());json_count+=1
    summary=json.loads((EVIDENCE/'summary.json').read_text())
    v=json.loads((EVIDENCE/'refreshed-server-readback.json').read_text())['evaluation']
    task=v['task']['data']['data'];op=v['operation']['data']['data'];ds=v['deliveries']['data']['items']
    assert v['task']['status']==v['operation']['status']==v['deliveries']['status']==200
    assert task['status']==summary['taskState']=='completed' and task['taskVersion']==summary['taskVersion']=='4'
    assert op['state']=='completed' and op['stage']=='TASK_COMPLETED' and op['deliveryState']=='accepted'
    assert len(ds)==1 and ds[0]['state']=='accepted' and ds[0]['deliveryId']==summary['deliveryId']==op['deliveryId']
    text='最短流程已走通。\n验证标记：Cedar path 807.'.encode()
    assert len(text)==summary['textBytes']==55 and hashlib.sha256(text).hexdigest()==summary['textSha256']==op['selectedOutputs'][0]['sha256']
    for name,path in [('point-once.json','/agent/tasks/426/point-and-deliberate'),('accept-once.json','/agent/tasks/426/finalizations')]:
        rs=json.loads((EVIDENCE/name).read_text())['requests']
        assert len([r for r in rs if r['method']=='POST' and r['path']==path])==1
    assert len(v['catalog']['data']['data']['entries'])==1
    for name in ['completed-results.json','queried-accept-status.json','refreshed-server-readback.json']:
        rs=json.loads((EVIDENCE/name).read_text())['requests']
        assert not any(r['method']=='POST' and '/finalizations' in r['path'] for r in rs)
    cleanup=json.loads((EVIDENCE/'cleanup-manifest.json').read_text())
    assert len(cleanup['worktrees'])==cleanup['worktreesRemoved']==61
    assert len(cleanup['localBranches'])==cleanup['localBranchesDeleted']==60
    assert sum(x['state']=='DELETED_READBACK_ABSENT' for x in cleanup['remoteBranches'])==10
    assert sum(x['state']=='KEEP_REMOTE_CHANGED' for x in cleanup['remoteBranches'])==3
    assert cleanup['sessionsDeleted']==0
    # These are immutable historical receipts, not a new online run.
    prior=json.loads((EVIDENCE/'prior-evidence-manifest.json').read_text())
    for f in prior['files']:
        p=ROOT/f['path'];assert p.stat().st_size==f['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==f['sha256']
    manifest=json.loads((EVIDENCE/'manifest.json').read_text())
    for item in manifest['files']:
        p=ROOT/item['path'];assert hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],item['path']
    return {'status':'PASS_DOCUMENT_EVIDENCE_CHECKS','relativeLinksChecked':links,'newJsonFilesParsed':json_count,'priorReceiptsVerified':len(prior['files']),'businessSubset':'PASS_WITH_UI_GAPS','fullMultimedia':'NOT_COMPLETE','builds':0,'deployments':0,'sessionsDeleted':0,'limitations':['No full application suite was run for document-only change','Historical imported contracts and failures preserved, not reclassified','Only new status-document links checked; historical archival links not globally rewritten']}

if __name__=='__main__': print(json.dumps(check(),ensure_ascii=False,indent=2))
