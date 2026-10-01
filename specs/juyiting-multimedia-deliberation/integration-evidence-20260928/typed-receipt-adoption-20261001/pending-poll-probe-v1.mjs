import { createRequire } from 'node:module'
const worktree = process.env.WEB_TYPED_WT
if (!worktree) throw new Error('WEB_TYPED_WT required')
const require = createRequire(`${worktree}/package.json`)
const { ref } = require('vue')
const { useHallTypedDeliberation } = await import(`${worktree}/src/composables/juyiting/useHallTypedDeliberation.js`)
const context = { conversationId: '7', conversationGeneration: '1', taskId: 'task-1', targetAgentId: 'agent-1', assignmentRevision: '4' }
const open = { schemaVersion: 1, conversationId: '7', conversationGeneration: '1', requestId: 'request-1', requestRevision: '1', turnId: 'turn-1', state: 'READY', outcome: { outcomeId: 'outcome-1', taskId: 'task-1', assignmentRevision: '4', assistantMessageId: '101', finalDigest: 'sha256:'+'a'.repeat(64), kind: 'CLARIFY', text: '请补充颜色', clarification: { pendingQuestionId: 'pending-1', state: 'OPEN', stateVersion: '0', question: '请补充颜色', requiredFacts: ['REQUIREMENT_DETAILS'], replyRequestId: null }, proposal: null } }
const storageMap = new Map(); const posts=[]
Object.defineProperty(globalThis, 'crypto', { value: { randomUUID: () => '00000000-0000-4000-8000-000000000123' }, configurable: true })
const lane = useHallTypedDeliberation({ actorScopeKey: ref('owner'), authorizationGeneration: ref(1), getContext: () => context, getContextGeneration: () => 1, getCatalogEntries: () => [], enabled: () => true,
 storage: { getItem: k => storageMap.get(k)||null, setItem: (k,v) => storageMap.set(k,v) },
 chatApi: { get: async () => ({data:{data:structuredClone(open)}}), create: async (path, body) => { posts.push({path,body}); return {data:{data: {schemaVersion:1,intent:body.intent,requestId:'reply-1',userMessageId:'102',turnIds:['turn-reply'],state:'ADMITTED',stateVersion:'0',eventCursor:'901',statusUrl:'/chat/requests/reply-1',typedOutcomeUrl:'/chat/conversations/7/requests/reply-1/typed-outcome',replay:false,pendingQuestionId:body.pendingQuestionId} }} } }
})
const first = await lane.readOne('request-1')
const chosen = lane.choosePending(first)
const selectedBefore = lane.selectedPending.value
await lane.readOne('request-1')
const selectedAfter = lane.selectedPending.value
const submitted = await lane.submit({ content:'请画一只蓝色小鸟。' })
const actualIntent = posts[0]?.body.intent
const preserved = chosen && selectedBefore !== null && selectedAfter !== null && JSON.stringify(selectedBefore) === JSON.stringify(selectedAfter)
const boundCAS = actualIntent === 'CLARIFICATION_REPLY' && posts[0].body.pendingQuestionId === 'pending-1' && posts[0].body.expectedPendingQuestionStateVersion === '0' && posts[0].body.parentOutcomeId === 'outcome-1'
console.log(JSON.stringify({worktree,scope:'actual production composable, no browser or runtime',chosen,selectedBefore,selectedAfter,submitted,actualIntent,posts,checks:{same_open_version_keeps_selected_pending:preserved,submit_preserves_clarification_cas:boundCAS},passed:preserved&&boundCAS},null,2))
lane.dispose(); process.exitCode = preserved && boundCAS ? 0 : 1
