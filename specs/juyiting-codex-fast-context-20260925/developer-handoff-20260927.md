# 开发交接：Fast deliberation 合并冲突与优化建议

日期：2026-09-27。目标：由原开发在 `codex/juyiting-codex-fast-deliberation-context` 完成整改，再评估合入组件 develop。本次只提交文档，不修复/合并功能代码。

## 结论与阅读入口

- **当前不能直接合入 develop**。2026-09-27 再次读取四仓远端，均与 `merge-evidence-20260927/manifest.json` 一致。
- 详细问题、候选文件定位和证据限制见 `merge-assessment-20260927.md`。历史 `integration-ready` 表示原候选集成记录，不代表与最新 develop 无冲突，也不覆盖此次 F1–F4。
- 多媒体需求另行提交到 SDD develop 的 `specs/juyiting-multimedia-deliberation/`。本分支无需一次性交付生图，但应提供可复用且真实的 durable 上下文/事件基础。
- 不创建独立 Reviewer；Owner 自检。慢请求仅观测，不新增任意 deadline、磁盘/swap 门槛或逐次发布审批。真实身份/ACL、数据库、幂等和授权检查保留。

## 冲突清单与保留原则

以下路径以仓库根为基准，完整仓库位置见证据 manifest；不是要求编辑 `/tmp` 评估副本。

| 仓库 | 冲突路径 | 处理建议 |
| --- | --- | --- |
| API | `chat/jia-chat-service/build.gradle` | 合并双方必要依赖与测试配置，不整文件覆盖 |
| API | `chat/jia-chat-service/src/main/java/cn/jia/chat/api/ChatController.java` | 同时保留服务端权威身份/可信资料与 durable admission，向新 service 传递解析后身份 |
| API | `chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentWebSocketHandler.java` | 保留多 owner 注册、ACK/重连与托管恢复；增量接入 durable 事件 |
| API | `chat/jia-chat-service/src/main/java/cn/jia/chat/service/JuyitingAgentRelayService.java` | 保留任务材料/宋江上下文，统一新旧 relay 路径权限 |
| API | `chat/jia-chat-service/src/test/java/cn/jia/chat/api/ChatControllerTest.java` | 保留身份与资料用例，补新协议伪造身份负向用例 |
| API | `chat/jia-chat-service/src/test/java/cn/jia/chat/handler/AgentWebSocketHandlerTest.java` | 保留注册、ACK、恢复测试并覆盖新协议 |
| Web | `src/composables/juyiting/hallConversationMessages.js` | 保留服务端身份展示与资料投影，叠加消息去重/恢复，不让旧事件覆盖新版本 |
| Web | `src/composables/juyiting/useHallConversation.js` | 合并任务材料入口、目标身份与 durable 请求状态，保留身份切换清理 |
| Client | `conf/codex-ws-agent/test/agent-client.test.mjs` | 保留 native start receipt、Profile 恢复与 fast CHAT 断言，不能删一方用例消冲突 |
| SDD | `api` / `web` gitlink | 等组件整合后固定已推送的精确 SHA，不用旧 feature SHA 覆盖 develop；勿顺带合入无关历史文档 |

Client 主程序自动合并后只做过语法检查，不表示最终集成已通过。SDD 缺历史子模块对象提示不能单独证明候选损坏。

## 开发整改清单

| ID / 优先级 | 责任范围（未派发） | 最小整改与通过证据 |
| --- | --- | --- |
| F1 / P1 | API Owner | admission/message/event/final 全程使用服务器解析身份；伪造 senderType/name 不得改变持久或显示身份 |
| F2 / P1 | API + Client Owner | 逐目标协商 fastChat/appServer/ACK/协议版本；覆盖关闭开关、旧客户端、自家接应、混合目标；现代受理后不偷偷降级重跑 |
| F3 / P1 | API + Client Owner | DB-backed 授权历史窗口/摘要/固定素材；冷线程、缓存失效、配置切换可恢复；内置宋江消费同一可信上下文 |
| F4 / P2 | API + Client Owner | 暂未实现 INSPECT 就收窄声明；如实现，必须固定引用与受控领取，不放开任意本机目录/执行工具 |
| DB | API Owner | 实际 MySQL 8 增量迁移、重入、恢复及事件/outbox 事务证据；不能用 H2 或 Java 单测替代 |
| AUTH | API Owner | 核对旧 machine JWT 无 tenant 的真实客户端影响，记录切换/重新签发/有效期兼容计划，覆盖聚义厅外调用方 |
| REG | 各组件 Owner | 最终 merged tree 回归最新 develop 身份、材料、多 owner、native START、重连，以及本分支 admission/replay/cancel |

修复优先级不是全局串行锁。契约冻结后可分仓并行，身份/上下文和能力协商存在真实依赖时才等待。

## 复核方式与现有证据边界

在干净独立 worktree 获取最新 develop 与候选后执行 `git merge-tree --write-tree <develop-sha> <candidate-sha>`；退出 1 表示冲突，输出写入自己任务的证据目录。合入前重新记录 exact SHA/tree，不能将本次旧模拟树当最终版本。

候选快照的轻量复核命令（在各自仓根执行）：

```sh
# Web：已有依赖时
node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --reporter spec tests/juyiting-codex-fast-deliberation.test.js tests/juyiting-hall-conversation.test.js
# Client：先进入 conf/codex-ws-agent
node --test test/chat-runtime.test.mjs test/agent-client.test.mjs
```

既有评估结果是 Web 79 passing、Client 141 tests passing，不是整改后测试。API 编译、MySQL、真实 Profile 和浏览器本轮均未执行。任何 Gradle 必须经 `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py`；正式实施验证遵循用户现行政策（2026-09-17 临时本地授权覆盖历史 Flow-only 文字），不伪造云效 Run，不从文档交接推导生产数据/付费调用授权。

## 返回交付要求

1. 对 F1–F4 逐项回填“修复 SHA、测试选择、结果、未完成项”；不只回复“冲突已解”。
2. 给出 API/Web/Client 最终 commit/tree 与实际数据库夹具/协议混用证据；源码通过与上线通过分开。
3. 提供组件合入次序和机器 JWT 兼容说明；根仓只更新已验证的组件 gitlink。
4. 多媒体方案继续复用 request/turn/outbox/snapshot/event，不另建聊天持久化体系；新增文件执行要以服务端受控桥接完成。
