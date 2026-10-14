import { createRequire } from 'node:module'
const worktree=process.env.WEB_TYPED_WT||'/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/web-typed-natural-followup-owner-v1-20261001'
const require=createRequire(`${worktree}/package.json`);const {ref}=require('vue')
const {useHallTypedDeliberation}=await import(`${worktree}/src/composables/juyiting/useHallTypedDeliberation.js`)
Object.defineProperty(globalThis,'crypto',{value:{randomUUID:()=>'00000000-0000-4000-8000-000000000101'},configurable:true})
const data=new Map();const lane=useHallTypedDeliberation({chatApi:{create:async()=>{throw new Error('ack lost')}},actorScopeKey:ref('owner'),authorizationGeneration:ref(1),getContext:()=>({conversationId:'7',conversationGeneration:'1',taskId:'task-1',targetAgentId:'agent-1',assignmentRevision:'4'}),getContextGeneration:()=>1,getCatalogEntries:()=>[],enabled:()=>true,storage:{getItem:k=>data.get(k)||null,setItem:(k,v)=>data.set(k,v)}})
const before=lane.recoveryAvailable.value;const submitted=await lane.submit({content:'请继续讨论。'});const after=lane.recoveryAvailable.value;lane.dispose()
console.log(JSON.stringify({worktree,before,submitted,after,expectedAfter:true,pass:before===false&&submitted===false&&after===true,scope:'real computed read before submit simulates first template render, then actual POST ack loss and local persistence; no Provider/API'},null,2));process.exitCode=after===true?0:1
