'use strict';
// Latest UI stays authoritative. This file only completes OFFLINE, local interactions.
const prototypePages=[['办事','home'],['事项','tasks'],['提出需求','create'],['点将册','agents'],['事项详情','detail'],['榜文议事','chat'],['密议','private'],['厅前公议','public'],['资料','workspace'],['资料详情','file'],['我的','mine'],['典籍阁','library'],['阅读器','reader'],['消息','messages'],['招贤令','catalog'],['厅中实景','map'],['使用帮助','help'],['个人中心入口','account'],['正式成果','results']];
function seedBaseline(){
 if(state.initializedScenario){if(page==='private'&&!state.privateChats[state.privateAgentId]){state.privateAgentId='0';state.privateChats['0']={agent:{id:'0',name:'宋江'},messages:[],outputs:[],delivery:[],chatDraft:'',chatFiles:[],quote:null,pending:false};}return;}
 const scenario=selectedScenario;state.baselineScenario=scenario;state.initializedScenario=true;
 const formal=['chat','detail','results'].includes(page),privatePage=page==='private';
 if(formal){state.task={title:'自然观察活动资料',description:'画一只鸟，并整理一份活动方案。',files:['ref-brief'],complete:false};state.agent={id:'0',name:'宋江'};state.selectedAgent={...state.agent};state.messages=[{role:'USER',text:state.task.description,files:['ref-brief']},{role:'AGENT',text:'你期望什么风格？可以在同一话头继续补充。'}];}
 if(privatePage){state.selectedAgent={id:'0',name:'宋江'};state.privateAgentId='0';state.privateChats['0']={agent:{...state.selectedAgent},messages:[],outputs:[],delivery:[],chatDraft:'',chatFiles:[],quote:null,pending:false};}
 const ctx=conversation();
 if(['chat','private','public'].includes(page)){
  if(scenario==='empty')ctx.messages=[];
  if(['waiting','streaming'].includes(scenario)){ctx.pending=true;ctx.pendingReason='fixture';}
  if(['results','completed'].includes(scenario)&&!ctx.outputs.length){const ids=['image','audio','document','text'].map(type=>output(type,'一只小鸟停在枝头。',1,ctx));ctx.delivery=[...ids];ctx.messages.push({role:'AGENT',text:'本次示例成果如下，可预览、下载、保存或引用修改。',outputs:ids});}
 }
 if(['cancel-ready','cancel-unknown','cancelled','history-error'].includes(scenario)&&state.task){state.task.notStarted=true;state.task.cancelled=['cancelled','history-error'].includes(scenario);if(state.task.cancelled){const id=output('text','保留的历史文字成果（离线示例）',1,state);state.delivery=[id];}state.cancellation={writes:0,status:'ready'};state.historyError=scenario==='history-error';}
 if(scenario==='completed'&&state.task){if(!state.outputs.length){const ids=['image','audio','document','text'].map(type=>output(type,'一只小鸟停在枝头。',1,state));state.delivery=ids;state.messages.push({role:'AGENT',text:'本次示例成果如下。',outputs:ids});}state.task.complete=true;state.final=[...state.delivery];state.operation={id:'demo-completed-operation',outputs:[...state.final],stage:'completed',writes:1};}
}
const optimizedComposer=syncCurrentComposer;
syncCurrentComposer=function(panel){optimizedComposer(panel);const ctx=conversation(),locked=ctx.pending||!!(ctx.task?.complete||ctx.task?.cancelled);const voice=$('.voice-start',panel);if(voice){voice.disabled=locked;voice.innerHTML=uiIcon('mic');voice.title='语音输入';}
 const actions=$('.composer-actions',panel);$('.composer-attach',panel)?.remove();const attach=document.createElement('button');attach.type='button';attach.className='composer-attach';attach.dataset.action='complete-materials';attach.title='添加资料';attach.setAttribute('aria-label','添加资料');attach.disabled=locked||state.baselineScenario==='recording';attach.innerHTML='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 11.5l-8.6 8.6a6 6 0 0 1-8.5-8.5l9-9a4 4 0 0 1 5.7 5.7l-9 9a2 2 0 0 1-2.8-2.8l8.3-8.3"/></svg>';actions.insertBefore(attach,$('.composer-inline-voice',actions));
 const more=$('.composer-more',panel);more.disabled=locked||state.baselineScenario==='recording';more.innerHTML=uiIcon('plus');more.title='更多操作';more.setAttribute('aria-label','更多操作');
 $('.composer-send',panel).innerHTML='<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5m-6 6 6-6 6 6"/></svg>';
 const form=$('.composer-submit',panel);
 $$('.composer-context,.composer-meta',panel).forEach(e=>e.remove());
 const contextLabel=page==='private'?'密议':page==='public'?'厅前公议':'榜文议事 / '+taskTitle();
 form.insertAdjacentHTML('afterbegin',`<div class="composer-context ${page==='private'?'is-private':'is-bounty'}"><span class="composer-context-label" title="${esc(contextLabel)}">${esc(contextLabel)}</span>${ctx.agent?`<span class="composer-target-chip" aria-label="传话对象">@${esc(ctx.agent.name)}</span>`:''}</div>`);
 form.insertAdjacentHTML('beforeend',`<div class="composer-meta"><span data-draft-count>${ctx.chatDraft.length}/1200</span><span>${ctx.pending?'候回话':page==='public'?'公共议事':page==='private'?'只与当前好汉交流':'只与当前承办交流'}</span></div>`);
 $('.composer-textarea',panel).maxLength=1200;
 const summary=$('.context-summary small',panel);if(summary)summary.title=summary.textContent;
 $$('.toolbar-actions button',panel).forEach(b=>{b.disabled=!!(ctx.pending||ctx.historyDeletingId||$('.inline-voice-status',panel)||((ctx.task?.complete||ctx.task?.cancelled)&&b.getAttribute('aria-label')!=='话头记录'));});
 if(['waiting','streaming'].includes(state.baselineScenario)&&!ctx.pending){$$('.is-pending',panel).forEach(e=>e.remove());}
 const menu=$('.composer-more',panel);menu?.setAttribute('aria-expanded','false');
 // Preserve actions and state, while the compact CSS positions toolbar right and voice before send.
 $('[aria-label="话头记录"]',panel)?.setAttribute('aria-expanded',String(!!ctx.historyOpen));
 const mapping={'ui-refresh':'complete-refresh','ui-history':'complete-history','ui-new':'complete-new','ui-voice':'complete-voice','ui-voice-stop':'complete-voice-stop','ui-voice-cancel':'complete-voice-cancel','ui-voice-append':'complete-voice-append','ui-voice-replace':'complete-voice-replace'};
 for(const [old,next] of Object.entries(mapping))$$(`[data-action="${old}"]`,panel).forEach(e=>e.dataset.action=next);
 if(ctx.historyOpen)renderConversationHistory();
};
const completionMore=showMore;
showMore=function(){completionMore();$('.composer-more-panel .composer-add-materials')?.remove();const more=$('.composer-more');if(more)more.setAttribute('aria-expanded',String(!!$('.composer-more-panel')));};
const optimizedSupplement=renderSupplement;
renderSupplement=function(){optimizedSupplement();document.title=labels[page]+' · 界面优化基准（离线交互）';const note=$('.baseline-provenance');if(note)note.textContent='界面对齐候选 · 2026-10-16 · 离线示例';
 $$('.workbench-account-action,.workbench-sidebar-account').forEach(e=>{e.disabled=false;e.dataset.prototypePage='account';});
 const brand=$('.workbench-brand');if(brand){brand.dataset.prototypePage='home';}
 if(page==='create'||unifiedTask()&&['chat','detail','results'].includes(page)){const crumb=$('.workbench-breadcrumb strong');if(crumb)crumb.textContent=page==='create'?'提出需求':'议事';if(page==='chat'){const title=$('#juyiting-floating-panel-title');if(title)title.textContent='议事';}}
 if(page==='home'){$$('.overview-tabs button').forEach((b,i)=>{b.dataset.action='complete-overview-tab';b.dataset.tab=String(i);b.setAttribute('aria-pressed',String((state.overviewTab||0)===i));});}
 if(page==='workspace'){$$('[data-action="ui-file"]').forEach(e=>e.remove());}
 if(page==='results')renderFormalResults();
 if(page==='catalog')renderRuntimeCatalog();
 if(page==='file')renderFileDetail();
 if(page==='library')renderLibrary();
 if(page==='reader')renderReader();
 if(page==='messages')renderMessages();
 if(page==='mine'){const root=$('.hall-mine-page');if(root&&!$('[data-action="complete-entries"]',root))root.insertAdjacentHTML('beforeend',`<div class="mmd baseline-extra">${button('全部入口','complete-entries')}${button('页面与状态索引','complete-index')}</div>`);}
 if(page==='help'){const root=$('.baseline-page');if(root)root.insertAdjacentHTML('beforeend',`<div class="mmd baseline-extra">${button('全部入口','complete-entries')}${button('页面与状态索引','complete-index')}</div>`);}
 refreshAllPageSurfaces();
 syncProductionNavigation();
 // Restore history after the visual shell is rerendered.
 if(['chat','private','public'].includes(page)&&conversation().historyOpen)renderConversationHistory();
};
// Presentation groups only: never mutate the underlying task or acceptance state.
const taskStatusNames=['待你补充','需核对','正在处理','已有结果','待点将','筹划中','议事中','办理中','待验收','受阻','已完成','失败','已取消','已归档'];
const taskGroups=['全部','待我处理','进行中','已结束'];
function taskBucket(){if(unifiedTask())return state.task.phase;return state.task?.cancelled?'已取消':state.task?.complete?'已完成':state.operation&&state.operation.stage!=='completed'?'受阻':state.error?'受阻':!state.agent?'待点将':state.pending?'办理中':state.outputs.length?'待验收':'议事中';}
function taskInGroup(group,bucket=taskBucket()){
 if(!state.task)return false;
 if(group==='全部')return true;
 if(group==='已结束')return ['已完成','失败','已取消','已归档','成果已归档'].includes(bucket);
 if(group==='待我处理')return ['待你补充','需核对','待点将','待验收','受阻'].includes(bucket)&&!state.pending&&state.operation?.stage!=='pending';
 return !['已完成','失败','已取消','已归档','成果已归档'].includes(bucket);
}
function productionTaskStatus(){const b=taskBucket();return {'议事中':'待开工（已点将）','正在处理':'办理中','已有结果':'待验收','待你补充':'受阻','需核对':'受阻','成果已归档':'已归档'}[b]||b;}
// Task browsing fixtures are separate from the user's unsubmitted requirement.
// Reading the list must never create a task or send a message.
const matterContextKeys=['task','agent','messages','outputs','delivery','final','operation','pending','pendingReason','error','chatDraft','chatFiles','quote','histories','historyOpen','cancellation','baselineScenario','topicId','topicTitle','topicUpdatedAt','historyPageLimit'];
function blankMatterContext(){return {task:null,agent:null,messages:[],outputs:[],delivery:[],final:[],operation:null,pending:false,pendingReason:null,error:null,chatDraft:'',chatFiles:[],quote:null,histories:[],historyOpen:false,cancellation:{writes:0,status:'ready'},baselineScenario:'ready'};}
function matterContextSnapshot(ctx=state){return structuredClone(Object.fromEntries(matterContextKeys.map(key=>[key,ctx[key]??blankMatterContext()[key]])));}
function currentMatterKey(){return state.task?.id||state.matterSelectionKey||'legacy-active';}
function ensureMatterLibrary(){
 if(state.matterLibrary)return;
 state.matterLibrary={};
 if(selectedScenario!=='empty'){
  const fixtures=[
   ['demo-list-001','整理亲子自然观察活动方案','梳理活动目标、人员分工与准备清单。','文案整理',null,false],
   ['demo-list-002','设计自然观察活动海报','准备一张突出活动主题的海报，先在议事中确认风格。','创意设计',{id:'1',name:'公孙胜'},false],
   ['demo-list-003','汇总活动筹备清单','已整理人员、物料与时间安排，保留结果供查看。','资料汇总',{id:'0',name:'宋江'},true]
  ];
  for(const [id,title,description,ability,agent,complete] of fixtures){
   const ctx=blankMatterContext();ctx.task={id,title,description,files:['ref-brief'],requiredAbilities:[ability],complete,example:true};ctx.agent=agent;
   ctx.messages=[{role:'USER',text:description,files:['ref-brief']}];
   if(agent)ctx.messages.push({role:'AGENT',text:complete?'筹备清单已整理，见下方示例文件。':'希望海报偏自然手绘，还是简洁信息排版？请在这里补充。'});
   if(complete){const out={id:id+'-result',name:'活动筹备清单.txt',type:'text',text:'筹备清单（离线示例）\n1. 确认活动时间与人员\n2. 准备观察材料\n3. 核对现场安排',note:'已完成 · 离线示例'};ctx.outputs=[out];ctx.delivery=[out.id];ctx.final=[out.id];ctx.messages[1].outputs=[out.id];ctx.operation={id:id+'-acceptance',stage:'completed',outputs:[out.id],writes:1};}
   state.matterLibrary[id]=ctx;
  }
 }
 // Recover previously preserved local matters without replacing current drafts.
 (state.previousMatters||[]).forEach((ctx,i)=>{const key=ctx.task?.id||'legacy-history-'+i;if(ctx.task&&!state.matterLibrary[key])state.matterLibrary[key]=Object.assign(blankMatterContext(),structuredClone(ctx));});
}
function saveMatterContext(){ensureMatterLibrary();if(state.task)state.matterLibrary[currentMatterKey()]=matterContextSnapshot();}
function listedMatters(){
 ensureMatterLibrary();const current=state.task?currentMatterKey():null;
 return [...(state.task?[{key:current,ctx:state,current:true}]:[]),...Object.entries(state.matterLibrary).filter(([key])=>key!==current).map(([key,ctx])=>({key,ctx,current:false}))];
}
function listedMatterStatus(ctx){
 if(ctx===state)return productionTaskStatus();
 if(ctx.task.unified)return {'正在处理':'办理中','已有结果':'待验收','待你补充':'受阻','需核对':'受阻'}[ctx.task.phase]||ctx.task.phase;
 return ctx.task.cancelled?'已取消':ctx.task.complete?'已完成':ctx.operation&&ctx.operation.stage!=='completed'||ctx.error?'受阻':!ctx.agent?'待点将':ctx.pending?'办理中':ctx.outputs.length?'待验收':'待开工（已点将）';
}
function listedMatterClass(ctx){return 'task-state-'+({'待点将':'open','筹划中':'planning','待开工（已点将）':'assigned','办理中':'running','待验收':'reviewing','受阻':'blocked','已完成':'done','失败':'failed','已取消':'cancelled','已归档':'archived'}[listedMatterStatus(ctx)]||'unknown');}
function openListedMatter(key){
 ensureMatterLibrary();
 if(state.task&&key===currentMatterKey()){go('detail');return;}
 if(state.pending||state.operation?.stage==='pending'){feedback('当前事项正在处理，请等回复完成后再切换；原输入已保留。');return;}
 const ctx=state.matterLibrary[key];if(!ctx)return;
 saveMatterContext();Object.assign(state,matterContextSnapshot(ctx));state.matterSelectionKey=key;state.selectedAgent=state.agent?{...state.agent}:null;
 state.recommendation=null;persist();go('detail');
}
function applyTaskFilters(){
 const rows=listedMatters(),query=(state.taskSearch||'').trim().toLowerCase();let visible=0;
 for(const card of $$('.task-card')){
  const row=rows.find(r=>r.key===card.dataset.matterKey),ctx=row?.ctx;
  const match=!!ctx&&(!state.taskFilter||listedMatterStatus(ctx)===state.taskFilter)&&(!state.taskAbility||(ctx.task.requiredAbilities||[]).includes(state.taskAbility))&&(!query||[ctx.task.id,ctx.task.title,ctx.task.description].join(' ').toLowerCase().includes(query));
  card.hidden=!match;card.style.display=match?'':'none';if(match)visible++;
 }
 const empty=$('.baseline-empty');if(empty){empty.hidden=visible>0;empty.innerHTML=rows.length?'没有符合筛选条件的事项。'+button('清除筛选','complete-task-clear'):'暂无事项，点击右上方“提出需求”开始。';}
 const count=$('[data-task-list-count]');if(count)count.textContent=`显示 ${visible} / ${rows.length} 项 · 示例数据仅存本地，不是账号真实事项`;
}
function simplifyHome(){
 $$('.workbench-create-action').forEach(e=>{e.dataset.prototypePage='create';});
 const aside=$('.overview-aside-card');if(aside)aside.innerHTML='<h3>需要你看一眼</h3><p>查看需要补充或核对的事项。</p>'+button('查看待处理列表','complete-go','data-page=tasks');
 if(aside)scoped(aside,'data-v-d13db084');
 const map=$('.overview-map-link');if(map)map.dataset.prototypePage='map';
 const heading=$('.overview-list-heading h3');if(heading)heading.textContent='接着上次办';
 const title=$('.overview-start-copy h2,.overview-start-copy h3');if(title)title.textContent='说一句你想办成的事';
 const next=$('.overview-quick-request button.primary');if(next)next.textContent='开始办事';

 const intro=$('.overview-start-copy>p');if(intro)intro.textContent='结果、补充要求和后续修改，都在同一段议事里继续。';
 const all=$('.overview-list-heading [data-prototype-page="tasks"]');if(all)all.textContent='悬赏榜';
 const refresh=$$('.overview-list-heading button').find(b=>b.textContent==='刷新');if(refresh)refresh.dataset.action='complete-task-refresh';
 const tab=state.overviewTab||0;
 $$('.overview-tabs button').forEach((b,i)=>{b.textContent=['最近事项','需要我处理','案卷'][i];});
 $$('.overview-item').slice(1).forEach(e=>e.remove());
 const card=$('.overview-item'),visible=!!state.task&&(tab===0||tab===1&&taskInGroup('待我处理')||tab===2&&!!state.task.archived);
 if(card){card.hidden=!visible;card.style.display=visible?'':'none';$$('.overview-technical',card).forEach(e=>e.remove());for(const b of $$('button',card)){b.dataset.prototypePage=unifiedTask()?'chat':'detail';b.textContent=unifiedTask()?'继续议事':state.task?.complete||state.task?.cancelled?'查看记录':'查看事项';}}
 const section=$('.overview-section');if(section){$$(':scope > button',section).forEach(e=>e.remove());if(!visible)section.insertAdjacentHTML('beforeend',`<p class="simplify-home-empty" role="status">${!state.task?'还没有事项，从上方提出第一个需求。':tab===1?'暂时没有需要你处理的事项。':'暂无已归档案卷。'}</p>`);}
}
function renderInteractiveList(){
 if(page==='home'){simplifyHome();return;}
 if(page!=='tasks')return;
 const rows=listedMatters(),list=$('.task-list');
 if(list){
  list.innerHTML=rows.map(({key,ctx,current})=>`<article class="task-card${current?' selected':''}" data-matter-key="${esc(key)}" data-action="complete-open-matter" tabindex="0" role="button" aria-label="查看事项：${esc(ctx.task.title)}"><div class="task-head"><strong>${esc(ctx.task.title)}</strong><span class="${listedMatterClass(ctx)}">${esc(listedMatterStatus(ctx))}</span></div><p>${esc(ctx.task.description)}</p><div class="task-meta"><span>${esc(ctx.task.id||key)}</span>${ctx.agent?`<span>领令：${esc(ctx.agent.name)}</span>`:''}<span>${ctx.task.example?'离线示例':'本地演示事项'}</span></div><div class="ability-tags">${(ctx.task.requiredAbilities?.length?ctx.task.requiredAbilities:['不拘本领']).map(a=>`<span>${esc(a)}</span>`).join('')}</div></article>`).join('')+'<div class="mmd baseline-empty empty-list" role="status" hidden></div>';
  scoped(list,'data-v-9209fea5');
 }
 const tabs=$('.task-status-tabs');
 const statuses=['待点将','筹划中','待开工（已点将）','办理中','待验收','受阻','已完成','失败','已取消','已归档'];
 if(tabs){tabs.setAttribute('aria-label','事项状态');tabs.innerHTML=statuses.map(name=>button(`${name} <span>${rows.filter(r=>listedMatterStatus(r.ctx)===name).length}</span>`,'complete-production-status',`data-status="${name}" aria-pressed="${state.taskFilter===name}" class="${state.taskFilter===name?'active':''}"`)).join('');tabs.insertAdjacentHTML('afterend','<p class="task-list-summary" data-task-list-count role="status"></p>');}
 const search=$('.task-search input');if(search){search.value=state.taskSearch||'';search.dataset.completeTaskSearch='true';}
 const ability=$('.task-search select');if(ability){const values=[...new Set(rows.flatMap(r=>r.ctx.task.requiredAbilities||[]))];if(state.taskAbility&&!values.includes(state.taskAbility))values.push(state.taskAbility);ability.innerHTML='<option value="">不拘本领</option>'+values.map(v=>`<option value="${esc(v)}">${esc(v)}</option>`).join('');ability.value=state.taskAbility||'';ability.dataset.completeTaskAbility='true';}

 applyTaskFilters();
}
function createProblem(){const unknown=state.simulation.create==='unknown';dialog(unknown?'提交状态待核对':'提交失败（示例）',`<p>${unknown?'尚不能确认受理，先核对状态，不重复创建。':'明确未受理。需求和附件均保留，可返回修改。'}</p>`,button(unknown?'核对创建状态':'返回修改','complete-create-status'));}
function beginAcceptance(){if(state.operation||!finalDraft.length||!state.task||state.task.cancelled||state.task.complete||state.pending)return;state.operation={id:'demo-operation-'+(++serial),outputs:[...finalDraft],stage:'pending',writes:1};if(page==='detail')renderDetail();persist();$('dialog[open]')?.close();operationDialog();setTimeout(resolveOperation,650);}
function operationDialog(){const op=state.operation;if(!op)return;finalDraft=[...op.outputs];dialog('验收进度',`<p role="status">${op.stage==='pending'?'正在核对原验收操作…':op.stage==='failed'?'验收未完成。原操作和成果已保留。':'验收状态未知。不重新提交验收。'}</p><small>原操作 ${esc(op.id)} · 冻结 ${op.outputs.length} 项成果</small><div class="mmd-attachments">${deliveryList()}</div>`,button('返回详情','complete-operation-detail')+button('查询原操作状态','complete-operation-status'));}
function resolveOperation(){const op=state.operation;if(!op||state.task?.complete)return;if(state.simulation.accept==='ok'){op.stage='completed';state.final=[...op.outputs];state.task.complete=true;persist();const d=$('dialog[open]');if(d?.getAttribute('aria-label')==='验收进度'){d.close();go('detail');feedback('示例验收完成。');}else render();return;}op.stage=state.simulation.accept==='failed'?'failed':'unknown';if(page==='detail')renderDetail();if(page==='results')renderFormalResults();persist();const d=$('dialog[open]');if(d?.getAttribute('aria-label')==='验收进度'){d.close();operationDialog();}}
async function addLocalFiles(selected){const ids=[];try{for(const f of selected){const id='local-'+(++serial),type=f.type.startsWith('image/')?'image':f.type.startsWith('audio/')?'audio':/text|json/.test(f.type)||/\.(txt|md|csv)$/i.test(f.name)?'text':'document';const a={id,name:f.name,type,note:'本机附件 · 不上传'};a.text=type==='text'?await f.text():type==='document'?'此格式仅演示选取与下载，未支持内容解析；不是已实现格式能力。':'';a.url=await new Promise((r,j)=>{const reader=new FileReader();reader.onload=()=>r(reader.result);reader.onerror=j;reader.readAsDataURL(f);});state.localFiles.push(a);ids.push(id);}const selectedIds=[...new Set([...picker.ids,...ids])],context=picker.context;$('dialog[open]')?.close();persist();openMaterials(context,selectedIds);}catch{feedback('本机示例文件未读取成功，已确认资料不变。');}}
function renderFileDetail(){
 const root=$('.baseline-page'),a=asset(state.fileId||'ref-brief');if(!root||!a)return;const meta=state.fileMeta[a.id]||{};
 const selected=meta.demoVersion||'1',versions=meta.demoHistory?(meta.demoHistoryLoaded?Array.from({length:102},(_,i)=>String(102-i)):Array.from({length:100},(_,i)=>String(102-i))):['1'];
 root.classList.add('all-file-detail','personal-workspace','is-hall-treasure');
 root.innerHTML=`<div class="treasure-content"><div class="treasure-file-heading"><div><h2>${esc(a.name)}</h2><p>${state.saved.includes(a.id)?'成果':'资料'} · ${meta.recycled?'已回收':'仅自己可见'} · 离线示例</p></div>${button(state.fileManage?'返回预览':'更多管理','complete-file-manage')}</div><div class="file-preview-body" ${state.fileManage?'hidden':''}><div class="treasure-preview-tools treasure-version-tools"><label>版本 <select aria-label="文件版本" data-workspace-version>${versions.map(v=>`<option value="${v}" ${selected===v?'selected':''}>v${v} · ${esc(a.name)}</option>`).join('')}</select></label>${button('下载','download',`data-id="${a.id}"`)}</div>${meta.demoHistory&&!meta.demoHistoryLoaded?button('读取更早版本','complete-workspace-history-more'):''}<p class="treasure-note">本次使用固定的 v${selected}；已有事项中的资料引用不会随新版本替换。</p>${meta.demoPartial?'<p class="treasure-note" role="status">预览内容不完整；请下载原文件查看。（离线状态示例）</p>':''}${meta.demoDetailError?`<p class="treasure-note" role="status">上传已保存，但详情读取失败；请重读详情，不要重复提交。（离线状态示例） ${button('重读详情','complete-workspace-detail-retry')}</p>`:''}<section class="treasure-preview" aria-label="文件预览">${media(a)}</section><div class="treasure-actions">${!meta.recycled?button('用于新委托','complete-use-file','class="treasure-primary"'):''}${button('预览','preview',`data-id="${a.id}"`)}</div><details class="treasure-note"><summary>离线修复状态演示</summary><p>仅演示交互；版本使用同一份示例内容，不代表服务端写入或不同历史字节。</p><div class="treasure-actions">${button('演示历史分页','complete-workspace-history-demo')}${button('演示部分预览','complete-workspace-partial-demo')}${button('演示保存后详情失败','complete-workspace-detail-demo')}${button('演示提交结果未知','complete-workspace-unknown-demo')}</div></details></div><section class="treasure-management ${state.fileManage?'is-open':''}" ${state.fileManage?'':'hidden'} aria-label="文件管理"><h3>文件管理</h3><p>旧版本及已有事项引用保留。本原型只修改示例文件，不上传到服务器。</p><div class="treasure-form"><label>上传新版本<input type="file" disabled aria-label="上传新版本（此原型未模拟）"></label><small>当前只演示固定 v1；新版本写入不在本原型中模拟。</small><button disabled>上传为新版本</button></div>${button('重命名','complete-rename')}${button(meta.recycled?'恢复':'移到回收站','complete-recycle')}</section></div>`;
 scoped(root,'data-v-a1bd66a6');
}
function renderLibrary(){
 const root=$('.baseline-page');if(!root)return;const tab=state.libraryTab||'reader';root.classList.add('library-panel');
 root.innerHTML=`<div class="library-tabs" role="tablist" aria-label="典籍阁入口">${button('典籍阅读','complete-library-tab',`data-tab="reader" role="tab" aria-selected="${tab==='reader'}" class="${tab==='reader'?'active':''}"`)}${button('案卷检索','complete-library-tab',`data-tab="search" role="tab" aria-selected="${tab==='search'}" class="${tab==='search'?'active':''}"`)}</div>`;
 if(tab==='reader')root.insertAdjacentHTML('beforeend',`<section class="archive-reader is-embedded-reader"><div class="archive-shelf"><header class="archive-shelf-header"><div><p class="reader-kicker">典籍阅读</p><h3>阁中典籍</h3><p>先择一部典籍，再进入沉浸翻阅。</p></div><span class="archive-shelf-count">共 1 部</span></header><article class="archive-book-card"><div class="archive-book-cover" aria-hidden="true"><span>古典</span><strong>水滸傳</strong><small>一百二十回</small></div><div class="archive-book-info"><p class="reader-kicker">已收录典籍</p><h4>水滸傳</h4><p>阅读、目录、书签与私人手札。原型正文采用脱敏排版示例。</p>${button('进入翻阅','complete-go','data-page="reader" class="archive-book-open"')}</div></article></div></section>`);
 else root.insertAdjacentHTML('beforeend',`<div class="library-search-tab"><form class="baseline-search library-search"><input aria-label="案卷检索关键词" placeholder="查项目案卷、议事旧录、往日回报" value="${esc(state.libraryQuery||'')}"><select aria-label="案卷来源" data-library-source><option value="all">全部案卷</option><option value="project">项目案卷</option><option value="meeting">议事旧录</option><option value="memory">长记</option></select>${button('查卷','complete-library-search')}</form><div class="library-hint"><span>藏书查卷</span><span>离线检索示例</span></div><div data-search-results class="result-list">${state.librarySearched?(state.libraryQuery?.match(/自然|活动/)&&(!state.librarySource||['all','project'].includes(state.librarySource))?`<article class="result-card"><div class="result-head"><strong>自然观察活动案卷</strong><small>示例案卷</small></div><p>亲子家庭自然观察活动的结论与待办。引用后仍需由你确认交办。</p><div class="result-meta">项目案卷 · 本地示例</div>${button('引用并起草需求','complete-case-draft')}</article>`:'<p class="empty-list" role="status">暂未查得案卷，请换个关键词或来源。</p>'):'<p class="empty-list" role="status">输入关键词后查阅案卷阁。</p>'}</div></div>`);
 scoped(root,'data-v-1c1bde34');if($('.archive-reader',root))scoped($('.archive-reader',root),'data-v-6cf6adee');if($('[data-library-source]'))$('[data-library-source]').value=state.librarySource||'all';const form=$('.library-search',root);if(form)form.addEventListener('submit',e=>{e.preventDefault();state.libraryQuery=$('input',form).value;state.librarySearched=true;render();});
}
function renderReader(){
 const root=$('.baseline-page');if(!root)return;state.reader||={chapter:1,bookmarks:[],notes:''};const r=state.reader;
 root.classList.add('all-reader');root.innerHTML=`<section class="archive-reader-fullscreen all-reader-frame"><header class="reader-header"><div class="reader-heading"><p class="reader-kicker">固定典籍 · 离线排版样例</p><h3 id="archive-reader-title">水滸傳</h3></div><div class="reader-header-actions"><span class="save-state">仅存于本原型</span>${button('目录','complete-toc','class="reader-header-button"')}${button('手札','complete-reader-notes','class="reader-header-button" aria-expanded="'+!!r.notesOpen+'"')}</div></header><div class="reader-layout ${r.notesOpen?'notes-open':''}"><article class="reader-content baseline-reader" tabindex="0"><h4>第${r.chapter}回 · 阅读排版示例</h4><p>以下是原型专用示例，不复制账号的阅读记录、手札或真实文件。</p><p>山间清晨，同行者整理一路的见闻，把需要进一步核实的内容记在纸上。阅读时可查看目录、留下书签，并将所选内容带入需求草稿。</p><p>这一页演示正文的字号、行距和独立滚动。切换章回后，书签和手札仍保存在当前原型会话中，不发送给生产服务。</p><p>想继续处理相关资料时，引用到需求即可。系统推荐承办后，由你确认，后续补充和结果都在同一议事中继续。</p></article><aside class="reader-notes" ${r.notesOpen?'':'data-desktop-notes'}><h4>私人手札</h4><textarea aria-label="手札草稿" placeholder="记录此处所思，仅存本地原型。">${esc(r.notes||'')}</textarea>${button('保存手札','complete-reader-save','class="note-save"')}<p class="reader-note-status" role="status">${r.notes?'已有本地手札':'尚未记录手札'}</p><h4>引用与提问</h4><p>引用示例段落起草需求，不会自动发送给好汉。</p>${button('引用当前段落起草交办','complete-reader-cite')}</aside></div><footer class="reader-footer">${button('上一回','complete-chapter',`data-chapter="${r.chapter-1}" ${r.chapter===1?'disabled':''}`)}<span>第 ${r.chapter} / 2 回（示例）</span>${button('下一回','complete-chapter',`data-chapter="${r.chapter+1}" ${r.chapter===2?'disabled':''}`)}${button('书签','complete-bookmarks')}${button('引用起草需求','complete-reader-cite')}</footer></section>`;
 scoped(root,'data-v-6cf6adee');
}
function renderMessages(){
 const root=$('.baseline-page');if(!root)return;root.classList.add('all-messages');
 const needs=taskInGroup('待我处理');root.innerHTML=`<section class="hall-overview is-messages"><div class="overview-list-heading"><h3>需要我处理</h3>${button('刷新','complete-task-refresh')}</div><div class="overview-list">${needs?`<article class="overview-item"><div class="overview-item-copy"><strong>${esc(taskTitle())}</strong><p>事项 · ${esc(state.agent?.name||'待安排')}</p><span class="overview-status">${esc(status())}</span></div>${button(unifiedTask()?'继续议事':'查看事项','complete-go',`data-page="${unifiedTask()?'chat':'detail'}"`)}</article>`:'<div class="all-empty" role="status"><span aria-hidden="true">✓</span><h3>暂时没有需要处理的事项</h3><p>需要补充信息或核对结果时，会集中出现在这里。</p></div>'}</div><p class="all-boundary-note">本页读取原型的同一事项状态，不模拟服务器推送。</p></section>`;scoped(root,'data-v-d13db084');
}
function historyTitle(ctx){return ctx.topicTitle||ctx.messages.find(m=>m.role==='USER'&&m.text?.trim())?.text.trim().slice(0,48)||ctx.chatDraft?.trim().slice(0,48)||'未题话头';}
function historyTime(value){if(!value||Number.isNaN(new Date(value).getTime()))return '时间未记';return new Intl.DateTimeFormat('zh-CN',{month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'}).format(new Date(value));}
function hasCurrentTopic(ctx){return !!(ctx.topicId||ctx.messages.length||ctx.chatDraft?.trim()||ctx.chatFiles?.length);}
function historySnapshot(ctx){
 ctx.topicId||='demo-topic-'+(++serial);
 return {id:ctx.topicId,title:historyTitle(ctx),updateTime:ctx.topicUpdatedAt||null,messages:structuredClone(ctx.messages),outputs:structuredClone(ctx.outputs),delivery:[...(ctx.delivery||[])],chatDraft:ctx.chatDraft,chatFiles:[...ctx.chatFiles],quote:ctx.quote};
}
function historyRows(ctx){
 const rows=[...(ctx.histories||[])];if(hasCurrentTopic(ctx)){const current=historySnapshot(ctx);return [current,...rows.filter(h=>h.id!==current.id)].sort((a,b)=>(Date.parse(b.updateTime)||0)-(Date.parse(a.updateTime)||0));}return rows;
}
function renderConversationHistory(){
 const panel=$('.chat-panel'),ctx=conversation();if(!panel)return;$('.baseline-history')?.remove();
 const toggle=$('[data-action=complete-history]',panel);toggle?.setAttribute('aria-expanded',String(!!ctx.historyOpen));toggle?.setAttribute('aria-controls','prototype-topic-history');
 if(!ctx.historyOpen)return;
 const rows=historyRows(ctx),limit=ctx.historyPageLimit||100,locked=ctx.pending||!!ctx.historyDeletingId||!!$('.inline-voice-status',panel);
 const trash='<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M4 7h16M9 7V4h6v3M6 7l1 13h10l1-13M10 10v7m4-7v7"/></svg>';
 let content=ctx.historyLoading?'<div class="history-state" role="status">正在翻检话头…</div>':ctx.topicHistoryError?`<div class="history-state is-error" role="alert">${esc(ctx.topicHistoryError)}</div>`:!rows.length?'<div class="history-state">此处暂无旧话头。</div>':`<ul class="history-list">${rows.slice(0,limit).map(h=>{const current=h.id===ctx.topicId,deleting=h.id===ctx.historyDeletingId;return `<li class="history-row">${button(`<strong>${esc(h.title||'未题话头')}</strong><small>${esc(historyTime(h.updateTime))}</small>`,current?'complete-select-current':'complete-select-history',`class="history-item${current?' selected':''}" data-history="${esc(h.id)}" ${current?'aria-current="page"':''} ${locked?'disabled':''}`)}${button(deleting?'<span role="status" aria-live="polite">删除中</span>':trash,current?'complete-delete-current':'complete-delete-history',`class="history-delete" data-history="${current?'current':esc(h.id)}" title="删除话头：${esc(h.title)}" aria-label="${deleting?'正在删除':'删除'}话头：${esc(h.title)}" ${locked||ctx.task?.cancelled?'disabled':''}`)}</li>`;}).join('')}</ul>${rows.length>limit?button('再取旧话头','complete-history-more',`class="history-load-more" ${locked?'disabled':''}`):''}`;
 $('.panel-toolbar',panel).insertAdjacentHTML('afterend',`<section id="prototype-topic-history" class="hall-conversation-history baseline-history" aria-label="话头记录">${content}</section>`);
}

function openEntries(){dialog('全部入口',`<div class="mmd-more-menu">${prototypePages.map(([label,next])=>button(label,'complete-go',`data-page="${next}"`)).join('')}</div>`);}
document.addEventListener('click',event=>{
 const t=event.target.closest('button,[data-action]');if(!t||t.disabled)return;const action=t.dataset.action;
 if(!action?.startsWith('complete-'))return;event.preventDefault();event.stopImmediatePropagation();
 const ctx=conversation();
 if(handleAllPageAction(action,t))return;
 if(action==='complete-page-back'){if(page==='detail'&&state.recommendation)state.recommendation=null;go(t.dataset.page);return;}
 if(action==='complete-agent-confirm'){if(!state.recommendation)return;state.recommendation=null;startUnifiedConversation(true);return;}
 if(handleDraftAction(action,t))return;
 if(handleSyncedAction(action,t))return;
 if(action==='complete-production-status'){state.taskFilter=state.taskFilter===t.dataset.status?'':t.dataset.status;render();return;}
 if(action==='complete-task-refresh'){render();feedback('已重读同一份离线事项，没有创建或修改。');return;}
 if(action==='complete-materials'){$('.composer-more-panel')?.remove();$('.composer-more')?.setAttribute('aria-expanded','false');openMaterials('chat');}
 if(action==='complete-go'){if(['detail','chat','results'].includes(t.dataset.page)&&!state.task){feedback('请先提出需求；或从页面与状态索引打开脱敏示例。');return;}if(t.dataset.page==='private'&&!state.privateAgentId){state.selectedAgent=state.selectedAgent||{id:'0',name:'宋江'};openPrivate();return;}go(t.dataset.page);}
 if(action==='complete-entries')openEntries();
 if(action==='complete-index')location.href='pages.html';
 if(action==='complete-overview-tab'){state.overviewTab=Number(t.dataset.tab);render();}
 if(action==='complete-task-group'){state.taskGroup=t.dataset.group;state.taskFilter='';render();}
 if(action==='complete-task-clear'){state.taskGroup='全部';state.taskFilter='';state.taskSearch='';state.taskAbility='';render();}
 if(action==='complete-workspace-filter'){state.workspaceFilter=t.dataset.filter;render();}
 if(action==='complete-create-status'){state.simulation.create='ok';t.closest('dialog').close();feedback('示例核对：未受理。原草稿保留，可显式提交。');}
 if(action==='complete-reply-status'){if(unifiedTask()){state.task.phase='待你补充';}state.simulation.reply='ok';ctx.error=null;ctx.pending=false;state.baselineScenario='ready';renderChat();feedback('示例核对：未受理；核对草稿后显式发送，不自动重发。');}
 if(action==='complete-operation-detail'){t.closest('dialog')?.close();go('detail');}
 if(action==='complete-operation-status')resolveOperation();
 if(action==='complete-refresh'){state.baselineScenario='ready';ctx.pending=false;ctx.error=null;render();feedback('已读取原演示话头状态；没有发送或重跑成果。');}
 if(action==='complete-history'){if($('.inline-voice-status')||ctx.historyDeletingId)return;ctx.historyOpen=!ctx.historyOpen;renderConversationHistory();persist();return;}
 if(action==='complete-history-more'){ctx.historyPageLimit=(ctx.historyPageLimit||100)+100;renderConversationHistory();persist();return;}
 if(action==='complete-select-current'){return;}
 if(action==='complete-new'){if(ctx.pending||(ctx.task?.complete||ctx.task?.cancelled))return;dialog('另起话头','<p>当前消息、草稿和资料会留在话头记录中。另起话头不创建事项，也不重复点将。</p>',button('取消','close-dialog')+button('另起话头','complete-new-confirm'));}
 if(action==='complete-new-confirm'){if(ctx.pending)return;ctx.histories=ctx.histories||[];if(hasCurrentTopic(ctx)){const snapshot=historySnapshot(ctx);ctx.histories=ctx.histories.filter(h=>h.id!==snapshot.id);ctx.histories.push(snapshot);}ctx.topicId='demo-topic-'+(++serial);ctx.topicTitle='';ctx.topicUpdatedAt=new Date().toISOString();ctx.messages=[];ctx.chatDraft='';ctx.chatFiles=[];ctx.quote=null;ctx.pending=false;ctx.historyOpen=false;t.closest('dialog').close();render();}
 if(action==='complete-select-history'){if(ctx.pending||ctx.historyDeletingId||$('.inline-voice-status'))return;const h=ctx.histories?.find(h=>h.id===t.dataset.history);if(!h)return;const active=hasCurrentTopic(ctx)?historySnapshot(ctx):null;ctx.histories=ctx.histories.filter(x=>x.id!==h.id&&x.id!==active?.id);if(active)ctx.histories.push(active);Object.assign(ctx,{topicId:h.id,topicTitle:h.title,topicUpdatedAt:h.updateTime||null,messages:structuredClone(h.messages),outputs:structuredClone(h.outputs),delivery:[...h.delivery],chatDraft:h.chatDraft,chatFiles:[...h.chatFiles],quote:h.quote,historyOpen:true});render();}
 if(action==='complete-delete-current'||action==='complete-delete-history'){if(ctx.task?.cancelled||ctx.pending||ctx.historyDeletingId)return;const h=action==='complete-delete-current'?{title:historyTitle(ctx)}:ctx.histories?.find(h=>h.id===t.dataset.history);if(!h)return;dialog('删除话头',`<p>确认删除“${esc(h.title||'未题话头')}”吗？删除后无法恢复。</p><small>仅删除本原型的话头，不删除事项、冻结成果或真实记录。</small>`,button('取消','close-dialog')+button('删除','complete-delete-confirm',`data-history="${action==='complete-delete-current'?'current':esc(t.dataset.history)}"`));}
 if(action==='complete-delete-confirm'){if(ctx.task?.cancelled||ctx.pending||ctx.historyDeletingId)return;if(t.dataset.history==='current'){ctx.messages=[];ctx.chatDraft='';ctx.chatFiles=[];ctx.quote=null;ctx.topicId=null;ctx.topicTitle='';ctx.topicUpdatedAt=null;}else ctx.histories=(ctx.histories||[]).filter(h=>h.id!==t.dataset.history);t.closest('dialog').close();render();}
 if(action==='complete-voice'){showVoiceStatus('recording');mapVoiceActions();}
 if(action==='complete-voice-stop'){showVoiceStatus('review');mapVoiceActions();}
 if(action==='complete-voice-cancel'){$('.baseline-voice-status')?.remove();state.baselineScenario='ready';renderChat();$('.composer-textarea')?.focus({preventScroll:true});if(ctx.historyOpen)renderConversationHistory();}
 if(action==='complete-voice-append'||action==='complete-voice-replace'){const text=$('.baseline-voice-status textarea').value.trim();if(!text){feedback('转写为空，草稿未改变。');return;}ctx.chatDraft=action==='complete-voice-replace'?text:[ctx.chatDraft,text].filter(Boolean).join('\n');state.baselineScenario='ready';$('.baseline-voice-status')?.remove();renderChat();$('.composer-textarea')?.focus({preventScroll:true});if(ctx.historyOpen)renderConversationHistory();}
 if(action==='complete-file'){state.fileId=t.dataset.id;state.fileManage=false;go('file');}
 if(action==='complete-rename'){dialog('重命名',`<label>名称<input aria-label="文件名称" value="${esc(asset(state.fileId||'ref-brief')?.name)}"></label>`,button('取消','close-dialog')+button('保存','complete-rename-save'));}
 if(action==='complete-rename-save'){const a=asset(state.fileId||'ref-brief'),name=$('dialog[open] input').value.trim();if(!name){feedback('名称不能为空。');return;}a.name=name;(state.fileMeta[a.id]||= {}).name=name;t.closest('dialog').close();render();}
 if(action==='complete-recycle'){const a=asset(state.fileId||'ref-brief'),m=state.fileMeta[a.id]||{};state.fileMeta[a.id]=m;if(m.recycled){m.recycled=false;render();}else dialog('移到回收站',`<p>确认将“${esc(a.name)}”移入回收站？仍可恢复。</p><p>任务引用 101 条；议事引用 2 条；现存输入授权 3 条。（离线示例计数）</p><p>已有固定版本引用和输入授权保留，本操作不会撤销授权。</p>`,button('取消','close-dialog')+button('演示确认信息过期','complete-workspace-stale-demo')+button('确认回收','complete-recycle-confirm'));}
 if(action==='complete-recycle-confirm'){const id=state.fileId||'ref-brief';(state.fileMeta[id]||= {}).recycled=true;t.closest('dialog').close();render();}
 if(action==='complete-use-file'){const id=state.fileId||'ref-brief';state.draftFiles=[...new Set([...state.draftFiles,id])];go('create');}
 if(action==='complete-library-tab'){state.libraryTab=t.dataset.tab;render();}
 if(action==='complete-library-search'){state.libraryQuery=$('[aria-label="案卷检索关键词"]').value.trim();state.librarySearched=true;renderLibrary();}
 if(action==='complete-case-draft'){state.draft='请根据自然观察活动案卷整理活动方案。';state.draftFiles=[...new Set([...state.draftFiles,'ref-brief'])];go('create');}
 if(action==='complete-toc'){dialog('目录',`<ol>${[1,2].map(i=>'<li>'+button('第'+i+'回','complete-chapter',`data-chapter="${i}"`)+'</li>').join('')}</ol>`);}
 if(action==='complete-chapter'){state.reader.chapter=Math.max(1,Math.min(2,Number(t.dataset.chapter)));$('dialog[open]')?.close();render();}
 if(action==='complete-bookmarks'){dialog('书签',`${state.reader.bookmarks.length?state.reader.bookmarks.map(n=>button('第'+n+'回','complete-chapter',`data-chapter="${n}"`)).join(''):'<p>暂无书签。</p>'}`,button('添加当前章节书签','complete-bookmark-save'));}
 if(action==='complete-bookmark-save'){state.reader.bookmarks=[...new Set([...state.reader.bookmarks,state.reader.chapter])];t.closest('dialog').close();feedback('演示书签已保存。');}
 if(action==='complete-notes'){dialog('手札',`<textarea aria-label="手札内容" rows="5">${esc(state.reader.notes)}</textarea>`,button('取消','close-dialog')+button('保存手札','complete-notes-save'));}
 if(action==='complete-notes-save'){state.reader.notes=$('[aria-label="手札内容"]').value;t.closest('dialog').close();feedback('演示手札已保存。');}
 persist();
},true);
// Voice is a temporary editing mode inside the same input boundary, not a panel below it.
showVoiceStatus=function(kind){
 $('.baseline-voice-status')?.remove();$('.composer-more-panel')?.remove();
 const root=$('.composer-input-area');if(!root)return;
 const recording=kind==='recording',hasDraft=!!conversation().chatDraft.trim();
 const heading=recording?'<div class="inline-voice-heading" role="status"><span class="voice-record-dot" aria-hidden="true"></span><strong>正在录音</strong><span class="voice-demo-time">00:03 · 示例</span></div><div class="inline-voice-wave" aria-hidden="true">'+[12,24,18,32,22,14,26,18,30,16,22].map(h=>`<i style="height:${h}px"></i>`).join('')+'</div>':'<div class="inline-voice-heading" role="status"><strong>检查转写内容</strong></div><textarea aria-label="语音转写草稿" rows="3">请把画面调整得明亮一些。</textarea>';
 const actions=recording?button('取消','complete-voice-cancel')+button('停止并转写','complete-voice-stop','class="inline-voice-primary"'):button('丢弃','complete-voice-cancel')+(hasDraft?button('替换草稿','complete-voice-replace'):'')+button(hasDraft?'追加到草稿':'放入输入框','complete-voice-append','class="inline-voice-primary"');
 root.insertAdjacentHTML('beforeend',`<section class="baseline-voice-status inline-voice-status" data-voice-mode="${kind}" aria-label="${recording?'录音':'转写预览'}">${heading}<small>${recording?'界面演示，不启用麦克风':'示例转写，可编辑；放入后仍需手动发送'}</small><div class="inline-voice-actions">${actions}</div></section>`);
 $$('.toolbar-actions button', $('.chat-panel')).forEach(b=>b.disabled=true);$$('.history-item,.history-delete,.history-load-more').forEach(b=>b.disabled=true);
 const focus=recording?$('[data-action=complete-voice-stop]',root):$('.baseline-voice-status textarea',root);focus?.focus({preventScroll:true});
};
function mapVoiceActions(){for(const [a,b] of [['ui-voice-stop','complete-voice-stop'],['ui-voice-cancel','complete-voice-cancel'],['ui-voice-append','complete-voice-append'],['ui-voice-replace','complete-voice-replace']])$$(`[data-action="${a}"]`).forEach(e=>e.dataset.action=b);}
document.addEventListener('input',e=>{if(e.target.dataset.completeTaskSearch){state.taskSearch=e.target.value;applyTaskFilters();persist();}});
document.addEventListener('change',e=>{if(e.target.matches('[data-task-status]')){state.taskFilter=e.target.value;applyTaskFilters();persist();}});

// Scoped 2026-10-13 source sync. All receipts below are explicitly local fixtures.
function canCancelDemo(){return !!state.task?.notStarted&&!state.task.cancelled&&!state.task.complete&&!state.pending&&!state.operation;}
function renderCancellation(){
 const card=$('.matter-advice-card');if(!card)return;
 $('.ordinary-cancellation',card)?.remove();
 if(state.task?.cancelled){card.insertAdjacentHTML('beforeend','<p role="status">事项已取消；历史指派与成果保留，不再继续办理。</p>');return;}
 if(!canCancelDemo()&&state.cancellation?.status!=='unknown')return;
 card.insertAdjacentHTML('beforeend',`<section class="ordinary-cancellation" aria-label="普通事项取消"><p>仅取消无资金事实、未实际开始的普通事项；已点将未开工也可申请，最终以服务端核验为准。历史指派与成果保留。</p>${button(state.cancellation?.status==='unknown'?'核对原取消结果':'取消未开工事项','complete-cancel','class="ordinary-cancel-action"')}${state.cancellation?.status==='unknown'?'<p role="status">结果尚未确认；只核对原事项，不重复提交取消。</p>':''}</section>`);
}
function renderFormalResults(){
 const root=supplementalRoot()||$('.formal-results-page');if(!root)return;
 root.classList.add('formal-results-page');
 // This page belongs to the matter flow, not to the borrowed 'mine' shell.
 $$('[data-workbench-tab]').forEach(tab=>{if(tab.dataset.workbenchTab==='tasks')tab.setAttribute('aria-current','page');else tab.removeAttribute('aria-current');});
 $$('.panel-workspace-link').forEach(entry=>entry.remove());
 if(unifiedTask()){renderUnifiedResults(root);return;}
 root.innerHTML=`<header><h2>正式成果</h2><p>同一事项的固定版本成果 · 离线示例，不是实际查询</p></header>${button('返回事项详情','complete-go','data-page="detail"')}`;
 if(!state.task){root.insertAdjacentHTML('beforeend','<p>请先提出需求。</p>');return;}
 // No workspace control in formal-results context; global navigation remains unchanged.
 if(state.task.cancelled){
  root.insertAdjacentHTML('beforeend',`<section class="formal-terminal-history"><p role="status">已取消；仅查看历史成果，不再继续办理或验收。</p><p role="${state.historyError?'alert':'status'}">${state.historyError?'历史成果读取失败（离线固定场景）；请核对原记录。':'历史记录已保留（离线示例）。'}</p><div class="terminal-history-actions" role="group" aria-label="重新读取历史成果">${button('重新读取历史成果','complete-history-reload','data-kind="artifacts"')}${button('重新读取议事文字成果','complete-history-reload','data-kind="text"')}</div>${state.historyError?'':state.outputs.map(a=>`<article><strong>${esc(a.name)}</strong>${media(a,true)}${button('下载历史成果','download',`data-id="${a.id}"`)}</article>`).join('')}</section>`);return;
 }
 const done=state.task.complete;
 if(state.operation&&!done){root.insertAdjacentHTML('beforeend',`<p role="status">验收状态：${esc(state.operation.stage)}；不重复提交。</p>${button('查询原操作状态','complete-operation-open')}`);return;}
 if(selectedScenario==='independent-roots'){root.insertAdjacentHTML('beforeend','<p>图片与文字属于两个独立请求，暂不能视为同次交付。</p><p>来源关联恢复仍待实现（R01）；不自动合并、不重新生成。</p>');return;}
 finalDraft=done?[...state.final]:[...state.delivery];
 root.insertAdjacentHTML('beforeend',`<p>${done?'事项已完成，最终成果如下。':'请查看本次成果，满意后确认验收；需要修改就返回议事。'}</p><div class="mmd-attachments" data-delivery-list>${deliveryList()}</div><div class="mmd-row">${done?'':button('继续修改','continue-chat')+button('确认验收','finish',`class="mmd-primary" ${finalDraft.length&&!state.pending?'':'disabled'}`)}</div>`);
}
function renderRuntimeCatalog(){
 const root=$('.baseline-page');if(!root)return;
 const r=state.runtimeDemo||= {open:selectedScenario.startsWith('runtime-'),mode:selectedScenario==='runtime-existing'?'existing':'new',imported:false,attempted:false,status:'',queries:0};
 root.classList.add('persona-catalog-panel');root.innerHTML=`<div class="catalog-summary"><span>2 位待请豪杰（示例）</span><span>接应方式由你确认</span></div><div class="catalog-grid">${[['林冲','豹子头','执行协作'],['公孙胜','入云龙','资料整理']].map(([name,nick,ability],i)=>`<article class="persona-card"><img class="all-persona-avatar" src="shared/juyiting-portraits/thumbs/${i===0?'linchong':'gongsunsheng'}.webp" alt="${name}画像"><div class="persona-main"><div class="persona-head"><strong>${name}</strong><em>梁山好汉</em></div><small>${nick}</small><div class="ability-tags"><span>${ability}</span><span>离线示例</span></div></div><div class="catalog-actions">${i===0?button('自家接应','complete-runtime-open')+button('山寨安顿','complete-runtime-hosted'):button('查看本领','complete-go','data-page="agents"')}</div></article>`).join('')}</div><p class="all-boundary-note">原型不绑定好汉、不生成密钥、不登记真实安装或付款。</p>`;scoped(root,'data-v-31fc08de');
 if(!r.open)return;
 root.insertAdjacentHTML('beforeend',`<section class="runtime-setup"><div class="runtime-guide-head"><strong>自家接应文书已备（示例）</strong>${button('关闭接应文书','complete-runtime-close')}</div><p>Runtime v1 自家接应；安装授权不代表 Runtime 在线或事项可办理。</p><dl class="runtime-scope"><div><dt>Tenant</dt><dd>demo-tenant</dd></div><div><dt>Client</dt><dd>demo-client</dd></div><div><dt>Agent</dt><dd>demo-linchong</dd></div><div><dt>Manifest 版本</dt><dd>v1（非真实清单）</dd></div></dl><h3>Runtime 指引</h3><p>统一目录：程序放 apps/cyf-agent-runtime-v1，配置与策略放 conf/cyf-agent-runtime-v1，各角色 HOME 放 state/cyf-agent-runtime-v1/INSTANCE/agents/SUBJECT/codex-home；基目录使用目标机本人获授权的位置。</p><p>已有统一 Runtime：沿用 installation、manifest、hostId、授权和完整会话；不重新生成交接材料、不重复登记或 enroll。本页不会自动更新目标机。</p><div class="runtime-actions">${button('首次接入（演示）','complete-runtime-mode','data-mode="new"')}${button('已有 Runtime（演示）','complete-runtime-mode','data-mode="existing"')}</div>${r.mode==='existing'?'<p role="status">已有安装：仅查询原安装状态，不重复登记。路径迁移、validate、服务切换与新事项验收须在实际环境完成。</p>':'<ol><li>确认目标机运行用户、文件 UID 与权限。</li><li>准备交接材料，安全传回 handoff.json。</li></ol><pre class="runtime-command">安装 → prepare → 网页登记 → profile/host 配置 → validate → enroll → 服务切换 → 新事项验收</pre><p>不要粘贴或传送 enrollment-secret、subject-key、JWT 或 API Key。</p><label>导入 handoff.json（原型禁用真实文件）<input type="file" accept="application/json,.json" disabled></label>'+button('载入脱敏 handoff 示例','complete-runtime-import')}${r.error?`<p class="runtime-error" role="alert">${esc(r.error)}</p>`:''}${r.imported?'<p role="status">示例作用域匹配；不代表真实材料已校验。</p>':''}<div class="runtime-actions">${button('明确登记安装','complete-runtime-register',`class="catalog-action primary" ${r.mode==='existing'||!r.imported||r.attempted?'disabled':''}`)}${button('手动查询同一安装','complete-runtime-query',`class="catalog-action subtle" ${r.mode==='new'&&!r.imported?'disabled':''}`)}</div>${r.status?`<p role="status">安装授权状态：${esc(r.status)}（离线固定回执）。PENDING / ACTIVE 不代表在线；仍须配置、validate、enroll、服务切换与新事项验收。</p>`:''}</section>`);
}
function handleSyncedAction(action,t){
 if(action==='complete-operation-open'){operationDialog();return true;}
 if(action==='complete-cancel'){
  if(state.cancellation?.status==='unknown'){state.cancellation.queries=(state.cancellation.queries||0)+1;persist();feedback('示例核对：结果仍未确认；不重复提交取消。');return true;}
  if(!canCancelDemo())return true;
  dialog('确认取消未开工事项？',`<p>即将申请取消“${esc(taskTitle())}”。仅限无资金事实且未实际开始的事项，最终由服务端核验；历史指派与成果保留。确认后不会继续办理；若结果未确认，只核对原结果，不重复提交。</p>`,button('保留事项','close-dialog')+button('确认取消事项','complete-cancel-confirm','class="ordinary-cancel-action"'));return true;
 }
 if(action==='complete-cancel-confirm'){
  if(!canCancelDemo()||state.cancellation?.writes)return true;
  state.cancellation={writes:1,queries:0,status:selectedScenario==='cancel-unknown'?'unknown':'cancelled'};
  if(state.cancellation.status==='cancelled'){state.task.cancelled=true;state.pending=false;}
  t.closest('dialog')?.close();render();return true;
 }
 if(action==='complete-history-reload'){state.historyReads||={artifacts:0,text:0};state.historyReads[t.dataset.kind]++;persist();feedback(state.historyError?'示例读取仍失败；保留原记录，不自动重跑。':'已重新读取同一份离线历史；没有发送或验收。');return true;}
 if(!action?.startsWith('complete-runtime-'))return false;
 const r=state.runtimeDemo;
 if(action==='complete-runtime-open')r.open=true;
 if(action==='complete-runtime-close'){r.open=false;renderRuntimeCatalog();persist();return true;}
 if(action==='complete-runtime-hosted'){dialog('山寨安顿','<p>保留已有付费安顿边界；本原型不报价、不付款、不绑定好汉。</p>');return true;}
 if(action==='complete-runtime-mode'){Object.assign(r,{mode:t.dataset.mode,error:''});}
 if(action==='complete-runtime-import'){
  r.error=selectedScenario==='runtime-invalid'?'示例作用域不匹配或材料已过期；不登记安装。':'';r.imported=!r.error;
 }
 if(action==='complete-runtime-register'&&r.mode==='new'&&r.imported&&!r.attempted){r.attempted=true;r.status=selectedScenario==='runtime-unknown'?'UNKNOWN':'PENDING';}
 if(action==='complete-runtime-query'){r.queries++;r.status=selectedScenario==='runtime-unknown'?'UNKNOWN':r.mode==='existing'?'ACTIVE':'PENDING';}
 renderRuntimeCatalog();persist();return true;
}

// One continuous conversation. Local demo only, never API/Provider authority.
const demoAgents=[['wuyong','吴用'],['0','宋江'],['1','公孙胜']];
function demoDraftFields(){return {title:state.title,instruction:state.draft,inputs:[...state.draftFiles],agentId:state.draftAgent||'wuyong'};}
function demoDraftSaved(){return !!state.savedPrivateDraft&&JSON.stringify(state.savedPrivateDraft.fields)===JSON.stringify(demoDraftFields());}
function saveDemoDraft(){state.savedPrivateDraft={fields:demoDraftFields(),revision:(state.savedPrivateDraft?.revision||0)+1};persist();renderDraftPage();}
function demoAgentSelect(){return `<select aria-label="承办好汉" data-draft-agent>${demoAgents.map(([id,name])=>`<option value="${id}" ${(state.draftAgent||'wuyong')===id?'selected':''}>${name}</option>`).join('')}</select>`;}
function unifiedTask(){return !!state.task?.unified;}
function ensureUnifiedTask(){
 saveMatterContext();
 if(state.task){state.previousMatters=state.previousMatters||[];state.previousMatters.push(structuredClone({task:state.task,agent:state.agent,messages:state.messages,outputs:state.outputs,delivery:state.delivery,final:state.final,operation:state.operation}));}
 const agentId=state.draftAgent||'wuyong';
 state.task={id:'demo-matter-'+(++serial),unified:true,title:state.title.trim()||state.draft.trim().slice(0,36)||'资料处理',description:state.draft,files:[...state.draftFiles],phase:'正在处理',complete:false,executions:[],turns:0};
 state.agent={id:agentId,name:demoAgents.find(([id])=>id===agentId)?.[1]||'吴用'};
 Object.assign(state,{messages:[],outputs:[],delivery:[],final:[],pending:false,error:null,operation:null,cancellation:{writes:0,status:'ready'},chatDraft:'',chatFiles:[],quote:null,histories:[],historyOpen:false,topicId:null,topicTitle:'',topicUpdatedAt:null,historyPageLimit:100,baselineScenario:'ready'});
}
function recommendDraftAgent(){
 // Offline capability fixtures, not a live routing service.
 if(/画|图片|插画|设计/.test(state.draft))return {id:'1',reason:'这项需求涉及创意与图像表达，推荐公孙胜。'};
 if(/协调|分工|统筹/.test(state.draft))return {id:'0',reason:'这项需求涉及统筹协调，推荐宋江。'};
 return {id:'wuyong',reason:'这项需求适合先梳理目标、整理内容，推荐吴用。'};
}
function openAgentRecommendation(){
 const recommended=recommendDraftAgent();state.draftAgent=recommended.id;
 state.recommendation={...recommended,from:page};go('detail');
}
function renderAgentRecommendation(){
 const card=$('.matter-advice-card');if(!card)return;
 const recommendation=state.recommendation,name=demoAgents.find(([id])=>id===recommendation.id)[1];
 card.setAttribute('data-agent-recommendation','');
 card.innerHTML=`<div class="matter-advice-heading"><span>办理建议</span></div><p class="matter-request">${esc(state.draft||'请根据所附资料处理。')}</p><dl><div><dt>预期成果</dt><dd>在议事中查看结果，并可继续补充或修改</dd></div><div><dt>建议承办</dt><dd>${name} <small>· 系统推荐</small></dd></div><div><dt>资料</dt><dd>${state.draftFiles.length?state.draftFiles.map(id=>esc(asset(id)?.name)).join('、'):'可选；也可以在议事中补充'}</dd></div></dl><p class="matter-fee-note">${esc(recommendation.reason)} 确认后进入议事，澄清、结果和修改都在原话头中继续。</p><details class="recommendation-alternative"><summary>另选承办 Agent</summary><label>承办好汉 ${demoAgentSelect()}</label></details><div class="matter-primary-actions">${button('确认承办，进入议事','complete-agent-confirm','class="matter-primary-action"')}</div><p class="draft-hint">离线推荐与处理示例，不调用模型、不扣费。</p>`;
 scoped(card,'data-v-9209fea5');
 $$('.task-material-links,.matter-results-action,.baseline-cancellation').forEach(e=>e.remove());
}
function syncProductionNavigation(){
 const primary=['home','tasks','workspace','mine'];
 const fallback={create:'tasks',detail:'home',chat:'detail',private:'agents',public:'map',agents:'home',file:'workspace',reader:'library',results:'detail',library:'mine',messages:'home',catalog:'agents',map:'home',help:'mine',account:'mine'};
 const target=page==='chat'?'detail':state.recommendation&&page==='detail'?state.recommendation.from:(state.returnPages?.[page]||fallback[page]||'home');
 const crumb=$('.workbench-breadcrumb strong');if(crumb)crumb.textContent=labels[page];
 if(primary.includes(page))return;
 const modal=['agents','catalog','library','reader','messages','help','account','private','public','chat','create'].includes(page);
 let header=page==='detail'?$('.bounty-modal-header'):$('.panel-title');
 const host=$('.hall-draft-editor,.baseline-page,.agent-panel,.formal-results-page');
 let panel=host?.closest('.floating-panel')||$('.floating-panel');
 if(!header){header=document.createElement('header');header.className='production-page-header';if(panel)panel.prepend(header);else if(host)host.prepend(header);else return;}
 if(modal&&panel){
  const overlay=panel.parentElement;overlay.className='panel-overlay theme-workbench all-pages-modal'+(['chat','private','public'].includes(page)?' is-chat-overlay':'');overlay.setAttribute('role','dialog');overlay.setAttribute('aria-modal','true');overlay.setAttribute('aria-label',labels[page]);
  panel.className='floating-panel layout-center-modal all-pages-panel panel-'+page;
  if(page==='create'){panel.classList.add('authenticated-draft-panel');overlay.classList.add('authenticated-draft-overlay');}
  panel.prepend(header);
  if(host)host.classList.add('all-page-content');
  // Background controls remain visible but cannot receive keyboard or pointer input.
  const frame=overlay.parentElement;for(const child of frame.children){if(child!==overlay&&!child.contains(overlay)){child.setAttribute('inert','');child.setAttribute('aria-hidden','true');}}
 }
 const back=page==='detail'?'bounty-back-button':'panel-return';header.classList.add('production-page-header');
 header.innerHTML=button('← 返回','complete-page-back',`class="${back}" data-page="${target}" aria-label="返回${esc(labels[target])}"`)+`<span id="juyiting-floating-panel-title">${esc(page==='chat'?'议事':labels[page])}</span>`+(modal?button('×','complete-page-back',`class="panel-close" data-page="${target}" aria-label="关闭${esc(labels[page])}"`):'');
 if(page==='map'){header.classList.add('all-map-back');$('.all-scene')?.prepend(header);}
}
function startUnifiedConversation(confirmed=false){
 if(!state.draft.trim()&&!state.draftFiles.length){feedback('请先填写需求或选择资料。');return;}
 if(state.draft.length>20000||state.title.length>200){feedback('内容超出长度，请修改后再发送；原文仍保留。');return;}
 if(state.simulation.create!=='ok'){createProblem();return;}
 if(confirmed!==true){openAgentRecommendation();return;}
 const text=state.draft.trim(),inputs=[...state.draftFiles];ensureUnifiedTask();
 state.draft='';state.title='';state.draftFiles=[];state.savedPrivateDraft=null;
 go('chat');sendUnifiedMessage(text,inputs,null);
}
function sendUnifiedMessage(text,inputs=[],quote=null){
 if(!unifiedTask()||state.pending||(!text.trim()&&!inputs.length))return;
 if(state.simulation.reply==='failed'){
  state.chatDraft=text;state.chatFiles=[...inputs];state.quote=quote;state.error='尚不能确认本条消息是否受理（模拟）。内容已保留，请先核对，不要重复发送。';state.task.phase='需核对';renderChat();persist();return;
 }
 const task=state.task,turn=++task.turns;
 const message={role:'USER',text:text||'请看看这份资料。',files:[...inputs],quote,turn};
 state.messages.push(message);task.files=[...new Set([...task.files,...inputs])];
 state.chatDraft='';state.chatFiles=[];state.quote=null;state.pending=true;state.pendingReason='unified-reply';task.phase='正在处理';persist();renderChat();
 setTimeout(()=>{
  if(state.task!==task||!state.pending||task.turns!==turn)return;
  const brief=text.trim(),missingPurpose=!brief||brief.length<5||/^(帮我|做一下|处理一下|优化一下|改一下|看看)[。！!\s]*$/.test(brief);
  const missingResume=/简历/.test(brief)&&!task.files.length;
  if(missingPurpose||missingResume){
   state.messages.push({role:'AGENT',text:missingResume?'请先添加需要优化的简历，也可以直接粘贴内容。收到后，我会继续在这里给你修改结果。':'你希望最后得到什么结果？可以补充用途或重点，也可以添加资料。我会沿着这段对话继续处理。',clarification:true,turn});
   task.phase='待你补充';
  }else{
   const round=task.executions.length+1;
   const snapshot={instruction:brief,inputs:task.files.map(id=>({fileId:id,version:1})),quote,agentId:state.agent.id};
   const body=round===1?`活动简报\n\n目标：梳理活动安排，明确下一步行动。\n结论：围绕活动主题组织内容，保留关键要求。\n待办：确认参与人员、完善时间安排、准备资料。`:`活动简报 · 修改稿\n\n已按本轮要求调整内容表达，保留关键结论与待办。\n本轮修改要求：${brief}\n\n上一版仍保留，可在原对话中预览、下载或继续引用修改。`;
   const id=output('text',body+'\n\n（离线示例，不是真实模型生成。）',round,state),a=asset(id);
   a.name=`${task.title}-第${round}版.txt`;a.note=`第 ${round} 版 · 离线示例`;a.round=round;
   task.executions.push({id:'demo-execution-'+(++serial),round,turn,fields:structuredClone(snapshot),outputs:[id],writes:1,phase:'已有结果'});
   state.delivery=[id];state.messages.push({role:'AGENT',text:round===1?'先给你这一版。结果在下面，可以直接查看；哪里不合适，继续告诉我就好。':'按你的补充改好了，这是第 '+round+' 版。上一版仍在这段对话里。',outputs:[id],turn});task.phase='已有结果';
  }
  state.pending=false;state.pendingReason=null;state.error=null;persist();
  if(page==='chat')renderChat();else if(['home','tasks','detail','results'].includes(page))render();
 },650);
}
function sendUnifiedDraft(){if(state.pending||state.error)return;sendUnifiedMessage(state.chatDraft.trim(),state.chatFiles,state.quote);}
function renderDraftPage(){
 const old=$('.hall-draft-editor')||$('.bounty-panel');if(!old)return;
 const root=document.createElement('section');root.className='hall-draft-editor hall-draft-editor--draft';root.setAttribute('aria-label','提出需求');old.replaceWith(root);
 const panel=root.closest('.floating-panel'),overlay=panel?.parentElement;if(panel){panel.className='floating-panel panel-draft layout-center-modal authenticated-draft-panel';const heading=$('.panel-title',panel);if(heading)heading.remove();}if(overlay){overlay.className='panel-overlay theme-workbench authenticated-draft-overlay';overlay.setAttribute('role','dialog');overlay.setAttribute('aria-modal','true');overlay.setAttribute('aria-label','提出需求');}
 const chips=state.draftFiles.length?state.draftFiles.map(id=>`<span>${esc(asset(id)?.name)} · v1（示例）</span>`).join(''):'<span class="muted">资料可稍后在议事中补充</span>';
 root.innerHTML=`<p class="draft-intro">说说你想办成的事，结果和后续修改都在同一段议事里。</p><form class="task-create-form"><label><span>需求描述</span><textarea name="taskDescription" placeholder="例如：把活动说明整理成一页简报，列出结论和待办。">${esc(state.draft)}</textarea></label><section class="draft-strip draft-materials"><div><h4>参考资料 <small>可选</small></h4><div class="draft-chips">${chips}</div></div>${button('添加资料','materials','data-context="draft"')}</section><details class="unified-optional"><summary>事项名称（可选）</summary><label><input name="taskTitle" aria-label="事项名称" placeholder="不填写时，按需求自动命名" value="${esc(state.title)}"></label></details><p class="draft-hint">点击开始办事后，系统会推荐承办 Agent，由你确认或另选；信息不足会在议事中询问。</p><div class="draft-actions"><span data-draft-save-status class="muted">${demoDraftSaved()?'草稿已保存。':'离线原型，不调用模型、不扣费。'}</span>${button('保存草稿','complete-draft-save')}${button('开始办事','complete-draft-next','class="primary"')}</div></form>`;
 $('.task-create-form',root).addEventListener('submit',e=>{e.preventDefault();startUnifiedConversation();});
}
function handleDraftAction(action,t){
 if(!action?.startsWith('complete-draft-'))return false;
 if(action==='complete-draft-save')saveDemoDraft();
 if(action==='complete-draft-next')startUnifiedConversation();
 if(action==='complete-draft-new'){Object.assign(state,{title:'',draft:'',draftFiles:[],savedPrivateDraft:null});go('create');}
 persist();return true;
}
function renderUnifiedDetail(){
 const card=$('.matter-advice-card');if(!card)return;card.classList.add('unified-matter');
 card.innerHTML=`<div class="matter-advice-heading"><span>事项</span><strong>${esc(state.task.phase)}</strong></div><h3>${esc(state.task.title)}</h3><p class="matter-request">${esc(state.task.description)}</p><p>${esc(state.agent.name)} · ${state.task.executions.length?'已有 '+state.task.executions.length+' 版结果':'仍在同一段议事中处理'}</p><p class="draft-hint">补充要求、查看结果、提出修改，都在原议事中继续。</p><div class="mmd-row">${button('继续议事','complete-go','data-page="chat" class="matter-primary-action mmd-primary"')}</div>`;
 const materials=$('.task-material-links');if(materials)materials.innerHTML=`<div class="mmd"><h4>事项资料</h4>${files(state.task.files,'task',false)}</div>`;
}
function renderUnifiedResults(root){
 root.classList.add('unified-results');root.innerHTML=`<header><h2>结果在原议事中</h2><p>每一版结果与修改要求都保留在同一段对话里。</p></header>${button('回到议事查看结果','complete-go','data-page="chat" class="mmd-primary"')}`;
}
document.addEventListener('change',e=>{if(e.target.matches('[data-draft-agent]')){state.draftAgent=e.target.value;persist();}});
document.addEventListener('input',e=>{if(page==='create'&&e.target.matches('[name=taskTitle],[name=taskDescription]')){const status=$('[data-draft-save-status]');if(status)status.textContent='草稿已修改，尚未发送。';}});

function syncTaskToolbar(){
 const panel=$('.bounty-panel'),bar=panel&&$('.panel-toolbar',panel);if(!bar)return;
 panel.dataset.uiSync='20261013';
 $$('.task-create-actions,.task-draft-actions,.task-create-form',panel).forEach(e=>e.remove());
 $$('.workbench-create-action').forEach(e=>{e.dataset.prototypePage='create';});
 const search=$('.task-search',bar);if(search){search.style.display='grid';search.style.gridTemplateColumns='minmax(0, 1fr) minmax(90px, 0.45fr)';search.style.gap='8px';}
 const input=$('input',search||bar),select=$('select',search||bar);
 if(input){input.style.gridColumn='auto';input.type='search';input.setAttribute('aria-label','搜索事项');input.placeholder='查榜号';input.dataset.completeTaskSearch='true';}
 if(select){select.style.gridColumn='auto';select.setAttribute('aria-label','筛选所需本领');if(select.options[0])select.options[0].textContent='不拘本领';}
 const refresh=$(':scope > button',bar);if(refresh){refresh.classList.add('task-refresh');refresh.setAttribute('aria-label','刷新事项');refresh.title='刷新事项';refresh.dataset.action='complete-task-refresh';refresh.innerHTML=uiIcon('refresh');}
 bar.style.display='grid';bar.style.gridTemplateColumns='minmax(0, 1fr) 44px';bar.style.alignItems='center';bar.style.gap='8px';
}

// 2026-10-16: page-specific production structures, in the existing prototype only.
function refreshAllPageSurfaces(){
 document.body.dataset.uiRevision='all-pages-20261016';document.body.dataset.currentPage=page;
 const navFamily={home:'overview',tasks:'tasks',create:'tasks',detail:'tasks',chat:'tasks',results:'tasks',workspace:'treasure',file:'treasure',mine:'mine',agents:'mine',catalog:'mine',library:'mine',reader:'mine',messages:'mine',help:'mine',account:'mine',private:'mine',public:'overview',map:'overview'};
 $$('[data-workbench-tab]').forEach(e=>{e.toggleAttribute('aria-current',e.dataset.workbenchTab===navFamily[page]);if(e.hasAttribute('aria-current'))e.setAttribute('aria-current','page');});
 $$('.workbench-account-action,.workbench-sidebar-account').forEach(e=>{e.disabled=page!=='home';if(page==='home')e.dataset.prototypePage='account';else delete e.dataset.prototypePage;e.title=page==='home'?'个人中心：原型仅说明入口，设置页待核验':'请返回首页后进入个人中心';});
 const root=$('.baseline-page');
 if(page==='mine'){
  const mine=$('.hall-mine-page');if(mine){mine.querySelectorAll('.baseline-extra').forEach(e=>e.remove());const grid=$('.mine-grid',mine);if(grid){const entries=[['agents','好汉名册','查看好汉本领与在线状态','account-circle-outline'],['library','典籍阁','阅读典籍、案卷与个人进度','notebook'],['messages','消息','查看需要你处理的事项','bell-outline'],['map','厅中实景','进入梁山场景与地图','map-marker-outline'],['account','个人中心','返回首页后进入个人中心','account-circle-outline']];grid.innerHTML=entries.map(([to,title,desc,icon])=>`<button type="button" data-action="complete-go" data-page="${to}" ${to==='account'?'disabled aria-disabled="true"':''}><i class="var-icon var-icon--set var-icon-${icon}" aria-hidden="true"></i><span><strong>${title}</strong><small>${desc}</small></span></button>`).join('');}scoped(mine,'data-v-2ccfdada');mine.insertAdjacentHTML('beforeend',`<footer class="all-mine-links">${button('使用帮助','complete-go','data-page="help"')}${button('全部页面索引','complete-index')}</footer>`);}
 }
 if(page==='help'&&root){
  const steps=[['从办事页开始','描述你想办成的事，按需添加资料。首页不用预先选择好汉。'],['由系统推荐承办','点击开始办事，在事项详情查看推荐承办 Agent，再确认或另选。'],['在同一议事里继续','需要澄清时直接补充，结果在原话头展示，不满意可继续修改。'],['随时找回进展和资料','事项保存当前进度，资料保留固定版本。返回不会清空草稿。']];const n=Math.min(state.helpStep||0,steps.length-1);
  root.classList.add('all-help');root.innerHTML=`<section class="onboarding-dialog all-help-dialog"><div class="dialog-heading"><div><p class="eyebrow">聚义厅 · 办事引导</p><h1 id="hall-onboarding-title">${steps[n][0]}</h1></div></div><p class="intro">${steps[n][1]}</p><div class="all-guide-track" aria-label="引导进度">${steps.map((_,i)=>`<span class="${i<=n?'active':''}"></span>`).join('')}</div><p class="step-progress">第 ${n+1} 步，共 ${steps.length} 步</p><p class="all-boundary-note">步骤按本次连续议事提案更新；所有操作均为离线示例。</p><div class="dialog-actions">${button('稍后','complete-page-back',`data-page="${state.returnPages?.help||'home'}"`)}${n?button('上一步','complete-help-step',`data-step="${n-1}"`):''}${n<steps.length-1?button('下一步','complete-help-step',`data-step="${n+1}" class="complete-button"`):button('开始体验','complete-go','data-page="home" class="complete-button"')}</div></section>`;
 }
 if(page==='account'&&root){root.classList.add('all-account');root.innerHTML=`<section class="all-account-card"><span class="all-persona-avatar" aria-hidden="true">我</span><h2>个人中心</h2><p>这是聚义厅外的账户模块入口。</p><p role="status">生产源码支持从首页进入个人中心；面板打开或语音交互锁定时暂不可进入。真实设置页面尚待核验。</p><div class="all-account-options">${['账户信息','授权管理','隐私设置'].map(x=>`<button disabled>${x}<small>原型暂未展示</small></button>`).join('')}</div><p class="all-boundary-note">此处仅说明入口边界，不代表生产账户功能不可用；不模拟未经核验的设置，也不读取或修改凭据。</p>${button('返回我的','complete-go','data-page="mine"')}</section>`;}
 if(page==='map'&&root){root.classList.add('all-map');document.body.append(root);root.innerHTML=`<section class="all-scene" aria-label="厅中实景静态原型"><img src="assets/hall-base-v3.webp" alt="现有梁山厅堂游戏底图；静态原型，非实时地图"><nav class="all-scene-tools" aria-label="实景工具"><strong>聚义厅</strong>${button('办事','complete-go','data-page="home"')}${button('消息','complete-go','data-page="messages"')}${button('资料','complete-go','data-page="workspace"')}${button('帮助','complete-go','data-page="help"')}</nav><div class="all-scene-spots">${button('点将册','complete-go','data-page="agents" class="scene-roster"')}${button('忠义堂公议','complete-go','data-page="public" class="scene-public"')}${button('悬赏榜','complete-go','data-page="tasks" class="scene-board"')}${button('典籍阁','complete-go','data-page="library" class="scene-library"')}</div><p class="all-scene-note">静态实景与入口演示 · 不运行游戏、坐标或联网好汉</p></section>`;}
 if(page==='workspace'){
  const input=$('.treasure-search input');if(input){input.value=state.workspaceQuery||'';input.setAttribute('aria-label','搜索文件名称');}
  const upload=$('.treasure-primary');if(upload)upload.dataset.action='complete-upload-panel';
  const form=$('.treasure-search');if(form)form.addEventListener('submit',e=>{e.preventDefault();e.stopImmediatePropagation();state.workspaceQuery=$('input',form).value;render();});
 }
 const note=$('.baseline-provenance');if(note)note.textContent='全页面对齐候选 · 2026-10-16 · 离线示例';
}
function handleAllPageAction(action,t){
 if(action==='complete-workspace-stale-demo'){dialog('确认信息已过期','<p>文件或关联情况已变化，请查看更新后的信息再确认。</p><p>旧确认已失效；本次没有回收文件。</p>',button('返回文件管理','close-dialog'));return true;}
 if(action==='complete-workspace-unknown-demo'){dialog('待确认的资料操作','<p>文件管理操作：提交结果尚未确认，请重试原操作核对结果，勿重复新建。</p><p>恢复标识仅保留在当前页面，刷新或关闭页面后无法在此继续重试。</p><p>离线交互示例，不发送请求、不持久化操作标识。</p>',button('关闭','close-dialog')+button('重试原操作','complete-workspace-original-retry'));return true;}
 if(action==='complete-workspace-original-retry'){t.closest('dialog').close();feedback('原操作已提交，已读取当前文件状态。（离线示例；未创建新操作）');return true;}

 if(action.startsWith('complete-workspace-')&&['complete-workspace-history-demo','complete-workspace-history-more','complete-workspace-partial-demo','complete-workspace-detail-demo','complete-workspace-detail-retry'].includes(action)){const id=state.fileId||'ref-brief',meta=state.fileMeta[id]||(state.fileMeta[id]={});if(action==='complete-workspace-history-demo'){meta.demoHistory=true;meta.demoHistoryLoaded=false;meta.demoVersion='102';}if(action==='complete-workspace-history-more')meta.demoHistoryLoaded=true;if(action==='complete-workspace-partial-demo')meta.demoPartial=!meta.demoPartial;if(action==='complete-workspace-detail-demo')meta.demoDetailError=true;if(action==='complete-workspace-detail-retry'){meta.demoDetailError=false;feedback('已重新读取详情（离线示例），未再次上传。');}render();return true;}

 if(action==='complete-open-matter'){openListedMatter(t.dataset.matterKey);return true;}
 if(action==='complete-agent-filter'){state.agentFilter=t.dataset.filter;renderAgents();persist();return true;}
 if(action==='complete-file-manage'){state.fileManage=!state.fileManage;render();return true;}
 if(action==='complete-help-step'){state.helpStep=Number(t.dataset.step);render();return true;}
 if(action==='complete-reader-notes'){state.reader.notesOpen=!state.reader.notesOpen;render();return true;}
 if(action==='complete-reader-save'){state.reader.notes=$('[aria-label="手札草稿"]').value;persist();feedback('手札已保存在本原型，不上传。');$('.reader-note-status').textContent='手札已保存（本地示例）';return true;}
 if(action==='complete-reader-cite'){state.draft=[state.draft,'请根据典籍第'+state.reader.chapter+'回的阅读示例，整理要点与待办。'].filter(Boolean).join('\n');go('create');return true;}
 if(action==='complete-upload-panel'){dialog('上传资料',`<p>上传本身不交办，也不会把资料发给好汉。本原型仅保存在当前标签页。</p><label>选择资料<input type="file" data-workspace-upload aria-label="选择本地资料"></label><label>显示名称（可选）<input data-upload-name aria-label="显示名称" placeholder="留空使用文件名称"></label><p data-upload-status role="status">尚未选择文件</p>`,button('取消','close-dialog')+button('保存到原型资料','complete-upload-confirm','disabled class="mmd-primary"'));return true;}
 if(action==='complete-upload-confirm'){const input=$('[data-workspace-upload]'),f=input?.files?.[0];if(!f)return true;const name=$('[data-upload-name]').value.trim()||f.name;t.disabled=true;const reader=new FileReader();reader.onload=()=>{const type=f.type.startsWith('image/')?'image':f.type.startsWith('audio/')?'audio':/text|json/.test(f.type)?'text':'document';state.localFiles.push({id:'local-'+(++serial),name,type,url:reader.result,note:'本机资料 · 未上传',text:type==='text'?'本地文件可下载查看。':''});$('dialog[open]')?.close();persist();render();feedback('已存入原型资料，没有上传或交办。');};reader.onerror=()=>{t.disabled=false;$('[data-upload-status]').textContent='读取失败，请重新选择文件。';};reader.readAsDataURL(f);return true;}
 return false;
}
document.addEventListener('change',e=>{if(e.target.matches('[data-library-source]')){state.librarySource=e.target.value;persist();}if(e.target.matches('[data-workspace-upload]')){const f=e.target.files?.[0];$('[data-action=complete-upload-confirm]').disabled=!f;$('[data-upload-status]').textContent=f?f.name:'尚未选择文件';}});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('dialog[open]')&&!['chat','private'].includes(page)){const back=$('.production-page-header [data-action=complete-page-back]');if(back){e.preventDefault();back.click();}}});

document.addEventListener('change',e=>{if(e.target.matches('[data-complete-task-ability]')){state.taskAbility=e.target.value;applyTaskFilters();persist();}});
document.addEventListener('keydown',e=>{if(['Enter',' '].includes(e.key)&&e.target.matches('.task-card[data-matter-key]')){e.preventDefault();openListedMatter(e.target.dataset.matterKey);}});

document.addEventListener('change',e=>{if(e.target.matches('[data-workspace-version]')){const id=state.fileId||'ref-brief',meta=state.fileMeta[id]||(state.fileMeta[id]={});meta.demoVersion=e.target.value;render();}});

// Update only the counter while typing; never rerender or move the input focus.
document.addEventListener('input',event=>{if(event.target.matches('.composer-textarea')){const count=document.querySelector('[data-draft-count]');if(count)count.textContent=event.target.value.length+'/1200';}});
