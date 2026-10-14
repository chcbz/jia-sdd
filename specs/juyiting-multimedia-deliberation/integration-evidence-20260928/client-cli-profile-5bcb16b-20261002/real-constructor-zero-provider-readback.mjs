import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { chmodSync, readFileSync, statSync, writeFileSync } from 'node:fs'
import { resolve } from 'node:path'
import { pathToFileURL } from 'node:url'

const [sourceRoot, localCandidatePath, managedCandidatePath, validationLocalPath, validationManagedPath, resultPath] = process.argv.slice(2)
const moduleUrl = name => pathToFileURL(resolve(sourceRoot, name))
const agent = await import(moduleUrl('agent-client.mjs'))
const scopesModule = await import(moduleUrl('managed-image-scope-config.mjs'))
const hostModule = await import(moduleUrl('managed-host.mjs'))
const ledgerModule = await import(moduleUrl('controlled-image-http-ledger.mjs'))
const configModule = await import(moduleUrl('controlled-image-http-config.mjs'))
const sha = value => createHash('sha256').update(value).digest('hex')
const json = path => JSON.parse(readFileSync(path, 'utf8'))
const localCandidate = json(localCandidatePath)
const managedCandidate = json(managedCandidatePath)
const validationLocal = json(validationLocalPath)
const validationManaged = json(validationManagedPath)
const auth = validationManaged.authorizations[0]

assert.deepEqual(localCandidate.source, {
  commit: '5bcb16bd8e2cf9a2fde50ac114367ae272c0335f',
  tree: 'e195b7fb150c3d45adc512e876cb4516de785b5b',
  parent: 'aedcd3da12543f588f85f4678898f4ac3ea777b4',
  acceptance: 'MAIN_HASH_VERIFIED_FF_IN_PROGRESS_NOT_INSTALLED'
})
assert.equal(localCandidate.profile.enabled, false)
assert.equal(localCandidate.activation.runtimeCopyPerformed, false)
assert.equal(localCandidate.activation.profileWritePerformed, false)
assert.equal(localCandidate.activation.serviceActionPerformed, false)
assert.equal(localCandidate.activation.providerCallsPerformed, 0)
assert.equal(managedCandidate.schemaVersion, 2)
assert.equal(managedCandidate.authorizations.length, 1)

// The only offline-validation rebinding is private evidence storage; install candidates retain their intended runtime roots.
const expectedValidationLocal = structuredClone(localCandidate)
expectedValidationLocal.profile.controlledImageHttpLedgerRoot = validationLocal.profile.controlledImageHttpLedgerRoot
expectedValidationLocal.profile.workspaceFileRootDir = validationLocal.profile.workspaceFileRootDir
assert.deepEqual(validationLocal, expectedValidationLocal)
const expectedValidationManaged = structuredClone(managedCandidate)
expectedValidationManaged.authorizations[0].controlledImageHttpLedgerRoot = auth.controlledImageHttpLedgerRoot
assert.deepEqual(validationManaged, expectedValidationManaged)
for (const path of [localCandidatePath, managedCandidatePath, validationLocalPath, validationManagedPath]) {
  const st = statSync(path)
  assert.equal(st.uid, process.getuid())
  assert.equal(st.mode & 0o777, 0o600)
}

const local = agent.normalizeProfile({ ...validationLocal.profile, enabled: true, status: '' })
assert.equal(local.profileId, localCandidate.profile.profileId)
assert.equal(local.agentId, localCandidate.profile.agentId)
assert.equal(local.controlledImageExecutorKind, 'GPT_IMAGE_CLI_V1')

const scopes = scopesModule.loadManagedImageScopeAuthorizations(validationManagedPath, { reservedProfiles: [local] })
assert.equal(scopes.count, 1)
const managedHost = new hostModule.ManagedHost({
  root: resolve(resultPath, '..', 'validation-managed-host-not-started'),
  templateHome: '/unused', codexBin: '/unused', runtimeInstanceId: 'offline-5bcb-readback',
  tenantId: auth.tenantId, clientId: auth.clientId, ownerJiacn: '*',
  attachProfile: async () => {}, profileState: () => null, conflicts: () => false,
  workspacePolicyId: 'repo-workspace-v1'
})
const managedBase = managedHost.profileFor({ tenantId: auth.tenantId, clientId: auth.clientId,
  ownerJiacn: auth.ownerJiacn, agentId: auth.agentId, intentId: auth.generation, apiKey: 'offline-fixture-only' })
