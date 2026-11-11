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

(async()=>{const log=(await client.logPipelineJobRun('5fb7d76ee6f9d07f148529c7','4403172','544066189','361')).body.log;const content=redact(log.content).split('\n').filter(l=>!l.startsWith('declare -x ')).join('\n');const result={queriedAt:new Date().toISOString(),run:361,job:544066189,more:log.more,outputTruncated:false,environmentDumpOmitted:true,content};fs.writeFileSync('/home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/optimization/evidence/user-facing-copy-cleanup-20261027/ci-2/log-full.json',JSON.stringify(result,null,2));console.log(JSON.stringify({more:log.more,chars:content.length}));})().catch(()=>{console.error('LOG_QUERY_FAILED');process.exitCode=1});