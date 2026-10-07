import { ref } from './archive-5e72cd8b/node_modules/vue/index.js'
import { useHallTypedDeliberation } from './archive-5e72cd8b/src/composables/juyiting/useHallTypedDeliberation.js'
import { catalogPage } from './archive-5e72cd8b/src/composables/juyiting/bountyRequestCatalog.js'

const sha = ch => `sha256:${ch.repeat(64)}`
const ctx = () => ref({ conversationId: '7', conversationGeneration: '1', taskId: 'task-1', targetAgentId: 'agent-1', assignmentRevision: '4' })
const storage = () => { const map=new Map(); return {getItem:k=>map.get(k)||null,setItem:(k,v)=>map.set(k,v)} }
const selector = { kind:'TASK_LINKED_WORKSPACE_VERSION', fileId:'file-1', version:'7', purpose:'REFERENCE', assetId:null, assetRevision:null }
const inspectMeta = requestId => ({ authorizationId:`authorization-${requestId}`, manifestDigest:sha('b'), sourceRefIds:['source-1'], inputSummary:{inputDigest:sha('c'),sources:[{sourceRefId:'source-1',sha256:'d'.repeat(64),byteLength:'12',carrier:'DIRECT_TEXT',contributionDigest:sha('e')}]}})
const answer = requestId => ({schemaVersion:2,contract:'juyiting-typed-inspection-v1',conversationId:'7',conversationGeneration:'1',requestId,requestRevision:'1',turnId:`turn-${requestId}`,state:'READY',outcome:{outcomeId:`outcome-${requestId}`,taskId:'task-1',assignmentRevision:'4',assistantMessageId:'101',finalDigest:sha('a'),kind:'ANSWER',text:'资料已查阅，给出答复。',clarification:null,proposal:null},inspection:inspectMeta(requestId)})
const readyProposal = requestId => ({schemaVersion:2,contract:'juyiting-typed-inspection-v1',conversationId:'7',conversationGeneration:'1',requestId,requestRevision:'1',turnId:`turn-${requestId}`,state:'READY',outcome:{outcomeId:`outcome-${requestId}`,taskId:'task-1',assignmentRevision:'4',assistantMessageId:'102',finalDigest:sha('f'),kind:'EXECUTION_PROPOSAL',text:'资料已经查阅，可以生成。',clarification:null,proposal:{proposalId:`proposal-${requestId}`,state:'PROPOSED',stateVersion:'0',operation:'GENERATE_IMAGE',instruction:'依据已查阅资料生成图像',sourceRefIds:['source-1'],sourceSelectors:[selector],parent:null}},inspection:inspectMeta(requestId)})
const receipt = requestId => ({schemaVersion:1,intent:'DISCUSSION',requestId,userMessageId:'100',turnIds:[`turn-${requestId}`],state:'ADMITTED',stateVersion:'0',eventCursor:'1',statusUrl:`/chat/requests/${requestId}`,typedOutcomeUrl:`/chat/conversations/7/requests/${requestId}/inspection-outcome`,replay:false,pendingQuestionId:null})
const serverCatalog = requestId => catalogPage({schemaVersion:1,scope:{conversationId:'7',conversationGeneration:'1',taskId:'task-1'},after:'0',through:'1',nextAfter:null,hasMore:false,entries:[{ordinal:'1',request:{requestId,requestRevision:'1',conversationId:'7',conversationGeneration:'1',userMessageId:'100',state:'RUNNING',stateVersion:'1',turns:[{turnId:`turn-${requestId}`,requestId,requestRevision:'1',conversationId:'7',conversationGeneration:'1',targetAgentId:'agent-1',contextSnapshotId:'snapshot-1',dispatchId:'dispatch-1',route:'INSPECT',state:'RUNNING',stateVersion:'1',lastDeltaSeq:'0',terminalReason:null,finalMessageId:null,createdAt:'1',updatedAt:'1'}],steps:[{stepId:'step-1',stepNumber:'1',taskId:'task-1',assignmentRevision:'4',targetAgentId:'agent-1',kind:'INSPECT',state:'RUNNING',stateVersion:'1',executionIntentId:null,executionId:null,executionState:null}]}}]},{conversationId:'7',taskId:'task-1',generation:'1',after:'0',through:'1'})
const lane = ({chatApi, store=null, catalog=()=>[], onProposal=null}) => { const context=ctx(); return useHallTypedDeliberation({chatApi,actorScopeKey:ref('owner'),authorizationGeneration:ref(1),getContext:()=>context.value,getContextGeneration:()=>1,getCatalogEntries:catalog,storage:store,enabled:()=>true,onProposal}) }
const record=(id, expected, actual, trace, detail='')=>({id,verdict:JSON.stringify(expected)===JSON.stringify(actual)?'PASS':'FAIL',expected,actual,trace,detail})
const results=[]

