import {launchChrome,evaluate,waitForExpression,stopChrome} from '/home/isp/wsps/cyf/web/scripts/juyiting/e13/lib/cdp-harness.mjs';
import {writeFile} from 'node:fs/promises';
const output='/home/isp/wsps/cyf/docs/implementation/evidence/matter-current-20261104/';
const browser=await launchChrome({debugPort:19465});const cdp=browser.cdp;const results=[];
const check=async(name,expression)=>{const r=await evaluate(cdp,`(()=>{${expression}})()`);if(r!==true)throw Error(name+': '+JSON.stringify(r));results.push(name);};
try{
 await cdp.send('Page.navigate',{url:'http://localhost:18786/index.html?ui=20261104-matter-edit&scenario=matter-edit-check#home'});
 await waitForExpression(cdp,'typeof canEditMatterRequirement==="function" && !!document.querySelector(".juyi-page")');
 for(const width of [1440,390,320]){
  await cdp.send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});
  await evaluate(cdp,`state.draft='根据资料整理统计。';state.title='原始标题';state.draftFiles=['ref-brief'];ensureUnifiedTask();go('detail');`);
  await check(width+' three entry points',`return document.querySelectorAll('[data-action="complete-edit-requirement"]').length===3;`);
  await check(width+' unchanged title preserves selection',`const kept=commissionEligible()[0].id;state.task.assignmentCandidate=kept;document.querySelector('[data-field=title]').click();document.querySelector('[data-action=complete-save-requirement]').click();return state.task.assignmentCandidate===kept&&!document.querySelector('dialog');`);
  await check(width+' cancel title',`document.querySelector('[data-field="title"]').click();document.querySelector('[data-requirement-value]').value='不应保存';document.querySelector('dialog [data-action="close-dialog"]').click();return state.task.title==='原始标题';`);
  await check(width+' empty title rejected',`document.querySelector('[data-field="title"]').click();document.querySelector('[data-requirement-value]').value='  ';document.querySelector('[data-action="complete-save-requirement"]').click();return state.task.title==='原始标题'&&!document.querySelector('[data-edit-error]').hidden;`);
  await check(width+' save title safely',`document.querySelector('[data-requirement-value]').value='新标题 <script> &';document.querySelector('[data-action="complete-save-requirement"]').click();return state.task.title==='新标题 <script> &'&&document.querySelector('.matter-advice-card h3').textContent===state.task.title&&!document.querySelector('dialog');`);
  await check(width+' save description',`document.querySelector('[data-field="description"]').click();document.querySelector('[data-requirement-value]').value='第一行\\n第二行';document.querySelector('[data-action="complete-save-requirement"]').click();return state.task.description==='第一行\\n第二行';`);
  await check(width+' cancel materials',`const old=JSON.stringify(state.task.files);document.querySelector('[data-field="files"]').click();picker.ids=['ref-html'];document.querySelector('dialog [data-action="close-dialog"]').click();return JSON.stringify(state.task.files)===old;`);
  await check(width+' save materials not draft',`const draft=JSON.stringify(state.draftFiles);document.querySelector('[data-field="files"]').click();picker.ids=['ref-html','ref-brief'];document.querySelector('[data-action="confirm-materials"]').click();return state.task.files.join(',')==='ref-html,ref-brief'&&JSON.stringify(state.draftFiles)===draft&&document.querySelector('.matter-advice-card').textContent.includes('2 份资料');`);
  await check(width+' unchanged material set preserves selection',`const kept=commissionEligible()[0].id;state.task.assignmentCandidate=kept;document.querySelector('[data-field=files]').click();picker.ids=[...state.task.files].reverse();document.querySelector('[data-action=confirm-materials]').click();return state.task.assignmentCandidate===kept&&!document.querySelector('dialog');`);
  await check(width+' previews retained',`return document.querySelectorAll('.task-material-links [data-action="preview"]').length===2;`);
  await check(width+' storage failure rolls back',`document.querySelector('[data-field="title"]').click();const original=persist;persist=()=>false;document.querySelector('[data-requirement-value]').value='不可保存';document.querySelector('[data-action="complete-save-requirement"]').click();persist=original;const ok=state.task.title==='新标题 <script> &'&&!document.querySelector('[data-edit-error]').hidden;document.querySelector('dialog').close();return ok;`);
  await check(width+' stale task cannot be edited',`document.querySelector('[data-field="title"]').click();const old=state.task;state.task={...old,title:'另一个事项'};document.querySelector('[data-requirement-value]').value='错误写入';document.querySelector('[data-action="complete-save-requirement"]').click();const ok=state.task.title==='另一个事项'&&old.title==='新标题 <script> &';document.querySelector('dialog').close();state.task=old;render();return ok;`);
  await check(width+' no horizontal page overflow',`return document.documentElement.scrollWidth<=innerWidth;`);
  const shot=await cdp.send('Page.captureScreenshot',{format:'png',captureBeyondViewport:false});await writeFile(output+width+'-detail.png',Buffer.from(shot.data,'base64'));
  await cdp.send('Page.reload');await waitForExpression(cdp,'typeof canEditMatterRequirement==="function" && !!document.querySelector("[data-field=title]")');
  await check(width+' reload retains edits',`return state.task.title==='新标题 <script> &'&&state.task.files.length===2&&state.agent===null;`);
  await check(width+' confirmed read only',`state.agent={id:'demo-agent',name:'林冲'};state.task.phase='进行中';render();return !document.querySelector('[data-action="complete-edit-requirement"]');`);
  await check(width+' canceled read only',`state.agent=null;state.task.cancelled=true;render();return !document.querySelector('[data-action="complete-edit-requirement"]');`);
 }
 await writeFile(output+'results.json',JSON.stringify({date:'2026-11-04',scope:'offline prototype only',passed:results.length,checks:results},null,2));console.log(JSON.stringify({passed:results.length}));
}finally{cdp.close();await stopChrome(browser.chrome,browser.userDataDir);}
