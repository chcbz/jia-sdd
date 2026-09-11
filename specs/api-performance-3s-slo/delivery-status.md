# API 3 秒性能治理 delivery status

更新：2026-09-11。本文件是状态投影，当前 owner/gate 仅取 `docs/implementation/TASKS.yaml#runtime_ledger_json`。

## 已交付的有界切片

- 生命周期：`implementing`，整体验收尚未完成。SDD 合同独立 R4 审查 ACCEPT0/0/0。
- `PERF-A02-LOG`：安全慢日志/单调计时，独立 source + 6 项定向单测 ACCEPT。
- `PERF-A01-HIST`：HTTP histogram/1s、2.5s、3s buckets/URI 上限，独立 source + 5 项定向测试 ACCEPT。
- 两项 API 切片已推送 `codex/perf-api-integration-20260911`：`5571d183fe7c612f2d5ebb272548aa5bfad77e90` / tree `b993a925464701b5a17c93461cf3f558036f5d13`，未发布。
- `PERF-BUILD-01`：上述合并 API 的日志 selector 经真实 offline Gradle 6/6PASS、零跳过，独立证据审查 ACCEPT0/0/0。非敏感占位属性绕过历史 publishing 配置缺失；不是完整模块、starter/metrics测试或启动证明。
- `PERF-01-TOOLS`：离线扫描/严格对账工具最终 R4 ACCEPT0/0/0，`43e0e46f8d9a07797713adb432c3bcab770dd8b0` / tree `e0a9c30fa385c1ff0ae42d2f70f97dd5d87bc3b9`。修复自定义注解漏检、外部可信工件绑定和哈希/解析竞态；26 项实际单测、真实 CLI 合成正反例通过。已推送工具分支，并 byte-exact 合入 `codex/perf-sdd-20260911`。
- R4 验证包装器及元数据脚本各有一次失败；原始命令结果/源码身份/工件 hash 经 main 与独立 reviewer 复核，足以支持有界源码验收。未伪造成功 wrapper 或 verifier-cache HIT；失败历史保留。

## 尚未完成

- 真实 grey/prod-profile 框架/管理面清单、受保护运行时采集、registry 全覆盖对账。
- 完整模块构建、应用启动、跨链路 trace/inflight/依赖预算、隔离性能基线、热点查询优化、逐接口 3 秒达标及发布。
- 旧 checkout 的42 Controller/约401 mapping，及后续 exact API `014fb7e` 的440条 supported mapping，均只是历史/非零诊断，不是 accepted 全量接口清单。

## 下一步

冻结隔离环境 profile、数据夹具和可信采集链；完成真实声明/运行时清单对账后，再启动六个热点接口的未优化基线和查询优化。不得用合成测试替代真实清单或压测，不得生产压测。

证据与失败矩阵：`../../docs/implementation/handoffs/PERF-CONTINUE-R3-20260911.md`；此前证据见 `PERF-FIRST-BATCH-20260911.md` 和 `PERF-VERIFY-R2-ROOT-CAUSE-20260911.md`。
