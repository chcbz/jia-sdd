import { readFileSync } from 'node:fs'
import { createHash } from 'node:crypto'
import { execFileSync } from 'node:child_process'
import { resolve } from 'node:path'
import { pathToFileURL } from 'node:url'
const [root, api, client] = process.argv.slice(2).map(p => resolve(p))
if (!root || !api || !client) throw new Error('Expected root, API and client worktrees')
const hash = bytes => createHash('sha256').update(bytes).digest('hex')
const fixturePath = 'specs/agent-output-delivery/fixtures.json'
const apiFixturePath = 'agent/jia-agent-service/src/test/resources/output-delivery-fixtures.json'
const clientPath = 'conf/codex-ws-agent/output-manifest.mjs'
const rootBytes = readFileSync(resolve(root, fixturePath))
const apiBytes = readFileSync(resolve(api, apiFixturePath))
if (!rootBytes.equals(apiBytes)) throw new Error('API fixture differs from root contract')
const refs = Object.fromEntries(Object.entries({ root, api, client }).map(([name, cwd]) => [name, execFileSync('git', ['rev-parse', 'HEAD'], { cwd, encoding: 'utf8' }).trim()]))
const fixture = JSON.parse(rootBytes)
const validator = await import(pathToFileURL(resolve(client, clientPath)).href)
validator.validateOutputManifest(fixture.manifest)
validator.validateOutputContext(fixture.outputContext, { taskId: fixture.outputContext.source.id })
const bytes = Buffer.from(fixture.sampleFile.utf8, 'utf8')
if (hash(bytes) !== fixture.sampleFile.sha256 || String(bytes.length) !== fixture.sampleFile.byteLength) throw new Error('Fixture bytes/hash mismatch')
console.log(JSON.stringify({ refs, checks: { apiFixtureByteIdentical: true, clientAcceptsFrozenManifest: true, clientAcceptsFrozenTaskContext: true, sampleBytesAndHash: true }, fixtureSha256: hash(rootBytes), clientValidatorSha256: hash(readFileSync(resolve(client, clientPath))), scope: 'Read-only contract/candidate association; no API transport, browser or lifecycle acceptance.' }, null, 2))
