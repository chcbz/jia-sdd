# 验收与证据矩阵（D2）

**以下 84 项全部仍是待执行业务验收条件，不是测试通过报告。** 当前源码提交和测试证据见 delivery.md / integration.yaml；组件测试与有界真实 HTTP/JDBC/POSIX/Client fixture 已运行，但不冒充完整 Runtime、部署或真实业务验收。历史 prospective tree 证据原样保留。

机器可读矩阵：[acceptance-cases.json](/home/isp/wsps/cyf/specs/archive-agent-maintenance/acceptance-cases.json)。功能要求见 [spec.md](/home/isp/wsps/cyf/specs/archive-agent-maintenance/spec.md)，合同见 [design.md](/home/isp/wsps/cyf/specs/archive-agent-maintenance/design.md)。

## 1. 测试层级

- API unit/contract：schema、DTO、鉴权、native filter、工具上下文、内容校验、CAS/幂等。
- 隔离 MySQL：真实 FK/CHECK、撤任与发布竞态、原子激活、唯一约束、迁移断点；不以 mock 事务代替。
- Client Node：命令协议、安装证明、固定 origin/资源范围、持久 inbox/断点/重放、凭据不进模型。
- Web unit + browser：reader 兼容、真实 HTTP 边界、身份清理、权限 UI、故障状态、移动布局。
- 集成 fixture：明确授权小型文本，至少一个非 120 回/无序言样本，旧水浒摘要不变。
- 真实业务验收：获授权管理者、真实任职 Agent、真实客户端、确定底本《三国演义》、发布回执、读回及私人数据闭环。

所有 Gradle 必须通过 `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py`，先检查 nearest build.gradle；实际 selector 在实现时按新增测试类确定。此处不伪造尚不存在的可运行测试命令。

## 2. 用例

### 身份与任职

| ID | 场景/触发 | 预期 | 工作包 | 状态 |
| --- | --- | --- | --- | --- |
| AUTH-01 | **普通读者不能任命**：读者调用任职写接口或诱导宋江任命 | 拒绝写入，数据库无任职/授权变化 | M2, M7 | 未执行 |
| AUTH-02 | **显示名不能授权**：另一个 Agent 显示名也叫吴用 | 仅 canonical Agent/binding 的任职有效 | M2 | 未执行 |
| AUTH-03 | **同 owner 任命**：管理者选择自己的当前绑定 Agent | 保存准确 scope/binding/skill/profile；可离线任命 | M2 | 未执行 |
| AUTH-04 | **跨 owner 任命拒绝**：书库管理者指定他人 Agent | 首期拒绝，不能仅凭管理公共书库权获得他人 Agent | M2 | 未执行 |
| AUTH-05 | **换 owner / binding**：任职后 Agent 解绑或变更 owner | 有效任职失效；旧作业写/发布拒绝，历史保留 | M2, M4 | 未执行 |
| AUTH-06 | **撤任线性化**：用数据库 barrier 并发撤任与发布 | 按提交/锁先后产生唯一正确结果，撤任提交后无新发布 | M2, M4 | 未执行 |
| AUTH-07 | **单岗位并发任命**：两个管理请求竞争同一 slot revision | 一个生效，另一个冲突；无两个当前负责人 | M2 | 未执行 |
| AUTH-08 | **仅编修不能发布**：DRAFT_ONLY Agent 调用 native publish | 403；草稿保留，可由有权管理者另行发布 | M2, M4 | 未执行 |
| AUTH-09 | **AUTO 授权交集**：岗位可自动发布但本 job 为 MANUAL | Agent 不能发布；管理者显式发布可成功 | M2, M4 | 未执行 |
| AUTH-10 | **书目范围**：EXPLICIT_WORKS 任职尝试新建别书或改另一本 | 拒绝且无跨 work 数据变化 | M2, M4 | 未执行 |
| AUTH-11 | **全维度隔离**：分别更换 tenant/client/owner/agent/runtime/job/source | 均不可跨范围读取草稿或写入，不泄露资源存在性 | M2, M4 | 未执行 |
| AUTH-12 | **管理权限撤销**：发起者书库授权撤销后后台准备发布 | 原授权不再允许发布；有权管理者可新授权接管 | M2, M4 | 未执行 |

