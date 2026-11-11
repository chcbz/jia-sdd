"""Task-scoped index only: never change shared checkout, branch or real index. No push/build."""
import os, subprocess, pathlib, tempfile, json
ROOT=pathlib.Path('/home/isp/wsps/cyf'); OUT=ROOT/'specs/juyiting-assignee-recommendation/evidence'
files={
'api':[
'chat/jia-chat-service/src/main/java/cn/jia/chat/tool/AgentTools.java',
'agent/jia-agent-core/src/main/java/cn/jia/agent/entity/AgentTaskAssigneeCandidateDTO.java',
'agent/jia-agent-api/src/main/java/cn/jia/agent/service/AgentService.java',
'agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentController.java',
'agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentServiceImpl.java',
'agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentServiceImplTest.java',
'agent/jia-agent-service/src/test/java/cn/jia/agent/skill/SkillManagementRecommendationTest.java',
'chat/jia-chat-service/src/main/java/cn/jia/chat/api/AssigneeRecommendationController.java',
'chat/jia-chat-service/src/test/java/cn/jia/chat/api/AssigneeRecommendationControllerTest.java'],
'web':['src/composables/juyiting/hallAssigneeRecommendation.js','src/composables/juyiting/useHallData.js',
'src/components/juyiting/BountyPanel.vue','src/components/world/JuyiHall.vue',
'prototypes/juyiting/assignee-recommendation.js','prototypes/juyiting/assignee-recommendation.css',
'tests/juyiting-hall-data.test.js','tests/juyiting-assignee-recommendation.test.js',
'tests/juyiting-component-behavior.test.js','tests/juyiting-flow-ui.test.js']}
for kind in ['main','test']:
 files['api'] += [str(p.relative_to(ROOT/'api')) for p in (ROOT/'api/chat/jia-chat-service/src'/kind/'java/cn/jia/chat/service/recommendation').glob('*.java')]
summary={}
with tempfile.TemporaryDirectory(prefix='cyf-recommend-index-') as tmp:
 for repo, paths in files.items():
  if repo != 'api': continue
  env=os.environ.copy();env['GIT_INDEX_FILE']=str(pathlib.Path(tmp)/(repo+'.index'))
  def git(*args, **kwargs):return subprocess.check_output(['git','-C',str(ROOT/repo)]+list(args),env=env,**kwargs)
  git('read-tree','HEAD');git('add','--',*paths)
  def stage(path,text):
   blob=git('hash-object','-w','--stdin',input=text.encode()).decode().strip()
   git('update-index','--add','--cacheinfo','100644,'+blob+','+path)
  if repo=='api':
   path='agent/jia-agent-service/src/main/java/cn/jia/agent/skill/SkillManagementService.java'
   current=(ROOT/repo/path).read_text();a=current.index('    /** Read-only recommendation facts.');b=current.index('    public Map<String,Object> skills(',a)
   base=git('show','HEAD:'+path).decode();anchor='    public Map<String,Object> skills(HostingRentHttp.Actor a,String agent,boolean admin) {'
   assert anchor in base;stage(path,base.replace(anchor,current[a:b]+anchor));paths.append(path)
  else:
   path='prototypes/juyiting/index.html';base=git('show','HEAD:'+path).decode();stage(path,base.replace('</head>','<script defer src="assignee-recommendation.js?v=1"></script><link rel="stylesheet" href="assignee-recommendation.css?v=1"></head>'));paths.append(path)
   path='prototypes/juyiting/specs/prototype-spec.md';base=git('show','HEAD:'+path).decode();current=(ROOT/repo/path).read_text();a=current.index('\n## 智能推荐承办 R1');stage(path,base+current[a:]);paths.append(path)
  patch=git('diff','--cached','--binary','HEAD');(OUT/(repo+'.patch')).write_bytes(patch)
  summary[repo]={'head':git('rev-parse','HEAD').decode().strip(),'candidateTreeOnHead':git('write-tree').decode().strip(),'paths':paths}
  git('read-tree','origin/develop')
  result=subprocess.run(['git','-C',str(ROOT/repo),'apply','--cached','--3way','-'],input=patch,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  summary[repo]['integrationBase']=git('rev-parse','origin/develop').decode().strip()
  summary[repo]['applyToDevelopExit']=result.returncode
  (OUT/(repo+'-integration-check.log')).write_bytes(result.stdout+result.stderr)
  if result.returncode==0:summary[repo]['candidateTreeOnDevelop']=git('write-tree').decode().strip()
(OUT/'api-candidate.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:{x:v[x] for x in v if x!='paths'} for k,v in summary.items()},indent=2))
