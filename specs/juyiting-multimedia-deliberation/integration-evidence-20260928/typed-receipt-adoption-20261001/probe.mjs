import { createRequire } from 'node:module'
import { readFileSync } from 'node:fs'
const worktree = process.env.WEB_TYPED_WT || '/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/web-typed-natural-followup-owner-v1-20261001'
const require = createRequire(`${worktree}/package.json`)
const Vue = require('vue')
const { ref, proxyRefs, isRef } = Vue
const { compile } = require('@vue/compiler-dom')
const { useHallTypedDeliberation } = await import(`${worktree}/src/composables/juyiting/useHallTypedDeliberation.js`)
const tests=[]
const test = async (name, fn) => { try { await fn(); tests.push({name,pass:true}) } catch(error) { tests.push({name,pass:false,error:error.message}) } }
const assert = (value,msg) => { if(!value)throw new Error(msg) }
const source = readFileSync(`${worktree}/src/components/world/JuyiHall.vue`,'utf8')
const clarify=()=>({schemaVersion:1,conversationId:'7',conversationGeneration:'1',requestId:'request-1',requestRevision:'1',turnId:'turn-1',state:'READY',outcome:{outcomeId:'outcome-1',taskId:'task-1',assignmentRevision:'4',assistantMessageId:'101',finalDigest:'sha256:'+'a'.repeat(64),kind:'CLARIFY',text:'请补充颜色',clarification:{pendingQuestionId:'pending-1',state:'OPEN',stateVersion:'0',question:'请补充颜色',requiredFacts:['REQUIREMENT_DETAILS'],replyRequestId:null},proposal:null}})
const answered=()=>{const p=clarify();p.outcome.clarification={...p.outcome.clarification,state:'ANSWERED',stateVersion:'1',replyRequestId:'reply-1'};return p}
const context={conversationId:'7',conversationGeneration:'1',taskId:'task-1',targetAgentId:'agent-1',assignmentRevision:'4'}
const config={actorScopeKey:ref('owner'),authorizationGeneration:ref(1),getContext:()=>context,getContextGeneration:()=>1,getCatalogEntries:()=>[],enabled:()=>true}
await test('real JuyiHall template passes typed refs as values not RefImpl',()=>{
 const tag=source.match(/<BountyDiscussionPanel\b[\s\S]*?>/)[0]
 const attrs=[...tag.matchAll(/:(typed-[a-z-]+)="([^"]+)"/g)].map(m=>`:${m[1]}="${m[2]}"`).join(' ')
 const render = new Function('Vue',compile(`<BountyDiscussionPanel ${attrs} />`,{mode:'function'}).code)(Vue)
 const values={typedDeliberation:{cards:ref([]),selectedPending:ref(null),recoveryAvailable:ref(false)},typedDeliberationEnabled:ref(true)}
 const vnode=render(proxyRefs(values),[])
 assert(Array.isArray(vnode.props['typed-outcomes']),`typed-outcomes=${isRef(vnode.props['typed-outcomes'])?'RefImpl':typeof vnode.props['typed-outcomes']}; Vue Array prop broken`)
 assert(vnode.props['typed-pending-question']===null,'pending-question is RefImpl instead of null')
 assert(vnode.props['typed-recovery-available']===false,'recovery-available is RefImpl instead of false')
})
await test('actual BountyDiscussionPanel forwards selected reference payload',()=>{
 const panel=readFileSync(`${worktree}/src/components/juyiting/BountyDiscussionPanel.vue`,'utf8')
 const tag=panel.match(/<ChatPanel\b[\s\S]*?>/)[0]
 const attr=tag.match(/@send-message="([^"]+)"/)[1]
 const render=new Function('Vue',compile(`<ChatPanel @send-message="${attr}" />`,{mode:'function'}).code)(Vue)
 const calls=[];const vnode=render({$emit:(...args)=>calls.push(args)},[])
 const selected={sourceSelectors:[{kind:'TASK_LINKED_WORKSPACE_VERSION',fileId:'f1',version:'1',purpose:'REFERENCE',assetId:null,assetRevision:null}]}
 vnode.props.onSendMessage(selected)
 assert(calls[0]?.[1]===selected,`actual forwarded args=${JSON.stringify(calls)}; selected references dropped`)
})
await test('out-of-order OPEN read cannot reopen ANSWERED question',async()=>{
 const pending=[];const lane=useHallTypedDeliberation({...config,chatApi:{get:()=>new Promise(resolve=>pending.push(resolve))}})
 const old=lane.readOne('request-1');const fresh=lane.readOne('request-1')
 pending[1]({data:{data:answered()}});await fresh
 pending[0]({data:{data:clarify()}});await old
 const state=lane.projections.value[0]?.outcome.clarification.state;lane.dispose()
 assert(state==='ANSWERED',`after new ANSWERED then late OPEN state=${state}`)
})
await test('ANSWERED read invalidates selected pending question before send',async()=>{
 let current=clarify();const lane=useHallTypedDeliberation({...config,chatApi:{get:async()=>({data:{data:current}})}})
 await lane.readOne('request-1');assert(lane.choosePending(lane.projections.value[0]),'choose pending failed')
 current=answered();await lane.readOne('request-1');const selected=lane.selectedPending.value;lane.dispose()
 assert(selected===null,`selected=${JSON.stringify(selected)}; already answered question remains reply target`)
})
await test('GET outcome cannot accept mismatched task/assignment into current scope',async()=>{
 const wrong=clarify();wrong.outcome.taskId='foreign-task';wrong.outcome.assignmentRevision='99'
 const lane=useHallTypedDeliberation({...config,chatApi:{get:async()=>({data:{data:wrong}})}})
 await lane.readOne('request-1');const count=lane.cards.value.length;lane.dispose()
 assert(count===0,`foreign task/assignment accepted cards=${count}`)
})
await test('proposal with selected TASK_LINKED reference remains displayable',async()=>{
 const {typedOutcomeProjection}=await import(`${worktree}/src/composables/juyiting/hallTypedDeliberation.js`)
 const p=clarify();p.outcome.kind='EXECUTION_PROPOSAL';p.outcome.clarification=null
 p.outcome.proposal={proposalId:'proposal-1',state:'PROPOSED',stateVersion:'0',operation:'GENERATE_IMAGE',instruction:'根据参考图画一只鸟',sourceRefIds:['source-1'],sourceSelectors:[{kind:'TASK_LINKED_WORKSPACE_VERSION',fileId:'f1',version:'1',purpose:'REFERENCE',assetId:null,assetRevision:null}],parent:null}
 assert(typedOutcomeProjection(p,context)!==null,'GEN with reference discarded by parser')
})
console.log(JSON.stringify({worktree,results:tests,passed:tests.filter(t=>t.pass).length,failed:tests.filter(t=>!t.pass).length,scope:'actual production Web composable and template/emit expressions; no browser/Provider/API runtime'},null,2))
process.exitCode=tests.some(t=>!t.pass)?1:0
