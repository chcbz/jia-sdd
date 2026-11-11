import {strict as assert} from 'node:assert'
import {writeFile} from 'node:fs/promises'
import {launchChrome,evaluate,waitForExpression,stopChrome} from '/home/isp/wsps/cyf/web/scripts/juyiting/e13/lib/cdp-harness.mjs'
const browser=await launchChrome({debugPort:19495}),cdp=browser.cdp,results=[]
try{
 for(const width of [1440,390,320]){
  await cdp.send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<760})
  await cdp.send('Page.navigate',{url:'http://127.0.0.1:18786/index.html?ui=20261103-html-md#file'})
  await waitForExpression(cdp,"typeof state!=='undefined' && typeof prototypeDocumentPreview==='function'")
  for(const id of ['ref-brief','ref-html']){
   await evaluate(cdp,`(()=>{state.fileId='${id}';state.fileManage=false;render();})()`)
   await waitForExpression(cdp,"!!document.querySelector('.document-preview iframe')")
   assert.equal(await evaluate(cdp,"document.querySelector('.document-preview iframe').getAttribute('sandbox')"),'')
   assert.equal(await evaluate(cdp,"document.querySelector('.document-preview iframe').srcdoc.includes('<h1>')"),true)
   assert.equal(await evaluate(cdp,"document.documentElement.scrollWidth<=innerWidth"),true)
  }
  results.push({width,html:true,markdown:true,sandbox:true,noPageOverflow:true})
 }
 await writeFile(new URL('./prototype-results.json',import.meta.url),JSON.stringify(results,null,2));console.log(JSON.stringify(results))
}finally{cdp.close();await stopChrome(browser.chrome,browser.userDataDir)}
