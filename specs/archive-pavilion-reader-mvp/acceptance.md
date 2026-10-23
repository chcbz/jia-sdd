# 案卷阁阅读 MVP acceptance

<!-- SDD delivery reconciliation 2026-09-06 -->
## 2026-09-06 全量状态核对

H01–H05W 已接受，H06 已发布；旧 reader 修复随 Web101ac4c 发布，CORS 补丁也已部署并通过可信/非可信预检，剩余 authenticated adapter/真实阅读闭环未完成，整体不归档。

完整任务/版本/证据及未完成项见 [delivery-status.md](delivery-status.md)。归档：仅 AR-20260906-05 / AR-20260906-04 历史发布记录。原文合同及历史验收材料保留，不把发布例外标成 PASS。

源码验收、生产发布、真实用户/设备验收分开。已有测试仅复用记录；本次为文档核对，无新增业务测试。未证明项保留未验证。
<!-- END SDD delivery reconciliation -->

## Contract/content

- [x] 内容来源、许可归属、上游 commit、原始 SHA-256 和 manifest SHA-256 可审计。
- [x] 引首11段与120回正文共3677个 reader paragraphs 均有稳定ID、API路径、byte length/hash；每回重复的两行 Wikisource 许可元数据不进入正文。
- [x] ACTIVE 内容恰有 120 个连续章回；章节/段落 ID、manifest 与 versioned weak ETag 可按 golden vectors 确定性重建，并按 HTTP weak comparison 处理 `If-None-Match`。
- [x] 发布后正文不可原地修改；内容变化会产生新 `editionId`。

## Reading and personal data

- [ ] 认证用户可浏览目录、完整章回、继续阅读、上一回/下一回。
- [ ] 阅读进度跨会话恢复；两个标签页并发不会静默覆盖。
- [ ] 用户可创建/删除书签和私人手札；冲突时保留本地草稿。
- [ ] 两个 OAuth 身份和两个 client 的进度、书签、手札完全隔离；越权统一 404。
- [ ] 缺失认证 scope 时零写入并 fail closed。

## Ask Agent

- [ ] 中文多字节、跨段选文由服务端按 byte offset/hash 精确重建。
- [ ] 默认 responder 明确为“案卷书吏”，不得冒充吴用或使用当前 selectedAgent。
- [ ] 问题创建重放不重复调度；版本/sequence全程使用 canonical decimal string，越过 `Long.MAX_VALUE` fail closed。
- [ ] SSE live-before-replay、watermark/buffer exact-next、gap/cursor-ahead/truncation/overflow `resync_required`、snapshot替换及服务端/客户端资源清理通过。
- [ ] provider 故障不影响阅读、进度、书签和手札。

## Compatibility/release

- [ ] `/chat/library/search` 与旧“引入传令”行为保持兼容。
- [ ] Elasticsearch 停止时典籍阅读和私人数据仍可用。
- [ ] API targeted/full、隔离 MySQL、Web tests/build 和真实浏览器 smoke 有可复用证据。
- [ ] feature flag 默认关闭；部署制品 SHA-pinned，备份/恢复和回滚步骤验证通过。

## Verification evidence

- API revision:
- Web revision:
- Content artifact/manifest:
- Commands/tests:
- Result: pending
