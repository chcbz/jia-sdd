from pathlib import Path
import subprocess,json,hashlib,datetime,threading,time
ROOT=Path('/home/isp/wsps/cyf/evidence/u1u3-entry-finalization-integration-v1')
SOURCE=Path('/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/api-entry-finalization-integration-v1')
SOCKET='/var/tmp/cyf-jyt-mmd-mysql-20260929-thread01a0dde8/mysql.sock'
ARGS=['mysql','--no-defaults','--socket='+SOCKET,'-u','root','--batch','--skip-column-names','--unbuffered']
sha=subprocess.check_output(['git','-C',str(SOURCE),'rev-parse','HEAD']).decode().strip();tree=subprocess.check_output(['git','-C',str(SOURCE),'rev-parse','HEAD^{tree}']).decode().strip()
DB='mmd_final_'+tree[:8]+'_'+datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
result={'candidate_commit':sha,'candidate_tree':tree,'database':DB,'scope':'current-thread isolated MySQL actual finalization DDL/constraints/locks only; NOT Java initializer lifecycle/module build/Provider/acceptance','cases':[],'failures':[]}
def run(sql,db=None):return subprocess.run(ARGS+([db] if db else []),input=sql,text=True,capture_output=True)
def require(sql,db=None):
 r=run(sql,db)
 if r.returncode:raise RuntimeError(r.stderr.strip())
 return r.stdout.strip()
def case(name,sql,reject=False,code=None):
 r=run('START TRANSACTION;\n'+sql+'\nROLLBACK;',DB)
 ok=(r.returncode!=0 and (code is None or ('ERROR '+str(code)+' ') in r.stderr)) if reject else r.returncode==0
 row={'name':name,'expected':'reject' if reject else 'accept','passed':ok,'exit':r.returncode,'stderr':r.stderr.strip()};result['cases'].append(row)
 if not ok:result['failures'].append(name)
def literal(v):return 'NULL' if v is None else str(v) if isinstance(v,int) else "'"+str(v).replace("'","''")+"'"
def insert(table,values):return 'INSERT INTO '+table+' ('+','.join(values)+') VALUES ('+','.join(literal(v) for v in values.values())+');'
identity=require('SELECT @@socket,@@datadir,@@version,@@port,@@skip_networking;').split('\t')
assert identity==[SOCKET,'/var/tmp/cyf-jyt-mmd-mysql-20260929-thread01a0dde8/data/','8.0.21','0','1'],identity
result['mysql_identity']=identity
require('CREATE DATABASE '+DB+' CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_bin;')
paths=[SOURCE/'agent/jia-agent-mapper/src/main/resources/db/agent-selected-output-finalization-v1.sql',SOURCE/'chat/jia-chat-mapper/src/main/resources/db/chat-selected-output-finalization-v1.sql']
result['ddl_sha256']={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in paths}
for repetition in range(2):
 for f in paths:require(f.read_text(),DB)
