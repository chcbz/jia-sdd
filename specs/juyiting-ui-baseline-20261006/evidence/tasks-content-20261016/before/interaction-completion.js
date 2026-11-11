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
 const summary=$('.context-summary small',panel);if(summary)summary.title=summary.textContent;
 $$('.toolbar-actions button',panel).forEach(b=>{if((ctx.task?.complete||ctx.task?.cancelled)&&b.dataset.action!=='ui-history')b.disabled=true;if(ctx.pending)b.disabled=true;});
 if(['waiting','streaming'].includes(state.baselineScenario)&&!ctx.pending){$$('.is-pending',panel).forEach(e=>e.remove());}
 const menu=$('.composer-more',panel);menu?.setAttribute('aria-expanded','false');
 // Preserve actions and state, while the compact CSS positions toolbar right and voice before send.
 const mapping={'ui-refresh':'complete-refresh','ui-history':'complete-history','ui-new':'complete-new','ui-voice':'complete-voice','ui-voice-stop':'complete-voice-stop','ui-voice-cancel':'complete-voice-cancel','ui-voice-append':'complete-voice-append','ui-voice-replace':'complete-voice-replace'};
 for(const [old,next] of Object.entries(mapping))$$(`[data-action="${old}"]`,panel).forEach(e=>e.dataset.action=next);
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
function applyTaskFilters(){
 const card=$('.task-card');if(!card)return;
 const match=!!state.task&&(!state.taskFilter||productionTaskStatus()===state.taskFilter)&&(!state.taskSearch||[state.task?.title,state.task?.description].join(' ').toLowerCase().includes(state.taskSearch.trim().toLowerCase()));
 card.hidden=!match;card.style.display=match?'':'none';
 const empty=$('.baseline-empty');if(empty){empty.hidden=match;empty.innerHTML=state.task?'没有符合筛选条件的事项，试试其他分组或清空筛选。':'暂无事项，点击右上方“提出需求”开始。';}
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
 const cards=$$('.task-card');cards.slice(1).forEach(e=>e.remove());const card=cards[0];if(card)card.dataset.prototypePage=unifiedTask()?'chat':'detail';
 const tabs=$('.task-status-tabs');
 const statuses=['待点将','筹划中','待开工（已点将）','办理中','待验收','受阻','已完成','失败','已取消','已归档'];
 if(tabs){tabs.setAttribute('aria-label','事项状态');tabs.innerHTML=statuses.map(name=>button(`${name} <span>${state.task&&productionTaskStatus()===name?1:0}</span>`,'complete-production-status',`data-status="${name}" aria-pressed="${state.taskFilter===name}" class="${state.taskFilter===name?'active':''}"`)).join('');tabs.insertAdjacentHTML('afterend','<p class="mmd baseline-empty" role="status"></p>');}
 const search=$('.task-search input');if(search){search.value=state.taskSearch||'';search.dataset.completeTaskSearch='true';}
 applyTaskFilters();
}
function createProblem(){const unknown=state.simulation.create==='unknown';dialog(unknown?'提交状态待核对':'提交失败（示例）',`<p>${unknown?'尚不能确认受理，先核对状态，不重复创建。':'明确未受理。需求和附件均保留，可返回修改。'}</p>`,button(unknown?'核对创建状态':'返回修改','complete-create-status'));}
function beginAcceptance(){if(state.operation||!finalDraft.length||!state.task||state.task.cancelled||state.task.complete||state.pending)return;state.operation={id:'demo-operation-'+(++serial),outputs:[...finalDraft],stage:'pending',writes:1};if(page==='detail')renderDetail();persist();$('dialog[open]')?.close();operationDialog();setTimeout(resolveOperation,650);}
function operationDialog(){const op=state.operation;if(!op)return;finalDraft=[...op.outputs];dialog('验收进度',`<p role="status">${op.stage==='pending'?'正在核对原验收操作…':op.stage==='failed'?'验收未完成。原操作和成果已保留。':'验收状态未知。不重新提交验收。'}</p><small>原操作 ${esc(op.id)} · 冻结 ${op.outputs.length} 项成果</small><div class="mmd-attachments">${deliveryList()}</div>`,button('返回详情','complete-operation-detail')+button('查询原操作状态','complete-operation-status'));}
function resolveOperation(){const op=state.operation;if(!op||state.task?.complete)return;if(state.simulation.accept==='ok'){op.stage='completed';state.final=[...op.outputs];state.task.complete=true;persist();const d=$('dialog[open]');if(d?.getAttribute('aria-label')==='验收进度'){d.close();go('detail');feedback('示例验收完成。');}else render();return;}op.stage=state.simulation.accept==='failed'?'failed':'unknown';if(page==='detail')renderDetail();if(page==='results')renderFormalResults();persist();const d=$('dialog[open]');if(d?.getAttribute('aria-label')==='验收进度'){d.close();operationDialog();}}
async function addLocalFiles(selected){const ids=[];try{for(const f of selected){const id='local-'+(++serial),type=f.type.startsWith('image/')?'image':f.type.startsWith('audio/')?'audio':/text|json/.test(f.type)||/\.(txt|md|csv)$/i.test(f.name)?'text':'document';const a={id,name:f.name,type,note:'本机附件 · 不上传'};a.text=type==='text'?await f.text():type==='document'?'此格式仅演示选取与下载，未支持内容解析；不是已实现格式能力。':'';a.url=await new Promise((r,j)=>{const reader=new FileReader();reader.onload=()=>r(reader.result);reader.onerror=j;reader.readAsDataURL(f);});state.localFiles.push(a);ids.push(id);}const selectedIds=[...new Set([...picker.ids,...ids])],context=picker.context;$('dialog[open]')?.close();persist();openMaterials(context,selectedIds);}catch{feedback('本机示例文件未读取成功，已确认资料不变。');}}
function renderFileDetail(){
 const root=$('.baseline-page'),a=asset(state.fileId||'ref-brief');if(!root||!a)return;const meta=state.fileMeta[a.id]||{};
 root.classList.add('all-file-detail','personal-workspace','is-hall-treasure');
 root.innerHTML=`<div class="treasure-content"><div class="treasure-file-heading"><div><h2>${esc(a.name)}</h2><p>${state.saved.includes(a.id)?'成果':'资料'} · ${meta.recycled?'已回收':'仅自己可见'} · 离线示例</p></div>${button(state.fileManage?'返回预览':'更多管理','complete-file-manage')}</div><div class="file-preview-body" ${state.fileManage?'hidden':''}><div class="treasure-preview-tools treasure-version-tools"><label>版本 <select aria-label="文件版本"><option>v1 · ${esc(a.name)}</option></select></label>${button('下载','download',`data-id="${a.id}"`)}</div><p class="treasure-note">本次使用固定的 v1；已有事项中的资料引用不会随新版本替换。</p><section class="treasure-preview" aria-label="文件预览">${media(a)}</section><div class="treasure-actions">${!meta.recycled?button('用于新委托','complete-use-file','class="treasure-primary"'):''}${button('预览','preview',`data-id="${a.id}"`)}</div></div><section class="treasure-management ${state.fileManage?'is-open':''}" ${state.fileManage?'':'hidden'} aria-label="文件管理"><h3>文件管理</h3><p>旧版本及已有事项引用保留。本原型只修改示例文件，不上传到服务器。</p><div class="treasure-form"><label>上传新版本<input type="file" disabled aria-label="上传新版本（此原型未模拟）"></label><small>当前只演示固定 v1；新版本写入不在本原型中模拟。</small><button disabled>上传为新版本</button></div>${button('重命名','complete-rename')}${button(meta.recycled?'恢复':'移到回收站','complete-recycle')}</section></div>`;
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
function renderConversationHistory(){const panel=$('.chat-panel'),ctx=conversation();if(!panel)return;$('.baseline-history')?.remove();const histories=ctx.histories||[];$('.panel-toolbar',panel).insertAdjacentHTML('afterend',`<section class="baseline-history mmd" aria-label="话头记录"><h3>当前话头</h3><p>${ctx.messages.length} 条示例消息</p>${ctx.task?.cancelled?'':button('删除当前话头','complete-delete-current')}<h3>已保存话头</h3>${histories.length?histories.map(h=>`<div class="baseline-history-row">${button(h.title,'complete-select-history',`data-history="${h.id}"`)}${ctx.task?.cancelled?'':button('删除','complete-delete-history',`data-history="${h.id}"`)}</div>`).join(''):'<p>暂无其他话头。</p>'}${button('关闭记录','complete-history')}</section>`);}
function historySnapshot(ctx){return {id:'demo-topic-'+(++serial),title:'演示话头 '+serial,messages:structuredClone(ctx.messages),outputs:structuredClone(ctx.outputs),delivery:[...(ctx.delivery||[])],chatDraft:ctx.chatDraft,chatFiles:[...ctx.chatFiles],quote:ctx.quote};}
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
 if(action==='complete-task-clear'){state.taskGroup='全部';state.taskFilter='';state.taskSearch='';render();}
 if(action==='complete-workspace-filter'){state.workspaceFilter=t.dataset.filter;render();}
 if(action==='complete-create-status'){state.simulation.create='ok';t.closest('dialog').close();feedback('示例核对：未受理。原草稿保留，可显式提交。');}
 if(action==='complete-reply-status'){if(unifiedTask()){state.task.phase='待你补充';}state.simulation.reply='ok';ctx.error=null;ctx.pending=false;state.baselineScenario='ready';renderChat();feedback('示例核对：未受理；核对草稿后显式发送，不自动重发。');}
 if(action==='complete-operation-detail'){t.closest('dialog')?.close();go('detail');}
 if(action==='complete-operation-status')resolveOperation();
 if(action==='complete-refresh'){state.baselineScenario='ready';ctx.pending=false;ctx.error=null;render();feedback('已读取原演示话头状态；没有发送或重跑成果。');}
 if(action==='complete-history'){ctx.historyOpen=!ctx.historyOpen;render();}
 if(action==='complete-new'){if(ctx.pending||(ctx.task?.complete||ctx.task?.cancelled))return;dialog('另起话头','<p>当前消息、草稿和资料会留在话头记录中。另起话头不创建事项，也不重复点将。</p>',button('取消','close-dialog')+button('另起话头','complete-new-confirm'));}
 if(action==='complete-new-confirm'){ctx.histories=ctx.histories||[];ctx.histories.push(historySnapshot(ctx));ctx.messages=[];ctx.chatDraft='';ctx.chatFiles=[];ctx.quote=null;ctx.pending=false;ctx.historyOpen=false;t.closest('dialog').close();render();}
 if(action==='complete-select-history'){const h=ctx.histories?.find(h=>h.id===t.dataset.history);if(!h)return;const active=historySnapshot(ctx);ctx.histories=ctx.histories.filter(x=>x.id!==h.id);ctx.histories.push(active);Object.assign(ctx,{messages:structuredClone(h.messages),outputs:structuredClone(h.outputs),delivery:[...h.delivery],chatDraft:h.chatDraft,chatFiles:[...h.chatFiles],quote:h.quote,historyOpen:false});render();}
 if(action==='complete-delete-current'||action==='complete-delete-history'){if(ctx.task?.cancelled)return;dialog('删除话头','<p>只删除当前原型中的示例消息，不删除事项、冻结成果或真实记录。</p>',button('取消','close-dialog')+button('删除','complete-delete-confirm',`data-history="${t.dataset.history||'current'}"`));}
 if(action==='complete-delete-confirm'){if(t.dataset.history==='current'){ctx.messages=[];ctx.chatDraft='';ctx.chatFiles=[];ctx.quote=null;}else ctx.histories=ctx.histories.filter(h=>h.id!==t.dataset.history);t.closest('dialog').close();render();}
 if(action==='complete-voice'){showVoiceStatus('recording');mapVoiceActions();}
 if(action==='complete-voice-stop'){showVoiceStatus('review');mapVoiceActions();}
 if(action==='complete-voice-cancel'){$('.baseline-voice-status')?.remove();state.baselineScenario='ready';renderChat();}
 if(action==='complete-voice-append'||action==='complete-voice-replace'){const text=$('.baseline-voice-status textarea').value.trim();if(!text){feedback('转写为空，草稿未改变。');return;}ctx.chatDraft=action==='complete-voice-replace'?text:[ctx.chatDraft,text].filter(Boolean).join('\n');state.baselineScenario='ready';$('.baseline-voice-status')?.remove();renderChat();}
 if(action==='complete-file'){state.fileId=t.dataset.id;state.fileManage=false;go('file');}
 if(action==='complete-rename'){dialog('重命名',`<label>名称<input aria-label="文件名称" value="${esc(asset(state.fileId||'ref-brief')?.name)}"></label>`,button('取消','close-dialog')+button('保存','complete-rename-save'));}
 if(action==='complete-rename-save'){const a=asset(state.fileId||'ref-brief'),name=$('dialog[open] input').value.trim();if(!name){feedback('名称不能为空。');return;}a.name=name;(state.fileMeta[a.id]||= {}).name=name;t.closest('dialog').close();render();}
 if(action==='complete-recycle'){const a=asset(state.fileId||'ref-brief'),m=state.fileMeta[a.id]||{};state.fileMeta[a.id]=m;if(m.recycled){m.recycled=false;render();}else dialog('移到回收站','<p>仅回收这一份演示资料，不删除其他文件、成果或话头。</p>',button('取消','close-dialog')+button('确认回收','complete-recycle-confirm'));}
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
 if(state.task){state.previousMatters=state.previousMatters||[];state.previousMatters.push(structuredClone({task:state.task,agent:state.agent,messages:state.messages,outputs:state.outputs,delivery:state.delivery,final:state.final,operation:state.operation}));}
 const agentId=state.draftAgent||'wuyong';
 state.task={id:'demo-matter-'+(++serial),unified:true,title:state.title.trim()||state.draft.trim().slice(0,36)||'资料处理',description:state.draft,files:[...state.draftFiles],phase:'正在处理',complete:false,executions:[],turns:0};
 state.agent={id:agentId,name:demoAgents.find(([id])=>id===agentId)?.[1]||'吴用'};
 Object.assign(state,{messages:[],outputs:[],delivery:[],final:[],pending:false,error:null,operation:null,cancellation:{writes:0,status:'ready'},chatDraft:'',chatFiles:[],quote:null,histories:[],historyOpen:false,baselineScenario:'ready'});
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
 $$('.workbench-account-action,.workbench-sidebar-account').forEach(e=>{e.disabled=true;delete e.dataset.prototypePage;e.title='当前生产测试账号的个人中心入口不可用';});
 const root=$('.baseline-page');
 if(page==='mine'){
  const mine=$('.hall-mine-page');if(mine){mine.querySelectorAll('.baseline-extra').forEach(e=>e.remove());const grid=$('.mine-grid',mine);if(grid){const entries=[['agents','好汉名册','查看好汉本领与在线状态','account-circle-outline'],['library','典籍阁','阅读典籍、案卷与个人进度','notebook'],['messages','消息','查看需要你处理的事项','bell-outline'],['map','厅中实景','进入梁山场景与地图','map-marker-outline'],['account','个人中心','生产测试账号当前不可用','account-circle-outline']];grid.innerHTML=entries.map(([to,title,desc,icon])=>`<button type="button" data-action="complete-go" data-page="${to}" ${to==='account'?'disabled aria-disabled="true"':''}><i class="var-icon var-icon--set var-icon-${icon}" aria-hidden="true"></i><span><strong>${title}</strong><small>${desc}</small></span></button>`).join('');}scoped(mine,'data-v-2ccfdada');mine.insertAdjacentHTML('beforeend',`<footer class="all-mine-links">${button('使用帮助','complete-go','data-page="help"')}${button('全部页面索引','complete-index')}</footer>`);}
 }
 if(page==='help'&&root){
  const steps=[['从办事页开始','描述你想办成的事，按需添加资料。首页不用预先选择好汉。'],['由系统推荐承办','点击开始办事，在事项详情查看推荐承办 Agent，再确认或另选。'],['在同一议事里继续','需要澄清时直接补充，结果在原话头展示，不满意可继续修改。'],['随时找回进展和资料','事项保存当前进度，资料保留固定版本。返回不会清空草稿。']];const n=Math.min(state.helpStep||0,steps.length-1);
  root.classList.add('all-help');root.innerHTML=`<section class="onboarding-dialog all-help-dialog"><div class="dialog-heading"><div><p class="eyebrow">聚义厅 · 办事引导</p><h1 id="hall-onboarding-title">${steps[n][0]}</h1></div></div><p class="intro">${steps[n][1]}</p><div class="all-guide-track" aria-label="引导进度">${steps.map((_,i)=>`<span class="${i<=n?'active':''}"></span>`).join('')}</div><p class="step-progress">第 ${n+1} 步，共 ${steps.length} 步</p><p class="all-boundary-note">步骤按本次连续议事提案更新；所有操作均为离线示例。</p><div class="dialog-actions">${button('稍后','complete-page-back',`data-page="${state.returnPages?.help||'home'}"`)}${n?button('上一步','complete-help-step',`data-step="${n-1}"`):''}${n<steps.length-1?button('下一步','complete-help-step',`data-step="${n+1}" class="complete-button"`):button('开始体验','complete-go','data-page="home" class="complete-button"')}</div></section>`;
 }
 if(page==='account'&&root){root.classList.add('all-account');root.innerHTML=`<section class="all-account-card"><span class="all-persona-avatar" aria-hidden="true">我</span><h2>个人中心</h2><p>这是聚义厅外的账户模块入口。</p><p role="status">当前生产测试账号的入口为禁用状态，不能核验后续设置页面。</p><div class="all-account-options">${['账户信息','授权管理','隐私设置'].map(x=>`<button disabled>${x}<small>当前不可用</small></button>`).join('')}</div><p class="all-boundary-note">只更新入口与不可用状态，不伪造账户页面，也不会读取或修改账号凭据。</p>${button('返回我的','complete-go','data-page="mine"')}</section>`;}
 if(page==='map'&&root){root.classList.add('all-map');document.body.append(root);root.innerHTML=`<section class="all-scene" aria-label="厅中实景静态原型"><img src="assets/hall-base-v3.webp" alt="现有梁山厅堂游戏底图；静态原型，非实时地图"><nav class="all-scene-tools" aria-label="实景工具"><strong>聚义厅</strong>${button('办事','complete-go','data-page="home"')}${button('消息','complete-go','data-page="messages"')}${button('资料','complete-go','data-page="workspace"')}${button('帮助','complete-go','data-page="help"')}</nav><div class="all-scene-spots">${button('点将册','complete-go','data-page="agents" class="scene-roster"')}${button('忠义堂公议','complete-go','data-page="public" class="scene-public"')}${button('悬赏榜','complete-go','data-page="tasks" class="scene-board"')}${button('典籍阁','complete-go','data-page="library" class="scene-library"')}</div><p class="all-scene-note">静态实景与入口演示 · 不运行游戏、坐标或联网好汉</p></section>`;}
 if(page==='workspace'){
  const input=$('.treasure-search input');if(input){input.value=state.workspaceQuery||'';input.setAttribute('aria-label','搜索文件名称');}
  const upload=$('.treasure-primary');if(upload)upload.dataset.action='complete-upload-panel';
  const form=$('.treasure-search');if(form)form.addEventListener('submit',e=>{e.preventDefault();e.stopImmediatePropagation();state.workspaceQuery=$('input',form).value;render();});
 }
 const note=$('.baseline-provenance');if(note)note.textContent='全页面对齐候选 · 2026-10-16 · 离线示例';
}
function handleAllPageAction(action,t){
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
