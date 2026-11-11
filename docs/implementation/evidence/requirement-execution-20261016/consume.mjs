import { readFileSync } from 'node:fs';
import {pollWorkspaceFileCommands, AgentMessageProcessor} from '/home/isp/apps/cyf-agent-runtime-v1/releases/runtime-interface-20261015-1.2.7-6a9d8d3/codex-ws-agent/agent-client.mjs';
const item=JSON.parse(readFileSync(new URL('./queue.json', import.meta.url)));
const profile={agentId:'agent',runtimeIdentity:{installationId:'rti_test',tenantId:'tenant',clientId:'client',canonicalAgentId:'agent'}};
for (const real of [false,true]) {
 const errors=[]; const processor=real?new AgentMessageProcessor({profile,onReject:e=>errors.push(e.code)}):{handle:async()=>{},onReject:e=>errors.push(e.code)};
 const state={workspaceFileBridge:{apiOrigin:'https://api.example.test'},workspaceFileRuntimeAuthHeader:`AgentRuntime rts1_${'f'.repeat(64)}`,processor};
 const result=await pollWorkspaceFileCommands({profile,state,fetchFn:async url=>{const r=new Response(JSON.stringify({protocolVersion:1,requestId:'fixture',code:'E0',msg:'ok',data:{items:[item]}}),{headers:{'Content-Type':'application/json','X-Request-Id':'fixture'}});Object.defineProperty(r,'url',{value:String(url)});return r}});
 console.log(JSON.stringify({realProcessor:real,result,errors}));
}
