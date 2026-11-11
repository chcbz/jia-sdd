// Discovery-only: owned empty environment, synthetic skills, no auth/model/Provider calls.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawn, execFileSync } from 'node:child_process';
import { createInterface } from 'node:readline';
import { fileURLToPath } from 'node:url';
const output = path.dirname(fileURLToPath(import.meta.url));
const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'cyf-design-discovery-'));
const home=path.join(temp,'home'), codexHome=path.join(temp,'codex-home'), workspace=path.join(temp,'workspace');
for (const p of [home,codexHome,workspace]) fs.mkdirSync(p,{mode:0o700});
fs.writeFileSync(path.join(codexHome,'config.toml'),'approval_policy = "never"\nsandbox_mode = "read-only"\nweb_search = "disabled"\n',{mode:0o600});
const skill=(root,name)=>{fs.mkdirSync(path.join(root,name),{recursive:true});fs.writeFileSync(path.join(root,name,'SKILL.md'),`---\nname: ${name}\ndescription: Synthetic discovery-only audit fixture, never execute.\n---\nThis is inert test data.\n`)};
skill(path.join(codexHome,'skills'),'audit-approved');
const report={at:new Date().toISOString(),scope:'Discovery only; no auth, no model, no thread/start or turn/start.',version:execFileSync('/usr/local/bin/codex',['--version'],{encoding:'utf8'}).trim()};
const child=spawn('/usr/local/bin/codex',['app-server'],{cwd:workspace,env:{PATH:process.env.PATH,LANG:'C.UTF-8',HOME:home,CODEX_HOME:codexHome},stdio:['pipe','pipe','pipe']});
let sequence=0,stderr='';const pending=new Map();const lines=createInterface({input:child.stdout});
child.stderr.on('data',d=>stderr=(stderr+d).slice(-2000));
lines.on('line',line=>{let m;try{m=JSON.parse(line)}catch{return}const p=pending.get(m.id);if(p){pending.delete(m.id);clearTimeout(p.timer);m.error?p.reject(Error(JSON.stringify(m.error))):p.resolve(m.result)}else if(m.id!=null&&m.method)child.stdin.write(JSON.stringify({id:m.id,error:{code:-32001,message:'No execution in audit'}})+'\n')});
child.on('exit',()=>{for(const p of pending.values()){clearTimeout(p.timer);p.reject(Error('Probe exited'))}pending.clear()});
const rpc=(method,params)=>new Promise((resolve,reject)=>{const id=++sequence;const timer=setTimeout(()=>{pending.delete(id);reject(Error('Diagnostic RPC timeout: '+method))},20000);pending.set(id,{resolve,reject,timer});child.stdin.write(JSON.stringify({id,method,params})+'\n')});
function skills(value){if(Array.isArray(value))return value.flatMap(skills);if(!value||typeof value!=='object')return [];if(typeof value.name==='string'&&typeof value.path==='string')return [{name:value.name,path:value.path,scope:value.scope,enabled:value.enabled}];return Object.values(value).flatMap(skills)}
try {
 await rpc('initialize',{clientInfo:{name:'cyf-design-audit',version:'1'}});child.stdin.write(JSON.stringify({method:'initialized',params:{}})+'\n');
 report.before=skills(await rpc('skills/list',{cwds:[workspace],forceReload:true}));
 skill(path.join(workspace,'.agents','skills'),'audit-untrusted-workspace');
 report.after=skills(await rpc('skills/list',{cwds:[workspace],forceReload:true}));
 report.workspaceSkillDiscovered=report.after.some(s=>s.name==='audit-untrusted-workspace'&&s.enabled!==false);
 report.approvedSkillDiscovered=report.before.some(s=>s.name==='audit-approved'&&s.enabled!==false);
 console.log(JSON.stringify(report,null,2));
} catch(error) {report.error=error.message;report.stderr=stderr;process.exitCode=1;console.error(error.message)}
finally {
 child.stdin.end();if(child.exitCode===null)await Promise.race([new Promise(r=>child.once('exit',r)),new Promise(r=>setTimeout(r,1500))]);
 if(child.exitCode===null){child.kill('SIGTERM');await new Promise(r=>child.once('exit',r))}
 lines.close();fs.rmSync(temp,{recursive:true,force:true});report.ownedTemporaryStateRemoved=true;
 fs.writeFileSync(path.join(output,'skill-discovery-result.json'),JSON.stringify(report,null,2)+'\n');
}
