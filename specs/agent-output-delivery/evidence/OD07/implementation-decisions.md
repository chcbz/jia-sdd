# OD07 implementation decisions

2026-09-13, writer proposal accepted by Root within existing implementation authorization:

1. Stage the final M003 contract: OD07 implements the four `agent_task_meta` columns and three `agent_task_work_item` columns, while `output_run_binding.work_item_id` already exists. OD08 adds delivery/review tables. Use distinct executable migration/strict-validation segments (M003A/M003B or repository-equivalent identifiers); never mark full M003 applied after only the OD07 segment. Validate fresh, upgrade, repeat and invalid/partial schema states per segment. The final schema-contract.yaml remains authoritative and unchanged.
2. Policy1 admission is default-off with an empty owner allowlist. Only an explicitly enabled isolated allowed owner/scope and a fresh capable client may enter the incomplete R2 development flow. Do not expose ordinary-user creation before downstream submit/review is implemented. No user-supplied policyVersion may override admission.
3. Serial API implementation: migration/DTO/ticket-bound HTTP lease+recovery/receipt; then all policy1 entry guards; then actual MySQL authenticated creation/dispatch, concurrency/run/rollback and policy0 regression. Freeze the API before client changes. Root remains the control-plane writer.

These are implementation staging decisions, not a reduced acceptance scope or authorization for deployment/financial integration. All final R2 fields, transactions and acceptance criteria remain due under OD07–OD11.

Feature-off compatibility correction: intermediate API3343342b added fields to shared MyBatis entities/mappers but initially conditioned M003A on the output business switch. Root identified that a feature-off old database could then receive SELECT/INSERT/UPDATE for absent columns. Writer confirmed and chose M003A as an unconditional Agent-core schema prerequisite after agentSchemaInitializer; policy1/HTTP admission remains default-off. Final candidate must prove strict upgrade plus legacy policy0 CRUD from a pre-M003A schema with the business switch disabled, without hand-installing the columns first. This correction is agreed, not yet validated or independently accepted.
