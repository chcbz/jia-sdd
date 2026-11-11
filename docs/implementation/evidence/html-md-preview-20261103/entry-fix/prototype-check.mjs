import assert from 'node:assert/strict'
import {writeFile} from 'node:fs/promises'
import {launchChrome,evaluate,waitForExpression,stopChrome} from '/home/isp/wsps/cyf/web/scripts/juyiting/e13/lib/cdp-harness.mjs'
const output=new URL(process.env.PROTOTYPE_EVIDENCE||'./',import.meta.url)
const b=await launchChrome({debugPort:19516});const {cdp}=b;const checks=[]
const delay=()=>new Promise(r=>setTimeout(r,200))
async function inspect(selector){
 await waitForExpression(cdp,`!!document.querySelector(${JSON.stringify(selector)})`,10000);let child;for(let i=0;i<30&&!child;i++){await delay();child=(await cdp.send('Page.getFrameTree')).frameTree.childFrames?.[0]?.frame.id}assert.ok(child)
 const {executionContextId}=await cdp.send('Page.createIsolatedWorld',{frameId:child,worldName:'inspect-document'})
 const {result}=await cdp.send('Runtime.evaluate',{expression:`({text:document.body.innerText,h1:document.querySelector('h1')?.textContent,script:!!document.querySelector('script')})`,contextId:executionContextId,returnByValue:true})
 assert.equal(result.value.h1,'实际正文');assert.equal(result.value.script,false)
 const geo=await evaluate(cdp,`(()=>{const f=document.querySelector(${JSON.stringify(selector)}),r=f.getBoundingClientRect();return {width:r.width,height:r.height,pageOverflow:document.documentElement.scrollWidth>innerWidth,frameVisible:r.width>100&&r.height>100,sandbox:f.getAttribute('sandbox')}})()`)
 assert.equal(geo.frameVisible,true);assert.equal(geo.pageOverflow,false);assert.equal(geo.sandbox,'');return geo
}
try {
 await cdp.send('Page.navigate',{url:(process.env.PROTOTYPE_URL||'http://localhost:18786')+'/index.html?ui=20261103-all-document-entries#chat'});await waitForExpression(cdp,`typeof readPrototypeFiles==='function' && !!document.querySelector('.composer-send')`,60000)
 for(const width of [1440,390,320]){
 await cdp.send('Emulation.setDeviceMetricsOverride',{width,height:900,deviceScaleFactor:1,mobile:width<760})
 for(const [ext,mime,body] of [['html','text/html','<h1>实际正文</h1><script>parent.pwned=1</script>'],['md','text/markdown','# 实际正文\n\n**重点**'],['htm','','<h1>实际正文</h1>'],['markdown','','# 实际正文']]){
 console.log('checking',width,ext);const id=await evaluate(cdp,`(async()=>{const [a]=await readPrototypeFiles([new File([${JSON.stringify(body)}],${JSON.stringify('实际资料.'+ext)},{type:${JSON.stringify(mime)}})]);state.localFiles.push(a);return a.id})()`)
 // Picker actual selection and mobile toggle, not renderer-only injection.
 await evaluate(cdp,`openMaterials('chat');document.querySelector('[data-action="picker-select"][data-id="${id}"]').click();if(innerWidth<=720)document.querySelector('[data-action="picker-preview"]').click()`)
 const chooser=await inspect('.material-inline-preview iframe')
 await evaluate(cdp,`document.querySelector('dialog[open]').close();conversation().messages=[{role:'USER',text:'实际附件',files:['${id}']}];renderChat();document.querySelector('[data-action="preview"][data-id="${id}"]').click()`)
 const discussion=await inspect('.mmd-preview iframe')
 if(ext==='html'){const shot=await cdp.send('Page.captureScreenshot',{format:'png'});await writeFile(new URL(`prototype-discussion-${width}.png`,output),Buffer.from(shot.data,'base64'))}
 await evaluate(cdp,`document.querySelector('dialog[open]').close()`)
 checks.push({width,ext,mime,chooser,discussion})
 }
 }
 // Actual workspace upload form must save body, not the old placeholder.
 await evaluate(cdp,`go('workspace');document.querySelector('[data-action="complete-upload-panel"]').click();const input=document.querySelector('[data-workspace-upload]'),dt=new DataTransfer();dt.items.add(new File(['<h1>实际正文</h1>'],'upload.html',{type:'text/html'}));input.files=dt.files;input.dispatchEvent(new Event('change',{bubbles:true}));document.querySelector('[data-action="complete-upload-confirm"]').click()`)
 await delay();assert.equal(await evaluate(cdp,`state.localFiles.at(-1).text`),'<h1>实际正文</h1>')
 const historical=await evaluate(cdp,`(()=>{const a={name:'旧上传.html',text:'本地文件可下载查看。',url:'data:text/html;base64,'+btoa('<h1>legacy</h1>')};return prototypeDocumentText(a)})()`);assert.equal(historical,'<h1>legacy</h1>')
 const renamed=await evaluate(cdp,`prototypeDocumentKind({name:'自定义显示名称',originalName:'原始.md',mime:'text/markdown'})`);assert.equal(renamed,'markdown')
 const empty=await evaluate(cdp,`readPrototypeFiles([new File([''],'empty.markdown')]).then(a=>a[0].text)`);assert.equal(empty,'')
 await writeFile(new URL('prototype-results.json',output),JSON.stringify({baseUrl:process.env.PROTOTYPE_URL||'http://localhost:18786',checks,workspaceUploadBody:true,emptyFile:true,historicalUpload:true,renamedUpload:true},null,2));console.log('PASS prototype 24 real entry previews, workspace upload and empty file')
}finally{cdp.close();await stopChrome(b.chrome,b.userDataDir)}
