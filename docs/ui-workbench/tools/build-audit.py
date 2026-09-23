"""Build traceable feature matrix and source fingerprint; no application writes."""
from pathlib import Path
import json, hashlib, subprocess, re
from collections import Counter
root=Path(__file__).resolve().parents[3]; out=root/'docs/ui-workbench'; ev=out/'evidence'
J='web/src/components/juyiting/'
paths={'hall':'web/src/components/world/JuyiHall.vue','entry':'web/src/components/world/JuyiHallEntry.vue','overview':J+'HallOverview.vue','draft':J+'HallDraftEditor.vue','bounty':J+'BountyPanel.vue','delivery':'web/src/components/deliveries/FormalDeliveryList.vue','mark':J+'HallPrivateMark.vue','team':J+'TeamRecommendationPanel.vue','plan':J+'WorkItemPlanPanel.vue','workspace':J+'TaskWorkspacePanel.vue','transfer':J+'ArtifactTransferPanel.vue','outcome':J+'ArtifactOutcomePanel.vue','chat':J+'ChatPanel.vue','composer':J+'HallChatComposer.vue','history':J+'HallConversationHistory.vue','files':'web/src/components/workspace/PersonalWorkspace.vue','library':J+'LibraryPanel.vue','reader':J+'archive/ArchiveReader.vue','persona':J+'PersonaCatalogPanel.vue','hosting':J+'HostingRentPanel.vue','account':'web/src/components/UserProfile.vue','router':'web/src/router/index.js'}
# feature | source alias | literal locator | status | demo evidence | gap / migration requirement
raw='''默认工作台、地图可达|hall|HallPortraitHome|UI覆盖|index.html：侧栏 / 概览地图卡 / quick|只确认导航可达；地图运行时另列
最近/待处理/案卷概览|overview|overview-tabs|部分|renderOverview / data-overview-filter|仅本地样例；缺来源分区错误、原事项身份核对
概览分区重试与分页|overview|loadPartition|缺失|无|保留部分成功数据；错误不显示为空；按来源继续读取
原正式任务/私人事项/旧执行/草稿入口|overview|typeLabels|部分|data-task → openTask|仅简化 formal/private 与 draft；缺 LEGACY_EXECUTION 原入口
消息中心的待处理语义|overview|打开不代表已读|偏差|renderMessages / read-messages|Demo 全部已读仅隐藏提示；不能代替正式成果已查看/验收标记
事项状态、本领筛选|bounty|taskAbilityFilter|部分|renderBounty / data-bounty-filter|支持本地筛选；缺真实计数、读取中、错误恢复
按榜号查榜|bounty|查榜号|缺失|#task-query 仅匹配标题|需保留榜号查询，不能只用名称搜索替代
原张榜表单与本领要求|bounty|task-create-form|缺失|new-formal → 统一表单|另保留直接张榜路径、requiredAbilities；不能并入简述型正式草稿
简述型正式任务创建|draft|只创建无悬赏|偏差|formal-demand / formal-confirm / submitDemand|必须标题30、简述200；无附件/格式/选人；创建未指派、不执行；当前Demo描述20000并要求选人、生成assigned
正式旧稿不支持字段处置|draft|hasUnsupportedFormalFields|缺失|无|原字段保留、阻止提交；明确移除而非静默丢失
私人交办输入/目标选择|draft|targetAgentId|部分|demand / confirm / #assign-agent|UI有明确目标；需真实 roster、固定版本与服务端支持的 MIME
账号草稿恢复、放弃、修订冲突|draft|恢复草稿|部分|save-draft / sourceId|仅内存；无恢复列表、分页、版本冲突、不覆盖本地输入
资料选择与预览返回|draft|temporaryInputs|部分|materials / preview|有选择返回；缺 fileId+version 固定引用及旧版保留
交办授权、外部服务与费用告知|draft|authorizationAcknowledgement|缺失|confirm 仅演示说明|提交前显式授权；缺提供方、费用与数据范围告知
提交不明核对、离开保存屏障|hall|leaveState|缺失|关闭表单/内存草稿|需核对原提交、保存失败重试/留页/放弃；禁止盲目重建
私人事项执行历史与修改再执行|draft|startRevision|缺失|task 静态时间线|需固定执行/成果版本、提出修改与新修订
个人归档、撤销归档、成果已查看|mark|<template>|部分|archive-task 单向收入案卷|缺撤销归档、精确结果集 viewed 标记、版本冲突恢复
正式成果批次与固定版本下载|delivery|<template>|部分|view-result → f3 TXT|缺批次、哈希、执行与固定版本；示例TXT不代表真实PDF成果
正式验收与退回修改|delivery|changes_requested|缺失|收入案卷按钮|归档不等于验收；拒收需原因，返工关联固定版本
单好汉显式指派|bounty|assign-task|部分|assign-task / #assign-agent|有显式选择；缺真实可指派权限与请求状态
多好汉指派|bounty|selectedAssignees|缺失|无|保留多选、明确传目标集合
宋江自动点将|bounty|auto-assign-task|缺失|无|独立动作与结果/失败说明
候选推荐和匹配解释|bounty|recommended-agent|缺失|静态人物能力列表|不能把人物设定当服务端实时推荐
团队推荐预演|team|<template>|缺失|无|保留人数/席位预算/风险/复核人、覆盖缺口与本地替换；现有组件也只是预演，不声称可最终确认团队
工作项规划|plan|<template>|条件缺失|无|受 WORK_ITEM_PLAN 开关及权限约束；需规划编辑/校验/保存交互
资金悬赏/报价/撤销/结算|bounty|fundedQuotePreview|条件缺失|无|经济构建开关+能力守卫；不可用通用确认交办替代报价确认/原请求恢复
任务协作工作台|workspace|task-workspace-panel|条件缺失|无|开关默认false；摘要/成员/工作项/待处理诉求/成果/会话及连接重试
协作文件传输与成果治理|hall|ArtifactTransfer|条件缺失|无|协作开关+主体权限；固定版本上传下载、取消、成果状态治理
点将册列表/状态/能力/详情|hall|renderedPanel === 'agents'|部分|renderAgents / data-select-agent|4位示例；缺真实载入、授权与失败态
地图与点将册数据独立|hall|mapAgents|UI覆盖|mapAgentIds / rosterIds|模拟数据分离，不证明真实API联调；必须保留 /agent/map 与 /agent/roster
108好汉招募与接入|persona|persona|部分|recruit 两张说明卡|缺108名册、绑定/重整接应、解绑、系统与我的身份区分
接入参数、命令复制与安装链接|persona|copySetupResult|缺失|recruit-preview 提示|缺profileId/workdir/env/config、复制结果、外部安装指引
服务端托管|hosting|<template>|条件缺失|无|由托管/经济能力决定；需保留可用性、订单/租用状态等现有流程，不在审计中执行
公议/私议/事项议事|chat|discussionVariant|部分|chat / chat-dialog / chat-task-context|能切本地上下文；缺真实会话scope与授权
真正新建会话|chat|new-conversation|偏差|new-chat|当前只是返回既有厅前公议；不能标为新建话头覆盖
历史选取/删除/分页|history|<template>|部分|chat-history / data-chat-key|只有已有上下文切换；缺新会话列表、删除确认、分页与失败恢复
@好汉与清除目标/草稿|composer|mention-agent|缺失|纯textarea|需候选菜单、目标chips、锁定目标与清空草稿
议事固定版本资料增删|chat|materialLinks|部分|chat-materials 将文件名写入草稿|不是绑定版本；缺建立会话前禁用、添加/删除引用和打开百宝箱
流式回复/加载失败/恢复重试|chat|eventStreamRecovering|缺失|同步假回复|需Markdown/安全渲染、等待/流中/恢复/重试、发送互斥状态
语音交互|hall|voiceFeatureEnabled|条件缺失|无|VOICE默认false；按能力保留转写确认和交互锁
聊天空间与独立滚动|chat|hall-messages|UI覆盖|V3.1 chat-layout；#chat-stream|布局优化覆盖；不代表消息业务覆盖，实机键盘仍待验
文件分类/搜索/预览/下载|files|embedded|部分|files / preview / download-file|本地名目与TXT；缺正式格式、图片/分页、多段预览
上传确认与显示名|files|upload|部分|local-file-input|仅记录文件名/大小，不读内容；缺正式上传确认、失败与进度
文件版本、追加、重命名|files|version|缺失|无|保留旧引用固定版本、版本选择、追加与改名
回收站/引用次数确认/恢复|files|trash|部分|delete-file / restore-file|缺引用次数与确认；没有永久删除需求，不擅自加入
文件载入/错误/空/分页|files|loadMore|部分|file-search 空结果|缺服务端分页、错误和权限处理
典籍阅读/案卷检索双入口|library|library-tabs|缺失|archive 说明文档+样例归档|名称已改典籍阁，但未保留正式双入口
水浒传目录/章节/阅读进度|reader|enterReading|缺失|reader 两篇帮助文档|帮助文档不能冒充原典阅读；需目录/上下回/继续阅读
书签添加/打开/删除|reader|createBookmark|缺失|无|保留阅读位置与账号归属
私人笔记增改删|reader|saveNote|缺失|无|保留选段与私密笔记关联
选段提问/重试/引用起草|reader|citeParagraph|缺失|无|原文上下文、提问恢复及引用到需求草稿
案卷关键词/来源过滤/引用|library|cite-library|缺失|无|project / meeting / memory，结果来源/时间/引用传令
沉浸阅读及横竖屏安全区|reader|virtualLandscape|缺失|普通dialog reader|需目录/笔记/阅读态与胶囊避让，不只是全文滚动
地图拖动缩放/场所/好汉入口|hall|HallStage|UI覆盖|map 静态图、5场所与5人物热点|只覆盖视觉和本地相机；不是游戏场景
实时场景、移动、气泡、模拟、声音|hall|simulationEnabled|部分|静态map / sound 提示|缺melonJS、快照/事件、模拟运行；声音按钮不播音
横竖屏/只读实景预览|hall|read-only-preview|部分|orientation 提示|没有真实虚拟旋转/只读live预览；只提示横屏
新手引导/访客模板交接|entry|<template>|部分|guide 4页文字|缺热点定位、账号持久化完成/稍后/重置、访客模板交接
个人资料权威读取与错误|account|<template>|部分|account 静态昵称头像|不读取会话身份；缺loading/error/retry
退出当前设备/全部设备确认|account|退出所有设备|缺失|logout → login 演示|不执行真实退出；缺全部设备确认及失败
运行看板与经济发现入口|account|command-observability-title|部分|account 无链接|运行看板入口缺失；经济/钱包/技能市场为条件入口
登录/回调与会话恢复|router|/oauth2/callback|部分|login / login-method|仅样式与提示；无真实认证、回调、找回密码或手机验证
偏好设置|hall|toggleHallSound|部分|settings 字体/大小/色温/标签|Demo独立会话内偏好，非生产设置全集；不要把新增原型设置当现有后台能力
弹层返回、焦点与移动导航|hall|activePanel|UI覆盖|openPanel / back / closePanel / mobile-nav|右下角典籍阁直达；其他入口在全部入口；浏览器默认dialog焦点机制，不代表完整无障碍认证'''
rows=[]; source_files=set()
for i,line in enumerate(raw.splitlines(),1):
 title,key,anchor,status,demo,gap=line.split('|'); rel=paths[key]; p=root/rel
 if not p.exists(): raise Exception(rel)
 lines=p.read_text().splitlines(); matches=[n for n,s in enumerate(lines,1) if anchor in s]
 if not matches: raise Exception(f'Anchor not found: {key} {anchor}')
 n=matches[0];source_files.add(rel)
 rows.append(dict(id=f'F{i:02}',feature=title,source=rel,line=n,anchor=anchor,status=status,demo=demo,requirement=gap))
