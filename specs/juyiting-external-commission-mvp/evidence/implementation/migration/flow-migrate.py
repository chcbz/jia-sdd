#!/usr/bin/python3
"""D31-only Flow hook. No LOCAL bridge, no helper edits, no alternative artifact admission.
Requires a root-only, exact Run binding via D31_FLOW_BINDING. This file is NOT run by tests.
"""
import contextlib
import datetime
import fcntl
import hashlib
import importlib.machinery
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import uuid

HERE = Path(__file__).resolve().parent
ADAPTER = Path('/usr/local/sbin/cyf-api-flow-deploy')
INSTALLER = '/usr/local/sbin/cyf-api-flow-install'
LIFECYCLE = '/usr/local/sbin/cyf-api-kit'
JAR = Path('/home/isp/hosts/cyf/api/cyf-api-kit.jar')
STATE = Path('/home/isp/state/cyf-api-flow')
MYSQL = ['/usr/bin/mysql','--no-defaults','--protocol=SOCKET',
         '--socket=/home/isp/apps/mysql/mysql.sock','--user=root',
         '--batch','--raw','--skip-column-names','--unbuffered','jia']
TABLES = ['agent_task_execution_grant','chat_dispatch_outbox',
          'agent_task_bounty_bootstrap_outbox','chat_typed_admission','chat_turn',
          'chat_context_snapshot','agent_identity_registry','agent_persona_binding',
          'agent_identity_legacy_manifest']

class Blocked(RuntimeError): pass

def need(ok, code):
    if not ok: raise Blocked(code)

