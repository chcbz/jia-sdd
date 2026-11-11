# 聚义厅必做详设：最新统一Runtime直接部署与新任务验收

- 修订日期：2026-10-09，Asia/Shanghai；本轮20:20核对本地Runtime/API基线。
- **当前范围以本版为准**：2.0.0前不做版本兼容；不把运行安全专项或历史流程打通作为开发、部署及验收门槛；最新版本的新功能能用即可。
- 当前交付状态（2026-10-09 23:16生产复验）：统一Runtime已部署；吴用435、林冲436新任务已完成。刷新后验收误提示已通过Web 1.14.1修复上线并复验。卢俊义属于另一个账号，本账号未验收，不属于绑定故障。下文设计及“未部署”候选描述保留为实施前历史基线，以本节交付摘要为准。
- 唯一目标：吴用、林冲、卢俊义由一个最新Runtime运行；用部署后新建的任务验证议事、执行和成果交付。原事项432及其他历史任务不属于验收对象。
- 接续现有UR06；本文N1～N3是工作切片，不新增任务ledger、Owner层级或Reviewer。原Runtime Owner处理真实源码缺口，Main部署及实测。

## 当前交付摘要（2026-10-09）

- Runtime部署版本：commit `2ce6fedf34832048e248fde3e07222f5ed867b7a`，tree `1d610486cbbe14ff410ee85e6ba1ee6e7c8e6163`；统一入口 `cyf-agent-runtime-v1@unified.service`。本次Web修复未改动或重启Runtime/API，未执行DDL。
- Web：`1.14.1`，commit `17ecf1c0b581cab1456acff4db097a6a4d335e3d`，tree `101daa30ed9658949dcc9b1d4cccfb2e4d2ce539`，Flow `4403172 / 193` SUCCESS。364个安装文件与同批制品匹配，11个公开HTTP资源摘要匹配；流水线已恢复原验证配置。
- 根因及修复：刷新保留验收intent而丢失内存receipt，原实现不自动查询回执，把未知状态误写成未完成。现在恢复合法intent后仅GET原回执，按服务端状态展示；账号/任务切换取消旧查询，不自动重发验收。
- 实测：435、436刷新/重新打开正式成果，均显示正确正文和“验收完成”；本次复验6次验收回执GET、0次验收POST，响应均为 `completed / accepted / completed`。本地定向89通过；同批Flow Mocha 2818通过、2 pending、0失败。
- 范围边界：不据此宣称卢俊义所属账号已验收，也不宣称所有历史任务已打通；公孙胜原托管入口停用后的offline未在本次恢复。
- 证据：`/var/tmp/cyf-ur06-finalization-fix-20261009/release-summary.json`、`browser-acceptance.json`；现有handoff `evidence/unified-agent-runtime-20261008/production-readback-20261009/main-handoff.json#ur06FinalizationRefreshFix`。

## 1. 实施前冻结的三项范围（以下为历史设计）

| 切片 | 必做内容 | 实施类型 | 完成标准 |
|---|---|---|---|
| N1 | 准备最新统一Runtime制品和三角色配置 | 复用已有实现，配置/部署准备 | 三角色使用最新manifest、各自身份与执行器配置，共用一个Runtime入口 |
| N2 | 直接停止本次替换范围内旧入口，启用唯一新Runtime | 直接部署，不开发切流系统 | 三角色都通过新认证、注册和实际能力检查；不再运行旧入口 |
| N3 | 生产新建任务，验证新流程 | 真实功能验收；有具体功能断点才修代码 | 新任务正常进入议事，按正常操作执行，产生可查看的成果 |

**目前没有证据要求先完成某项新增代码，才能开始N1。** 核对过的session、WS、统一host、安装器及现有业务链均已有实现。不能为满足“必须编码”而另造功能。

### 1.1 明确移出必做范围

