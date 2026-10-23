WITH source_candidates AS (
 SELECT o.event_id,b.grant_id,b.grant_version,b.assignment_revision,b.requirement_revision
 FROM chat_dispatch_outbox o
 JOIN chat_turn t ON BINARY t.tenant_id=BINARY o.tenant_id AND BINARY t.client_id=BINARY o.client_id
  AND BINARY t.owner_jiacn=BINARY o.owner_jiacn AND BINARY t.turn_id=BINARY o.turn_id AND BINARY t.dispatch_id=BINARY o.dispatch_id
 JOIN chat_context_snapshot s ON BINARY s.snapshot_id=BINARY t.snapshot_id AND BINARY s.tenant_id=BINARY t.tenant_id
  AND BINARY s.client_id=BINARY t.client_id AND BINARY s.owner_jiacn=BINARY t.owner_jiacn
  AND BINARY s.request_id=BINARY t.request_id AND s.request_revision=t.request_revision
  AND BINARY s.conversation_id=BINARY t.conversation_id AND s.conversation_generation=t.conversation_generation
  AND BINARY s.target_agent_id=BINARY t.target_agent_id AND BINARY s.context_digest=BINARY t.context_digest
 LEFT JOIN chat_typed_admission a ON BINARY a.tenant_id=BINARY t.tenant_id AND BINARY a.client_id=BINARY t.client_id
  AND BINARY a.owner_jiacn=BINARY t.owner_jiacn AND BINARY a.request_id=BINARY t.request_id
  AND a.request_revision=t.request_revision AND BINARY a.conversation_id=BINARY t.conversation_id
  AND a.conversation_generation=t.conversation_generation
 JOIN agent_task_bounty_bootstrap_outbox b ON BINARY b.tenant_id=BINARY t.tenant_id AND BINARY b.client_id=BINARY t.client_id
  AND BINARY b.owner_jiacn=BINARY t.owner_jiacn AND BINARY b.target_agent_id=BINARY t.target_agent_id
  AND BINARY b.task_id=BINARY JSON_UNQUOTE(JSON_EXTRACT(o.payload_json,'$.taskId'))
  AND ((BINARY b.admitted_request_id=BINARY t.request_id AND BINARY b.admitted_conversation_id=BINARY t.conversation_id)
    OR (BINARY b.task_id=BINARY a.task_id AND b.assignment_revision=a.assignment_revision))
 JOIN agent_task_execution_grant g ON BINARY g.tenant_id=BINARY b.tenant_id AND BINARY g.client_id=BINARY b.client_id
  AND BINARY g.owner_jiacn=BINARY b.owner_jiacn AND BINARY g.task_id=BINARY b.task_id
  AND BINARY g.grant_id=BINARY b.grant_id AND BINARY g.target_agent_id=BINARY b.target_agent_id
  AND g.assignment_revision=b.assignment_revision AND g.requirement_revision=b.requirement_revision
  AND (g.grant_version=b.grant_version OR (g.state IN ('REVOKED','SUPERSEDED') AND g.grant_version=b.grant_version+1))
 WHERE o.event_type='DISPATCH' AND JSON_UNQUOTE(JSON_EXTRACT(o.payload_json,'$.conversationScopeType'))='bounty'
  AND BINARY JSON_UNQUOTE(JSON_EXTRACT(o.payload_json,'$.contextHash'))=BINARY t.context_digest
  AND BINARY JSON_UNQUOTE(JSON_EXTRACT(o.payload_json,'$.requestId'))=BINARY t.request_id
  AND BINARY JSON_UNQUOTE(JSON_EXTRACT(o.payload_json,'$.targetAgentId'))=BINARY t.target_agent_id
  AND BINARY JSON_UNQUOTE(JSON_EXTRACT(o.payload_json,'$.contextSnapshotId'))=BINARY t.snapshot_id
), distinct_candidates AS (
 SELECT DISTINCT event_id,grant_id,grant_version,assignment_revision,requirement_revision FROM source_candidates
), proven AS (
 SELECT event_id,MIN(grant_id) grant_id,MIN(grant_version) grant_version,
  MIN(assignment_revision) assignment_revision,MIN(requirement_revision) requirement_revision
 FROM distinct_candidates GROUP BY event_id HAVING COUNT(*)=1
)
