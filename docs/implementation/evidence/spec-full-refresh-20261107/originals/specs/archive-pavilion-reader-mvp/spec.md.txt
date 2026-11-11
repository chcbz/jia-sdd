# 案卷阁阅读 MVP

> 文档收口（2026-10-23）：保留阅读器、进度/书签/私人手札和内容样本；不因旧pending重复判定后续已测场景。 本轮仅核对文档归属与覆盖，不重新验证源码/上线；执行规则以根AGENTS为准。


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
<!-- END SDD delivery reconciliation -->

## Problem

当前案卷阁仅支持项目案卷/记忆检索与引用，不能承载完整书籍阅读，也没有稳定的章回定位、跨会话阅读进度、书签、私人手札或选文问 Agent 能力。若直接把正文塞入现有 `/chat/library/search`，会混淆公开典籍与私人记忆的事实源，并继承 Elasticsearch 降级与 ACL 边界。

## Goals

1. 首期提供一个固定、不可变的《水浒传》120 回完整版本。
2. 支持目录、按回阅读、继续阅读、上一回/下一回。
3. 为认证用户保存阅读进度、书签和私人手札，避免并发静默覆盖。
4. 支持基于服务端校验选文向默认“案卷书吏”提问；吴用保持普通 Agent，不获得内建身份。
5. 保留现有案卷检索和“引入传令”能力，不破坏聚义厅现有主线。

## Non-goals

- 用户上传 EPUB/PDF、OCR、后台编辑和多版本锚点迁移。
- 全文/语义搜索、离线阅读、共享批注、导出、音频和复杂阅读统计。
- 任职、悬赏和积分报酬；这些在阅读闭环验收后另立 SDD。
- 按“吴用”姓名、地图选中态或 `/agent/active` 自动路由。
- 首期多轮 Agent 会话、多 Agent 协作或 Agent 读取私人手札。

## Scope

- API：新建 `/archive/v1` 事实域，提供固定正文、进度、书签、手札和单轮选文提问接口。
- Web：扩展案卷阁为“典籍阅读/案卷检索”双入口，新增阅读器及独立状态 composable。
- Content：冻结 120 回正文来源、原始 SHA-256、章回/段落稳定 ID 和 manifest。

## Constraints and risks

- 正文版本发布后不可原地修改；任何勘误发布新 `editionId`。
- 私人数据必须按服务端身份精确隔离；缺少 tenant/client/jiacn 时 fail closed。
- 正文不进入 Elasticsearch；现有 `/chat/library/search` 保持独立。
- 进度、书签、手札使用 CAS；写入使用幂等键。
- P0 schema/ACL/事务工作必须由 `critical_worker` 实施并独立 Review。
- 当前 C08 发布门禁仍为 NO-GO；本功能可以先完成规格与独立候选，但不得绕过现有发布门禁部署。
- 记录 Gradle 全量、隔离 MySQL、npm build 和 integration worktree 的资源快照，但固定内存/磁盘阈值不再阻断执行；真实 OOM/ENOSPC 仍需归因。
