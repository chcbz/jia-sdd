from pathlib import Path
import subprocess,json,hashlib
root=Path('/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/api-entry-finalization-integration-v1')
e=Path('/home/isp/wsps/cyf/evidence/u1u3-entry-finalization-integration-v1')
h=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
git=lambda *args:subprocess.check_output(['git','-C',str(root)]+list(args)).decode().strip()
sha=git('rev-parse','HEAD');tree=git('rev-parse','HEAD^{tree}')
changed=git('diff','--name-only','194ec91a',sha,'--','*.java').splitlines()
main=[p for p in changed if '/src/main/java/' in p]
test=[p for p in changed if ('/src/test/java/' in p or '/src/chatDeliberationTest/java/' in p) and not p.endswith('ChatSchemaReadinessLifecycleTest.java')]
test.append('agent/jia-agent-service/src/test/java/cn/jia/agent/config/AgentTaskExecutionGrantSchemaContractTest.java')
resources=['agent/jia-agent-mapper/src/main/resources/db/agent-selected-output-finalization-v1.sql','chat/jia-chat-mapper/src/main/resources/db/chat-selected-output-finalization-v1.sql']
old=json.loads(Path('/home/isp/wsps/cyf/evidence/u4-schema-readiness-v1/bounded-source-manifest-v3.json').read_text())
manifest={'schema_version':1,'candidate_commit':sha,'candidate_tree':tree,'main_source_count':len(main),'test_source_count':len(test),'sources':[{'path':str(root/p),'relative_path':p,'kind':'main' if p in main else 'test' if p in test else 'resource','sha256':h(root/p),'size_bytes':(root/p).stat().st_size} for p in main+test+resources],'lombok':old['lombok']}
manifestPath=e/'bounded-sources-v3.json';manifestPath.write_text(json.dumps(manifest,indent=2)+'\n')
classes=[p.split('/java/',1)[1].replace('/','.').replace('.java','') for p in test]
base=Path('/home/isp/wsps/cyf/evidence/u4-schema-readiness-v1/bounded-schema-readiness-v3.init.gradle').read_text()
base=base.replace("final String TASK_PREFIX = 'u4BoundedV3'","final String TASK_PREFIX = 'mmdEntryFinalV3'")
base=base.replace("final File evidenceRoot = new File('/home/isp/wsps/cyf/evidence/u4-schema-readiness-v1')","final File evidenceRoot = new File('"+str(e)+"')")
base=base.replace("final File runRoot = new File(evidenceRoot, 'bounded-b6ad3746-v3')","final File runRoot = new File(evidenceRoot, 'bounded-"+tree[:8]+"-v3')")
base=base.replace("final File classLoadLog = new File(runRoot, 'class-load.log')","final File classLoadLog = new File(runRoot, 'class-load-%p.log')")
for name in ['bounded-classpath-v1.txt','bounded-classpath-content-v1.json']:
 base=base.replace("new File(evidenceRoot, '"+name+"')","new File('/home/isp/wsps/cyf/evidence/u4-schema-readiness-v1/"+name+"')")
base=base.replace("new File(evidenceRoot, 'bounded-source-manifest-v3.json')","new File(evidenceRoot, 'bounded-sources-v3.json')")
base=base.replace('a794e5b1b7a4f9fb287783f114f4190d09040c73ac09c9e4edb51e0a7c3de991',h(manifestPath))
base=base.replace('399cb3c30002c728a2329a6347f1f4d15f2d3fcf',sha).replace('b6ad3746c235e91ae1cae15278636b66f1b253bf',tree)
a=base.index('    def mainSourcePaths = [');b=base.index('\n    def preflight',a)
base=base[:a]+"    def mainSourcePaths = [\n"+',\n'.join("            new File(root.rootDir, '"+p+"')" for p in main)+"\n    ]\n    def selectedTestSources = [\n"+',\n'.join("            new File(root.rootDir, '"+p+"')" for p in test)+"\n    ]\n    def resources = [\n"+',\n'.join("            new File(root.rootDir, '"+p+"')" for p in resources)+"\n    ]\n"+base[b:]
base=base.replace('source_count: 5','main_source_count: '+str(len(main))+',\n                    test_source_count: '+str(len(test)))
base=base.replace('CompileLifecycleTest','CompileSelectedTests').replace('SchemaReadinessLifecycle','SelectedContracts')
base=base.replace('source(root.files(lifecycleSource.absolutePath))','source(root.files(selectedTestSources))')
base=base.replace("doLast { writeClassManifest(mainOverlay, new File(runRoot, 'main-overlay-manifest.json')) }", """doLast {
            resources.each { resource ->
                File target = new File(mainOverlay, 'db/' + resource.name)
                target.parentFile.mkdirs()
                target.bytes = resource.bytes
            }
            writeClassManifest(mainOverlay, new File(runRoot, 'main-overlay-manifest.json'))
        }""")
