from pathlib import Path
import unittest,tempfile,io,json,ast,hashlib,tarfile,sqlite3,os
I=Path(__file__).resolve().parent
source=(I/'install-local-artifact.py').read_text();prefix=source[:source.index('assert len(sys.argv)==3')]
class Integration(unittest.TestCase):
 def setUp(self):
  self.temp=tempfile.TemporaryDirectory(dir=I.parent/'tmp');self.addCleanup(self.temp.cleanup);self.base=Path(self.temp.name);self.root=self.base/'state';self.root.mkdir();self.back=self.base/'back';self.back.mkdir();self.ns={'__file__':str(I/'install-local-artifact.py')};exec(compile(prefix,'installer','exec'),self.ns);self.ns.update(TASK=self.base,build_id='fixture-local',artifact_sha='a'*64,local_source={'expectedPreviousRecordSha256':'b'*64})
 def archive(self):
  with (self.base/'backup.log').open('wb') as log:return self.ns['write_state_archive'](self.back/'state.tar.gz',[self.root],log)
 def test_real_adapter_archive_preserves_recovery_and_binding(self):
  (self.root/'authorization.json').write_text('fixture');digest=self.archive();receipt=json.loads((self.back/'state-scope.json').read_text());self.assertEqual(receipt['archiveSha256'],digest);self.assertEqual(receipt['releaseBinding']['commit'],self.ns['COMMIT']);self.assertEqual(receipt['releaseBinding']['buildId'],'fixture-local');self.assertEqual(json.loads((self.base/'state-scope.json').read_text()),receipt)
 def test_real_adapter_omits_only_known_probe(self):
  probe=self.root/'unified/agents/test/inspection-state/abcdef/measurement/.isolated-Ab1234';probe.mkdir(parents=True);(probe/'diagnostic').write_text('skip');(probe.parent/'unknown').write_text('keep');self.archive()
  with tarfile.open(self.back/'state.tar.gz') as t:names=t.getnames()
  self.assertFalse(any('.isolated-' in n for n in names));self.assertTrue(any(n.endswith('/unknown') for n in names));self.assertTrue((probe/'diagnostic').exists())
 def test_existing_backup_never_overwritten(self):
  self.archive()
  with self.assertRaises(ValueError):self.archive()
 def test_backup_failure_does_not_switch_program(self):
  nodes=ast.parse(source).body;transaction=next(n for n in nodes if isinstance(n,ast.Try) and any(isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='old_pid' for t in x.targets) for x in n.body));text=ast.get_source_segment(source,transaction);self.assertLess(text.index('systemctl\',\'stop'),text.index('write_state_archive'));self.assertLess(text.index('write_state_archive'),text.index('os.rename(APP,retired)'));self.assertIn('if stopped and not new_started:',text);self.assertNotIn('extractall',text)
 def test_no_strip_and_sandbox_digest_preserved(self):
  self.assertIn("slim.slim_staged_python(stage/'codex-bridge/.toolchain')",source);self.assertIn("'TOOLCHAIN_VIEW_CHANGED_REQUIRES_REVIEW'",source)
 def test_host_lock_precedes_release_lock(self):
  for n in ('prepare-runtime.py','apply-prepared-runtime.py'):
   x=(I/n).read_text();self.assertIn('cyf-host-cleanup.lock',x);self.assertLess(x.index('cyf-host-cleanup.lock'),x.index('exec('))
if __name__=='__main__':unittest.main(verbosity=2)
