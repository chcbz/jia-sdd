# 验收方案与用例

> 当前用户交互以 [普通请求与统一动作合同](ordinary-request-actions-v3.md) 为准：四步完成，不设图片专用“受控请求”或确认链。历史冻结合同不作为新界面流程；完整发布验收仍未完成。

> **2026-10-03 最新实施指令**：用户明确“无需做太多兼容补丁，一切都按新方案实施”。新入口、新请求统一走通用资料与按需议事；不新增旧生图入口、双轨产品流程或回退适配工程。只保留身份隔离、幂等、未完成请求及既有内容保护，不以历史兼容覆盖率阻塞新方案。

> **2026-10-03 用户纠偏（当前优先）**：[通用资料详设增量v3](unified-materials-correction-20261003.md)取代独立参考图入口及图片限定业务流程。唯一“添加资料（可选）”须支持图片/文档/音频等；Agent判断用途，通用会话、输出、保存与交付保持完整范围。不是文案改名；绘图专用wire仅作为执行适配，不扩展旧产品入口，原34项需补UM01–UM10。当前已完成创建/资料基础源码自检，通用点将会话链路与整体验收仍待完成。

> **2026-09-28 验收增量**：[详设v2第11节](fusion-detailed-design-v2.md) 新增FD01–FD12，与本文件AC01–AC22合计34项产品用例，均未因本轮代码合并自动通过。实际源码定向检查见 [整合回执](integration-baseline-20260928.md)。

原始设计日期：2026-09-27；当时全部用例状态：**NOT_RUN**。最新实测增量见文末，不把原始设计表当作当前已验收状态。下列是未来验收设计，不是已实现/已通过的证明；前期 fast-deliberation 79/141 测试不计入本需求。

## 1. 环境与数据

使用用户指定测试账号及其已授权测试 Agent；凭据从安全运行输入取得，不写入文档、Git、测试日志。准备该用户可读的参考图片、测试音频、普通文件，以及第二用户不可互访数据。准备 server 与 local 两种已知实际版本的目标 Agent；缺少某模式或能力则记 blocked/not-run，不冒充通过。

真实模型/收费工具仅在该测试用途已有明确授权范围运行；负向和失败测试尽量用隔离夹具。真实浏览器+平台+Agent 的正向端到端不可由开发助手直接生成文件、静态 demo、mock 事件或文件路径回答替代。

## 2. 验收矩阵

