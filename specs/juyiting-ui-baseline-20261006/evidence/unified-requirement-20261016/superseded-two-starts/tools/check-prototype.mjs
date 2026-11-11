// Local document checks only; Chromium report is separate and authoritative for layout.
import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import {createRequire} from 'node:module'
import {fileURLToPath} from 'node:url'
const dir=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../prototype')
const evidence=process.env.PROTOTYPE_EVIDENCE_DIR||path.resolve(dir,'../evidence/ui-sync-20261013');fs.mkdirSync(evidence,{recursive:true})
const require=createRequire(path.resolve(process.argv[2]||'/home/isp/wsps/cyf/web/package.json'))
const {JSDOM}=require('jsdom'),results=[]
const pages=['home','tasks','create','agents','detail','chat','private','public','workspace','mine','library','messages','catalog','map','file','reader','help','account','results']
const scenarios=['ready','empty','waiting','streaming','error','recording','voice-review','results','completed','create-failure','create-unknown','reply-failure','accept-unknown','accept-failure','independent-roots','cancel-ready','cancel-unknown','cancelled','history-error','runtime-ready','runtime-existing','runtime-unknown','runtime-invalid']
function create(page,width=390,scenario='ready') {
 const dom=new JSDOM(fs.readFileSync(dir+'/index.html','utf8'),{url:`http://localhost/?scenario=${scenario}#${page}`,runScripts:'outside-only',pretendToBeVisual:true})
 Object.defineProperty(dom.window.HTMLElement.prototype,'innerText',{get(){return this.textContent},set(v){this.textContent=v}});
 dom.window.structuredClone=structuredClone;dom.window.innerWidth=width;dom.window.innerHeight=844
 dom.window.HTMLDialogElement.prototype.showModal=function(){this.setAttribute('open','')}
 dom.window.HTMLDialogElement.prototype.close=function(){this.removeAttribute('open');this.dispatchEvent(new dom.window.Event('close'))}
 dom.window.eval([...dom.window.document.querySelectorAll('script[src]')].map(s=>fs.readFileSync(path.join(dir,s.getAttribute('src')),'utf8')).join('\n')+'\nwindow.test={go,accept,state,conversation,submitRequest};')
 return dom
}
function click(d,s){const n=d.window.document.querySelector(s);assert(n,s);assert(!n.disabled,s);n.click()}
for(const width of [320,390,1440])for(const p of pages){const d=create(p,width);assert(d.window.document.title.includes('界面优化基准'));assert.equal(d.window.document.querySelectorAll('.discussion-brief').length,0);for(const el of d.window.document.querySelectorAll('[src]')){const src=el.getAttribute('src');if(!/^(data:|blob:|https?:)/.test(src))assert(fs.existsSync(path.join(dir,src)),p+': '+src)}results.push({page:p,width,pass:true});d.window.close()}
for(const s of scenarios){const d=create(s==='completed'?'detail':'chat',390,s);if(s!=='completed'){for(const cls of ['composer-more','voice-start','composer-send'])assert(d.window.document.querySelector('.composer-input-area .'+cls));for(const title of ['重取回话','话头记录','另起话头'])assert(d.window.document.querySelector(`[aria-label="${title}"]`))}results.push({scenario:s,pass:true});d.window.close()}
{
 const d=create('chat'),q=s=>d.window.document.querySelector(s);assert(q('.composer-more + .composer-attach'));assert(q('.composer-inline-voice + .composer-send'));click(d,'.composer-more');assert(!q('.composer-more-panel .composer-add-materials'));click(d,'[data-action=ui-settings]');assert(q('.voice-disclosure').textContent.includes('AI'));assert(!q('.voice-settings').textContent.includes('识别语言'));click(d,'[data-action=complete-materials]');click(d,'[data-pick=ref-brief]');click(d,'[data-action=confirm-materials]');assert(q('.composer-body').textContent.includes('活动说明'));
 click(d,'[data-action=complete-history]');assert(q('.baseline-history'));click(d,'[data-action=complete-history]');click(d,'[data-action=complete-voice]');click(d,'[data-action=complete-voice-stop]');q('.baseline-voice-status textarea').value='测试转写';click(d,'[data-action=complete-voice-append]');assert(q('.composer-textarea').value.includes('测试转写'));results.push({interaction:'optimized settings/materials/history/voice',pass:true});d.window.close()
}
{
 const d=create('chat',390,'results');assert.equal(d.window.document.querySelectorAll('.mmd-result').length,4);d.window.test.go('detail');d.window.test.accept();assert.equal(d.window.document.querySelectorAll('dialog input[type=checkbox]').length,0);click(d,'[data-action=finish]');await new Promise(r=>setTimeout(r,750));assert(d.window.test.state.task.complete);assert.equal(d.window.test.state.operation.writes,1);results.push({interaction:'single acceptance and read-only state',pass:true});d.window.close()
}
const idx=new JSDOM(fs.readFileSync(dir+'/pages.html','utf8'));const links=[...idx.window.document.querySelectorAll('a')];assert.equal(links.filter(l=>l.textContent.includes('打开页面')).length,19);assert.equal(links.filter(l=>l.textContent.includes('体验分支')).length,23);for(const l of links){const p=l.getAttribute('href').split(/[?#]/)[0];assert(fs.existsSync(path.resolve(dir,p)),p)}idx.window.close();results.push({index:'19 pages, 23 states, links resolve',pass:true})
for(const f of ['prototype.js','baseline-ui.js','interaction-completion.js'])assert(!/\bfetch\s*\(|XMLHttpRequest|WebSocket\s*\(|getUserMedia\s*\(/.test(fs.readFileSync(dir+'/'+f,'utf8')))

for(const scenario of ['cancel-ready','cancel-unknown']){
 const d=create('detail',390,scenario),q=s=>d.window.document.querySelector(s),st=d.window.test.state;
 const before=JSON.stringify(st.task);click(d,'[data-action=complete-cancel]');click(d,'dialog footer [data-action=close-dialog]');assert.equal(JSON.stringify(st.task),before);
 click(d,'[data-action=complete-cancel]');click(d,'[data-action=complete-cancel-confirm]');assert.equal(st.cancellation.writes,1);
 if(scenario==='cancel-unknown'){assert(!st.task.cancelled);click(d,'[data-action=complete-cancel]');assert.equal(st.cancellation.writes,1);assert.equal(st.cancellation.queries,1);}else{assert(st.task.cancelled);click(d,'.matter-results-action');assert(q('.terminal-history-actions'));assert(!q('[data-action=finish]'));assert(!q('[data-action=workspace]'));}
 results.push({interaction:scenario,pass:true});d.window.close();
}
for(const scenario of ['runtime-ready','runtime-existing','runtime-unknown','runtime-invalid']){
 const d=create('catalog',390,scenario),q=s=>d.window.document.querySelector(s),st=d.window.test.state;
 assert(q('[data-action=complete-runtime-register]').disabled);
 if(scenario!=='runtime-existing')click(d,'[data-action=complete-runtime-import]');
 if(scenario==='runtime-invalid')assert(q('[data-action=complete-runtime-register]').disabled);
 else {if(scenario!=='runtime-existing')click(d,'[data-action=complete-runtime-register]');click(d,'[data-action=complete-runtime-query]');assert(q('[data-action=complete-runtime-register]').disabled);assert.equal(st.runtimeDemo.status,scenario==='runtime-unknown'?'UNKNOWN':scenario==='runtime-existing'?'ACTIVE':'PENDING');}
 click(d,'[data-action=complete-runtime-close]');assert(!q('.runtime-setup'));
 results.push({interaction:scenario,pass:true});d.window.close();
}

{
 const d=create('detail',390,'cancel-ready'),q=s=>d.window.document.querySelector(s),st=d.window.test.state;
 click(d,'[data-action=complete-cancel]');click(d,'[data-action=complete-cancel-confirm]');
 d.window.test.go('chat');assert(q('.composer-textarea').placeholder.includes('已取消'));click(d,'[data-action=complete-history]');assert(!q('[data-action=complete-delete-current]'));
 st.agent=null;d.window.test.go('agents');click(d,'.agent-row');assert(!q('[data-action=assign]'));
 st.draft='新需求不覆盖原取消事项';d.window.test.submitRequest();assert(st.task.cancelled);assert.equal(st.cancellation.writes,1);assert(q('.hall-draft-editor'));assert.equal(st.draft,'新需求不覆盖原取消事项');
 results.push({interaction:'terminal wording, no assign/delete and new-task cancellation isolation',pass:true});d.window.close();
}

{
 const d=create('home'),st=d.window.test.state,q=s=>d.window.document.querySelector(s);
 const change=(selector,value)=>{q(selector).value=value;q(selector).dispatchEvent(new d.window.Event('change',{bubbles:true}));};
 st.draft='整理一页简报';st.draftFiles=['ref-brief'];d.window.test.submitRequest();assert(!st.task);assert(q('.hall-draft-editor'));assert.equal(q('[name=taskDescription]').value,st.draft);
 change('[data-draft-agent]','wuyong');click(d,'[data-action=complete-draft-next]');assert(q('[data-action=complete-draft-submit]').disabled);assert(!st.task);
 click(d,'[data-draft-authorized]');click(d,'[data-action=complete-draft-submit]');assert(st.task.unified);assert.equal(st.task.executions.length,1);assert.equal(st.task.phase,'等待承接');assert.equal(st.outputs.length,0);
 const id=st.task.id,frozen=JSON.stringify(st.task.executions[0].fields);click(d,'[data-action=complete-task-refresh]');assert.equal(st.task.executions.length,1);
 click(d,'[data-action=complete-draft-progress]');assert.equal(st.task.phase,'办理中');click(d,'[data-action=complete-draft-progress]');assert.equal(st.task.phase,'成果已归档');assert.equal(st.outputs.length,1);
 click(d,'.matter-results-action');assert(q('.unified-results'));click(d,'[data-action=preview]');assert(q('dialog[open]'));click(d,'dialog [data-action=close-dialog]');click(d,'[data-action=complete-draft-revise]');assert.equal(st.task.id,id);assert.equal(st.task.round,2);assert.equal(st.outputs.length,1);
 st.draft='压缩到半页';d.window.test.go('create');click(d,'[data-action=complete-draft-next]');click(d,'[data-draft-authorized]');click(d,'[data-action=complete-draft-submit]');assert.equal(st.task.executions.length,2);assert.equal(JSON.stringify(st.task.executions[0].fields),frozen);assert.equal(st.task.id,id);
 results.push({interaction:'unified direct entry/explicit authority/one execution/progress/results/revision same matter',pass:true});d.window.close();
}
{
 const d=create('create'),st=d.window.test.state,q=s=>d.window.document.querySelector(s);
 st.draft='讨论活动方案';st.draftFiles=['ref-brief'];d.window.test.go('create');click(d,'[data-mode=discuss]');q('[data-draft-agent]').value='wuyong';q('[data-draft-agent]').dispatchEvent(new d.window.Event('change',{bubbles:true}));click(d,'[data-action=complete-draft-next]');
 assert.equal(st.task.phase,'议事中');assert.equal(st.outputs.length,0);assert.equal(st.task.executions.length,0);const id=st.task.id;
 q('.composer-textarea').value='面向亲子家庭';q('.composer-textarea').dispatchEvent(new d.window.Event('input',{bubbles:true}));q('.composer-submit').dispatchEvent(new d.window.Event('submit',{bubbles:true,cancelable:true}));assert.equal(st.outputs.length,0);assert(st.messages.some(m=>m.supplement));
 click(d,'[data-action=complete-draft-confirm]');assert(q('.confirmation-grid').textContent.includes('面向亲子家庭'));assert(q('[data-action=complete-draft-submit]').disabled);
 click(d,'[data-draft-authorized]');click(d,'[data-action=complete-draft-submit]');assert.equal(st.task.id,id);assert.equal(st.task.executions.length,1);assert.equal(st.task.executions[0].discussion,'面向亲子家庭');
 d.window.test.go('chat');assert(q('.composer-textarea').disabled);assert(q('.composer-send').disabled);assert(!q('[data-action=complete-draft-confirm]'));
 results.push({interaction:'unified discussion clarifies only, same matter explicit execution and locked scope',pass:true});d.window.close();
}

{
 const d=create('tasks'),q=s=>d.window.document.querySelector(s);assert(!q('.bounty-panel .task-create-actions'));assert(!q('.bounty-panel .task-create-form'));assert(q('[aria-label="搜索事项"]'));assert(q('[aria-label="刷新事项"]'));click(d,'[data-action=complete-task-refresh]');results.push({interaction:'compact task toolbar without duplicate create form',pass:true});d.window.close();
}
const hashes=Object.fromEntries(['prototype.js','baseline-ui.js','interaction-completion.js','interaction-completion.css'].map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(dir+'/'+f)).digest('hex')]))
const report={checkedOn:'2026-10-16',method:'JSDOM local document/interaction checks, not visual acceptance',status:'PASS',count:results.length,results,sourceHashes:hashes,productAcceptance:false}
fs.writeFileSync(evidence+'/prototype-checks.json',JSON.stringify(report,null,2)+'\n');console.log('PASS '+results.length+' document checks')
