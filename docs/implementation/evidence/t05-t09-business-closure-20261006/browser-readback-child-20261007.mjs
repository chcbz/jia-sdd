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
await send('Page.navigate',{url:'https://kit.chaoyoufan.cn/juyiting'});await new Promise(r=>setTimeout(r,4000));
const apiBase='https://api.chaoyoufan.cn';
const get=async path=>evalv(`(async()=>{const raw=localStorage.getItem('api_token');if(!raw)return {status:0,ok:false,data:null,error:'no_api_token'};let token='';try{token=JSON.parse(raw)?.data||''}catch{token=raw}if(!token)return {status:0,ok:false,data:null,error:'empty_token'};try{const res=await fetch(${JSON.stringify(apiBase+path)},{headers:{Accept:'application/json',Authorization:'Bearer '+token,'Content-Type':'application/json'}});const text=await res.text();let data;try{data=JSON.parse(text)}catch{data={__text:text.slice(0,800)}}return {status:res.status,ok:res.ok,data}}catch(e){return {status:0,ok:false,data:null,error:e.message}}})()`);
const parent='mmd-typed-request_2502196aeba31a18770e1ed99764f2c5457211ce';
const child='action-inspect_3b984649450f9d1509627c3d3f5da45777769ea9';
const readback={
  at:new Date().toISOString(),
  apiBase,
  parent,
  child,
  parentRequest:await get(`/chat/requests/${parent}`),
  parentTyped:await get(`/chat/conversations/1760458004867/requests/${parent}/typed-outcome`),
  childRequest:await get(`/chat/requests/${child}`),
  childInspection:await get(`/chat/conversations/1760458004867/requests/${child}/inspection-outcome`),
  childTyped:await get(`/chat/conversations/1760458004867/requests/${child}/typed-outcome`),
  browserPid:chrome.pid
};
await writeFile(dir+'/task424-fixed-send-child-readback-20261007.json',JSON.stringify(readback,null,2));
console.log(JSON.stringify({ok:true,parentRequest:{status:readback.parentRequest.status,state:readback.parentRequest.data?.data?.state},parentTyped:{status:readback.parentTyped.status,state:readback.parentTyped.data?.data?.state,actionState:readback.parentTyped.data?.data?.actionProgress?.state,childId:readback.parentTyped.data?.data?.actionProgress?.childRequestId},childRequest:{status:readback.childRequest.status,state:readback.childRequest.data?.data?.state,turns:readback.childRequest.data?.data?.turns},childInspection:{status:readback.childInspection.status,state:readback.childInspection.data?.data?.state,outcome:readback.childInspection.data?.data?.outcome,inspection:readback.childInspection.data?.data?.inspection},childTypedStatus:readback.childTyped.status},null,2));
await send('Browser.close').catch(()=>{});ws.close();try{await new Promise(resolve=>chrome.exitCode!==null?resolve():chrome.once('exit',resolve))}catch{}process.exit(0);
