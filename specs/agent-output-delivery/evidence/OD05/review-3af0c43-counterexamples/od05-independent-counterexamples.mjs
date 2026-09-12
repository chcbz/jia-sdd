import * as Vue from '/home/chc/wsps/cyf-worktrees/output-web/node_modules/vue/index.mjs'
import { mount } from '/home/chc/wsps/cyf-worktrees/output-web/node_modules/@vue/test-utils/dist/vue-test-utils.cjs.js'
import { compileScript, parse } from '/home/chc/wsps/cyf-worktrees/output-web/node_modules/@vue/compiler-sfc/dist/compiler-sfc.cjs.js'
import { readFileSync } from 'node:fs'
import { useOutputs, parseOutputResourceQuery } from '/home/chc/wsps/cyf-worktrees/output-web/src/composables/useOutputs.js'
const { ref, computed, nextTick, defineComponent, h } = Vue
for (const key of ['SVGElement', 'Element', 'Node']) globalThis[key] ||= window[key]
const flush = async () => { for (let i=0;i<12;i++){await Promise.resolve();await nextTick()} }
const sourceData={type:'CONVERSATION',id:'conv-a'}
const item=(id='report',version='1')=>({source:sourceData,outputId:id,version,title:`${id} v${version}`,previewKind:'NONE',state:'AVAILABLE',canDownload:true,publicationKind:'CONVERSATION_OUTPUT'})
const page=items=>({data:{code:'E0',data:{items,nextCursor:null,snapshotAt:'100'}}})
const harness=(source,options,component)=>{let outputs;const wrapper=mount(defineComponent({setup(){outputs=useOutputs(source,options);return()=>h(component||'div',component?{outputs}:null)}}));return{outputs,wrapper}}
{
 const source=ref(sourceData),syncing=ref(true), tasks=[]
 const timer={setTimeout(callback,delay){tasks.push({callback,delay});return tasks.length},clearTimeout(){}}
 const {outputs,wrapper}=harness(source,{syncing,timer,document:{hidden:false},http:{get:async()=>{throw Object.assign(new Error('revoked'),{status:403,retryable:false})}}})
 await flush();console.log('EXPLICIT_NONRETRYABLE_WHILE_SYNCING',JSON.stringify({error:outputs.error.value,scheduledDelays:tasks.map(x=>x.delay)}));wrapper.unmount()
}
{
 const source=ref(sourceData);let removed=false
 const {outputs,wrapper}=harness(source,{http:{get:async()=>page(removed?[]:[item('revoked-secret')])}})
 await flush();removed=true;await outputs.refresh();console.log('EMPTY_AUTHORITATIVE_REFRESH',JSON.stringify({items:outputs.items.value.map(x=>x.title),nextCursor:outputs.nextCursor.value}));wrapper.unmount()
}
const compile=(file,replacements=[])=>{
 const filename='/home/chc/wsps/cyf-worktrees/output-web/src/components/outputs/'+file+'.vue'
 let body=compileScript(parse(readFileSync(filename,'utf8'),{filename}).descriptor,{id:file,inlineTemplate:true}).content.replace(/^import\s+\{([^}]+)\}\s+from\s+['"]vue['"];?\s*$/gm,(_,names)=>'var {'+names.split(',').map(x=>x.trim().replace(/\s+as\s+/,': ')).join(',')+'} = Vue')
 for(const [pattern,replacement] of replacements)body=body.replace(pattern,replacement)
 return new Function('Vue',...replacements.map((_,i)=>'dep'+i),body.replace('export default','return'))(Vue,...replacements.map(x=>x[2]))
}
const Card=compile('OutputCard'),Preview=compile('OutputPreview')
const List=compile('OutputList',[[/^import\s+OutputCard.*$/gm,'var OutputCard = dep0',Card],[/^import\s+OutputPreview.*$/gm,'var OutputPreview = dep1',Preview],[/^import\s+\{\s*parseOutputResourceQuery\s*\}\s+from.*$/gm,'var parseOutputResourceQuery = dep2',parseOutputResourceQuery]])
{
 const query=ref({outputSourceType:'CONVERSATION',outputSourceId:'conv-a',outputId:'report',outputVersion:'1'})
 const route=()=>'/chat?'+new URLSearchParams(query.value)
 window.history.replaceState({},'',route())
 const request=computed(()=>parseOutputResourceQuery(query.value)),source=computed(()=>request.value.source),calls=[]
 const {wrapper}=harness(source,{http:{get:async(url)=>{calls.push(url);return url.endsWith('/outputs')?page([]):{data:{data:{item:item('report',url.split('/').at(-1))}}}}}},List)
 await flush();query.value={...query.value,outputVersion:'2'};window.history.replaceState({},'',route());await flush()
 console.log('SAME_COMPONENT_RESOURCE_NAVIGATION',JSON.stringify({currentUrl:window.location.href,calls,rendered:wrapper.text()}));wrapper.unmount()
}
{
 const source=ref(sourceData);let resolveA,resolveB
 const {outputs,wrapper}=harness(source,{http:{get:async(url)=>url.endsWith('/outputs')?page([]):url.includes('/a/')?new Promise(r=>resolveA=r):new Promise(r=>resolveB=r)}})
 await flush();const pa=outputs.loadVersions(item('a'));await flush();outputs.clearVersions();const pb=outputs.loadVersions(item('b'));await flush();resolveA(page([item('a')]));await pa
 console.log('CANCELLED_VERSION_RESPONSE',JSON.stringify({target:outputs.versionTarget.value.outputId,rows:outputs.versions.value.map(x=>x.outputId),versionsLoading:outputs.versionsLoading.value}));resolveB(page([item('b')]));await pb;wrapper.unmount()
}
{
 const {useHttp}=await import('/home/chc/wsps/cyf-worktrees/output-web/src/composables/useHttp.js')
 const {stopIdentityBoundWork}=await import('/home/chc/wsps/cyf-worktrees/output-web/src/utils/identityLifecycle.js')
 const source=ref(sourceData),events=[]
 globalThis.URL.createObjectURL=()=>{events.push('create-old-blob-url');return 'blob:old-identity'}
 globalThis.URL.revokeObjectURL=()=>{}
 document.addEventListener('click',event=>{if(event.target.tagName==='A'){events.push('save-old-identity-file');event.preventDefault()}},true)
 globalThis.fetch=async url=>{
  if(!url.endsWith('/download'))return new Response(JSON.stringify(page([]).data),{status:200})
  const response=new Response('old-identity-secret',{status:200})
  response.blob=async()=>{
   queueMicrotask(()=>queueMicrotask(()=>{events.push('identity-cleared');stopIdentityBoundWork()}))
   return new Blob(['old-identity-secret'])
  }
  return response
 }
 const {outputs,wrapper}=harness(source,{http:{get:(url,params,config)=>useHttp().get(url,params,{...config,authStore:{token:async()=>"counterexample-test-token",authorizationGeneration:1}})}});await flush()
 const failure=await outputs.download(item()).catch(e=>e)
 console.log('REAL_HTTP_DOWNLOAD_SAVE_AFTER_IDENTITY_CLEAR',JSON.stringify({events,result:failure?.name,message:failure?.message}));wrapper.unmount()
}
