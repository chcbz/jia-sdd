# 页面与状态覆盖

“覆盖”表示页面可打开、入口/代表性状态可查看，不代表真实业务功能已验证。还原层级见 [design.md](design.md)。

| 页面 | 入口 | 对照源码 / 范围 |
|---|---|---|
| 办事首页 | [打开](prototype/index.html#home) | JuyiHall.vue / HallOverview.vue；快速需求、资料选择、事项入口 |
| 事项 | [打开](prototype/index.html#tasks) | BountyPanel.vue；列表、需求与详情入口 |
| 提出需求 | [打开](prototype/index.html#create) | HallDraftEditor.vue；正文、可选资料、取消选择 |
| 点将册 | [打开](prototype/index.html#agents) | AgentPanel.vue；选择好汉、密议、点将并议事、招贤令 |
| 事项详情 | [打开](prototype/index.html#detail) | BountyPanel.vue；资料、进展、正式成果与验收 |
| 榜文议事 | [打开](prototype/index.html#chat) | BountyDiscussionPanel.vue / ChatPanel.vue / HallChatComposer.vue |
| 密议 | [打开](prototype/index.html#private) | PrivateDiscussionPanel.vue；独立演示会话，不创建真实事项 |
| 厅前公议 | [打开](prototype/index.html#public) | PublicDiscussionPanel.vue；共享输入布局，示例发言 |
| 资料 / 百宝箱 | [打开](prototype/index.html#workspace) | PersonalWorkspace.vue；资料、示例已保存成果 |
| 资料详情 | [打开](prototype/index.html#file) | 文件版本/预览/下载/管理入口；结构原型 |
| 我的 | [打开](prototype/index.html#mine) | HallMinePage.vue；好汉、典籍、消息、实景、个人中心 |
| 典籍阁 | [打开](prototype/index.html#library) | LibraryPanel.vue；典籍阅读、案卷检索，结构原型 |
| 阅读器 | [打开](prototype/index.html#reader) | archive/ArchiveReader.vue；目录、书签、手札，结构原型 |
| 消息 | [打开](prototype/index.html#messages) | HallOverview.vue messagesOnly；待处理/草稿，结构原型 |
| 招贤令 | [打开](prototype/index.html#catalog) | PersonaCatalogPanel.vue；接入/山寨安顿入口，不执行安装或付费 |
| 厅中实景 | [打开](prototype/index.html#map) | HallStage.vue；已有厅堂静态美术与入口，不模拟实时游戏 |
| 使用帮助 | [打开](prototype/index.html#help) | 现有帮助入口的离线体验说明，不扩展新业务页面 |
| 个人中心入口 | [打开](prototype/index.html#account) | JuyiHall.vue openProfile；外部模块边界，不复制账号页面 |

## 可重复打开的议事状态

每个链接独立打开会建立相应的脱敏演示状态。`scenario` 控制代表性界面，不控制真实业务。

| 状态 | 入口 | 展示内容 |
|---|---|---|
| 可输入 | [打开](prototype/index.html?scenario=ready#chat) | 四项最新布局，＋弹层、历史、另起话头 |
| 空话头 | [打开](prototype/index.html?scenario=empty#chat) | 空消息区、文本输入 |
| 等待回复 | [打开](prototype/index.html?scenario=waiting#chat) | 等待提示和禁用输入 |
| 流式回复 | [打开](prototype/index.html?scenario=streaming#chat) | 回话未尽示意，不运行 SSE |
| 读取失败 | [打开](prototype/index.html?scenario=error#chat) | 错误提示与重试 |
| 录音 | [打开](prototype/index.html?scenario=recording#chat) | 录音提示、停止、取消；不启用麦克风 |
| 转写草稿 | [打开](prototype/index.html?scenario=voice-review#chat) | 追加、替换、丢弃，不自动发送 |
| 多媒体成果 | [打开](prototype/index.html?scenario=results#chat) | 图片、音频、文档、文字，预览/下载/保存/引用修改 |
| 完成 | [打开](prototype/index.html?scenario=completed#detail) | 已完成详情及本次验收结果 |

## 交互检查范围

- 桌面 1440 和手机 390 两种 viewport 的 18 个页面 DOM 与本地资源路径。
- 9 个议事状态、四项布局约束、无工作空间按钮。
- ＋ → 资料选择 → 确认；语音回答设置与 AI 告知；录音示意 → 转写草稿。
- 顶部历史 → 删除确认；重取、另起话头的原型入口。
- 多媒体成果 → 事项详情 → 验收；无验收多选。
- 我的 → 典籍检索；资料 → 详情 → 重命名 / 回收 / 恢复。

## 不声称已覆盖的真实能力

网络错误/重连、Agent 真实处理、Provider 输出、实际文件权限、支付与托管安装、数据库幂等、真实录音、原生系统键盘、设备横竖屏、melonJS 移动/遮挡、真实章页与阅读进度、完整外部个人中心。补充页面的逐像素视觉验收尚未执行。
