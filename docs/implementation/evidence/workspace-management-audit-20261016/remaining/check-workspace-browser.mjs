// Task-scoped diagnostic; reuses existing Vite preview and CDP harness, no production build.
import assert from 'node:assert/strict'
import { createRequire } from 'node:module'
import { pathToFileURL } from 'node:url'
import { join } from 'node:path'
import { readFileSync, writeFileSync, mkdirSync, readdirSync } from 'node:fs'
import { createHash } from 'node:crypto'
import net from 'node:net'
const web = '/home/isp/wsps/worktrees/cyf-workspace-remaining-web-20261016'
const out = process.env.CYF_WORKSPACE_EVIDENCE
const origin = new URL(process.env.CYF_WORKSPACE_ORIGIN)
assert.equal(origin.hostname, '127.0.0.1')
const files = JSON.parse(process.env.CYF_WORKSPACE_FILES)
const req = createRequire(join(web, 'package.json'))
const { createServer } = await import(pathToFileURL(req.resolve('vite')))
const { default: vue } = await import(pathToFileURL(req.resolve('@vitejs/plugin-vue')))
const launcher = join(out, 'browser-launcher.sh')
writeFileSync(launcher, `#!/bin/sh\nexec /usr/lib64/chromium-browser/chromium-browser --no-sandbox "$@" 2>'${out}/browser-stderr.log'\n`, { mode: 0o700 })
process.env.CHROME_PATH = launcher
const { launchChrome, stopChrome, evaluate, waitForExpression } = await import(pathToFileURL(join(web, 'scripts/juyiting/e13/lib/cdp-harness.mjs')))
const entry = `
import {createApp,reactive,nextTick} from 'vue'
import Component from '/@fs/${web}/src/components/workspace/PersonalWorkspace.vue'
import {createApi} from '/@fs/${web}/src/composables/useHttp.js'
export const auth=reactive({authorizationGeneration:1,oauthClientId:'client-a',token:async()=>window.__tokens[window.__identity]})
export const globalStore=reactive({user:{id:'ownerA'}})
window.__identity='ownerA';window.__drafts=[];window.__auxiliary=[];window.__wire=[]
const originalFetch=window.fetch.bind(window);window.fetch=async(...args)=>{const r=await originalFetch(...args);if(r.headers.get('content-type')?.includes('json'))window.__wire.push({url:String(args[0]),requestId:new Headers(args[1]?.headers).get('X-Request-Id'),responseRequestId:r.headers.get('X-Request-Id'),status:r.status,body:await r.clone().text()});return r}
const transport=createApi('/agent')
export const api={execute:options=>{
 if(options.url.startsWith('/personal-workspace/files')||options.url.startsWith('/personal-workspace/operations/')) return transport.execute({...options,authStore:auth,rum:false})
 window.__auxiliary.push(options.url)
 if(options.url==='/roster')return Promise.resolve([])
 if(options.url==='/personal-workspace/executions/capabilities')return Promise.resolve({allowedMimeTypes:[],inputMimeTypes:[],generationEnabled:false})
 if(options.url==='/personal-workspace/executions'&&options.method==='GET')return Promise.resolve({items:[],nextCursor:null,hasMore:false})
 throw Error('Out of scope: '+options.url)
}}
window.__switch=async()=>{window.__identity='ownerB';globalStore.user={id:'ownerB'};auth.authorizationGeneration++;await nextTick();return window.__workspace.items.value.length===0&&window.__workspace.detail.value===null}
createApp(Component,{embedded:true,onStartDraft:e=>window.__drafts.push(e)}).mount('#app')
`
const virtual = {
  'audit-entry': entry,
  'audit-auth': `export {auth as useStoreValue} from 'audit-entry';import{auth}from'audit-entry';export const useApiStore=()=>auth`,
  'audit-global': `import{globalStore}from'audit-entry';export const useGlobalStore=()=>globalStore`,
  'audit-workspace': `import{usePersonalWorkspace as real}from'/@fs/${web}/src/composables/usePersonalWorkspace.js';export{savePersonalWorkspaceBlob}from'/@fs/${web}/src/composables/usePersonalWorkspace.js';import{api}from'audit-entry';export const usePersonalWorkspace=o=>{const value=real({...o,api});window.__workspace=value;return value}`,
  'audit-execution': `import{usePersonalWorkspaceExecution as real}from'/@fs/${web}/src/composables/usePersonalWorkspaceExecution.js';import{api}from'audit-entry';export const usePersonalWorkspaceExecution=o=>real({...o,api})`
}
let chrome, server
const requests=[], observations=[], runtimeErrors=[]
const observe=(name,kind,actual)=>observations.push({name,kind,actual})
try {
  server=await createServer({configFile:false,envFile:false,root:web,logLevel:'silent',cacheDir:join(out,'vite-cache'),optimizeDeps:{noDiscovery:true,include:[]},
    resolve:{alias:[{find:'@/stores/api',replacement:'audit-auth'},{find:'@/stores/global',replacement:'audit-global'},{find:'@/composables/usePersonalWorkspace',replacement:'audit-workspace'},{find:'@/composables/usePersonalWorkspaceExecution',replacement:'audit-execution'},{find:'@',replacement:join(web,'src')}]},
    plugins:[vue(),{name:'workspace-audit-mount',resolveId:id=>Object.hasOwn(virtual,id)?'\0'+id:null,load:id=>virtual[id.slice(1)],configureServer(s){s.middlewares.use((r,p,next)=>{if(r.url!=='/')return next();p.setHeader('Content-Type','text/html');p.end('<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{margin:0}*{box-sizing:border-box}</style><div id="app"></div><script type="module" src="/@id/__x00__audit-entry"></script>')})}}],
    server:{host:'127.0.0.1',port:0,fs:{allow:[web]},proxy:{'/agent':{target:origin.origin,configure(proxy){proxy.on('proxyRes',(response,request)=>{
 const requestIds=[];for(let i=0;i<response.rawHeaders.length;i+=2)if(response.rawHeaders[i].toLowerCase()==='x-request-id')requestIds.push(response.rawHeaders[i+1]);
 requests.push({path:request.url,method:request.method,status:response.statusCode,upstreamRequestIds:requestIds,diagnosticHeaderDedup:false});

})}}}}})
  await server.listen()
  const reservation=net.createServer();await new Promise(r=>reservation.listen(0,'127.0.0.1',r));const debugPort=reservation.address().port;await new Promise(r=>reservation.close(r))
  chrome=await launchChrome({debugPort});writeFileSync(join(out,'browser-owned-process.json'),JSON.stringify({pid:chrome.chrome.pid,profile:chrome.userDataDir,debugPort}));const {cdp}=chrome
  cdp.on('Runtime.exceptionThrown',event=>runtimeErrors.push(event.exceptionDetails?.exception?.description||event.exceptionDetails?.text||'runtime-error'))
  await cdp.send('Runtime.enable')
  await cdp.send('Page.addScriptToEvaluateOnNewDocument',{source:`window.__tokens=${process.env.CYF_WORKSPACE_TOKENS}`})
  const click=async selector=>{
    const point=await evaluate(cdp,`(()=>{const e=document.querySelector(${JSON.stringify(selector)});if(!e||e.disabled)throw Error('Control missing/disabled: '+${JSON.stringify(selector)});e.scrollIntoView({block:'center'});const r=e.getBoundingClientRect(),x=r.x+r.width/2,y=r.y+r.height/2;if(x<0||y<0||x>=innerWidth||y>=innerHeight||!e.contains(document.elementFromPoint(x,y)))throw Error('Control clipped/covered');return{x,y}})()`)
    await cdp.send('Input.dispatchMouseEvent',{type:'mousePressed',...point,button:'left',clickCount:1});await cdp.send('Input.dispatchMouseEvent',{type:'mouseReleased',...point,button:'left',clickCount:1})
  }
  const reload=async()=>{await cdp.send('Page.navigate',{url:`http://127.0.0.1:${server.httpServer.address().port}/`});await waitForExpression(cdp,`document.querySelector('[data-file-id="${files.download}"]')`)}
  const open=async id=>{await click(`[data-file-id="${id}"]`);await waitForExpression(cdp,`document.querySelector('.treasure-preview pre')?.textContent.length>0`)}
  await cdp.send('Page.navigate',{url:`http://127.0.0.1:${server.httpServer.address().port}/`})
  await waitForExpression(cdp,`document.querySelector('[data-file-id="${files.download}"]')`)
  const originalWire=await evaluate(cdp,`window.__wire[0]`)
  assert.equal(originalWire.status,200)
  assert.equal(originalWire.responseRequestId,originalWire.requestId)
  assert.deepEqual(requests[0].upstreamRequestIds,[originalWire.requestId])
  observe('unmodified-chain-single-request-id-accepted','regression-pass',{requestIds:requests[0].upstreamRequestIds})
  for(const [name,width,height] of [['desktop',1440,900],['mobile',390,844],['landscape',844,390]]) {
    await cdp.send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:name==='mobile'})
    await reload();await open(files.download)
    assert.equal(await evaluate(cdp,`document.querySelector('.treasure-preview pre').textContent`),'browser-download-original')
    await click('.treasure-actions .treasure-primary')
    assert.equal(await evaluate(cdp,`window.__drafts[0]?.inputs[0].version`),'1')
    const png=await cdp.send('Page.captureScreenshot',{format:'png'});writeFileSync(join(out,`workspace-${name}.png`),Buffer.from(png.data,'base64'))
    observe(`click-preview-draft-${name}`,'normal',{width,height,version:'1'})
  }
  await cdp.send('Emulation.setDeviceMetricsOverride',{width:1440,height:900,deviceScaleFactor:1,mobile:false})
  await reload();await open(files.download)
  const downloads=join(out,'downloads');mkdirSync(downloads,{recursive:true})
  await cdp.send('Browser.setDownloadBehavior',{behavior:'allow',downloadPath:downloads,eventsEnabled:true})
  await click('.treasure-version-tools > button')
  // Local polling verifies actual disk completion; never treats HTTP200 alone as download proof.
  let saved
  for(let i=0;i<100;i++){saved=readdirSync(downloads).find(n=>!n.endsWith('.crdownload'));if(saved)break;await new Promise(r=>setTimeout(r,100))}
  assert.ok(saved,'download not written to disk')
  const bytes=readFileSync(join(downloads,saved));assert.equal(bytes.toString(),'browser-download-original')
  observe('real-browser-download-sha256','normal',{sha256:createHash('sha256').update(bytes).digest('hex'),filename:saved})
  // Real UI lifecycle against the private HTTP/MySQL fixture, using synthetic bytes only.
  const setFile=async(selector,path)=>{const {root}=await cdp.send('DOM.getDocument');const {nodeId}=await cdp.send('DOM.querySelector',{nodeId:root.nodeId,selector});assert.ok(nodeId);await cdp.send('DOM.setFileInputFiles',{nodeId,files:[path]})}
  await reload();await click('.treasure-intro > button')
  const uploadPath=join(out,'ui-upload.txt');writeFileSync(uploadPath,'ui-first-version')
  await setFile('.treasure-form input[type=file]',uploadPath);await click('.treasure-actions .treasure-primary')
  await waitForExpression(cdp,`document.querySelector('.treasure-content')?.dataset.view==='list'&&window.__workspace.lastOperation.value?.fileId`)
  const uploaded=await evaluate(cdp,`window.__workspace.lastOperation.value.fileId`)
  await open(uploaded);assert.equal(await evaluate(cdp,`document.querySelector('.treasure-preview pre').textContent`),'ui-first-version')
  await click('.treasure-file-heading > button');await click('.treasure-management form input')
  await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'a',code:'KeyA',windowsVirtualKeyCode:65,modifiers:2})
  await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'a',code:'KeyA',windowsVirtualKeyCode:65,modifiers:2})
  await cdp.send('Input.insertText',{text:'ui-renamed'})
  await click('.treasure-management form button');await waitForExpression(cdp,`window.__workspace.detail.value?.file.displayName==='ui-renamed'&&window.__workspace.actionState.value==='ready'`)
  const appendPath=join(out,'ui-append.txt');writeFileSync(appendPath,'ui-second-version')
  await setFile('.treasure-management input[type=file]',appendPath);await click('.treasure-management > .treasure-form:nth-child(2) button')
  await waitForExpression(cdp,`window.__workspace.detail.value?.file.latestVersion==='2'&&window.__workspace.actionState.value==='ready'&&!window.__workspace.loading.value`)
  await click('.treasure-manage-danger > button');await waitForExpression(cdp,`!!document.querySelector('[aria-label="回收确认"]')`)
  await click('[aria-label="回收确认"] .treasure-actions button:last-child')
  await waitForExpression(cdp,`document.querySelector('.treasure-content')?.dataset.view==='list'&&!window.__workspace.loading.value`)
  assert.equal(await evaluate(cdp,`!!document.querySelector('[data-file-id="${uploaded}"]')`),false)
  await click('.treasure-tabs button:nth-child(4)');await waitForExpression(cdp,`!!document.querySelector('[data-file-id="${uploaded}"]')`)
  await open(uploaded);assert.equal(await evaluate(cdp,`document.querySelector('.treasure-preview pre').textContent`),'ui-second-version')
  await click('.treasure-file-heading > button');await click('.treasure-management > button')
  await waitForExpression(cdp,`document.querySelector('.treasure-content')?.dataset.view==='list'&&!window.__workspace.loading.value`)
  await click('.treasure-tabs button:first-child');await waitForExpression(cdp,`!!document.querySelector('[data-file-id="${uploaded}"]')`)
  await open(uploaded);assert.equal(await evaluate(cdp,`document.querySelector('.treasure-preview pre').textContent`),'ui-second-version')
  observe('ui-upload-rename-append-trash-restore','normal',{fileId:uploaded,latestVersion:'2',preview:'ui-second-version',transport:'direct loopback, no nginx compression'})
  await reload();await open(files.history)
  assert.equal(await evaluate(cdp,`document.querySelectorAll('.treasure-version-tools option').length`),100)
  assert.equal(await evaluate(cdp,`[...document.querySelectorAll('.treasure-version-tools option')].some(e=>e.value==='1')`),false)
  const before=await evaluate(cdp,`document.querySelector('.treasure-preview pre').textContent`)
  // Native keyboard selection, not DOM mutation: current v102 -> v101.
  await click('.treasure-version-tools select')
  await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'ArrowDown',code:'ArrowDown',windowsVirtualKeyCode:40})
  await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'ArrowDown',code:'ArrowDown',windowsVirtualKeyCode:40})
  await cdp.send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13})
  await cdp.send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13})
  await waitForExpression(cdp,`document.querySelector('.treasure-version-tools select').value==='101'`)
  await waitForExpression(cdp,`document.querySelector('.treasure-preview pre')?.textContent!==${JSON.stringify(before)}`)
  await click('.treasure-actions .treasure-primary')
  assert.equal(await evaluate(cdp,`window.__drafts.at(-1)?.inputs[0].version`),'101')
  observe('history-select-refreshes-preview-and-fixed-version-draft','regression-pass',{selected:'101'})
  await click('.treasure-file-heading > button')
  await click('.treasure-manage-danger > button')
  await waitForExpression(cdp,`document.querySelector('[aria-label="回收确认"]')`)
  const confirmation=await evaluate(cdp,`document.querySelector('[aria-label="回收确认"]').textContent`)
  assert.match(confirmation,/任务引用 101 条/);assert.match(confirmation,/议事引用 1 条/);assert.match(confirmation,/现存输入授权 100 条/)
  for(const [name,width,height] of [['desktop',1440,900],['mobile',390,844],['landscape',844,390]]) {
    await cdp.send('Emulation.setDeviceMetricsOverride',{width,height,deviceScaleFactor:1,mobile:name==='mobile'})
    await evaluate(cdp,`document.querySelector('[aria-label="回收确认"]').scrollIntoView({block:'center'})`)
    const png=await cdp.send('Page.captureScreenshot',{format:'png'});writeFileSync(join(out,`workspace-confirmation-${name}.png`),Buffer.from(png.data,'base64'))
  }
  observe('exact-confirmation-three-categories','regression-pass',confirmation)
  assert.equal(await evaluate(cdp,`window.__switch()`),true)
  await waitForExpression(cdp,`!document.querySelector('.treasure-preview pre')&&!document.querySelector('.treasure-file-row')`)
  observe('identity-switch-clears-dom-and-state','normal',true)
  assert.equal(runtimeErrors.length,0,JSON.stringify(runtimeErrors))
  writeFileSync(join(out,'browser-observations.json'),JSON.stringify({observations,requests,runtimeErrors,boundaries:['No header normalization or deduplication; genuine transport consumed by production adapter','real file HTTP/MySQL chain','synthetic auth and component mount','roster/execution capabilities/history are auxiliary stubs','mobile viewport emulation, not physical phone','no production OAuth or Flow']},null,2))
  console.log(JSON.stringify({status:'PASS',observations:observations.length,requests:requests.length,defectsReproduced:observations.filter(o=>o.kind==='defect-reproduced').length}))
}catch(error){let pageState=null;if(chrome){try{pageState=await evaluate(chrome.cdp,`({text:document.body.innerText,workspaceError:window.__workspace?.error?.value,wire:window.__wire})`)}catch{}}writeFileSync(join(out,'browser-failure.json'),JSON.stringify({message:error.message,stack:error.stack,runtimeErrors,observations,requests,pageState},null,2));throw error}finally{if(chrome){chrome.cdp.close();await stopChrome(chrome.chrome,chrome.userDataDir)}if(server)await server.close()}
