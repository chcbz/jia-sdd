import { mkdirSync, mkdtempSync, writeFileSync, rmSync } from 'node:fs'
import { resolve } from 'node:path'
import { spawnSync, spawn } from 'node:child_process'
import { measureMinimalNativeExecutionToolchain, prepareNativeExecutionLayout, nativeExecutionMountArgs, buildNativeExecutionCodexConfig } from '/home/isp/wsps/chcbz/isp-install/conf/codex-bridge/native-execution-profile.mjs'
import { buildTypedInspectionCodexConfig } from '/home/isp/wsps/chcbz/isp-install/conf/codex-bridge/typed-inspection-profile.mjs'
import { AppServerAdapter } from '/home/isp/wsps/chcbz/isp-install/conf/codex-bridge/app-server-adapter.mjs'
const root=mkdtempSync('/tmp/cyf-nested-'); const dir=n=>{let p=resolve(root,n);mkdirSync(p,{recursive:true,mode:0o700});return p}
try {
 const stateRoot=dir('state'); const codexHome=dir('state/codex-home'); writeFileSync(resolve(codexHome,'config.toml'),buildNativeExecutionCodexConfig(buildTypedInspectionCodexConfig({})))
 const layout=prepareNativeExecutionLayout({inputDirectory:dir('exec/inputs'),scratchDirectory:dir('exec/scratch'),draftsDirectory:dir('exec/drafts'),stateRoot,sourceHome:dir('main-home'),skills:[],toolchain:measureMinimalNativeExecutionToolchain(),nativeExecution:{executionId:'probe',tools:[],checkActive(){},callTool(){}}})
 const args=['--unshare-all','--die-with-parent','--new-session','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--ro-bind','/usr/local/lib/node_modules/@openai/codex/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl','/runtime','--ro-bind',layout.inputDirectory,'/inputs',...nativeExecutionMountArgs({layout,engineState:{codexHome},neutralDirectory:dir('neutral'),skillsDirectory:dir('skills')}),'--setenv','HOME','/state/home','--setenv','CODEX_HOME','/state/codex-home','--chdir','/execution']
 for(const name of ['.git','.codex','.agents','.aws']) {dir(`neutral/${name}`)}
 const child = spawn('/usr/bin/bwrap', [...args,'/runtime/bin/codex','app-server'], {env:{LANG:'C.UTF-8'},stdio:['pipe','pipe','pipe']})
 const adapter = new AppServerAdapter({child})
 try {
  await adapter.request('initialize',{clientInfo:{name:'probe',version:'1'}}); adapter.notify('initialized',{})
  const r=await adapter.request('command/exec',{command:['/bin/bash','-c','printf nested-ok > /outputs/a.txt && cat /outputs/a.txt; ! (echo bad > /state/codex-home/leak)'],cwd:'/execution',sandboxPolicy:{type:'workspaceWrite',writableRoots:['/workspace','/outputs'],networkAccess:false,excludeSlashTmp:true,excludeTmpdirEnvVar:true}})
  console.log(JSON.stringify(r))
 } finally {await adapter.shutdown()}

} finally{rmSync(root,{recursive:true,force:true})}
