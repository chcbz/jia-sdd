// One authorized operation per invocation; fixed new CI pipeline only.
// Credentials stay in memory. No retry loops. No deployment operation exists here.
const fs = require('fs');
const crypto = require('crypto');
const SDK = require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625');
const {redact, summarize} = require('/root/.codex/skills/aliyun-pipeline/scripts/flow.cjs');
const ORG = '5fb7d76ee6f9d07f148529c7', PIPELINE = '5256653';
const conf = JSON.parse(fs.readFileSync('/root/.aliyun/config.json', 'utf8'));
const profile = conf.profiles.find(p => p.name === conf.current);
const client = new SDK.default({accessKeyId: profile.access_key_id, accessKeySecret: profile.access_key_secret,
  endpoint:'devops.cn-hangzhou.aliyuncs.com', regionId:'cn-hangzhou', readTimeout:25000, connectTimeout:10000});
const sha = x => crypto.createHash('sha256').update(x).digest('hex');
async function body(req) {
  const b = (await req).body;
  if (!b || b.success === false || b.errorCode) {
    const e = new Error(b && (b.errorMessage || b.message) || 'Missing API body');
    e.code = b && b.errorCode; e.requestId = b && b.requestId; throw e;
  }
  return b;
}
async function runs() {
  const b = await body(client.listPipelineRuns(ORG,PIPELINE,new SDK.ListPipelineRunsRequest({maxResults:100})));
  if (!Array.isArray(b.pipelineRuns)) throw new Error('Missing run list');
  return {runs:b.pipelineRuns.map(r => ({id:r.pipelineRunId,status:r.status,started:r.startTime})),nextToken:b.nextToken};
}
async function main() {
  const [mode, arg, expected] = process.argv.slice(2);
  let out;
  if (mode === 'runs') out = await runs();
  else if (mode === 'config') {
    const b = await body(client.getPipeline(ORG,PIPELINE));
    const p = b.pipeline, f = p.pipelineConfig.flow;
    out={name:p.name,configKeys:Object.keys(p.pipelineConfig),flowType:typeof f,
      flowSha256:sha(typeof f==='string'?f:JSON.stringify(f)),flowLength:JSON.stringify(f).length,
      flow:f}; // This dedicated new pipeline contains no secrets; never use this helper for legacy pipelines.
  } else if (mode === 'status' || mode === 'log') {
    if (!/^[0-9]+$/.test(arg||'')) throw new Error('Numeric Run required');
    const r=(await body(client.getPipelineRun(ORG,PIPELINE,arg))).pipelineRun;
    out=summarize(r);
    if(mode==='log') {
      if(!/^[0-9]+$/.test(expected||'')) throw new Error('Numeric Job required');
      const jobs=(r.stages||[]).flatMap(s=>s.stageInfo?.jobs||[]);
      if(!jobs.some(j=>String(j.id)===expected)) throw new Error('Job not in run');
      const l=(await body(client.logPipelineJobRun(ORG,PIPELINE,expected,arg))).log;
      out={run:arg,job:expected,status:r.status,more:l.more,content:redact(l.content||'')};
    }
  } else if(mode==='update') {
    const content=fs.readFileSync(arg,'utf8');
    if(sha(content)!==expected) throw new Error('Reviewed config hash mismatch');
    const before=await runs();
    if(before.runs.some(r=>!['SUCCESS','FAIL','FAILED','CANCELED','CANCELLED'].includes(r.status))) throw new Error('Existing nonterminal run; reconcile first');
    const startedAt=new Date().toISOString();
    const b=await body(client.updatePipeline(ORG,new SDK.UpdatePipelineRequest({pipelineId:PIPELINE,name:'cyf-api-kit-ci',content})));
    out={operation:'update',startedAt,configSha256:expected,requestId:b.requestId,success:b.success};
  } else if(mode==='start') {
    const context=JSON.parse(fs.readFileSync(arg,'utf8'));
    if(sha(fs.readFileSync(arg))!==expected || context.pipeline!==PIPELINE || context.org!==ORG) throw new Error('Frozen start context mismatch');
    const before=await runs();
    if(JSON.stringify(before.runs.map(r=>r.id).sort())!==JSON.stringify(context.existingRunIds.slice().sort())) throw new Error('Run list changed; reconcile');
    if(before.nextToken) throw new Error('Unpaginated history; reconcile');
    // API writes may be ambiguous. Caller records request time BEFORE invoking;
    // on any exception only inspect runs, NEVER invoke start unchanged again.
    const b=await body(client.startPipelineRun(ORG,PIPELINE,new SDK.StartPipelineRunRequest({params:JSON.stringify(context.params)})));
    out={operation:'start',response:b};
  } else throw new Error('Unsupported mode');
  console.log(JSON.stringify({queriedAt:new Date().toISOString(),org:ORG,pipeline:PIPELINE,...out},null,2));
}
main().catch(e=>{console.error(JSON.stringify({code:e.code||'LOCAL_OR_NETWORK',message:redact(String(e.message||'unknown')).slice(0,1500),requestId:e.requestId||e.data?.RequestId||null}));process.exitCode=1;});
