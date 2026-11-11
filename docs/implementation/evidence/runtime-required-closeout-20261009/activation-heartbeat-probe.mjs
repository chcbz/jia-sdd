// Local synthetic reproduction only: no HTTP, WS, provider, service or production state.
import { mkdtemp, mkdir, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import assert from 'node:assert/strict';
import { runUnifiedRuntime } from '/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/agent-runtime.mjs';
import { runtimeSubjectKey } from '/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/manifest.mjs';
const root = await mkdtemp(join(tmpdir(), 'cyf-mustdo-heartbeat-'));
try {
  const host = join(root, 'host'); await mkdir(host, {mode:0o700});
  const agents = [];
  for (let i=0; i<2; i++) {
    const stateRoot=join(root, `subject-${i}`); await mkdir(stateRoot,{mode:0o700});
    const manifest={tenantId:'0',clientId:'synthetic',canonicalAgentId:`synthetic-${i}`,installationId:`synthetic-install-${i}`};
    agents.push({manifest,stateRoot,subjectKey:runtimeSubjectKey(manifest)});
  }
  const controller=new AbortController(); const states=[]; let calls=0; let enter;
  const entered=new Promise(resolve=>{enter=resolve});
  const running=runUnifiedRuntime({config:{hostId:'synthetic-host',stateRoot:host,agents},apiOrigin:'https://example.invalid',instanceId:'synthetic-boot',signal:controller.signal,
    createAdapters:async()=>({
      createExecutor:({subjectKey})=>{
        const s={subjectKey,ready:false,release:null}; states.push(s);
        return {initialize:async()=>{},activate:async()=>{
          if(subjectKey===agents[0].subjectKey){s.ready=true;return;}
          enter();await new Promise(resolve=>{s.release=resolve});
        },ready:()=>s.ready,pause:async()=>{},close:async()=>{s.release?.()}};
      },heartbeat:async()=>{calls++},close:async()=>{for(const s of states)s.release?.()}
    })});
  await entered;
  for(let i=0;i<5;i++) await new Promise(resolve=>setImmediate(resolve));
  const observation={firstAgentReady:states.find(s=>s.subjectKey===agents[0].subjectKey).ready,secondAgentActivationPending:true,heartbeatCallsBeforeAbort:calls};
  controller.abort(); const snapshot=await running;
  assert.equal(observation.firstAgentReady,true);assert.equal(observation.heartbeatCallsBeforeAbort,0);
  assert.ok(snapshot.agents.every(s=>s.phase==='STOPPED'));
  console.log(JSON.stringify({at:new Date().toISOString(),kind:'LOCAL_SYNTHETIC_REPRODUCTION_NOT_PRODUCTION',runtimeCommit:'5489c0e946114ec601e246a4eb93a0bff3b57c24',observation,shutdown:'STOPPED',conclusion:'Global activation barrier prevents healthy peer heartbeat until all activations settle'},null,2));
} finally {await rm(root,{recursive:true,force:true});}
