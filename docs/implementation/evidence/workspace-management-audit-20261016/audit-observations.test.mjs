import { strict as assert } from 'node:assert'
import { readFileSync } from 'node:fs'
import { createRequire } from 'node:module'
const require = createRequire('/home/isp/wsps/cyf/web/package.json')
const { describe, it } = await import(require.resolve('mocha'))
const Vue = await import(require.resolve('vue'))
const { compileScript, parse } = await import(require.resolve('@vue/compiler-sfc'))
const { mount, flushPromises } = await import(require.resolve('@vue/test-utils'))
const { usePersonalWorkspace } = await import('/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspace.js')
const { deliveryTypeText } = await import('/home/isp/wsps/cyf/web/src/utils/executionFormats.js')
const source = readFileSync('/home/isp/wsps/cyf/web/src/components/workspace/PersonalWorkspace.vue', 'utf8')
const hallSource = readFileSync('/home/isp/wsps/cyf/web/src/components/world/JuyiHall.vue', 'utf8')
const { descriptor } = parse(source, { filename: 'PersonalWorkspace.vue' })
let script = compileScript(descriptor, { id: 'personal-workspace-execution-component', inlineTemplate: true }).content
script = script
  .replace(/^import\s+\{([^}]+)\}\s+from\s+['"]vue['"];?\s*$/gm, (_, names) => `var { ${names.replace(/\s+as\s+/g, ': ')} } = Vue`)
  .replace(/^import\s+\{\s*useApiStore\s*\}\s+from\s+['"]@\/stores\/api['"];?\s*$/gm, 'var { useApiStore } = deps')
  .replace(/^import\s+\{\s*useGlobalStore\s*\}\s+from\s+['"]@\/stores\/global['"];?\s*$/gm, 'var { useGlobalStore } = deps')
  .replace(/^import\s+\{\s*savePersonalWorkspaceBlob,\s*usePersonalWorkspace\s*\}\s+from\s+['"]@\/composables\/usePersonalWorkspace['"];?\s*$/gm, 'var { savePersonalWorkspaceBlob, usePersonalWorkspace } = deps')
  .replace(/^import\s+\{\s*usePersonalWorkspaceExecution\s*\}\s+from\s+['"]@\/composables\/usePersonalWorkspaceExecution['"];?\s*$/gm, 'var { usePersonalWorkspaceExecution } = deps')
  .replace(/^import\s+\{\s*deliveryTypeText\s*\}\s+from\s+['"]@\/utils\/executionFormats['"];?\s*$/gm, 'var { deliveryTypeText } = deps')
  .replace('export default', 'return')

const executionMock = () => {
  const receipt = Vue.ref({ executionId: 'exec_1', targetAgentId: 'agent_1', state: 'QUEUED', outputContentMimeType: 'image/png' })
  const pending = Vue.ref(true)
  const execution = {
    agents: Vue.ref([{ agentId: 'agent_1', name: '林冲', status: 'online' }]), rosterState: Vue.ref('ready'), rosterError: Vue.ref(''), selectedAgentId: Vue.ref('agent_1'), selectedAgent: Vue.ref({ agentId: 'agent_1', name: '林冲' }), selectedExecutionAgent: Vue.ref({ agentId: 'agent_1', name: '林冲' }), allowedMimeTypes: Vue.ref(['image/png']), inputMimeTypes: Vue.ref(['text/plain']), capabilityState: Vue.ref('ready'), capabilityError: Vue.ref(''), generationEnabled: Vue.ref(true), execution: Vue.ref({ executionId: 'exec_1', state: 'QUEUED' }), receipt, executionState: Vue.ref('ready'), pending, unresolvedIntent: Vue.ref(null), error: Vue.ref(''), completionNotice: Vue.ref(''), history: Vue.ref([{ executionId: 'exec_old', targetAgentId: 'agent_1', state: 'FAILED', outputContentMimeType: 'image/png', createdAt: 1 }]), historyState: Vue.ref('ready'), historyError: Vue.ref(''), historyNextCursor: Vue.ref(null),
    loadCapabilities: async () => ({ allowedMimeTypes: ['image/png'] }), loadAgents: async () => [], loadHistory: async () => [], recover: async () => [], selectAgent: () => true, create: async () => null, selectHistoryExecution: async () => null, refreshExecution: async () => null, revokeInputs: async () => null, dispose: () => {}
  }
  execution.prepareNewRequest = () => { receipt.value = null; pending.value = false; execution.execution.value = null; execution.executionState.value = 'idle'; return true }
  return execution
}

// These are diagnostic observations of the CURRENT tree, not desired-behavior acceptance.
const file = (id = 'audit-a', extra = {}) => ({ fileId: id, displayName: `${id}.txt`, state: 'ACTIVE', latestVersion: '2', metadataRevision: '1', mediaFamily: 'TEXT', originKind: 'USER_UPLOAD', ...extra })
const version = (id = 'audit-a', value = '2') => ({ fileId: id, version: value, originalFilename: `${id}-v${value}.txt`, contentMimeType: 'text/plain', byteLength: '1024', createdAt: 1 })
const detail = (id = 'audit-a') => ({ file: file(id), latestVersion: version(id), versions: [version(id), version(id, '1')], relations: [], derivation: [] })
const deferred = () => { let resolve; const promise = new Promise(r => { resolve = r }); return { promise, resolve } }
const blobFile = () => { const b = new Blob(['hello'], { type: 'text/plain' }); Object.defineProperty(b, 'name', { value: 'sample.txt' }); return b }
const reply = (o, value, etag) => { o.onSuccess?.(value, { headers: etag ? { etag } : {} }); return value }
const apiFixture = (override = () => undefined) => {
 const calls = []
 return { calls, execute: async o => {
   calls.push(o)
   const custom = override(o); if (custom !== undefined) return await custom
   const id = o.url.match(/\/files\/([^/]+)/)?.[1] || 'audit-a'
   if (o.url.endsWith('/usage')) return { impactRevision: '1', taskReferences: [], activeExecutions: [] }
   if (o.url.endsWith('/preview')) return { state: 'READY', parts: [{ partId: 'content', contentMimeType: 'text/plain' }], partial: false }
   if (o.url.endsWith('/content')) return new Blob(['content'], { type: 'text/plain' })
   if (o.url.endsWith('/files')) return { items: [file()], hasMore: false, nextCursor: null }
   return reply(o, detail(id), `"${id}:1"`)
 } }
}
const mountReal = (api, embedded = true) => {
 const workspace = usePersonalWorkspace({ api })
 const component = new Function('Vue', 'deps', script)(Vue, {
   useApiStore: () => ({ authorizationGeneration: 1, oauthClientId: 'audit-client' }),
   useGlobalStore: () => ({ user: { id: 'audit-owner' } }),
   usePersonalWorkspace: () => workspace, usePersonalWorkspaceExecution: executionMock,
   savePersonalWorkspaceBlob: () => {}, deliveryTypeText
 })
 return { workspace, wrapper: mount(component, { props: { embedded } }) }
}
describe('workspace audit: happy paths with current string-valued wire fixtures', () => {
 it('lists, reads detail, previews and downloads an explicit fixed string version', async () => {
  const api = apiFixture(); const w = usePersonalWorkspace({ api })
  try {
   assert.equal(await w.refresh(), true); assert.equal((await w.select('audit-a')).file.fileId, 'audit-a')
   assert.equal((await w.previewVersion('1')).text, 'content')
   assert.equal((await w.download('1')).filename, 'audit-a-v1.txt')
  } finally { w.dispose() }
 })
 it('uploads and appends with explicit previous version; preserves the confirmed receipt', async () => {
  const api = apiFixture(o => o.method === 'POST' ? reply(o, { file: file(), version: version(), operation: { operationId: 'audit-op', state: 'COMMITTED' } }) : undefined)
  const w = usePersonalWorkspace({ api })
  try {
   assert.ok(await w.upload(blobFile())); assert.ok(await w.appendVersion(blobFile()))
   const posts = api.calls.filter(o => o.method === 'POST'); assert.equal(posts[1].data.get('expectedPreviousVersion'), '2')
   assert.equal(w.lastOperation.value.state, 'COMMITTED')
  } finally { w.dispose() }
 })
 it('renames, trashes and restores when revision preconditions agree', async () => {
  let rev = 1
  const api = apiFixture(o => o.method !== 'GET' ? (() => {
   assert.equal(o.headers['If-Match'], `"audit-a:${rev}"`)
   if (o.url.endsWith('/trash')) assert.equal(o.data.acknowledgeExistingReferences, true)
   rev++; return reply(o, file('audit-a', { metadataRevision: String(rev), state: o.url.endsWith('/trash') ? 'TRASHED' : 'ACTIVE' }), `"audit-a:${rev}"`)
  })() : o.url.endsWith('/usage') ? { impactRevision: String(rev), taskReferences: [], activeExecutions: [] } : undefined)
  const w = usePersonalWorkspace({ api })
  try { await w.select('audit-a'); assert.ok(await w.rename('renamed')); assert.ok(await w.trash(await w.usage())); assert.ok(await w.restore()) } finally { w.dispose() }
 })
})
describe('workspace audit: confirmed defects (passing means bug reproduced, NOT feature passed)', () => {
 it('version dropdown turns wire strings into numbers, breaking preview/download and draft selection', async () => {
  const api = apiFixture(); const { workspace, wrapper } = mountReal(api)
  try {
   await flushPromises(); await wrapper.get('.treasure-file-row button').trigger('click'); await flushPromises()
   assert.equal(workspace.preview.value.kind, 'text')
   await wrapper.get('select').setValue('1'); await flushPromises()
   assert.equal(workspace.preview.value.kind, 'text')
   assert.equal(api.calls.filter(o => o.url.includes('/versions/1/preview')).length, 0)
   const before = api.calls.filter(o => o.url.endsWith('/content')).length
   await wrapper.findAll('button').find(b => b.text() === '下载').trigger('click'); await flushPromises()
   assert.equal(api.calls.filter(o => o.url.endsWith('/content')).length, before)
   await wrapper.findAll('button').find(b => b.text() === '用于新委托').trigger('click')
   assert.equal(wrapper.emitted('start-draft'), undefined)
  } finally { wrapper.unmount() }
 })
 it('late rename response for file A overwrites selected B with mixed A metadata/B versions', async () => {
  const gate = deferred(); const api = apiFixture(o => o.method === 'PATCH' ? gate.promise : undefined)
  const w = usePersonalWorkspace({ api })
  try {
   await w.select('audit-a'); const pending = w.rename('rename-a'); await w.select('audit-b')
   gate.resolve(file('audit-a', { metadataRevision: '2' })); await pending
   assert.equal(w.detail.value.file.fileId, 'audit-a'); assert.equal(w.detail.value.versions[0].fileId, 'audit-b')
  } finally { w.dispose() }
 })
 it('changing list state while loading drops the new request and displays old ACTIVE data under trash filter', async () => {
  const gate = deferred(); const api = apiFixture(o => o.url.endsWith('/files') ? gate.promise : undefined)
  const { wrapper } = mountReal(api)
  try {
   await wrapper.findAll('button').find(b => b.text() === '回收站').trigger('click')
   gate.resolve({ items: [file()], hasMore: false, nextCursor: null }); await flushPromises()
   assert.equal(wrapper.findAll('.treasure-tabs button').find(b => b.text() === '回收站').attributes('aria-pressed'), 'true')
   assert.equal(wrapper.findAll('.treasure-file-row').length, 1)
   assert.equal(api.calls.filter(o => o.url.endsWith('/files')).length, 1)
   assert.equal(api.calls[0].params.state, 'ACTIVE')
  } finally { wrapper.unmount() }
 })
 it('repeating a lost upload response uses a new key and permits two committed files', async () => {
  const committed = new Map()
  const api = apiFixture(o => o.method === 'POST' ? (() => {
   committed.set(o.headers['Idempotency-Key'], file(`upload-${committed.size + 1}`))
   throw new TypeError('synthetic lost response after server commit')
  })() : undefined)
  const w = usePersonalWorkspace({ api })
  try { assert.equal(await w.upload(blobFile()), null); assert.equal(await w.upload(blobFile()), null); assert.equal(committed.size, 2); assert.equal(w.lastOperation.value, null) } finally { w.dispose() }
 })
 it('upload followed by detail GET failure returns success/ready although detail is absent', async () => {
  const api = apiFixture(o => o.method === 'POST' ? { file: file(), version: version(), operation: { operationId: 'audit-op', state: 'COMMITTED' } } : Promise.reject(new Error('synthetic detail unavailable')))
  const w = usePersonalWorkspace({ api })
  try { assert.ok(await w.upload(blobFile())); assert.equal(w.detail.value, null); assert.equal(w.actionState.value, 'ready'); assert.equal(w.error.value, 'synthetic detail unavailable') } finally { w.dispose() }
 })
 it('partial preview text hides the server warning in the actual embedded component', async () => {
  const api = apiFixture(o => o.url.endsWith('/preview') ? { state: 'READY', partial: true, reason: 'AUDIT_PARTIAL_WARNING', parts: [{ partId: 'content', contentMimeType: 'text/plain' }] } : undefined)
  const { workspace, wrapper } = mountReal(api)
  try {
   await flushPromises(); await wrapper.get('.treasure-file-row button').trigger('click'); await flushPromises()
   assert.equal(workspace.preview.value.message, 'AUDIT_PARTIAL_WARNING')
   assert.equal(wrapper.text().includes('AUDIT_PARTIAL_WARNING'), false)
  } finally { wrapper.unmount() }
 })
 it('failure to refresh leaves a prior page cursor available for a new query', async () => {
  let first = true
  const api = apiFixture(o => o.url.endsWith('/files') ? first ? (first = false, { items: [file()], hasMore: true, nextCursor: 'old-query-cursor' }) : Promise.reject(new Error('synthetic failed refresh')) : undefined)
  const w = usePersonalWorkspace({ api })
  try {
   await w.refresh({ q: 'old' }); await w.refresh({ q: 'new' })
   assert.equal(w.nextCursor.value, 'old-query-cursor'); assert.equal(w.listState.value, 'error')
   await w.loadMore({ q: 'new' }); assert.equal(api.calls.at(-1).params.cursor, 'old-query-cursor'); assert.equal(api.calls.at(-1).params.q, 'new')
  } finally { w.dispose() }
 })
 it('the default download/preview argument is a version object and fails validation', async () => {
  const w = usePersonalWorkspace({ api: apiFixture() })
  try { await w.select('audit-a'); assert.equal(await w.download(), null); assert.equal(await w.previewVersion(), null) } finally { w.dispose() }
 })
})

describe('workspace audit: additional contract and presentation observations', () => {
 it('string latestVersion concatenates into v21; string byteLength renders as unknown size', async () => {
  const { wrapper } = mountReal(apiFixture(), false)
  try {
   await flushPromises()
   await wrapper.findAll('.box-actions button').find(b => b.text().includes('资料柜')).trigger('click')
   await wrapper.get('.file-row').trigger('click'); await flushPromises()
   const input = wrapper.get('.version-upload input[type=file]')
   Object.defineProperty(input.element, 'files', { configurable: true, value: [blobFile()] })
   await input.trigger('change')
   assert.match(wrapper.get('.version-upload').text(), /将创建 v21/)
   await wrapper.findAll('.detail-tabs button').find(b => b.text() === '版本与预览').trigger('click')
   assert.match(wrapper.get('.version-row small').text(), /大小未知/)
  } finally { wrapper.unmount() }
 })
 it('weak current ETag makes rename, trash AND restore fail even without a revision change', async () => {
  for (const action of ['rename', 'trash', 'restore']) {
   const api = apiFixture(o => o.method === 'GET' && !o.url.endsWith('/usage') ? reply(o, detail(), 'W/"audit-a:1"') : o.method !== 'GET' ? (() => {
    assert.equal(o.headers['If-Match'], 'W/"audit-a:1"')
    throw Object.assign(new Error('File metadata changed'), { code: 'METADATA_CHANGED', status: 412 })
   })() : undefined)
   const w = usePersonalWorkspace({ api })
   try { await w.select('audit-a'); const result = await w[action](action === 'rename' ? 'new-name' : { impactRevision: '1' }); assert.equal(result, null); assert.match(w.error.value, /文件信息已变化/) } finally { w.dispose() }
  }
 })
 it('usage can refresh impactRevision while retaining stale detail ETag', async () => {
  const api = apiFixture(o => o.url.endsWith('/usage') ? { impactRevision: '2', taskReferences: [{ taskId: 'audit-task' }], activeExecutions: [] } : o.method === 'POST' ? (() => {
    assert.equal(o.data.impactRevision, '2'); assert.equal(o.headers['If-Match'], '"audit-a:1"')
    throw Object.assign(new Error('changed'), { status: 412 })
  })() : undefined)
  const w = usePersonalWorkspace({ api })
  try { await w.select('audit-a'); assert.equal(await w.trash(await w.usage()), null); assert.equal(w.detail.value.etag, '"audit-a:1"') } finally { w.dispose() }
 })
 it('identity switch suppresses late mutation data without exposing old-owner details', async () => {
  const epoch = Vue.ref('owner-a'); const gate = deferred()
  const w = usePersonalWorkspace({ identityEpoch: epoch, api: apiFixture(o => o.method === 'PATCH' ? gate.promise : undefined) })
  try { await w.select('audit-a'); const pending = w.rename('late'); epoch.value = 'owner-b'; gate.resolve(file()); assert.equal(await pending, null); assert.equal(w.detail.value, null); assert.equal(w.error.value, '') } finally { w.dispose() }
 })
 it('multipart browser-file inference supports blank/octet-stream MIME and rejects HTML', async () => {
  for (const type of ['', 'application/octet-stream', 'text/html']) {
   let writes = 0
   const api = apiFixture(o => o.method === 'POST' ? (writes++, { file: file(), version: version(), operation: { operationId: 'audit-upload', state: 'COMMITTED' } }) : undefined)
   const w = usePersonalWorkspace({ api })
   const b = new Blob(['plain text'], { type }); Object.defineProperty(b, 'name', { value: 'plain.txt' })
   try { const result = await w.upload(b); assert.equal(!!result, type !== 'text/html'); assert.equal(writes, type === 'text/html' ? 0 : 1) } finally { w.dispose() }
  }
 })
})

describe('workspace audit: directory, receipts and safety controls', () => {
 it('search/media/state filters and explicit paging preserve fixed fields and deduplicate file IDs', async () => {
  const api = apiFixture(o => o.url.endsWith('/files') ? o.params.cursor ? { items: [file(), file('audit-b')], nextCursor: null, hasMore: false } : { items: [file()], nextCursor: 'audit-page-2', hasMore: true } : undefined)
  const w = usePersonalWorkspace({ api })
  try {
   assert.equal(await w.refresh({ q: 'audit', mediaFamily: 'TEXT', state: 'TRASHED' }), true)
   assert.deepEqual(api.calls[0].params, { q: 'audit', mediaFamily: 'TEXT', state: 'TRASHED' })
   assert.equal(await w.loadMore({ q: 'audit', mediaFamily: 'TEXT', state: 'TRASHED' }), true)
   assert.deepEqual(w.items.value.map(v => v.fileId), ['audit-a', 'audit-b']); assert.equal(w.nextCursor.value, null)
  } finally { w.dispose() }
 })
 it('a later detail selection wins over an earlier in-flight GET', async () => {
  const gate = deferred(); const w = usePersonalWorkspace({ api: apiFixture(o => o.url.endsWith('/audit-a') ? gate.promise : undefined) })
  try { const pending = w.select('audit-a'); await w.select('audit-b'); gate.resolve(detail()); assert.equal(await pending, null); assert.equal(w.detail.value.file.fileId, 'audit-b') } finally { w.dispose() }
 })
 it('known operation IDs can be queried without resubmitting the write', async () => {
  const api = apiFixture(o => o.url.includes('/operations/') ? { operationId: 'audit-operation', state: 'COMMITTED', fileId: 'audit-a', fileVersion: '2' } : undefined)
  const w = usePersonalWorkspace({ api })
  try { assert.equal((await w.operation('audit-operation')).state, 'COMMITTED'); assert.equal(api.calls.length, 1); assert.equal(api.calls[0].method, 'GET') } finally { w.dispose() }
 })
 it('a genuine metadata conflict does not silently retry or mark the operation successful', async () => {
  const api = apiFixture(o => o.method === 'PATCH' ? Promise.reject(Object.assign(new Error('changed'), { status: 412, code: 'METADATA_CHANGED' })) : undefined)
  const w = usePersonalWorkspace({ api })
  try { await w.select('audit-a'); assert.equal(await w.rename('changed'), null); assert.equal(w.actionState.value, 'error'); assert.equal(api.calls.filter(o => o.method === 'PATCH').length, 1); assert.equal(w.detail.value.file.metadataRevision, '1') } finally { w.dispose() }
 })
})
