# 2026-10-19 异常修复版本发布与主需求复核

## 结论与授权边界

用户授权一次上线后回到当前交互优化需求；Owner chat-stop-main。API1.16.10、Web1.16.11已通过各自同Run测试、构建、制品验证和部署。**安装成功，不等于业务闭环全部验收通过，更不等于完整优化方案已上线。** 模型重复“收到。”专项暂停；尚不能认定纯模型故障。Runtime隔离候选f94c254f未合入、未安装。本轮没有第二次发布。

| 组件 | 固定源码 / tree | 正式Flow与部署单 | 测试与上线核对 |
| --- | --- | --- | --- |
| API 1.16.10 | cd2146f408e692fc58424390e89a40d2f10eb7d2 / b757d4cf1b4d3c1b864a2be47106ba0e0b734d56 | 5260799/162 SUCCESS；71357070 | 2420项：2325通过、95跳过、0失败/错误；分层、fresh JAR。安装JAR匹配同Run摘要，健康UP |
| Web 1.16.11 | f112b0b2044032d34d0f5a39251f40bbb1b5cbee / add99ae8393f3ec294c301fbc2a9380cb46de2d6 | 4403172/233 SUCCESS；71357493 | 3054通过、2pending、0失败；构建/扫描。366个制品文件与安装匹配；浏览器实际加载16个资源及入口匹配 |

API archive SHA256 `163aff836155c73161dbd729f80077db797dbd66df22b5cc65d4100e8b95f093`；JAR `f36206fb630c1f93aa36f6144ebcd520a0774ce84472927b3af2bac9acadd4f7`。Web archive `aae8db3ba9894a0f804ba6c3994ee4f44fdee05b74e9916ab763bee18576daf9`。各端安全摘要在本目录api/web子目录；原Flow配置均恢复并readback。最初API控制调用缺pipelineName在云端写入前失败，补齐并重新preflight后只启动正式Run162，不存在含糊重复发布。原始控制证据 `/var/tmp/cyf-followup-release-20261019/` 含私有参数，不整目录复制；部分云日志接口返回more，不宣称完整日志已归档。

## 生产业务冒烟：USER即时显示失败，不能按模型问题忽略

使用测试task467、会话1760458006508、吴用，13:45进行一次实际页面发送；未重复POST。请求 `mmd-typed-request_5696ecb015383b667a7b7546b58d67161dc22431`，USER1859367、ASSISTANT1859371，turn `turn_1160b7727953f6014c4549ec3e864fe82478e4db`。HTTP ADMITTED、权威请求RUNNING→COMPLETED、turn发布完成；结果为“收到。”且deliverable=false，不自动认定可验收。

`browser/followup-immediate.json` 和截图证明：新USER没有即时进入当前议事页；新ASSISTANT出现。回执后有GET request，没有内容重读。静态资源已经核对为Run233，不归因旧缓存。模型回复质量与这一前端渲染问题分开跟踪。

### 源码推演及最小失败复现

基线Web f112b0b。`useHallConversation.adoptTypedDiscussionReceipt`读取并校验request，然后`applyRequestView`，随后再检查调用方isCurrent，最后加载会话内容。`JuyiHall.vue`同步watch原始`activeRequest.conversationGeneration`并调用`invalidateFollowupContext`。当历史会话已从权威上下文/目录取得generation=1，而activeRequest尚为空时，接纳同代request会令此原始字段undefined→1，反而同步失效当前操作，跳过内容加载。

复用现有page-routing测试的真实composable和AST提取的真实同步watch，令isCurrent跟随实际followupContextGeneration。`self-fence-diagnostic.log`：预期接纳true，实际false；调用只有LIST、初始CONTENT、GET request，没有接纳后的CONTENT。此最小复现证明代码中确有自失效路径，符合线上现象；尚未在生产Vue内部直接追踪全部watch，不能排除其他并发问题。

诊断源保存为`followup-self-fence.diagnostic.test.js`，复制到Web tests同级可用现有setup定向运行；证据里的失败是预期行为未满足，不是通过测试。已移除工作区临时失败测试，**未修改生产实现、未声称修复**。详设已补录所需修正和安全回归，下一步先在既有正式测试文件补红绿回归。

## 回到原需求后的核对

- 原型文档/交互94项本地检查通过；19页×1440/390/320共57布局通过，错误0。
- natural-revision场景覆盖直接修改、普通讨论、澄清、陈旧引用、历史保留、明确验收；1440/390/320诊断通过。均为原型fixture，不是生产真实业务通过。
- 原型P02文字表中“窄屏换行”与用户要求冲突，已改为单行横向滚动，不新增统计行；更新对应SHA256SUMS并完整校验通过。
- 设计基线76文件定向对比，5文件变化，见design-source-delta.json；不是全仓差异证明。
- 当前源码仍存在finalization提交/accept耦合，ActionOutcome VERSION=4；设计中的提交与决定拆分、v5修改意图及完整四阶段投影未完成。不得把本次停止/回执相关异常修复版本标记为E03–E08整套需求交付。
- 后续主线：补USER自失效回归及修正 → 固定C01契约与C03提交/决定拆分 → C04自然修改/验收互斥 → C05统一状态/三入口 → 真实完整闭环。正式验证仍走Flow；未授权再次部署。