### 原生通道与工具

| ID | 场景/触发 | 预期 | 工作包 | 状态 |
| --- | --- | --- | --- | --- |
| NATIVE-01 | **native 精确路由**：逐个验证新增方法/路径及相邻非法路径 | 仅合同路径可用，Controller/filter 均覆盖 | M2, M6 | 未执行 |
| NATIVE-02 | **认证通道不能混用**：用户 JWT 调 native，runtime 凭据调 admin/me | 拒绝；不提升为另一种 principal | M2 | 未执行 |
| NATIVE-03 | **头与路径歧义**：重复 Authorization/Agent header、编码分隔符、Origin | 失败关闭，不绕过白名单或落入 OAuth 通道 | M2 | 未执行 |
| NATIVE-04 | **请求主体伪造权限**：正文加入 owner/tenant/permissions/其他 draftId | 拒绝未知或冲突字段，无权限升级 | M2, M4 | 未执行 |
| NATIVE-05 | **可信协调上下文**：从普通会话或伪造 persona 调宋江工具 | 服务端不接受模型声称的 coordinator 身份 | M7 | 未执行 |
| NATIVE-06 | **旁路工具隔离**：在典籍协调请求尝试 shell/SQL/任意 URL 工具 | 请求工具集合不提供旁路，业务服务再次鉴权 | M7 | 未执行 |
| NATIVE-07 | **正文提示注入**：来源正文要求调用发布、读密钥或改任职 | 视为纯文本；无越权调用、外泄或隐藏副作用 | M5, M6, M7 | 未执行 |
| NATIVE-08 | **凭据不进模型**：捕获 prompt/tool result/manifest/日志/UI 回执 | 无 JWT/runtime secret/DB credential，bridge 固定 origin | M6, M7 | 未执行 |

### 平台技能与执行资格

| ID | 场景/触发 | 预期 | 工作包 | 状态 |
| --- | --- | --- | --- | --- |
| SKILL-01 | **abilities 不等于安装**：runtime 上报 archive-maintainer 字符串但无安装事实 | WAITING_SKILL，不派发或执行写操作 | M3, M4 | 未执行 |
| SKILL-02 | **平台配置不收费**：关闭技能市场资金操作后安装平台技能 | 安装回执有效；钱包/订单/资金流水均无变化 | M3 | 未执行 |
| SKILL-03 | **包/版本篡改**：下载包或回执的摘要/version/Agent/command 不匹配 | 不能激活安装事实，不触发任职扩大 | M3, M6 | 未执行 |
| SKILL-04 | **安装回执伪造/重放**：普通 HTTP 声称成功，或重放其他 runtime/origin 回执 | 拒绝；同一真实回执重放仅返回原结果 | M3 | 未执行 |
| SKILL-05 | **安装器文件安全**：测试穿越/符号链接/执行文件伪装/损坏归档 | 不写出授权安装范围；失败归因不伪造退款/成功 | M3 | 未执行 |
| SKILL-06 | **在途技能升级/撤销**：任务运行中安装新版本或撤销已绑定版本 | 升级不替换在途包；撤销暂停依赖任务 | M3, M6 | 未执行 |
| SKILL-07 | **老客户端协议不支持**：client 不支持新 archive 命令 | 明确待更新，不降级成自由 shell 或普通文件执行 | M3, M6 | 未执行 |

### 内容、来源与版本

