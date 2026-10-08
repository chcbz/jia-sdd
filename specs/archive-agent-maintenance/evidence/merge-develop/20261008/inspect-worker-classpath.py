import pathlib,shlex,os,json
files=sorted(pathlib.Path('/root/.gradle/.tmp').glob('gradle-worker-classpath*'),key=lambda x:x.stat().st_mtime,reverse=True)[:2]
for p in files:
 args=shlex.split(p.read_text())
 for i,a in enumerate(args):
  if a in ('-cp','-classpath'):
   entries=args[i+1].split(':')
   print(json.dumps({'file':str(p),'mtime':p.stat().st_mtime,'worker_entries':[{'path':x,'exists':os.path.exists(x)} for x in entries if 'worker' in x.lower()],'missing_entries':[x for x in entries if not os.path.exists(x)]}))
