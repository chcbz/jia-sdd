'use strict';
// Latest UI stays authoritative. This file only completes OFFLINE, local interactions.
const prototypePages=[['办事','home'],['事项','tasks'],['提出需求','create'],['点将册','agents'],['事项详情','detail'],['榜文议事','chat'],['密议','private'],['厅前公议','public'],['资料','workspace'],['资料详情','file'],['我的','mine'],['典籍阁','library'],['阅读器','reader'],['消息','messages'],['招贤令','catalog'],['厅中实景','map'],['使用帮助','help'],['个人中心入口','account']];
function seedBaseline(){
 if(state.initializedScenario){if(page==='private'&&!state.privateChats[state.privateAgentId]){state.privateAgentId='0';state.privateChats['0']={agent:{id:'0',name:'宋江'},messages:[],outputs:[],delivery:[],chatDraft:'',chatFiles:[],quote:null,pending:false};}return;}
 const scenario=selectedScenario;state.baselineScenario=scenario;state.initializedScenario=true;
 const formal=['chat','detail'].includes(page),privatePage=page==='private';
 if(formal){state.task={title:'自然观察活动资料',description:'画一只鸟，并整理一份活动方案。',files:['ref-brief'],complete:false};state.agent={id:'0',name:'宋江'};state.selectedAgent={...state.agent};state.messages=[{role:'USER',text:state.task.description,files:['ref-brief']},{role:'AGENT',text:'你期望什么风格？可以在同一话头继续补充。'}];}
 if(privatePage){state.selectedAgent={id:'0',name:'宋江'};state.privateAgentId='0';state.privateChats['0']={agent:{...state.selectedAgent},messages:[],outputs:[],delivery:[],chatDraft:'',chatFiles:[],quote:null,pending:false};}
 const ctx=conversation();
 if(['chat','private','public'].includes(page)){
  if(scenario==='empty')ctx.messages=[];
  if(['waiting','streaming'].includes(scenario)){ctx.pending=true;ctx.pendingReason='fixture';}
  if(['results','completed'].includes(scenario)&&!ctx.outputs.length){const ids=['image','audio','document','text'].map(type=>output(type,'一只小鸟停在枝头。',1,ctx));ctx.delivery=[...ids];ctx.messages.push({role:'AGENT',text:'本次示例成果如下，可预览、下载、保存或引用修改。',outputs:ids});}
 }
 if(scenario==='completed'&&state.task){if(!state.outputs.length){const ids=['image','audio','document','text'].map(type=>output(type,'一只小鸟停在枝头。',1,state));state.delivery=ids;state.messages.push({role:'AGENT',text:'本次示例成果如下。',outputs:ids});}state.task.complete=true;state.final=[...state.delivery];state.operation={id:'demo-completed-operation',outputs:[...state.final],stage:'completed',writes:1};}
}
const optimizedComposer=syncCurrentComposer;
syncCurrentComposer=function(panel){optimizedComposer(panel);const ctx=conversation(),locked=ctx.pending||!!ctx.task?.complete;const voice=$('.voice-start',panel);if(voice)voice.disabled=locked;$('.composer-more',panel).disabled=locked;
 $$('.toolbar-actions button',panel).forEach(b=>{if(ctx.task?.complete&&b.dataset.action!=='ui-history')b.disabled=true;if(ctx.pending)b.disabled=true;});
 if(['waiting','streaming'].includes(state.baselineScenario)&&!ctx.pending){$$('.is-pending',panel).forEach(e=>e.remove());}
 const menu=$('.composer-more',panel);menu?.setAttribute('aria-expanded','false');
 // Scope exact UI actions to completed interactions, without moving the latest toolbar or voice.
 const mapping={'ui-refresh':'complete-refresh','ui-history':'complete-history','ui-new':'complete-new','ui-voice':'complete-voice','ui-voice-stop':'complete-voice-stop','ui-voice-cancel':'complete-voice-cancel','ui-voice-append':'complete-voice-append','ui-voice-replace':'complete-voice-replace'};
 for(const [old,next] of Object.entries(mapping))$$(`[data-action="${old}"]`,panel).forEach(e=>e.dataset.action=next);
};
const optimizedSupplement=renderSupplement;
renderSupplement=function(){optimizedSupplement();document.title=labels[page]+' · 界面优化基准（离线交互）';const note=$('.baseline-provenance');if(note)note.textContent='优化界面 · 交互补全 2026-10-07 · 离线示例';
 $$('.workbench-account-action,.workbench-sidebar-account').forEach(e=>{e.disabled=false;e.dataset.prototypePage='account';});
 const brand=$('.workbench-brand');if(brand){brand.dataset.prototypePage='home';}
 if(page==='home'){$$('.overview-tabs button').forEach((b,i)=>{b.dataset.action='complete-overview-tab';b.dataset.tab=String(i);b.setAttribute('aria-pressed',String((state.overviewTab||0)===i));});}
 if(page==='workspace'){$$('[data-action="ui-file"]').forEach(e=>e.remove());}
 if(page==='file')renderFileDetail();
 if(page==='library')renderLibrary();
 if(page==='reader')renderReader();
 if(page==='messages')renderMessages();
 if(page==='mine'){const root=$('.hall-mine-page');if(root&&!$('[data-action="complete-entries"]',root))root.insertAdjacentHTML('beforeend',`<div class="mmd baseline-extra">${button('全部入口','complete-entries')}${button('页面与状态索引','complete-index')}</div>`);}
 if(page==='help'){const root=$('.baseline-page');if(root)root.insertAdjacentHTML('beforeend',`<div class="mmd baseline-extra">${button('全部入口','complete-entries')}${button('页面与状态索引','complete-index')}</div>`);}
 // Restore history after the visual shell is rerendered.
 if(['chat','private','public'].includes(page)&&conversation().historyOpen)renderConversationHistory();
};
function renderInteractiveList(){
 if(page==='home'){$$('.overview-item').slice(1).forEach(e=>e.remove());if(!state.task)$$('.overview-item').forEach(e=>e.remove());else $$('.overview-item').forEach(card=>{for(const b of $$('button',card)){b.dataset.prototypePage='detail';}});}
 if(page!=='tasks')return;
 const cards=$$('.task-card');cards.slice(1).forEach(e=>e.remove());const card=cards[0];
 const bucket=state.task?.complete?'已完成':!state.agent?'待点将':state.pending?'办理中':state.operation&&state.operation.stage!=='completed'?'受阻':state.outputs.length?'待验收':'议事中',filter=state.taskFilter||bucket;
 for(const b of $$('.task-status-tabs button')){const name=b.innerText.trim().replace(/\s*\d+$/,'');b.dataset.action='complete-task-filter';b.dataset.filter=name;b.innerText=name+' '+(state.task&&name===bucket?'1':'0');b.classList.toggle('active',name===filter);}
 if(card){card.dataset.prototypePage='detail';if(!state.task||bucket!==filter){card.style.display='none';card.insertAdjacentHTML('afterend','<p class="mmd baseline-empty" role="status">此状态暂无演示事项。</p>');}}
 const search=$('.bounty-search-bar input,.task-filters input');if(search){search.value=state.taskSearch||'';search.dataset.completeTaskSearch='true';}
}
function createProblem(){const unknown=state.simulation.create==='unknown';dialog(unknown?'提交状态待核对':'提交失败（示例）',`<p>${unknown?'尚不能确认受理，先核对状态，不重复创建。':'明确未受理。需求和附件均保留，可返回修改。'}</p>`,button(unknown?'核对创建状态':'返回修改','complete-create-status'));}
function beginAcceptance(){if(state.operation||!finalDraft.length||!state.task||state.pending)return;state.operation={id:'demo-operation-'+(++serial),outputs:[...finalDraft],stage:'pending',writes:1};if(page==='detail')renderDetail();persist();$('dialog[open]')?.close();operationDialog();setTimeout(resolveOperation,650);}
function operationDialog(){const op=state.operation;if(!op)return;finalDraft=[...op.outputs];dialog('验收进度',`<p role="status">${op.stage==='pending'?'正在核对原验收操作…':op.stage==='failed'?'验收未完成。原操作和成果已保留。':'验收状态未知。不重新提交验收。'}</p><small>原操作 ${esc(op.id)} · 冻结 ${op.outputs.length} 项成果</small><div class="mmd-attachments">${deliveryList()}</div>`,button('返回详情','complete-operation-detail')+button('查询原操作状态','complete-operation-status'));}
function resolveOperation(){const op=state.operation;if(!op||state.task?.complete)return;if(state.simulation.accept==='ok'){op.stage='completed';state.final=[...op.outputs];state.task.complete=true;persist();const d=$('dialog[open]');if(d?.getAttribute('aria-label')==='验收进度'){d.close();go('detail');feedback('示例验收完成。');}else render();return;}op.stage=state.simulation.accept==='failed'?'failed':'unknown';if(page==='detail')renderDetail();persist();const d=$('dialog[open]');if(d?.getAttribute('aria-label')==='验收进度'){d.close();operationDialog();}}
async function addLocalFiles(selected){const ids=[];try{for(const f of selected){const id='local-'+(++serial),type=f.type.startsWith('image/')?'image':f.type.startsWith('audio/')?'audio':/text|json/.test(f.type)||/\.(txt|md|csv)$/i.test(f.name)?'text':'document';const a={id,name:f.name,type,note:'本机附件 · 不上传'};a.text=type==='text'?await f.text():type==='document'?'此格式仅演示选取与下载，未支持内容解析；不是已实现格式能力。':'';a.url=await new Promise((r,j)=>{const reader=new FileReader();reader.onload=()=>r(reader.result);reader.onerror=j;reader.readAsDataURL(f);});state.localFiles.push(a);ids.push(id);}const selectedIds=[...new Set([...picker.ids,...ids])],context=picker.context;$('dialog[open]')?.close();persist();openMaterials(context,selectedIds);}catch{feedback('本机示例文件未读取成功，已确认资料不变。');}}
function renderFileDetail(){const root=$('.baseline-page'),a=asset(state.fileId||'ref-brief');if(!root||!a)return;const meta=state.fileMeta[a.id]||{};root.innerHTML=`<header><h2>资料详情</h2><p>本地文件示例 · 不改变真实工作空间</p></header><h3>${esc(a.name)}</h3><p>${esc(a.note||a.type)} · v1（当前示例版本）${meta.recycled?' · 已回收':''}</p><div class="baseline-tabs">${button('预览','preview',`data-id="${a.id}"`)}${button('下载','download',`data-id="${a.id}"`)}${button('返回资料','ui-go','data-page="workspace"')}</div><div class="baseline-card">${button('重命名','complete-rename')}${button(meta.recycled?'恢复':'移到回收站','complete-recycle')}${!meta.recycled?button('作为需求资料','complete-use-file'):''}</div><p class="mmd-muted">无虚构的第二历史版本；未实现的永久删除不提供成功按钮。</p>`;}
function renderLibrary(){const root=$('.baseline-page');if(!root)return;const tab=state.libraryTab||'reader';root.classList.add('library-panel');root.innerHTML=`<header><h2>典籍阁</h2><p>阅读、检索与引用均为离线示例</p></header><div class="library-tabs">${button('典籍阅读','complete-library-tab',`data-tab="reader" class="${tab==='reader'?'active':''}"`)}${button('案卷检索','complete-library-tab',`data-tab="search" class="${tab==='search'?'active':''}"`)}</div>`;
 if(tab==='reader')root.insertAdjacentHTML('beforeend',card('水浒传','示例排版、目录、书签与手札','reader'));
 else root.insertAdjacentHTML('beforeend',`<form class="baseline-search"><input aria-label="案卷检索关键词" placeholder="输入示例关键词，如自然观察" value="${esc(state.libraryQuery||'')}">${button('查卷','complete-library-search')}</form><div data-search-results>${state.librarySearched?(state.libraryQuery?.includes('自然')||state.libraryQuery?.includes('活动')?`<div class="baseline-card"><h3>自然观察活动案卷</h3><p>脱敏案卷示例，可作为资料带入需求草稿。</p>${button('引用并起草需求','complete-case-draft')}</div>`:'<p role="status">没有匹配的示例案卷，请换个关键词。</p>'):'<p>请输入关键词后查卷。</p>'}</div>`);}
