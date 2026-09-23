# 聚义厅轻量工作台 UI 详设 · V3.1 实现基线

日期：2026-09-23。属性来源：本地Demo源码及Chromium 142.0.7444.175的计算样式，不是凭截图估值。**本文描述当前原型；未覆盖业务见feature-coverage.md，不能据本文直接替换正式系统。** 本轮不改UI、不改业务，只归档和复核。

## 1. 文档结构与读法

- 本文：设计变量、字体层级、尺寸/排版、响应式、路由/动作、状态与迁移要求。
- `component-attributes.md`：桌面1440×900、移动390×844的代表组件尺寸、字体、内外边距、间距、圆角、边框、颜色逐项表。
- `control-targets.md`：180种去重后的控件文字/目标属性（同类状态可能多条），区分按钮导航、动作、资源与真实外链。
- `evidence/computed-ui.json`：38种页面/代表状态×2视口=76份采样，5,139个已布局节点，1,339组去重计算样式；另有15组断点采样。每节点保留selector、矩形、inlineStyle、属性、scroll与styleId；用styles[styleId]查完整属性。含滚动区外的已布局节点，不表示每节点都在首屏内。
- `evidence/controls.json`：1,008条含重复视口/场景的控件记录；不是1,008个独立产品功能。
- `evidence/css-rules.json`：浏览器CSSOM的完整规则、media、伪类与font-face，按样式表和源顺序保存。`evidence/source/`为HTML/CSS/JS快照（无图片/图标资源，非独立可运行包）；完整Demo仍在deliverables。
- `evidence/source-manifest.json`：本地提交、分支、dirty状态与审计文件SHA-256。以快照为准，不把root提交号视为dirty子模块的完整状态。

所有值为**CSS px**；小数来自字体和flex布局。实测W×H是给定视口/文案的结果，不能把它全部写死为width/height。设计规则以CSS约束为准。系统字体、设备像素比、浏览器和文案变化会影响换行。

## 2. 视觉变量

|变量|默认值|用途|
|---|---|---|
|`--paper`|`#FFFEFA`|卡片、输入框、页头/弹层纸面|
|`--paper-strong`|`#F5F4F0`|工作台底色、页脚|
|`--paper-muted`|`#F3F3ED`|浅层辅助背景|
|`--ink`|`#242E2B`|主正文|
|`--muted`|`#68716B`|说明、次级文字|
|`--line`|`#E3E5DC`|卡片/分割线，通常1px|
|`--brand` / hover|`#923F30` / `#793326`|朱砂主操作|
|`--green` / bg|`#21604D` / `#EAF2ED`|正向/已选语义|
|`--amber` / bg|`#87551C` / `#F9EFDE`|待处理|
|`--red` / bg|`#A13F35` / `#FAEAE6`|异常/危险|
|输入边框 / placeholder|`#CCD2C5` / `#7D867B`|字段边界/提示|
|普通hover背景 / 边框|`#F0F1EA` / `#C4CABE`|按钮hover|
|通知底色 / 边框 / 文字|`#F2F2EA` / `#B2BB9E` / `#5D6659`|notice|
|他人气泡 / 自己气泡|`#F2F2EB` / `#EAF0E6`|聊天消息|
|本人气泡边框|`#DBE4D3`|与他人区分|
|地图遗留色|`--header=#302116`, `--gold=#E2C38A`|地图HUD等暖色体系，不强制改为纸面颜色|

注意：变量`--radius=8px`不是所有组件统一圆角。实际按钮7、输入6、卡片11/12、头像50%、移动全屏弹层0；附表列最终值。

## 3. 字体、字号与行距

UI字体栈：

```css
-apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
"Hiragino Sans GB", "Microsoft YaHei", "Noto Sans CJK SC", sans-serif
```

品牌字体栈：

```css
"Noto Serif CJK SC", "Songti SC", STSong, serif
```

默认正文无衬线，只有品牌、首页主标题、阅读标题等使用衬线。无需在线字体请求；图标使用本地Varlet icon font。字体栈不是保证安装的字体：本次Linux的`.welcome h1`汉字实际使用**Droid Sans Fallback**（CDP证据在platformFonts），不应宣称已实测宋体效果；Windows/macOS/iOS需分别验字形和换行。

