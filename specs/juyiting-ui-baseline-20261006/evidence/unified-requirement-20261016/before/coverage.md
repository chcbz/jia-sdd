## 2026-10-13 控件反馈修订

P02 在页内标题右侧统一“提出需求”（空/非空、桌面/手机），搜索与刷新独占一行，能力/状态下移；P09 去旧渐变hover，保留主按钮/选中分类层级和键盘可见焦点。仅离线提案，不改业务契约。根基线 `5db58c2d17dfbab868f6e550f84d6a4ed8c48203` + 本地文件，输入SHA和证据见 `evidence/ui-feedback-20261013/`；下方简化轮的空态创建与搜索三列描述由本节更新。

---

## 当前增量：界面简化候选（2026-10-13）

P01 首页收敛为需求与当前事项列表；P02 四组筛选 + 10种细状态与搜索交集；P05 按沟通、办理、验收、未知、终态突出唯一主操作。范围为离线设计，不是对应产品源码已实现。原值与新证据在 `evidence/ui-simplify-20261013/`，原源码同步和历史覆盖在下方保留。来源为根 `77bd860c3660763911dc79bce7a3278420a5e2b2` 加此前未提交原型，受测输入以报告 SHA 为准。

---

# 当前增量覆盖 · 2026-10-13

源码 `cb730681`，仅本轮列明切片；原外壳与历史覆盖保留下方，不代表整站最新或线上验收。

