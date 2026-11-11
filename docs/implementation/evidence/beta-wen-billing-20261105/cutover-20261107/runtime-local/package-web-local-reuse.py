import pathlib,json,hashlib,subprocess,tarfile,os,time,io
P=pathlib.Path; S=P('/home/isp/wsps/worktrees/beta-wen-billing-web');old=P('/tmp/cyf-beta-retirement-20261106/retained-web-build-b1c97e2');B=P('/home/isp/state/cyf-local-build/tasks/cyf-beta-wen-cutover-20261107/web');B.mkdir(parents=True,exist_ok=True)
def sha(p):return hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
def git(*a):return subprocess.check_output(['git',*a],cwd=S,text=True).strip()
assert not git('status','--porcelain');assert git('rev-parse','HEAD')=='b1c97e2ba909f08cda36eba8b7246027b30cfbeb'
archive=old/'cyf-web-1.16.124.tar.gz';assert sha(archive)=='8fe3c64ef10b7b8734ebe7b78d7e30016829efc8a60c02309b61e180490a6c95'
source={'commit':git('rev-parse','HEAD'),'tree':git('rev-parse','HEAD^{tree}')}
tests=['app-title','home-login-redirect','identity-scope','interface-wire','production-build-flags','public-entry-navigation','public-pwa-beta-entry','pwa-shell-freshness','hosting-rent','hosting-rent-ui','wen-amount','economy-wallet-bounty','economy-request-intent-storage','juyiting-assignee-recommendation','juyiting-agent-profile-capabilities']
cmd=['/home/isp/apps/node/bin/node','--import','tsx','./node_modules/mocha/bin/mocha.js','--no-config','--require','./tests/setup.js','--timeout','10000','--exit','--reporter','mochawesome','--reporter-options','reportDir='+str(B/'test-reports')+',reportFilename=mochawesome.json,consoleReporter=dot',*[f'tests/{n}.test.js' for n in tests]]
start=time.time()
assert '117 passing' in (B/'tests.log').read_text() # reuse fresh successful exact-input report; packaging-only retry
report=B/'test-reports/mochawesome.json';stats=json.loads(report.read_text())['stats'];assert stats['failures']==0
files={}
with tarfile.open(archive) as t:
 for m in t:
  if m.isdir():continue
  n=str(P(m.name).relative_to('dist'));assert m.isfile() and not P(n).is_absolute() and '..' not in P(n).parts
  data=t.extractfile(m).read();files[n]={'sha256':hashlib.sha256(data).hexdigest(),'size':len(data)}
  p=old/'web-dist'/n;assert p.is_file() and sha(p)==files[n]['sha256'],'BUILD_OUTPUT_DRIFT'
assert files and not git('status','--porcelain')
manifest={'format':'cyf-local-web-build-v2','buildId':'beta-wen-cutover-20261107-web','source':source,'version':'1.16.124','files':files,'scope':'Reuse exact verified b1c97e2 Vite output and original archive; fresh LOCAL release baseline and affected billing/UI tests; no rebuild or production operation','tests':{'reportSha256':sha(report),'selector':tests,'stats':{k:stats[k] for k in ['tests','passes','failures','pending']}}}
(B/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n');(B/'package').mkdir();pkg=B/'package/web.tgz'
with tarfile.open(archive) as inp,tarfile.open(pkg,'w:gz',compresslevel=1) as out:
 for m in inp:
  if m.isdir():continue
  m.name=str(P(m.name).relative_to('dist'));out.addfile(m,inp.extractfile(m))
 out.add(B/'manifest.json',arcname='cyf-local-build.json')
# Execute actual installed validator read-only against file manifest.
import runpy
helper=runpy.run_path('/usr/local/sbin/cyf-web-flow-deploy',run_name='local_validator')
# Its staged map is derived only from archive bytes, not trusting source entries.
staged={}
with tarfile.open(pkg) as t:
 for m in t:
  if m.name=='cyf-local-build.json':continue
  data=t.extractfile(m).read();staged[m.name]={'sha256':hashlib.sha256(data).hexdigest(),'size':len(data)}
assert staged==files
helper['validate_local_manifest']((B/'manifest.json').read_bytes(),{n:{**v,'path':old/'web-dist'/n} for n,v in staged.items()})
result={'status':'PACKAGED','source':source,'originalBuildEvidence':str(old/'result.json'),'originalArchiveSha256':sha(archive),'testCommand':cmd,'artifact':{'path':str(pkg),'sha256':sha(pkg),'size':pkg.stat().st_size},'stats':manifest['tests']['stats'],'wallSeconds':round(time.time()-start,3),'installed':False}
(B/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
