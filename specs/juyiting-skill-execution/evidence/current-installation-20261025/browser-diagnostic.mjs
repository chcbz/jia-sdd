import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import { readFile, writeFile, mkdir, stat, copyFile } from 'node:fs/promises'
import { createReadStream } from 'node:fs'
import { createServer as createHttpServer } from 'node:http'
import { join, resolve, extname, sep } from 'node:path'
import net from 'node:net'
import { pathToFileURL } from 'node:url'
import { setTimeout as delay } from 'node:timers/promises'

const web = '/var/tmp/cyf-skill-current-20261025/web-source'
const repo = '/home/isp/wsps/cyf/web'
const verifyDir = '/var/tmp/cyf-skill-current-20261025'
const out = join(verifyDir, 'browser')
const prototypeRoot = join(repo, 'prototypes/juyiting')
const sourceFiles = [
  'src/components/economy/SkillManagement.vue',
  'src/composables/useSkillMarket.js',
  'src/utils/skillManagementContract.js',
  'src/composables/useHttp.js',
  'tests/helpers/skill-management-components.js',
  'tests/fixtures/skill-management/helpers.js',
  'tests/fixtures/skill-management/management-contract-v1.schema.json',
  'tests/fixtures/skill-management/management-contract-v1.examples.json',
  'tests/fixtures/skill-management/management-contract-v1.behavior.json',
  'tests/fixtures/skill-management/source.json',
  'package.json', 'package-lock.json', 'vite.config.js'
]
const prototypeFiles = ['index.html', 'skill-management.js', 'skill-management.css', 'specs/prototype-spec.md', 'SHA256SUMS.txt'].map(x => join(prototypeRoot, x))
const sha = bytes => createHash('sha256').update(bytes).digest('hex')
const hashFile = async path => sha(await readFile(path))
const snapshots = async () => Object.fromEntries(await Promise.all(sourceFiles.map(async name => [name, await hashFile(join(web, name))])))
await mkdir(out, { recursive: true })
const snapshotRoot = join(out, 'input-snapshot/src')
const frozenFiles = ['components/economy/SkillManagement.vue', 'composables/useSkillMarket.js', 'utils/skillManagementContract.js']
for (const name of frozenFiles) { const destination = join(snapshotRoot, name); await mkdir(join(destination, '..'), { recursive: true }); await copyFile(join(web, 'src', name), destination) }
const pinBefore = await snapshots()
const frozenSha256 = Object.fromEntries(await Promise.all(frozenFiles.map(async name => [name, await hashFile(join(snapshotRoot, name))])))
for (const name of frozenFiles) if (frozenSha256[name] !== pinBefore[`src/${name}`]) throw new Error(`source changed while snapshotting: ${name}`)
const protoBefore = Object.fromEntries(await Promise.all(prototypeFiles.map(async path => [path.slice(prototypeRoot.length + 1), await hashFile(path)])))
const examples = JSON.parse(await readFile(join(web, 'tests/fixtures/skill-management/management-contract-v1.examples.json'), 'utf8'))
const example = name => structuredClone(examples.cases.find(item => item.name === name).value)
const { createRequire: makeRequire } = await import('node:module')
const require = makeRequire(join(web, 'package.json'))
const { createServer } = await import(pathToFileURL(require.resolve('vite')))
const vuePlugin = (await import(pathToFileURL(require.resolve('@vitejs/plugin-vue')))).default
const harnessPath = join(web, 'scripts/juyiting/e13/lib/cdp-harness.mjs')
const chromeBin = '/var/tmp/cyf-skill-management-20261023/implementation/verification/browser-runtime/extracted/chrome-headless-shell-linux64/chrome-headless-shell'
const chromeLauncher = join(out, 'chromium-root-launcher.sh')
await writeFile(chromeLauncher, `#!/bin/sh\nprintf '%s\\n' "$*" > '${join(out, 'chrome-args.log')}'\nexec '${chromeBin}' --no-sandbox "$@" 2>'${join(out, 'chrome-stderr.log')}'\n`, { mode: 0o700 })
process.env.CHROME_PATH = chromeLauncher
process.env.JUYITING_CDP_COMMAND_TIMEOUT_MS = '15000'
const { launchChrome, stopChrome, evaluate, waitForExpression } = await import(pathToFileURL(harnessPath))
const freePort = async () => {
  const server = net.createServer()
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve) })
  const port = server.address().port
  await new Promise(resolve => server.close(resolve))
  return port
}
const debugPort = await freePort()
const vitePort = await freePort()
const runtimeRoot = join(out, 'vite-root')
await mkdir(join(runtimeRoot, 'src'), { recursive: true })
await writeFile(join(runtimeRoot, 'index.html'), '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0;background:#f5f4f0;font:15px/1.65 sans-serif}.diagnostic-shell{padding:12px}.harness-controls{display:flex;gap:8px;flex-wrap:wrap}.harness-controls button{min-height:44px}</style><div id="app"></div><script type="module" src="/src/main.js"></script>')

