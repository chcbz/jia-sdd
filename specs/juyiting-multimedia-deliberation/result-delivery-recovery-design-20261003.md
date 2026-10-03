# Agent 图片结果传输与恢复设计（2026-10-03）

状态：事实与安全边界已确认；自动恢复接口尚未实现/验收。本文不增加付费授权，不取代完整 AC01–AC22 / FD01–FD12。

## 1. 已证实的问题与当前候选

- 原417：START成功后，上传与failure均404。旧Client `5bcb16bd` 在finally删除整个runDirectory；目标Agent目录现无输出，付费claim仍CLAIMED。无法从claim重新构造PNG。
- API `25bb98a4` / tree `18c15bc6`：增加内部RESULT authority，承认已消费的START授权；仍核对原执行/consent/operation/START lease、当前会话ACL与提交fence。不因消费后的Provider/source准入失败而拒收结果。仅原fence有效期间的提交修复，正在Owner验证；不是过期lease恢复。
- Client `8b3c35fa` / tree `e307f98a`：有效PNG上传前写私有delivery字节与receipt，文件和目录fsync；404、lease过期、commit ACK丢失时保留，不把已产出图片误报普通执行失败。53项相关mock测试通过，7项可选CLI集成因未配测试环境跳过；7个leaf回归在旧lane失败（Node含父组计9fail）。仅feature源码候选，尚未部署。
- 当前inbox只返回未START的QUEUED执行；现有START lease拒绝provider-started执行。因此只保留文件不能自动重传，不能宣称本轮已闭环。

## 2. 不变的长期边界

1. **生成授权、结果传输权限分开。** START/付费claim继续一次性；结果恢复不能授予Provider调用、工具执行、读取新的参考资料或重新点将的权限。
2. **先保全字节，再上传。** 私有receipt绑定API origin、Agent、完整command及其摘要、outputId、MIME、长度和内容摘要；不能仅凭文件名或图片存在作归属判断。失败时既不删claim也不清已产出结果。
3. **平台内容仍只有一份权威对象。** Agent delivery目录是有界单执行的未确认传输副本，不是第三套用户文件系统。平台commit成功后，会话展示、可选工作空间引用、正式交付引用使用同一已校验对象/固定版本；明确commit ACK后可删除该运行的传输副本。
4. **恢复不等于重新生成。** 服务端已有COMMITTED输出则读回原receipt；有STAGED输出则幂等完成commit；有本地spool则结果专用lease上传原字节。三条路径均不调用Provider。
5. **没有字节就如实失败/待人工处理。** 不能把无法恢复的旧请求一直写成“生成较慢”，也不能未经证实标记成功。新的付费执行不是重传；必须单独核对既有授权范围、预算和新intent，不能暗改原记录。

## 3. 后续最小跨端合同（待实现，非现有API）

### 3.1 Result-only recovery admission

建议在现有conversation runtime路由下提供独立结果恢复入口，不复用START入口。

- 输入精确executionId、commandId、messageId、原inputSnapshotDigest与输出proof（outputId、sha256、byteLength）。身份来自现有AgentRuntime认证，不信任body的owner/tenant。
- 服务端按现有root → authority → execution锁序，校验tenant/client/owner、当前目标Agent、assignment/conversation generation与当前会话ACL、持久consumed START及原执行绑定。
- 原START事实保持不可变；另外持久化/区分结果传输lease。活动lease互斥，不抢占；过期恢复需CAS，不能把传输lease当成新的生成权限。
- 返回只允许stage/commit/read-receipt的fence，绑定一个输出proof；任何Provider START/input读取路径明确拒绝result-only fence。
- 过期恢复不重新依赖Provider在线、模型声明仍可查询或参考图片仍可读取，但不绕过当前会话ACL、结果接收权与明确撤销。
- 已COMMITTED返回同receipt；已FAILED/CANCELLED或权限不符不发新lease。不能覆盖已存在但不同摘要的STAGED/COMMITTED结果。

### 3.2 Client recovery

- 只遍历当前明确profile/Agent私有根，不跨用户搜索文件；拒绝symlink、hardlink、不符owner/权限、摘要/命令/来源不一致及未写完整的receipt。
- 先向服务端读取同execution的结果状态，再申请result-only lease；有权才上传原字节，收到精确commit receipt才清理。
- 无论重启、断网、ACK丢失或lease更新，均不调用原executor，不删除/重新创建付费claim。
- 缺少/损坏spool只报告恢复不可用，不自动“失败”另一仍可能产出的runtime。传输与Provider结果未知分别呈现。

### 3.3 无spool的异常终止

原417属于旧客户端未保全字节的个案，不能靠新代码复活。

- 需要owner可见的业务终止动作或已有明确授权下的可审计恢复操作，不用生产DML改状态。
- 精确绑定request/step/intent/execution与预期stateVersion，验证当前owner/会话ACL及START事实；事务内核对没有已STAGED/COMMITTED输出，并防止与在途commit竞态。
- 记录调用者、原因、证据摘要和幂等键。客户端自报“找不到文件”不是服务端已证明全局无副本；审计理由应区分“owner放弃未交付结果”和“已验证结果丢失”。
- 同一事务收敛execution、step、request并发送可重放事件。保留consumed授权、paid claim和历史计费事实，不退款、不伪报Provider未执行、不启动新执行。

## 4. 验证与发布顺序

1. API当前404最小候选：Owner单元/真实隔离MySQL、consumed授权/跨owner/旧fence/未START/重复commit回归；通过后按独立版本发布，不能混入未测试AC12。
2. Client保全候选：验证私有字节、权限/路径、实际CLI mock链路、lease过期/404/commit丢ACK；精确发布版本及运行模块摘要，仍不冒充Provider验收。
3. 冻结result-only合同后实现跨端恢复；必须覆盖原START不可重放、runtime切换、撤权、状态CAS、事务失败、结果已提交与本地记录损坏。
4. 原417按证据如实收敛；在已有授权边界内继续实际业务闭环。只有图片真实进入会话、预览/下载摘要一致、工作空间可选保存、正式交付验收及完整34项完成后，通知整体可验收。
