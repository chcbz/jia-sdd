import io,base64,gzip,hashlib,json,pathlib,re
root=pathlib.Path('/home/isp/wsps/cyf'); work=pathlib.Path('/var/tmp/cyf-backend-flow-5m-20261016')
files={'ops/orchestration/cyf_orchestrator.py':(root/'ops/orchestration/cyf_orchestrator.py').read_text(),
       'docs/implementation/TASKS.yaml':(work/'task-snapshot.yaml').read_text(),
       'prepare-backend-jdk.py':(root/'ops/ci/aliyun-flow/prepare-backend-jdk.py').read_text(),
       'flow-compile-cache.init.gradle':(root/'ops/ci/aliyun-flow/flow-compile-cache.init.gradle').read_text()}
payload=json.dumps(files,sort_keys=True).encode();buffer=io.BytesIO()
with gzip.GzipFile(fileobj=buffer,mode='wb',mtime=0) as z: z.write(payload)
compressed=buffer.getvalue()
branch='codex/backend-flow-5m-20261016';sha='58b4b5f408257c6d5103d915e13c7927c1571e20';tree='3e60bd5858735790b7886ef00a9a94614816fb75'
preamble='''set -eu
export CYF_EXPERIMENT="$(mktemp -d /tmp/cyf-backend-flow-5m.XXXXXX)"
printf 'CYF_FLOW_PHASE runtime.begin wall=%s monotonic=' "$(date -u +%FT%TZ)"; cut -d' ' -f1 /proc/uptime
python3 - <<'CYFTOOLS'
import io,base64,gzip,hashlib,json,os,pathlib
raw=base64.b64decode('PAYLOAD',validate=True)
assert hashlib.sha256(raw).hexdigest()=='DIGEST', 'tool bundle hash mismatch'
root=pathlib.Path(os.environ['CYF_EXPERIMENT'])
for name,text in json.loads(gzip.decompress(raw).decode()).items():
 p=root/name
 p.parent.mkdir(mode=0o700,parents=True,exist_ok=True)
 p.write_text(text)
 p.chmod(0o600)
CYFTOOLS
python3 "$CYF_EXPERIMENT/prepare-backend-jdk.py" --cache "$HOME/.cache/cyf-backend-jdk-archives" --destination "$CYF_EXPERIMENT/jdk" > "$CYF_EXPERIMENT/jdk-result.txt"
cat "$CYF_EXPERIMENT/jdk-result.txt"
export JAVA_HOME="$(tail -1 "$CYF_EXPERIMENT/jdk-result.txt")"
export PATH="$JAVA_HOME/bin:$PATH"
java -version
printf 'CYF_FLOW_PHASE runtime.end wall=%s monotonic=' "$(date -u +%FT%TZ)"; cut -d' ' -f1 /proc/uptime
export CYF_FLOW_COMPILE_CACHE_OPT_IN=1
test "$CI_COMMIT_SHA" = "__SOURCE_SHA__"
test "$(git rev-parse HEAD^{tree})" = "TREE"
'''.replace('PAYLOAD',base64.b64encode(compressed).decode()).replace('DIGEST',hashlib.sha256(compressed).hexdigest()).replace('__SOURCE_SHA__',sha).replace('TREE',tree)
# Preserve original selectors, diagnostics and same-run package checks exactly.
s=(work/'before-run.sh').read_text(); s=s.replace('set -eu\n',preamble,1)
# Source commit5d54634 removed chatDeliberation and moved retained inputs.
# Reuse maintained tasks, executing every retained test class once.
mapped=json.loads((work/'chat-suite-dedup-selectors.json').read_text())
replacement=[]
for record in mapped:
 replacement.append('  :chat:jia-chat-service:'+record['task']+' \\')
 replacement.extend('  --tests '+name+' \\' for name in record['uniqueTests'])
s=s.replace('  :chat:jia-chat-service:chatDeliberation \\', '\n'.join(replacement))
s=s.replace('  :chat:jia-chat-service:test \\', '  :chat:jia-chat-service:test \\\n  --tests cn.jia.chat.api.ChatConversationEventsHttpTest \\\n  --tests cn.jia.chat.handler.SkillExecutionDeclarationTest \\')

s=s.replace('in develop|','in '+branch+'|develop|',1)
s=s.replace("not in ('develop',", "not in ('"+branch+"', 'develop',",1)
s=s.replace('export CYF_FLOW_BUILD_ROOT="$PWD/_cyf_flow_build"','export CYF_FLOW_BUILD_ROOT="$CYF_EXPERIMENT/build"')
s=s.replace("build = root / '_cyf_flow_build'","build = Path(env['CYF_FLOW_BUILD_ROOT'])")
s=s.replace('--project-cache-dir "$PWD/_cyf_project_cache"','--project-cache-dir "$CYF_EXPERIMENT/project-cache"')
fixture=hashlib.sha256((hashlib.sha256(compressed).hexdigest()+sha+hashlib.sha256(s.encode()).hexdigest()).encode()).hexdigest()
entry='''printf 'CYF_FLOW_PHASE gradle.begin wall=%s monotonic=' "$(date -u +%FT%TZ)"; cut -d' ' -f1 /proc/uptime
python3 "$CYF_EXPERIMENT/ops/orchestration/cyf_orchestrator.py" gradle --cwd "$PWD" --tree-sha TREE --selector backend-flow-5m-original-selectors-v1 --fixture-digest FIXTURE BACKEND-FLOW-5M-20261016 -- ./gradlew --build-cache'''.replace('TREE',tree).replace('FIXTURE',fixture)
s=s.replace('sh ./gradlew',entry,1)
s=s.replace('--init-script ops/ci/aliyun-flow/cold-init.gradle \\', '--init-script ops/ci/aliyun-flow/cold-init.gradle \\\n  --init-script "$CYF_EXPERIMENT/flow-compile-cache.init.gradle" \\',1)
s=s.replace('gradle_rc=$?\n','gradle_rc=$?\nprintf \'CYF_FLOW_PHASE gradle.end wall=%s monotonic=\' "$(date -u +%FT%TZ)"; cut -d\' \' -f1 /proc/uptime\n',1)
s+='\nprintf \'CYF_FLOW_PHASE package.end wall=%s monotonic=\' "$(date -u +%FT%TZ)"; cut -d\' \' -f1 /proc/uptime\n'
# The orchestrator checks all untracked source bytes: outputs stay outside checkout.
(work/'candidate-run.sh').write_text(s)
selectors=lambda x:re.findall(r'--tests\s+([^\s\\]+)|^\s+(:[^\s\\]+)',x,re.M)
assert set(selectors((work/'before-run.sh').read_text())) - {('', ':chat:jia-chat-service:chatDeliberation')} <= set(selectors(s))
(work/'candidate-proof.json').write_text(json.dumps({'source':sha,'tree':tree,'branch':branch,'toolBundleSha256':hashlib.sha256(compressed).hexdigest(),'fixtureDigest':fixture,'unchangedExistingSelectorsExceptRemovedTask':True,'removedTaskSourceCommit':'5d54634a3d3b279923ee87f61fc724767c6d8cbc','maintainedChatTestClasses':sum(len(r['uniqueTests']) for r in mapped),'selectorCount':len(selectors(s)),'noDeploy':True},indent=2)+'\n')
