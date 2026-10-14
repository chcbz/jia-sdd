import { ref } from './temporary-archive/node_modules/vue/index.mjs'
import { useHallTypedDeliberation } from './temporary-archive/src/composables/juyiting/useHallTypedDeliberation.js'

const sha = ch => `sha256:${ch.repeat(64)}`
const context = () => ref({ conversationId: '7', conversationGeneration: '1', taskId: 'task-1', targetAgentId: 'agent-1', assignmentRevision: '4' })
const memoryStore = () => { const map = new Map(); return { getItem: k => map.get(k) || null, setItem: (k, v) => map.set(k, v) } }
const source = { kind: 'TASK_LINKED_WORKSPACE_VERSION', fileId: 'file-1', version: '7', purpose: 'REFERENCE', assetId: null, assetRevision: null }
const answer = requestId => ({
  schemaVersion: 2, contract: 'juyiting-typed-inspection-v1', conversationId: '7', conversationGeneration: '1', requestId, requestRevision: '1', turnId: `turn-${requestId}`, state: 'READY',
  outcome: { outcomeId: `outcome-${requestId}`, taskId: 'task-1', assignmentRevision: '4', assistantMessageId: '101', finalDigest: sha('a'), kind: 'ANSWER', text: '资料已查阅，给出答复。', clarification: null, proposal: null },
  inspection: { authorizationId: `authorization-${requestId}`, manifestDigest: sha('b'), sourceRefIds: ['source-1'], inputSummary: { inputDigest: sha('c'), sources: [{ sourceRefId: 'source-1', sha256: 'd'.repeat(64), byteLength: '12', carrier: 'DIRECT_TEXT', contributionDigest: sha('e') }] } }
})
const proposal = requestId => ({
  schemaVersion: 2, contract: 'juyiting-typed-inspection-v1', conversationId: '7', conversationGeneration: '1', requestId, requestRevision: '1', turnId: `turn-${requestId}`, state: 'READY',
  outcome: { outcomeId: `outcome-${requestId}`, taskId: 'task-1', assignmentRevision: '4', assistantMessageId: '102', finalDigest: sha('f'), kind: 'EXECUTION_PROPOSAL', text: '资料已经查阅，可以生成。', clarification: null,
    proposal: { proposalId: `proposal-${requestId}`, state: 'PROPOSED', stateVersion: '0', operation: 'GENERATE_IMAGE', instruction: '依据已查阅资料生成一张图像', sourceRefIds: ['source-1'], sourceSelectors: [source], parent: null } },
  inspection: { authorizationId: `authorization-${requestId}`, manifestDigest: sha('b'), sourceRefIds: ['source-1'], inputSummary: { inputDigest: sha('c'), sources: [{ sourceRefId: 'source-1', sha256: 'd'.repeat(64), byteLength: '12', carrier: 'DIRECT_TEXT', contributionDigest: sha('e') }] } }
})
const inspectionReceipt = requestId => ({ schemaVersion: 1, intent: 'DISCUSSION', requestId, userMessageId: '100', turnIds: [`turn-${requestId}`], state: 'ADMITTED', stateVersion: '0', eventCursor: '1', statusUrl: `/chat/requests/${requestId}`, typedOutcomeUrl: `/chat/conversations/7/requests/${requestId}/inspection-outcome`, replay: false, pendingQuestionId: null })
const laneFor = ({ chatApi, storage = null, catalog = () => [], onProposal = null }) => {
  const ctx=context()
  return useHallTypedDeliberation({ chatApi, actorScopeKey: ref('owner'), authorizationGeneration: ref(1), getContext: () => ctx.value, getContextGeneration: () => 1, getCatalogEntries: catalog, storage, enabled: () => true, onProposal })
}
const status = (id, expected, actual, trace, details = '') => ({ id, expected, actual, verdict: expected === actual ? 'PASS' : 'FAIL', trace, details })
const results=[]

// 1. Fresh page: no local storage, only the server catalog advertises an INSPECT request.
{
  const calls=[]
  const catalog = () => [{ request: { requestId: 'request-server-inspect' }, step: { kind: 'INSPECT', state: 'RUNNING' } }]
  const lane=laneFor({ storage: null, catalog, chatApi: { get: async path => { calls.push(path); if (path.endsWith('/inspection-outcome')) return { data: { data: answer('request-server-inspect') } }; throw Object.assign(new Error('typed CHAT route absent'), { status: 404 }) } } })
  const refreshResult=await lane.refresh()
  const visible=lane.projections.value.map(p=>({requestId:p.requestId,purpose:p.purpose,state:p.state,outcome:p.outcome?.kind||null}))
  const expectedPath='/conversations/7/requests/request-server-inspect/inspection-outcome'
  results.push(status('fresh-server-catalog-inspect-recovery', expectedPath, calls[0] || null, calls, `refresh=${refreshResult}; displayed=${JSON.stringify(visible)}; storage=null`))
  lane.dispose()
}

// 2. A fully valid READY INSPECT execution proposal is explicitly confirmed.
{
  const calls=[]; const proposalCalls=[]
  const lane=laneFor({ chatApi: { get: async path => { calls.push(path); return { data: { data: proposal('request-ready-inspect') } } } }, onProposal: async payload => { proposalCalls.push(payload); return true } })
  const read=await lane.readOne('request-ready-inspect', undefined, 'INSPECT')
  const confirmed=await lane.confirmProposal(read)
  const actual=JSON.stringify({confirmed,onProposalCalls:proposalCalls.length})
  const expected=JSON.stringify({confirmed:true,onProposalCalls:1})
  results.push(status('ready-inspect-proposal-explicit-confirm', expected, actual, calls, `projectionPurpose=${read?.purpose||null}; callbackPayload=${JSON.stringify(proposalCalls)}`))
  lane.dispose()
}

// 3. An INSPECT submission reaches a valid READY ANSWER; status must no longer say awaiting inspection.
{
  const calls=[]; const storage=memoryStore()
  const lane=laneFor({ storage, chatApi: { create: async (path, body) => { calls.push(['POST',path,body.intent]); return { data: { data: inspectionReceipt('request-ready-answer') } } }, get: async path => { calls.push(['GET',path]); return { data: { data: answer('request-ready-answer') } } } } })
  const submitted=await lane.submit({ content: '请查阅此资料。', sourceSelectors: [source], inspection: true })
  const actual=lane.inspectionStatus.value
  const isAwaiting=/已受理|等待 Agent 查阅|尚未表示已读/.test(actual)
  results.push(status('ready-inspect-answer-status-clears-waiting', false, isAwaiting, calls, `submitted=${submitted}; status=${JSON.stringify(actual)}; cards=${JSON.stringify(lane.cards.value.map(c=>({purpose:c.purpose,kind:c.outcome.kind})))}; projections=${JSON.stringify(lane.projections.value.map(p=>({purpose:p.purpose,state:p.state,kind:p.outcome?.kind||null})) )}`))
  lane.dispose()
}

console.log(JSON.stringify({candidate:{head:'1496f486e361cc4f9515c8840bc459c0adb78e38',tree:'006e7e88d3bacaa3f05e81d5c09e2eaebfd53d9e'},runtime:{node:process.version},results},null,2))