const escapeJs = value => JSON.stringify(value).replaceAll('<', '\\u003c')
const componentPath = join(snapshotRoot, 'components/economy/SkillManagement.vue')
const virtualEntry = `
import { createApp, h, nextTick, ref } from 'vue'
import SkillManagement from ${escapeJs('/@fs' + componentPath)}
const FIXTURES = ${escapeJs(examples)}
const pick = name => structuredClone(FIXTURES.cases.find(x => x.name === name).value.data)
const scenario = ref('install')
const show = ref(false)
const actorScopeKey = ref('synthetic-owner-stable')
const identityKey = ref('synthetic-identity-a')
const targetAgent = ref({ agentId: 'agt_demo', name: '测试好汉' })
const requests = []
let mutableList
let currentChange
function makeList(which) {
  const list = pick('skill-list')
  list.items = [list.items[0]]
  const row = list.items[0]
  if (which === 'install') {
    row.installed = null; row.skillRevision = '0'; row.upgradeEligibility = 'NOT_APPLICABLE'
    row.desiredEnabled = false; row.admissionEnabled = false; row.runtime.state = 'OFFLINE'
    row.allowedActions = ['VIEW', 'INSTALL']; row.latestChange = null
  } else {
    currentChange = pick('accepted-offline-install')
    currentChange.status = which === 'retry' ? 'FAILED_RETRYABLE' : 'RECOVERY_REQUIRED'
    currentChange.reasonCode = which === 'retry' ? 'PREPARATION_FAILED' : 'RECEIPT_UNKNOWN'
    currentChange.retryAllowed = which === 'retry'
    row.skillRevision = currentChange.skillRevision
    row.latestChange = structuredClone(currentChange)
    row.allowedActions = which === 'retry' ? ['VIEW', 'RETRY'] : ['VIEW', 'RECONCILE']
  }
  list.agentId = 'agt_demo'
  return list
}
function apiFor() {
  return {
    async get(path, _query, options = {}) {
      requests.push({ method: 'GET', path, headers: options.headers || {}, scope: targetAgent.value.agentId })
      if (path.endsWith('/skills')) {
        if (targetAgent.value.agentId !== 'agt_demo') return { agentId: targetAgent.value.agentId, agentVersion: '12', items: [] }
        mutableList ||= makeList(scenario.value)
        return structuredClone(mutableList)
      }
      if (path.endsWith('/skill-changes')) return { agentId: targetAgent.value.agentId, items: currentChange ? [structuredClone(currentChange)] : [] }
      if (path.includes('/skill-changes/')) return structuredClone(currentChange)
      throw new Error('unexpected fixture GET ' + path)
    },
    async post(path, data, options = {}) {
      requests.push({ method: 'POST', path, data: structuredClone(data), headers: options.headers || {}, scope: targetAgent.value.agentId })
      if (path === '/skill-orders/quotes') {
        const quote = pick(data.action === 'INSTALL' ? 'quote-install-response' : 'quote-upgrade-response')
        quote.expiresAt = Date.now() + 60_000
        return quote
      }
      if (path.endsWith('/retry')) {
        currentChange = { ...currentChange, attempt: currentChange.attempt + 1, skillRevision: '2', changeRevision: '2', status: 'WAITING_AGENT', reasonCode: 'AGENT_OFFLINE', retryAllowed: false, target: { ...currentChange.target, skillInstallationId: 'si_retry' }, updatedAt: Date.now() }
        mutableList = makeList('retry'); mutableList.items[0].skillRevision = '2'; mutableList.items[0].latestChange = structuredClone(currentChange); mutableList.items[0].allowedActions = ['VIEW', 'RECONCILE']
        return structuredClone(currentChange)
      }
      if (path.endsWith('/reconcile')) return structuredClone(currentChange)
      if (path.endsWith('/skill-changes')) {
        currentChange = pick('accepted-offline-install')
        currentChange.updatedAt = Date.now()
        mutableList = makeList('install'); mutableList.items[0].latestChange = structuredClone(currentChange); mutableList.items[0].skillRevision = currentChange.skillRevision; mutableList.items[0].allowedActions = ['VIEW', 'RECONCILE']
        return structuredClone(currentChange)
      }
      throw new Error('unexpected fixture POST ' + path)
    }
  }
}
const app = createApp({
  setup() {
    const open = () => { scenario.value = 'install'; mutableList = null; currentChange = null; show.value = true }
    const setScenario = name => { scenario.value = name; mutableList = null; currentChange = null; actorScopeKey.value = 'synthetic-owner-stable'; identityKey.value = 'synthetic-identity-a'; targetAgent.value = { agentId: 'agt_demo', name: '测试好汉' }; show.value = false; nextTick(() => { show.value = true }) }
    const switchIdentity = () => { identityKey.value = 'synthetic-identity-b'; targetAgent.value = { agentId: 'agt_other', name: '另一身份' } }
    window.__SM = { requests, open, setScenario, switchIdentity }
    return () => h('main', { class: 'diagnostic-shell' }, [
      h('div', { class: 'harness-controls' }, [
        h('button', { id: 'open-manager', onClick: open }, '打开管理'),
        h('button', { id: 'scenario-retry', onClick: () => setScenario('retry') }, '测试重试态'),
        h('button', { id: 'scenario-reconcile', onClick: () => setScenario('reconcile') }, '测试核对态'),
        h('button', { id: 'switch-identity', onClick: switchIdentity }, '切换身份')
      ]),
      h(SkillManagement, { key: scenario.value + ':' + targetAgent.value.agentId, show: show.value, targetAgent: targetAgent.value, actorScopeKey: actorScopeKey.value, identityKey: identityKey.value, agentApi: apiFor(), 'onUpdate:show': value => { show.value = value } })
    ])
  }
})
app.mount('#app')
`
await writeFile(join(runtimeRoot, 'src/main.js'), virtualEntry)

