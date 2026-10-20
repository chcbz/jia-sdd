import base64
import gzip
import hashlib
import importlib.util
import json
import pathlib
import re
import subprocess
import unittest

BASE = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('prepare_ci', BASE / 'prepare-backend-ci.py')
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


class DefaultCiTest(unittest.TestCase):
    def test_renderer_is_deterministic_and_template_is_current(self):
        template = (BASE / 'templates/backend-develop-release.yaml').read_text()
        shell = (BASE / 'backend-ci-run.sh').read_text()
        self.assertEqual(m.render(template, shell), m.render(template, shell))
        self.assertEqual(m.render(template, shell), template)

    def test_bundle_has_no_human_task_snapshot_or_source_pin(self):
        template = (BASE / 'templates/backend-develop-release.yaml').read_text()
        raw = base64.b64decode(re.search(r"raw=base64.b64decode\('([^']+)'", template)[1])
        self.assertIn(hashlib.sha256(raw).hexdigest(), template)
        files = json.loads(gzip.decompress(raw))
        self.assertNotIn('docs/implementation/TASKS.yaml', files)
        for name, path in m.TOOL_FILES.items():
            self.assertEqual(files[name], path.read_text())
        self.assertNotIn('9ca2776c27ce3270efa0ea4c366b7de0e68e8dbb', template)
        self.assertNotIn('BACKEND-FLOW-5M-20261016', template)

    def test_preserved_trigger_and_no_deploy(self):
        template = (BASE / 'templates/backend-develop-release.yaml').read_text()
        self.assertIn('triggerEvents:\n      - push', template)
        self.assertIn('branchesFilter: ^(develop|codex/v1-6-voice-api-readiness-20260917|codex/mmd-unified-materials-api-20261003)$', template)
        self.assertNotIn('VMDeploy', template)
        self.assertNotIn('\n  deploy:', template)

    def test_required_profile_and_quality_tasks(self):
        argv = json.loads((BASE / 'backend-ci-policy.json').read_text())['argv']
        for required in ('--parallel', '--max-workers=3', '--build-cache', 'validateLayering', ':starter:bootJar'):
            self.assertIn(required, argv)
        self.assertNotIn('-x', argv)
        self.assertEqual(argv.count('./gradlew'), 1)
        shell = (BASE / 'backend-ci-run.sh').read_text()
        self.assertIn("'gradle','--flow-ci'", shell)
        self.assertIn('CYF_FLOW_SHORT_LIVED_TEST_JVM=1', shell)
        self.assertIn('CYF_BUILD_INPUT', shell)
        self.assertNotIn('local-release-metadata', shell)
        subprocess.run(['bash', '-n', str(BASE / 'backend-ci-run.sh')], check=True)


if __name__ == '__main__':
    unittest.main()
