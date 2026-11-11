import fs from 'node:fs';import {createRequire} from 'node:module';
const root='/home/isp/wsps/worktrees/user-facing-copy-cleanup-web-20261027',out='/tmp/cyf-user-copy-browser-20261027',evidence='/home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/optimization/evidence/user-facing-copy-cleanup-20261027';
const require=createRequire(root+'/package.json'),{parse,compileScript}=require('@vue/compiler-sfc');
const {descriptor}=parse(fs.readFileSync(root+'/src/components/personal-workspace/WorkspaceWriteRecovery.vue','utf8'));
const code=compileScript(descriptor,{id:'recovery',inlineTemplate:true}).content.replace(/^import\s+\{([^}]+)\}\s+from\s+['"]vue['"];?\s*$/gm,(_,names)=>`const {${names.replace(/\s+as\s+/g,': ')}}=Vue`).replace('export default','return');
fs.copyFileSync(require.resolve('vue/dist/vue.global.js'),out+'/vue.js');
fs.writeFileSync(out+'/fixture.html',`<!doctype html><html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><div id="app"></div><script src="vue.js"></script><script>const Component=new Function('Vue',${JSON.stringify(code)})(Vue);const pending=Vue.ref([{target:'internal-id',label:'添加资料',state:'UNKNOWN'}]);window.pending=pending;Vue.createApp({render:()=>Vue.h(Component,{pending:pending.value,onRetry:()=>pending.value=[]})}).mount('#app')</script></html>`);
const port=fs.readFileSync(out+'/profile/DevToolsActivePort','utf8').split('\n')[0];const target=await(await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json();const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r);let serial=0;const pending=new Map(),checks=[],errors=[];ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result)}if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails)};const cdp=(method,params={})=>new Promise((resolve,reject)=>{const id=++serial;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});const ev=async expression=>{const r=await cdp('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value};const pause=ms=>new Promise(r=>setTimeout(r,ms));const check=(name,pass)=>{checks.push({name,pass});if(!pass)throw Error(name)};
await cdp('Runtime.enable');await cdp('Page.enable');
try {
 for(const width of [390,1440]){
  await cdp('Emulation.setDeviceMetricsOverride',{width,height:860,deviceScaleFactor:1,mobile:width===390});
  await cdp('Page.navigate',{url:'file://'+out+'/fixture.html'});for(let i=0;i<50;i++){await pause(100);if(await ev(`!!document.querySelector('.workspace-write-recovery')`))break}
  check(width+' unknown keeps warning and recovery',await ev(`document.body.innerText.includes('结果尚未确认')&&!!document.querySelector('button')`));
  check(width+' no internal id',await ev(`!document.body.innerText.includes('internal-id')`));
  await ev(`document.querySelector('button').click()`);await pause(50);
  check(width+' completed state quiet',await ev(`!document.querySelector('.workspace-write-recovery')&&!document.body.innerText.includes('已提交')`));
  await cdp('Page.navigate',{url:'http://127.0.0.1:18786/index.html?scenario=ready&preview=copy-cleanup-20261027#chat'});for(let i=0;i<50;i++){await pause(100);if(await ev(`location.protocol==='http:'&&document.readyState==='complete'&&document.body.innerText.length>200`))break}
  check(width+' existing prototype opens',await ev(`document.title.length>0&&location.protocol==='http:'&&document.readyState==='complete'&&document.body.innerText.length>200`));
  check(width+' prototype removes old success feedback',!fs.readFileSync('/home/isp/wsps/cyf/web/prototypes/juyiting/interaction-completion.js','utf8').includes("feedback('原操作已提交"));
  fs.writeFileSync(evidence+'/prototype-'+width+'.png',Buffer.from((await cdp('Page.captureScreenshot',{format:'png'})).data,'base64'));
 }
 check('no runtime exceptions',errors.length===0);
}finally{fs.writeFileSync(evidence+'/browser-checks.json',JSON.stringify({scope:'production recovery component with local fixture, existing offline prototype; not authenticated live APIs',checks,errors},null,2));ws.close()}
console.log(JSON.stringify({checks:checks.length,failed:checks.filter(x=>!x.pass).length,errors:errors.length}));
