const fs=require('fs'),crypto=require('crypto');const SDK=require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625');
const auth=JSON.parse(fs.readFileSync('/root/.codex/auth.json'));const client=new SDK.default({accessKeyId:auth.ALIBABA_CLOUD_ACCESS_KEY_ID,accessKeySecret:auth.ALIBABA_CLOUD_ACCESS_KEY_SECRET,endpoint:'devops.cn-hangzhou.aliyuncs.com',regionId:'cn-hangzhou',connectTimeout:5000,readTimeout:10000});
function redact(value) {
  return String(value).replace(/\x1b\[[0-9;]*m/g, '')
    .replace(/-----BEGIN ([A-Z0-9 ]*PRIVATE KEY)-----[\s\S]*?(?:-----END \1-----|$)/g, '[REDACTED_PRIVATE_KEY]')
    .replace(/https?:\/\/[^\s<>"']+/gi, raw => {
      try {
        const u = new URL(raw);
        if (u.username || u.password) { u.username = 'REDACTED'; u.password = ''; }
        if (u.search) u.search = '?REDACTED';
        if (u.hash) u.hash = '#REDACTED';
        return u.toString();
      } catch { return '[REDACTED_URL]'; }
    })
    .split('\n').map(line => /(?:authorization|access[_-]?key(?:[_-]?(?:id|secret))?|accessKey(?:Id|Secret)?|secret|password|passwd|token|credential|private[_ -]?key)["']?\s*[:=]/i.test(line)
      ? '[REDACTED_CREDENTIAL_LINE]' : line).join('\n')
    .replace(/\bLTAI[A-Za-z0-9]+\b/g, '[REDACTED_ACCESS_KEY]');
}

(async()=>{const start=JSON.parse(fs.readFileSync(__dirname+'/web-start.json'));const run=String(start.run?.id||start.runId||start.returnedRunId);const org='5fb7d76ee6f9d07f148529c7',pipeline='4403172';const r=(await client.getPipelineRun(org,pipeline,run)).body.pipelineRun;const jobs=r.stages.flatMap(s=>s.stageInfo.jobs);const summary={queriedAt:new Date().toISOString(),run,status:r.status,jobs:jobs.map(j=>({id:j.id,name:j.name,status:j.status,actions:(j.actions||[]).map(a=>({type:a.type,deployOrderId:a.params?.deployOrderId}))})),artifacts:jobs.flatMap(j=>(j.actions||[]).filter(a=>a.type==='GetPipelineArtifactUrl').flatMap(a=>a.params.files))};fs.writeFileSync(__dirname+'/flow-result.json',JSON.stringify(summary,null,2));for(const j of jobs.filter(j=>j.actions?.some(a=>a.type==='LogPipelineJobRun'))){const log=(await client.logPipelineJobRun(org,pipeline,String(j.id),run)).body.log;if(log?.content){const content=redact(log.content).split('\n').filter(l=>!l.startsWith('declare -x ')).join('\n');fs.writeFileSync(__dirname+'/log-'+j.id+'.json',JSON.stringify({job:j.id,name:j.name,more:log.more,outputTruncated:false,environmentDumpOmitted:true,content},null,2));}}console.log(JSON.stringify(summary));})().catch(()=>{console.error('RELEASE_EVIDENCE_QUERY_FAILED');process.exitCode=1});