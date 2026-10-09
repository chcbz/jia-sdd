# CYF Workspace Guidance

## 规则适用范围（2026-10-08）

- 本文件规定 **CYF 项目统一规则**，适用于本项目的前端、后端及参与任务的子 Agent，不修改 Codex 全局规则、其他项目规则或共享技能。
- 本项目构建/测试/部署采用下述“前端 Flow、后端本地”分工；父目录说明或共享技能中旧的“双端 Flow”及自动部署默认不作为本项目执行依据。其余服务器目录、权限、身份、锁、备份与生产操作边界继续保留。

## 项目入口

- `web/`（Vue）和 `api/`（Java/Gradle）是独立组件仓库；根仓库负责协调与文档。
- 项目地图：`docs/codex-project-map.md`；跨仓交付：`docs/sdd-workflow.md`；聚义厅：`docs/juyiting-runbook.md`。优先定向搜索，详细知识放对应指南。
- 开工选择验证入口时，先查 `ops/orchestration/README.md` 的已有工具索引，按任务读取对应说明；不默认重新编写 runner，也不全量加载历史证据。

## 开发原则

- 快速迭代优先推进，问题通过修复或技术栈优化解决，不默认保守回退。
- **聚义厅低于 `2.0.0` 均为内测版本，不考虑旧版本兼容，一切以最新版本为准。** 前后端、Agent 客户端、文档与测试同步采用最新契约，不保留旧版本兼容层或双轨实现；`2.0.0` 及后续策略另行明确。
- 每项任务一个 Owner，自检后合入组件 `develop`，不创建独立 Reviewer、不逐次加人工审批或重复构建。改动限于任务范围，不覆盖或回退无关修改。
- 保留身份/ACL、幂等、事务、锁归属及相关回归；生产数据、迁移、扣费和流水线外操作按实际授权与恢复要求执行。

## 文档收口

- 已核验特性的稳定知识回写既有架构、模块和运维说明；不把实施流水账堆进整体架构。原需求、冻结合同、测试和发布证据保留原路径，作为历史来源而非当前开发指令。
- 局部更新注明核对日期、源码 commit 和覆盖范围；未核实部分保留旧基线标识。源码实现、历史发布和当前线上状态分开，不因文档整理重标任务完成。具体收口方式见 `docs/sdd-workflow.md`，日常知识入口见 `docs/knowledge-base/README.md`。

## 开发效率与上下文管理（2026-10-08）

适用于本项目所有开发任务；验证与文档深度按改动范围和风险确定，不按功能大小免除必要设计或回归。详细流程与效果评估统一维护在 `docs/sdd-workflow.md#development-efficiency`。

- **先固定范围和源码**：在现有 handoff 记录目标/非目标、唯一 Owner、仓库/branch/worktree、base commit/tree、验收和最早定向验证。分别核对本地HEAD、远端develop、受测候选和线上版本；查询注明时间，远端不可达时不声称最新。不覆盖脏工作区。
- **按需读取上下文**：先读项目入口、相关模块和当前handoff，再定向搜索源码；详细日志/历史证据保留文件路径，不全量载入。压缩或交接保留目标、固定源码、已确认结论、证据路径、真实阻塞及下一条动作，不靠聊天记忆接续。
- **复用并连续推进**：先查已有工具；同一Owner在授权范围内连续完成实现、自检与集成准备，阶段通知不是停工点。不默认扩建提效框架或新增Reviewer/逐阶段审批，实际阻塞有证据才补工具。
- **分层验证**：先取得最小有效反馈，再覆盖受影响回归；精确输入及完整证据匹配才能复用。正式验证和发布遵守下文，不把本机诊断或历史成功当作正式验收/上线。
- **明确交接与收口**：派发子Agent/独立worktree时显式提供 `/home/isp/wsps/cyf/AGENTS.md`、命中的工具说明、真实任务ID与源码基线，在当前handoff确认接收方已读取。活动Agent不自动重载规则，在自然接续点提醒，不抢占或改派。稳定知识回写既有指南，证据保留原处。
- **评估实际收益**：沿用handoff模板记录定位/实现/验证/等待，未知留空，开发完成与发布等待分开。当前只证实执行历史验证与缓存复用可行，整体开发周期和上下文收益仍待可比任务验证；不新增台账、硬时限或无实测缩时承诺。
- **专项工具按范围使用**：执行历史相关改动复用 `ops/orchestration/execution_history_check.py`（浏览器定向诊断加 `--browser`），详见 `specs/juyiting-execution-recovery/contract-pilot/README.md`；使用本任务和固定源码，不照搬示例ID/旧版本，不强制无关功能运行。

## 构建与版本化部署（2026-10-08）

