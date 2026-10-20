"""Exercise the actual embedded relocation code, using private synthetic homes."""
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import unittest

BASE = pathlib.Path(__file__).resolve().parents[1]
CODE = re.search(r"python3 - <<'PYMAVENCACHE'\n(.*?)\nPYMAVENCACHE", (BASE / 'backend-ci-run.sh').read_text(), re.S)[1]


class MavenCacheTest(unittest.TestCase):
    def setUp(self):
        self.home_tmp = tempfile.TemporaryDirectory()
        self.scratch_tmp = tempfile.TemporaryDirectory(prefix='cyf-backend-flow-ci.', dir='/tmp')
        self.addCleanup(self.home_tmp.cleanup)
        self.addCleanup(self.scratch_tmp.cleanup)
        self.home = pathlib.Path(self.home_tmp.name)
        self.scratch = pathlib.Path(self.scratch_tmp.name)
        self.m2 = self.home / '.m2'
        self.repo = self.m2 / 'repository'
        self.repo.mkdir(parents=True)
        (self.repo / 'artifact.jar').write_bytes(b'synthetic fixture')
        (self.m2 / 'settings.xml').write_text('synthetic secret sentinel')
        self.env = dict(os.environ, HOME=str(self.home), CYF_EXPERIMENT=str(self.scratch),
                        PIPELINE_ID='5260799', BUILD_NUMBER='203')

    def run_code(self):
        return subprocess.run([sys.executable, '-c', CODE], env=self.env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True)

    def state(self):
        return json.loads((self.scratch / 'maven-cache-state.json').read_text())

    def test_moves_repository_only_and_retains_settings_and_bytes(self):
        result = self.run_code()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(self.state()['moved'])
        self.assertFalse(self.repo.exists())
        self.assertEqual((self.scratch / 'maven-platform-repository/artifact.jar').read_bytes(), b'synthetic fixture')
        self.assertEqual((self.m2 / 'settings.xml').read_text(), 'synthetic secret sentinel')
        self.assertNotIn('synthetic secret sentinel', result.stdout)
        self.assertNotIn(str(self.home), result.stdout)

    def test_does_not_follow_repository_symlink(self):
        actual = self.m2 / 'actual'
        self.repo.rename(actual)
        self.repo.symlink_to(actual, target_is_directory=True)
        self.assertEqual(self.run_code().returncode, 0)
        self.assertEqual(self.state()['status'], 'SYMLINK_NOT_FOLLOWED')
        self.assertTrue((actual / 'artifact.jar').is_file())

    def test_does_not_follow_parent_symlink(self):
        actual = self.home / 'actual'
        self.m2.rename(actual)
        self.m2.symlink_to(actual, target_is_directory=True)
        self.assertEqual(self.run_code().returncode, 0)
        self.assertEqual(self.state()['status'], 'SYMLINK_NOT_FOLLOWED')
        self.assertTrue((actual / 'repository/artifact.jar').is_file())

    def test_absent_repository_is_not_created(self):
        self.repo.rename(self.m2 / 'not-repository')
        self.assertEqual(self.run_code().returncode, 0)
        self.assertEqual(self.state()['status'], 'REPOSITORY_ABSENT')
        self.assertFalse(self.repo.exists())

    def test_existing_destination_is_not_overwritten(self):
        (self.scratch / 'maven-platform-repository').mkdir()
        self.assertEqual(self.run_code().returncode, 0)
        self.assertEqual(self.state()['status'], 'DESTINATION_EXISTS')
        self.assertTrue((self.repo / 'artifact.jar').is_file())

    def test_rejects_other_pipeline_without_touching_repository(self):
        self.env['PIPELINE_ID'] = '4403172'
        self.assertNotEqual(self.run_code().returncode, 0)
        self.assertTrue((self.repo / 'artifact.jar').is_file())
        self.assertFalse((self.scratch / 'maven-cache-state.json').exists())


if __name__ == '__main__':
    unittest.main()
