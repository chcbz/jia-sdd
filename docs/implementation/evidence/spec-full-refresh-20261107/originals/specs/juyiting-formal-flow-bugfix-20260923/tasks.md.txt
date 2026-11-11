# 1.13.19 修复工作拆分（候选已实施，线上验收待办）

版本修复方案：`docs/implementation/V1_13_19_FORMAL_FLOW_BUGFIX_PLAN_20260923.md`。先执行 T0：重新核对线上/远端 develop/版本占用并固定身份、持久派发和正式执行合同。

本文件为需求工作包，不是运行台账；当前唯一运行 ledger 是 `docs/implementation/TASKS.yaml`。不创建独立 Reviewer。

| 工作包 | 责任角色 | 范围 | 依赖/完成标准 |
| --- | --- | --- | --- |
| T1 | API/Chat Owner | BF-01/BF-02：按 owner/tenant/client/member 查明拒发与 404，修合法链路 | 可先做只读归因；补同范围成功与跨范围拒绝测试，不移除 ACL |
| T2 | API/运维 Owner | BF-05：workspace/events 实际 503 分支与能力开关 | 可与 T1 并行诊断；不重启 foreign 进程、不直接把 allowlist 放开为通配 |
| T3 | Web Owner | BF-01 派发子状态/恢复提示；BF-06 完整状态映射 | 展示合同确定后实施；静态映射与 T1 可独立推进 |
| T4 | Web Owner | BF-04：深层百宝箱可查看/返回原任务 | 同层导航方案，不改身份/授权边界 |
| T5 | API+Web Owner | BF-03：正式任务固定版本选材和执行授权 | 先核对/冻结现有能力可复用合同，再端到端接入 |
| T6 | Runtime Owner | 验证吴用/林冲实际 profile、命令 receipt、领取/执行/成果回写 | 依赖 T1 对应派发可用；保留 workspace/lease/幂等隔离，不用裸聊天完成回报替代交付 |
| T7 | 集成测试 Owner | 430×932 UI 同 taskId 全链路、返工、刷新恢复、交付摘要 | T1/T2/T5/T6 前置通过；下游当前 BLOCKED_NOT_REACHED |

建议顺序：T1/T2 确定真实断点；T3/T4 可并行；再 T5/T6；最后 T7。不以所有任务全串行阻塞独立就绪工作。

不创建独立 Reviewer，Owner 自检；身份/事务/租约相关回归必须保留。修复后如需本地测试构建发布，依既有授权由 exact SHA 形成证据；Gradle 只经 orchestrator 串行。本轮已完成本地定向测试、正式构建和联合制品校验；尚未部署、尚无线上业务验收，见 release 计划最新候选实施记录。

### 上线后增量工作包（2026-09-23，原 BF-01..06 非闭环证据）

| 工作包 | 责任 | 不可跳过的完成标准 |
| --- | --- | --- |
| T8 / BF-07 | API Owner | 同一正式 taskId 的 legacy `MEMBER_DONE`/`WORK_ITEM_COMPLETED` 不可在无正式 submitted/用户 accepted 时推进 completed；有凭据/跨 owner/旧版兼容/幂等/CAS/lease 回归，保留 #396 原始结局，不直接 DML |
| T9 / BF-08 | Chat/Web Owner | 在连接中断后用原 conversationId/事件游标安全恢复最终回复；没有 Agent 回话时诚实展示未知，不自动二次发送或自动执行 |
| T10 / 链接回执 | API/Web Owner | 201 缺浏览器可见 ETag 时只读回查唯一精确 relation/version/state，不重复 POST/DELETE；不把缺失回执当成功 |

2026-09-23 22:34 补充：BF-07 两次 Gradle 均被本机内核 OOM 杀掉（非测试断言失败），按相同根因停止重试，需有可验证的隔离构建资源/内存整改再运行；BF-08 日志实证 WebSocket 任务会话错误地把 owner/jiacn 当 task tenant，Chat 修复候选已提交待测试。Web 断流原 ID 只读回查定向 45 PASS，不代表线上回话/全链路通过；新 release/例外发布不可由原 1.13.19 授权自动推出。


## 1.13.22 增量工作（唯一执行台账仍为TASKS.yaml）

