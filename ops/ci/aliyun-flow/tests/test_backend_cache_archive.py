"""Check the real GNU tar exclusion against synthetic caches and artifacts."""
import hashlib
import os
import pathlib
import subprocess
import tarfile
import tempfile
import unittest


class CacheArchiveTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = pathlib.Path(self.tmp.name)
        self.home = self.base / 'root'
        for name in ('.m2/repository/unneeded.jar', '.m2/settings.xml', '.gradle/caches/dependency.jar',
                     '.cache/cyf-backend-jdk-archives/jdk.tgz', '.cache/cyf-backend-mysql-archives/mysql.txz'):
            p = self.home / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(('synthetic ' + name).encode())
        self.env = dict(os.environ, TAR_OPTIONS='--exclude=.m2/repository')

    def archive(self, args, name='archive.tgz'):
        target = self.base / name
        subprocess.run(['tar', '-czf', str(target)] + args, env=self.env, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        with tarfile.open(str(target)) as arc:
            return arc.getnames()

    def test_relative_cache_paths_exclude_only_maven_repository(self):
        names = self.archive(['-C', str(self.home), '.m2', '.gradle', '.cache'])
        self.assertFalse(any('/repository' in n for n in names))
        for n in ('.m2/settings.xml', '.gradle/caches/dependency.jar', '.cache/cyf-backend-jdk-archives/jdk.tgz', '.cache/cyf-backend-mysql-archives/mysql.txz'):
            self.assertIn(n, names)

    def test_absolute_cache_path_is_also_filtered(self):
        names = self.archive([str(self.home / '.m2')])
        self.assertFalse(any('/repository' in n for n in names))
        self.assertTrue(any(n.endswith('settings.xml') for n in names))

    def test_root_relative_cache_path_is_also_filtered(self):
        names = self.archive(['-C', str(self.base), 'root/.m2'])
        self.assertNotIn('root/.m2/repository/unneeded.jar', names)
        self.assertIn('root/.m2/settings.xml', names)

    def test_source_files_and_settings_are_untouched(self):
        before = {str(p.relative_to(self.home)): hashlib.sha256(p.read_bytes()).hexdigest()
                  for p in self.home.rglob('*') if p.is_file()}
        self.archive(['-C', str(self.home), '.m2', '.gradle', '.cache'])
        after = {str(p.relative_to(self.home)): hashlib.sha256(p.read_bytes()).hexdigest()
                 for p in self.home.rglob('*') if p.is_file()}
        self.assertEqual(before, after)

    def test_existing_full_archive_restores_without_maven_payload(self):
        old = self.base / 'old.tgz'
        env = dict(os.environ)
        env.pop('TAR_OPTIONS', None)
        subprocess.run(['tar', '-czf', str(old), '-C', str(self.home), '.m2', '.gradle', '.cache'], env=env, check=True)
        dest = self.base / 'restore'
        dest.mkdir()
        subprocess.run(['tar', '-xzf', str(old), '-C', str(dest)], env=self.env, check=True)
        self.assertFalse((dest / '.m2/repository').exists())
        self.assertTrue((dest / '.m2/settings.xml').is_file())
        self.assertTrue((dest / '.gradle/caches/dependency.jar').is_file())

    def test_allowed_release_artifact_members_are_not_filtered(self):
        src = self.base / 'artifact'
        src.mkdir()
        wanted = ['application.jar', 'receipt.json', 'application.metadata.json', 'dependency.provenance.json', 'test-results/summary.json', 'test-results/TEST-fixture.xml']
        for name in wanted:
            p = src / name
            p.parent.mkdir(exist_ok=True)
            p.write_bytes(b'synthetic fixture')
        names = self.archive(['-C', str(src), '.'])
        self.assertEqual(sorted(n.lstrip('./') for n in names if n not in ('.', './test-results')), sorted(wanted))


if __name__ == '__main__':
    unittest.main()
