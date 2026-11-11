from pathlib import Path
import json,hashlib
root=Path('/home/isp/wsps/cyf/evidence/u1u3-entry-finalization-integration-v1')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
p=json.loads((root/'bounded-plan-v1.json').read_text())
oldRun=root/'bounded-db276cb9-v1'
def dh(d):
 digest=hashlib.sha256();count=0;size=0
 for f in sorted([f for f in d.rglob('*') if f.is_file()],key=lambda f:str(f.relative_to(d))):
  r=str(f.relative_to(d));l=f.stat().st_size;digest.update((r+'\0'+str(l)+'\0'+h(f)+'\n').encode());count+=1;size+=l
 return {'sha256':digest.hexdigest(),'file_count':count,'size_bytes':size}
compiled={'main_overlay':{'path':str(oldRun/'main-overlay'),**dh(oldRun/'main-overlay')},'test_overlay':{'path':str(oldRun/'test-overlay'),**dh(oldRun/'test-overlay')},'prior_compile_log':{'path':str(root/'gradle-bounded-v1-configuration-fixed.log'),'sha256':h(root/'gradle-bounded-v1-configuration-fixed.log')},'main_manifest_sha256':h(oldRun/'main-overlay-manifest.json'),'test_manifest_sha256':h(oldRun/'test-overlay-manifest.json')}
(root/'verified-compiled-overlay-reuse-v2.json').write_text(json.dumps(compiled,indent=2)+'\n')
s=(root/'bounded-entry-finalization-v1.init.gradle').read_text()
s=s.replace("final String TASK_PREFIX = 'mmdEntryFinalV1'","final String TASK_PREFIX = 'mmdEntryFinalV2'")
s=s.replace("final File runRoot = new File(evidenceRoot, 'bounded-db276cb9-v1')","final File runRoot = new File(evidenceRoot, 'test-db276cb9-v2')")
s=s.replace("final File mainOverlay = new File(runRoot, 'main-overlay')","final File mainOverlay = new File('"+str(oldRun/'main-overlay')+"')")
s=s.replace("final File testOverlay = new File(runRoot, 'test-overlay')","final File testOverlay = new File('"+str(oldRun/'test-overlay')+"')")
s=s.replace("includeTestsMatching('cn.jia.chat.config.ChatSelectedContractsTest')",'\n            '.join("includeTestsMatching('"+c+"')" for c in p['class_filters']))
a=s.index('    def compileMain = root.tasks.register(');b=s.index('    def lifecycleTest = root.tasks.register(',a)
s=s[:a]+s[b:]
s=s.replace('dependsOn(compileTest)','dependsOn(preflight)')
s=s.replace('                    compileMain.get().path,\n                    compileTest.get().path,\n','')
s=s.replace('bounded-task-graph-db276cb9-v1.json','bounded-task-graph-db276cb9-v2.json')
needle='            runRoot.mkdirs()'
check=''
for k in ['main_overlay','test_overlay']:
 val=compiled[k];d='mainOverlay' if k=='main_overlay' else 'testOverlay'
 check+="""            def %sDigest = sha256Directory(%s)
            if (%sDigest.sha256 != '%s' || %sDigest.fileCount != %s || %sDigest.sizeBytes != %s)
                throw new GradleException('Exact unchanged compiled %s reuse failed')
"""%(d,d,d,val['sha256'],d,val['file_count'],d,val['size_bytes'],k)
s=s.replace(needle,check+needle)
init=root/'bounded-entry-finalization-v2.init.gradle';init.write_text(s)
actual=[x.split("includeTestsMatching('",1)[1].split("')",1)[0] for x in s.splitlines() if "includeTestsMatching('" in x]
assert actual==p['class_filters'],(actual,p['class_filters'])
p['schema_version']=2;p['selector']=':mmdEntryFinalV2SelectedContracts';p['init_sha256']=h(init);p['compilation_reused_from_exact_same_source_tree']=compiled;p['task_graph']=[':mmdEntryFinalV2Preflight',':mmdEntryFinalV2SelectedContracts'];p['retained_failures']=['CLI positional REMAINDER misplaced options: no Gradle','v1 missing non-secret publication placeholders: no preflight/compile/tests','v1 exact25main+10test compiled; template filter was renamed before replacement; no JUnit tests ran'];p.pop('fixture_digest');p['fixture_digest']=hashlib.sha256(json.dumps(p,sort_keys=True).encode()).hexdigest();(root/'bounded-plan-v2.json').write_text(json.dumps(p,indent=2)+'\n')
print('PASS exact filters10, two-task graph, verified same-source compiled overlays; fixture='+p['fixture_digest'])
