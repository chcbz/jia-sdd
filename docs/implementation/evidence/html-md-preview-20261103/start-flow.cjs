// Scoped one-shot start. Existing flow-control 1.1.0 stops before sending when
// >100 history entries exist. Reconcile ALL pages, preserving frozen inputs.
const fs = require('node:fs')
const path = require('node:path')
const { createHash } = require('node:crypto')
const { execFileSync } = require('node:child_process')
const SDK = require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625')
const { canonicalFlowText } = require('/home/isp/wsps/cyf/ops/ci/aliyun-flow/flow-control.cjs')
const org = '5fb7d76ee6f9d07f148529c7', pipeline = '4403172', repo = 'https://gitee.com/chcbz/cyf-web-kit.git'
const dir = path.resolve(process.env.FLOW_START_EVIDENCE_DIR || __dirname)
const save = (name, value) => fs.writeFileSync(path.join(dir, name), JSON.stringify(value, null, 2) + '\n')
const credentials = JSON.parse(fs.readFileSync('/root/.codex/auth.json', 'utf8'))
const client = new SDK.default({ accessKeyId: credentials.ALIBABA_CLOUD_ACCESS_KEY_ID, accessKeySecret: credentials.ALIBABA_CLOUD_ACCESS_KEY_SECRET, endpoint: 'devops.cn-hangzhou.aliyuncs.com', connectTimeout: 10000, readTimeout: 25000 })
const body = async promise => { const r = (await promise).body; if (r.success !== true) throw Error('API_FAILURE'); return r }
async function main () {
  if (fs.existsSync(path.join(dir, 'flow-start-attempt.json'))) throw Error('ALREADY_ATTEMPTED_RECONCILE_ONLY')
  const config = (await body(client.getPipeline(org, pipeline))).pipeline
  const previous = JSON.parse(fs.readFileSync(path.join(dir, 'flow-config-summary.json'))).configuration
  const hash = createHash('sha256').update(canonicalFlowText(config.pipelineConfig.flow)).digest('hex')
  if (hash !== previous.canonicalConfigSha256) throw Error('CONFIG_CHANGED')
  const ids = []; let nextToken
  do {
    const page = await body(client.listPipelineRuns(org, pipeline, new SDK.ListPipelineRunsRequest({ maxResults: 100, nextToken })))
    for (const run of page.pipelineRuns) { ids.push(String(run.pipelineRunId)); if (['RUNNING', 'QUEUED', 'WAITING'].includes(run.status)) throw Error('ACTIVE_RUN_COORDINATION_REQUIRED') }
    nextToken = page.nextToken || undefined
  } while (nextToken)
  const commit = execFileSync('git', ['-C', '/home/isp/wsps/worktrees/html-md-preview-web-20261103', 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim()
  const remote = execFileSync('git', ['-C', '/home/isp/wsps/worktrees/html-md-preview-web-20261103', 'ls-remote', 'origin', 'refs/heads/develop'], { encoding: 'utf8' }).split(/\s/)[0]
  if (commit !== remote) throw Error('SOURCE_MOVED')
  const context = { schemaVersion: 1, kind: 'cyf.flow.start-context.v1', org, pipeline, pipelineName: config.name, canonicalConfigSha256: hash, existingRunIds: ids, requestStartedAt: new Date().toISOString(), params: { runningBranchs: { [repo]: 'develop' } }, expectedSources: [{ repo, branch: 'develop', commit }] }
  save('flow-start-context.json', context)
  save('flow-start-attempt.json', { at: context.requestStartedAt, org, pipeline, commit, operation: 'start-once' })
  try {
    const result = await body(client.startPipelineRun(org, pipeline, new SDK.StartPipelineRunRequest({ params: JSON.stringify(context.params) })))
    if (!result.pipelineRunId) throw Error('NO_RETURNED_ID')
    const safe = { at: new Date().toISOString(), org, pipeline, returnedRunId: String(result.pipelineRunId), commit, state: 'RETURNED_ID_VERIFY_SOURCE', existingRunCount: ids.length }
    save('flow-start-result.json', safe); console.log(JSON.stringify(safe))
  } catch (_) {
    save('flow-start-result.json', { at: new Date().toISOString(), org, pipeline, commit, state: 'UNKNOWN_RECONCILE_DO_NOT_RETRY' })
    throw Error('START_UNKNOWN_RECONCILE_ONLY')
  }
}
main().catch(error => { console.error(JSON.stringify({ error: /^[A-Z_]+$/.test(error.message) ? error.message : 'CONTROL_FAILURE', action: 'read-only reconciliation; do not blindly repeat' })); process.exitCode = 1 })