| ID | 场景/操作 | 必须观察到的结果 |
| --- | --- | --- |
| AC01 | 不选资料，输入“画一只鸟”并点将 | 自动创建/复用悬赏议事并发送需求；不强制打开空间或再点生成 |
| AC02 | 从统一资料入口混选图片/文档/音频/普通文件v2，源文件随后产生v3 | 四类真实请求/服务端快照均保留；首条资料卡及按需runtime实际输入仍为v2，含授权领取/摘要、预览/移除证据；不能只改文案或只测图片 |
| AC03 | 双击/重试点将、刷新、多端同一意图 | 一次 assignment 意图对应一个会话、一个首条请求；无重复模型执行 |
| AC04 | 点将成功后中断投递，恢复网络 | 明确点将成功/投递待恢复，恢复同意图不重复点将；响应未知先查状态 |
| AC05 | 信息充分且能力/授权满足 | Agent 直接输出/执行，既有授权内不要求第二次开始；状态与实际执行一致 |
| AC06 | 需求确有歧义，用户回复澄清 | 同会话提问和继续，澄清不持有生成 lease；补充后可继续执行 |
| AC07 | 图像生成、上传完成 | 就绪后无需刷新显示；预览实际可解码、宽高有效；下载可打开且 SHA-256 与服务端一致；不是本机路径/重定向循环 |
| AC08 | 会话含音频 | 可点击播放/暂停、下载、保存；有真实字节/MIME，宣称支持拖动时验证 Range；不自动播放；不要求该 Agent 会音频生成 |
| AC09 | 一条回复包含文本、多图、音频/文件；文字先结束 | 混排正常，晚到媒体仍原位更新；一个附件失败不隐藏其他成果；未知格式明确预览限制但可合法下载 |
| AC10 | 未保存第一稿，直接引用“改成蓝色” | runtime 实际取得第一稿，生成新 execution；同一会话可看旧新稿，源参考文件未被覆盖 |
| AC11 | 生成中/已就绪时刷新、断线重连、乱序/重复事件 | 无重复生成/part；低 revision 不回退；历史含已就绪媒体；游标失效按快照重同步无漏事件 |
| AC12 | 保存文字片段、图片、音频和普通文件，重复点击 | 仅选中项进入个人空间；普通重复保存不多副本，文本片段已冻结；保存失败只重试归档 |
| AC13 | 明确另存副本/更新已有文件，两个端使用相同旧版本更新 | 另存可产生新文件；新版本需 CAS，第二个旧 expectedVersion 冲突，不覆盖他人/新版本 |
| AC14 | 不先保存，验收面板仅选择最新图片和文字 | 正式成果只含选中精确集合；旧稿不进入；验收后服务端任务真正完成才显示完成 |
| AC15 | 执行失败、正式提交/验收/完成各阶段分别故障；可选归档失败 | 执行FAILED停止会话等待，不自动重执行；展示真实阶段，恢复原 operation 不重复收费/验收；已验收而任务未完成不误标完成；归档失败独立重试 |
| AC16 | 第二账号猜 asset/file/conversation/execution/operation ID；媒体 Range/HEAD；伪造身份 | 所有访问和写入受 ACL 隔离，不能通过哈希/直链/事件越权；senderType/name 以服务端身份为准 |
| AC17 | server 和 local 分别跑图片及非绘图/混合资料主流程并检查运行目录 | 独立 roots/task/run；资料仅授权领取、输出仅声明上传；无需共享挂载，两种模式预览/下载均可用 |
| AC18 | 新旧客户端混用、fastChat 关闭、缺图片/INSPECT 能力 | 逐目标匹配协议/能力，明确可用/不可用；现代受理后不静默降级重跑，旧文本入口仍正常 |
| AC19 | 恶意素材要求读取其他目录/工具，伪造执行意图/producer/lease，超授权收费 | 服务端与 runtime 拒绝越界；只读 CHAT 无任意工具；生产者 token 不泄露浏览器 |
| AC20 | 冷线程/缓存丢失/配置变化，内置宋江及远端分别继续对话 | 从授权业务历史/摘要/精确资产重建上下文；实际包含上一稿/需求，不仅 ID 或当前一句话 |
| AC21 | 生成中取消、切换身份、重新点将；旧 Agent 晚到提交 | 新身份无旧内容泄漏；取消反映实际结果；旧 assignment 无权完成新分配；交接资料重新授权 |
| AC22 | Agent 离线后读成果；会话删除；旧 PRIVATE/TASK/普通聊天回归 | 已就绪资产依保留/权限可读；已个人保存和正式交付不随会话删除丢失；旧执行/普通聊天无语义回退 |

## 3. 数据/事务专项（实施 Owner 自检）

- MySQL 增量迁移：空库/旧库/重复执行/失败恢复、唯一约束、事务失败后的 outbox/asset/part 一致性；记录 DDL SHA/fixture digest。
- 同键异 payload 409；同键同 payload 返回原结果；提交响应丢失/查询 404 不导致生成新意图。
- formal delivery 晋升、用户验收与 task complete 的身份、版本/CAS、锁和失败恢复逐段覆盖；实际转存摘要一致。
- Runtime START 先于 Provider，未签收/失去 lease 不调用；输出上传失败能恢复上传而非重新计费生成。
- MIME/内容、路径穿越/符号链接、文件/媒体认证过期、SSE 重连、音频 Range 与安全预览测试。
- 原分支 OAuth machine JWT tenant 变化由 F0 核验，记录兼容发布证据，不顺带宣称通用身份系统已经全部验收。

## 4. 浏览器执行脚本轮廓

