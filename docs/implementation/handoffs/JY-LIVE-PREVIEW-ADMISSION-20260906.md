# JY-LIVE-PREVIEW — 设计与路径交接（2026-09-06）

输入：控制线程 `01a004d0-16ac-7482-9112-054f42b59ad8` 转达用户授权真实只读动态缩略地图。此文为交接证据，不是第二运行台账；未创建 Writer。

## 设计边界

- 同地图、单运行态、只读、位置连续；不能复制第二个游戏循环或输入所有权。
- 源线程可起草 `specs/juyiting-live-map-preview/` 五件套，明确可观察验收；不改本日09:21归档快照/manifest或已冻结其他合同。
- 安全并行候选：独立新增 preview 展示组件、纯输入/缩放策略与纯测试；文件名尚需现有负责线程提交 exact owned paths 后正式 claim，不能据此修改共享入口。
- 共享路径：HallStage、JuyitingGame 及其生命周期/输入/尺寸逻辑仍归 `JY-FOLLOWUP-SCREEN-20260906`。等其 accepted + exact handoff 后再集成，不强占或复制 Writer。

## 请求 SCREEN Owner 提供

1. exact 新候选 commit/tree 及仍 owned 的共享文件清单。
2. runloop/visibility、尺寸更新、输入启停、mount/unmount 的只读消费合同。
3. 可供缩略地图订阅的位置/视口快照与生命周期边界；不要求暂停其整改或提前实现 preview。
4. 不冲突新组件/纯测试路径建议与后续共享接入交接点。

## 下一步

源线程收集上述合同，提交既有拟任 Writer 的 thread/base/tree/worktree/owned paths，由统一 orchestrator 做 task-scoped claim。独立设计不等待全局 Writer；重型验证/共享入口接入不提前启动。无部署、进程信号、daemon/unit/证据或 Gradle锁操作。

## 2026-09-06 16:44 CST — ECO 主控明确释放地图接线源码范围

- 有效回执来源：ECO W11 主控 `01a05abc-c76e-7c63-bb36-fafbd6fa913c` 明确确认自身身份，并释放**预览独立 worktree 内 `src/components/world/JuyiHall.vue` 地图接线源码 claim**。这是实际主控回执，不是根据 `owner=null` 推断释放。
- ECO `48c79fabfbca76688ee99c257fa9e50dc9b2604b` / tree `b76b5f50aaeb90dd4f29ad368ecf2e58a51414dc` 候选、工作树、证据和依赖继续冻结且不触碰。ECO 后续预计仅修 commerce composable 与 tests，不占生产 Hall 地图接线范围；“预计”不等于授权修改其源码。
- 接收方仍为原 Terra `01a07470-7977-7b72-a7c5-9f0b4c336336`，独立 worktree `.worktrees/juyiting-live-map-preview-20260906`；承接实际 `3329e076cc060213baa3a51a5f006073b2289ec6` / tree `b756ec7c00f1fb31fa210d63a12b1a9fcc285e02`，不得把尚未产生的整页接线 commit 填入台账。
- 允许继续原 P1 四路径及 P2 合同 §7 十一路径；新增解锁仅限 `JuyiHall.vue` 地图/稳定 target/单 HallStage Teleport/页面生命周期接线及必要展示状态。不得借此改资金/commerce、R9 stale completion/public return、显式目标 Agent 或 voice 行为。既有 accepted SCREEN/reader/layout 仍须保留。
- 此处不宣称当前预览基线已包含 ECO 未发布的 R9 全部代码；未来合并必须保留其语义。预览需提交新 exact commit/tree 和相对 `3329` 的 `JuyiHall.vue` 独立 delta，交 ECO 主控核对，禁止整文件覆盖。
- 既有三 selector 27/27 PASS 只属于 `3329/b756` 有界 adapter；新页面接线需新证据，不能继承整页 PASS。主控路径释放不包含重任务、测试重跑、build、browser、Gradle、部署或 API runtime 准入。
- 唯一当前执行状态仍为 `TASKS.yaml#runtime_ledger_json`，本文只作为实际交接证据。原生宿主 waiting_user 不阻塞 H5 地图接线。

### dac1 页面差异的 ECO 兼容性回执（2026-09-06，源主控转交）

预览主控 `01a004d0-16ac-7482-9112-054f42b59ad8` 转交已确认 ECO 主控 `01a05abc-c76e-7c63-bb36-fafbd6fa913c` 的只读兼容回执：`dac1c555042ce48d7c2e274df2b8396456efb0a1` / tree `fd3e0c6321a29f2b7e1d3f7a57ddc8c18343efe6` 相对 `3329` 的 JuyiHall 补丁 SHA256 `66675aef6a9a43750e04ecaf6a654d97814a68ec3ab327491d579f3073c36e31` 一致；+84/-2 未触及 funded、R9 stale completion/public return、显式 Agent 范围，无地图接线认领冲突。协调线程此前已独立核对该补丁与 Git 差异的哈希一致。

这是 **dac1 差异的兼容性回执，不是 LIVE 源码或运行验收**，不适用于未经核对的后续补丁。源主控同时转报 ECO 新候选简称 `c45a5da/edd82` 仅涉及 useSkillMarket 与 tests，其候选内 Hall 内容仍与 `48c79` 一致；此处不把 ECO 候选内文件当作线上版本，也不推断 ECO 已部署。原 Terra 继续已有首 target/高度链收口，最终新 exact 与新页面 delta 仍需提交双方核对，禁止用整文件替换覆盖 ECO 后续内容。无额外测试、构建、运行或部署授权。
