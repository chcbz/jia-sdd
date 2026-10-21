-- Only after committed backfill/postcheck and approved recovery sequence from README.
-- Once-only: inspect exact nullable/index metadata for partial execution.
ALTER TABLE agent_task_execution_grant
 MODIFY COLUMN executor_owner_jiacn VARCHAR(50) COLLATE utf8mb4_0900_bin NOT NULL,
 MODIFY COLUMN executor_binding_id BIGINT NOT NULL,
 ADD INDEX idx_atxg_executor (tenant_id,client_id,executor_owner_jiacn,target_agent_id,state);
