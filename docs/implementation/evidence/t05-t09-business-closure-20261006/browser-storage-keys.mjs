import {spawn} from 'node:child_process';
import {readFile,rm} from 'node:fs/promises';
import WebSocket from '/home/isp/wsps/cyf/web/node_modules/ws/index.js';
const profile='/var/tmp/cyf-t05-t09-browser-W7vzug';
for(const p of ['SingletonLock','SingletonCookie','SingletonSocket']){try{await rm(profile+'/'+p,{force:true})}catch{}}
const chrome=spawn('/usr/bin/chromium-browser',['--no-sandbox','--headless=new','--disable-gpu','--disable-component-update','--no-first-run','--no-default-browser-check','--remote-debugging-address=127.0.0.1','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--window-size=1440,1000','about:blank'],{stdio:['ignore','ignore','pipe']});
let port;for(let i=0;i<300;i++){try{const a=await readFile(profile+'/DevToolsActivePort','utf8');const c=a.split('\n')[0];if((await fetch(`http://127.0.0.1:${c}/json/version`)).ok){port=c;break}}catch{}if(chrome.exitCode!==null)throw Error('exit');await new Promise(r=>setTimeout(r,100))}
const target=await(await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json();
const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.once('open',r);ws.once('error',j)});
let seq=0;const pending=new Map();ws.on('message',raw=>{const m=JSON.parse(raw);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);clearTimeout(p.t);m.error?p.j(Error(m.error.message)):p.r(m.result)}}});
const send=(method,params={})=>new Promise((r,j)=>{const id=++seq;const t=setTimeout(()=>j(Error('timeout')),60000);pending.set(id,{r,j,t});ws.send(JSON.stringify({id,method,params}))});
const evalv=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(r.exceptionDetails.text);return r.result?.value};
await send('Page.enable');await send('Runtime.enable');
await send('Page.navigate',{url:'https://kit.chaoyoufan.cn/juyiting'});await new Promise(r=>setTimeout(r,4000));
const out=await evalv(`(()=>{const ls={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);ls[k]=localStorage.getItem(k)?.length}const ss={};for(let i=0;i<sessionStorage.length;i++){const k=sessionStorage.key(i);ss[k]=sessionStorage.getItem(k)?.length}return {origin:location.origin,localStorageKeys:Object.keys(ls),localStorageLengths:ls,sessionStorageKeys:Object.keys(ss),sessionStorageLengths:ss,cookies:document.cookie.split(';').map(x=>x.trim().split('=')[0]).filter(Boolean)}})()`);
console.log(JSON.stringify(out,null,2));
await send('Browser.close').catch(()=>{});ws.close();try{await new Promise(resolve=>chrome.exitCode!==null?resolve():chrome.once('exit',resolve))}catch{}process.exit(0);
