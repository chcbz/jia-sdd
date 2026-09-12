import contextlib
import importlib.machinery
import io
import json
import pathlib
import subprocess
import tempfile
import unittest
from unittest import mock

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / 'ops/ci/aliyun-flow/flow-release-monitor.py'


def load():
    return importlib.machinery.SourceFileLoader('flow_release_monitor', str(SCRIPT)).load_module()


class FlowReleaseMonitorTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='flow-release-monitor-')
        self.path = pathlib.Path(self.tmp.name) / 'state.json'
        self.monitor = load()
        self.target = {
            'task_id': 'FLOW-RELEASE-MONITOR-20260912',
            'pipeline': '5260799',
            'run': '20',
            'expected_commit': 'a' * 40,
        }

    def tearDown(self):
        self.tmp.cleanup()

    def config(self):
        return {'targets': [self.target], 'state': str(self.path)}

    def state(self):
        return json.loads(self.path.read_text())

    def test_success_is_deduplicated_and_receipt_is_not_inbox_claim(self):
        with mock.patch.object(self.monitor, '_flow_status', return_value=('SUCCESS', ['a' * 40])), \
             mock.patch.object(self.monitor, '_send_email', return_value=True) as mail:
            self.assertEqual(0, self.monitor.check(self.config()))
            self.assertEqual(0, self.monitor.check(self.config()))
        mail.assert_called_once()
        self.assertIn('Flow成功，线上版本/业务验收仍需主控核验', mail.call_args[0][1])
        saved = self.state()
        record = next(iter(saved['targets'].values()))['notices']['success_expected_commit']
        self.assertTrue(record['accepted'])
        self.assertEqual('unknown', record['receipt']['inbox_delivery'])

    def test_sha_mismatch_notifies_once_and_requires_controller(self):
        with mock.patch.object(self.monitor, '_flow_status', return_value=('SUCCESS', ['b' * 40])), \
             mock.patch.object(self.monitor, '_send_email', return_value=True) as mail:
            self.assertEqual(0, self.monitor.check(self.config()))
            self.assertEqual(0, self.monitor.check(self.config()))
        mail.assert_called_once()
        subject, body = mail.call_args[0]
        self.assertIn('SHA不匹配', subject)
        self.assertIn('需主控核验', body)
        record = next(iter(self.state()['targets'].values()))['notices']['success_sha_mismatch']
        self.assertTrue(record['accepted'])
        self.assertEqual('unknown', record['receipt']['inbox_delivery'])

    def test_terminal_failure_retries_email_at_most_three_times(self):
        with mock.patch.object(self.monitor, '_flow_status', return_value=('FAIL', [])), \
             mock.patch.object(self.monitor, '_send_email', return_value=False) as mail:
            self.assertEqual(2, self.monitor.check(self.config()))
            self.assertEqual(2, self.monitor.check(self.config()))
            self.assertEqual(2, self.monitor.check(self.config()))
            self.assertEqual(2, self.monitor.check(self.config()))
        self.assertEqual(3, mail.call_count)
        record = next(iter(self.state()['targets'].values()))['notices']['terminal_fail']
        self.assertEqual(3, record['attempts'])
        self.assertFalse(record['accepted'])

    def test_timeout_alerts_only_after_three_consecutive_observation_errors(self):
        with mock.patch.object(self.monitor, '_flow_status', side_effect=self.monitor.ObservationError('flow_timeout')), \
             mock.patch.object(self.monitor, '_send_email', return_value=True) as mail:
            self.assertEqual(0, self.monitor.check(self.config()))
            self.assertEqual(0, self.monitor.check(self.config()))
            self.assertEqual(0, self.monitor.check(self.config()))
            self.assertEqual(0, self.monitor.check(self.config()))
        mail.assert_called_once()
        self.assertIn('flow_timeout', mail.call_args[0][1])

    def test_flow_subprocess_timeout_is_safely_classified(self):
        process = mock.Mock()
        process.communicate.side_effect = [subprocess.TimeoutExpired(['node'], 30), (b'', b'')]
        with mock.patch.object(self.monitor.subprocess, 'Popen', return_value=process):
            with self.assertRaisesRegex(self.monitor.ObservationError, 'flow_timeout'):
                self.monitor._flow_status(self.target)
        process.kill.assert_called_once()

    def test_flow_and_mail_commands_are_bounded_and_do_not_inherit_output(self):
        flow = mock.Mock(returncode=0)
        flow.communicate.return_value = (json.dumps({
            'org': self.monitor.FLOW_ORG, 'pipeline': '5260799', 'run': '20',
            'status': 'RUNNING', 'sources': []}).encode('utf-8'), b'untrusted')
        mail = mock.Mock(returncode=0)
        mail.communicate.return_value = (b'', b'')
        with mock.patch.object(self.monitor.subprocess, 'Popen', side_effect=[flow, mail]) as popen:
            self.assertEqual(('RUNNING', []), self.monitor._flow_status(self.target))
            self.assertTrue(self.monitor._send_email('safe-subject', 'safe-body'))
        self.assertEqual(['node', self.monitor.FLOW_COMMAND, 'status', '--org', self.monitor.FLOW_ORG,
                          '--pipeline', '5260799', '--run', '20', '--credentials-file',
                          self.monitor.CREDENTIALS_FILE], popen.call_args_list[0][0][0])
        self.assertEqual([self.monitor.MAIL_COMMAND, 'safe-subject', 'safe-body'], popen.call_args_list[1][0][0])
        self.assertEqual(self.monitor.FLOW_TIMEOUT_SECONDS, flow.communicate.call_args[1]['timeout'])

    def test_main_does_not_emit_flow_or_error_output(self):
        payload = json.dumps(self.config())
        stdout = io.StringIO()
        stderr = io.StringIO()
        with mock.patch.object(self.monitor, '_flow_status', side_effect=self.monitor.ObservationError('flow_output_invalid')), \
             contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            self.assertEqual(0, self.monitor.main(['--check', '--config', payload]))
        self.assertEqual('', stdout.getvalue())
        self.assertEqual('', stderr.getvalue())

    def test_rejects_unapproved_pipeline_and_org(self):
        config = self.config()
        config['targets'][0]['pipeline'] = '1'
        self.assertEqual(2, self.monitor.main(['--check', '--config', json.dumps(config)]))
        config = self.config()
        config['org'] = 'other'
        self.assertEqual(2, self.monitor.main(['--check', '--config', json.dumps(config)]))


if __name__ == '__main__':
    unittest.main()