// (1) Exact validated server catalog RequestView, route INSPECT, no storage.
{
 const calls=[]; const page=serverCatalog('request-server-inspect'); if(!page) throw new Error('fixture catalog page rejected')
 const l=lane({store:null,catalog:()=>page.entries,chatApi:{get:async path=>{calls.push(path);if(path.endsWith('/inspection-outcome'))return {data:{data:answer('request-server-inspect')}};throw Object.assign(new Error('typed chat path absent'),{status:404})}}})
 const refreshed=await l.refresh(); const actual={firstGet:calls[0]||null,displayed:l.projections.value.map(p=>({purpose:p.purpose,state:p.state,kind:p.outcome?.kind||null}))}
 results.push(record('cold-recovery-server-catalog-route-inspect',{firstGet:'/conversations/7/requests/request-server-inspect/inspection-outcome',displayed:[{purpose:'INSPECT',state:'READY',kind:'ANSWER'}]},actual,calls,`catalog route=${page.entries[0].request.turns[0].route}; storage=null; refresh=${refreshed}`));l.dispose()
}

// (2) Explicit confirm of a real validated READY INSPECT proposal must invoke the existing preview callback.
{
 const calls=[];const callbacks=[];const l=lane({chatApi:{get:async path=>{calls.push(path);return {data:{data:readyProposal('request-ready-inspect')}}}},onProposal:async payload=>{callbacks.push(payload);return true}})
 const p=await l.readOne('request-ready-inspect',undefined,'INSPECT'); const confirmed=await l.confirmProposal(p)
 results.push(record('ready-inspect-explicit-confirm-routes-preview',{confirmed:true,onProposalCalls:1},{confirmed,onProposalCalls:callbacks.length},calls,`purpose=${p?.purpose||null}; callback=${JSON.stringify(callbacks)}`));l.dispose()
}

// (3) A valid submitted INSPECT becomes READY ANSWER; waiting status must clear.
{
 const calls=[];const l=lane({store:storage(),chatApi:{create:async(path,body)=>{calls.push(['POST',path,body.intent]);return {data:{data:receipt('request-ready-answer')}}},get:async path=>{calls.push(['GET',path]);return {data:{data:answer('request-ready-answer')}}}}})
 const submitted=await l.submit({content:'请查阅此资料。',sourceSelectors:[selector],inspection:true});const s=l.inspectionStatus.value;const waiting=/已受理|等待 Agent 查阅|尚未表示已读/.test(s)
 results.push(record('ready-inspect-answer-clears-waiting',false,waiting,calls,`submitted=${submitted}; inspectionStatus=${JSON.stringify(s)}; cards=${JSON.stringify(l.cards.value.map(x=>({purpose:x.purpose,kind:x.outcome.kind})) )}`));l.dispose()
}
console.log(JSON.stringify({candidate:{head:'5e72cd8b5f22c21d80b4d3a349b6f3f6b44a56bc',tree:'08774d4f80a9df7806580bc2485bdfb48dacba99',archive:'git archive'},runtime:{node:process.version},results},null,2))