| ID | 场景/触发 | 预期 | 工作包 | 状态 |
| --- | --- | --- | --- | --- |
| CONTENT-01 | **非 120 回 / 无序言**：使用明确合法小 fixture，不满足旧种子形状 | 正常导入并读回，数据库与服务都不硬编码 120 | M1, M5 | 未执行 |
| CONTENT-02 | **来源固定与权利声明**：缺来源摘要/固定版本或必要权利说明 | WAITING_INPUT/校验失败，不擅自选现代底本 | M5 | 未执行 |
| CONTENT-03 | **不臆造原著**：底本缺章，Agent 生成看似合理章节补上 | 来源映射/目录校验不通过，不上架 | M5, M6 | 未执行 |
| CONTENT-04 | **跨语言摘要向量**：Java/Node 对中文、罕见字、换行、JSON 键顺序处理 | 规范化结果/摘要一致，非法 Unicode/重复键拒绝 | M1, M5, M6 | 未执行 |
| CONTENT-05 | **持久化内容再校验**：上传声明摘要正确但存储实际字节损坏 | 发布前读回失败，READY/发布不伪造 | M1, M4, M5 | 未执行 |
| CONTENT-06 | **章节目录完整性**：缺章/重复/乱序/实际目录与冻结来源不同 | 定位具体块与来源差异；真实不完整阻止发布 | M5 | 未执行 |
| CONTENT-07 | **草稿 CAS 与校验失效**：两个编辑写同 revision，或校验后再改正文 | 冲突不覆盖；改动后旧 validation 不可发布 | M4, M5 | 未执行 |
| CONTENT-08 | **READY 不公开**：把成功导入但未发布 editionId 交给读者 | 正文/目录/提问/私人数据新锚点入口均不泄露 | M1, M4 | 未执行 |
| CONTENT-09 | **原子激活**：发布事务中注入失败与重启 | active/publication/job/outbox 全提交或全不提交 | M4 | 未执行 |
| CONTENT-10 | **新版本不覆盖旧锚点**：已给旧版建立进度/书签/手札后发布勘误 | 新 editionId；旧文本/ID/hash 和旧私人数据不变且仍可读 | M1, M4, M8 | 未执行 |
| CONTENT-11 | **下架与默认版选择**：管理者明确下架当前版，不指定替代版 | active 置空、正文有权请求410；不自动退旧版，私人笔记保留 | M1, M4, M8 | 未执行 |
| CONTENT-12 | **同标题/重复新增**：不同 turn 再请求相同标题，含相同/不同 canonicalKey | 提示可能已有作品；唯一 key 不重复，不能自动覆盖不同作品 | M4, M7 | 未执行 |
| CONTENT-13 | **固定来源/网络出口**：传入任意 URL、重定向内网或读非授权文件版本 | 来源适配拒绝；不向外部 origin 附带凭据 | M5, M6 | 未执行 |
| CONTENT-14 | **XSS/正文指令数据化**：正文含 HTML/script/危险链接 | 阅读纯文本或受控净化，不执行脚本/隐式抓取 | M5, M8 | 未执行 |

### 可靠性与故障恢复

| ID | 场景/触发 | 预期 | 工作包 | 状态 |
| --- | --- | --- | --- | --- |
| RECOVERY-01 | **章节提交响应丢失**：DB 已提交，客户端网络断开 | 按同 key 或 draft digest 恢复，仅一个有效章节 | M4, M6 | 未执行 |
| RECOVERY-02 | **同 key 不同请求**：复用 Idempotency-Key 修改 body/path/候选 | 409，不静默覆盖或生成新操作 | M4 | 未执行 |
| RECOVERY-03 | **未知状态不能当未受理**：POST 仍在途时查询 key 得404 | UI/Agent 仍保留原 key，不能断言失败并另起作业 | M4, M6, M8 | 未执行 |
| RECOVERY-04 | **命令重复/乱序**：重复 delivery 或旧 epoch start/write/result | 同执行幂等；旧 epoch 拒绝；ACK 不置 PUBLISHED | M4, M6 | 未执行 |
| RECOVERY-05 | **离线和慢处理**：断连/长时解析/性能超过历史 SLO | 作业等待/继续；不因预算不足取消或跳过后续步骤 | M4, M6, M8 | 未执行 |
| RECOVERY-06 | **同实例重连/新实例恢复**：分别断线同 runtime 和换 runtime | 同实例可恢复；新实例须正式恢复并隔离旧 epoch | M2, M4, M6 | 未执行 |
| RECOVERY-07 | **临时对象写入后崩溃**：对象成功但 DB 引用未提交 | 原操作恢复或清理本命名空间孤儿，不影响其他任务 | M4 | 未执行 |
| RECOVERY-08 | **READY 后激活前崩溃**：正文完整 READY 但无 publication | 有权同 operation 恢复，读者此前不可见 | M4 | 未执行 |
| RECOVERY-09 | **发布后通知丢失**：publication 提交后 outbox 暂时失败 | job/result 可查询；投影最终收敛，不重复发布 | M4, M7, M8 | 未执行 |
| RECOVERY-10 | **并发版本发布**：两个 job 指向同 (expectedWorkRevision, expectedActiveEditionId)，另测 active A→B→A | 只有一个成功，另一个明确 CAS 冲突，不后写覆盖 | M4 | 未执行 |
| RECOVERY-11 | **显式取消/移交**：在运行时由有权管理者取消或移交 | 旧执行后续写拒绝，草稿/历史保留；不操作 foreign 进程 | M2, M4, M6 | 未执行 |
| RECOVERY-12 | **事件恢复与游标**：重复乱序事件及过期 cursor | 按 sequence 幂等；返回 RESYNC_REQUIRED 并取真实快照 | M4, M8 | 未执行 |
| RECOVERY-13 | **根因有界重试**：同输入相同错误连续两次 | blocked_root_cause；修复后才新 attempt，历史失败保留 | M4, M6 | 未执行 |

