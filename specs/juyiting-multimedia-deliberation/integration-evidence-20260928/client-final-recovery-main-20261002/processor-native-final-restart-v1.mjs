import test from 'node:test'
import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { chmodSync, lstatSync, mkdirSync, mkdtempSync, readFileSync, symlinkSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { resolve } from 'node:path'
import { deflateSync } from 'node:zlib'
import { canonicalSha256, buildThreadKey, PersistentChatInbox, validateChatDispatch } from '/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/client-inspection-runtime-owner-20261002/conf/codex-ws-agent/chat-runtime.mjs'
import { CODEX_APP_SERVER_SCHEMA_CONTRACTS } from '/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/client-inspection-runtime-owner-20261002/conf/codex-ws-agent/app-server-adapter.mjs'
import {
  BUILTIN_TYPED_INSPECTION_DECODERS, TypedInspectionMaterializer, decodePngInspectionInput, decodeWavInspectionInput,
  recoverTypedInspection, resolveTypedInspectionRequest, runTypedInspection
} from '/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/client-inspection-runtime-owner-20261002/conf/codex-ws-agent/typed-inspection-runtime.mjs'
import { TYPED_INSPECTION_OUTPUT_SCHEMA, validateTypedInspectionOutcome, validateTypedInteractionOutcome } from '/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/client-inspection-runtime-owner-20261002/conf/codex-ws-agent/juyiting-typed-outcome.mjs'

const digest = bytes => createHash('sha256').update(bytes).digest('hex')
const prefixed = value => `sha256:${digest(Buffer.from(value))}`
const contract = CODEX_APP_SERVER_SCHEMA_CONTRACTS['codex-cli-0.159.2']
const ids = {
  tenantId: 'tenant-a', ownerJiacn: 'owner-a', clientId: 'client-a', conversationId: '42', conversationGeneration: '7',
  taskId: 'task-1', requestId: 'request-1', requestRevision: '1', targetAgentId: 'agent-1', turnId: 'turn-1'
}
const discussionFacts = {
  schemaVersion: 1, referenceMode: 'AVAILABLE', supportedOperations: ['GENERATE_IMAGE', 'EDIT_IMAGE'],
  availableSources: [{ sourceRefId: 'source-1', kind: 'TASK_WORKSPACE_FILE', mediaType: 'text' }]
}
const sourceFor = (bytes = Buffer.from('bird\n'), overrides = {}) => ({
  sourceRefId: 'source-1',
  selector: { kind: 'TASK_LINKED_WORKSPACE_VERSION', fileId: 'file-1', version: '2', purpose: 'REFERENCE', assetId: null, assetRevision: null },
  mediaKind: 'text', mimeType: 'text/plain', byteLength: String(bytes.length), sha256: digest(bytes), carrier: 'DIRECT_TEXT',
  carrierContractDigest: prefixed('direct-text-v1'), ...overrides
})
const manifestFor = (source = sourceFor()) => ({
  schemaVersion: 1, purpose: 'INSPECT',
  scope: { tenantId: ids.tenantId, ownerJiacn: ids.ownerJiacn, clientId: ids.clientId, conversationId: ids.conversationId, conversationGeneration: ids.conversationGeneration, taskId: ids.taskId, assignmentRevision: '3', requestId: ids.requestId, requestRevision: ids.requestRevision, targetAgentId: ids.targetAgentId },
  profile: {
    profileId: 'inspection-profile', engineContractId: 'engine-contract-v1', enginePolicyDigest: prefixed('engine'),
    toolPolicyDigest: prefixed('tool'), inputPolicyDigest: prefixed('input')
  }, sources: [source]
})
const markerFor = manifest => ({
  schemaVersion: 1, contract: 'juyiting-typed-inspection-v1', purpose: 'INSPECT', discussionFacts,
  manifest, manifestDigest: canonicalSha256(manifest), authorizationId: `inspection_${'a'.repeat(40)}`
})
const messageFor = (source = sourceFor(), overrides = {}) => {
  const manifest = manifestFor(source); const typedInspection = markerFor(manifest)
  const sourceVector = { conversationGeneration: ids.conversationGeneration, messageHighWatermark: '10', taskRevision: '2', executionRevision: null, bindingVersion: '3', summaryRevision: null }
  const facts = {
    conversation: { id: ids.conversationId, generation: ids.conversationGeneration, scopeType: 'bounty' },
    task: { id: ids.taskId }, targetAgentId: ids.targetAgentId, typedInspection
  }
  const contextHash = canonicalSha256({ sourceVector, facts })
  return validateChatDispatch({
    schemaVersion: 1, messageType: 'chat.message', ...ids, dispatchId: 'dispatch-1', messageId: 'message-1', route: 'INSPECT', content: 'Describe the selected material.',
    contextSnapshotId: 'snapshot-1', contextHash, sourceVector, factsManifest: facts,
    contextSnapshot: { schemaVersion: '1', contextSnapshotId: 'snapshot-1', contextHash, sourceVector, facts },
    ownerJiacn: ids.ownerJiacn, dedupeKey: `${ids.tenantId}:${ids.ownerJiacn}:${ids.clientId}:dispatch-1`,
    dispatchAckType: 'chat.dispatch.ack', ackRequired: true, deliverySemantics: 'AT_LEAST_ONCE_DURABLE_DEDUPE_REQUIRED', ...overrides
  })
}
const profile = {
  profileId: 'runtime-profile', agentId: ids.targetAgentId, typedInspectionEnabled: true,
  appServerSchemaContractId: contract.contractId, chatModel: 'no-paid-call-in-test'
}
const readback = typed => ({
  schemaVersion: 1, measured: true, ...typed.manifest.profile, toolPolicy: 'STRICT_NO_TOOLS', recovery: 'durable-inbox-turn-readback-v1',
  supportedInputs: typed.manifest.sources.map(source => ({ mediaKind: source.mediaKind, mimeType: source.mimeType, carrier: source.carrier, carrierContractDigest: source.carrierContractDigest }))
})
const adapterReadback = () => ({ initialize: {}, schema: { ...contract, schemaContractId: contract.contractId, measured: true }, models: {}, config: {} })
const response = ({ url, bytes, mimeType = 'text/plain', length = String(bytes.length), status = 200, redirected = false }) => ({
  status, redirected, url, headers: { get: name => ({ 'content-type': mimeType, 'content-length': length }[name.toLowerCase()] ?? null) },
  arrayBuffer: async () => bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength)
})



