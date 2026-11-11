// Diagnostic only: real installed file bridge, isolated filesystem, synthetic HTTP replies.
// No database, production request, Provider invocation, or production state mutation.
import { WorkspaceFileBridge } from '/home/isp/apps/cyf-agent-runtime-v1/releases/runtime-interface-20261015-1.2.7-6a9d8d3/codex-ws-agent/workspace-file-bridge.mjs'
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs'
import { tmpdir } from 'node:os'
import { join } from 'node:path'
const root = mkdtempSync(join(tmpdir(), 'cyf-requirement-receipt-probe-'))
const command = { taskId: 'fixture_task', runId: 'fixture_run', inputManifest: [], outputManifest: [{ outputId: 'output_1', relativePath: 'outputs/result.txt', contentType: 'text/plain', maxLength: 1024, uploadPath: '/internal/agent/tasks/fixture_task/runs/fixture_run/outputs/output_1/content' }] }
const calls = []
const bridge = new WorkspaceFileBridge({ apiOrigin: 'https://api.example.test', rootDir: root,
  fetchFn: async (url, options) => {
    calls.push({ method: options.method, path: new URL(url).pathname })
    const data = new URL(url).pathname.includes('/output-commits/')
      ? { manifestId: 'WRONG_MANIFEST', state: 'COMMITTED', items: [] }
      : { outputId: 'WRONG_OUTPUT', sha256: 'b'.repeat(64), byteLength: '999', state: 'STAGED' }
    const response = new Response(JSON.stringify({ protocolVersion: 1, requestId: 'fixture', code: 'E0', msg: 'ok', data }),
      { status: 200, headers: { 'Content-Type': 'application/json', 'X-Request-Id': 'fixture' } })
    Object.defineProperty(response, 'url', { value: String(url) })
    return response
  } })
try {
  const run = await bridge.materializeInputs(command, { runtimeAuthHeader: `AgentRuntime rts1_${'f'.repeat(64)}`, runtimeAgentId: 'agent', runtimeInstanceId: 'instance' })
  mkdirSync(join(run.runDirectory, 'outputs'))
  writeFileSync(join(run.runDirectory, 'outputs/result.txt'), 'Synthetic diagnostic output. No model invoked.\n')
  const result = await bridge.uploadOutputsAndCommit(command, { runtimeAuthHeader: `AgentRuntime rts1_${'f'.repeat(64)}`, runtimeAgentId: 'agent', runtimeInstanceId: 'instance' })
  console.log(JSON.stringify({ observedDefect: 'Bridge confirms locally computed manifest despite wrong staged-output and commit receipt', returnedManifestId: result.manifestId, serverManifestId: 'WRONG_MANIFEST', calls, boundary: 'Real installed bridge; synthetic successful envelopes and output, NOT actual delivery success' }, null, 2))
} finally { rmSync(root, { recursive: true }) }
