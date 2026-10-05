import os
from pathlib import Path
import subprocess
import tempfile
import unittest
SOURCE=Path(__file__).resolve().parents[1]/'host/cyf-api-flow-install'
class ForwardRepairTest(unittest.TestCase):
 def run_case(self, flag='1', match='1', state='failed', recovery='forward_only_candidate_retained', target='candidate', start_fail=False, health_fail=False, record_fail=False):
  s=SOURCE.read_text(); funcs=[]
  for name in ['restore_and_start','resume_forward_candidate']:
   a=s.index(name+'() {'); b=s.index('\n}',a)+2;funcs.append(s[a:b])
  with tempfile.TemporaryDirectory() as d:
   p=Path(d); calls=p/'calls';lc=p/'lifecycle';lc.write_text('#!/bin/bash\necho lifecycle:start >> "$CALLS"\nexit '+('1' if start_fail else '0')+'\n');lc.chmod(0o700)
   pre='''set -eu
write_record() { echo "record:$*" >> "$CALLS"; RECORD_RETURN; }
lifecycle_healthy() { echo health >> "$CALLS"; HEALTH_RETURN; }
finalize_candidate() { echo finalize >> "$CALLS"; exit 0; }
fail() { echo fail >> "$CALLS"; exit 23; }
recoverable_fail() { echo record_fail >> "$CALLS"; exit 24; }
stop_and_verify() { echo old_stop >> "$CALLS"; }
detach_candidate() { echo detach >> "$CALLS"; }
restore_backup() { echo old_restore >> "$CALLS"; }
'''.replace('RECORD_RETURN','return 1' if record_fail else 'return 0').replace('HEALTH_RETURN','return 1' if health_fail else 'return 0')
   env=dict(os.environ,CALLS=str(calls),LIFECYCLE=str(lc),STOP_RC='0',CYF_API_FLOW_FORWARD_ONLY=flag,RECORD_MATCH=match,RECORD_STATUS=state,RECORD_RECOVERY=recovery,TARGET_STATE=target,JAR_SHA='candidate')
   r=subprocess.run(['bash','-c',pre+'\n'.join(funcs)+'\nresume_forward_candidate'],env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
   return r.returncode,calls.read_text().splitlines() if calls.exists() else []
 def test_same_candidate_explicit_retry_starts_and_finalizes(self):
  rc,c=self.run_case();self.assertEqual(rc,0);self.assertEqual(c,['record:activating forward_repair candidate_retained 0','lifecycle:start','health','finalize'])
 def test_wrong_flag_ticket_hash_state_or_failure_kind_cannot_resume(self):
  for kw in [dict(flag='0'),dict(match='0'),dict(target='other'),dict(state='activating'),dict(recovery='other')]:
   with self.subTest(kw=kw):rc,c=self.run_case(**kw);self.assertEqual(rc,1);self.assertEqual(c,[])
 def test_start_failure_retains_candidate_without_old_version_actions(self):
  rc,c=self.run_case(start_fail=True);self.assertEqual(rc,23);self.assertIn('record:failed forward_repair_start_failed forward_only_candidate_retained 0',c);self.assertNotIn('finalize',c);self.assertFalse(any('old_' in x or x=='detach' for x in c))
 def test_health_failure_retains_candidate_without_old_version_actions(self):
  rc,c=self.run_case(health_fail=True);self.assertEqual(rc,23);self.assertIn('record:failed forward_repair_status_failed forward_only_candidate_retained 0',c);self.assertNotIn('finalize',c)
 def test_interrupted_durable_intent_never_starts_or_restores(self):
  rc,c=self.run_case(record_fail=True);self.assertEqual(rc,24);self.assertNotIn('lifecycle:start',c);self.assertEqual(c[-1],'record_fail')
if __name__=='__main__': unittest.main()
