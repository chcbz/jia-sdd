import os
import pathlib
import subprocess
import tempfile
import unittest

SOURCE = pathlib.Path(os.environ.get('CYF_FORWARD_INSTALLER_TEST_SOURCE',
    str(pathlib.Path(__file__).resolve().parents[1] / 'host/cyf-api-flow-install')))

class ForwardOnlyReleaseTest(unittest.TestCase):
    def run_phase(self, flag, phase='candidate_start_failed', record_fails=False):
        source = SOURCE.read_text()
        start = source.index('restore_and_start() {')
        end = source.index('\n}', start) + 2
        function = source[start:end]
        with tempfile.TemporaryDirectory(prefix='cyf-forward-test-') as d:
            root = pathlib.Path(d); calls = root/'calls'; jar = root/'candidate.jar'
            jar.write_bytes(b'new candidate bytes must be preserved')
            lifecycle = root/'lifecycle'
            lifecycle.write_text('#!/bin/bash\nprintf "lifecycle:%s\\n" "$*" >> "$CALLS"\n')
            lifecycle.chmod(0o700)
            script = '''set -eu
STOP_RC=0
write_record() { printf 'record:%s\\n' "$*" >> "$CALLS"; RETURN_RECORD; }
stop_and_verify() { echo stop >> "$CALLS"; }
detach_candidate() { echo detach >> "$CALLS"; }
assert_old_or_absent() { :; }
restore_backup() { echo restore_old >> "$CALLS"; }
lifecycle_healthy() { :; }
fail() { echo fail >> "$CALLS"; exit 23; }
recoverable_fail() { echo record_failure >> "$CALLS"; exit 24; }
'''.replace('RETURN_RECORD', 'return 1' if record_fails else 'return 0')
            script += function + '\nrestore_and_start "$PHASE"\n'
            env = dict(os.environ, CALLS=str(calls), LIFECYCLE=str(lifecycle),
                CYF_API_FLOW_FORWARD_ONLY=flag, PHASE=phase)
            r = subprocess.run(['bash','-c',script], env=env, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, universal_newlines=True)
            return r.returncode, calls.read_text().splitlines(), jar.read_bytes()

    def test_forward_only_blocks_stop_detach_backup_restore_and_old_start(self):
        for phase in ['candidate_start_failed', 'candidate_status_failed',
                      'activating_candidate_recovery', 'failed_rollback_recovery']:
            with self.subTest(phase=phase):
                code, calls, jar = self.run_phase('1', phase)
                self.assertEqual(code, 23)
                self.assertEqual(calls, ['record:failed '+phase+' forward_only_candidate_retained 0','fail'])
                self.assertEqual(jar, b'new candidate bytes must be preserved')

    def test_default_preserves_existing_rollback_for_other_releases(self):
        code, calls, _ = self.run_phase('0')
        self.assertEqual(code, 1)
        self.assertIn('stop', calls); self.assertIn('detach', calls)
        self.assertIn('restore_old', calls); self.assertIn('lifecycle:start', calls)
        self.assertIn('record:failed candidate_start_failed restored_healthy 0', calls)

    def test_durable_failure_write_error_never_falls_through_to_old_jar(self):
        code, calls, jar = self.run_phase('1', record_fails=True)
        self.assertEqual(code, 24)
        self.assertEqual(calls[-1], 'record_failure')
        self.assertNotIn('restore_old', calls)
        self.assertEqual(jar, b'new candidate bytes must be preserved')

if __name__ == '__main__':
    unittest.main()