const {AgentMessageProcessor,PersistentCommandInbox,ChatAckOutbox,FairLaneScheduler}=await import('/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/client-inspection-runtime-owner-20261002/conf/codex-ws-agent/agent-client.mjs')
const base='/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/client-inspection-runtime-owner-20261002/conf/codex-ws-agent/'
const sourceHashes=()=>Object.fromEntries(['agent-client.mjs','chat-runtime.mjs','typed-inspection-runtime.mjs','app-server-adapter.mjs'].map(p=>[p,digest(readFileSync(base+p))]))
const before=sourceHashes(), root=mkdtempSync(resolve('/var/tmp/cyf-mmd-client-runtime-main-probes-20261002','processor-restart-'))
chmodSync(root,0o700)
const bytes=Buffer.from('bird\n'), message=messageFor(sourceFor(bytes)), typed=resolveTypedInspectionRequest(profile,message)
let starts=0, reads=0, releases=0, sends=[], rejections=[]
const adapter={closed:false,readback:adapterReadback(),startOrResumeThread:async()=>({threadId:'engine-thread-1',state:'HOT'}),runTurn:async opts=>{starts++;opts.onAccepted({threadId:'engine-thread-1',turnId:'engine-turn-1'});throw Object.assign(Error('SIMULATED_ACCEPTED_RESPONSE_LOSS'),{code:'TURN_ACCEPTANCE_UNKNOWN'})},reconcileTurn:async()=>{reads++;return {status:'TERMINAL',terminalStatus:'completed',turnId:'engine-turn-1',result:{thread:{id:'engine-thread-1'}},turn:{id:'engine-turn-1',status:'completed',items:[{type:'agentMessage',text:JSON.stringify({schemaVersion:2,kind:'ANSWER',text:'Observed bird.',clarification:null,proposal:null})}]}}},interrupt:async()=>{}}
const profileRuntime={releaseAdapter:async()=>{releases++}}
const sendFinal=(_p,_m,content,extra)=>{sends.push({content,extra});return false}
const makeProcessor=()=>{
 const chatInbox=new PersistentChatInbox({rootDir:root,profile})
 const processor=new AgentMessageProcessor({profile,inbox:new PersistentCommandInbox({rootDir:root,profile}),chatInbox,chatAckOutbox:new ChatAckOutbox({rootDir:root,profile}),lanes:new FairLaneScheduler(),runCommand:async()=>assert.fail('no command'),runChat:(m,controls)=>runTypedInspection(profile,m,{adapter,profileRuntime,isolationReadback:readback(typed),materializer:{materialize:async()=>({directory:'/private/probe',sources:[{...sourceFor(bytes),bytes}]})},controls,sendFinal}),recoverChat:(m,record,controls)=>recoverTypedInspection(profile,m,record,{adapter,profileRuntime,isolationReadback:readback(typed),controls,sendFinal}),sendFn:()=>true,onReject:e=>rejections.push(e.code)})
 return {processor,chatInbox}
}
const first=makeProcessor();first.processor.start();await first.processor.handle(message)
for(let n=0;n<100&&sends.length<1;n++)await new Promise(r=>setTimeout(r,10))
await first.processor.waitForIdle();first.processor.stop()
assert.equal(starts,1);assert.equal(reads,1);assert.equal(sends.length,1);assert.equal(first.chatInbox.listRecovery().length,1)
const prepared=first.chatInbox.listRecovery()[0].record.finalPrepared
assert.ok(prepared);assert.equal(prepared.content,'Observed bird.')
const second=makeProcessor();second.processor.start()
for(let n=0;n<100&&sends.length<2;n++)await new Promise(r=>setTimeout(r,10))
await second.processor.waitForIdle();second.processor.stop()
assert.equal(starts,1);assert.equal(reads,1);assert.equal(sends.length,2);assert.deepEqual(sends[0],sends[1]);assert.deepEqual(before,sourceHashes())
console.log(JSON.stringify({scope:'actual processor/runtime/inbox; disk reload; fake native adapter and WS; no provider or server ACK',sourceHashes:before,sourceUnchanged:true,starts,readbacks:reads,releases,identicalReplay:true,sends:sends.length,preparedDigest:prepared.finalDigest,recoveryRecords:second.chatInbox.listRecovery().length,rejections,status:'PASS_UNCONFIRMED_NOT_PRODUCT_ACCEPTANCE'},null,2))
