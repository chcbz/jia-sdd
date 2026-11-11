const fs = require('node:fs')
const path = require('node:path')
const crypto = require('node:crypto')
const assert = require('node:assert/strict')
const { execFileSync } = require('node:child_process')
const yaml = require('/home/isp/wsps/cyf/web/node_modules/js-yaml')
const sdd = '/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/sdd'
const feature = path.join(sdd, 'specs/juyiting-multimedia-deliberation')
const c = yaml.load(fs.readFileSync(path.join(feature, 'integration.yaml'), 'utf8'))
const v = JSON.parse(fs.readFileSync(path.join(feature, 'integration-evidence-20260928/u3-finalization-web-verification-20260930.json'), 'utf8'))
const git = (...args) => execFileSync('git', args, { encoding: 'utf8' }).trim()
const digest = name => crypto.createHash('sha256').update(fs.readFileSync(name)).digest('hex')
assert.equal(c.pinned_revisions.web_commit, v.web_commit)
assert.equal(c.pinned_revisions.web_tree, v.web_tree)
assert.equal(git('-C', sdd, 'ls-files', '--stage', 'web').split(/\s+/)[1], v.web_commit)
const web = path.join(sdd, '../web')
assert.equal(git('-C', web, 'rev-parse', 'HEAD'), v.web_commit)
assert.equal(git('-C', web, 'rev-parse', 'HEAD^{tree}'), v.web_tree)
for (const [name, hash] of Object.entries(v.source_sha256)) assert.equal(digest(path.join(web, name)), hash)
assert.equal(digest(path.join(feature, v.contract.path)), v.contract.sha256)
assert.equal(v.verification.passing, 57)
assert.equal(['new_finalization_cases', 'gallery_cases', 'catalog_cases', 'archive_cases', 'inline_cases'].reduce((sum, key) => sum + v.verification[key], 0), 57)
assert.equal(c.acceptance.status, 'not_run')
assert.equal(c.acceptance.case_count, 34)
assert.equal(c.verification.browser, 'not_run')
for (const name of ['README.md', 'fusion-detailed-design-v2.md', 'integration-u3-finalization-web-20260930.md']) {
  for (const match of fs.readFileSync(path.join(feature, name), 'utf8').matchAll(/\]\(([^)]+)\)/g)) {
    const target = match[1]
    if (/^(http|mailto:|#)/.test(target)) continue
    assert(fs.existsSync(path.join(feature, target.split('#')[0])), `${name}: ${target}`)
  }
}
const result = { date: '2026-09-30', status: 'PASS',
  checks: ['YAML actual js-yaml parser', 'exact Web commit/tree/gitlink', 'source digests', 'immutable contract digest', '57 test count', 'local Markdown links', '34 product cases/browser remain NOT_RUN'],
  initial_tooling_failures: ['Python PyYAML absent', 'node yaml absent', 'SDD cwd python3 resolves Python 3.6 which does not accept subprocess text=True'],
  remediation: 'Use existing js-yaml dependency and Node child_process/fs/crypto; no package install or new runtime dependency',
  product_acceptance: 'NOT_RUN', release: 'NOT_RUN' }
fs.writeFileSync('/home/isp/wsps/cyf/evidence/u3-finalization-v1/web/docs-static-verification.json', JSON.stringify(result, null, 2) + '\n')
console.log('PASS: exact Web commit/tree/gitlink, source and contract digests, 57 test count, links and NOT_RUN boundaries')
