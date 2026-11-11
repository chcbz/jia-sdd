const fs=require('node:fs'),path=require('node:path')
const SDK=require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625')
const {summarize}=require('/root/.codex/skills/aliyun-pipeline/scripts/flow.cjs')
const auth=JSON.parse(fs.readFileSync('/root/.codex/auth.json','utf8')),org='5fb7d76ee6f9d07f148529c7',pipeline='4403172',run='418'
const client=new SDK.default({accessKeyId:auth.ALIBABA_CLOUD_ACCESS_KEY_ID,accessKeySecret:auth.ALIBABA_CLOUD_ACCESS_KEY_SECRET,endpoint:'devops.cn-hangzhou.aliyuncs.com',readTimeout:25000,connectTimeout:10000})
;(async()=>{const response=(await client.getPipelineRun(org,pipeline,run)).body;if(!response.success)throw Error('READ_FAILED');const r=response.pipelineRun,at=new Date().toISOString();const summary={at,org,pipeline,...summarize(r)};fs.writeFileSync(path.join(__dirname,'flow-detail.json'),JSON.stringify(summary,null,2));console.log(JSON.stringify(summary));
for(const job of (r.stages||[]).flatMap(s=>s.stageInfo?.jobs||[])){
 const response=(await client.logPipelineJobRun(org,pipeline,String(job.id),run)).body;if(!response.success||!response.log)continue
 const safe=(response.log.content||'').split('\n').filter(line=>/\]\s+(?:\d+ (?:passing|pending|failing)|✓ built in|CYF_FLOW_PHASE |CYF_WEB_ARTIFACT )/.test(line)).join('\n')
 fs.writeFileSync(path.join(__dirname,'flow-job-'+job.id+'-summary.json'),JSON.stringify({at,run,job:job.id,more:response.log.more,summary:safe},null,2));console.log(safe)
}
})().catch(()=>{console.error('FLOW_READ_FAILED');process.exitCode=1})
