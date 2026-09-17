# 1.7.0 详细设计：经济与技能市场只读预览

2026-09-17；契约版本 `economy-readonly-v1`。这是待实现契约，不表示下列新接口已经上线。

## 1. 已核对基线及问题

2026-09-17 通过远端 `ls-remote` 核实：
- API origin/develop及冻结release/1.6.0：`a8e9170873062165176626775d66c92dfc2e7a1a`，tree `7ed64de0a3519b18b14f1ea8fe82463fa0993679`。
- Web origin/develop及冻结release/1.6.0：`74420db2c82fb2f5dee673f337c13bb546d53f93`，tree `4e4b4924ea7bb3a26b649726424f3ae2b81a4202`。
- primary本地develop落后且有其他任务脏改，不作为开发起点，不reset、不移动既有release。

现有实现并非空白：
- `web/src/components/Wallet.vue`、`web/src/utils/silverAmount.js` 已有钱包/流水与安全整数显示。
- `web/src/components/economy/SkillMarket.vue`、`web/src/composables/useSkillMarket.js` 已有商品/购买/权益流程。
- `web/src/components/juyiting/HostingRentPanel.vue`、`web/src/composables/juyiting/useHostingRent.js` 已有租金交易流程。
- API `EconomyWalletService.wallet/ledger` 是可复用的只读查询；`SkillMarketplaceService.catalog` 却依赖可交易/派发条件；`SkillAgentVersions.requireOwned` 内会ensure/advance版本，不能误作只读校验。
- 既有悬赏/技能/租金POST quotes会创建记录；技能purchase冻结资金并生成安装意图。不能仅将按钮换成“预览”后调用原链路。
- 既有 `FundedBountyPreviewPriceBook` 明示 `SYNTHETIC_PREVIEW_FIXTURE_NOT_PROVIDER_PRICING`，不是OpenAI实时价格；复用计算器但不改变/冒充生产价。

## 2. 页面与用户流程

新增 `/economy-preview`（认证路由），从个人中心进入；本轮不改 `/wallet`、`/skill-market`、张榜/点将既有交易行为。原链接保留原开关，新增入口不得跳转到购买确认页。

总览固定横幅：“只读预览：本次操作不扣款、不下单、不安装、不启用托管”。五个分区：
1. 钱包：真实可用/冻结SILVER、最近流水及加载更多；没有账户成功读到零可显示0，接口失败绝不显示0。
2. 悬赏试算：预算、最低预期收益、预计/最坏四类token输入；显示计算费用/平台费/Agent预计收益/预算是否覆盖。标明示例价表，结果不是可提交的报价。
3. 技能目录：名称、版本、目录标价、权限、部署限制；详情动作叫“查看详情”，无购买/下载/安装动作。
4. Agent状态：显式选择roster中自己的Agent，权益状态与安装证据分两列；离线、证据过期、无证明、未知分别展示。不因为权益ACTIVE或自由文本ability就显示“已安装”。
5. 托管：local显示“不适用/不收租”；server显示参考方案的价格/周期及已有租约（如有）。不出现续费、开通、重整按钮。

每张卡片状态：idle/loading/ready/empty/unavailable/error；身份失效单独处理。卡片失败只影响本卡，可手动重试；不无限自动重试/轮询。移动端可纵向滚动，详情可关闭，金额长文本不撑破布局。

## 3. 独立只读边界

新增后端 `economy.read-only-preview.enabled`（缺省false）与Web `VITE_ECONOMY_READONLY_PREVIEW_ENABLED`（缺省false）。新API命名空间 `/economy/preview/`，不修改既有 `/economy/capabilities` 语义，不开启 `economy.preview.enabled`、`economy.skill.marketplace.enabled`、发银或托管收费开关。

认证成功且新开关启用即可按自己的scope读取，不新增用户allowlist。身份来自受信JWT `jiacn/client_id/sub`，沿用有效身份解析规则，缺失拒绝；不trim、不大小写折叠、不把tenant='0'或默认用户自动归属给当前人。schema/数据不可用只影响相应能力，不要求启用交易才能读。

预览服务只注入读取端口/纯计算器；不得依赖posting/treasury、命令publisher、购买/续租/quote写服务、provisioner。现有Service只有经证明无副作用的读方法才可复用。`@Transactional(readOnly=true)`不是零写入证明，测试须断言无INSERT/UPDATE/DELETE/outbox/网络调用，且不调用FOR UPDATE读取后ensure的旧路径。

## 4. API合同

统一 `JsonResult`：成功 `{code:"E0",data:...}`；失败 `{code:"稳定错误码",message:"用户可读说明"}` 并保留真实HTTP状态。所有响应 `Cache-Control: private, no-store`。金额、版本、毫秒时间戳用十进制字符串；不经浮点。

