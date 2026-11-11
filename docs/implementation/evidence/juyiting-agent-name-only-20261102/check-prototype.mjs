import { strict as assert } from 'node:assert'
import { writeFile } from 'node:fs/promises'
import { launchChrome,evaluate,waitForExpression,stopChrome } from '/home/isp/wsps/cyf/web/scripts/juyiting/e13/lib/cdp-harness.mjs'
const browser=await launchChrome({debugPort:19493}),cdp=browser.cdp,results=[]
try {
 for(const width of [1440,390,320]) {
  await cdp.send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<760})
  await cdp.send('Page.navigate',{url:'http://127.0.0.1:18786/index.html#tasks'})
  await waitForExpression(cdp,"!!document.querySelector('[data-complete-task-agent]')")
  await evaluate(cdp,`(()=>{state.taskFilter='';state.taskAgent='';state.taskSearch='';state.matterLibrary={};for(const id of ['a','b']){const ctx=blankMatterContext();ctx.task={id,title:id,description:'',files:[],requiredAbilities:[]};ctx.agent={id,name:'吴用'};state.matterLibrary[id]=ctx;}render();})()`)
  assert.deepEqual(await evaluate(cdp,"Array.from(document.querySelector('[data-complete-task-agent]').options,o=>[o.value,o.text])"),[['','全部承接 Agent'],['a','吴用'],['b','吴用']])
  await evaluate(cdp,"(()=>{const s=document.querySelector('[data-complete-task-agent]');s.value='b';s.dispatchEvent(new Event('change',{bubbles:true}));})()")
  assert.deepEqual(await evaluate(cdp,"Array.from(document.querySelectorAll('.task-card')).filter(e=>!e.hidden).map(e=>e.dataset.matterKey)"),['b'])
  results.push({width,namesOnly:true,distinctValues:true,filterById:true})
 }
 await writeFile(new URL('./prototype-results.json',import.meta.url),JSON.stringify(results,null,2));console.log(JSON.stringify(results))
}finally{browser.cdp.close();await stopChrome(browser.chrome,browser.userDataDir)}