let vite, chrome, cdp, staticServer
const checks = []
const screenshots = {}
let stage = 'initialized'
let runtimeEvidence = {}
const viteMessages = []
const browserErrors = []
const cdpEvents = []
const navigationProbes = []
const requestsAt = () => evaluate(cdp, 'window.__SM.requests.slice()')
const check = (name, condition, detail = '') => {
  assert.ok(condition, `${name}${detail ? `: ${detail}` : ''}`)
  checks.push({ name, status: 'PASS', ...(detail ? { detail } : {}) })
}
const capture = async name => {
  const result = await cdp.send('Page.captureScreenshot', { format: 'png', fromSurface: true, captureBeyondViewport: false })
  const bytes = Buffer.from(result.data, 'base64')
  const path = join(out, `${name}.png`)
  await writeFile(path, bytes)
  screenshots[`${name}.png`] = { sha256: sha(bytes), bytes: bytes.length }
}
const click = async selector => {
  const point = await evaluate(cdp, `(() => { const e=document.querySelector(${JSON.stringify(selector)}); if(!e||e.disabled) throw Error('missing/disabled '+${JSON.stringify(selector)}); e.scrollIntoView({block:'center'}); const r=e.getBoundingClientRect(),x=r.x+r.width/2,y=r.y+r.height/2; if(x<0||y<0||x>=innerWidth||y>=innerHeight||!e.contains(document.elementFromPoint(x,y))) throw Error('clipped/covered '+${JSON.stringify(selector)}); return {x,y} })()`)
  await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', ...point, button: 'left', clickCount: 1 })
  await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', ...point, button: 'left', clickCount: 1 })
}
const clickByText = async text => {
  const point = await evaluate(cdp, `(() => {const b=[...document.querySelectorAll('button')].find(x=>x.textContent.trim()===${JSON.stringify(text)}); if(!b||b.disabled) throw Error('button text missing/disabled: '+${JSON.stringify(text)}); b.scrollIntoView({block:'center'}); const r=b.getBoundingClientRect(),x=r.x+r.width/2,y=r.y+r.height/2; if(!b.contains(document.elementFromPoint(x,y))) throw Error('button clipped/covered: '+${JSON.stringify(text)}); return {x,y} })()`)
  await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', ...point, button: 'left', clickCount: 1 })
  await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', ...point, button: 'left', clickCount: 1 })
}
const wait = async expr => waitForExpression(cdp, expr, 15000)
const viewport = async (width, height, label, mobile = width <= 700) => {
  await cdp.send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile })
  await delay(350)
  const dims = await evaluate(cdp, '({iw:innerWidth,ih:innerHeight,sw:document.documentElement.scrollWidth,sh:document.documentElement.scrollHeight,dialog:document.querySelector("dialog.skill-manager")?.getBoundingClientRect().toJSON()||null,open:document.querySelector("dialog.skill-manager")?.open||false})')
  check(`${label}: viewport configured`, dims.iw === width && dims.ih === height, JSON.stringify(dims))
  check(`${label}: no horizontal overflow`, dims.sw <= width, JSON.stringify(dims))
  return dims
}

