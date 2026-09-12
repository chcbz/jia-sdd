import test from 'node:test'
import assert from 'node:assert/strict'
import { resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
import { withChromiumCloseCompatibility } from './output-browser-session.mjs'

const webRoot = process.env.OD_BROWSER_WEB_ROOT
assert(webRoot, 'Set OD_BROWSER_WEB_ROOT to the accepted Web worktree')
const { CdpSession } = await import(pathToFileURL(resolve(webRoot, 'tests/juyiting-public-beta-ui-smoke.mjs')))
const Session = withChromiumCloseCompatibility(CdpSession)
const runtime = { guard: { signal: new AbortController().signal, beforeBoundary () {}, remainingMs: () => 1000 }, cdpCommandTimeoutMs: 1000, cdpCloseTimeoutMs: 200 }
async function fixture (response = {}) {
  class Socket extends EventTarget {
    readyState = 0
    constructor () { super(); queueMicrotask(() => { this.readyState = 1; this.dispatchEvent(new Event('open')) }) }
    emitClose (data) {
      this.readyState = 3
      this.dispatchEvent(Object.assign(new Event('close'), data))
    }
    close (code, reason) {
      this.readyState = 2
      queueMicrotask(() => this.emitClose({ code, reason, wasClean: true, ...response }))
    }
  }
  const session = new Session(runtime, 'ws://127.0.0.1:1', Socket)
  await session.open()
  return session
}
const messages = error => [error.message, ...(error.errors || []).flatMap(messages)].join('\n')
const rejects = (session, pattern) => assert.rejects(session.close(), error => pattern.test(messages(error)))

test('strict echo remains accepted without compatibility', async () => {
  const session = await fixture(); await session.close()
  assert.equal(session.closeObservation.strictMatch, true)
  assert.equal(session.closeObservation.compatibilityUsed, false)
})
test('local clean 1000 with empty reason uses compatibility', async () => {
  const session = await fixture({ reason: '' }); await session.close()
  assert.equal(session.closeObservation.compatibilityUsed, true)
})
test('remote close before local initiation stays rejected', async () => {
  const session = await fixture()
  session.ws.emitClose({ code: 1000, reason: '', wasClean: true })
  await rejects(session, /remote or unproven close/)
  assert.equal(session.closeObservation.compatibilityUsed, false)
})
test('CLOSING socket cannot manufacture a local handshake', async () => {
  const session = await fixture(); session.ws.readyState = 2
  const timer = setTimeout(() => session.ws.emitClose({ code: 1000, reason: '', wasClean: true }), 30)
  try { await rejects(session, /remote close was already in progress/) } finally { clearTimeout(timer) }
  assert.equal(session.closeObservation.localInitiated, false)
})
test('preexisting handler and socket errors survive compatible close', async () => {
  const session = await fixture({ reason: '' })
  session.handlerErrors.push(new Error('prior handler fault'))
  session.recordSocketError(new Error('prior socket fault'))
  await assert.rejects(session.close(), error => /prior handler fault/.test(messages(error)) && /prior socket fault/.test(messages(error)))
  assert.equal(session.closeObservation.compatibilityUsed, true)
})
for (const response of [{ code: 1006, reason: '' }, { wasClean: false, reason: '' }, { reason: 'unexpected' }]) {
  test(`invalid close stays rejected: ${JSON.stringify(response)}`, async () => {
    const session = await fixture(response); await rejects(session, /remote or unproven close/)
    assert.equal(session.closeObservation.compatibilityUsed, false)
  })
}
test('queued remote 1006 cannot be hidden by local close', async () => {
  const session = await fixture({ reason: '' })
  queueMicrotask(() => session.ws.emitClose({ code: 1006, reason: '', wasClean: false }))
  await rejects(session, /remote or unproven close/)
  assert.equal(session.closeObservation.compatibilityUsed, false)
})
