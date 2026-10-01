# API 多轮/自然澄清：真实验证与修复进展

日期：2026-10-01。这是实际证据补充，不改冻结协议/DDL，不是发布或产品验收。

## 1. 已执行结果（按来源区分，不混计）

| exact candidate / 运行 | 实际结果 | 结论 |
| --- | --- | --- |
| `30632a9` / v5 | Agent 39通过；Chat 31项中30通过、1失败 | Jackson3 unchecked parse exception 绕过 INVALID_REQUEST；另有 XML 目标目录缺失的收集错误，原误报 NOT_RUN 与事后纠正均保留 |
| `a213784` / v6 | Agent 39通过；正常 Chat 生产/测试编译完成，但 Gradle daemon Java heap space，Chat测试未运行 | 与上一行真实断言失败不同；原128m daemon终态及日志保存，未将编译完成当测试通过 |
| `a213784` / v7 Chat V3 | 11个类、33项通过，0失败/错误/跳过 | 原 strict duplicate/trailing 错误及新增4个解析入口回归通过 |
| 同一 v7 / V2 | 17个类、82项通过，0失败/错误/跳过 | 既有点将/生成桥完整所选兼容套件通过 |
| 同一 v7 / typed11 | 11个类、64项中51通过、13失败，0错误/跳过 | 真实自然讨论/澄清闭包未通过，候选不提升 |

v7复用同一 exact tree 的 v6 Agent 9份XML/39项，保留原 fixture digest 与隔离数据库前缀，不谎报为本轮 fresh。v7新增39份 fresh XML/179项；加上明确复用39项为218项、205通过/13失败。这些数字不是34项产品验收或真实浏览器闭环。

## 2. 修复和剩余失败

`a21378413366cfe96962ff49adf6b43d8d883d45` / tree `cf0308a1bb8d2726fb338e0f2711d8052ca6222c` 仅在严格 wire 读取处捕获具体 JacksonException 并映射原 INVALID_REQUEST；非JSON RuntimeException继续传播。原严格断言保留，未扩大执行授权。

v7剩余13项分组：
- 4项：DDL读取器把已批准外键的 `ON DELETE RESTRICT` 误认为破坏性 DELETE，尚未进入真实typed表成功初始化。
- 1项：typed facts 用 `Map.copyOf` 复制，拒绝既有事实清单刻意保留的 null 字段。
- 2项：WebSocket测试的 FinalResult 没有真实协议要求的 turn。
- 4项：实际Spring测试容器缺既有必需 ChatInteractionStepStore 依赖。
- 2项：测试用自造 `request-new` 代替服务端确定性request ID，导致状态URL或pending CAS不匹配。

下一源码包限定7条路径：修复上述两处Java实现及测试装配，保持SQL/DDL、CHECK/FK、事务、身份权限、黄金fixture和强断言。任何超出冻结合同的迁移/授权/事务语义变更不属于该包。修复后先真实跑typed11，按变更影响补兼容回归，不重复跑未变的已验证包。

### 2.1 67937 修复已提交，开始精确候选验证

候选 `67937da02b811b463ba837c8a0f0bc636406df5a` / tree `7a6de5e54f5cf4dd6d12b21f95769aa17f1f666f`，parent 为上述 a213。Main 已核对 clean、精确7路径、SQL与黄金fixture不变以及生产改动范围；[源码核对及原合同](integration-evidence-20260928/api-67937-source-check-20261001/manifest.json)保留摘要。

修复已覆盖前述5组根因，并补充破坏性DDL拒绝、nullable facts摘要、WebSocket回执和服务端请求ID绑定断言。澄清CAS mock 的成功桩使用宽入参，但调用后精确验证 receipt requestId 与捕获的服务端DTO一致，fresh case另固定确定性ID；没有更改生产CAS语义。

v8 仅先运行完整 typed11（包括真实隔离MySQL和Spring事务）；沿用原worktree增量缓存、正常依赖/AP图及有据256m daemon，不重跑无关构建。授权执行不等于已通过；a213上的Chat V3/V2/Agent证据仍明确属于父候选，不能自动算成67937全套通过。待本轮结果再确定最小兼容回归范围。API feature pin仍保持87c0，尚未发布或可验收。

