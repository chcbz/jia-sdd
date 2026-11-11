// Task-bound total-run watchdog. No deployment, no cancellation of unrelated runs.
const fs=require('fs'),path=require('path');
const SDK=require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625');
const dir=path.resolve(process.argv[2]),context=JSON.parse(fs.readFileSync(path.join(dir,'flow-start-context.json'))),started=JSON.parse(fs.readFileSync(path.join(dir,'flow-start-result.json')));
const run=String(started.returnedRunId||started.run?.id||'');
if(!/^\d+$/.test(run)||context.existingRunIds.includes(run)||started.ambiguousResponse)throw Error('Owned Run identity is not established');
const auth=JSON.parse(fs.readFileSync('/root/.codex/auth.json'));
const client=new SDK.default({accessKeyId:auth.ALIBABA_CLOUD_ACCESS_KEY_ID||auth.accessKeyId,accessKeySecret:auth.ALIBABA_CLOUD_ACCESS_KEY_SECRET||auth.accessKeySecret,endpoint:'devops.cn-hangzhou.aliyuncs.com',regionId:'cn-hangzhou',connectTimeout:5000,readTimeout:10000});
const terminal=['SUCCESS','FAIL','CANCELED','CANCELLED','SKIP'];
let canceled=fs.existsSync(path.join(dir,'stop-attempt.json'));
async function main(){
 while(true){
  try{
   const response=await client.getPipelineRun(context.org,context.pipeline,run);
   if(!response.body.success)throw Error('read failed');
   const r=response.body.pipelineRun;
   const sources=(r.sources||[]).map(s=>{let commits=[];try{commits=JSON.parse(s.data?.commint).map(x=>x.commitId)}catch{}return {branch:s.data?.branch,commits}});
   const summary={checkedAt:new Date().toISOString(),pipeline:context.pipeline,run,status:r.status,startTime:r.startTime,endTime:r.endTime,sources,stages:(r.stages||[]).map(s=>({name:s.name,status:s.status,jobs:(s.stageInfo?.jobs||[]).map(j=>({id:j.id,name:j.name,status:j.status}))}))};
   fs.writeFileSync(path.join(dir,'status.json'),JSON.stringify(summary,null,2)+'\n');
   console.log(JSON.stringify(summary));
   if(terminal.includes(r.status))break;
   const elapsed=(Date.now()-(Number(r.startTime)||Date.parse(started.requestStartedAt)))/1000;
   // Reserve transport time inside the user's 600s total allowance.
   if(elapsed>=580&&!canceled){
    if(!sources.some(s=>s.branch==='develop'&&s.commits.includes(context.expectedSources[0].commit)))throw Error('Source not proven; cannot cancel');
    fs.writeFileSync(path.join(dir,'stop-attempt.json'),JSON.stringify({run,at:new Date().toISOString(),elapsed,reason:'600s total budget; transport reserve'})+'\n',{flag:'wx'});canceled=true;
    await client.stopPipelineRun(context.org,context.pipeline,run);
   }
  }catch(e){fs.appendFileSync(path.join(dir,'watch-errors.jsonl'),JSON.stringify({at:new Date().toISOString(),error:'Flow status/stop call failed; no write retry'})+'\n');}
  await new Promise(resolve=>setTimeout(resolve,10000));
 }
}
main().catch(()=>{process.exitCode=1});
