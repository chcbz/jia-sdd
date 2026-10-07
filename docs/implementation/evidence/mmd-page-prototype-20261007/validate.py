#!/usr/bin/env python3
"""Scoped document/prototype checks; no application build or live writes."""
import hashlib,json,pathlib,re,subprocess
R=pathlib.Path('/home/isp/wsps/cyf');S=R/'specs/juyiting-multimedia-deliberation';P=S/'prototypes/complete-20261007';E=R/'docs/implementation/evidence/mmd-page-prototype-20261007'
def check():
 links=0
 selected=[S/n for n in ['README.md','design.md','acceptance.md','remaining-tasks-20261007.md','shortest-flow-test-20261007.md','page-interaction-prototype-20261007.md']]+[S/'prototypes/README.md',P/'README.md',E/'report.md']
 # For old large entry documents, only validate this task's dated header, not historical archives.
 for f in selected:
  text=f.read_text()
  if f.name in ['design.md','acceptance.md'] or f==S/'README.md' or f==S/'prototypes/README.md':text=text.split('\n\n',1)[0]
  for t in re.findall(r'\]\(([^)]+)\)',text):
   if t.startswith(('http:','https:','#')):continue
   assert (f.parent/t.split('#')[0].split('?')[0]).exists(),(str(f),t);links+=1
 for f in [P/'index.html',P/'scenarios.html']:
  for t in re.findall(r'(?:src|href)="([^"]+)"',f.read_text()):
   if t.startswith(('data:','http:','https:','#')):continue
   assert (f.parent/t.split('?')[0]).exists(),(str(f),t);links+=1
 v=json.loads((P/'prototype-checks.json').read_text());assert v['notProductionAcceptance'] is True and not v['errors'];assert all(x['pass'] for x in v['checks'])
 for f,h in v['sourceHashes'].items():assert hashlib.sha256((P/f).read_bytes()).hexdigest()==h,f
 sf=json.loads((E/'sf05-visible-dom.json').read_text());bs=sf['blocks'];assert len(bs)==2 and bs[0]['text']==bs[1]['text'] and all(x['rect']['width']>0 and x['rect']['height']>0 and x['display']=='block' and x['visibility']=='visible' for x in bs)
 net=json.loads((E/'network-summary.json').read_text());assert not net['unclassifiedPOST'];assert all(x==0 for x in net['businessActionsInvoked'].values())
 for f in E.glob('*.json'):
  if f.name not in ['validation.json','manifest.json']:json.loads(f.read_text())
 yaml="const fs=require('fs'),yaml=require('./web/node_modules/js-yaml');const x=yaml.load(fs.readFileSync('specs/juyiting-multimedia-deliberation/integration.yaml','utf8')).latest_status_20261007;if(x.overall!=='NOT_COMPLETE'||x.interaction_prototype_status!=='OFFLINE_DESIGN_ONLY_NOT_PRODUCT_FIX'||x.interaction_prototype_production_deployed!==false)throw Error('inconsistent status');"
 subprocess.check_call(['node','-e',yaml],cwd=str(R))
 return {'status':'PASS_DOCUMENT_PROTOTYPE_CHECKS','linksChecked':links,'prototypeChecks':len(v['checks']),'layoutChecks':len(v['layouts']),'browserErrors':len(v['errors']),'SF05':'CONFIRMED_VISIBLE_DUPLICATION_NOT_SERVER_DUPLICATE','fullProduct':'NOT_COMPLETE','applicationBuilds':0,'deployments':0,'newBusinessActions':0}
if __name__=='__main__':print(json.dumps(check(),ensure_ascii=False,indent=2))