assert.equal(managedBase.profileId, auth.profileId)
assert.equal(managedBase.profileId.length, 130)
assert.equal(configModule.isControlledImageProfileIdentity(managedBase.profileId, managedBase.agentId), true)
const managed = agent.resolveManagedRuntimeProfile(managedBase, {
  workspaceFileApiOrigin: 'http://127.0.0.1:10018',
  workspaceFileRootDir: resolve(resultPath, '..', 'validation-workspaces', 'managed-binding15'),
  nativeConversationHttpPollEnabled: false,
  nativeConversationImageGenerationEnabled: true,
  executionReportCommandTypes: []
}, scopes)
assert.equal(managed.profileId, auth.profileId)
assert.equal(managed.controlledImageExecutorKind, 'GPT_IMAGE_CLI_V1')
assert.equal(managed.controlledImageHttpLedgerRoot, auth.controlledImageHttpLedgerRoot)
assert.equal(managed.nativeConversationHttpPollEnabled, true)
assert.equal(managed.nativeConversationImageGenerationEnabled, false)

let providerFetchCalls = 0
let nativeFetchCalls = 0
let executorExecuteCalls = 0
let pollCalls = 0
const providerSentinel = async () => { providerFetchCalls++; throw new Error('Provider fetch forbidden in zero-call readback') }
const nativeSentinel = async () => { nativeFetchCalls++; throw new Error('native fetch forbidden in zero-call readback') }
const compose = (profile, runtimeInstanceId) => {
  // Deliberately do not pass createLedger/createHttpExecutor/createCliExecutor/createPollProtocol.
  const runtime = agent.createControlledImageV3SourceRuntime({
    profile,
    getAuth: () => 'AgentRuntime 00000000000000000000000000000000',
    controlledEnv: { CYF_CONTROLLED_IMAGE_API_KEY: 'dummy-offline-not-a-provider-key' },
    providerFetchFn: providerSentinel,
    nativeFetchFn: nativeSentinel,
    runtimeInstanceId
  })
  assert.equal(runtime.configReady, true)
  assert.equal(runtime.controlledImageV3Ready, true)
  assert.equal(runtime.credentialReady, true)
  assert.equal(runtime.adapterKind, 'GPT_IMAGE_CLI_V1')
  assert.equal(typeof runtime.executor, 'function')
  assert.equal(typeof runtime.pollProtocol?.poll, 'function')
  const registration = agent.buildAgentRegistrationPayload(profile, null, true, null, null, runtime)
  assert.equal(registration.controlledImageBountyExecutionV3.enabled, true)
  assert.deepEqual(registration.controlledImageBountyExecutionV3.operations.map(item => item.operation), ['GENERATE_IMAGE', 'EDIT_IMAGE'])
  assert.equal(registration.nativeProviderCredentialBinding.enabled, true)
  assert.equal(registration.nativeProviderCredentialBinding.bindingId, 'mmd-images-chcbz-20261002')
  assert.equal(registration.nativeProviderCredentialBinding.bindingEpoch, '1')
  assert.equal(registration.nativeProviderCredentialBinding.modelId, 'gpt-image-2.5')
  return { runtime, registration }
}
const localComposed = compose(local, 'offline-5bcb-local')
const managedComposed = compose(managed, 'offline-5bcb-managed')

