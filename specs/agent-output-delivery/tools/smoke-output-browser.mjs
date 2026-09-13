// Live output resource-route or Hall bounty navigation smoke. No mocked API responses or model dispatch.
// Input JSON: webRoot, tokenFile, outputDirectory, resourceRoute, title,
// expectedSha256, expectedText or expectedImageSize {width,height} (optional).
// Resource route must use local Vite15173.
// Optional entryMode: 'hall-bounty', bountyStatus: open/assigned/running/completed/failed/archived.
import { spawn } from 'node:child_process'
import { createRequire } from 'node:module'
import { withChromiumCloseCompatibility } from './output-browser-session.mjs'
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
const entryMode = config.entryMode ?? 'resource-route'
assert(['resource-route', 'hall-bounty'].includes(entryMode))
const bountyStatusLabels = {
  open: '待点将', assigned: '已点将', running: '在办', completed: '交令', failed: '失手', archived: '入档'
}
if (entryMode === 'hall-bounty') {
  assert.equal(sourceType, 'TASK')
  assert(Object.hasOwn(bountyStatusLabels, config.bountyStatus))
}
const part = name => encodeURIComponent(route.searchParams.get(name))
const collection = sourceType === 'TASK'
  ? `/agent/tasks/${part('outputSourceId')}/artifacts`
  : `/chat/conversations/${part('outputSourceId')}/outputs`
const downloadPath = `/api${collection}/${part('outputId')}/versions/${part('outputVersion')}/download`
assert(/^[a-f0-9]{64}$/.test(config.expectedSha256))
assert(typeof config.title === 'string' && config.title.length > 0)
if (config.expectedImageSize !== undefined) {
  assert(config.expectedText === undefined, 'Choose one expected preview type')
  for (const dimension of ['width', 'height']) {
    assert(Number.isInteger(config.expectedImageSize[dimension]) && config.expectedImageSize[dimension] > 0)
  }
}
const token = JSON.parse(await readFile(config.tokenFile, 'utf8')).access_token
assert(typeof token === 'string' && token.length > 0)
const tokenExpires = Number(JSON.parse(Buffer.from(token.split('.')[1], 'base64url')).exp) * 1000
assert(tokenExpires > Date.now() + 180_000, 'Refresh the test OAuth token before this probe')
const { CdpSession, stopChrome } = await import(pathToFileURL(resolve(
  config.webRoot, 'tests/juyiting-public-beta-ui-smoke.mjs')))
const OutputBrowserSession = withChromiumCloseCompatibility(CdpSession)
const WebSocketCtor = createRequire(resolve(config.webRoot, 'package.json'))('ws')
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
const blockedResources = []
let failureMessage = ''
let terminalErrors = []
let failureDom = null
const cleanupMessages = []
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


const click = async expression => {
  await evaluate(`(${expression}).scrollIntoView({ block: 'center', inline: 'nearest' })`)
  const point = await poll(() => evaluate(`(() => {
    const e = (${expression}); if (!e || e.disabled) return null;
    const r = e.getBoundingClientRect(); const x = r.left+r.width/2, y = r.top+r.height/2;
    if (!(r.width > 0 && r.height > 0 && x >= 0 && y >= 0 && x < innerWidth && y < innerHeight)) return null;
    const top = document.elementFromPoint(x,y);
    return top && (top === e || e.contains(top)) ? { x, y } : null;
  })()`))
  await cdp.send('Input.dispatchMouseEvent', { type: 'mouseMoved', ...point })
  await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', button: 'left', clickCount: 1, ...point })
  await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', button: 'left', clickCount: 1, ...point })
}

