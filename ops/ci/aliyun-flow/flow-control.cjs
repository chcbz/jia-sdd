#!/usr/bin/env node
'use strict';

/*
 * Versioned, narrow Aliyun Flow control plane.
 *
 * One invocation performs exactly one named operation.  It intentionally has
 * no mutation beyond the named operation and never emits credentials, raw API
 * responses, or candidate configuration contents.
 */
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const SDK = require('/root/.codex/skills/aliyun-pipeline/node_modules/@alicloud/devops20210625');

const CLI_VERSION = '1.0.0';
const ENDPOINT = 'devops.cn-hangzhou.aliyuncs.com';
const REGION = 'cn-hangzhou';
const SHA256 = /^[a-f0-9]{64}$/;
const IDENTIFIER = /^[A-Za-z0-9._:-]{1,160}$/;
const RUN_ID = /^[1-9][0-9]*$/;
const COMMANDS = new Set(['config', 'list', 'create', 'update', 'start', 'status']);
const OPTION_NAMES = {
  config: new Set(['org', 'pipeline', 'allowlist', 'credentials-file']),
  list: new Set(['org', 'pipeline', 'allowlist', 'credentials-file']),
  status: new Set(['org', 'pipeline', 'run', 'allowlist', 'credentials-file']),
  create: new Set(['org', 'name', 'candidate', 'candidate-sha256', 'allowlist', 'credentials-file']),
  update: new Set(['org', 'pipeline', 'name', 'candidate', 'candidate-sha256', 'allowlist', 'credentials-file']),
  start: new Set(['org', 'pipeline', 'context', 'context-sha256', 'allowlist', 'credentials-file']),
};
class ControlError extends Error {
  constructor(code) {
    super(code);
    this.code = code;
  }
}

function fail(code) { throw new ControlError(code); }
function sha256(bytes) { return crypto.createHash('sha256').update(bytes).digest('hex'); }
function now() { return new Date().toISOString(); }
function requireValue(value, code) { if (!value) fail(code); return value; }
function requireIdentifier(value, code) {
  if (!IDENTIFIER.test(String(value || ''))) fail(code);
  return String(value);
}
function requireSha256(value, code) {
  if (!SHA256.test(String(value || ''))) fail(code);
  return String(value);
}
function isRecord(value) { return value !== null && typeof value === 'object' && !Array.isArray(value); }

function parseArgs(argv) {
  if (argv.length === 1 && argv[0] === '--version') return { command: 'version', options: {} };
  const command = argv.shift();
  if (!COMMANDS.has(command)) fail('UNSUPPORTED_COMMAND');
  const options = {};
  while (argv.length) {
    const token = argv.shift();
    if (!token.startsWith('--')) fail('INVALID_ARGUMENT');
    const key = token.slice(2);
    if (!key || !OPTION_NAMES[command].has(key) || Object.prototype.hasOwnProperty.call(options, key)) fail('INVALID_ARGUMENT');
    const value = argv.shift();
    if (!value || value.startsWith('--')) fail('MISSING_ARGUMENT_VALUE');
    options[key] = value;
  }
  return { command, options };
}

function readJsonFile(file, code) {
  try {
    const text = fs.readFileSync(path.resolve(file), 'utf8');
    const parsed = JSON.parse(text);
    if (!isRecord(parsed)) fail(code);
    return parsed;
  } catch (error) {
    if (error instanceof ControlError) throw error;
    fail(code);
  }
}

function credentials(options) {
  const source = options['credentials-file']
    ? readJsonFile(options['credentials-file'], 'INVALID_CREDENTIALS_FILE')
    : process.env;
  const accessKeyId = source.ALIBABA_CLOUD_ACCESS_KEY_ID || source.accessKeyId || source.access_key_id;
  const accessKeySecret = source.ALIBABA_CLOUD_ACCESS_KEY_SECRET || source.accessKeySecret || source.access_key_secret;
  const securityToken = source.ALIBABA_CLOUD_SECURITY_TOKEN || source.securityToken || source.security_token;
  if (typeof accessKeyId !== 'string' || !accessKeyId.trim() ||
      typeof accessKeySecret !== 'string' || !accessKeySecret.trim() ||
      (securityToken !== undefined && (typeof securityToken !== 'string' || !securityToken.trim()))) {
    fail('CREDENTIALS_UNAVAILABLE');
  }
  const config = {
    accessKeyId,
    accessKeySecret,
    endpoint: ENDPOINT,
    regionId: REGION,
    connectTimeout: 10000,
    readTimeout: 25000,
  };
  if (securityToken) config.securityToken = securityToken;
  return new SDK.default(config);
}

