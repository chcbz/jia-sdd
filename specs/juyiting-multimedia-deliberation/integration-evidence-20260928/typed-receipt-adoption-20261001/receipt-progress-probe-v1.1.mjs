import { createRequire } from 'node:module'
const worktree = process.env.WEB_TYPED_WT
if (!worktree) throw new Error('WEB_TYPED_WT required')
const require = createRequire(`${worktree}/package.json`)
const { JSDOM } = require('jsdom')
const dom = new JSDOM('<!doctype html><html><body></body></html>', { url:'http://localhost' })
for (const [key,value] of Object.entries({window:dom.window,document:dom.window.document,navigator:dom.window.navigator,DOMParser:dom.window.DOMParser})) Object.defineProperty(globalThis,key,{value,writable:true,configurable:true})
const {ref} = require('vue')
const {useHallConversation} = await import(`${worktree}/src/composables/juyiting/useHallConversation.js`)
const receipt = {schemaVersion:1,intent:'DISCUSSION',requestId:'request-typed-1',userMessageId:'100',turnIds:['turn-typed-1'],state:'ADMITTED',stateVersion:'0',eventCursor:'1',statusUrl:'/chat/requests/request-typed-1',typedOutcomeUrl:'/chat/conversations/7/requests/request-typed-1/typed-outcome',replay:false,pendingQuestionId:null}
const context = {conversationId:'7',conversationGeneration:'1',taskId:'task-1',targetAgentId:'agent-1',assignmentRevision:'4'}
const canonical = () => ({requestId:'request-typed-1',requestRevision:'1',stateVersion:'0',conversationId:'7',conversationGeneration:'1',userMessageId:'100',state:'ADMITTED',turns:[{turnId:'turn-typed-1',requestId:'request-typed-1',requestRevision:'1',stateVersion:'0',conversationId:'7',conversationGeneration:'1',targetAgentId:'agent-1',state:'WAITING',lastDeltaSeq:'0',finalMessageId:null}]})
const results=[]
for (const [name,mutate,expected] of [
 ['canonical RUNNING request after ADMITTED receipt adopts',v=>{v.state='RUNNING';v.turns[0].state='RECEIVED'},true],
 ['progressed COMPLETED request adopts same immutable receipt binding',v=>{v.state='COMPLETED';v.stateVersion='1';v.turns[0].state='FINAL_PERSISTED';v.turns[0].stateVersion='3';v.turns[0].finalMessageId='101'},true],
 ['aggregate RUNNING is not the frozen admission receipt state',v=>{receipt.state='RUNNING';v.state='RUNNING';v.turns[0].state='RECEIVED'},false]
]) {
 const calls=[]; const view=canonical();mutate(view)
 const hall = useHallConversation({apiStore:{authorizationGeneration:1,token:async()=>null},chatContext:ref({conversationScopeType:'bounty',conversationScopeKey:'task-1',mode:'bounty',taskId:'task-1',targetAgentId:'agent-1',targetAgentIds:['agent-1']}),chatMode:ref('bounty'),selectedTask:ref({id:'task-1'}),selectedAgent:ref({agentId:'agent-1',name:'吴用'}),chatApi:{
 list:async(_p,_b,o)=>{calls.push('LIST');o.onSuccess({data:[{id:'7',conversationType:'juyiting',conversationScopeType:'bounty',conversationScopeKey:'task-1'}]})},
 getById:async(_p,id,o)=>{calls.push(`CONTENT:${id}`);o.onSuccess({data:[]})}, get:async path=>{calls.push(`GET:${path}`);return {data:{data:view}}},create:async()=>{throw new Error('unexpected POST')}
 },globalStore:{getJiacn:'owner',user:{}},log:{warn:()=>{},error:()=>{}},openPanel:()=>{},outgoingMetadata:ref({}),portraitShortName:a=>a?.name||'',showToast:()=>{}})
 await hall.loadHallMessages();calls.length=0
 const accepted=await hall.adoptTypedDiscussionReceipt({receipt,context,isCurrent:()=>true})
 const pass=accepted===expected && (expected || (hall.activeRequest.value===null && !calls.some(c=>c.startsWith('CONTENT:'))))
 results.push({name,expected,accepted,activeRequestId:hall.activeRequest.value?.requestId||null,calls,pass})
 hall.disposeHallConversation()
}
console.log(JSON.stringify({worktree,scope:'actual production composable with existing API RequestView RUNNING/COMPLETED state semantics; no live API or browser',results,passed:results.filter(r=>r.pass).length,failed:results.filter(r=>!r.pass).length},null,2));dom.window.close();process.exitCode=results.some(r=>!r.pass)?1:0
