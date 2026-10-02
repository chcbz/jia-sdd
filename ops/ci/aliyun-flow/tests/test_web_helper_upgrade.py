"""Temporary-fixture behavior tests for the same-Run helper CAS/rollback bootstrap."""
import hashlib
import importlib.machinery
import io
import json
import os
from pathlib import Path
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[4]
MODULE = ROOT / 'ops/ci/aliyun-flow/auto/web_helper_upgrade.py'
COMMIT = 'a' * 40
TREE = 'b' * 40


def load(label):
    return importlib.machinery.SourceFileLoader('web_helper_upgrade_' + label, str(MODULE)).load_module()


class Result:
    def __init__(self, returncode):
        self.returncode = returncode


class WebHelperUpgradeTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='cyf-web-helper-upgrade-')
        self.base = Path(self.tmp.name)
        self.root = self.base / 'state'
        self.target_parent = self.base / 'sbin'
        self.root.mkdir(mode=0o700)
        self.target_parent.mkdir(mode=0o755)
        self.target = self.target_parent / 'cyf-web-flow-deploy'
        self.old = b'old helper bytes'
        self.candidate = b'candidate helper bytes'
        self.target.write_bytes(self.old)
        self.target.chmod(0o755)
        self.old_sha = hashlib.sha256(self.old).hexdigest()
        self.candidate_sha = hashlib.sha256(self.candidate).hexdigest()

    def tearDown(self):
        self.tmp.cleanup()

    def package(self, tree=TREE):
        package = self.root / 'downloads/92/package.tgz'
        package.parent.mkdir(parents=True, mode=0o700)
        helper_release = dict(
            schema_version=1, pipeline_id='4403172', run_id='92', branch='develop', commit=COMMIT,
            tree=TREE, helper=dict(path='installer/cyf-web-flow-deploy', size=len(self.candidate),
                                   sha256=self.candidate_sha, mode='0700'))
        entries = [
            ('installer/cyf-web-flow-deploy', self.candidate),
            ('installer/helper-release.json', json.dumps(helper_release).encode()),
            ('source-tree.txt', (tree + '\n').encode()),
        ]
        with tarfile.open(str(package), 'w:gz') as archive:
            for name, value in entries:
                member = tarfile.TarInfo(name)
                member.size = len(value)
                archive.addfile(member, io.BytesIO(value))
        package.chmod(0o600)
        return package

    def call(self, label, package, runner, events):
        helper = load(label)
        return helper.upgrade_and_run('4403172', '92', COMMIT, package, self.target,
                                      self.old_sha, self.candidate_sha, self.root,
                                      runner=runner, reporter=events.append)

    def test_cas_installs_candidate_and_preserves_old_root_only_rollback(self):
        package = self.package()
        calls, events = [], []

        def runner(args, check=False):
            calls.append((args, check, self.target.read_bytes()))
            return Result(0)

        self.assertEqual(self.call('success', package, runner, events), 0)
        self.assertEqual(self.target.read_bytes(), self.candidate)
        self.assertEqual(calls, [([str(self.target), '4403172', '92', COMMIT], False, self.candidate)])
        backups = list((self.root / 'helper-rollbacks').iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual(backups[0].read_bytes(), self.old)
        self.assertEqual(oct(backups[0].stat().st_mode & 0o777), '0o600')
        self.assertTrue(any('CYF_WEB_HELPER_UPGRADE=INSTALLED' in value for value in events))

    def test_nonzero_candidate_restores_predecessor(self):
        package = self.package()
        events = []
        self.assertEqual(self.call('rollback', package, lambda args, check=False: Result(7), events), 7)
        self.assertEqual(self.target.read_bytes(), self.old)
        self.assertTrue(any('CYF_WEB_HELPER_UPGRADE=ROLLED_BACK' in value for value in events))

    def test_tree_binding_mismatch_fails_before_cas_or_runner(self):
        package = self.package(tree='c' * 40)
        calls, events = [], []
        with self.assertRaisesRegex(SystemExit, 'does not match this Flow run'):
            self.call('tree-mismatch', package,
                      lambda args, check=False: calls.append(args) or Result(0), events)
        self.assertEqual(calls, [])
        self.assertEqual(self.target.read_bytes(), self.old)
        self.assertFalse((self.root / 'helper-rollbacks').exists())


if __name__ == '__main__':
    unittest.main()