function renderReader(){const root=$('.baseline-page');if(!root)return;state.reader=state.reader||{chapter:1,bookmarks:[],notes:''};const r=state.reader;root.innerHTML=`<header><h2>典籍阅读</h2><p>示意章页，不冒充真实章节内容或进度</p></header><div class="baseline-tabs">${button('目录','complete-toc')}${button('书签','complete-bookmarks')}${button('手札','complete-notes')}${button('返回书架','ui-go','data-page="library"')}</div><article class="baseline-reader"><h3>水浒传 · 第${r.chapter}回（排版示意）</h3><p>此处为阅读排版样本。当前示例章节、书签和手札仅保留在当前原型标签内。</p><p>新需求可按这一页的阅读结构提出；真实典籍、同步进度和账号隐私仍以产品为准。</p></article><div class="baseline-tabs">${button('上一章','complete-chapter',`data-chapter="${r.chapter-1}" ${r.chapter===1?'disabled':''}`)}${button('下一章','complete-chapter',`data-chapter="${r.chapter+1}" ${r.chapter===2?'disabled':''}`)}</div>`;}
function renderMessages(){const root=$('.baseline-page');if(!root)return;root.innerHTML='<header><h2>消息</h2><p>当前原型的待处理事项，不伪造服务器推送</p></header>';if(state.task&&!state.task.complete)root.insertAdjacentHTML('beforeend',card(state.task.title,status(),'detail'));else root.insertAdjacentHTML('beforeend','<p role="status">暂时没有待处理事项。</p>');if(state.draft||state.draftFiles.length)root.insertAdjacentHTML('beforeend',card('未交办草稿','正文与已确认资料仍保留','create'));}
function renderConversationHistory(){const panel=$('.chat-panel'),ctx=conversation();if(!panel)return;$('.baseline-history')?.remove();const histories=ctx.histories||[];$('.panel-toolbar',panel).insertAdjacentHTML('afterend',`<section class="baseline-history mmd" aria-label="话头记录"><h3>当前话头</h3><p>${ctx.messages.length} 条示例消息</p>${button('删除当前话头','complete-delete-current')}<h3>已保存话头</h3>${histories.length?histories.map(h=>`<div class="baseline-history-row">${button(h.title,'complete-select-history',`data-history="${h.id}"`)}${button('删除','complete-delete-history',`data-history="${h.id}"`)}</div>`).join(''):'<p>暂无其他话头。</p>'}${button('关闭记录','complete-history')}</section>`);}
function historySnapshot(ctx){return {id:'demo-topic-'+(++serial),title:'演示话头 '+serial,messages:structuredClone(ctx.messages),outputs:structuredClone(ctx.outputs),delivery:[...(ctx.delivery||[])],chatDraft:ctx.chatDraft,chatFiles:[...ctx.chatFiles],quote:ctx.quote};}
function openEntries(){dialog('全部入口',`<div class="mmd-more-menu">${prototypePages.map(([label,next])=>button(label,'complete-go',`data-page="${next}"`)).join('')}</div>`);}
document.addEventListener('click',event=>{
 const t=event.target.closest('button,[data-action]');if(!t||t.disabled)return;const action=t.dataset.action;
 if(!action?.startsWith('complete-'))return;event.preventDefault();event.stopImmediatePropagation();
 const ctx=conversation();
 if(action==='complete-go'){if(['detail','chat'].includes(t.dataset.page)&&!state.task){feedback('请先提出需求；或从页面与状态索引打开脱敏示例。');return;}if(t.dataset.page==='private'&&!state.privateAgentId){state.selectedAgent=state.selectedAgent||{id:'0',name:'宋江'};openPrivate();return;}go(t.dataset.page);}
 if(action==='complete-entries')openEntries();
 if(action==='complete-index')location.href='pages.html';
 if(action==='complete-overview-tab'){state.overviewTab=Number(t.dataset.tab);render();}
 if(action==='complete-task-filter'){state.taskFilter=t.dataset.filter;render();}
 if(action==='complete-workspace-filter'){state.workspaceFilter=t.dataset.filter;render();}
 if(action==='complete-create-status'){state.simulation.create='ok';t.closest('dialog').close();feedback('示例核对：未受理。原草稿保留，可显式提交。');}
 if(action==='complete-reply-status'){state.simulation.reply='ok';ctx.error=null;ctx.pending=false;state.baselineScenario='ready';renderChat();feedback('示例核对：未受理；核对草稿后显式发送，不自动重发。');}
 if(action==='complete-operation-detail'){t.closest('dialog')?.close();go('detail');}
 if(action==='complete-operation-status')resolveOperation();
 if(action==='complete-refresh'){state.baselineScenario='ready';ctx.pending=false;ctx.error=null;render();feedback('已读取原演示话头状态；没有发送或重跑成果。');}
 if(action==='complete-history'){ctx.historyOpen=!ctx.historyOpen;render();}
 if(action==='complete-new'){if(ctx.pending||ctx.task?.complete)return;dialog('另起话头','<p>当前消息、草稿和资料会留在话头记录中。另起话头不创建事项，也不重复点将。</p>',button('取消','close-dialog')+button('另起话头','complete-new-confirm'));}
 if(action==='complete-new-confirm'){ctx.histories=ctx.histories||[];ctx.histories.push(historySnapshot(ctx));ctx.messages=[];ctx.chatDraft='';ctx.chatFiles=[];ctx.quote=null;ctx.pending=false;ctx.historyOpen=false;t.closest('dialog').close();render();}
 if(action==='complete-select-history'){const h=ctx.histories?.find(h=>h.id===t.dataset.history);if(!h)return;const active=historySnapshot(ctx);ctx.histories=ctx.histories.filter(x=>x.id!==h.id);ctx.histories.push(active);Object.assign(ctx,{messages:structuredClone(h.messages),outputs:structuredClone(h.outputs),delivery:[...h.delivery],chatDraft:h.chatDraft,chatFiles:[...h.chatFiles],quote:h.quote,historyOpen:false});render();}
 if(action==='complete-delete-current'||action==='complete-delete-history'){dialog('删除话头','<p>只删除当前原型中的示例消息，不删除事项、冻结成果或真实记录。</p>',button('取消','close-dialog')+button('删除','complete-delete-confirm',`data-history="${t.dataset.history||'current'}"`));}
 if(action==='complete-delete-confirm'){if(t.dataset.history==='current'){ctx.messages=[];ctx.chatDraft='';ctx.chatFiles=[];ctx.quote=null;}else ctx.histories=ctx.histories.filter(h=>h.id!==t.dataset.history);t.closest('dialog').close();render();}
 if(action==='complete-voice'){showVoiceStatus('recording');mapVoiceActions();}
 if(action==='complete-voice-stop'){showVoiceStatus('review');mapVoiceActions();}
 if(action==='complete-voice-cancel'){$('.baseline-voice-status')?.remove();state.baselineScenario='ready';renderChat();}
 if(action==='complete-voice-append'||action==='complete-voice-replace'){const text=$('.baseline-voice-status textarea').value.trim();if(!text){feedback('转写为空，草稿未改变。');return;}ctx.chatDraft=action==='complete-voice-replace'?text:[ctx.chatDraft,text].filter(Boolean).join('\n');state.baselineScenario='ready';$('.baseline-voice-status')?.remove();renderChat();}
 if(action==='complete-file'){state.fileId=t.dataset.id;go('file');}
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
document.addEventListener('input',e=>{if(e.target.dataset.completeTaskSearch){state.taskSearch=e.target.value;const c=$('.task-card');if(c&&state.task)c.style.display=!state.taskSearch||state.task.title.includes(state.taskSearch)?'':'none';persist();}});
