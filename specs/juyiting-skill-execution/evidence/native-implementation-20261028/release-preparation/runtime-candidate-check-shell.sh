set -euo pipefail
umask 077
timeout --signal=TERM --kill-after=10s 500 bash -euo pipefail <<'CYF_SYSTEM_CODEX_BUILD'
expected=22b4511945d7ef7e6cfbda0f482f6c8910ce8306
test "$PIPELINE_ID" = 5264702
test "$CI_COMMIT_SHA" = "$expected"
test "$(git rev-parse HEAD)" = "$expected"
test "$(git rev-parse HEAD^{tree})" = d8529e3ba852dc541b527c46d556dd8126b7d527
test -z "$(git status --porcelain --untracked-files=all)"
# Existing installer-consumer regression pins a historical Git fixture; shallow clones lack it.
fixture=5666fd2c990e4577cd4e16d5a32924ea0f3a8b7b
if ! git cat-file -e "$fixture^{commit}" 2>/dev/null; then
  git fetch --no-tags --depth=1 origin "$fixture"
fi
test "$(git rev-parse "$fixture^{tree}")" = d3cdc69da62bddc48af0bc86b4f32dbfa9429b60
test "$(git rev-parse HEAD)" = "$expected"
# Run66 spent the 330s build budget in repository metadata before any test.
# Pin the same signed bubblewrap RPM used by the previous successful environment;
# no 41MB updates metadata refresh, no disabled integrity checks or missing tests.
for package in ca-certificates curl tar xz git python3; do rpm -q --quiet "$package"; done
if ! rpm -q --quiet bubblewrap; then
  rpm_file="$PWD/_bubblewrap.rpm"
  curl --fail --location --connect-timeout 15 --max-time 60 https://mirrors.aliyun.com/alinux/3/updates/x86_64/Packages/bubblewrap-0.4.0-2.2.al8.x86_64.rpm --output "$rpm_file"
  printf '%s  %s\n' 8c054aaf7f711c42ceee8e9a58dfbe8c953c063eb3619488b3ea6e6392c70af0 "$rpm_file" | sha256sum -c -
  signature="$(rpm -Kv "$rpm_file")"
  printf '%s\n' "$signature"
  ! printf '%s\n' "$signature" | grep -E 'NOKEY|NOT OK|BAD|NOTTRUSTED'
  printf '%s\n' "$signature" | grep -E 'Signature.*key ID cac33616: OK'
  rpm -Uvh "$rpm_file"
