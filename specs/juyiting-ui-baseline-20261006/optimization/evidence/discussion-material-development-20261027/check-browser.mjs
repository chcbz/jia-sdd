import fs from 'node:fs'
const root='/tmp/cyf-discussion-material-dev-20261027'
const evidence='/home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/optimization/evidence/discussion-material-development-20261027'
const port=fs.readFileSync(root+'/profile/DevToolsActivePort','utf8').split('\n')[0]
const target=await(await fetch(`http://127.0.0.1:${port}/json/new?about:blank`,{method:'PUT'})).json()
const ws=new WebSocket(target.webSocketDebuggerUrl);await new Promise(r=>ws.onopen=r)
let serial=0;const pending=new Map(),errors=[],checks=[]
ws.onmessage=e=>{const m=JSON.parse(e.data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result)}if(m.method==='Runtime.exceptionThrown')errors.push(m.params.exceptionDetails)}
const cdp=(method,params={})=>new Promise((resolve,reject)=>{const id=++serial;pending.set(id,{resolve,reject});ws.send(JSON.stringify({id,method,params}))})
const ev=async expression=>{const r=await cdp('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value}
const pause=ms=>new Promise(r=>setTimeout(r,ms))
const check=(name,pass)=>{checks.push({name,pass});if(!pass)throw new Error(name)}
await cdp('Runtime.enable');await cdp('Page.enable')
try {
for(const variant of ['public','private','bounty']) for(const width of [320,390,720,721,1440]){
 await cdp('Emulation.setDeviceMetricsOverride',{width,height:860,deviceScaleFactor:1,mobile:width<=720})
 await cdp('Page.navigate',{url:`http://127.0.0.1:18787/index.html?variant=${variant}`})
 for(let i=0;i<60;i++){await pause(100);if(await ev(`!!document.querySelector('.composer-attachment-card')`))break}
 const label=variant+'/'+width
 check(label+' components loaded',await ev(`!!document.querySelector('.composer-attachment-card')`))
 check(label+' no horizontal page overflow',await ev(`document.documentElement.scrollWidth<=innerWidth`))
 check(label+' left tools / right voice and send',await ev(`(()=>{const r=s=>document.querySelector(s).getBoundingClientRect();return r('.composer-more').left<r('.composer-add-materials').left&&r('.composer-add-materials').right<r('.composer-inline-voice').left&&r('.composer-inline-voice').right<=r('.composer-send').left})()`))
 check(label+' attachments inside input; scrollable and hidden scrollbar',await ev(`(()=>{const e=document.querySelector('.composer-input-area .composer-attachment-strip');e.scrollLeft=90;return e.scrollLeft>0&&getComputedStyle(e).scrollbarWidth==='none'&&e.tabIndex===0})()`))
 await ev(`(()=>{const rail=document.querySelector('.composer-attachment-strip');rail.scrollLeft=0;rail.focus()})()`)
 await cdp('Input.dispatchKeyEvent',{type:'keyDown',key:'ArrowRight',code:'ArrowRight',windowsVirtualKeyCode:39})
 await cdp('Input.dispatchKeyEvent',{type:'keyUp',key:'ArrowRight',code:'ArrowRight',windowsVirtualKeyCode:39});await pause(200)
 check(label+' keyboard still scrolls attachment strip',await ev(`document.querySelector('.composer-attachment-strip').scrollLeft>0`))
 await ev(`document.querySelector('.composer-add-materials').click()`);await pause(200)
 if(width<=720){
  check(label+' three native options',await ev(`document.querySelector('.composer-material-actions')?.textContent==='拍照相册资料'&&document.querySelector('input[capture]').accept==='image/*'&&!document.querySelector('input[multiple]').hasAttribute('capture')`))
  await ev(`document.body.dispatchEvent(new PointerEvent('pointerdown',{bubbles:true}))`);await pause(30)
  check(label+' outside dismissal',await ev(`!document.querySelector('.composer-material-actions')`))
  await ev(`document.querySelector('.composer-add-materials').click()`);await pause(30)
  await ev(`document.dispatchEvent(new KeyboardEvent('keydown',{key:'Escape',bubbles:true,cancelable:true}))`);await pause(30)
  check(label+' Escape dismissal and focus',await ev(`!document.querySelector('.composer-material-actions')&&document.activeElement===document.querySelector('.composer-add-materials')`))
  await ev(`document.querySelector('.composer-add-materials').click()`);await pause(30)
  await ev(`document.querySelector('.composer-material-actions button:last-child').click()`);await pause(200)
 }
 check(label+' common material dialog',await ev(`!!document.querySelector('.quick-material-picker[open]')&&!document.querySelector('.composer-material-actions')`))
 await ev(`document.querySelector('.quick-material-back').click()`);await pause(100)
 check(label+' cancel preserves references and text',await ev(`document.querySelectorAll('.composer-attachment-card').length===6&&document.querySelector('textarea').value==='请结合资料继续讨论'`))
 await ev(`document.querySelector('.composer-attachment-strip').scrollLeft=0`)
 if(width===390||width===1440){if(width===390){await ev(`document.querySelector('.composer-add-materials').click()`);await pause(50)}const {data}=await cdp('Page.captureScreenshot',{format:'png'});fs.writeFileSync(`${evidence}/${variant}-${width}.png`,Buffer.from(data,'base64'))}
}
check('no runtime exceptions',errors.length===0)
} finally {fs.writeFileSync(evidence+'/browser-checks.json',JSON.stringify({fixture:'real Vue production components; mocked workspace/links, not live APIs',checks,errors},null,2));ws.close()}
console.log(JSON.stringify({checks:checks.length,failed:checks.filter(x=>!x.pass).length,errors:errors.length}))
