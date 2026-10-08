"""Portable source contract: production API has exactly one installation target."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[4]
HOST=ROOT/'ops/ci/aliyun-flow/host'
class CanonicalApiPathTests(unittest.TestCase):
 def test_lifecycle_and_installer_target(self):
  self.assertRegex((HOST/'cyf-api-kit').read_text(),r'(?m)^DEPLOY_DIR=/home/isp/hosts/cyf/api$')
  self.assertRegex((HOST/'cyf-api-flow-install').read_text(),r'(?m)^TARGET_JAR=/home/isp/hosts/cyf/api/cyf-api-kit\.jar$')
 def test_schema_targets(self):
  for name in ['cyf-api-additive-schema','cyf-api-e05-additive-schema']:
   self.assertIn("CANONICAL_JAR = Path('/home/isp/hosts/cyf/api/cyf-api-kit.jar')",(HOST/name).read_text())
 def test_completion_target_and_ancestors(self):
  text=(ROOT/'ops/ci/aliyun-flow/auto/complete-installed-schema.py').read_text()
  self.assertIn("self.jar = Path('/home/isp/hosts/cyf/api/cyf-api-kit.jar')",text)
  for name in ['/home','/home/isp','/home/isp/hosts','/home/isp/hosts/cyf','/home/isp/hosts/cyf/api']:
   self.assertIn('Path(%r)'%name,text)
 def test_no_old_opt_deployment_defaults(self):
  for name in ['cyf-api-kit','cyf-api-flow-install','cyf-api-additive-schema','cyf-api-e05-additive-schema']:
   self.assertNotIn('/opt/cyf/service/api',(HOST/name).read_text())
 def test_root_owned_ancestor_guards(self):
  for name in ['cyf-api-kit','cyf-api-flow-install']:
   text=(HOST/name).read_text()
   self.assertIn('for parent in /home /home/isp /home/isp/hosts /home/isp/hosts/cyf;',text)
   self.assertIn('& 0022',text)
 def test_launcher_closes_migration_locks(self):
  self.assertIn('5>&- 6>&- 7>&- 8>&- 9>&- &',(HOST/'cyf-api-kit').read_text())
if __name__=='__main__':unittest.main(verbosity=2)