base=base.replace("includeTestsMatching('cn.jia.chat.config.ChatSchemaReadinessLifecycleTest')",'\n            '.join("includeTestsMatching('"+c+"')" for c in classes))
base=base.replace('forkEvery = 0','forkEvery = 1')
base=base.replace("if (!classLoadLog.isFile()) throw new GradleException('Missing JVM class-load proof')\n            String loaded = classLoadLog.getText('UTF-8')", """List<File> logs = runRoot.listFiles().findAll { it.name.startsWith('class-load-') && it.name.endsWith('.log') }
            if (logs.isEmpty()) throw new GradleException('Missing JVM class-load proof')
            String loaded = logs.collect { it.getText('UTF-8') }.join('\\n')""")
a=base.index('            Map<String, String> expected = [');b=base.index('            Map<String, List<String>> proof',a)
needed=['cn.jia.agent.service.impl.AgentTaskExecutionGrantServiceImpl','cn.jia.agent.api.AgentController','cn.jia.agent.service.impl.AgentTaskRequirementSnapshotServiceImpl','cn.jia.agent.service.impl.AgentTaskDeliberationOperationReadServiceImpl','cn.jia.agent.service.impl.AgentSelectedOutputFinalizationServiceImpl','cn.jia.chat.service.ChatSelectedOutputFinalizationService','cn.jia.chat.api.AgentTaskSelectedOutputFinalizationController','cn.jia.agent.config.AgentSelectedOutputFinalizationSchemaInitializer','cn.jia.chat.config.ChatSelectedOutputFinalizationSchemaInitializer']
base=base[:a]+"            Map<String, String> expected = [\n"+',\n'.join("                    '"+c+"': mainOverlay.absolutePath" for c in needed)+',\n'+',\n'.join("                    '"+c+"': testOverlay.absolutePath" for c in classes)+"\n            ]\n"+base[b:]
base=base.replace('bounded-task-graph-b6ad3746-v3.json','bounded-task-graph-'+tree[:8]+'-v3.json')
init=e/'bounded-entry-finalization-v3.init.gradle';init.write_text(base)
plan={'candidate_commit':sha,'candidate_tree':tree,'baseline':'194ec91a','verification_scope':'bounded exact changed main sources and selected actual tests; NOT normal module build or MySQL or product acceptance','main_sources':len(main),'test_sources':len(test),'resources':len(resources),'selector':':mmdEntryFinalV3SelectedContracts','class_filters':classes,'classpath_entries':364,'no_built_by_dependency_graph':True,'source_manifest_sha256':h(manifestPath),'init_sha256':h(init),'gradle_jvm':'-Xmx256m -XX:MaxMetaspaceSize=160m -XX:ActiveProcessorCount=2 -XX:+UseSerialGC','test_jvm':'-Xmx128m -XX:MaxMetaspaceSize=96m -XX:ActiveProcessorCount=1 -XX:+UseSerialGC','forkEvery':1,'resource_caps_not_admission_gates':True,'original_tree_unchanged':True,'source_diagnosis':['null sub_part mapped before Optional.findFirst throws NPE; select entry before nullable value mapping','new schema mutex must wait under user policy, GET_LOCK(-1) semantic indefinite not arbitrary higher deadline']}
plan['fixture_digest']=hashlib.sha256(json.dumps(plan,sort_keys=True).encode()).hexdigest();(e/'bounded-plan-v3.json').write_text(json.dumps(plan,indent=2)+'\n')
print(json.dumps(plan,indent=2))
