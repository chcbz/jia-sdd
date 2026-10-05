'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const test = require('node:test');
const source = fs.readFileSync(process.env.FLOW_CONTROL_TEST_SOURCE || path.join(__dirname, '..', 'flow-control.cjs'), 'utf8');
const start = source.indexOf('async function listRuns(');
assert.ok(start >= 0);
const end = source.indexOf('\n}', start) + 2;
const listRuns = vm.runInNewContext(`(${source.slice(start, end)})`, {
  SDK: { ListPipelineRunsRequest: class { constructor(value) { Object.assign(this, value); } } },
  readBody: async value => (await value).body,
  body: async value => (await value).body,
  fail: code => { throw Object.assign(new Error(code), { code }); }
});
const row = id => ({ pipelineRunId: id, status: 'SUCCESS' });
const ok = value => Promise.resolve({ body: { success: true, ...value } });
test('run listing reconciles every page instead of treating a 100-run history as a blocker', async () => {
  const requests = [];
  const client = { listPipelineRuns: (org, pipeline, request) => {
    requests.push({ org, pipeline, ...request });
    return ok(request.nextToken ? { pipelineRuns: [row(1)] } : { pipelineRuns: [row(2)], nextToken: 'page2' });
  } };
  const value = await listRuns(client, 'org', 'pipeline', 100);
  assert.deepEqual(Array.from(value.runs, r => r.pipelineRunId), [2, 1]);
  assert.equal(value.nextToken, null);
  assert.equal(requests.length, 2);
  assert.equal(requests[1].nextToken, 'page2');
  assert.ok(requests.every(r => r.org === 'org' && r.pipeline === 'pipeline' && r.maxResults === 100));
});
test('repeated pagination token fails closed without sending writes', async () => {
  let calls = 0;
  const client = { listPipelineRuns: () => ok({ pipelineRuns: [row(++calls)], nextToken: 'loop' }) };
  await assert.rejects(listRuns(client, 'org', 'pipeline', 100), { code: 'RUN_LIST_PAGINATION_INVALID' });
  assert.equal(calls, 2);
});
test('overlapping run identities require fresh reconciliation, not silent deduplication', async () => {
  let calls = 0;
  const client = { listPipelineRuns: () => ok({ pipelineRuns: [row(2)], nextToken: ++calls === 1 ? 'page2' : undefined }) };
  await assert.rejects(listRuns(client, 'org', 'pipeline', 100), { code: 'RUN_LIST_DUPLICATE_ID' });
});
test('later page transport failure never returns an incomplete successful history', async () => {
  const client = { listPipelineRuns: (org, pipeline, request) => request.nextToken
    ? Promise.reject(new Error('read failed')) : ok({ pipelineRuns: [row(2)], nextToken: 'page2' }) };
  await assert.rejects(listRuns(client, 'org', 'pipeline', 100), /read failed/);
});
test('malformed later-page run id fails closed', async () => {
  const client = { listPipelineRuns: (org, pipeline, request) => ok(request.nextToken
    ? { pipelineRuns: [{ status: 'SUCCESS' }] } : { pipelineRuns: [row(2)], nextToken: 'page2' }) };
  await assert.rejects(listRuns(client, 'org', 'pipeline', 100), { code: 'RUN_LIST_ID_INVALID' });
});
