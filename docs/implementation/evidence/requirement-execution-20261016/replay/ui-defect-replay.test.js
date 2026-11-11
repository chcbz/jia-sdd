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
  editorState = { error, draft, receipt, caseView, executionResults, resultsState, resultsError, created, loadedResults, workspaceCalls }
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


describe('REQUIREMENT-EXECUTION-20261016 observed UI defects (diagnostic, not acceptance)', () => {
  it('reproduces stale QUEUED submit receipt overriding refreshed completed execution', async () => {
    HallDraftEditor = loadEditor()
    const wrapper = mount(HallDraftEditor, { props: { identityScope: 'tenant\u0000client\u0000owner' } })
    editorState.receipt.value = { ref: { sourceType: 'PRIVATE_CASE', sourceId: 'case-1' }, execution: { executionId: 'exec-1', targetAgentId: 'agent-1', state: 'QUEUED' }, task: null, submittedAt: 1 }
    editorState.caseView.value = { caseId: 'case-1', title: 'fixture', executions: [{ revisionNo: '1', execution: { executionId: 'exec-1', targetAgentId: 'agent-1', state: 'OUTPUT_COMMITTED' } }] }
    await Vue.nextTick()
    expect(wrapper.find('.case-receipt strong').text()).to.equal('等待执行')
    expect(wrapper.text()).to.include('已有已归档输出')
    expect(button(wrapper, '查看成果')).to.equal(undefined)
    console.log('OBSERVED_DEFECT: refreshed completed execution remains QUEUED and result action is missing')
    wrapper.unmount()
  })
  it('reproduces completed receipt with contradictory no-output summary', async () => {
    HallDraftEditor = loadEditor()
    const wrapper = mount(HallDraftEditor, { props: { identityScope: 'tenant\u0000client\u0000owner' } })
    editorState.receipt.value = { ref: { sourceType: 'PRIVATE_CASE', sourceId: 'case-1' }, execution: { executionId: 'exec-1', targetAgentId: 'agent-1', state: 'OUTPUT_COMMITTED' }, task: null, submittedAt: 1 }
    editorState.caseView.value = { caseId: 'case-1', title: 'fixture', executions: [{ revisionNo: '1', execution: { executionId: 'exec-1', targetAgentId: 'agent-1', state: 'OUTPUT_COMMITTED' } }] }
    await Vue.nextTick()
    expect(wrapper.find('.case-receipt strong').text()).to.equal('已有已归档输出')
    expect(wrapper.find('.case-receipt').text()).to.include('已受理，尚未取得成果。')
    console.log('OBSERVED_DEFECT: completed header still says no results received')
    wrapper.unmount()
  })
  it('reproduces refresh error hidden on existing receipt page', async () => {
    HallDraftEditor = loadEditor()
    const wrapper = mount(HallDraftEditor, { props: { identityScope: 'tenant\u0000client\u0000owner' } })
    editorState.receipt.value = { ref: { sourceType: 'PRIVATE_CASE', sourceId: 'case-1' }, execution: { executionId: 'exec-1', targetAgentId: 'agent-1', state: 'QUEUED' }, task: null, submittedAt: 1 }
    editorState.error.value = 'fixture-refresh-failed'
    await Vue.nextTick()
    expect(wrapper.text()).not.to.include('fixture-refresh-failed')
    console.log('OBSERVED_DEFECT: receipt refresh failure is not visible')
    wrapper.unmount()
  })
})
