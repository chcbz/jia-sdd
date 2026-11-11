import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import cp from 'node:child_process';
import {collateExecutionPayload,validateExecutionPayload,EXECUTION_PAYLOAD_FILES} from './conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs';
const out=path.resolve('_runtime_export'),payload=path.join(out,'payload');fs.mkdirSync(payload);
await collateExecutionPayload(path.resolve('conf/codex-bridge'),path.join(payload,'codex-bridge'));
fs.cpSync(path.resolve('conf/codex-bridge/node_modules'),path.join(payload,'codex-bridge/node_modules'),{recursive:true,dereference:true,errorOnExist:true,force:false});
await validateExecutionPayload(path.join(payload,'codex-bridge'),{toolchain:false});
const installer=fs.readFileSync('conf/cyf-agent-runtime-v1/install.sh','utf8');
const lists=[...installer.matchAll(/for file in ([\s\S]*?); do\s+install -m (0[0-7]+) "\$SOURCE_DIR\/\$file"/g)];
if(lists.length!==2)throw Error('Runtime installer catalog changed');
for(const m of lists){for(const name of m[1].replace(/\\\n/g,' ').trim().split(/\s+/)){
 if(name.includes('..')||name.startsWith('/'))throw Error('Unsafe source path');
 const dest=path.join(payload,'runtime',name);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(path.join('conf/cyf-agent-runtime-v1',name),dest);fs.chmodSync(dest,parseInt(m[2],8));
}}
const files=[];function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else if(e.isFile())files.push({path:path.relative(payload,p),sha256:crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),mode:fs.statSync(p).mode&0o777});else throw Error('Unsafe payload')}}walk(payload);
const meta={pipeline:process.env.PIPELINE_ID,run:process.env.BUILD_NUMBER,commit:process.env.CI_COMMIT_SHA,tree:cp.execFileSync('git',['rev-parse','HEAD^{tree}'],{encoding:'utf8'}).trim(),version:JSON.parse(fs.readFileSync(path.join(payload,'runtime/package.json'))).version,engineFileCount:EXECUTION_PAYLOAD_FILES.length,files};
if(meta.version!=='1.3.21'||JSON.parse(fs.readFileSync('conf/codex-bridge/package.json')).version!=='1.1.12')throw Error('Unexpected candidate');
meta.dependencyProvenance={method:'same-Run npm ci --ignore-scripts --no-audit --no-fund',lockSha256:crypto.createHash('sha256').update(fs.readFileSync('conf/codex-bridge/package-lock.json')).digest('hex'),buildNode:process.versions.node,retainedPythonRequirementsSha256:crypto.createHash('sha256').update(fs.readFileSync('conf/codex-bridge/toolchain/requirements.txt')).digest('hex')};
fs.writeFileSync(path.join(out,'release.json'),JSON.stringify(meta,null,2)+'\n');
console.log('RUNTIME_PAYLOAD_FILES='+files.length);console.log('RUNTIME_SOURCE='+meta.commit);console.log('RUNTIME_TREE='+meta.tree);
