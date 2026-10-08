import pathlib,subprocess,re,json,datetime
r=pathlib.Path(r'C:\Users\Think\.codex\worktrees\archive-agent-maintenance\cyf-web-kit');f=r/'specs/archive-agent-maintenance/integration.yaml';s=f.read_text(encoding='utf-8');repos={'api':r/'api','web':r/'web','client':r.parent/'isp-install'}
def g(p,*a):return subprocess.check_output(['git','-C',str(p),*a],text=True).strip()
heads={k:g(p,'rev-parse','HEAD') for k,p in repos.items()}
for k,p in repos.items():
 assert not g(p,'status','--porcelain'),k
 branch='codex/archive-agent-maintenance-'+k
 assert g(p,'branch','--show-current')==branch
 assert g(p,'ls-remote','origin','refs/heads/'+branch).split()[0]==heads[k]
m=re.search(r'^pinned_revisions:\n(.*?)(?=^\S)',s,re.M|re.S);assert m
b=m.group(0)
for k,sha in heads.items():b,n=re.subn(r'^  '+k+r'_commit: [0-9a-f]{40}$','  '+k+'_commit: '+sha,b,flags=re.M);assert n==1
s=s[:m.start()]+b+s[m.end():]
s=s.replace('develop_merged_source_accepted_components_pushed_server_validation_pending','develop_merged_postmerge_repairs_pushed_server_retest_pending')
s=s.replace('status: merged_source_pushed_postmerge_mysql_initialization_repair_pushed_retest_pending','status: merged_source_pushed_postmerge_mysql_and_test_harness_repairs_pushed_retest_pending')
s=s.replace('server_validation: pending_exact_merged_remote_source','server_validation: attempt3_failed_repaired_source_pending_attempt4')
s=s.replace('after_fix_linux_mysql: pending','after_fix_linux_mysql: attempt3_completed_with_remaining_fixture_failures_37_mvp_48_archive')
s+='''
post_merge_fixture_harness_repair_20261008:
  status: source_reviewed_components_pushed_server_retest_pending
  api_commit: %s
  web_commit: %s
  client_commit: %s
  api_review: evidence/merge-develop/20261008/mysql-fixture-review-final.json
  node_review: evidence/merge-develop/20261008/node-harness-review-final.json
  baseline_comparison: evidence/merge-develop/20261008/server-results/node-develop-baseline/comparison.json
  real_runtime_browser: not_run
  business_acceptance: not_run
  production_changes: false
  whole_feature_accepted: false
''' % (heads['api'],heads['web'],heads['client'])
f.write_text(s,encoding='utf-8',newline='\n')
(r/'specs/archive-agent-maintenance/evidence/merge-develop/20261008/component-repair-pins.json').write_text(json.dumps({'at':datetime.datetime.now().astimezone().isoformat(),'components':{k:{'commit':v,'tree':g(repos[k],'rev-parse','HEAD^{tree}')} for k,v in heads.items()},'only_current_pin_block_updated_historical_hashes_preserved':True,'production_operation':False},indent=2)+'\n',encoding='utf-8')
print(heads)