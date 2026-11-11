import { validMaterialVersion } from '../src/composables/juyiting/materialVersion.js'
import { expect } from 'chai'
import { after, before, describe, it } from 'mocha'
import { readFileSync } from 'node:fs'
import { compileScript, parse } from '@vue/compiler-sfc'
import { deliveryTypeText } from '../src/utils/executionFormats.js'

let Vue
let mount
let HallDraftEditor
let editorState

const loadEditor = (deps = editorDeps()) => {
  const filename = new URL('../src/components/juyiting/HallDraftEditor.vue', import.meta.url).pathname
  const { descriptor } = parse(readFileSync(filename, 'utf8'), { filename })
  const script = compileScript(descriptor, { id: 'hall-draft-editor-test', inlineTemplate: true }).content
    .replace(/^import\s+\{([^}]+)\}\s+from\s+['"]vue['"];?\s*$/gm, (_line, bindings) => {
      const values = bindings.split(',').map(binding => {
        const [name, alias] = binding.trim().split(/\s+as\s+/)
        return alias ? `${name}: ${alias}` : name
      }).join(', ')
      return `var { ${values} } = Vue`
    })
    .replace(/^import\s+\{[^}]+\}\s+from\s+['"]@\/composables\/usePersonalWorkspace['"];?\s*$/gm, 'var { savePersonalWorkspaceBlob, usePersonalWorkspace } = deps')
    .replace(/^import\s+\{\s*useHallDrafts\s*\}\s+from\s+['"]@\/composables\/juyiting\/useHallDrafts['"];?\s*$/gm, 'var { useHallDrafts } = deps')
    .replace(/^import\s+HallPrivateMark\s+from\s+['"]\.\/HallPrivateMark\.vue['"];?\s*$/gm, 'var HallPrivateMark = { name: \'HallPrivateMark\', props: [\'sourceRef\', \'resultRef\', \'identityScope\', \'identityEpoch\'], template: \'<section class="private-mark-test-slot" />\' }')
    .replace(/^import\s+\{\s*deliveryTypeText\s*\}\s+from\s+['"]@\/utils\/executionFormats['"];?\s*$/gm, 'var { deliveryTypeText } = deps')
    .replace(/^import\s+\{\s*validMaterialVersion\s*\}\s+from\s+['"][^'"]+['"];?\s*$/gm, 'var { validMaterialVersion } = deps')
    .replace('export default', 'return')
  return new Function('Vue', 'deps', script)(Vue, { ...deps, deliveryTypeText, validMaterialVersion })
}

const editorDeps = () => {
  const draft = Vue.ref(null)
  const summaries = Vue.ref([])
  const nextCursor = Vue.ref(null)
  const state = Vue.ref('idle')
  const error = Vue.ref('')
  const reloadRequired = Vue.ref(false)
  const receipt = Vue.ref(null)
  const submissionState = Vue.ref('idle')
  const caseView = Vue.ref(null)
  const submissionRecovery = Vue.ref(null)
  const unresolvedIntent = Vue.ref(null)
  const executionResults = Vue.ref(null)
  const resultsState = Vue.ref('idle')
  const resultsError = Vue.ref('')
  const created = []
  const loadedResults = []
  const workspaceCalls = []
  editorState = { draft, receipt, caseView, executionResults, resultsState, resultsError, created, loadedResults, workspaceCalls }
  return {
    useHallDrafts: () => ({
      capabilityState: Vue.ref('ready'), capabilityError: Vue.ref(''), allowedMimeTypes: Vue.ref(['application/pdf']), generationEnabled: Vue.ref(true), loadCapabilities: async () => true,
      draft, summaries, nextCursor, state, error, reloadRequired, receipt, submissionState, caseView, submissionRecovery, unresolvedIntent, executionResults, resultsState, resultsError,
      create: async fields => {
        created.push(fields)
        draft.value = { draftId: `draft-${created.length}`, revision: '1', state: 'EDITING', editableFields: fields }
        return draft.value
      },
      save: async fields => { draft.value = { ...draft.value, revision: '2', editableFields: fields }; return draft.value },
      list: async () => true, loadMore: async () => false, load: async () => null, discard: async () => null,
      submit: async () => null, reconcileSubmission: async () => null, loadCase: async () => null,
      loadResults: async executionId => {
        loadedResults.push(executionId)
        executionResults.value = {
          executionId, state: 'OUTPUT_COMMITTED', manifestId: 'manifest-1', allowedActions: ['VIEW', 'CREATE_REVISION'],
          items: [
            { outputId: 'output-1', fileId: 'file-1', fileVersion: '2', mime: 'application/pdf', filename: '结案.pdf', byteLength: '12', sha256: 'a'.repeat(64), availability: 'AVAILABLE' },
            { outputId: 'output-2', fileId: 'file-2', fileVersion: '7', mime: 'text/plain', filename: '缺失.txt', byteLength: '3', sha256: 'b'.repeat(64), availability: 'UNAVAILABLE' }
          ]
        }
        resultsState.value = 'ready'
        return executionResults.value
      },
      dispose: () => {}
    }),
    usePersonalWorkspace: () => ({
      loading: Vue.ref(false), error: Vue.ref(''), items: Vue.ref([]), listState: Vue.ref('empty'), detail: Vue.ref(null), preview: Vue.ref(null),
      refresh: async () => true,
      select: async fileId => { workspaceCalls.push(['select', fileId]); return { file: { fileId } } },
      previewVersion: async version => { workspaceCalls.push(['preview', version]); return true },
      download: async version => { workspaceCalls.push(['download', version]); return { blob: {}, filename: '结案.pdf' } },
      dispose: () => {}
    }),
    savePersonalWorkspaceBlob: result => { workspaceCalls.push(['save', result.filename]) }
  }
}

const button = (wrapper, text) => wrapper.findAll('button').find(item => item.text() === text)
const enterConfirm = async wrapper => { const next = button(wrapper, wrapper.text().includes('下一步：确认创建') ? '下一步：确认创建' : '下一步：确认交办'); if (next) { await next.trigger('click'); await new Promise(resolve => setTimeout(resolve, 0)); await Vue.nextTick() } }

before(async () => {
  for (const key of ['SVGElement', 'Element', 'Node']) {
    Object.defineProperty(globalThis, key, { configurable: true, writable: true, value: globalThis.window[key] })
  }
  Vue = await import('vue')
  ;({ mount } = await import('@vue/test-utils'))
  HallDraftEditor = loadEditor()
})
after(() => { document.body.innerHTML = '' })


describe('REQUIREMENT-EXECUTION-20261016 isolated step replay with installed Java DTOs', () => {
  it('clicks draft/material/save/authorize/submit, then reproduces blocked refreshed result', async () => {
    const fixture = JSON.parse(readFileSync(new URL('../../docs/implementation/evidence/requirement-execution-20261016/replay/java-flow-fixture.json', import.meta.url), 'utf8'))
    const { useHallDrafts: actualUseHallDrafts } = await import('../src/composables/juyiting/useHallDrafts.js')
    const calls = []; let complete = false; let key = 0
    const api = { execute: async request => {
      calls.push({ method: request.method, url: request.url, data: request.data, headers: request.headers })
      const path = request.url
      if (path.endsWith('/capabilities')) return structuredClone(fixture.capabilities)
      if (path === '/hall/drafts' && request.method === 'POST') {
        expect(request.data.inputs).to.deep.equal([{ fileId: 'fixture_file', version: '1' }])
        return structuredClone(fixture.draft)
      }
      if (path === '/hall/drafts/fixture_draft' && request.method === 'PUT') return structuredClone(fixture.saved)
      if (path === '/hall/drafts/fixture_draft/submit') return structuredClone(fixture.receipt)
      if (path === '/hall/cases/fixture_case') return structuredClone(complete ? fixture.completed : fixture.queued)
      if (path === '/hall/executions/fixture_execution/results') return structuredClone(fixture.results)
      throw new Error(`Unexpected fixture request ${request.method} ${path}`)
    } }
    const scope = 'fixture-tenant\u0000fixture-client\u0000fixture-owner'
    const model = actualUseHallDrafts({ agentApi: api, identityScope: scope, keyFactory: () => `replay-${++key}` })
    const deps = editorDeps(); const baseWorkspace = deps.usePersonalWorkspace
    deps.useHallDrafts = () => model
    deps.usePersonalWorkspace = () => { const workspace = baseWorkspace(); workspace.items.value = [{ fileId: 'fixture_file', latestVersion: '1', displayName: '合成资料.pdf' }]; return workspace }
    const Component = loadEditor(deps)
    const wrapper = mount(Component, { props: { agents: [{ agentId: 'agent', name: '合成好汉' }], selectedAgent: { agentId: 'agent' }, identityScope: scope } })
    const settle = async () => { await new Promise(resolve => setTimeout(resolve, 0)); await Vue.nextTick() }
    await settle()
    await wrapper.find('input').setValue(fixture.draft.editableFields.title)
    await wrapper.find('textarea').setValue(fixture.draft.editableFields.instruction)
    await wrapper.find('select[aria-label="期望格式"]').setValue('application/pdf')
    await button(wrapper, '添加资料').trigger('click'); await settle()
    await wrapper.find('input[type="checkbox"]').setValue(true)
    await button(wrapper, '使用所选资料').trigger('click'); await settle()
    await wrapper.find('form').trigger('submit'); await settle()
    expect(model.draft.value.draftId).to.equal('fixture_draft')
    await button(wrapper, '下一步：确认交办').trigger('click'); await settle()
    const save = button(wrapper, '保存更改'); if (save) { await save.trigger('click'); await settle() }
    await wrapper.find('input[type="checkbox"]').setValue(true)
    expect(button(wrapper, '确认授权并交办').attributes('disabled')).to.equal(undefined)
    await button(wrapper, '确认授权并交办').trigger('click'); await settle()
    expect(model.receipt.value.execution.executionId).to.equal('fixture_execution')
    expect(wrapper.find('.case-receipt strong').text()).to.equal('等待执行')
    expect(calls.filter(call => call.url.endsWith('/submit'))).to.have.length(1)
    complete = true
    await button(wrapper, '核对进展').trigger('click'); await settle()
    expect(model.caseView.value.executions[0].execution.state).to.equal('OUTPUT_COMMITTED')
    expect(wrapper.find('.case-receipt strong').text()).to.equal('等待执行')
    console.log('STEP_REPLAY: UI save/materials/authorization/one submit works with installed Java DTOs; refreshed complete state is masked by original receipt')
    console.log('BOUNDARY: synthetic API business responses; no live HTTP, DB, Provider, or real PDF generation')
    console.log('REQUEST_SEQUENCE:', JSON.stringify(calls.map(({ method, url }) => ({ method, url }))))
    wrapper.unmount(); model.dispose()
  })
})
