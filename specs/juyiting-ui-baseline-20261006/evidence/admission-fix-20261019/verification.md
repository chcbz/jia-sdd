# 议事发送异常定位及修复进度

核对日期：2026-10-19，Owner：当前任务。规则：根AGENTS、API公共接口规范v1.2；无页面样式或操作流程变更，未修改原型或前端产品代码。

## 已定位

1. 密议400：生产2026-10-18 23:40:50.472日志明确定位`JsonRequest.data.ChatMessageDTO.requestRevision`，收到String "1"，严格mapper拒绝隐式转换Long。前端请求版本为十进制String，服务端字段未显式适配。不是登录失败或模型异常。请求未受理后的404不能当作已创建回话。
2. 正式事项448的503：本轮真实UI单次发送响应为`TYPED_DELIBERATION_PERSISTENCE_ERROR / Typed deliberation runtime is unavailable`，requestId `612260b7-5eec-449a-93f0-31dc7aa2a000`。生产只读事务按该会话tenant/client/owner及李逵Agent精确查询，运行状态offline，最后在线2026-10-15 16:34:49.745+08:00；installation仍ACTIVE，不等于运行在线。本机统一host仅吴用/林冲/卢俊义，李逵为自家机器selfhost-li159-118-935f9597。未更改Agent归属/重分配/启动或重启服务，不把SKILL_BASELINE_REQUIRED当作此503根因。

## 修复候选

API基线b76a1d0aeda572767a6d4734d050121d985bd9c9；候选3a960261ffad6e12d6e412df62eeac953b0d8f64/tree616defad011a2991acfa1e90ea7c92b7147d3103，远端分支codex/chat-admission-fix-20261019。
- ChatMessageDTO.requestRevision显式使用D1字符串解码器，保留内部Long精度；序列化同样输出精确String。
- 只接受正规范十进制字符串和Long范围，不开启全局隐式转换，不接受JSON数字、前导零、负值、浮点或溢出。
- ChatStreamHttpTest改用生产ApiEnvelopeJsonConfig/ApiRequestEnvelopeAdvice，真实报文包含requestRevision；新增12种非法值受理前拒绝及Long.MAX_VALUE往返回归。既有流结束/错误/取消语义测试保留。

## 验证与发布边界

Flow5260799/Run153固定该候选，沿用原验证工具、compile-only缓存和现行测试集合，额外包含ChatStreamHttpTest；校验/构建/上传而非部署。原配置已保存，Run终态后需恢复并readback。完整控制记录在/var/tmp/cyf-chat-admission-fix-20261019。正式结果待Run终态，不把diff检查作为测试通过。
生产JAR只读摘要d487704e014b1cfcb631c90a484f9f27a404cb24a9cbcc5368b50f5ef1dc3cc0；尚未关联精确安装源码，不以本地HEAD代替生产版本。当前未发布，未证明线上400消失，未取得取消按钮正例。

## 00:21收口

Run153 SUCCESS：2389项执行，2294通过、95跳过、0失败/错误；本次ChatStreamHttpTest 6项全部通过且无跳过。诊断压缩内容摘要已重算匹配，commit/run匹配；分层检查、fresh bootJar、同Run上传成功，制品SHA来自认证日志，尚未独立下载复算。原Flow配置已恢复并readback匹配。

李逵自家机器173.230.149.118使用历史固定known_hosts只读SSH探测，返回Permission denied；当前SSH agent socket不可用，未取得远程运维会话。不能声称已恢复Agent。下一步需要可用的该主机SSH入口/密钥路径；同时按明确版本完成API的Flow发布和真实回归。未push develop（当前原配置push会自动触发另一轮旧选择器CI）；候选远端保留。此任务未全部完成。
