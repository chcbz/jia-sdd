# 冻结契约与边界

## API（JWT owner-only，private/no-store）
- `GET /agent/personal-workspace/executions?limit=20&beforeCreatedAt=<ms>&beforeExecutionId=<id>`：游标两项必须同时有或同时无；limit 1–100 为分页长度，不是性能取消阈值。按 created_at DESC、execution_id 字节序 DESC，以 limit+1 判断下一页。
- 返回 `{items:[{executionId,targetAgentId,state,outputContentMimeType,createdAt}],nextCursor:{createdAt,executionId}|null}`。不返回私密需求/输入正文/运行凭证；无条目不等于加载失败。
- `GET /agent/personal-workspace/executions/request`，以 `Idempotency-Key` header 查原请求：返回现有 ExecutionView，未查到404/EXECUTION_NOT_FOUND。只读，绝不调用 create。404不能证明在途POST以后不会提交。
- tenant/client/owner 严格匹配，数据库大小写/空白折叠不能扩大作用域；保留服务层防御校验。沿用现有400/404/503错误合同。
- 既有 `POST /internal/agent/tasks/{taskId}/runs/{runId}/failure` 仅补 runtime filter 的精确允许路径；仍验证 native-only、无Origin、有效runtime token、agent/runtime/owner，浏览器JWT不获得能力。

## 前端
- 提交后在当前交付台显示真实回执、执行者、编号与状态；QUEUED只解释为已受理且等待结果，不推断模型运行阶段。
- 当前在途/未知意图不允许再次普通提交；程序层防连击，不仅禁用按钮。传输未知查询同一个幂等键，不自动重发。
- 历史从服务端读取并可分页/选中恢复；选中/轮询/加载并发不得用旧回包覆盖新状态；身份变更立即清理。
- 仅可按已确认owner/client命名空间保存小型待核对key/执行ID；不能保存令牌、密码、私密正文或文件内容。服务端身份校验不依赖浏览器缓存。
- 关闭页面不是取消后台执行。文件详情返回真实select结果，才能从列表打开。

## 风险、发布、兼容
无DDL、无生产DML、无运行重派发。先验证API兼容现有前端，再发布配套前端；旧API上历史404必须呈现暂不可恢复，不伪报空。当地本地发布授权有效，不触发Flow；精确SHA、相关测试、制品哈希、互斥与实际健康仍必须保留。已有失败记录修复必须另有精确恢复授权，不能因上线而推导。
