# U2 原生生图单次 Provider START：融合分支证据（2026-09-29）

API `jia` 的融合分支已快进到 `9d9cdf2ef90074989ac78ad514db450091f26809`（tree `0bb2971d3f10d183a89fb86926b6e0a6f7023751`），并推送远端；本 SDD 更新相同 gitlink。Provider 开始前在服务端任务根/grant/execution 锁下核验当前租约、精确资料版本、授权，原子持久化一次 `conversation_provider_started_at` 与租约版本。已 START 的执行不能重新领取/重复 START；响应丢失必须按未知结果对账，不许自动再次付费。新的 MySQL `v1_16` 增量迁移为单个 `ALTER TABLE`，部分列或缺少有效 CHECK 将禁止启动。`mmdU2ConversationOutput` exact-tree 定向 **49/49 PASS**（4 schema、22 service、23 runtime/security），日志 `evidence/u2-references/gradle-provider-start-9d9cdf2e.log`。**尚无隔离 MySQL 新/旧库实际升级回归；这不是生产迁移或付款许可。**

Client 独立候选 `codex/juyiting-mmd-native-image-executor` 现为 `03214a1c71ee61dd45c5fe23d9e4bd03fd45a9a9`（tree `50a413ea4a6dd3076b9e501d5929ed47baf02e6c`），在已确认原生输入、存在执行器、尚有效租约时，向上述精确 endpoint 提交 fenced `POST /internal/agent/tasks/{taskId}/runs/{runId}/conversation/provider-start`。只有收到严格 `{started:true}` 成功响应才调用内置 imagegen；未知/格式不符/错误响应均停止且不报告虚假失败，不自动重试。定向测试 13/13，全目录 Node 测试 **417/417 PASS**（本地复用另一隔离工作树已有依赖，无生产构建或付费调用）；客户端候选**仍未合入主融合分支**，必须先与参考图受控下载 Owner 的独立候选合并、对齐输入合同并在组合树重验。原文 `costAuthorizationRef(null)` 仍不授权收费，显式环境开关默认关闭。

下一步：隔离 MySQL 升级测试、客户端参考图物化合同合并及安全回归、成本授权/预算事实和收费 Provider 的人工确认；会话 `part.ready`、归档/正式交付、浏览器预览下载验收依旧未完成。**未合入 develop、未发布、未达到画鸟可验收。**