|层级/位置|桌面字号/字重/行高|390px移动端|说明|
|---|---|---|---|
|基础正文|15 / 400 / 24.75|同左|`--base-size=15`, `--body-height=1.65`|
|首页欢迎h1|28 / 500 / 42|25 / 500 / 37.5|品牌字体；字距桌面0.8，手机0|
|普通页面h1|27 / 500 / 37.8|25 / 500 / 35|非聊天页|
|弹层h1|22 / 500 / 30.8|21 / 500 / 29.4|无衬线|
|常规h2 / h3|20 / 600 / 30；16 / 600 / 24|局部覆盖见附表|不以浏览器默认粗体代替|
|首页事项标题|15 / 500 / 23.25|同左|榜单标题桌面16，手机15|
|事项元信息 / 状态|12 / 400 / 19.8；11px状态|11px|仅辅助信息，不缩小正文来腾空间|
|议事工具条标题|16 / 600 / 24|同左|超长单行ellipsis|
|消息气泡正文|15 / 400 / 25.5|14 / 400 / 23.8|`white-space:pre-wrap; overflow-wrap:anywhere`|
|聊天输入|15 / 400 / 24|16 / 400 / 25.6|手机输入单独16px；不是把所有文字统一16|
|聊天计数|11 / 400 / 16.5|同左|辅助说明|
|阅读段落|16 / 400 / 30.4|15 / 400 / 28.5|移动继承15，行高1.9；不要照抄页脚“正文16px”文案|
|字段输入|16 / 400 / 26.4|同左|普通textarea另行高1.7|
|普通按钮|14 / 500 / 20.3|按位置覆盖|导航/页签/列表操作11–14不等|
|底部导航文字 / 图标|隐藏|11 / 500 / 15.95；图标21|标签“典籍阁”不截断|

**已发现的文案/样式差异**：reader页脚声称正文16px，但≤600px正文为15px；详设记实际计算值，后续修正说明或统一字号，不能把文案当样式证据。

舒适大字：body base变17；intro/task-title/chat-bubble/reader p设17；多数非图标按钮16；task-meta/agent-info small/.small设14。局部更高特异性仍可覆盖，如`.board-list .task-title`，因此不是全站等比放大。传统模式仅替换`--font-ui`为品牌衬线栈。淡纸色把paper变`#FFF`、paper-strong变`#F1F3F4`。偏好仅内存；刷新恢复，不改真实账号设置。

## 4. 框架与间距

### 4.1 工作台

- 主框`#business-shell`：侧栏 + `minmax(0,1fr)`；单行`minmax(0,1fr)`，工作区必须`min-height:0`。
- 常规侧栏216宽；≤1200变192；≤760隐藏。默认padding `28px 15px 16px`。
- 桌面页头高76（实测），padding `12px 36px`；≤1000最小68；≤760最小64。窄横屏最小58。
- 普通主区`#work-main`独立滚动，默认padding `30px 36px 24px`；桌面最大正文宽1320。不要让body和main同时争夺滚动。
- 首页两栏：`minmax(0,1fr) 300px`，gap24；≤1200右栏264、gap18；≤1000变单列主体，附属卡横向两列；≤600附属卡也单列。
- 概览标题、需求卡、事项卡间距按附表；需求卡padding26/28、gap22、radius12；手机21/18、gap12。最近事项卡padding22/24/0、radius11；手机18/16/0。
- 普通业务页`.page-surface`边框1、radius12；page-body padding26，≤1000为22，≤600为20/16。
- 地图预览默认高176；≤1000为165；≤600为185。它是入口卡片，不替代实时地图。

### 4.2 手机底栏与安全区

- ≤760显示四项：**办事概览、我的事项、厅内议事、典籍阁**；最后一个`data-view=archive`直达，不打开“更多”。
- 高`62px + env(safe-area-inset-bottom)`，padding `5px 12px max(5px, safe-area-bottom)`；position:absolute、底0、z-index10；按钮各占一份，min-height50、图文竖排gap4。
- 工作区预留同等padding-bottom，避免遮住发送区；右上角“全部入口”保留点将册、百宝箱、消息、个人、设置、帮助、地图。
- 普通页头`10px 16px`（≤600）；mobile header隐藏“提出需求”大按钮，需求可从概览卡进入。
- 本次headless安全区为0；env写法已归档，但刘海/胶囊、实体键盘和系统缩放未实机验证。顶部普通工作栏目前无统一safe-area-top补偿，真机需检查，不能声称全机型通过。

