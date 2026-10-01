# 自然议事闭包：本轮真实验证与修复（2026-10-01）

本记录为源码/验证证据，不是第二任务台账。不改冻结合同、研发 pins 或产品验收状态。运行Owner/gate仍在主工作区 `docs/implementation/TASKS.yaml#runtime_ledger_json`。

## 1. Web实际通过项与未通过项

原Owner候选 `eba12b14bfe74b31272902b619e6f76376efc60f` / tree `34ce0ce7d790913ab4bdf7334a6794186ba661f3`，12条授权路径。Main实际执行原7文件定向测试：**31通过**。但主线程补测真实模板/emit/production composable边界：**7失败**，因此未晋升。

1. Page将嵌套cards/pending/recovery ref本体传给组件，真实Vue接收RefImpl而不是数组/null/布尔值。
2. BountyDiscussionPanel丢弃send-message参数，本轮选定reference没有到达Page/API。
3. 较晚返回的OPEN覆盖已收到的ANSWERED，问题状态倒退。
4. ANSWERED readback未清除已选pending，下一条仍拟答已回答的问题。
5. foreign task outcome被加入当前cards；历史assignment仍应遵循原scope读权限，不能借修复隐藏历史。
6. GENERATE_IMAGE携带合法参考源时被parser丢弃。冻结Client合同允许GEN引用image，并非仅无参考。
7. recoveryAvailable被首次模板读取缓存为false，原键UNKNOWN持久化写入后不响应更新，恢复按钮不会出现。

原始未改probe、stdout、31项日志和SHA见[便携manifest](integration-evidence-20260928/web-typed-eba12b1-main-failures/manifest.json)。Owner按固定矩阵修复新child，并补typed_question_answered的权威GET提示、cold recovery/dispose生命周期；不是提高数字门槛或关闭功能来获得通过。

## 2. API实际编译失败与新源码修复

`b3c02a1646a583d0ceda08dc83922ec90859f003`的正常生产源图编译成功，但测试编译真实失败：旧AgentTaskProviderCostConsentServiceImplTest.MemoryDao未实现新增follow-up DAO接口。实际javac报revokeFollowup一项；另五项由接口/源码逐项比对确认。此次**0测试、0 fresh XML**，不能把62项V3/MySQL3和82项V2当通过。

原Owner已提供最小child `da1710bcbe966209015941debdcee179034a0bb7` / tree `337ebd925036d0faba365249a105d4784d95dc31`，parent为b3c02a，只增加该一个测试文件的62行；六方法实现purpose/scope/operationGrant/版本与合法状态CAS，生产源与selector不变。Main独立核对parent/path/tree/blob/whitespace和Owner证据。该child仍**待实际验证**，不是源码验收或发布结论。

[精确验证授权矩阵](integration-evidence-20260928/api-followup-v3-memorydao-child-verification-matrix-20261001.json)允许原Verifier在自身干净worktree更新该child、保持真实正常源图/AP/依赖/既有测试并经orchestrator串行运行；不得删除V2、缩selector、复制class或用手工javac绕过。原OOM/import/testCompile失败分别保留。

## 3. 完整交付仍须继续

API原子typed final/question CAS/new CHAT续办包仍在独立Owner施工。本轮不合develop、不生产构建/部署、不调用付费Provider、不修改生产数据库。后续必须精确组合、真实隔离MySQL及当前session/身份闭包，再继续真实INSPECT、双接应、全部媒体预览下载保存、正式交付验收/完成与目标版本发布。源码切片通过不代表34项产品/29桥/浏览器全流程通过，未达到条件不通知“可以验收”。
