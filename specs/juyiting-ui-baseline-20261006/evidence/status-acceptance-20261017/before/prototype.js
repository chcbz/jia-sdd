'use strict';
// Standalone, offline prototype only. No production runtime, API, Provider, or account access.
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels={results:'正式成果',public:'厅前公议',library:'典籍阁',messages:'消息',catalog:'招贤令',map:'厅中实景',help:'使用帮助',file:'资料详情',reader:'典籍阅读',account:'个人中心入口',home:'办事',tasks:'事项',create:'提出需求',agents:'点将册',detail:'事项详情',chat:'悬赏议事',private:'密议',workspace:'资料',mine:'我的'};
const catalog=[
 {id:'ref-bird',name:'小鸟图片.svg',type:'image',url:'assets/bird-v1.svg',note:'图片 · 示意插画'},
 {id:'ref-brief',name:'活动说明.md',type:'document',url:'assets/brief.md',text:'# 活动说明\n主题：自然观察\n对象：亲子家庭\n需要：一张配图、一段介绍、一份活动方案。',note:'文档'},
 {id:'ref-audio',name:'音频示例.wav',type:'audio',url:'assets/sample.wav',note:'音频 · 2 秒示意音'},
 {id:'ref-text',name:'小鸟介绍.txt',type:'text',text:'小鸟停在枝头，观察四周。保持距离，安静欣赏。',note:'文本'}
];
const state={draft:'',title:'',draftFiles:[],chatDraft:'',chatFiles:[],quote:null,task:null,agent:null,messages:[],outputs:[],archive:[],saved:[],final:[],pending:false,selectedAgent:null,privateChats:{},privateAgentId:null,delivery:[]};
let page=labels[location.hash.slice(1)]?location.hash.slice(1):'home',view='',toastTimer,picker=null,lastFocus=null,workspaceFrom=null,serial=0,finalDraft=[];
const selectedScenario=new URLSearchParams(location.search).get('scenario')||'ready';
const storageKey='cyf-ui-baseline-interactions-conversation-20261016:'+selectedScenario;
Object.assign(state,{localFiles:[],operation:null,fileMeta:{},publicChat:{agent:{id:'public-demo',name:'厅前好汉'},messages:[],outputs:[],delivery:[],chatDraft:'',chatFiles:[],quote:null,pending:false},simulation:{create:selectedScenario==='create-failure'?'failed':selectedScenario==='create-unknown'?'unknown':'ok',reply:selectedScenario==='reply-failure'?'failed':'ok',accept:selectedScenario==='accept-unknown'?'unknown':selectedScenario==='accept-failure'?'failed':'ok'}});
if(new URLSearchParams(location.search).get('reset')==='1'){try{sessionStorage.removeItem(storageKey);}catch{}const u=new URL(location.href);u.searchParams.delete('reset');history.replaceState(null,'',u.pathname+u.search+u.hash);}
try{const stored=JSON.parse(sessionStorage.getItem(storageKey)||'null');if(stored?.state){Object.assign(state,stored.state);serial=stored.serial||0;}}catch{/* Browser storage may be unavailable. */}
for(const a of [...catalog,...state.localFiles])if(state.fileMeta[a.id]?.name)a.name=state.fileMeta[a.id].name;
const conversation=()=>page==='private'?(state.privateChats[state.privateAgentId]||state):page==='public'?state.publicChat:state;
function persist(){try{sessionStorage.setItem(storageKey,JSON.stringify({state,serial}));return true;}catch{return false;/* No business storage is used. */}}
function openPrivate(){const a=state.selectedAgent;if(!a)return;state.privateAgentId=a.id;if(!state.privateChats[a.id])state.privateChats[a.id]={agent:{...a},messages:[],outputs:[],chatDraft:'',chatFiles:[],quote:null,pending:false,delivery:[]};go('private');}
const taskTitle=()=>state.task?.title||state.draft||'画一只鸟';
const status=()=>state.task?.cancelled?'已取消':state.task?.complete?'已完成':unifiedTask()?state.task.phase:state.task?.cancelled?'已取消':state.task?.complete?'已完成':state.operation?.stage==='pending'?'验收中':state.operation?.stage==='unknown'?'验收待核对':state.operation?.stage==='failed'?'验收未完成':state.pending?'办理中':state.error?'回复待核对':state.outputs.length?'待验收':state.agent?'议事中':'待点将';
const asset=id=>[...catalog,...state.localFiles,...state.archive,...state.publicChat.outputs,...state.outputs,...Object.values(state.privateChats).flatMap(c=>c.outputs)].find(a=>a.id===id);
function scoped(root,key){root?.setAttribute(key,'');$$('*',root).forEach(e=>e.setAttribute(key,''));return root;}
function insert(parent,html,scope){const wrap=document.createElement('div');wrap.innerHTML=html;if(scope)scoped(wrap,scope);parent.append(...wrap.childNodes);}
function feedback(message){$('#prototype-feedback')?.remove();const n=document.createElement('div');n.id='prototype-feedback';n.role='status';n.textContent=message;document.body.append(n);clearTimeout(toastTimer);toastTimer=setTimeout(()=>n.remove(),2600);}
function syncViewport(){$$('.juyi-page').forEach(e=>e.style.setProperty('--hall-visual-height',innerHeight+'px'));}
function button(label,action,extra=''){
 const addClass=name=>{extra=/class="/.test(extra)?extra.replace('class="','class="'+name+' '):extra+' class="'+name+'"';};
 if((action==='close-dialog'||action==='complete-page-back'||action==='complete-runtime-close')&&(label==='×'||label.startsWith('关闭'))){
  const accessible=label==='×'?'关闭当前窗口':label;
  addClass('ui-close');if(!extra.includes('aria-label='))extra+=' aria-label="'+esc(accessible)+'"';
  extra+=' title="'+esc(accessible)+'"';label=uiIcon('close');
 }else if(action==='download'){addClass('ui-download');label=uiIcon('download')+'<span>'+label+'</span>';}
 return `<button type="button" data-action="${action}" ${extra}>${label}</button>`;
}
function files(ids,context,removable=true){if(context==='chat')return `<div class="composer-file-caption">资料 ${ids.length} 份</div><div class="mmd-attachments composer-file-rail" aria-label="待发送资料">${ids.map(id=>{const a=asset(id);return a?`<div class="composer-file-chip">${button(esc(a.name),'preview',`data-id="${esc(id)}" class="composer-file-name" title="预览 ${esc(a.name)}"`)}${removable?button('×','remove',`data-id="${esc(id)}" data-context="chat" aria-label="移除 ${esc(a.name)}" ${conversation().pending||conversation().task?.complete||conversation().task?.cancelled?'disabled':''}`):''}</div>`:'';}).join('')}</div>`;return `<div class="mmd mmd-attachments">${ids.map(id=>{const a=asset(id);return a?`<div class="mmd-chip"><span>${esc(a.name)}</span>${button('预览','preview',`data-id="${id}"`)}${removable?button('移除','remove',`data-id="${id}" data-context="${context}"`):''}</div>`:''}).join('')}</div>`;}
function media(a,full=false){if(a.type==='image')return `<img src="${a.url}" alt="${esc(a.name)}（原型示意插画）" data-action="preview" data-id="${a.id}">`;if(a.type==='audio')return `<audio controls preload="metadata" src="${a.url}" aria-label="${esc(a.name)}"></audio><small class="mmd-muted">${a.id.startsWith('local-')?'本机音频，未上传':'2 秒示意音，非真实配音'}</small>`;return `<pre>${esc(full?a.text:(a.text||'可预览、下载此文件。').slice(0,220))}</pre>`;}
function result(a){if(conversation()===state&&unifiedTask())return `<section class="mmd-result unified-message-result" data-result="${a.id}"><div class="unified-result-heading"><strong>${esc(a.name)}</strong><small>${esc(a.note)}</small></div><pre class="unified-result-body">${esc(a.text)}</pre><div class="mmd-row">${button('预览','preview',`data-id="${a.id}"`)}${button('下载','download',`data-id="${a.id}"`)}${button('修改这一版','quote',`data-id="${a.id}" ${state.pending?'disabled':''}`)}</div></section>`;return `<section class="mmd-result" data-result="${a.id}"><strong>${esc(a.name)}</strong>${media(a)}<div class="mmd-row">${button('预览','preview',`data-id="${a.id}"`)}${button('下载','download',`data-id="${a.id}"`)}${button(state.saved.includes(a.id)?'已保存':'保存到工作空间','save',`data-id="${a.id}" ${state.saved.includes(a.id)?'disabled':''}`)}${!(conversation().task?.complete||conversation().task?.cancelled)?button('引用修改','quote',`data-id="${a.id}"`):''}</div></section>`;}
function common(){
 $$('.quick-reference-open,.hall-reference-picker,.formal-task-execution').forEach(e=>e.remove());
 $$('.overview-start-copy>p').forEach(e=>e.textContent='说清想办的事，选一位好汉一起完成。也可以添加已有资料。');
 $$('.quick-material-open').forEach(e=>{delete e.dataset.prototypePage;e.textContent='添加资料（可选）';e.dataset.action='materials';e.dataset.context='draft';});
 const input=$('.overview-quick-request textarea');if(input){input.value=state.draft;input.placeholder='例如：画一只鸟，或整理一份活动方案。';const submit=$('.overview-quick-request button.primary');submit.disabled=!state.draft.trim()&&!state.draftFiles.length;$('.quick-request-input small').textContent=state.draft.length+'/200';$('.quick-request-actions').insertAdjacentHTML('afterend',files(state.draftFiles,'draft'));}
 // Preserve existing sample lists. Only the first item is the interactive task.
 $$('.overview-item,.task-card').forEach((e,i)=>{if(e.matches('.overview-item')&&i!==0)return;if(e.matches('.task-card')&&e!==$('.task-card'))return;const title=$('strong,h3,h4',e);if(title)title.textContent=taskTitle();const badge=$('[class*=state],.status-badge,.overview-status',e);if(badge)badge.textContent=status();if(e.matches('.overview-item')){const desc=$('.overview-item-copy>p',e);if(desc)desc.textContent=(unifiedTask()?'事项 · ':'正式事项 · ')+(state.agent?.name||'待安排');}else if($(':scope>p',e))$(':scope>p',e).textContent=state.task?.description||taskTitle();});
 $$('.task-create-actions').forEach(group=>{const first=$('button',group);if(!first)return;$$('button',group).slice(1).forEach(e=>e.remove());first.textContent='提出需求';first.dataset.prototypePage='create';});
 $$('.task-data-state').forEach(e=>e.remove());
 $$('.task-status-tabs button').forEach(e=>{if(e.textContent.includes('待开工'))e.firstChild.textContent='议事中 ';});
 if(page==='tasks')syncTaskToolbar();
 $$('form').forEach(f=>f.addEventListener('submit',onSubmit));
}
function render(){
 if(page==='chat'&&awaitingAssignment()){page='detail';history.replaceState(null,'','#detail');}
 view=innerWidth<=900?'mobile':'desktop';const snapshotPage=['private','public'].includes(page)?'chat':(['library','messages','catalog','map','help','file','reader','account','results'].includes(page)?'mine':page);const snap=window.BASELINE_SNAPSHOTS[view+'-'+snapshotPage]||window.BASELINE_SNAPSHOTS[view+'-home'];
 document.body.innerHTML=snap.html.replaceAll('../bird.svg','assets/bird-v1.svg').replaceAll('./juyiting-portraits/','shared/juyiting-portraits/').replaceAll('./static/','shared/static/');
 document.body.className=snap.bodyClass;document.documentElement.className=snap.htmlClass;document.title=labels[page]+' · 当前源码界面基准（离线示例）';syncViewport();common();
 if(page==='home'||page==='tasks')renderInteractiveList();if(page==='create')renderCreate();if(page==='agents')renderAgents();if(page==='detail'||page==='chat')renderDetail();if(['chat','private','public'].includes(page))renderChat();if(page==='workspace')renderWorkspace();renderSupplement();persist();
}
function go(next){if(!labels[next])return;if(next==='chat'&&awaitingAssignment())next='detail';state.returnPages||={};if(next!==page&&!['home','tasks','workspace','mine'].includes(next)&&!(next==='detail'&&['chat','results'].includes(page)))state.returnPages[next]=page;if(next===page){render();return;}page=next;history.pushState(null,'','#'+page);render();}
function renderCreate(){renderDraftPage();}
function renderAgents(){const panel=$('.agent-panel');if(!panel)return;const rows=$$('.agent-row',panel);$$('.status-filter button',panel).forEach((b,i)=>{b.dataset.action='complete-agent-filter';b.dataset.filter=String(i);b.classList.toggle('active',String(state.agentFilter||0)===String(i));b.setAttribute('aria-pressed',String(String(state.agentFilter||0)===String(i)));});rows.forEach((row,i)=>{row.dataset.action='choose-agent';row.dataset.agent=String(i);const labels=['','候命','办事','出征','失联'];row.hidden=!!Number(state.agentFilter)&&!($('em',row)?.textContent||'').includes(labels[Number(state.agentFilter)]);row.style.display=row.hidden?'none':'';row.setAttribute('aria-pressed',state.selectedAgent?.id===String(i));});const detail=$('.detail-card',panel);detail.classList.add('mmd','mmd-agent-detail');const selected=state.selectedAgent,row=selected?$('.agent-row[data-agent="'+selected.id+'"]',panel):null;detail.innerHTML=selected?`<div class="detail-head">${$('.mini-avatar',row)?.outerHTML||'<span class="all-persona-avatar">将</span>'}<div><strong>${esc(selected.name)}</strong><small>好汉本领 · 本地示例</small></div></div><div class="ability-tags"><span>${esc($('small',row)?.textContent||'资料协作')}</span><span>离线演示</span></div><div class="agent-detail-actions">${button('与这位好汉密议','private-chat')}${state.task&&!state.agent&&!state.task.complete&&!state.task.cancelled?button('点将并议事','assign','class="point-and-deliberate"'):''}</div><p>先核对本领和可用状态；本原型不连接实际好汉。</p>`:'<div class="all-empty"><h3>点一位厅中好汉</h3><p>查看动静、本领与所领事项。</p></div>';scoped(detail,'data-v-b5581454');}

function renderDetail(){if(unifiedTask()){renderUnifiedDetail();return;}const card=$('.matter-advice-card');if(card){renderMatterOverview(card,false);}
 const materials=$('.task-material-links');if(materials){materials.innerHTML=`<div class="mmd"><h4>资料与成果</h4>${files(state.task?.files||[],'task',false)}<p class="mmd-muted">${state.outputs.length?`已有 ${state.outputs.length} 份成果，可在议事中查看。`:'尚无成果，可在议事中继续补充需求和资料。'}</p></div>`;}
 renderCancellation();
 const b=$('.matter-results-action'),primary=$('.matter-primary-action');
 const terminal=!!(state.task?.cancelled||state.task?.complete),hasResults=state.outputs.length>0;
 const resultsPrimary=terminal||!!state.operation||(!state.pending&&hasResults);
 if(primary){primary.classList.toggle('simplify-secondary',resultsPrimary);primary.dataset.mainAction=String(!resultsPrimary);if(!resultsPrimary&&state.agent)primary.textContent=matterDetailPresentation().action;}
 if(b){b.hidden=!resultsPrimary;b.dataset.mainAction=String(resultsPrimary);b.textContent=state.task?.cancelled?'查看历史成果':state.task?.complete?'查看验收结果':state.operation?'核对验收进度':'查看成果并验收';b.dataset.action='accept';}

}
function renderChat(){
 const ctx=conversation(),isPrivate=page==='private',isPublic=page==='public';
 const panel=$('.chat-panel');if(!panel)return;$$('.mmd-composer-extra',panel).forEach(e=>e.remove());
 $$('.context-summary strong,.discussion-brief strong').forEach(e=>e.textContent=isPrivate?'密议':isPublic?'厅前公议':'榜文议事');$$('.context-summary small,.discussion-brief small').forEach(e=>e.textContent=isPrivate?(ctx.agent?.name||'请选择好汉'):taskTitle()+' / '+(ctx.agent?.name||'尚未点将'));const em=$('.context-summary em');if(em)em.textContent=isPrivate?(ctx.pending?'正在回复':'与好汉单独聊聊'):status();if(!isPrivate){const back=$('.panel-return');if(back)back.dataset.prototypePage=isPublic?'map':'detail';}if(isPrivate){const back=$('.panel-return');if(back)back.dataset.prototypePage='agents';const heading=$('#juyiting-floating-panel-title');if(heading)heading.textContent='密议';}
 $$('.discussion-brief').forEach(e=>e.remove());
 const messages=$('.hall-messages');messages.setAttribute('aria-live','polite');messages.innerHTML=ctx.messages.map((m,index)=>`<div class="hall-message ${m.role}"><div class="message-head"><strong>${m.role==='USER'?'你':esc(ctx.agent?.name||'好汉')}</strong></div><div class="message-content"><p>${esc(m.text)}</p></div>${m.quote?`<div class="mmd mmd-quote">引用：${esc(asset(m.quote)?.name)}</div>`:''}${files(m.files||[],'message',false)}<details data-v-4c0df501 class="text-selection-archive"><summary data-v-4c0df501>保存文字片段</summary><label data-v-4c0df501>要保存的文字<textarea data-v-4c0df501 data-message-text="${index}" rows="3">${esc(m.text)}</textarea></label><button data-v-4c0df501 type="button" data-action="save-text" data-message="${index}">保存到工作空间</button></details>${m.outputs?.length?`<div class="mmd mmd-results">${m.outputs.map(id=>result(asset(id))).join('')}</div>`:''}</div>`).join('')+(ctx.error?`<div class="mmd mmd-interaction-error" role="alert">${esc(ctx.error)} ${button('核对回复状态','complete-reply-status')}</div>`:'')+(ctx.pending?'<p class="mmd-pending" role="status">正在回复…</p>':'');scoped(messages,'data-v-8f1da78a');
 if(!ctx.messages.length)insert(messages,`<p class="mmd-pending">${isPrivate?'想聊什么，直接说吧。密议不会创建或更改事项。':isPublic?'这里是公共议事，可继续讨论，不会自动创建事项。':ctx.task?'这是此事项的新话头。请继续补充需求，无需重新提交事项。':'请先提出需求，确认承办后在这里继续沟通。'}</p>`);
 const input=$('.composer-textarea');input.disabled=!!(ctx.task?.complete||ctx.task?.cancelled);input.value=ctx.chatDraft;input.placeholder=ctx.task?.cancelled?'事项已取消，仅查看议事记录':ctx.task?.complete?'事项已完成':'补充需求，或告诉好汉哪里需要调整…';
 $$('.composer-context,.composer-meta,.hall-voice-controls',panel).forEach(e=>e.remove());input.rows=2;input.style.height='';
 $('.composer-execute')?.remove();const send=$('.composer-send');send.innerHTML='发送';send.ariaLabel='发送';send.title='发送';send.disabled=ctx.pending||!!(ctx.task?.complete||ctx.task?.cancelled)||(!ctx.chatDraft.trim()&&!ctx.chatFiles.length)||(!ctx.agent&&page!=='public');
 const form=$('.composer-submit'),body=$('.composer-body');$$('.composer-more',panel).forEach(e=>e.remove());
 const extra=document.createElement('div');extra.className='mmd mmd-composer-extra';extra.innerHTML=`${ctx.quote?`<div class="mmd-quote">引用：${esc(asset(ctx.quote)?.name)} ${button('取消引用','unquote')}</div>`:''}${files(ctx.chatFiles,'chat')}`;if(ctx.quote||ctx.chatFiles.length)body.before(extra);
 const more=document.createElement('button');more.type='button';more.className='composer-more';more.dataset.action='composer-more';more.textContent='＋';more.ariaLabel='添加资料、语音输入与设置';more.title='添加资料、语音输入与设置';more.disabled=!!(ctx.task?.complete||ctx.task?.cancelled);$('.composer-actions').prepend(more);
 syncCurrentComposer(panel);
 if(ctx===state&&unifiedTask()){
  input.disabled=ctx.pending||!!(ctx.task.complete||ctx.task.cancelled);input.placeholder=ctx.task.cancelled?'事项已取消，仅查看议事记录':ctx.task.complete?'事项已完成，仅查看议事记录':ctx.task.phase==='待你补充'?'在这里补充要求或添加资料…':'哪里需要调整？直接说，继续改。';send.disabled=ctx.pending||!!ctx.error||!!(ctx.task.complete||ctx.task.cancelled)||(!ctx.chatDraft.trim()&&!ctx.chatFiles.length);
  const heading=$('.context-summary strong',panel);if(heading)heading.textContent='议事';
  const subtitle=$('.context-summary small',panel);if(subtitle)subtitle.textContent=ctx.task.title+' / '+ctx.agent.name;
  const phase=$('.context-summary em',panel);if(phase)phase.textContent=ctx.task.phase;
  $('.unified-chat-banner',panel)?.remove();
  $('.unified-conversation-note',panel)?.remove();
  const title=$('#juyiting-floating-panel-title');if(title)title.textContent='议事';
 }

 const scrollEnd=()=>{if(messages.isConnected)messages.scrollTop=messages.scrollHeight;};requestAnimationFrame(scrollEnd);$$('img',messages).forEach(img=>img.addEventListener('load',scrollEnd,{once:true}));
}
function renderWorkspace(){const list=$('.treasure-file-list');if(!list)return;const all=[...catalog,...state.localFiles,...state.saved.map(asset)].filter((a,i,arr)=>arr.findIndex(x=>x.id===a.id)===i),filter=state.workspaceFilter||'全部';const items=all.filter(a=>filter==='回收站'?state.fileMeta[a.id]?.recycled:!state.fileMeta[a.id]?.recycled&&(filter==='全部'||filter==='资料'&&!state.saved.includes(a.id)||filter==='成果'&&state.saved.includes(a.id)));
 list.innerHTML=items.filter(a=>!state.workspaceQuery||a.name.toLowerCase().includes(state.workspaceQuery.toLowerCase())).map(a=>`<div class="treasure-file-row" data-file-id="${a.id}"><div><strong>${esc(a.name)}</strong><p>${esc(a.note||a.type)} · 本地演示版本</p></div>${button('查看','complete-file',`data-id="${a.id}"`)}</div>`).join('')||'<p class="mmd" role="status">此分类暂无资料。</p>';scoped(list,'data-v-a1bd66a6');const tabs=$('.treasure-tabs');if(tabs)tabs.innerHTML=['全部','资料','成果','回收站'].map(label=>button(label,'complete-workspace-filter',`data-filter="${label}" aria-pressed="${filter===label}"`)).join('');}
function submitRequest(){startUnifiedConversation();}
function assign(){if(!state.selectedAgent||!state.task||state.agent||(state.task.complete||state.task.cancelled))return;state.task.notStarted=false;state.agent={...state.selectedAgent};state.messages=[{role:'USER',text:state.task.description,files:[...state.task.files]}];go('chat');reply(state.task.description||'请确认这些资料的用途。',true,state);}
function output(type,text,revision,ctx=conversation()){const id='result-'+(++serial);const a={id,type,name:'',text,note:'第 '+revision+' 稿'};if(type==='image'){a.name=`小鸟-第${revision}稿.svg`;a.url=revision===1?'assets/bird-v1.svg':'assets/bird-v2.svg';}else if(type==='audio'){a.name=`音频-第${revision}稿.wav`;a.url='assets/sample.wav';}else if(type==='document'){a.name=`活动方案-第${revision}稿.md`;a.url='assets/plan.md';a.text='# 自然观察活动方案\n\n目标：认识身边的鸟类，记录观察结果。\n\n1. 介绍观察方法。\n2. 分组观察并记录。\n3. 分享发现，整理成果。\n\n保持距离，不打扰动物。';}else a.name=`文字成果-第${revision}稿.txt`;ctx.outputs.push(a);return id;}
function reply(text,first=false,ctx=conversation()){
 ctx.pending=true;ctx.pendingReason='reply';if(conversation()===ctx&&(['chat','private','public'].includes(page)))renderChat();persist();const task=ctx.task;
 setTimeout(()=>{if(ctx.task!==task||task?.cancelled)return;const revision=ctx.messages.filter(m=>m.outputs?.length).length+1;let ids=[],answer;
 if(ctx!==state&&!/画|图片|照片|音频|配音|方案|文档|文件|介绍/.test(text)){answer='我是'+ctx.agent.name+'，可以直接和我聊，也可以补充资料。你想先聊哪件事？';}
 else if(first&&(!ctx.task?.description||/^(帮我|做一下|处理一下|优化一下|改一下|看看)[。！!\s]*$/.test(text.trim())||text.trim().length<3)){answer='你希望完成什么内容？可以补充用途或想要的结果，也可以添加一份资料。';}
 else {const history=ctx.messages.filter(m=>m.role==='USER').map(m=>m.text).join(' ');const image=asset(ctx.messages.at(-1)?.quote)?.type==='image'||/画|图片|小鸟|照片|配图|插画/.test(text)||(!/音频|配音|文档|方案|文字|介绍/.test(text)&&/画|图片|小鸟|照片/.test(history));const audio=/音频|配音|声音/.test(text),doc=/方案|文档|文件|纪要/.test(text);if(image)ids.push(output('image','',revision,ctx));if(audio)ids.push(output('audio','',revision,ctx));if(doc)ids.push(output('document','',revision,ctx));if(!ids.length||/文字|介绍|说明/.test(text))ids.push(output('text','小鸟停在枝头，轻轻侧头，望向远处。愿你在忙碌中，也留意身边这些小小的美好。\n\n（原型示例文字，可作为独立成果验收。）',revision,ctx));answer=first?'先给你这一版，看看是否符合你的想法。':'已按补充内容整理了新一稿，上一稿仍保留在会话中。';}
 ctx.messages.push({role:'AGENT',text:answer,outputs:ids});
 // Explicit demo deliverable slots: a revision replaces its slot, not unrelated files.
 for(const id of ids){const a=asset(id);ctx.delivery=(ctx.delivery||[]).filter(old=>asset(old)?.type!==a.type);ctx.delivery.push(id);}
 ctx.error=null;ctx.pending=false;ctx.pendingReason=null;persist();if(conversation()===ctx&&(['chat','private','public'].includes(page)))renderChat();else if(ctx===state&&page==='detail')renderDetail();
 },650);
}
function send(){const ctx=conversation();if(ctx===state&&unifiedTask()){sendUnifiedDraft();return;}if(state.simulation.reply==='failed'){ctx.error='示例：尚不能确认已受理。草稿和附件保留，不自动重发。';renderChat();persist();return;}if(ctx.pending||(ctx.task?.complete||ctx.task?.cancelled)||(!ctx.agent&&page!=='public')||(!ctx.chatDraft.trim()&&!ctx.chatFiles.length))return;if(ctx===state&&ctx.task)ctx.task.notStarted=false;const text=ctx.chatDraft.trim();ctx.messages.push({role:'USER',text:text||'请结合这些资料继续。',files:[...ctx.chatFiles],quote:ctx.quote});if(ctx===state&&ctx.task)ctx.task.files=[...new Set([...ctx.task.files,...ctx.chatFiles])];ctx.chatFiles=[];ctx.chatDraft='';ctx.quote=null;reply(text||'请结合这些资料继续。',false,ctx);}
function dialog(title,html,footer=''){const d=document.createElement('dialog');d.className='mmd mmd-dialog'+(title==='删除话头'?' history-delete-dialog':'');d.setAttribute('aria-label',title);d.innerHTML=`<header><h3>${esc(title)}</h3>${title==='删除话头'?'':button('关闭','close-dialog','aria-label="关闭窗口"')}</header>${html}${footer?'<footer>'+footer+'</footer>':''}`;document.body.append(d);lastFocus=document.activeElement;d.addEventListener('close',()=>{d.remove();if(lastFocus?.isConnected)lastFocus.focus();});d.showModal();return d;}
function openMaterials(context,selection=null){
 const ids=selection||(context==='chat'?conversation().chatFiles:state.draftFiles);
 picker={context,conversation:conversation(),ids:[...ids],selected:null,preview:false,previewDismissed:false,expanded:false};
 const d=dialog('选择资料','');d.classList.add('material-picker-dialog');
 d.querySelector('header').innerHTML=button('← 返回','close-dialog','class="panel-return material-back" aria-label="返回，取消本次资料选择"')+'<div><h3>选择资料</h3><p>从工作空间选择资料，固定版本后添加。</p></div>';
 d.insertAdjacentHTML('beforeend','<div class="material-picker-main"><div class="material-picker-body" aria-label="可选资料"></div><section class="material-detail" aria-label="当前资料"></section></div><footer class="material-picker-footer"></footer>');
 d.addEventListener('cancel',e=>{if(picker.expanded||picker.preview){e.preventDefault();if(picker.expanded)picker.expanded=false;else {picker.preview=false;picker.previewDismissed=true;}renderMaterialPicker(picker.preview?'picker-preview':'picker-toggle-selected');}});
 renderMaterialPicker();$('.material-back',d).focus({preventScroll:true});
}
function renderMaterialPicker(focusAction,focusId){
 const d=$('.material-picker-dialog');if(!d)return;
 const active=document.activeElement,scroll=$('.material-picker-body',d).scrollTop,desktop=innerWidth>720;
 if(desktop){picker.preview=false;picker.previewDismissed=false;}
 focusAction=focusAction||active?.dataset.action;focusId=focusId||active?.dataset.id;
 const all=[...new Map([...catalog,...state.localFiles,...state.saved.map(asset)].filter(a=>a&&!state.fileMeta[a.id]?.recycled).map(a=>[a.id,a])).values()];
 d.classList.toggle('is-preview',picker.preview);d.classList.toggle('preview-dismissed',!!picker.previewDismissed);
 const back=$('.material-back',d);back.dataset.action=picker.preview?'picker-preview':'close-dialog';back.setAttribute('aria-label',picker.preview?'返回资料列表':'返回，取消本次资料选择');
 $('.material-picker-body',d).innerHTML=all.map(a=>button(`<span><strong>${esc(a.name)}</strong><small>最新 v${esc(a.version||1)}</small></span>${picker.ids.includes(a.id)?'<span class="material-added">已添加</span>':'<span class="material-chevron" aria-hidden="true">›</span>'}`,'picker-select',`data-id="${esc(a.id)}" aria-pressed="${picker.selected===a.id}" class="material-file${picker.selected===a.id?' selected':''}"`)).join('')||'<p>暂无资料，也可以直接提需求。</p>';
 const a=asset(picker.selected);
 $('.material-detail',d).innerHTML=a?`<div class="material-detail-heading"><strong>${esc(a.name)}</strong><small>已固定 v${esc(a.version||1)} · 版本管理在工作空间</small></div>${picker.previewDismissed?'<p class="material-preview-collapsed" role="status">预览已关闭，可重新预览或继续选择资料。</p>':''}<section class="material-inline-preview" aria-label="资料预览">${a.type==='image'?`<img src="${esc(a.url)}" alt="${esc(a.name)}（原型示意插画）">`:media(a,true)}</section><div class="material-version">${desktop||picker.preview?'':button('预览','picker-preview','aria-expanded="false"')}${button('下载','download',`data-id="${esc(a.id)}"`)}${button(picker.ids.includes(a.id)?'已添加':'添加','picker-stage',picker.ids.includes(a.id)?'disabled':'class="mmd-primary"')}</div>`:'<div class="material-preview-empty"><span aria-hidden="true">▧</span><p>选择一份资料</p><small>在这里查看完整预览并添加</small></div>';
 $('.material-picker-body',d).scrollTop=scroll;
 $('.material-picker-footer',d).innerHTML=`${picker.expanded?`<section id="material-selected-tray" class="material-selection-tray" aria-label="已选资料"><div class="material-tray-heading"><strong>已选资料（${picker.ids.length}）</strong>${button('收起','picker-toggle-selected')}</div><ul class="material-staged">${picker.ids.map(id=>{const x=asset(id);return x?`<li><span>${esc(x.name)}<small>固定 v${esc(x.version||1)}</small></span>${button('移除','picker-remove',`data-id="${esc(id)}" aria-label="移除 ${esc(x.name)}"`)}</li>`:'';}).join('')||'<li>尚未添加资料</li>'}</ul></section>`:''}<div class="material-selection-summary">${button('已选 '+picker.ids.length+' 份资料 '+(picker.expanded?'⌄':'⌃'),'picker-toggle-selected','aria-expanded="'+picker.expanded+'"')}<small role="status">${picker.ids.length?'点击完成后带入需求':'资料非必选'}</small></div><div class="material-footer-actions">${button('取消','close-dialog')}${button('完成（'+picker.ids.length+'）','confirm-materials','class="mmd-primary"')}</div>`;
 const candidate=$$('[data-action]',d).find(e=>e.dataset.action===focusAction&&(!focusId||e.dataset.id===focusId)&&!e.disabled&&e.getClientRects().length);
 if(candidate)candidate.focus({preventScroll:true});else if(d.contains(active)&&focusAction)$('[data-action=confirm-materials]',d).focus({preventScroll:true});
}
function preview(id){const a=asset(id);if(!a)return;const d=dialog(a.name,`<div class="mmd-preview">${media(a,true)}<p class="mmd-muted">${a.type==='image'?'原型示意插画，非真实 Agent 生成照片。':'离线示例内容。'}</p></div>`,button('下载文件','download',`data-id="${id}" class="mmd-primary"`));d.classList.add('attachment-preview');}
function download(id){const a=asset(id);if(!a)return;let url=a.url,blob=false;if(!url){url=URL.createObjectURL(new Blob([a.text||''],{type:'text/plain;charset=utf-8'}));blob=true;}const link=document.createElement('a');link.href=url;link.download=a.name;document.body.append(link);link.click();link.remove();if(blob)setTimeout(()=>URL.revokeObjectURL(url),2000);}
function deliveryList(){return finalDraft.map(id=>{const a=asset(id);return a?`<div class="mmd-chip"><span><strong>${esc(a.name)}</strong><br><small>${esc(a.note)}</small></span>${button('预览','preview',`data-id="${id}"`)}</div>`:''}).join('')||'<p class="mmd-muted">尚无可验收成果；请回原议事补充需求。</p>';}
function accept(){if(state.task)go('results');}

function onSubmit(e){e.preventDefault();if(e.target.matches('.overview-quick-request'))submitRequest();else if(e.target.matches('.task-create-form'))startUnifiedConversation();else if(e.target.matches('.composer-submit'))send();else feedback('原型保留原有入口，本次只演示需求协作流程。');}
document.addEventListener('input',e=>{const t=e.target;if(t.matches('.overview-quick-request textarea')){state.draft=t.value;$('.quick-request-input small').textContent=t.value.length+'/200';$('.overview-quick-request button.primary').disabled=!t.value.trim()&&!state.draftFiles.length;}if(t.name==='taskDescription')state.draft=t.value;if(t.name==='taskTitle')state.title=t.value;if(t.matches('.composer-textarea')){const ctx=conversation();ctx.chatDraft=t.value;$('.composer-send').disabled=(ctx===state&&unifiedTask()&&!!ctx.error)||ctx.pending||!!(ctx.task?.complete||ctx.task?.cancelled)||(!t.value.trim()&&!ctx.chatFiles.length)||(!ctx.agent&&page!=='public');}});
document.addEventListener('change',e=>{const t=e.target;if(t.matches('[data-local-files]')){addLocalFiles(t.files);return;}if(t.dataset.pick){picker.ids=t.checked?[...new Set([...picker.ids,t.dataset.pick])]:picker.ids.filter(id=>id!==t.dataset.pick);$('[data-action=confirm-materials]').textContent='确定（'+picker.ids.length+'）';}});
document.addEventListener('click',e=>{
 const t=e.target.closest('[data-action],button,a,[data-prototype-page]');if(!t||t.disabled||t.matches('a[download]'))return;
 if(t.type==='submit'&&t.closest('form'))return;e.preventDefault();const action=t.dataset.action,id=t.dataset.id;
 if(action==='composer-more'){dialog('更多',`<div class="mmd-more-menu">${button('添加资料','composer-materials')}${button('语音输入','voice-record')}${button('语音设置','voice-settings')}</div>`);return;}
 if(action==='composer-materials'){t.closest('dialog').close();openMaterials('chat');return;}
 if(action==='voice-record'){t.closest('dialog').close();dialog('语音输入','<p role="status">正在录音…</p><p class="mmd-muted">交互演示，不会启用麦克风。</p>',button('取消','close-dialog')+button('结束录音','voice-stop','class="mmd-primary"'));return;}
 if(action==='voice-stop'){t.closest('dialog').close();dialog('确认语音文字','<label class="mmd-voice-transcript">识别内容（可修改）<textarea rows="3" aria-label="识别内容">请把画面调整得明亮一些。</textarea></label><p class="mmd-muted">以上为示例转写，不是真实录音识别。</p>',button('取消','close-dialog')+button('放入输入框','voice-use','class="mmd-primary"'));return;}
 if(action==='voice-use'){const text=$('.mmd-voice-transcript textarea').value.trim();if(!text){feedback('请输入要使用的文字');return;}const ctx=conversation();ctx.chatDraft=[ctx.chatDraft,text].filter(Boolean).join('\n');t.closest('dialog').close();renderChat();$('.composer-textarea').focus();return;}
 if(action==='voice-settings'){t.closest('dialog').close();dialog('语音设置',`<label>识别语言 <select class="mmd-voice-language" aria-label="识别语言"><option value="zh-CN">中文</option><option value="en-US">English</option></select></label><p class="mmd-muted">设置只保留在本原型，不连接语音服务。</p>`,button('取消','close-dialog')+button('保存','voice-settings-save','class="mmd-primary"'));$('.mmd-voice-language').value=state.voiceLanguage||'zh-CN';return;}
 if(action==='voice-settings-save'){state.voiceLanguage=$('.mmd-voice-language').value;t.closest('dialog').close();feedback('已保存原型语音设置');return;}
 if(action==='materials'){openMaterials(t.dataset.context);return;}
 if(action==='picker-select'){picker.selected=id;picker.preview=false;picker.previewDismissed=false;picker.expanded=false;renderMaterialPicker();return;}
 if(action==='picker-preview'){if(innerWidth>720)return;picker.preview=!picker.preview;picker.previewDismissed=!picker.preview;picker.expanded=false;renderMaterialPicker('picker-preview');return;}
  if(action==='picker-toggle-selected'){picker.expanded=!picker.expanded;renderMaterialPicker('picker-toggle-selected');return;}
 if(action==='picker-stage'){if(picker.selected&&!picker.ids.includes(picker.selected))picker.ids.push(picker.selected);renderMaterialPicker('picker-preview');return;}
 if(action==='picker-remove'){picker.ids=picker.ids.filter(x=>x!==id);renderMaterialPicker('picker-toggle-selected');return;}
 if(action==='confirm-materials'){if(picker.context==='chat')picker.conversation.chatFiles=[...picker.ids];else state.draftFiles=[...picker.ids];t.closest('dialog').close();persist();render();return;}
 if(action==='close-dialog'){t.closest('dialog').close();return;}
 if(action==='preview'){if(!t.closest('.mmd-preview'))preview(id);return;}
 if(action==='download'){download(id);return;}
 if(action==='remove'){const key=t.dataset.context==='chat'?'chatFiles':'draftFiles';const ctx=t.dataset.context==='chat'?conversation():state;ctx[key]=ctx[key].filter(x=>x!==id);render();return;}
 if(action==='choose-agent'){state.selectedAgent={id:t.dataset.agent,name:$('strong',t).textContent};renderAgents();return;}
 if(action==='private-chat'){openPrivate();return;}
 if(action==='assign'){assign();return;}
 if(action==='save-text'){const text=$('[data-message-text="'+t.dataset.message+'"]').value.trim();if(!text){feedback('先选好要保存的文字');return;}const a={id:'saved-text-'+(++serial),name:'议事文字片段-'+serial+'.txt',type:'text',text,note:'议事文字'};state.archive.push(a);state.saved.push(a.id);feedback('文字片段已保存到工作空间');return;}
 if(action==='save'){if(!state.saved.includes(id)){state.saved.push(id);state.archive.push({...asset(id)});}t.disabled=true;t.textContent='已保存';feedback('已保存到工作空间');return;}
 if(action==='quote'){const ctx=conversation();ctx.quote=id;ctx.chatDraft=unifiedTask()&&ctx===state?'请把这一版改为：':'请把这一稿';renderChat();$('.composer-textarea').focus();return;}
 if(action==='unquote'){conversation().quote=null;renderChat();return;}
 if(action==='workspace'){workspaceFrom='chat';go('workspace');return;}
 if(action==='back-chat'){go('chat');return;}
 if(action==='task-files'){dialog('事项资料',state.task?.files.length?files(state.task.files,'task',false):'<p>暂无资料，可以继续议事，无需添加。</p>');return;}
 if(action==='accept'){accept();return;}
 if(action==='continue-chat'){if(state.task?.complete||state.task?.cancelled){feedback('终态事项只读。');return;}go(state.agent?'chat':'agents');return;}
 if(action==='finish'){beginAcceptance();return;}
 if(t.dataset.prototypePage){if(t.dataset.prototypePage==='detail'&&!state.task){feedback('先提出需求，原型不自动建立事项。');return;}if(t.dataset.prototypePage==='materials')openMaterials('draft');else if(t.dataset.prototypePage==='workspace'){workspaceFrom=page==='chat'?'chat':null;go('workspace');}else go(t.dataset.prototypePage);return;}
 if(t.matches('.workbench-mobile-more')){dialog('更多',`<div class="mmd-row">${button('点将册','go-agents')}${button('提出需求','go-create')}</div>`);return;}
 if(action==='go-agents'){go('agents');return;}if(action==='go-create'){go('create');return;}
 if(t.matches('.voice-start,.voice-settings-trigger')){feedback('此原型不启用麦克风，语音入口保持原样。');return;}
 feedback('保留现有入口；本次原型只演示需求、资料、议事与验收。');
});
window.addEventListener('hashchange',()=>{if(labels[location.hash.slice(1)]){page=location.hash.slice(1);if(page!=='detail')state.recommendation=null;render();}});
window.addEventListener('resize',()=>{if($('dialog[open]')){syncViewport();if($('.material-picker-dialog'))renderMaterialPicker();return;}if(view!==(innerWidth<=900?'mobile':'desktop'))render();else syncViewport();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('dialog[open]')){if(page==='chat')go('detail');else if(page==='private')go('agents');}});
for(const event of ['input','change','click'])document.addEventListener(event,()=>queueMicrotask(persist));
window.addEventListener('pagehide',persist);
seedBaseline();
render();
for(const ctx of [state,state.publicChat,...Object.values(state.privateChats)])if(ctx.pending&&['reply','unified-reply'].includes(ctx.pendingReason)){ctx.pending=false;ctx.error='示例：刷新时回复状态待核对，不自动重发。';if(ctx.task?.unified)ctx.task.phase='需核对';persist();if(['chat','private','public'].includes(page))renderChat();}
if(state.operation?.stage==='pending')setTimeout(resolveOperation,350);
