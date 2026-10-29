# 身份与业务租户解耦：全库结构盘点（2026-10-29）

Owner：当前任务主Agent。任务ID：IDENTITY-TENANT-DECOUPLING-20261029。源码：API `a5f28ec1dd84c33217e30ff748de898bc50c2f07`。

范围：本机MySQL可见业务库jia与jia_dev全部353个表/视图；不含MySQL系统库，不代表其他主机。只读元数据，没有写库/DDL/发布。
**覆盖含义：全量结构盘点和主源码精确表名引用索引，不等于353个对象全部业务链路通过安全审计。** 逐行待核状态保留；分类为候选处置，不是迁移已执行。
完整列、索引、外键、数据库程序与引用证据：`/home/isp/state/cyf-identity-decoupling-20261029/`。源码引用来自固定Git对象，不包含其他Owner脏工作树。
`client_id`在oauth_client中是协议客户端标识，在业务表中可能是应用授权范围，不能同名同删。

| 库 | 表/视图 | 租户列 | client列 | 处置分类 | 建议与边界 | 核对深度 |
|---|---|---|---|---|---|---|
| jia | `act_ge_bytearray` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ge_property` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ge_schema_log` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_actinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_attachment` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_batch` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_caseactinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_caseinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_comment` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_dec_in` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_dec_out` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_decinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_detail` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_ext_task_log` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_identitylink` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_incident` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_job_log` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_op_log` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_procinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_taskinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_hi_varinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_id_group` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_id_info` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_id_membership` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_id_tenant` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_id_tenant_member` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_id_user` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_re_camformdef` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_re_case_def` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_re_decision_def` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_re_decision_req_def` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_re_deployment` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_re_procdef` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_authorization` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_batch` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_case_execution` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_case_sentry_part` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_event_subscr` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_execution` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_ext_task` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_filter` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_identitylink` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_incident` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_job` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_jobdef` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_meter_log` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_task` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_task_meter_log` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `act_ru_variable` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia | `agent_command_delivery` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_command_operation_audit` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_command_redrive_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_consumer_inbox` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_controlled_image_bridge_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_controlled_image_execution_source_v3` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_controlled_image_intent_operation_grant` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_execution_report_head` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_execution_report_inbox` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_external_service_policy` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_hosted_profile` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_identity_alias` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_identity_legacy_apply_run` | 无 | 无 | AUDIT_PRESERVE | 保留迁移审计、原始租户证据及防篡改触发器；不重写历史 | 结构/引用索引；业务读写待核 |
| jia | `agent_identity_legacy_manifest` | 无 | 无 | AUDIT_PRESERVE | 保留迁移审计、原始租户证据及防篡改触发器；不重写历史 | 结构/引用索引；业务读写待核 |
| jia | `agent_identity_registry` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_outbox_event` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_persona` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia | `agent_persona_binding` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_persona_binding_bak_20260802_tenant_scope` | 有 | 有 | HISTORICAL_PRESERVE | 历史备份保留原结构，不当作活动业务表迁移 | 名称/结构；活动引用待核 |
| jia | `agent_personal_workspace_conversation_file_link` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_personal_workspace_conversation_link_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_personal_workspace_execution` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_personal_workspace_execution_input` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_personal_workspace_execution_output` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_personal_workspace_file` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_personal_workspace_file_version` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_personal_workspace_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_personal_workspace_task_file_link` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_personal_workspace_task_link_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_position_authority` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_position_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_position_state` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_runtime` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_runtime_deleted_backup_20260622` | 有 | 有 | HISTORICAL_PRESERVE | 历史备份保留原结构，不当作活动业务表迁移 | 名称/结构；活动引用待核 |
| jia | `agent_runtime_v1_installation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_scene_event` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_scene_phase_report` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_scene_state` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_scene_version` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_selected_output_finalization` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_skill_execution` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_artifact` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_artifact_outcome` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_artifact_outcome_decision` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_backfill_issue` | 有 | 有 | AUDIT_PRESERVE | 保留迁移审计、原始租户证据及防篡改触发器；不重写历史 | 结构/引用索引；业务读写待核 |
| jia | `agent_task_backfill_manifest` | 有 | 有 | AUDIT_PRESERVE | 保留迁移审计、原始租户证据及防篡改触发器；不重写历史 | 结构/引用索引；业务读写待核 |
| jia | `agent_task_backfill_manifest_batch` | 无 | 无 | AUDIT_PRESERVE | 保留迁移审计、原始租户证据及防篡改触发器；不重写历史 | 结构/引用索引；业务读写待核 |
| jia | `agent_task_backfill_run` | 无 | 无 | AUDIT_PRESERVE | 保留迁移审计、原始租户证据及防篡改触发器；不重写历史 | 结构/引用索引；业务读写待核 |
| jia | `agent_task_bounty_bootstrap_outbox` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_bounty_claim_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_bounty_quote` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_bounty_settlement` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_creation_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_event` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_execution_grant` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_formal_delivery` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_formal_delivery_item` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_funding` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_funding_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_historical_event_manifest` | 有 | 有 | AUDIT_PRESERVE | 保留迁移审计、原始租户证据及防篡改触发器；不重写历史 | 结构/引用索引；业务读写待核 |
| jia | `agent_task_historical_event_manifest_batch` | 无 | 无 | AUDIT_PRESERVE | 保留迁移审计、原始租户证据及防篡改触发器；不重写历史 | 结构/引用索引；业务读写待核 |
| jia | `agent_task_historical_event_run` | 无 | 无 | AUDIT_PRESERVE | 保留迁移审计、原始租户证据及防篡改触发器；不重写历史 | 结构/引用索引；业务读写待核 |
| jia | `agent_task_member` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_meta` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_note` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_provider_cost_consent` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_request` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_requirement_snapshot` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_thread` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_task_work_item` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `agent_work_item_reassignment` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `archive_bookmark` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `archive_chapter` | 无 | 无 | SHARED_METADATA_REVIEW | 当前无业务tenant列；可作共享定义/出版物候选，灰度写入和发布必须隔离 | 结构/引用索引；共享写策略待核 |
| jia | `archive_edition` | 无 | 无 | SHARED_METADATA_REVIEW | 当前无业务tenant列；可作共享定义/出版物候选，灰度写入和发布必须隔离 | 结构/引用索引；共享写策略待核 |
| jia | `archive_idempotency` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `archive_note` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `archive_paragraph` | 无 | 无 | SHARED_METADATA_REVIEW | 当前无业务tenant列；可作共享定义/出版物候选，灰度写入和发布必须隔离 | 结构/引用索引；共享写策略待核 |
| jia | `archive_reader_progress` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `archive_work` | 无 | 无 | SHARED_METADATA_REVIEW | 当前无业务tenant列；可作共享定义/出版物候选，灰度写入和发布必须隔离 | 结构/引用索引；共享写策略待核 |
| jia | `chat_bounty_binding` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_context_snapshot` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_conversation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_conversation_archive_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_conversation_asset` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_conversation_event` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_deliberation_schema_version` | 无 | 无 | SHARED_METADATA_REVIEW | 当前无业务tenant列；可作共享定义/出版物候选，灰度写入和发布必须隔离 | 结构/引用索引；共享写策略待核 |
| jia | `chat_dispatch_outbox` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_interaction_step` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_message` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_request` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_selected_output_finalization` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_selected_output_finalization_item` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_step_execution_link` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_task_delivery_review_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_turn` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_typed_admission` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_typed_outcome` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_typed_pending_question` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_typed_proposal` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `chat_typed_review_context` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `core_action` | 无 | 无 | SHARED_METADATA_REVIEW | 当前无业务tenant列；可作共享定义/出版物候选，灰度写入和发布必须隔离 | 结构/引用索引；共享写策略待核 |
| jia | `core_dict` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia | `core_log` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `core_notice` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `dialogue_template` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia | `dwz_record` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_account` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_entry` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_escrow` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_escrow_funding_lot` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_hosting_lease` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_hosting_provisioning_intent` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_hosting_rent_plan` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia | `economy_hosting_rent_quote` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_hosting_reprovision` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_actor_root` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_agent_version` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_change` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_change_command` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_credential_operation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_delivery_binding` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_entitlement` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_installation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_installation_authorization` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_managed_credential` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_managed_state` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_management_quote` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_management_request` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_management_result` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_order` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_order_receipt` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_product` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_product_version` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_purchase_quote` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_result_receipt` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_skill_upgrade_policy` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `economy_transaction` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `hall_case_execution` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `hall_private_case` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `hall_private_mark` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `hall_request_draft` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `isp_file` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `kefu_faq` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia | `kefu_message` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `kefu_msg_log` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `kefu_msg_subscribe` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `kefu_msg_type` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia | `mat_media` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `mat_news` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `mat_phrase` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `mat_phrase_vote` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `mat_pv_log` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `mat_tip` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `mat_vote` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `mat_vote_item` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `mat_vote_question` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `mat_vote_tick` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `oauth_action` | 无 | 无 | SHARED_METADATA_REVIEW | 当前无业务tenant列；可作共享定义/出版物候选，灰度写入和发布必须隔离 | 结构/引用索引；共享写策略待核 |
| jia | `oauth_api_key` | 有 | 有 | KEEP_CREDENTIAL_SCOPE | 保留tenant/client；业务执行凭据不可因OAuth客户端全局化而扩大权限 | 结构/源码引用；完整授权链待核 |
| jia | `oauth_client` | 有 | 有 | REMOVE_IDENTITY_SCOPE | 删除tenant_id；保留协议client_id；签发租户来源改为实例配置，保留客户端准入 | 已查直接代码依赖 |
| jia | `oauth_resource` | 无 | 无 | SHARED_METADATA_REVIEW | 当前无业务tenant列；可作共享定义/出版物候选，灰度写入和发布必须隔离 | 结构/引用索引；共享写策略待核 |
| jia | `point_gift` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `point_gift_usage` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `point_record` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `point_referral` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `point_sign` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `sms_buy` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia | `sms_code` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia | `sms_config` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia | `sms_message` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia | `sms_package` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia | `sms_reply` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia | `sms_send` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia | `sms_template` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia | `task_item` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `task_item_bak` | 有 | 有 | HISTORICAL_PRESERVE | 历史备份保留原结构，不当作活动业务表迁移 | 名称/结构；活动引用待核 |
| jia | `task_plan` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `user_auth` | 无 | 无 | AUTH_RELATION_REVIEW | 无tenant/client；需核对是否仍使用及角色/权限父表同域约束，不直接清理或加列 | 本轮主源码精确表名检索未见引用；非退役证明 |
| jia | `user_group` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia | `user_group_rel` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia | `user_info` | 有 | 有 | REMOVE_IDENTITY_SCOPE | 删除client_id/tenant_id；point等业务字段须另行解耦或维持灰度禁写；保留账号状态/auth_epoch | 已查直接代码依赖 |
| jia | `user_msg` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia | `user_org` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia | `user_org_rel` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia | `user_perms` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia | `user_perms_rel` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia | `user_role` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia | `user_role_rel` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia | `v_task_item` | 有 | 有 | VIEW_REVIEW | 保留；随底表过滤规则核对视图定义，不能以视图名绕隔离 | 结构已查；链路待核 |
| jia | `wx_daily_vote_message_receipt` | 无 | 无 | EXTERNAL_SCOPE_REVIEW | 现无tenant列；现有appid等外部作用域不能自动等同环境，回调/幂等/凭据需单独隔离 | 结构/引用索引；外部副作用待核 |
| jia | `wx_daily_vote_receipt` | 无 | 无 | EXTERNAL_SCOPE_REVIEW | 现无tenant列；现有appid等外部作用域不能自动等同环境，回调/幂等/凭据需单独隔离 | 结构/引用索引；外部副作用待核 |
| jia | `wx_mp_info` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia | `wx_mp_template` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia | `wx_mp_user` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia | `wx_pay_info` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia | `wx_pay_order` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia_dev | `act_ge_bytearray` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ge_property` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ge_schema_log` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_actinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_attachment` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_batch` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_caseactinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_caseinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_comment` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_dec_in` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_dec_out` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_decinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_detail` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_ext_task_log` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_identitylink` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_incident` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_job_log` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_op_log` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_procinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_taskinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_hi_varinst` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_id_group` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_id_info` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_id_membership` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_id_tenant` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_id_tenant_member` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_id_user` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_re_camformdef` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_re_case_def` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_re_decision_def` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_re_decision_req_def` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_re_deployment` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_re_procdef` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_authorization` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_batch` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_case_execution` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_case_sentry_part` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_event_subscr` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_execution` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_ext_task` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_filter` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_identitylink` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_incident` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_job` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_jobdef` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_meter_log` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_task` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_task_meter_log` | 无 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `act_ru_variable` | 有 | 无 | ENGINE_OWNED | 保留引擎结构；租户/执行器按引擎契约隔离，禁直接批量删TENANT_ID_ | 结构盘点；引擎运行配置待核 |
| jia_dev | `agent_persona` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia_dev | `agent_runtime` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `agent_task_meta` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `chat_conversation` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `chat_message` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `core_dict` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia_dev | `core_log` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `core_notice` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `dialogue_template` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia_dev | `dwz_record` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `isp_file` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `kefu_faq` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia_dev | `kefu_message` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `kefu_msg_log` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `kefu_msg_subscribe` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `kefu_msg_type` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia_dev | `mat_media` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `mat_news` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `mat_phrase` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `mat_phrase_vote` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `mat_pv_log` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `mat_tip` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `mat_vote` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `mat_vote_item` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `mat_vote_question` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `mat_vote_tick` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `oauth_api_key` | 有 | 有 | KEEP_CREDENTIAL_SCOPE | 保留tenant/client；业务执行凭据不可因OAuth客户端全局化而扩大权限 | 结构/源码引用；完整授权链待核 |
| jia_dev | `oauth_client` | 有 | 有 | REMOVE_IDENTITY_SCOPE | 删除tenant_id；保留协议client_id；签发租户来源改为实例配置，保留客户端准入 | 已查直接代码依赖 |
| jia_dev | `point_gift` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `point_gift_usage` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `point_record` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `point_referral` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `point_sign` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `sms_buy` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia_dev | `sms_code` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia_dev | `sms_config` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia_dev | `sms_message` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia_dev | `sms_package` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia_dev | `sms_reply` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia_dev | `sms_send` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia_dev | `sms_template` | 有 | 有 | CATALOG_REVIEW | 目录可共享不等于业务数据可共享；保留现列，区分公共只读定义与租户覆盖后再决定拆表 | 结构/引用索引；共享语义待核 |
| jia_dev | `task_item` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `task_plan` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `user_group` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia_dev | `user_group_rel` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia_dev | `user_info` | 有 | 有 | REMOVE_IDENTITY_SCOPE | 删除client_id/tenant_id；point等业务字段须另行解耦或维持灰度禁写；保留账号状态/auth_epoch | 已查直接代码依赖 |
| jia_dev | `user_msg` | 有 | 有 | KEEP_BUSINESS_SCOPE | 保留tenant；client先保留现有应用/授权语义；核对查询/唯一键/后台领取均同域，不因用户去client而删除业务client | 结构/引用索引；全调用链待核 |
| jia_dev | `user_org` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia_dev | `user_org_rel` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia_dev | `user_perms` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia_dev | `user_perms_rel` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia_dev | `user_role` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia_dev | `user_role_rel` | 有 | 有 | KEEP_BUSINESS_AUTH_SCOPE | 保留tenant/client；global user_id指向身份，关系及角色/组织权限按环境分区，JOIN须同域 | 结构及用户关联查询已查；完整授权待核 |
| jia_dev | `v_task_item` | 有 | 有 | VIEW_REVIEW | 保留；随底表过滤规则核对视图定义，不能以视图名绕隔离 | 结构已查；链路待核 |
| jia_dev | `wx_mp_info` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia_dev | `wx_mp_template` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia_dev | `wx_mp_user` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia_dev | `wx_pay_info` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |
| jia_dev | `wx_pay_order` | 有 | 有 | EXTERNAL_SCOPE_REVIEW | 保留tenant/client；外部appid/merchant/验证码及发送凭据另行隔离，禁止灰度真实扣费/发信 | 结构/引用索引；外部副作用待核 |

