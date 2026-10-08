import { readFileSync, writeFileSync } from 'node:fs'
import { createRequire } from 'node:module'
import { ref, reactive, watch, nextTick } from '/home/isp/wsps/cyf/web/node_modules/vue/dist/vue.runtime.esm-bundler.js'
import { useHallPointAndStartControlledBridge } from './immutable-02a116c/src/composables/juyiting/useHallPointAndStartControlledBridge.js'
import { useHallPointAndStart } from './immutable-02a116c/src/composables/juyiting/useHallPointAndStart.js'
import { createPointAndStartIntentStore } from './immutable-02a116c/src/composables/juyiting/hallPointAndStartIntent.js'
import { pointAndStartRecoveryLane } from './immutable-02a116c/src/composables/juyiting/hallPointAndStartRecoveryLane.js'
import { computed } from '/home/isp/wsps/cyf/web/node_modules/vue/dist/vue.runtime.esm-bundler.js'
import { providerConsentAcknowledgement } from './immutable-02a116c/src/composables/juyiting/hallPointAndStartProviderConsent.js'
const require = createRequire('/home/isp/wsps/cyf/web/package.json'); const { parse } = require('@vue/compiler-sfc'); const babel = require('@babel/parser')
const { descriptor } = parse(readFileSync(new URL('./immutable-02a116c/src/components/world/JuyiHall.vue', import.meta.url), 'utf8')); const script = descriptor.scriptSetup.content
const ast = babel.parse(script, { sourceType: 'module' }); const declarations = ast.program.body.flatMap(node => node.declarations || [])
const declaration = name => { const node = declarations.find(node => node.id.name === name); const parent = ast.program.body.find(nodeParent => nodeParent.declarations?.includes(node)); if (!node || !parent) throw Error(name); return parent.kind + ' ' + script.slice(node.start, node.end) }
const expression = name => { const node = declarations.find(node => node.id.name === name); if (!node) throw Error(name); return script.slice(node.init.start, node.init.end) }
const boundNode = declarations.find(node => node.init?.callee?.name === 'useHallPointAndStartControlledBridge').init.arguments[0].properties.find(node => node.key.name === 'onBound').value
const boundExpression = script.slice(boundNode.start, boundNode.end)
const watchers = ast.program.body.filter(node => node.type === 'ExpressionStatement' && node.expression?.callee?.name === 'watch').map(node => script.slice(node.expression.start, node.expression.end)).filter(code => code.includes('[selectedTask.value?.id, selectedTask.value?.taskVersion') || code.includes('watch([() => apiStore.authorizationGeneration, hallIdentityScope, () => selectedAgent.value?.agentId]'))
if (watchers.length !== 2) throw Error('actual lifecycle watch expressions missing')
const make = (expression, deps) => new Function(...Object.keys(deps), 'return (' + expression + ')')(...Object.values(deps))
const fixture = JSON.parse(readFileSync(new URL('./immutable-02a116c/tests/fixtures/controlled-image-bridge-v1.json', import.meta.url))); const copy = value => JSON.parse(JSON.stringify(value))
const tid = 'task_fixture_1'; const agentId = 'agent_fixture_1'
const preparing = { schemaVersion: 1, taskId: tid, targetAgentId: agentId, requirementRevision: '3', assignmentRevision: '7', taskVersion: '7', grantId: 'grant_fixture_1', grantVersion: '1', grantState: 'ACTIVE', permittedOperations: ['GENERATE_IMAGE'], inputs: [], bootstrapId: 'bootstrap_fixture_1', bootstrapState: 'PENDING', stateVersion: '1', initialOperation: 'GENERATE_IMAGE', conversationId: null, initialRequestId: null, currentAssignment: true }
const admitted = { ...preparing, bootstrapState: 'ADMITTED', stateVersion: '2', conversationId: '9007199254740993', initialRequestId: 'initial_fixture_1' }
async function scenario(invalidateWhilePending) {
  const scope = ref('tenant\u0000client\u0000owner'); const values = new Map(); const storage = { getItem: key => values.get(key) ?? null, setItem: (key, value) => values.set(key, value) }; const calls = []; let reads = 0; let adopted = 0; let opened = 0; let entered = 0
  let secondReadyResolve, releaseSecond; const secondReady = new Promise(resolve => { secondReadyResolve = resolve }); const secondValue = new Promise(resolve => { releaseSecond = resolve })
  let adoptedResolve; const adoptedDone = new Promise(resolve => { adoptedResolve = resolve })
  const selectedTask = ref({ id: tid, taskVersion: '6', requirementRevision: '3' }); const selectedAgent = ref({ agentId }); const apiStore = reactive({ authorizationGeneration: 1 }); const tasks = ref([selectedTask.value]); const roster = ref([{ agentId }, { agentId: 'agent_new' }])
  const api = { get: async path => { calls.push(['GET', path]); if (path.endsWith('/requirements/current')) return { data: { taskId: tid, taskVersion: '6', requirementRevision: '3' } }; if (path.endsWith('/assignment-operation')) { reads++; if (reads === 1) return { data: preparing }; secondReadyResolve(); return { data: await secondValue } }; if (path === `/tasks/${tid}`) return { data: reads >= 2 ? { id: tid, taskVersion: '7', status: 'assigned', assignedAgentId: agentId } : { id: tid, taskVersion: '6', status: 'open' } }; throw Error(path) }, create: async path => { calls.push(['POST', path]); return { data: path.endsWith('cost-consents') ? { ...copy(fixture.wire.wrapper_receipt.providerConsent), state: 'ISSUED', version: '1' } : copy(fixture.wire.wrapper_receipt) } } }
  let ordinary, controlled
  const noopFence = { invalidate() {} }
  const factoryDeps = { ref, watch, nextTick, hallIdentityScope: scope, apiStore, selectedTask, selectedAgent, panelDisposed: false, operableRosterAgents: roster, tasks,
    openPanel: () => { opened++; return true }, enterBountyDiscussion: () => { entered++ }, adoptBountyBootstrap: reference => { adopted++; adoptedResolve(reference); return true },
    pointAndStartObservation: noopFence, controlledImageObservation: noopFence, pointAndStartReferenceInputs: noopFence,
    invalidateControlledBridge: () => controlled?.invalidate(), stopPointAndStartObservation: () => ordinary?.stopObservation(), pointAndStartCapability: ref(null), controlledImageCapability: ref(null), controlledConsentOffer: ref(null),
    pointAndStartIntentState: id => createPointAndStartIntentStore({ storage, scope: scope.value, taskId: id }).read(), pointAndStartRecoveryLane, checkControlledBridgeOriginal: taskId => controlled.checkOriginal(taskId), checkPointAndStart: taskId => ordinary.checkOriginal(taskId), pointAndStartState: computed(() => ordinary?.state.value), showToast: () => {}, explainPointAndStartState: () => '' }
  const factoryBody = ['pointAndStartContextGeneration', 'admittedPointAndStartTaskFingerprint', 'pointAndStartTaskFingerprint', 'preserveAdmittedPointAndStartContext', 'clearPointAndStartCapability', 'attachAdmittedPointAndStart', 'checkPointAndStartOriginal'].map(declaration).join(';')
  const page = new Function(...Object.keys(factoryDeps), factoryBody + '; const stops = [' + watchers.join(',') + ']; return { pointAndStartContextGeneration, attachAdmittedPointAndStart, clearPointAndStartCapability, stops }')(...Object.values(factoryDeps))
  ordinary = useHallPointAndStart({ agentApi: api, actorScopeKey: scope, storage, getContextGeneration: () => page.pointAndStartContextGeneration.value, onAdmitted: page.attachAdmittedPointAndStart })
  const onBound = make(boundExpression, { observePointAndStart: ordinary.observeOriginal })
  controlled = useHallPointAndStartControlledBridge({ agentApi: api, actorScopeKey: scope, storage, keys: { createAssignmentKey: () => 'fixture_assignment_key', createIssueKey: () => 'fixture_issue_key' }, onBound })
  const stops = page.stops
  controlled.selectContext({ taskId: tid, targetAgentId: agentId })
  const started = await controlled.start({ task: { id: tid }, agent: { agentId }, requestedOperations: ['GENERATE_IMAGE'], initialOperation: 'GENERATE_IMAGE', providerBinding: { bindingId: 'fixture_binding', bindingEpoch: '1' }, acknowledgement: providerConsentAcknowledgement })
  await secondReady
  const preparingStatus = ordinary.state.value.status; const invalidationGeneration = page.pointAndStartContextGeneration.value
  if (invalidateWhilePending === 'target') selectedAgent.value = { agentId: 'agent_new' }
  if (invalidateWhilePending === 'authorization') apiStore.authorizationGeneration++
  if (invalidateWhilePending === 'revision') selectedTask.value = { ...selectedTask.value, taskVersion: '7', requirementRevision: '4' }
  const idle = new Promise(resolve => { if (!ordinary.busy.value) return resolve(); const stop = watch(ordinary.busy, busy => { if (!busy) { stop(); resolve() } }, { flush: 'sync' }) })
  releaseSecond(admitted); await idle; await nextTick(); await new Promise(resolve => setImmediate(resolve))
  if (!invalidateWhilePending) await adoptedDone
  const result = { scenario: invalidateWhilePending ? invalidateWhilePending + '_switch_while_original_GET_awaited' : 'actual_Page_onBound_PREPARING_to_ADMITTED', started, preparingStatus, invalidationGeneration: page.pointAndStartContextGeneration.value, ordinaryState: ordinary.state.value.status, adopted, opened, entered, selectedAgentId: selectedAgent.value.agentId, calls, expectations: { adopted: invalidateWhilePending ? 0 : 1, bridgePOSTs: 1, legacyAssignPOSTs: 0 } }
  result.actualBridgePOSTs = calls.filter(([method, path]) => method === 'POST' && path.endsWith('controlled-image')).length; result.actualLegacyAssignPOSTs = calls.filter(([method, path]) => method === 'POST' && path.endsWith('/assign')).length
  for (const stop of stops) stop(); controlled.dispose(); ordinary.dispose(); return result
}
const results = []
for (const stale of [false, 'target', 'authorization', 'revision']) results.push(await scenario(stale))
const output = { commit: '02a116cc24c85f008fb30d7c3cbfd29f3cb651fd', tree: '064c1606fa121467c7ade25befb8184dac2f52b2', evidenceScope: 'immutable actual Page onBound/attach/clear/watch expressions + actual Vue and controlled/native composables; actual Page check recovery handler wired in lifecycle watches; unavailable fresh read is distinguished from released old GET; fake HTTP, not full SFC mount/browser', results }
writeFileSync('/var/tmp/cyf-mmd-main-web-bridge-probe/page-bootstrap-02a116c-actual-recovery-findings.json', JSON.stringify(output, null, 2) + '\n'); console.log(JSON.stringify(output, null, 2))
