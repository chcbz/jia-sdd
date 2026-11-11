# API1.16.31发布与多轮图片回归（2026-10-23）

## 发布：通过

固定API `041548f601385a3463fbba06b929991371d93d9c` / tree `1bc5ae21325d9763e8325f31f4cc88a53317a5f3`，发布版本1.16.31。Flow5260799/249 SUCCESS，部署单71707194单机Success。3047项测试中2921通过、126跳过、0失败/错误；本次11项新增测试均实际执行通过，保留validateLayering及fresh bootJar。制品、receipt和安装JAR摘要同Run闭合，health/readiness均UP。API前一版本备份及恢复信息见installation-verification.json。

临时Flow配置已恢复前值并readback，健康监控按本任务maintenance marker所有权核验后resume。不改Web、Runtime、共享Codex、Provider、模型、账号或付费配置，无DDL。

## 浏览器回归：BLOCKED，不是完整验收通过

使用ziyue/吴用，新事项519、会话1760458007097。

| 项目 | 实际结果 |
| --- | --- |
| 新登录、上传图、资料列表刷新与自动选中 | PASS，真实上传201/COMMITTED |
| 手机资料预览 | PASS，800×600原图可见，预览开关、返回、取消/完成均有截图；不等于所有按钮再次实际点击 |
| 建事项并指定吴用 | PASS，真实point-and-deliberate受理，吴用online |
| 第一轮识图 | BLOCKED，模型启动前失败，无识图答案 |
| 连续追问、连续改图、逐轮输入/输出SHA | NOT_VERIFIED |
| 纯文字生图→识图→连续修改 | NOT_VERIFIED，未继续创建新失败请求 |
| 最终成果预览/验收、PC与移动端完成态 | NOT_VERIFIED |

fixture为白底、左蓝三角、右黄圆、上黑方块，原文件SHA `a80176157363cc3233eee10e3a89851cf743f70cbdbf3952d66ef534dc7b8d97`。未指定尺寸履约，PDF仍不验。

## 根因与操作边界

Runtime1.2.8/PID1404284已持有此前验证的Codex0.161.0测量；当前共享 `/usr/local/bin/codex` 已指向0.164.0包，其wrapper mtime为19:20:46、真实二进制mtime为19:21:21（北京时间2026-10-23）。二进制现308139304B，不同于此前292309256B。Runtime现行schema合同没有0.164.0。

519在20:14:21记录 `RECOVERY_REQUIRED / CHAT_FAILURE: CODEX_APP_SERVER_CONFIGURED_EXECUTABLE_DRIFT`；已有资料preparation，但没有engineThreadId或runningAt。对应后端仍RUNNING/DISPATCHED，页面“正在回话”，不能视为模型已执行。`task519-blocker.json`记录精确路径、时间、版本与请求关联。这里只确认依赖替换与拒绝原因，没有证据说明由谁执行了共享升级。

本轮API安装未修改共享Codex。未关闭完整性校验，未清恢复文件，未强行改业务状态，未回退全局包或重启影响其他工作的Runtime。需要另行明确Runtime的0.164.0兼容/依赖隔离实施与启用，再继续本矩阵；只重启也不能解决固定schema版本不匹配。

测试清理说明：首次点击停止被浏览器写保护拦截，没有发到后端；页面保守保留“停止结果尚未确认”。后续只重入核对，没有再次发起模型工作或伪造取消成功。519仍按最后权威回读记为RUNNING/DISPATCHED，不把工具拦截当产品取消失败证据；待依赖修复后按原请求状态决定恢复/取消。

原始浏览器网络与运行证据：`/var/tmp/cyf-external-flow-20261021/browser/previous-output-20261023/`；发布控制与日志：`/var/tmp/cyf-previous-output-release-20261023/`。登录凭据、认证会话不入库。详见[本轮handoff](../../../../docs/implementation/handoffs/PREVIOUS-OUTPUT-REVISION-20261023.md)。
