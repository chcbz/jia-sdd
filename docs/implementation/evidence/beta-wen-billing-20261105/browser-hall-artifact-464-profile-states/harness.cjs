const {spawn}=require('child_process'),fs=require('fs');
const WebSocket=require('/home/isp/wsps/worktrees/beta-wen-billing-runtime/conf/codex-bridge/node_modules/ws');
const root='/tmp/cyf-beta-retirement-20261106/chromium-hall-artifact-464-profile-states',E='/home/isp/wsps/cyf/docs/implementation/evidence/beta-wen-billing-20261105/browser-hall-artifact-464-profile-states';
const pause=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const child=spawn('/usr/bin/chromium-browser',['--headless','--no-sandbox','--disable-gpu','--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+root,'about:blank'],{stdio:'ignore'});let ws;try {
for(let n=0;!fs.existsSync(root+'/DevToolsActivePort');n++){if(n>100)throw Error('browser startup unavailable');await pause(100)}
const port=fs.readFileSync(root+'/DevToolsActivePort','utf8').split('\n')[0];const pages=await(await fetch('http://127.0.0.1:'+port+'/json')).json();ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.once('open',r);ws.once('error',j)});
let scenario='missing';let seq=0;const pending=new Map(),errors=[],requests=[];const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
ws.on('message',bytes=>{const m=JSON.parse(bytes);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);m.error?p.reject(Error(m.error.message)):p.resolve(m.result)}}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text);else if(m.method==='Fetch.requestPaused'){(async()=>{
 const p=m.params,u=new URL(p.request.url);if(u.origin==='http://127.0.0.1:37673'){await call('Fetch.continueRequest',{requestId:p.requestId});return}
 requests.push({method:p.request.method,path:u.pathname});
 const headers={'Access-Control-Allow-Origin':'http://127.0.0.1:37673','Access-Control-Allow-Methods':'GET,POST,OPTIONS','Access-Control-Allow-Headers':'authorization,content-type,x-request-id,x-client-id','Access-Control-Allow-Credentials':'true','Access-Control-Expose-Headers':'X-Request-Id','Content-Type':'application/json'};
 let data={},status=200;
 if(u.pathname==='/economy/capabilities')data={economyPreviewEnabled:true,skillMarketplaceEnabled:false,principalScopeSha256:'a'.repeat(64)};
 else if(u.pathname==='/economy/wallet')data={available:{currency:'WEN',amountMinor:'3500'},held:{currency:'WEN',amountMinor:'13'}};
 else if(u.pathname==='/economy/ledger')data={items:[]};
 else if(u.pathname==='/user/my')data={tenantId:'fixture-tenant',id:'fixture-owner',jiacn:'fixture-owner',nickname:'内测验收'};
 else if(u.pathname==='/agent/roster')data={items:[{agentId:'fixture-agent',name:'内测好汉',status:'offline',boundToMe:scenario!=='nonowner',canOperate:scenario!=='nonowner',systemAgent:false,abilities:['内容管理']}],total:'1',pageNum:1,pageSize:100};
 else if(u.pathname==='/agent/map'||u.pathname==='/agent/personas/catalog')data=[];
 else if(u.pathname==='/economy/events')data={grants:[]};
 else if(u.pathname==='/agent/tasks/search')data={items:[],total:'0',pageNum:1,pageSize:20};
 else if(u.pathname==='/agent/tasks/status-counts')data={phaseCounts:{PENDING_ASSIGNMENT:'0',IN_PROGRESS:'0',PENDING_ACCEPTANCE:'0',UNKNOWN:'0',COMPLETED:'0',HISTORY:'0',total:'0'},rawStatusCounts:{total:'0'}};
 else if(u.pathname==='/agent/fixture-agent/profile-capabilities')data={agentId:'fixture-agent',executionModel:null,observedAt:10000,lastSeenAt:10000,abilities:['内容管理'],skills:{status:'AVAILABLE',catalogRevision:'1',reasonCode:null,items:[]}};
 else status=503;
 if(u.pathname==='/agent/fixture-agent/profile-capabilities'&&scenario==='error')status=503;
 const requestId=Object.entries(p.request.headers).find(([k])=>k.toLowerCase()==='x-request-id')?.[1]||'browser-fixture';headers['X-Request-Id']=requestId;
 await call('Fetch.fulfillRequest',{requestId:p.requestId,responseCode:p.request.method==='OPTIONS'?204:status,responseHeaders:Object.entries(headers).map(([name,value])=>({name,value})),body:Buffer.from(p.request.method==='OPTIONS'?'':JSON.stringify({protocolVersion:1,requestId,code:status===200?'E0':'FIXTURE_UNAVAILABLE',msg:'fixture',data})).toString('base64')});
})().catch(e=>errors.push(e.message))}});
await call('Page.enable');await call('Runtime.enable');await call('Fetch.enable',{patterns:[{urlPattern:'*'}]});
await call('Page.addScriptToEvaluateOnNewDocument',{source:`localStorage.setItem('api_token',JSON.stringify({data:'synthetic-browser-fixture',expTime:Date.now()+3600000}));`});
const results=[];
for(const [name,width,height,state] of [['desktop-missing',1440,1000,'missing'],['mobile-missing',390,844,'missing'],['desktop-error',1440,1000,'error'],['mobile-error',390,844,'error'],['desktop-nonowner',1440,1000,'nonowner'],['mobile-nonowner',390,844,'nonowner']]){
 scenario=state;
 await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width===390});
 await call('Page.navigate',{url:'http://127.0.0.1:37673/juyiting'});
 for(let n=0;n<100;n++){const v=await call('Runtime.evaluate',{expression:"document.querySelector('.wallet-balances')?.innerText || ''",returnByValue:true});if(n>=30)break;await pause(100)}
 await call('Runtime.evaluate',{expression:`document.querySelector('[aria-label="稍后查看新手引导"]')?.click()`});
 await call('Runtime.evaluate',{expression:`[...document.querySelectorAll('button')].find(e=>e.innerText.trim()==='查看好汉名册')?.click()`}); await pause(700);
 await call('Runtime.evaluate',{expression:`document.querySelector('[data-agent-id="fixture-agent"]')?.click()`}); await pause(700);
 for(let n=0;n<40;n++){const t=await call('Runtime.evaluate',{expression:"document.querySelector('.profile-model')?.textContent",returnByValue:true});if(t.result.value==='暂未上报'||n>=10)break;await pause(100)}
 const r=await call('Runtime.evaluate',{expression:`JSON.stringify({path:location.pathname,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,title:document.querySelector('#wallet-title')?.textContent,balances:document.querySelector('.wallet-balances')?.innerText,model:document.querySelector('[aria-label="使用模型"]')?.innerText,text:document.body.innerText})`,returnByValue:true});results.push({name,state,...JSON.parse(r.result.value)});
 const image=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(E+'/'+name+'.png',Buffer.from(image.data,'base64'));
}
fs.writeFileSync(E+'/checks.json',JSON.stringify({scope:'immutable Web464 production bundle with intercepted synthetic HTTP fixtures; not real backend or production acceptance',source:'fa957871ada3ec389c53582caa6512d31108e553',results,errors,requests},null,2)+'\n');console.log(JSON.stringify({results,errors,requests}));if(errors.length||results.some(r=>!r.model?.includes({missing:'暂未上报',error:'模型读取失败，可刷新重试',nonowner:'仅拥有者可查看模型'}[r.state])||r.scrollWidth>r.width))process.exitCode=1;
}finally{ws?.close();child.kill('SIGTERM')}})().catch(e=>{console.error(e.message);process.exitCode=1});