function allowlisted(options, org, pipeline) {
  if (!options.allowlist) return;
  const allowlist = readJsonFile(options.allowlist, 'INVALID_ALLOWLIST');
  const organizations = Array.isArray(allowlist.organizations) ? allowlist.organizations : [];
  const pipelines = Array.isArray(allowlist.pipelines) ? allowlist.pipelines : [];
  if (!organizations.every(value => typeof value === 'string') ||
      !pipelines.every(item => isRecord(item) && typeof item.org === 'string' && typeof item.pipeline === 'string')) {
    fail('INVALID_ALLOWLIST');
  }
  if (!organizations.includes(org)) fail('ORG_NOT_ALLOWLISTED');
  if (pipeline !== null && !pipelines.some(item => item.org === org && item.pipeline === pipeline)) {
    fail('PIPELINE_NOT_ALLOWLISTED');
  }
}

function scope(options, requiresPipeline) {
  const org = requireIdentifier(options.org, 'INVALID_ORG');
  const pipeline = requiresPipeline ? requireIdentifier(options.pipeline, 'INVALID_PIPELINE') : null;
  allowlisted(options, org, pipeline);
  return { org, pipeline };
}

function candidate(options) {
  const expected = requireSha256(options['candidate-sha256'], 'INVALID_CANDIDATE_SHA256');
  const candidateFile = requireValue(options.candidate, 'MISSING_CANDIDATE_FILE');
  let content;
  try { content = fs.readFileSync(path.resolve(candidateFile)); } catch (_) { fail('CANDIDATE_UNREADABLE'); }
  if (sha256(content) !== expected) fail('CANDIDATE_SHA256_MISMATCH');
  return { content: content.toString('utf8'), sha256: expected };
}

function pipelineConfig(pipeline) {
  const config = pipeline && pipeline.pipelineConfig;
  if (!isRecord(config) || typeof config.flow !== 'string') fail('PIPELINE_CONFIGURATION_UNAVAILABLE');
  return config;
}

function configSummary(pipeline) {
  const config = pipelineConfig(pipeline);
  const sources = Array.isArray(config.sources) ? config.sources : [];
  return {
    name: typeof pipeline.name === 'string' ? pipeline.name : null,
    configSha256: sha256(Buffer.from(config.flow, 'utf8')),
    configBytes: Buffer.byteLength(config.flow, 'utf8'),
    sourceCount: sources.length,
    sourceKinds: sources.map(source => isRecord(source) && typeof source.type === 'string' ? source.type : 'unknown'),
  };
}

function runSummary(run) {
  return {
    id: run.pipelineRunId === undefined ? null : String(run.pipelineRunId),
    status: typeof run.status === 'string' ? run.status : 'UNKNOWN',
    startTime: run.startTime === undefined ? null : run.startTime,
  };
}

async function body(request) {
  try {
    const response = await request;
    const result = response && response.body;
    if (!result || result.success === false || result.errorCode) fail('FLOW_API_REJECTED');
    return result;
  } catch (error) {
    if (error instanceof ControlError) throw error;
    fail('FLOW_API_UNAVAILABLE');
  }
}

async function getPipeline(client, org, pipeline) {
  const result = await body(client.getPipeline(org, pipeline));
  if (!isRecord(result.pipeline)) fail('PIPELINE_NOT_FOUND');
  return result.pipeline;
}

async function listRuns(client, org, pipeline, maxResults) {
  const result = await body(client.listPipelineRuns(
    org, pipeline, new SDK.ListPipelineRunsRequest({ maxResults })
  ));
  if (!Array.isArray(result.pipelineRuns)) fail('RUN_LIST_UNAVAILABLE');
  return { runs: result.pipelineRuns, nextToken: result.nextToken || null };
}

function frozenStartContext(options, org, pipeline) {
  const expected = requireSha256(options['context-sha256'], 'INVALID_CONTEXT_SHA256');
  const contextFile = requireValue(options.context, 'MISSING_CONTEXT_FILE');
  let bytes;
  try { bytes = fs.readFileSync(path.resolve(contextFile)); } catch (_) { fail('CONTEXT_UNREADABLE'); }
  if (sha256(bytes) !== expected) fail('CONTEXT_SHA256_MISMATCH');
  let context;
  try { context = JSON.parse(bytes.toString('utf8')); } catch (_) { fail('INVALID_CONTEXT'); }
  if (!isRecord(context) || context.schemaVersion !== 1 || context.kind !== 'cyf.flow.start-context.v1' ||
      context.org !== org || context.pipeline !== pipeline || !Array.isArray(context.existingRunIds) ||
      typeof context.requestStartedAt !== 'string' || !isRecord(context.params) ||
      !context.existingRunIds.every(id => RUN_ID.test(String(id)))) fail('INVALID_CONTEXT');
  if (Number.isNaN(Date.parse(context.requestStartedAt))) fail('INVALID_CONTEXT');
  return { context, sha256: expected };
}