| Method / Path | 输入 | data成功响应 | 范围与限制 |
|---|---|---|---|
| GET `/economy/preview/capabilities` | 无query | 下方固定结构 | 验证身份；关开关返回enabled=false，不假称故障 |
| GET `/economy/preview/wallet` | 无query | `{currency,availableMicro,heldMicro,version}` | exact tenant/client/actor；复用一致快照，不创建账户 |
| GET `/economy/preview/ledger?cursor=&limit=50` | 延用钱包cursor/limit规则，limit≤100是既有分页契约 | `{items:[{transactionId,entryId,businessType,businessRef,direction,amountMicro,status,postedAt}],nextCursor}` | scope在每页SQL再次校验；cursor不授予权限 |
| GET `/economy/preview/skill-products?offset=0&limit=50` | 非负规范offset，limit 1..100（复用已有目录读取范围） | `{items:[Product],nextOffset}` | 同tenant/client已发布商品；limit+1判定有无下一页；不种子、不读取ZIP/私密凭据 |
| GET `/economy/preview/skill-products/{productId}` | exact ID | `Product` | 只读join已发布商品与有效版本，不经交易gate |
| GET `/economy/preview/agents/{agentId}/skills` | 显式agentId | `{agentId,entitlements:[],installationEvidence:[],observedAt}` | 服务端只读核实当前拥有关系；非owner/不存在统一404 |
| GET `/economy/preview/hosting-plan` | 无query | `{source,planVersion,amountMicro,periodSeconds,currency,activationAllowed:false}` | 当前配置或既有参考方案；无有效描述时503，不伪造价格 |
| GET `/economy/preview/agents/{agentId}/hosting-lease` | 显式agentId | `{agentId,applicability,lease:null\|{leaseId,version,status,planVersion,amountMicro,periodSeconds,paidFrom,paidThrough}}` | 当前owner可读；local为NOT_APPLICABLE；无租约是null |
| POST `/economy/preview/bounty-estimates` | 下方规范输入 | 下方试算结果 | 仅纯计算，无taskId/quoteId/orderId，无任何落库或Provider请求 |

`Product`只暴露 `{productId,name,description,productVersionId,skillKey,skillVersion,priceMicro,permissions,deploymentRestriction,priceSource:"CATALOG",purchaseAllowed:false}`。不是`canPurchase=true`的原交易DTO。不返回包下载地址、服务器路径、Provider凭据。目录采用现有排序、返回nextOffset；分页期间数据变化可刷新，不承诺全量历史快照。

capabilities固定结构：
```json
{
  "contractVersion":"economy-readonly-v1",
  "mode":"READ_ONLY_PREVIEW",
  "enabled":true,
  "principalScopeFingerprint":"opaque-exact-actor-scope-fingerprint",
  "features":{"wallet":true,"ledger":true,"catalog":true,"installationStatus":true,"hostingPlan":true,"hostingLease":true},
  "actions":{"estimate":true,"issue":false,"purchase":false,"settle":false,"refund":false,"install":false,"hostingActivate":false,"hostingRenew":false}
}
```
features/actions.estimate由开关和已实现读取能力计算；不可将未实现接口标true。此结构不保证每次读取成功，真实DB错误仍响应503。mutation flags固定false，不接受客户端覆盖。关开关时所有features/estimate为false。fingerprint仅用于浏览器隔离，不是授权凭据。

试算请求（所有数字为规范非负decimal-string，long范围，estimated逐类不得大于worst）：
```json
{
  "grossBountyAmountMicro":"1000000000",
  "minimumAcceptedPayoutMicro":"0",
  "estimatedTokens":{"input":"18000","cachedInput":"4000","output":"6000","reasoning":"3000"},
  "worstTokens":{"input":"36000","cachedInput":"8000","output":"12000","reasoning":"6000"}
}
```
响应包含 `mode:"SIMULATION"`、`charged:false`、`persisted:false`、`currency:"SILVER"`、`priceBookVersion`、`rateProvenance:"SYNTHETIC_PREVIEW_FIXTURE_NOT_PROVIDER_PRICING"`、回显token类别、`estimatedComputeMicro/worstComputeMicro/platformFeeMicro/estimatedAgentPayoutMicro/worstAgentPayoutMicro/budgetHeadroomMicro` 和 `budgetCovered`。输入溢出/负数/未知字段/重复key/错误类型拒绝，不能悄悄截断。复用 `FundedBountyQuoteCalculator.calculate`，保留其BigInteger中间运算和上取整；缓存输入与普通输入不重复计价。费率只作示例，本轮不更新价格。

此POST是计算RPC，不落正式quote，不需Idempotency-Key；同输入同priceBookVersion同结果，可手动重算，不产生订单重试。旧quote/claim/order/bind等仍走自己的原ACL及授权，不接收预览结果作为资金凭证。

