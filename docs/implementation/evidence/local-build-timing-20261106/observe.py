import pathlib,json,time,datetime,subprocess
D=pathlib.Path(__file__).resolve().parent
with (D/'host-samples.jsonl').open('a',buffering=1) as out:
 while True:
  t=time.time();mem={}
  for line in pathlib.Path('/proc/meminfo').read_text().splitlines():
   k,v=line.split(':',1)
   if k in ['MemAvailable','MemFree','SwapFree']:mem[k]=v.strip()
  row={'at':datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8))).isoformat(),'cpuCounters':pathlib.Path('/proc/stat').read_text().splitlines()[0],'load':pathlib.Path('/proc/loadavg').read_text().strip(),'memory':mem,'diskAvailableBytes':__import__('shutil').disk_usage('/').free,'processes':subprocess.check_output(['ps','-eo','pid,ppid,pcpu,rss,comm']).decode().splitlines(),'observedGradleLock':False}
  log=D/'api-gradle.log'
  if log.exists() and 'GRADLE_LOCK_ACQUIRED task=LOCAL-BUILD-TIMING-20261106' in log.read_text(errors='replace'):
   row['observedGradleLock']=True
  out.write(json.dumps(row)+'\n')
  try:
   if json.loads((D/'result.json').read_text()).get('status')=='FINISHED':break
  except (FileNotFoundError,ValueError):pass
  time.sleep(max(1,5-(time.time()-t)))