v8实际终态：runner 读取 argv 缺失的 `environment` 字段，抛出 `KeyError`，尚未启动Gradle，日志为空、0测试。自有桥已关闭；不是67937源码失败，也不是测试通过。[原始失败证据](integration-evidence-20260928/api-67937-v8-harness-failure-20261001/manifest.json)保留不覆盖。已授权验证Owner在独立v9目录修正环境映射、核验runner所需字段和模拟启动路径后执行一次typed11；不得沿用未修正输入盲重试。

### 2.2 v9：61通过，剩余4失败已定位

修正验证脚本环境字段后，v9 在 exact67937 上完成正常编译和全部 typed11：**11份fresh XML，65项测试，61通过、4失败、0错误/跳过**。Main已独立逐XML计数；[原始日志、XML和修复合同](integration-evidence-20260928/api-67937-v9-20261001/portable-manifest.json)可复核。正常Gradle共63任务，3执行/60 up-to-date，耗时约73秒；自有桥关闭、私有数据库清理通过，mysqld未操作。不是可验收或发布通过。

- 3项MySQL失败：第一次真正执行到 pending-question DDL，发现 `chk_chat_typed_pending_version` 末尾额外一个 `)`；语法失败，不能宣称建表或约束校验通过。
- 1项Admission测试失败：合法 `contexts.resolve` 调用尚未被显式verify，直接 `verifyNoMoreInteractions` 报错；不是生产身份不匹配。
- nullable facts、有效WebSocket turn/回执、Spring依赖与事务组、服务端ID/CAS原失败已在本轮通过；其余SQL约束仍待真实验证。

下一包冻结为3路径机械修复：Main固定SQL一字节删除，保留全部CHECK谓词/FK/索引；补精确context调用verify，保留no-more-interactions；补语法回归。旧“SQL字节不变”合同保留历史，新合同仅对这一字节显式修订，不授权生产迁移、数据写入或放宽catalog检查。新child提交后再跑typed11，不重复未修正67937。

## 3. 验证效率与证据真实性

- v6记录了128m Gradle daemon的真实堆耗尽；v7仅将该daemon试验性分配改为256m并加逐阶段GC日志，编译器/Test heap、正常Gradle依赖/AP图不变。不是新增资源门禁，也不宣称256m为测得最小值或宿主OOM问题已消失。
- v7正常复用编译结果，Chat阶段60个任务中仅目标Test实际执行、59个up-to-date；不手工借class，不禁用AP，不全局rerun。
- 继续使用原Owner独立worktree保存正常增量历史；源码提交、tree、测试输入和结果仍精确绑定。
- v6原source_roots错误指向父候选worktree，原文件保留，另附逐源hash及actual child class纠正；v7全部source_roots绑定a213。
- XML目标目录执行前建立。JUnit执行与收集故障分别记录，不能再把已执行阶段记为NOT_RUN。
- 仅本线程隔离MySQL及自有TCP桥；每阶段私有前缀清理核验，桥已关闭，mysqld未重启/变更。

原始日志、XML、GC、计划、argv、纠正与Main独立计数在[便携证据](integration-evidence-20260928/api-strict-wire-v6-20261001/portable-manifest.json)。Main首次v7比较脚本误用了改名前phase名称，纠正后再发执行GO；没有因此启动额外运行，纠正记录也保留。

## 4. INSPECT下一包的源码依据

[API/Client/Web接线准备](integration-evidence-20260928/inspect-authority-prep-20261001/prepared.md)已以API a213、Client607d、Web ebb实际源码核对，并保存真实0.159.2公开schema的持久副本。这是准备，尚未冻结或实现。

复用现有request/inbox/binding/typed pending状态及受权快照，不预设第二套状态机；新增purpose-scoped runtime读取边界须验证当前身份/目标/assignment/generation/精确来源，不能借EXECUTE START或人类浏览器下载权限。0.159.2支持localImage/localAudio字段，但schema不证明模型理解、严格无工具或文件系统隔离。资料目录仍不能冒充已读取内容，不新增未测算的count/byte硬门槛。

## 5. 发布与通知

组件feature及研发pin保持API `87c0acc`、Web `ebb664f`、Client `607d251`，没有提升失败a213、没有合develop或发布。版本须发布前重新核对占用，不能盲用历史1.13.45–47。完整多媒体、双接应、真实浏览器、保存/正式交付/验收完成仍须实测；尚不能通知用户“可以验收”。唯一实时责任台账仍为主工作区TASKS.yaml。
