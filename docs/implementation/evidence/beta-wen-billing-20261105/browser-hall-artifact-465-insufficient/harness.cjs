const {spawn}=require('child_process'),fs=require('fs');
const WebSocket=require('/home/isp/wsps/worktrees/beta-wen-billing-runtime/conf/codex-bridge/node_modules/ws');
const root='/tmp/cyf-beta-retirement-20261106/chromium-hall-artifact-465-insufficient',E='/home/isp/wsps/cyf/docs/implementation/evidence/beta-wen-billing-20261105/browser-hall-artifact-465-insufficient';
const task={id:'task',taskVersion:'7',title:'内测报价验收事项',description:'核对事项报价与承办入口',status:'open',requiredAbilities:[],assignedAgentIds:[]};
const recommendation=JSON.parse(fs.readFileSync('/home/isp/wsps/worktrees/beta-wen-billing-web/tests/fixtures/billing/task-recommendation-quote.json','utf8')).data;
const pause=ms=>new Promise(r=>setTimeout(r,ms));
(async()=>{const child=spawn('/usr/bin/chromium-browser',['--headless','--no-sandbox','--disable-gpu','--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1','--no-first-run','--no-default-browser-check','--remote-debugging-port=0','--user-data-dir='+root,'about:blank'],{stdio:'ignore'});let ws;try {
for(let n=0;!fs.existsSync(root+'/DevToolsActivePort');n++){if(n>100)throw Error('browser startup unavailable');await pause(100)}
const port=fs.readFileSync(root+'/DevToolsActivePort','utf8').split('\n')[0];const pages=await(await fetch('http://127.0.0.1:'+port+'/json')).json();ws=new WebSocket(pages.find(p=>p.type==='page').webSocketDebuggerUrl);await new Promise((r,j)=>{ws.once('open',r);ws.once('error',j)});
let scenario='available';let seq=0;const pending=new Map(),errors=[],requests=[];const call=(method,params={})=>new Promise((resolve,reject)=>{const id=++seq;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))});
ws.on('message',bytes=>{const m=JSON.parse(bytes);if(m.id){const p=pending.get(m.id);if(p){pending.delete(m.id);m.error?p.reject(Error(m.error.message)):p.resolve(m.result)}}else if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails.text);else if(m.method==='Fetch.requestPaused'){(async()=>{
 const p=m.params,u=new URL(p.request.url);if(u.origin==='http://127.0.0.1:55133'){await call('Fetch.continueRequest',{requestId:p.requestId});return}
 requests.push({method:p.request.method,path:u.pathname,payload:p.request.postData?JSON.parse(p.request.postData):null});
 const headers={'Access-Control-Allow-Origin':'http://127.0.0.1:55133','Access-Control-Allow-Methods':'GET,POST,OPTIONS','Access-Control-Allow-Headers':'authorization,content-type,x-request-id,x-client-id,idempotency-key','Access-Control-Allow-Credentials':'true','Access-Control-Expose-Headers':'X-Request-Id','Content-Type':'application/json'};
 let data={},status=200;
 if(u.pathname==='/economy/capabilities')data={economyPreviewEnabled:true,skillMarketplaceEnabled:false,principalScopeSha256:'a'.repeat(64)};
 else if(u.pathname==='/economy/wallet')data={available:{currency:'WEN',amountMinor:'3500'},held:{currency:'WEN',amountMinor:'13'}};
 else if(u.pathname==='/economy/ledger')data={items:[]};
 else if(u.pathname==='/user/my')data={tenantId:'fixture-tenant',id:'fixture-owner',jiacn:'fixture-owner',nickname:'内测验收'};
 else if(u.pathname==='/agent/roster')data={items:[{agentId:'fixture-agent',name:'内测好汉',status:'offline',boundToMe:true,canOperate:true,systemAgent:false,abilities:['内容管理']}],total:'1',pageNum:1,pageSize:100};
 else if(u.pathname==='/agent/map'||u.pathname==='/agent/personas/catalog')data=[];
 else if(u.pathname==='/economy/events')data={grants:[]};
 else if(u.pathname==='/agent/tasks/search')data={items:[task],total:'1',pageNum:1,pageSize:20};
 else if(u.pathname==='/agent/tasks/status-counts')data={phaseCounts:{PENDING_ASSIGNMENT:'0',IN_PROGRESS:'0',PENDING_ACCEPTANCE:'0',UNKNOWN:'0',COMPLETED:'0',HISTORY:'0',total:'0'},rawStatusCounts:{total:'0'}};
 else if(u.pathname==='/agent/fixture-agent/profile-capabilities')data={agentId:'fixture-agent',executionModel:'gpt-6-luna',observedAt:10000,lastSeenAt:10000,abilities:['内容管理'],skills:{status:'AVAILABLE',catalogRevision:'1',reasonCode:null,items:[]}};
 else if(u.pathname==='/agent/tasks/task')data=task;
 else if(u.pathname==='/agent/tasks/task/requirements/current')data={taskId:'task',taskVersion:'7',requirementRevision:'3',title:task.title,description:task.description,contentSha256:'a'.repeat(64),source:'CREATE'};
 else if(u.pathname==='/agent/tasks/task/point-and-deliberate'){status=409;data=null;}
 else if(u.pathname==='/agent/tasks/task/recommend')data=scenario==='available'?recommendation:{...recommendation,recommendations:recommendation.recommendations.map(r=>({...r,quote:{state:'UNAVAILABLE',quoteId:null,recommendationId:'recommendation-1',amount:null,unavailableReason:'MODEL_PRICE_MISSING'}}))};
 else if(u.pathname==='/agent/tasks/task/assignee-candidates')data={items:[{agentId:'a',displayName:'Agent',providerDisplayName:null,isMine:true,availability:'online'}],nextAfterAgentId:null};
 else status=503;
 const requestId=Object.entries(p.request.headers).find(([k])=>k.toLowerCase()==='x-request-id')?.[1]||'browser-fixture';headers['X-Request-Id']=requestId;
 await call('Fetch.fulfillRequest',{requestId:p.requestId,responseCode:p.request.method==='OPTIONS'?204:status,responseHeaders:Object.entries(headers).map(([name,value])=>({name,value})),body:Buffer.from(p.request.method==='OPTIONS'?'':JSON.stringify({protocolVersion:1,requestId,code:status===200?'E0':status===409?'TASK_FUNDS_INSUFFICIENT':'FIXTURE_UNAVAILABLE',msg:status===409?'Available balance is insufficient for the selected task quotation':'fixture',data})).toString('base64')});
})().catch(e=>errors.push(e.message))}});
await call('Page.enable');await call('Runtime.enable');await call('Fetch.enable',{patterns:[{urlPattern:'*'}]});
await call('Page.addScriptToEvaluateOnNewDocument',{source:`localStorage.setItem('api_token',JSON.stringify({data:'synthetic-browser-fixture',expTime:Date.now()+3600000}));`});
const results=[];
for(const [name,width,height,state] of [['desktop-available',1440,1000,'available'],['mobile-available',390,844,'available']]){scenario=state;
 await call('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:width===390});
 await call('Page.navigate',{url:'http://127.0.0.1:55133/juyiting'});
 for(let n=0;n<100;n++){const v=await call('Runtime.evaluate',{expression:"document.querySelector('.wallet-balances')?.innerText || ''",returnByValue:true});if(n>=30)break;await pause(100)}
 await call('Runtime.evaluate',{expression:`document.querySelector('[aria-label="稍后查看新手引导"]')?.click()`});
 await call('Runtime.evaluate',{expression:`[...document.querySelectorAll('[data-workbench-tab="tasks"]')].find(e=>e.getBoundingClientRect().width>0)?.click()`}); await pause(700);
 await call('Runtime.evaluate',{expression:`document.querySelector('.task-card')?.click()`}); await pause(700);
 for(let n=0;n<40;n++){const t=await call('Runtime.evaluate',{expression:"Boolean(document.querySelector('.matter-candidate-card'))",returnByValue:true});if(t.result.value)break;await pause(100)}
 await call('Runtime.evaluate',{expression:"document.querySelector('.matter-candidate-card')?.click()"});await pause(300);

 await call('Runtime.evaluate',{expression:"document.querySelector('.matter-primary-action')?.click()"});await pause(1000);
 const r=await call('Runtime.evaluate',{expression:`JSON.stringify({path:location.pathname,width:innerWidth,scrollWidth:document.documentElement.scrollWidth,title:document.querySelector('#wallet-title')?.textContent,balances:document.querySelector('.wallet-balances')?.innerText,quote:document.querySelector('.matter-quote')?.textContent,confirmDisabled:document.querySelector('.matter-primary-action')?.disabled,confirmText:document.querySelector('.matter-primary-action')?.innerText,text:document.body.innerText})`,returnByValue:true});results.push({name,state,...JSON.parse(r.result.value)});
 const image=await call('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});fs.writeFileSync(E+'/'+name+'.png',Buffer.from(image.data,'base64'));
}
fs.writeFileSync(E+'/checks.json',JSON.stringify({scope:'immutable Web465 production bundle with intercepted synthetic HTTP fixtures; not real backend or production acceptance',source:'0407d2582386982c0e4d759810e533f2e383db04',results,errors,requests},null,2)+'\n');console.log(JSON.stringify({results,errors,requests}));if(errors.length||results.some(r=>!r.text.includes('可用文余额不足，无法确认承办；本次未预占费用。')||r.scrollWidth>r.width)||requests.filter(r=>r.method==='POST'&&r.path.endsWith('/point-and-deliberate')).length!==2)process.exitCode=1;
}finally{ws?.close();child.kill('SIGTERM')}})().catch(e=>{console.error(e.message);process.exitCode=1});