1. 登录指定账号，记录实际 Web/API/Client 版本，不把本地 HEAD 当线上版本。
2. 无参考资料需求 → 显式点将 → 自动悬赏议事 → 图片预览/下载 → 引用改色 → 不保存直接选最终成果并验收。
3. 有参考图需求 → 证明固定版本被读取 → 同会话澄清或直接输出 → 主动保存选中稿/文本 → 验收。
4. 音频和普通文件混排 → 播放/预览/下载/保存 → 刷新、离线与恢复验证。
5. 在另一接应模式跑图片主流程；第二用户进行读取/写入隔离和身份切换负向验证。
6. 记录全部实际结果，不仅 API 200/HTTP 上传成功；失败保留对应阶段和恢复动作。

## 5. 证据字段与通过标准

每条用例记录：ID、状态（PASS/FAIL/BLOCKED/NOT_RUN）、exact commit/tree/部署版本、执行命令或浏览器步骤、测试身份标签（不含凭据）、task/conversation/request/turn/message/part/execution/run/asset IDs、文件 MIME/字节数/SHA-256、正式 delivery/decision/task 终态、可复核截图/日志位置。

图片纵切通过仅标 I1；完整 feature 要求全矩阵与专项风险回归，并有用户实际验收结论。源码测试、部署健康与产品验收分开报告；不以任意 1s/3s SLO、剩余预算或未测算资源门槛判失败。真实权限错误、文件不可预览/下载、重复执行、状态误报是实际失败。

## 2026-10-03 实测增量（API1.13.63 / Web1.13.61）

- 原418图片经已授权平台Agent生成；本轮仅恢复原成果，不重复Provider/START。真实会话显示、放大预览、浏览器下载均确认同一PNG：1370×1148，1,863,523字节，SHA256 `2bc30dd5c2acc8434d3be2bde0757bb5346f2d9597f43f95ed9f1ed896fe35a8`。
- UI选中唯一原图并验收：task completed / delivery accepted；随后只读GET正式列表、manifest及正式图片均200，manifest集合与原图摘要一致。未重复验收POST。
- 可选工作空间保存服务端saved，原文件`pws_a528e9d30e944acebc27f1f23376a2ca` v1；旧前端拒绝typed回执导致界面误报。最小解析修复在4403172/164，尚不记线上修复通过。
- 这只是图片主路径的部分真实证据：不把AC07的无刷新实时更新、AC12全部媒体、AC14文字+图筛选/不先归档等未执行分支标PASS；音频/混排/改图/固定参考版本/双模式/权限专项等仍需完整验收。API重启后实际重新登录，不宣称无感恢复。
- 证据：[release1.13.63](integration-evidence-20260928/release-1.13.63/release-result.json)、同目录正式manifest/图片只读回执。完整34项仍未完成。

## 2026-10-03 16:18 增量（Web1.13.64 / Flow4403172 Run164）

- exact `0b665640dbd3de6535f7e020eac24941a232f5ff`，云效2959 PASS / 2 pending / 0 FAIL；同Run制品`9ec99791b41914771e23ba9883ba4f271e55a8dd651440255bc35c371bf5a3b1`，部署单70602569健康，364安装文件与5个公网浏览器资源字节一致。语音SVG修复e586已为祖先，无重复合入。
- 原保存意图首次升级恢复因旧回执未保存operationId，显式重试原幂等POST，返回同一arc/file/v1；再次正常刷新后仅GET原archive operation和finalization，两者仍saved/completed。未重复生成、未重新验收、未新建副本。
- 真实工作空间UI原图v1可预览、下载；下载字节与原图及正式交付一致。截图位于本Main证据目录`/var/tmp/cyf-mmd-bird-delivery-main-20261003/workspace-original-preview.png`和`run164-archive-finalized.png`，均已视觉核验。
- 旧前端保存误报已消除。此轮不新增Provider调用；完整34项仍未完成，不能把图像部分闭环称为全部多媒体功能已验收。
- 证据：[release1.13.64](integration-evidence-20260928/release-1.13.64/release-result.json)。

## 2026-10-03 16:42 增量（API1.13.65 / Web1.13.64不变）

