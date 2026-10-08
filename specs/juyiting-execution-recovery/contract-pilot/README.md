# 执行历史契约试点（DEV-FEEDBACK-PILOT-20261008）

选择既有只读 `GET /agent/personal-workspace/executions`，不新增产品接口或业务行为。合同样例唯一来源为 `execution-history.json`；数据全部合成，不含真实账号、凭据或需求正文。

## 已实现与可执行范围

- 固定本地已核对 API/Web SHA，给出空页、首/末页、非法游标、服务不可用五个样例。
- `check-consumer.mjs` 直接加载固定 Web 源码中的真实 `usePersonalWorkspaceExecution`，注入样例 API 响应；验证 ready/empty/error 区分、只读调用、游标分页与追加结果。
- 使用独立、干净的 Web worktree；脚本检查 HEAD 和脏状态。依赖只复用已有 node_modules，不安装、不构建、不修改该工作区源码；未执行 lockfile/工具链完整性验证，所以结果仅作低成本诊断。
- 禁止意外 fetch；不会登录、录音、执行任务、调用 Provider 或扣费。不能把 injected API 当成真实 HTTP。

```bash
node specs/juyiting-execution-recovery/contract-pilot/check-consumer.mjs \
  /home/isp/wsps/worktrees/cyf-contract-consumer-20261008
```

脚本引用本目录 JSON；输出包含层级及 Java/Flow NOT_RUN。非法游标/503 样例在前端仅验证错误响应不会被误当空列表，不声称前端已经发出非法游标或验证了服务端参数校验。

## 后端与真实链路接入点（尚未实现/执行）

当前样例已被前端诊断消费，**尚未接入 Java 测试，因此不是两端共同通过的合同测试**。不把本样例加入发布门禁。

已核对后端入口（相对于 api 仓库）：
- `agent/jia-agent-service/src/main/java/cn/jia/agent/api/PersonalWorkspaceExecutionController.java`
- `agent/jia-agent-api/src/main/java/cn/jia/agent/service/PersonalWorkspaceExecutionService.java` 的 ExecutionSummary/ExecutionCursor/ExecutionHistoryView
- `agent/jia-agent-service/src/test/java/cn/jia/agent/api/PersonalWorkspaceExecutionControllerTest.java`：已有摘要白名单、private/no-store、非法游标、缺失 scope 的 MockMvc 测试；本轮没有重跑，也不是数据库链路证明。

后续实现保持同一份 JSON，不复制成第二套期望值：
1. 在独立固定 API 源码工作区将 JSON 作为显式测试资源输入并记录摘要；后端真实序列化结果与样例比对，非法游标须断言未调用 service。
2. 增加隔离数据库的合成 owner-A/owner-B 数据，走真实认证/Controller/service/DAO，证明隔离、游标顺序与无创建/派发副作用。不要使用生产数据或其他任务数据库。
3. 将真实 HTTP 响应交给前端消费者，保留请求认证、状态码、缓存头及身份切换回归。后端先读相关 build.gradle，经编排入口串行执行，并保留 validateLayering；前端正式验证仍走 Flow。

以上未完成的层级均为 NOT_RUN；本轮没有后台服务、数据库 fixture 或生产访问，因此不宣称最小真实跨端链路已打通。

## 本轮证据

- Python 开工工具：15 项隔离测试通过，原编排器19项回归通过。
- 前端消费者：5个共享样例＋一次跨页消费，30条断言通过；没有触发全量测试/生产构建。
- 首轮诊断发现测试脚本只传 append=true，未显式传 cursor；按真实 loadHistory 签名修正脚本后通过。原失败保留，未修改产品代码来迎合测试。
- 日志与文件摘要见根任务 handoff `docs/implementation/handoffs/DEV-FEEDBACK-PILOT-20261008.md`；这不是正式验收证据缓存。
