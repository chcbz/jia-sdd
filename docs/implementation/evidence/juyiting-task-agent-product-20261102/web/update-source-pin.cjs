// Only advance the existing immutable candidate guard; preserve all CI work and host separation.
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const SDK=require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625');
const {configSummary,commandUpdate}=require('/home/isp/wsps/cyf/ops/ci/aliyun-flow/flow-control.cjs');
const a=JSON.parse(fs.readFileSync('/root/.codex/auth.json'));
const c=new SDK.default({accessKeyId:a.ALIBABA_CLOUD_ACCESS_KEY_ID||a.accessKeyId,accessKeySecret:a.ALIBABA_CLOUD_ACCESS_KEY_SECRET||a.accessKeySecret,endpoint:'devops.cn-hangzhou.aliyuncs.com',regionId:'cn-hangzhou'});
const org='5fb7d76ee6f9d07f148529c7',pipeline='4403172',dir=__dirname;
async function main(){
 if(fs.existsSync(path.join(dir,'config-update-attempt.json')))throw Error('Already attempted; reconcile read-only');
 let token;do{const r=await c.listPipelineRuns(org,pipeline,new SDK.ListPipelineRunsRequest({maxResults:100,nextToken:token}));if(!r.body.success)throw Error('read failed');if(r.body.pipelineRuns.some(x=>!['SUCCESS','FAIL','CANCELED','CANCELLED','SKIP'].includes(x.status)))throw Error('Active/unknown run; no configuration change');token=r.body.nextToken;}while(token);
 const p=(await c.getPipeline(org,pipeline)).body.pipeline,before=configSummary(p);
 if(before.canonicalConfigSha256!=='0e738b29638713e653a0b3114329adb95c332d23b901237b17d16258bf2313eb')throw Error('Configuration changed; no write');
 const old='test "$CI_COMMIT_SHA" = 5470363fc33d7689890763a54eb0ee23ac8d84d2',next='test "$CI_COMMIT_SHA" = 339f3be8af09e09ba46e0b29a8e68d8fc30d8576';
 const f=p.pipelineConfig.flow;if(f.split(old).length!==2)throw Error('Pin is not unique');
 if(/password:|accessKeySecret:|access_key_secret:|authorization:/i.test(f))throw Error('Sensitive backup requires separate handling');
 fs.writeFileSync(path.join(dir,'flow-before.yaml'),f,{mode:0o600,flag:'wx'});
 const candidate=path.join(dir,'flow-candidate.yaml');fs.writeFileSync(candidate,f.replace(old,next),{mode:0o600,flag:'wx'});
 const sha=crypto.createHash('sha256').update(fs.readFileSync(candidate)).digest('hex');
 fs.writeFileSync(path.join(dir,'config-update-attempt.json'),JSON.stringify({at:new Date().toISOString(),before,candidateSha256:sha})+'\n',{flag:'wx'});
 const result=await commandUpdate(c,{org,pipeline,name:before.name,candidate,'candidate-sha256':sha,allowlist:path.join(dir,'flow-allowlist.json')});
 fs.writeFileSync(path.join(dir,'config-update-result.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result));
}
main().catch(()=>{console.error('Source pin update stopped; reconcile read-only, no write retry');process.exitCode=1});
