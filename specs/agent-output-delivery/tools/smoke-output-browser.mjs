// Live output resource-route smoke. No mocked API responses and no model dispatch.
// Input JSON: webRoot, tokenFile, outputDirectory, resourceRoute, title,
// expectedSha256, expectedText (optional). Resource route must use local Vite15173.
import { spawn } from 'node:child_process'
import { createHash } from 'node:crypto'
import { mkdir, mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import { join, resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import { setTimeout as delay } from 'node:timers/promises'
import assert from 'node:assert/strict'

const config = JSON.parse(await readFile(process.argv[2], 'utf8'))
const origin = 'http://127.0.0.1:15173'
const route = new URL(config.resourceRoute)
assert.equal(route.origin, origin)
assert.equal(route.pathname, '/chat')
assert(!route.username && !route.password && !route.hash)
assert.deepEqual([...route.searchParams.keys()].sort(),
  ['outputId', 'outputSourceId', 'outputSourceType', 'outputVersion'].sort())
const sourceType = route.searchParams.get('outputSourceType')
assert(['TASK', 'CONVERSATION'].includes(sourceType))
const part = name => encodeURIComponent(route.searchParams.get(name))
const collection = sourceType === 'TASK'
  ? `/agent/tasks/${part('outputSourceId')}/artifacts`
  : `/chat/conversations/${part('outputSourceId')}/outputs`
const downloadPath = `/api${collection}/${part('outputId')}/versions/${part('outputVersion')}/download`
assert(/^[a-f0-9]{64}$/.test(config.expectedSha256))
assert(typeof config.title === 'string' && config.title.length > 0)
const token = JSON.parse(await readFile(config.tokenFile, 'utf8')).access_token
assert(typeof token === 'string' && token.length > 0)
const { CdpSession, stopChrome } = await import(pathToFileURL(resolve(
  config.webRoot, 'tests/juyiting-public-beta-ui-smoke.mjs')))
const outputDirectory = resolve(config.outputDirectory)
await mkdir(outputDirectory, { recursive: true, mode: 0o700 })
const profile = await mkdtemp(join(tmpdir(), 'od06-output-browser-'))
const abort = new AbortController()
const deadline = Date.now() + 180_000
const guard = {
  signal: abort.signal,
  remainingMs: () => Math.max(0, deadline - Date.now()),
  beforeBoundary: () => {
    if (abort.signal.aborted || Date.now() >= deadline) throw new Error('Browser deadline reached')
  }
}
const timeout = setTimeout(() => abort.abort(), 180_000)
const onSignal = () => abort.abort()
process.on('SIGINT', onSignal)
process.on('SIGTERM', onSignal)
let chrome
let cdp
let step = 'launch'
let succeeded = false
const observations = []
const network = []
const cleanupFailures = []
const poll = async (check, limit = 25_000) => {
  const end = Date.now() + limit
  while (Date.now() < end) {
    guard.beforeBoundary()
    const value = await check()
    if (value) return value
    await delay(250, undefined, { signal: abort.signal })
  }
  throw new Error('Condition timed out')
}
const evaluate = async expression => {
  cdp.throwTerminalErrors()
  const response = await cdp.send('Runtime.evaluate', {
    expression, returnByValue: true, awaitPromise: true
  })
  if (response.exceptionDetails) throw new Error('Browser evaluation failed')
  return response.result?.value
}

try {
  chrome = spawn('/usr/bin/chromium', [
    '--headless=new', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
    '--disable-background-networking', '--disable-component-update', '--disable-sync',
    '--disable-extensions', '--remote-debugging-port=0',
    '--remote-debugging-address=127.0.0.1', `--user-data-dir=${profile}`, 'about:blank'
  ], { stdio: 'ignore', detached: true })
  await new Promise((yes, no) => { chrome.once('spawn', yes); chrome.once('error', no) })
  const port = await poll(async () => {
    try { return Number((await readFile(join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]) }
    catch { return false }
  })
  assert(Number.isInteger(port) && port > 0 && port <= 65535)
  const response = await fetch(`http://127.0.0.1:${port}/json/new?about:blank`, {
    method: 'PUT', signal: abort.signal
  })
  assert(response.ok)
  const target = await response.json()
  const wsUrl = new URL(target.webSocketDebuggerUrl)
  assert.equal(wsUrl.hostname, '127.0.0.1')
  assert.equal(Number(wsUrl.port), port)
  assert.equal(wsUrl.protocol, 'ws:')
  cdp = new CdpSession({ guard, cdpCommandTimeoutMs: 20_000 }, wsUrl, WebSocket)
  await cdp.open()
  await cdp.send('Page.enable')
  await cdp.send('Runtime.enable')
  await cdp.send('Network.enable')
  await cdp.send('Network.setCacheDisabled', { cacheDisabled: true })
  cdp.on('Fetch.requestPaused', async ({ requestId, request }) => {
    const url = new URL(request.url)
    const allowed = url.origin === origin || url.protocol === 'data:' ||
      (url.protocol === 'blob:' && url.origin === origin)
    if (!allowed) {
      await cdp.send('Fetch.failRequest', { requestId, errorReason: 'BlockedByClient' })
      throw new Error('Unapproved browser request origin')
    }
    await cdp.send('Fetch.continueRequest', { requestId })
  })
  cdp.on('Network.responseReceived', ({ response: value }) => {
    const url = new URL(value.url)
    if (url.origin === origin && url.pathname.startsWith('/api/')) {
      network.push({ path: url.pathname, status: value.status })
    }
  })
  await cdp.send('Fetch.enable', { patterns: [{ urlPattern: '*' }] })
  await cdp.send('Page.addScriptToEvaluateOnNewDocument', {
    source: `if (window.top === window && location.origin === ${JSON.stringify(origin)}) {
      localStorage.setItem('api_token', ${JSON.stringify(JSON.stringify({ data: token, expTime: Date.now() + 600_000 }))});
    }`
  })
  const card = `Array.from(document.querySelectorAll('.output-card.is-targeted')).find(e =>
    e.querySelector('strong')?.textContent === ${JSON.stringify(config.title)})`
  for (const view of [{ name: 'desktop', width: 1440, height: 900, mobile: false },
    { name: 'mobile-simulation', width: 390, height: 844, mobile: true }]) {
    step = `${view.name}:load`
    const networkStart = network.length
    const downloads = join(outputDirectory, `${view.name}-downloads`)
    await mkdir(downloads, { mode: 0o700 })
    await cdp.send('Browser.setDownloadBehavior', { behavior: 'allow', downloadPath: downloads })
    await cdp.send('Emulation.setDeviceMetricsOverride', {
      width: view.width, height: view.height, mobile: view.mobile, deviceScaleFactor: 1
    })
    await cdp.send('Page.navigate', { url: route.href })
    await poll(() => evaluate(`Boolean(${card})`))
    assert.equal(await evaluate('location.origin'), origin)
    await evaluate(`(${card}).scrollIntoView({ block: 'center' })`)
    if (typeof config.expectedText === 'string') {
      step = `${view.name}:preview`
      await evaluate(`Array.from((${card}).querySelectorAll('button')).find(b => b.textContent.trim() === '预览').click()`)
      await poll(() => evaluate(`document.querySelector('.output-preview pre')?.textContent === ${JSON.stringify(config.expectedText)}`))
    }
    step = `${view.name}:download`
    await evaluate(`Array.from((${card}).querySelectorAll('button')).find(b => b.textContent.trim() === '下载' && !b.disabled).click()`)
    const filename = await poll(async () => {
      const names = await readdir(downloads)
      return names.length === 1 && !names[0].endsWith('.crdownload') ? names[0] : false
    })
    const bytes = await readFile(join(downloads, filename))
    const hash = createHash('sha256').update(bytes).digest('hex')
    assert.equal(hash, config.expectedSha256)
    await cdp.terminalBarrier()
    assert(network.slice(networkStart).some(item => item.path === downloadPath && item.status === 200))
    const bounds = await evaluate(`(() => { const r=(${card}).getBoundingClientRect();
      return {left:r.left,right:r.right,width:r.width,viewport:innerWidth}; })()`)
    assert(bounds.width > 0 && bounds.left >= -1 && bounds.right <= bounds.viewport + 1)
    const shot = await cdp.send('Page.captureScreenshot', { format: 'png' })
    await writeFile(join(outputDirectory, `${view.name}.png`), Buffer.from(shot.data, 'base64'), { mode: 0o600 })
    observations.push({ viewport: view, bytes: bytes.length, sha256: hash, filename,
      previewTextMatched: typeof config.expectedText === 'string', cardBounds: bounds })
  }
  await cdp.terminalBarrier()
  succeeded = true
} catch {
  // Record the operation label only; never dump browser/network exceptions with credentials.
  succeeded = false
} finally {
  if (cdp) { try { await cdp.close() } catch { cleanupFailures.push('cdp_close') } }
  if (chrome?.pid) {
    try { await stopChrome(chrome, profile) } catch { cleanupFailures.push('chrome_cleanup') }
  } else await rm(profile, { recursive: true, force: true })
  clearTimeout(timeout)
  process.off('SIGINT', onSignal)
  process.off('SIGTERM', onSignal)
  const report = { succeeded: succeeded && cleanupFailures.length === 0, step, observations,
    network, cleanupFailures, authentication: 'real OAuth token bootstrapped into isolated browser storage',
    limits: ['Not browser OAuth login acceptance.', 'Mobile emulation is not WeChat physical-device evidence.',
      'Uses existing published files; does not create trusted runs or stop Agents.'] }
  await writeFile(join(outputDirectory, 'observation.json'), JSON.stringify(report, null, 2) + '\n', { mode: 0o600 })
  console.log(JSON.stringify({ succeeded: report.succeeded, step, observedViewports: observations.length, cleanupFailures }))
  if (!report.succeeded) process.exitCode = 1
}
