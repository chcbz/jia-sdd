# 案卷阁阅读 MVP design

## 2026-10-23 通用典籍解耦候选（尚未部署）

核验更新（2026-10-23，范围：本节通用典籍解耦）：API `58aaa4dab2` 的Flow238、Web `5cc78184` 的Flow298均测试/构建成功；生产JAR已核实不含书籍fixture，独立数据包validate正反例通过。生产未切换，60秒启动未实测。完整测试数量、跳过项及制品摘要见下述handoff。

用户新要求：书籍数据由数据库维护，新增书籍不改程序。此节是当前候选合同；下方固定《水浒传》/120回/必需引首/启动导入是历史MVP基线，不再用于指导本次实现。API候选 `58aaa4dab2`（base `683adf775f`），Web候选 `5cc78184`（base `232a32ff`）；云端结果和完整SHA见 `../../docs/implementation/handoffs/ARCHIVE-CONTENT-DECOUPLING-20261023.md`，不能据候选合同认定线上已切换。

- 应用启动仅做schema初始化/核验，不读书籍资源、不导入、不全文对账；书籍内容不进生产classpath。
- `GET /archive/v1/works` 的 data 为 `{items:[{workId,title,editionId,chapterCount}]}`；只列READY活动版。目录改为必需 `?workId=...`，不隐式选择固定书。
- 正章节数量由数据决定，支持超过120章；`activeEdition.preface` 可为null。数据库维持原FK/唯一键/总数校验，旧库两项CHECK需显式一次性迁移。
- 完读以该edition实际末章末段末字节为准；提问请求必需顶层 `editionId`，服务端核验该版本/选文，锚点结构不变。
- 前端按数据库书架展示；切书保存旧进度，阻止静默丢弃待处理写操作，旧书响应不能污染新书状态。身份/ACL/CAS/幂等仍保留。
- 新增书籍走仓库外数据包准备→SHA校验→显式事务发布→业务核验。READY正文不可原位改，修订使用新edition。通用工具和恢复边界见API `ops/archive/README.md`。
- 无生产迁移、导入、部署、重启授权；不宣称已达到60秒整体启动。当前轻量自检与正式Flow验证分别记录。


<!-- SDD delivery reconciliation 2026-09-06 -->
## 2026-09-06 全量状态核对

H01–H05W 已接受，H06 已发布；旧 reader 修复随 Web101ac4c 发布，CORS 补丁也已部署并通过可信/非可信预检，剩余 authenticated adapter/真实阅读闭环未完成，整体不归档。

完整任务/版本/证据及未完成项见 [delivery-status.md](delivery-status.md)。归档：仅 AR-20260906-05 / AR-20260906-04 历史发布记录。原文合同及历史验收材料保留，不把发布例外标成 PASS。

### 本次设计边界补充

增补用户 UX 要求：点击阅读先进入典籍列表，选择典籍后进入占满可用视口的沉浸阅读；目录默认收起、允许按需展开。浏览器原生全屏受宿主权限约束，不保证微信强制横屏。保留 /archive/v1、exact-scope、CAS/幂等与账户切换 generation fencing。CORS 放行应精确匹配受信 origin/合法 headers，不用通配或移除幂等键绕过。UX 列表/全屏/目录默认收起及 authenticated save/read 闭环仍是待核实要求；CORS 五行补丁则已有独立 ACCEPT 与生产预检证据（可信 OPTIONS200 含幂等键、非可信403无 AllowOrigin），两者不能混称未验证，也不重复修补。
<!-- END SDD delivery reconciliation -->

## User flow

1. 用户进入案卷阁，默认看到“典籍阅读”，仍可切换到原“案卷检索”。
2. 首次进入加载固定《水浒传》版本目录及本人进度；有进度时显示“继续阅读”。
3. 阅读器支持章回目录、上一回/下一回、段落定位、自动保存状态和显式书签。
4. 用户可在当前段落或选文处创建私人手札；冲突时保留本地草稿，不静默覆盖。
5. 用户选择正文后可“问案卷书吏”；服务端重建并校验选文，再创建单轮问题。
6. 吴用仍是普通 Agent；任职机制未上线前，首期问题明确路由到 built-in 降级角色“案卷书吏”。

