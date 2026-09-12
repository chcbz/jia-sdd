import os
from pathlib import Path
import subprocess
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[4]
INSTALLER = ROOT / 'ops/ci/aliyun-flow/host/cyf-api-flow-install'


class ApiFlowInstallLockTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(
            prefix='cyf-api-flow-install-lock-', dir='/tmp')
        self.root = Path(self.tmp.name)
        self.root.chmod(0o700)
        (self.root / 'state/incoming').mkdir(parents=True, mode=0o700)
        (self.root / 'service').mkdir(mode=0o700)
        (self.root / 'bin').mkdir(mode=0o700)
        lifecycle = self.root / 'bin/cyf-api-kit'
        lifecycle.write_text('#!/bin/sh\nexit 0\n')
        lifecycle.chmod(0o700)
        self.lock = self.root / 'cyf-release-api.lock'
        self.lock.write_bytes(b'')
        self.lock.chmod(0o600)
        self.package = self.root / 'state/incoming/package.tgz'
        self.package.write_bytes(b'not inspected before the lock')
        self.package.chmod(0o644)
        self.env = dict(os.environ)
        self.env.update(
            CYF_RELEASE_OFFLINE_TEST='YES',
            CYF_API_FLOW_INSTALL_TEST_ROOT=str(self.root),
        )

    def tearDown(self):
        self.tmp.cleanup()

    def run_installer(self):
        started = time.monotonic()
        result = subprocess.run(
            [str(INSTALLER)],
            env=self.env,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        return result, time.monotonic() - started

    def hold_lock(self, seconds):
        marker = self.root / 'holder-ready'
        holder = subprocess.Popen([
            'flock', '-x', str(self.lock), 'sh', '-c',
            'printf held > "$1"; sleep "$2"',
            'lock-holder', str(marker), str(seconds),
        ])
        deadline = time.monotonic() + 5
        while not marker.exists() and holder.poll() is None and time.monotonic() < deadline:
            time.sleep(0.01)
        self.assertTrue(marker.exists(), 'temporary holder did not acquire fixture lock')
        self.assertIsNone(holder.poll(), 'temporary holder exited before installer started')
        return holder

    def assert_reached_first_post_lock_action(self, result):
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('approval is missing or unsafe', result.stderr)
        self.assertNotIn('another API release is active', result.stderr)
        self.assertEqual(self.package.stat().st_mode & 0o777, 0o600)

    def test_immediate_acquisition_reaches_post_lock_action(self):
        result, elapsed = self.run_installer()

        self.assert_reached_first_post_lock_action(result)
        self.assertLess(elapsed, 5)

    def test_short_holder_release_allows_bounded_waiter_to_acquire(self):
        holder = self.hold_lock(0.5)
        result, elapsed = self.run_installer()
        holder.wait(timeout=5)

        self.assert_reached_first_post_lock_action(result)
        self.assertGreaterEqual(elapsed, 0.2)
        self.assertLess(elapsed, 5)

    def test_sustained_holder_times_out_without_post_lock_action(self):
        holder = self.hold_lock(64)
        original = self.package.read_bytes()
        result, elapsed = self.run_installer()
        holder.wait(timeout=10)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn('another API release is active', result.stderr)
        self.assertNotIn('approval is missing or unsafe', result.stderr)
        self.assertGreaterEqual(elapsed, 59)
        self.assertLess(elapsed, 64)
        self.assertEqual(self.package.read_bytes(), original)
        self.assertEqual(self.package.stat().st_mode & 0o777, 0o644)
        self.assertFalse((self.root / 'state/record.json').exists())
        self.assertEqual(list((self.root / 'state/backups').iterdir()), [])


if __name__ == '__main__':
    unittest.main()
