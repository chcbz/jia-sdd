import importlib.machinery
import os
from pathlib import Path
from types import SimpleNamespace
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch, Mock

ROOT = Path(__file__).resolve().parents[1]
deploy = importlib.machinery.SourceFileLoader('backup_alias_deploy', str(ROOT/'host/cyf-api-flow-deploy')).load_module()

class BackupDirectoryTest(unittest.TestCase):
    def check(self, alias=True, logical='/var/lib/cyf-api-flow/backups', target='/home/isp/baks/flow-api', uid=0, gid=0, mode=0o700, link_uid=0, link_gid=0, target_link=False, directory=True):
        path=Mock(); path.__eq__ = Mock(side_effect=lambda other: str(other)==logical)
        path.lstat.return_value=SimpleNamespace(st_mode=stat.S_IFLNK if alias else stat.S_IFDIR, st_uid=link_uid, st_gid=link_gid)
        path.resolve.return_value=Path(target)
        path.stat.return_value=SimpleNamespace(st_mode=(stat.S_IFDIR if directory else stat.S_IFREG)|mode,st_uid=uid,st_gid=gid)
        with patch.object(Path,'is_symlink',return_value=target_link):
            deploy.validate_backup_directory(path)

    def test_physical_root_directory(self): self.check(alias=False)
    def test_exact_existing_alias(self): self.check()
    def test_reject_wrong_alias_target_owner_permissions_or_file(self):
        for kwargs in [dict(logical='/tmp/backups'), dict(target='/tmp/other'),dict(link_uid=1),dict(link_gid=1),dict(uid=1),dict(gid=1),dict(mode=0o755),dict(target_link=True),dict(directory=False)]:
            with self.subTest(kwargs=kwargs), self.assertRaises(SystemExit): self.check(**kwargs)
    def test_real_temporary_directory_permission_validation(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d); p.chmod(0o700); deploy.validate_backup_directory(p)
            p.chmod(0o755)
            with self.assertRaises(SystemExit): deploy.validate_backup_directory(p)
    def test_installer_alias_deny_by_default_and_offline(self):
        source=(ROOT/'host/cyf-api-flow-install').read_text()
        a=source.index('validate_backup_alias() {'); b=source.index('\n}',a)+2
        function=source[a:b]
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); physical=root/'physical'; physical.mkdir(); alias=root/'alias'; alias.symlink_to(physical)
            for offline in ['0','1']:
                env=dict(os.environ,BACKUP_ROOT=str(alias),OFFLINE_TEST=offline)
                r=subprocess.run(['bash','-c','fail() { exit 29; }\n'+function+'\nvalidate_backup_alias'],env=env)
                self.assertEqual(r.returncode,29)
            env=dict(os.environ,BACKUP_ROOT=str(physical),OFFLINE_TEST='1')
            r=subprocess.run(['bash','-c','fail() { exit 29; }\n'+function+'\nvalidate_backup_alias'],env=env)
            self.assertEqual(r.returncode,0)
    @unittest.skipUnless(Path("/var/lib/cyf-api-flow/backups").is_symlink(), "host alias observation only")
    def test_actual_readonly_approved_alias(self):
        deploy.validate_backup_directory(Path('/var/lib/cyf-api-flow/backups'))

if __name__=='__main__': unittest.main()
