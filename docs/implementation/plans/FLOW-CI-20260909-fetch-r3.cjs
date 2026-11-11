// Same-run authenticated evidence download. Fixed pipeline, no cloud writes.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const {Readable,Transform}=require('stream'),{pipeline}=require('stream/promises');
const SDK=require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625');
const root='/home/isp/wsps/cyf/docs/implementation/plans',ORG='5fb7d76ee6f9d07f148529c7',PID='5256653';
const a=JSON.parse(fs.readFileSync('/root/.aliyun/config.json'));const p=a.profiles.find(x=>x.name===a.current);
const c=new SDK.default({accessKeyId:p.access_key_id,accessKeySecret:p.access_key_secret,endpoint:'devops.cn-hangzhou.aliyuncs.com',readTimeout:25000,connectTimeout:10000});
const sha=x=>crypto.createHash('sha256').update(x).digest('hex');
const normalize=s=>s.replace(/[\r\n]+$/,'');
const need=(b,m)=>{if(!b)throw Error(m)};
async function body(q){const b=(await q).body;need(b&&b.success!==false&&!b.errorCode,'API_FAILURE');return b;}
async function main(){const run=process.argv[2];need(/^[1-9][0-9]*$/.test(run||''),'INVALID_RUN');
 const ctx=JSON.parse(fs.readFileSync(path.join(root,'FLOW-CI-20260909-cold-r3-context.json')));
 const r=(await body(c.getPipelineRun(ORG,PID,run))).pipelineRun;
 const jobs=(r.stages||[]).flatMap(s=>s.stageInfo?.jobs||[]);need(jobs.length===1,'JOB_COUNT_MISMATCH');const j=jobs[0];
 const q=typeof j.params==='string'?JSON.parse(j.params):j.params;
 need(String(q.BUILD_NUMBER)===run&&String(q.PIPELINE_ID)===PID&&q.ENGINE_TASK_SIGN==='cloud_ci-api_ci','PLATFORM_BINDING_MISMATCH');
 need(q.steps.length===3&&q.steps[0].CI_RUNTIME_VERSION==='jdk21','STEP_CONTRACT_MISMATCH');
 const commands=q.steps.filter(s=>typeof s.command==='string');need(commands.length===2,'COMMAND_COUNT_MISMATCH');
 const local=['FLOW-CI-20260909-build-step-r3.sh','FLOW-CI-20260909-final-gate-r3.sh'];
 const cmdChecks=commands.map((s,i)=>{const expected=fs.readFileSync(path.join(root,local[i]),'utf8');need(normalize(s.command)===normalize(expected),'COMMAND_BYTES_MISMATCH');return {name:s.name,command_sha256:sha(s.command),terminal_newline_normalized_sha256:sha(normalize(s.command))}});
 need(q.steps[1].ARCHIVE_PATH==='_flow_ci_export/'||JSON.stringify(q.steps[1].ARCHIVE_PATH)==='["_flow_ci_export/"]','UPLOAD_PATH_MISMATCH');
 const sources=q.sources.map(s=>({repo:s.data.repo,branch:s.data.branch,commit:s.data.commitId}));
 need(sources.length===1&&sources[0].repo===ctx.source.repo_url&&sources[0].branch==='develop'&&/^[0-9a-f]{40}$/.test(sources[0].commit),'SOURCE_MISMATCH');
 const provenance={queriedAt:new Date().toISOString(),pipeline:PID,run:Number(run),status:r.status,job:j.id,jobStatus:j.status,engineTaskSign:q.ENGINE_TASK_SIGN,platformRun:String(q.BUILD_NUMBER),sources,cmdChecks,ticketSha256:ctx.ticket_sha256};
 if(!['SUCCESS','FAIL','FAILED','CANCELED','CANCELLED'].includes(r.status)){console.log(JSON.stringify({...provenance,downloaded:false},null,2));return;}
 const files=j.actions.filter(a=>a.type==='GetPipelineArtifactUrl').flatMap(a=>a.params.files||[]);need(files.length===1&&files[0].fileName==='Artifacts_5256653.tgz','ARTIFACT_LOCATOR_MISMATCH');
 const f=files[0],b=await body(c.getPipelineArtifactUrl(ORG,new SDK.GetPipelineArtifactUrlRequest(f)));
 const u=new URL(b.fileUrl);need(u.protocol==='https:'&&!u.username&&!u.password&&(/\.aliyuncs\.com$/.test(u.hostname)||/\.aliyun\.com$/.test(u.hostname)),'UNTRUSTED_DOWNLOAD_HOST');
 const dir='/tmp/cyf-flow-ci-download-run'+run;fs.mkdirSync(dir,{mode:0o700});
 const dest=path.join(dir,f.fileName),h=crypto.createHash('sha256');let bytes=0;
 const res=await fetch(u,{redirect:'error',signal:AbortSignal.timeout(300000)});need(res.status===200,'DOWNLOAD_HTTP_FAILURE');
 await pipeline(Readable.fromWeb(res.body),new Transform({transform(chunk,enc,cb){bytes+=chunk.length;if(bytes>1024*1024*1024){cb(Error('DOWNLOAD_SIZE_LIMIT'));return}h.update(chunk);cb(null,chunk)}}),fs.createWriteStream(dest,{flags:'wx',mode:0o600}));
 Object.assign(provenance,{artifact:f,localPath:dest,bytes,sha256:h.digest('hex'),urlRequestId:b.requestId});
 fs.writeFileSync(path.join(dir,'download-receipt.json'),JSON.stringify(provenance,null,2)+'\n',{flag:'wx',mode:0o600});console.log(JSON.stringify(provenance,null,2));
}
main().catch(e=>{console.error(JSON.stringify({error:/^[A-Z_]+$/.test(e.message)?e.message:'SANITIZED_FETCH_FAILURE',action:'Read-only reconcile, no cloud retry'}));process.exitCode=1});
