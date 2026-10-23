# 聚义厅语音输入与会话 — 验收

API/Web 源码、集成和独立构建材料已有 accepted；语音生产启用与真实 Provider 证明尚未完成。

## 未完成验收

- [ ] 真实 runtime Owner 自然终态和健康基线交接
- [ ] 最终生命周期/包身份及 release guard
- [ ] 认证 STT/TTS 和 Provider 能力证明
- [ ] enabled Web 最后发布与公共/设备 smoke

## 证据边界

源码 Review、selector 测试、build、推送、部署、运行时激活分别验证。当前阶段不能整体标记 PASS；既有测试只引用，不重跑，不操作其他线程证据目录。逐任务 SHA 与证据摘要见 delivery-status.md。

- [ ] 应验合同追踪完整：HTTP 形状/错误/权限与冻结音频安全合同逐项映射；source accepted 不能代替合同验收。

## 2026-09-17：1.6.0 当前验收补充

按 `docs/implementation/V1_6_VOICE_BETA_EXECUTION_20260917.md` 第 5 节验收。历史 source accepted 与 20/22 只读接口回归均不能替代语音验收。移除独立 Reviewer/最终 release_guard 队列，由责任 Owner 自检；保留实际身份、取消、幂等、云端测试与制品健康核验。未调用真实 Provider、未启用生产语音，不标记功能整体 PASS。

### 2026-09-17 候选验证状态

Web `c5fe7484` 的慢发送/回复、取消/关闭朗读、迟到回调隔离及按钮点击定向自检 25 PASS（非正式云验）。API `ab7ba3f6` 的新增 JWT/CORS/响应形状与隔离/超时回归尚未执行。两个候选已推送，尚未合入 develop、没有新发布或语音激活。后续统一上线，以用户最新安排为准。

### 09:36 最终云端回执（覆盖上文“未启动”状态）

- 已确认并修复 Start 分支过滤问题：API 返回 HTTP400，精确原因是 `branchesFilter=^develop$` 不允许候选。仅放宽为 develop 或各自唯一候选分支，默认 source branch 保持 develop，仍无 deploy。
- API `5260799 / Run85`、Web `4403172 / Run116` 已创建，source branch 分别匹配已推送的语音候选；两者均在数秒内 FAIL，日志为空（more=false），未返回 checkout commit、测试报告或制品。**不能宣称精确 SHA 验证通过，也不能据此判断单测失败或确认额度不足。**
- 当前候选依然未合入 develop；生产未改变。没有盲目 Retry、没有本地 Gradle/Vite 重型验证替代、没有付费 Provider 调用。
- 下一步：从云效运行详情/管理员取得执行启动失败的确切原因并修复；有实际补救后才重试精确候选测试/构建，成功后合入 develop，继续保持部署暂停。
- 可复核证据：`docs/implementation/handoffs/V1-6-VOICE-CLOUD-VERIFICATION-20260917.json`；唯一运行台账保持未完成。
