import ast,pathlib,json,hashlib,os,stat,tempfile,copy,unittest
P=pathlib.Path;B=P('/home/isp/state/cyf-local-build/tasks/cyf-beta-wen-cutover-20261107/runtime');I=B/'install';script=I/'install-local-artifact.py'
sha=lambda p:hashlib.file_digest(P(p).open('rb'),'sha256').hexdigest()
result=json.loads((B/'package-result.json').read_text());RECORDS=P('/home/isp/apps/cyf-agent-runtime-v1/release-records')
doc={'sourceKind':'LOCAL','commit':result['source']['commit'],'tree':result['source']['tree'],'version':result['version'],'buildId':result['buildId'],'buildEvidencePath':result['evidence']['path'],'buildEvidenceSha256':result['evidence']['sha256'],'artifactPath':result['artifact']['path'],'artifactSha256':result['artifact']['sha256'],'expectedPreviousRecordSha256':sha(RECORDS/'current.json')}
p=I/'local-release-input.json';p.write_text(json.dumps(doc,indent=2)+'\n');p.chmod(0o600)
# Only execute the pure source-admission function; never execute installer top level.
module=ast.parse(script.read_text());fn=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='load_local_source');ns=dict(P=P,os=os,stat=stat,json=json,sha=sha,RECORDS=RECORDS,COMMIT=doc['commit'],TREE=doc['tree']);exec(compile(ast.Module(body=[fn],type_ignores=[]),str(script),'exec'),ns);load=ns['load_local_source']
class SourceAdmission(unittest.TestCase):
 def test_real_local_artifact_and_linked_test_evidence(self):self.assertEqual(load(str(p),sha(p)),doc)
 def test_changed_input_hash(self):
  with self.assertRaises(AssertionError):load(str(p),'0'*64)
 def rejected(self,values):
  with tempfile.TemporaryDirectory(prefix='cyf-wen-admit-') as d:
   q=P(d)/'input.json';q.write_text(json.dumps({**doc,**values}));q.chmod(0o600)
   with self.assertRaises(AssertionError):load(str(q),sha(q))
 def test_reject_flow_identity(self):self.rejected({'pipeline':'5264702','run':'165'})
 def test_reject_source_change(self):self.rejected({'commit':'0'*40})
 def test_reject_artifact_change(self):self.rejected({'artifactSha256':'0'*64})
 def test_reject_evidence_change(self):self.rejected({'buildEvidenceSha256':'0'*64})
 def test_reject_predecessor_drift(self):self.rejected({'expectedPreviousRecordSha256':'0'*64})
 def test_reject_wrong_version(self):self.rejected({'version':'1.3.64'})
 def test_original_recovery_and_state_protections_retained(self):
  baseline=ast.parse(P('/home/isp/state/cyf-diagnostics/hall-three-issues-20261106/followup/deploy/runtime-install/install-local-artifact.py').read_text())
  names=('capture_writer_objects','retire_stopped_writer_objects','write_state_archive','manifest','critical','validate','persist_recovery_report')
  for name in names:
   old=next(n for n in baseline.body if isinstance(n,ast.FunctionDef) and n.name==name);new=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name==name)
   self.assertEqual(ast.dump(old),ast.dump(new),name)
r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(SourceAdmission))
receipt={'status':'PASS' if r.wasSuccessful() else 'FAIL','tests':r.testsRun,'failures':len(r.failures),'errors':len(r.errors),'installerSha256':sha(script),'descriptorSha256':sha(p),'scope':'Source admission + unchanged protection AST only; no staging, stopping, state write or installation executed'}
(I/'source-admission-tests.json').write_text(json.dumps(receipt,indent=2)+'\n');raise SystemExit(not r.wasSuccessful())