### 4.3 弹层

- 原生dialog：默认宽`min(1000px,100vw - 64px)`，max-height `100dvh - 64px`，radius12，边框1；shadow `0 26px 90px #242E2B29`。
- demand / confirm / account / settings / login / guide收窄为`min(720px,100vw - 64px)`。
- chat高`min(780px,100dvh - 64px)`；agents最小高`min(620px,100dvh - 64px)`。
- 页头padding21/26；body26，可滚动；footer16/24。页头、页脚不跟随body滚动。遮罩`#20292066`、blur2。
- ≤600普通弹层全屏100vw×100dvh、margin0、radius0、border0；head16/16并避让顶部safe-area；body20/16；footer14/16并避让底部safe-area。
- max-height560且横屏：宽`min(1000px,100vw - 32px)`、max-height `100dvh - 24px`、radius10、height auto；聊天低高度另设固定可用高，见下一节。
- 打开弹层保存returnFocus；返回恢复上级栈；关闭返回触发控件，控件消失则回work-main。Escape走cancel→closePanel。未实现浏览器历史URL栈。

## 5. 厅内议事空间专项

**不再使用“页标题+小聊天卡”的高度相减布局。** 页面h1保留给辅助技术，但视觉裁剪成1×1；工作页脚隐藏。

|对象|桌面规则|≤760规则|
|---|---|---|
|主区|padding16/24、overflow hidden|padding0|
|page-view|flex column、100%宽高、min-height0|同左|
|page-surface|flex1、height auto、min-height0|无边框/圆角|
|page-body|flex1、min-height0、padding14/20/0、overflow hidden|12/16/0|
|对象横向选择条|gap8、margin-bottom8、padding-bottom4；按钮min-height36、padding7/12|同左，水平滚动|
|工具条|nowrap、gap8、padding-bottom10；按钮组gap4|按钮min-height40、字号12|
|chat-stream|flex1、min-height0、overflow auto、padding16/0、gap18、overscroll contain|同左|
|footer|flex none、padding12/20|10/16|
|composer|grid列`minmax(0,1fr) auto`、两行、gap6/10|同左|
|textarea|高52、min48、max112、padding12；第1行第1列|字号16、禁止resize|
|发送按钮|第1行第2列，底对齐、min-height48、padding10/16|padding10/13|
|计数|第2行跨两列、11px/1.5|同左|

消息不压缩（flex:none）。发送滚到最后一条；消息增加只增加stream.scrollHeight，不增大整页。桌面气泡padding12/14，手机10/12；他人radius `0 8 8 8`，本人`8 0 8 8`。头像桌面32、手机28（其余头像见附表）。上下文chip超长ellipsis但保留title。

主页面隐藏重复recipient副文案；弹层保留，≤560高时隐藏。弹层聊天head12/20、body16/20/0、footer12/20；≤600左右16且加入safe-area。高度≤560：主体上下padding0、body顶部6、footer上下6、对象按钮最小32、工具条padding-bottom4；弹层chat高`100dvh - 24px`。

|视口|旧消息区高|V3.1消息区高|
|---|---:|---:|
|390×844|188.95|511.50|
|320×740|100|407.50|
|1440×900|281.66|575.50|
|844×390|100|146.50|

数值来自既有chat-layout对比；本轮390/1440重测吻合。真实软键盘弹出、动态地址栏、超长会话、缩放200%和真实长Markdown仍需独立验证；仅缩小视口不等于系统键盘测试。

## 6. 控件与交互状态

