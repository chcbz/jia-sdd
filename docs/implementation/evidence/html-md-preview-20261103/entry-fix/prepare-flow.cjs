const fs=require('node:fs'),path=require('node:path'),crypto=require('node:crypto')
const SDK=require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625')
const c=JSON.parse(fs.readFileSync('/root/.codex/auth.json','utf8'))
const client=new SDK.default({accessKeyId:c.ALIBABA_CLOUD_ACCESS_KEY_ID,accessKeySecret:c.ALIBABA_CLOUD_ACCESS_KEY_SECRET,endpoint:'devops.cn-hangzhou.aliyuncs.com',readTimeout:25000,connectTimeout:10000})
const org='5fb7d76ee6f9d07f148529c7',pipeline='4403172'
;(async()=>{
let nextToken,active=[];do{const r=(await client.listPipelineRuns(org,pipeline,new SDK.ListPipelineRunsRequest({maxResults:100,nextToken}))).body;if(!r.success)throw Error('LIST_FAILED');active.push(...r.pipelineRuns.filter(r=>['RUNNING','QUEUED','WAITING'].includes(r.status)).map(r=>({id:r.pipelineRunId,status:r.status})));nextToken=r.nextToken||undefined}while(nextToken)
if(active.length){console.log(JSON.stringify({active}));return}
const r=(await client.getPipeline(org,pipeline)).body;if(!r.success)throw Error('CONFIG_FAILED');const flow=r.pipeline.pipelineConfig.flow
const dir='/home/isp/state/html-md-preview-entry-fix-20261103';fs.mkdirSync(dir,{recursive:true,mode:0o700});fs.writeFileSync(path.join(dir,'before-pin.yaml'),flow,{mode:0o600,flag:'wx'})
const commit=require('node:child_process').execFileSync('git',['-C','/home/isp/wsps/worktrees/preview-entry-fix-20261103','rev-parse','HEAD'],{encoding:'utf8'}).trim();const guards=[...flow.matchAll(/test "\$CI_COMMIT_SHA" = ([a-f0-9]{40})/g)];if(guards.length!==1)throw Error('GUARD_UNKNOWN');const candidate=flow.replace(guards[0][1],commit);fs.writeFileSync(path.join(dir,'candidate.yaml'),candidate,{mode:0o600,flag:'wx'});console.log(JSON.stringify({commit,candidateSha256:crypto.createHash('sha256').update(candidate).digest('hex'),active,name:r.pipeline.name,guards:[...new Set(flow.match(/\b[a-f0-9]{40}\b/g))],workerOnly:!/(VMDeploy|ssh |scp |cyf-web-flow-host)/i.test(flow),bytes:flow.length}))
})().catch(()=>{console.error('PREPARE_FAILED');process.exitCode=1})
