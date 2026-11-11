import fs from 'node:fs'
import {createRequire} from 'node:module'
const root='/home/isp/wsps/worktrees/discussion-material-unified-web-20261027'
const require=createRequire(root+'/package.json')
const {parse,compileScript,compileStyle}=require('@vue/compiler-sfc')
const out='/tmp/cyf-discussion-material-dev-20261027'
let css='',code=''
for(const name of ['HallChatComposer','HallMaterialPicker','HallMaterialThumbnail','ChatPanel']){
 const {descriptor}=parse(fs.readFileSync(`${root}/src/components/juyiting/${name}.vue`,'utf8'))
 const id=`data-v-${name}`
 const compiled=compileScript(descriptor,{id,inlineTemplate:true}).content
  .replace(/^import\s+\{([^}]+)\}\s+from\s+['"]vue['"];?\s*$/gm,(_,names)=>`const {${names.replace(/\s+as\s+/g,': ')}}=Vue`)
  .replace(/^import\s+\{([^}]+)\}\s+from\s+['"][^'"]+['"];?\s*$/gm,(_,names)=>`const {${names}}=deps`)
  .replace(/^import\s+(\w+)\s+from\s+['"][^'"]+['"];?\s*$/gm,(_,name)=>`const ${name}=deps.${name}`)
  .replace('export default','return')
 code+=`deps.${name}=new Function('Vue','deps',${JSON.stringify(compiled)})(Vue,deps);deps.${name}.__scopeId=${JSON.stringify(id)};\n`
 for(const style of descriptor.styles) css+=compileStyle({id,source:style.content,scoped:style.scoped}).code+'\n'
}
const setup=`const {ref,watch}=Vue;
const files=Array.from({length:6},(_,i)=>({fileId:'file-'+i,latestVersion:'1',state:'ACTIVE',displayName:i%2?'需求说明-'+i+'.txt':'参考图片-'+i+'.png'}));
const blank={render:()=>null};
const workspace=()=>{const state={items:ref(files),detail:ref(null),preview:ref({kind:'none'}),pendingWrites:ref([]),listState:ref('ready'),nextCursor:ref(null),loading:ref(false),error:ref(''),writeNotice:ref(''),actionState:ref('idle'),refresh:async()=>true,closeDetail(){state.preview.value={kind:'none'}},dispose(){},select:async id=>{const file=files.find(x=>x.fileId===id);state.detail.value={file,latestVersion:{version:'1'},versions:[{fileId:id,version:'1',contentMimeType:file.displayName.endsWith('.png')?'image/png':'text/plain'}]};return state.detail.value},previewVersion:async()=>{state.preview.value={kind:'text',text:'浏览器组件夹具：不访问真实业务数据。'}}};return state};
const directory=()=>{const links=ref(files.map((file,i)=>({relationId:'link-'+i,fileId:file.fileId,version:'1',role:'REFERENCE',state:'ACTIVE'})));return {...workspace(),links,load:async()=>true,detach:async link=>{links.value=links.value.filter(x=>x.relationId!==link.relationId);return true},attach:async material=>{const link={...material,relationId:'new-'+material.fileId,state:'ACTIVE'};links.value.push(link);return link}}};
const deps={usePersonalWorkspace:workspace,usePersonalWorkspaceConversationLinks:directory,usePersonalWorkspaceTaskLinks:directory,validMaterialVersion:v=>/^\\d+$/.test(v),marked:Object.assign(x=>x,{setOptions(){}}),DOMPurify:{sanitize:x=>x},discussionTurns:()=>[],discussionDeliveryText:()=>'',discussionTurnStatus:()=>'',HallMessageParts:blank,BountyTextSelectionArchive:blank,BountyTypedOutcomeCard:blank,WorkspaceWriteRecovery:blank,HallConversationHistory:blank,PdfDocumentPreview:blank,HallVoiceControls:{props:['recordingTarget'],template:'<Teleport v-if="recordingTarget" :to="recordingTarget"><button type="button" aria-label="语音输入">🎙</button></Teleport>'}};
`
fs.copyFileSync(require.resolve('vue/dist/vue.global.js'),out+'/vue.js')
fs.writeFileSync(out+'/index.html',`<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width,initial-scale=1"><meta charset="utf-8"><style>html,body,#app{margin:0;height:100%;font-family:Arial,sans-serif}*{box-sizing:border-box}.discussion-surface{height:100%;display:flex;flex-direction:column;max-width:1100px;margin:auto}${css}</style></head><body><div id="app"></div><script src="vue.js"></script><script>${setup}\n${code}\nconst variant=new URLSearchParams(location.search).get('variant')||'public';Vue.createApp({render:()=>Vue.h(deps.ChatPanel,{class:'discussion-surface',discussionVariant:variant,conversationId:'thread-fixture',identityScope:'fixture-only',selectedTask:{id:'task-fixture'},draft:'请结合资料继续讨论',mentionLabel:()=>'',senderText:()=>''})}).component('var-icon',{template:'<span aria-hidden="true">◇</span>'}).mount('#app');</script></body></html>`)
