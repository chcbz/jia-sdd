const fs = require('fs')
const SDK = require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625')
const a = JSON.parse(fs.readFileSync('/root/.codex/auth.json','utf8'))
const client = new SDK.default({accessKeyId:a.ALIBABA_CLOUD_ACCESS_KEY_ID || a.accessKeyId,accessKeySecret:a.ALIBABA_CLOUD_ACCESS_KEY_SECRET || a.accessKeySecret,endpoint:'devops.cn-hangzhou.aliyuncs.com',regionId:'cn-hangzhou'})
client.getPipeline('5fb7d76ee6f9d07f148529c7',process.argv[2] || '4403172').then(r=>{
 if(!r.body.success) throw Error('read failed')
 const c=r.body.pipeline.pipelineConfig;const f=c.flow
 console.log(JSON.stringify({checkedAt:new Date().toISOString(),sourceSummary:c.sources?.map(s=>({type:s.type})),safetyLines:f.split('\n').filter(l=>/triggerEvents|branchesFilter|branch:|step:|timeoutMinutes|CI_COMMIT_REF_NAME|ssh |VMDeploy|deploy:|host:|upload|autoTrigger|enable:/.test(l)),hostDeployStep:/step:\s*(VMDeploy|SSH)/.test(f)},null,2))
}).catch(()=>{console.error('configuration read failed');process.exitCode=1})
