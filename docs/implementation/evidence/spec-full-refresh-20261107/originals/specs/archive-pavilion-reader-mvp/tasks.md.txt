# 案卷阁阅读 MVP tasks

<!-- SDD delivery reconciliation 2026-09-06 -->
## 2026-09-06 全量状态核对

H01–H05W 已接受，H06 已发布；旧 reader 修复随 Web101ac4c 发布，CORS 补丁也已部署并通过可信/非可信预检，剩余 authenticated adapter/真实阅读闭环未完成，整体不归档。

完整任务/版本/证据及未完成项见 [delivery-status.md](delivery-status.md)。归档：仅 AR-20260906-05 / AR-20260906-04 历史发布记录。原文合同及历史验收材料保留，不把发布例外标成 PASS。

### 当前执行动作

CORS 五行补丁已独立 ACCEPT 并应用生产，可信 OPTIONS200/非可信来源403 已记录；不重复修补。由现有阅读 Owner 完成 authenticated save/read adapter 回归及读取、进度、书签/手札、关闭重开的业务闭环。

以下原始清单为合同/历史记录；当前完成状态采用 delivery-status 的任务映射，不能据旧未勾选项重新派工。
<!-- END SDD delivery reconciliation -->

## Control/content

- [x] **H01 Contract/content**：冻结来源、许可归属、原始 SHA、120 回连续性、稳定 ID、manifest/golden fixture 和失败矩阵。Owner：main orchestrator；独立只读 Review。

## API (`api/`)

- [x] **H02 Catalog/schema**：正文 schema、initializer、确定性导入、catalog/chapter API、ETag、feature flag。P0 migration；`critical_worker` + independent reviewer。
- [x] **H03 Reader data/ACL**：进度、书签、私人手札 exact-scope、CAS、幂等、tombstone 和真实 MySQL 隔离验证。P0 ACL/transaction；`critical_worker` + independent reviewer。
- [x] **H05A Question backend**：服务端选文重建、问题/outbox/event/SSE、案卷书吏 fallback，不接受目标 Agent。P0 transaction/replay；H04 后实施。

## Web (`web/`)

- [x] **H04 Reader UI**：案卷阁双页签、目录/正文/继续阅读、进度、书签、手札、冲突状态和 responsive/accessibility。契约冻结后由 `balanced_worker` 实施。
- [x] **H05W Ask Agent UI**：选文问案卷书吏、snapshot/SSE reducer、断线恢复；不得读取 selectedAgent。

## Integration and verification

- [ ] **H06 Integration/release**：真实 MySQL、120 回 hash/count、两身份两 client ACL、浏览器闭环、ES 停止降级、旧案卷检索回归、SHA-pinned artifact、备份/恢复和 feature-flag 回滚。

## Review cadence

- H01、H02、H03、H05A 为即时独立 Review。
- H04/H05W 的低风险 UI 细项自测后按垂直切片 Review，不按按钮逐项正式 Review。
- H06 只复用匹配 tree SHA + selector + fixture digest 的证据；最终 tree 全量验证一次。
