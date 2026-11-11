"""Resume the original controlled Runtime transaction from a verified prepared candidate.
Has production side effects. Never rerun the prepare phase or restore business state.
"""
from pathlib import Path
import json,hashlib,ast,os,fcntl,sys,datetime
I=Path(__file__).resolve().parent;script=I/'install-local-artifact.py';source=script.read_text();prepared=json.loads((I/'prepared.json').read_text());descriptor=I/'local-release-input.json'
sha=lambda p:hashlib.file_digest(p.open('rb'),'sha256').hexdigest()
assert sys.argv[1:]==['--install'],'explicit --install required'
assert sha(script)==prepared['installerSha256'] and sha(descriptor)==prepared['descriptorSha256'],'PREPARATION_INPUT_CHANGED'
ns={'__file__':str(script),'__name__':'runtime_apply_prepared'}
exec(compile(source[:source.index('assert len(sys.argv)==3')],str(script),'exec'),ns)
lockpath=Path('/run/lock/cyf-wuyong-versioned-release.lock');fd=os.open(lockpath,os.O_RDWR|os.O_NOFOLLOW);fcntl.flock(fd,fcntl.LOCK_EX|fcntl.LOCK_NB);assert os.fstat(fd).st_ino==lockpath.lstat().st_ino
local=ns['load_local_source'](str(descriptor),prepared['descriptorSha256'])
assert sha(I/'prepared.manifest.json')==prepared['stageManifestSha256']
stage=Path(prepared['stage']);assert ns['manifest'](stage)==json.loads((I/'prepared.manifest.json').read_text()),'PREPARED_PROGRAM_DRIFT'
assert ns['critical']()==prepared['before'],'IDENTITY_OR_CONFIG_CHANGED'
current=json.loads((ns['RECORDS']/'current.json').read_text());assert current==prepared['old'],'BASELINE_RECORD_CHANGED'
assert sorted(ns['manifest'](ns['APP']),key=lambda x:x['path'])==sorted(json.loads((ns['RECORDS']/'current.manifest.json').read_text()),key=lambda x:x['path']),'BASELINE_PROGRAM_DRIFT'
ns.update(local_source=local,build_id=local['buildId'],artifact_sha=local['artifactSha256'],config=prepared['config'],before=prepared['before'],old=prepared['old'],meta=prepared['meta'],report=prepared['report'],stage=stage)
# Reuse the original live-inbox enumeration, not the preparation-time snapshot.
module=ast.parse(source);fn=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='inbox_roots');exec(compile(ast.Module(body=[fn],type_ignores=[]),str(script),'exec'),ns)
ns['report']['applyStartedAt']=datetime.datetime.now(datetime.timezone.utc).isoformat()
ns['signal'].signal(ns['signal'].SIGTERM,ns['terminated']) if 'terminated' in ns else None
# The signal handler is defined between preparation and application in the original.
fn=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='terminated');exec(compile(ast.Module(body=[fn],type_ignores=[]),str(script),'exec'),ns)
ns['signal'].signal(ns['signal'].SIGTERM,ns['terminated']);ns['signal'].signal(ns['signal'].SIGINT,ns['terminated'])
exec(compile(source[source.index('stopped=False;switched=False;new_started=False'):],str(script),'exec'),ns)