- 旧版本兼容、旧认证fallback、双轨、灰度、逐角色试切、旧Runtime回退。
- 运行安全专项：无停机切换、在途排空方案、故障注入、强制恢复演练、额外监控/回滚系统、跨版本状态迁移框架。
- 历史任务续跑、历史成果补报、旧ACK/旧checkpoint迁移、事项432或411的闭环验收。
- MQ接线、付费托管恢复、F01全量适配、文件跨重启恢复、旧health脚本、telemetry、E13旧提案及PhaseA历史扩列。
- 上一版R1的“一个Agent注册等待影响其他Agent心跳”修复：保留已知缺陷记录，**不再作为正常新任务可用的预置门槛**；若实际新任务因此不可用，再修这个明确断点。

上版详细诊断、代码建议与历史证据保存在本文同级的证据目录，不再作为本轮派单清单。只核销新功能，不宣称完成异常恢复、多Agent故障隔离或历史业务修复。

### 1.2 不增加工作，也不删掉现有功能校验

不新增安全加固任务，不为缩小范围去改掉已有鉴权、身份校验、事务、幂等或安装器约束。它们已是当前代码的一部分，正常使用即可。

“不验历史”不等于执行清库、清队列、删除凭据、把历史任务改成功或伪装成未执行。本文没有这些操作，也没有自动扩大到其他聊天进程的处置。若已有历史数据阻塞新入口，报告具体数据和现有代码的拒绝原因；不要默默扩建历史恢复系统或擅自清除数据。

## 2. 固定源码、代码行号及是否需要修改

### 2026-10-09 清理后候选补充

**最新候选覆盖下述清理基线**：按用户明确要求取消Runtime的Node版本限制，commit `b70de3dbf77ef0600376cd65c067b9546efca81d`，tree `e33b1e5e580e9cfd916b565609c0b97760c93a72`，已推送develop。Node22.19.0下受影响回归119项通过、1项既有skip；记录实际版本，不据此保证任意版本可运行。未部署。证据：`docs/implementation/evidence/runtime-required-closeout-20261009/node-unpin-result.json`。

已完成本轮停用入口/一次性工具源码清理并推送Runtime develop：`4cc61829534ba2cdaabdad594c811a486298097d`，tree `f0a5d4035807fa3294115d4f0d49cb45ef1451cb`；403测试通过、0失败、1个既有跨端skip，未部署。N1应绑定此候选或明确核对后的更新候选。下表保留20:20原基线作为来源；除下面已更新的agent-client位置外，其余行号仍按原基线，不将历史版本冒称当前线上。详细清理范围见 `docs/implementation/evidence/runtime-required-closeout-20261009/legacy-cleanup-result.md`。

| 组件 | 基线 | 结论 |
|---|---|---|
| Runtime | `/home/isp/wsps/chcbz/isp-install`，commit `5489c0e946114ec601e246a4eb93a0bff3b57c24`，tree `66424e5e9063f316869b00c952a3859625ece77f` | 本轮核对HEAD未变，优先交付现成实现 |
| API | `/home/isp/wsps/cyf/api`，commit `1e9111028fbdff1ae5452f64aec843e85e81ad59`，tree `0416b722d735c58af4653892b6ee269e8f9d1498` | 已有新Runtime认证和任务业务契约，默认不改 |
| Web | 上轮已核发布commit `c6ae76010c43153659cc6d55c902a1765c620932`、Flow4403172/Run186 | 历史发布证据；本轮未重新核当前线上或远端，不能称其是最新Web |

实施前核对实际候选，若相关函数已变化按diff接续，不覆盖其他改动。本轮没有重新查远端，不将本地HEAD冒称远端最新。