fi
rpm -q bubblewrap
node_sha=6c172a9ab6718f7b801fb5a7bd486af2ee5e32758086a04b84fcce2aa77095e6
archive="$PWD/_node.tar.xz"
curl --fail --location --connect-timeout 15 --max-time 90 https://mirrors.aliyun.com/nodejs-release/v24.22.1/node-v24.22.1-linux-x64.tar.xz --output "$archive"
printf '%s  %s\n' "$node_sha" "$archive" | sha256sum -c -
node_root="$(mktemp -d "$HOME/cyf-runtime-node.XXXXXX")"
trap 'rm -rf -- "$node_root"' EXIT
tar --no-same-owner -xJf "$archive" -C "$node_root"
export PATH="$node_root/node-v24.22.1-linux-x64/bin:$PATH"
mkdir -m 700 "$node_root/home" "$node_root/tmp"
test "$(node --version)" = v24.22.1
(cd conf/codex-bridge && env -i PATH="$PATH" HOME="$node_root/home" TMPDIR="$node_root/tmp" npm ci --ignore-scripts --registry=https://registry.npmmirror.com --fetch-retries=1 --fetch-timeout=60000 --no-audit --no-fund)
mkdir -m 700 _runtime_export
env -i PATH="$PATH" HOME="$node_root/home" TMPDIR="$node_root/tmp" node --test --test-concurrency=2 conf/codex-bridge/test/juyiting-action-model-schema.test.mjs conf/codex-bridge/test/juyiting-action-outcome.test.mjs conf/codex-bridge/test/juyiting-typed-runtime.test.mjs conf/codex-bridge/test/juyiting-review-v5.test.mjs conf/codex-bridge/test/skill-conversation.test.mjs conf/codex-bridge/test/skill-execution-store.test.mjs conf/codex-bridge/test/skill-executor.test.mjs conf/codex-bridge/test/conversation-native.test.mjs conf/codex-bridge/test/skill-install-manager.test.mjs conf/codex-bridge/test/skill-management-wire.test.mjs conf/codex-bridge/test/skill-registry.test.mjs conf/codex-bridge/test/archive-position-skills.test.mjs conf/codex-bridge/test/agent-client.test.mjs conf/codex-bridge/test/skill-registration.test.mjs conf/codex-bridge/test/native-single-entry.test.mjs conf/codex-bridge/test/native-execution.test.mjs conf/codex-bridge/test/native-execution-profile.test.mjs conf/codex-bridge/test/native-artifact-session.test.mjs conf/codex-bridge/test/native-artifact-snapshot.test.mjs conf/codex-bridge/test/native-skill-config.test.mjs conf/codex-bridge/test/app-server-native-execution.test.mjs conf/codex-bridge/test/app-server-native-handshake.test.mjs conf/codex-bridge/test/typed-inspection-profile.test.mjs conf/codex-bridge/test/typed-inspection-network.test.mjs conf/cyf-agent-runtime-v1/test/install-entry-convergence.test.mjs conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs conf/cyf-agent-runtime-v1/test/hosting-config.test.mjs conf/skills/native-image/test/image.test.mjs conf/cyf-agent-runtime-v1/test/provider-environments.test.mjs conf/codex-bridge/test/app-server-stream.test.mjs > _runtime_export/tests.log 2>&1 || { cat _runtime_export/tests.log; exit 1; }
cat _runtime_export/tests.log
node --input-type=module <<'PAYLOAD'
import fs from 'node:fs';import path from 'node:path';import crypto from 'node:crypto';import cp from 'node:child_process';
import {collateExecutionPayload,validateExecutionPayload,EXECUTION_PAYLOAD_FILES} from './conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs';
const out=path.resolve('_runtime_export'),payload=path.join(out,'payload');fs.mkdirSync(payload);
await collateExecutionPayload(path.resolve('conf/codex-bridge'),path.join(payload,'codex-bridge'));
fs.cpSync(path.resolve('conf/codex-bridge/node_modules'),path.join(payload,'codex-bridge/node_modules'),{recursive:true,dereference:true,errorOnExist:true,force:false});
await validateExecutionPayload(path.join(payload,'codex-bridge'),{toolchain:false});
const installer=fs.readFileSync('conf/cyf-agent-runtime-v1/install.sh','utf8');
const lists=[...installer.matchAll(/for file in ([\s\S]*?); do\s+install -m (0[0-7]+) "\$SOURCE_DIR\/\$file"/g)];
if(lists.length!==2)throw Error('Runtime installer catalog changed');
for(const m of lists){for(const name of m[1].replace(/\\\n/g,' ').trim().split(/\s+/)){
 if(name.includes('..')||name.startsWith('/'))throw Error('Unsafe source path');
 const dest=path.join(payload,'runtime',name);fs.mkdirSync(path.dirname(dest),{recursive:true});fs.copyFileSync(path.join('conf/cyf-agent-runtime-v1',name),dest);fs.chmodSync(dest,parseInt(m[2],8));
}}
const files=[];function walk(dir){for(const e of fs.readdirSync(dir,{withFileTypes:true})){const p=path.join(dir,e.name);if(e.isDirectory())walk(p);else if(e.isFile())files.push({path:path.relative(payload,p),sha256:crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex'),mode:fs.statSync(p).mode&0o777});else throw Error('Unsafe payload')}}walk(payload);
const meta={pipeline:process.env.PIPELINE_ID,run:process.env.BUILD_NUMBER,commit:process.env.CI_COMMIT_SHA,tree:cp.execFileSync('git',['rev-parse','HEAD^{tree}'],{encoding:'utf8'}).trim(),version:JSON.parse(fs.readFileSync(path.join(payload,'runtime/package.json'))).version,engineFileCount:EXECUTION_PAYLOAD_FILES.length,files};
if(meta.version!=='1.3.21'||JSON.parse(fs.readFileSync('conf/codex-bridge/package.json')).version!=='1.1.12')throw Error('Unexpected candidate');
meta.dependencyProvenance={method:'same-Run npm ci --ignore-scripts --no-audit --no-fund',lockSha256:crypto.createHash('sha256').update(fs.readFileSync('conf/codex-bridge/package-lock.json')).digest('hex'),buildNode:process.versions.node,retainedPythonRequirementsSha256:crypto.createHash('sha256').update(fs.readFileSync('conf/codex-bridge/toolchain/requirements.txt')).digest('hex')};
fs.writeFileSync(path.join(out,'release.json'),JSON.stringify(meta,null,2)+'\n');
console.log('RUNTIME_PAYLOAD_FILES='+files.length);console.log('RUNTIME_SOURCE='+meta.commit);console.log('RUNTIME_TREE='+meta.tree);
PAYLOAD
python3 - <<'IMAGE_PACKAGE'
import hashlib, json, os, pathlib, stat, subprocess, zipfile
root=pathlib.Path('conf/skills/native-image').resolve()
out=pathlib.Path('_runtime_export').resolve()
raw=subprocess.check_output(['git','ls-files','-z','--','SKILL.md','scripts','vendor'],cwd=root)
names=sorted(os.fsdecode(x) for x in raw.split(b'\0') if x)
assert names and 'SKILL.md' in names and len(names)==len(set(names))
assert all(n=='SKILL.md' or n.startswith(('scripts/','vendor/')) for n in names)
for name in names:
    p=pathlib.PurePosixPath(name)
    assert not p.is_absolute() and '..' not in p.parts and not any(c in name for c in ('\n','\r','\x00'))
    q=root
    for part in p.parts:
        q=q/part
        st=q.lstat()
        assert not stat.S_ISLNK(st.st_mode)
    assert stat.S_ISREG(st.st_mode) and st.st_nlink==1
archive=out/'native-image.zip'
with zipfile.ZipFile(archive,'x',compression=zipfile.ZIP_DEFLATED) as z:
    for name in names: z.write(root/name,arcname=name)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None and sorted(z.namelist())==names
    assert all(not stat.S_ISLNK(i.external_attr >> 16) for i in z.infolist())
size=archive.stat().st_size
h=hashlib.sha256()
with archive.open('rb') as f:
    for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
meta={'commit':os.environ['CI_COMMIT_SHA'],'tree':subprocess.check_output(['git','rev-parse','HEAD^{tree}'],universal_newlines=True).strip(),'pipeline':os.environ['PIPELINE_ID'],'run':os.environ['BUILD_NUMBER'],'file':'native-image.zip','sha256':h.hexdigest(),'byteLength':size,'entries':names}
(out/'native-image-package.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
print('NATIVE_IMAGE_PACKAGE_SHA256='+h.hexdigest(),'BYTES='+str(size))
IMAGE_PACKAGE

CYF_SYSTEM_CODEX_BUILD