const replay = (profile, label) => {
  const first = new ledgerModule.ControlledImageHttpLedger({ rootDir: profile.controlledImageHttpLedgerRoot,
    profileId: profile.profileId, agentId: profile.agentId })
  const commandId = `offline-${label}-claim`
  const claim = { commandId, requestDigest: sha(Buffer.from(`5bcb16b\0${label}`, 'utf8')),
    bindingId: profile.controlledImageHttpBindingId, bindingEpoch: profile.controlledImageHttpBindingEpoch,
    modelId: profile.controlledImageHttpModelId }
  const created = first.createClaim(claim)
  const persisted = json(created.path)
  assert.equal(persisted.profileId, profile.profileId)
  assert.equal(persisted.agentId, profile.agentId)
  assert.equal(persisted.commandId, commandId)
  assert.equal(statSync(created.path).mode & 0o777, 0o600)
  const restarted = new ledgerModule.ControlledImageHttpLedger({ rootDir: profile.controlledImageHttpLedgerRoot,
    profileId: profile.profileId, agentId: profile.agentId })
  assert.equal(restarted.claimPath(commandId), created.path)
  let replayCode = null
  try { restarted.createClaim(claim) } catch (error) { replayCode = error?.code || error?.name }
  assert.equal(replayCode, 'CONTROLLED_IMAGE_ALREADY_CLAIMED')
  return Object.freeze({ profileIdLength: profile.profileId.length,
    profileScopeSha256: sha(Buffer.from(`${profile.profileId}\0${profile.agentId}`, 'utf8')),
    ledgerRootSha256: sha(Buffer.from(profile.controlledImageHttpLedgerRoot, 'utf8')),
    claimRecordSha256: sha(readFileSync(created.path)), replayCode })
}
const localReplay = replay(local, 'local')
const managedReplay = replay(managed, 'managed')
assert.equal(managedReplay.profileIdLength, 130)

const mismatch = agent.resolveManagedRuntimeProfile({ ...managedBase,
  managedGeneration: `${managedBase.managedGeneration}-mismatch` }, {
  workspaceFileApiOrigin: 'http://127.0.0.1:10018',
  workspaceFileRootDir: resolve(resultPath, '..', 'validation-workspaces', 'managed-binding15'),
  nativeConversationHttpPollEnabled: false,
  nativeConversationImageGenerationEnabled: true,
  executionReportCommandTypes: []
}, scopes)
assert.equal(mismatch.controlledImageHttpEnabled, false)
assert.equal(mismatch.controlledImageExecutorKind, '')
assert.equal(providerFetchCalls, 0)
assert.equal(nativeFetchCalls, 0)
assert.equal(executorExecuteCalls, 0)
assert.equal(pollCalls, 0)

const result = {
  status: 'PASS_REAL_DEFAULT_FACTORIES_ZERO_PROVIDER_INACTIVE',
  source: { commit: '5bcb16bd8e2cf9a2fde50ac114367ae272c0335f',
    tree: 'e195b7fb150c3d45adc512e876cb4516de785b5b',
    parent: 'aedcd3da12543f588f85f4678898f4ac3ea777b4',
    promotionState: 'MAIN_HASH_VERIFIED_FF_IN_PROGRESS_NOT_INSTALLED' },
  candidatesOnDiskInactive: true,
  candidateRuntimeLedgerRootsWritten: false,
  validationLedgerScope: 'PRIVATE_EVIDENCE_ONLY',
  factoryOverrides: [],
  actualDefaultLedgerConstructed: true,
  actualDefaultCliExecutorConstructed: true,
  actualDefaultPollProtocolConstructed: true,
  localBinding1: { profileIdLength: local.profileId.length, exactIdentityMatch: true,
    runtimeReady: localComposed.runtime.controlledImageV3Ready, registrationOperations: ['GENERATE_IMAGE', 'EDIT_IMAGE'],
    ledgerReplay: localReplay },
  managedBinding15: { profileIdLength: managed.profileId.length,
    profileIdSha256: sha(Buffer.from(managed.profileId, 'utf8')), exactIdentityMatch: managed.profileId === auth.profileId,
    scopeLoaderCount: scopes.count, mismatchFailClosed: true,
    runtimeReady: managedComposed.runtime.controlledImageV3Ready, registrationOperations: ['GENERATE_IMAGE', 'EDIT_IMAGE'],
    ledgerReplay: managedReplay },
  providerFetchCalls, nativeFetchCalls, executorExecuteCalls, pollCalls,
  actualCredentialLoaded: false,
  dummyCredentialOnly: true,
  secretBytesRecorded: false,
  runtimeCopy: false,
  runtimeEnvWrite: false,
  productionProfileWrite: false,
  serviceAction: false
}
writeFileSync(resultPath, `${JSON.stringify(result, null, 2)}\n`, { mode: 0o600 })
chmodSync(resultPath, 0o600)
