import {spawn} from 'node:child_process';
import {readFile,writeFile,rm} from 'node:fs/promises';
import WebSocket from '/home/isp/wsps/cyf/web/node_modules/ws/index.js';

const dir='/home/isp/wsps/cyf/docs/implementation/evidence/t05-t09-business-closure-20261006';
const profile='/var/tmp/cyf-t05-t09-browser-W7vzug';
const CONVERSATION_ID='1760458004867';
const TASK_ID='424';
const TASK_TITLE='T05–T09图文闭环-20261006：阅读所附图片与文本';
const NEW_MESSAGE='20261007-修复后独立再验证：请读取随本条消息发送的既有图片与文本资料，按从左到右依次描述图片中对象的颜色、形状与数量，并逐字引用文本中的验证短语。只回答现有资料，不生成或修改文件。';

for(const p of ['SingletonLock','SingletonCookie','SingletonSocket']){try{await rm(profile+'/'+p,{force:true})}catch{}}
const chrome=spawn('/usr/bin/chromium-browser',['--no-sandbox','--headless=new','--disable-gpu','--disable-component-update','--no-first-run','--no-default-browser-check','--remote-debugging-address=127.0.0.1','--remote-debugging-port=0',`--user-data-dir=${profile}`,'--window-size=1440,1000','about:blank'],{stdio:['ignore','ignore','pipe']});
let stderr='';chrome.stderr.on('data',b=>{stderr=(stderr+b.toString()).slice(-4096)});
let port;
for(let i=0;i<300;i++){
  try{const a=await readFile(profile+'/DevToolsActivePort','utf8');const c=a.split('\n')[0];if((await fetch(`http://127.0.0.1:${c}/json/version`)).ok){port=c;break}}catch{}
  if(chrome.exitCode!==null)throw Error('CHROME_EXIT:'+chrome.exitCode);
  await new Promise(r=>setTimeout(r,100));
}
if(!port)throw Error('NO_PORT '+stderr.slice(-400));
const target=await(await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json();
const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise((r,j)=>{ws.once('open',r);ws.once('error',j)});
let seq=0;const pending=new Map();const network=[];
ws.on('message',raw=>{const m=JSON.parse(raw);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);clearTimeout(p.t);m.error?p.j(Error(m.error.message)):p.r(m.result)}}else if(m.method==='Network.requestWillBeSent'){const r=m.params.request;try{const u=new URL(r.url);if(u.protocol.startsWith('http')&&r.method==='POST'){network.push({kind:'request',at:Date.now(),method:r.method,path:u.pathname,postData:r.postData||null,requestId:m.params.requestId})}}catch{}}else if(m.method==='Network.responseReceived'){const r=m.params.response;try{const u=new URL(r.url);if(u.protocol.startsWith('http')){network.push({kind:'response',at:Date.now(),path:u.pathname,status:r.status,type:m.params.type,requestId:m.params.requestId,mime:m.params.response.mimeType})}}catch{}}});
const send=(method,params={})=>new Promise((r,j)=>{const id=++seq;const t=setTimeout(()=>{pending.delete(id);j(Error('TIMEOUT '+method))},120000);pending.set(id,{r,j,t});ws.send(JSON.stringify({id,method,params}))});
const evalv=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error('EVAL_FAIL '+JSON.stringify(r.exceptionDetails));return r.result?.value};
const shot=async name=>{const r=await send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await writeFile(dir+'/'+name+'.png',Buffer.from(r.data,'base64'));return dir+'/'+name+'.png'};
const apiFetchInPage=async path=>{
  try{
    return await evalv(`(async()=>{try{const res=await fetch(${JSON.stringify(path)},{headers:{Accept:'application/json'},credentials:'include'});const text=await res.text();let data;try{data=JSON.parse(text)}catch{data={__text:text.slice(0,1000)}}return {status:res.status,ok:res.ok,data}}catch(e){return {status:0,ok:false,data:null,error:e.message}}})()`);
  }catch(e){return {status:0,ok:false,data:null,error:e.message}}
};

