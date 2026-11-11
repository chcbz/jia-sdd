from pathlib import Path
import subprocess,time,json,os
base=Path(__file__).parent; stage=base/'probe-stage';source=Path('/home/isp/apps/cyf-agent-runtime-v1/app')
ev=Path('/home/isp/wsps/cyf/docs/implementation/evidence/runtime-footprint-20261109')
start=time.monotonic()
env=dict(os.environ,TMPDIR=str(base/'tmp'),TMP=str(base/'tmp'),TEMP=str(base/'tmp'),PYTHONDONTWRITEBYTECODE='1')
subprocess.run(['cp','-a','--reflink=never',str(source/'runtime'),str(source/'node'),str(stage)],check=True,env=env)
children=[str(p) for p in (source/'codex-bridge').iterdir() if p.name not in ('.toolchain','.sandbox-toolchain')]
subprocess.run(['cp','-a','--reflink=never']+children+[str(stage/'codex-bridge')],check=True,env=env)
with (ev/'sandbox-rebuild.log').open('wb') as log:
 cmd=[str(stage/'node/bin/node'),str(stage/'runtime/lib/prepare-toolchain-image.mjs'),'--root',str(stage)]
 p=subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,timeout=120)
 result={'command':cmd,'seconds':time.monotonic()-start,'exitCode':p.returncode,'productionChanged':False}
 if p.returncode==0:
  result['stageAllocatedBytes']=int(subprocess.check_output(['du','-s','-B1',str(stage)]).split()[0])
  result['sourceAllocatedBytes']=int(subprocess.check_output(['du','-s','-B1',str(source)]).split()[0])
  result['savedAllocatedBytes']=result['sourceAllocatedBytes']-result['stageAllocatedBytes']
 (ev/'sandbox-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
