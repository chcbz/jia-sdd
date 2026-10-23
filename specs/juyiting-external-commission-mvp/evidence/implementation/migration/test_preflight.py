"""Local tests of read-only gate decisions; no DB connection, builds, or deployment."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('d31_preflight',str(P/'flow-preflight.py'))
gate=importlib.util.module_from_spec(spec);spec.loader.exec_module(gate)
class GateTest(unittest.TestCase):
    def setUp(self):
        self.report=json.loads((P/'flow-preflight-report.json').read_text())['audit']
        self.pins=json.loads((P/'candidate-pins.json').read_text())
    def row(self,name):
        return next(x for x in self.report['observations'] if x['section']==name)
    def test_proven_migration_freeze_passes_even_with_old_manifest_tenant_diagnostic(self):
        self.assertEqual([],gate.reasons_for(self.report,self.pins))
    def test_binding_replacement_or_unproven_subject_blocks(self):
        self.row('migrationBindingFreeze')['proven']-=1
        self.assertIn('UNPROVEN_MIGRATION_BINDING',gate.reasons_for(self.report,self.pins))
    def test_unknown_original_dispatch_blocks(self):
        self.row('chatProof')['provenDispatches']-=1
        self.assertIn('UNPROVEN_CHAT_REFERENCE',gate.reasons_for(self.report,self.pins))
    def test_ambiguous_dispatch_blocks(self):
        self.row('chatProof')['ambiguousDispatches']=1
        self.assertIn('UNPROVEN_CHAT_REFERENCE',gate.reasons_for(self.report,self.pins))
    def test_wrong_server_blocks(self):
        self.row('target')['serverUuidSha256']='different'
        self.assertIn('TARGET_CHANGED',gate.reasons_for(self.report,self.pins))
    def test_partial_schema_cannot_replay_expand(self):
        self.report['observations'].append({'section':'schema'})
        self.assertIn('EXPANSION_ALREADY_STARTED_USE_PHASE_RESUME',gate.reasons_for(self.report,self.pins))
    def test_invalid_audit_not_pass(self):
        self.report['observations']=[]
        with self.assertRaises(ValueError): gate.reasons_for(self.report,self.pins)
if __name__=='__main__': unittest.main()
