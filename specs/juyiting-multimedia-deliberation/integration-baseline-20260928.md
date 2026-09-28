# 四仓融合研发基线与验证回执

日期：2026-09-28。目标：四仓 `codex/juyiting-multimedia-deliberation`。下列组件 exact SHA 为本轮研发基线，远端推送回读见便携证据；SDD exact SHA 由包含本文件的根仓提交确定。

## 授权边界

只建立 feature 分支、合入 fast 源码、解决冲突/必要安全兼容修复并相关自检、编制长期方案及详设。不更新 develop/release，不部署、不启动真实数据库迁移、不调用付费模型。原主工作区脏文件不回退；唯一运行台账只添加本轮两项源码Owner任务及一项跨仓wire收敛任务。

## 输入基线

| 仓库 | develop | fast |
| --- | --- | --- |
| SDD | ccd6cbabe0c9f737ae61237c0d01c4df821e8a5c | 9f47e63e456a7965d954e6d1e645a083920d784e |
| API | e15e1a9d947e86e5f81a3288948087466a8a879c | caee54fc27a08146f9cc57219cf86c763e41c531 |
| Web | 9854173f7f409ca2f1c862eb153b0e3574ee58ff | 96838f17fc24fbf21781be39476aa9723dee3a2c |
| Client | 29fda32acca7a4c4f7a66a4188946853086e6dcb | 68dbe8992a56c8e1041056a9123b1156d1d2b35e |

## 根仓选择性整合

SDD真正启动双亲merge后，仅引入 `specs/juyiting-codex-fast-context-20260925/`，保留develop其他文档和多媒体需求，更新本feature规格/索引及新组件gitlink。根仓本轮3处冲突（api/web gitlink、specs/INDEX.md）按该范围解决；不自动传播fast历史中其他文档变化。API/Web/Client由各Owner逐处合并源码，不使用整文件覆盖。

## 最终组件研发 pin

| 仓库 | commit | tree |
| --- | --- | --- |
| api | 742ba9035e3a05c0f4896fd93e5cb285ddb297f6 | a71e20a7d478e5abd91d114744b7f34466e7cafe |
| web | 3e37d05f7e7c68487d72abdca928112a0d0b680f | 88dff45b3559f5f5579d6848e641f7ae69bbb862 |
| client | 33e38de96f157c020c0bf0b3db4bee451b3b7c3f | 52fe002075307392d2f32c5d96d4b7ea88f98137 |

上述为开发 pin，不是 accepted/released 业务基线。API/Web gitlink 随本SDD提交固定；Client不是子模块，固定在 integration.yaml。

API真实merge为 `3e608552a4750ad073e8c8bf4f821053e79fc660`，其后为相关测试/wire合同修正；Web最终提交即merge；Client真实merge为 `d79896e1a877cde9c6fb6278e5ad1a80dac3cf74`，其后仅收敛可信身份字段引起的wire变化。各仓保留develop与fast祖先，不改写原分支。

## 实际定向验证（非产品验收）

| 仓库/selector | 结果 | 范围限制 |
| --- | --- | --- |
| API `:chat:jia-chat-service:chatDeliberation` | 56 tests，0失败/错误/跳过 | durable request/context/wire等定向测试，非真实MySQL迁移 |
| API `:chat:jia-chat-service:bf08FormalFlow` | 60 tests，0失败/错误/跳过 | controller/relay/identity回归；与其他selector可能重叠，不累计成独立用例总数 |
| API `:chat:jia-chat-service:managedHostingHandshake` | 3 tests，0失败/错误/跳过 | managed握手定向测试，不证明所有机器JWT历史兼容 |
| API `:chat:jia-chat-service:test --tests cn.jia.chat.service.JuyitingAgentRelayServiceTest` | 10 tests，0失败/错误/跳过 | 可信身份/资料relay专项 |
| Web 4个相关test文件 | 86 passing | fast会话、议事、资料链接、账户导航 |
| Client agent-client/chat-runtime/managed-host | 最终树167 passing，0失败/跳过 | START、ACK、默认禁用及wire；初始merge日志另留历史，不重复计数 |

chatDeliberation最后一次exact-tree调用为Gradle UP-TO-DATE，复用同source set在bc4bd8b提交已通过的56项XML结果；后续742ba90仅补另一source set的Mockito导入，没有把缓存复用冒充重新执行。API便携`.log`为事后摘要，详细case结果另见xml-suite-case-summary.json。

