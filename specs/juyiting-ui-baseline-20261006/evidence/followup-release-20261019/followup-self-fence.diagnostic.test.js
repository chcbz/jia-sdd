import * as discussionContract from '../src/components/juyiting/discussionPanelContract.js'
import { expect } from 'chai'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { createRequire } from 'node:module'
import * as Vue from 'vue'
import { ref } from 'vue'
import { mount } from '@vue/test-utils'
import { useHallConversation as actualHallConversation } from '../src/composables/juyiting/useHallConversation.js'
import { currentChatStreamMock } from './fixtures/current-chat-stream-mock.js'
const useHallConversation = options => actualHallConversation({ ...options, chatApi: currentChatStreamMock(options.chatApi) })
import { compileScript } from '@vue/compiler-sfc'
const require = createRequire(import.meta.url)
const { parse } = require('@vue/compiler-sfc')
const babel = require('@babel/parser')
const source = readFileSync(new URL('../src/components/world/JuyiHall.vue', import.meta.url), 'utf8')
const script = parse(source, { filename: 'JuyiHall.vue' }).descriptor.scriptSetup.content
const program = babel.parse(script, { sourceType: 'module' }).program
const declarations = program.body.flatMap(node => node.declarations || [])
const handler = name => { const node = declarations.find(item => item.id?.name === name); if (!node) throw new Error(`missing ${name}`); return script.slice(node.init.start, node.init.end) }
const option = (callee, name) => {
  let call = declarations.find(item => item.init?.callee?.name === callee)?.init
  if (!call) call = program.body.find(node => node.type === 'ExpressionStatement' && node.expression?.type === 'AssignmentExpression' && node.expression.right?.callee?.name === callee)?.expression.right
  const property = call?.arguments?.[0]?.properties?.find(item => item.key?.name === name)
  if (!property) throw new Error(`missing ${callee}.${name}`)
  return script.slice(property.value.start, property.value.end)
}
const typedReceipt = (requestId = 'request-typed-1', turnId = 'turn-typed-1') => ({ schemaVersion: 3, intent: 'DISCUSSION', requestId, userMessageId: '100', turnIds: [turnId], state: 'ADMITTED', stateVersion: '0', eventCursor: '1', statusUrl: `/chat/requests/${requestId}`, typedOutcomeUrl: `/chat/conversations/7/requests/${requestId}/typed-outcome`, replay: false, pendingQuestionId: null })
const typedRequest = (requestId = 'request-typed-1', turnId = 'turn-typed-1', { state = 'RUNNING', stateVersion = '0', turnState = 'RECEIVED', turnStateVersion = '0', finalMessageId = null } = {}) => ({ requestId, requestRevision: '1', stateVersion, conversationId: '7', conversationGeneration: '1', userMessageId: '100', state, turns: [{ turnId, requestId, requestRevision: '1', stateVersion: turnStateVersion, conversationId: '7', conversationGeneration: '1', targetAgentId: 'agent-1', state: turnState, lastDeltaSeq: '0', finalMessageId }] })
describe('production followup self-fence reproduction', () => {
  it('diagnostic: same-generation receipt must not invalidate its own transcript refresh', async () => {
    const calls = []; const chatContext = ref({ conversationScopeType: 'bounty', conversationScopeKey: 'task:task-1', mode: 'bounty', participantAgentIds: ['agent-1'], targetAgentIds: ['agent-1'], targetAgentId: 'agent-1', taskId: 'task-1' })
    const selectedTask = ref({ id: 'task-1' }); const selectedAgent = ref({ agentId: 'agent-1', name: '吴用' })
    const requestView = typedRequest()
    const conversation = useHallConversation({ apiStore: { authorizationGeneration: 1, token: async () => null }, chatContext, chatMode: ref('bounty'),
      chatApi: { list: async (_path, _body, options) => { calls.push('LIST'); options.onSuccess({ items: [{ id: '7', conversationType: 'juyiting', conversationScopeType: 'bounty', conversationScopeKey: 'task:task-1' }], nextCursor: null, hasMore: false }) },
        getById: async (_path, id, options) => { calls.push(`CONTENT:${id}`); options.onSuccess(([{ id: 'message-user-1', senderType: 'user', content: '请画一只鸟' }])) },
        get: async path => { calls.push(`GET:${path}`); return ((requestView)) },
        create: async () => { calls.push('POST'); throw new Error('must not post') } },
      globalStore: { getJiacn: 'owner', user: {} }, log: { warn: () => {}, error: () => {} }, openPanel: () => {}, outgoingMetadata: ref({}), portraitShortName: agent => agent?.name || '', selectedAgent, selectedTask, showToast: () => {} })
    let stopFence
    try {
      expect(await conversation.loadHallMessages()).to.equal(true)
      const followupTaskFence = ref('task-1'); const apiStore = Vue.reactive({ authorizationGeneration: 1 })
      const hallIdentityScope = ref('owner'); const chatMode = ref('bounty')
      const followupContextGeneration = ref(0)
      const typedDeliberation = { invalidate() {} }
      const invalidateFollowupContext = new Function('followupContextGeneration', 'typedDeliberation', `return (${handler('invalidateFollowupContext')})`)(followupContextGeneration, typedDeliberation)
      const watcher = program.body.find(node => node.type === 'ExpressionStatement' && node.expression?.callee?.name === 'watch' && node.expression.arguments[1]?.name === 'invalidateFollowupContext').expression
      stopFence = new Function('watch', 'followupTaskFence', 'apiStore', 'hallIdentityScope', 'conversationId', 'activeRequest', 'bountyInteractionTargetId', 'chatContext', 'chatMode', 'invalidateFollowupContext', `return (${script.slice(watcher.start, watcher.end)})`)(Vue.watch, followupTaskFence, apiStore, hallIdentityScope, conversation.conversationId, conversation.activeRequest, () => 'agent-1', chatContext, chatMode, invalidateFollowupContext)
      const originalGeneration = followupContextGeneration.value
      const pageAccepted = new Function('adoptTypedDiscussionReceipt', 'bountyRequestCatalog', 'showToast', `return (${option('useHallTypedDeliberation', 'onAccepted')})`)(conversation.adoptTypedDiscussionReceipt, { hint: () => calls.push('HINT') }, text => calls.push(`TOAST:${text}`))
      expect(await pageAccepted({ receipt: typedReceipt(), context: { conversationId: '7', taskId: 'task-1', targetAgentId: 'agent-1', assignmentRevision: '4', conversationGeneration: '1' }, isCurrent: () => followupContextGeneration.value === originalGeneration })).to.equal(true)
      expect(conversation.activeRequest.value).to.include({ requestId: 'request-typed-1', state: 'RUNNING', stateVersion: '0' })
      expect(conversation.activeTurns.value[0]).to.include({ turnId: 'turn-typed-1', state: 'RECEIVED', stateVersion: '0' })
      expect(conversation.messages.value.map(message => message.localId)).to.deep.equal(['message-user-1'])
      expect(calls.filter(call => call === 'POST')).to.deep.equal([])
      expect(calls.filter(call => call === 'GET:/requests/request-typed-1')).to.have.length(1)
      expect(calls.filter(call => call === 'CONTENT:7')).to.have.length(2)
      expect(calls).to.include('HINT')
    } finally { console.log('DIAGNOSTIC_CALLS', JSON.stringify(calls)); stopFence?.(); conversation.disposeHallConversation() }
  })
})