result['ddl_repeat_passed']=True
meta=require("SELECT table_name,engine,table_collation FROM information_schema.tables WHERE table_schema=DATABASE() ORDER BY table_name;",DB)
assert all('\tInnoDB\tutf8mb4_0900_bin' in row for row in meta.splitlines());assert len(meta.splitlines())==3
result['table_metadata']=meta
indexes=require("SELECT table_name,index_name,non_unique,seq_in_index,column_name,IF(sub_part IS NULL,'SQL_NULL',CAST(sub_part AS CHAR)) FROM information_schema.statistics WHERE table_schema=DATABASE() ORDER BY table_name,index_name,seq_in_index;",DB)
assert all(row.endswith('\tSQL_NULL') for row in indexes.splitlines());result['index_metadata']=indexes
checks=require("SELECT table_name,constraint_name,enforced FROM information_schema.table_constraints WHERE constraint_schema=DATABASE() AND constraint_type='CHECK' ORDER BY table_name,constraint_name;",DB)
assert len(checks.splitlines())==14 and all(row.endswith('\tYES') for row in checks.splitlines());result['enforced_checks']=checks
agent=dict(operation_id='op-1',tenant_id='0',client_id='client-1',owner_jiacn='owner-1',task_id='task-1',immutable_digest='a'*64,source_facts_digest='b'*64,expected_task_version=7,expected_assignment_revision=7,conversation_id='100',conversation_generation=3,target_agent_id='agent-1',grant_id='grant-1',grant_version=2,run_id='run-1',summary='chosen',delivery_id='delivery-1',manifest_artifact_id='manifest-1',phase='CLAIMING',version=0,created_at=1,updated_at=1)
chat=dict(operation_id='op-1',tenant_id='0',owner_jiacn='owner-1',client_id='client-1',task_id='task-1',idempotency_key='key-0001',request_digest='b'*64,conversation_id='100',expected_task_version=7,expected_assignment_revision=7,summary='chosen',state='pending',stage='PROMOTING',state_version=1,task_state='assigned',task_version=7,retryable=0,created_at=1,updated_at=1)
item=dict(tenant_id='0',owner_jiacn='owner-1',client_id='client-1',operation_id='op-1',item_order=0,request_id='req-1',step_id='step-1',output_id='out-1',sha256='a'*64,title='bird',purpose='final')
A='agent_selected_output_finalization';C='chat_selected_output_finalization';I='chat_selected_output_finalization_item'
case('agent_claiming',insert(A,agent));case('agent_leased',insert(A,dict(agent,phase='LEASED',lease_token='fixture-lease',lease_work_item_version=5)))
case('agent_null_lease_version_rejected',insert(A,dict(agent,phase='LEASED',lease_token='fixture-lease',lease_work_item_version=None)),True,3819)
case('agent_negative_lease_version_rejected',insert(A,dict(agent,phase='READY',lease_token='fixture-lease',lease_work_item_version=-1)),True,3819)
case('agent_submitted_cleared_token',insert(A,dict(agent,phase='SUBMITTED',lease_work_item_version=5)))
case('agent_submitted_credential_retention_rejected',insert(A,dict(agent,phase='SUBMITTED',lease_token='fixture-lease',lease_work_item_version=5)),True,3819)
case('agent_unsafe_version_rejected',insert(A,dict(agent,expected_task_version=9007199254740992)),True,3819)
case('agent_scope_unique_delivery',insert(A,agent)+insert(A,dict(agent,operation_id='op-2')),True,1062)
case('agent_owner_isolation',insert(A,agent)+insert(A,dict(agent,owner_jiacn='other-owner')))
case('agent_case_binary_scope',insert(A,agent)+insert(A,dict(agent,owner_jiacn='OWNER-1')))
case('chat_promoting',insert(C,chat))
sub=dict(chat,stage='SUBMITTED',delivery_id='delivery-1',delivery_state='submitted',task_state='reviewing',task_version=9)
case('chat_submitted',insert(C,sub))
case('chat_null_delivery_state_rejected',insert(C,dict(sub,delivery_state=None)),True,3819)
case('chat_accepting_changes_requested',insert(C,dict(sub,state='failed',stage='ACCEPTING',delivery_state='changes_requested',task_state='running',task_version=10,error_code='FINALIZATION_DELIVERY_CHANGES_REQUESTED')))
terminal=dict(sub,state='completed',stage='TASK_COMPLETED',delivery_state='accepted',task_state='completed',task_version=10)
case('chat_completed',insert(C,terminal))
case('chat_completed_null_delivery_state_rejected',insert(C,dict(terminal,delivery_state=None)),True,3819)
case('chat_completed_before_acceptance_rejected',insert(C,dict(terminal,delivery_state='submitted')),True,3819)
case('chat_task_completed_pending_rejected',insert(C,dict(terminal,state='pending')),True,3819)
case('chat_duplicate_original_key_rejected',insert(C,chat)+insert(C,dict(chat,operation_id='op-2')),True,1062)
case('chat_owner_isolation',insert(C,chat)+insert(C,dict(chat,owner_jiacn='other-owner')))
case('chat_bad_original_key_rejected',insert(C,dict(chat,idempotency_key='unsafe/key')),True,3819)
case('chat_precision_rejected',insert(C,dict(chat,task_version=9007199254740992)),True,3819)
case('item_exact_source_unique',insert(I,item)+insert(I,dict(item,item_order=1)),True,1062)
case('item_max_order',insert(I,dict(item,item_order=98)))
case('item_out_of_range_order_rejected',insert(I,dict(item,item_order=99)),True,3819)
case('item_owner_isolation',insert(I,item)+insert(I,dict(item,owner_jiacn='other-owner')))
# Three owned connections: observe exact contention, never cancel a waiter or steal lock.
def session():return subprocess.Popen(ARGS,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
def send(p,s):p.stdin.write(s+'\n');p.stdin.flush()
def ask(p,s):send(p,s);return p.stdout.readline().strip()
owner=session();waiter=session();observer=session()
try:
 oid=int(ask(owner,'SELECT CONNECTION_ID();'));wid=int(ask(waiter,'SELECT CONNECTION_ID();'))
 locks=[]
 for prefix in ['agent','chat']:
  # Fixture-scoped name, exact production -1 timeout semantics, never take shared production lock.
  name='mmd:'+DB+':'+prefix;assert len(name)<=64
  assert ask(owner,"SELECT GET_LOCK('"+name+"',-1);")=='1'
  assert ask(observer,"SELECT IS_USED_LOCK('"+name+"');")==str(oid)
  answer=[];send(waiter,"SELECT GET_LOCK('"+name+"',-1);")
  thread=threading.Thread(target=lambda:answer.append(waiter.stdout.readline().strip()));thread.start()
  while True:
   state=ask(observer,'SELECT COALESCE((SELECT STATE FROM information_schema.processlist WHERE ID='+str(wid)+"),'absent');")
   if state=='User lock':break
   if not thread.is_alive():raise AssertionError('waiter returned before holder released: '+repr(answer))
   time.sleep(0.02)
  assert ask(observer,"SELECT RELEASE_LOCK('"+name+"');")=='0'
  assert ask(owner,"SELECT RELEASE_LOCK('"+name+"');")=='1'
  thread.join();assert answer==['1'],answer
  assert ask(observer,"SELECT IS_USED_LOCK('"+name+"');")==str(wid)
  assert ask(owner,"SELECT RELEASE_LOCK('"+name+"');")=='0'
  assert ask(waiter,"SELECT RELEASE_LOCK('"+name+"');")=='1'
  assert ask(observer,"SELECT IS_FREE_LOCK('"+name+"');")=='1'
  locks.append({'name':name,'holder_connection':oid,'waiter_connection':wid,'observed_state':'User lock','wait_parameter':-1,'nonowner_release':0,'holder_release':1,'waiter_acquired':1,'waiter_release':1,'free_after':1})
 result['lock_semantics']=locks
finally:
 for p in [owner,waiter,observer]:
  p.stdin.close();p.wait()
result['pass']=not result['failures'];result['passed_cases']=sum(c['passed'] for c in result['cases']);result['total_cases']=len(result['cases']);result['database_retained_no_foreign_schema_write']=True
out=ROOT/('mysql-finalization-'+tree[:8]+'-v1.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'path':str(out),'pass':result['pass'],'passed_cases':result['passed_cases'],'total_cases':result['total_cases'],'failures':result['failures'],'ddl_repeat_passed':True,'lock_semantics_passed':True},indent=2))
raise SystemExit(0 if result['pass'] else 1)
