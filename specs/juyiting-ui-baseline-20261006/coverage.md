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
