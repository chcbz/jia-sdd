'use strict';
// Contract-only check. Does not invoke application code, network, build, DB or installer.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const root = path.resolve(__dirname, '../../../..');
const base = path.join(root, 'specs/juyiting-skill-execution');
const Ajv = require(path.join(root, 'web/node_modules/ajv'));
const load = n => JSON.parse(fs.readFileSync(path.join(base, 'fixtures', n), 'utf8'));
const schema = load('management-contract-v1.schema.json');
const fixtures = load('management-contract-v1.examples.json');
const behavior = load('management-contract-v1.behavior.json');
const errors = [];
const check = (condition, message) => { if (!condition) errors.push(message); };
const ajv = new Ajv({ allErrors: true, coerceTypes: false, removeAdditional: false, useDefaults: false });
ajv.addSchema(schema);
check(ajv.validateSchema(schema), 'schema meta-validation');
const names = new Set();
for (const c of fixtures.cases) {
  check(!names.has(c.name), `duplicate fixture: ${c.name}`); names.add(c.name);
  const validate = ajv.compile({ $ref: schema.$id + '#/definitions/' + c.definition });
  check(validate(c.value) === c.valid, `${c.name}: ${JSON.stringify(validate.errors)}`);
  if (c.headers?.['X-Request-Id']) check(c.headers['X-Request-Id'] === c.value.requestId, `${c.name}: header requestId`);
  if (c.valid && c.definition === 'HttpError') check(behavior.errorStatus[c.value.code] === c.httpStatus, `${c.name}: error status mapping`);
}
function canonical(v) {
  if (v === null || typeof v === 'boolean') return JSON.stringify(v);
  if (typeof v === 'number') {
    if (!Number.isSafeInteger(v) || Object.is(v, -0)) throw new Error('noncanonical number');
    return JSON.stringify(v);
  }
  if (typeof v === 'string') {
    for (const c of v) { const n = c.codePointAt(0); if (n >= 0xd800 && n <= 0xdfff) throw new Error('unpaired surrogate'); }
    return JSON.stringify(v);
  }
  if (Array.isArray(v)) return '[' + v.map(canonical).join(',') + ']';
  return '{' + Object.keys(v).sort((a, b) => Buffer.compare(Buffer.from(a), Buffer.from(b)))
    .map(k => canonical(k) + ':' + canonical(v[k])).join(',') + '}';
}
const hash = (domain, v) => crypto.createHash('sha256').update(domain + '\0', 'utf8').update(canonical(v), 'utf8').digest('hex');
for (const v of fixtures.digestVectors) {
  check(canonical(v.value) === v.canonicalUtf8, `canonical bytes: ${v.domain}`);
  check(hash(v.domain, v.value) === v.sha256, `digest: ${v.domain}`);
}
for (const c of fixtures.cases.filter(c => c.valid)) {
  const d = c.value.data;
  if (c.definition === 'Command') {
    const { commandSha256, deliveryEpoch, ...stable } = d;
    check(hash('cyf.skill.command.v2', stable) === commandSha256, `${c.name}: command hash`);
    check(d.fencingToken === d.skillRevision, `${c.name}: revision fence`);
    if (d.phase === 'PREPARE') check(d.downloadPath === `/internal/agent/skill-installations/${d.target.skillInstallationId}/package`, `${c.name}: target path`);
    if (d.phase === 'ACTIVATE') {
      const selected = Object.fromEntries(['skillChangeId', 'attempt', 'source', 'target', 'approvedPermissionsSha256'].map(k => [k, d[k]]));
      check(hash('cyf.skill.prepared.v1', selected) === d.preparedSha256, `${c.name}: prepared binding`);
    }
  }
  if (c.definition === 'Result') {
    const { resultSha256, ...stable } = d;
    check(hash('cyf.skill.result.v2', stable) === resultSha256, `${c.name}: result hash`);
  }
}
const codes = [...schema.definitions.HttpError.properties.code.enum].sort();
check(JSON.stringify(codes) === JSON.stringify(Object.keys(behavior.errorStatus).sort()), 'error code/status completeness');
const routeKeys = new Set();
for (const r of behavior.routes) {
  const key = r.method + ' ' + r.path;
  check(!routeKeys.has(key), 'duplicate route: ' + key); routeKeys.add(key);
  for (const n of [r.requestDefinition, r.responseDefinition, r.errorDefinition].filter(Boolean)) check(Boolean(schema.definitions[n]), `missing definition ${n}`);
  check(r.method !== 'GET' || (!r.requestDefinition && !r.idempotencyKeyRequired), 'GET side-effect contract');
}
check(behavior.cases.every(c => c.status === 'NOT_RUN'), 'must not claim business tests executed');
const report = {
  checkedAt: new Date().toISOString(),
  scope: 'Offline schema/fixture/hash/navigation consistency only; no real Java serializer, product consumers, HTTP/WS/DB, Flow or business tests',
  result: errors.length ? 'FAIL' : 'PASS',
  schemaDefinitions: Object.keys(schema.definitions).length,
  positiveCases: fixtures.cases.filter(c => c.valid).length,
  negativeCases: fixtures.cases.filter(c => !c.valid).length,
  digestVectors: fixtures.digestVectors.length,
  httpRoutes: behavior.routes.length,
  businessCasesNotRun: behavior.cases.length,
  errors
};
fs.writeFileSync(path.join(__dirname, 'static-check.json'), JSON.stringify(report, null, 2) + '\n');
console.log(JSON.stringify(report, null, 2));
if (errors.length) process.exitCode = 1;
