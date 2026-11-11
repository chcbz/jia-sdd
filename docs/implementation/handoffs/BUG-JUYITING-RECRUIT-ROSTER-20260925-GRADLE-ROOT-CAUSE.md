# BUG-JUYITING-RECRUIT-ROSTER-20260925 Gradle 根因矩阵

日期：2026-09-25

| 失败 | 证据 | 根因 | 有界整改 |
| --- | --- | --- | --- |
| 1 | `build.gradle:109` 缺少 `repoUsername`，测试未执行 | 错把宿主 `gradle.properties` 当作仓库凭据来源 | 核对文件内容与构建入口，不改产品代码 |
| 2 | 复制后的文件仅有 JVM/checksum 属性，仍在配置阶段同点失败 | 本地 targeted Gradle 未加载仓库自带 `ops/ci/aliyun-flow/cold-init.gradle`；该脚本提供公共仓库 URL 和空凭据默认值 | 保持 exact commit/tree 与 selector 不变，仅在命令增加 `-I ops/ci/aliyun-flow/cold-init.gradle`，串行重跑一次；新失败先归因，不盲重试 |

本矩阵不授权发布、生产数据写入或放宽测试断言。

## Focused test failure, 2026-09-25 22:57 CST

| Evidence | Root cause | Bounded remediation |
| --- | --- | --- |
| `EconomyWalletControllerTest:99` saw two mapper calls | Fixed economy tenant `0` makes both valid nonzero `jiacn` claims pass the same wallet scope; the assertion still expected one call | Keep both positive owner cases and assert exactly two calls |
| `EconomyPreviewConfigurationTest:63` missing onboarding bean | Its properties-only fixture explicitly enabled only `EconomyPreviewProperties` | Add `EconomyOnboardingGrantProperties` to that test fixture; no production configuration change |
