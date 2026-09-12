// Probe-only Chromium compatibility; do not relax the shared product smoke helper.
export function withChromiumCloseCompatibility (BaseSession) {
  return class OutputBrowserSession extends BaseSession {
    isExpectedLocalClose (event) {
      const strictMatch = super.isExpectedLocalClose(event)
      const handshake = this.localCloseHandshake
      const compatible = handshake?.initiated === true && handshake.code === 1000 &&
        event?.wasClean === true && event.code === 1000 && event.reason === ''
      this.closeObservation = {
        localInitiated: handshake?.initiated === true,
        expectedCode: handshake?.code ?? null,
        actualCode: event?.code ?? null,
        wasClean: event?.wasClean === true,
        reasonEmpty: event?.reason === '',
        strictMatch,
        compatibilityUsed: !strictMatch && compatible
      }
      return strictMatch || compatible
    }
  }
}
