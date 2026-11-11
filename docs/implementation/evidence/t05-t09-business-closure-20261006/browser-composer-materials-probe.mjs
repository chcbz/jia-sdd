import {spawn} from 'node:child_process';
import {readFile,writeFile,rm} from 'node:fs/promises';
import WebSocket from '/home/isp/wsps/cyf/web/node_modules/ws/index.js';
const dir='/home/isp/wsps/cyf/docs/implementation/evidence/t05-t09-business-closure-20261006';
const profile='/var/tmp/cyf-t05-t09-browser-W7vzug';
for(const p of ['SingletonLock','SingletonCookie','SingletonSocket']){try{await rm(profile+'/'+p,{force:true})}catch{}}
const chrome=spawn('/usr/bin/chromium-browser',['--no-sandbox','--headless=new','--disable-gpu','--disable-component-update','--no-first-run','--no-default-browser-check','--remote-debugging-address=127.0.0.1','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--window-size=1440,1000','about:blank'],{stdio:['ignore','ignore','pipe']});
let stderr='';chrome.stderr.on('data',b=>{stderr=(stderr+b.toString()).slice(-4096)});
let port;for(let i=0;i<300;i++){try{const a=await readFile(profile+'/DevToolsActivePort','utf8');const c=a.split('\n')[0];if((await fetch(`http://127.0.0.1:${c}/json/version`)).ok){port=c;break}}catch{}if(chrome.exitCode!==null)throw Error('CHROME_EXIT:'+chrome.exitCode);await new Promise(r=>setTimeout(r,100))}
if(!port)throw Error('NO_PORT');
const target=await(await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json();
const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.once('open',r);ws.once('error',j)});
let seq=0;const pending=new Map();ws.on('message',raw=>{const m=JSON.parse(raw);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);clearTimeout(p.t);m.error?p.j(Error(m.error.message)):p.r(m.result)}}});
const send=(method,params={})=>new Promise((r,j)=>{const id=++seq;const t=setTimeout(()=>{pending.delete(id);j(Error('TIMEOUT'))},60000);pending.set(id,{r,j,t});ws.send(JSON.stringify({id,method,params}))});
const evalv=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error('EVAL_FAIL '+JSON.stringify(r.exceptionDetails));return r.result?.value};
await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
await send('Page.navigate',{url:'https://kit.chaoyoufan.cn/juyiting'});await new Promise(r=>setTimeout(r,4500));
await evalv(`(()=>{const item=[...document.querySelectorAll('.overview-item')].find(e=>e.querySelector('.overview-item-title strong')?.innerText==='T05–T09图文闭环-20261006：阅读所附图片与文本');item.querySelector('button').click();return true})()`);await new Promise(r=>setTimeout(r,3500));
await evalv(`(()=>{document.querySelector('.composer-more').click();return true})()`);await new Promise(r=>setTimeout(r,600));
await evalv(`(()=>{document.querySelector('.composer-add-materials').click();return true})()`);await new Promise(r=>setTimeout(r,2500));
const out=await evalv(`(()=>({text:document.body.innerText.slice(0,12000),visibleButtons:[...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map((b,i)=>({i,text:(b.innerText||'').trim(),cls:(typeof b.className==='string'?b.className:''),aria:b.getAttribute('aria-label'),title:b.title})).slice(-60),checkboxes:[...document.querySelectorAll('input[type=checkbox]')].map((e,i)=>({i,checked:e.checked,visible:e.offsetParent!==null,cls:e.className,id:e.id})),fileInputs:[...document.querySelectorAll('input[type=file]')].map((e,i)=>({i,visible:e.offsetParent!==null,accept:e.accept,cls:e.className})),pickers:[...document.querySelectorAll('[class*=material],[class*=picker],[class*=browse]')].map(e=>({tag:e.tagName,cls:e.className,html:e.outerHTML.slice(0,1000)})).slice(0,40)}))()`);
await writeFile(dir+'/browser-composer-materials-probe.json',JSON.stringify({at:new Date().toISOString(),out},null,2));
console.log(JSON.stringify({ok:true,text:out.text,visibleButtons:out.visibleButtons,checkboxes:out.checkboxes,fileInputs:out.fileInputs},null,2));
await send('Browser.close').catch(()=>{});ws.close();try{await new Promise(resolve=>chrome.exitCode!==null?resolve():chrome.once('exit',resolve))}catch{}process.exit(0);
