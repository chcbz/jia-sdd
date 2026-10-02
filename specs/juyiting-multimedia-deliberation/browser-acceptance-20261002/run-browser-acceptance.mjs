#!/usr/bin/env node
/**
 * Real-platform acceptance recorder. It never launches a browser, service, model,
 * task, Flow run, or deployment. In execution mode it attaches only to an
 * operator-supplied CDP endpoint and records browser-observed facts.
 */
import { createHash } from 'node:crypto'
import { mkdir, readFile, readdir, stat, writeFile } from 'node:fs/promises'
import { basename, dirname, isAbsolute, join, resolve } from 'node:path'
import { fileURLToPath, pathToFileURL } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const planPath = join(here, 'acceptance-plan.json')
const args = new Set(process.argv.slice(2))
const execute = args.has('--execute')
const primary = args.has('--primary')
const sha256 = bytes => createHash('sha256').update(bytes).digest('hex')
const json = value => JSON.stringify(value, null, 2)
const redact = value => String(value ?? '')
  .replace(/((?:authorization|token|password|secret|cookie)\s*[:=]\s*)[^\s,;]+/gi, '$1[REDACTED]')
  .replace(/(Bearer\s+)[^\s,;]+/gi, '$1[REDACTED]')
const safeUrl = raw => { try { const value = new URL(raw); return `${value.origin}${value.pathname}` } catch { return '[unparseable-url]' } }
const required = (name) => { const value = process.env[name]; if (!value) throw new Error(`BLOCKED_MISSING_${name}`); return value }
const loadJson = async path => JSON.parse(await readFile(path, 'utf8'))
const writeEvidence = async (root, name, value, binary = false) => {
  const path = join(root, name)
  await mkdir(dirname(path), { recursive: true })
  await writeFile(path, binary ? value : json(value))
  return { path, sha256: sha256(binary ? value : Buffer.from(json(value))) }
}
const checkPlan = plan => {
  const expected = [...Array(22)].map((_, i) => `AC${String(i + 1).padStart(2, '0')}`).concat([...Array(12)].map((_, i) => `FD${String(i + 1).padStart(2, '0')}`))
  const ids = plan.cases.map(item => item.id)
  if (ids.length !== 34 || new Set(ids).size !== 34 || expected.some(id => !ids.includes(id))) throw new Error('INVALID_ACCEPTANCE_PLAN_CASE_SET')
  if (plan.cases.some(item => item.status !== 'NOT_RUN')) throw new Error('PLAN_MUST_REMAIN_NOT_RUN')
  return expected
}
const pageTarget = async endpoint => {
  const normalized = endpoint.replace(/\/$/, '')
  const listUrl = normalized.endsWith('/json/list') ? normalized : `${normalized}/json/list`
  const targets = await (await fetch(listUrl)).json()
  const target = targets.find(item => item.type === 'page' && item.webSocketDebuggerUrl)
  if (!target) throw new Error('BLOCKED_NO_PAGE_TARGET_AT_CDP_ENDPOINT')
  return target
}
const importReusableCdp = async () => {
  // The existing Web-owned helper is deliberately injected at runtime. This SDD
  // harness does not copy its launcher and cannot spawn Chromium.
  const modulePath = required('JYT_CDP_HARNESS_MODULE')
  const resolved = isAbsolute(modulePath) ? modulePath : resolve(process.cwd(), modulePath)
  const helper = await import(pathToFileURL(resolved).href)
  for (const key of ['CdpSession', 'captureViewportPng', 'evaluate']) if (typeof helper[key] !== 'function') throw new Error(`BLOCKED_CDP_HELPER_MISSING_${key}`)
  return helper
}
const domSnapshot = async (evaluate) => evaluate(`(() => {
  const visible = e => Boolean(e && e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden');
  const list = selector => [...document.querySelectorAll(selector)].filter(visible).slice(0, 80).map(e => ({
    tag: e.tagName, text: (e.innerText || e.textContent || '').trim().slice(0, 240), aria: e.getAttribute('aria-label'),
    cls: typeof e.className === 'string' ? e.className.slice(0, 200) : '', selector
  }));
  return {
    title: document.title, url: location.href, text: document.body?.innerText?.slice(0, 12000) || '',
    buttons: list('button'), dialogs: list('[role="dialog"]'), images: [...document.images].filter(visible).slice(0,80).map(i => ({
      alt: i.alt, src: i.currentSrc || i.src, naturalWidth: i.naturalWidth, naturalHeight: i.naturalHeight, complete: i.complete
    })), status: list('[aria-live]'), sourceCandidates: {
      hall: list('.hall-stage, .bounty-panel, .bounty-discussion-panel, [aria-label="悬赏议事 v2 状态"]'),
      media: list('.media-asset'), archive: list('.text-selection-archive'), finalization: list('.bounty-finalization')
    }
  };
})()`)
const selectorExpression = selector => `(() => { const e = document.querySelector(${JSON.stringify(selector)}); if (!e || !e.getClientRects().length) return { ok:false, reason:'selector-not-visible' }; e.click(); return { ok:true, tag:e.tagName, text:(e.innerText||e.textContent||'').trim().slice(0,240) }; })()`
const textClickExpression = (text, selector = 'button') => `(() => { const values=[...document.querySelectorAll(${JSON.stringify(selector)})].filter(e=>e.getClientRects().length); const e=values.find(e=>(e.innerText||e.textContent||'').trim()===${JSON.stringify(text)}); if(!e)return {ok:false,reason:'text-not-visible',text:${JSON.stringify(text)}}; e.click(); return {ok:true,tag:e.tagName,text:(e.innerText||e.textContent||'').trim()}; })()`
const fillExpression = (selector, value) => `(() => { const e=document.querySelector(${JSON.stringify(selector)}); if(!e||!e.getClientRects().length)return {ok:false,reason:'selector-not-visible'}; e.focus(); e.value=${JSON.stringify(value)}; e.dispatchEvent(new InputEvent('input',{bubbles:true,inputType:'insertText',data:${JSON.stringify(value)}})); e.dispatchEvent(new Event('change',{bubbles:true})); return {ok:true,tag:e.tagName}; })()`
const proveImage = async evaluate => evaluate(`(() => [...document.images].filter(i => i.getClientRects().length).map(i => ({src:i.currentSrc||i.src,alt:i.alt,naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight,complete:i.complete,decoded:i.complete&&i.naturalWidth>0&&i.naturalHeight>0})) )()`)
const collectResponseIds = async (cdp, responses) => {
  const found = new Map()
  const visit = (value, path = '') => {
    if (Array.isArray(value)) return value.forEach((item, index) => visit(item, `${path}[${index}]`))
    if (!value || typeof value !== 'object') return
    for (const [key, item] of Object.entries(value)) {
      const next = path ? `${path}.${key}` : key
      if (/(?:task|conversation|request|turn|message|part|execution|run|asset|file|delivery|decision|operation)(?:Id|ID)$/i.test(key) && (typeof item === 'string' || typeof item === 'number')) found.set(`${key}:${item}`, { key, value: String(item), path: next })
      visit(item, next)
    }
  }
  for (const response of responses) {
    if (!String(response.mimeType || '').toLowerCase().includes('json')) continue
    try { const body = await cdp.send('Network.getResponseBody', { requestId: response.requestId }); visit(JSON.parse(body.body || 'null')) } catch { /* Not all browser bodies remain available; preserve response metadata. */ }
  }
  return [...found.values()]
}
const collectDownloads = async directory => {
  const entries = await readdir(directory, { withFileTypes: true }).catch(() => [])
  const result = []
  for (const entry of entries) {
    if (!entry.isFile()) continue
    const path = join(directory, entry.name); const bytes = await readFile(path); const info = await stat(path)
    result.push({ name: basename(path), bytes: info.size, sha256: sha256(bytes) })
  }
  return result
}
const runActions = async ({ actions, cdp, evaluate, evidenceRoot, downloads, baseUrl }) => {
  const results = []
  for (const [index, action] of actions.entries()) {
    const name = String(action.name || `${index + 1}`).replace(/[^A-Za-z0-9_.-]/g, '_')
    let result
    if (action.type === 'navigate') {
      const destination = new URL(action.url)
      if (destination.origin !== new URL(baseUrl).origin) throw new Error('BLOCKED_ACTION_NAVIGATION_OUTSIDE_DEPLOYED_ORIGIN')
      result = await cdp.send('Page.navigate', { url: action.url })
    }
    else if (action.type === 'clickSelector') result = await evaluate(selectorExpression(action.selector))
    else if (action.type === 'clickText') result = await evaluate(textClickExpression(action.text, action.selector || 'button'))
    else if (action.type === 'fill') result = await evaluate(fillExpression(action.selector, action.value))
    else if (action.type === 'snapshot') result = await domSnapshot(evaluate)
    else if (action.type === 'imageProof') result = await proveImage(evaluate)
    else if (action.type === 'downloadProof') result = await collectDownloads(downloads)
    else if (action.type === 'checkpoint') result = { operatorCheckpoint: String(action.note || ''), status: 'OBSERVED_NOT_ASSERTED' }
    else throw new Error(`UNSUPPORTED_ACTION_${action.type}`)
    const artifact = await writeEvidence(evidenceRoot, `actions/${String(index + 1).padStart(2, '0')}-${name}.json`, JSON.parse(JSON.stringify(result, (_, v) => typeof v === 'string' ? redact(v) : v)))
    if (action.screenshot) {
      const png = await cdp.__capture(); await writeEvidence(evidenceRoot, `screenshots/${String(index + 1).padStart(2, '0')}-${name}.png`, png, true)
    }
    results.push({ index, type: action.type, name, resultFile: artifact.path, resultSha256: artifact.sha256 })
  }
  return results
}