- 普通按钮最小42高、padding8/14、gap7、radius7、border1；图标按钮和紧凑列表各有覆盖，不以42/44px概括所有触控区。
- 主按钮背景brand，字色paper；hover背景brand-hover，但**hover边框实际为#C4CABE**（通用规则覆盖）。若要同色深朱砂边框是后续设计修正，不是现状。
- focus-visible：3px solid `rgba(146,63,48,.5)`、offset3。某些遗留a规则仍为金色；Demo无常驻href导航。
- disabled：opacity .48、cursor not-allowed；按钮事件委托先检查disabled。默认主按钮禁用样式经合成disabled采样，不表示每个业务流程已经实现禁用态。
- active导航/页签/选中好汉通过class配合aria-current/aria-pressed；颜色不是唯一状态标识。
- 表单input/select：width100%、min-height44、padding10/12、radius6、border1；普通textarea min-height128（≤600为116）、line-height1.7、垂直resize。
- 字段错误role=alert，不清空超长文本。Demo正式名目≤30/私人≤200，描述均≤20000；**正式简述这里存在业务偏差，必须按覆盖报告修正**。议事≤1200为原型限制，不等同服务端合同。
- 空列表显示标题+说明；本原型只有少量预置失败提示，没有覆盖服务端loading/403/版本冲突/流式中/未知提交等状态。
- Toast role=status、aria-live=polite，约4000ms隐藏；若弹层打开，toast移入dialog以保证可见，关闭移回body。手机普通toast底82，dialog内底18。
- 地图拖动使用pointer捕获；滚轮缩放1–2.3，键盘+/-缩放、0复位、方向键平移。没有真实场景更新、声音或强制横屏。
- prefers-reduced-motion只关闭现有对应过渡（详见CSSOM），不能据此声称全面动效无障碍达标。

无障碍后续验收：核查11px辅助文字、实际触控尺寸、各状态对比度、焦点遮挡、页面缩放与屏幕阅读器；本轮未作WCAG合规认证。

## 7. 导航、链接与动作合同

### 7.1 主页面（非URL路由）

|界面名称|key|入口|
|---|---|---|
|办事概览|overview|品牌、侧栏、底栏、全部入口|
|我的事项|bounty|侧栏/底栏/概览“全部事项”；地图文案“悬赏榜”|
|厅内议事|chat|侧栏/底栏/先聊一聊/地图|
|点将册|agents|侧栏/全部入口/首页好汉/地图|
|百宝箱|files|侧栏/全部入口/首页资料条/地图|
|典籍阁|archive|侧栏/右下角底栏/全部入口/地图|
|消息通知|messages|页头铃铛/全部入口/地图HUD|
|个人中心|account|侧栏账号/全部入口/地图头像|
|偏好设置|settings|侧栏/全部入口/个人中心/帮助|
|使用帮助|help|侧栏/全部入口/地图HUD|

`data-view`总是navigate；普通工作台`data-open`主页面也是navigate；从地图或已有弹层push打开时，则进入dialog并可返回。`data-mode=map`隐藏工作台、激活地图；`data-mode=overview`回概览。**不改pathname/hash，不支持页面深链接、URL分享或浏览器Back作为内部导航。**后续接Vue Router必须明确与真实`/juyiting`及其他全站路由的映射，不能想当然创建`/archive`。

### 7.2 动作分组（每个按钮的实际属性见control-targets.md）

|动作族|输入与目标|本地副作用/返回|
|---|---|---|
|new-demand / new-formal / agent-demand / file-demand|private/formal、显式好汉或资料id→demand|保存适用内存草稿，后者带资料；不直接提交|
|save-draft / next-demand / edit-demand|校验→本地draft或confirm / 返回|保留文本；不持久化账号|
|submit-demand / assign-task|assign-agent→task|模拟assigned；**正式任务路径不合现有语义**|
|data-task|draft→demand；其他→task|按明确id打开，无真实权限检查|
|pick-materials / task-materials / chat-materials|materials|保留调用方；use-materials回填草稿/事项/议事，后者只是文件名文本|
|preview-file / view-result|preview(id)，result固定f3|只读示例文本；关闭回原处|
|download-file|临时Blob|TXT下载，见控件登记；无服务端请求|
|upload-file / delete-file / restore-file|文件选择/文件id|元信息登记、内存移回收站/恢复；不改磁盘|
|task-chat / agent-chat / data-chat-key|明确事项/好汉上下文|上下文各自保留草稿和消息|
|new-chat / chat-history|既有厅前公议 / 历史弹层|前者不创建新会话；后者不支持删除|
|archive-task|明确task.id|仅本地archived=true；不验收、不标真实结果已查看|
|data-doc|reader(id)|只读两篇演示说明，非水浒传目录|
|read-messages|messages|隐藏本地未读点，不代表权威事项状态变化|
|data-setting / reset-style|font/size/tint/tips|修改CSS变量/类/标签显示；不存账号|
|guide-prev / guide-next|step0–3|说明页翻页，无持久化引导进度|
|login-form / login-method / logout|演示登录/提示|不请求认证；logout不退出任何设备|
|recruit-preview|本地/服务端说明|不绑定、不安装、不产生凭据|
|refresh-overview / refresh-board|本地重新渲染|不请求服务器；refresh-board为源码保留动作，当前无独立可见按钮|
|sound / orientation / reset-map|提示 / 相机复位|声响不播音；方向提示不锁屏|
|close / back / overview / navigation|关闭/上级/概览/quick|恢复焦点；主页面“完成”回概览|

