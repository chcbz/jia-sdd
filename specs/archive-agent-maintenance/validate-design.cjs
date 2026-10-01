#!/usr/bin/env node
'use strict'
// Documentation/evidence validation only. This script does not run application tests, builds, runtime calls or production mutations.
const fs = require('node:fs')
const path = require('node:path')
const crypto = require('node:crypto')
const cp = require('node:child_process')

const dir = __dirname
const root = path.resolve(dir, '../..')
const yaml = require(require.resolve('js-yaml', { paths: [root, path.join(root, 'web')] }))
const read = name => {
  const file = path.resolve(dir, name)
  checkExistingRealPath(`feature_read:${name}`, dir, file, { rejectSymlink: true })
  return fs.readFileSync(file, 'utf8')
}
const hash = bytes => crypto.createHash('sha256').update(bytes).digest('hex')
const checks = []

function check(name, condition) {
  checks.push({ name, passed: !!condition })
  if (!condition) throw new Error(`Documentation validation failed: ${name}`)
}

function resolvedEnv(name, fallback) {
  return path.resolve(process.env[name] || fallback)
}

function inside(base, candidate) {
  const rel = path.relative(path.resolve(base), path.resolve(candidate))
  return rel === '' || (rel !== '..' && !rel.startsWith(`..${path.sep}`) && !path.isAbsolute(rel))
}

const realpath = value => (fs.realpathSync.native || fs.realpathSync)(value)

function checkExistingRealPath(label, base, candidate, options = {}) {
  check(`${label}:lexically_inside`, inside(base, candidate))
  const stat = fs.lstatSync(candidate)
  if (options.rejectSymlink) check(`${label}:not_symlink`, !stat.isSymbolicLink())
  const realBase = realpath(base)
  const realCandidate = realpath(candidate)
  check(`${label}:realpath_inside`, inside(realBase, realCandidate))
  return realCandidate
}

function safeRelativeParts(value, label) {
  check(`${label}:relative_path`, typeof value === 'string' && value.length > 0 && !value.startsWith('/') && !value.startsWith('\\'))
  const parts = value.split('/')
  check(`${label}:no_path_escape`, parts.every(part => part !== '' && part !== '.' && part !== '..' && !part.includes('\\') && !part.includes('\0')))
  return parts
}

const mappedRoot = resolvedEnv('CYF_AAM_ROOT_REPO', root)
const repoRoots = {
  root: mappedRoot,
  api: resolvedEnv('CYF_AAM_API_REPO', path.join(mappedRoot, 'api')),
  web: resolvedEnv('CYF_AAM_WEB_REPO', path.join(mappedRoot, 'web')),
  client: resolvedEnv('CYF_AAM_CLIENT_REPO', path.resolve(mappedRoot, '..', 'isp-install'))
}
for (const [name, repo] of Object.entries(repoRoots)) {
  check(`repo_root_exists:${name}`, fs.statSync(repo).isDirectory())
  check(`repo_root_realpath_is_directory:${name}`, fs.statSync(realpath(repo)).isDirectory())
  check(`repo_root_is_git:${name}`, cp.execFileSync('git', ['-C', repo, 'rev-parse', '--is-inside-work-tree'], { encoding: 'utf8' }).trim() === 'true')
}

const linuxMappings = [
  ['/home/isp/wsps/chcbz/isp-install', repoRoots.client],
  ['/home/isp/wsps/cyf/api', repoRoots.api],
  ['/home/isp/wsps/cyf/web', repoRoots.web],
  ['/home/isp/wsps/cyf', repoRoots.root]
]

