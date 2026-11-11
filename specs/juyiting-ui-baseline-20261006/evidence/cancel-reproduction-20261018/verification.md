# 生产“取消待处理回话”条件复现

核对日期：2026-10-18（日志 UTC，部分操作对应上海时间次日凌晨）。范围：生产真实 UI 发出测试纯文字消息、观察工具栏；未点击取消、验收或部署。

## 实测

- 正式事项448、会话1760458005697：单次 POST /chat/conversations/1760458005697/interactions/discussion 返回503，未观察到取消按钮。未取得此响应正文，不判定根因。
- 吴用新密议：单次 POST /chat/stream 返回400，code=E003，msg=参数异常；随后请求查询返回404、CHAT_NOT_FOUND。页面提示“传令连接中断，结果未知”与“需要恢复核对”，观察窗口内未出现取消按钮。
- 浏览器守卫阻止的推荐 POST 不属于生产接口故障。日志中的 OPTIONS 200 不代表对应 POST 成功。
- 没有获得可取消回话的正向样本，因此不能声称已动态验证按钮正常或不存在。不盲目重发。

## 源码条件（不是生产已安装版本证明）

本地 web HEAD 6fbdb6618b1132316a95db87cca9402de83138e8。
ChatPanel.vue 以 durableCancelTarget 控制按钮显示；hallDeliberationState.js 的 cancellationTarget 需要 requestId 和至少一个有 turnId 的未终态回话；单回话还需有效 stateVersion。多个未终态回话使用 allPending 目标。
单有“生成中”或“恢复核对”文字并不足以证明满足条件。

## 证据

actions.jsonl、readonly-network.json、formal-cancel-observations.json、cancel-observations.json、http-error-400.json、http-error-404.json。
private-request-not-admitted.png 是失败状态截图，不是取消按钮出现截图。下一步应先定位上述发送受理失败，再用有效未终态回话验证显示和取消行为；当前未开展修复或部署。