文件、下拉过滤、资料checkbox及表单提交不全经button click：事件委托还有input/change/submit；完整data attrs及name/type已随控件清单保存。用户操作的动态id不会变成可共享href。

## 8. 响应式规则优先级

继承基础CSS → V3工作台覆盖 → V3.1聊天覆盖。不要只抄文件首段。边界采用包含等号的max-width：

|条件|主要变化|
|---|---|
|min-width1600|主内容/header/footer左右54|
|max-width1500（旧基础）|仅仍匹配的旧地图/布局规则，完整声明见CSSOM；不作为新工作台主断点|
|max-width1200|侧栏192、主区26、右栏264、隐藏start-steps|
|max-width1000|单主列、附属区两列、文件/好汉单列、面包屑缩减、body22|
|max-width760|隐藏侧栏、底栏62+safe-area、全部入口显示、议事全宽|
|max-width600|普通主区22/16、附属区单列、弹层全屏、表单/卡片进一步紧凑|
|max-width360|隐藏demo-badge/start-mark、页签更紧凑|
|max-height560 + landscape|紧凑弹层、页头、隐藏work-footnote|
|max-height560（V3.1）|聊天压缩纵向留白，不要求横屏|

已补采320、360、600/601、760/761、1000/1001、1200/1201、1500/1501、1599/1600、844×390的聊天结构。断点采样≠每页每种数据状态都测过；既有115个响应式案例另行归档。

## 9. 待补页面的设计约束（不是已实现属性）

迁移时延续上述token与组件，不以“大改”删除现有能力。至少补：

1. 典籍阁：阅读/检索两个一级分区；阅读目录/章节/进度、笔记/书签、选段问答与引用；查询结果来源与引用操作。
2. 正式创建与私人交办分别成流程；正式创建后留在未指派态，后续任务指派/验收走原功能。
3. 草稿/材料：固定版本、格式能力、授权确认、保存状态与冲突/未知提交处置；文件详情含版本列表、重命名、追加版本和引用次数确认。
4. 会话：新建、删除确认、历史分页、@目标、材料引用列表、等待/流中/恢复/失败；保留V3.1消息区优先布局。
5. 交付：已查看、个人归档、正式验收/返工三套独立动作，明确任务/执行/成果版本。
6. 条件功能：保留原开关与能力可见性，显示不可用原因；未设计页面不要复制原型虚构的“已完成”状态。

这些页面的最终布局和像素规格待补原型后再实测；目前只规定必须保留的交互，不伪造不存在的UI属性。

## 10. 复现与验证

在仓库根目录运行（先自行启动完整Demo的静态服务；不访问线上）：

```bash
python3 -m http.server 8878 --bind 127.0.0.1 --directory deliverables/ui-workbench-demo
# 另一个终端；需本机Chromium与playwright-core，路径可用环境变量覆盖
node docs/ui-workbench/tools/capture-ui.cjs
python3 docs/ui-workbench/tools/build-audit.py
python3 docs/ui-workbench/tools/build-ui-reference.py
```

`DEMO_URL`、`PLAYWRIGHT_MODULE`、`CHROMIUM_PATH`可覆盖默认配置。采样器仅在浏览器响应中注入__audit以进入代表状态，原Demo文件不变；合成错误/禁用/回收站状态只为采样，不算真实业务测试。脚本没有读取测试账号密码，不在文档保存凭据。

本轮76份属性采样无JS异常、无失败请求、无外部请求。仅文档/采样工具变更，未运行生产前端build，不改既有脏spec或生产源码。真实业务全覆盖仍需按feature-coverage.md补齐并联调验收。