await send('Page.enable');await send('Runtime.enable');await send('Network.enable');
await send('Page.navigate',{url:'https://kit.chaoyoufan.cn/juyiting'});
await new Promise(r=>setTimeout(r,4500));
const clickTask=await evalv(`(()=>{const item=[...document.querySelectorAll('.overview-item')].find(e=>e.querySelector('.overview-item-title strong')?.innerText===${JSON.stringify(TASK_TITLE)});if(!item)return {error:'task item not found'};const btn=item.querySelector('button');if(!btn)return {error:'task button not found'};btn.click();return {clicked:true,title:item.querySelector('.overview-item-title strong').innerText}})()`);
if(clickTask.error)throw Error(clickTask.error);
await new Promise(r=>setTimeout(r,3500));
const openPicker=await evalv(`(async()=>{const wait=ms=>new Promise(r=>setTimeout(r,ms));for(let i=0;i<20;i++){if(document.querySelector('textarea.composer-textarea'))break;await wait(250)}const ta=document.querySelector('textarea.composer-textarea');if(!ta)return {error:'composer missing'};document.querySelector('.composer-more').click();await wait(400);document.querySelector('.composer-add-materials').click();await wait(1800);return {ok:true}})()`);
if(openPicker.error)throw Error(openPicker.error);
const prep=await evalv(`(async()=>{const wait=ms=>new Promise(r=>setTimeout(r,ms));let boxes=[];for(let i=0;i<20;i++){boxes=[...document.querySelectorAll('.material-reference-picker input[type=checkbox]')].filter(b=>b.offsetParent!==null);if(boxes.length===2)break;await wait(250)}if(boxes.length!==2)return {error:'expected 2 visible material checkboxes, got '+boxes.length};
for(const b of boxes){if(!b.checked){b.click();await wait(80)}}
await wait(300);
const ta=document.querySelector('textarea.composer-textarea');
const setter=Object.getOwnPropertyDescriptor(HTMLTextAreaElement.prototype,'value').set;
setter.call(ta,${JSON.stringify(NEW_MESSAGE)});
ta.dispatchEvent(new Event('input',{bubbles:true}));
await wait(500);
const sendBtn=document.querySelector('button.composer-send');
return {checked:boxes.map(b=>b.checked),sendDisabled:sendBtn?.disabled,draft:ta.value,boxCount:boxes.length}})()`);
if(prep.error)throw Error(prep.error);
if(!prep.checked.every(Boolean))throw Error('not all checkboxes checked: '+JSON.stringify(prep.checked));
if(prep.sendDisabled!==false)throw Error('send button still disabled: '+JSON.stringify(prep.sendDisabled));
await shot('task424-fixed-send-before');
const beforeNetIndex=network.length;
const clickedSend=await evalv(`(()=>{const b=document.querySelector('button.composer-send');if(!b||b.disabled)return {error:'send unavailable'};b.click();return {clicked:true}})()`);
if(clickedSend.error)throw Error(clickedSend.error);
const sendAt=Date.now();
const beforeText=await evalv(`document.body.innerText.slice(-3000)`).catch(()=>'');

// Wait for the single typed DISCUSSION POST to be observed. No retry is ever issued.
let postRequest=null;let postResponse=null;
for(let i=0;i<40;i++){
  await new Promise(r=>setTimeout(r,250));
  postRequest=network.find(e=>e.kind==='request'&&e.method==='POST'&&/\/interactions\/discussion$/.test(e.path));
  postResponse=network.find(e=>e.kind==='response'&&e.requestId===postRequest?.requestId);
  if(postRequest&&postResponse)break;
}
let newRequestId=null;let postBodyText=null;let postStatus=postResponse?.status||null;
if(postRequest&&postResponse){
  try{
    const body=await send('Network.getResponseBody',{requestId:postRequest.requestId});
    postBodyText=body.body||null;
    const parsed=JSON.parse(body.body||'{}');
    newRequestId=parsed?.data?.requestId||parsed?.requestId||parsed?.data?.receipt?.requestId||parsed?.receipt?.requestId||null;
  }catch(e){postBodyText=postBodyText||('ERR:'+e.message)}
}
if(!newRequestId){
  // Fallback: newest mmd-typed-request path observed after send in network responses.
  const re=/mmd-typed-request_[A-Za-z0-9]+/;
  for(const e of network.slice(beforeNetIndex)){const m=e.path.match(re);if(m){newRequestId=m[0];break}}
}