## Core invariants

- `workId=shuihuzhuan`，首版 `editionId=shuihuzhuan-zh-120-v1`。
- ACTIVE 版本的正文、章节顺序、段落边界和 ID 永不原地修改。
- 正文身份以 UTF-8 原始字节与 SHA-256 为准；不得隐式 trim 或 Unicode 归一化。
- 用户资源只允许精确 `(tenantId, clientId, ownerJiacn)` 所有者访问；不存在和越权统一 404。
- owner/tenant/client 只取服务端认证上下文，不接受请求体传入，也不回退 `Anonymous`。
- `/chat/library/search` 继续表示项目案卷/记忆检索，不作为典籍正文事实源。
- Agent prompt 不隐式包含私人手札、书签或记忆搜索结果。

## Content contract

### Source candidate

- 上游：Wikisource 120 回本的确定性抓取产物。
- 冻结镜像：`pondahai/shuihu-wiki` commit `b8d911354bd4d8f399e140c458853926f6beb875`。
- 原始文件：`data/shuihu_raw.txt`。
- 原始 SHA-256：`1023e78e50df0b0902b47ea2f29f0901aa14e55b6d243bd1ce8cfa3202440b47`。
- 验证结果：120 个连续回目，末回为“第一百二十回 宋公明神聚蓼儿窪 徽宗帝夢游梁山泊”。
- 发布包必须包含来源与许可归属说明；若最终批准来源变化，必须更换原始 SHA；若正文或段落边界变化，必须更换 `editionId`。

### Stable IDs

- work title 精确为 `水滸傳`；chapter：`shuihuzhuan-zh-120-v1-c001` … `-c120`。
- paragraph：`<chapterId>-p0001`，按章内原始顺序递增。
- manifest 记录每章标题、段落数量、UTF-8 byte length、paragraph SHA-256 和整版 manifest SHA-256。
- 内部自增主键不得作为外部正文或用户资源 ID。

### Text anchor

```json
{
  "editionManifestSha256": "64-lowercase-hex",
  "blockType": "CHAPTER",
  "blockId": "shuihuzhuan-zh-120-v1-c001",
  "segments": [{
    "paragraphId": "shuihuzhuan-zh-120-v1-c001-p0003",
    "startByte": 0,
    "endByte": 48,
    "paragraphSha256": "64-lowercase-hex"
  }],
  "selectionSha256": "64-lowercase-hex"
}
```

offset 是 UTF-8 byte 左闭右开区间，必须落在码点边界；`blockType` 只能是 `PREFACE` 或 `CHAPTER`，`blockId` 必须分别等于该版 `prefaceId` 或 `chapterId`。最多 16 个同一 block 内的连续 segment，总选文不超过 8192 bytes。服务端按段落原字节重建权威 `selectedText`。

## Data model and state

- `archive_work`、`archive_edition`、`archive_chapter`、`archive_paragraph`。
- `archive_reader_progress`：每 owner/client/edition 一行，`ABSENT -> IN_PROGRESS -> COMPLETED`，重读不清除 `completedAt`。
- `archive_bookmark`、`archive_note`：客户端小写 UUID，`ACTIVE -> DELETED` tombstone。
- `archive_idempotency`：owner + method + canonical path + key，保存请求哈希与首次响应。
- `archive_question`、`archive_question_event`、`archive_outbox`：在 H05A 中实现，状态为 `QUEUED -> RUNNING -> SUCCEEDED/FAILED_RETRYABLE/FAILED_FINAL`。

所有可变资源使用 `version BIGINT` CAS；0 行更新返回 409，不自动覆盖或合并。

## API and data contract

