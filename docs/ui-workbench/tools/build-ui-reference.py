from pathlib import Path
import json, re, shutil
out=Path(__file__).resolve().parents[1]; root=out.parents[1]; x=json.loads((out/'evidence/computed-ui.json').read_text())
def pick(scene,w,spec):
 c=next(c for c in x['captures'] if c['scene']==scene and c['width']==w)
 bits=spec.split(' '); nodes=c['nodes']; prefixes=[None]
 for bit in bits:
  matches=[n for n in nodes if any(prefix is None or n['selector'].startswith(prefix+' > ') for prefix in prefixes) and (n['selector']==bit if bit.startswith('#') else bit[1:] in n['class'].split() if bit.startswith('.') else n['tag']==bit)]
  if not matches:return None
  prefixes=[n['selector'] for n in matches]
 return matches[0]
items='''工作台侧栏|overview|.sidebar
顶部栏|overview|.work-header
头部操作组|overview|.work-header-actions
主体滚动区|overview|#work-main
侧栏菜单|overview|.side-nav button
侧栏品牌|overview|.work-brand
品牌印章|overview|.brand-seal
移动导航|overview|.mobile-nav
移动导航按钮|overview|.mobile-nav button
移动导航图标|overview|.mobile-nav i
首页标题|overview|.welcome h1
首页副标题|overview|.welcome p
首页眉题|overview|.eyebrow
提出需求卡|overview|.start-card
提出需求标题|overview|.start-copy h2
提出需求主按钮|overview|.start-copy button
概览两栏|overview|.overview-columns
最近事项卡|overview|.recent-card
卡片标题|overview|.section-head h2
事项行|overview|.task-row
事项名|overview|.task-title
事项元信息|overview|.task-meta
状态标签|overview|.status
页签|overview|.tabs button
地图预览卡|overview|.map-entry
侧边好汉头像|overview|.compact-agent .portrait
资料条|overview|.resource-strip
普通页面眉题|bounty|.page-heading .eyebrow
普通页面标题|bounty|#page-title
普通页面说明|bounty|#page-description
普通页面容器|bounty|.page-surface
普通页面内边距|bounty|#page-body
筛选行|bounty|.filter-row
本领下拉|bounty|#ability-filter
事项搜索输入|bounty|#task-query
榜文标题|bounty|.task-title
榜文操作按钮|bounty|.task-actions button
弹层总框|demand|#panel
弹层页头|demand|.panel-header
弹层眉题|demand|.panel-kicker
弹层标题|demand|#panel-title
弹层正文区|demand|#panel-body
弹层页脚|demand|#panel-footer
需求步骤条|demand|.steps
表单字段组|demand|.field
字段标签|demand|.field-label
单行输入|demand|.field input
需求多行输入|demand|.field textarea
字段辅助|demand|.field-help
附件选择区|demand|.upload-block
附件chip|demand|.attachment-chip
字段错误|demand-error|#demand-error
确认说明|confirm|.notice
详情定义列表|confirm|.definition
明确好汉下拉|confirm|#assign-agent
空列表|bounty-empty|.empty
好汉双栏|agent-selected|.agent-layout
好汉选中行|agent-selected|.selected
好汉列表头像|agent-selected|.agent-row .portrait
好汉详情头像|agent-selected|.agent-detail .portrait
好汉详情|agent-selected|.agent-detail
文件网格|files|.file-grid
文件卡片|files|.file-card
文件操作按钮|files|.file-card button
资料选择项|materials|.check-row
文档预览|preview|.document-preview
典籍目录行|archive|.doc-row
阅读弹层|reader|#panel
阅读正文容器|reader|.reader
阅读段落|reader|.reader p
偏好行|settings|.setting-row
快捷宫格|quick|.quick-grid
快捷卡|quick|.quick-card
议事主区|chat|#work-main
议事容器|chat|.page-surface
议事页体|chat|#page-body
议事对象行|chat|.chat-sessions
议事对象按钮|chat|.chat-sessions button
议事工具条|chat|.chat-toolbar
议事工具条标题|chat|.chat-toolbar h3
议事滚动区|chat|#chat-stream
议事页脚|chat|#page-footer
议事输入排版|chat|.chat-composer
议事输入框|chat|#chat-input
议事发送|chat|.chat-composer button
议事字数说明|chat|#chat-counter
消息头像|chat-populated|.chat-message .portrait
消息气泡|chat-populated|.chat-bubble
本人气泡|chat-populated|.me .chat-bubble
弹层议事|chat-dialog|#panel
弹层议事页体|chat-dialog|#panel-body
弹层议事页脚|chat-dialog|#panel-footer
登录表单|login|.login-form
新手标题|guide-0|.brand-text
地图工具条|map|.map-hud
地图场所按钮|map|.landmark
地图好汉热区|map|.agent-hit'''
text='''# 组件属性实测附表（V3.1）

由tools/build-ui-reference.py从computed-ui.json生成。默认风格；D=1440×900，M=390×844；所有长度为CSS px。W×H是本次文案/字体下的实际包围盒，不应全部硬编码。P/M=padding/margin，顺序为上右下左（CSS简写）；gap列可能为normal，表示未显式指定，不能理解为组件无间隔。

本表覆盖常用代表组件；同类不同位置、选中/异常状态、全部边框/阴影/滚动/定位属性查JSON。定位名称对应原型，不代表正式业务页面已补齐。

|组件 / 场景 / 选择器|视口|W×H|字号 / 字重 / 行高|P；M；gap|圆角 / 边框|前景 / 背景|
|---|---|---|---|---|---|---|
'''
missing=[]
for line in items.splitlines():
 label,scene,spec=line.split('|')
 for w in [1440,390]:
  n=pick(scene,w,spec)
  if not n:
   if not (w==390 and spec in ['.sidebar','.side-nav button','.work-brand','.brand-seal']) and not (w==1440 and spec.startswith('.mobile-nav')):missing.append((scene,w,spec))
   continue
  s=x['styles'][n['styleId']];r=n['rect'];size=f"{r['width']:.2f}×{r['height']:.2f}"
  text+=f"|{label} / {scene} / `{spec}`|{'D' if w==1440 else 'M'}|{size}|{s['font-size']} / {s['font-weight']} / {s['line-height']}|{s['padding']}；{s['margin']}；{s['gap']}|{s['border-radius']} / {s['border']}|{s['color']} / {s['background-color']}|\n"