### 用户闭环与兼容迁移

| ID | 场景/触发 | 预期 | 工作包 | 状态 |
| --- | --- | --- | --- | --- |
| UX-01 | **旧水浒启动不夺指针**：已有后续合法版本时重启 archive bootstrap | 不切回种子版，不重写原文/摘要 | M1 | 未执行 |
| UX-02 | **新旧 schema 桥接**：空库、旧库、已迁移库及中断迁移恢复 | 初始化/schema 校验兼容，步骤可恢复，无误删个人数据 | M1 | 未执行 |
| UX-03 | **旧 API shape 不变**：旧客户端使用 /archive/v1/catalog 和原 question 入口 | 原返回结构/旧锚点解释兼容，不把 catalog 突变数组 | M1 | 未执行 |
| UX-04 | **新增书阅读全链路**：选择新增书，阅读、续读、书签、手札、选文提问 | 全按新 edition/manifest 验证和 owner 持久化，不回落水浒 | M1, M8 | 未执行 |
| UX-05 | **进度初始化顺序**：已有后段进度，从书架进入/刷新 reader | 先读进度再开章；自动保存不覆盖为卷首 | M8 | 未执行 |
| UX-06 | **跨书/跨身份缓存**：切换书、版本、账号并模拟旧响应晚到 | 不会错书/泄露进度手札草稿，身份变更取消旧请求 | M8 | 未执行 |
| UX-07 | **真实 HTTP/CORS**：真实 createApi→fetch，带幂等/If-Match/JWT；可信/不可信 Origin | 合法预检/ETag读取正确，非授权跨域不放行 | M2, M8 | 未执行 |
| UX-08 | **首次任命用户路径**：无任职，对宋江要求新增书 | 引导明确任命；不自行给任意吴用赋公共维护权 | M7, M8 | 未执行 |
| UX-09 | **缺来源/待技能/离线**：分别触发三种真实阻碍 | 显示准确下一步；不把三者均称执行失败 | M7, M8 | 未执行 |
| UX-10 | **普通读者建议**：普通读者对宋江要求新增公共书 | 明确提示需要书库管理者且未创建维护单，不形成收费执行、建议队列或越权写内容 | M7, M8 | 未执行 |
| UX-11 | **端到端 DRAFT_ONLY**：已任命吴用仅编修，对宋江要求新增固定来源书 | 返回待发布草稿及真实校验，有权管理者可手动发布 | M1, M2, M3, M4, M5, M6, M7, M8 | 未执行 |
| UX-12 | **端到端 AUTO 三国演义**：明确授权的真实底本/任职/AUTO，经宋江交办 | 真实 Agent 完成；服务端publication + 新书读回 + 正确汇报 | M1, M2, M3, M4, M5, M6, M7, M8 | 未执行 |
| UX-13 | **读回失败不重发发布**：publication 已提交，但阅读探测暂时失败 | 报告已提交但读回异常，不重复激活/假报完全成功 | M4, M7, M8 | 未执行 |
| UX-14 | **移动/横竖屏/返回**：真实浏览器视口与键盘缩高、深层返回、焦点 | 关键操作可见，正文/手札有界滚动，回到正确书架/作业 | M8 | 未执行 |
| UX-15 | **权限撤销后前端**：页面仍持旧 capabilities，后台撤任/撤管理授权 | 服务端拒绝，前端清理敏感写状态；不依赖隐藏按钮 | M2, M8 | 未执行 |
| UX-16 | **部署事实不混淆**：核对制品、版本、初始化、runtime、真实内容回执 | 有完整 exact source/test/artifact/online 证据；没有 Flow Run 则不伪造 | M9, M10 | 未执行 |

