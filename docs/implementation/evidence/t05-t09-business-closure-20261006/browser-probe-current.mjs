import {spawn} from 'node:child_process';
import {readFile,writeFile,rm} from 'node:fs/promises';
import WebSocket from '/home/isp/wsps/cyf/web/node_modules/ws/index.js';

const dir='/home/isp/wsps/cyf/docs/implementation/evidence/t05-t09-business-closure-20261006';
const profile='/var/tmp/cyf-t05-t09-browser-W7vzug';
for(const p of ['SingletonLock','SingletonCookie','SingletonSocket']){try{await rm(profile+'/'+p,{force:true})}catch{}}
const chrome=spawn('/usr/bin/chromium-browser',['--no-sandbox','--headless=new','--disable-gpu','--disable-component-update','--no-first-run','--no-default-browser-check','--remote-debugging-address=127.0.0.1','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--window-size=1440,1000','about:blank'],{stdio:['ignore','ignore','pipe']});
let stderr='';chrome.stderr.on('data',b=>{stderr=(stderr+b.toString()).slice(-4096)});
let port;
for(let i=0;i<300;i++){
  try{
    const active=await readFile(profile+'/DevToolsActivePort','utf8');
    const candidate=active.split('\n')[0];
    const ready=await fetch(`http://127.0.0.1:${candidate}/json/version`);
    if(ready.ok){port=candidate;break}
  }catch{}
  if(chrome.exitCode!==null) throw Error('CHROME_EXIT:'+chrome.exitCode);
  await new Promise(r=>setTimeout(r,100));
}
if(!port) throw Error('CHROME_START_NOT_OBSERVED: '+stderr.slice(-500));
const target=await(await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json();
const ws=new WebSocket(target.webSocketDebuggerUrl);
await new Promise((r,j)=>{ws.once('open',r);ws.once('error',j)});
let seq=0;const pending=new Map();
ws.on('message',raw=>{const m=JSON.parse(raw);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);clearTimeout(p.t);m.error?p.j(Error(m.error.message)):p.r(m.result)}}});
const send=(method,params={})=>new Promise((r,j)=>{const id=++seq;const t=setTimeout(()=>{pending.delete(id);j(Error('CDP_TRANSPORT_TIMEOUT:'+method))},60000);pending.set(id,{r,j,t});ws.send(JSON.stringify({id,method,params}))});
const evalv=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error('PAGE_EVAL_FAILED: '+(r.exceptionDetails.exception?.description||r.exceptionDetails.text));return r.result?.value};
await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
await send('Page.navigate',{url:'https://kit.chaoyoufan.cn/juyiting'});
await new Promise(r=>setTimeout(r,6000));
const state=await evalv(`(async()=>{
  const wait=ms=>new Promise(r=>setTimeout(r,ms));
  for(let i=0;i<20;i++){if(document.readyState==='complete' && document.body && document.body.innerText.length>0) break; await wait(300)}
  const token=localStorage.getItem('apiToken')||localStorage.getItem('token')||localStorage.getItem('access_token')||null;
  const cards=[...document.querySelectorAll('div,li,button')].map(e=>({tag:e.tagName,text:(e.innerText||'').trim().slice(0,80),title:e.title,aria:e.getAttribute('aria-label'),cls:(typeof e.className==='string'?e.className:'').slice(0,80)})).filter(x=>x.text.includes('图文闭环')||x.text.includes('查看进展')||x.text.includes('T05–T09')).slice(0,30);
  return {url:location.href,path:location.pathname,ready:document.readyState,title:document.title,text:document.body.innerText.slice(0,8000),token:!!token,login:!!document.querySelector('input[type=password],input[placeholder="密码"]'),cards};
})()`);
await writeFile(dir+'/browser-probe-current.json',JSON.stringify({at:new Date().toISOString(),pid:chrome.pid,profile,cdpPort:port,state},null,2));
console.log(JSON.stringify({ok:true,pid:chrome.pid,port,url:state.url,ready:state.ready,title:state.title,login:state.login,token:state.token,cards:state.cards.length,textLen:state.text.length},null,2));
await send('Browser.close').catch(()=>{});ws.close();
try{await new Promise(resolve=>chrome.exitCode!==null?resolve():chrome.once('exit',resolve))}catch{}
process.exit(0);
