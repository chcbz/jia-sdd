const {spawn}=require('child_process'),fs=require('fs');
const WebSocket=require('/home/isp/wsps/worktrees/beta-wen-billing-runtime/conf/codex-bridge/node_modules/ws');
const root='/tmp/cyf-beta-retirement-20261106/chromium-wallet-artifact-464',E='/home/isp/wsps/cyf/docs/implementation/evidence/beta-wen-billing-20261105/browser-wallet-artifact-464';
const pause=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const child=spawn('/usr/bin/chromium-browser',['--headless','--no-sandbox','--disable-gpu','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+root,'about:blank'],{stdio:'ignore'});let ws;try {
for(let n=0;!fs.existsSync(root+'/DevToolsActivePort');n++){if(n>100)throw Error('browser startup unavailable');await pause(100)}
const port=fs.readFileSync(root+'/DevToolsActivePort','utf8').split('\n')[0];const pages=await(await fetch('http://127.0.0.1:'+port+'/json')).json();ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.once('open',r);ws.once('error',j)});
let seq=0;const pending=new Map(),errors=[],requests=[];const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
ws.on('message',bytes=>{const m=JSON.parse(bytes);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);m.error?p.reject(Error(m.error.message)):p.resolve(m.result)}}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text);else if(m.method==='Fetch.requestPaused'){(async()=>{
 const p=m.params,u=new URL(p.request.url);if(u.origin==='http://127.0.0.1:41393'){await call('Fetch.continueRequest',{requestId:p.requestId});return}
 requests.push({method:p.request.method,path:u.pathname});
 const headers={'Access-Control-Allow-Origin':'http://127.0.0.1:41393','Access-Control-Allow-Methods':'GET,POST,OPTIONS','Access-Control-Allow-Headers':'authorization,content-type,x-request-id,x-client-id','Access-Control-Allow-Credentials':'true','Access-Control-Expose-Headers':'X-Request-Id','Content-Type':'application/json'};
 let data={},status=200;
 if(u.pathname==='/economy/capabilities')data={economyPreviewEnabled:true,skillMarketplaceEnabled:false,principalScopeSha256:'a'.repeat(64)};
 else if(u.pathname==='/economy/wallet')data={available:{currency:'WEN',amountMinor:'3500'},held:{currency:'WEN',amountMinor:'13'}};
 else if(u.pathname==='/economy/ledger')data={items:[]};
 else status=503;
 const requestId=Object.entries(p.request.headers).find(([k])=>k.toLowerCase()==='x-request-id')?.[1]||'browser-fixture';headers['X-Request-Id']=requestId;
 await call('Fetch.fulfillRequest',{requestId:p.requestId,responseCode:p.request.method==='OPTIONS'?204:status,responseHeaders:Object.entries(headers).map(([name,value])=>({name,value})),body:Buffer.from(p.request.method==='OPTIONS'?'':JSON.stringify({protocolVersion:1,requestId,code:status===200?'E0':'FIXTURE_UNAVAILABLE',msg:'fixture',data})).toString('base64')});
})().catch(e=>errors.push(e.message))}});
await call('Page.enable');await call('Runtime.enable');await call('Fetch.enable',{patterns:[{urlPattern:'*'}]});
await call('Page.addScriptToEvaluateOnNewDocument',{source:`localStorage.setItem('api_token',JSON.stringify({data:'synthetic-browser-fixture',expTime:Date.now()+3600000}));`});
const results=[];
for(const [name,width,height] of [['desktop',1440,1000],['mobile',390,844]]){
 await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:name==='mobile'});
 await call('Page.navigate',{url:'http://127.0.0.1:41393/wallet'});
 for(let n=0;n<100;n++){const v=await call('Runtime.evaluate',{expression:"document.querySelector('.wallet-balances')?.innerText || ''",returnByValue:true});if(v.result.value.includes('3500')||v.result.value.includes('3,500'))break;await pause(100)}
 const r=await call('Runtime.evaluate',{expression:`JSON.stringify({path:location.pathname,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,title:document.querySelector('#wallet-title')?.textContent,balances:document.querySelector('.wallet-balances')?.innerText,text:document.querySelector('.wallet-page')?.innerText})`,returnByValue:true});results.push({name,...JSON.parse(r.result.value)});
 const image=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(E+'/'+name+'.png',Buffer.from(image.data,'base64'));
}
fs.writeFileSync(E+'/checks.json',JSON.stringify({scope:'immutable Web464 production bundle with intercepted synthetic HTTP fixtures; not real backend or production acceptance',source:'fa957871ada3ec389c53582caa6512d31108e553',results,errors,requests},null,2)+'\n');console.log(JSON.stringify({results,errors,requests}));if(errors.length||results.some(r=>r.width<r.scrollWidth||r.title!=='钱袋 · 文'||!/13\s*文/.test(r.balances || '')||r.text.includes('银两')))process.exitCode=1;
}finally{ws?.close();child.kill('SIGTERM')}})().catch(e=>{console.error(e.message);process.exitCode=1});