| 代码入口 | 精确位置 | 当前动作 |
|---|---|---|
| CLI：validate/enroll/run、单host生命周期 | [agent-runtime.mjs:38–85](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/agent-runtime.mjs#L38) | 直接复用，不新增入口 |
| host/多subject配置及subjectKey | [manifest.mjs:44–46,69–131](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/manifest.mjs#L44) | 生成符合现有schema的配置，不改schema |
| session与WS proof | [runtime-client.mjs:37–59,169–185](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/runtime-client.mjs#L37) | 复用现有新认证，不给旧sidecar补兼容 |
| 注册与能力声明 | [execution-adapter.mjs:39–100](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs#L39) | 以真实回执为准，不手写READY |
| 真正执行器启动 | [agent-client.mjs:6128–6185](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L6128) | 提供受支持CLI、独立HOME和原功能配置 |
| 实际任务/聊天能力 | [agent-client.mjs:6464–6496](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L6464) | 核正常新任务所需能力，不做异常恢复专项 |
| 安装器 | [install.sh:5–61](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/install.sh#L5) | 复用完整制品入口，不另写发布脚本 |

## 3. N1：配置字段、接口和数据库契约

### 3.1 单Runtime配置

目标配置文件：`/etc/cyf-agent-runtime-v1/unified.host.json`。顶层只允许以下四字段：

```json
{
  "configVersion": 1,
  "hostId": "<本机持久hostId>",
  "stateRoot": "/home/isp/state/cyf-agent-runtime-v1/unified/host",
  "agents": [
    {
      "manifestPath": "<吴用manifest绝对路径>",
      "profilePath": "<吴用profile绝对路径>",
      "stateRoot": "<吴用state绝对路径>"
    },
    {
      "manifestPath": "<林冲manifest绝对路径>",
      "profilePath": "<林冲profile绝对路径>",
      "stateRoot": "<林冲state绝对路径>"
    },
    {
      "manifestPath": "<卢俊义manifest绝对路径>",
      "profilePath": "<卢俊义profile绝对路径>",
      "stateRoot": "<卢俊义state绝对路径>"
    }
  ]
}
```

以上是字段模板，替换所有占位符后才能运行，不能把昵称作为canonicalAgentId。

| 对象 | 必填字段/现有规则 |
|---|---|
| manifest | `runtimeProtocolVersion="v1",manifestVersion,installationId,tenantId,clientId,canonicalAgentId,manifestSha256`；摘要使用原digestManifest |
| profile | `profileId,agentId,codexBin,codexHome,codexWorkdir`；agentId等于manifest.canonicalAgentId；不放旧API key |
| 议事相关配置 | 原`appServerEnabled/fastChatEnabled/chatEngine/typedDeliberationEnabled`与实际app-server能力对应；不能只开布尔值就算功能可用 |
| installation授权文件 | `<agent.stateRoot>/runtime-authorization.json`；`installationId,runtimeAuthorization`；复用有效授权，不重复消费enrollment secret |
| host/boot | hostId持久；runtimeInstanceId由原CLI每次启动生成；三角色共用host/boot、各自有独立session |
| 进程环境文件 | `/etc/cyf-agent-runtime-v1/unified.conf`；原`CYF_RUNTIME_V1_API_BASE_URL`及需要的`CYF_RUNTIME_WORKSPACE_POLICIES_FILE` |

原配置解析器会检查路径、目录和文件属性，按现有要求准备即可，不改检查逻辑。历史状态格式不在本轮兼容范围；同一已执行主体不能用清空账本伪装全新主体。使用当前代码可直接接受的配置/状态，若不能接受，明确实际输入缺口，不自动开发历史迁移功能。

原CLI未从任意环境变量加载 `providerEnvironments` 映射，不能把凭据塞进unified.conf就假称子进程可用。采用已有独立Codex HOME和受支持的Provider配置，是否可用由真实新任务验证。

### 3.2 认证请求/响应：直接按最新契约

```text
POST /agent/runtime/v1/session
Authorization: Bearer <该installation的授权>
Content-Type: application/json
body字符串字段：
installationId, tenantId, clientId, canonicalAgentId,
manifestVersion, manifestSha256, hostId, runtimeInstanceId
```

原`identityOf()`负责去掉本地manifest摘要的`sha256:`前缀。响应`JsonResult.data`字段：
`installationId,tenantId,clientId,canonicalAgentId,hostId,runtimeInstanceId,sessionGeneration,scheme,sessionToken,websocketPath,status`。

期望scheme=`AgentRuntime`、status=`CHANNEL_PENDING`、websocketPath=`/ws/agent/channel`；sessionGeneration为正整数。随后原client用sessionToken及五个`X-Agent-*`身份头连接WS，由原注册链确认实际能力。不要把CHANNEL_PENDING当READY。

API已有实现：[AgentRuntimeAuthenticationService.java:53–104](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/security/AgentRuntimeAuthenticationService.java#L53)、[AgentRuntimeV1Controller.java:75–81](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentRuntimeV1Controller.java#L75)。400先查请求字段，401/403查真实身份与授权；默认不修改后端认证。

### 3.3 表字段：本轮不新增DDL、不处理历史记录

| 表 | 新流程使用的既有字段 | 如何产生/更新 |
|---|---|---|
| `agent_runtime_v1_installation` | `installation_id,canonical_agent_id,manifest_version,manifest_sha256,tenant_id,client_id,status,runtime_authorization_hash` | 原安装授权服务；有效installation用于新session，不手工改hash |
| `agent_runtime` | `agent_id,tenant_id,client_id,owner_jiacn,binding_id,runtime_installation_id,runtime_host_id,runtime_instance_id,runtime_session_generation,token_hash,status,last_seen_at` | 原session/注册/心跳服务；不SQL写online |
| `agent_task_bounty_bootstrap_outbox` | `bootstrap_id,task_id,target_agent_id,source_business_action_id,requirement_revision,assignment_revision,permitted_operation,status,attempt_count,version,admitted_conversation_id,admitted_request_id,last_error_code` | 新任务/指派动作生成原outbox；原relay完成入会话，不重用旧任务ID |

类型与现有约束来源：[installation SQL](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-runtime-v1-schema.sql)、[runtime schema:25–51](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/schema.sql#L25)、[fence字段SQL](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-runtime-session-fence-v1.sql)、[bootstrap SQL](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-task-bounty-bootstrap-outbox-v1.sql)。这些仅供开发定位，不是待重跑的迁移清单。

## 4. N2：直接部署，不开发运行安全专项

执行顺序固定为：**准备新制品/配置 → 停止替换范围内旧入口 → 安装并启动唯一新Runtime → 验证新任务**。允许短暂不可用，不做灰度或无停机方案。

1. 沿原installer生成完整新制品，使用其已有`--target/--node/--npm/--python/--engine-root`参数；目标目录必须符合原安装器规则，不为复用旧目录改掉安装器限制。
2. Node不设置项目版本限制；原installer将实际打入制品的版本写入`runtime/node-version.txt`及日志，发布记录引用该实际版本和Node二进制摘要。JS依赖和私有Python工具链沿现成安装过程，不改第三方依赖要求；不新增验收框架、备用installer或宿主包替代方案。
3. 目标实例为`cyf-agent-runtime-v1@unified.service`，配置为§3.1；使用原[unit模板](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/systemd/cyf-agent-runtime-v1@.service)。
4. 旧吴用WS/sidecar及本次范围内的共享旧入口直接退出运行，不保留旧协议服务作备用。共享unit若还含其他聊天主体，只明确一次停机的影响对象，不据此开发逐profile安全切流系统；本文不扩大这些主体的数据删除或任务取消权限。
5. 原`validate.sh --root <artifact> --config <config>`及新Runtime启动后，核三个subject的session、WS和所需能力。新认证失败修新配置/新候选，不恢复旧API key。
6. API/Web没改就不为Runtime部署重发；确需API修复时走项目本地构建发布，Web修复走Flow4403172，不改变项目构建分工。

不安排：历史在途排空、旧格式全量迁移、故障演练、额外备份/回滚开发、共享进程热重载开发、持续监控框架。原工具自带的行为按原实现执行，不另加工作，也不为了删除已有检查而改代码。

## 5. N3：只验部署后新建流程

### 5.1 验收用例

| 用例 | 操作 | 判定 |
|---|---|---|
| NEW-01 三角色可用 | 新Runtime正常启动，读取实际注册/能力 | 三角色同一host/boot，分别有合法session，功能所需能力实际可用；不是只有进程active |
| NEW-02 新任务议事 | 正常登录，新建一个带本轮标记的测试任务，按原界面选择Agent并发起议事 | 记录新taskId和bootstrapId；新bootstrap ADMITTED，产生关联会话/请求，Agent真实回复 |
| NEW-03 新任务执行 | 对同一新任务按原产品流程明确执行 | 正常产生执行记录和结果，不绕过产品原有执行确认 |
| NEW-04 新成果查看 | 查看正式成果/文件内容，再刷新页面 | 内容可查看、必要时可下载，刷新后仍可读取；不能仅凭列表200判成功 |
| NEW-05 其他角色 | 用原界面选择另外角色进行新的简短议事；涉及协作则按现有功能操作 | 新任务可由选中角色处理；不强制构造故障/撤销/跨重启场景 |

测试任务使用新ID，不续原432，不使用旧bootstrap，不为验收重放历史命令。测试输入选择不含秘密、无真实付款或外部发布副作用的简短内容；费用与正式验收动作沿原授权，不新增业务功能。

### 5.2 注意议事、执行与成果不是同一个状态

[ChatBountyBootstrapAdmissionService.java:128–153](/home/isp/wsps/cyf/api/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyBootstrapAdmissionService.java#L128) 中`DELIBERATE`只是typed DISCUSSION，不自动授予执行权限。因此NEW-02通过不等于NEW-03/04通过；尚未执行时正式成果为空，不直接判代码缺陷。

成果查询沿已有接口：`GET /agent/tasks/{newTaskId}/formal-deliveries`、`GET /agent/tasks/{newTaskId}/deliverables`。源码：[AgentTaskFormalDeliveryController.java:93–142](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskFormalDeliveryController.java#L93)、[AgentTaskDeliverableController.java:65–103](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskDeliverableController.java#L65)。不新建表、不新增按钮。

### 5.3 只修阻塞新功能的最早断点

| 实际断点 | 精确接点 | 最小实施方向 |
|---|---|---|
| session失败 | runtime-client.mjs:169–177；API认证服务:53–104 | 先对齐8字段/installation授权；无证据不改认证代码 |
| 无注册/能力不可用 | execution-adapter.mjs:39–100；agent-client.mjs:6128–6185 | 修具体配置或实际执行器接线，不伪造READY |
| 新bootstrap等待 | [ChatBountyBootstrapRelay.java:84–135](/home/isp/wsps/cyf/api/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyBootstrapRelay.java#L84) | 核新任务目标的实际能力与原relay状态；不手工设ADMITTED |
| 新任务上下文请求确实被拒 | runtime-client.mjs:202–216 | 只有该断点实际出现，才按完整缺口详设补相应最小路径适配，不开放全部接口 |
| 新成果未生成 | 原执行记录、上述成果controller、当前report入口 | 先确认执行已授权/已运行，再修缺失提交，不做历史补报工程 |
| 一角色注册等待确实阻塞新功能 | agent-runtime.mjs:45–56 | 采用上版已定位的心跳屏障修复；届时补该函数和对应测试，不因此加入全套可靠性专项 |

实施时沿具体函数和原测试增加最小回归，记录新源码commit/tree。没有新功能失败证据就不动源码；不把历史失败记录重新变成当前开发任务。

## 6. 交付与验收结束条件

- N1由Main/原Runtime Owner准备现成制品与配置；有源码缺口才由唯一Owner实施。
- N2直接部署，不等待历史任务完成，不以旧格式支持或运行安全专项完成为前置条件。
- N3直接在生产用新任务验收；每项记录实际新ID、功能结果与失败位置，不新增框架/长期台账。
- 新Runtime三角色可用，NEW-02～04通过且其他角色正常新请求可用，即可核销本轮新功能交付。
- 结论仅写“新功能可用”；不声称历史流程已恢复、历史数据已迁移、可靠性缺陷已修复或整个UR05已全部完成。
- 本文修订本身不等于已编码、已部署或已验收。本轮未运行新的功能测试或生产操作。
