-- Once only; inspect each column on partial execution. No UPDATE from current active grant.
ALTER TABLE agent_task_execution_grant
 ADD COLUMN executor_owner_jiacn VARCHAR(50) COLLATE utf8mb4_0900_bin NULL,
 ADD COLUMN executor_binding_id BIGINT NULL,
 ADD COLUMN external_policy_revision BIGINT NULL;
