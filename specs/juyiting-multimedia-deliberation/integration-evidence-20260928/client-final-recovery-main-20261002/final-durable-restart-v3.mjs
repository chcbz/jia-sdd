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


const sourcePath = '/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/client-inspection-runtime-owner-20261002/conf/codex-ws-agent/typed-inspection-runtime.mjs'
const sourceHash = digest(readFileSync(sourcePath)), results=[]
for (const mode of ['false','throw','true-unconfirmed']) {
 const root=mkdtempSync(resolve('/var/tmp/cyf-mmd-client-runtime-main-probes-20261002','restart-')); chmodSync(root,0o700)
 const inboxProfile={profileId:profile.profileId,agentId:profile.agentId}
 const inbox=new PersistentChatInbox({rootDir:root,profile:inboxProfile}); inbox.initialize()
 const bytes=Buffer.from('bird\n'), message=messageFor(sourceFor(bytes)), typed=resolveTypedInspectionRequest(profile,message)
 const accepted=await inbox.accept(message), item=inbox.claim(accepted.key)
 let starts=0, releases=0, attempts=[]
 const adapter={closed:false,readback:adapterReadback(),startOrResumeThread:async()=>({threadId:'engine-thread-1',state:'HOT'}),runTurn:async opts=>{starts++;opts.onAccepted({threadId:'engine-thread-1',turnId:'engine-turn-1'});return {threadId:'engine-thread-1',turnId:'engine-turn-1',content:JSON.stringify({schemaVersion:2,kind:'ANSWER',text:'Observed bird.',clarification:null,proposal:null})}},interrupt:async()=>{}}
 const first=await runTypedInspection(profile,message,{adapter,profileRuntime:{releaseAdapter:async()=>{releases++}},isolationReadback:readback(typed),materializer:{materialize:async()=>({directory:'/private/probe',sources:[{...sourceFor(bytes),bytes}]})},controls:{markPrepared:v=>inbox.markPrepared(item,v),markRunning:(_,v)=>inbox.markRunning(item,v),markFinalPrepared:v=>inbox.markFinalPrepared(item,v),markFinalPublication:v=>inbox.markFinalPublication(item,v),isCancelled:()=>false},sendFinal:(_,__,content,extra)=>{attempts.push({content,extra});if(mode==='throw')throw Error('SIMULATED_WS_WRITE_FAILURE');return mode==='true-unconfirmed'}})
 inbox.recoveryRequired(item, first.recoveryReason)
 const restarted=new PersistentChatInbox({rootDir:root,profile:inboxProfile});restarted.initialize()
 const record=restarted.listRecovery()[0]
 const replay=await recoverTypedInspection(profile,message,record.record,{controls:{markFinalPublication:v=>restarted.markFinalPublication(record,v)},sendFinal:(_,__,content,extra)=>{attempts.push({content,extra});return true}})
 assert.equal(starts,1);assert.equal(first.status,'recovery_required');assert.equal(replay.serverPersistence,'unconfirmed');assert.deepEqual(attempts[0],attempts[1]);assert.equal(first.finalDigest,replay.finalDigest)
 results.push({mode,starts,releases,identicalReplay:true,finalDigest:first.finalDigest,firstPublication:first.publicationState,replayedPublication:replay.publicationState,serverPersistence:replay.serverPersistence})
}
assert.equal(sourceHash,digest(readFileSync(sourcePath)))
console.log(JSON.stringify({sourcePath,sourceHash,sourceUnchanged:true,scope:'real disk inbox reload; fake engine and transport; no provider/network; not server ACK acceptance',results},null,2))
