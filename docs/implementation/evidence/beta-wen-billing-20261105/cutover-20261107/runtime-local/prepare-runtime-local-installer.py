from pathlib import Path
import shutil
base=Path('/home/isp/state/cyf-diagnostics/hall-three-issues-20261106/followup/deploy/runtime-install');out=Path('/home/isp/state/cyf-local-build/tasks/cyf-beta-wen-cutover-20261107/runtime/install');out.mkdir(mode=0o700)
s=(base/'install-local-artifact.py').read_text()
s=s.replace("TASK=P('/home/isp/state/cyf-diagnostics/hall-three-issues-20261106/followup/deploy/runtime-install')", "TASK=P(__file__).resolve().parent")
s=s.replace("BACK=P('/home/isp/baks/cyf-agent-runtime-v1/20261106-hall-followup-166')", "BACK=P('/home/isp/baks/cyf-agent-runtime-v1/20261107-beta-wen-local')")
s=s.replace("COMMIT='c1fc18174b256c90051874485c8c77967efad62a'; TREE='9dc7ef80bbdd135cf81386a424d68f4c7ca95a0d'", "COMMIT='d7e51840f2cfc3cea6afda5a7e7e8d1b07d3f776'; TREE='36ce18f7c3b433ad085c3d02eef843bb87304144'")
a=s.index('def load_local_source(');b=s.index("assert len(sys.argv)==3",a)
s=s[:a]+'''def load_local_source(input_path, expected_input_sha):
 path=P(input_path);st=path.lstat()
 assert path.is_absolute() and stat.S_ISREG(st.st_mode) and st.st_uid==os.geteuid() and stat.S_IMODE(st.st_mode)==0o600
 assert sha(path)==expected_input_sha,'LOCAL_INPUT_CHANGED'
 local=json.loads(path.read_text())
 assert local['sourceKind']=='LOCAL' and not any(k in local for k in ('pipeline','run','flowStatus','buildJobId')),'GENUINE_LOCAL_SOURCE_REQUIRED'
 assert local['commit']==COMMIT and local['tree']==TREE and local['version']=='1.3.66'
 assert local['buildId']=='beta-wen-cutover-20261107-runtime'
 evidence=P(local['buildEvidencePath']);assert sha(evidence)==local['buildEvidenceSha256'],'SOURCE_EVIDENCE_CHANGED'
 proof=json.loads(evidence.read_text())
 assert proof['format']=='cyf-runtime-local-evidence-v1' and proof['status']=='VERIFIED_WITH_EXACT_INPUT_REUSE'
 assert proof['source']=={'commit':COMMIT,'tree':TREE},'SOURCE_MISMATCH'
 for key in ('base','followup'):
  item=proof[key];result_path=P(item['path']);assert sha(result_path)==item['sha256'],'TEST_EVIDENCE_CHANGED'
  result=json.loads(result_path.read_text());assert result['sourceUnchanged']
  assert sha(result_path.parent/'tests.log')==item['testsLogSha256']==result['testsLogSha256'],'TEST_LOG_CHANGED'
 follow=json.loads(P(proof['followup']['path']).read_text())
 assert follow['exitCode']==0 and follow['sourceCommit']==COMMIT and follow['sourceTree']==TREE,'FOLLOWUP_NOT_VERIFIED'
 assert sha(P(local['artifactPath']))==local['artifactSha256'],'ARTIFACT_CHANGED'
 assert sha(RECORDS/'current.json')==local['expectedPreviousRecordSha256'],'PREDECESSOR_CHANGED'
 return local
''' +s[b:]
s=s.replace("local_source=load_local_source(sys.argv[1],sys.argv[2]);run_id=local_source['run']", "local_source=load_local_source(sys.argv[1],sys.argv[2]);build_id=local_source['buildId']")
s=s.replace("meta['version']=='1.3.65'", "meta['version']=='1.3.66'")
s=s.replace("assert str(meta['pipeline'])=='5264702' and str(meta['run'])==run_id", "assert meta['sourceKind']=='LOCAL' and meta['buildId']==build_id and meta['buildEvidenceSha256']==local_source['buildEvidenceSha256']\nassert sha(extract/'build-evidence.json')==local_source['buildEvidenceSha256']")
s=s.replace("old['runtimeVersion']=='1.3.61' and old['sourceCommit']=='cfe99ae99effaf502a7c516f86aeb50f9808085a'", "old['runtimeVersion']=='1.3.65' and old['sourceCommit']=='c1fc18174b256c90051874485c8c77967efad62a'")
s=s.replace("old_lock['version']=='1.1.50' and new_lock['version']=='1.1.54'", "old_lock['version']=='1.1.54' and new_lock['version']=='1.1.55'")
s=s.replace("'.hall-followup-166-candidate'", "'.beta-wen-local-candidate'")
s=s.replace("'executionLocation':'host-after-flow','sourceFlowStatus':local_source['flowStatus'],'sourceBuildJobId':local_source['buildJobId'],'pipeline':'5264702','run':run_id", "'executionLocation':'host-local','sourceKind':'LOCAL','buildId':build_id")
s=s.replace("'flowArtifactSha256':artifact_sha", "'artifactSha256':artifact_sha")
s=s.replace("'version':'1.3.65'", "'version':'1.3.66'")
s=s.replace("'1.3.65.manifest.json'", "'1.3.66.manifest.json'")
s=s.replace("'runtimeVersion':'1.3.65'", "'runtimeVersion':'1.3.66'")
s=s.replace("'pipeline':'5264702','run':run_id", "'sourceKind':'LOCAL','buildId':build_id")
s=s.replace("'npmLockedFromSameRun':meta['dependencyProvenance']", "'npmLockedDependencies':meta['dependencyProvenance']")
s=s.replace("'executionLocation':'host-after-flow','sourceFlowStatus':local_source['flowStatus']", "'executionLocation':'host-local'")
s=s.replace("2026-11-06 Runtime1.3.65 '+COMMIT+' Flow5264702/'+run_id+':", "2026-11-07 Runtime1.3.66 '+COMMIT+' LOCAL '+build_id+':")
s=s.replace("RUNTIME_INSTALL_COMPLETE version=1.3.65 run='+run_id", "RUNTIME_INSTALL_COMPLETE version=1.3.66 build='+build_id")
s=s.replace('UNSAFE_FLOW_ARTIFACT','UNSAFE_LOCAL_ARTIFACT').replace('# This fixed Flow artifact', '# This fixed LOCAL artifact')
s=s.replace('This task preserves scoped CHAT threads across ordinary and material turns; no identity migration;', 'This task installs usage accounting with retained production startup recovery; no identity migration;')
s=s.replace('Python/browser toolchains retain the verified Run155 baseline', 'Python/browser toolchains retain the current verified production baseline')
s=s.replace('runtime-release/install-flow-artifact.py', 'runtime-release/install-flow-artifact.py; explicit LOCAL-source adaptation')
assert 'run_id' not in s and "local_source['flowStatus']" not in s
(out/'install-local-artifact.py').write_text(s)
for name in ('verify-startup-readiness.mjs','verify-installed-carriers.mjs'):
 shutil.copy2(base/name,out/name)
# Host probes come from this exact tested candidate, never older copied fixtures.
import json,hashlib
src=Path('/home/isp/wsps/worktrees/beta-wen-billing-runtime/conf/codex-bridge/test');(out/'host-probes').mkdir()
probes=[]
for n in ('native-document-toolchain.test.mjs','native-browser-toolchain.test.mjs','native-browser-execution-profile.test.mjs'):
 shutil.copy2(src/n,out/'host-probes'/n);probes.append({'file':n,'sha256':hashlib.sha256((src/n).read_bytes()).hexdigest()})
(out/'host-probe-source.json').write_text(json.dumps({'sourceCommit':'d7e51840f2cfc3cea6afda5a7e7e8d1b07d3f776','probes':probes},indent=2)+'\n')
print(out)
