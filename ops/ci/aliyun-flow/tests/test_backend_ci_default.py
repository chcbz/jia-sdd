import base64
import gzip
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import tempfile
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

    def test_timing_summary_survives_truncated_cloud_log_without_raw_environment(self):
        shell = (BASE / 'backend-ci-run.sh').read_text()
        code = shell.split("<<'PYTESTREPORT'\n", 1)[1].split('\nPYTESTREPORT', 1)[0]
        code = code.split('# Bounded, value-free cache inventory.', 1)[0]
        phase = dict(phase='init', rootBuild=True, elapsedSeconds=0.1, jvmUptimeSeconds=3.0,
                     processCpuSeconds=2.0, availableProcessors=3, c1Only=False)
        timing = dict(task=':example:test', rootBuild=True, startedSeconds=1.0, seconds=2.0,
                      skipped=False, skipMessage=None, failed=False)
        with tempfile.TemporaryDirectory() as temporary:
            cwd = pathlib.Path(temporary)
            build = cwd / 'build'
            build.mkdir()
            (build / 'TEST-example.xml').write_text(
                '<testsuite name="example" tests="1" failures="0" errors="0" skipped="0"/>')
            (build / 'gradle-output.log').write_text(
                'UNRELATED_ENV=do-not-copy-this\nCYF_GRADLE_PHASE ' + json.dumps(phase) +
                '\nCYF_TASK_TIMING ' + json.dumps(timing) + '\n')
            env = dict(os.environ, CYF_FLOW_BUILD_ROOT=str(build), PIPELINE_ID='5260799',
                       BUILD_NUMBER='1', CI_COMMIT_SHA='a' * 40)
            subprocess.run(['python3', '-c', code], cwd=str(cwd), env=env, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            summary = json.loads((cwd / '_cyf_api_flow_export/test-results/summary.json').read_text())
            self.assertEqual(summary['gradlePhases'], [phase])
            self.assertEqual(summary['taskTimings'], [timing])
            self.assertEqual(summary['counts']['tests'], 1)
            self.assertNotIn('do-not-copy-this', json.dumps(summary))

    def test_required_profile_and_quality_tasks(self):
        argv = json.loads((BASE / 'backend-ci-policy.json').read_text())['argv']
        for required in ('--parallel', '--max-workers=3', '--build-cache', 'validateLayering', ':starter:bootJar'):
            self.assertIn(required, argv)
        self.assertNotIn('-x', argv)
        self.assertFalse(any(x.startswith('-Dorg.gradle.jvmargs=') for x in argv))
        self.assertEqual(next(x for x in argv if x.startswith(':')),
                         ':agent:jia-agent-mapper:test')
        self.assertEqual(argv.count('./gradlew'), 1)
        shell = (BASE / 'backend-ci-run.sh').read_text()
        self.assertIn("'gradle','--flow-ci'", shell)
        self.assertIn('CYF_FLOW_SHORT_LIVED_TEST_JVM=1', shell)
        self.assertIn('CYF_BUILD_INPUT', shell)
        self.assertIn('CYF_GRADLE_PHASE', shell)
        self.assertIn('startedSeconds:', shell)
        self.assertIn("summary['gradlePhases']", shell)
        self.assertIn("summary['taskTimings']", shell)
        self.assertNotIn('println(cyfRuntime.inputArguments)', shell)
        self.assertNotIn('text=True', shell)  # Flow worker Python 3.6
        self.assertIn('universal_newlines=True', shell)
        self.assertNotIn('local-release-metadata', shell)
        template = (BASE / 'templates/backend-develop-release.yaml').read_text()
        self.assertIn('step: JavaBuild', template)
        self.assertIn('jdkVersion: "1.8"', template)
        self.assertIn('prepare-backend-jdk.py', shell)
        self.assertLess(shell.index('export JAVA_HOME='), shell.index("'gradle','--flow-ci'"))
        self.assertIn('CYF_CACHE_INVENTORY', shell)
        self.assertIn("summary['cacheInventory']=result", shell)
        self.assertNotIn("dest/'cache-inventory.json'", shell)  # installer admits summary/XML only
        subprocess.run(['bash', '-n', str(BASE / 'backend-ci-run.sh')], check=True)


if __name__ == '__main__':
    unittest.main()
