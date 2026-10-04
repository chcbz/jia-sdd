'use strict';
// Standalone, offline prototype only. No production runtime, API, Provider, or account access.
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>[...r.querySelectorAll(s)];
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const labels={home:'办事',tasks:'事项',create:'提出需求',agents:'点将册',detail:'事项详情',chat:'悬赏议事',workspace:'资料',mine:'我的'};
const catalog=[
 {id:'ref-bird',name:'小鸟图片.svg',type:'image',url:'assets/bird-v1.svg',note:'图片 · 示意插画'},
 {id:'ref-brief',name:'活动说明.md',type:'document',url:'assets/brief.md',text:'# 活动说明\n主题：自然观察\n对象：亲子家庭\n需要：一张配图、一段介绍、一份活动方案。',note:'文档'},
 {id:'ref-audio',name:'音频示例.wav',type:'audio',url:'assets/sample.wav',note:'音频 · 2 秒示意音'},
 {id:'ref-text',name:'小鸟介绍.txt',type:'text',text:'小鸟停在枝头，观察四周。保持距离，安静欣赏。',note:'文本'}
];
const state={draft:'',title:'',draftFiles:[],chatDraft:'',chatFiles:[],quote:null,task:null,agent:null,messages:[],outputs:[],archive:[],saved:[],final:[],pending:false,selectedAgent:null};
let page=labels[location.hash.slice(1)]?location.hash.slice(1):'home',view='',toastTimer,picker=null,lastFocus=null,workspaceFrom=null,serial=0,finalDraft=[];
const taskTitle=()=>state.task?.title||state.draft||'画一只鸟';
const status=()=>state.task?.complete?'已完成':state.pending?'办理中':state.outputs.length?'待验收':state.agent?'议事中':'待点将';
const asset=id=>[...catalog,...state.archive,...state.outputs].find(a=>a.id===id);
function scoped(root,key){root?.setAttribute(key,'');$$('*',root).forEach(e=>e.setAttribute(key,''));return root;}
function insert(parent,html,scope){const wrap=document.createElement('div');wrap.innerHTML=html;if(scope)scoped(wrap,scope);parent.append(...wrap.childNodes);}
function feedback(message){$('#prototype-feedback')?.remove();const n=document.createElement('div');n.id='prototype-feedback';n.role='status';n.textContent=message;document.body.append(n);clearTimeout(toastTimer);toastTimer=setTimeout(()=>n.remove(),2600);}
function syncViewport(){$$('.juyi-page').forEach(e=>e.style.setProperty('--hall-visual-height',innerHeight+'px'));}
function button(label,action,extra=''){return `<button type="button" data-action="${action}" ${extra}>${label}</button>`;}
function files(ids,context,removable=true){return `<div class="mmd mmd-attachments">${ids.map(id=>{const a=asset(id);return a?`<div class="mmd-chip"><span>${esc(a.name)}</span>${button('预览','preview',`data-id="${id}"`)}${removable?button('移除','remove',`data-id="${id}" data-context="${context}"`):''}</div>`:''}).join('')}</div>`;}
function media(a,full=false){if(a.type==='image')return `<img src="${a.url}" alt="${esc(a.name)}（原型示意插画）" data-action="preview" data-id="${a.id}">`;if(a.type==='audio')return `<audio controls preload="metadata" src="${a.url}" aria-label="${esc(a.name)}"></audio><small class="mmd-muted">2 秒示意音，非真实配音</small>`;return `<pre>${esc(full?a.text:(a.text||'可预览、下载此文件。').slice(0,220))}</pre>`;}
function result(a){return `<section class="mmd-result" data-result="${a.id}"><strong>${esc(a.name)}</strong>${media(a)}<div class="mmd-row">${button('预览','preview',`data-id="${a.id}"`)}${button('下载','download',`data-id="${a.id}"`)}${button(state.saved.includes(a.id)?'已保存':'保存到工作空间','save',`data-id="${a.id}" ${state.saved.includes(a.id)?'disabled':''}`)}${!state.task?.complete?button('引用修改','quote',`data-id="${a.id}"`):''}</div></section>`;}
function common(){
 $$('.quick-reference-open,.hall-reference-picker,.formal-task-execution').forEach(e=>e.remove());
 $$('.overview-start-copy>p').forEach(e=>e.textContent='说清想办的事，选一位好汉一起完成。也可以添加已有资料。');
 $$('.quick-material-open').forEach(e=>{delete e.dataset.prototypePage;e.textContent='添加资料（可选）';e.dataset.action='materials';e.dataset.context='draft';});
 const input=$('.overview-quick-request textarea');if(input){input.value=state.draft;input.placeholder='例如：画一只鸟，或整理一份活动方案。';const submit=$('.overview-quick-request button.primary');submit.disabled=!state.draft.trim();$('.quick-request-input small').textContent=state.draft.length+'/200';$('.quick-request-actions').insertAdjacentHTML('afterend',files(state.draftFiles,'draft'));}
 // Preserve existing sample lists. Only the first item is the interactive task.
 $$('.overview-item,.task-card').forEach((e,i)=>{if(e.matches('.overview-item')&&i!==0)return;if(e.matches('.task-card')&&e!==$('.task-card'))return;const title=$('strong,h3,h4',e);if(title)title.textContent=taskTitle();const badge=$('[class*=state],.status-badge,.overview-status',e);if(badge)badge.textContent=status();if(e.matches('.overview-item')){const desc=$('.overview-item-copy>p',e);if(desc)desc.textContent='正式事项 · '+(state.agent?.name||'待安排');}else if($(':scope>p',e))$(':scope>p',e).textContent=state.task?.description||taskTitle();});
 $$('.task-create-actions').forEach(group=>{const first=$('button',group);if(!first)return;$$('button',group).slice(1).forEach(e=>e.remove());first.textContent='提出需求';first.dataset.prototypePage='create';});
 $$('.task-data-state').forEach(e=>e.remove());
 $$('.task-status-tabs button').forEach(e=>{if(e.textContent.includes('待开工'))e.firstChild.textContent='议事中 ';});
 $$('form').forEach(f=>f.addEventListener('submit',onSubmit));
}
function render(){
 view=innerWidth<=900?'mobile':'desktop';const snap=window.BASELINE_SNAPSHOTS[view+'-'+page]||window.BASELINE_SNAPSHOTS[view+'-home'];
 document.body.innerHTML=snap.html.replaceAll('./juyiting-portraits/','../current/juyiting-portraits/').replaceAll('./static/','../current/static/');
 document.body.className=snap.bodyClass;document.documentElement.className=snap.htmlClass;document.title=labels[page]+' · 调整版原型（离线示例）';syncViewport();common();
 if(page==='create')renderCreate();if(page==='agents')renderAgents();if(page==='detail'||page==='chat')renderDetail();if(page==='chat')renderChat();if(page==='workspace')renderWorkspace();
}
function go(next){if(!labels[next])return;page=next;history.replaceState(null,'','#'+page);render();}
function renderCreate(){const form=$('.task-create-form');if(!form)return;$('[name=taskTitle]',form).value=state.title;$('[name=taskTitle]',form).placeholder='需求名称（可选）';$('[name=taskDescription]',form).value=state.draft;const desc=$('[name=taskDescription]',form);desc.placeholder='想完成什么？';$('button[type=submit]',form).textContent='提交需求';desc.insertAdjacentHTML('afterend',`<div class="mmd">${button('添加资料（可选）','materials','data-context="draft"')}${files(state.draftFiles,'draft')}</div>`);$('button[type=submit]',form).disabled=!state.draft.trim();}
function renderAgents(){const panel=$('.agent-panel');if(!panel)return;$$('.agent-row',panel).forEach((row,i)=>{row.dataset.action='choose-agent';row.dataset.agent=String(i);row.setAttribute('aria-pressed',state.selectedAgent?.id===String(i));});const detail=$('.detail-card',panel);detail.classList.add('mmd','mmd-agent-detail');const selected=state.selectedAgent;const row=selected?$('.agent-row[data-agent="'+selected.id+'"]',panel):null;detail.innerHTML=selected?`<h3>${esc(selected.name)}</h3><p>${esc($('small',row)?.textContent||'')}</p><p class="mmd-muted">${esc($('em',row)?.textContent||'')}</p>${button('点将并议事','assign','class="mmd-primary"')}`:'<p>点一位好汉，查看本领并选择承办人。</p>';}
function renderDetail(){const card=$('.matter-advice-card');if(card){$('.matter-advice-heading span',card).textContent='事项进展';$('.matter-advice-heading strong',card).textContent=status();$('.matter-request',card).textContent=state.task?.description||taskTitle();$('dl',card).innerHTML=`<div><dt>承办好汉</dt><dd>${esc(state.agent?.name||'尚未点将')}</dd></div><div><dt>资料</dt><dd>${state.task?.files.length||0} 份</dd></div>`;scoped($('dl',card),'data-v-9209fea5');$('.matter-fee-note',card)?.remove();const b=$('.matter-primary-action',card);b.textContent=state.agent?'继续议事':'去点将';b.dataset.prototypePage=state.agent?'chat':'agents';}
 const materials=$('.task-material-links');if(materials){materials.innerHTML=`<div class="mmd"><h4>资料与成果</h4>${files(state.task?.files||[],'task',false)}<p class="mmd-muted">${state.outputs.length?`已有 ${state.outputs.length} 份成果，可在议事中查看。`:'尚无成果，可在议事中继续补充需求和资料。'}</p></div>`;}
 const b=$('.matter-results-action');if(b){b.textContent=state.task?.complete?'查看验收结果':'查看正式成果与验收';b.dataset.action='accept';}
}
function renderChat(){
 const panel=$('.chat-panel');if(!panel)return;$$('.mmd-composer-extra',panel).forEach(e=>e.remove());
 $$('.context-summary strong,.discussion-brief strong').forEach(e=>e.textContent='悬赏议事');$$('.context-summary small,.discussion-brief small').forEach(e=>e.textContent=taskTitle()+' / '+(state.agent?.name||'公孙胜'));const em=$('.context-summary em');if(em)em.textContent=status();
 $('.toolbar-actions',panel)?.remove();
 const messages=$('.hall-messages');messages.setAttribute('aria-live','polite');messages.innerHTML=state.messages.map((m,index)=>`<div class="hall-message ${m.role}"><div class="message-head"><strong>${m.role==='USER'?'你':esc(state.agent?.name||'好汉')}</strong></div><div class="message-content"><p>${esc(m.text)}</p></div>${m.quote?`<div class="mmd mmd-quote">引用：${esc(asset(m.quote)?.name)}</div>`:''}${files(m.files||[],'message',false)}<details data-v-4c0df501 class="text-selection-archive"><summary data-v-4c0df501>保存文字片段</summary><label data-v-4c0df501>要保存的文字<textarea data-v-4c0df501 data-message-text="${index}" rows="3">${esc(m.text)}</textarea></label><button data-v-4c0df501 type="button" data-action="save-text" data-message="${index}">保存到工作空间</button></details>${m.outputs?.length?`<div class="mmd mmd-results">${m.outputs.map(id=>result(asset(id))).join('')}</div>`:''}</div>`).join('')+(state.pending?'<p class="mmd-pending" role="status">正在回复…</p>':'');scoped(messages,'data-v-8f1da78a');
 if(!state.messages.length)insert(messages,'<p class="mmd-pending">请先提出需求并点将，需求和资料将自动带入这里。</p>');
 const input=$('.composer-textarea');input.disabled=!!state.task?.complete;input.value=state.chatDraft;input.placeholder=state.task?.complete?'事项已完成':'补充需求，或告诉好汉哪里需要调整…';
 $$('.composer-context,.composer-meta,.hall-voice-controls',panel).forEach(e=>e.remove());input.rows=2;input.style.height='';
 $('.composer-execute')?.remove();const send=$('.composer-send');send.innerHTML='发送';send.ariaLabel='发送';send.title='发送';send.disabled=state.pending||!!state.task?.complete||(!state.chatDraft.trim()&&!state.chatFiles.length)||!state.agent;
 const form=$('.composer-submit'),body=$('.composer-body');$$('.composer-more',panel).forEach(e=>e.remove());
 const extra=document.createElement('div');extra.className='mmd mmd-composer-extra';extra.innerHTML=`${state.quote?`<div class="mmd-quote">引用：${esc(asset(state.quote)?.name)} ${button('取消引用','unquote')}</div>`:''}${files(state.chatFiles,'chat')}`;if(state.quote||state.chatFiles.length)body.prepend(extra);
 const more=document.createElement('button');more.type='button';more.className='composer-more';more.dataset.action='composer-more';more.textContent='＋';more.ariaLabel='添加资料、语音输入与设置';more.title='添加资料、语音输入与设置';more.disabled=!!state.task?.complete;$('.composer-actions').prepend(more);
 const scrollEnd=()=>{if(messages.isConnected)messages.scrollTop=messages.scrollHeight;};requestAnimationFrame(scrollEnd);$$('img',messages).forEach(img=>img.addEventListener('load',scrollEnd,{once:true}));
}
function renderWorkspace(){const list=$('.treasure-file-list');if(!list)return;const items=[...catalog,...state.saved.map(asset)];list.innerHTML=items.map(a=>`<div class="treasure-file-row"><div><strong>${esc(a.name)}</strong><p>${catalog.includes(a)?'已有资料':'从议事保存的成果'} · ${esc(a.note||({image:'图片',audio:'音频',document:'文档',text:'文本'}[a.type]))}</p></div><button type="button" data-action="preview" data-id="${a.id}">查看</button></div>`).join('');scoped(list,'data-v-a1bd66a6');if(workspaceFrom)list.insertAdjacentHTML('beforebegin',`<div class="mmd mmd-workspace-back">${button('← 返回议事','back-chat')}</div>`);}
function submitRequest(){if(!state.draft.trim())return;state.task={title:state.title.trim()||state.draft.trim().slice(0,36),description:state.draft.trim(),files:[...state.draftFiles],complete:false};state.agent=null;state.messages=[];state.outputs=[];state.final=[];state.selectedAgent=null;state.chatDraft='';state.chatFiles=[];state.quote=null;go('agents');}
function assign(){if(!state.selectedAgent)return;if(!state.task){state.task={title:taskTitle(),description:state.draft||taskTitle(),files:[...state.draftFiles],complete:false};}state.agent={...state.selectedAgent};state.messages=[{role:'USER',text:state.task.description,files:[...state.task.files]}];go('chat');reply(state.task.description,true);}
function output(type,text,revision){const id='result-'+(++serial);const a={id,type,name:'',text,note:'第 '+revision+' 稿'};if(type==='image'){a.name=`小鸟-第${revision}稿.svg`;a.url=revision===1?'assets/bird-v1.svg':'assets/bird-v2.svg';}else if(type==='audio'){a.name=`音频-第${revision}稿.wav`;a.url='assets/sample.wav';}else if(type==='document'){a.name=`活动方案-第${revision}稿.md`;a.url='assets/plan.md';a.text='# 自然观察活动方案\n\n目标：认识身边的鸟类，记录观察结果。\n\n1. 介绍观察方法。\n2. 分组观察并记录。\n3. 分享发现，整理成果。\n\n保持距离，不打扰动物。';}else a.name=`文字成果-第${revision}稿.txt`;state.outputs.push(a);return id;}
function reply(text,first=false){
 state.pending=true;if(page==='chat')renderChat();const task=state.task;
 setTimeout(()=>{if(state.task!==task)return;const revision=state.messages.filter(m=>m.outputs?.length).length+1;let ids=[],answer;
 if(first&&(/^(帮我|做一下|处理一下|优化一下|改一下|看看)[。！!\s]*$/.test(text.trim())||text.trim().length<3)){answer='你希望完成什么内容？可以补充用途或想要的结果，也可以添加一份资料。';}
 else {const history=state.messages.filter(m=>m.role==='USER').map(m=>m.text).join(' ');const image=asset(state.messages.at(-1)?.quote)?.type==='image'||/画|图片|小鸟|照片|配图|插画/.test(text)||(!/音频|配音|文档|方案|文字|介绍/.test(text)&&/画|图片|小鸟|照片/.test(history));const audio=/音频|配音|声音/.test(text),doc=/方案|文档|文件|纪要/.test(text);if(image)ids.push(output('image','',revision));if(audio)ids.push(output('audio','',revision));if(doc)ids.push(output('document','',revision));if(!ids.length||/文字|介绍|说明/.test(text))ids.push(output('text','小鸟停在枝头，轻轻侧头，望向远处。愿你在忙碌中，也留意身边这些小小的美好。\n\n（原型示例文字，可作为独立成果验收。）',revision));answer=first?'先给你这一版，看看是否符合你的想法。':'已按补充内容整理了新一稿，上一稿仍保留在会话中。';}
 state.messages.push({role:'AGENT',text:answer,outputs:ids});state.pending=false;if(page==='chat')renderChat();else if(page==='detail')renderDetail();
 },650);
}
function send(){if(state.pending||state.task?.complete||!state.agent||(!state.chatDraft.trim()&&!state.chatFiles.length))return;const text=state.chatDraft.trim();state.messages.push({role:'USER',text:text||'请结合这些资料继续。',files:[...state.chatFiles],quote:state.quote});state.task.files=[...new Set([...state.task.files,...state.chatFiles])];state.chatFiles=[];state.chatDraft='';state.quote=null;reply(text||'请结合这些资料继续。');}
function dialog(title,html,footer=''){const d=document.createElement('dialog');d.className='mmd mmd-dialog';d.setAttribute('aria-label',title);d.innerHTML=`<header><h3>${esc(title)}</h3>${button('关闭','close-dialog','aria-label="关闭窗口"')}</header>${html}${footer?'<footer>'+footer+'</footer>':''}`;document.body.append(d);lastFocus=document.activeElement;d.addEventListener('close',()=>{d.remove();if(lastFocus?.isConnected)lastFocus.focus();});d.showModal();return d;}
function openMaterials(context){const ids=context==='chat'?state.chatFiles:state.draftFiles;picker={context,ids:[...ids]};const all=[...catalog,...state.saved.map(asset)];dialog('添加资料（可选）',`<p class="mmd-muted">从工作空间选择图片、文档或音频，也可以不选。</p><div class="mmd-files">${all.map(a=>`<div class="mmd-file-option"><input type="checkbox" id="pick-${a.id}" data-pick="${a.id}" ${ids.includes(a.id)?'checked':''}><label for="pick-${a.id}"><strong>${esc(a.name)}</strong><br><small>${esc(a.note||a.type)}</small></label>${button('预览','preview',`data-id="${a.id}"`)}</div>`).join('')}</div>`,button('取消','close-dialog')+button('确定（'+ids.length+'）','confirm-materials','class="mmd-primary"'));}
function preview(id){const a=asset(id);if(!a)return;dialog(a.name,`<div class="mmd-preview">${media(a,true)}<p class="mmd-muted">${a.type==='image'?'原型示意插画，非真实 Agent 生成照片。':'离线示例内容。'}</p></div>`,button('下载','download',`data-id="${id}"`));}
function download(id){const a=asset(id);if(!a)return;let url=a.url,blob=false;if(!url){url=URL.createObjectURL(new Blob([a.text||''],{type:'text/plain;charset=utf-8'}));blob=true;}const link=document.createElement('a');link.href=url;link.download=a.name;document.body.append(link);link.click();link.remove();if(blob)setTimeout(()=>URL.revokeObjectURL(url),2000);}
function deliveryList(){return finalDraft.map(id=>{const a=asset(id);return a?`<div class="mmd-chip"><span><strong>${esc(a.name)}</strong><br><small>${esc(a.note)}</small></span>${button('预览','preview',`data-id="${id}"`)}</div>`:''}).join('')||'<p class="mmd-muted">尚未选定交付内容。</p>';}
function accept(){const done=state.task?.complete;finalDraft=done?[...state.final]:[...([...state.messages].reverse().find(m=>m.role==='AGENT'&&m.outputs?.length)?.outputs||[])];dialog(done?'验收结果':'验收成果',`<p>${done?'事项已完成，最终成果如下。':'请查看本次交付内容，满意后确认验收。无需先保存到工作空间。'}</p><div class="mmd-attachments" data-delivery-list>${deliveryList()}</div>${!done&&state.outputs.length?`<details class="mmd-final-adjust"><summary>调整交付内容</summary><p class="mmd-muted">只有需要更换稿次或增减成果时才调整；未选的旧稿不会计入本次验收。</p><div class="mmd-selection">${state.outputs.map(a=>`<label><input type="checkbox" data-final="${a.id}" ${finalDraft.includes(a.id)?'checked':''}><span><strong>${esc(a.name)}</strong><small>${esc(a.note)}</small></span>${button('预览','preview',`data-id="${a.id}"`)}</label>`).join('')}</div></details>`:''}`,done?button('关闭','close-dialog'):button('继续修改','continue-chat')+button('确认验收并完成','finish',`class="mmd-primary" ${finalDraft.length?'':'disabled'}`));}
function onSubmit(e){e.preventDefault();if(e.target.matches('.overview-quick-request,.task-create-form'))submitRequest();else if(e.target.matches('.composer-submit'))send();else feedback('原型保留原有入口，本次只演示需求协作流程。');}
document.addEventListener('input',e=>{const t=e.target;if(t.matches('.overview-quick-request textarea')){state.draft=t.value;$('.quick-request-input small').textContent=t.value.length+'/200';$('.overview-quick-request button.primary').disabled=!t.value.trim();}if(t.name==='taskDescription'){state.draft=t.value;$('.task-create-form button[type=submit]').disabled=!t.value.trim();}if(t.name==='taskTitle')state.title=t.value;if(t.matches('.composer-textarea')){state.chatDraft=t.value;$('.composer-send').disabled=state.pending||(!t.value.trim()&&!state.chatFiles.length)||!state.agent;}});
document.addEventListener('change',e=>{const t=e.target;if(t.dataset.pick){picker.ids=t.checked?[...new Set([...picker.ids,t.dataset.pick])]:picker.ids.filter(id=>id!==t.dataset.pick);$('[data-action=confirm-materials]').textContent='确定（'+picker.ids.length+'）';}if(t.dataset.final){finalDraft=t.checked?[...new Set([...finalDraft,t.dataset.final])]:finalDraft.filter(id=>id!==t.dataset.final);$('[data-action=finish]').disabled=!finalDraft.length;$('[data-delivery-list]').innerHTML=deliveryList();}});
document.addEventListener('click',e=>{
 const t=e.target.closest('[data-action],button,a,[data-prototype-page]');if(!t||t.disabled||t.matches('a[download]'))return;
 if(t.type==='submit'&&t.closest('form'))return;e.preventDefault();const action=t.dataset.action,id=t.dataset.id;
 if(action==='composer-more'){dialog('更多',`<div class="mmd-more-menu">${button('添加资料','composer-materials')}${button('语音输入','voice-demo')}${button('语音设置','voice-demo')}</div>`);return;}
 if(action==='composer-materials'){t.closest('dialog').close();openMaterials('chat');return;}
 if(action==='voice-demo'){t.closest('dialog').close();feedback('语音入口演示，本原型不启用麦克风。');return;}
 if(action==='materials'){openMaterials(t.dataset.context);return;}
 if(action==='confirm-materials'){if(picker.context==='chat')state.chatFiles=[...picker.ids];else state.draftFiles=[...picker.ids];t.closest('dialog').close();render();return;}
 if(action==='close-dialog'){t.closest('dialog').close();return;}
 if(action==='preview'){if(!t.closest('.mmd-preview'))preview(id);return;}
 if(action==='download'){download(id);return;}
 if(action==='remove'){const key=t.dataset.context==='chat'?'chatFiles':'draftFiles';state[key]=state[key].filter(x=>x!==id);render();return;}
 if(action==='choose-agent'){state.selectedAgent={id:t.dataset.agent,name:$('strong',t).textContent};renderAgents();return;}
 if(action==='assign'){assign();return;}
 if(action==='save-text'){const text=$('[data-message-text="'+t.dataset.message+'"]').value.trim();if(!text){feedback('先选好要保存的文字');return;}const a={id:'saved-text-'+(++serial),name:'议事文字片段-'+serial+'.txt',type:'text',text,note:'议事文字'};state.archive.push(a);state.saved.push(a.id);feedback('文字片段已保存到工作空间');return;}
 if(action==='save'){if(!state.saved.includes(id)){state.saved.push(id);state.archive.push({...asset(id)});}t.disabled=true;t.textContent='已保存';feedback('已保存到工作空间');return;}
 if(action==='quote'){state.quote=id;state.chatDraft='请把这一稿';renderChat();$('.composer-textarea').focus();return;}
 if(action==='unquote'){state.quote=null;renderChat();return;}
 if(action==='workspace'){workspaceFrom='chat';go('workspace');return;}
 if(action==='back-chat'){go('chat');return;}
 if(action==='task-files'){dialog('事项资料',state.task?.files.length?files(state.task.files,'task',false):'<p>暂无资料，可以继续议事，无需添加。</p>');return;}
 if(action==='accept'){accept();return;}
 if(action==='continue-chat'){go(state.agent?'chat':'agents');return;}
 if(action==='finish'){if(!finalDraft.length||!state.task)return;state.final=[...finalDraft];state.task.complete=true;go('detail');feedback('验收完成，事项已完成');return;}
 if(t.dataset.prototypePage){if(t.dataset.prototypePage==='materials')openMaterials('draft');else if(t.dataset.prototypePage==='workspace'){workspaceFrom=page==='chat'?'chat':null;go('workspace');}else go(t.dataset.prototypePage);return;}
 if(t.matches('.workbench-mobile-more')){dialog('更多',`<div class="mmd-row">${button('点将册','go-agents')}${button('提出需求','go-create')}</div>`);return;}
 if(action==='go-agents'){go('agents');return;}if(action==='go-create'){go('create');return;}
 if(t.matches('.voice-start,.voice-settings-trigger')){feedback('此原型不启用麦克风，语音入口保持原样。');return;}
 feedback('保留现有入口；本次原型只演示需求、资料、议事与验收。');
});
window.addEventListener('hashchange',()=>{if(labels[location.hash.slice(1)]){page=location.hash.slice(1);render();}});
window.addEventListener('resize',()=>{if(view!==(innerWidth<=900?'mobile':'desktop'))render();else syncViewport();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('dialog[open]')&&page==='chat')go('detail');});
render();
