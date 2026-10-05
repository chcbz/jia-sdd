import importlib.machinery
import io
import os
from pathlib import Path
import re
import subprocess
import tarfile
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
DEPLOY=Path(os.environ.get('CYF_REPORT_DEPLOY_TEST_SOURCE',str(ROOT/'host/cyf-api-flow-deploy')))
INSTALLER=ROOT/'host/cyf-api-flow-install'
deploy=importlib.machinery.SourceFileLoader('report_package_deploy',str(DEPLOY)).load_module()

class ReportPackageTest(unittest.TestCase):
    def package(self, path, extra=None, omit=None):
        with tarfile.open(str(path),'w:gz') as t:
            for name in sorted(deploy.EXPECTED_MEMBERS):
                if name==omit: continue
                raw=b'core'; m=tarfile.TarInfo('./'+name);m.size=len(raw);t.addfile(m,io.BytesIO(raw))
            for name,kind in extra or []:
                m=tarfile.TarInfo(name)
                if kind=='dir': m.type=tarfile.DIRTYPE;t.addfile(m)
                elif kind=='link':m.type=tarfile.SYMTYPE;m.linkname='/tmp/escape';t.addfile(m)
                elif kind=='hardlink':m.type=tarfile.LNKTYPE;m.linkname='application.jar';t.addfile(m)
                else:raw=b'report';m.size=len(raw);t.addfile(m,io.BytesIO(raw))
    def scripts(self):
        s=INSTALLER.read_text()
        a=s.index('EXTRACT_BYTES="$(python3');start=s.index("<<'PY'\n",a)+len("<<'PY'\n");end=s.index('\nPY\n',start)
        admission=s[start:end]
        start=s.index('def write_all(fd, block):');end=s.index('directory_fd =',start)
        extraction='import os,sys,tarfile\nfrom pathlib import Path\npackage=Path(sys.argv[1]);root=Path(sys.argv[2])\nexpected='+repr(deploy.EXPECTED_MEMBERS)+'\n'+s[start:end]+'\nprint(total)\n'
        return admission,extraction
    def exercise(self, extra=None, omit=None, expect_ok=True):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'package.tgz';self.package(p,extra,omit)
            with tarfile.open(str(p)) as t:
                if expect_ok:self.assertEqual(set(deploy.validated_release_members(t)),deploy.EXPECTED_MEMBERS)
                else:
                    with self.assertRaises(SystemExit):deploy.validated_release_members(t)
            for i,script in enumerate(self.scripts()):
                root=Path(d)/('out'+str(i));root.mkdir(mode=0o700)
                r=subprocess.run(['python3','-I','-B','-',str(p),str(root)],input=script,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
                if expect_ok:
                    self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(int(r.stdout.strip()),20)
                    if i==1:self.assertEqual({q.name for q in root.iterdir()},deploy.EXPECTED_MEMBERS)
                else:self.assertNotEqual(r.returncode,0)
    def test_original_five_file_release_still_accepted(self):self.exercise()
    def test_cloud_xml_and_summary_admitted_but_never_extracted(self):
        self.exercise([('./test-results','dir'),('./test-results/jia','dir'),('./test-results/jia/tests.xml','file'),('./test-results/summary.json','file')])
    def test_symlink_hardlink_traversal_absolute_or_backslash_report_rejected(self):
        for name,kind in [('test-results/test.xml','link'),('test-results/test.xml','hardlink'),('test-results/../escape.xml','file'),('/test-results/a.xml','file'),('test-results/a\\b.xml','file')]:
            with self.subTest(name=name,kind=kind):self.exercise([(name,kind)],expect_ok=False)
    def test_duplicate_report_and_directory_rejected(self):
        for name,kind in [('test-results/a.xml','file'),('test-results','dir')]:
            with self.subTest(name=name):self.exercise([(name,kind),(name,kind)],expect_ok=False)
    def test_arbitrary_report_payload_not_admitted(self):self.exercise([('test-results/runner.sh','file')],expect_ok=False)
    def test_unknown_root_file_rejected(self):self.exercise([('surprise.xml','file')],expect_ok=False)
    def test_duplicate_core_rejected(self):self.exercise([('application.jar','file')],expect_ok=False)
    def test_reports_never_substitute_missing_core(self):self.exercise([('test-results/a.xml','file')],omit='application.jar',expect_ok=False)
    @unittest.skipUnless(Path('/var/lib/cyf-api-flow/downloads/110/package.tgz').is_file(),'actual Flow110 read-only evidence')
    def test_actual_flow110_full_catalog_readonly(self):
        with tarfile.open('/var/lib/cyf-api-flow/downloads/110/package.tgz') as t:self.assertEqual(set(deploy.validated_release_members(t)),deploy.EXPECTED_MEMBERS)
        script=self.scripts()[0];r=subprocess.run(['python3','-I','-B','-','/var/lib/cyf-api-flow/downloads/110/package.tgz'],input=script,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True);self.assertEqual(r.returncode,0,r.stderr);self.assertGreater(int(r.stdout),0)

if __name__=='__main__':unittest.main()