try {
  chrome = spawn('/usr/bin/chromium', [
    '--headless=new', '--password-store=basic', '--disable-gpu', '--no-first-run', '--no-default-browser-check',
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
  cdp = new OutputBrowserSession({ guard, cdpCommandTimeoutMs: 20_000 }, wsUrl, WebSocketCtor)
  await cdp.open()
  await cdp.send('Page.enable')
  await cdp.send('Runtime.enable')
  await cdp.send('Network.enable')
  await cdp.send('Network.setCacheDisabled', { cacheDisabled: true })
  cdp.on('Fetch.requestPaused', async ({ requestId, request, resourceType }) => {
    const url = new URL(request.url)
    const allowed = url.origin === origin || url.protocol === 'data:' ||
      (url.protocol === 'blob:' && url.origin === origin)
    if (!allowed) {
      blockedResources.push({ origin: url.origin, resourceType })
      await cdp.send('Fetch.failRequest', { requestId, errorReason: 'BlockedByClient' })
      const hasAuthorization = Object.keys(request.headers || {}).some(key => key.toLowerCase() === 'authorization')
      if (resourceType === 'Document' || hasAuthorization) throw new Error('Unapproved credential or navigation origin')
      return
    }
    if (url.origin === origin && request.method !== 'GET' &&
      (/^\/api\/chat\/stream\/?$/.test(url.pathname) ||
        /^\/api\/agent\/tasks\/[^/]+\/(?:assign|auto-assign|deliveries|rework)(?:\/|$)/.test(url.pathname))) {
      await cdp.send('Fetch.failRequest', { requestId, errorReason: 'BlockedByClient' })
      throw new Error('Read-only navigation attempted task execution or review')
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
      localStorage.setItem('api_token', ${JSON.stringify(JSON.stringify({ data: token, expTime: tokenExpires }))});
    }`
  })
  const cardSelector = entryMode === 'hall-bounty' ? '.bounty-modal .output-card' : '.output-card.is-targeted'
  const card = `Array.from(document.querySelectorAll(${JSON.stringify(cardSelector)})).find(e =>
    e.querySelector('strong')?.textContent === ${JSON.stringify(config.title)})`
  const openBounty = async () => {
    const navigationStep = step
    const quickAction = `document.querySelector('[data-tour="portrait-action-tasks"]')`
    step = `${navigationStep}:find-board-entry`
    await poll(() => evaluate(`Boolean(${quickAction})`))
    // Dismiss through the actual user control; do not overwrite onboarding or Vue state.
    if (await evaluate(`Boolean(document.querySelector('.onboarding-overlay'))`)) {
      step = `${navigationStep}:dismiss-onboarding`
      await click(`document.querySelector('.onboarding-dialog [aria-label="稍后查看新手引导"]')`)
      await poll(() => evaluate(`!document.querySelector('.onboarding-overlay')`))
    }
    step = `${navigationStep}:open-board`
    const landscape = await evaluate(`document.querySelector('.juyi-page')?.classList.contains('experience-landscape-map')`)
    if (landscape) {
      // Read the same canonical hotspot geometry as onboarding, then use real pointer input.
      // Do not call focusHotspot/openPanel or assign component state.
      const point = await poll(() => evaluate(`(async () => {
        const { juyitingGame } = await import('/src/game/index.js');
        const { viewportBoundsToClientRect } = await import('/src/components/juyiting/hallOnboardingGeometry.js');
        const page = document.querySelector('.juyi-page');
        const canvas = page?.querySelector('.hall-board .melon-layer canvas');
        const r = viewportBoundsToClientRect({ bounds: juyitingGame.getHotspotScreenBounds('bounty-board'),
          canvasRect: canvas?.getBoundingClientRect(), viewport: juyitingGame.getRenderSnapshot()?.viewport,
          virtualLandscape: page?.classList.contains('is-virtual-landscape') });
        if (!r) return null;
        const x = r.left + r.width / 2, y = r.top + r.height / 2;
        if (x < 0 || y < 0 || x >= innerWidth || y >= innerHeight) return null;
        return document.elementFromPoint(x, y) === canvas ? { x, y } : null;
      })()`))
      await cdp.send('Input.dispatchMouseEvent', { type: 'mouseMoved', ...point })
      await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', button: 'left', clickCount: 1, ...point })
      await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', button: 'left', clickCount: 1, ...point })
    } else await click(quickAction)
    await poll(() => evaluate(`Boolean(document.querySelector('.bounty-panel .task-search input'))`))
    const label = JSON.stringify(bountyStatusLabels[config.bountyStatus])
    step = `${navigationStep}:filter-and-search`
    await click(`Array.from(document.querySelectorAll('.task-status-tabs button')).find(e =>
      Array.from(e.childNodes).filter(n => n.nodeType === Node.TEXT_NODE).map(n => n.textContent).join('').trim() === ${label})`)
    await click(`document.querySelector('.bounty-panel .task-search input')`)
    await cdp.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'a', code: 'KeyA', windowsVirtualKeyCode: 65, modifiers: 2 })
    await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'a', code: 'KeyA', windowsVirtualKeyCode: 65, modifiers: 2 })
    await cdp.send('Input.insertText', { text: route.searchParams.get('outputSourceId') })
    await cdp.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 })
    await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 })
    const taskCard = `Array.from(document.querySelectorAll('.task-card')).find(e =>
      Array.from(e.querySelectorAll('.task-meta span')).some(s => s.textContent.trim() === ${JSON.stringify(route.searchParams.get('outputSourceId'))}))`
    step = `${navigationStep}:find-task`
    await poll(() => evaluate(`Boolean(${taskCard})`))
    step = `${navigationStep}:open-task`
    await click(taskCard)
    await poll(() => evaluate(`Boolean(${card})`))
    assert(await evaluate(`document.querySelector('.bounty-modal .modal-task-info')?.textContent.includes(${JSON.stringify(route.searchParams.get('outputSourceId'))})`))
  }
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
    if (entryMode === 'hall-bounty') {
      await cdp.send('Emulation.setTouchEmulationEnabled', { enabled: view.mobile, maxTouchPoints: 1 })
    }
    await cdp.send('Page.navigate', { url: entryMode === 'hall-bounty'
      ? `${origin}/juyiting?nativeOrientation=portrait` : route.href })
    if (entryMode === 'hall-bounty') {
      step = `${view.name}:hall-bounty-navigation`
      await openBounty()
      step = `${view.name}:close-and-reopen`
      await click(`document.querySelector('.bounty-modal .modal-close')`)
      await poll(() => evaluate(`!document.querySelector('.bounty-modal')`))
      await click(`document.querySelector('.floating-panel .panel-close')`)
      await poll(() => evaluate(`!document.querySelector('.panel-overlay')`))
      await openBounty()
    }
    await poll(() => evaluate(`Boolean(${card})`))
    assert.equal(await evaluate('location.origin'), origin)
    await evaluate(`(${card}).scrollIntoView({ block: 'center' })`)
    if (typeof config.expectedText === 'string' || config.expectedImageSize) {
      step = `${view.name}:preview`
      await click(`Array.from((${card}).querySelectorAll('button')).find(b => b.textContent.trim() === '预览')`)
      if (typeof config.expectedText === 'string') {
        await poll(() => evaluate(`document.querySelector('.output-preview pre')?.textContent === ${JSON.stringify(config.expectedText)}`))
      } else {
        await poll(() => evaluate(`(() => { const img = document.querySelector('.output-preview img');
          return img?.complete && img.alt === ${JSON.stringify(config.title)} &&
            img.naturalWidth === ${config.expectedImageSize.width} && img.naturalHeight === ${config.expectedImageSize.height}; })()`))
      }
    }
    step = `${view.name}:download`
    await click(`Array.from((${card}).querySelectorAll('button')).find(b => b.textContent.trim() === '下载' && !b.disabled)`)
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
    observations.push({ viewport: view, entryMode, closedAndReopened: entryMode === 'hall-bounty',
      bytes: bytes.length, sha256: hash, filename,
      previewTextMatched: typeof config.expectedText === 'string',
      previewImageMatched: Boolean(config.expectedImageSize), expectedImageSize: config.expectedImageSize ?? null,
      cardBounds: bounds })
  }
  await cdp.terminalBarrier()
  succeeded = true
} catch (error) {
  failureMessage = String(error?.message || 'Browser probe failed').replaceAll(token, '[REDACTED_TOKEN]')
  terminalErrors = cdp?.takeTerminalErrors().map(e => String(e.message).replaceAll(token, '[REDACTED_TOKEN]')) || []
  if (cdp && !abort.signal.aborted) {
    try {
      failureDom = await evaluate(`({ path: location.pathname,
        hallClass: document.querySelector('.juyi-page')?.className ?? null,
        onboarding: Boolean(document.querySelector('.onboarding-overlay')),
        tourAnchors: Array.from(document.querySelectorAll('[data-tour]')).map(e => e.getAttribute('data-tour')),
        bountyPanels: document.querySelectorAll('.bounty-panel').length,
        taskCards: document.querySelectorAll('.task-card').length,
        outputCards: document.querySelectorAll('.output-card').length })`)
      const shot = await cdp.send('Page.captureScreenshot', { format: 'png' })
      await writeFile(join(outputDirectory, 'failure.png'), Buffer.from(shot.data, 'base64'), { mode: 0o600 })
    } catch { /* Keep the original failure and bounded cleanup even if diagnostics are unavailable. */ }
  }
  succeeded = false
} finally {
  if (cdp) { try { await cdp.close() } catch (error) {
    cleanupFailures.push('cdp_close')
    cleanupMessages.push(String(error.message).replaceAll(token, '[REDACTED_TOKEN]'))
  } }
  if (chrome?.pid) {
    try { await stopChrome(chrome, profile) } catch { cleanupFailures.push('chrome_cleanup') }
  } else await rm(profile, { recursive: true, force: true })
  clearTimeout(timeout)
  process.off('SIGINT', onSignal)
  process.off('SIGTERM', onSignal)
  const report = { succeeded: succeeded && cleanupFailures.length === 0, entryMode, step, observations,
    network, blockedResources, failureMessage, failureDom, terminalErrors, cleanupFailures, cleanupMessages,
    closeObservation: cdp?.closeObservation ?? null,
    eventCounts: Object.fromEntries([...new Set(cdp?.events.map(e => e.method) || [])].map(method =>
      [method, cdp.events.filter(e => e.method === method).length])),
    authentication: 'real OAuth token bootstrapped into isolated browser storage',
    limits: ['Not browser OAuth login acceptance.', 'Mobile emulation is not WeChat physical-device evidence.',
      'Uses existing published files; does not create trusted runs or stop Agents.'] }
  await writeFile(join(outputDirectory, 'observation.json'), JSON.stringify(report, null, 2) + '\n', { mode: 0o600 })
  console.log(JSON.stringify({ succeeded: report.succeeded, step, observedViewports: observations.length, cleanupFailures }))
  if (!report.succeeded) process.exitCode = 1
}
