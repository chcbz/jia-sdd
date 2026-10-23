const {chromium}=require('/home/isp/wsps/cyf/deliverables/verification/juyiting-formal-flow-1.13.19/browser-tools/node_modules/playwright-core');
const assert=require('assert'),fs=require('fs');
(async()=>{
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium-browser',headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1440,height:1000}}),errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto('http://127.0.0.1:18786/?scenario=detail-switch-check&reset=1#agents');
 assert.equal(await page.locator('.commission-settings').count(),0);assert.equal(await page.locator('[role=switch]').count(),0);
 for(const [id,expected] of [['4',[false,true]],['3',[true,true]],['4',[true,false]],['3',[false,false]]]){
  await page.locator(`[data-action=choose-agent][data-agent="${id}"]`).click();
  const toggle=page.locator('.agent-detail-scroll [role=switch]');assert.equal(await toggle.count(),1);await toggle.focus();await page.keyboard.press('Space');
  assert.deepEqual(await page.evaluate(()=>commissionAgents.filter(a=>a.owner===commissionViewer).map(commissionOpen)),expected);
  assert.equal(await page.locator('[role=switch]:focus').count(),1);
 }
 await page.locator('[data-action=choose-agent][data-agent="4"]').click();await page.screenshot({path:__dirname+'/desktop.png'});
 await page.locator('[data-action=choose-agent][data-agent="0"]').click();assert.equal(await page.locator('[role=switch]').count(),0);assert.equal(await page.locator('.commission-readonly').count(),1);
 await page.setViewportSize({width:390,height:844});await page.evaluate(()=>{state.selectedAgent=null;agentMobileDetail=false;render()});
 await page.locator('[data-action=choose-agent][data-agent="4"]').click();assert(await page.locator('[role=switch]').isVisible());await page.locator('[role=switch]').click();assert.equal(await page.locator('[role=switch]').getAttribute('aria-checked'),'true');
 await page.screenshot({path:__dirname+'/mobile.png'});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
 await page.locator('[data-action=agent-roster-back]').click();await page.locator('[data-action=choose-agent][data-agent="3"]').click();assert.equal(await page.locator('[role=switch]').getAttribute('aria-checked'),'false');
 await page.reload();assert.equal(await page.evaluate(()=>state.commissionSwitches['4']),true);assert.equal(await page.evaluate(()=>state.commissionSwitches['3']),false);
 assert.deepEqual(errors,[]);fs.writeFileSync(__dirname+'/result.json',JSON.stringify({date:new Date().toISOString(),scope:'offline prototype only',passed:['no separate roster card','only selected owned Agent has switch','four independent combinations','keyboard toggles and focus retained','external Agent read-only','mobile detail interaction and roster return','reload retains independent states','no horizontal document overflow'],errors},null,2));
 await browser.close();console.log('PASS');
})().catch(e=>{console.error(e);process.exit(1)});
