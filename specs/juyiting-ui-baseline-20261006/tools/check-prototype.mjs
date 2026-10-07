// Local document checks only; Chromium report is separate and authoritative for layout.
import assert from 'node:assert/strict'
import fs from 'node:fs'
import path from 'node:path'
import crypto from 'node:crypto'
import {createRequire} from 'node:module'
import {fileURLToPath} from 'node:url'
const dir=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../prototype')
const require=createRequire(path.resolve(process.argv[2]||'/home/isp/wsps/cyf/web/package.json'))
const {JSDOM}=require('jsdom'),results=[]
const pages=['home','tasks','create','agents','detail','chat','private','public','workspace','mine','library','messages','catalog','map','file','reader','help','account']
const scenarios=['ready','empty','waiting','streaming','error','recording','voice-review','results','completed','create-failure','create-unknown','reply-failure','accept-unknown','accept-failure','independent-roots']
function create(page,width=390,scenario='ready') {
 const dom=new JSDOM(fs.readFileSync(dir+'/index.html','utf8'),{url:`http://localhost/?scenario=${scenario}#${page}`,runScripts:'outside-only',pretendToBeVisual:true})
 Object.defineProperty(dom.window.HTMLElement.prototype,'innerText',{get(){return this.textContent},set(v){this.textContent=v}});
 dom.window.structuredClone=structuredClone;dom.window.innerWidth=width;dom.window.innerHeight=844
 dom.window.HTMLDialogElement.prototype.showModal=function(){this.setAttribute('open','')}
 dom.window.HTMLDialogElement.prototype.close=function(){this.removeAttribute('open');this.dispatchEvent(new dom.window.Event('close'))}
 dom.window.eval([...dom.window.document.querySelectorAll('script[src]')].map(s=>fs.readFileSync(path.join(dir,s.getAttribute('src')),'utf8')).join('\n')+'\nwindow.test={go,accept,state,conversation};')
 return dom
}
function click(d,s){const n=d.window.document.querySelector(s);assert(n,s);assert(!n.disabled,s);n.click()}
for(const width of [320,390,1440])for(const p of pages){const d=create(p,width);assert(d.window.document.title.includes('界面优化基准'));assert.equal(d.window.document.querySelectorAll('.discussion-brief').length,0);for(const el of d.window.document.querySelectorAll('[src]')){const src=el.getAttribute('src');if(!/^(data:|blob:|https?:)/.test(src))assert(fs.existsSync(path.join(dir,src)),p+': '+src)}results.push({page:p,width,pass:true});d.window.close()}
for(const s of scenarios){const d=create(s==='completed'?'detail':'chat',390,s);if(s!=='completed'){for(const cls of ['composer-more','voice-start','composer-send'])assert(d.window.document.querySelector('.composer-input-area .'+cls));for(const title of ['重取回话','话头记录','另起话头'])assert(d.window.document.querySelector(`[aria-label="${title}"]`))}results.push({scenario:s,pass:true});d.window.close()}
{
 const d=create('chat'),q=s=>d.window.document.querySelector(s);click(d,'.composer-more');click(d,'[data-action=ui-settings]');assert(q('.voice-disclosure').textContent.includes('AI'));assert(!q('.voice-settings').textContent.includes('识别语言'));click(d,'[data-action=ui-materials]');click(d,'[data-pick=ref-brief]');click(d,'[data-action=confirm-materials]');assert(q('.composer-body').textContent.includes('活动说明'));
 click(d,'[data-action=complete-history]');assert(q('.baseline-history'));click(d,'[data-action=complete-history]');click(d,'[data-action=complete-voice]');click(d,'[data-action=complete-voice-stop]');q('.baseline-voice-status textarea').value='测试转写';click(d,'[data-action=complete-voice-append]');assert(q('.composer-textarea').value.includes('测试转写'));results.push({interaction:'optimized settings/materials/history/voice',pass:true});d.window.close()
}
{
 const d=create('chat',390,'results');assert.equal(d.window.document.querySelectorAll('.mmd-result').length,4);d.window.test.go('detail');d.window.test.accept();assert.equal(d.window.document.querySelectorAll('dialog input[type=checkbox]').length,0);click(d,'[data-action=finish]');await new Promise(r=>setTimeout(r,750));assert(d.window.test.state.task.complete);assert.equal(d.window.test.state.operation.writes,1);results.push({interaction:'single acceptance and read-only state',pass:true});d.window.close()
}
const idx=new JSDOM(fs.readFileSync(dir+'/pages.html','utf8'));const links=[...idx.window.document.querySelectorAll('a')];assert.equal(links.filter(l=>l.textContent.includes('打开页面')).length,18);assert.equal(links.filter(l=>l.textContent.includes('体验分支')).length,15);for(const l of links){const p=l.getAttribute('href').split(/[?#]/)[0];assert(fs.existsSync(path.resolve(dir,p)),p)}idx.window.close();results.push({index:'18 pages, 15 states, links resolve',pass:true})
for(const f of ['prototype.js','baseline-ui.js','interaction-completion.js'])assert(!/\bfetch\s*\(|XMLHttpRequest|WebSocket\s*\(|getUserMedia\s*\(/.test(fs.readFileSync(dir+'/'+f,'utf8')))
const hashes=Object.fromEntries(['prototype.js','baseline-ui.js','interaction-completion.js','interaction-completion.css'].map(f=>[f,crypto.createHash('sha256').update(fs.readFileSync(dir+'/'+f)).digest('hex')]))
const report={checkedOn:'2026-10-07',method:'JSDOM local document/interaction checks, not visual acceptance',status:'PASS',count:results.length,results,sourceHashes:hashes,productAcceptance:false}
fs.writeFileSync(dir+'/prototype-checks.json',JSON.stringify(report,null,2)+'\n');console.log('PASS '+results.length+' document checks')
