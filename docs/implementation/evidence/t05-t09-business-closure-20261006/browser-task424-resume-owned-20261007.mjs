import {spawn} from 'node:child_process';
import {readFile,writeFile,rm} from 'node:fs/promises';
import WebSocket from '/home/isp/wsps/cyf/web/node_modules/ws/index.js';
const dir='/home/isp/wsps/cyf/docs/implementation/evidence/t05-t09-business-closure-20261006';
const profile='/var/tmp/cyf-t05-t09-browser-W7vzug';
// Profile ownership checked before launch; do not delete Chromium locks.
const chrome=spawn('/usr/bin/chromium-browser',['--no-sandbox','--headless=new','--disable-gpu','--disable-component-update','--no-first-run','--no-default-browser-check','--remote-debugging-address=127.0.0.1','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--window-size=1440,1000','about:blank'],{stdio:['ignore','ignore','pipe']});
let stderr='';chrome.stderr.on('data',b=>{stderr=(stderr+b.toString()).slice(-4096)});
let port;
for(let i=0;i<300;i++){try{const a=await readFile(profile+'/DevToolsActivePort','utf8');const c=a.split('\n')[0];if((await fetch(`http://127.0.0.1:${c}/json/version`)).ok){port=c;break}}catch{}if(chrome.exitCode!==null)throw Error('CHROME_EXIT:'+chrome.exitCode);await new Promise(r=>setTimeout(r,100))}
if(!port)throw Error('NO_PORT '+stderr.slice(-400));
const target=await(await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json();
const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.once('open',r);ws.once('error',j)});
let seq=0;const pending=new Map();const net=[];ws.on('message',raw=>{const m=JSON.parse(raw);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);clearTimeout(p.t);m.error?p.j(Error(m.error.message)):p.r(m.result)}}else if(m.method==='Network.responseReceived'){const r=m.params.response;const u=new URL(r.url);if(u.protocol.startsWith('http'))net.push({at:Date.now(),path:u.pathname,status:r.status,type:m.params.type})}});
const send=(method,params={})=>new Promise((r,j)=>{const id=++seq;const t=setTimeout(()=>{pending.delete(id);j(Error('TIMEOUT '+method))},60000);pending.set(id,{r,j,t});ws.send(JSON.stringify({id,method,params}))});
const evalv=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error('EVAL_FAIL '+JSON.stringify(r.exceptionDetails));return r.result?.value};
await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
await send('Page.navigate',{url:'https://kit.chaoyoufan.cn/juyiting'});
await new Promise(r=>setTimeout(r,5000));
const clicked=await evalv(`(()=>{const item=[...document.querySelectorAll('.overview-item')].find(e=>e.querySelector('.overview-item-title strong')?.innerText==='T05–T09图文闭环-20261006：阅读所附图片与文本');if(!item)return {error:'item not found'};const btn=item.querySelector('button');if(!btn)return {error:'button not found'};btn.click();return {clicked:true,title:item.querySelector('.overview-item-title strong').innerText};})()`);
await new Promise(r=>setTimeout(r,4000));
const state=await evalv(`(async()=>{const wait=ms=>new Promise(r=>setTimeout(r,ms));for(let i=0;i<20;i++){if(document.body.innerText.includes('榜文议事')||document.body.innerText.includes('厅内议事'))break;await wait(300)}return {url:location.href,path:location.pathname,text:document.body.innerText.slice(0,12000),inputs:[...document.querySelectorAll('textarea,input')].map((e,i)=>({i,tag:e.tagName,type:e.type,placeholder:e.placeholder,value:(e.value||'').slice(0,200),aria:e.getAttribute('aria-label'),title:e.title,disabled:e.disabled,visible:e.offsetParent!==null,cls:(typeof e.className==='string'?e.className:'').slice(0,120)})),buttons:[...document.querySelectorAll('button,a')].filter(e=>e.offsetParent!==null).map((e,i)=>({i,tag:e.tagName,text:(e.innerText||'').trim().slice(0,80),title:e.title,aria:e.getAttribute('aria-label'),disabled:e.disabled,cls:(typeof e.className==='string'?e.className:'').slice(0,120)})).slice(0,80)}})()`);
const shot=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await writeFile(dir+'/task424-terminal-ui-20261007.png',Buffer.from(shot.data,'base64'));
await writeFile(dir+'/task424-terminal-ui-20261007.json',JSON.stringify({at:new Date().toISOString(),pid:chrome.pid,clicked,net:net.slice(-60),state},null,2));
console.log(JSON.stringify({ok:true,clicked,url:state.url,text:state.text,inputs:state.inputs,net:net.slice(-30)},null,2));
await writeFile(dir+'/browser-owned.json',JSON.stringify({pid:chrome.pid,profile,cdpPort:port,scope:'T05-T09 task-owned browser only',startedAt:new Date().toISOString()},null,2)); console.log('OWNED_BROWSER_READY '+chrome.pid+' '+port); await new Promise(resolve=>chrome.once('exit',resolve)); ws.close();
