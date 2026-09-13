"""Offline F06 deploy integration tests; never touch production helpers or MySQL."""
import fcntl
import grp
import importlib.machinery
import json
import os
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[4]
DEPLOY = ROOT / 'ops/ci/aliyun-flow/host/cyf-api-flow-deploy'
loader = importlib.machinery.SourceFileLoader('cyf_api_flow_deploy_f06_test', str(DEPLOY))
deploy = loader.load_module()


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


class ApiFlowDeployF06Test(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='cyf-api-flow-deploy-f06-', dir='/tmp')
        self.base = Path(self.tmp.name)
        self.base.chmod(0o700)
        self.state = self.base / 'state'
        self.state.mkdir(mode=0o700)
        self.release_lock = self.base / 'cyf-release-api.lock'
        self.release_lock.touch(mode=0o660)
        os.chown(self.release_lock, 0, grp.getgrnam('isp').gr_gid)
        self.release_lock.chmod(0o660)
        self.runner = self.base / 'cyf-api-additive-schema'
        self.calls = self.base / 'runner-calls'
        self.observed = self.base / 'runner-observed.json'
        self.context = {
            'pipeline_id': '5260799',
            'run_id': '40',
            'source_commit_sha': 'a' * 40,
            'source_tree_sha': 'b' * 40,
            'receipt_sha256': 'c' * 64,
            'jar_sha256': 'd' * 64,
        }
        self.previous = {
            'ROOT': deploy.ROOT,
            'SCHEMA_RESULTS': deploy.SCHEMA_RESULTS,
            'RELEASE_LOCK': deploy.RELEASE_LOCK,
            'SCHEMA_RUNNER': deploy.SCHEMA_RUNNER,
            '_SCHEMA_CONTEXT': deploy._SCHEMA_CONTEXT,
        }
        deploy.ROOT = self.state
        deploy.SCHEMA_RESULTS = self.state / 'schema-results'
        deploy.RELEASE_LOCK = self.release_lock
        deploy.SCHEMA_RUNNER = self.runner
        deploy._SCHEMA_CONTEXT = self.context
        self.old_password = os.environ.get(deploy.SCHEMA_PASSWORD_ENV)
        self.old_attacker = os.environ.get('CYF_F06_SCHEMA_OFFLINE_TEST')
        os.environ[deploy.SCHEMA_PASSWORD_ENV] = 'offline-secret-never-persist'
        os.environ['CYF_F06_SCHEMA_OFFLINE_TEST'] = 'YES'
        self.write_record()
        self.write_runner(self.report('pass'), 0)

    def tearDown(self):
        for name, value in self.previous.items():
            setattr(deploy, name, value)
        if self.old_password is None:
            os.environ.pop(deploy.SCHEMA_PASSWORD_ENV, None)
        else:
            os.environ[deploy.SCHEMA_PASSWORD_ENV] = self.old_password
        if self.old_attacker is None:
            os.environ.pop('CYF_F06_SCHEMA_OFFLINE_TEST', None)
        else:
            os.environ['CYF_F06_SCHEMA_OFFLINE_TEST'] = self.old_attacker
        self.tmp.cleanup()

    def report(self, status, error=None, partial=False):
        tables = {
            'agent_task_artifact_outcome': {'status': 'created_equivalent'},
            'agent_task_artifact_outcome_decision': {'status': 'created_equivalent'},
        }
        value = {
            'schema_version': 1,
            'operation': 'apply',
            'status': status,
            'transaction_model': 'mysql_ddl_autocommit_per_create_no_rollback_or_drop',
            'lock_order': ['f06_runner_file_lock', 'f06_mysql_named_lock'],
            'tables': tables,
        }
        if partial:
            tables['agent_task_artifact_outcome_decision'] = {
                'status': 'create_backend_error_absent'}
            value['failed_table'] = 'agent_task_artifact_outcome_decision'
        if error is not None:
            value['error'] = error
        return value

    def write_record(self, **changes):
        value = {
            'schema_version': 2,
            'status': 'installed',
            'phase': 'installed',
            'recovery': 'not_required',
            'ticket_sha256': 'e' * 64,
            'source_commit_sha': self.context['source_commit_sha'],
            'source_tree_sha': self.context['source_tree_sha'],
            'run_id': self.context['run_id'],
            'receipt_sha256': self.context['receipt_sha256'],
            'candidate_sha256': self.context['jar_sha256'],
            'previous_sha256': 'f' * 64,
            'backup': str(self.state / 'backups/fixture.jar'),
            'candidate_stop_rc': 0,
            'timestamp': '20260913T000000Z',
        }
        value.update(changes)
        path = self.state / 'record.json'
        path.write_bytes(encoded(value))
        path.chmod(0o600)

    def write_runner(self, report, return_code, stderr=''):
        script = '''#!/usr/bin/python3
import fcntl, json, os
from pathlib import Path
lock = Path(%r)
calls = Path(%r)
observed = Path(%r)
count = int(calls.read_text()) + 1 if calls.exists() else 1
calls.write_text(str(count))
with lock.open('r+') as stream:
    try:
        fcntl.flock(stream.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        release_lock_held = True
    else:
        release_lock_held = False
observed.write_text(json.dumps({
    'argv': __import__('sys').argv[1:],
    'env_keys': sorted(os.environ),
    'release_lock_held': release_lock_held,
}, sort_keys=True))
print(%r)
if %r:
    print(%r, file=__import__('sys').stderr)
raise SystemExit(%d)
''' % (str(self.release_lock), str(self.calls), str(self.observed),
       json.dumps(report, sort_keys=True, separators=(',', ':')), bool(stderr), stderr,
       return_code)
        self.runner.write_text(script)
        self.runner.chmod(0o755)

    def result(self):
        return json.loads((deploy.SCHEMA_RESULTS / 'run-40.json').read_text())

    def test_success_runs_once_under_release_lock_and_does_not_claim_feature_activation(self):
        self.assertEqual(deploy.apply_schema_after_install(self.context), 0)
        result = self.result()
        self.assertEqual(result['status'], 'pass')
        self.assertEqual(result['activation_claim'], 'schema_only_not_feature_activation')
        self.assertEqual(result['sql_sha256'], deploy.SCHEMA_SQL_SHA256)
        self.assertEqual(self.calls.read_text(), '1')
        observed = json.loads(self.observed.read_text())
        self.assertTrue(observed['release_lock_held'])
        self.assertEqual(observed['argv'], ['--apply'])
        self.assertEqual(
            observed['env_keys'], ['CYF_F06_MYSQL_PASSWORD', 'LC_ALL', 'PATH'])
        evidence = ''.join(path.read_text(errors='replace')
                           for path in deploy.SCHEMA_RESULTS.iterdir())
        self.assertNotIn('offline-secret-never-persist', evidence)
        for path in deploy.SCHEMA_RESULTS.iterdir():
            self.assertEqual(path.stat().st_mode & 0o777, 0o600)

    def test_same_run_pass_is_reused_without_rerunning_runner(self):
        self.assertEqual(deploy.apply_schema_after_install(self.context), 0)
        self.assertEqual(deploy.apply_schema_after_install(self.context), 0)
        self.assertEqual(self.calls.read_text(), '1')

    def test_partial_ddl_failure_is_preserved_and_same_run_is_not_retried(self):
        self.write_runner(self.report('failed', 'create_statement_failed', partial=True), 1,
                          stderr='fixture backend error')
        self.assertEqual(deploy.apply_schema_after_install(self.context), 1)
        first = self.result()
        self.assertEqual(first['error'], 'create_statement_failed')
        self.assertEqual(first['runner_report']['failed_table'],
                         'agent_task_artifact_outcome_decision')
        self.assertEqual(first['runner_report']['tables']['agent_task_artifact_outcome']['status'],
                         'created_equivalent')
        self.assertEqual(deploy.apply_schema_after_install(self.context), 1)
        self.assertEqual(self.calls.read_text(), '1')
        self.assertEqual(self.result(), first)
        self.assertEqual((deploy.SCHEMA_RESULTS / 'run-40.stderr').read_text().strip(),
                         'fixture backend error')

    def test_interrupted_running_state_requires_manual_recovery_without_rerun(self):
        deploy.ensure_private_directory(deploy.SCHEMA_RESULTS)
        running = deploy.schema_state(
            self.context, 'running', '2026-09-13T00:00:00.000000Z',
            action='inspect durable metadata; do not rerun')
        deploy.write_schema_state(deploy.schema_paths('40')['state'], running, create=True)
        self.assertEqual(deploy.apply_schema_after_install(self.context), 1)
        self.assertFalse(self.calls.exists())
        self.assertEqual(self.result()['status'], 'running')

    def test_installer_failure_is_returned_without_schema_attempt_or_password_leak(self):
        installer = self.base / 'failed-installer'
        installer_observed = self.base / 'installer-observed'
        installer.write_text(
            '#!/usr/bin/python3\nimport os\nfrom pathlib import Path\n'
            + 'Path(%r).write_text(str(%r in os.environ))\nraise SystemExit(7)\n'
            % (str(installer_observed), deploy.SCHEMA_PASSWORD_ENV))
        installer.chmod(0o755)
        self.assertEqual(deploy.invoke_installer(str(installer)), 7)
        self.assertEqual(installer_observed.read_text(), 'False')
        self.assertFalse(deploy.SCHEMA_RESULTS.exists())
        self.assertFalse(self.calls.exists())

    def test_already_installed_recovery_path_still_invokes_schema(self):
        installer = self.base / 'already-installed'
        installer.write_text('#!/bin/sh\necho CYF_API_FLOW_INSTALL=PASS_ALREADY_INSTALLED\nexit 0\n')
        installer.chmod(0o755)
        self.assertEqual(deploy.invoke_installer(str(installer)), 0)
        self.assertEqual(self.calls.read_text(), '1')
        self.assertEqual(self.result()['status'], 'pass')

    def test_wrong_installed_record_fails_before_runner_and_is_durable(self):
        self.write_record(run_id='41')
        self.assertEqual(deploy.apply_schema_after_install(self.context), 1)
        self.assertFalse(self.calls.exists())
        result = self.result()
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['error'], 'same_run_installed_record_mismatch')

    def test_missing_runner_and_db_principal_are_both_actionable(self):
        self.runner.unlink()
        os.environ.pop(deploy.SCHEMA_PASSWORD_ENV)
        self.assertEqual(deploy.apply_schema_after_install(self.context), 1)
        result = self.result()
        self.assertEqual(result['status'], 'blocked_precondition')
        self.assertEqual(result['error'], 'schema_activation_prerequisites_missing')
        self.assertEqual(result['prerequisites'], [
            'schema_runner_not_installed',
            'db_principal_or_protected_password_not_configured',
        ])
        self.assertIn('cyf_f06_schema_runner', result['action'])
        self.assertIn('new Flow run', result['action'])

    def test_malformed_runner_output_is_preserved_and_not_treated_as_success(self):
        self.write_runner('not-a-runner-report', 0)
        self.assertEqual(deploy.apply_schema_after_install(self.context), 1)
        result = self.result()
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['error'], 'schema_runner_report_contract_mismatch')
        self.assertIsNone(result['runner_report'])
        self.assertTrue((deploy.SCHEMA_RESULTS / 'run-40.stdout').is_file())
        self.assertEqual(deploy.apply_schema_after_install(self.context), 1)
        self.assertEqual(self.calls.read_text(), '1')

    def test_runner_cannot_report_pass_with_an_unverified_table(self):
        report = self.report('pass')
        report['tables']['agent_task_artifact_outcome_decision']['status'] = 'not_attempted'
        self.write_runner(report, 0)
        self.assertEqual(deploy.apply_schema_after_install(self.context), 1)
        result = self.result()
        self.assertEqual(result['status'], 'failed')
        self.assertEqual(result['error'], 'schema_runner_false_success')
        self.assertEqual(self.calls.read_text(), '1')

    def test_runner_native_failure_code_and_report_are_retained(self):
        self.write_runner(self.report('failed', 'mysql_session_ended'), 9,
                          stderr='access denied fixture')
        self.assertEqual(deploy.apply_schema_after_install(self.context), 9)
        result = self.result()
        self.assertEqual(result['runner_exit_code'], 9)
        self.assertEqual(result['error'], 'mysql_session_ended')
        self.assertEqual(result['runner_report']['error'], 'mysql_session_ended')
        self.assertNotEqual(result['stderr_sha256'], '0' * 64)


if __name__ == '__main__':
    unittest.main()
