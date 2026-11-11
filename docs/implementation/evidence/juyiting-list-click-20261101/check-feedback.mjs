import { strict as assert } from 'node:assert'
import { writeFile } from 'node:fs/promises'
import { launchChrome, evaluate, waitForExpression, stopChrome } from '/home/isp/wsps/cyf/web/scripts/juyiting/e13/lib/cdp-harness.mjs'
const out = new URL('./', import.meta.url)
const browser = await launchChrome({ debugPort: 19487 })
const cdp = browser.cdp
const checks = []
const pages = [
  { name: 'home', row: '.overview-section .overview-item', control: '.overview-section .overview-item > button', destination: '#detail', heading: '.task-detail-title,.bounty-task-title' },
  { name: 'workspace', row: '.treasure-file-row', control: '.treasure-file-open', destination: '#file', heading: '.treasure-file-heading h2' }
]
async function load(width, page) {
  await cdp.send('Emulation.setDeviceMetricsOverride', { width, height: 900, deviceScaleFactor: 1, mobile: width < 760 })
  await cdp.send('Page.navigate', { url: `http://127.0.0.1:18786/index.html?listFeedback=20261101#${page.name}` })
  await waitForExpression(cdp, `location.hash === '#${page.name}' && !!document.querySelector(${JSON.stringify(page.control)})`)
  await evaluate(cdp, 'new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))')
  await evaluate(cdp, `(() => {
    window.feedbackClicks=[];
    if(window.feedbackListener) window.removeEventListener('click',window.feedbackListener,true);
    window.feedbackListener=e => {const b=e.target.closest(${JSON.stringify(page.control)}); if(b) feedbackClicks.push(b.dataset.matterKey || b.dataset.id);};
    window.addEventListener('click',window.feedbackListener,true);
  })()`)
}
async function pointFor(page, area) {
  return evaluate(cdp, `(() => {
    const row=document.querySelector(${JSON.stringify(page.row)});row.scrollIntoView({block:'center'});
    const area=${JSON.stringify(area)};
    const el=row.querySelector(area==='title'?'strong':area==='metadata'?'p':area==='status'?'.overview-status':'button');
    const r=(area.endsWith('blank')?row:el).getBoundingClientRect();
    const x=area==='top-blank'||area==='bottom-blank'?r.left+4:area==='right-blank'?r.right-4:r.left+r.width/2;
    const y=area==='top-blank'?r.top+4:area==='bottom-blank'?r.bottom-4:r.top+r.height/2;
    return {x,y,ref:row.querySelector('button').dataset.matterKey || row.querySelector('button').dataset.id};
  })()`)
}
async function clickAt({x,y}) {
  await cdp.send('Input.dispatchMouseEvent', { type:'mousePressed',x,y,button:'left',clickCount:1 })
  await cdp.send('Input.dispatchMouseEvent', { type:'mouseReleased',x,y,button:'left',clickCount:1 })
}
try {
  for (const width of [1440,390,320]) {
    for (const page of pages) {
      for (const area of ['title','metadata',...(page.name==='home'?['status']:[]),'top-blank','bottom-blank','right-blank','button']) {
        await load(width,page)
        assert.equal(await evaluate(cdp, `document.querySelector(${JSON.stringify(page.control)}).querySelector('svg')?.dataset.icon`),'chevronRight',`${page.name} arrow`)
        const point=await pointFor(page,area)
        assert(await evaluate(cdp,`document.elementFromPoint(${point.x},${point.y})?.closest(${JSON.stringify(page.control)}) != null`),`${page.name}/${width}/${area} hit`)
        await clickAt(point)
        await waitForExpression(cdp,`location.hash === ${JSON.stringify(page.destination)}`)
        assert.deepEqual(await evaluate(cdp,'feedbackClicks'),[point.ref],`${page.name}/${width}/${area} opens once with exact ref`)
        checks.push({ page:page.name,width,area,ref:point.ref,openedOnce:true })
      }
      for (const key of ['Enter',' ']) {
        await load(width,page)
        await cdp.send('Page.bringToFront')
        assert(await evaluate(cdp,`document.querySelector(${JSON.stringify(page.control)}).focus();document.activeElement.matches(${JSON.stringify(page.control)})`))
        const enter=key==='Enter'
        await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key,code:enter?'Enter':'Space',windowsVirtualKeyCode:enter?13:32,text:enter?'\r':' ',unmodifiedText:enter?'\r':' '})
        await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key,code:enter?'Enter':'Space',windowsVirtualKeyCode:enter?13:32})
        await waitForExpression(cdp,`location.hash === ${JSON.stringify(page.destination)}`)
        checks.push({page:page.name,width,keyboard:key,opened:true})
      }
      await load(width,page)
      const point=await pointFor(page,'top-blank')
      await evaluate(cdp,`document.querySelector(${JSON.stringify(page.control)}).disabled=true`)
      await clickAt(point)
      assert.equal(await evaluate(cdp,'location.hash'),`#${page.name}`)
      assert.deepEqual(await evaluate(cdp,'feedbackClicks'),[])
      checks.push({page:page.name,width,disabled:true,stayedInList:true})
      await evaluate(cdp,`document.querySelector(${JSON.stringify(page.control)}).disabled=false`)
      assert(await evaluate(cdp,'document.documentElement.scrollWidth <= innerWidth'))
      const screenshot=await cdp.send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false})
      await writeFile(new URL(`feedback-${page.name}-${width}.png`,out),Buffer.from(screenshot.data,'base64'))
      console.log('passed',page.name,width)
    }
  }
  const errors=cdp.events.filter(e=>e.method==='Runtime.exceptionThrown')
  assert.deepEqual(errors,[],'no uncaught browser exceptions')
  await writeFile(new URL('feedback-results.json',out),JSON.stringify({scope:'offline prototype only; user screenshot corrections',checks,uncaughtExceptions:errors.length},null,2))
  console.log(JSON.stringify({passed:checks.length}))
} finally { cdp.close();await stopChrome(browser.chrome,browser.userDataDir) }
