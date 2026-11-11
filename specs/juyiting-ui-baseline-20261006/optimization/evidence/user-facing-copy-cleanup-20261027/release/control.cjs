// Authorized USER-FACING-COPY-CLEANUP-20261027 release, fixed source, no other-run cancellation.
const fs=require('fs'),cp=require('child_process'),crypto=require('crypto'),y=require('/home/isp/wsps/cyf/web/node_modules/js-yaml'),SDK=require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625'),ctl=require('/home/isp/wsps/cyf/ops/ci/aliyun-flow/flow-control.cjs');process.umask(0o077);
const dir=__dirname,org='5fb7d76ee6f9d07f148529c7',hash=x=>crypto.createHash('sha256').update(x).digest('hex');
const a=JSON.parse(fs.readFileSync('/root/.codex/auth.json'));const c=new SDK.default({accessKeyId:a.ALIBABA_CLOUD_ACCESS_KEY_ID,accessKeySecret:a.ALIBABA_CLOUD_ACCESS_KEY_SECRET,endpoint:'devops.cn-hangzhou.aliyuncs.com',connectTimeout:5000,readTimeout:15000});
const specs={ops:{id:'5264702',repo:'',path:'/home/isp/wsps/chcbz/isp-install'},runtime:{id:'5264702',repo:'https://gitee.com/chcbz/isp-install',path:'/home/isp/wsps/chcbz/isp-install'},api:{id:'5260799',repo:'https://gitee.com/chcbz/jia.git',path:'/home/isp/wsps/worktrees/business-normal-api-20261027'},web:{id:'4403172',repo:'https://gitee.com/chcbz/cyf-web-kit.git',path:'/home/isp/wsps/cyf/web'}};
const rawList=c.listPipelineRuns.bind(c);c.listPipelineRuns=async(o,id)=>{let out=[],token,r;do{r=await rawList(o,id,new SDK.ListPipelineRunsRequest({maxResults:100,...(token?{nextToken:token}:{})}));if(!r.body.success)throw Error('LIST_FAILED');out.push(...r.body.pipelineRuns);token=r.body.nextToken;}while(token);return {...r,body:{...r.body,pipelineRuns:out,nextToken:null}}};
const save=(name,v)=>fs.writeFileSync(dir+'/'+name,JSON.stringify(v,null,2)+'\n'),git=(s,arg)=>cp.execFileSync('git',['-C',s.path,'rev-parse',arg],{encoding:'utf8'}).trim();
(async()=>{const [op,name]=process.argv.slice(2),s=specs[name];if(!s||name!=='web')throw Error('SCOPE');const runs=(await c.listPipelineRuns(org,s.id)).body.pipelineRuns;
if(op==='status'){const start=JSON.parse(fs.readFileSync(dir+'/'+name+'-start.json')),id=start.run?.id||start.runId;const r=(await c.getPipelineRun(org,s.id,String(id))).body;if(!r.success)throw Error('READ');save(name+'-run.json',r.pipelineRun);console.log(JSON.stringify({pipeline:s.id,run:id,status:r.pipelineRun.status,start:r.pipelineRun.startTime}));return;}
if(runs.some(r=>!['SUCCESS','FAIL','CANCELED','CANCELLED','SKIPPED'].includes(r.status)))throw Error('ACTIVE_RUN_NO_WRITE');
const response=(await c.getPipeline(org,s.id)).body;if(!response.success)throw Error('GET');const current=response.pipeline,summary=ctl.configSummary(current);
if(op==='prepare'){
 if(fs.existsSync(dir+'/'+name+'-original.yaml'))throw Error('SNAPSHOT_EXISTS');fs.writeFileSync(dir+'/'+name+'-original.yaml',current.pipelineConfig.flow);save(name+'-original.json',summary);
 const sha=git(s,'361ed19bf405d81813e993bac533fb2e729385cc'),tree=git(s,'361ed19bf405d81813e993bac533fb2e729385cc^{tree}'),branch='develop';const cfg=y.load(fs.readFileSync(dir+'/'+name+'-release.yaml','utf8'));
 for(const src of Object.values(cfg.sources)){src.branch=branch;src.triggerEvents=[];src.branchesFilter='^'+branch.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')+'$';}
 const text=y.dump(cfg,{lineWidth:-1,noRefs:true});fs.writeFileSync(dir+'/'+name+'-candidate.yaml',text);
 const ctx={schemaVersion:1,kind:'cyf.flow.start-context.v1',org,pipeline:s.id,pipelineName:current.name,canonicalConfigSha256:hash(ctl.canonicalFlowText(text)),existingRunIds:runs.map(r=>String(r.pipelineRunId)),requestStartedAt:new Date().toISOString(),params:name==='ops'?{envs:{}}:{runningBranchs:{[s.repo]:branch},envs:{}},expectedSources:name==='ops'?[]:[{repo:s.repo,branch,commit:sha}]};save(name+'-start-context.json',ctx);console.log(JSON.stringify({prepared:name,commit:sha,tree,branch,stages:Object.keys(cfg.stages)}));return;
}
const allowlist=dir+'/allowlist.json';
if(op==='update'||op==='restore'){
 const expected=op==='update'?JSON.parse(fs.readFileSync(dir+'/'+name+'-original.json')).canonicalConfigSha256:hash(ctl.canonicalFlowText(fs.readFileSync(dir+'/'+name+'-candidate.yaml','utf8')));
 if(summary.canonicalConfigSha256!==expected)throw Error('CONFIG_CHANGED_NO_WRITE');
 const candidate=dir+'/'+name+(op==='update'?'-candidate.yaml':'-original.yaml');const result=await ctl.commandUpdate(c,{org,pipeline:s.id,name:current.name,allowlist,candidate,'candidate-sha256':hash(fs.readFileSync(candidate))});save(name+'-'+op+'.json',result);console.log(JSON.stringify(result));return;
}
if(op==='start'){
 const path=dir+'/'+name+'-start-context.json',ctx=JSON.parse(fs.readFileSync(path));ctx.existingRunIds=runs.map(r=>String(r.pipelineRunId));ctx.requestStartedAt=new Date().toISOString();save(name+'-start-context.json',ctx);const result=await ctl.commandStart(c,{org,pipeline:s.id,allowlist,context:path,'context-sha256':hash(fs.readFileSync(path))});save(name+'-start.json',result);console.log(JSON.stringify(result));return;
}throw Error('ACTION');})().catch(e=>{console.error(e.code||e.message);process.exitCode=1});
