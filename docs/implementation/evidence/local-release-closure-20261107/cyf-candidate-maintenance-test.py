import sys,importlib.util,unittest
from pathlib import Path
c=Path('/tmp/cyf-closure-validation-20261107');test=c/'ops/maintenance/tests/test_flow_host_cleanup.py'
sys.argv=[str(test),str(c/'ops/maintenance/flow_host_cleanup.py')]
s=importlib.util.spec_from_file_location('candidate_flow_test',test);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
original=m.m.Paths
class CandidatePaths(original):
 def __init__(self):
  super().__init__();self.validator=Path('/root/cyf-closure-validation-20261107/cyf-api-flow-deploy');self.web_validator=Path('/root/cyf-closure-validation-20261107/cyf-web-flow-deploy')
m.m.Paths=CandidatePaths
result=unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromModule(m));sys.exit(not result.wasSuccessful())
