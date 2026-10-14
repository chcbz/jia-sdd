import { createHash } from 'node:crypto'
import { chmodSync, mkdtempSync, readFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { resolve } from 'node:path'
import { AppServerAdapter } from 'file:///home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/client-inspection-runtime-owner-20261002/conf/codex-ws-agent/app-server-adapter.mjs'
import { TypedInspectionProfileRuntime } from 'file:///home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/client-inspection-runtime-owner-20261002/conf/codex-ws-agent/typed-inspection-profile.mjs'

const sha256 = path => createHash('sha256').update(readFileSync(path)).digest('hex')
const rootPath = '/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/client-inspection-runtime-owner-20261002'
const sourceFiles = [
  'conf/codex-ws-agent/typed-inspection-profile.mjs',
  'conf/codex-ws-agent/app-server-adapter.mjs',
  'conf/codex-ws-agent/typed-inspection-network.mjs',
  'conf/codex-ws-agent/chat-runtime.mjs'
]
const sourceHashes = Object.fromEntries(sourceFiles.map(path => [path, sha256(resolve(rootPath, path))]))
const methods = []
let modelReadback = null
const originalRequest = AppServerAdapter.prototype.request
AppServerAdapter.prototype.request = async function (method, params, timeoutMs) {
  methods.push(method)
  if (/^(?:thread|turn)\//.test(method)) throw Object.assign(new Error(`PROHIBITED_PAID_OR_TURN_METHOD:${method}`), { code: 'PROHIBITED_PAID_OR_TURN_METHOD' })
  const result = await originalRequest.call(this, method, params, timeoutMs)
  if (method === 'model/list') modelReadback = result
  return result
}
const root = mkdtempSync(resolve(tmpdir(), 'typed-inspection-exact-native-')); chmodSync(root, 0o700)
const profile = {
  profileId: 'native-exact-nonpaid', agentId: 'native-exact-nonpaid-agent',
  codexBin: '/usr/local/bin/codex', codexHome: '/root/.codex', appServerSchemaContractId: 'codex-cli-0.159.2',
  typedInspectionSupportedInputs: [
    { mediaKind: 'text', mimeType: 'text/plain', carrier: 'DIRECT_TEXT', carrierContractDigest: `sha256:${'1'.repeat(64)}` }
  ],
  typedInspectionProviderNetwork: 'isolated'
}
const runtime = new TypedInspectionProfileRuntime({ profile, materializerRoot: resolve(root, 'inputs'), stateRoot: resolve(root, 'state') })
const safeModel = model => {
  const capabilities = {}
  for (const key of ['inputModalities', 'supportedInputModalities', 'modalities', 'supportsImages', 'supportsAudio', 'supportsVision']) {
    if (Object.hasOwn(model, key) && ['string', 'boolean'].includes(typeof model[key]) || Array.isArray(model[key])) capabilities[key] = model[key]
  }
  return {
    id: String(model.id ?? model.model ?? model.slug ?? ''),
    displayName: String(model.displayName ?? model.name ?? ''),
    keys: Object.keys(model).sort(),
    capabilities
  }
}
try {
  const measurement = await runtime.measure()
  const models = Array.isArray(modelReadback?.data) ? modelReadback.data.map(safeModel) : []
  const result = {
    schemaVersion: 1,
    observedAt: new Date().toISOString(),
    source: {
      commit: 'd082e1c285c1f323d2bca9458c6eca4ce67e9069',
      tree: 'afc199d590fcd2e0c1c1822ca8e9fadce69e180a',
      files: sourceHashes
    },
    execution: {
      paidProviderCallAuthorized: false,
      turnStartAllowed: false,
      requestMethods: methods,
      prohibitedTurnMethodsObserved: methods.filter(method => /^(?:thread|turn)\//.test(method))
    },
    readback: {
      measured: measurement.measured,
      contractReady: measurement.contractReady,
      providerExecutionNetwork: measurement.providerExecutionNetwork,
      nativeAttestationDigest: measurement.nativeAttestationDigest,
      schemaContractId: measurement.nativeProbe.schemaContractId,
      modelCount: measurement.nativeProbe.modelCount,
      mcpCatalogCount: measurement.nativeProbe.mcpCatalogCount,
      modelCatalog: models,
      supportedInputsMeasuredForUnderstanding: [],
      declaration: runtime.declaration()
    },
    conclusion: 'NON_PAID_NATIVE_HANDSHAKE_ONLY_NO_MEDIA_UNDERSTANDING_PROOF'
  }
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`)
} finally {
  AppServerAdapter.prototype.request = originalRequest
  await runtime.dispose().catch(() => {})
  rmSync(root, { recursive: true, force: true })
}