错误：401 `UNAUTHENTICATED`；403 `PREVIEW_SCOPE_UNAVAILABLE`或`PREVIEW_DISABLED`；404 `PREVIEW_RESOURCE_NOT_FOUND`（Agent越权/不存在不区分）；400 `PREVIEW_BAD_REQUEST`；503 `PREVIEW_DATA_UNAVAILABLE`/`PREVIEW_PLAN_UNAVAILABLE`。其他网络错误保持失败，不包装为空列表或成功。

## 5. 数据、安装事实及ACL

- SILVER与旧point独立；1 SILVER=1,000,000 micro-silver，沿用既有精度，不在本版本增加人民币支付/兑换承诺。
- 钱包/流水归tenant+client+actor；目录归tenant+client；Agent状态和租约必须另验证actor的当前拥有关系。只看client或agentId不够。
- 复用账本/商品版本/权益/安装/租约表，不建新钱包、订单、安装事实源。按existing schema检查SQL的真实二进制比较/排序规则；不能仅凭注解或字符长度声称byte-exact。大小写、尾空格、前缀、tenant与client交叉fixture须证明隔离。
- 安装投影字段：`installationId,skillKey,skillVersion,status,evidenceKind,verifiedAt`；只有现有可验证安装记录/ACK关联证明可标VERIFIED_INSTALLED。权益ACTIVE不代替它；不支持的证明或没关联记录显示UNCONFIRMED，不能由本轮客户端制造确认。既有历史证据不等于当前在线运行健康。
- 本轮预期**不需DDL/生产DML/seed**。实际缺表或字段时先显示该卡不可用并记录，不自动迁移、不补假数据；如确需迁移，另交精确变更与授权，不把缺口藏进发布脚本。
- read-only owner lookup不能复用会ensure/advance版本的`SkillAgentVersions.requireOwned`；用纯SELECT验证现有绑定，事务内读取一致快照。绑定切换后新请求重新验权，客户端同时丢弃旧请求。

## 6. 前端实现与兼容

新增独立preview composable/API适配器和只读页面；复用`silverAmount.js`与商品/流水纯展示片段，避免复制完整交易状态机。第一个轻量切片为无框架依赖的`src/utils/economyReadOnlyPreviewPolicy.js`与Node定向测试，冻结capability接纳及scope响应围栏。

状态由认证generation+scope fingerprint+agentId+request generation绑定；钱包/目录/试算等无Agent上下文必须显式使用`agentId:null`，缺失/空串无效，null与实际Agent切换也须丢弃旧响应；logout/login/client切换先清空所有卡片与试算，取消本任务fetch，任何迟到响应不提交。预览数据只放内存，不写原交易journal，不恢复/重放历史purchase请求。缺字段/未知契约/mutation=true能力不得放行写动作；显示协议异常并保留文字聊天等正常能力。

不重构张榜、点将、阅读、成果取件、横竖屏、语音或Agent WebSocket协议。`/agent/map`和`/agent/roster`继续分开；roster沿用POST查询而非臆造GET，显式target不依赖地图隐式选中。只读状态展示不要求离线Agent变在线。

## 7. 验证、交付和风险

详见`acceptance.md`。最核心证据是：开启新preview、关闭全部旧交易开关，仍可读自己数据/做试算，业务写表和外部副作用为零；双身份双client不能交叉读；旧功能不回退。

责任Owner自检，不设独立Reviewer。API/Web可在独立worktree并行；Gradle经orchestrator串行；只有契约联调/集成和部署顺序串行。组件自检合origin/develop（快进/精确merge，不覆盖其他提交），相关测试通过后创建新的冻结release/1.7.0，记录前后端commit/tree、测试与制品SHA、`build_origin=local_user_authorized`；云效恢复前本地发布，不伪造Flow Run。

本请求启动开发，不等于此刻操作生产。发布阶段依现有授权、实际健康、进程归属和互斥由指定Owner执行；先API新增读接口再Web新入口，保存可恢复安装。新只读开关需在发布包配置中明确启用并做认证验收，不能以默认false的隐藏页声称交付可用；旧交易开关保持发布前值，不因预览被启用。旧release/1.6.0不移动。故障优先关闭新入口，不关闭旧聊天/阅读服务；恢复版本时记录真实产物，不以无关性能阈值阻止服务。

风险：①把老quote当无副作用读取；②scope查询/安装“成功”误判；③不存在的表被伪空处理；④金额精度；⑤新开关误启收费；⑥磁盘实际不足。前五项用最小相关测试；磁盘按实际构建/制品/恢复副本测算，不增加任意10G门槛。2026-09-17盘点时仅18MiB可用且在下降，因此目前只执行文档和轻量切片，未启动构建；需查明增长来源并由其Owner处理后安排构建，不能在没有空间证据时承诺发布时间。