const plan = await loadJson(planPath)
const ids = checkPlan(plan)
if (!execute) {
  console.log(json({ status: 'PREPARED_NOT_EXECUTED', cases: ids.length, primaryJourney: plan.primaryJourney, note: 'No CDP connection, browser launch, model request, task creation, Flow action, or deployment was performed.' }))
  process.exit(0)
}
if (process.env.JYT_BROWSER_ACCEPTANCE_ALLOW_LIVE !== '1') throw new Error('BLOCKED_LIVE_AUTHORIZATION_GATE')
if (!primary) throw new Error('BLOCKED_EXECUTION_SCOPE_REQUIRE_PRIMARY')
const metadataPath = required('JYT_ACCEPTANCE_METADATA_JSON')
const actionsPath = required('JYT_ACCEPTANCE_ACTIONS_JSON')
const endpoint = required('JYT_BROWSER_CDP_URL')
const baseUrl = required('JYT_ACCEPTANCE_BASE_URL')
const metadata = await loadJson(metadataPath)
for (const key of ['deployedCommit', 'deployedTree', 'flowRun', 'artifactSha256', 'identityLabel', 'effectiveUiFlags']) if (!metadata[key]) throw new Error(`BLOCKED_METADATA_${key}`)
if (metadata.deployedCommit !== plan.sourcePins.webCommit || metadata.deployedTree !== plan.sourcePins.webTree) throw new Error('BLOCKED_DEPLOYED_SOURCE_PIN_MISMATCH')
if (!Array.isArray(metadata.effectiveUiFlags) || plan.sourcePins.uiFlagsRequired.some(flag => !metadata.effectiveUiFlags.includes(flag))) throw new Error('BLOCKED_REQUIRED_UI_FLAGS_NOT_PROVEN')
if (!String(metadata.baseUrl || baseUrl).startsWith('http')) throw new Error('BLOCKED_INVALID_BASE_URL')
const evidenceRoot = resolve(process.env.JYT_ACCEPTANCE_EVIDENCE_DIR || join(process.cwd(), `juyiting-browser-acceptance-${Date.now()}`))
const downloads = join(evidenceRoot, 'downloads')
await mkdir(downloads, { recursive: true })
const actions = await loadJson(actionsPath)
if (!Array.isArray(actions.actions) || actions.actions.length === 0) throw new Error('BLOCKED_NO_OPERATOR_ACTIONS')
if (JSON.stringify(actions).includes('OPERATOR_REPLACE_') || JSON.stringify(actions).includes('DEPLOYED-HOST')) throw new Error('BLOCKED_UNRESOLVED_OPERATOR_ACTION_TEMPLATE')
const { CdpSession, captureViewportPng, evaluate } = await importReusableCdp()
const target = await pageTarget(endpoint)
const cdp = new CdpSession(target.webSocketDebuggerUrl)
const network = []
try {
  await cdp.open(); await cdp.send('Page.enable'); await cdp.send('Runtime.enable'); await cdp.send('Network.enable')
  cdp.on('Network.responseReceived', event => network.push({ at: new Date().toISOString(), requestId: event.requestId, url: safeUrl(event.response?.url), status: event.response?.status, mimeType: event.response?.mimeType, type: event.type }))
  cdp.__capture = () => captureViewportPng(cdp)
  await cdp.send('Browser.setDownloadBehavior', { behavior: 'allow', downloadPath: downloads, eventsEnabled: true }).catch(() => {})
  const initial = await domSnapshot(expression => evaluate(cdp, expression))
  await writeEvidence(evidenceRoot, 'initial-dom.json', JSON.parse(JSON.stringify(initial, (_, v) => typeof v === 'string' ? redact(v) : v)))
  const actionResults = await runActions({ actions: actions.actions, cdp, evaluate: expression => evaluate(cdp, expression), evidenceRoot, downloads, baseUrl })
  const final = await domSnapshot(expression => evaluate(cdp, expression))
  const observedIds = await collectResponseIds(cdp, network)
  const manifest = { status: 'PARTIAL_COMPLETED', executionScope: 'primaryJourneyOnly', sourcePlan: { webCommit: plan.sourcePins.webCommit, webTree: plan.sourcePins.webTree }, metadata: { ...metadata, identityLabel: redact(metadata.identityLabel) }, endpoint: safeUrl(endpoint), baseUrl: safeUrl(baseUrl), actionResults, network: network.map(({ requestId, ...item }) => ({ ...item, url: redact(item.url) })), observedIds, downloads: await collectDownloads(downloads), final: JSON.parse(JSON.stringify(final, (_, v) => typeof v === 'string' ? redact(v) : v)), cases: plan.cases.map(item => ({ id: item.id, status: 'NOT_RUN' })), note: 'This recorder never promotes a case. A responsible operator must correlate the captured real events/IDs/screenshots and set each matrix outcome after review.' }
  await writeEvidence(evidenceRoot, 'manifest.json', manifest)
  console.log(json({ status: manifest.status, evidenceRoot, casesRemainNotRun: 34, downloads: manifest.downloads }))
} finally { cdp.close() }
