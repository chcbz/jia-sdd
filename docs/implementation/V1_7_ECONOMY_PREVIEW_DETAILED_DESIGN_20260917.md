# 下一版本：1.7.0 经济与技能市场预览

2026-09-17。用户要求语音验收延期，直接开始下一版。本版本不是银两真实交易上线，也不含isp-install。

## 需求清单

1. 个人中心新增经济预览入口，明确不扣费/不安装/不开通。
2. 钱包余额、冻结额、分页流水的当前身份只读展示。
3. 悬赏预算与token成本纯试算，明确示例价表、无正式报价落库。
4. 技能目录、版本、价格、权限与部署限制展示。
5. 显式选择自己的Agent，区分权益与真实安装证据；无证明不标成功。
6. 托管参考价格/周期与已有租约只读展示，local不收费。
7. 双身份双client隔离、迟到响应清理、移动端滚动与旧功能回归。

完整规格（后续实现以此为准）：
- `specs/economy-readonly-preview-v1-7/spec.md`：来源、已有基础、本轮增量与非目标。
- `specs/economy-readonly-preview-v1-7/design.md`：现状核查、页面交互、九类API合同、数据/ACL/零写入边界、兼容与发布。
- `specs/economy-readonly-preview-v1-7/tasks.md`：并行路径责任、实际依赖及墙钟估算。
- `specs/economy-readonly-preview-v1-7/acceptance.md`：验收矩阵。
- `specs/economy-readonly-preview-v1-7/integration.yaml`：基线/候选/发布分别记录，不伪造完成。

API/Web分开并行，Owner自检，不设Reviewer；仅Gradle重型验证和集成部署互斥。估算12–24小时净执行窗口，资源等待另计，初轮候选后重估。当前磁盘仅数十MiB且在增长；本轮启动详设/轻量代码，未启动大型构建、未操作生产。当前未发布1.7。

语音两个任务已deferred，保留TTS404/STT未执行和关闭入口；这不是验收通过。1.6固定release不动，经济生产冻结合同不动。任务当前Owner/gate只在TASKS.yaml runtime_ledger_json。

## 首个实现切片（2026-09-17）

已提交Web只读策略模块与定向测试：`058fe4271b49e9ba4419a8fc6fd58f5dca069287` / tree `823c85842798b992864d1a534f01275ddfcf8cd6`，Owner执行7/7 PASS。支持严格能力校验、禁用交易动作、身份/Agent/请求代次隔离及无Agent卡片上下文。仅此切片完成；尚未push/合develop、未接页面、未发布。证据为`docs/implementation/handoffs/V1-7-WEB-POLICY-20260917.json`；Owner已释放，API/UI/集成任务仍待继续实施。

## 16:02 进度修订

已完成用户授权深度清理，删除29个完成worktree及12个旧Flow二进制副本，约5.68GiB分配块；磁盘满盘问题已解除，API健康200/UP。API/UI两个Owner已实际并行开工，前文“仅剩数MiB、其余待分配”是14时计划快照，不再作为当前阻塞。当前仍未完成1.7集成或发布。详见`DISK_DEEP_CLEANUP_20260917.md`与唯一台账。