try {
  stage = 'create-vite-server'
  const plugin = {
    name: 'skill-management-diagnostic-entry',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = new URL(req.url || '/', 'http://127.0.0.1')
        if (url.pathname.startsWith('/prototype/')) {
          const relative = decodeURIComponent(url.pathname.slice('/prototype/'.length) || 'index.html')
          const target = resolve(prototypeRoot, relative)
          if (target !== prototypeRoot && !target.startsWith(prototypeRoot + sep)) { res.statusCode = 403; res.end(); return }
          const file = relative.endsWith('/') ? join(target, 'index.html') : target
          stat(file).then(() => {
            const mime = ({ '.html':'text/html; charset=utf-8', '.js':'text/javascript; charset=utf-8', '.css':'text/css; charset=utf-8', '.svg':'image/svg+xml', '.png':'image/png', '.webp':'image/webp', '.woff2':'font/woff2' })[extname(file)] || 'application/octet-stream'
            res.setHeader('Content-Type', mime)
            createReadStream(file).pipe(res)
          }).catch(next)
          return
        }
        next()
      })
    }
  }
  vite = await createServer({
    configFile: false, envFile: false, root: runtimeRoot, logLevel: 'warn', cacheDir: join(out, 'vite-cache'),
    optimizeDeps: { noDiscovery: true, include: [], entries: [] },
    resolve: { alias: [
      { find: '@/composables/useSkillMarket.js', replacement: join(snapshotRoot, 'composables/useSkillMarket.js') },
      { find: '@/utils/skillManagementContract.js', replacement: join(snapshotRoot, 'utils/skillManagementContract.js') },
      { find: '@', replacement: join(web, 'src') },
      { find: 'vue', replacement: join(web, 'node_modules/vue/dist/vue.esm-bundler.js') }
    ] },
    plugins: [
      { name: 'skill-management-snapshot-relative-imports', enforce: 'pre', resolveId(source, importer) {
        if (!importer || !resolve(importer).startsWith(resolve(snapshotRoot) + sep)) return null
        let rel
        if (source.startsWith('@/')) rel = source.slice(2)
        else if (source.startsWith('.')) rel = resolve(join(importer, '..'), source).slice(resolve(snapshotRoot) .length + 1)
        else return null
        const frozen = join(snapshotRoot, rel)
        return frozenFiles.includes(rel) ? frozen : join(web, 'src', rel)
      } },
      vuePlugin(), plugin
    ],
    server: { host: '127.0.0.1', port: vitePort, strictPort: true, fs: { allow: [runtimeRoot, web, repo, prototypeRoot] } }
  })
  await vite.listen()
  const port = vite.httpServer.address().port
  const preflight = {}
  for (const path of ['/', '/src/main.js', '/@fs' + componentPath]) { const response = await fetch(`http://127.0.0.1:${port}${path}`); const body = await response.text(); preflight[path] = { status: response.status, contentType: response.headers.get('content-type'), bodySha256: sha(body), preview: body.slice(0, 400) }; if (!response.ok) throw new Error(`Vite preflight ${path} returned ${response.status}: ${body.slice(0, 1000)}`) }
  runtimeEvidence = { port, debugPort, preflight }
  stage = 'launch-chromium'
  chrome = await launchChrome({ windowSize: '1440,900', debugPort })
  cdp = chrome.cdp
  await cdp.send('Page.enable')
  await cdp.send('Runtime.enable')
  cdp.on('Page.frameStartedLoading', params => { cdpEvents.push({ phase: stage, method: 'Page.frameStartedLoading', params }); browserErrors.push(`frameStarted:${params.frameId}`) })
  cdp.on('Page.frameNavigated', params => { cdpEvents.push({ phase: stage, method: 'Page.frameNavigated', params }); browserErrors.push(`frameNavigated:${params.frame?.url}`) })
  cdp.on('Network.requestWillBeSent', params => cdpEvents.push({ phase: stage, method: 'Network.requestWillBeSent', params: { url: params.request?.url, requestId: params.requestId, method: params.request?.method } }))
  cdp.on('Network.responseReceived', params => cdpEvents.push({ phase: stage, method: 'Network.responseReceived', params: { url: params.response?.url, status: params.response?.status, requestId: params.requestId } }))
  cdp.on('Network.loadingFailed', params => { cdpEvents.push({ phase: stage, method: 'Network.loadingFailed', params }); browserErrors.push(`networkFailed:${params.errorText}:${params.requestId}`) })
  cdp.on('Runtime.exceptionThrown', params => browserErrors.push(params.exceptionDetails?.text || 'runtime exception'))
  cdp.on('Log.entryAdded', params => { if (params.entry?.level === 'error') browserErrors.push(params.entry.text) })
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false })
  const navigateProbe = async (name, url) => {
    stage = name
    const from = cdpEvents.length
    const navigation = await cdp.send('Page.navigate', { url }).then(value => ({ status: 'ACK', value }), error => ({ status: 'TIMEOUT_OR_ERROR', error: String(error) }))
    await delay(250)
    const page = await evaluate(cdp, '({url:location.href,title:document.title,readyState:document.readyState,text:document.body?.innerText||""})').catch(error => ({ evaluateError: String(error) }))
    const evidence = { name, url, navigation, page, events: cdpEvents.slice(from) }
    navigationProbes.push(evidence)
    return evidence
  }
  const dataProbe = await navigateProbe('probe-data-url', 'data:text/html;charset=utf-8,%3C!doctype%20html%3E%3Ctitle%3Esm-data-probe%3C/title%3E%3Cbody%3Edata%20navigation%20ok%3C/body%3E')
  const dataOk = dataProbe.page?.title === 'sm-data-probe' && dataProbe.page?.text.includes('data navigation ok')
  checks.push({ name: 'data URL navigation probe', status: dataOk ? 'PASS' : 'FAIL', detail: JSON.stringify(dataProbe) })
  staticServer = createHttpServer((_req, res) => { res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'Connection': 'close' }); res.end('<!doctype html><title>sm-static-probe</title><body>loopback static navigation ok</body>') })
  await new Promise((resolve, reject) => { staticServer.once('error', reject); staticServer.listen(0, '127.0.0.1', resolve) })
  const staticPort = staticServer.address().port
  const staticUrl = `http://127.0.0.1:${staticPort}/`
  const staticFetch = await fetch(staticUrl).then(async response => ({ status: response.status, body: await response.text() }))
  runtimeEvidence.staticProbe = { staticPort, staticFetch: { status: staticFetch.status, bodySha256: sha(staticFetch.body) } }
  const staticProbe = await navigateProbe('probe-loopback-static', staticUrl)
  const staticOk = staticFetch.status === 200 && staticProbe.page?.title === 'sm-static-probe' && staticProbe.page?.text.includes('loopback static navigation ok')
  checks.push({ name: 'loopback static navigation probe', status: staticOk ? 'PASS' : 'FAIL', detail: JSON.stringify(staticProbe) })
  if (!dataOk || !staticOk) throw new Error(`navigation layer failed before Vite: data=${dataOk}, loopbackStatic=${staticOk}`)
  const componentProbe = await navigateProbe('probe-vite-component-entry', `http://127.0.0.1:${port}/`)
  const componentNavigationAck = componentProbe.navigation.status === 'ACK'
  runtimeEvidence.viteNavigation = { status: componentProbe.navigation.status, page: componentProbe.page, eventMethods: componentProbe.events.map(item => item.method) }
  checks.push({ name: 'Vite component entry navigation probe', status: componentNavigationAck ? 'PASS' : 'FAIL', detail: JSON.stringify(runtimeEvidence.viteNavigation) })
  if (!componentNavigationAck || !componentProbe.page?.url?.startsWith(`http://127.0.0.1:${port}/`)) throw new Error('Vite navigation did not commit; stopping before component assertions')
  stage = 'assert-component-mounted'
  await wait('Boolean(document.querySelector("#open-manager"))')
  await wait('Boolean(document.querySelector("#open-manager"))')
  await click('#open-manager')
  await wait('Boolean(document.querySelector("dialog.skill-manager[open] [data-skill-row]"))')

  for (const [width, height, label] of [[320, 720, 'web-320'], [390, 844, 'web-390'], [1440, 900, 'web-1440'], [390, 480, 'web-390x480']]) {
    await viewport(width, height, label)
    await capture(label)
    const rect = await evaluate(cdp, 'document.querySelector("dialog.skill-manager").getBoundingClientRect().toJSON()')
    check(`${label}: dialog within viewport`, rect.left >= -1 && rect.right <= width + 1 && rect.top >= -1 && rect.bottom <= height + 1, JSON.stringify(rect))
  }

  // The current fixed prototype is served read-only by this Vite middleware; its query
  // route opens the same management dialog from the offline agent roster.
  await cdp.send('Emulation.setDeviceMetricsOverride', { width: 1440, height: 900, deviceScaleFactor: 1, mobile: false })
  stage = 'navigate-prototype'
  await cdp.send('Page.navigate', { url: `http://127.0.0.1:${port}/prototype/index.html?scenario=skill-management#agents` })
  await wait('Boolean(document.querySelector("dialog.skill-manager[open]"))')
  const protoMetrics = {}
  for (const [width, height, name] of [[320,720,'proto-320'],[390,844,'proto-390'],[1440,900,'proto-1440'],[390,480,'proto-390x480']]) {
    await viewport(width, height, name)
    protoMetrics[name] = await evaluate(cdp, '(() => {const d=document.querySelector("dialog.skill-manager");const r=d.getBoundingClientRect();return {left:r.left,top:r.top,width:r.width,height:r.height,scrollHeight:d.scrollHeight,clientHeight:d.clientHeight,scrollWidth:document.documentElement.scrollWidth,innerWidth}})()')
    await capture(name)
  }
  check('prototype route is offline/synthetic', await evaluate(cdp, 'document.title.includes("离线示例") || document.querySelector(".skill-demo") !== null'), 'prototype only; not product evidence')

  // Open the production component again for interaction checks.
  stage = 'navigate-component-reopen'
  await cdp.send('Page.navigate', { url: `http://127.0.0.1:${port}/` })
  await wait('Boolean(document.querySelector("#open-manager"))')
  await click('#open-manager')
  await wait('Boolean(document.querySelector("dialog.skill-manager[open] [data-skill-row]"))')
  await viewport(390, 480, 'interaction-390x480')
  await clickByText('安装')
  await wait('Boolean(document.querySelector(".skill-inline-panel"))')
  const inputs = await evaluate(cdp, 'document.querySelectorAll(".skill-install-permissions input").length')
  check('install permission controls present', inputs >= 1, String(inputs))
  await capture('web-permissions-390x480')
  await evaluate(cdp, 'document.querySelectorAll(".skill-install-permissions input").forEach(x=>{if(!x.checked){x.checked=true;x.dispatchEvent(new Event("change",{bubbles:true}))}})')
  await clickByText('获取报价')
  await wait('[...document.querySelectorAll("button")].some(x=>x.textContent.trim()==="确认安装")')
  await wait('Boolean(document.querySelector(".skill-install-quote")?.textContent.includes("本次报价"))')
  check('quote request used exact shared fixture operation', (await requestsAt()).some(r => r.method === 'POST' && r.path === '/skill-orders/quotes'), JSON.stringify(await requestsAt()))
  await capture('web-install-quote-390x480')
  await cdp.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 })
  await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 })
  await wait('!document.querySelector(".skill-inline-panel")')
  await clickByText('安装')
  await wait('document.querySelectorAll(".skill-install-permissions input").length > 0')
  check('collapse/reopen retains approved permissions and quote', await evaluate(cdp, 'document.querySelectorAll(".skill-install-permissions input:checked").length>0 && document.querySelector(".skill-install-quote").textContent.includes("本次报价")'))
  await cdp.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 })
  await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Escape', code: 'Escape', windowsVirtualKeyCode: 27 })
  await wait('!document.querySelector(".skill-inline-panel")')

  // Trusted keyboard test: focus/visibility first, then focus last item using exact product filter.
  await cdp.send('Page.bringToFront')
  await cdp.send('Emulation.setFocusEmulationEnabled', { enabled: true })
  const tabResult = await evaluate(cdp, `(() => {const d=document.querySelector('dialog.skill-manager'),a=Array.from(d.querySelectorAll('button:not(:disabled),input:not(:disabled),summary,[tabindex="0"]')).filter(el=>{if(!el.getClientRects().length)return false;for(let p=el.parentElement;p&&p!==d;p=p.parentElement)if(p.matches('details:not([open])')&&!p.querySelector(':scope > summary')?.contains(el))return false;return true});if(a.length<2)return {count:a.length,last:false};a.at(-1).focus();return {count:a.length,last:document.activeElement===a.at(-1),active:document.activeElement?.outerHTML?.slice(0,240),first:a[0]?.outerHTML?.slice(0,240),lastNode:a.at(-1)?.outerHTML?.slice(0,240)}})()`)
  const focusBeforeTab = await evaluate(cdp, '({hasFocus:document.hasFocus(),visibilityState:document.visibilityState,active:document.activeElement?.outerHTML?.slice(0,240)})')
  await evaluate(cdp, `(() => {window.__tabEvents=[];document.addEventListener('keydown',e=>window.__tabEvents.push({key:e.key,isTrusted:e.isTrusted,defaultPrevented:e.defaultPrevented,targetTag:e.target?.tagName,targetText:e.target?.textContent?.trim(),target:e.target?.outerHTML?.slice(0,240),activeAtDocumentBubble:document.activeElement?.outerHTML?.slice(0,240)}),false)})()`)
  await cdp.send('Input.dispatchKeyEvent', { type: 'rawKeyDown', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 })
  await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Tab', code: 'Tab', windowsVirtualKeyCode: 9 })
  const tabAfter = await evaluate(cdp, `(() => {const d=document.querySelector('dialog.skill-manager'),a=Array.from(d.querySelectorAll('button:not(:disabled),input:not(:disabled),summary,[tabindex="0"]')).filter(el=>{if(!el.getClientRects().length)return false;for(let p=el.parentElement;p&&p!==d;p=p.parentElement)if(p.matches('details:not([open])')&&!p.querySelector(':scope > summary')?.contains(el))return false;return true});return {events:window.__tabEvents,active:document.activeElement?.outerHTML?.slice(0,240),first:a[0]?.outerHTML?.slice(0,240),last:a.at(-1)?.outerHTML?.slice(0,240),activeIsFirst:document.activeElement===a[0],targets:a.length}})()`)
  const trustedTabObserved = tabAfter.events?.some(event => event.key === 'Tab' && event.isTrusted)
  const tabHandledAndWrapped = tabResult.last && trustedTabObserved && tabAfter.events.some(event => event.key === 'Tab' && event.defaultPrevented) && tabAfter.activeIsFirst
  checks.push({name:'CDP trusted Tab from last visible target wraps to first',status:!focusBeforeTab.hasFocus || focusBeforeTab.visibilityState !== 'visible' || !tabResult.last ? 'UNTESTED' : tabHandledAndWrapped ? 'PASS' : 'FAIL',detail:JSON.stringify({tabResult,focusBeforeTab,tabAfter,method:'Page.bringToFront + focus emulation before focus; production focusable filter; CDP rawKeyDown/keyUp'})})
  await click('dialog.skill-manager .ui-close')
  await wait('!document.querySelector("dialog.skill-manager[open]")')
  check('close emits dismissal and closes dialog', await evaluate(cdp, '!document.querySelector("dialog.skill-manager").open && document.querySelector("#open-manager")!==null'))

  // Identity switching must clear previous Agent data and close contextual draft.
  await click('#open-manager')
  await wait('Boolean(document.querySelector("dialog.skill-manager[open] [data-skill-row]"))')
  await clickByText('安装')
  await evaluate(cdp, 'document.querySelectorAll(".skill-install-permissions input").forEach(x=>{x.checked=true;x.dispatchEvent(new Event("change",{bubbles:true}))})')
  await evaluate(cdp, 'window.__SM.switchIdentity()')
  await wait('document.querySelector("dialog.skill-manager[open]") && !document.querySelector("[data-skill-row]")')
  check('identity switch clears prior Agent row and draft', await evaluate(cdp, '!document.body.innerText.includes("图片修改") && !document.querySelector(".skill-inline-panel")'))

  // Retry and reconcile are UI/consumer fixture diagnostics only.
  await evaluate(cdp, "window.__SM.setScenario('retry')")
  await wait('Boolean(document.querySelector("dialog.skill-manager[open] [data-skill-row]"))')
  check('retry fixture exposes retryable state', await evaluate(cdp, 'document.body.innerText.includes("准备失败，可重试") || document.body.innerText.includes("核对结果")'))
  await clickByText('查看进度')
  await wait('Boolean(document.querySelector(".skill-inline-panel"))')
  if (await evaluate(cdp, '!![...document.querySelectorAll("button")].find(b=>b.textContent.trim()==="重试原操作")')) {
    await clickByText('重试原操作')
    await wait('window.__SM.requests.some(r=>r.method==="POST"&&r.path.endsWith("/retry"))')
    check('retry uses original skillChange path and one injected request', (await requestsAt()).filter(r => r.method === 'POST' && r.path.endsWith('/retry')).length === 1)
  } else {
    check('retry button is available for fixture', false, 'not rendered')
  }
  await capture('web-retry-390x480')

  await evaluate(cdp, "window.__SM.setScenario('reconcile')")
  await wait('Boolean(document.querySelector("dialog.skill-manager[open] [data-skill-row]"))')
  await clickByText('核对结果')
  await wait('Boolean(document.querySelector(".skill-inline-panel"))')
  await clickByText('查询原操作')
  await wait('window.__SM.requests.some(r=>r.method==="GET"&&r.path.includes("/skill-changes/sc_install"))')
  check('reconcile diagnostic only queries original change', (await requestsAt()).some(r => r.method === 'GET' && r.path.includes('/skill-changes/sc_install')))
  check('reconcile fixture emits no install/provider operation', !(await requestsAt()).some(r => r.path.includes('/package') || r.path.includes('/provider')))
  await capture('web-reconcile-390x480')

  // Prototype dimensions are compared as geometry only; component is a standalone mount.
  const webMetrics = {}
  stage = 'navigate-component-reopen'
  await cdp.send('Page.navigate', { url: `http://127.0.0.1:${port}/` })
  await wait('Boolean(document.querySelector("#open-manager"))')
  await click('#open-manager')
  await wait('Boolean(document.querySelector("dialog.skill-manager[open]"))')
  for (const [width, height, name] of [[320,720,'web-320'],[390,844,'web-390'],[1440,900,'web-1440'],[390,480,'web-390x480']]) {
    await cdp.send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: width <= 700 })
    await delay(150)
    webMetrics[name] = await evaluate(cdp, '(() => {const d=document.querySelector("dialog.skill-manager");const r=d.getBoundingClientRect();return {left:r.left,top:r.top,width:r.width,height:r.height,scrollHeight:d.scrollHeight,clientHeight:d.clientHeight,scrollWidth:document.documentElement.scrollWidth,innerWidth}})()')
  }

  const pinAfter = await snapshots()
  const protoAfter = Object.fromEntries(await Promise.all(prototypeFiles.map(async path => [path.slice(prototypeRoot.length + 1), await hashFile(path)])))
  check('Web inputs unchanged during diagnostic', JSON.stringify(pinBefore) === JSON.stringify(pinAfter), JSON.stringify({ pinBefore, pinAfter }))
  check('prototype inputs unchanged during diagnostic', JSON.stringify(protoBefore) === JSON.stringify(protoAfter))
  const report = {
    status: checks.every(c => c.status === 'PASS') ? 'PASS' : 'FAIL',
    classification: 'Web production-component browser diagnostic with injected agentApi DTO responses; synthetic only; NOT API/DB/Runtime E2E',
    taskId: 'SKILL-MANAGEMENT-API-20261023',
    candidate: { commit: '075c0c28a7cf7410d915dc15ca5eb5ff50ace01d', trackedTree: '752e9bccdf3e2bda5506f28424e6e214e8010518', dirtyDevelopmentSnapshot: false, sourceSha256: pinBefore, frozenMountedSnapshotSha256: frozenSha256 },
    sharedFixtures: {
      schema: await hashFile(join(web, 'tests/fixtures/skill-management/management-contract-v1.schema.json')),
      examples: await hashFile(join(web, 'tests/fixtures/skill-management/management-contract-v1.examples.json')),
      behavior: await hashFile(join(web, 'tests/fixtures/skill-management/management-contract-v1.behavior.json')),
      sourceManifest: await hashFile(join(web, 'tests/fixtures/skill-management/source.json'))
    },
    prototypeSha256: protoBefore,
    runtime: { preflight, node: process.version, chromiumPath: chromeBin, chromiumSha256: await hashFile(chromeBin), launcherSha256: await hashFile(chromeLauncher), vitePort: port, cdpPort: debugPort, harnessSha256: await hashFile(harnessPath) },
    viewportGeometry: { web: webMetrics, prototype: protoMetrics },
    checks, screenshots, navigationProbes, cdpEvents,
    requests: await requestsAt(),
    gaps: ['No real HTTP wire/public envelope or useHttp path in this browser mount; agentApi prop receives DTO fixtures.', 'No authenticated API, DB transactions/ledger, actual Runtime installation/package/journal, Flow run, deploy or online acceptance.', 'Viewport is Chromium emulation, not physical mobile/soft-keyboard device; 390x480 is low-height viewport only.', 'Prototype is an offline synthetic target and is not product acceptance evidence.']
  }
  const reportPath = join(out, 'result.json')
  await writeFile(reportPath, JSON.stringify(report, null, 2) + '\n')
  console.log(JSON.stringify({ status: report.status, checks: checks.length, failures: checks.filter(c => c.status !== 'PASS'), reportPath, screenshots: Object.keys(screenshots), candidateTree: report.candidate.trackedTree, componentSha: pinBefore['src/components/economy/SkillManagement.vue'] }, null, 2))
} catch (error) {
  const report = { status: 'FAIL', classification: 'Web production-component browser diagnostic with synthetic injected agentApi DTO responses; NOT E2E', stage, runtimeEvidence, viteMessages, browserErrors, cdpEvents: cdpEvents.slice(-100), navigationProbes, error: String(error?.stack || error), candidate: { commit: '075c0c28a7cf7410d915dc15ca5eb5ff50ace01d', trackedTree: '752e9bccdf3e2bda5506f28424e6e214e8010518', sourceSha256: pinBefore, frozenMountedSnapshotSha256: frozenSha256 }, checks, screenshots }
  await writeFile(join(out, 'failure.json'), JSON.stringify(report, null, 2) + '\n')
  console.error(JSON.stringify({ status: 'FAIL', error: report.error, reportPath: join(out, 'failure.json') }, null, 2))
  process.exitCode = 1
} finally {
  if (cdp) cdp.close()
  if (chrome) await stopChrome(chrome.chrome, chrome.userDataDir)
  if (vite) await vite.close()
  if (staticServer) await new Promise(resolve => staticServer.close(resolve))
}