- 真实418事件GET持续404：只读事务内锁读遭MySQL1792拒绝，错误被转换成CHAT_NOT_FOUND。实际数据库仅只读诊断（0 DML）与真实Spring/MyBatis/MySQL测试均复现。修复保持所有身份/代次谓词，只有事件水位/回放改非锁读；写操作保留原锁。
- API `eb9f95a6abe0402bb40168cb2d98b67d471079b3` / tree `09e6077be34bbed27007043ae97ec97ef1fd1670`，24 PASS、0FAIL、0skip，按已授权`local_user_authorized`构建发布并健康。Web继续复用Run164，未重复构建。
- 上线实际SSE变为200，但浏览器原始字节暴露`data:data:`/`data:id:`二次包装，尚不能正常解析。**AC07实时更新与AC11回放仍不通过**，不能把HTTP200当实时展示通过。已进入真实MVC序列化回归/后续修复。
- 详见[release1.13.65](integration-evidence-20260928/release-1.13.65/release-result.json)。没有Provider或START重放，没有修改418原图/归档/验收。

## 2026-10-03 17:22 增量（API1.13.66候选，尚未上线）

- 真实MVC红测在修正fixture认证后复现两项`data:data:`重复编码与一项SSE Accept异常JSON不可表示；首次fixture失败单独保留，未冒充有效产品红测。
- exact `9d55c06a4a3b6fbc7604fe8a24d531ac762585f1` / tree `669c0d58761cf5504e95b2d2a43a3b8b85b4a484`：4项MVC+24项原MySQL/事件回归，28 PASS、0FAIL、0skip。typed ServerSentEvent交由MVC单次编码，事件type/会话/代次来自授权journal，大游标保持字符串；JSON异常显式Content-Type。未修改legacy stream或权限/写锁。
- develop及冻结release/1.13.66已push/readback；既有授权本地正常bootJar完成，JAR `d904aa03fd2f55134c2b69f624dea35607c86dadfba247ec3797c74c4d2c5db8`。**候选不是线上版本**。
- 首次安装在修改前因PID CAS不匹配停止：构建期间健康监控将原Main PID4113499切换到PID4135305/healthmon scope，已部署仍API1.13.65同JAR69dde且UP。未操作新进程、未修改监控；已发conflict-alert并请原Runtime Owner协调维护归属，不盲目重试。
- Web仍Run164，不新增前端Run；0Provider/START重放/生产DML，原418成果保留。实际修复后浏览器测试尚NOT_RUN，AC07/AC11不能提升，完整34项不宣称通过。
- 固定证据：[1.13.66候选状态](integration-evidence-20260928/release-1.13.66/candidate-state.json)。

## 2026-10-03 17:50 增量（API1.13.66实际发布，Web1.13.64不变）

- 固定9d55/tree669候选及JAR d904已实际运行，PID4147942、Runtime Owner a3 scope，HTTP200/UP；配置/launcher不变，monitor已resume且maintenance=false/in_flight=null。不新增前端Run，复用正式Run164。
- 完整保留控制面失败：attempt1 PID变化修改前停止；attempt2应用已健康却因monitor status75误触发回退，旧65实际恢复；attempt3揭示monitor.lock→canonical release锁与deploy release锁→monitor CLI的锁反序。Owner仅释放精确自有shell4147570 FD8（pidfd_getfd/flock UN，signal0），foreign monitor自然继续，未重启健康API，无attempt4。所有monitor CLI以后均置于release锁外，内部只检查maintenance marker/CAS，不能靠扩大超时或无限互等掩盖死锁。
- 真实浏览器原418 GET200单层SSE：events3/4含权威type/会话/代次，ready4；Last-Event-ID4只返回ready，无重复旧事件。实际UI只有1次SSE GET、1次历史GET、0无效事件帧，无旧二次编码引起的resync。原图再次放大预览并视觉确认。
- 只读正式交付仍accepted；manifest/image与工作空间v1均200，原PNG摘要2bc30dd5…一致。未重生成、未重验收、未新增保存副本、0额外Provider。曾登录旧页面后落到API根的HTTP2错误，正常返回kit完成登录；不宣称无感认证恢复。
- AC07/AC11仅提升本次真实协议/已有媒体回放/游标续读子例；尚未新生成实时媒体或覆盖全部乱序/断线场景，完整34项仍未完成。另实测已完成request/output目录仍定期轮询，记录为优化项，不按任意SLO中断。
- 详见[发布结果](integration-evidence-20260928/release-1.13.66/release-result.json)、同目录browser-verdict及原始失败/解环回执。

