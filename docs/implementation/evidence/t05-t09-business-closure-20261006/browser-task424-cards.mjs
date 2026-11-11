import {spawn} from 'node:child_process';
import {readFile,writeFile,rm} from 'node:fs/promises';
import WebSocket from '/home/isp/wsps/cyf/web/node_modules/ws/index.js';
const dir='/home/isp/wsps/cyf/docs/implementation/evidence/t05-t09-business-closure-20261006';
const profile='/var/tmp/cyf-t05-t09-browser-W7vzug';
for(const p of ['SingletonLock','SingletonCookie','SingletonSocket']){try{await rm(profile+'/'+p,{force:true})}catch{}}
const chrome=spawn('/usr/bin/chromium-browser',['--no-sandbox','--headless=new','--disable-gpu','--disable-component-update','--no-first-run','--no-default-browser-check','--remote-debugging-address=127.0.0.1','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--window-size=1440,1000','about:blank'],{stdio:['ignore','ignore','pipe']});
let stderr='';chrome.stderr.on('data',b=>{stderr=(stderr+b.toString()).slice(-4096)});
let port;
for(let i=0;i<300;i++){try{const a=await readFile(profile+'/DevToolsActivePort','utf8');const c=a.split('\n')[0];if((await fetch(`http://127.0.0.1:${c}/json/version`)).ok){port=c;break}}catch{}if(chrome.exitCode!==null)throw Error('CHROME_EXIT:'+chrome.exitCode);await new Promise(r=>setTimeout(r,100))}
if(!port)throw Error('NO_PORT '+stderr.slice(-400));
const target=await(await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json();
const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.once('open',r);ws.once('error',j)});
let seq=0;const pending=new Map();ws.on('message',raw=>{const m=JSON.parse(raw);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);clearTimeout(p.t);m.error?p.j(Error(m.error.message)):p.r(m.result)}}});
const send=(method,params={})=>new Promise((r,j)=>{const id=++seq;const t=setTimeout(()=>{pending.delete(id);j(Error('TIMEOUT '+method))},60000);pending.set(id,{r,j,t});ws.send(JSON.stringify({id,method,params}))});
const evalv=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error('EVAL_FAIL '+JSON.stringify(r.exceptionDetails));return r.result?.value};
await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
await send('Page.navigate',{url:'https://kit.chaoyoufan.cn/juyiting'});
await new Promise(r=>setTimeout(r,5000));
const cards=await evalv(`(()=>{const items=[...document.querySelectorAll('.overview-item')];return items.map((e,i)=>{const t=e.querySelector('.overview-item-title')?.innerText||'';const copy=e.querySelector('.overview-item-copy')?.innerText||'';const btns=[...e.querySelectorAll('button,a')].map(b=>b.innerText.trim()).filter(Boolean);return {i,title:t,status:(e.innerText.match(/已领令|已完成|待领令|尚未交办|交付待验收|执行未完成|处理异常|成果可查看/)?.[0]||''),btns,html:e.outerHTML.slice(0,1200)};})})()`);
console.log(JSON.stringify({ok:true,pid:chrome.pid,cards},null,2));
await send('Browser.close').catch(()=>{});ws.close();try{await new Promise(resolve=>chrome.exitCode!==null?resolve():chrome.once('exit',resolve))}catch{}process.exit(0);
