# 通用点将 → 自动议事：新主路径合同（2026-10-03）

## 决策与边界

遵循用户“无需做太多兼容补丁，一切都按新方案实施”：普通需求统一添加资料、显式点将、自动悬赏议事。新点将不要求选择生成图片/编辑图片/资料用途，不以原生绘图能力或独立 Images API 配置作为进入议事的前提。旧操作只保留未完成请求与已有内容保护，不再为旧生图入口增加产品分支。

本合同落实**点将与自动首轮议事源码**，不等同于完整多媒体交付已完成。API、Client 候选仅推送特性分支；Web 新点将接线、自动查阅/执行、真实媒体与正式验收仍待完成，没有此次发布或线上成功证据。

## HTTP

- `POST /agent/tasks/{taskId}/point-and-deliberate`
- `GET /agent/tasks/{taskId}/point-and-deliberate/request`
- 两者均要求 owner JWT、tenant=0、唯一 `Idempotency-Key`，禁止 query 覆盖身份/意图；响应 `Cache-Control: private, no-store`。
- POST JSON **只允许**下面三个字段；版本为 canonical decimal string，不允许数字强制转换、重复字段、尾随 JSON、客户端资料目录/权限/绘图参数。

```json
{"targetAgentId":"agent-id","expectedTaskVersion":"0","requirementRevision":"1"}
```

POST 成功返回 HTTP 200 + 现有 `JsonResult.data` 内的 `AssignmentOperationView`；含原 task/target、字符串版本、grant/bootstrap 状态、冻结 inputs 目录、`initialOperation=DELIBERATE`。PENDING/CLAIMED/RETRY 不是 Agent 已收到或需求完成；ADMITTED 才具有 conversationId/initialRequestId，依然不是执行成功。GET 只读，不重新创建、补发首轮或调用 Provider。

POST 事务提交后若投影读取失败，浏览器须保留原键与原正文并核对原请求；不能因此生成新键或回退 `/assign`。400 格式错误，401 身份不成立，404 请求/目标/资料不在授权范围，409 原键异意图或版本冲突；持久态/来源故障维持真实 5xx。错误不返回数据库、私有路径或密钥。旧 image 操作不能被新 GET 解释为 DELIBERATE。

## 服务端点将事务

1. owner-scoped task-root 锁下核对服务端不可变需求修订。
2. 首次请求读取该任务全部 ACTIVE INPUT/REFERENCE 关联，固定 fileId/version；从真实版本读取 MIME/字节数/SHA-256。输出不是输入资料；同文件不同版本不合并。相同版本若有两历史关系只保留一次，内部优先 INPUT。
3. 全目录按既有32版本存储容量核对；非输入关联造成分页时继续读取，不把第一页误当全集。超限明确失败，不丢弃第33项。scope、失效文件、关联、版本均必须重新验证。
4. 复用原任务指派/grant/bootstrap outbox 同一事务。新初始操作为 DELIBERATE；基础操作集合为 DELIBERATE + INSPECT_INPUTS，**没有 GENERATE_IMAGE、paidExecutionAuthorized 或 costAuthorizationRef**。
5. 原键重放从原 grant 输入快照重建意图，不混入后来补充的资料；原目标/版本/正文哈希仍核对。下游 admission 仍检查当前 assignment/grant，不把历史重放当当前执行权。

没有新增文件系统、历史回填、表或 DDL；资料用途字段仅为内部精确 ACL 关系，不变成 UI 入口。

## 自动首轮

- Bootstrap 消费前复核完整需求修订及资料摘要；通过现有 grant admission 和 task/binding/conversation 锁序建立唯一 bounty 会话。
- DELIBERATE 复用 `ChatTypedDiscussionAdmissionService`，把完整 `title + description` 和全部精确选择器送入 DISCUSSION。稳定首轮 key 由原 sourceBusinessActionId 及作用域派生。
- typed admission 持久化源目录及 durable CHAT request/turn/outbox；Agent 可以 ANSWER、CLARIFY 或提出后续执行建议。重复消费复用原 typed receipt。
- 初始 CHAT **没有执行 step/executionId**；不插入 WAITING_ADMISSION image link，不伪造正在生图。
- typed 目录支持 INPUT/REFERENCE 精确关系与32项；SQL 保留 owner/client/tenant/task/file/version，并对 link_role 精确匹配。提供目录不等于已读取文件字节。
- Client 同步接收32项混合媒体目录，仍验证来源唯一、媒体类型、会话与目标绑定；不扩大操作或付费授权。

## 源码自检与剩余工作

详见同目录证据 `integration-evidence-20260928/unified-materials-correction-20261003/generic-point-source-progress.json`。

已完成：点将 Service/HTTP 59PASS；bootstrap/typed/事务相关51PASS、3个条件 MySQL 用例未运行；Client18PASS。新 SQL 的精确角色核对目前是单元夹具验证，不冒充真实 MySQL 新路径验收。此前创建/资料选择证据保持独立，不重复累加为全链路通过。

必须继续：

1. Web 普通点将唯一接入此新路径，移除新请求的绘图能力前置和用途选择；保留原在途意图只读保护、身份/代次 fencing、原键恢复与自动会话接入。
2. 资料按需查阅：目前 inspection 仍有 REFERENCE/16 限制，要统一 INPUT/32 与精确 ACL；Agent 自主查阅/执行编排尚未完成。
3. 执行建议 → 实际能力/既有授权校验 → 执行/多媒体实时展示，不强制多一轮用户确认，不把统一授权推导成未授权扣费。
4. 失败终态投影、仅本地 spool 未 STAGED 上传恢复、双接应、真实媒体预览/下载、归档与正式交付验收。
5. 统一候选达到上线条件后按既定版本/Flow 政策发布；保持此前线上版本和已有内容，禁止重放418/419/420或删除 paid claim。
