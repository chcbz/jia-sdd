# 产物交付验收计划

当前状态：OD00 本地依赖与跨模块事务开发门槛已通过；OD01 在 `c5330dd5` 获独立开发门槛 APPROVE，最新去重修复证据为 280 项通过，见 [evidence/OD01/accepted-review-c5330dd5.md](evidence/OD01/accepted-review-c5330dd5.md)。OD02 在 `a04c2feb` 已通过独立开发复审，见 [evidence/OD02/accepted-review-a04c2feb.md](evidence/OD02/accepted-review-a04c2feb.md)；OD03 在 `4c292cc3` 通过独立开发复审（[证据](evidence/OD03/accepted-review-4c292cc3.md)），OD04 在 `29aa70da` 通过独立开发复审（[证据](evidence/OD04/accepted-review-29aa70da.md)），OD05 共用成果前端实施中；以下端到端取件/交付场景仍待执行；尚未进行生产迁移或线上验收。本地依赖替换与后续门槛见 [evidence/OD00/downstream-gates.md](evidence/OD00/downstream-gates.md)，逐项状态见 [task-ledger.yaml](task-ledger.yaml)。

## 必须通过的可观察场景

| ID | 场景 | 期望结果 |
| --- | --- | --- |
| O01 | 本地 Agent 对话生成 PDF/PNG/文本 | 用户看到对应成果，下载 bytes 的 SHA-256 与受验证快照一致 |
| O02 | 托管 Agent 通过 manifest 指定代码文件、patch 或说明包 | 指定成果均可获取且快照 hash 一致；R1 不承诺自动发现全部 Git 变化，自动完整补丁增强按 execution-plan 第9节延期 |
| O03 | 产物登记后关闭 Agent、归档执行目录 | 用户在保留期内仍能下载，文件不依赖原目录 |
| O04 | 文件上传中断、完成 ACK 丢失、客户端重启 | 原幂等操作恢复；不重跑模型、不产生重复成果版本 |
| O05 | 会话关闭再打开、SSE 断线和事件乱序 | 通过列表恢复一致视图，不丢附件、不以重复事件重复创建卡片 |
| O06 | 超过最近 100 条成果 | 可分页找到历史产物；工作台明确显示截断 |
| O07 | 用户 A 访问用户 B 的 ID、同 scope 无权产物、过期绑定、伪造 source | 列表/详情/下载/事件均拒绝；不能通过 objectId 或 actorAgentId 绕过 |
| O08 | 发布人没有可选 Agent / 工作台开关关闭 | 仍能从榜文获取明确交付给自己的文件和验收 |
| O09 | Agent 私有草稿与他人 reviewer 成果 | 不会因拥有 Agent、taskId 或被协调者引用就泄漏给发布人 |
| O10 | 路径穿越、符号链接替换、FIFO、导出期间修改文件 | 拒绝越界/特殊文件；快照边界生效；正文与登记哈希一致 |
| O11 | hash 不符、伪 MIME、超限、恶意 HTML/SVG/ZIP | 不登记为可用文件，不在主站执行；上传失败原因可理解 |
| O12 | 对象先上传后 DB 回滚、GC 与引用并发 | 重试可完成；孤儿可清理，已引用对象不被 GC 误删 |
| O13 | 需要文件的悬赏只回报 completed | 不进入新规则的正式交付完成/验收状态，明确提示缺交付件 |
| O14 | 纯文本结论任务 | 可提交有效文本成果，不要求无意义附件 |
| O15 | 多文件悬赏提交 | 所有项 READY、scope 正确、版本被冻结；部分上传失败不能提交完整交付 |
| O16 | 迟到租约、并发重分配与提交 | 正式结果不能被旧执行覆盖；候选文件与正式交付清楚区分 |
| O17 | 提交 v1 后发布 v2，再验收 v1 | 验收的是冻结的 v1；旧 revision 已失效时返回 409，而非默默替换 |
| O18 | 双击验收、同键异参、验收与返工并发 | 只发生一次合法迁移，有审计且可恢复，冲突不会误完成任务 |
| O19 | 旧正文、旧外链、legacy_result、历史本地文件 | 如实区分可导出、未托管、无成果、可补交；不捏造历史交付 |
| O20 | 到期保留、争议保全、Agent 解绑 | 到期预警正确；保全防止清理；解绑不抹去已交付副本 |
| O21 | 桌面/移动浏览器、微信 WebView 真机 | 可完成受支持格式取件；受限环境有已验证的授权替代入口 |
| O22 | 新旧 Agent 混合、存储临时失效 | 新要求文件任务不分配给不支持者；暂停写入仍保留可用读路径 |
| O23 | 大小写/尾空格身份变体、通用 conversation get、伪造 runId、历史归属冲突 | 精确 scope/owner/run 验证拒绝；不借通用查询或回填扩大权限 |
| O24 | 对新策略任务分别调用 legacy completed、旧 result commit、直接状态更新、WS/HTTP 双入口 | 所有路径服从同一交付提交事务；不能缺 delivery pin/冻结版本就完成 |
| O25 | 引用到期/用户删除/争议 hold/GC/下载同时发生 | 固定锁序无死锁；活跃 pin/hold 阻止误删；DELETING 不接收新引用；过期版本不因其他引用残留而恢复访问 |

