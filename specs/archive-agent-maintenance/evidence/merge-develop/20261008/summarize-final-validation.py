import pathlib,json,subprocess,hashlib,datetime,re,xml.etree.ElementTree as E
root=pathlib.Path(r'C:\Users\Think\.codex\worktrees\archive-agent-maintenance\cyf-web-kit');feature=root/'specs/archive-agent-maintenance';ev=feature/'evidence/merge-develop/20261008';server=ev/'server-results'
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
api=load(server/'attempt4/api-result.json');snap=load(server/'attempt4/final-source-snapshot.json');node=load(server/'node-final/result.json');base=load(ev/'api-local-attempt3/result.json');protected=load(ev/'protected-fixture-postmerge-proof.json')
def g(p,*a):return subprocess.check_output(['git','-c','core.longpaths=true','-C',str(p),*a],text=True).strip()
repos={'root':root,'api':root/'api','web':root/'web','client':root.parent/'isp-install'}
develop={'root':'7997310541164ff0b4586a17cd55c59a79c4d34e','api':'ce047c43e0f275d1ad427c484b8919213be36fa4','web':'dbfe20bca65d1939b37198bb55b5b95fd5fa2775','client':'0d80e588be271891348e38b8892d9b9a9b0bb436'}
now={}
for k,p in repos.items():
 sha=g(p,'rev-parse','HEAD');tree=g(p,'rev-parse','HEAD^{tree}');branch='codex/archive-agent-maintenance'+('' if k=='root' else '-'+k)
 assert g(p,'ls-remote','origin','refs/heads/'+branch).split()[0]==sha
 assert subprocess.call(['git','-C',str(p),'merge-base','--is-ancestor',develop[k],sha])==0
 if k!='root':assert sha==snap['repos'][k]['commit']==node['repos'][k]['commit'] and tree==snap['repos'][k]['tree']==node['repos'][k]['tree']
 now[k]={'branch':branch,'commit':sha,'tree':tree,'exact_remote_verified':True,'develop_merged':True}
assert api['source_unchanged'] and api['all_requested_suites_have_fresh_xml'] and snap['own_mysql_port34061_closed']
assert all(v['source_unchanged'] for v in snap['repos'].values()) and all(v['source_unchanged'] for v in node['repos'].values())
assert api['api_commit']==now['api']['commit'] and api['api_tree']==now['api']['tree']
for d in api['suites']:
 for f in d['fresh_xml']:assert hashlib.sha256((server/'attempt4'/d['task']/f['file']).read_bytes()).hexdigest()==f['sha256']
 assert d['tests']==d['pass']+d['failures']+d['errors']+d['skipped']
old=next(d for d in base['suites'] if d['task'].endswith('archiveRegression'))['failure_set'];new=next(d for d in api['suites'] if d['task']=='archiveRegression')['failure_set']
for f in protected['files']:
 p=repos[f['repository']];disk=(p/f['file']).read_bytes();blob=subprocess.check_output(['git','-C',str(p),'show','HEAD:'+f['file']]);assert disk==blob and hashlib.sha256(disk).hexdigest()==f['sha256']
accept=load(feature/'acceptance-cases.json');assert len(accept['cases'])==84 and all(c['status']=='not_run' and c['evidence'] is None for c in accept['cases'])
m=re.search(r'^pinned_revisions:\n(.*?)(?=^\S)',(feature/'integration.yaml').read_text(encoding='utf-8'),re.M|re.S);assert m
for k in ['api','web','client']:assert '  '+k+'_commit: '+now[k]['commit'] in m.group(0)
assert g(root,'ls-files','-s','api').split()[1]==now['api']['commit'] and g(root,'ls-files','-s','web').split()[1]==now['web']['commit']
r={'at':datetime.datetime.now().astimezone().isoformat(),'source_consistency_checks_passed':True,'current_remote_delivery_before_final_evidence_commit':now,'tested_server_root':snap['repos']['root']['commit'],'api':{'gradle_exit':api['gradle_exit'],'suites':[{k:d[k] for k in ['task','tests','pass','failures','errors','skipped']} for d in api['suites']],'archive_failure_methods_not_in_previous_observed_nonmysql_set':sorted(set(new)-set(old)),'archive_removed_previously_observed_failure_methods':sorted(set(old)-set(new)),'known_baseline_failure_methods':old,'baseline_scope':'Previous Windows archive suite: 11 failures and MySQL skips; unknown live MySQL failures must not be labeled merge-introduced without a runnable premerge comparison.'},'web':{'local_focused':load(ev/'node-local-harness-attempt3/web-component-result.json')['stats'],'linux_full':node['web']['stats'],'introduced_failures_vs_frozen_develop_affected_files':node['web']['introduced_vs_develop_four_files'],'remaining_failure_titles':[f['fullTitle'] for f in node['web']['failures']],'build_exit':node['web']['build_exit'],'real_browser_e2e':'not_run'},'client':node['client'],'protected_bytes_preserved':True,'own_mysql_port34061_closed':True,'business_acceptance_cases':84,'business_acceptance':'not_run','production_operations':False,'whole_feature_accepted':False,'boundary':'Source/pin/remote/fresh-XML/byte consistency only. Test failures remain recorded; component suites and bounded mocks are not complete Runtime/business acceptance.'}
(ev/'final-validation-summary.json').write_text(json.dumps(r,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:r[k] for k in ['source_consistency_checks_passed','api','client']},indent=2));print('WEB',r['web']['linux_full'],'INTRODUCED',r['web']['introduced_failures_vs_frozen_develop_affected_files'])