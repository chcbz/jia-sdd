from pathlib import Path
import hashlib,json,subprocess,datetime
R=Path('/home/isp/wsps/cyf'); E=R/'docs/implementation/evidence/local-release-closure-20261107'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
m=json.loads((E/'directory-layout-migration.json').read_text())
for p,h in m['productionRecordsBefore'].items(): assert sha(p)==h
assert sha(R/'ops/maintenance/rebuildable_cache_cleanup.py')==sha('/usr/local/libexec/cyf/rebuildable_cache_cleanup.py')==m['sourceHelperSha256']
assert sha('/home/isp/state/cyf-host-cleanup/completed-tasks.json')==m['registryAfterSha256']
expected={'api-current':('api','e319b12a69039a20c5fc20afb0c001a025a07ca320afd6f74bc1bde6e9804a17'),'api-rollback':('api','877333fffa348a2ee9e56d9768c460fcdb37e7b4716a3ff4c89592bca4b7fd8e'),'web-current':('web','704fc894ac5894e759b15e40621a946e049d3ad778451092255aaaa80295add9')}
for suffix,(component,h) in expected.items():assert sha('/home/isp/pkgs/cyf/cyf-local-archive-20261107-'+suffix+'/package/'+component+'.tgz')==h
assert not Path('/home/isp/wsps/private-maintenance').exists()
assert not Path('/home/isp/wsps/cyf-worktrees').exists()
assert len(list(Path('/home/isp/baks/private-maintenance').iterdir()))==13
assert len(list(Path('/home/isp/wsps/worktrees').iterdir()))==15
assert Path('/proc/2168125').exists()
health=subprocess.check_output(['curl','--fail','--silent','--max-time','10','http://127.0.0.1:10018/actuator/health'],text=True)
assert 'UP' in health
counts={}
for name,n in [('rebuildable',69),('runtime',41),('flow',61),('shell',84)]:
 t=(E/('directory-layout-'+name+'-tests.log')).read_text();assert ('All 84 tests passed.' in t if name=='shell' else ('Ran '+str(n)+' tests' in t and '\nOK' in t));counts[name]=n
v={'verifiedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),'tests':counts,'totalTests':sum(counts.values()),'installedHelperMatchesSource':True,'packageHashesUnchanged':True,'productionRecordsUnchanged':True,'apiPidUnchanged':2168125,'apiHealth':json.loads(health),'oldPrivatePathAbsent':True,'emptyCyfWorktreesAbsent':True,'historicalArchiveDirectories':13,'legacySharedTaskDirectories':15,'noServiceRestart':True,'noPayloadSpaceReclaimedByRename':True}
(E/'directory-layout-verification.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(v,ensure_ascii=False,indent=2))
