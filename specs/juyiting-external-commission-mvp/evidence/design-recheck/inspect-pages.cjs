const fs=require('fs');const {chromium}=require('/home/isp/wsps/cyf/deliverables/verification/juyiting-formal-flow-1.13.19/browser-tools/node_modules/playwright-core');
(async()=>{const dir=__dirname,owned=JSON.parse(fs.readFileSync(dir+'/owned-targets.json')).targets[0];const browser=await chromium.connectOverCDP('http://127.0.0.1:'+owned.cdpPort);const page=browser.contexts()[0].pages()[0];const results=[];const responses=[];page.on('response',r=>{const u=new URL(r.url());if(u.hostname.endsWith('chaoyoufan.cn'))responses.push({path:u.pathname,status:r.status()})});
async function snap(name){name="current-"+name;await page.screenshot({path:dir+'/'+name+'.png'});const text=await page.locator('body').innerText();results.push({name,viewport:page.viewportSize(),text:text.slice(-16000),horizontalOverflow:await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});fs.writeFileSync(dir+'/current-page-actions.json',JSON.stringify({at:new Date().toISOString(),results,responses},null,2));console.log(name,text.slice(-3200))}
await page.goto('https://kit.chaoyoufan.cn/juyiting');await page.waitForTimeout(1500);
const later=page.getByRole('button',{name:'稍后',exact:true});if(await later.isVisible())await later.click();
await page.getByRole('button',{name:'提出需求',exact:true}).first().click();await page.waitForTimeout(700);await snap('live-create');
await page.getByRole('button',{name:/返回/}).filter({visible:true}).first().click();
const pending=page.locator('.overview-item').filter({hasText:'待点将'}).first();await pending.getByRole('button',{name:'查看进展',exact:true}).click();await page.waitForTimeout(2000);await snap('live-pending-task');
await page.getByRole('button',{name:'另选承办Agent',exact:true}).click();await snap('live-assignee-options');
await page.setViewportSize({width:390,height:844});await page.waitForTimeout(500);await snap('live-pending-mobile');
console.log('READ_ONLY_PAGES_OK');process.exit(0);
})().catch(e=>{console.error(e.message);process.exit(1)});
