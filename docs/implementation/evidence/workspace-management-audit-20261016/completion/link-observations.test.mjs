import { strict as assert } from 'node:assert'
import { createRequire } from 'node:module'
const require=createRequire('/home/isp/wsps/cyf/web/package.json')
const {describe,it}=await import(require.resolve('mocha'))
const {ref}=await import(require.resolve('vue'))
const {usePersonalWorkspaceTaskLinks}=await import('/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspaceTaskLinks.js')
const {usePersonalWorkspaceConversationLinks}=await import('/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspaceConversationLinks.js')
for(const [kind,create] of [['task',usePersonalWorkspaceTaskLinks],['conversation',usePersonalWorkspaceConversationLinks]]){
 describe(`${kind} links supplementary diagnostic (defect reproduction, not acceptance)`,()=>{
  const link=(state='ACTIVE')=>({relationId:'audit-relation',[kind+'Id']:'audit-parent',fileId:'audit-file',version:'1',role:'INPUT',state,relationRevision:state==='ACTIVE'?'1':'2',createdAt:1})
  it('rejects an already committed attach solely because the response ETag is weak',async()=>{
   let commits=0
   const api={execute:async o=>{if(o.method==='GET')return {items:[link()],hasMore:false,nextCursor:null};commits++;const data=link();o.onSuccess?.(data,{headers:{etag:'W/"audit-relation:1"'}});return data}}
   const adapter=create({api,[kind+'Id']:ref('audit-parent'),identityEpoch:ref('owner-a')})
   try{assert.equal(await adapter.attach({fileId:'audit-file',version:'1',role:'INPUT'}),null);assert.equal(commits,1);assert.ok(adapter.error.value)}finally{adapter.dispose()}
  })
  it('rejects an already committed detach solely because the response ETag is weak',async()=>{
   let commits=0
   const api={execute:async o=>{if(o.method==='GET')return {items:[link()],hasMore:false,nextCursor:null};commits++;const data={link:link('DETACHED'),executionSnapshotsPreserved:true};o.onSuccess?.(data,{headers:{etag:'W/"audit-relation:2"'}});return data}}
   const adapter=create({api,[kind+'Id']:ref('audit-parent'),identityEpoch:ref('owner-a')})
   try{await adapter.load();assert.equal(await adapter.detach(link()),null);assert.equal(commits,1);assert.ok(adapter.error.value)}finally{adapter.dispose()}
  })
  it('creates a different key when the user retries an uncertain attach',async()=>{
   const keys=[];const api={execute:async o=>{keys.push(o.headers['Idempotency-Key']);throw new TypeError('Synthetic response lost')}}
   const adapter=create({api,[kind+'Id']:ref('audit-parent'),identityEpoch:ref('owner-a')})
   try{await adapter.attach({fileId:'audit-file',version:'1',role:'INPUT'});await adapter.attach({fileId:'audit-file',version:'1',role:'INPUT'});assert.equal(keys.length,2);assert.notEqual(keys[0],keys[1])}finally{adapter.dispose()}
  })
 })
}