### D2 兼容与共享边界

| ID | 场景/触发 | 预期 | 工作包 | 状态 |
| --- | --- | --- | --- | --- |
| D2-01 | **旧办事台不扩类型**：打开维护单及原 hall overview/items/marks | 典籍只走独立面板/会话卡，旧 ItemRef 枚举、分区、游标和动作保持兼容 | M4, M8 | 未执行 |
| D2-02 | **直达与宋江边界**：分别向宋江和已任职吴用交办；另用密议 | 双入口同一授权用例；直达不经宋江，宋江不获得密议读取权 | M2, M7, M8 | 未执行 |
| D2-03 | **跨入口重放**：原 requestIntentId 从断线重试和会话卡恢复 | 只有一个 job/当前执行，异内容同 key 冲突；不能从 chat/task 重复派发 | M4, M6, M7 | 未执行 |
| D2-04 | **唯一执行权威**：业务 outbox 投递响应丢失后恢复 | 重用同 dispatchKey/command/executionRef，不建第二套调度或 archive 命令轮询 | M4, M6 | 未执行 |
| D2-05 | **两套 Runtime 隔离**：仅 heartbeat/ACK 的 Runtime v1 和 legacy 客户端混用 | 按目标实际能力投递；不支持者待就绪，不混用凭据/profile/state，不强制切换其他 Agent | M2, M6 | 未执行 |
| D2-06 | **逐目标能力变更**：受理后目标撤销命令能力或更换绑定 | 分发前重新校验，不发送不支持协议，不偷偷 fallback 重跑 | M2, M6 | 未执行 |
| D2-07 | **共享安装适配**：平台来源与商业来源安装同 key 技能，且仅标 deliverable 标签 | 来源分别核验，不伪造订单或扣费；标签不能提供安装事实/ACL/正式验收证据 | M3, M6 | 未执行 |
| D2-08 | **私人来源公开用途**：仅授 READ 的私人文件尝试 AUTO 或管理员发布 | 无 PUBLICATION_USE 时拒绝发布；有精确来源/书库/用途授权后才可继续 | M2, M4, M5 | 未执行 |
| D2-09 | **公开投影脱敏**：普通读者查询 capabilities 与会话维护卡 | 不返回他人 owner/agentId/binding/runtime/endpoint 或私人 source storageRef | M2, M8 | 未执行 |
| D2-10 | **冷线程与工具隔离**：更换模型线程后继续修订，另打开普通聊天 | 服务端注入已授权历史与精确来源；典籍工具限制不改变其他会话能力 | M7, M8 | 未执行 |
| D2-11 | **业务等待不占 lease**：草稿完成后等待人工发布并保持会话打开 | 释放执行 lease，保留 job；管理员用新的有效授权发布，不复用过期 producer 凭据 | M4, M6 | 未执行 |
| D2-12 | **共享存储不新增文件系统**：从私人来源导入草稿并封存正文 | 来源/草稿使用既有受控对象，正文落 archive；不迁移旧目录，不自动保存或正式验收 | M1, M4, M5 | 未执行 |
| D2-13 | **严格身份与内容迁移**：迁移前后以 tenant=0 与旧 tenant=owner 请求 | 内容兼容不恢复旧身份；owner/client 私人数据隔离不变 | M1, M2, M9 | 未执行 |
| D2-14 | **业务完成不混同**：分别产生草稿完成、publication 提交、读回失败和成功 | 状态分别可见，不把文件 manifest/技能安装/正式验收当典籍发布，读回失败不重复激活 | M4, M8, M9 | 未执行 |

