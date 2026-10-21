"""Offline control-flow/partial-DDL diagnostics; never invokes production main/lifecycle/DB."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch
spec=importlib.util.spec_from_file_location('d31',Path(__file__).with_name('flow-migrate.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class MigrationContract(unittest.TestCase):
    def hook_case(self, outcome=None, migration_error=False):
        calls=[];migration=Mock();adapter=Mock();adapter.LOCK='fixture'
        migration.run_locked.side_effect=lambda: calls.append('migration')
        migration.mark.side_effect=lambda *a,**k:calls.append(a[0])
        migration.failed_install_stop.side_effect=lambda:calls.append('stop-failed-candidate')
        if migration_error: migration.run_locked.side_effect=m.Blocked('PROOF_FAILED')
        def original(path):
            self.assertEqual(path,m.INSTALLER);self.assertEqual(os.environ['CYF_API_FLOW_FORWARD_ONLY'],'1')
            calls.append('original-adapter')
            if isinstance(outcome,BaseException): raise outcome
            return outcome or 0
        with patch.object(m,'held_coordinator',side_effect=lambda _:calls.append('held')),patch.dict(os.environ,{},clear=True):
            hook=m.install_hook(adapter,migration,original)
            if migration_error or isinstance(outcome,BaseException):
                with self.assertRaises((m.Blocked,ValueError)):hook(m.INSTALLER)
            else:self.assertEqual(hook(m.INSTALLER),outcome or 0)
        return calls
    def test_original_admission_and_migration_precede_start(self):
        self.assertEqual(self.hook_case(),['migration','held','ORIGINAL_INSTALLER_CALLED','original-adapter','ORIGINAL_INSTALLER_VERIFIED'])
    def test_proof_failure_never_calls_installer(self):self.assertEqual(self.hook_case(migration_error=True),[])
    def test_failed_install_stays_stopped(self):self.assertEqual(self.hook_case(1)[-1],'stop-failed-candidate')
    def test_exception_stays_stopped(self):self.assertEqual(self.hook_case(ValueError('fixture'))[-1],'stop-failed-candidate')
    def test_same_column_is_noop_but_wrong_definition_refused(self):
        good=dict(type='bigint',collation=None,nullable='NO',default=None,extra='')
        m.check_column(good,'bigint',None,'NO')
        for key,value in [('type','int'),('nullable','YES'),('default','0'),('extra','auto_increment')]:
            with self.assertRaises(m.Blocked):m.check_column(dict(good,**{key:value}),'bigint',None,'NO')
    def test_existing_wrong_index_not_recreated(self):
        db=Mock();db.json.return_value=[dict(name='wrong',nonUnique=1,prefix=None,expression=None)]
        with self.assertRaises(m.Blocked):m.ensure_index(db,'chat_dispatch_outbox','idx_chat_outbox_dispatch',True)
        db.query.assert_not_called()
    def test_missing_index_created_then_verified(self):
        db=Mock();expected=m.INDEXES[('chat_dispatch_outbox','idx_chat_outbox_dispatch')]
        db.json.side_effect=[[],[dict(name=n,nonUnique=1,prefix=None,expression=None) for n in expected]]
        m.ensure_index(db,'chat_dispatch_outbox','idx_chat_outbox_dispatch',True);db.query.assert_called_once()
    def test_postcheck_rejects_missing_or_conflicting_backfill(self):
        migration=m.Migration(Mock(),dict(run='34',commit='a'*40),{})
        migration.db=Mock()
        for row in ['14\t1\t0\t0','14\t0\t1\t0','13\t0\t0\t0','14\t0\t0\t1']:
            migration.db.file.return_value=[row]
            with self.assertRaises(m.Blocked):migration.check_counts('fixture',14)
        migration.db.file.return_value=['14\t0\t0\t0'];migration.check_counts('fixture',14)
    def test_pinned_sql_changed_is_rejected_before_execute(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);sql=root/'fixed.sql';sql.write_text('SELECT 1;');os.chmod(str(sql),0o600)
            (root/'candidate-pins.json').write_text(json.dumps({'inputs':[{'file':'fixed.sql','sha256':m.sha(sql)}]}))
            with patch.object(m,'HERE',root):
                self.assertEqual(m.pinned_text('fixed.sql'),'SELECT 1;');sql.write_text('SELECT 2;')
                with self.assertRaises(m.Blocked):m.pinned_text('fixed.sql')
                with self.assertRaises(m.Blocked):m.pinned_text('other.sql')
    def test_backup_mutation_blocks_resume(self):
        with tempfile.TemporaryDirectory() as d:
            migration=m.Migration(Mock(),dict(run='34',commit='a'*40),{});migration.directory=Path(d)
            p=Path(d)/'before.sql';p.write_text('fixture');os.chmod(str(p),0o600)
            migration.journal={'backup':{'before.sql':m.sha(p)}};migration.backup();p.write_text('changed')
            with self.assertRaises(m.Blocked):migration.backup()

if __name__=='__main__':unittest.main(verbosity=2)
