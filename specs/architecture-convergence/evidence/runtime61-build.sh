set -euo pipefail
umask 077
timeout --signal=TERM --kill-after=10s 330 bash -euo pipefail <<'CYF_SYSTEM_CODEX_BUILD'
expected=336d92c2ad97afd3c7ac0979873eb4e324fff574
test "$PIPELINE_ID" = 5264702
test "$CI_COMMIT_SHA" = "$expected"
test "$(git rev-parse HEAD)" = "$expected"
test "$(git rev-parse HEAD^{tree})" = 63c409f978771e19d0c3f249d28ddf57f1e45bda
test -z "$(git status --porcelain --untracked-files=no)"
# Existing installer-consumer regression pins a historical Git fixture; shallow clones lack it.
fixture=5666fd2c990e4577cd4e16d5a32924ea0f3a8b7b
if ! git cat-file -e "$fixture^{commit}" 2>/dev/null; then
  git fetch --no-tags --depth=1 origin "$fixture"
fi
test "$(git rev-parse "$fixture^{tree}")" = d3cdc69da62bddc48af0bc86b4f32dbfa9429b60
test "$(git rev-parse HEAD)" = "$expected"
manager=
if test -x /usr/bin/dnf; then manager=/usr/bin/dnf; elif test -x /usr/bin/yum; then manager=/usr/bin/yum; fi
test -n "$manager"
missing_packages=
for package in ca-certificates curl tar xz git bubblewrap; do
 if ! rpm -q --quiet "$package"; then missing_packages="$missing_packages $package"; fi
done
if test -n "$missing_packages"; then "$manager" -y --setopt=gpgcheck=1 --setopt=install_weak_deps=False install $missing_packages; fi
node_sha=6c172a9ab6718f7b801fb5a7bd486af2ee5e32758086a04b84fcce2aa77095e6
archive="$PWD/_node.tar.xz"
curl --fail --location --connect-timeout 15 --max-time 90 https://mirrors.aliyun.com/nodejs-release/v24.22.1/node-v24.22.1-linux-x64.tar.xz --output "$archive"
printf '%s  %s\n' "$node_sha" "$archive" | sha256sum -c -
node_root="$(mktemp -d "$HOME/cyf-runtime-node.XXXXXX")"
trap 'rm -rf -- "$node_root"' EXIT
tar --no-same-owner -xJf "$archive" -C "$node_root"
export PATH="$node_root/node-v24.22.1-linux-x64/bin:$PATH"
test "$(node --version)" = v24.22.1
(cd conf/codex-ws-agent && npm ci --ignore-scripts --registry=https://registry.npmmirror.com --fetch-retries=1 --fetch-timeout=60000 --no-audit --no-fund)
node --input-type=module <<'NODE_POLICY_DIAGNOSTIC'
import fs from 'node:fs';import path from 'node:path';
for(const label of ['_node/node-v24.22.1-linux-x64/bin/node',process.execPath]){
 const absolute=path.resolve(label);let p=absolute;
 if(!fs.existsSync(p)) p=path.dirname(p);
 console.log('NODE_POLICY_CHAIN',label);
 for(;;){if(fs.existsSync(p)){const s=fs.lstatSync(p);console.log(JSON.stringify({path:p,uid:s.uid,mode:(s.mode&0o7777).toString(8),worldWritable:!!(s.mode&0o002)}));}const parent=path.dirname(p);if(parent===p)break;p=parent;}
}
const {createLocalScriptRunner}=await import('./conf/codex-ws-agent/skill-runners/local-script.mjs');
const result=await createLocalScriptRunner().probeTool();console.log('NODE_PRIVATE_LAYOUT_PROBE',JSON.stringify(result));
if(!result.ready)process.exitCode=1;
NODE_POLICY_DIAGNOSTIC
mkdir -m 700 _runtime_export
node --test --test-concurrency=2 conf/codex-ws-agent/test/skill-conversation.test.mjs conf/codex-ws-agent/test/skill-execution-store.test.mjs conf/codex-ws-agent/test/skill-executor.test.mjs conf/codex-ws-agent/test/conversation-native.test.mjs conf/codex-ws-agent/test/skill-install-manager.test.mjs conf/codex-ws-agent/test/skill-management-wire.test.mjs conf/codex-ws-agent/test/skill-registry.test.mjs conf/codex-ws-agent/test/archive-position-skills.test.mjs conf/codex-ws-agent/test/agent-client.test.mjs conf/codex-ws-agent/test/skill-native-host.test.mjs conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs conf/cyf-agent-runtime-v1/test/hosting-config.test.mjs > _runtime_export/tests.log 2>&1 || { cat _runtime_export/tests.log; exit 1; }
cat _runtime_export/tests.log
node --input-type=module <<'PAYLOAD'
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import cp from 'node:child_process';
import {collateExecutionPayload,EXECUTION_PAYLOAD_FILES} from './conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs';
const out=path.resolve('_runtime_export'),payload=path.join(out,'payload');fs.mkdirSync(payload);
await collateExecutionPayload(path.resolve('conf/codex-ws-agent'),path.join(payload,'codex-ws-agent'));
fs.cpSync(path.resolve('conf/codex-ws-agent/node_modules'),path.join(payload,'codex-ws-agent/node_modules'),{recursive:true,dereference:true,errorOnExist:true,force:false});
const installer=fs.readFileSync('conf/cyf-agent-runtime-v1/install.sh','utf8');
const lists=[...installer.matchAll(/for file in ([\s\S]*?); do\s+install -m (0[0-7]+) "\$SOURCE_DIR\/\$file"/g)];
if(lists.length!==2)throw Error('Runtime installer catalog changed');
for(const m of lists){for(const name of m[1].replace(/\\\n/g,' ').trim().split(/\s+/)){
 if(name.includes('..')||name.startsWith('/'))throw Error('Unsafe source path');
 const dest=path.join(payload,'runtime',name);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(path.join('conf/cyf-agent-runtime-v1',name),dest);fs.chmodSync(dest,parseInt(m[2],8));
}}
const files=[];function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else if(e.isFile())files.push({path:path.relative(payload,p),sha256:crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),mode:fs.statSync(p).mode&0o777});else throw Error('Unsafe payload')}}walk(payload);
const meta={pipeline:process.env.PIPELINE_ID,run:process.env.BUILD_NUMBER,commit:process.env.CI_COMMIT_SHA,tree:cp.execFileSync('git',['rev-parse','HEAD^{tree}'],{encoding:'utf8'}).trim(),version:JSON.parse(fs.readFileSync(path.join(payload,'runtime/package.json'))).version,engineFileCount:EXECUTION_PAYLOAD_FILES.length,files};
if(meta.version!=='1.3.10')throw Error('Unexpected candidate');
meta.dependencyProvenance={method:'same-Run npm ci --ignore-scripts --no-audit --no-fund',lockSha256:crypto.createHash('sha256').update(fs.readFileSync('conf/codex-ws-agent/package-lock.json')).digest('hex'),buildNode:process.versions.node,retainedPythonRequirementsSha256:crypto.createHash('sha256').update(fs.readFileSync('conf/codex-ws-agent/toolchain/requirements.txt')).digest('hex')};
fs.writeFileSync(path.join(out,'release.json'),JSON.stringify(meta,null,2)+'\n');
console.log('RUNTIME_PAYLOAD_FILES='+files.length);console.log('RUNTIME_SOURCE='+meta.commit);console.log('RUNTIME_TREE='+meta.tree);
PAYLOAD

CYF_SYSTEM_CODEX_BUILD