## 3. 覆盖与分层完成标准

总计 **84 项**，覆盖 U1–U9、M0 以外所有实施/验证包；M0 以合同/基线冻结记录验证，不伪装成应用运行用例。

1. **设计交付**：五件套、源码审计、用例覆盖/结构通过；不意味着下面各层通过。
2. **源码与集成**：所有相关用例有 exact source/tree、selector、fixture digest、原始结果；不足项明确列出，integration pins 可复现。
3. **技术发布**：与源码绑定的制品 SHA-256、发布顺序、schema/client/API/Web 版本、实际健康；遵守有效 Flow 或用户本地例外，不互相冒充。
4. **实际业务验收**：真实任职/安装事实、原始来源摘要、校验 candidate、publication、读回以及用户可操作路径齐备。模型一句“完成”/HTTP202/ACK/文件生成都不等于此层。

## 4. 证据最小字段

`root/API/Web/Client commit + tree`、测试 selector、DB fixture/schema digest、skill version/package digest/安装确认、管理者与任职授权引用（脱敏）、job/run/command、source raw digest、draftRevision/validationId、edition/manifest digest、publicationId、读回结果、部署制品 digest 与 build_origin。不得保存 token、DB 凭据、私人手札正文或其他任务的证据目录。

若只有草稿模式，通过点为 AWAITING_PUBLISH，不能标 AUTO/实际上架通过；没有《三国演义》授权来源时先验证 fixture，不伪称真实书已新增。

## 5. 2026-09-30 历史局部实现证据（不是当前进度）

- 业务用例：机器矩阵 84 项全部 `not_run`，`evidence=null`；下面的组件测试不得回填为 PASS。
- API 前次冻结 prospective tree `7d61d50e9a262eeb43bc8cc9ab77763bd9cec27b`（非 commit）：平台 48、native security 6、maintenance 31，合计 85 项定向测试通过；archive regression 共 195 项、12 fail、3 skip，失败方法集合与 commit `e15e1a9d947e86e5f81a3288948087466a8a879c` baseline 完全相同，delta 为空。Spring `AnnotationConfigApplicationContext` 装配测试包含平台服务与 `ArchiveMaintenanceServiceImpl`。
- API 当前 resolver tree `67dc1c225a1cc020f5c68b44b992a6f329dc1a01`（非 commit）：平台 63/native 6/maintenance 34，共 103 定向通过；archive 198 项、12 fail、3 skip，既有失败方法集合不变。原历史 proof 泄漏 P1 与两项 P2 已修，Raman 局部 ACCEPT；任职仍不可执行，不等于 Agent 已就绪。最终证据在 `resolver-stage2/attempt3/`，原 REJECT 与失败日志保留。
- Client prospective tree `a3ea0078fd11feb1fa25d4ca4109bc4231b57b45`（非 commit）：隔离 Linux chroot 中 246/246 Node tests 通过、0 skip；安全安装 manager 默认关闭，`client_entry_wired=false`，未发生 live installation。
- Web prospective tree `e7d4cc80afcccb0acb4c33a209763c7d52052f43`（非 commit）：archive tests 82 通过，`npm run build` 通过；未部署。
- 原始证据在 [evidence/2026-09-30](/home/isp/wsps/cyf/specs/archive-agent-maintenance/evidence/2026-09-30)。尚未执行真实 MySQL/DB、HTTP、跨组件、授权任职、真实技能安装/执行、内容发布、Flow 或生产验收。
- 2026-09-30 主线程已运行前轮文档静态检查；本轮 resolver 证据增量的静态检查状态以 `integration.yaml` 的 `verification.documentation.status` 为准。生成的 [documentation-check.json](/home/isp/wsps/cyf/specs/archive-agent-maintenance/documentation-check.json) 只证明结构、冻结源码和证据声明自洽，不是安全认证或集成验收。

