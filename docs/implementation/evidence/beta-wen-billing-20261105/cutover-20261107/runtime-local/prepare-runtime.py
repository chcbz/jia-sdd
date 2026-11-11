from pathlib import Path
import sys,json,hashlib,time
I=Path(__file__).resolve().parent;script=I/'install-local-artifact.py';descriptor=I/'local-release-input.json';source=script.read_text();marker='stopped=False;switched=False;new_started=False'
assert source.count(marker)==1
start=time.time();sys.argv=[str(script),str(descriptor),hashlib.sha256(descriptor.read_bytes()).hexdigest()]
ns={'__file__':str(script),'__name__':'runtime_prepare'}
exec(compile(source.split(marker)[0],str(script),'exec'),ns)
# Candidate is measured but the original stop/switch/start block has NOT run.
manifest=ns['manifest'](ns['stage']);ns['atomic'](I/'prepared.manifest.json',manifest)
state={'installerSha256':hashlib.sha256(script.read_bytes()).hexdigest(),'descriptorSha256':hashlib.sha256(descriptor.read_bytes()).hexdigest(),'stage':str(ns['stage']),'stageManifestSha256':ns['sha'](I/'prepared.manifest.json'),'before':ns['before'],'old':ns['old'],'meta':ns['meta'],'config':ns['config'],'report':ns['report'],'wallSeconds':round(time.time()-start,3),'status':'PREPARED_NOT_INSTALLED','serviceStopped':False}
ns['atomic'](I/'prepared.json',state);print(json.dumps({k:v for k,v in state.items() if k not in ('meta','config','before','old')},indent=2))