- BF10 runtime：严格相关迟到注册ACK修复，候选faf8d1d，110定向回归PASS；待共享服务发布归属/授权及上线实际pickup核验。
- BF11 API/Web：精确owner撤销/过期回收及明确UI入口，先补隔离/CAS/事务/未知POST恢复用例；保留#397，不自动重跑。预备API工作树 `.worktrees/api-1.13.22-bf11`目前为未改动API20基线。
- BF12 API/Web：真实开工事实与主任务状态一致性，排队不得视为Provider运行。
- 集成：保持吴用、同#397、430×932竖屏；服务发布权限与无在途工作核验后继续。正式PDF→返工→验收→归档全部真实通过才通知可验收。


## 2026-09-24 状态补充
- BF10：已获得共享runtime空闲接管授权并部署1.13.22，3个注册ACK；原#397未自动重跑。
- BF11：API精确过期租约回收+owner明确撤销；Web持久未知意图、禁止替代执行、精确只读恢复已实现并通过定向回归。
- BF12：API native start + root-first状态事务、runtime Provider前精确回执确认已实现；真实H2验证通过。API/Web冻结1.13.22、runtime冻结1.13.23，构建/配套部署和移动浏览器业务验收仍待完成。
- 当前流水账只见TASKS.yaml，不把此文档作为运行Owner/门禁状态。

## BF-13（2026-09-24 线上撤销后实证）
- #397 撤销返回 INPUTS_REVOKED、工作项 ready；WORK_ITEM_REQUEUED 正确清空 assigneeAgentId。Web22 却仅接受 ready + 原承办人，误挡再次办理。
- 新增 Web 1.13.23：与现有 API beginTaskExecution 对齐，只允许唯一 required/ready 项 assignee=null 或精确目标；保留任务级唯一点将、会话、主体、身份、快照及多项歧义检查。无 API/runtime 改动，无 DML。
- 55 项相关定向测试通过（含2新增回归）；移动实际验收待部署后继续，不能报闭环成功。

## BF-14（2026-09-24 正式提交503实证）
- #397 新执行 pwe_11fc8a88438f478e86dc354d35bf8632 已真实自动开工，PDF上传201，但正式output-commit返回503，随后failure回执200，交付列表为空；不算正式交付通过。
- 生产只启用私人工作区存储，缺少 task-artifact-storage 开关，工厂默认 Disabled；这是确定缺项，Controller未记录内部异常，尚不能断言503唯一原因。
- 1.13.24_config_only：启用独立私有正式成果存储，目录700/服务用户，保留默认MIME/大小限制及身份隔离。复用已发布API22 exact JAR，不重建、不修改旧冻结分支。
- 两类存储定向回归16 PASS/0 FAIL/0 ERROR/0 SKIP；配置留存前值、候选摘要，等待发布互斥，空队列核验后canonical launcher重启与实际健康核验。
- 发布后继续同#397竖屏验证，未知commit不重试；先读终态及正式交付，再显式新执行。返工、验收、完成、归档尚未通过。

## 2026-09-24 用户追加改版合入
- 将Web `codex/juyiting-lightweight-workbench` / 8f47a12 合入当前244f944，计划Web1.13.24；保留线上API22+BF14配置和runtime23，不回退为改版分支旧配套API。
- 真实合并冲突仅两个测试文件；保留身份恢复回归及新导航回归。现有挂载fixture需补TaskMaterialLinks别名和useFormalTaskExecutionScope，失败按测试装载依赖归因，不删除断言。
- 当前#397在办理中，上一执行已FAILED且正式成果为空；用户追加需求时尚未新发起Provider执行。改版发布后继续同任务430×932验证。

## 改版复测中的后续优化需求（不冒充已修复）
- BF15：正式执行历史只读过滤不能通过逐条“选中执行”遍历所有私人历史；避免无关QUEUED被暂存/轮询并阻断当前TASK。保留原未知POST恢复标识及精确范围检查。
- BF16：工作台SSE重新同步/授权暂不可用时，不应静默清空同身份/任务/会话的办理说明与固定输入勾选。身份或任务切换仍必须清理；权限失效时禁止提交，不保留可用授权。
- BF17：悬赏状态筛选请求竞态需按generation校验，迟到旧请求不能覆盖用户新筛选。
- BF18：本次ACK high-water约3.8万条，runtime拾取#397新执行耗时约5分半，源码每次ACK同步重复扫描全部证据。列为基于证据的瓶颈排查；禁止删历史/绕幂等、锁归属或调大性能超时充作修复。当前已真实STARTED，等待本次正式交付结果。

