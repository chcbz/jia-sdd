#!/usr/bin/env python3
"""JYT-D31 production read-only audit. No DDL/DML, credentials, content, or raw IDs in output."""
import datetime
import hashlib
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
MYSQL = ['/usr/bin/mysql', '--no-defaults', '--protocol=SOCKET',
         '--socket=/home/isp/apps/mysql/mysql.sock', '--user=root', '--batch', '--raw', '--skip-column-names', 'jia']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def queries():
    proof = (HERE / 'chat-proof.cte.sql').read_text()
    freeze = (HERE / 'grant-freeze.cte.sql').read_text()
    # A single consistent read-only transaction; no locks, temp tables or session writes outside READ ONLY setup.
    return "SET SESSION TRANSACTION READ ONLY; START TRANSACTION WITH CONSISTENT SNAPSHOT, READ ONLY;\n" + "\n".join([
        "SELECT JSON_OBJECT('section','target','database',DATABASE(),'mysqlVersion',VERSION(),'serverUuidSha256',SHA2(@@server_uuid,256));",
        "SELECT JSON_OBJECT('section','grantStates','state',state,'count',COUNT(*)) FROM agent_task_execution_grant GROUP BY state;",
        "SELECT JSON_OBJECT('section','bootstrapStates','status',status,'count',COUNT(*)) FROM agent_task_bounty_bootstrap_outbox GROUP BY status;",
        "SELECT JSON_OBJECT('section','outboxStates','eventType',event_type,'status',status,'count',COUNT(*)) FROM chat_dispatch_outbox GROUP BY event_type,status;",
        "SELECT JSON_OBJECT('section','turnStates','route',route,'state',state,'count',COUNT(*)) FROM chat_turn GROUP BY route,state;",
        "SELECT JSON_OBJECT('section','schema','table',table_name,'column',column_name,'type',column_type,'nullable',is_nullable,'collation',collation_name) FROM information_schema.columns WHERE table_schema='jia' AND ((table_name='agent_task_execution_grant' AND column_name IN ('executor_owner_jiacn','executor_binding_id','external_policy_revision')) OR (table_name='chat_dispatch_outbox' AND column_name IN ('task_grant_id','task_grant_version','task_assignment_revision','task_requirement_revision'))) ORDER BY table_name,ordinal_position;",
        "SELECT JSON_OBJECT('section','indexes','table',table_name,'index',index_name,'column',column_name,'position',seq_in_index,'nonUnique',non_unique) FROM information_schema.statistics WHERE table_schema='jia' AND index_name IN ('idx_atxg_executor','idx_chat_outbox_dispatch') ORDER BY table_name,index_name,seq_in_index;",
        "SELECT JSON_OBJECT('section','engine','table',table_name,'engine',engine) FROM information_schema.tables WHERE table_schema='jia' AND table_name IN ('agent_task_execution_grant','chat_dispatch_outbox','agent_identity_registry','agent_identity_legacy_manifest','agent_task_bounty_bootstrap_outbox','chat_typed_admission','chat_turn','chat_context_snapshot');",
        "SELECT JSON_OBJECT('section','invalidDispatchJson','count',COUNT(*)) FROM chat_dispatch_outbox WHERE event_type='DISPATCH' AND NOT JSON_VALID(payload_json);",
        proof + "SELECT JSON_OBJECT('section','chatProof','bountyDispatches',(SELECT COUNT(*) FROM chat_dispatch_outbox WHERE event_type='DISPATCH' AND JSON_UNQUOTE(JSON_EXTRACT(payload_json,'$.conversationScopeType'))='bounty'),'provenDispatches',(SELECT COUNT(*) FROM proven),'ambiguousDispatches',(SELECT COUNT(*) FROM (SELECT event_id FROM distinct_candidates GROUP BY event_id HAVING COUNT(*)>1) x));",
        proof + "SELECT JSON_OBJECT('section','unresolvedChat','dispatchHash',LEFT(SHA2(CONCAT('JYT-D31:',o.dispatch_id),256),16),'outboxStatus',o.status,'turnState',t.state) FROM chat_dispatch_outbox o JOIN chat_turn t ON t.turn_id=o.turn_id LEFT JOIN proven p ON p.event_id=o.event_id WHERE o.event_type='DISPATCH' AND JSON_UNQUOTE(JSON_EXTRACT(o.payload_json,'$.conversationScopeType'))='bounty' AND p.event_id IS NULL;",
        proof + "SELECT JSON_OBJECT('section','inflightChat','turnHash',LEFT(SHA2(CONCAT('JYT-D31:',t.turn_id),256),16),'state',t.state,'proven',p.event_id IS NOT NULL) FROM chat_turn t JOIN chat_dispatch_outbox o ON o.turn_id=t.turn_id AND o.event_type='DISPATCH' LEFT JOIN proven p ON p.event_id=o.event_id WHERE t.state NOT IN ('PUBLISHED','FINAL_PERSISTED','FAILED','CANCELLED');",
        "SELECT JSON_OBJECT('section','grantBindingProof','grants',COUNT(*),'strictManifestProven',SUM(EXISTS(SELECT 1 FROM agent_identity_legacy_manifest m WHERE BINARY m.canonical_agent_id=BINARY g.target_agent_id AND BINARY m.source_client_id=BINARY g.client_id AND BINARY m.source_owner_jiacn=BINARY g.owner_jiacn AND BINARY m.target_tenant_id=BINARY g.tenant_id AND m.binding_id IS NOT NULL AND m.approval_status='APPROVED' AND m.approved_at<=g.created_at)),'currentRegistryCandidatesNotProof',SUM(EXISTS(SELECT 1 FROM agent_identity_registry i WHERE BINARY i.canonical_agent_id=BINARY g.target_agent_id AND BINARY i.tenant_id=BINARY g.tenant_id AND BINARY i.client_id=BINARY g.client_id AND BINARY i.owner_jiacn=BINARY g.owner_jiacn AND i.binding_id IS NOT NULL))) FROM agent_task_execution_grant g;",
        "SELECT JSON_OBJECT('section','unresolvedGrant','grantHash',LEFT(SHA2(CONCAT('JYT-D31:',g.grant_id),256),16),'state',g.state) FROM agent_task_execution_grant g WHERE NOT EXISTS(SELECT 1 FROM agent_identity_legacy_manifest m WHERE BINARY m.canonical_agent_id=BINARY g.target_agent_id AND BINARY m.source_client_id=BINARY g.client_id AND BINARY m.source_owner_jiacn=BINARY g.owner_jiacn AND BINARY m.target_tenant_id=BINARY g.tenant_id AND m.binding_id IS NOT NULL AND m.approval_status='APPROVED' AND m.approved_at<=g.created_at);",
        freeze + "SELECT JSON_OBJECT('section','migrationBindingFreeze','grants',(SELECT COUNT(*) FROM agent_task_execution_grant),'proven',COUNT(*),'semantics','freeze-at-migration-not-retroactive-grant-binding') FROM freeze_proven;",
        freeze + "SELECT JSON_OBJECT('section','unresolvedMigrationFreeze','grantHash',LEFT(SHA2(CONCAT('JYT-D31:',g.grant_id),256),16)) FROM agent_task_execution_grant g LEFT JOIN freeze_proven p ON p.id=g.id WHERE p.id IS NULL;",
        "SELECT JSON_OBJECT('section','registryGuards','trigger',trigger_name,'created',created,'bodySha256',SHA2(action_statement,256)) FROM information_schema.triggers WHERE trigger_schema='jia' AND event_object_table='agent_identity_registry';",
        "ROLLBACK;"
    ])

def main():
    if len(sys.argv) != 1:
        raise SystemExit('No arguments accepted; this entry is read-only and cannot apply a migration.')
    result = subprocess.run(MYSQL, input=queries(), universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode:
        # Do not echo SQL, target data or client diagnostics into shared logs.
        print(json.dumps({'status':'AUDIT_FAILED','mysqlExit':result.returncode}))
        return 2
    rows = [json.loads(line) for line in result.stdout.splitlines() if line.strip()]
    output = {'task':'JYT-EXTERNAL-D31-CHAT-20261021','capturedAt':datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'mode':'read-only-consistent-snapshot','targetSocket':'/home/isp/apps/mysql/mysql.sock','targetSchema':'jia',
              'scriptSha256':sha(Path(__file__).resolve()),'proofSha256':sha(HERE/'chat-proof.cte.sql'),'observations':rows,
              'releaseReady':False,'note':'strictManifestProven/unresolvedGrant are legacy tenant-equality diagnostics, NOT migration blockers. migrationBindingFreeze is the same-owner cutover proof. Release additionally needs stopped writers, backup, schema postcheck and Flow artifact validation.'}
    print(json.dumps(output,ensure_ascii=False,indent=2))
    return 0

if __name__=='__main__':
    sys.exit(main())
