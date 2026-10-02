"""Offline packaging contract for the frozen same-Run web-helper artifact."""
import base64
import hashlib
import json
from pathlib import Path
import re
import subprocess
import tempfile
import os
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[4]
TEMPLATE = ROOT / 'ops/ci/aliyun-flow/templates/frontend-develop-release.yaml'
HELPER = ROOT / 'ops/ci/aliyun-flow/host/cyf-web-flow-deploy'
UPGRADER = ROOT / 'ops/ci/aliyun-flow/auto/web_helper_upgrade.py'
PREDECESSOR = 'c4f446828968ae329e976daeb4014c7be945d6c335b7bb930fbb390632802541'
CANDIDATE = 'be51ee223163e5c424d641639fbd2c9540925f14dcb3f2faaba273b974e90385'


def frozen_buffer(source, name):
    matched = re.search(r"const " + name + r"=Buffer\.from\('([^']+)'\,'base64'\);", source)
    if matched is None:
        raise AssertionError('missing frozen ' + name)
    return base64.b64decode(matched.group(1), validate=True)


class WebHelperUpgradeTemplateTest(unittest.TestCase):
    def setUp(self):
        self.source = TEMPLATE.read_text()

    def node_manifest(self):
        marker = "                node <<'CYF_MANIFEST'\n"
        return self.source.split(marker, 1)[1].split('                CYF_MANIFEST\n', 1)[0]

    def test_frozen_payloads_match_tracked_sources_without_web_checkout_lookup(self):
        helper = frozen_buffer(self.source, 'helper')
        upgrader = frozen_buffer(self.source, 'upgradeScript')
        self.assertEqual(helper, HELPER.read_bytes())
        self.assertEqual(upgrader, UPGRADER.read_bytes())
        self.assertEqual(hashlib.sha256(helper).hexdigest(), CANDIDATE)
        self.assertEqual(hashlib.sha256(upgrader).hexdigest(),
                         '4b2278413644ca9c8761715b74e3ccfe174462d6f6a7c6551fa5f4b8a75ed0d2')
        self.assertNotIn("helperSource='ops/ci/", self.node_manifest())
        self.assertIn("const expectedHelperSha='" + CANDIDATE + "'", self.source)
        self.assertIn("installer/helper-release.json", self.source)

    def test_web_like_checkout_packages_frozen_helper_without_sdd_source_path(self):
        source = self.node_manifest()
        with tempfile.TemporaryDirectory(prefix='cyf-web-like-checkout-') as temp:
            checkout = Path(temp)
            export = checkout / '_cyf_web_develop_ci_export'
            (export / 'dist').mkdir(parents=True)
            (export / 'dist/index.html').write_bytes(b'<html>fixture</html>')
            commit = 'a' * 40
            tree = 'b' * 40
            (checkout / 'package.json').write_text(json.dumps({'version': '1.0.1'}) + '\n')
            (export / 'source-commit.txt').write_text(commit + '\n')
            (export / 'source-tree.txt').write_text(tree + '\n')
            self.assertFalse((checkout / 'ops/ci/aliyun-flow/host/cyf-web-flow-deploy').exists())
            env = dict(os.environ, PIPELINE_ID='4403172', BUILD_NUMBER='92',
                       CI_COMMIT_REF_NAME='develop', CI_COMMIT_SHA=commit)
            result = subprocess.run(['node', '-e', source], cwd=str(checkout), env=env,
                                    universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.assertEqual(result.returncode, 0, result.stderr)
            helper = export / 'installer/cyf-web-flow-deploy'
            release = json.loads((export / 'installer/helper-release.json').read_text())
            self.assertEqual(hashlib.sha256(helper.read_bytes()).hexdigest(), CANDIDATE)
            self.assertEqual(release['tree'], tree)
            self.assertEqual(release['commit'], commit)
            self.assertEqual(json.loads((export / 'release.json').read_text())['package_version'], '1.0.1')
            self.assertEqual(release['helper']['sha256'], CANDIDATE)

    def test_bootstrap_is_compilable_and_uses_same_run_artifact(self):
        marker = "<<'CYF_WEB_HELPER_UPGRADE_BOOTSTRAP'\n"
        bootstrap = self.source.split(marker, 1)[1].split(
            '            CYF_WEB_HELPER_UPGRADE_BOOTSTRAP\n', 1)[0]
        compile(textwrap.dedent(bootstrap), str(TEMPLATE) + ':helper-upgrade', 'exec')
        self.assertIn(PREDECESSOR, self.source)
        self.assertIn(CANDIDATE, self.source)
        self.assertIn("/var/lib/cyf-web-flow/downloads/${BUILD_NUMBER}/package.tgz", self.source)
        self.assertIn('frozen bootstrap digest mismatch', bootstrap)
        self.assertIn("artifact: $[stages.cloud_ci.web_ci.upload_artifact.artifacts.cyf_web_flow_4403172]",
                      self.source)


if __name__ == '__main__':
    unittest.main()