Base path：`/archive/v1`。正常响应延续 `JsonResult`；错误必须同时使用正确 HTTP status。

### Read-only content

- `GET /catalog`：作品、ACTIVE 版本、manifest、120 回目录。
- `GET /editions/{editionId}/chapters/{chapterId}`：章标题和有序段落。
- Content JSON semantic representation version is `1`. Catalog `data` is exactly `representationSchemaVersion, workId, title, activeEdition`，其中 `title` 精确为 manifest 冻结值 `水滸傳`; `activeEdition` contains `editionId, manifestSha256, sourceSha256, prefaceParagraphCount, chapterParagraphCount, readerParagraphCount, readerUtf8ByteLength, preface, chapters`. Preface/catalog block summaries contain `blockType, blockId, number, title, paragraphCount, utf8ByteLength, etag`. A preface/chapter `data` object is exactly `representationSchemaVersion, editionId, manifestSha256, blockType, blockId, number, title, paragraphCount, utf8ByteLength, paragraphs`; paragraph fields are exactly `paragraphId, ordinal, text, utf8ByteLength, sha256`. Preface `number` is `null`. Field meaning/removal/addition or media-type semantic change requires a new representation version.
- Catalog uses weak ETag `W/"archive-catalog-json-v1-<manifestSha256>"`. Preface/chapter use weak ETag `W/"archive-block-json-v1-<blockContentSha256>"`. The `JsonResult` transport envelope and harmless serialization-byte changes are intentionally outside weak semantic equality; API media type remains JSON UTF-8.
- `blockContentSha256` is SHA-256 lowercase hex over: `editionManifestSha256 + LF + blockType + LF + blockId + LF + title + LF`, then for every paragraph in order append `paragraphId + TAB + paragraphSha256 + TAB + canonicalDecimal(utf8ByteLength) + LF`. Any title, order, boundary or text hash change changes the validator.
- `If-None-Match` follows HTTP weak comparison: a valid comma-separated entity-tag list matches when any opaque tag equals the current tag regardless of `W/`; `*` matches an existing representation. A match returns 304 with no body. Malformed conditional syntax returns 400 `INVALID_CONDITIONAL_HEADER`; a valid stale tag returns 200. Golden vectors live in `golden-summary.json` and focused tests.

### Progress

- `GET /me/progress/{editionId}`；未创建时 `data:null`。
- `PUT /me/progress/{editionId}`：`expectedVersion` + location + `markCompleted`。
- 创建时 `expectedVersion=0`；完成仅允许位于末章末段末尾。

### Bookmarks

- `GET /me/bookmarks?editionId=...&cursor=...&limit=100`
- `PUT /me/bookmarks/{bookmarkId}`
- `DELETE /me/bookmarks/{bookmarkId}`，使用版本前置条件并返回 tombstone。

### Private notes

- `GET /me/notes?editionId=...&chapterId=...&cursor=...&limit=100`
- `PUT /me/notes/{noteId}`：纯文本最多 20,000 UTF-8 bytes，可带 anchor。
- `DELETE /me/notes/{noteId}`。

### Selected-text question

- `PUT /me/questions/{questionId}`：创建并返回 202。
- `GET /me/questions/{questionId}`：状态与答案快照。
- `GET /me/questions/{questionId}/events`：SSE，`Last-Event-ID` 为 question-local sequence。
- `POST /me/questions/{questionId}/retry`：仅 FAILED_RETRYABLE。
- 请求中出现 `targetAgentId`、`agentId` 或角色名时返回 422；首期 responder 固定为 `archive-clerk-v1 / 案卷书吏 / fallback`。

### Errors

