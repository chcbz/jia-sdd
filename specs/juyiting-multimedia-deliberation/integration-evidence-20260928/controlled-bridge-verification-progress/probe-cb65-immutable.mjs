import { readFileSync, writeFileSync } from 'node:fs'
import { ref } from '/home/isp/wsps/cyf/web/node_modules/vue/dist/vue.runtime.esm-bundler.js'
import { useHallPointAndStartControlledBridge } from '/var/tmp/cyf-mmd-main-web-bridge-probe/immutable-cb65/src/composables/juyiting/useHallPointAndStartControlledBridge.js'
import { useHallPointAndStart } from '/var/tmp/cyf-mmd-main-web-bridge-probe/immutable-cb65/src/composables/juyiting/useHallPointAndStart.js'
import { providerConsentAcknowledgement } from '/var/tmp/cyf-mmd-main-web-bridge-probe/immutable-cb65/src/composables/juyiting/hallPointAndStartProviderConsent.js'
const fixture=JSON.parse(readFileSync('/var/tmp/cyf-mmd-main-web-bridge-probe/immutable-cb65/tests/fixtures/controlled-image-bridge-v1.json'))
const copy=v=>JSON.parse(JSON.stringify(v)); const memory=()=>{const m=new Map();return{getItem:k=>m.get(k)??null,setItem:(k,v)=>m.set(k,v)}}
const tid='task_fixture_1', aid='agent_fixture_1', scope=ref('tenant\u0000client\u0000owner')
const bound=()=>copy(fixture.wire.wrapper_receipt),issue=()=>({...copy(fixture.wire.wrapper_receipt.providerConsent),state:'ISSUED',version:'1'})
const task=()=>({id:tid,taskVersion:'6',status:'open'})
const req=()=>({taskId:tid,taskVersion:'6',requirementRevision:'3',title:'fixture',description:null,contentSha256:'a'.repeat(64),source:'CREATE'})
const params={task:task(),agent:{agentId:aid},requestedOperations:['GENERATE_IMAGE'],initialOperation:'GENERATE_IMAGE',inputRefs:[],providerBinding:{bindingId:'fixture_binding',bindingEpoch:'1'},acknowledgement:providerConsentAcknowledgement}
const setup=({storage=memory(),api,onBound}={})=>{
 const calls=[];api=api||{get:async path=>{calls.push(['GET',path]);return{data:path.endsWith('/requirements/current')?req():task()}},create:async path=>{calls.push(['POST',path]);return{data:path.endsWith('cost-consents')?issue():bound()}}}
 const flow=useHallPointAndStartControlledBridge({agentApi:api,actorScopeKey:scope,storage,keys:{createAssignmentKey:()=> 'fixture_assignment_key',createIssueKey:()=> 'fixture_issue_key'},onBound});flow.selectContext({taskId:tid,targetAgentId:aid});return{flow,calls,storage}
}
const findings=[]
// Actual page callback delegates to old core checkOriginal which rejects consent-bearing intents.
{
 const storage=memory();let adopted=0;const oldCalls=[]
 const native=useHallPointAndStart({agentApi:{get:async p=>{oldCalls.push(p);throw Error('not reached')}},actorScopeKey:scope,storage,onAdmitted:async()=>{adopted++;return true}})
 const h=setup({storage,onBound:async()=>native.checkOriginal(tid)});const result=await h.flow.start(params)
 findings.push({case:'actual controlled-flow + legacy-checkOriginal page callback',result,posts:h.calls.filter(c=>c[0]==='POST').length,adopted,projection_GETs:oldCalls.length,native_state:native.state.value.status,expected:'adopt original first conversation, not BOUND UI alone'})
 h.flow.dispose();native.dispose()
}
// Deferred GET404 after identity/selection invalidation still calls create before current check.
{
 const first=setup();await first.flow.start(params);first.flow.dispose();let rejectGet;let posted=0
 const h=setup({storage:first.storage,api:{get:()=>new Promise((_,reject)=>{rejectGet=reject}),create:async()=>{posted++;return{data:bound()}}}})
 const pending=h.flow.resumeOriginal(tid);await Promise.resolve();h.flow.invalidate();rejectGet(Object.assign(new Error('absent'),{status:404}));const result=await pending
 findings.push({case:'late GET404 after invalidation',result,bridge_POSTs:posted,expected_POSTs:0});h.flow.dispose()
}
// Uncertain issuer stage leaves durable intent but both recovery actions do no authoritative GET.
{
 const calls=[];const h=setup({api:{get:async p=>{calls.push(['GET',p]);return{data:p.endsWith('/requirements/current')?req():task()}},create:async p=>{calls.push(['POST',p]);throw new Error('issuer response lost')}}})
 const result=await h.flow.start(params);calls.length=0;const checked=await h.flow.checkOriginal(tid),resumed=await h.flow.resumeOriginal(tid)
 findings.push({case:'issue response lost before bridge wrapper',start_result:result,check_result:checked,resume_result:resumed,recovery_HTTP:calls,expected:'original issuerkey read-only check; no newkey/reissue on refresh'});h.flow.dispose()
}
const out={commit:'cb65ebfa74267dcc7151757fa18a2ade32ed85e3',tree:'4ed8dadf36eacc35458ed5f253305ae259086c38',actual_code_fake_HTTP_no_provider:true,findings};writeFileSync('/var/tmp/cyf-mmd-main-web-bridge-probe/findings-cb65-immutable.json',JSON.stringify(out,null,2)+'\n');console.log(JSON.stringify(out,null,2))
