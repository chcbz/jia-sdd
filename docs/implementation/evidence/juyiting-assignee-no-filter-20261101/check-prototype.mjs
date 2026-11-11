import { strict as assert } from 'node:assert'
import { writeFile } from 'node:fs/promises'
import { launchChrome, evaluate, waitForExpression, stopChrome } from '/home/isp/wsps/cyf/web/scripts/juyiting/e13/lib/cdp-harness.mjs'
const out = new URL('./', import.meta.url), checks = [], errors = []
const browser = await launchChrome({ debugPort: 19489 }), cdp = browser.cdp
cdp.on?.('Runtime.exceptionThrown', e => errors.push(e))
try {
 for (const width of [1440, 390, 320]) {
  await cdp.send('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: width < 760 })
  await cdp.send('Page.navigate', { url: 'http://127.0.0.1:18786/index.html?ui=20261101-no-assignee-filter#detail' })
  await waitForExpression(cdp, "typeof commissionAssignment === 'function' && typeof state !== 'undefined'")
  await evaluate(cdp, `state.agent=null;state.task={title:'承办筛选原型回归',description:'整理资料',files:[],complete:false};state.commissionFilter='external';render()`)
  await waitForExpression(cdp, "!!document.querySelector('.commission-assignment')")
  assert.equal(await evaluate(cdp,"document.querySelectorAll('[data-action=commission-filter]').length"),0)
  const all = await evaluate(cdp,"Array.from(document.querySelectorAll('.commission-assignment [data-action=complete-recommend-agent]'),b=>b.dataset.agent)")
  assert.deepEqual([...all].sort(),['0','1','3','4'])
  // Selection remains explicit and does not dispatch, including an offline owned Agent.
  await evaluate(cdp,"document.querySelector('.commission-assignment [data-agent=\"3\"]').click()")
  await waitForExpression(cdp,"document.querySelector('.commission-assignment summary')?.textContent.includes('林冲')")
  assert.equal(await evaluate(cdp,'awaitingAssignment()'),true)
  assert.equal(await evaluate(cdp,"!!document.querySelector('[data-action=complete-agent-confirm]')"),true)
  assert.equal(await evaluate(cdp,'document.documentElement.scrollWidth <= innerWidth'),true)
  await evaluate(cdp,"document.querySelector('.commission-assignment').scrollIntoView({block:'center'})")
  await writeFile(new URL(`detail-${width}.png`,out),Buffer.from((await cdp.send('Page.captureScreenshot',{format:'png'})).data,'base64'))
  checks.push({width,page:'detail',noFilter:true,allEligibleIncludingMineAndExternal:true,ineligibleExternalAbsent:true,staleFilterIgnored:true,manualSelectionWithoutDispatch:true,noOverflow:true})
  await cdp.send('Page.navigate',{url:'http://127.0.0.1:18786/index.html?scenario=assignee-recommendation&ui=20261101-no-assignee-filter#detail'})
  await waitForExpression(cdp,"document.querySelectorAll('[data-model-candidate]').length===2")
  assert.equal(await evaluate(cdp,"document.querySelectorAll('[data-model-filter],[aria-label=候选所属筛选]').length"),0)
  await evaluate(cdp,"document.querySelector('[data-model-candidate=吴用]').click()")
  await waitForExpression(cdp,"document.querySelector('[data-model-candidate=吴用]')?.getAttribute('aria-pressed')==='true'")
  await evaluate(cdp,"document.querySelector('[data-recommendation-stage=LOADING]').click()")
  assert.equal(await evaluate(cdp,"Array.from(document.querySelectorAll('[data-model-candidate]')).every(b=>b.disabled)"),true)
  await evaluate(cdp,"document.querySelector('[data-recommendation-stage=NO_CANDIDATES]').click()")
  assert.equal(await evaluate(cdp,"document.querySelectorAll('[data-model-candidate]').length"),0)
  assert.equal(await evaluate(cdp,"document.querySelector('[data-model-confirm]').disabled"),true)
  checks.push({width,page:'recommendation',noFilter:true,bothOrigins:true,selectable:true,loadingDisabled:true,emptyConfirmDisabled:true})
 }
 assert.equal(errors.length,0)
 await writeFile(new URL('results.json',out),JSON.stringify({checks,uncaughtExceptions:errors.length},null,2)+'\n')
 console.log(JSON.stringify(checks,null,2))
} finally { cdp.close(); await stopChrome(browser.chrome,browser.userDataDir) }
