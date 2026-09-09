# Agent 工作空间产物与悬赏交付：可行性分析

状态：Draft，可评审方案，尚未实施。分析日期：2026-09-09。

## 结论

可行，建议建设统一的产物服务，同时服务于「与 Agent 对话」和「悬赏任务交付」。已有任务成果、版本、哈希、工作项提交事务、工作台快照和事件机制可复用；缺口横跨 Agent 客户端、后端存储与协议、用户权限、前端取件和业务验收，不能仅通过增加下载按钮解决。

推荐第一期打通：指定产物 → 安全采集 → 私有存储 → 正式登记 → 用户预览/下载 → 悬赏提交与验收。随后补齐目录浏览、历史补交和大文件能力。交付文件上传后，即使 Agent 离线或原工作空间归档，用户仍可在保留期内取件。

总体约束见 [design.md](design.md)，已细化的v1.1契约见 [detailed-design.md](detailed-design.md)，逐步实施和提效计划见 [execution-plan.md](execution-plan.md)，任务见 [tasks.md](tasks.md)，验收见 [acceptance.md](acceptance.md)。本文与设计中的新增接口、状态、默认参数均为建议，不代表当前已有能力。

## 1. 核查范围与证据边界

本次为源码静态分析，未访问生产数据库、未验证线上 feature flag、未实际执行远端 Agent 或下载测试。核查基线：

| 仓库 | 本地位置 | HEAD |
| --- | --- | --- |
| 协调仓 | `/home/chc/wsps/cyf` | `bda6f44` |
| API | `api/` | `492adc7e` |
| Web | `web/` | `77666e8` |
| Agent 客户端 | `/home/chc/wsps/isp-install/conf/codex-ws-agent/` | 安装仓 `a100a50` |

客户端属于独立的 `isp-install` 仓库，不在当前协调仓的两个 submodule 中。实施和发布必须记录三个实现仓版本。历史文档中的 `/home/isp/wsps/chcbz/isp-install` 在当前机器不存在，以上表实际路径为准。

## 2. 当前链路与具体断点

| 环节 | 源码事实 | 对用户的影响 |
| --- | --- | --- |
| 本地执行 | 客户端 `agent-client.mjs` 的 `runCodex` 调用 CLI，使用 profile 目录或受策略管理的任务 workspace | 文件留在执行机器，浏览器无法直接读取其路径 |
| 完成回报 | `finish` 从 CLI 文本提取 `replyContent`，聊天发最终消息，命令发 `task.report`/`codex.result`，带 `output`、`workspacePath` | 当前执行函数未采集并上传实际文件；运行成功不证明文件已交付 |
| 旧版任务接收 | `AgentWebSocketHandler.reportTask` 只向 DTO 填入 Agent、状态、标题、失败原因；`AgentServiceImpl.reportTask` 按兼容链路推进状态 | 该入口没有把 `output`、`workspacePath` 持久化成正式成果 |
| 新版协议 | `artifact.publish`、非 legacy `work.result` 转到 `sendDeferredProtocolHandler`，返回 `PROTOCOL_HANDLER_NOT_AVAILABLE` | 有消息名称和服务接口，还没有接通这一入站处理链路 |
| 租约传输 | 同一处理器的 `work.progress/work.heartbeat` 也转到 deferred；已有 `AgentWorkItemLeaseService` 领域接口 | 新悬赏提交依赖可用的领取/开工/续租链路，需要一起打通最小闭环，不能只接收最终结果 |
| 任务成果领域 | `AgentTaskCollaborationServiceImpl` 已实现发布、查询和版本列表；`agent_task_artifact` 有正文、URI、SHA-256、版本及可见性 | 可复用领域基础，不能据此认定文件传输、HTTP 取件已经可用 |
| 外部资源校验 | 内联正文最大 256 KiB，验证真实哈希；外部 URI 只检查协议/格式、声明哈希及可选长度 | 一个合格的 URI 字符串不能证明远端对象存在、可读、内容正确或能长期保留 |
| 工作项提交 | `AgentWorkItemResultCommitServiceImpl` 在租约/version 校验后发布一个成果并进入 `submitted` | 可作为正式提交基础；现有结果只记录 `resultArtifactId`，需要冻结确切版本及多文件集合 |
| 工作台读取 | workspace DTO 的成果只投影 ID、标题、类型、版本、生产者等，不返回内容或存储 URI | 前端现有「最近成果」只能展示摘要；还受前后端开关控制 |
| 用户界面 | `TaskWorkspacePanel.vue` 无预览/下载操作；`BountyPanel.vue` 主要提供点将、议事和资金预览；聊天主要渲染 Markdown | 缺少用户可操作的交付入口、附件卡片和正式验收视图 |
| 权限 | workspace 从 JWT 的 `jiacn/client_id` 获取 scope，再校验显式 `actorAgentId` 是己方 Agent 且为任务成员 | 这是 Agent 协作视角，需要增加用户作为会话所有者/任务发布者的产物读取和验收视角 |
| 通用文件服务 | ISP 有 `/file/res/...`，按本地文件 URI 读取字节 | 该 Controller 未体现任务/会话成果 ACL、上传会话、版本和私有对象签名，不宜直接充当新交付入口 |
| 资金悬赏 | Web 有 capability 控制的资金预览、报价/结算请求；当前 API checkout 未找到对应资金榜业务 Controller/Service | 不能声称当前线上已具备或缺少某种扣款行为；资金联动需核对实际后端基线 |