def sha(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

def trusted(path, mode=None):
    p=Path(path); s=p.lstat()
    need(stat.S_ISREG(s.st_mode) and s.st_uid==0 and s.st_nlink==1
         and not s.st_mode & 0o022 and (mode is None or stat.S_IMODE(s.st_mode)==mode),'UNTRUSTED_FILE')
    return p

def atomic(path, value):
    p=Path(path); tmp=p.with_name('.'+p.name+'.'+uuid.uuid4().hex)
    fd=os.open(str(tmp),os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
    with os.fdopen(fd,'w') as f:
        json.dump(value,f,sort_keys=True,indent=2);f.write('\n');f.flush();os.fsync(f.fileno())
    os.replace(str(tmp),str(p))
    fd=os.open(str(p.parent),os.O_RDONLY|os.O_DIRECTORY)
    try: os.fsync(fd)
    finally: os.close(fd)

def pinned_text(name):
    pins=json.loads(trusted(HERE/'candidate-pins.json').read_text())
    match=[p for p in pins['inputs'] if p['file']==name]
    need(len(match)==1,'UNPINNED_SQL')
    raw=trusted(HERE/name).read_bytes()
    need(hashlib.sha256(raw).hexdigest()==match[0]['sha256'],'SQL_CHANGED_AT_USE')
    return raw.decode('utf-8')

def load_adapter():
    loader=importlib.machinery.SourceFileLoader('d31_pinned_flow_adapter',str(ADAPTER))
    spec=importlib.util.spec_from_loader(loader.name,loader)
    module=importlib.util.module_from_spec(spec);loader.exec_module(module)
    return module

def check_inputs(binding, argv):
    keys={'format','pipeline','run','commit','tree','version','artifactSha256','pinsSha256',
          'wrapperSha256','oldJarSha256','oldRecordSha256','rollbackPolicy','otherWritersQuiesced'}
    need(set(binding)==keys and binding['format']=='jyt-d31-flow-migration-v1','BINDING_SHAPE')
    need(binding['pipeline']=='5260799' and re.fullmatch('[1-9][0-9]*',binding['run']) is not None,'FLOW_ID')
    need(argv==[binding[k] for k in ('pipeline','run','commit','version','artifactSha256')],'FLOW_ARGUMENT_MISMATCH')
    need(all(re.fullmatch('[0-9a-f]{40}',binding[k]) for k in ('commit','tree')),'SOURCE_ID')
    need(all(re.fullmatch('[0-9a-f]{64}',binding[k]) for k in
             ('artifactSha256','pinsSha256','wrapperSha256','oldJarSha256','oldRecordSha256')),'DIGEST_SHAPE')
    need(binding['rollbackPolicy']=='forward-only' and binding['otherWritersQuiesced'] is True,'CUTOVER_CONTRACT')
    need(sha(trusted(HERE/'candidate-pins.json'))==binding['pinsSha256'],'PINS_CHANGED')
    need(sha(trusted(Path(__file__)))==binding['wrapperSha256'],'WRAPPER_CHANGED')
    pins=json.loads((HERE/'candidate-pins.json').read_text())
    for item in pins['inputs']: need(sha(trusted(HERE/item['file']))==item['sha256'],'PINNED_INPUT_CHANGED')
    for name,digest in pins['installedHelpers'].items(): need(sha(trusted(name))==digest,'HELPER_CHANGED')
    return pins

def held_coordinator(path):
    """Prove original main owns the actual kernel flock; do not acquire/adopt it."""
    s=Path(path).lstat();need(stat.S_ISREG(s.st_mode) and s.st_uid==0 and stat.S_IMODE(s.st_mode)==0o600,'COORDINATOR_METADATA')
    key=(os.major(s.st_dev),os.minor(s.st_dev),s.st_ino)
    for p in Path('/proc/self/fdinfo').iterdir():
        try: lines=p.read_text().splitlines()
        except FileNotFoundError: continue
        for line in lines:
            a=line.split()
            if len(a)>=9 and a[0]=='lock:' and a[2:5]==['FLOCK','ADVISORY','WRITE']:
                major,minor,inode=a[6].split(':')
                if (int(major,16),int(minor,16),int(inode))==key and int(a[5])==os.getpid(): return
    raise Blocked('ORIGINAL_COORDINATOR_NOT_HELD')

@contextlib.contextmanager
def release_lifecycle(adapter):
    held_coordinator(adapter.LOCK)
    for fd in (8,9):
        try: os.fstat(fd)
        except OSError: continue
        raise Blocked('INHERITED_DESCRIPTOR_CONFLICT')
    opened=[]
    try:
        fd=adapter.acquire_e05_release_lock(adapter.RELEASE_LOCK) # unchanged existing release-lock primitive
        os.dup2(fd,8)
        if fd!=8: os.close(fd)
        opened.append(8)
        path=Path('/tmp/cyf-api-lifecycle.lock');s=path.lstat()
        need(stat.S_ISREG(s.st_mode) and s.st_uid==0 and s.st_nlink==1 and stat.S_IMODE(s.st_mode)==0o600,'LIFECYCLE_LOCK_METADATA')
        fd=os.open(str(path),os.O_RDWR|os.O_NOFOLLOW);os.dup2(fd,9)
        if fd!=9: os.close(fd)
        opened.append(9)
        f=os.fstat(9);need((f.st_dev,f.st_ino)==(s.st_dev,s.st_ino),'LIFECYCLE_LOCK_CHANGED')
        fcntl.flock(9,fcntl.LOCK_EX)
        env=adapter.installer_environment()
        for k in list(env):
            if k.startswith(('CYF_RELEASE_','CYF_LIFECYCLE_LOCK_','CYF_API_LOCAL_',
                             'CYF_API_FLOW_INSTALL_TEST_','CYF_API_FLOW_TEST_','CYF_API_KIT_VALIDATION')): env.pop(k,None)
        for fd,prefix in ((8,'CYF_RELEASE_LOCK_'),(9,'CYF_LIFECYCLE_LOCK_')):
            s=os.fstat(fd)
            env.update({prefix+'INHERITED_FD':str(fd),prefix+'DEVICE':str(s.st_dev),
                        prefix+'INODE':str(s.st_ino),prefix+'HELD':'1'})
        yield env
    finally:
        for fd in reversed(opened): os.close(fd)

class Database:
    """One mysql session: named lock + DML transactions stay on this connection."""
    def __init__(self, directory):
        self.err=open(str(directory/'mysql.stderr'),'ab',buffering=0)
        self.p=subprocess.Popen(MYSQL,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=self.err,
                                universal_newlines=True,bufsize=1)
    def query(self, sql):
        marker='D31_'+uuid.uuid4().hex
        self.p.stdin.write(sql.rstrip().rstrip(';')+';\nSELECT "'+marker+'";\n');self.p.stdin.flush()
        rows=[]
        while True:
            line=self.p.stdout.readline()
            need(bool(line),'MYSQL_STATEMENT_FAILED_SEE_PRIVATE_LOG')
            line=line.rstrip('\n')
            if line==marker: return rows
            rows.append(line)
    def json(self, sql): return [json.loads(s) for s in self.query(sql)]
    def file(self, name): return self.query(pinned_text(name))
    def close(self):
        if self.p.poll() is None:
            self.p.stdin.close() # EOF rolls back any open transaction and releases named lock
            self.p.wait()
        self.p.stdout.close();self.err.close()

# Exact additive column definitions, no arbitrary table/SQL input accepted.
COLUMNS={
 'agent_task_execution_grant':[
  ('executor_owner_jiacn','varchar(50)','utf8mb4_0900_bin'),('executor_binding_id','bigint',None),
  ('external_policy_revision','bigint',None)],
 'chat_dispatch_outbox':[
  ('task_grant_id','varchar(100)','utf8mb4_0900_bin'),('task_grant_version','bigint',None),
  ('task_assignment_revision','bigint',None),('task_requirement_revision','bigint',None)]}
INDEXES={
 ('chat_dispatch_outbox','idx_chat_outbox_dispatch'):['tenant_id','client_id','dispatch_id','event_type'],
 ('agent_task_execution_grant','idx_atxg_executor'):['tenant_id','client_id','executor_owner_jiacn','target_agent_id','state']}

def columns(db, table):
    return db.json("SELECT JSON_OBJECT('name',column_name,'type',column_type,'collation',collation_name,'nullable',is_nullable,'default',column_default,'extra',extra) FROM information_schema.columns WHERE table_schema='jia' AND table_name='"+table+"' ORDER BY ordinal_position")

def check_column(row, typ, collation, nullable=None):
    need(row['type']==typ and row['collation']==collation and row['default'] is None and row['extra']=='','COLUMN_DRIFT')
    if nullable is not None: need(row['nullable']==nullable,'COLUMN_NULLABILITY_DRIFT')

def index_rows(db,table,name):
    return db.json("SELECT JSON_OBJECT('name',column_name,'nonUnique',non_unique,'prefix',sub_part,'expression',expression) FROM information_schema.statistics WHERE table_schema='jia' AND table_name='"+table+"' AND index_name='"+name+"' ORDER BY seq_in_index")

def ensure_index(db, table, name, mutate):
    expected=INDEXES[(table,name)]; rows=index_rows(db,table,name)
    if not rows and mutate:
        db.query('CREATE INDEX '+name+' ON '+table+' ('+','.join(expected)+')');rows=index_rows(db,table,name)
    need([r['name'] for r in rows]==expected and all(r['nonUnique']==1 and r['prefix'] is None and r['expression'] is None for r in rows),'INDEX_DRIFT')

def policy_catalog(db):
    """Exact fixed policy schema, including uniqueness and CHECK semantics."""
    table='agent_external_service_policy'; rows=columns(db,table)
    expected=[('id','bigint',None),('tenant_id','varchar(50)','utf8mb4_0900_bin'),
      ('client_id','varchar(50)','utf8mb4_0900_bin'),('provider_owner_jiacn','varchar(50)','utf8mb4_0900_bin'),
      ('agent_id','varchar(100)','utf8mb4_0900_bin'),('binding_id','bigint',None),('revision','bigint',None),
      ('expected_revision','bigint',None),('enabled','tinyint(1)',None),
      ('idempotency_key','varchar(100)','utf8mb4_0900_bin'),('request_hash','char(64)','ascii_bin'),('created_at','bigint',None)]
    need([r['name'] for r in rows]==[r[0] for r in expected],'POLICY_COLUMNS')
    for r,(name,typ,coll) in zip(rows,expected):
        need(r['extra']==('auto_increment' if name=='id' else ''),'POLICY_EXTRA')
        r=dict(r,extra='');check_column(r,typ,coll,'NO')
    for name,fields in {'PRIMARY':['id'],'uk_external_policy_revision':['tenant_id','client_id','agent_id','binding_id','revision'],
                        'uk_external_policy_request':['tenant_id','client_id','provider_owner_jiacn','idempotency_key']}.items():
        idx=index_rows(db,table,name)
        need([r['name'] for r in idx]==fields and all(r['nonUnique']==0 and r['prefix'] is None and r['expression'] is None for r in idx),'POLICY_INDEX')
    checks=db.json("SELECT JSON_OBJECT('name',cc.constraint_name,'clause',cc.check_clause,'enforced',tc.enforced) FROM information_schema.check_constraints cc JOIN information_schema.table_constraints tc ON tc.constraint_schema=cc.constraint_schema AND tc.constraint_name=cc.constraint_name WHERE tc.table_schema='jia' AND tc.table_name='agent_external_service_policy' AND tc.constraint_type='CHECK'")
    expected_checks={'chk_external_policy_revision':'expected_revision>=0andrevision=expected_revision+1',
                     'chk_external_policy_enabled':'enabledin0,1','chk_external_policy_binding':'binding_id>0'}
    actual={r['name']:re.sub(r'[\s`()]+','',r['clause']).lower() for r in checks}
    need(actual==expected_checks and all(r['enforced']=='YES' for r in checks),'POLICY_CHECKS')
    need(db.query("SELECT CONCAT(engine,':',table_collation) FROM information_schema.tables WHERE table_schema='jia' AND table_name='agent_external_service_policy'")==['InnoDB:utf8mb4_0900_bin'],'POLICY_TABLE')

class Migration:
    def __init__(self, adapter, binding, pins):
        self.a=adapter;self.b=binding;self.pins=pins
        self.directory=Path('/home/isp/baks')/('jyt-external-d31-'+binding['run']+'-'+binding['commit'])
        self.journal=None;self.db=None
    def mark(self, phase, **values):
        self.journal['phase']=phase;self.journal.update(values)
        self.journal['updatedAt']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        atomic(self.directory/'phase.json',self.journal)
    def validate_candidate(self):
        held_coordinator(self.a.LOCK)
        check_inputs(self.b,sys.argv[1:])
        approval=json.loads(trusted(self.a.APPROVAL,0o600).read_text())
        need(approval.get('schema_version')==2 and approval.get('consumed') is False,'NON_FLOW_OR_CONSUMED_APPROVAL')
        for key,bkey in [('run_id','run'),('source_commit_sha','commit'),('source_tree_sha','tree')]:
            need(approval.get(key)==self.b[bkey],'APPROVAL_BINDING')
        context=self.a._SCHEMA_CONTEXT
        need(context and context['run_id']==self.b['run'] and context['pipeline_id']=='5260799'
             and context['receipt_sha256']==approval['receipt_sha256'] and context['jar_sha256']==approval['jar_sha256'],'ORIGINAL_VERIFIED_CONTEXT')
        need(sha(trusted(self.a.PACKAGE))==self.b['artifactSha256'],'ARTIFACT_CHANGED')
        version=json.loads(trusted(self.a.ROOT/('versioned-release-'+self.b['run']+'.json'),0o600).read_text())
        need(version['status']=='prepared' and version['artifact_sha256']==self.b['artifactSha256']
             and version['commit']==self.b['commit'] and version['tree']==self.b['tree']
             and version['receipt_sha256']==approval['receipt_sha256'] and version['jar_sha256']==approval['jar_sha256'],'VERSIONED_RELEASE_CHANGED')
        return approval
    def init_journal(self, approval):
        self.directory.mkdir(mode=0o700,exist_ok=True)
        s=self.directory.lstat();need(stat.S_ISDIR(s.st_mode) and s.st_uid==0 and stat.S_IMODE(s.st_mode)==0o700,'BACKUP_DIRECTORY_UNSAFE')
        path=self.directory/'phase.json'
        exact={'binding':self.b,'receiptSha256':approval['receipt_sha256'],'candidateSha256':approval['jar_sha256']}
        if path.exists():
            self.journal=json.loads(trusted(path,0o600).read_text())
            need(all(self.journal.get(k)==v for k,v in exact.items()),'FOREIGN_MIGRATION_JOURNAL')
        else:
            self.journal=exact;self.mark('PREPARED')
    def lifecycle(self, action, env):
        need(action in ('stop','status'),'NO_WRAPPER_START')
        with open(str(self.directory/('lifecycle-'+action+'.log')),'ab') as output:
            result=subprocess.run([LIFECYCLE,action],env=env,pass_fds=(8,9),close_fds=True,stdout=output,stderr=output)
        return result.returncode
    def stop(self, env):
        need(self.lifecycle('stop',env)==0,'STOP_FAILED')
        need(self.lifecycle('status',env)!=0,'SERVICE_STILL_ACTIVE')
        # Original lifecycle identity guard plus independent canonical JVM scan.
        need(not Path('/run/cyf-api/cyf-api-kit.runtime').exists(),'RUNTIME_RECORD_STILL_PRESENT')
        for proc in Path('/proc').iterdir():
            if not proc.name.isdigit(): continue
            try:
                args=(proc/'cmdline').read_bytes().split(b'\0')
                if b'-jar' not in args: continue
                cwd=Path(os.readlink(str(proc/'cwd')))
                for n,arg in enumerate(args[:-1]):
                    if arg==b'-jar':
                        jar=Path(os.fsdecode(args[n+1]));jar=jar if jar.is_absolute() else cwd/jar
                        need(jar.resolve()!=JAR.resolve() and cwd.resolve()!=JAR.parent.resolve(),'SURVIVING_CANONICAL_WRITER')
            except (FileNotFoundError,ProcessLookupError): continue
    def connect(self):
        self.db=Database(self.directory)
        while True:
            lock=self.db.query("SELECT GET_LOCK('cyf:external-commission:v1',60)")
            if lock==['1']: break
            need(lock==['0'],'MYSQL_LOCK_FAILED')
        target=self.db.json("SELECT JSON_OBJECT('schema',DATABASE(),'uuid',SHA2(@@server_uuid,256),'version',VERSION())")[0]
        need(target=={'schema':'jia','uuid':self.pins['target']['serverUuidSha256'],'version':self.pins['target']['mysqlVersionObserved']},'DB_TARGET_CHANGED')
    def catalog(self):
        return self.db.json("SELECT JSON_OBJECT('table',table_name,'name',column_name,'type',column_type,'nullable',is_nullable,'collation',collation_name,'extra',extra,'default',column_default) FROM information_schema.columns WHERE table_schema='jia' AND table_name IN ('agent_task_execution_grant','chat_dispatch_outbox','agent_external_service_policy') ORDER BY table_name,ordinal_position") + self.db.json("SELECT JSON_OBJECT('table',table_name,'index',index_name,'column',column_name,'position',seq_in_index,'nonUnique',non_unique,'prefix',sub_part,'expression',expression) FROM information_schema.statistics WHERE table_schema='jia' AND table_name IN ('agent_task_execution_grant','chat_dispatch_outbox','agent_external_service_policy') ORDER BY table_name,index_name,seq_in_index")
    def backup(self):
        if self.journal.get('backup'):
            for name,digest in self.journal['backup'].items(): need(sha(trusted(self.directory/name,0o600))==digest,'BACKUP_CHANGED')
            return
        # Once any DDL is marked, a new after-DDL backup cannot masquerade as the original.
        need(not self.journal.get('ddlStarted'),'ORIGINAL_BACKUP_MISSING')
        atomic(self.directory/'catalog-before.json',self.catalog())
        for name,source,digest in [('application-before.jar',JAR,self.b['oldJarSha256']),
                ('record-before.json',self.a.ROOT/'record.json',self.b['oldRecordSha256'])]:
            need(sha(trusted(source))==digest,'PREBACKUP_SOURCE_CHANGED')
            target=self.directory/name
            if target.exists(): need(sha(trusted(target,0o600))==digest,'BACKUP_FILE_CONFLICT')
            else:
                with target.open('xb') as out,source.open('rb') as inp:
                    shutil.copyfileobj(inp,out);out.flush();os.fsync(out.fileno())
                os.chmod(str(target),0o600)
            need(sha(target)==digest,'BACKUP_COPY_FAILED')
        tables=list(TABLES)
        if columns(self.db,'agent_external_service_policy'): tables.append('agent_external_service_policy')
        output=self.directory/'database-before.sql'
        # Interrupted dump is not a completed backup; replace only its own unsealed temporary file.
        tmp=self.directory/'database-before.sql.partial'
        with open(str(tmp),'wb') as out,open(str(self.directory/'mysqldump.stderr'),'ab') as err:
            result=subprocess.run(['/usr/bin/mysqldump','--no-defaults','--protocol=SOCKET',
              '--socket=/home/isp/apps/mysql/mysql.sock','--user=root','--single-transaction',
              '--skip-lock-tables','--no-tablespaces','--set-gtid-purged=OFF','jia']+tables,stdout=out,stderr=err)
            out.flush();os.fsync(out.fileno())
        need(result.returncode==0 and tmp.stat().st_size>0,'BACKUP_FAILED')
        os.replace(str(tmp),str(output))
        self.mark('BACKUP_COMPLETE',backup={n:sha(self.directory/n) for n in ('database-before.sql','catalog-before.json','application-before.jar','record-before.json')})
    def proof(self):
        grants=self.db.query(pinned_text('grant-freeze.cte.sql')+"SELECT (SELECT COUNT(*) FROM agent_task_execution_grant),COUNT(*) FROM freeze_proven")
        need(len(grants)==1,'GRANT_PROOF_SHAPE');total,proven=map(int,grants[0].split('\t'))
        need(total==proven,'UNPROVEN_GRANT_FREEZE')
        chat=self.db.query(pinned_text('chat-proof.cte.sql')+"SELECT (SELECT COUNT(*) FROM chat_dispatch_outbox WHERE event_type='DISPATCH' AND JSON_UNQUOTE(JSON_EXTRACT(payload_json,'$.conversationScopeType'))='bounty'),(SELECT COUNT(*) FROM proven),(SELECT COUNT(*) FROM (SELECT event_id FROM distinct_candidates GROUP BY event_id HAVING COUNT(*)>1) amb)")
        need(len(chat)==1,'CHAT_PROOF_SHAPE');bounty,proven,amb=map(int,chat[0].split('\t'))
        need(bounty==proven and amb==0,'UNPROVEN_CHAT_REFERENCE')
        counts={'grants':total,'bountyDispatches':bounty}
        if 'inventory' in self.journal: need(counts==self.journal['inventory'],'INVENTORY_CHANGED_DURING_MAINTENANCE')
        self.mark('PROOF_VERIFIED',inventory=counts)
    def expand(self):
        self.mark('EXPANDING',ddlStarted=True)
        for table,defs in COLUMNS.items():
            for name,typ,coll in defs:
                rows={r['name']:r for r in columns(self.db,table)}
                if name not in rows:
                    self.db.query('ALTER TABLE '+table+' ADD COLUMN '+name+' '+typ+
                                  (' COLLATE '+coll if coll else '')+' NULL')
                    rows={r['name']:r for r in columns(self.db,table)}
                nullable=None if table=='agent_task_execution_grant' and name!='external_policy_revision' else 'YES'
                check_column(rows[name],typ,coll,nullable)
                self.mark('COLUMN_READY',lastColumn=table+'.'+name)
        ensure_index(self.db,'chat_dispatch_outbox','idx_chat_outbox_dispatch',True)
        if not columns(self.db,'agent_external_service_policy'): self.db.file('candidate-agent-policy.sql')
        policy_catalog(self.db);self.mark('EXPANDED')
    def check_counts(self, name, expected):
        rows=self.db.file(name);need(len(rows)==1,'POSTCHECK_SHAPE')
        values=[int(x) if x!='NULL' else 0 for x in rows[0].split('\t')]
        need(values[0]==expected and all(v==0 for v in values[1:]),'POSTCHECK_FAILED_'+name)
    def backfill(self):
        self.db.file('02-agent-freeze.sql') # leaves same session transaction open
        self.check_counts('04-agent-postcheck.sql',self.journal['inventory']['grants'])
        self.db.query('COMMIT');self.mark('GRANT_FROZEN')
        sql=pinned_text('02-chat-proven-backfill.sql')
        need(sql.rstrip().endswith('COMMIT;'),'CHAT_SCRIPT_SHAPE')
        self.db.query(sql.rstrip()[:-len('COMMIT;')])
        self.check_counts('03-chat-postcheck.sql',self.journal['inventory']['bountyDispatches'])
        self.db.query('COMMIT');self.mark('CHAT_BACKFILLED')
    def original_catalog_unchanged(self):
        before=json.loads(trusted(self.directory/'catalog-before.json',0o600).read_text())
        current=self.catalog()
        for row in before:
            if row['table']=='agent_external_service_policy': continue
            if row.get('name') in {x[0] for x in COLUMNS.get(row['table'],[])}: continue
            if (row['table'],row.get('index')) in INDEXES: continue
            need(row in current,'ORIGINAL_CATALOG_CHANGED')
        for table in TABLES:
            need(self.db.query("SELECT engine FROM information_schema.tables WHERE table_schema='jia' AND table_name='"+table+"'")==['InnoDB'],'ENGINE_CHANGED')

    def schema_postcheck(self):
        for table,defs in COLUMNS.items():
            rows={r['name']:r for r in columns(self.db,table)}
            for name,typ,coll in defs:
                nullable='NO' if table=='agent_task_execution_grant' and name!='external_policy_revision' else 'YES'
                need(name in rows,'COLUMN_MISSING');check_column(rows[name],typ,coll,nullable)
        for table,name in INDEXES: ensure_index(self.db,table,name,False)
        policy_catalog(self.db)
        self.original_catalog_unchanged()
    def finalize(self):
        for name,typ,coll in COLUMNS['agent_task_execution_grant'][:2]:
            row={r['name']:r for r in columns(self.db,'agent_task_execution_grant')}[name]
            if row['nullable']=='YES':
                self.db.query('ALTER TABLE agent_task_execution_grant MODIFY COLUMN '+name+' '+typ+
                              (' COLLATE '+coll if coll else '')+' NOT NULL')
        ensure_index(self.db,'agent_task_execution_grant','idx_atxg_executor',True)
        self.schema_postcheck()
        self.check_counts('04-agent-postcheck.sql',self.journal['inventory']['grants'])
        self.check_counts('03-chat-postcheck.sql',self.journal['inventory']['bountyDispatches'])
        catalog=self.catalog();atomic(self.directory/'catalog-after.json',catalog)
        self.mark('MIGRATION_COMPLETE',migrationComplete=True,catalogAfterSha256=sha(self.directory/'catalog-after.json'))
    def run_locked(self):
        approval=self.validate_candidate();self.init_journal(approval)
        with release_lifecycle(self.a) as env:
            current=sha(trusted(JAR));record=Path(self.a.ROOT)/'record.json'
            if current==self.b['oldJarSha256']:
                need(sha(trusted(record,0o600))==self.b['oldRecordSha256'],'OLD_RECORD_CHANGED')
            else:
                need(current==approval['jar_sha256'] and self.journal.get('migrationComplete'),'UNEXPECTED_CANONICAL_JAR')
                r=json.loads(trusted(record,0o600).read_text())
                need(r.get('run_id')==self.b['run'] and r.get('receipt_sha256')==approval['receipt_sha256']
                     and r.get('candidate_sha256')==current and r.get('status')=='failed'
                     and r.get('recovery')=='forward_only_candidate_retained','NOT_EXACT_FORWARD_RECOVERY')
            record_before=sha(trusted(record,0o600))
            self.stop(env);self.mark('STOPPED')
            try:
                self.connect()
                if self.journal.get('migrationComplete'):
                    self.schema_postcheck()
                    need(self.catalog()==json.loads(trusted(self.directory/'catalog-after.json',0o600).read_text()),'COMPLETED_SCHEMA_DRIFT')
                else:
                    self.proof();self.backup();self.expand();self.backfill();self.finalize()
                self.validate_candidate()
                need(sha(JAR)==current and sha(record)==record_before,'PREINSTALL_STATE_CHANGED')
                self.mark('READY_FOR_ORIGINAL_INSTALLER',preinstallJarSha256=current,preinstallRecordSha256=sha(record))
            except BaseException:
                self.mark('MIGRATION_FAILED_STOPPED')
                raise
            finally:
                if self.db: self.db.close();self.db=None
        # Coordinator is still held by original main. No LOCAL receipt or inherited lock
        # environment is passed to installer, which reacquires the original release lock.
        held_coordinator(self.a.LOCK)
    def failed_install_stop(self):
        with release_lifecycle(self.a) as env:
            need(sha(trusted(JAR)) in (self.b['oldJarSha256'],self.journal['candidateSha256']),'FAILED_INSTALL_FOREIGN_JAR')
            self.stop(env);self.mark('INSTALL_FAILED_STOPPED')

def install_hook(adapter, migration, original):
    def hook(installer):
        need(installer==INSTALLER,'UNEXPECTED_INSTALLER')
        migration.run_locked()
        held_coordinator(adapter.LOCK)
        os.environ['CYF_API_FLOW_FORWARD_ONLY']='1'
        migration.mark('ORIGINAL_INSTALLER_CALLED',forwardOnly=True)
        try: result=original(installer)
        except BaseException:
            migration.failed_install_stop();raise
        if result:
            migration.failed_install_stop()
        else: migration.mark('ORIGINAL_INSTALLER_VERIFIED')
        return result
    return hook

def main():
    os.umask(0o077)
    need(os.geteuid()==0,'ROOT_REQUIRED')
    need(len(sys.argv)==6,'ORIGINAL_FIVE_ARGUMENTS_REQUIRED')
    need(not any(k.startswith(('CYF_API_LOCAL_','CYF_RELEASE_OFFLINE_TEST','CYF_API_FLOW_TEST_',
                               'CYF_API_FLOW_INSTALL_TEST_')) for k in os.environ),'TEST_OR_LOCAL_ENV_REJECTED')
    binding=json.loads(trusted(os.environ['D31_FLOW_BINDING'],0o600).read_text())
    pins=check_inputs(binding,sys.argv[1:])
    adapter=load_adapter()
    migration=Migration(adapter,binding,pins)
    adapter.invoke_installer=install_hook(adapter,migration,adapter.invoke_installer)
    adapter.main() # original argument/provenance/approval/coordinator logic, unchanged

if __name__=='__main__':
    try: main()
    except (Blocked,OSError,KeyError,ValueError) as exc:
        # Private logs hold DB/lifecycle details. Never echo SQL/content/credentials.
        print(json.dumps({'status':'BLOCKED','feature':'JYT-D31','reason':str(exc) if isinstance(exc,Blocked) else type(exc).__name__}))
        raise SystemExit(2)
