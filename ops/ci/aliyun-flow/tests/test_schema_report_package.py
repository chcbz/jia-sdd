"""Report catalog safety for both fixed-SQL schema runners; no DB calls."""
import importlib.machinery,io,os,tarfile,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SchemaReportPackageTest(unittest.TestCase):
 def test_safe_reports_and_adversarial_members(self):
  for name in ('cyf-api-additive-schema','cyf-api-e05-additive-schema'):
   module=importlib.machinery.SourceFileLoader(name,str(ROOT/'host'/name)).load_module()
   cases=[([],True),([('test-results','dir'),('test-results/sub','dir'),('test-results/sub/test.xml','file'),('test-results/summary.json','file')],True)]
   for member,kind in [('test-results/a.xml','link'),('test-results/a.xml','hardlink'),('test-results/../a.xml','file'),('/test-results/a.xml','file'),('test-results/a\\b.xml','file'),('test-results/runner.sh','file')]:cases.append(([(member,kind)],False))
   cases.extend([([('test-results/a.xml','file')]*2,False),([('test-results','dir')]*2,False),([('application.jar','file')],False)])
   for extra,ok in cases:
    with self.subTest(runner=name,extra=extra),tempfile.TemporaryDirectory() as d:
     p=Path(d)/'package.tgz'
     with tarfile.open(str(p),'w:gz') as t:
      for member in sorted(module.EXPECTED_PACKAGE_MEMBERS):
       raw=b'core';m=tarfile.TarInfo('./'+member);m.size=len(raw);t.addfile(m,io.BytesIO(raw))
      for member,kind in extra:
       m=tarfile.TarInfo(member)
       if kind=='dir':m.type=tarfile.DIRTYPE;t.addfile(m)
       elif kind in ('link','hardlink'):m.type=tarfile.SYMTYPE if kind=='link' else tarfile.LNKTYPE;m.linkname='application.jar';t.addfile(m)
       else:raw=b'report';m.size=len(raw);t.addfile(m,io.BytesIO(raw))
     p.chmod(0o600)
     if ok:self.assertEqual(module.load_package(p,os.getuid(),0o600)[0],b'core')
     else:
      with self.assertRaises(module.SchemaError):module.load_package(p,os.getuid(),0o600)
if __name__=='__main__':unittest.main()
