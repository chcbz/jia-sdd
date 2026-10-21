-- Execute only while ALL writers stopped, after backup + fresh preflight.
-- Freeze migration-time same-owner identity; NOT a claim that old grant stored binding.
-- This script intentionally leaves transaction OPEN. Same mysql session must verify
-- 04-agent-postcheck.sql missing/conflicting = 0, then COMMIT; otherwise ROLLBACK.
START TRANSACTION;
WITH freeze_candidates AS (
 SELECT g.id, g.grant_id, g.owner_jiacn executor_owner_jiacn, i.binding_id executor_binding_id
 FROM agent_task_execution_grant g
 JOIN agent_identity_registry i ON BINARY i.canonical_agent_id=BINARY g.target_agent_id
  AND BINARY i.tenant_id=BINARY g.tenant_id AND BINARY i.client_id=BINARY g.client_id
  AND BINARY i.owner_jiacn=BINARY g.owner_jiacn
 JOIN agent_persona_binding b ON b.id=i.binding_id
  AND BINARY b.agent_id=BINARY i.canonical_agent_id AND BINARY b.tenant_id=BINARY i.tenant_id
  AND BINARY b.client_id=BINARY i.client_id AND BINARY b.jiacn=BINARY i.owner_jiacn
 WHERE i.canonical_type='LEGACY_CANONICAL' AND i.lifecycle_status='ACTIVE' AND b.status=1
  AND i.binding_id>0 AND i.create_time<=g.created_at AND i.provisioned_at<=g.created_at
  AND b.create_time<=g.created_at AND b.bound_at<=g.created_at
  AND i.update_time<=g.created_at AND b.update_time<=g.created_at
  AND BINARY g.issued_by=BINARY g.owner_jiacn
  AND NOT EXISTS (SELECT 1 FROM agent_persona_binding x WHERE BINARY x.agent_id=BINARY b.agent_id AND x.id<>b.id)
  AND EXISTS (SELECT 1 FROM agent_identity_legacy_manifest m
   WHERE BINARY m.canonical_agent_id=BINARY g.target_agent_id
    AND BINARY m.source_client_id=BINARY g.client_id AND BINARY m.source_owner_jiacn=BINARY g.owner_jiacn
    AND m.binding_id=i.binding_id AND m.approval_status='APPROVED' AND m.approved_at<=g.created_at)
  AND EXISTS (SELECT 1 FROM agent_task_bounty_bootstrap_outbox s
   WHERE BINARY s.tenant_id=BINARY g.tenant_id AND BINARY s.client_id=BINARY g.client_id
    AND BINARY s.owner_jiacn=BINARY g.owner_jiacn AND BINARY s.task_id=BINARY g.task_id
    AND BINARY s.grant_id=BINARY g.grant_id AND BINARY s.target_agent_id=BINARY g.target_agent_id
    AND BINARY s.source_business_action_id=BINARY g.source_business_action_id
    AND s.assignment_revision=g.assignment_revision AND s.requirement_revision=g.requirement_revision
    AND (s.grant_version=g.grant_version OR (g.state IN ('REVOKED','SUPERSEDED') AND s.grant_version+1=g.grant_version)))
  AND 2=(SELECT COUNT(*) FROM information_schema.triggers tr WHERE tr.trigger_schema=DATABASE()
   AND tr.event_object_table='agent_identity_registry' AND tr.action_timing='BEFORE'
   AND UNIX_TIMESTAMP(tr.created)*1000<=g.created_at
   AND ((tr.trigger_name='trg_identity_registry_immutable_update' AND tr.event_manipulation='UPDATE'
    AND SHA2(tr.action_statement,256)='8cd26a8a03dab27589a440ab1e1f64547d38736b506748ff9444a040cdc7004c')
    OR (tr.trigger_name='trg_identity_registry_no_delete' AND tr.event_manipulation='DELETE'
    AND SHA2(tr.action_statement,256)='a74a659888fe8875cabedaad5846a0c8b2b7927340d43986b68fd88d2db11f13')))
), freeze_proven AS (
 SELECT id,MIN(grant_id) grant_id,MIN(executor_owner_jiacn) executor_owner_jiacn,
  MIN(executor_binding_id) executor_binding_id FROM freeze_candidates GROUP BY id HAVING COUNT(*)=1
)
UPDATE agent_task_execution_grant g JOIN freeze_proven p ON p.id=g.id
 SET g.executor_owner_jiacn=p.executor_owner_jiacn, g.executor_binding_id=p.executor_binding_id
 WHERE g.executor_owner_jiacn IS NULL AND g.executor_binding_id IS NULL
 AND g.external_policy_revision IS NULL;