async function commandConfig(client, options) {
  const { org, pipeline } = scope(options, true);
  return { operation: 'config', org, pipeline, configuration: configSummary(await getPipeline(client, org, pipeline)) };
}

async function commandList(client, options) {
  const { org, pipeline } = scope(options, true);
  const listed = await listRuns(client, org, pipeline, 100);
  return { operation: 'list', org, pipeline, runs: listed.runs.map(runSummary), nextToken: listed.nextToken };
}

async function commandStatus(client, options) {
  const { org, pipeline } = scope(options, true);
  const run = requireIdentifier(options.run, 'INVALID_RUN');
  const result = await body(client.getPipelineRun(org, pipeline, run));
  if (!isRecord(result.pipelineRun)) fail('RUN_NOT_FOUND');
  return { operation: 'status', org, pipeline, run: runSummary(result.pipelineRun) };
}

async function commandCreate(client, options) {
  const { org } = scope(options, false);
  const name = requireIdentifier(options.name, 'INVALID_PIPELINE_NAME');
  const reviewed = candidate(options);
  const created = await body(client.createPipeline(org, new SDK.CreatePipelineRequest({ name, content: reviewed.content })));
  // The generated DevOps SDK preserves the service's historical `pipelinId` spelling.
  const pipeline = requireIdentifier(created.pipelinId, 'CREATE_RESULT_UNAVAILABLE');
  const readback = configSummary(await getPipeline(client, org, pipeline));
  if (readback.name !== name || readback.configSha256 !== reviewed.sha256) fail('CREATE_READBACK_MISMATCH');
  return { operation: 'create', org, pipeline, candidateSha256: reviewed.sha256, readback };
}

async function commandUpdate(client, options) {
  const { org, pipeline } = scope(options, true);
  const name = requireIdentifier(options.name, 'INVALID_PIPELINE_NAME');
  const reviewed = candidate(options);
  const before = configSummary(await getPipeline(client, org, pipeline));
  await body(client.updatePipeline(org, new SDK.UpdatePipelineRequest({ pipelineId: pipeline, name, content: reviewed.content })));
  const readback = configSummary(await getPipeline(client, org, pipeline));
  if (readback.name !== name || readback.configSha256 !== reviewed.sha256) fail('UPDATE_READBACK_MISMATCH');
  return { operation: 'update', org, pipeline, candidateSha256: reviewed.sha256, before, readback };
}

async function commandStart(client, options) {
  const { org, pipeline } = scope(options, true);
  const frozen = frozenStartContext(options, org, pipeline);
  const before = await listRuns(client, org, pipeline, 100);
  if (before.nextToken !== null) fail('RUN_HISTORY_REQUIRES_RECONCILIATION');
  const existingRunIds = before.runs.map(run => String(run.pipelineRunId)).sort();
  const frozenRunIds = frozen.context.existingRunIds.map(String).sort();
  if (JSON.stringify(existingRunIds) !== JSON.stringify(frozenRunIds)) fail('START_CONTEXT_STALE');
  const requestStartedAt = now();
  const started = await body(client.startPipelineRun(
    org, pipeline, new SDK.StartPipelineRunRequest({ params: JSON.stringify(frozen.context.params) })
  ));
  return {
    operation: 'start', org, pipeline, contextSha256: frozen.sha256,
    existingRunIds, requestStartedAt,
    runId: started.pipelineRunId === undefined ? null : String(started.pipelineRunId),
  };
}

async function main() {
  const parsed = parseArgs(process.argv.slice(2));
  if (parsed.command === 'version') {
    process.stdout.write(JSON.stringify({ version: CLI_VERSION }) + '\n');
    return;
  }
  const client = credentials(parsed.options);
  const handlers = {
    config: commandConfig, list: commandList, create: commandCreate,
    update: commandUpdate, start: commandStart, status: commandStatus,
  };
  const result = await handlers[parsed.command](client, parsed.options);
  process.stdout.write(JSON.stringify({ version: CLI_VERSION, at: now(), ...result }) + '\n');
}

main().catch(error => {
  const code = error instanceof ControlError ? error.code : 'CONTROL_FAILURE';
  process.stderr.write(JSON.stringify({ version: CLI_VERSION, error: code, action: 'reconcile read-only; do not repeat a write' }) + '\n');
  process.exitCode = 2;
});