- 401 `AUTH_CONTEXT_INCOMPLETE`
- 404 `ARCHIVE_RESOURCE_NOT_FOUND`（也用于越权隐藏）
- 400 `INVALID_EVENT_CURSOR` / `INVALID_CONDITIONAL_HEADER`
- 409 `VERSION_CONFLICT` / `VERSION_EXHAUSTED` / `IDEMPOTENCY_KEY_REUSED`
- 422 `INVALID_VERSION` / `INVALID_TEXT_ANCHOR` / `CONTENT_HASH_MISMATCH` / `ROUTING_NOT_SUPPORTED`
- 429 `QUESTION_RATE_LIMITED`
- 503 `QUESTION_PROVIDER_UNAVAILABLE`

## Transactions and failure windows

- 正文分批导入 STAGING；验证完整性后单事务切换 ACTIVE。
- 进度/书签/手札的 CAS、tombstone 和幂等响应同事务。
- 响应丢失时相同幂等键返回首次结果；相同 key 不同请求哈希返回 409。
- 两标签页同时更新时一个成功、一个冲突；前端保留未保存手札草稿。
- 问题创建、首事件、outbox 和幂等响应同事务；外部模型调用不得占用数据库事务。
- SSE 事件先持久化再发布；断线以 sequence 重放，重复 sequence 幂等忽略。
- Elasticsearch 不可用不得影响典籍阅读、进度、书签和手札。

## Frontend behavior

- `LibraryPanel` 保留现有 props/emits 和“案卷检索”，新增页签作为外壳。
- 新建 reader component/composable 和 `createApi('/archive/v1')` 门面，不把正文混入 `useHallLibrary` 搜索状态。
- 滚动稳定后 debounce 保存；只有服务端确认才显示“已保存”。`pagehide` 只做尽力 flush。
- 进度冲突刷新服务端位置；手札冲突保留本地草稿并提示人工处理。
- 不读取隐藏 selectedAgent，不调用 `/agent/active`。

## Compatibility and rollout

1. H01 冻结规格、内容来源、manifest 生成规则和失败测试矩阵。
2. H02/H03 实施 schema、正文、用户数据 API，feature flag 默认关闭。
3. H04 实施 Web 阅读闭环；旧案卷检索保持可用。
4. H05A 单独实施选文问“案卷书吏”后端，H05W 单独实施前端与恢复，不与阅读数据混审。
5. H06 完成真实 MySQL、两身份/两 client、浏览器和发布恢复门禁。
6. 回滚旧代码时保留新表和内容，不执行 destructive down migration。

## Decisions

- 建立 `/archive/v1` 独立事实域；正文不进入 Elasticsearch。
- 首版固定 120 回，不支持上传和多版本。
- 私人数据 exact-scope、CAS、幂等；吴用不是 built-in。
- 任职、悬赏、积分报酬延后到阅读闭环验收后另立 SDD。

## Contract clarifications required before H02

### Composite owner and idempotency scope

`ownerScope` always means the full server-derived tuple `(tenantId, clientId, ownerJiacn)`; no component may be omitted or supplied by the client. Every idempotency row and lookup key is exactly `(tenantId, clientId, ownerJiacn, HTTP method, canonical path including sorted query, Idempotency-Key)`.

All PUT/POST/DELETE requests carry `Idempotency-Key` as an HTTP header. The server rejects blank, non-ASCII or over-128-byte keys. The request hash is SHA-256 over method, canonical path and canonical UTF-8 JSON: recursively sorted object keys, array order preserved, no insignificant whitespace, duplicate JSON keys rejected, integer fields represented as decimal strings where specified, and floats forbidden in write DTOs. Same composite scope/key/hash replays the original HTTP status and response; same scope/key with a different hash returns 409. Records are retained at least seven days and are committed in the same transaction as the business mutation.

### Version wire rules

All resource versions, event sequences and cursors use canonical non-negative signed-BIGINT decimal strings on the wire and must never be converted to JavaScript `Number`. The only valid lexical form is `0|[1-9][0-9]{0,18}` and the numeric value must be `<= 9223372036854775807` (`Long.MAX_VALUE`); leading zeroes, signs, whitespace, exponent notation and larger values are invalid. Invalid request versions return 422 `INVALID_VERSION`; invalid `Last-Event-ID` returns 400 `INVALID_EVENT_CURSOR`, with zero writes/events. A mutation that would increment `Long.MAX_VALUE` returns 409 `VERSION_EXHAUSTED`, also with zero writes/events.