## 2026-09-24 BF19/BF20/BF21（1.13.25 候选）
- [ ] BF19：正式交付页未接入议事、明确承办人及固定成果，返工入口不可达。通过已核验本榜文议事 scope 接线，成果按交付ID/决定版本匹配，跨身份/榜文/Agent 清空，不自动调用 Provider。
- [ ] BF20：#397 “要求修改”实际返回400。Controller 的 readBounded 循环重复调用 getInputStream，线上 EsRequestWrapper 每次返回新流，使合法body重复直至64KB拒绝。改为单次获取流，HTTP回归全部带真实包装器；保留大小/结构/身份验证。
- [ ] BF21：前端验收把 revision 作为 expectedDeliveryVersion；应发送独立 deliveryVersion（r1 初始决定版本0）。修正合同并回归。
- 已完成：Web1.13.24改版合入上线，#397 正式提交200、r1 PDF五页真实浏览器预览通过，文件hash与artifact一致，独有附件校验码存在。当前仍 submitted，400未产生决定。未宣称闭环验收通过。

## 2026-09-24 BF22 / Web1.13.26
- [x] 要求修改HTTP 200，r1 decisionVersion=1、taskVersion=3、workItemVersion=10；BF20/21真实回归通过。
- [x] BF22代码与26项测试通过：线上会话成果返回已存在的权威taskId，旧前端白名单拒绝整个目录。接纳并校验published taskId；与所选榜文冲突则不作为返工源；不从选中状态替换服务端artifact所属taskId。私人目录不可冒带taskId。
- [ ] Web1.13.26发布及实际返工→r2 PDF→验收→归档。API25与runtime23不变。
- 已实际发生两次构建OOM；本次先确认无在途Provider、保存并关闭本任务浏览器，使用canonical stop暂时停止本任务API25；构建完成/失败均恢复原exact JAR与配置。未影响其他任务进程。

## 2026-09-24 BF23 / API1.13.27
- [x] Web1.13.26已上线，BF22实际回归：任务397目录正常，原output_1/PDF v1返工入口可达。
- [ ] 13:21:36真实UI单次返工POST返回404，未重发。GET file-links仅含原txt INPUT，成果目录PUBLISHED PDF可用；队列要求源PDF具有INPUT/REFERENCE，返工适配器只验证发布来源、未创建输入关联。
- [ ] 修复在原owner/task-root事务内先验证changes_requested+decisionVersion+已发布固定成果，再通过现有TaskLinkService幂等创建精确INPUT，后进入原TASK queue。队列/租约失败整体回滚，保留原产物；不绕INPUT门禁、不放宽PRIVATE/跨任务文件访问。
- [ ] 回归覆盖真实Rework→Execution服务链（不预设已有INPUT）、拒绝异主成果/不可用源文件、保留一般TASK输入限制；本地相关测试/构建和新冻结release后只部署API，Web26/runtime23不动。

## 2026-09-24 14:54 最终执行补充（覆盖上文旧时点待办，不改写失败历史）
- [x] BF19/20/21：正式返工入口、真实包装器body读取、独立决定版本已部署并由同#397真实修改/验收核验。
- [x] BF22：Web26成果taskId严格合同已上线，最终Web28保留；返工源可达。
- [x] BF23：API27精确PDF INPUT关联+原TASK队列同事务，48项相关回归/构建/部署通过；真实返工POST202、运行SUCCEEDED、r2正式提交200。
- [x] 增量合入改版最新e53b3c3；Web28相关268项与构建通过，健康发布。
- [x] 同#397 r2六页核验、UI验收200、completed、UI归档200、整页刷新archived、PDF再次下载摘要相同。
- [ ] BF15–18、BF24–25后续优化，见remaining-bugfixes.md；不是本轮已修。