counts=Counter(r['status'] for r in rows)
ev.mkdir(exist_ok=True)
(ev/'feature-matrix.json').write_text(json.dumps({'date':'2026-09-23','counts':dict(counts),'rows':rows},ensure_ascii=False,indent=2)+'\n')
intro='''# 轻量工作台 V3.1 功能覆盖复核

日期：2026-09-23。**结论：尚未覆盖现有全部功能，不可直接替换当前聚义厅。** 本轮只审计和补充详设，没有补实现缺失业务，也未改生产代码。

## 1. 基线与判定口径

- 对照对象：当前本地 `web/src/components/world/JuyiHall.vue` 的实际挂载链及相关路由，不以旧组件目录的所有文件为功能全集。
- 原型：`deliverables/ui-workbench-demo/` V3.1，默认轻量工作台、右下角“典籍阁”、扩大议事区域。
- 本轮新证据为**本地源码与本地浏览器**；没有重新登录线上、没有核对线上部署产物。源码含未提交改动，提交号不足以代表快照，详见 `evidence/source-manifest.json` 的SHA-256。
- 既有线上观察只能作背景；代码存在不等于当前账号可用。条件能力列单列，不把默认关闭功能说成当前线上必然可见。
- **UI覆盖**：该条限定的导航/布局/本地交互覆盖，不表示API已实现。**部分**：存在原型入口或一部分流程。**缺失**：无对应UI。**偏差**：存在会误导迁移的语义差异。**条件缺失**：受开关/主体/能力限制，原型仍未表示。全站其他模块为范围外，另列。
- Demo所有业务数据仅页面内存，刷新重置；对话为假回复；本地文件仅记录名字/大小；下载是示例TXT；没有认证、真实上传、执行、验收或后端连通性。

## 2. 必须先解决的迁移阻断

1. **正式任务创建不应等同私人交办**。当前HallDraftEditor的TASK_CREATE是标题≤30、简述≤200、无选人/格式/附件、明确确认后创建未指派任务，不启动执行。Demo却使用20000字说明、选人、格式和资料，确认后变为assigned。旧稿不支持字段也必须原样保留并明确移除。
2. **“典籍阁”只是正确命名，功能并未补齐**。现有阅读器、书签、笔记、选段问答及案卷检索均不能用两篇帮助文档代替。
3. **收入案卷≠成果已查看≠正式验收**。三种意图、权限和写操作应独立；消息全部已读不能伪装成这些状态已完成。
4. **固定版本、授权、提交不明恢复不可简化掉**。不要用内存文件名替代fileId+version，不要用重新交办替代原请求核对。
5. **回厅前公议≠新建会话**。Demo的new-chat只切换现有上下文；现有会话新建/删除/分页/恢复需另外设计。

## 3. 逐项矩阵

以下是有界审计清单，不把分组条目的计数当成产品全部行为总数；不计算误导性的“整体覆盖百分比”。源定位对应本轮本地快照，未来行号可能漂移。Demo证据函数均位于 `evidence/source/app.js`，DOM位于同目录index.html。

'''
intro+='清单条目：'+str(len(rows))+'；'+ '，'.join(f'{k} {v}' for k,v in counts.items())+'。\n\n'
intro+='|编号|功能|判定|源码证据（本地）|原型证据|缺口/迁移要求|\n|---|---|---|---|---|---|\n'
for r in rows:
 intro+=f"|{r['id']}|{r['feature']}|{r['status']}|`{r['source']}:{r['line']}`|{r['demo']}|{r['requirement']}|\n"
