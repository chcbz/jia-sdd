"""Small offline control-plane fixtures; never invoke a production process or Gradle."""
import fcntl
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[4]
HOST = ROOT / 'ops/ci/aliyun-flow/host'


def encoded(value):
    return (json.dumps(value, sort_keys=True, separators=(',', ':')) + '\n').encode()


def digest(value):
    return hashlib.sha256(value).hexdigest()


class ApiGatePolicyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='cyf-gate-policy-', dir='/tmp')
        self.root = Path(self.tmp.name)
        self.root.chmod(0o700)
        for name in ('state/incoming', 'state/backups', 'service', 'bin'):
            (self.root / name).mkdir(parents=True, exist_ok=True, mode=0o700)
        self.old = b'old-fixture-artifact'
        self.target = self.root / 'service/cyf-api-kit.jar'
        self.target.write_bytes(self.old)
        lock = self.root / 'cyf-release-api.lock'
        lock.touch(mode=0o600)
        lifecycle = self.root / 'bin/cyf-api-kit'
        lifecycle.write_text('''#!/bin/sh
root="$(dirname "$0")/.."
echo "$1" >> "$root/calls"
case "$1" in
stop) touch "$root/stopped" ;;
start) rm -f "$root/stopped" ;;
status) if [ -e "$root/stopped" ]; then echo STATUS=STOPPED; exit 3; fi; echo HEALTH=UP ;;
esac
''')
        lifecycle.chmod(0o700)
        jar = io.BytesIO()
        with zipfile.ZipFile(jar, 'w') as archive:
            archive.writestr('META-INF/MANIFEST.MF', 'Spring-Boot-Classes: BOOT-INF/classes/\nStart-Class: fixture.Main\n')
            archive.writestr('BOOT-INF/lib/fixture.jar', b'fixture')
        self.jar = jar.getvalue()
        provenance = encoded({'fixture': True})
        flow = dict(organization_id='5fb7d76ee6f9d07f148529c7', pipeline_id='5260799',
                    job_id='cloud_ci.api_ci', run_id='34', source_tip_sha='a' * 40)
        source = dict(branch='develop', commit_sha='a' * 40, tree_sha='b' * 40,
                      clean_before=True, clean_after=True)
        records = [dict(kind='application_jar', path='application.jar', sha256=digest(self.jar), size=len(self.jar)),
                   dict(kind='dependency_provenance', path='dependency.provenance.json', sha256=digest(provenance), size=len(provenance))]
        receipt = dict(schema_version=1, status='success', gradle_exit_code=0, bridge_exit_code=0,
                       ticket_sha256='c' * 64, flow=flow, source=source, files=records)
        receipt_bytes = encoded(receipt)
        metadata = dict(schema_version=1, receipt_sha256=digest(receipt_bytes), flow=flow, source=source,
                        application_jar=records[0], dependency_provenance=records[1])
        sidecar = dict(schema_version=1, receipt_sha256=digest(receipt_bytes), flow=flow,
                       sha256=digest(self.jar), size=len(self.jar))
        self.members = {'application.jar': self.jar, 'application.metadata.json': encoded(metadata),
                        'application.sidecar.json': encoded(sidecar), 'dependency.provenance.json': provenance,
                        'receipt.json': receipt_bytes}
        self.write_package()
        approval = dict(schema_version=2, ticket_sha256='c' * 64, source_commit_sha='a' * 40,
                        source_tree_sha='b' * 40, run_id='34', receipt_sha256=digest(receipt_bytes),
                        jar_sha256=digest(self.jar), consumed=False)
        path = self.root / 'state/approval.json'
        path.write_bytes(encoded(approval))
        path.chmod(0o600)
        self.env = dict(os.environ, CYF_RELEASE_OFFLINE_TEST='YES',
                        CYF_API_FLOW_INSTALL_TEST_ROOT=str(self.root),
                        CYF_API_FLOW_TEST_TARGET_AVAILABLE_BYTES=str(2 * 1024 * 1024),
                        CYF_API_FLOW_TEST_BACKUP_AVAILABLE_BYTES=str(2 * 1024 * 1024))

    def tearDown(self):
        self.tmp.cleanup()

    def write_package(self):
        with tarfile.open(str(self.root / 'state/incoming/package.tgz'), 'w:gz') as archive:
            for name, content in self.members.items():
                info = tarfile.TarInfo(name)
                info.size = len(content)
                archive.addfile(info, io.BytesIO(content))

    def install(self):
        return subprocess.run([str(HOST / 'cyf-api-flow-install')], env=self.env,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              universal_newlines=True, timeout=15)

    def assert_untouched(self):
        self.assertEqual(self.target.read_bytes(), self.old)
        self.assertFalse((self.root / 'calls').exists())

    def test_actual_artifact_space_succeeds_far_below_five_gib(self):
        result = self.install()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(self.target.read_bytes(), self.jar)
        record = json.loads((self.root / 'state/record.json').read_text())
        self.assertEqual(record['status'], 'installed')
        self.assertEqual(Path(record['backup']).read_bytes(), self.old)

    def test_insufficient_actual_space_stops_before_lifecycle(self):
        self.env['CYF_API_FLOW_TEST_TARGET_AVAILABLE_BYTES'] = '1'
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('capacity before unpacking', result.stderr)
        self.assert_untouched()

    def test_separate_backup_filesystem_requires_actual_backup_bytes(self):
        self.env.update(CYF_API_FLOW_TEST_TARGET_DEVICE='1', CYF_API_FLOW_TEST_BACKUP_DEVICE='2',
                        CYF_API_FLOW_TEST_BACKUP_AVAILABLE_BYTES='1')
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('backup capacity', result.stderr)
        self.assert_untouched()

    def test_tampered_artifact_is_rejected(self):
        self.members['application.jar'] += b'tamper'
        self.write_package()
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('JAR does not match receipt', result.stderr)
        self.assert_untouched()

    def test_wrong_source_approval_is_rejected(self):
        p = self.root / 'state/approval.json'
        data = json.loads(p.read_text())
        data['source_commit_sha'] = 'd' * 40
        p.write_bytes(encoded(data))
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('does not match exact root approval', result.stderr)
        self.assert_untouched()

    def test_path_traversal_is_rejected(self):
        self.members['../outside'] = b'forbidden'
        self.write_package()
        result = self.install()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('package member', result.stderr)
        self.assertFalse((self.root / 'outside').exists())
        self.assert_untouched()

    def test_embedded_python_compiles(self):
        for name in ('cyf-api-flow-install', 'cyf-api-kit'):
            text = (HOST / name).read_text()
            for index, body in enumerate(re.findall(r"<<'PY'\n(.*?)\nPY", text, re.S)):
                compile(body, '%s:embedded:%s' % (name, index), 'exec')

    def test_unmeasured_limits_and_timeout_kill_are_absent(self):
        installer = (HOST / 'cyf-api-flow-install').read_text()
        lifecycle = (HOST / 'cyf-api-kit').read_text()
        deploy = (HOST / 'cyf-api-flow-deploy').read_text()
        for name in ('MIN_LIFECYCLE_BYTES', 'MAX_PACKAGE_BYTES', 'MAX_EXTRACT_BYTES'):
            self.assertNotIn(name, installer)
        for name in ('MIN_DISK_AVAILABLE_BYTES', 'MIN_MEMORY_AVAILABLE_BYTES', 'TIMEOUT_SECONDS', '"$ticks" KILL'):
            self.assertNotIn(name, lifecycle)
        self.assertNotIn('LOCK_NB', deploy)
        self.assertNotIn('flock -w', installer)
        self.assertIn('healthy_endpoint_owned_by', lifecycle)
        self.assertIn('runtime_record_matches', lifecycle)
        self.assertIn('verify_lock_fd', lifecycle)


if __name__ == '__main__':
    unittest.main()
