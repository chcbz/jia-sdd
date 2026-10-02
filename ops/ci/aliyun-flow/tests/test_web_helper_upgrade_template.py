"""Static contract for the same-Run web deploy-helper upgrade bootstrap."""
import hashlib
from pathlib import Path
import re
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[4]
TEMPLATE = ROOT / 'ops/ci/aliyun-flow/templates/frontend-develop-release.yaml'
HELPER = ROOT / 'ops/ci/aliyun-flow/host/cyf-web-flow-deploy'
PREDECESSOR = 'c4f446828968ae329e976daeb4014c7be945d6c335b7bb930fbb390632802541'
CANDIDATE = 'be51ee223163e5c424d641639fbd2c9540925f14dcb3f2faaba273b974e90385'


class WebHelperUpgradeTemplateTest(unittest.TestCase):
    def setUp(self):
        self.source = TEMPLATE.read_text()

    def test_ci_artifact_freezes_the_tracked_helper_bytes(self):
        self.assertEqual(hashlib.sha256(HELPER.read_bytes()).hexdigest(), CANDIDATE)
        self.assertIn("const expectedHelperSha='" + CANDIDATE + "'", self.source)
        self.assertIn("const helperPath='installer/cyf-web-flow-deploy'", self.source)
        self.assertIn("installer/helper-release.json", self.source)
        self.assertIn("tree:fs.readFileSync(path.join(root,'source-tree.txt'),'utf8').trim()", self.source)
        self.assertIn("helper_sha256:helperSha", self.source)

    def test_deploy_bootstrap_is_compilable_and_pins_cas_identities(self):
        marker = "<<'CYF_WEB_HELPER_UPGRADE'\n"
        self.assertIn(marker, self.source)
        bootstrap = self.source.split(marker, 1)[1].split("            CYF_WEB_HELPER_UPGRADE\n", 1)[0]
        compile(textwrap.dedent(bootstrap), str(TEMPLATE) + ':helper-upgrade', 'exec')
        self.assertIn(PREDECESSOR, self.source)
        self.assertIn(CANDIDATE, self.source)
        self.assertIn("expected_members = {'installer/cyf-web-flow-deploy', 'installer/helper-release.json'}", bootstrap)
        self.assertIn("helper release manifest does not match this Flow run", bootstrap)
        self.assertIn("fcntl.flock(lock_fd, fcntl.LOCK_EX)", bootstrap)
        self.assertNotIn('LOCK_NB', bootstrap)
        self.assertIn("installed helper changed before compare-and-swap", bootstrap)
        self.assertIn('CYF_WEB_HELPER_UPGRADE=ROLLED_BACK', bootstrap)
        self.assertIn("subprocess.run([str(target), pipeline, run, commit]", bootstrap)
        self.assertIn("/var/lib/cyf-web-flow/downloads/${BUILD_NUMBER}/package.tgz", self.source)
        self.assertRegex(self.source, re.compile(r"artifact: \$\[stages\.cloud_ci\.web_ci\.upload_artifact\.artifacts\.cyf_web_flow_4403172\]"))


if __name__ == '__main__':
    unittest.main()
