// Fixed-scope control only. Never persist/print credentials or raw API errors.
const fs=require('fs'), crypto=require('crypto');
const SDK=require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625');
const ORG='5fb7d76ee6f9d07f148529c7', NAME='cyf-flow-ci-maven-auth-5256653';
const BASE='https://packages.aliyun.com/'+ORG+'/maven/2049636-release-r6d3t8';
const config=JSON.parse(fs.readFileSync('/root/.aliyun/config.json','utf8'));
const p=config.profiles.find(x=>x.name===config.current);
const c=new SDK.default({accessKeyId:p.access_key_id,accessKeySecret:p.access_key_secret,endpoint:'devops.cn-hangzhou.aliyuncs.com',regionId:'cn-hangzhou',readTimeout:25000,connectTimeout:10000});
async function body(q){const b=(await q).body;if(!b||b.success===false||b.errorCode)throw Error('API_FAILURE');return b;}
async function credentials(){
 const b=await body(c.getPipeline(ORG,'1466118'));
 const flow=b.pipeline.pipelineConfig.flow;
 for(const line of flow.split('\n')){
  const m=line.match(/^\s*command:\s*(".*")\s*$/);if(!m)continue;
  const cmd=JSON.parse(m[1]);if(!cmd.includes('init.gradle'))continue;
  const u=cmd.match(/^repoUsername\s*=\s*(.+)$/m),p=cmd.match(/^repoPassword\s*=\s*(.+)$/m);
  if(!u||!p)continue;
  const vals=[u[1].trim(),p[1].trim()];
  if(vals.some(v=>!v||/[\r\n]/.test(v)||v.includes('${')||v.includes('***')))throw Error('INVALID_EXISTING_AUTH');
  return vals;
 }throw Error('AUTH_NOT_FOUND');
}
async function groups(){let nextToken,all=[];do{
 const b=await body(c.listVariableGroups(ORG,new SDK.ListVariableGroupsRequest({maxResults:100,nextToken})));
 if(!Array.isArray(b.variableGroups))throw Error('INVALID_GROUP_LIST');
 all.push(...b.variableGroups);nextToken=b.nextToken;
}while(nextToken);return all;}
function safe(g){return {id:g.id,name:g.name,variables:(g.variables||[]).map(v=>({name:v.name,isEncrypted:v.isEncrypted})),relatedPipelines:(g.relatedPipelines||[]).map(p=>({id:p.id}))};}
async function main(){const mode=process.argv[2];
 if(mode==='list'){console.log(JSON.stringify({queriedAt:new Date().toISOString(),groups:(await groups()).map(safe)},null,2));return;}
 if(mode==='hash'){
  const [u,p]=await credentials(),auth='Basic '+Buffer.from(u+':'+p).toString('base64');let out=[];
  for(const ext of ['pom','jar']){
   const url=BASE+'/org/opencv/opencv/4.5.5/opencv-4.5.5.'+ext;
   const res=await fetch(url,{headers:{Authorization:auth},redirect:'error',signal:AbortSignal.timeout(120000)});
   if(res.status!==200)throw Error('ARTIFACT_HTTP_FAILURE');
   let bytes=0;const hash=crypto.createHash('sha256');let prefix=Buffer.alloc(0);
   for await(const chunk of res.body){bytes+=chunk.length;if(bytes>128*1024*1024)throw Error('ARTIFACT_SIZE_LIMIT');hash.update(chunk);if(prefix.length<8)prefix=Buffer.concat([prefix,Buffer.from(chunk)]).subarray(0,8);}
   if(ext==='jar'&&(bytes<100||prefix[0]!==0x50||prefix[1]!==0x4b))throw Error('INVALID_JAR_SIGNATURE');
   out.push({extension:ext,status:res.status,bytes,sha256:hash.digest('hex')});
  }
  console.log(JSON.stringify({verifiedAt:new Date().toISOString(),repository:BASE,coordinate:'org.opencv:opencv:4.5.5',artifacts:out,credentialsPersisted:false,artifactPersisted:false,method:'authenticated streaming GET; redirects rejected'},null,2));return;
 }
 if(mode==='create'){
  const existing=await groups();if(existing.some(g=>g.name===NAME))throw Error('EXISTING_NAME_RECONCILE_ONLY');
  const [username,password]=await credentials();
  console.log(JSON.stringify({operation:'create-intent',name:NAME,requestedAt:new Date().toISOString(),existingGroupIds:existing.map(g=>g.id)}));
  const b=await body(c.createVariableGroup(ORG,new SDK.CreateVariableGroupRequest({name:NAME,description:'Dedicated manual no-deploy CI5256653 Maven consumer authentication; permissions inherited, not asserted read-only.',variables:JSON.stringify([{name:'CYF_MAVEN_USERNAME',value:username,isEncrypted:true},{name:'CYF_MAVEN_PASSWORD',value:password,isEncrypted:true}])})));
  if(!b.variableGroupId)throw Error('MISSING_CREATED_ID_RECONCILE_ONLY');
  console.log(JSON.stringify({operation:'created',variableGroupId:b.variableGroupId,requestId:b.requestId}));
  const g=(await body(c.getVariableGroup(ORG,String(b.variableGroupId)))).variableGroup;
  if(!g||g.name!==NAME||g.variables.length!==2||g.variables.some(v=>!v.isEncrypted)||g.relatedPipelines?.length)throw Error('GROUP_READBACK_MISMATCH');
  console.log(JSON.stringify({operation:'verified',group:safe(g)},null,2));return;
 }throw Error('UNSUPPORTED_MODE');
}
main().catch(()=>{console.error(JSON.stringify({error:'CONTROL_OPERATION_FAILED',action:'Read-only reconcile; do not repeat ambiguous writes.'}));process.exitCode=1;});