- **前端走阿里云 Flow，后端走本地构建部署。** 正式前端测试、生产构建、制品与部署复用 `4403172`；后端正式测试、构建、制品生成与部署默认本地执行，不再默认启动 `5260799` 或后端 CI-only Flow。旧 Flow 入口保留历史与按需诊断用途，不新增流水线。
- **develop 不自动部署。** develop 用于开发集成与验证；合入、push 或验证成功均不触发部署，也不按定时任务自动发布最新 develop。
- **统一版本化部署：确定发布版本 → 固定源码 commit/tree → 对应环境测试/构建 → 同批不可变制品 → 部署 → 在线核验。** 前端绑定同 Flow Run 制品；后端绑定同本地 build ID、日志和制品 SHA-256。版本、源码、制品和部署记录须对应，不得将验证成功报告为版本已上线。
- 前端本机仅开发预览、控制面与低成本定向诊断；禁止本机生产打包、源码到生产脚本或 Flow 失败后回退本机构建。本地结果不替代精确 commit 的前端 Flow 证据。
- 后端在固定 commit 的干净源码目录或独立 worktree 构建，不在生产安装目录编译，不发布脏工作区。所有 Gradle 测试/构建/诊断先读最新相关 `build.gradle`，通过 `python3 ops/orchestration/cyf_orchestrator.py gradle ...` 串行执行；保留依赖完整性、定向回归与 `validateLayering`。
- 后端正式本地发布默认复用持久依赖与compile-only缓存：既有Gradle入口识别本地release opt-in及匹配的固定metadata init，无缓存参数即可启用；测试、`validateLayering`、依赖完整性及fresh最终JAR仍执行，不缓存测试/生产JAR。普通诊断和Flow不受影响，显式隔离/无编译缓存诊断保留；冷缓存不承诺热缓存耗时。用法、实际argv证据和工具回读见 `ops/orchestration/README.md`（2026-10-09核对）。
- 后端本地发布采用可追溯制品安装，保留统一发布锁、身份/权限、备份、可恢复安装和健康/业务核验，不恢复旧 pull/build/restart 快捷脚本。现有 `*-flow-deploy` 要求真实 Run；本地制品入口需完成适配和验证后使用，不伪造云端回执。
- 发布记录包含版本、commit/tree、前端 Flow Run 或后端本地 build ID/日志、测试摘要、制品摘要、部署顺序和在线核验。配置保存、历史回执或候选成功不等于当前发布成功。本次规则更新不直接触发构建、部署或服务重启。详见 `docs/aliyun-flow-cicd-strategy.md`。

## 操作边界

- 文档、只读查询和轻量检查直接执行，无需应用构建；无运行时副作用的可逆配置写入先保存前值、固定候选并 readback。风险操作由 Owner 核对目标、授权与恢复措施。
- 性能只观测和优化，不因 SLO/性能预算拒绝请求、中断流或下传强制 deadline；保留真实网络错误、明确传输超时、用户/身份切换取消，不绕锁、不伪报成功。
- 不设置无证据的资源、包大小或等待时限门槛；新增硬门禁须有实际问题与推导。保留制品完整性、发布互斥、可恢复安装和实际健康，互斥等待、不抢占。
- 临时运维复用 `5264702`，默认只读；有活动 Run 不覆盖配置、不取消他人任务，不按重试新增流水线。复用入口不增加操作授权。
- 独立任务可在非重叠路径、独立 worktree 并行；不操作其他聊天的进程、服务或证据。进程控制须精确归属与明确授权，冲突仅告警协调。
- Agent 路由见 `docs/implementation/MODEL_ROUTING.yaml`；DeepSeek 保持禁用，停用 Reviewer 不调度。任务 ledger 见 `docs/implementation/TASKS.yaml#runtime_ledger_json`。
- 失败先归因；同根因、同输入连续失败两次停止盲重试。证据按 tree SHA、测试 selector 与 fixture 复用；状态转换、归因及证据复用走 `ops/orchestration/cyf_orchestrator.py`。
- 完成、异常或需用户操作时主动通知，并给出下一步。性能与门禁细则见 `specs/api-performance-3s-slo/spec.md`、`docs/aliyun-flow-gate-policy.md`。

## 生产 API 安装目录（2026-10-07）

- 最终部署 JAR 固定为 `/home/isp/hosts/cyf/api/cyf-api-kit.jar`；生产进程的 `-jar` 与 cwd 使用该实体目录。`/opt/cyf/service/api` 仅为兼容链接，不恢复第二套实体部署。
- 后端正式构建在本地固定源码目录/独立 worktree；生产目录只安装已验证制品。既有 Flow 状态/下载仍留在 `/var/lib/cyf-api-flow`，备份留在 `/home/isp/baks`，不将历史 Flow 回执当成本地 build 证据。旧 M1/M2 releases 目录不作为新的生产 API 安装目标。
- 主机控制工具 source 位于 `ops/ci/aliyun-flow/host`。路径修改/重装后执行只读 `/usr/bin/python3 -I -B /home/isp/bin/tests/test_cyf_api_canonical_path.py`；保留现行脚本的其他修复，不整文件回退到较旧版本。
