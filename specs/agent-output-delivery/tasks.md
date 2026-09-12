# 可执行任务清单 v1.1

实施状态：OD00～OD05 已通过开发门槛与独立评审，OD06 正在补齐客户端保留清理及 R1 集成；逐项状态以 [task-ledger.yaml](task-ledger.yaml) 为准。每项只有一个写入者，验证后独立只读评审。用户已授权持续推进 OD00～OD11，无需重复确认常规实施；发布仍须满足实际发布门槛。流程与命令见 [execution-plan.md](execution-plan.md)，技术契约见 [detailed-design.md](detailed-design.md)。

| ID | 版本 | 工作项与文件责任 | 写入角色 → 只读评审 | 人日 | 解锁条件/验收 |
| --- | --- | --- | --- | --- | --- |
| OD00 | R1 | **契约与真实依赖核对**；api/web/client部署和版本记录 | main_orchestrator → architect | 0.5～0.5 | 事务/存储/扫描器/run证据，契约冲突清零；O26 |
| OD01 | R1 | **来源归属、run绑定和WS ticket交换**；agent output身份；chat relay/owner DAO/WS | critical_worker → adversarial_reviewer | 1～1.5 | 错误owner、tenant=0、过期binding拒绝，ticket不入聊天；O07,O09,O23,O26 |
| OD02 | R1 | **字节对象、配额、上传校验和GC**；agent-api/core/mapper/service output存储与M001 | critical_worker → adversarial_reviewer | 1～1.5 | 真实字节上传/校验；epoch隔离、配额CAS、GC负向；O10,O11,O12,O20,O25,O27,O28 |
| OD03 | R1 | **任务/对话成果发布、列表和鉴权下载**；agent artifact M002；chat_output；精确ACL与代理读 | critical_worker → adversarial_reviewer | 1～1.5 | OWNER_SHARE显式；private隔离；离线取件hash一致；O03,O06,O07,O08,O09,O19,O29 |
| OD04 | R1 | **客户端manifest、安全快照、持久恢复**；isp-install/conf/codex-ws-agent/output-*.mjs及执行finish | critical_worker → adversarial_reviewer | 1.5～2 | 两个执行模式；manifest指定代码包取件；重启继续已有快照，不重跑模型；O01,O02,O04,O10,O22,O30 |
| OD05 | R1 | **共用成果UI与两个入口**；web/components/outputs与chat/bounty/workspace、useOutputs | balanced_worker → adversarial_reviewer | 1～1.5 | 用户切换/source切换不串数据；下载、分页、过期提示；O01,O05,O06,O08,O21 |
| OD06 | R1 | **R1集成、发布候选和演示**；串行保留清理/API合并与构建修复、独立验证、root证据 | main_orchestrator → release_guard | 1～1.5 | API/Web/client版本及R1矩阵通过，等待发布授权；R1_GATE |
| OD07 | R2 | **HTTP租约和policy1全部入口禁入**；agent lease/assign/legacy/aggregation与client心跳 | critical_worker → adversarial_reviewer | 1～1.5 | claim/start/heartbeat/release可用；单工作项/旧路径硬限制；O13,O16,O22,O24,O31 |
| OD08 | R2 | **唯一正式提交事务**；agent task_delivery M003/TaskDeliverySubmissionService | critical_worker → adversarial_reviewer | 1.5～2 | 固定版本、delivery pin、submitted CAS和事件同事务；O14,O15,O16,O17,O24,O25 |
| OD09 | R2 | **人工验收、要求修改和显式返工派发**；agent review/rework/aggregation与client新run接入 | critical_worker → adversarial_reviewer | 1～2 | submitted->ready返工；新run/lease；重复/旧批次拒绝；O17,O18,O20,O32,O33 |
| OD10 | R2 | **交付要求与验收UI**；web榜文表单、批次/审核/重新执行面板 | balanced_worker → adversarial_reviewer | 0.75～1 | 409与结果未知恢复；展示确切批次及审核者权限；O13,O14,O15,O17,O18,O33 |
| OD11 | R2 | **R2事务和三仓集成验收**；只读验证；root证据和候选三仓版本 | main_orchestrator → release_guard | 0.75～1 | R2矩阵/负向路径/迁移/开关和演示证据齐备；R2_GATE |

R1合计7～10人日，R2追加5～7.5人日，工程总计12～17.5人日（对外按12～18），另留2～3人日缓冲。各项估计包含常规验证与评审；外部等待不计为人日。

## 每项开工清单

- [ ] 上游任务验收与只读评审完成，基线/分支/任务责任明确。
- [ ] 读取OpenAPI/schema/fixture本版本，列出相关失败场景。
- [ ] 实现、针对性验证、评审、原写入者修复；不还原无关改动。
- [ ] 提交具体commit、测试结果、风险和演示供审阅；独立评审通过后更新任务状态并继续已授权任务。

## 特别责任边界

冻结 OpenAPI 共 21 个 HTTP operation，按下面的责任分配验收，避免只接写接口而遗漏查询/能力入口；这张表表示任务范围，不表示已实现。

| 任务 | operation 数 | 接口责任 |
| --- | ---: | --- |
| OD02 | 4 | createUpload、putUploadBytes、completeUpload、getUpload |
| OD03 | 11 | getOutputCapabilities；task/chat 各自的 publish、list、listVersions、getVersion、downloadVersion |
| OD07 | 2 | mutateWorkLease、getWorkLease |
| OD08 | 2 | submitDelivery、listDeliveries |
| OD09 | 2 | reviewDelivery、dispatchRework |

- OD06 已知前置修复按 [串行集成交接](evidence/OD06/serial-integration-handoff.md) 分别由唯一 critical_worker 实施并独立评审，再执行集成验证。
- main_orchestrator仅写root计划/证据/集成控制文件；OD00/OD06/OD11如需执行验证由test_runner承担单一验证子任务，发布门槛由release_guard判定。
- P0代码、迁移、权限、租约与并发由critical_worker写；balanced_worker仅在冻结契约后负责普通Vue/接口接线。
- Client独立仓为 `/home/chc/wsps/isp-install`；不把其源码复制进root，不由root的API/Web gitlink代替client版本记录。
- 业务类放置与未来文件名单见详细设计第3节；不新增agent→chat依赖或跨库伪事务。
- 每条Gradle命令必须持 `/tmp/cyf-gradle.lock`；Web实现按用户AGENTS完成build。文档阶段不跑业务构建。

## 延后项（不阻塞R1/R2）

- [ ] P3-01：受限工作空间目录浏览与历史文件补交UI。
- [ ] P3-02：多工作项/多Agent正式交付、联合批次和部分验收。
- [ ] P3-03：分片大文件、批量ZIP、签名直传、更多安全预览。
- [ ] P3-04：Agent跨来源成果聚合页、原生微信下载桥接。
- [ ] P3-05：审计真实资金后端后制定验收结算/费用/争议契约。
- [ ] P3-06：按实际需要增加WS artifact.publish/work.result适配；必须委托已有唯一应用事务。

未列为本轮的增强工作不因名称相近被默认混入任务。若需求新增，更新契约和关键路径再估算。

OD00状态`accepted_for_development`表示本地开发证据和独立评审通过，仅解锁OD01；它不是生产验收完成。延后门槛及责任阶段见[evidence/OD00/downstream-gates.md](evidence/OD00/downstream-gates.md)。
