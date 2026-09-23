# 控件与跳转属性登记（V3.1）

下表由实际DOM采集去重。场景名见详设。`data-*`不是URL：通常调用navigate/openPanel/applyAction，地址栏不变；没有href的按钮不可伪称支持复制链接/新标签打开。所有示例id仅用于本地fixture。完整DOM路径、aria属性、type/name/placeholder、样式索引及视口见evidence/controls.json。

|场景|显示文字或无障碍名称|标签 / 目标属性|
|---|---|---|
|overview|聚聚义厅一起，把事情办成。|`button` {"data-view": "overview"}|
|overview|办事概览|`button` {"data-view": "overview"}|
|overview|我的事项|`button` {"data-view": "bounty"}|
|overview|厅内议事|`button` {"data-view": "chat"}|
|overview|点将册|`button` {"data-view": "agents"}|
|overview|百宝箱|`button` {"data-view": "files"}|
|overview|典籍阁|`button` {"data-view": "archive"}|
|overview|厅中实景去梁山走一走|`button` {"data-mode": "map"}|
|overview|偏好设置|`button` {"data-view": "settings"}|
|overview|使用帮助|`button` {"data-view": "help"}|
|overview|体验账号本地演示空间|`button` {"data-view": "account"}|
|overview|消息通知|`button` {"data-view": "messages"}|
|overview|提出需求|`button` {"data-action": "new-demand"}|
|overview|聚义厅 · 轻量工作台今天，想办成什么事？不必独自忙碌，让合适的好汉与你一起。 事说一件你想办的事从目标开始，补齐资料，再交给明确的好汉。 提出需求 先聊一聊01说清目标02选好帮手03收好成果 接着上次办进展、资料和讨|`main` {}|
|overview|提出需求|`button` {"type": "button", "data-action": "new-demand"}|
|overview|先聊一聊|`button` {"type": "button", "data-open": "chat"}|
|overview|全部事项|`button` {"type": "button", "data-open": "bounty"}|
|overview|最近事项|`button` {"data-overview-filter": "recent"}|
|overview|需要我处理2|`button` {"data-overview-filter": "attention"}|
|overview|已归档|`button` {"data-overview-filter": "archive"}|
|overview|查看进展|`button` {"data-task": "DEMO-401"}|
|overview|继续填写|`button` {"data-task": "DEMO-402"}|
|overview|处理异常|`button` {"data-task": "DEMO-403"}|
|overview|查看进展|`button` {"data-task": "DEMO-404"}|
|overview|查看成果|`button` {"data-task": "DEMO-405"}|
|overview|刷新|`button` {"type": "button", "data-action": "refresh-overview"}|
|overview|打开百宝箱|`button` {"type": "button", "data-open": "files"}|
|overview|也可以，去厅中走走厅中实景 · 静态地图演示|`button` {"data-mode": "map"}|
|overview|优化简历草稿已保留 · 接着填写|`button` {"data-task": "DEMO-402"}|
|overview|B站视频发布资料待补充 · 处理异常|`button` {"data-task": "DEMO-403"}|
|overview|点将册|`button` {"type": "button", "data-open": "agents"}|
|overview|吴用智多星协作 · 管理 · 调度|`button` {"data-agent": "wuyong"}|
|overview|林冲豹子头本领待配置|`button` {"data-agent": "linchong"}|
|overview|扈三娘一丈青本领待配置|`button` {"data-agent": "husanniang"}|
|bounty|事项类型|`select` {}|
|bounty|本领筛选|`select` {}|
|bounty|正式悬赏|`button` {"type": "button", "data-action": "new-formal"}|
|bounty|新建事项|`button` {"type": "button", "data-action": "new-demand"}|
|bounty|搜索事项名称|`input` {}|
|bounty|搜索|`button` {"type": "submit"}|
|bounty|全部5|`button` {"data-bounty-filter": "all"}|
|bounty|草稿1|`button` {"data-bounty-filter": "draft"}|
|bounty|待领令1|`button` {"data-bounty-filter": "open"}|
|bounty|已领令1|`button` {"data-bounty-filter": "assigned"}|
|bounty|办理中0|`button` {"data-bounty-filter": "running"}|
|bounty|成果0|`button` {"data-bounty-filter": "completed"}|
|bounty|异常1|`button` {"data-bounty-filter": "failed"}|
|bounty|已归档1|`button` {"data-bounty-filter": "archived"}|
|chat|厅前公议|`button` {"data-chat-key": "hall:public"}|
|chat|吴用|`button` {"data-chat-key": "hall:wuyong"}|
|chat|林冲|`button` {"data-chat-key": "hall:linchong"}|
|chat|引用资料|`button` {"type": "button", "data-action": "chat-materials"}|
|chat|话头记录|`button` {"type": "button", "data-action": "chat-history"}|
|chat|返回厅前公议|`button` {"type": "button", "data-action": "new-chat"}|
|chat|帮我梳理需求|`button` {"type": "button", "data-action": "chat-prompt", "data-text": "帮我梳理一下需求，并列出需要确认的问题。"}|
|chat|把事情拆成步骤|`button` {"type": "button", "data-action": "chat-prompt", "data-text": "请把这件事拆成几个可以推进的步骤。"}|
|chat|议事内容|`textarea` {}|
|chat|传令|`button` {"type": "submit"}|
|agents|全寨|`button` {"data-roster-filter": "全寨"}|
|agents|候命|`button` {"data-roster-filter": "候命"}|
|agents|办事|`button` {"data-roster-filter": "办事"}|
|agents|出征|`button` {"data-roster-filter": "出征"}|
|agents|失联|`button` {"data-roster-filter": "失联"}|
|agents|招贤令|`button` {"type": "button", "data-open": "recruit"}|
|agents|扈三娘一丈青 / 地慧星未录本领候命|`button` {"data-select-agent": "husanniang"}|
|agents|李逵黑旋风 / 天杀星未录本领候命|`button` {"data-select-agent": "likui"}|
|agents|林冲豹子头 / 天雄星未录本领候命|`button` {"data-select-agent": "linchong"}|
|agents|吴用智多星 / 天机星聚义厅协作 · 智能体管理 · 智能体调度候命|`button` {"data-select-agent": "wuyong"}|
|files|上传资料|`button` {"type": "button", "data-action": "upload-file"}|
|files|全部|`button` {"data-file-filter": "全部"}|
|files|资料|`button` {"data-file-filter": "资料"}|
|files|成果|`button` {"data-file-filter": "成果"}|
|files|回收站|`button` {"data-file-filter": "回收站"}|
|files|搜索文件名称|`input` {}|
|files|预览|`button` {"type": "button", "data-action": "preview-file", "data-id": "f1"}|
|files|引用到新需求|`button` {"type": "button", "data-action": "file-demand", "data-id": "f1"}|
|files|移入回收站|`button` {"type": "button", "data-action": "delete-file", "data-id": "f1"}|
|files|预览|`button` {"type": "button", "data-action": "preview-file", "data-id": "f2"}|
|files|引用到新需求|`button` {"type": "button", "data-action": "file-demand", "data-id": "f2"}|
|files|移入回收站|`button` {"type": "button", "data-action": "delete-file", "data-id": "f2"}|
|files|预览|`button` {"type": "button", "data-action": "preview-file", "data-id": "f3"}|
|files|引用到新需求|`button` {"type": "button", "data-action": "file-demand", "data-id": "f3"}|
|files|移入回收站|`button` {"type": "button", "data-action": "delete-file", "data-id": "f3"}|
|archive|聚义厅使用指南工作台、事项与交办如何衔接|`button` {"data-doc": "guide"}|
|archive|轻量工作台设计说明暖白底色、清晰正文、朱砂主按钮、克制的品牌字体|`button` {"data-doc": "style"}|
|archive|新品发布文案 · 示例交付吴用 · 已收入案卷|`button` {"data-task": "DEMO-405"}|
|messages|标记演示消息已读|`button` {"type": "button", "data-action": "read-messages"}|
|account|查看登录页样式|`button` {"type": "button", "data-open": "login"}|
|account|样式设置|`button` {"type": "button", "data-open": "settings"}|
|account|典籍阁|`button` {"type": "button", "data-open": "archive"}|
|account|退出演示账号|`button` {"type": "button", "data-action": "logout"}|
|settings|清晰无衬线传统衬线对比|`select` {"data-setting": "font"}|
|settings|标准舒适大字|`select` {"data-setting": "size"}|
|settings|暖纸色淡纸色|`select` {"data-setting": "tint"}|
|settings|（无文本，见aria/placeholder）|`input` {"type": "checkbox", "data-setting": "tips"}|
|settings|恢复样式|`button` {"type": "button", "data-action": "reset-style"}|
|settings|完成|`button` {"type": "button", "data-action": "close"}|
|help|办事概览接着上次，或提出新需求|`button` {"data-mode": "overview"}|
|help|悬赏榜筛选榜文、查看进展|`button` {"data-open": "bounty"}|
|help|点将册查看本领，找好汉议事|`button` {"data-open": "agents"}|
|help|百宝箱选资料后回到原事项|`button` {"data-open": "files"}|
|help|重看新手引导|`button` {"type": "button", "data-open": "guide"}|
|help|字体与样式设置|`button` {"type": "button", "data-open": "settings"}|
|help|查看完整演示说明|`button` {"type": "button", "data-open": "archive"}|
|quick|关闭面板|`button` {"data-action": "close"}|
|quick|个人中心|`button` {"data-view": "account"}|
|quick|厅中实景|`button` {"data-mode": "map"}|
|quick|关闭|`button` {"type": "button", "data-action": "close"}|
|demand|（无文本，见aria/placeholder）|`input` {"name": "title"}|
|demand|梳理目标、责任人与下一步行动。|`textarea` {"name": "description"}|
|demand|添加资料|`button` {"type": "button", "data-action": "pick-materials"}|
|demand|PDFPPT（PPTX）Excel（XLSX）Word（DOCX）JPEG 图片PNG 图片|`select` {"name": "format"}|
|demand|保存草稿|`button` {"type": "button", "data-action": "save-draft"}|
|demand|下一步：确认交办|`button` {"type": "button", "data-action": "next-demand"}|
|confirm|请选择好汉扈三娘 · 一丈青李逵 · 黑旋风林冲 · 豹子头吴用 · 智多星|`select` {}|
|confirm|返回修改|`button` {"type": "button", "data-action": "edit-demand"}|
|confirm|确认交办（演示）|`button` {"type": "button", "data-action": "submit-demand"}|
|task-open|补充资料|`button` {"type": "button", "data-action": "task-materials", "data-id": "DEMO-404"}|
|task-open|围绕此事议事|`button` {"type": "button", "data-action": "task-chat", "data-id": "DEMO-404"}|
|task-open|选择好汉交办|`button` {"type": "button", "data-action": "assign-task", "data-id": "DEMO-404"}|
|task-assigned|会议要点.txt|`button` {"type": "button", "data-action": "preview-file", "data-id": "f1"}|
|task-assigned|补充资料|`button` {"type": "button", "data-action": "task-materials", "data-id": "DEMO-401"}|
|task-assigned|围绕此事议事|`button` {"type": "button", "data-action": "task-chat", "data-id": "DEMO-401"}|
|task-assigned|返回工作台|`button` {"type": "button", "data-action": "overview"}|
|task-failed|补充资料|`button` {"type": "button", "data-action": "task-materials", "data-id": "DEMO-403"}|
|task-failed|围绕此事议事|`button` {"type": "button", "data-action": "task-chat", "data-id": "DEMO-403"}|
|task-failed|重新交办（演示）|`button` {"type": "button", "data-action": "assign-task", "data-id": "DEMO-403"}|
|task-completed|品牌介绍.txt|`button` {"type": "button", "data-action": "preview-file", "data-id": "f2"}|
|task-completed|补充资料|`button` {"type": "button", "data-action": "task-materials", "data-id": "DEMO-405"}|
|task-completed|围绕此事议事|`button` {"type": "button", "data-action": "task-chat", "data-id": "DEMO-405"}|
|task-completed|查看示例成果|`button` {"type": "button", "data-action": "view-result", "data-id": "DEMO-405"}|
|task-completed|已收入案卷|`button` {"type": "button", "data-action": "archive-task", "data-id": "DEMO-405", "disabled": ""}|
|materials|（无文本，见aria/placeholder）|`input` {"type": "checkbox", "data-material-id": "f1"}|
|materials|（无文本，见aria/placeholder）|`input` {"type": "checkbox", "data-material-id": "f2"}|
|materials|（无文本，见aria/placeholder）|`input` {"type": "checkbox", "data-material-id": "f3"}|
|materials|取消|`button` {"type": "button", "data-action": "back"}|
|materials|引用所选资料|`button` {"type": "button", "data-action": "use-materials"}|
|preview|返回|`button` {"type": "button", "data-action": "back"}|
|preview|下载示例文本|`button` {"type": "button", "data-action": "download-file", "data-id": "f1"}|
|reader|返回目录|`button` {"type": "button", "data-action": "back"}|
|login|（无文本，见aria/placeholder）|`input` {}|
|login|（无文本，见aria/placeholder）|`input` {"type": "password"}|
|login|进入演示|`button` {"type": "submit"}|
|login|手机登录|`button` {"type": "button", "data-action": "login-method", "data-label": "手机登录"}|
|login|忘记密码|`button` {"type": "button", "data-action": "login-method", "data-label": "找回密码"}|
|login|微信登录演示|`button` {"type": "button", "data-action": "login-method", "data-label": "微信登录"}|
|login|GitHub 登录演示|`button` {"type": "button", "data-action": "login-method", "data-label": "GitHub 登录"}|
|recruit|本地接入预览客户端接入说明|`button` {"data-action": "recruit-preview", "data-label": "本地客户端"}|
|recruit|服务端接入预览服务端配置说明|`button` {"data-action": "recruit-preview", "data-label": "服务端客户端"}|
|chat-history|厅前公议0 条演示消息|`button` {"data-chat-key": "hall:public"}|
|chat-history|吴用0 条演示消息|`button` {"data-chat-key": "hall:wuyong"}|
|chat-history|林冲0 条演示消息|`button` {"data-chat-key": "hall:linchong"}|
|guide-0|稍后|`button` {"type": "button", "data-action": "close"}|
|guide-0|下一步|`button` {"type": "button", "data-action": "guide-next"}|
|guide-3|上一步|`button` {"type": "button", "data-action": "guide-prev"}|
|guide-3|开始体验|`button` {"type": "button", "data-action": "close"}|
|agent-selected|找他议事|`button` {"type": "button", "data-action": "agent-chat", "data-id": "wuyong"}|
|agent-selected|交办一件事|`button` {"type": "button", "data-action": "agent-demand", "data-id": "wuyong"}|
|files-trash|恢复|`button` {"type": "button", "data-action": "restore-file", "data-id": "f1"}|
|map|聚义厅地图演示，拖动浏览，使用加减号缩放，数字0复位|`section` {}|
|map|悬赏榜查看榜文|`button` {"data-open": "bounty"}|
|map|厅内议事坐下聊一聊|`button` {"data-open": "chat"}|
|map|点将册认识好汉|`button` {"data-open": "agents"}|
|map|百宝箱资料与成果|`button` {"data-open": "files"}|
|map|典籍阁查阅案卷|`button` {"data-open": "archive"}|
|map|查看扈三娘|`button` {"data-agent": "husanniang"}|
|map|查看李逵|`button` {"data-agent": "likui"}|
|map|查看林冲|`button` {"data-agent": "linchong"}|
|map|查看宋江|`button` {"data-agent": "songjiang"}|
|map|查看吴用|`button` {"data-agent": "wuyong"}|
|map|聚义厅快捷入口|`button` {"data-open": "quick"}|
|map|个人中心|`button` {"data-open": "account"}|
|map|办事概览|`button` {"data-mode": "overview"}|
|map|查看消息|`button` {"data-open": "messages"}|
|map|打开百宝箱|`button` {"data-open": "files"}|
|map|声响设置|`button` {"data-action": "sound"}|
|map|怎么开始|`button` {"data-open": "help"}|
|map|回主厅|`button` {"data-action": "reset-map"}|
|overview|全部入口|`button` {"data-action": "navigation"}|
|map|横屏看全景|`button` {"data-action": "orientation"}|

## 非导航资源与运行时下载

- `index.html`加载`styles.css`、`assets/icons.css`、`app.js`。图片包括`assets/hall-scene.webp`和角色webp；均相对当前目录，非外部URL。
- `download-file`创建`blob:`临时URL，临时`a.download=演示-<文件名>.txt`，MIME `text/plain;charset=utf-8`，点击后约1000ms撤销URL。不是服务端签名下载；无PDF/DOCX真实交付。
- Demo不调用fetch/XHR/WebSocket，没有持久化storage；文件选择器multiple=true，但只登记name和size。不写用户原文件。
- 真实PersonaCatalogPanel中的安装指导地址是`https://gitee.com/chcbz/isp-install/blob/master/skills/codex-ws-agent-install/SKILL.md`，`target="_blank" rel="noopener noreferrer"`；Demo未实现。生产Agent通道`wss://api.chaoyoufan.cn/ws/agent/channel`是传输地址，不是菜单链接，不能放入href导航。
- 当前真实站点路由登记见feature-coverage.md第4节；Demo的`archive`/`chat`等key不等同`/archive`或`/chat`正式路由，不应凭名字生成链接。