重跑本轮静态检查：

```bash
node /home/isp/wsps/cyf/specs/archive-agent-maintenance/validate-design.cjs
```

该命令只读取冻结 Git 对象、解析文档/YAML/JSON与已存在的组件测试证据，并更新本目录的静态检查记录；依赖现有 Web node_modules 中的 js-yaml，不安装依赖，不启动应用、不运行应用测试或访问生产。

### 2026-09-30 execution 最新局部证据（不回填业务 PASS）

API 冻结 prospective tree `57fad153289a06d512c53a10cb39d410dee44e44` 的四 task 实际持锁复测：平台66/native6/maintenance43，共115定向全绿；archive208/11fail/0skip，三个H02/H03/H05A真实MySQL测试通过。新增失败集合为空，原reader-data catalog失败已修，其余11个既有失败保留；整体Gradle仍失败。见 `evidence/2026-09-30/execution-stage4/attempt4-real-mysql/` 的源码证明、XML、日志与 baseline-comparison。初始化/JDBC probe另为92497fc6树的14/14实库检查，见 `mysql-stage3/attempt3/`。两者均非业务E2E；执行切片独立复审仍在进行，Client/M7未接，不提交为完成版。
最新局部复测为 ae12d17 树（非 commit）的 attempt7-real-mysql：125 定向通过、archive217/11baselinefail/0skip、introduced=[]；两项真实 RR 并发及三项旧域 MySQL 测试通过。attempt5 编译失败、attempt6 mock 夹具失败均保留。独立复审仍待回执；这些不是 Runtime/HTTP/WebSocket/业务验收，84 项保持 not_run。

最终 execution 局部切片 b6fb79 树的 attempt10-real-mysql：126 定向全绿、archive217/11baselinefail/0skip、introduced=[]，5 实库测试通过，Raman 局部 ACCEPT。attempt8 未完成及 attempt9 隔离 DB 停止失败均保留。M5 开始实施，M6/M7/AUTO/HTTP/WebSocket/整体验收与提交推送未完成，84 项仍 not_run。

### 2026-09-30 M5 局部验证补充（不是业务验收）

- API tree `889f63ac33251e85c288e945c339c9e4f4a48582`：Node14/14；持锁实库定向129/129；全archive219/11既有失败/0skip，introduced=[]，整体Gradle exit1。证据 `evidence/2026-09-30/execution-stage4/m5-attempt2-real-mysql/`。
- 确定性包 SHA `8894d96341067dd7f9e2f45696eef44057dc61346255a0323b2d713a3c7ea081`（40563 bytes）；独立M5复审无剩余P0/P1/P2。首轮compile/checker失败另留原件，不冒充全量绿色。
- Client冻结基线四selector246/246；Client真实受控入口/AUTO/恢复/M7及跨组件验收未完成。84业务用例仍not_run，pins null，未提交/推送/发布。


## 6. 2026-10-01 当前源码交付验证

以 `delivery.md` 和 `integration.yaml` 的精确 commit/tree/pins 为准。Web245/245PASS+build0；API定向173PASS、archive258/11既有FAIL/0skip且delta空；Client443/442PASS/1既有FAIL/0skip且delta空；有界真实HTTP/JDBC/POSIX/Client fixture1/1PASS，MANUAL显式管理发布、AUTO/replay唯一publication/event、实际Reader读回。独立最终scope ACCEPT，不代表84业务用例或完整Runtime E2E。历史文档checker exit1仍披露，单独当前交付gate不替代它。

## 2026-10-07 最新接续（覆盖历史当前状态）

原D2源码与文档已收口，全部局部源码包独立接受。API5722e7fa / Web6dd4553c / Client9426030；最后生命周期Client Linux104PASS，API同树Chat76PASS及Agent17Windows环境失败原件保留。完整远程提交回执以evidence/delivery/resume-20261007/为准，组件→Root推送后再做隔离服务端全面验证。生产发布/迁移/真实任职与上架/付费调用未执行，84业务用例仍not_run；源范围接受不是whole-feature accepted。