intro+='''
## 4. 条件功能与全站边界

源码`.env.production`默认：SIMULATION=true，TASK_WORKSPACE=false，ECONOMY_PREVIEW=false，VOICE=false；WORK_ITEM_PLAN和ECONOMY_READONLY_PREVIEW未设置（代码按true检查）。构建环境覆盖、账户授权、服务器能力仍会改变可用性，**未据此推断线上状态**。

团队推荐组件已挂载，但操作受任务权威元数据约束；它当前也是推荐预演，没有最终团队确认接口，不把尚未实现的能力当现有功能缺口。

|路由|与本原型关系|
|---|---|
|`/juyiting`|本轮主要业务对照；Demo本身不实现该URL路由|
|`/`, `/demo`, `/oauth2/callback`|全站落地页、访客样例、真实认证回调不在轻量厅内原型实现范围|
|`/chat`|通用聊天独立模块，不等同厅内议事|
|`/task`, `/list`, `/history`, `/add`|全站任务模块，不等同悬赏榜|
|`/gift`, `/pay`, `/order/list`|礼品、支付、订单未覆盖|
|`/economy-preview`, `/wallet`, `/skill-market`|受构建/能力守卫限制；未覆盖|
|`/command-observability`|独立运行看板未覆盖；个人中心应保留发现入口|
|`/profile`|原型只有静态个人中心；未覆盖真实资料与安全流程|
|`/messages`, `/help`|全站消息/帮助与Demo厅内通知/使用说明并非同一模块|
|`/vote`, `/phrase`, `/dwz`, `/wx/mp`, `/hello`|其他注册模块，未纳入本次厅内UI重构；迁移不能顺手删除路由|

以上为router注册范围核对，不宣称完成每个独立模块的内部功能审计。若目标是“整个站点全部UI”，需对这些模块另立界面清单。

## 5. 补齐优先级与验收入口

- **A / 迁移前必做**：正式/私人语义拆分，固定版本资料，授权确认，异常/冲突/未知提交恢复；区分已查看/验收/归档。
- **B / 常用功能全覆盖前必做**：典籍阅读和检索、书签笔记；会话新建删除分页和@目标；文件版本/重命名/回收确认；多好汉指派/自动点将/推荐；真实账号安全。
- **C / 能力可见时必做**：语音、工作项、协作工作台、经济/托管。保留开关和禁用原因，不因本轮关闭而删除设计。
- **保留原实现或单独规划**：实时地图游戏运行时、新手引导与访客交接、全站独立路由。静态地图只可用于视觉评审。

每项补齐至少提供：入口、正常/空/读取/失败/无权限/冲突状态（按业务适用）、返回规则、移动布局、键盘焦点、明确对象与版本、对应接口/事件和测试。当前详设的测量值只覆盖已存在原型，不伪造这些尚未设计页面的“最终像素值”。

## 6. 验证证据的边界

既有本地原型报告：64项功能断言、115个响应式页面/视口案例、56项议事布局断言；详情存于evidence/demo-tests。它们是Demo自测，不是现有业务功能对等测试。
本轮另外采集页面/弹层/代表状态的计算样式与控件目标，见详设和evidence/computed-ui.json；含仅用于采样的内存fixture，不当端到端用例。真实外部认证、上传、执行、付费、解绑、退出设备、正式验收均未操作。
'''
(out/'feature-coverage.md').write_text(intro)
source_files.update(['web/src/router/index.js','web/.env.production','deliverables/ui-workbench-demo/index.html','deliverables/ui-workbench-demo/styles.css','deliverables/ui-workbench-demo/app.js'])
def git(dir,*args):return subprocess.check_output(['git','-C',str(root/dir),*args],text=True).strip()
manifest={'auditDate':'2026-09-23','scope':'Local working-tree source, not deployed build','repositories':{d or '.':{'branch':git(d,'branch','--show-current'),'head':git(d,'rev-parse','HEAD'),'status':git(d,'status','--short')} for d in ['','web','api']},'files':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in sorted(source_files)}}
(ev/'source-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
print(len(rows),counts)