16:27 +08:00追加：远端develop为`de6776fb3092a3e71aa5004d115c1280b742f2aa`，与本表引用索引的a5f28ec1相比全部主源码无变化，仅测试fixture更新；本盘点主源码结论仍适用，未将旧测试结果视为新提交验证。

### 2026-10-29 20:51 +08:00 生产jia已执行的增量（其余库存仍为原观察基线）

生产运行源码`d8f9672f1ed24ef8cdc2796773259f98feed5c41` / Flow5260799/380：
- `user_info`已删除client_id、tenant_id、point，保留全局身份、安全状态及原用户记录。
- `oauth_client`已删除tenant_id，保留OAuth协议client_id；生产签发准入由配置清单确定。
- `point_account`已创建，按(tenant_id,jiacn)隔离余额；310有效身份导入逐行核对一致，1条无jiacn历史记录按用户要求跳过。
- `user_business_membership`已创建并迁入311条原成员归属；成员关系不授予权限，也不等同全权限域已灰度化。
- `point_sign`、`point_referral`已增加tenant+用户/推荐人资格查询索引。其他业务/权限表scope继续保留，外部副作用和完整灰度路由未放开。

上述只适用于已核验生产jia。本表其他数据库（包括jia_dev）没有据此执行DDL，也不因主库上线更新成“已完成”。生产健康、PKCE登录及积分读取验证通过；详见同目录主handoff的20:51收口和私有release-binding证据。
