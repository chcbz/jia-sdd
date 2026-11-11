import { strict as assert } from 'node:assert'
import { writeFile } from 'node:fs/promises'
import { launchChrome,evaluate,waitForExpression,stopChrome } from '/home/isp/wsps/cyf/web/scripts/juyiting/e13/lib/cdp-harness.mjs'
const out=new URL('./',import.meta.url),results=[],exceptions=[]
const browser=await launchChrome({debugPort:19491}),cdp=browser.cdp
cdp.on('Runtime.exceptionThrown',e=>exceptions.push(e))
const visible=()=>evaluate(cdp,"Array.from(document.querySelectorAll('.task-card')).filter(e=>!e.hidden).map(e=>e.dataset.matterKey).sort()")
const choose=val=>evaluate(cdp,`(()=>{const s=document.querySelector('[data-complete-task-agent]');s.value=${JSON.stringify(val)};s.dispatchEvent(new Event('change',{bubbles:true}));})()`)
const search=val=>evaluate(cdp,`(()=>{const s=document.querySelector('[data-complete-task-search]');s.value=${JSON.stringify(val)};s.dispatchEvent(new Event('input',{bubbles:true}));})()`)
try{
 for(const width of [1440,390,320]){
  await cdp.send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<760})
  await cdp.send('Page.navigate',{url:'http://127.0.0.1:18786/index.html?ui=20261102-task-agent-filter#tasks'})
  await waitForExpression(cdp,"!!document.querySelector('[data-complete-task-agent]')")
  await evaluate(cdp,`(()=>{
   state.task=null;state.agent=null;state.pending=false;state.taskFilter='待确认承办';state.taskAbility='不存在的旧技能';state.taskAgent='';state.taskSearch='';state.matterLibrary={};state.matterFixtureRevision=2;
   for(const [id,agent,skill,complete] of [['a',{id:0,name:'吴用'},'整理',false],['b',{id:'b',name:'公孙胜'},'整理',false],['c',{id:'0',name:'吴用'},'绘图',true],['d',{id:'d',name:'吴用'},'绘图',false],['pending',null,'整理',false]]){
    const ctx=blankMatterContext();ctx.task={id,title:id==='c'?'测试二':'测试'+id,description:'筛选回归',files:[],requiredAbilities:[skill],complete};ctx.agent=agent;state.matterLibrary[id]=ctx;
   }render();
  })()`)
  assert.deepEqual(await visible(),['pending'])
  assert.equal(await evaluate(cdp,"document.querySelector('[data-status=待承办]')?.getAttribute('aria-pressed')"),'true')
  await evaluate(cdp,"state.taskFilter='';render()")
  assert.deepEqual(await visible(),['a','b','c','d','pending'])
  const opts=await evaluate(cdp,"Array.from(document.querySelector('[data-complete-task-agent]').options,o=>[o.value,o.text])")
  assert.deepEqual(opts,[['','全部承接 Agent'],['0','吴用'],['b','公孙胜'],['d','吴用']])
  await choose('0');assert.deepEqual(await visible(),['a','c'])
  await search('测试二');assert.deepEqual(await visible(),['c'])
  await evaluate(cdp,"document.querySelector('[data-status=已完成]').click()")
  assert.deepEqual(await visible(),['c'])
  await cdp.send('Page.reload')
  await waitForExpression(cdp,"document.querySelector('[data-complete-task-agent]')?.value==='0'")
  assert.deepEqual(await visible(),['c'])
  await search('no-matches');assert.deepEqual(await visible(),[])
  await evaluate(cdp,"document.querySelector('.baseline-empty [data-action=complete-task-clear]').click()")
  assert.deepEqual(await visible(),['a','b','c','d','pending'])
  assert.equal(await evaluate(cdp,"document.querySelector('[data-complete-task-agent]').value"),'')
  await choose('b');assert.deepEqual(await visible(),['b'])
  assert.equal(await evaluate(cdp,"document.documentElement.scrollWidth<=innerWidth"),true)
  assert.equal(await evaluate(cdp,"document.body.innerText.includes('待确认承办')"),false)
  await writeFile(new URL(`tasks-${width}.png`,out),Buffer.from((await cdp.send('Page.captureScreenshot',{format:'png'})).data,'base64'))
  await choose('');await evaluate(cdp,"document.querySelector('[data-status=待承办]').click()")
  assert.deepEqual(await visible(),['pending'])
  await evaluate(cdp,"document.querySelector('.task-card:not([hidden])').click()")
  await waitForExpression(cdp,"location.hash==='#detail' && !!document.querySelector('.matter-advice-card')")
  assert.equal(await evaluate(cdp,"document.querySelector('.matter-advice-card').innerText.includes('待承办')"),true)
  assert.equal(await evaluate(cdp,"document.body.innerText.includes('待确认承办')"),false)
  assert.equal(await evaluate(cdp,"document.querySelectorAll('[data-action=commission-filter]').length"),0)
  assert.equal(await evaluate(cdp,'awaitingAssignment()'),true)
  await cdp.send('Page.navigate',{url:'http://127.0.0.1:18786/index.html?ui=20261102-task-agent-filter#home'})
  await waitForExpression(cdp,"!!document.querySelector('.overview-section')")
  assert.equal(await evaluate(cdp,"document.querySelector('.overview-section').innerText.includes('待承办')"),true)
  assert.equal(await evaluate(cdp,"document.body.innerText.includes('待确认承办')"),false)
  results.push({width,agentIdFilter:true,numericZeroAndDedupe:true,sameNameDifferentIds:true,skillsIgnored:true,combinedNameAndStatus:true,reloadRetainsFilter:true,clearResetsAll:true,pendingVisibleInAll:true,oldStatusMapped:true,newStatusInListDetailHome:true,noAutomaticDispatch:true,noOverflow:true})
 }
 await cdp.send('Page.navigate',{url:'http://127.0.0.1:18786/index.html?scenario=assignee-recommendation&ui=20261102-task-agent-filter#detail'})
 await waitForExpression(cdp,"!!document.querySelector('[data-model-confirm]')")
 assert.equal(await evaluate(cdp,"document.querySelector('.matter-advice-heading').innerText.includes('待承办')"),true)
 assert.equal(await evaluate(cdp,"document.body.innerText.includes('待确认承办')"),false)
 assert.equal(exceptions.length,0)
 await writeFile(new URL('results.json',out),JSON.stringify({results,recommendationLabel:true,uncaughtExceptions:exceptions.length},null,2)+'\n');console.log(JSON.stringify(results,null,2))
}finally{cdp.close();await stopChrome(browser.chrome,browser.userDataDir)}
