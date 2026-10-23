# 聚义厅语音输入与会话 — 任务

任务级实施/审核/验证由 `docs/implementation/TASKS.yaml#runtime_ledger_json` 唯一管理；不在此派发第二份 Owner。

## 2026-09-17 12:51 当前状态（优先于下方历史）

- [x] API相关215项、Web全量2186项通过；Web另2项原有pending未计PASS。
- [x] 本地API/Web生产构建成功，双组件合入develop并冻结远端`release/1.6.0`。
- [x] 不可变制品/commit/tree/工具摘要绑定，联合verify与两组件dry-run通过。
- [x] 本地实际安装与线上健康核验完成：API UP；Web根页/聚义厅/入口资源200且摘要一致；发布锁已释放。
- [ ] 真实Provider启用、授权付费调用及设备验收：另列范围，尚未完成。

当前执行依据：`docs/implementation/V1_6_LOCAL_RELEASE_PLAN_20260917.md`。下列早期Flow/Reviewer/禁止部署条款是历史，已由最新本地发布授权替代；不抹去历史失败证据。

## 剩余交付

- [ ] 真实 runtime Owner 自然终态和健康基线交接
- [ ] 最终生命周期/包身份及 release guard
- [ ] 认证 STT/TTS 和 Provider 能力证明
- [ ] enabled Web 最后发布与公共/设备 smoke

完整快照映射见 [delivery-status.md](delivery-status.md)。历史定义中未进入当前运行台账的任务仍是规划，不擅自启动。

## 仓库分工（角色，不是第二份执行认领）

| 仓库/职责 | 路由 | 边界 |
| --- | --- | --- |
| API | critical_worker | 身份/ACL/事务/后端核心；exact task owner 读取运行台账 |
| Web | balanced_worker | 冻结合同下交互与前端集成；不得修改 API owned paths |
| 集成/归档 | main_orchestrator | 不重置脏主树，不覆盖其他任务认领 |
| 验证 | gpt_test_runner | exact tree/selector/fixture；重型资源串行 |
| 独立审查 | sol_reviewer | 只读，不预实现或修复 |

- [ ] 合同追踪：把既有语音 HTTP 请求/响应/错误合同集中映射到 design.md，并按冻结架构核对 accepted 实现；不创建或修改 API。

## 2026-09-17：1.6.0 当前实施

本节替代上文历史执行角色中的独立 Reviewer/release guard 要求，不改写历史证据。

- [ ] `V1-6-VOICE-WEB-AVAILABILITY-20260917`：移除 120 秒自动关闭语音回合；sending/waiting_reply 可停止等待；慢回复和迟到响应隔离回归。唯一 Owner 在 runtime ledger，独立 Web worktree 开发。
- [x] 集中已有 HTTP 契约到 `docs/implementation/V1_6_VOICE_BETA_EXECUTION_20260917.md`，只代表文档补齐，不代表真实业务验收。
- [ ] Owner 自检候选后集成 develop；正式云端测试、制品、发布和 readback。
- [ ] 授权范围明确后做真实 STT/TTS/设备验收，未授权不调用 Provider。

本轮不处理外派 Persona Catalog/378 缺陷，不改客户端或生产数据。

### 2026-09-17 候选进度（不覆盖历史）

- [x] Web 等待/取消可用性修复：已推送 `c5fe7484`，25 项本地定向自检通过。
- [x] API 语音身份/租约/传输配置修复及 HTTP 契约回归代码：已推送 `ab7ba3f6`，静态检查通过。
- [ ] 精确候选 Flow 测试与构建（API 新增回归尚未执行）。
- [ ] 通过后合入 develop；用户本次要求后续统一上线，禁止自动部署。
- [ ] 单独安排生产激活、授权 Provider 与真实设备验收。

候选证据以 `docs/implementation/handoffs/V1-6-VOICE-{WEB,API}-CANDIDATE-20260917.json` 为索引；Owner/gate 只在唯一 runtime ledger 登记。

### 2026-09-17 10:34 最新本地发布授权与回归

本节覆盖上文“禁止自动部署/等待Flow”执行条件：云效暂不可用，用户允许本地验证后从已合入develop的精确提交冻结release分支发布。

- [x] 前后端初始候选已合入各组件develop并核对远端。
- [ ] 本地真实回归整改：Web成果版本校验及W11夹具已修，77项定向通过；后端95项编译错误消除，实际执行144项中136通过、8失败、无skip。
- [ ] 修复本轮发现的两个任务会话DAO调用将tenant误当owner参数的问题，并验证真实H2跨作用域隔离；解决真实HTTP CORS失败，重验精确候选。
- [ ] 修复本机Chromium测试启动/基准溯源后完整验证，构建精确本地制品。
- [ ] 冻结组件release分支，记录commit/tree与本地产物摘要；按互斥/归属执行可恢复发布及线上检查。
- [ ] 语音生产启用/Provider付费/设备验收仍单独授权，不与代码部署混为一谈。

详见 `/home/isp/wsps/cyf/docs/implementation/V1_6_LOCAL_RELEASE_PLAN_20260917.md`，Owner/gate仍仅在runtime ledger。
