import fs from 'node:fs';import assert from 'node:assert/strict';
const app='/home/isp/apps/cyf-agent-runtime-v1/app';
const {normalizeProfile}=await import(app+'/codex-bridge/agent-client.mjs');
const {TypedInspectionProfileRuntime}=await import(app+'/codex-bridge/typed-inspection-profile.mjs');
const {initializeNativeToolchain}=await import(app+'/codex-bridge/native-document-toolchain.mjs');
const results=[];
for(const name of ['linchong','wuyong']) {
 const root=fs.mkdtempSync(import.meta.dirname+'/carrier-readback-');
 const raw=JSON.parse(fs.readFileSync('/home/isp/conf/cyf-agent-runtime-v1/unified-profiles/'+name+'.json'));
 const runtime=new TypedInspectionProfileRuntime({profile:normalizeProfile(raw,{},0,{isolated:true}),materializerRoot:root+'/inputs',stateRoot:root+'/state'});
 try {await initializeNativeToolchain(runtime);const measured=await runtime.measure();assert.equal(measured.contractReady,true);assert.equal(measured.supportedInputs.length,10);results.push({profile:name,contractReady:true,supportedInputs:measured.supportedInputs,binding:measured.binding,evidencePath:raw.inputCarriers.carrierEvidencePath,evidenceDigest:raw.inputCarriers.carrierEvidenceDigest});}
 finally {await runtime.dispose();fs.rmSync(root,{recursive:true,force:true});}
}
fs.writeFileSync(import.meta.dirname+'/installed-carrier-readback.json',JSON.stringify({at:new Date().toISOString(),realModelTurns:0,profilesChanged:false,results},null,2));
console.log('EXISTING_CARRIER_EVIDENCE_PASS profiles=2 model_turns=0');