| 编号 | 本轮覆盖 | 入口 |
|---|---|---|
| P19 | 正式成果独立页；无页面工作空间入口 | [打开](prototype/index.html?reset=1&scenario=results#results) |
| S16 | 未开工事项取消确认/保留，成功后只读 | [打开](prototype/index.html?reset=1&scenario=cancel-ready#detail) |
| S17 | 取消未知：保留原事项，只核对不重提 | [打开](prototype/index.html?reset=1&scenario=cancel-unknown#detail) |
| S18 | 已取消历史成果，两类重读/示例下载 | [打开](prototype/index.html?reset=1&scenario=cancelled#results) |
| S19 | 历史读取失败不伪报恢复、不重跑 | [打开](prototype/index.html?reset=1&scenario=history-error#results) |
| S20 | Runtime 首次接入/脱敏 handoff/单次登记示意 | [打开](prototype/index.html?reset=1&scenario=runtime-ready#catalog) |
| S21 | 已有安装仅查询，不重复登记 | [打开](prototype/index.html?reset=1&scenario=runtime-existing#catalog) |
| S22 | 登记未知只查询同一安装，不自动注册 | [打开](prototype/index.html?reset=1&scenario=runtime-unknown#catalog) |
| S23 | 材料不匹配或过期拒绝登记（固定失败示例） | [打开](prototype/index.html?reset=1&scenario=runtime-invalid#catalog) |

P03 替换旧任务榜内嵌表单为 HallDraftEditor 独立私人草稿；覆盖保存、确认交办、选人后重存/授权、刷新原回执及不修改正式事项。P02 同步单行搜索/本领/44px 刷新按钮，移除榜内重复创建入口；P04 点将/密议按钮排列保留；P05/P15/P19 纳入新交互。运行时状态仅本地 fixture，PENDING/ACTIVE 不等于在线。取消仅可用于明确未开始的无资金示例，不能推导真实服务端授权/幂等已验收。

---

# 页面与状态覆盖 · 交互补全 2026-10-07

唯一主入口：[优化界面原型](prototype/index.html#home)。[可点击索引](prototype/pages.html) · [交互说明](interaction-guide-20261007.md)。覆盖只表示离线交互，不代表产品上线或真实业务闭环通过。

## 页面 P01–P18

| 编号与名称 | 交互范围 | 入口 |
|---|---|---|
| P01 · 办事 | 快速需求、资料选择、最近事项 | [打开](prototype/index.html?reset=1&scenario=ready#home) |
| P02 · 事项 | 状态筛选、空列表、事项入口 | [打开](prototype/index.html?reset=1&scenario=ready#tasks) |
| P03 · 提出需求 | 正文/附件-only、成功清空、失败保留 | [打开](prototype/index.html?reset=1&scenario=ready#create) |
| P04 · 点将册 | 选择好汉、点将、密议、招贤令 | [打开](prototype/index.html?reset=1&scenario=ready#agents) |
| P05 · 事项详情 | 资料、进展、回议事、正式验收 | [打开](prototype/index.html?reset=1&scenario=ready#detail) |
| P06 · 榜文议事 | 需求、补充、多媒体、稿件引用 | [打开](prototype/index.html?reset=1&scenario=results#chat) |
| P07 · 密议 | 每位好汉独立话头与草稿 | [打开](prototype/index.html?reset=1&scenario=ready#private) |
| P08 · 厅前公议 | 与正式事项、密议隔离 | [打开](prototype/index.html?reset=1&scenario=ready#public) |
| P09 · 资料/百宝箱 | 分类、可选保存、回收站、再引用 | [打开](prototype/index.html?reset=1&scenario=ready#workspace) |
| P10 · 资料详情 | 预览、下载、重命名、回收/恢复 | [打开](prototype/index.html?reset=1&scenario=ready#file) |
| P11 · 我的 | 原有次级入口、全部入口 | [打开](prototype/index.html?reset=1&scenario=ready#mine) |
| P12 · 典籍阁 | 书架、案卷检索、结果/空态 | [打开](prototype/index.html?reset=1&scenario=ready#library) |
| P13 · 阅读器 | 目录、章节、书签、手札 | [打开](prototype/index.html?reset=1&scenario=ready#reader) |
| P14 · 消息 | 待处理事项、草稿与空态 | [打开](prototype/index.html?reset=1&scenario=ready#messages) |
| P15 · 招贤令 | 好汉与接入/安顿边界 | [打开](prototype/index.html?reset=1&scenario=ready#catalog) |
| P16 · 厅中实景 | 原美术与功能入口、静态地图 | [打开](prototype/index.html?reset=1&scenario=ready#map) |
| P17 · 使用帮助 | 当前最短流程及页面索引 | [打开](prototype/index.html?reset=1&scenario=ready#help) |
| P18 · 个人中心入口 | 保留外部账号模块边界 | [打开](prototype/index.html?reset=1&scenario=ready#account) |

## 状态 S01–S15

| 编号与名称 | 交互范围 | 入口 |
|---|---|---|
| S01 · 可输入 | 最新工具栏与输入框 | [打开](prototype/index.html?reset=1&scenario=ready#chat) |
| S02 · 空话头 | 空消息与可编辑输入 | [打开](prototype/index.html?reset=1&scenario=empty#chat) |
| S03 · 等待回复 | 禁重复发送与操作 | [打开](prototype/index.html?reset=1&scenario=waiting#chat) |
| S04 · 流式示意 | 回话未尽，不运行真实SSE | [打开](prototype/index.html?reset=1&scenario=streaming#chat) |
| S05 · 读取失败 | 重试只读原话头，不重发 | [打开](prototype/index.html?reset=1&scenario=error#chat) |
| S06 · 录音示意 | 停止、取消，不启用麦克风 | [打开](prototype/index.html?reset=1&scenario=recording#chat) |
| S07 · 转写待确认 | 追加/替换/丢弃，不自动发送 | [打开](prototype/index.html?reset=1&scenario=voice-review#chat) |
| S08 · 多媒体成果 | 预览下载、保存可选、引用修改 | [打开](prototype/index.html?reset=1&scenario=results#chat) |
| S09 · 已完成 | 只读成果，不再验收或改稿 | [打开](prototype/index.html?reset=1&scenario=completed#detail) |
| S10 · 创建失败 | 保留草稿与资料，返回修改 | [打开](prototype/index.html?reset=1&scenario=create-failure#home) |
| S11 · 创建未知 | 核对状态，不重复创建 | [打开](prototype/index.html?reset=1&scenario=create-unknown#home) |
| S12 · 发送未明确受理 | 创建点将后发送补充，保留输入 | [打开](prototype/index.html?reset=1&scenario=reply-failure#home) |
| S13 · 验收状态未知 | 创建点将后验收，查询原操作 | [打开](prototype/index.html?reset=1&scenario=accept-unknown#home) |
| S14 · 验收失败 | 冻结成果保留，不伪报成功 | [打开](prototype/index.html?reset=1&scenario=accept-failure#home) |
| S15 · 独立root阻塞 | 来源关联待实现，不能确认验收 | [打开](prototype/index.html?reset=1&scenario=independent-roots#home) |

## 验证与边界

真实 Chromium 检查桌面1440、手机390及窄屏320布局、原生点击、示例下载与音频播放；报告见 [acceptance.md](acceptance.md)。并非真机、生产应用或线上视觉采样。固定源码来源和历史美术不改。

不模拟真实 Agent/Provider、SSE、支付、数据库、权限、麦克风、系统键盘、完整账号模块、实时地图、真实书库。独立图文 root 长期关联恢复 R01 仍待实现；相关验收被明确阻塞，不能由示例成功替代。
