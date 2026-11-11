import fs from 'node:fs';import path from 'node:path';import {pathToFileURL} from 'node:url';import assert from 'node:assert/strict';
process.umask(0o077);const [app,base]=process.argv.slice(2);const mod=name=>import(pathToFileURL(path.join(app,'codex-bridge',name)).href);
const {normalizeProfile}=await mod('agent-client.mjs');const {NativeExecutionProfileRuntime}=await mod('native-execution-runtime.mjs');const {initializeNativeToolchain}=await mod('native-document-toolchain.mjs');
const root=fs.mkdtempSync(path.join(base,'readiness-state-'));const raw=JSON.parse(fs.readFileSync(process.argv[4] || '/home/isp/conf/cyf-agent-runtime-v1/unified-profiles/wuyong.json'));// A staging path has a different mount/toolchain binding. Only the isolated probe omits production carrier evidence; final-path check remains mandatory.
if (app !== '/home/isp/apps/cyf-agent-runtime-v1/app') raw.inputCarriers={...raw.inputCarriers,carrierEvidencePath:null,carrierEvidenceDigest:null};
const profile=normalizeProfile(raw,{},0,{isolated:true});const runtime=new NativeExecutionProfileRuntime({profile,materializerRoot:root+'/inputs',stateRoot:root+'/state'});const start=Date.now();let report;
try {await initializeNativeToolchain(runtime);const declaration=await runtime.measureNativeExecution();report={at:new Date().toISOString(),artifactPath:app,declaration,failure:runtime.nativeExecutionMeasurementFailure,documentFailure:runtime.nativeDocumentMeasurementFailure,browserFailure:runtime.nativeBrowserMeasurementFailure,pdfFailure:runtime.nativePdfMeasurementFailure,scriptFailure:runtime.nativeScriptMeasurementFailure,elapsedMs:Date.now()-start};
assert.equal(report.failure,null);assert.equal(report.documentFailure,null);assert.equal(report.browserFailure,null);assert.equal(report.pdfFailure,null);assert.equal(report.scriptFailure,null);
for(const mime of ['text/plain','text/markdown','text/html','image/png','application/pdf','application/vnd.openxmlformats-officedocument.wordprocessingml.document','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'])assert.ok(declaration.outputMimeTypes.includes(mime),mime);
assert.ok(declaration.supportedToolPolicyRefs.includes('NATIVE_SKILL_SCRIPT_V1'));report.passed=true;

} finally {await runtime.dispose();fs.rmSync(root,{recursive:true,force:true});fs.writeFileSync(path.join(base,'host-startup-readiness.json'),JSON.stringify(report??{passed:false},null,2));}
console.log(JSON.stringify(report));