## v1.1 新增实施验收

| ID | 场景 | 期望结果 |
| --- | --- | --- |
| O26 | trusted run创建、WS ticket交换、跨binding与重启恢复 | ticket只单播桥接进程；run不能伪造；新runtime不能借恢复取得旧lease |
| O27 | PUT断流/超时、旧writer晚到、重复complete | epoch隔离和CAS阻止旧字节覆盖；VERIFYING持久恢复；真实hash一致 |
| O28 | 并发超配额、重复上传、失败/删除计数 | 锁内预留，额度不超卖/重复扣占；GC释放真实占用 |
| O29 | ROLE_CANDIDATE/OWNER_SHARE/READ_PIN及正文成果 | 只有明确分享/交付授权可取件；读取pin不扩大ACL，正文不绕过权限 |
| O30 | manifest越界/重复ID/队列损坏/重启 | 失败关闭，快照先持久再解锁，网络重试不增加模型执行次数 |
| O31 | policy1新任务通过旧点将/组队/增工作项/legacy result尝试绕过 | 服务端只允许单Agent单required work item，旧完成路径全部拒绝 |
| O32 | 提交后要求修改再重新执行 | submitted→ready；旧批次终态；新run/lease及revision，不自动执行 |
| O33 | rework双击/响应丢失、revision/attempt耗尽、旧批验收 | 唯一outbox/receipt；不重复执行、不暗中重置次数，旧版本409 |

R1/R2分别按[execution-plan.md](execution-plan.md)第9节执行门槛；O01本地/托管以R1支持的Linux平台为界。多人正式验收、目录浏览、原生下载bridge尚不在本轮支持清单。

## 后续资金联动专属门槛

- [ ] 先给出实际资金后端仓库/commit/接口/托管状态机证据。
- [ ] 验收事件重复投递、结算超时/重试均不重复扣款或发放。
- [ ] 已验收但结算待处理与未验收的 UI/账本状态一致。
- [ ] 算力成本、悬赏报酬、退款/争议规则分别有契约与账本测试。

## 实施时需记录的证据

- API：上传/ACL/幂等/引用与 GC/租约/验收真实事务测试；每条 Gradle 命令持 `/tmp/cyf-gradle.lock`。
- Client：导出安全、执行锁与上传快照、重启队列恢复的 Node 测试。
- Web：成果列表、下载错误、刷新恢复、验收版本冲突的相关测试与生产构建结果。
- 集成：两个 Agent 部署模式 + 三类文件，用户实际取件和离线取件结果；桌面与移动环境证据。
- 发布：API/Web/client 三仓版本、迁移、存储配置、能力协商、灰度实例及用户阶段确认。

## 本次方案检查

- 已检查 API/Web/Agent 客户端源码与本地基线；主分析不依赖历史设计文档认定功能已实现。
- 仅新增设计文档与项目入口索引；不修改 API/Web/client 实现及其 gitlink。
- 文档相对链接、空白、YAML 格式与 Draft/未 pin 状态检查通过；API/Web 工作树未修改。
- 独立只读架构评审提出身份归属、唯一提交事务、引用保留/GC 三项方案阻塞，已修订并经复查确认无方案级阻塞；对应负向与并发场景为 O23～O25。
- 复查额外提醒的 scoped 会话 DAO `'0'` 兼容分支/jiacn 校验已明确写入 design 第 6 节。上述评审是设计审查，不代替实现测试或上线验收。

## v1.1 文档验证（本次详设）

- OpenAPI结构/21个operation的路径参数与认证/279个内部引用检查通过；36个JSON Schema元定义、7组正常示例、4组应拒绝的schema反例检查通过。使用Python jsonschema Draft202012Validator及结构检查，未运行独立完整OpenAPI工具链或真实API测试。
- 12张新表契约、4组旧表扩展的索引列引用检查通过；12个任务无缺失依赖/环、全部not_started，R1合计7～10、R2追加5～7.5人日。文档链接/空白/YAML通过；API/Web工作树未修改。
- v1.1独立只读设计复查无设计级阻塞；submit不要求预先OWNER_SHARE、R1对话只覆盖真实工作空间Agent的两条提醒已明确。最终恢复契约增补复核亦无新增阻塞；须在实施中测试提交/返工/新旧run领取并发，以及成功提交丢ACK后的终态receipt恢复。

- 能力协商细化为独立runtime outputCapabilities快照（注册/心跳扩展），不混用业务abilities；实施OD01验证旧客户端缺失、旧runtime晚到、过期快照及R2能力误报拒绝。
