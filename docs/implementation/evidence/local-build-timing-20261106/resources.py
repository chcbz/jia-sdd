import pathlib,json,datetime
D=pathlib.Path(__file__).resolve().parent
r=json.loads((D/'result.json').read_text())
s=[]
for line in (D/'host-samples.jsonl').read_text().splitlines():
 try:
  v=json.loads(line); v['ts']=datetime.datetime.fromisoformat(v['at']).timestamp();v['cpu']=list(map(int,v['cpuCounters'].split()[1:]));s.append(v)
 except (ValueError,KeyError):pass
out={}
for comp,c in r['components'].items():
 for st in c['stages']:
  if not st.get('startedAt'):continue
  lo=datetime.datetime.fromisoformat(st['startedAt']).timestamp();hi=datetime.datetime.fromisoformat(st.get('endedAt') or datetime.datetime.now(datetime.timezone.utc).isoformat()).timestamp()
  subset=[v for v in s if lo<=v['ts']<=hi]
  if len(subset)<2:continue
  delta=[b-a for a,b in zip(subset[0]['cpu'],subset[-1]['cpu'])];total=sum(delta[:8])
  out[comp+':'+st['name']]={'samples':len(subset),'sampledSeconds':round(subset[-1]['ts']-subset[0]['ts'],3),'ioWaitPercent':round(100*delta[4]/total,2),'cpuBusyPercent':round(100*(total-delta[3]-delta[4])/total,2),'memoryAvailableMinKiB':min(int(v['memory']['MemAvailable'].split()[0]) for v in subset),'diskAvailableMinBytes':min(v['diskAvailableBytes'] for v in subset),'minLoad1':min(float(v['load'].split()[0]) for v in subset),'maxLoad1':max(float(v['load'].split()[0]) for v in subset)}
(D/'resources-summary.json').write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))
