const fs=require('fs'),http=require('http'),path=require('path');
const source='/home/isp/state/cyf-local-build/tasks/JUYITING-HELP-20261109/source';
const {parse,compileScript,compileStyle}=require(source+'/node_modules/@vue/compiler-sfc');
const {chromium}=require('/tmp/banyishu-ctyun-browser/node_modules/playwright-core');
const raw=fs.readFileSync(source+'/src/components/juyiting/HallHelpCenter.vue','utf8');
const {descriptor}=parse(raw);const scope='data-v-help-browser';
let script=compileScript(descriptor,{id:scope,inlineTemplate:true}).content
.replaceAll("from 'vue'","from '/vue.js'").replaceAll('from "vue"','from "/vue.js"')
.replace(/from ['"]@\/content\/hallHelp['"]/g,"from '/content.js'")
.replace(/from ['"]@\/composables\/useHelpFeedback['"]/g,"from '/feedback.js'")
.replace(/from ['"]@\/(?:composables\/useHttp|stores\/global|stores\/api)['"]/g,"from '/fixture.js'")
.replace('export default','const component =');
script+='\ncomponent.__scopeId="'+scope+'";export default component;';
const style=compileStyle({source:descriptor.styles[0].content,id:scope,scoped:true}).code;
const files={
 '/vue.js':fs.readFileSync(source+'/node_modules/vue/dist/vue.esm-browser.js'),
 '/component.js':script,'/content.js':fs.readFileSync(source+'/src/content/hallHelp.js'),
 '/feedback.js':fs.readFileSync(source+'/src/composables/useHelpFeedback.js','utf8').replace("from 'vue'","from '/vue.js'"),
 '/fixture.js':`export const useGlobalStore=()=>({getJiacn:'offline-browser-fixture'});export const useApiStore=()=>({authorizationGeneration:1});export const kefuApi={post:async()=>{window.feedbackCalls=(window.feedbackCalls||0)+1;throw Object.assign(new Error('fixture rejection'),{status:400})}};`,
 '/style.css':style+`\nhtml,body{margin:0;font-family:system-ui,sans-serif;color:#29352f;background:#e8e8e1}#app{height:100dvh;display:flex;flex-direction:column;max-width:960px;margin:auto;background:#f5f4f0}header.shell{display:flex;align-items:center;gap:24px;padding:12px 20px;border-bottom:1px solid #deded4}header.shell button{min-height:44px;background:none;border:0;color:#974a38}.hall-help-center{height:100%}.fixture{font-size:12px;color:#68716b;margin-left:auto}`,
 '/':`<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="stylesheet" href="/style.css"><div id="app"></div><script type="module">import{createApp,h,ref}from'/vue.js';import Help from'/component.js';createApp({setup(){const panel=ref(null);return()=>[h('header',{class:'shell'},[h('button',{onClick:()=>panel.value.back()},'返回'),h('strong','使用帮助'),h('span',{class:'fixture'},'组件验证 · 离线服务替身')]),h(Help,{ref:panel,onNavigate:x=>window.lastNavigation=x,onReplay:()=>window.replayCalls=(window.replayCalls||0)+1})]}}).component('var-icon',{props:['name'],render(){return h('span',{'aria-hidden':true},this.name==='magnify'?'⌕':'›')}}).mount('#app')</script></html>`
};
(async()=>{
 const server=http.createServer((req,res)=>{const p=req.url.split('?')[0];if(!(p in files)){res.writeHead(404);return res.end()}res.setHeader('Content-Type',p.endsWith('.js')?'text/javascript':p.endsWith('.css')?'text/css':'text/html');res.end(files[p])});await new Promise(done=>server.listen(0,'127.0.0.1',done));
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium-browser',headless:true,args:['--no-sandbox','--disable-dev-shm-usage']});
 const checks=[];try{
 for(const width of [390,1440]){
 const page=await browser.newPage({viewport:{width,height:900}});const errors=[];page.on('pageerror',e=>errors.push(e.message));
 await page.goto(`http://127.0.0.1:${server.address().port}/`);await page.locator('input[type=search]').waitFor();
 await page.screenshot({path:path.join(__dirname,`implemented-help-${width}.png`)});
 await page.locator('input[type=search]').fill('机器人');await page.locator('.help-row').click();
 await page.getByRole('heading',{name:'怎样了解好汉能做什么？'}).waitFor();
 await page.getByRole('button',{name:'查看好汉名册'}).click();if(await page.evaluate(()=>window.lastNavigation)!=='agents')throw Error('navigation');
 await page.getByRole('button',{name:'返回',exact:true}).click();if(await page.locator('input[type=search]').inputValue()!=='机器人')throw Error('query lost');
 await page.locator('input[type=search]').fill('不存在的搜索');await page.getByRole('heading',{name:'还没有找到相关帮助'}).waitFor();
 await page.locator('.help-empty button').click();await page.locator('textarea').fill('浏览器离线反馈');await page.getByRole('button',{name:'提交反馈',exact:true}).click();await page.getByRole('alert').waitFor();
 if(await page.locator('textarea').inputValue()!=='浏览器离线反馈')throw Error('draft lost');
 if(await page.evaluate(()=>window.feedbackCalls)!==1)throw Error('feedback unexpectedly repeated');
 await page.getByRole('button',{name:'返回',exact:true}).click();await page.locator('input[type=search]').fill('');await page.getByRole('button',{name:'重看新手引导'}).click();if(await page.evaluate(()=>window.replayCalls)!==1)throw Error('replay');
 const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth);if(overflow||errors.length)throw Error(JSON.stringify({width,errors,overflow}));
 checks.push({width,passed:true,errors,horizontalOverflow:overflow});await page.close();
 }
 fs.writeFileSync(path.join(__dirname,'browser-checks.json'),JSON.stringify({scope:'Real HallHelpCenter SFC and feedback adapter; offline stores/service and parent navigation fixture, not full application or production',checks},null,2));console.log(checks);
 }finally{await browser.close();server.close()}
})().catch(e=>{console.error(e);process.exit(1)});