Create uses `expectedVersion:"0"`; every successful mutation returns `version:"N+1"`. Progress/bookmark/note PUT carries `expectedVersion`; DELETE carries `If-Match: "vN"` and advances to a DELETED tombstone at `N+1`. A 409 response returns the current decimal-string version but never another owner's data. Client retry is allowed only with a new request derived from the returned current state; blind overwrite is forbidden.

### Preface completeness

The edition includes `prefaceId=shuihuzhuan-zh-120-v1-preface` and its 11 stable paragraphs. `GET /editions/{editionId}/preface` returns it using the same paragraph DTO/hash/ETag rules as chapters. Catalog orders the preface before chapter 1. Progress locations and text anchors use the same `(blockType, blockId)` discriminator and may reference either the preface or a chapter; completion still requires the end of chapter 120. Manifest exposes `prefaceParagraphCount=11`, `chapterParagraphCount=3666`, `readerParagraphCount=3677` and byte lengths. The two repeated Wikisource public-domain notice lines per chapter remain covered by the frozen source SHA but are excluded from reader paragraphs.

### Multi-segment selected text

Segments must be in strictly increasing paragraph order within one chapter or the preface, without duplicates or overlap. Paragraph ordinals must be contiguous. The first and last segment may be partial; every intermediate paragraph must span byte `0..utf8ByteLength`. Each offset must be a UTF-8 code-point boundary. The authoritative selected bytes are segment slices joined in order by exactly two LF bytes (`0x0A 0x0A`); `selectionSha256` is computed over those joined bytes and `selectedText` is their UTF-8 decoding. Empty selection is invalid.

### Durable question event/replay contract

Question snapshot contains decimal-string `version` and `currentSequence`, status, responder, complete persisted answer, retry count and last error code. Events contain `schemaVersion`, `questionId`, decimal-string `sequence`, `type`, `occurredAt` and type-specific payload. Allocation locks the exact-scoped question row, increments `current_sequence` exactly once, inserts `(questionId, sequence)` in the same transaction, commits, then publishes the persisted event after commit. Rollback publishes nothing.

SSE subscribes to the exact-scoped live source before database replay and creates a bounded per-connection buffer. It then reads the persisted question `currentSequence` as `replayWatermark`, replays `(Last-Event-ID, replayWatermark]`, and merges/deduplicates buffered live events by sequence. Events that arrive between subscription and watermark capture may exist in both sources and are emitted once; events above the watermark remain buffered until replay reaches the watermark, then are drained in exact-next order before switching to direct live delivery. Buffer overflow, cursor ahead, truncated history, replay gap or any unverifiable continuity emits `resync_required` without allocating a sequence and then closes the stream.

On client disconnect, emitter timeout/error, `resync_required`, question switch or feature-flag disable, the server atomically cancels the live subscription, in-flight replay query/publisher and heartbeat, marks the emitter closed, and clears the buffer; late callbacks must not write to a closed emitter. The Web owner closes the old stream, GETs a fresh snapshot, replaces state, then reconnects from `currentSequence`. One composable owns each active reader, retry timer and polling fallback; question switch, feature-flag off and unmount cancel all readers/timers. Heartbeats allocate no sequence.

Question creation, selected-text snapshot, sequence 1 event, outbox and idempotency response commit together. Worker claim uses a lease plus fencing token; provider calls occur outside DB transactions. Only the current fencing token may persist deltas or completion. If provider returns but persistence fails, the attempt remains retryable and a later fenced attempt may regenerate; no unpersisted answer is exposed. Persisted delta before publication is recovered by replay. Maximum three attempts, then `FAILED_FINAL`.
