# 典籍阁 Agent 任职与内容维护：develop 合入与缺口核对

核对日期：2026-10-13。任务 AAM-MERGE-DEVELOP-20261013。状态：组件合入已完成并推送；本报告随 Root merge 提交，功能未整体验收。

## 范围与分支

只在隔离 worktree 将 develop 合入现有 `codex/archive-agent-maintenance*` 特性分支；不合回 develop/master，不 force push，不触碰原 D 盘工作区。没有部署、实际任职、生产安装/上架、付费模型调用。

17:30 首次 fetch 后，18:17 再次核验发现 API/Client develop 又有提交，18:55 收口复查又纳入 API 的 dynamic skill package 提交，最终合入以下精确基线；“最新”是此查询时点，而非对未来提交的保证。

| 仓库 | 本轮 develop 基线 | 特性候选 |
|---|---|---|
| Root | `77bd860c3660763911dc79bce7a3278420a5e2b2` | 本报告所在 merge commit |
| API | `281ee445621ad1887f0aca4262f9c47103543560` | `b4ccdefd96adbae6d6a149def43fb52c443df195` |
| Web | `cb730681570688e0051b5cd79737a3c004817881` | `68c93f247ba101910200ab6122c59821f36b3faa` |
| Client | `6325af1d858bf6e35b3e7046bf967f2c85ba7d5b` | `35b4ab6159aa20728676237a0779232cd8d628c9` |

## 本轮实际验证

- Web：19 个相关 selector **531/531 PASS，0 pending**；受测前后 tree `220b91dd2734c054ce762545b1bea4b38ba1c096` 一致。覆盖典籍维护/Reader、会话、宋江/直达、回执、讨论页与悬赏内联结果。不是浏览器 Runtime E2E。
- Web 默认 `npm test`：**exit 1，测试加载失败**。`juyiting-bounty-text-selection.test.js:420` 在 Windows 构造 `C:\C:\...` 路径；该文件 blob 与 develop 相同。没有获得默认套件测试结果，不能记为 PASS。新默认配置排除 16 个资产/遮挡 selector；上轮 39 失败未因此被认定修复。
- API：相对旧分支修改/新增的 **195 个 Java 文件 parse-only，0 语法错误**；**未做类型检查/编译/Gradle 单测**。
- API 服务端尝试基于早期候选 `e9dd2138`（不是最终 API commit）：隔离 MySQL 初始化失败，日志为 Performance schema tables initialization failed，同期文件系统近耗尽；Gradle 尚未执行。只删除本任务失败 MySQL 数据目录约 175 MB，保留日志，未清理其他任务/生产目录或杀进程，不在相同条件下盲重跑。不能确定全部磁盘下降由本任务造成。
- Client 最终：Linux 全套 **1005 / 995 PASS / 0 FAIL / 10 SKIP**；Runtime 三个 selector **123/123 PASS，0 SKIP**。精确 commit `35b4ab6`、tree `3a3b7674`，受测前后源码干净且不变。10 个 skip 为现有真实 CLI/provider/bwrap 环境项，不是通过。
- Client 历史失败与修复：Linux 首轮精确候选 `5bec7d2`：全套 1005 / 940 PASS / 55 FAIL / 10 SKIP；Runtime 三个 selector 123 / 122 PASS / 1 FAIL。已定位并窄修共享 extractor 误把批准典籍包当作新 executable manifest、PLATFORM 顶层 installationId 未拒绝；未改测试断言或 ZIP。新候选 `35b4ab6` 同套复测全部非跳过用例通过；独立只读 Sol 窄复核关闭两项源码问题，范围不扩展到整套 API/Client/ACL/E2E；首轮失败原件永久保留。
- 正式前端 Flow、生产构建、真实浏览器/Runtime 验收：未执行。源码 push 与局部测试不等于上线或全功能完成。

## 已有功能，不应再当作从零待开发

核对当前 Controller、Service、Web 面板与定向测试：任职/撤任/书目与权限范围、固定来源快照、WAITING_INPUT/WAITING_ASSIGNEE 与 resolve-input、草稿 blocks/PATCH/校验/operation 恢复、版本历史/发布/下架、维护回执卡与 Reader 版本对比均已有实现。

## 还缺什么（按优先级）

1. **新统一 Runtime 的闭环验收**：本次 develop 移除了旧独立 API-key launcher/installer，必须以 installation/session proof、readyCommandTypes、HTTP ACK 为唯一权威。典籍与平台技能接线已随合并适配（唯一入口、精确 native 路由、完整 session proof、payload/scanner/Ajv/schema 闭包）；仍需要真实统一安装包启动、平台技能安装、典籍执行/native 回调、断线重连/重放、旧会话/撤任 fencing 的跨组件验证，不能复活旧执行轨道造绿。
2. **API 测试代码迁移与完整编译**：旧特性测试仍引用已删除的 API-key 构造、registerCommandProtocols、旧 bind/6参数 dispatch；ControlledTarget 第二参数由 key 字符串变为 SessionFence。影响 AgentControlledRuntimeProtocolTest、AgentControlledWebSocketDispatchTest、ArchiveCrossComponentFixtureConfiguration/Server、ArchiveAgentExecutionAdapterTest、PlatformSkillInstallationServiceTest、PlatformInstalledSkillResolverTest、ArchiveExecutionCommandDispatcherTest。静态不匹配已确认，但尚无本轮 compiler 结果。须迁移 fixture 并保留身份/ACL/撤权负例，不能删测试或加旧 API-key fallback。
3. **实库失败修复/归因**：2026-10-08 曾有 5 个维护/MySQL 失败及另外 11 个 archive 回归失败。维护 Service 与对应并发测试 blob 未随这次 develop 改变，不能声称已修；本轮没跑，亦不把历史数字填成本轮失败数。须先恢复隔离验证空间，然后用当前精确源码跑 fresh XML 与 validateLayering。
4. **网关发布接线**：本次 develop 引入的 nginx native location 清单没有 `/internal/archive/v1/...` 和 `/internal/agent/platform-skills/...`；上线前需核对目标站点其他 location 是否覆盖，并补精确 method/path 代理与测试。没有读取或修改线上 nginx，不断言线上已经不可达。
5. **产品级端到端与上线准备**：真实宋江/直达 → 当前任职 Agent → DRAFT_ONLY 草稿路径或 PUBLISH_VALIDATED + AUTO 授权发布路径 → publication → Reader 读回，以及撤任/改派/重连闭环，尚未用最新统一 Runtime 完整验证；84 项业务验收仍全部 not_run、evidence=null。首任管理员、授权来源、显式任职、功能开关、部署顺序与实际上架均未执行。

结论：基础页面和业务接口已存在，主要剩余工作是统一 Runtime 契约迁移、后端测试/实库问题、网关接线与真实业务闭环；**当前不能按“功能已完成/可上线”验收**。

## 证据

本轮原件：`evidence/merge-develop/20261013/`；历史结果保留 `merge-validation-20261008.md`。当期 pin 仅更新 integration.yaml 的 pinned_revisions，不重写旧 SHA/测试/证据。批准技能 ZIP 与历史 SQL 保留原始字节。