const samples=[];
let apiReadbacks=[];
let terminalObserved=false;
let terminalReason='';
let lastReadback=null;
const requestTerminal=new Set(['COMPLETED','FAILED','CANCELLED']);
const timeoutAt=sendAt+180000;
while(Date.now()<timeoutAt){
  await new Promise(r=>setTimeout(r,3000));
  let sample;
  try{sample=await evalv(`(()=>({at:Date.now(),tail:document.body.innerText.slice(-3500),sendDisabled:document.querySelector('button.composer-send')?.disabled,newTextGrew:document.body.innerText.length>${beforeText?beforeText.length+0:0}}))()`)}catch(e){sample={at:Date.now(),error:e.message}}
  samples.push(sample);
  const rb={at:new Date().toISOString(),newRequestId};
  if(newRequestId){
    const [req,typed]=await Promise.all([
      apiFetchInPage(`/chat/requests/${newRequestId}`),
      apiFetchInPage(`/chat/conversations/${CONVERSATION_ID}/requests/${newRequestId}/typed-outcome`)
    ]);
    rb.request=req;rb.typed=typed;
    const reqState=req?.data?.state||null;
    const actionState=typed?.data?.actionProgress?.state||null;
    const typedState=typed?.data?.state||null;
    let childId=typed?.data?.actionProgress?.childRequestId||typed?.data?.inspection?.requestId||null;
    // INSPECT child may be referenced under actionProgress.childRequestId.
    if(!childId){const r=typed?.data?.action?.sourceRefIds; childId=null}
    rb.childId=childId||null;
    if(childId){
      const [childReq,childOut]=await Promise.all([
        apiFetchInPage(`/chat/requests/${childId}`),
        apiFetchInPage(`/chat/conversations/${CONVERSATION_ID}/requests/${childId}/inspection-outcome`)
      ]);
      rb.childRequest=childReq;rb.childInspection=childOut;
      const childState=childReq?.data?.state||null;
      const childOutState=childOut?.data?.state||childOut?.data?.inspection?.state||null;
      if((childState&&requestTerminal.has(childState))||(childOutState&&['COMPLETED','FAILED','CANCELLED'].includes(childOutState))){
        terminalObserved=true;terminalReason='child_terminal';
      }
    }
    if(requestTerminal.has(reqState)&&(!typed?.data?.actionProgress||['COMPLETED','FAILED','CANCELLED'].includes(actionState))){
      terminalObserved=true;terminalReason='request_and_action_terminal';
    } else if(requestTerminal.has(reqState)&&typed?.data?.actionProgress==null){
      terminalObserved=true;terminalReason='request_terminal_no_action';
    } else if(['FAILED','CANCELLED'].includes(reqState)||['FAILED','CANCELLED'].includes(typedState)){
      terminalObserved=true;terminalReason='terminal_failed_or_cancelled';
    }
    lastReadback=rb;
  }
  apiReadbacks.push(rb);
  if(terminalObserved)break;
}
if(terminalObserved) await new Promise(r=>setTimeout(r,4000));
const afterState=await evalv(`(()=>({url:location.href,path:location.pathname,text:document.body.innerText.slice(0,18000),buttons:[...document.querySelectorAll('button')].filter(b=>b.offsetParent!==null).map(b=>({text:(b.innerText||'').trim(),aria:b.getAttribute('aria-label'),title:b.title,disabled:b.disabled})).slice(-40),checkboxes:[...document.querySelectorAll('input[type=checkbox]')].filter(b=>b.offsetParent!==null).map(b=>b.checked)}))()`).catch(e=>({error:e.message}));
await shot('task424-fixed-send-after');
const postEvents=network.slice(beforeNetIndex);
const evidence={
  at:new Date().toISOString(),
  mode:'SINGLE_NEW_BROWSER_DISCUSSION_WITH_EXISTING_TASK_LINKED_INPUTS',
  taskId:TASK_ID,
  conversationId:CONVERSATION_ID,
  taskTitle:TASK_TITLE,
  newMessage:NEW_MESSAGE,
  clickTask,
  prep,
  clickedSend,
  sendAt:new Date(sendAt).toISOString(),
  pollSeconds:(Date.now()-sendAt)/1000,
  beforeText,
  postRequestObserved:!!postRequest,
  postRequestPath:postRequest?.path||null,
  postStatus,
  postBodyText,
  newRequestId,
  terminalObserved,
  terminalReason,
  samples,
  apiReadbacks,
  lastReadback,
  afterState,
  network:postEvents,
  browserPid:chrome.pid,
  chromeStderrTail:stderr.slice(-1000)
};
await writeFile(dir+'/task424-fixed-send-once-20261007.json',JSON.stringify(evidence,null,2));
console.log(JSON.stringify({ok:true,prep,clickedSend,newRequestId,postStatus,postRequestObserved:!!postRequest,terminalObserved,terminalReason,pollSeconds:evidence.pollSeconds,lastReadback:lastReadback&&{reqState:lastReadback.request?.data?.state,actionState:lastReadback.typed?.data?.actionProgress?.state,childId:lastReadback.childId,childReqState:lastReadback.childRequest?.data?.state,childOutState:lastReadback.childInspection?.data?.state||lastReadback.childInspection?.data?.inspection?.state},screenshot:dir+'/task424-fixed-send-after.png'},null,2));
await send('Browser.close').catch(()=>{});ws.close();
try{await new Promise(resolve=>chrome.exitCode!==null?resolve():chrome.once('exit',resolve))}catch{}
process.exit(0);