function mapLinuxAbsolute(target, label) {
  const mapping = linuxMappings.find(([prefix]) => target === prefix || target.startsWith(`${prefix}/`))
  check(`${label}:known_linux_prefix`, !!mapping)
  const [prefix, base] = mapping
  const remainder = target.slice(prefix.length).replace(/^\//, '')
  const parts = remainder === '' ? [] : safeRelativeParts(remainder, `${label}:suffix`)
  const candidate = path.resolve(base, ...parts)
  check(`${label}:mapped_inside_repo`, inside(base, candidate))
  return { base, candidate }
}

function mapDocumentTarget(target, label) {
  if (target.startsWith('/')) return mapLinuxAbsolute(target, label)
  check(`${label}:no_unsupported_absolute_path`, !path.isAbsolute(target))
  const candidate = path.resolve(dir, target)
  check(`${label}:relative_inside_feature`, inside(dir, candidate))
  return { base: dir, candidate }
}

const required = ['spec.md', 'design.md', 'tasks.md', 'acceptance.md', 'integration.yaml']
check('sdd_five_required_files_present', required.every(name => fs.statSync(path.join(dir, name)).isFile()))
const integration = yaml.load(read('integration.yaml'), { json: false })
check('yaml_parsed_and_feature_D2', integration.feature_id === 'archive-agent-maintenance'
  && ['ready', 'implementing'].includes(integration.status) && integration.contract.revision === 'D2')
check('no_release_or_integration_pins_claimed', Object.values(integration.pinned_revisions).every(value => value === null)
  && integration.release.status === 'not_started' && integration.release.flow_run === null
  && integration.release.build_origin === null && integration.release.artifact_sha256 === null
  && integration.source_observation.production_verified === false && integration.source_observation.release_evidence === false)

const suite = JSON.parse(read('acceptance-cases.json'))
const cases = suite.cases
check('all_84_acceptance_cases_unexecuted', cases.length === 84 && cases.every(c => c.status === 'not_run' && c.evidence === null))
check('unique_acceptance_case_ids', new Set(cases.map(c => c.id)).size === cases.length)
check('acceptance_not_claimed', integration.acceptance.status === 'not_run')

if (integration.status === 'ready') {
  check('ready_has_no_component_test_claim', ['api', 'web', 'client', 'integration'].every(name => integration.verification[name] === 'not_run'))
  check('ready_handoff_state', integration.implementation_handoff.status === 'ready_for_M0_not_dispatched')
} else {
  check('implementing_owners_assigned', ['api', 'web', 'client', 'integration'].every(name => typeof integration.owners[name] === 'string' && integration.owners[name] !== 'unassigned'))
  check('implementing_verification_states', integration.verification.documentation
    && ['pending_refresh', 'passed_static_self_check'].includes(integration.verification.documentation.status)
    && ['api', 'web', 'client'].every(name => integration.verification[name] && integration.verification[name].status === 'partial')
    && integration.verification.integration && integration.verification.integration.status === 'not_run')
  check('implementing_not_accepted_or_released', integration.implementation_handoff.status === 'implementation_in_progress'
    && integration.acceptance.status === 'not_run' && integration.release.status === 'not_started')
  check('implementation_baseline_present', fs.statSync(path.join(dir, 'implementation-baseline.md')).isFile())

  const evidenceDir = path.join(dir, 'evidence', '2026-09-30')
  const evidenceSha256 = {
    'api-wiring-test-summary.json': '754526ae9e579757f0e39fcb3892aab4ccf3788737937401ccbae2be90fe736d',
    'client-final-source-proof.json': 'b65bcca29f21ec43ceaffdd6cade3d587357272c9cef24bb9f4cf6f6f29bfab3',
    'web-final-source-proof.json': '015de7827bb11fee8b43a9d77096644302eb33a4af27f85f13d074485043662e',
    'api-wiring-focused.log': '1aad58511caa6dddd3bafc1fb77094b99321f3cd78893d7b5a11f315a0c061dc',
    'api-wiring-regression.log': 'c7ea1a821ae9f95defdd2deb1ffff59ddf94f11cec942e35358b140b59db095d',
    'client-final-linux.log': '3065d4b97a8ed9da1c065f1dec862397eca6a598e3c81373ed8cf78be5e5db78',
    'web-archive-tests.log': '700927ac2b057a94ee73cf62b5e5adcab58c7ad986be468e808b7b904d045456',
    'web-build.log': 'fd5bba506d081958ede08b6ffe8d8a7263fa15e4ecd008c0aed4ea3663d729b7',
    'api-archive-regression-comparison.json': 'c8feac0f476a8629a37b47d9f2366f896812c202666e4dec8e49360d5c9315a3'
  }
  checkExistingRealPath('evidence_directory', dir, evidenceDir, { rejectSymlink: true })
  for (const [name, expected] of Object.entries(evidenceSha256)) {
    const file = path.join(evidenceDir, name)
    check(`evidence_present:${name}`, fs.statSync(file).isFile())
    checkExistingRealPath(`evidence_path:${name}`, evidenceDir, file, { rejectSymlink: true })
    check(`evidence_sha256:${name}`, hash(fs.readFileSync(file)) === expected)
  }

  const api = JSON.parse(fs.readFileSync(path.join(evidenceDir, 'api-wiring-test-summary.json'), 'utf8'))
  const apiSuites = Object.fromEntries(api.results.map(result => [result.suite, result]))
  check('api_prospective_tree_not_commit', api.source.tree === '7d61d50e9a262eeb43bc8cc9ab77763bd9cec27b'
    && api.source.kind === 'prospective_worktree_tree_not_commit')
  check('api_85_focused_passed', ['platform', 'native_security', 'maintenance'].reduce((total, name) => total + apiSuites[name].tests, 0) === 85
    && ['platform', 'native_security', 'maintenance'].every(name => apiSuites[name].failures === 0 && apiSuites[name].errors === 0 && apiSuites[name].skipped === 0))
  check('api_archive_regression_baseline_failures_preserved', apiSuites.full_archive.tests === 195
    && apiSuites.full_archive.failures === 12 && apiSuites.full_archive.errors === 0 && apiSuites.full_archive.skipped === 3
    && api.archive_regression.status === 'failed_with_identical_baseline_failure_set'
    && Array.isArray(api.archive_regression.failure_set_delta) && api.archive_regression.failure_set_delta.length === 0
    && JSON.stringify(api.archive_regression.current_failures) === JSON.stringify(api.archive_regression.baseline_failures))

  const comparison = JSON.parse(fs.readFileSync(path.join(evidenceDir, 'api-archive-regression-comparison.json'), 'utf8'))
  check('api_original_baseline_comparison_preserved', comparison.status === 'failed_with_identical_baseline_failure_set'
    && comparison.current_tests === 194 && comparison.current_skipped === 3
    && comparison.current_failures.length === 12 && comparison.introduced_failure_set.length === 0
    && JSON.stringify(comparison.current_failures) === JSON.stringify(comparison.baseline_failures))

  const client = JSON.parse(fs.readFileSync(path.join(evidenceDir, 'client-final-source-proof.json'), 'utf8'))
  check('client_246_pass_and_not_wired', client.prospective_tree === 'a3ea0078fd11feb1fa25d4ca4109bc4231b57b45'
    && client.prospective_tree_is_commit === false && client.results.tests === 246 && client.results.passed === 246
    && client.results.failed === 0 && client.results.skipped === 0 && client.client_entry_wired === false
    && client.production_verified === false)
  check('client_log_digest_matches_proof', client.log_sha256 === hash(fs.readFileSync(path.join(evidenceDir, 'client-final-linux.log'))))
  for (const [relative, expected] of Object.entries(client.source_sha256)) {
    const parts = safeRelativeParts(relative, `client_source:${relative}`)
    const file = path.resolve(repoRoots.client, 'conf', 'codex-ws-agent', ...parts)
    check(`client_source_inside_repo:${relative}`, inside(repoRoots.client, file))
    check(`client_source_exists:${relative}`, fs.statSync(file).isFile())
    checkExistingRealPath(`client_source_realpath:${relative}`, repoRoots.client, file, { rejectSymlink: true })
    // This is the historical 246-test snapshot, not the current runner worktree.
    // Bind its recorded hashes to its exact prospective Git tree so later source repairs
    // cannot invalidate old evidence or be mistaken for a rerun of the old tests.
    check(`client_historical_tree:${relative}`, /^[0-9a-f]{40}$/.test(client.prospective_tree))
    const historicalPath = `conf/codex-ws-agent/${parts.join('/')}`
    const historicalEntry = cp.execFileSync('git', ['-C', repoRoots.client, 'ls-tree', client.prospective_tree, '--', historicalPath], { encoding: 'utf8' }).trim()
    check(`client_historical_regular_blob:${relative}`, /^(100644|100755) blob [0-9a-f]{40}\t/.test(historicalEntry))
    const historicalBytes = cp.execFileSync('git', ['-C', repoRoots.client, 'show', `${client.prospective_tree}:${historicalPath}`], { maxBuffer: 16 * 1024 * 1024 })
    check(`client_historical_source_sha256:${relative}`, hash(historicalBytes) === expected)
  }

  const web = JSON.parse(fs.readFileSync(path.join(evidenceDir, 'web-final-source-proof.json'), 'utf8'))
  check('web_82_and_build_passed_not_deployed', web.tree === 'e7d4cc80afcccb0acb4c33a209763c7d52052f43'
    && web.kind === 'prospective_worktree_tree_not_commit' && web.tests.passed === 82 && web.tests.failed === 0
    && web.build.status === 'passed' && web.build.production_deployed === false)
  check('web_log_digests_match_proof', web.logs.tests === hash(fs.readFileSync(path.join(evidenceDir, 'web-archive-tests.log')))
    && web.logs.build === hash(fs.readFileSync(path.join(evidenceDir, 'web-build.log'))))


  const resolverStage2Dir = path.join(evidenceDir, 'resolver-stage2')
  const resolverAttempt3Dir = path.join(resolverStage2Dir, 'attempt3')
  checkExistingRealPath('resolver_stage2_directory', evidenceDir, resolverStage2Dir, { rejectSymlink: true })
  checkExistingRealPath('resolver_attempt3_directory', resolverStage2Dir, resolverAttempt3Dir, { rejectSymlink: true })
  const attempt3EvidenceSha256 = {
    'api-resolver-source-proof.json': 'd3ed0f64cd5938a66e9f4a21fd6e5374225e6b4c19a437b6d1d4b6bebf8a2ed8',
    'api-resolver-test-summary.json': 'b4cb3c8b60fd078e37b21a0ea27a310cc20abafdc44f0c208db794f9a615f5af',
    'api-resolver-gradle.log': '8e719d8413a6dc763c20d823beeb76bc01300cef05bbe940fb151f47bb40418f',
    'review-final.json': '18aa6875d763c2cc7d53bd76a9732e973d2fac54940bdc9aa8f3a9197ec8ef8f'
  }
  for (const [name, expected] of Object.entries(attempt3EvidenceSha256)) {
    const file = path.join(resolverAttempt3Dir, name)
    check(`resolver_attempt3_evidence_present:${name}`, fs.statSync(file).isFile())
    checkExistingRealPath(`resolver_attempt3_evidence_path:${name}`, resolverAttempt3Dir, file, { rejectSymlink: true })
    check(`resolver_attempt3_evidence_sha256:${name}`, hash(fs.readFileSync(file)) === expected)
  }

  const rejectedReviewFile = path.join(resolverStage2Dir, 'review-attempt2.json')
  checkExistingRealPath('resolver_attempt2_review_path', resolverStage2Dir, rejectedReviewFile, { rejectSymlink: true })
  check('resolver_attempt2_reject_original_preserved', hash(fs.readFileSync(rejectedReviewFile)) === '7ae24958961bc52b526fcb516d4d9a072a072a30d7770882c7237e747c1b0c3e')
  const rejectedReview = JSON.parse(fs.readFileSync(rejectedReviewFile, 'utf8'))
  check('resolver_attempt2_remains_rejected_history', rejectedReview.verdict === 'REJECT'
    && rejectedReview.source_tree === 'f88f5125ae99d345a544ef8d1fa929055be1e14a'
    && rejectedReview.whole_feature_accepted === false
    && rejectedReview.real_mysql_run === false && rejectedReview.http_e2e_run === false)

  const attempt3Source = JSON.parse(fs.readFileSync(path.join(resolverAttempt3Dir, 'api-resolver-source-proof.json'), 'utf8'))
  const attempt3Summary = JSON.parse(fs.readFileSync(path.join(resolverAttempt3Dir, 'api-resolver-test-summary.json'), 'utf8'))
  const attempt3ReviewFile = path.join(resolverAttempt3Dir, 'review-final.json')
  const attempt3Review = JSON.parse(fs.readFileSync(attempt3ReviewFile, 'utf8'))
  const expectedResolverSelectors = [
    ':agent:jia-agent-service:archivePlatformContracts',
    ':agent:jia-agent-service:archiveMaintenanceSecurity',
    ':chat:jia-chat-service:archiveMaintenanceMvp',
    ':chat:jia-chat-service:archiveRegression'
  ]
  check('resolver_attempt3_summary_bound_to_source_proof', JSON.stringify(attempt3Summary.source) === JSON.stringify(attempt3Source))
  check('resolver_attempt3_prospective_tree_not_commit', attempt3Source.kind === 'prospective_worktree_tree_not_commit'
    && attempt3Source.tree === '67dc1c225a1cc020f5c68b44b992a6f329dc1a01'
    && attempt3Source.supersedes_rejected_tree === 'f88f5125ae99d345a544ef8d1fa929055be1e14a'
    && attempt3Source.previous_stage_tree === '7d61d50e9a262eeb43bc8cc9ab77763bd9cec27b'
    && attempt3Source.base_commit === 'e15e1a9d947e86e5f81a3288948087466a8a879c'
    && cp.execFileSync('git', ['-C', repoRoots.api, 'cat-file', '-t', attempt3Source.tree], { encoding: 'utf8' }).trim() === 'tree'
    && cp.execFileSync('git', ['-C', repoRoots.api, 'cat-file', '-t', attempt3Source.base_commit], { encoding: 'utf8' }).trim() === 'commit')
  check('resolver_attempt3_exact_selectors', JSON.stringify(attempt3Source.selector) === JSON.stringify(expectedResolverSelectors)
    && attempt3Summary.gradle_lock === 'C:/tmp/cyf-gradle.lock')
  check('resolver_attempt3_has_19_unique_source_files', Array.isArray(attempt3Source.source_files)
    && attempt3Source.source_files.length === 19
    && new Set(attempt3Source.source_files.map(item => item.path)).size === 19)
  for (const item of attempt3Source.source_files) {
    safeRelativeParts(item.path, `resolver_attempt3_source_path:${item.path}`)
    check(`resolver_attempt3_source_metadata:${item.path}`, /^[0-9a-f]{40}$/.test(item.git_blob)
      && /^[0-9a-f]{64}$/.test(item.sha256) && Number.isInteger(item.bytes) && item.bytes > 0)
    const revisionPath = `${attempt3Source.tree}:${item.path}`
    const bytes = cp.execFileSync('git', ['-C', repoRoots.api, 'show', revisionPath], { maxBuffer: 16 * 1024 * 1024 })
    const blob = cp.execFileSync('git', ['-C', repoRoots.api, 'rev-parse', revisionPath], { encoding: 'utf8' }).trim()
    const treeEntry = cp.execFileSync('git', ['-C', repoRoots.api, 'ls-tree', attempt3Source.tree, '--', item.path], { encoding: 'utf8' }).trim()
    const treeMatch = /^(100644|100755) blob ([0-9a-f]{40})\t(.+)$/.exec(treeEntry)
    check(`resolver_attempt3_regular_git_blob:${item.path}`, treeMatch !== null
      && treeMatch[2] === item.git_blob && treeMatch[3] === item.path)
    check(`resolver_attempt3_frozen_source:${item.path}`, hash(bytes) === item.sha256
      && bytes.length === item.bytes && blob === item.git_blob)
  }

  const attempt3Suites = Object.fromEntries(attempt3Summary.results.map(result => [result.suite, result]))
  check('resolver_attempt3_exact_suite_set', attempt3Summary.results.length === 4
    && Object.keys(attempt3Suites).length === 4
    && ['platform', 'native_security', 'maintenance', 'archive_regression'].every(name => Object.hasOwn(attempt3Suites, name)))
  check('resolver_attempt3_103_focused_passed', ['platform', 'native_security', 'maintenance']
    .reduce((total, name) => total + attempt3Suites[name].tests, 0) === 103
    && ['platform', 'native_security', 'maintenance'].every(name => attempt3Suites[name].failures === 0
      && attempt3Suites[name].errors === 0 && attempt3Suites[name].skipped === 0))
  const attempt3Archive = attempt3Suites.archive_regression
  check('resolver_attempt3_archive_regression_preserves_baseline_failures', attempt3Archive.tests === 198
    && attempt3Archive.failures === 12 && attempt3Archive.errors === 0 && attempt3Archive.skipped === 3
    && Array.isArray(attempt3Summary.comparison.baseline_failures)
    && Array.isArray(attempt3Summary.comparison.current_failures)
    && Array.isArray(attempt3Summary.comparison.introduced_failure_set)
    && Array.isArray(attempt3Summary.comparison.removed_failure_set)
    && attempt3Summary.comparison.introduced_failure_set.length === 0
    && attempt3Summary.comparison.removed_failure_set.length === 0
    && JSON.stringify([...attempt3Summary.comparison.current_failures].sort())
      === JSON.stringify([...attempt3Summary.comparison.baseline_failures].sort())
    && JSON.stringify([...attempt3Summary.comparison.baseline_failures].sort())
      === JSON.stringify([...comparison.baseline_failures].sort()))
  const expectedResolvedFindings = [
    'HISTORICAL_SORT_INDEX',
    'NON_EXACT_HISTORICAL_PROOF',
    'NULL_REFERENCE_ACCEPTED'
  ]
  check('resolver_attempt3_final_review_exact_local_accept', attempt3Review.scope === 'InstalledSkillResolver local source slice only'
    && attempt3Review.source_tree === attempt3Source.tree && attempt3Review.verdict === 'ACCEPT'
    && Array.isArray(attempt3Review.resolved_findings)
    && JSON.stringify([...attempt3Review.resolved_findings].sort()) === JSON.stringify(expectedResolvedFindings)
    && attempt3Review.new_p0 === 0 && attempt3Review.new_p1 === 0 && attempt3Review.new_p2 === 0)
  check('resolver_attempt3_final_review_counts_match_evidence', attempt3Review.source_files_verified === 19
    && attempt3Review.source_files_total === attempt3Source.source_files.length
    && attempt3Review.xml_reports_verified === 56
    && attempt3Review.focused_tests === 103 && attempt3Review.focused_failures === 0
    && attempt3Review.gradle_log_sha256 === attempt3EvidenceSha256['api-resolver-gradle.log']
    && attempt3Review.archive_regression.tests === attempt3Archive.tests
    && attempt3Review.archive_regression.failures === attempt3Archive.failures
    && attempt3Review.archive_regression.skipped === attempt3Archive.skipped
    && Array.isArray(attempt3Review.archive_regression.introduced_failure_set)
    && attempt3Review.archive_regression.introduced_failure_set.length === 0
    && Array.isArray(attempt3Review.archive_regression.removed_failure_set)
    && attempt3Review.archive_regression.removed_failure_set.length === 0
    && attempt3Review.archive_regression.gradle_status === 'BUILD_FAILED_baseline_failures_preserved')
  check('resolver_attempt3_final_review_explicitly_keeps_unverified_boundaries_closed', attempt3Review.real_mysql_run === false
    && attempt3Review.http_e2e_run === false && attempt3Review.concurrent_rebinding_run === false
    && attempt3Review.whole_feature_accepted === false && attempt3Review.native_execution_enabled === false
    && integration.verification.integration.status === 'not_run')

  const resolverSliceReview = integration.verification.api.resolver_slice_review
  const resolverReviewEvidence = mapLinuxAbsolute(resolverSliceReview.evidence, 'resolver_slice_review_evidence')
  check('resolver_attempt3_integration_review_binding', integration.status === 'implementing'
    && integration.verification.api.status === 'partial'
    && resolverSliceReview.verdict === 'ACCEPT_local_slice_only'
    && resolverSliceReview.tree === attempt3Source.tree
    && resolverSliceReview.tree === attempt3Review.source_tree
    && resolverSliceReview.evidence === '/home/isp/wsps/cyf/specs/archive-agent-maintenance/evidence/2026-09-30/resolver-stage2/attempt3/review-final.json'
    && path.resolve(resolverReviewEvidence.candidate) === path.resolve(attempt3ReviewFile)
    && resolverSliceReview.native_execution_enabled === false
    && resolverSliceReview.native_execution_enabled === attempt3Review.native_execution_enabled)
  checkExistingRealPath('resolver_slice_review_evidence_realpath', resolverReviewEvidence.base,
    resolverReviewEvidence.candidate, { rejectSymlink: true })

  const attempt3XmlDir = path.join(resolverAttempt3Dir, 'xml')
  checkExistingRealPath('resolver_attempt3_xml_directory', resolverAttempt3Dir, attempt3XmlDir, { rejectSymlink: true })
  const declaredXml = []
  for (const result of attempt3Summary.results) {
    check(`resolver_attempt3_xml_manifest_array:${result.suite}`, Array.isArray(result.xml))
    for (const item of result.xml) {
      const parts = safeRelativeParts(item.file, `resolver_attempt3_xml_name:${result.suite}:${item.file}`)
      check(`resolver_attempt3_xml_leaf_name:${result.suite}:${item.file}`, parts.length === 1
        && /^TEST-[A-Za-z0-9.$_-]+\.xml$/.test(item.file) && /^[0-9a-f]{64}$/.test(item.sha256))
      const file = path.resolve(attempt3XmlDir, result.suite, item.file)
      check(`resolver_attempt3_xml_inside:${result.suite}:${item.file}`, inside(attempt3XmlDir, file))
      checkExistingRealPath(`resolver_attempt3_xml_path:${result.suite}:${item.file}`, attempt3XmlDir, file, { rejectSymlink: true })
      check(`resolver_attempt3_xml_regular:${result.suite}:${item.file}`, fs.statSync(file).isFile())
      check(`resolver_attempt3_xml_sha256:${result.suite}:${item.file}`, hash(fs.readFileSync(file)) === item.sha256)
      declaredXml.push(`${result.suite}/${item.file}`)
    }
  }
  check('resolver_attempt3_56_unique_xml_records', declaredXml.length === 56 && new Set(declaredXml).size === 56)
  const actualXml = []
  const xmlSuiteEntries = fs.readdirSync(attempt3XmlDir, { withFileTypes: true })
  check('resolver_attempt3_xml_only_declared_suite_directories', xmlSuiteEntries.length === 4
    && xmlSuiteEntries.every(entry => ['platform', 'native_security', 'maintenance', 'archive_regression'].includes(entry.name)
      && entry.isDirectory() && !entry.isSymbolicLink()))
  for (const suiteEntry of xmlSuiteEntries) {
    const suiteDir = path.join(attempt3XmlDir, suiteEntry.name)
    checkExistingRealPath(`resolver_attempt3_xml_suite:${suiteEntry.name}`, attempt3XmlDir, suiteDir, { rejectSymlink: true })
    for (const entry of fs.readdirSync(suiteDir, { withFileTypes: true })) {
      const file = path.join(suiteDir, entry.name)
      check(`resolver_attempt3_xml_entry_regular:${suiteEntry.name}:${entry.name}`, entry.isFile() && !entry.isSymbolicLink())
      checkExistingRealPath(`resolver_attempt3_xml_entry_path:${suiteEntry.name}:${entry.name}`, attempt3XmlDir, file, { rejectSymlink: true })
      actualXml.push(`${suiteEntry.name}/${entry.name}`)
    }
  }
  check('resolver_attempt3_xml_manifest_matches_files', JSON.stringify(actualXml.sort()) === JSON.stringify(declaredXml.sort()))

  const attempt3Log = fs.readFileSync(path.join(resolverAttempt3Dir, 'api-resolver-gradle.log'), 'utf8')
  check('resolver_attempt3_log_matches_recorded_selectors_and_counts', expectedResolverSelectors.every(selector => attempt3Log.includes(`> Task ${selector}`))
    && attempt3Log.includes('198 tests completed, 12 failed, 3 skipped')
    && attempt3Log.includes('BUILD FAILED') && !attempt3Log.includes('BUILD SUCCESSFUL'))
}

check('D2_acceptance_case_family', suite.revision === 'D2' && cases.filter(c => c.id.startsWith('D2-')).length === 14)
const design = read('design.md')
check('D2_removes_legacy_hall_projection_proposal', !design.includes('新增 `sourceType=archive-maintenance`') && design.includes('不扩展现有 ItemRef/OVERVIEW-v1'))
check('D2_no_parallel_command_polling', !design.includes('| GET `/internal/archive/v1/commands` |') && design.includes('不新增 `/internal/archive/v1/commands`'))
check('D2_shared_auth_transport_publication_boundaries', ['PUBLICATION_USE', 'legacy codex-ws-agent', 'Runtime v1', 'ArchiveAgentExecutionPort', 'dispatchKey', '直达', 'juyiting-multimedia-deliberation'].every(x => design.includes(x)))
check('handoff_present', fs.statSync(path.join(dir, 'handoff.md')).isFile())
const stories = new Set(cases.flatMap(c => c.user_stories))
check('user_stories_U1_to_U9_covered', Array.from({ length: 9 }, (_, i) => `U${i + 1}`).every(x => stories.has(x)) && stories.size === 9)
const workPackages = new Set(cases.flatMap(c => c.work_packages))
check('implementation_packages_M1_to_M10_covered', Array.from({ length: 10 }, (_, i) => `M${i + 1}`).every(x => workPackages.has(x)) && workPackages.size === 10)
const acceptance = read('acceptance.md')
check('machine_cases_match_human_matrix', cases.every(c => acceptance.includes(`| ${c.id} |`) && acceptance.includes(c.expected))
  && acceptance.includes(`**${cases.length} 项**`))
const tasks = read('tasks.md')
const estimates = [...tasks.matchAll(/\| (\d+)–(\d+) \|$/gm)].map(m => [Number(m[1]), Number(m[2])])
check('estimate_derived_from_work_packages', estimates.length === 11 && estimates.reduce((sum, value) => sum + value[0], 0) === 27
  && estimates.reduce((sum, value) => sum + value[1], 0) === 46)

const audit = JSON.parse(read('source-audit.json'))
check('source_audit_is_observation_not_release', audit.remote_refs_fetched_for_this_audit === false && audit.deployed_version_verified === false)
for (const item of audit.files) {
  check(`known_audit_repository:${item.repository}`, Object.hasOwn(repoRoots, item.repository))
  const repo = repoRoots[item.repository]
  safeRelativeParts(item.path, `frozen_source_path:${item.repository}:${item.path}`)
  const bytes = cp.execFileSync('git', ['-C', repo, 'show', `${item.revision}:${item.path}`], { maxBuffer: 16 * 1024 * 1024 })
  const blob = cp.execFileSync('git', ['-C', repo, 'rev-parse', `${item.revision}:${item.path}`], { encoding: 'utf8' }).trim()
  check(`frozen_source:${item.repository}:${item.path}`, hash(bytes) === item.sha256 && bytes.length === item.bytes && blob === item.git_blob)
}

let linkCount = 0
let jsonExampleCount = 0
for (const name of fs.readdirSync(dir).filter(name => name.endsWith('.md'))) {
  const text = read(name)
  check(`no_trailing_whitespace:${name}`, !/[\t ]+$/m.test(text))
  check(`balanced_code_fences:${name}`, (text.match(/^```/gm) || []).length % 2 === 0)
  for (const match of text.matchAll(/\[[^\]\n]+\]\(([^)]+)\)/g)) {
    const target = match[1].split('#')[0]
    if (!target || /^(?:https?:|mailto:)/.test(target)) continue
    linkCount++
    const mapped = mapDocumentTarget(target, `local_link:${name}:${target}`)
    const exists = fs.existsSync(mapped.candidate)
    check(`local_link_exists:${name}:${target}`, exists || mapped.candidate === path.join(dir, 'documentation-check.json'))
    if (exists) checkExistingRealPath(`local_link_realpath:${name}:${target}`, mapped.base, mapped.candidate)
  }
  for (const match of text.matchAll(/```json\n([\s\S]*?)\n```/g)) {
    JSON.parse(match[1])
    jsonExampleCount++
  }
}
check('json_examples_parse', jsonExampleCount > 0)
const indexFile = path.join(repoRoots.root, 'specs/INDEX.md')
checkExistingRealPath('scoped_index_path', repoRoots.root, indexFile, { rejectSymlink: true })
check('index_contains_scoped_design_entry', fs.readFileSync(indexFile, 'utf8').includes('## 典籍阁 Agent 任职与内容维护方案'))
cp.execFileSync('git', ['-C', repoRoots.root, 'diff', '--check', '--', 'specs/INDEX.md', 'specs/archive-agent-maintenance'], { encoding: 'utf8' })
check('scoped_diff_whitespace_check', true)

function walkFiles(current, prefix = '') {
  const result = []
  for (const entry of fs.readdirSync(current, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
    const relative = prefix ? `${prefix}/${entry.name}` : entry.name
    if (relative === 'documentation-check.json') continue
    check(`feature_tree_entry_not_symlink:${relative}`, !entry.isSymbolicLink())
    const entryPath = path.join(current, entry.name)
    checkExistingRealPath(`feature_tree_realpath:${relative}`, dir, entryPath, { rejectSymlink: true })
    if (entry.isDirectory()) result.push(...walkFiles(entryPath, relative))
    else {
      check(`feature_tree_entry_is_regular_file:${relative}`, entry.isFile())
      result.push(relative)
    }
  }
  return result
}
const documentDigests = Object.fromEntries(walkFiles(dir).map(name => [name, hash(fs.readFileSync(path.join(dir, ...name.split('/'))))]))
const result = {
  feature_id: 'archive-agent-maintenance',
  kind: 'documentation_and_recorded_evidence_static_self_check_only',
  command: `node ${path.join(dir, 'validate-design.cjs')}`,
  status: 'passed',
  integration_status_observed: integration.status,
  documentation_status_before_run: typeof integration.verification.documentation === 'string'
    ? integration.verification.documentation : integration.verification.documentation.status,
  checks_count: checks.length,
  source_files_verified: audit.files.length,
  acceptance_cases: cases.length,
  acceptance_status: 'not_run',
  local_links_checked: linkCount,
  json_examples_parsed: jsonExampleCount,
  recorded_component_tests_verified: integration.status === 'implementing',
  application_tests_run: false,
  production_operations_run: false,
  release_evidence: false,
  checks,
  document_sha256: documentDigests
}
fs.writeFileSync(path.join(dir, 'documentation-check.json'), JSON.stringify(result, null, 2) + '\n')
console.log(JSON.stringify({
  status: result.status,
  checks: checks.length,
  source_files: audit.files.length,
  acceptance_cases: cases.length,
  local_links: linkCount,
  recorded_component_tests_verified: result.recorded_component_tests_verified,
  application_tests_run: false
}, null, 2))
