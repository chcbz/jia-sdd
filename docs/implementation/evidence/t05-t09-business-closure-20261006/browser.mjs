import {spawn} from 'node:child_process';
import {mkdir,mkdtemp,readFile,writeFile} from 'node:fs/promises';
import {createInterface} from 'node:readline';
import WebSocket from '/home/isp/wsps/cyf/web/node_modules/ws/index.js';
const dir='/home/isp/wsps/cyf/docs/implementation/evidence/t05-t09-business-closure-20261006';
const profile=process.env.CYF_TASK_BROWSER_PROFILE || await mkdtemp('/var/tmp/cyf-t05-t09-browser-');
const previousPortFile=await readFile(profile+'/DevToolsActivePort','utf8').catch(()=>null);
const chrome=spawn('/usr/bin/chromium-browser',['--no-sandbox','--headless=new','--disable-gpu','--disable-component-update','--no-first-run','--no-default-browser-check','--remote-debugging-address=127.0.0.1','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--window-size=1440,1000','about:blank'],{stdio:['ignore','ignore','pipe']});
let stderr='';chrome.stderr.on('data',b=>{stderr=(stderr+b.toString()).slice(-4096)});
let port;for(let i=0;i<200;i++){try{const active=await readFile(profile+'/DevToolsActivePort','utf8');if(active!==previousPortFile){const candidate=active.split('\n')[0];const ready=await fetch(`http://127.0.0.1:${candidate}/json/version`);if(ready.ok){port=candidate;break}}}catch{}if(chrome.exitCode!==null)throw Error('CHROME_EXIT:'+chrome.exitCode);await new Promise(r=>setTimeout(r,100))}
if(!port)throw Error('CHROME_START_NOT_OBSERVED');
const target=await(await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json();const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.once('open',r);ws.once('error',j)});
let seq=0;const pending=new Map();const observed=[];
ws.on('message',raw=>{const m=JSON.parse(raw);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);clearTimeout(p.t);m.error?p.j(Error(m.error.message)):p.r(m.result)}}else if(m.method==='Network.responseReceived'){const response=m.params.response;const url=new URL(response.url);if(url.protocol.startsWith('http'))observed.push({origin:url.origin,path:url.pathname,status:response.status,type:m.params.type})}});
const send=(method,params={})=>new Promise((r,j)=>{const id=++seq;const t=setTimeout(()=>{pending.delete(id);j(Error('CDP_TRANSPORT_TIMEOUT:'+method))},45000);pending.set(id,{r,j,t});ws.send(JSON.stringify({id,method,params}))});
await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
await mkdir(dir+'/downloads',{recursive:true,mode:0o700});
await send('Browser.setDownloadBehavior',{behavior:'allow',downloadPath:dir+'/downloads',eventsEnabled:true});
await writeFile(dir+'/browser-owned.json',JSON.stringify({pid:chrome.pid,profile,cdpPort:port,scope:'only this browser; no runtime service control'},null,2));console.log(JSON.stringify({ready:true,pid:chrome.pid}));
for await(const line of createInterface({input:process.stdin,terminal:false})){if(!line.trim())continue;try{const req=JSON.parse(line);let result;if(req.op==='navigate'){result=await send('Page.navigate',{url:req.url})}else if(req.op==='evaluate'){const r=await send('Runtime.evaluate',{expression:req.expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(r.exceptionDetails.text);result=r.result?.value}else if(req.op==='screenshot'){if(!/^[a-zA-Z0-9_-]+$/.test(req.name))throw Error('BAD_NAME');const r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await writeFile(dir+'/'+req.name+'.png',Buffer.from(r.data,'base64'));result={path:dir+'/'+req.name+'.png'}}else if(req.op==='network'){result=observed.slice(-40)}else if(req.op==='close'){await send('Browser.close').catch(()=>{});ws.close();await new Promise(resolve=>chrome.exitCode!==null?resolve():chrome.once('exit',resolve));console.log(JSON.stringify({closed:true,pid:chrome.pid,exitCode:chrome.exitCode}));process.exit(0)}else throw Error('UNKNOWN_OP');console.log(JSON.stringify({ok:true,result}))}catch(e){console.log(JSON.stringify({ok:false,error:e.message}))}}
