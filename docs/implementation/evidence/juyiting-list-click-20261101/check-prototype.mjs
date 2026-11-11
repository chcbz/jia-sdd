import { strict as assert } from 'node:assert'
import { writeFile } from 'node:fs/promises'
import { launchChrome, evaluate, waitForExpression, stopChrome } from '/home/isp/wsps/cyf/web/scripts/juyiting/e13/lib/cdp-harness.mjs'
const out = new URL('./', import.meta.url)
const browser = await launchChrome({ debugPort: 19487 })
const cdp = browser.cdp
const checks = []
async function load(width) {
  await cdp.send('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: width < 760 })
  await cdp.send('Page.navigate', { url: 'http://127.0.0.1:18786/index.html#workspace' })
  await waitForExpression(cdp, "location.hash === '#workspace' && !!document.querySelector('.treasure-file-open')")
  await evaluate(cdp, 'new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
}
async function clickAt(point) {
  await cdp.send('Input.dispatchMouseEvent', { type: 'mousePressed', ...point, button: 'left', clickCount: 1 })
  await cdp.send('Input.dispatchMouseEvent', { type: 'mouseReleased', ...point, button: 'left', clickCount: 1 })
}
try {
  for (const width of [1440, 390, 320]) {
    for (const area of ['title', 'metadata', 'blank', 'button']) {
      await load(width)
      const point = await evaluate(cdp, `(() => {
        const row = document.querySelector('.treasure-file-row'); row.scrollIntoView({block:'center'});
        const target = row.querySelector(${JSON.stringify(area === 'title' ? 'strong' : area === 'metadata' ? 'p' : 'button')});
        const r = ( ${JSON.stringify(area)} === 'blank' ? row : target).getBoundingClientRect();
        return {x: r.left + (${JSON.stringify(area)} === 'blank' ? 4 : r.width/2), y: r.top + (${JSON.stringify(area)} === 'blank' ? 4 : r.height/2)};
      })()`)
      assert(await evaluate(cdp, `document.elementFromPoint(${point.x},${point.y})?.closest('button')?.classList.contains('treasure-file-open')`), `hit target ${width}/${area}`)
      await clickAt(point)
      await waitForExpression(cdp, "location.hash === '#file' && !!document.querySelector('.treasure-file-heading')")
      checks.push({ width, area, opened: true }); console.log('passed',width,area)
    }
    await load(width)
    await cdp.send('Page.bringToFront')
    assert(await evaluate(cdp, "document.querySelector('.treasure-file-open').focus(); document.activeElement.matches('.treasure-file-open')"))
    await cdp.send('Input.dispatchKeyEvent', { type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13, text: '\r', unmodifiedText: '\r' })
    await cdp.send('Input.dispatchKeyEvent', { type: 'keyUp', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13 })
    await waitForExpression(cdp, "location.hash === '#file'")
    checks.push({ width, keyboard: 'Enter', opened: true })
    await load(width)
    const disabled = await evaluate(cdp, `(() => { const b = document.querySelector('.treasure-file-open'); b.disabled = true; const r=b.parentElement.getBoundingClientRect(); return {x:r.left+4,y:r.top+4}; })()`)
    await clickAt(disabled)
    assert.equal(await evaluate(cdp, 'location.hash'), '#workspace')
    checks.push({ width, disabled: true, stayedInList: true })
    await evaluate(cdp, "document.querySelector('.treasure-file-open').disabled=false;document.querySelector('.treasure-file-row strong').textContent='这是一份很长的资料名称用于检查移动端换行与整行点击区域-固定版本说明.txt'")
    assert(await evaluate(cdp, 'document.documentElement.scrollWidth <= innerWidth'), `no horizontal overflow ${width}`)
    const screenshot = await cdp.send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false })
    await writeFile(new URL(`prototype-${width}.png`, out), Buffer.from(screenshot.data, 'base64'))
  }
  await writeFile(new URL('prototype-results.json', out), JSON.stringify({ scope: 'offline prototype only', checks }, null, 2))
  console.log(JSON.stringify({ passed: checks.length, screenshots: [1440,390,320] }))
} finally { cdp.close(); await stopChrome(browser.chrome, browser.userDataDir) }
