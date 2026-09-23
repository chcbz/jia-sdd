// Read-only demo audit. Instruments a served response in-browser; never rewrites the demo.
const fs = require('node:fs'), path = require('node:path'), crypto = require('node:crypto');
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || '/tmp/cyf-ui-audit-tools/node_modules/playwright-core');
const root = path.resolve(__dirname, '../../..'), out = path.resolve(__dirname, '../evidence');
const base = process.env.DEMO_URL || 'http://127.0.0.1:8878';
const props = ['font-family','font-size','font-weight','font-style','line-height','letter-spacing','color','background-color','background-image','display','position','width','height','min-width','max-width','min-height','max-height','padding','margin','gap','row-gap','column-gap','border','border-radius','box-shadow','outline','outline-offset','opacity','cursor','overflow','overflow-x','overflow-y','overscroll-behavior','flex','flex-direction','flex-wrap','grid-template-columns','grid-template-rows','align-items','align-self','justify-content','white-space','word-break','overflow-wrap','text-overflow','text-align','z-index','top','right','bottom','left','transform','transition','resize'];
const scenes = ['overview','bounty','chat','agents','files','archive','messages','account','settings','help','quick','demand','formal-demand','confirm','formal-confirm','task-open','task-assigned','task-failed','task-completed','materials','preview','reader','login','recruit','chat-history','guide-0','guide-3','agent-selected','files-trash','chat-populated','chat-dialog','demand-error','bounty-empty','map','map-chat','style-large','style-serif','style-soft'];
(async () => {
 fs.mkdirSync(out,{recursive:true});
 const browser = await chromium.launch({executablePath:process.env.CHROMIUM_PATH || '/usr/bin/chromium',args:['--no-sandbox'],headless:true});
 const errors=[], failed=[], external=[], styles=[], styleIndex=new Map(), captures=[], states=[];
 const intern = s=>{let k=JSON.stringify(s);if(!styleIndex.has(k)){styleIndex.set(k,styles.length);styles.push(s);}return styleIndex.get(k);};
 let cssRules, tokens, platformFonts;
 for(const [width,height] of [[1440,900],[390,844]]) {
  const p=await browser.newPage({viewport:{width,height}});
  p.on('pageerror',e=>errors.push(e.message));p.on('requestfailed',r=>failed.push(r.url()));p.on('request',r=>{if(!r.url().startsWith(base)&&!r.url().startsWith('data:')&&!r.url().startsWith('blob:'))external.push(r.url());});
  await p.route('**/app.js',async route=>{const res=await route.fetch();let text=await res.text();text=text.replace(/\}\)\(\);\s*$/, 'window.__audit={state,navigate,openPanel,setMode,renderMain,applySettings,toast};\n})();');if(!text.includes('window.__audit'))throw Error('Instrumentation failed');await route.fulfill({response:res,body:text});});
  for(const scene of scenes){
   await p.goto(base);await p.evaluate(()=>document.fonts.ready);
   await p.evaluate(scene=>{
    const a=window.__audit,s=a.state;
    s.draft={...s.draft,title:'整理会议结论',description:'梳理目标、责任人与下一步行动。',agent:'wuyong',materials:['f1']};
    const pages=['overview','bounty','chat','agents','files','archive','messages','account','settings','help'];
    if(pages.includes(scene))a.navigate(scene);
    else if(scene==='formal-demand'||scene==='formal-confirm'){s.draft.kind='formal';a.openPanel(scene==='formal-demand'?'demand':'confirm');}
    else if(scene.startsWith('task-'))a.openPanel('task',{id:({'task-open':'DEMO-404','task-assigned':'DEMO-401','task-failed':'DEMO-403','task-completed':'DEMO-405'})[scene]});
    else if(scene==='preview')a.openPanel('preview',{id:'f1'});
    else if(scene.startsWith('guide-'))a.openPanel('guide',{step:Number(scene.split('-')[1])});
    else if(scene==='agent-selected'){s.selectedAgent='wuyong';a.navigate('agents');}
    else if(scene==='files-trash'){s.files[0].deleted=true;s.fileFilter='回收站';a.navigate('files');}
    else if(scene==='bounty-empty'){s.taskQuery='不存在的事项';a.navigate('bounty');}
    else if(scene==='demand-error'){a.openPanel('demand');document.querySelector('#demand-error').textContent='请先填写事项名称。';}
    else if(scene==='chat-populated'||scene==='chat-dialog'||scene==='map-chat'){
     s.chats['hall:public']=[{role:'user',text:'请整理会议结论。'},{role:'assistant',text:'【演示回复】先确认目标和资料，不执行真实任务。'}];
     if(scene==='map-chat')a.setMode('map');
     if(scene==='chat-populated')a.navigate('chat');else a.openPanel('chat',{},true);
    } else if(scene==='map')a.setMode('map');
    else if(scene.startsWith('style-')){if(scene==='style-large')s.size='large';if(scene==='style-serif')s.font='serif';if(scene==='style-soft')s.tint='soft';a.applySettings();a.navigate('overview');}
    else a.openPanel(scene);
   },scene);
   await p.waitForTimeout(40);
   const result=await p.evaluate(props=>{
    const dialog=document.querySelector('dialog[open]'),roots=dialog?[dialog]:[document.querySelector('#app')];
    function selector(e){if(e.id)return '#'+CSS.escape(e.id);const bits=[];while(e&&e.tagName!=='BODY'){if(e.id){bits.unshift('#'+CSS.escape(e.id));break;}const tag=e.tagName.toLowerCase(),i=[...e.parentElement.children].filter(n=>n.tagName===e.tagName).indexOf(e)+1;bits.unshift(tag+':nth-of-type('+i+')');e=e.parentElement;}return bits.join(' > ');}
    const nodes=[];for(const root of roots)for(const e of [root,...root.querySelectorAll('*')]){
     const r=e.getBoundingClientRect(),s=getComputedStyle(e);if(!r.width||!r.height||s.visibility==='hidden'||e.closest('[hidden]'))continue;
     const style=Object.fromEntries(props.map(k=>[k,s.getPropertyValue(k)]));
     const attrs=Object.fromEntries([...e.attributes].filter(a=>/^(data-|aria-|href$|target$|rel$|type$|name$|placeholder$|maxlength$|download$|disabled$|title$)/.test(a.name)).map(a=>[a.name,a.value]));
     nodes.push({selector:selector(e),tag:e.tagName.toLowerCase(),class:e.className,label:(e.getAttribute('aria-label')||e.textContent||'').trim().replace(/\s+/g,' ').slice(0,110),rect:{x:r.x,y:r.y,width:r.width,height:r.height},style,attrs,inlineStyle:e.getAttribute('style'),scroll:{width:e.scrollWidth,height:e.scrollHeight,clientWidth:e.clientWidth,clientHeight:e.clientHeight},control:e.matches('a,button,input,textarea,select,summary,[tabindex]')});
    }
    return {nodes,url:location.href,dialog:!!dialog,documentOverflow:document.documentElement.scrollWidth>innerWidth};
   },props);
   result.nodes.forEach(n=>{n.styleId=intern(n.style);delete n.style;});captures.push({scene,width,height,...result});
   if(scene==='overview'&&width===1440){
    cssRules=await p.evaluate(()=>[...document.styleSheets].map(sheet=>({href:sheet.href,rules:[...sheet.cssRules].map((r,i)=>({index:i,css:r.cssText}))})));
    tokens=await p.evaluate(()=>Object.fromEntries([...getComputedStyle(document.documentElement)].filter(k=>k.startsWith('--')).map(k=>[k,getComputedStyle(document.documentElement).getPropertyValue(k).trim()])));
    const cdp=await p.context().newCDPSession(p);await cdp.send('DOM.enable');await cdp.send('CSS.enable');const {root}=await cdp.send('DOM.getDocument');const {nodeId}=await cdp.send('DOM.querySelector',{nodeId:root.nodeId,selector:'.welcome h1'});platformFonts=await cdp.send('CSS.getPlatformFontsForNode',{nodeId});await cdp.detach();
    const button=p.locator('.start-copy button.primary');
    const sample=async name=>{const s=await button.evaluate((e,props)=>Object.fromEntries(props.map(k=>[k,getComputedStyle(e).getPropertyValue(k)])),props);states.push({name,selector:'.start-copy button.primary',styleId:intern(s)});};
    await sample('default');await button.hover();await sample('hover');await p.mouse.move(0,0);await button.focus();await p.keyboard.press('Tab');await p.keyboard.press('Shift+Tab');await sample('keyboard-focus');await button.evaluate(e=>e.disabled=true);await sample('synthetic-disabled');
   }
  }
  await p.close();
 }
 const breakpoints=[];const p=await browser.newPage();for(const [width,height] of [[320,740],[360,740],[600,900],[601,900],[760,900],[761,900],[1000,900],[1001,900],[1200,900],[1201,900],[1500,900],[1501,900],[1599,900],[1600,900],[844,390]]){await p.setViewportSize({width,height});await p.goto(base);await p.evaluate(()=>document.querySelector('[data-view="chat"]').click());await p.waitForTimeout(30);breakpoints.push(await p.evaluate(()=>{const val=s=>{const e=document.querySelector(s),r=e.getBoundingClientRect(),c=getComputedStyle(e);return {width:r.width,height:r.height,padding:c.padding,display:c.display,overflow:c.overflow};};return{width:innerWidth,height:innerHeight,sidebar:val('.sidebar'),header:val('.work-header'),main:val('#work-main'),body:val('#page-body'),footer:val('#page-footer'),stream:val('#chat-stream'),mobileNav:val('.mobile-nav')};}));}
 const report={capturedAt:new Date().toISOString(),browser:await browser.version(),base,viewports:[[1440,900],[390,844]],scenes,properties:props,scope:'Demo only; instrumented fixtures, not end-to-end equivalence or online verification',captures,styles,states,breakpoints,tokens,platformFonts,errors,failed,external};
 fs.writeFileSync(path.join(out,'computed-ui.json'),JSON.stringify(report,null,2)+'\n');fs.writeFileSync(path.join(out,'css-rules.json'),JSON.stringify(cssRules,null,2)+'\n');
 const controls=captures.flatMap(c=>c.nodes.filter(n=>n.control).map(n=>({scene:c.scene,viewport:`${c.width}x${c.height}`,selector:n.selector,label:n.label,tag:n.tag,attrs:n.attrs,styleId:n.styleId})));
 fs.writeFileSync(path.join(out,'controls.json'),JSON.stringify(controls,null,2)+'\n');
 fs.mkdirSync(path.join(out,'source'),{recursive:true});for(const name of ['index.html','styles.css','app.js'])fs.copyFileSync(path.join(root,'deliverables/ui-workbench-demo',name),path.join(out,'source',name));
 console.log(JSON.stringify({captures:captures.length,nodes:captures.reduce((s,c)=>s+c.nodes.length,0),styles:styles.length,controls:controls.length,breakpoints:breakpoints.length,errors,failed,external}));await browser.close();if(errors.length||failed.length||external.length)process.exitCode=1;
})().catch(e=>{console.error(e);process.exit(1)});
