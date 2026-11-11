// Task-scoped pagination adapter for existing flow-control commandStart.
// The CLI refuses a truncated >100-run history; enumerate all pages, never drop history.
const fs=require('fs'),path=require('path'),crypto=require('crypto'),cp=require('child_process')
const SDK=require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625')
const {commandStart,configSummary}=require('/home/isp/wsps/cyf/ops/ci/aliyun-flow/flow-control.cjs')
const out=__dirname,org='5fb7d76ee6f9d07f148529c7',pipeline='4403172',commit='339f3be8af09e09ba46e0b29a8e68d8fc30d8576',repo='https://gitee.com/chcbz/cyf-web-kit.git'
const auth=JSON.parse(fs.readFileSync('/root/.codex/auth.json','utf8'))
const client=new SDK.default({accessKeyId:auth.ALIBABA_CLOUD_ACCESS_KEY_ID||auth.accessKeyId,accessKeySecret:auth.ALIBABA_CLOUD_ACCESS_KEY_SECRET||auth.accessKeySecret,endpoint:'devops.cn-hangzhou.aliyuncs.com',regionId:'cn-hangzhou'})
const allClient={getPipeline:(...a)=>client.getPipeline(...a),getPipelineRun:(...a)=>client.getPipelineRun(...a),startPipelineRun:(...a)=>client.startPipelineRun(...a),listPipelineRuns:async(o,p)=>{
 let nextToken;const runs=[];const seen=new Set()
 do { const r=await client.listPipelineRuns(o,p,new SDK.ListPipelineRunsRequest({maxResults:100,nextToken})); if(!r.body.success) throw Error('history read failed');runs.push(...r.body.pipelineRuns);nextToken=r.body.nextToken;if(nextToken&&seen.has(nextToken)) throw Error('pagination cycle');seen.add(nextToken) }while(nextToken)
 return {body:{success:true,pipelineRuns:runs}}
}}
async function main(){
 if(fs.existsSync(path.join(out,'flow-start-attempt.json'))) throw Error('start already attempted; reconcile read-only')
 const remote=cp.execFileSync('git',['ls-remote',repo,'refs/heads/develop'],{encoding:'utf8'}).split(/\s/)[0];if(remote!==commit)throw Error('source moved')
 const config=(await client.getPipeline(org,pipeline)).body.pipeline
 const summary=configSummary(config);if(summary.canonicalConfigSha256!=='6d1b668d2f016596418b0f37cb110e83c01feb9b6882499bda1b9a772bdaf68a')throw Error('configuration changed')
 const runs=(await allClient.listPipelineRuns(org,pipeline)).body.pipelineRuns
 if(runs.some(r=>!['SUCCESS','FAIL','CANCELED','CANCELLED','SKIP'].includes(r.status)))throw Error('active or unknown run; coordinate')
 const context={schemaVersion:1,kind:'cyf.flow.start-context.v1',org,pipeline,pipelineName:summary.name,canonicalConfigSha256:summary.canonicalConfigSha256,existingRunIds:runs.map(r=>String(r.pipelineRunId)),requestStartedAt:new Date().toISOString(),params:{runningBranchs:{[repo]:'develop'}},expectedSources:[{repo,branch:'develop',commit}]}
 const file=path.join(out,'flow-start-context.json');fs.writeFileSync(file,JSON.stringify(context,null,2)+'\n');const sha=crypto.createHash('sha256').update(fs.readFileSync(file)).digest('hex')
 const allow=path.join(out,'flow-allowlist.json');fs.writeFileSync(allow,JSON.stringify({organizations:[org],pipelines:[{org,pipeline}]}))
 fs.writeFileSync(path.join(out,'flow-start-attempt.json'),JSON.stringify({at:new Date().toISOString(),contextSha256:sha,historyCount:runs.length})+'\n',{flag:'wx'})
 const result=await commandStart(allClient,{org,pipeline,context:file,'context-sha256':sha,allowlist:allow})
 fs.writeFileSync(path.join(out,'flow-start-result.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result))
}
main().catch(e=>{console.error('Start stopped; reconcile read-only. '+(e.message.match(/^[a-z ;>-]+$/i)?e.message:'API or controller failure'));process.exitCode=1})
