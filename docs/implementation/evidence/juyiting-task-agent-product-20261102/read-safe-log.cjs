// Never persist environment dumps or source credentials from build logs.
const fs=require('fs'),SDK=require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625');
const {redact}=require('/root/.codex/skills/aliyun-pipeline/scripts/flow.cjs');
const a=JSON.parse(fs.readFileSync('/root/.codex/auth.json'));
const c=new SDK.default({accessKeyId:a.ALIBABA_CLOUD_ACCESS_KEY_ID||a.accessKeyId,accessKeySecret:a.ALIBABA_CLOUD_ACCESS_KEY_SECRET||a.accessKeySecret,endpoint:'devops.cn-hangzhou.aliyuncs.com',regionId:'cn-hangzhou'});
const [pipeline,run,job,file]=process.argv.slice(2),org='5fb7d76ee6f9d07f148529c7';
async function main(){
 const detail=(await c.getPipelineRun(org,pipeline,run)).body.pipelineRun;
 if(!(detail.stages||[]).flatMap(s=>s.stageInfo?.jobs||[]).some(j=>String(j.id)===job))throw Error('job mismatch');
 const response=await c.logPipelineJobRun(org,pipeline,job,run);if(!response.body.success)throw Error('read failed');
 const l=response.body.log;
 const lines=l.content.split('\n').filter(line=>!/declare -x|SOURCES=|ACCESS.?KEY|secret|password|passwd|credential|authorization|PRIVATE KEY|token["'\s:=]/i.test(line));
 const content=redact(lines.join('\n'));
 fs.writeFileSync(file,JSON.stringify({checkedAt:new Date().toISOString(),pipeline,run,job,more:l.more,content},null,2)+'\n');
 console.log(content.split('\n').filter(line=>/error|fail|exception|BUILD|CYF_FLOW_PHASE|passing|tests completed|npm ERR|cannot|not found|\b[0-9]+ failing|\) /i.test(line)).slice(-55).join('\n'));
}
main().catch(()=>{console.error('Log read failed; raw error suppressed');process.exitCode=1});