API经orchestrator串行Gradle执行；Web/Client为本地定向检查。本轮不生产构建、不伪造Flow Run，不代表已完成云端发布/在线验收。最终Owner回执与日志见 `integration-evidence-20260928/`。

保留失败历史：Web首次回归发现发出端身份/metadata不合合同，移除不可信字段后通过；API先后修复旧eventPayload签名、reflection/提示文本断言、fixture字节漂移及缺失Mockito静态导入。每次均记录归因并变更候选后复测，不能将首次失败改写成通过。

## 跨仓wire一致性

Client pin API不可变提交 `bc4bd8b15cc06ed29bc591ad01258d1533711f2a` 的生成夹具；最终API HEAD保留相同字节。fixture SHA-256：`db50396c2522f7fe8c32af8027abc253782c16eee8354119b2eac643140ce6ee`，7308 bytes。Client provenance、runtime pin和contract assertions同步更新；最终源字节比较与推送回读保留证据。

## 缺陷与未验证范围

- **F1已做源码修复并通过范围内回归**：durable admission/context/event/Agent回复采用服务端可信sender身份，不能信任客户端/Agent伪造姓名；不据此宣称所有身份迁移风险关闭。
- **F2未完成**：服务端逐目标能力协商仍待补齐；Client `CODEX_FAST_CHAT_ENABLED`、`CODEX_APP_SERVER_ENABLED`、`CODEX_TRUE_DELTA_ENABLED` 仍默认false。直接启用/部署不能保证默认新协议可用。
- **F3未完成**：本次保留develop可信taskMaterials及builtin宋江上下文，但完整授权历史/摘要/冷线程重建仍缺失，不能只靠thread缓存。
- **F4未完成**：真实INSPECT读取/精确资料引用仍待实现；read-only-constrained不等于严格无工具。
- 实际MySQL8空库/存量迁移与恢复、历史机器JWT tenant兼容、真实引擎工具隔离、双接应Provider调用与浏览器流程均未执行；不得标PASS。
- 多媒体统一admission/grant/asset、预览下载保存、正式晋升验收等新业务尚未实现。**AC01–AC22 + FD01–FD12共34项产品验收全部NOT_RUN**。

## 下一步

从 [融合实施计划v2](fusion-implementation-plan-v2.md) 的U0基础收口开始，冻结U1授权/统一交互合同，再做图片纵切和完整多媒体；只在真实验收与授权条件成立后制定合入/发布动作。本次未修改develop/release、未部署。

## 2026-09-28 后续源码增量（不改写最初整合回执）

Web新增会话媒体part reducer/私有读取展示切片 `de72f12649de1038efa197f804e2d67f2d59f777` / tree `f67f67d69140ad6b40f873d4427ae4dd6eb0c808`，四组定向测试 **155 passing**，SFC语法检查通过，完整日志摘要与推送回读见便携证据。此增量**不代表**尚未实现的服务端会话资产API或“画鸟”真实交付已验收。原始表格的Web 3e37d05与86测试是此前源码整合时点，当前SDD gitlink已更新到de72f12。完整后续交付计划见 [分版本交付](versioned-delivery-plan-20260928.md)。

## 增量：U0-R真实能力声明（2026-09-28）

Client feature远端已从 `33e38de` 快进至 `326b85767cb97e211bfa32cba673631a674f5d83` / tree `5cfe533f79144c0f001ab0b0d4a4dc1c1b15644a`（推送readback一致）；本节不覆盖上表的首次整合时点。`agent.register`/`agent.presence` 共用 `runtimeCapabilities.capabilityContractVersion=1`：默认fast关闭时CHAT不可用，只读约束不冒充经验证严格无工具；INSPECT和新EXECUTE均未广告，旧PRIVATE/TASK/native START仅是legacy兼容能力。冻结fixture见Client `conf/codex-ws-agent/test/fixtures/u0-runtime-capabilities-v1.json`。

主线程在新tree执行 `node --check agent-client.mjs`、`node --test test/agent-client.test.mjs test/config-runtime.test.mjs`：**150 passing，0 failed**（两套合跑输出 `# tests 150`，`# pass 150`）；Client Owner原文档分开执行116与34同为150，最终口头146与实跑不一致，以实际合跑为准。U0-A服务端尚在开发，真实逐目标协商/旧新客户端负向、Provider无工具证明及MySQL/JWT未闭合；本pin只是研发进展，不是出厂条件。