主要证据落点：

- [Agent 接收处理器](../../api/chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentWebSocketHandler.java)：`handleTextMessage`、`sendDeferredProtocolHandler`、`reportTask`、`saveAgentMessage`。
- [任务成果服务](../../api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskCollaborationServiceImpl.java)：`publishLocked`、`validateArtifactPayload`、`canReadArtifact`。
- [工作项结果事务](../../api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentWorkItemResultCommitServiceImpl.java)：`commit`。
- [工作台服务](../../api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskWorkspaceServiceImpl.java)：`authorizeRows`、`artifactDtos`。
- [任务工作台](../../web/src/components/juyiting/TaskWorkspacePanel.vue)、[悬赏榜](../../web/src/components/juyiting/BountyPanel.vue)、[聊天展示](../../web/src/components/juyiting/ChatPanel.vue)。

## 3. 用户真正需要得到什么

| 场景 | 目标体验 | 交付内容 |
| --- | --- | --- |
| 对话生成报告 | 回复出现「报告.pdf」，可预览、下载、查看版本 | 文件、摘要、生成来源 |
| 对话生成代码 | 可查看修改说明并下载补丁/代码包 | patch、必要的新文件、base/head commit、复现说明 |
| 悬赏完成 | 榜文展示正式交付批次、文件列表、验收标准及结果 | 最终产物、运行/使用说明、测试或验证证据 |
| 返工 | 旧交付留存，新批次明确说明变更 | 不可覆盖的版本和批次 |
| Agent 离线 | 已交付内容仍可获取；未上传内容显示待同步 | 平台保存的副本 |
| 获取现有目录文件 | 从允许导出的目录选文件或要求 Agent 补交 | 明确选择的文件快照 |

「工作空间」须在产品上区分：Agent 执行目录、任务协作工作台、用户收到的产物。第一期交付目录中的指定成果，不承诺浏览或同步整个运行目录。

支持纯文本类任务：结构化的结论、说明或查询结果也可以是正式成果，不能为了通过验收强行制造空文件。发布任务时声明 `text/files/mixed` 交付要求；要求文件的任务不能只凭“已完成”三字提交。

## 4. 方案比较

| 路径 | 优点 | 局限 | 建议 |
| --- | --- | --- | --- |
| 把本地路径放进聊天 | 改动小 | 路径不具备跨机器可达性，无权限和保留保证 | 仅用于本地诊断 |
| 暴露 Agent 文件服务器 | 可以远程浏览 | 本地/NAT/离线不可用，目录权限复杂，产生入站网络依赖 | 不作为主要交付链路 |
| Git commit/PR 交付 | 代码审阅和历史完善 | 报告、图片、大文件适配差；用户可能无仓库权限 | 作为代码类成果的一种补充 |
| 平台托管产物 + 业务引用 | 可离线取件，统一 ACL、版本、下载和验收 | 需要存储、协议、迁移、客户端改造 | 推荐 |

存储推荐私有对象存储（部署选型可选 OSS 或 S3 兼容服务），通过适配接口接入。已有阿里云部署并不证明对象存储已开通，实施前核对 bucket、地域、网关限制和出网条件。开发环境可用私有本地目录适配器，但应沿用相同鉴权与状态机；生产不以应用容器临时磁盘保存成果。

## 5. 可行性、成本与实施边界

- 技术可行性高：Vue/Java/Node 能完成该链路，任务领域已有较多基础，无需整体更换技术栈。
- 主要投入是可靠性与权限闭环：文件可用性、运行到会话/任务的可信绑定、断线重传、版本冻结、用户验收。
- v1.1按单一写入任务串行执行：**R1取件7～10人日，R2正式单Agent验收累计12～18人日；加2～3人日缓冲，计划14～21人日**（约3～4工作周，不含外部等待）。原18～28人日概算由HTTP首发、共享契约/组件及推迟增强项调整；不宣称同等完整范围的全部工作都消失。此估计包含常规验证/评审，不是已测量工期承诺。
- 完整目录浏览、跨设备历史补交、分片大文件、批量ZIP、更多预览格式仍暂估追加8～15人日；多人正式验收、原生微信桥接、代码PR自动化按各自契约另估。
- 资金联动需独立核查现有钱包/托管结算实现后估算；没有这一基线，不把“验收后打款”纳入第一期必达承诺。

容量示例（规划假设）：1,000 个日活用户 × 每日 3 次产出 × 平均 2 MiB × 保留 30 天，约 176 GiB 活跃数据；若平均下载 1.5 次，约 264 GiB/月下载流量。另计版本、预览衍生件、冗余、请求次数和安全处理成本。实际费用按选定供应商计价，视频类产物可能远超这个假设。

本方案默认：用户私有、显式交付、单文件暂定 50 MiB、单次交付 200 MiB/100 个文件、未完成上传暂存 24 小时。普通对话产物暂定保留 30 天并提供到期提醒；正式验收产物暂定至少 90 天，纠纷/保全状态暂停清理。额度与保留策略在发布前形成产品配置及用户可见说明。

## 6. 决策建议

v1.1已完成实施细化，建议按execution-plan先交付R1两个入口取件，再完成R2单Agent正式验收，随后扩展目录浏览、多人验收与资金联动。需要在实施启动时确定的是存储部署参数、配额/保留产品策略，以及资金系统真实集成基线；这些不妨碍当前对核心技术方案作可行性判断。
