import { writeFileSync } from 'node:fs'
import { measureCodexAppServerBinary, AppServerAdapter, cleanupCodexAppServerSnapshots } from '/home/isp/wsps/cyf/.worktrees/t05-t09-managed-chat-client-20261006/conf/codex-ws-agent/app-server-adapter.mjs'
import { buildTypedDeliberationDeclaration } from '/home/isp/wsps/cyf/.worktrees/t05-t09-managed-chat-client-20261006/conf/codex-ws-agent/juyiting-typed-outcome.mjs'
const profile = { codexBin: '/usr/local/lib/node_modules/@openai/codex/bin/codex.js',
 codexHome: '/home/isp/apps/codex-ws-agent/managed-host/owners/owner-b0gyekQxUFVQdnNwaWNWYWs2OXVCNHdEYUZMZw/agt_510b7fea20564b52bc70b3a08d2c6c4f/hri_74f970e5-c623-4e00-88c0-a39ac0125b45/home',
 appServerSchemaContractId: 'codex-cli-0.160.0', typedDeliberationEnabled: true,
 fastChatEnabled: true, appServerEnabled: true, chatEngine: 'app-server', chatSandbox: 'read-only', chatToolPolicy: 'read-only-constrained' }
let adapter
try {
 const measured = measureCodexAppServerBinary(profile, { snapshotRoot: '/home/isp/wsps/private-maintenance/t05-t09-managed-chat-20261006' })
 adapter = AppServerAdapter.spawn(profile, { cwd: '/home/isp/wsps/private-maintenance/t05-t09-managed-chat-20261006', schemaMeasurement: measured })
 await adapter.verifySpawnedExecutable(); await adapter.initialize()
 const result = { verifiedAt: new Date().toISOString(), binarySchemaMeasurement: measured,
  initialized: Boolean(adapter.readback.initialize), processExecutable: adapter.readback.processExecutable,
  declaration: buildTypedDeliberationDeclaration(profile, adapter), providerTurns: 0 }
 writeFileSync('/home/isp/wsps/cyf/docs/implementation/evidence/t05-t09-business-closure-20261006/native-01600-measured-readiness.json', JSON.stringify(result,null,2)+'\n')
 console.log(JSON.stringify({ initialized: result.initialized, declaration: result.declaration, providerTurns: 0 }))
} finally { if(adapter) await adapter.shutdown({ timeoutMs: 1000 }); cleanupCodexAppServerSnapshots() }
