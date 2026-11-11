const fs=require('fs');const SDK=require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625');
const auth=JSON.parse(fs.readFileSync('/root/.codex/auth.json'));const client=new SDK.default({accessKeyId:auth.ALIBABA_CLOUD_ACCESS_KEY_ID,accessKeySecret:auth.ALIBABA_CLOUD_ACCESS_KEY_SECRET,endpoint:'devops.cn-hangzhou.aliyuncs.com',regionId:'cn-hangzhou',connectTimeout:5000,readTimeout:10000});
const org='5fb7d76ee6f9d07f148529c7',pipeline='4403172',commit='c5657bb334a6cf1651c9874d22eadfc295b57ea9',before=new Set([355,354,353,352,351,350]);
const out='/home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/optimization/evidence/discussion-material-development-20261027/flow-watch.json';const evidence={task:'DISCUSSION-MATERIAL-UNIFIED-20261027',commit,org,pipeline,observations:[]};let runId=null,cancelSent=false;
const save=()=>fs.writeFileSync(out,JSON.stringify(evidence,null,2));const pause=ms=>new Promise(r=>setTimeout(r,ms));
async function body(p){const b=(await p).body;if(!b||b.success===false||b.errorCode)throw new Error('FLOW_API_READ_FAILED');return b}
const commits=r=>(r.sources||[]).flatMap(s=>{try{return JSON.parse(s.data.commint).map(x=>x.commitId)}catch{return[]}});
(async()=>{for(;;){try{
 if(!runId){const list=await body(client.listPipelineRuns(org,pipeline,new SDK.ListPipelineRunsRequest({maxResults:10})));for(const candidate of list.pipelineRuns||[]){if(before.has(candidate.pipelineRunId)||Number(candidate.pipelineRunId)<=355)continue;const r=(await body(client.getPipelineRun(org,pipeline,String(candidate.pipelineRunId)))).pipelineRun;if(commits(r).includes(commit)){runId=String(candidate.pipelineRunId);evidence.run=runId;break}}if(!runId){await pause(3000);continue}}
 const r=(await body(client.getPipelineRun(org,pipeline,runId))).pipelineRun;if(!commits(r).includes(commit))throw new Error('SOURCE_MISMATCH');
 const elapsed=(Date.now()-Number(r.startTime))/1000;const status=r.status;evidence.observations.push({at:new Date().toISOString(),status,elapsedSeconds:Math.round(elapsed),startTime:r.startTime,endTime:r.endTime});save();console.log(JSON.stringify({runId,status,elapsed:Math.round(elapsed)}));
 if(['SUCCESS','FAIL','FAILED','CANCELED','CANCELLED','STOPPED','TERMINATED'].includes(status)){evidence.finalStatus=status;evidence.totalSeconds=r.endTime?(Number(r.endTime)-Number(r.startTime))/1000:null;save();break}
 if(elapsed>=580&&!cancelSent){cancelSent=true;evidence.cancelRequestedAt=new Date().toISOString();save();await body(client.stopPipelineRun(org,pipeline,runId));evidence.cancelAcknowledgedAt=new Date().toISOString();save()}
 await pause(elapsed>=550?2000:10000)
 }catch(e){evidence.observations.push({at:new Date().toISOString(),error:e.message==='SOURCE_MISMATCH'?'SOURCE_MISMATCH':'FLOW_API_UNAVAILABLE'});save();if(e.message==='SOURCE_MISMATCH')throw e;await pause(2000)}}})().catch(()=>{console.error('FLOW_MONITOR_FAILED');process.exitCode=1});
