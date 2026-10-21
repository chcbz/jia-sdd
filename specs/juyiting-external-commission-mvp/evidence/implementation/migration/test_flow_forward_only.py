#!/usr/bin/env python3
"""Reuse existing numeric-Flow fixture against installed helpers, only /tmp fake lifecycle.
Synthetic receipts are unit inputs, NOT a real Flow candidate approval or deployment evidence.
"""
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
ROOT=Path('/home/isp/wsps/cyf')
def load(name,path):
    loader=importlib.machinery.SourceFileLoader(name,str(path))
    spec=importlib.util.spec_from_loader(name,loader)
    module=importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module
fixture=load('d31_existing_gate_fixture',ROOT/'ops/ci/aliyun-flow/tests/test_api_gate_policy.py')
adapter=load('d31_installed_adapter',Path('/usr/local/sbin/cyf-api-flow-deploy'))

class FlowForwardOnlyTest(fixture.ApiGatePolicyTest):
    def setUp(self):
        super().setUp()
        pins=json.loads((HERE/'candidate-pins.json').read_text())
        for name in ('/usr/local/sbin/cyf-api-flow-deploy','/usr/local/sbin/cyf-api-flow-install'):
            self.assertEqual(pins['installedHelpers'][name],hashlib.sha256(Path(name).read_bytes()).hexdigest())
        # Never inherit real stopped-maintenance/local authority or a caller fault into fixture.
        for key in list(self.env):
            if key.startswith('CYF_API_LOCAL_') or key in ('CYF_API_FLOW_FORWARD_ONLY','CYF_API_FLOW_TEST_FAULT'):
                del self.env[key]
        approval=json.loads((self.root/'state/approval.json').read_text())
        self.assertEqual(approval['schema_version'],2)
        self.assertEqual(approval['run_id'],'34')
        self.assertNotIn('release',approval) # no LOCAL binding/receipt
    def install(self):
        with patch.dict(os.environ,self.env,clear=True):
            env=adapter.installer_environment()
        self.assertEqual(env.get('CYF_API_FLOW_FORWARD_ONLY'),self.env.get('CYF_API_FLOW_FORWARD_ONLY'))
        return subprocess.run(['/usr/local/sbin/cyf-api-flow-install'],env=env,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True,timeout=15)
    def test_adapter_keeps_forward_only_and_removes_schema_passwords(self):
        with patch.dict(os.environ,{'CYF_API_FLOW_FORWARD_ONLY':'1',
                adapter.SCHEMA_PASSWORD_ENV:'synthetic',adapter.E05_SCHEMA_PASSWORD_ENV:'synthetic'},clear=True):
            env=adapter.installer_environment()
        self.assertEqual(env['CYF_API_FLOW_FORWARD_ONLY'],'1')
        self.assertNotIn(adapter.SCHEMA_PASSWORD_ENV,env)
        self.assertNotIn(adapter.E05_SCHEMA_PASSWORD_ENV,env)
    def test_flow_failed_record_retains_exact_numeric_candidate_binding(self):
        lifecycle=self.root/'bin/cyf-api-kit'
        lifecycle.write_text(lifecycle.read_text().replace('start) rm -f "$root/stopped" ;;','start) exit 1 ;;'))
        self.env['CYF_API_FLOW_FORWARD_ONLY']='1'
        result=self.install()
        self.assertNotEqual(result.returncode,0)
        record=json.loads((self.root/'state/record.json').read_text())
        approval=json.loads((self.root/'state/approval.json').read_text())
        self.assertEqual(record['recovery'],'forward_only_candidate_retained')
        self.assertEqual(record['run_id'],approval['run_id'])
        self.assertEqual(record['source_commit_sha'],approval['source_commit_sha'])
        self.assertEqual(record['receipt_sha256'],approval['receipt_sha256'])
        self.assertEqual(record['candidate_sha256'],approval['jar_sha256'])
        self.assertNotIn('release',record)
        self.assertEqual((self.root/'calls').read_text().splitlines(),['stop','status','start'])

if __name__=='__main__':
    names=[
      'test_adapter_keeps_forward_only_and_removes_schema_passwords',
      'test_flow_failed_record_retains_exact_numeric_candidate_binding',
      'test_preservation_forward_only_failure_retains_candidate_and_exact_retry_finalizes',
      'test_preservation_forward_only_foreign_receipt_cannot_resume_or_restore',
      'test_wrong_source_approval_is_rejected',
      'test_tampered_artifact_is_rejected',
    ]
    result=unittest.TextTestRunner(verbosity=2).run(unittest.TestSuite(FlowForwardOnlyTest(n) for n in names))
    raise SystemExit(0 if result.wasSuccessful() else 1)
