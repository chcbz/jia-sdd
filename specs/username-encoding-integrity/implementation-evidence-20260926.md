# 用户名编码完整性实施证据（2026-09-26）

## 1. 固定版本

| 组件 | commit | tree | 远端 `develop` readback |
| --- | --- | --- | --- |
| API | `188bf0c0e85afed82c1258b63f298491d669d575` | `71b6fbac75bec0166d392cbb7d502af3976a8320` | MATCH |
| Web | `c2af3ce30e7ced1e3d4d93234a1538e13bd73585` | `e6a80a167782cb3ea7b2763897a13b81530e0ab1` | MATCH |

API 候选同时固定到 `codex/username-encoding-integrity-api-20260926`，Web 候选固定到
`codex/username-encoding-integrity-web-20260926`；两次 `develop` 更新均为 non-force fast-forward。

## 2. 已落地的污染阻断

- OAuth provider 响应保持为 `byte[]`，去可选 UTF-8 BOM 后使用 fatal UTF-8 decoder；malformed、空 body、非法 JSON 安全失败。
- provider nickname 采用 source-aware 策略：合法中文、emoji 和西文重音保留；控制字符、超长和高置信 mojibake 不写入；无效新值不覆盖已有 MySQL/LDAP 好值。
- 人类聊天 sender 只从认证 `EsContext` 和 `UserService.findByJiacn` 解析。HTTP request 与 metadata 中的 `senderName/senderType` 兼容接收但无条件忽略。
- 普通聊天、Advisor、聚义厅 relay、内建流和持久化复用服务器权威 sender。Advisor 的 ASSISTANT 消息固定为 `senderType=assistant`、`senderName=助手`，不再继承“陈惠超”。
- Agent WebSocket final、delta、数据库和 metadata 根据认证 session agentId 的 runtime/persona 解析，忽略 payload `senderName/agentName`。
- Web 使用唯一 `displayName.js`：percent UTF-8 → raw Latin-1 fatal UTF-8 round-trip → control strip → trim；个人中心、聚义厅和普通聊天统一调用。
- 乐观本人消息使用 `isSelf:true` 和“你”；历史本人只按稳定 `jiacn/ownerJiacn/owner.jiacn` 判断；Web 不再发送 sender authority 字段。
- 历史 `messageType` 优先于旧 `senderType=user`，避免旧 ASSISTANT 行被错标为本人。

## 3. 姓名与不可逆数据原则

正确姓名固定为 **陈惠超**，UTF-8 为 `E9 99 88 E6 83 A0 E8 B6 85`。完整 raw Latin-1 mojibake
`é\u0099\u0088æ\u0083\u00A0è¶\u0085` 可严格 round-trip 恢复；截图中的 `éæ\u00A0è¶` 已先丢失 C1 字节，不能唯一还原，代码只回退 username/jiacn/“你”/类型名称，不猜姓名。

## 4. 本地验证

### API

均通过 `python3 ops/orchestration/cyf_orchestrator.py gradle ...` 串行执行：

- OAuth focused：PASS，41 tasks；证据键 `ea121ff41e07f5f68f1b27b8976f6fe89cb85ba0b8cd67d0e837429068903f2e`。
- User entity boundary：PASS；证据键 `28883add94daa65aca6de051086e3307b70d8293974bd3b64b5ee2773d47dc4d`。
- User upsert preservation：PASS；证据键 `7e2567b20ca029610c06434a3d4d4afc921b305f145ace844f62411791e89f6a`。

以上 PASS 对应 Advisor 最终修复之前的 API tree。最终 tree 的 Chat 选择器尚无成功本地结果：低内存、单 worker 输入在进入 Chat 编译前由宿主全局 OOM killer 终止于 `agent:jia-agent-core:compileJava`，内核记录被杀 Java `anon-rss 647692kB`。这不是 Chat 编译诊断，未据此跳过测试或宣称通过；详见 `local-gradle-root-cause-20260926.md`。

### Web

最终 commit/tree `c2af3ce...` / `e6a80a...`：

- 核心定向测试：83 PASS。
- Hall/SFC 挂载集成：5 PASS。
- `node --check src/utils/displayName.js`、相关 Hall JavaScript 与 `git diff --check`：PASS。
- 一次完整 `npm test` 在 harness 修复前得到 2405 PASS / 2 pending / 53 FAIL。本任务引入的 7 项失败（5 个手写 SFC harness 缺少共享 helper mock、2 个旧源码契约断言）已在后续提交修复；剩余 46 项归因于既存无关 fixture、provenance 和旧源码断言，未为本任务放宽或篡改。
- source-equivalent 的前一候选曾完成 Vite production build（1259 modules），但不能替代 exact-final-tree 证据。
- exact-final-tree 再构建同样完成 1259 modules transform，进入 rendering 后被宿主 OOM killer 以 exit 137 终止。因此不声明最终制品，不使用残留 `dist/` 作为发布证据。

## 5. Flow 状态

北京时间 2026-09-26 13:03 查询：

- API `5260799` 最新仍为 Run 96 FAIL，source commit 未返回；未出现绑定 API `188bf0c0...` 的新 Run。
- Web `4403172` 最新仍为 Run 147 FAIL，source commit 未返回；未出现绑定 Web `c2af3ce...` 的新 Run。

未手工重复触发，未伪报 Flow 成功。正式测试、制品、部署和线上健康仍待 exact-SHA 云端证据，或按仍生效的 2026-09-17 本地发布授权补齐本地生产构建、冻结 release、制品摘要和实际健康。

## 6. 明确未执行

- 未做生产 MySQL/LDAP/chat DML。
- 未猜测或批量改写不可逆历史姓名。
- 未操作其他任务进程、Gradle daemon 或证据目录。
- 未把本地定向检查当作生产发布成功。
