'use strict';
(() => {
  const $ = (s, root = document) => (root === document ? document.querySelector('#panel[open]')?.querySelector(s) : null) || root.querySelector(s);
  const $$ = (s, root = document) => [...root.querySelectorAll(s)];
  const esc = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const icon = name => `<i class="var-icon--set var-icon-${name}" aria-hidden="true"></i>`;
  const button = (text, action, style = '', attrs = '') => `<button type="button" class="${style}" data-action="${action}" ${attrs}>${text}</button>`;
  const openButton = (text, name, style = '') => `<button type="button" class="${style}" data-open="${name}">${text}</button>`;
  const sampleTime = '09-23 16:30';
  const people = {
    songjiang:{id:'songjiang',name:'宋江',nickname:'及时雨',star:'天魁星',abilities:['统筹协作','需求分拨'],state:'候命',description:'负责统筹与分拨。这里使用演示资料，不代表线上好汉的实时能力。'},
    wuyong:{id:'wuyong',name:'吴用',nickname:'智多星',star:'天机星',abilities:['聚义厅协作','智能体管理','智能体调度'],state:'候命',description:'从需求梳理、方案设计到步骤拆解，先把事情想清楚，再与众好汉协作。'},
    linchong:{id:'linchong',name:'林冲',nickname:'豹子头',star:'天雄星',abilities:[],state:'候命',description:'本领尚未配置。本演示不把人物设定当作运行时能力，交办前需在正式环境确认。'},
    husanniang:{id:'husanniang',name:'扈三娘',nickname:'一丈青',star:'地慧星',abilities:[],state:'候命',description:'本领尚未配置。可在正式环境中查看能力与可用状态；当前仅为界面演示。'},
    likui:{id:'likui',name:'李逵',nickname:'黑旋风',star:'天杀星',abilities:[],state:'候命',description:'本领尚未配置。保留好汉风格，真实能力以正式环境的运行时配置为准。'},
    lujunyi:{id:'lujunyi',name:'卢俊义',nickname:'玉麒麟',star:'天罡星',abilities:[],state:'候命',description:'地图中的展示好汉，不代表点将册中可用的执行者。'}
  };
  // The map and roster are deliberately independent, as in the production contract.
  const mapAgentIds = ['songjiang','wuyong','linchong','husanniang','likui','lujunyi'];
  const rosterIds = ['husanniang','likui','linchong','wuyong'];
  const initialTasks = [
    {id:'DEMO-401',title:'整理一份会议简报',status:'assigned',agent:'wuyong',kind:'formal',description:'将会议记录整理成一页简报，列出结论、负责人和下一步行动。',format:'PDF',materials:['f1'],updatedAt:5},
    {id:'DEMO-402',title:'优化简历',status:'draft',agent:'linchong',kind:'private',description:'优化项目经历的表达，突出个人贡献和可量化成果。',format:'Word（DOCX）',materials:[],updatedAt:4},
    {id:'DEMO-403',title:'B站视频发布',status:'failed',agent:'husanniang',kind:'formal',description:'准备投稿文案和素材清单。演示异常：缺少完整的视频素材。',format:'PDF',materials:[],updatedAt:3},
    {id:'DEMO-404',title:'生成一个网站',status:'open',agent:'',kind:'formal',description:'制作一个用于展示服务内容的网站原型，先确认页面范围与内容。',format:'PDF',materials:[],updatedAt:2},
    {id:'DEMO-405',title:'新品发布文案 · 示例交付',status:'completed',agent:'wuyong',kind:'formal',description:'包含一份发布长文、三条渠道短帖与发布检查清单。',format:'PDF',materials:['f2'],updatedAt:1,archived:true}
  ];
  const initialFiles = [
    {id:'f1',name:'会议要点.txt',type:'资料',size:'2.4 KB',date:'09-23 14:20',body:'会议要点\n\n1. 明确本次交付目标与范围。\n2. 梳理负责人及待确认的问题。\n3. 形成一页简报与行动清单。\n\n以上均为本地演示材料。'},
    {id:'f2',name:'品牌介绍.txt',type:'资料',size:'1.8 KB',date:'09-22 10:30',body:'品牌介绍\n\n聚义厅：让合适的好汉，把事情一起办成。\n\n此文件为演示资料，未读取账户真实文件。'},
    {id:'f3',name:'发布文案-示例成果.txt',type:'成果',size:'3.2 KB',date:'09-23 15:10',body:'新品发布文案 · 示例成果\n\n标题：一件事，一起办成。\n\n聚义厅将目标、讨论、资料和成果放在同一件事里，让协作清晰可追溯。\n\n发布检查：核对内容、确认渠道、检查素材授权。\n\n这是预置示例，不是 AI 的实时生成结果。'}
  ];
  const freshDraft = () => ({title:'',description:'',format:'PDF',materials:[],agent:'',kind:'private',sourceId:null});
  const state = {mode:'overview',view:'overview',overlay:false,taskQuery:'',taskKind:'all',panel:null,args:{},history:[],tasks:structuredClone(initialTasks),files:structuredClone(initialFiles),draft:freshDraft(),overviewFilter:'recent',bountyFilter:'all',ability:'all',rosterFilter:'全寨',selectedAgent:null,fileFilter:'全部',fileQuery:'',chatRecipient:null,chatTask:null,chats:{public:[]},chatDrafts:{},materialSelection:[],materialReturn:null,sound:false,font:'clean',size:'normal',tint:'warm',tips:true,messageRead:false,returnFocus:null};
  const labels = {draft:'尚未交办',open:'待领令',assigned:'已领令',running:'办理中',completed:'成果可查看',failed:'未完成',archived:'已归档'};
  const tone = code => ({draft:'wait',open:'wait',failed:'failed',archived:'neutral'}[code] || '');
  const status = (code, custom) => `<span class="status ${tone(code)}">${esc(custom || labels[code] || code)}</span>`;
  const agentName = id => people[id]?.name || '待安排';
  const portrait = (id, cls = '') => `<img class="portrait ${cls}" src="assets/${people[id] ? id : 'songjiang'}.webp" alt="${esc(agentName(id))}">`;
  const kindName = task => task.status === 'draft' ? '草稿' : task.kind === 'formal' ? '正式事项' : '私人事项';
  const actionLabel = task => task.status === 'draft' ? '继续填写' : task.status === 'failed' ? '处理异常' : task.status === 'completed' ? '查看成果' : '查看进展';
  const panel = $('#panel');
  let body = $('#page-body'), footer = $('#page-footer');
  let toastTimer;
  function toast(text) { clearTimeout(toastTimer); const toastNode=$('#toast'); (panel.open?panel:document.body).append(toastNode); toastNode.textContent=text; toastNode.hidden=false; toastTimer=setTimeout(()=>$('#toast').hidden=true,4000); }
  function notifyInPanel(text) { toast(text); }
  const pages = {
    overview:['办事概览',''], bounty:['我的事项','从一个想法，到一份交付。所有进展在这里接着办。'],
    chat:['厅内议事','先把事情聊清楚，再决定交给谁。'], agents:['点将册','认识好汉，查看本领，明确选择协作对象。'],
    files:['百宝箱','资料与成果，留在一起，随时继续用。'], archive:['典籍阁','把经验留下，把办成的事收好。'],
    messages:['消息通知','只关注需要你处理的事情。'],account:['个人中心','管理你的演示空间与登录入口。'],
    settings:['偏好设置','适合自己的字号与纸面，让阅读更轻松。'],help:['使用帮助','从提出需求开始，走完一次协作。']
  };
  function setMode(mode) {
    closePanel(false); state.mode=mode; $('#app').dataset.mode=mode;
    $('#business-shell').hidden=mode!=='overview'; $('#map-stage').inert=mode!=='map';
    if(mode==='overview') navigate('overview'); else resizeMap();
  }
  function navigate(name) {
    if(!pages[name])return;
    closePanel(false);state.mode='overview';state.view=name;state.panel=name==='overview'?null:name;state.args={};
    $('#app').dataset.mode='overview';$('#business-shell').hidden=false;$('#map-stage').inert=true;
    body=$('#page-body');footer=$('#page-footer');
    renderMain();$('#work-main').scrollTop=0;$('#work-main').focus({preventScroll:true});
  }
  function renderMain() {
    const view=state.view;$('#business-shell').dataset.view=view;$('#overview').hidden=view!=='overview';$('#page-view').hidden=view==='overview';
    $('#current-page').textContent=pages[view][0];$('#page-title').textContent=pages[view][0];$('#page-description').textContent=pages[view][1];
    $$('#business-shell [data-view]').forEach(el=>{el.classList.toggle('active',el.dataset.view===view);if(el.dataset.view===view)el.setAttribute('aria-current','page');else el.removeAttribute('aria-current');});
    if(view==='overview')renderOverview();else renderPanel();
  }
  function openPanel(name, args = {}, push = false) {
    if(pages[name] && !push && state.mode==='overview'){navigate(name);return;}
    if(push && state.overlay)state.history.push({name:state.panel,args:{...state.args}});else if(!state.overlay||!push)state.history=[];
    if(!state.overlay)state.returnFocus=document.activeElement;
    state.overlay=true;state.panel=name;state.args=args;body=$('#panel-body');footer=$('#panel-footer');
    if(!panel.open)panel.showModal();renderPanel();
    requestAnimationFrame(()=>{ const focus=body.querySelector('[data-autofocus]') || $('.back-button:not([hidden])',panel) || $('.panel-header [data-action=close]',panel); focus?.focus({preventScroll:true}); });
  }
  function closePanel(refresh=true) {
    const wasOpen=state.overlay;const toastNode=$('#toast');if(toastNode)document.body.append(toastNode);if(panel.open)panel.close();
    state.overlay=false;state.history=[];state.panel=state.mode==='overview'&&state.view!=='overview'?state.view:null;state.args={};
    $('#panel-body').innerHTML='';$('#panel-footer').innerHTML='';body=$('#page-body');footer=$('#page-footer');
    if(refresh&&state.mode==='overview')renderMain();
    if(wasOpen&&state.returnFocus?.isConnected)state.returnFocus.focus({preventScroll:true});
    else if(wasOpen&&state.mode==='overview')$('#work-main').focus({preventScroll:true});
  }
  function back() {
    const last=state.history.pop();if(last){state.panel=last.name;state.args=last.args;renderPanel();$('.panel-header button:not([hidden])',panel)?.focus();}else closePanel();
  }
  panel.addEventListener('cancel',event=>{event.preventDefault();closePanel();});
  function setPanel(title,html,actions='') {
    body.innerHTML=html;footer.innerHTML=actions;footer.hidden=!actions;body.classList.toggle('chat-layout',state.panel==='chat');body.scrollTop=0;
    if(state.overlay){$('#panel-title').textContent=title;panel.dataset.panel=state.panel;$('.back-button',panel).hidden=state.history.length===0;}
    else $('#page-view').dataset.page=state.view;
  }
  function taskRows(tasks) {
    return tasks.map(t=>`<article class="task-row"><div class="task-copy"><div class="task-title">${esc(t.title)}</div><div class="task-meta">${status(t.status)}<span>${kindName(t)} · ${agentName(t.agent)}</span></div></div><div class="task-actions"><button data-task="${esc(t.id)}">${actionLabel(t)} ${icon('chevron-right')}</button></div></article>`).join('') || empty('暂时没有事项','这里的筛选仅影响当前示例列表。');
  }
  function empty(title,text,action=''){return `<div class="empty">${icon('file-document-outline')}<h3>${title}</h3><p>${text}</p>${action}</div>`;}
  function filteredTasks(filter){return state.tasks.filter(t=>filter==='attention'?['draft','failed'].includes(t.status)&&!t.archived:filter==='archive'?t.archived:true).sort((a,b)=>b.updatedAt-a.updatedAt);}
  function renderOverview(){
    const waiting=state.tasks.filter(t=>['draft','failed'].includes(t.status)&&!t.archived).length;
    $('#overview').innerHTML=`<section class="welcome"><div class="eyebrow">聚义厅 · 轻量工作台</div><h1>今天，想办成什么事？</h1><p>不必独自忙碌，让合适的好汉与你一起。</p></section>
      <section class="start-card"><div class="start-mark">事</div><div class="start-copy"><h2>说一件你想办的事</h2><p>从目标开始，补齐资料，再交给明确的好汉。</p><div class="row">${button(icon('plus')+' 提出需求','new-demand','primary')}${openButton(icon('chat-processing-outline')+' 先聊一聊','chat')}</div></div><div class="start-steps"><span><b>01</b>说清目标</span><i></i><span><b>02</b>选好帮手</span><i></i><span><b>03</b>收好成果</span></div></section>
      <div class="overview-columns"><div class="overview-primary"><section class="work-card recent-card"><div class="section-head"><div><h2>接着上次办</h2><p>进展、资料和讨论，都在同一件事里。</p></div>${openButton('全部事项 '+icon('chevron-right'),'bounty','text-button')}</div><nav class="tabs" aria-label="事项范围">${[['recent','最近事项'],['attention','需要我处理'],['archive','已归档']].map(([key,label])=>`<button data-overview-filter="${key}" class="${state.overviewFilter===key?'active':''}" aria-pressed="${state.overviewFilter===key}">${label}${key==='attention'?`<span class="count">${waiting}</span>`:''}</button>`).join('')}</nav><section id="overview-rows" aria-live="polite">${taskRows(filteredTasks(state.overviewFilter))}</section><div class="card-bottom"><span>示例空间 · ${state.tasks.length} 件事项</span>${button(icon('refresh')+' 刷新','refresh-overview','text-button')}</div></section>
      <section class="work-card resource-strip"><div class="resource-icon">${icon('file-document-outline')}</div><div class="grow"><h3>资料留在这里，下次不用重找</h3><p>引用已有资料，也可以查看示例成果。</p></div>${openButton('打开百宝箱 '+icon('chevron-right'),'files','text-button')}</section></div>
      <aside class="overview-aside"><button class="map-entry" data-mode="map"><img src="assets/hall-scene.webp" alt="梁山聚义厅静态场景预览"><span class="map-entry-copy"><span><strong>也可以，去厅中走走</strong><small>厅中实景 · 静态地图演示</small></span>${icon('chevron-right')}</span></button><section class="work-card attention-card"><div class="section-head"><h2>需要你看一眼</h2>${icon('bell-outline')}</div>${state.tasks.filter(t=>['failed','draft'].includes(t.status)&&!t.archived).slice(0,2).map(t=>`<button class="attention-item" data-task="${t.id}"><span class="attention-dot ${t.status}"></span><span><strong>${esc(t.title)}</strong><small>${t.status==='failed'?'资料待补充 · 处理异常':'草稿已保留 · 接着填写'}</small></span>${icon('chevron-right')}</button>`).join('')||'<p class="small muted">暂时没有待处理事项。</p>'}</section>
      <section class="work-card compact-agents"><div class="section-head"><h2>找位好汉</h2>${openButton('点将册 '+icon('chevron-right'),'agents','text-button')}</div>${['wuyong','linchong','husanniang'].map(id=>`<button class="compact-agent" data-agent="${id}">${portrait(id)}<span><strong>${people[id].name}<small>${people[id].nickname}</small></strong><em>${people[id].abilities.length?'协作 · 管理 · 调度':'本领待配置'}</em></span>${icon('chevron-right')}</button>`).join('')}<p class="side-note">点将册 ${rosterIds.length} 位 · 状态均为演示</p></section>
      </aside></div>`;
  }
  const titles={quick:'聚义厅',bounty:'悬赏榜',chat:'厅内议事',files:'百宝箱',agents:'点将册',messages:'消息',account:'个人中心',archive:'典籍阁',settings:'样式设置',help:'怎么开始？',login:'用户登录',demand:'提出需求',confirm:'确认交办',materials:'选择资料',preview:'资料预览',task:'事项进展',recruit:'招贤令',reader:'典籍阁',guide:'新手引导'};
  function renderPanel(){
    switch(state.panel){
      case 'quick': renderQuick();break;
      case 'bounty':renderBounty();break;
      case 'agents':renderAgents();break;
      case 'demand':renderDemand();break;
      case 'confirm':renderConfirm();break;
      case 'task':renderTask();break;
      case 'chat':renderChat();break;
      case 'chat-history':renderChatHistory();break;
      case 'files':renderFiles();break;
      case 'materials':renderMaterials();break;
      case 'preview':renderPreview();break;
      case 'archive':renderArchive();break;
      case 'reader':renderReader();break;
      case 'messages':renderMessages();break;
      case 'account':renderAccount();break;
      case 'settings':renderSettings();break;
      case 'help':renderHelp();break;
      case 'guide':renderGuide();break;
      case 'login':renderLogin();break;
      case 'recruit':renderRecruit();break;
      default:setPanel('界面演示',empty('暂无内容','返回聚义厅继续体验。'));
    }
  }
  function renderQuick(){
    const items=[['overview','home-outline','办事概览'],['bounty','format-list-checkbox','我的事项'],['chat','chat-processing-outline','厅内议事'],['agents','account-circle-outline','点将册'],['files','file-document-outline','百宝箱'],['archive','notebook','典籍阁'],['messages','bell-outline','消息通知'],['account','account-circle-outline','个人中心'],['settings','cog-outline','偏好设置'],['help','help-circle-outline','使用帮助']];
    setPanel('全部入口',`<div class="quick-grid">${items.map(([id,i,label])=>`<button class="quick-card" data-view="${id}">${icon(i)}<span>${label}</span></button>`).join('')}<button class="quick-card" data-mode="map">${icon('map-marker-outline')}<span>厅中实景</span></button></div>`,`<span class="muted">工作台为首页，地图始终可达</span>${button('关闭','close')}`);
  }
  function renderBounty(){
    const stages=[['all','全部'],['draft','草稿'],['open','待领令'],['assigned','已领令'],['running','办理中'],['completed','成果'],['failed','异常'],['archived','已归档']];
    const inStage=(t,key)=>key==='all'?true:key==='archived'?t.archived:t.status===key&&!t.archived;
    let tasks=state.tasks.filter(t=>inStage(t,state.bountyFilter)&&(state.taskKind==='all'||t.kind===state.taskKind)&&t.title.toLowerCase().includes(state.taskQuery.toLowerCase()));
    if(state.ability!=='all')tasks=tasks.filter(t=>t.agent&&people[t.agent]?.abilities.includes(state.ability));
    setPanel('我的事项',`<div class="filter-row"><div class="row"><select id="task-kind" aria-label="事项类型">${[['all','所有事项类型'],['formal','正式悬赏'],['private','私人事项']].map(([v,l])=>`<option value="${v}" ${state.taskKind===v?'selected':''}>${l}</option>`).join('')}</select><select id="ability-filter" aria-label="本领筛选"><option value="all">所有本领</option>${['聚义厅协作','智能体管理','智能体调度'].map(a=>`<option ${state.ability===a?'selected':''}>${a}</option>`).join('')}</select></div><div class="row">${button('正式悬赏','new-formal')}${button(icon('plus')+' 新建事项','new-demand','primary')}</div></div><form id="task-search" class="search-row"><input id="task-query" aria-label="搜索事项名称" placeholder="搜索事项名称" value="${esc(state.taskQuery)}"><button type="submit">${icon('magnify')}搜索</button></form><nav class="tabs" aria-label="事项状态">${stages.map(([key,l])=>`<button class="${state.bountyFilter===key?'active':''}" data-bounty-filter="${key}" aria-pressed="${state.bountyFilter===key}">${l}<span class="count">${state.tasks.filter(t=>inStage(t,key)).length}</span></button>`).join('')}</nav><div class="board-list">${taskRows(tasks.sort((a,b)=>b.updatedAt-a.updatedAt))}</div><p class="side-note">${tasks.length} 件符合当前筛选 · 已领令不等于正在执行 · 本地演示数据</p>`);
  }
  function renderAgents(){
    const active=state.selectedAgent&&people[state.selectedAgent];
    const roster=rosterIds.map(id=>people[id]).filter(p=>state.rosterFilter==='全寨'||p.state===state.rosterFilter);
    setPanel('点将册',`<div class="filter-row"><div class="segmented">${['全寨','候命','办事','出征','失联'].map(l=>`<button data-roster-filter="${l}" class="${state.rosterFilter===l?'active':''}" aria-pressed="${state.rosterFilter===l}">${l}</button>`).join('')}</div>${openButton('招贤令','recruit')}</div><div class="row between small muted"><span>簿上 ${rosterIds.length} / 厅中 ${mapAgentIds.length}</span><span>演示状态 · 非实时在线人数</span></div><div class="agent-layout"><div class="agent-list">${roster.map(p=>`<button class="agent-row ${p.id===state.selectedAgent?'selected':''}" data-select-agent="${p.id}" aria-pressed="${p.id===state.selectedAgent}">${portrait(p.id)}<span class="agent-info"><strong>${p.name}</strong><small>${p.nickname} / ${p.star}<br>${p.abilities.length?p.abilities.join(' · '):'未录本领'}</small></span>${status('assigned',p.state)}</button>`).join('')||empty('此分类没有好汉','筛选点将册不会改变地图中的好汉。')}</div><section class="agent-detail" aria-live="polite">${active?`${portrait(active.id)}<h2>${active.name} <span class="small muted">${active.nickname}</span></h2><p>${active.description}</p><div class="section-gap">${active.abilities.map(a=>`<span class="tag">${a}</span>`).join('')||'<span class="tag">本领尚未配置</span>'}</div><div class="row">${button('找他议事','agent-chat','',`data-id="${active.id}"`)}${rosterIds.includes(active.id)?button('交办一件事','agent-demand','primary',`data-id="${active.id}"`):'<span class="small muted">仅作地图展示</span>'}</div>`:`<h3>点一位好汉，看看他的本领。</h3><p>查看好汉后，可以议事，或带着明确目标交办。</p>`}</section></div>`);
  }
  function startDraft(kind='private',agent=''){if(state.draft.kind!==kind||!(state.draft.title||state.draft.description))state.draft=freshDraft();state.draft.kind=kind;if(agent)state.draft.agent=agent;openPanel('demand',{},state.overlay);}
  function renderDemand(){
    const d=state.draft,limit=d.kind==='formal'?30:200;
    setPanel(d.kind==='formal'?'起草正式任务':'提出需求',`<div class="steps"><span class="active"><b>1</b>说明需求</span><span><b>2</b>确认交办</span></div><form id="demand-form" novalidate><label class="field"><span class="field-label">${d.kind==='formal'?'任务名目':'事项名称'}<span class="optional">必填</span></span><input name="title" value="${esc(d.title)}" placeholder="给这件事起个名字" autocomplete="off"><span class="field-help"><span>最多 ${limit} 字，超限时提示，不截断原文</span><span id="title-count">${d.title.length}/${limit}</span></span></label><label class="field"><span class="field-label">需求描述<span class="optional">必填</span></span><textarea name="description" placeholder="例如：把会议纪要整理成一页简报，列出结论和待办。">${esc(d.description)}</textarea><span class="field-help"><span>写清目标、范围与希望得到的成果</span><span id="description-count">${d.description.length}/20000</span></span></label><div class="field"><span class="field-label">参考资料 <span class="optional">可选</span></span><div class="upload-block"><span id="draft-materials" class="small muted">${d.materials.length?`已选择 ${d.materials.length} 份资料`:'未引用资料'}</span>${button(icon('plus')+' 添加资料','pick-materials')}</div>${d.materials.length?`<div class="row" style="margin-top:10px">${d.materials.map(id=>`<span class="attachment-chip">${icon('file-document-outline')}${esc(state.files.find(f=>f.id===id)?.name||'资料')}</span>`).join('')}</div>`:''}</div><label class="field" style="margin-bottom:0"><span class="field-label">交付格式</span><select name="format">${['PDF','PPT（PPTX）','Excel（XLSX）','Word（DOCX）','JPEG 图片','PNG 图片'].map(f=>`<option ${d.format===f?'selected':''}>${f}</option>`).join('')}</select><span class="field-help">此处为示例格式；正式系统仍以服务端能力为准。</span></label><p id="demand-error" class="error-message" role="alert"></p></form>`,`<span class="muted">草稿仅保留在本次演示中</span><div class="row">${button('保存草稿','save-draft')}${button('下一步：确认交办','next-demand','primary')}</div>`);
  }
  function draftError(requireDescription=true){const d=state.draft,max=d.kind==='formal'?30:200;if(!d.title.trim())return'请先填写事项名称。';if(d.title.length>max)return`事项名称超过 ${max} 字，原文已保留，请缩短后继续。`;if(requireDescription&&!d.description.trim())return'请说明你的目标与希望得到的成果。';if(d.description.length>20000)return'需求描述超过 20000 字，原文已保留。';return'';}
  function renderConfirm(){const d=state.draft;setPanel('确认交办',`<div class="steps"><span><b>✓</b>说明需求</span><span class="active"><b>2</b>确认交办</span></div><h2 style="margin-bottom:14px">${esc(d.title)}</h2><p class="intro" style="white-space:pre-wrap">${esc(d.description)}</p><dl class="definition"><dt>事项类型</dt><dd>${d.kind==='formal'?'正式任务':'私人交办'}</dd><dt>交付格式</dt><dd>${esc(d.format)}</dd><dt>参考资料</dt><dd>${d.materials.length?`${d.materials.length} 份`:'未引用'}</dd></dl><hr class="divider"><label class="field"><span class="field-label">明确执行好汉 <span class="optional">必选</span></span><select id="assign-agent"><option value="">请选择好汉</option>${rosterIds.map(id=>`<option value="${id}" ${d.agent===id?'selected':''}>${people[id].name} · ${people[id].nickname}</option>`).join('')}</select><span class="field-help">交办使用这里明确选择的目标，不依赖地图上的隐藏选中状态。</span></label><div class="notice">这是本地流程模拟。确认后仅创建或更新本地示例事项，不调用线上接口，不消耗积分、不触发好汉执行。</div><p class="error-message" id="confirm-error" role="alert"></p>`,`<span class="muted">请核对范围与执行者</span><div class="row">${button('返回修改','edit-demand')}${button('确认交办（演示）','submit-demand','primary')}</div>`);}
  function saveDraft(){const error=draftError(false);if(error){$('#demand-error').textContent=error;return;}const d=state.draft,found=state.tasks.find(t=>t.id===d.sourceId&&t.status==='draft');if(found)Object.assign(found,structuredClone(d),{id:found.id,status:'draft',updatedAt:Date.now()});else{const id=`DEMO-${Date.now().toString().slice(-6)}`;state.tasks.unshift({...structuredClone(d),id,status:'draft',updatedAt:Date.now()});d.sourceId=id;}toast('演示草稿已保留；刷新页面即清空。');if(state.mode==='overview')renderOverview();}
  function submitDemand(){if(!rosterIds.includes(state.draft.agent)){$('#confirm-error').textContent='请选择一位点将册中的好汉。';$('#assign-agent').focus();return;}const d=structuredClone(state.draft);const draft=state.tasks.find(t=>t.id===(state.args.reassignId||d.sourceId)&&(state.args.reassignId||t.status==='draft'));const t={...d,id:draft?.id||`DEMO-${Date.now().toString().slice(-6)}`,status:'assigned',updatedAt:Date.now()};if(draft)Object.assign(draft,t);else state.tasks.unshift(t);state.draft=freshDraft();if(state.mode==='overview')renderOverview();state.history=[];openPanel('task',{id:t.id,created:true},false);toast('已完成演示交办，未触发真实执行。');}
  function openTask(id){const t=state.tasks.find(t=>t.id===id);if(!t)return;if(t.status==='draft'){state.draft={...freshDraft(),...structuredClone(t),sourceId:t.id};openPanel('demand',{},state.overlay);}else openPanel('task',{id},state.overlay);}
  function renderTask(){const t=state.tasks.find(t=>t.id===state.args.id);if(!t){setPanel('事项进展',empty('未找到事项','示例可能已被重置。'));return;}let notice=state.args.created?'<div class="notice success" style="margin-bottom:20px">演示交办已完成。本条示例为“已领令”，不代表正在执行或已经完成。</div>':'';
    if(t.status==='failed')notice+='<div class="notice error" style="margin-bottom:20px">演示异常：资料不完整。可补充资料后重新交办；不会重试真实任务。</div>';
    setPanel('事项进展',`${notice}<div class="task-detail-title"><h2>${esc(t.title)}</h2>${status(t.status)}</div><dl class="definition"><dt>事项编号</dt><dd>${esc(t.id)}</dd><dt>负责好汉</dt><dd>${agentName(t.agent)}</dd><dt>事项类型</dt><dd>${kindName(t)}</dd><dt>交付格式</dt><dd>${esc(t.format)}</dd></dl><hr class="divider"><h3>需求与范围</h3><p class="intro" style="margin:12px 0;white-space:pre-wrap">${esc(t.description)}</p><h3 class="section-gap">参考资料</h3><div class="row" style="margin-top:12px">${t.materials.length?t.materials.map(id=>button(icon('file-document-outline')+esc(state.files.find(f=>f.id===id)?.name||'资料'),'preview-file','',`data-id="${id}"`)).join(''):'<span class="small muted">未引用资料</span>'}${button('补充资料','task-materials','text-button',`data-id="${t.id}"`)}</div><h3 class="section-gap">事项进展</h3><ul class="timeline"><li>需求已记录<small>本地示例 · ${sampleTime}</small></li>${t.agent?`<li>已指定 ${agentName(t.agent)}<small>仅模拟交办，不建立真实运行任务</small></li>`:'<li>等待选择好汉<small>请明确执行者后再交办</small></li>'}<li>${labels[t.status]}<small>${t.status==='completed'?'此成果为预置示例。':'界面状态演示，不代表线上实时进度。'}</small></li></ul>${t.status==='completed'?'<div class="notice success">示例交付已准备，可查看内容或收入案卷。没有自动验收真实成果。</div>':''}`,`<span class="muted">所有操作仅改变本地示例</span><div class="row">${button('围绕此事议事','task-chat','',`data-id="${t.id}"`)}${t.status==='open'||t.status==='failed'?button(t.status==='failed'?'重新交办（演示）':'选择好汉交办','assign-task','primary',`data-id="${t.id}"`):t.status==='completed'?button('查看示例成果','view-result','primary',`data-id="${t.id}"`):button('返回工作台','overview','primary')}${t.status==='completed'?button(t.archived?'已收入案卷':'收入案卷','archive-task','',`data-id="${t.id}" ${t.archived?'disabled':''}`):''}</div>`);
  }
  function chatKey(){return `${state.chatTask||'hall'}:${state.chatRecipient||'public'}`;}
  function renderChat(){const key=chatKey(),messages=state.chats[key]||[];const recipient=state.chatRecipient?agentName(state.chatRecipient):'厅前公议';setPanel('厅内议事',`${!state.overlay?chatSessions():''}<div class="chat-toolbar"><div><h3>${recipient}</h3><div class="chat-recipient">${state.chatRecipient?'与这位好汉议事':'未点名时，由宋江分拨。'} · 本地演示</div></div><div class="row">${button('引用资料','chat-materials','ghost')}${button(icon('history'),'chat-history','icon-button','aria-label="话头记录" title="话头记录"')}${button(icon('home-outline'),'new-chat','icon-button','aria-label="返回厅前公议" title="返回厅前公议"')}</div></div>${state.chatTask?`<div class="chat-task-context"><span class="chat-context-chip" title="${esc(state.tasks.find(t=>t.id===state.chatTask)?.title||'当前事项')}">事项：${esc(state.tasks.find(t=>t.id===state.chatTask)?.title||'当前事项')}</span></div>`:''}<div id="chat-stream" class="chat-stream" aria-live="polite">${messages.length?messages.map(m=>`<article class="chat-message ${m.role==='user'?'me':''}">${m.role==='user'?'<span class="portrait" style="display:grid;place-items:center">我</span>':portrait(state.chatRecipient||'songjiang')}<div><div class="chat-byline">${m.role==='user'?'我':recipient==='厅前公议'?'宋江':recipient} · 演示</div><div class="chat-bubble">${esc(m.text)}</div></div></article>`).join(''):`<div class="chat-empty"><h2>厅前暂未开话头。</h2><p>说清目标，请众好汉一起拿个主意。</p><div class="row">${button('帮我梳理需求','chat-prompt','',`data-text="帮我梳理一下需求，并列出需要确认的问题。"`)}${button('把事情拆成步骤','chat-prompt','',`data-text="请把这件事拆成几个可以推进的步骤。"`)}</div></div>`}</div>`,`<form id="chat-form" class="chat-composer"><textarea id="chat-input" rows="1" aria-label="议事内容" placeholder="写下想讨论的目标或问题…">${esc(state.chatDrafts[key]||'')}</textarea><div class="row"><span class="muted" id="chat-counter">${(state.chatDrafts[key]||'').length}/1200 · 本地模拟，不调用 AI</span><button class="primary" type="submit">传令 ${icon('chevron-right')}</button></div></form>`);requestAnimationFrame(()=>{const stream=$('#chat-stream');if(stream)stream.scrollTop=stream.scrollHeight;});}
  function chatContexts(){return [...new Set(['hall:public','hall:wuyong','hall:linchong',...Object.keys(state.chats),...Object.keys(state.chatDrafts)])].filter(k=>k!=='public');}
  function contextLabel(key){const [task,agent]=key.split(':');return (task==='hall'?'':(state.tasks.find(t=>t.id===task)?.title||'事项')+' · ')+(agent==='public'?'厅前公议':agentName(agent));}
  function chatSessions(){return `<nav class="chat-sessions" aria-label="议事对象">${chatContexts().map(key=>`<button data-chat-key="${esc(key)}" class="${key===chatKey()?'active':''}" aria-pressed="${key===chatKey()}">${esc(contextLabel(key))}</button>`).join('')}</nav>`;}
  function renderChatHistory(){setPanel('话头记录',`<p class="intro">每位好汉、每件事项的对话和未发送草稿分别保留。仅本次演示有效。</p>${chatContexts().map(key=>`<button class="doc-row" data-chat-key="${esc(key)}"><span class="grow"><strong>${esc(contextLabel(key))}</strong><small>${(state.chats[key]||[]).length} 条演示消息${state.chatDrafts[key]?' · 有未发送草稿':''}</small></span>${icon('chevron-right')}</button>`).join('')}`);}
  function sendChat(){const key=chatKey(),text=state.chatDrafts[key]||'';if(!text.trim()){toast('先写一句想说的话。');return;}if(text.length>1200){toast('话头超过1200字，原文保留，请缩短后发送。');return;}state.chats[key] ||= [];state.chats[key].push({role:'user',text});state.chats[key].push({role:'assistant',text:'【演示回复】收到。可以先明确目标，再补齐参考资料，最后确认由哪位好汉交办。这里仅展示对话排版，不会调用真实 AI 或执行任务。'});state.chatDrafts[key]='';renderChat();$('#chat-input').focus();}
  function filesForView(){return state.files.filter(f=>(state.fileFilter==='回收站'?f.deleted:!f.deleted)&&(state.fileFilter==='全部'||state.fileFilter==='回收站'||f.type===state.fileFilter)&&f.name.toLowerCase().includes(state.fileQuery.toLowerCase()));}
  function renderFiles(){const files=filesForView();setPanel('百宝箱',`<div class="row between files-heading" style="align-items:flex-start"><div class="grow"><h2>资料与成果</h2><p class="intro" style="margin-top:8px">管理资料与成果。这里仅记录示例文件名，不读取或上传文件内容。</p></div>${button(icon('upload')+' 上传资料','upload-file','primary')}</div><input id="local-file-input" type="file" multiple hidden><div class="tabs">${['全部','资料','成果','回收站'].map(t=>`<button class="${t===state.fileFilter?'active':''}" data-file-filter="${t}" aria-pressed="${t===state.fileFilter}">${t}</button>`).join('')}</div><form id="file-search" class="search-row"><input id="file-query" aria-label="搜索文件名称" placeholder="搜索文件名称" value="${esc(state.fileQuery)}"><button type="submit">${icon('magnify')}搜索</button></form><div class="file-grid">${files.map(f=>`<article class="file-card"><div class="file-name">${icon('file-document-outline')}<span>${esc(f.name)}</span></div><div class="file-meta">${esc(f.type)} · ${esc(f.size)} · ${esc(f.date)}</div><div class="row">${button('预览','preview-file','',`data-id="${f.id}"`)}${f.deleted?button('恢复','restore-file','',`data-id="${f.id}"`):`${button('引用到新需求','file-demand','',`data-id="${f.id}"`)}${button('移入回收站','delete-file','ghost',`data-id="${f.id}"`)}`}</div></article>`).join('')}</div>${!files.length?empty('这里暂时没有文件','可以切换分类，或修改搜索条件。'):''}`);}
  function renderMaterials(){setPanel('选择资料',`<p class="intro">选好资料后，回到刚才的事项。这里只关联本地演示资料。</p><div>${state.files.filter(f=>!f.deleted).map(f=>`<label class="check-row"><input type="checkbox" data-material-id="${f.id}" ${state.materialSelection.includes(f.id)?'checked':''}>${icon('file-document-outline')}<span class="grow"><strong>${esc(f.name)}</strong><br><small class="muted">${f.type} · ${esc(f.size)}</small></span></label>`).join('')||empty('没有可选资料','先在百宝箱中添加演示文件。')}</div>`,`<span class="muted" id="material-count">已选择 ${state.materialSelection.length} 份</span><div class="row">${button('取消','back')}${button('引用所选资料','use-materials','primary')}</div>`);}
  function pickMaterials(target,id){state.materialReturn={target,id};state.materialSelection=target==='draft'?[...state.draft.materials]:target==='task'?[...(state.tasks.find(t=>t.id===id)?.materials||[])]:[];openPanel('materials',{},true);}
  function useMaterials(){const r=state.materialReturn;if(r.target==='draft')state.draft.materials=[...state.materialSelection];if(r.target==='task'){const t=state.tasks.find(t=>t.id===r.id);if(t)t.materials=[...state.materialSelection];}if(r.target==='chat'){const names=state.materialSelection.map(id=>state.files.find(f=>f.id===id)?.name).filter(Boolean);const key=chatKey();state.chatDrafts[key]=(state.chatDrafts[key]||'')+(names.length?`\n参考资料：${names.join('、')}`:'');}back();toast(`已引用 ${state.materialSelection.length} 份演示资料。`);}
  function renderPreview(){const f=state.files.find(f=>f.id===state.args.id);if(!f){setPanel('资料预览',empty('文件不存在','请返回百宝箱。'));return;}setPanel('资料预览',`<div class="document-preview"><div class="eyebrow">${f.type} · 本地示例</div><h2>${esc(f.name)}</h2><p style="white-space:pre-wrap">${esc(f.body||'仅记录了本地文件名。为保护隐私，Demo 未读取该文件的内容，也没有上传至任何服务器。')}</p></div>`,`<span class="muted">不会下载或访问真实账户文件</span><div class="row">${button('返回','back')}${button('下载示例文本','download-file','primary',`data-id="${f.id}"`)}</div>`);}
  const docs=[{id:'guide',title:'聚义厅使用指南',sub:'工作台、事项与交办如何衔接',body:'<h3>从工作台开始</h3><p>默认进入办事概览；事项、议事、好汉和资料使用独立页面。地图保留在侧栏及概览卡片中，进入后仍为沉浸场景。</p><h3>把目标说明白</h3><p>提出需求，补充参考资料，选择交付格式，然后明确选择执行好汉，确认本次模拟交办。</p><h3>所有信息跟随事项</h3><p>在事项详情中查看进展、关联资料、继续议事。已领令不代表正在执行，查看成果不等于完成验收。</p>'},{id:'style',title:'轻量工作台设计说明',sub:'暖白底色、清晰正文、朱砂主按钮、克制的品牌字体',body:'<h3>层级更少，日常更直接</h3><p>常用功能放在工作台主页面，详情与表单才打开弹层。概览先呈现新需求入口和已有事项，不使用装饰性大屏指标。</p><h3>字体与颜色</h3><p>正文使用本机中文无衬线字体；仅品牌与首页问候使用少量宋体。常规正文 15px，辅助信息 13px，主标题 28px。朱砂表示主要操作，松绿表示正常状态，琥珀表示等待，红色表示异常，并始终配有文字。</p><h3>移动端</h3><p>底部提供概览、事项、议事与典籍阁；右上角保留全部入口。双栏卡片纵向排列，表单全屏显示，底部操作区独立保留。地图依旧可以进入。</p>'}];
  function renderArchive(){setPanel('典籍阁',`<p class="intro">说明与案卷分开查看。以下为预置演示内容，非真实账户知识库。</p><h3>厅中典籍</h3>${docs.map(d=>`<button class="doc-row" data-doc="${d.id}"><span class="grow"><strong>${d.title}</strong><small>${d.sub}</small></span>${icon('chevron-right')}</button>`).join('')}<h3 class="section-gap">我的案卷</h3>${state.tasks.filter(t=>t.archived).map(t=>`<button class="doc-row" data-task="${t.id}"><span class="grow"><strong>${esc(t.title)}</strong><small>${agentName(t.agent)} · 已收入案卷</small></span>${icon('chevron-right')}</button>`).join('')||empty('暂无案卷','可以在示例成果页体验归档。')}`);}
  function renderReader(){const doc=docs.find(d=>d.id===state.args.id)||docs[0];setPanel('典籍阁',`<article class="reader"><div class="eyebrow">聚义厅 · 演示典籍</div><h2>${doc.title}</h2>${doc.body}</article>`,`${button('返回目录','back')}<span class="muted">正文16px · 行高1.9 · 仅本地阅读</span>`);}
  function renderMessages(){setPanel('消息',`<div class="row between" style="margin-bottom:18px"><h2>需要我处理</h2>${button(state.messageRead?'已标为已读':'标记演示消息已读','read-messages','ghost')}</div><p class="intro">查看消息不等于验收、归档或完成任务；这里均为本地提示。</p><div class="notice-list">${state.tasks.filter(t=>t.status==='failed'||t.status==='draft').map(t=>`<article class="notification">${icon(t.status==='failed'?'alert-circle-outline':'file-document-outline')}<div class="grow"><h3>${esc(t.title)}</h3><p>${t.status==='failed'?'演示任务未完成，待补充资料并确认下一步。':'草稿尚未交办，可以接着填写。'}</p><button data-task="${t.id}" class="text-button">${actionLabel(t)} ${icon('chevron-right')}</button></div></article>`).join('')||empty('没有需要处理的消息','安心办事，有需要时再回来。')}</div>`);}
  function renderAccount(){setPanel('个人中心',`<div class="row" style="margin-bottom:24px">${portrait('songjiang')}<div><h2>体验账号</h2><div class="small muted">UI Demo · 非真实登录会话</div></div></div><h3 style="margin-bottom:18px">基本资料</h3><dl class="definition"><dt>昵称</dt><dd>体验账号</dd><dt>账号</dt><dd>demo-user</dd><dt>用户编号</dt><dd>仅演示</dd></dl><hr class="divider"><h3>登录与安全</h3><p class="intro" style="margin-top:10px">不接入登录服务，不修改真实资料，也不会退出任何真实设备。</p><div class="row">${openButton('查看登录页样式','login')}${openButton('样式设置','settings')}${openButton('典籍阁','archive')}${button('退出演示账号','logout','danger')}</div><div class="notice section-gap">所有示例仅存在于本页面内存中；刷新后恢复初始数据。请勿输入真实密码或敏感信息。</div>`);}
  function renderSettings(){setPanel('样式设置',`<p class="intro">根据阅读习惯微调字号与纸面。默认进入轻量工作台，地图保留独立入口。</p><label class="setting-row"><span><strong>正文风格</strong><small>优化版使用系统无衬线；传统风格用于对比。</small></span><select data-setting="font"><option value="clean" ${state.font==='clean'?'selected':''}>清晰无衬线</option><option value="serif" ${state.font==='serif'?'selected':''}>传统衬线对比</option></select></label><label class="setting-row"><span><strong>字号</strong><small>保留标题、正文和辅助信息层次。</small></span><select data-setting="size"><option value="normal" ${state.size==='normal'?'selected':''}>标准</option><option value="large" ${state.size==='large'?'selected':''}>舒适大字</option></select></label><label class="setting-row"><span><strong>纸面色温</strong><small>暖白与淡灰两种纸面，搭配朱砂主色。</small></span><select data-setting="tint"><option value="warm" ${state.tint==='warm'?'selected':''}>暖纸色</option><option value="soft" ${state.tint==='soft'?'selected':''}>淡纸色</option></select></label><label class="setting-row"><span><strong>地图场所标签</strong><small>显示或隐藏演示点击区域。</small></span><input type="checkbox" data-setting="tips" ${state.tips?'checked':''}></label><div class="notice section-gap">默认进入办事概览。侧栏、全部入口和概览卡片都能进入地图；不加载外部字体。</div>`,`<span class="muted">仅本次演示生效</span><div class="row">${button('恢复样式','reset-style')}${button('完成','close','primary')}</div>`);}
  function applySettings(){document.documentElement.style.setProperty('--font-ui',state.font==='clean'?'-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans CJK SC",sans-serif':'"Noto Serif CJK SC","Songti SC",STSong,serif');document.body.classList.toggle('large-type',state.size==='large');document.documentElement.style.setProperty('--paper',state.tint==='warm'?'#fffefa':'#ffffff');document.documentElement.style.setProperty('--paper-strong',state.tint==='warm'?'#f5f4f0':'#f1f3f4');$$('.landmark').forEach(e=>e.hidden=!state.tips);}
  function renderHelp(){setPanel('怎么开始？',`<p class="intro">这版以轻量工作台为默认首页，集中处理事项；地图作为次级入口，保留梁山场景与轻量工具栏。</p><div class="quick-grid"><button class="quick-card" data-mode="overview">${icon('format-list-checkbox')}<span>办事概览</span><small>接着上次，或提出新需求</small></button><button class="quick-card" data-open="bounty">${icon('notebook')}<span>悬赏榜</span><small>筛选榜文、查看进展</small></button><button class="quick-card" data-open="agents">${icon('account-circle-outline')}<span>点将册</span><small>查看本领，找好汉议事</small></button><button class="quick-card" data-open="files">${icon('wrench')}<span>百宝箱</span><small>选资料后回到原事项</small></button></div><hr class="divider"><div class="row">${openButton('重看新手引导','guide')}${openButton('字体与样式设置','settings')}${openButton('查看完整演示说明','archive')}</div><p class="intro section-gap" style="margin-bottom:0">地图底图是本次线上实测截图，不是游戏运行时；支持拖动、缩放、场所/好汉点击。交办、对话、资料、归档均为本地模拟，不连接线上服务。</p>`);}
  function renderGuide(){const step=state.args.step||0;const data=[['先看工作台，再接着办','默认进入办事概览。提出新需求，或者继续已有事项；需要你处理的内容会单独列出。'],['地图依旧在，随时去逛逛','从侧栏、全部入口或概览的地图卡片进入梁山。地图使用原有静态场景，可拖动、缩放及点击入口。'],['从需求到明确交办','填写需求，选择资料，然后明确指定执行好汉。最后只模拟生成事项，不进行真实执行。'],['常用功能整页，详情按需打开','事项、议事、资料与好汉拥有完整页面；表单与详情使用弹层。移动端通过底部导航切换。']][step];setPanel('新手引导',`<div class="eyebrow">第 ${step+1} 步，共 4 步</div><h2 class="brand-text" style="font-size:26px;margin:10px 0 18px">${data[0]}</h2><p class="intro">${data[1]}</p>`,`<span class="muted">不记录到真实账户</span><div class="row">${step?button('上一步','guide-prev'):button('稍后','close')}${button(step===3?'开始体验':'下一步',step===3?'close':'guide-next','primary')}</div>`);}
  function renderLogin(){setPanel('用户登录',`<div class="login-brand"><span class="brand-seal">聚</span><h2>回到聚义厅</h2><p>原有登录方式，统一品牌和字体。仅演示。</p></div><form id="login-form" class="login-form"><label class="field"><span class="field-label">用户名</span><input id="demo-login-name" autocomplete="off" placeholder="任意演示昵称" required></label><label class="field"><span class="field-label">演示密码</span><input type="password" autocomplete="off" placeholder="不要输入真实密码；可留空"></label><button class="primary" type="submit">进入演示</button><div class="row between section-gap">${button('手机登录','login-method','text-button',`data-label="手机登录"`)}${button('忘记密码','login-method','text-button',`data-label="找回密码"`)}</div><div class="login-other">第三方账号登录<div class="row">${button(icon('chat-processing-outline'),'login-method','',`data-label="微信登录" aria-label="微信登录演示"`)}${button(icon('github'),'login-method','',`data-label="GitHub 登录" aria-label="GitHub 登录演示"`)}</div></div><div class="notice">所有登录按钮仅展示交互提示，不发送用户名或密码，不连接认证服务。</div></form>`);}
  function renderRecruit(){setPanel('招贤令',`<h2>把你的 AI 帮手带入聚义厅</h2><p class="intro section-gap">这里展示招募面板的字体、表单和层级，不安装客户端、不生成真实密钥。</p><div class="quick-grid"><button class="quick-card" data-action="recruit-preview" data-label="本地客户端">${icon('cellphone')}<span>本地接入</span><small>预览客户端接入说明</small></button><button class="quick-card" data-action="recruit-preview" data-label="服务端客户端">${icon('code-json')}<span>服务端接入</span><small>预览服务端配置说明</small></button></div><div id="recruit-note" class="notice section-gap">正式招募涉及安装和授权，本 Demo 不执行此类操作。</div>`);}
  function applyAction(action,target){
    const id=target.dataset.id;
    switch(action){
      case 'close':if(state.overlay)closePanel();else navigate('overview');break;
      case 'navigation':openPanel('quick');break;
      case 'back':back();break;
      case 'overview':setMode('overview');break;
      case 'map':setMode('map');break;
      case 'sound':state.sound=!state.sound;toast(`演示声响设置：${state.sound?'开启':'关闭'}（Demo不播放音频）`);break;
      case 'reset-map':camera.zoom=1;camera.panX=0;camera.panY=0;resizeMap();toast('已回到主厅视角。');break;
      case 'orientation':toast('请将设备横过来查看全景。Demo 不强制锁定设备方向。');break;
      case 'new-demand':startDraft('private');break;
      case 'new-formal':startDraft('formal');break;
      case 'save-draft':saveDraft();break;
      case 'next-demand':{const error=draftError();if(error){$('#demand-error').textContent=error;$('#demand-error').scrollIntoView({block:'nearest'});}else openPanel('confirm',{},true);break;}
      case 'edit-demand':back();break;
      case 'submit-demand':submitDemand();break;
      case 'pick-materials':pickMaterials('draft');break;
      case 'task-materials':pickMaterials('task',id);break;
      case 'chat-materials':pickMaterials('chat');break;
      case 'use-materials':useMaterials();break;
      case 'preview-file':openPanel('preview',{id},true);break;
      case 'agent-chat':state.chatRecipient=id;state.chatTask=null;openPanel('chat',{},true);break;
      case 'agent-demand':startDraft('private',id);break;
      case 'task-chat':{const t=state.tasks.find(t=>t.id===id);state.chatRecipient=t?.agent||null;state.chatTask=id;openPanel('chat',{},true);break;}
      case 'assign-task':{const t=state.tasks.find(t=>t.id===id);state.draft={...freshDraft(),...structuredClone(t),sourceId:t.id};openPanel('confirm',{reassignId:t.id},true);break;}
      case 'view-result':openPanel('preview',{id:'f3'},true);break;
      case 'archive-task':{const t=state.tasks.find(t=>t.id===id);if(t)t.archived=true;renderTask();toast('已收入本地演示案卷，不代表实际验收。');if(state.mode==='overview')renderOverview();break;}
      case 'refresh-overview':renderOverview();toast('已刷新本地示例列表。');break;
      case 'refresh-board':renderBounty();toast('已重查本地示例榜文。');break;
      case 'chat-prompt':state.chatDrafts[chatKey()]=target.dataset.text;$('#chat-input').value=target.dataset.text;$('#chat-input').focus();break;
      case 'new-chat':state.chatTask=null;state.chatRecipient=null;renderChat();break;
      case 'chat-history':openPanel('chat-history',{},true);break;
      case 'upload-file':$('#local-file-input').click();break;
      case 'delete-file':{const f=state.files.find(f=>f.id===id);if(f)f.deleted=true;renderFiles();toast('已移入本地演示回收站；未删除原始文件。');break;}
      case 'restore-file':{const f=state.files.find(f=>f.id===id);if(f)f.deleted=false;renderFiles();toast('已恢复示例记录。');break;}
      case 'file-demand':state.draft=freshDraft();state.draft.materials=[id];openPanel('demand',{},true);break;
      case 'download-file':{const f=state.files.find(f=>f.id===id);if(!f)return;const blob=new Blob([f.body||'本Demo只记录了文件名，未读取原文件内容。'],{type:'text/plain;charset=utf-8'});const url=URL.createObjectURL(blob);const a=document.createElement('a');a.href=url;a.download=`演示-${f.name.replace(/\.[^.]+$/,'')}.txt`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);break;}
      case 'read-messages':state.messageRead=true;$$('.unread-dot').forEach(e=>e.hidden=true);renderMessages();break;
      case 'reset-style':Object.assign(state,{font:'clean',size:'normal',tint:'warm',tips:true});applySettings();renderSettings();break;
      case 'guide-next':state.args.step=Math.min(3,(state.args.step||0)+1);renderGuide();break;
      case 'guide-prev':state.args.step=Math.max(0,(state.args.step||0)-1);renderGuide();break;
      case 'logout':openPanel('login',{},true);toast('只进入登录样式演示；没有退出任何真实设备。');break;
      case 'login-method':toast(`${target.dataset.label}仅展示入口，不连接认证服务。`);break;
      case 'recruit-preview':$('#recruit-note').textContent=`${target.dataset.label}接入演示：选择好汉身份 → 配置连接参数 → 核验连通性。此处不生成密钥、不安装或启动任何客户端。`;break;
    }
  }
  document.addEventListener('click',event=>{
    const target=event.target.closest('button');if(!target||target.disabled)return;
    if(target.dataset.chatKey){const [task,agent]=target.dataset.chatKey.split(':');state.chatTask=task==='hall'?null:task;state.chatRecipient=agent==='public'?null:agent;if(state.panel==='chat-history'){back();}else renderChat();return;}
    if(target.dataset.view){if(target.dataset.view==='chat'){state.chatRecipient=null;state.chatTask=null;}navigate(target.dataset.view);return;}
    if(target.dataset.mode){setMode(target.dataset.mode);return;}
    if(target.dataset.open){if(target.dataset.open==='chat'){state.chatRecipient=null;state.chatTask=null;}openPanel(target.dataset.open,{},state.overlay);return;}
    if(target.dataset.agent){state.selectedAgent=target.dataset.agent;openPanel('agents');return;}
    if(target.dataset.selectAgent){state.selectedAgent=target.dataset.selectAgent;renderAgents();if(innerWidth<=600)$('.agent-detail')?.scrollIntoView({block:'nearest'});return;}
    if(target.dataset.overviewFilter){state.overviewFilter=target.dataset.overviewFilter;renderOverview();return;}
    if(target.dataset.bountyFilter){state.bountyFilter=target.dataset.bountyFilter;renderBounty();return;}
    if(target.dataset.rosterFilter){state.rosterFilter=target.dataset.rosterFilter;renderAgents();return;}
    if(target.dataset.fileFilter){state.fileFilter=target.dataset.fileFilter;renderFiles();return;}
    if(target.dataset.task){openTask(target.dataset.task);return;}
    if(target.dataset.doc){openPanel('reader',{id:target.dataset.doc},true);return;}
    if(target.dataset.action)applyAction(target.dataset.action,target);
  });
  document.addEventListener('input',event=>{
    const el=event.target;
    if(el.closest('#demand-form')&&['title','description','format'].includes(el.name)){state.draft[el.name]=el.value;const titleCount=$('#title-count'),descCount=$('#description-count');if(titleCount)titleCount.textContent=`${state.draft.title.length}/${state.draft.kind==='formal'?30:200}`;if(descCount)descCount.textContent=`${state.draft.description.length}/20000`;if($('#demand-error'))$('#demand-error').textContent='';}
    if(el.id==='chat-input'){state.chatDrafts[chatKey()]=el.value;$('#chat-counter').textContent=`${el.value.length}/1200 · 本地模拟，不调用 AI`;}
  });
  document.addEventListener('change',event=>{const el=event.target;
    if(el.id==='assign-agent')state.draft.agent=el.value;
    if(el.id==='task-kind'){state.taskKind=el.value;renderBounty();}
    if(el.id==='ability-filter'){state.ability=el.value;renderBounty();}
    if(el.dataset.materialId){state.materialSelection=el.checked?[...new Set([...state.materialSelection,el.dataset.materialId])]:state.materialSelection.filter(id=>id!==el.dataset.materialId);$('#material-count').textContent=`已选择 ${state.materialSelection.length} 份`;}
    if(el.dataset.setting){state[el.dataset.setting]=el.type==='checkbox'?el.checked:el.value;applySettings();}
    if(el.id==='local-file-input'){[...el.files].forEach((f,i)=>state.files.unshift({id:`local-${Date.now()}-${i}`,name:f.name,size:`${(f.size/1024).toFixed(1)} KB`,date:'本次演示',type:'资料',body:null}));renderFiles();toast('仅添加文件名到本地演示；文件内容未读取、未上传。');}
  });
  document.addEventListener('submit',event=>{event.preventDefault();if(event.target.id==='chat-form')sendChat();if(event.target.id==='task-search'){state.taskQuery=$('#task-query').value.trim();renderBounty();}if(event.target.id==='file-search'){state.fileQuery=$('#file-query').value.trim();renderFiles();}if(event.target.id==='login-form'){setMode('overview');toast('已进入演示。未发送登录信息，也未创建真实会话。');}});
  // Map camera: DOM is created once; panel changes and resizing do not remount it.
  const camera={zoom:1,panX:0,panY:0,scale:1,x:0,y:0};
  const stage=$('#map-stage'),world=$('#map-world');
  function resizeMap(){const w=stage.clientWidth,h=stage.clientHeight;camera.scale=Math.max(w/1440,h/880)*camera.zoom;const maxX=Math.max(0,(1440*camera.scale-w)/2),maxY=Math.max(0,(880*camera.scale-h)/2);camera.panX=Math.max(-maxX,Math.min(maxX,camera.panX));camera.panY=Math.max(-maxY,Math.min(maxY,camera.panY));camera.x=(w-1440*camera.scale)/2+camera.panX;camera.y=(h-880*camera.scale)/2+camera.panY;world.style.transform=`translate(${camera.x}px,${camera.y}px) scale(${camera.scale})`;}
  let drag=null;
  stage.addEventListener('pointerdown',e=>{if(e.target.closest('button'))return;drag={x:e.clientX,y:e.clientY,px:camera.panX,py:camera.panY};stage.setPointerCapture(e.pointerId);});
  stage.addEventListener('pointermove',e=>{if(!drag)return;camera.panX=drag.px+e.clientX-drag.x;camera.panY=drag.py+e.clientY-drag.y;resizeMap();});
  stage.addEventListener('pointerup',()=>drag=null);stage.addEventListener('pointercancel',()=>drag=null);
  stage.addEventListener('wheel',e=>{if(panel.open||state.mode!=='map')return;e.preventDefault();camera.zoom=Math.max(1,Math.min(2.3,camera.zoom+(e.deltaY>0?-.09:.09)));resizeMap();},{passive:false});
  stage.addEventListener('keydown',e=>{if(['+','=','-','0'].includes(e.key)){e.preventDefault();if(e.key==='0'){camera.zoom=1;camera.panX=0;camera.panY=0;}else camera.zoom=Math.max(1,Math.min(2.3,camera.zoom+(e.key==='-'?-.1:.1)));resizeMap();}const d={ArrowLeft:[35,0],ArrowRight:[-35,0],ArrowUp:[0,35],ArrowDown:[0,-35]}[e.key];if(d){e.preventDefault();camera.panX+=d[0];camera.panY+=d[1];resizeMap();}});
  addEventListener('resize',resizeMap);new ResizeObserver(resizeMap).observe(stage);
  resizeMap();applySettings();navigate('overview');
})();