## 2026-10-03 参考图固定版本新旅程（API66 / Web64）

- 新419/UI选v2→独立测试源文件追加v3→明确点吴用，创建/授权回执仍为v2及2bc原图摘要；AC02仅选择、持久化、授权子例，未证明runtime字节领取。
- 原POST201，GET assignment-operation500：MySQL JSON列重排键/空格与读取原始字节相等检查冲突。真实MySQL/公开read红测2失败；源码8359ec5修复后29通过0失败0跳过，自检后FF推develop，尚未发布。
- 后台已建会话1760458004762，execution另行FAILED/AGENT_DELIVERY_FAILED且Provider START为null；该执行故障未归因，AC17未通过。未重放原点将、未重置状态、未修改418、0生产DML。
- 详见[进展与限制](reference-v2-read-integrity-progress-20261003.md)。完整34项未完成，不以新源代码绿灯提升线上或产品验收。


## 2026-10-03 20:30 增量（API1.13.67，Web1.13.64不变）

- 原419同意图键只读GET实际200：v2/摘要/原ADMITTED会话保留；原FAILED执行和null START没有被修改。查询故障已线上验证修复，不提升整项AC02/AC17。
- 非空source序列化联合record多余null导致严格Client拒收，真实HTTP红测2/10失败；最小修复后10通过。线上旧DTO/实际Jackson+部署Client的离线跨语言验证两种source红绿及10项负向通过；不是完整runtime实测或419唯一历史根因证据。
- API按既有local_user_authorized发布，制品1d4549…、PID19026、HTTP200/UP，monitor已交回；Web无新Run。API重启实际需要重新登录，不声称无感。
- 新正常意图的实际参考字节、local生成、实时图片与同会话改图仍待执行，完整34项仍未完成。详见[本轮发布](release-1.13.67-reference-wire-progress-20261003.md)。


## 2026-10-03 21:54 通用资料M2源码子集

Web `6a2b71e` / tree `5651935a`：66项定向回归通过，Overview统一入口、真实adapter四类型混选/payload/固定版本预览下载/移除、workspace audio两界面渲染及旧响应/身份隔离。HTTP/bytes为fixture、媒体元素是实际Vue DOM；没有真实平台后端原子受理或Agent处理证据，未新跑Chromium/Flow/生产构建/Provider。仅记录UM01/UM02相关源码子例，**不提升UM整项或原34项为通过**；Bounty/M1/M3/M4仍待接通。参见[精确候选及证据](integration-evidence-20260928/unified-materials-correction-20261003/web-source-progress.json)。


## 2026-10-05 三端候选与正式云测状态

API329d44fd / Clientb8d74b1 / Web10ff97b已快进合入各自develop，根gitlink固定配套源码。旧Web Run165的7项失败已修复测试接线，当前定向诊断43PASS、不替代正式云测。原API109/Web166正在cloud_ci；尚无本轮云测终态、制品或新流程真实业务验收。暂停部署配置未改，运行版本未更新、Provider未调用。见 [本轮回执](implementation-evidence-20261004/integration-cloud-ci-20261005/manifest.json)，不自动将AC/UM/FD标为PASS。


2026-10-05 19:54 CST补充：API109正式CI及同Run制品核验完成（312 suite XML /2667测试条目/0失败/101 skipped；不代表全业务验收）。Web166 checkout精确匹配，扫描通过，完整测试/构建仍进行中；API/Web/Client运行版本未更新。以本轮manifest和api109制品回执为准，不将源码/CI成功自动提升为线上AC通过。


2026-10-05 20:15 CST：Web166终态FAIL（3136通过/2pending/10失败，无制品），旧接线/入口断言已修复为Webf6b81b4，定向86PASS，lint与基线同7错误无新增。正式Web167正在运行，checkout尚未报告。API109有效证据沿用。真实运行版本/Provider闭环仍未验收，发布/调用授权待用户答复；不据此更新AC为PASS。

20:17 CST只读回执：Web167实际checkout已报告f6b81b40ee4a579c579af4cb7ab1e0e76e362173，与目标一致，scan SUCCESS，完整测试/构建仍RUNNING；覆盖上段checkout pending的阶段状态。