(out/'component-attributes.md').write_text(text)
text='''# 控件与跳转属性登记（V3.1）

下表由实际DOM采集去重。场景名见详设。`data-*`不是URL：通常调用navigate/openPanel/applyAction，地址栏不变；没有href的按钮不可伪称支持复制链接/新标签打开。所有示例id仅用于本地fixture。完整DOM路径、aria属性、type/name/placeholder、样式索引及视口见evidence/controls.json。

|场景|显示文字或无障碍名称|标签 / 目标属性|
|---|---|---|
'''
seen=set()
for c in json.loads((out/'evidence/controls.json').read_text()):
 attrs={k:v for k,v in c['attrs'].items() if k.startswith('data-') or k in ['href','target','rel','download','type','name','disabled']}
 key=(c['label'],json.dumps(attrs,sort_keys=True),c['tag'])
 if key in seen:continue
 seen.add(key)
 label=c['label'].replace('|','\\|')
 text+=f"|{c['scene']}|{label or '（无文本，见aria/placeholder）'}|`{c['tag']}` {json.dumps(attrs,ensure_ascii=False).replace('|',' / ')}|\n"
text+='''
## 非导航资源与运行时下载

- `index.html`加载`styles.css`、`assets/icons.css`、`app.js`。图片包括`assets/hall-scene.webp`和角色webp；均相对当前目录，非外部URL。
- `download-file`创建`blob:`临时URL，临时`a.download=演示-<文件名>.txt`，MIME `text/plain;charset=utf-8`，点击后约1000ms撤销URL。不是服务端签名下载；无PDF/DOCX真实交付。
- Demo不调用fetch/XHR/WebSocket，没有持久化storage；文件选择器multiple=true，但只登记name和size。不写用户原文件。
- 真实PersonaCatalogPanel中的安装指导地址是`https://gitee.com/chcbz/isp-install/blob/master/skills/codex-ws-agent-install/SKILL.md`，`target="_blank" rel="noopener noreferrer"`；Demo未实现。生产Agent通道`wss://api.chaoyoufan.cn/ws/agent/channel`是传输地址，不是菜单链接，不能放入href导航。
- 当前真实站点路由登记见feature-coverage.md第4节；Demo的`archive`/`chat`等key不等同`/archive`或`/chat`正式路由，不应凭名字生成链接。
'''
(out/'control-targets.md').write_text(text)
testdir=out/'evidence/demo-tests';testdir.mkdir(exist_ok=True)
for name in ['test-results.json','responsive-results.json','chat-layout-results.json','chat-layout-before.json']:
 shutil.copyfile(root/'deliverables/ui-workbench-demo'/name,testdir/name)
print('missing samples',missing,'unique controls',len(seen))
