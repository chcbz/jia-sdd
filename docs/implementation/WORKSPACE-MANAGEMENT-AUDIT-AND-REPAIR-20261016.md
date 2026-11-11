# 资料管理全功能排查与修复方案

> **2026-10-16 16:47实施更新：必要前端修复已实现并合入develop，最终commit `1e779e9`。229项本地定向回归、原型三视口检查通过；正式Flow启动回执UNKNOWN，最终候选尚无正式通过证据，未部署。详情见代码级方案§16；其余问题未一并修复。**

核对日期：2026-10-16（Asia/Shanghai）。任务：`WORKSPACE-MANAGEMENT-AUDIT-20261016`。Owner：本聊天 Codex。

## 必要性复核更正（2026-10-16 16:10）

本轮未新增运行测试。原方案存在不必要扩展，最新收敛决策见代码级修复设计§15，优先于下文拟实施结论。尤其F13仅证明隔离fixture重复响应头：安装包含spring-web 7.0.8，原fixture实际运行依赖等价性尚未核实，业务类SHA一致不足以外推线上；撤回“生产公共层必须先修”的断言。F10实际为提交成功/ready后detail为空且error保留，不是已证明上传接口报失败。会话执行输入变动是否完整推进回收确认revision仍待分支级验证。不能称所有改动都有必要或影响已完全闭合。API当前HEAD ab379ba8f27a3b1481fc426d6d007ae76b096b2e，仅新增schema initializer及测试变化，历史测试未移标新源码；Web未变。

## 继续核验收口（2026-10-16 15:12，Asia/Shanghai）

**以下为最新诊断结论；后文初轮数字/待验项保留作历史基线，若冲突以本节为准。调查已推进到可执行的隔离证据收口，不等于全功能验收或修复上线。** 原11组扩展为13组：新增F12同key并发竞争异常、F13公共响应关联头重复；另有独立的线上502可用性异常。

### 本次实际完成

|证据层级|精确结果|边界|
|---|---|---|
|既有前端回归|原70通过，未重复跑；原20诊断观察保留|本机诊断，非Flow正式验收|
|新增关联adapter诊断|6个缺陷复现观察通过：任务/会话attach、detach弱ETag已提交回执拒绝；丢回执后attach换key|`completion/link-observations.test.mjs`及`.log`；不是功能修复通过|
|旧后端HTTP fixture整改|104/104通过，17 suites，API测试候选`b35568b6146773d6ed3fb9c529190d192af13458`|只改5个旧测试信封、Q请求、字符串及preview断言；该轮后续新增测试编译失败，不把整轮Gradle称成功|
|新增真实MySQL/HTTP诊断|最终候选`cf37f8e36f6c0ecbdd5894450812fe49cd01d9af`，一个聚合JUnit测试通过；14条观察=8正常/流程完成+6缺陷复现；validateLayering通过|`verification-8.log`、`junit-completion/`、`mysql-http-observations.json`；观察不是14个独立JUnit用例|
|真实浏览器|8条观察=6正常+2缺陷复现；46个代理请求；三视口预览/起草、落盘哈希、上传→重命名→追加→回收→恢复、身份切换|**未修改链首先复现F13失败；后续UI使用测试代理对完全相同的重复请求ID头去重**。不是原链全通过，不是完整站点/真实手机或线上OAuth|

- 私有MySQL8.0.21+真实schema/MyBatis/事务/文件存储+Tomcat+生产`ResourceServerConfig`与`AccountSecurityJwtValidator`。账号目录、会话访问端口和少量辅助页面接口为合成fixture，不冒充整个生产应用。
- 匿名合法/畸形请求401、伪签名401、过期安全epoch401；owner/client跨scope详情、usage、版本、下载、预览、part、operation拒绝；请求体身份注入400。只证明这些已测组合，不声称所有越权场景穷尽。
- 0/50/51目录分页和无匹配搜索；101历史版本100+1分页、追加到102后旧cursor仍准确、跨文件cursor拒绝。
- 任务101条只报100、会话1条持久化但未报告；执行输入0/1/100/101的101截断、非QUEUED及REVOKED过滤已实际验证。未调用任何Provider。
- 强CAS回收/恢复保留原字节；弱If-Match重命名/回收/恢复412；追加不更新metadataRevision；受控usage跨查询插入引用后返回旧revision配新引用，均有运行证据。
- 并发追加得到一个COMMITTED、一个VERSION_CONFLICT；任务关联与回收竞争得到一个COMMITTED、一个METADATA_CHANGED。仅已测锁序，无“永不死锁”承诺。
- 真实浏览器下载`audit.txt`落盘SHA-256：`fc124c1ae69e29d988c1866d9b0fdf6ac7a3d2a18d81ba211e355c6a038d49eb`。真实下拉选v101时仍显示v102，下载/起草不请求，历史仅100项且缺v1，F02/F08确认。

### 新增两项必须修复

**F12（P1）同幂等键竞争可漏出SQL异常。** 两次首次查无记录经屏障同时完成，随后竞争插入：一个COMMITTED、一个`DuplicateKeyException`；数据库仍只有一个文件/operation。`PersonalWorkspaceWriteService.claim`在同一重复读事务内catch后重读旧快照，不能保证看见另一事务已提交记录。应让claimOnce独立事务先回滚退出，再由非事务编排调用新事务查回执；保留scope/hash/唯一约束，不能吞异常或换key。详设§11已给具体类和方法。

**F13（P1）公共响应头重复阻断浏览器。** `RequestIdFilter`与`ApiEnvelopeAdvice`共同写`X-Request-Id`；原始上游输出两个相同头，浏览器得到`id, id`，与单值JSON/request不一致，`useHttp`拒绝HTTP200。详设§12给统一Servlet写头方案及真实HTTP `allValues`恰好1的回归要求。不能通过放宽前端严格解析或把测试代理干预带入生产解决。安装JAR这3个边界类也已比对SHA一致。

### 线上只读结论及不能补出的证据

- **2026-10-16 15:07:43再次检查**：文件目录、合成不存在任务/会话关联入口匿名GET均502，10018无监听；14:47同样结果。14:49进程检查未见规范API JAR进程。仅确认这些时点的可用性异常，停服原因未确定，不推断是本功能故障或某个任务造成；没有重启/部署/写生产数据。需服务Owner核对活动维护/发布及生命周期日志，按授权恢复流程处理。
- 原nginx安全访问日志不记录ETag/If-Match；**无法从这份历史日志还原用户此前失败请求头**。弱ETag是隔离完整复现且配置吻合的高置信原因，不排除真实版本冲突。服务恢复后需用合成身份捕获新的脱敏请求头，不能把新请求冒充原用户历史证据。
- 共7个选定安装类与当前编译业务类字节一致（原4类+关联ID边界3类）；没有完整源码→安装回执闭包，不能宣称整包版本完全对应。
- 仍未完成：生产完整OAuth登录/真实账号全链路、真实移动设备/全媒体解码、运行中生产配置确认、修复后前端Flow与后端固定提交验收、授权版本化发布与在线回归。收费Provider明确不在本审计范围。

### 交付状态

主Web/API无本次业务改动。新增测试只在`/home/isp/wsps/worktrees/cyf-workspace-audit-completion-20261016`分支`codex/workspace-audit-completion-20261016`；最终tree `39288cb46905d565104290fe8910c7218868abba`。未合入、未push、未Flow、未部署。测试fixture整改不能当产品修复；所有拟修代码均在代码级方案中，尚未实施/编译。建议先处理生产可用性，再修F13公共协议边界，随后F01/F02及状态隔离，最后联动完成幂等F04/F12、usage一致性/计数与历史分页。

## 一、初轮结论（历史基线）

**不是单一的“删除按钮”问题，而是文件版本契约、异步页面状态和写操作恢复没有一起收口。** 本轮覆盖资料管理的现有功能入口、前后端实现与隔离回归，形成 **11 组问题**。最先修复的是：

1. 压缩后的 ETag 被当作业务写入版本，回收、重命名、恢复可能全部 412。
2. 历史版本下拉框把协议字符串变成数字，导致切版本后仍展示旧预览、下载/起草不响应。
3. 文件 A 的迟到写回执能覆盖正在查看的 B，产生 A 元数据配 B 版本列表。
4. 写操作回执丢失后再次点击会生成新幂等键，上传可能产生重复文件。

**本轮不是“全功能验收通过”或“已修复”。** 前端现有回归70项通过；补充20项诊断观察通过，其中9项验证正常/保护路径、11项确认缺陷现象（缺陷复现通过不等于功能通过）；后端104项实际执行，93通过、11失败；分层检查通过。未改业务源码、未部署、未修改用户生产资料。

## 二、范围、源码与生产边界

### 2.1 固定源码

|组件|本地受查源码|tree|实际查询的远端 develop|
|---|---|---|---|
|Web|`2c8d6703eead623f555029341101cb688b9d448a`|`d436146d65e07a7af842b3e83271143e775b0390`|`421f628c245b83466cafb70510ff69188180bdee`|
|API|`fc399976710f5b724916013926be2cbff899af8c`|`6fed56f00065889f186d578d54a1656afb66a43a`|同本地|

查询日期为2026-10-16；Web差异只有本聊天上一项议事输入框提交，本轮未推送。两组件开工与收口均干净。接口以 `/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.2（2026-10-14）为固定基线，不恢复旧裸响应或数字版本兼容分支。

### 2.2 生产只读检查

- 当前安装 Web `index.html` 指向 `index-CIv_J8tq.js`；沿当前入口依赖图定位到 `JuyiHallEntry-CG_jCWul.js`，并确认其中包含原样回传详情 ETag 的资料写入逻辑。没有把静态目录里残留的33份历史同类bundle都当成正在运行的版本。
- API实体JAR：`/home/isp/hosts/cyf/api/cyf-api-kit.jar`，SHA-256 `aaaf5667f88d666dfcd369102a7131ad081e47170fa03e9361586292fe68a45c`。本次未取得将该JAR绑定当前源码的完整安装回执，不推断源码/安装版本完全一致。
- 2026-10-16已读取日志窗口：目录、详情、预览、usage及一次下载有200记录；回收2次412，重命名1次412。状态码只能证明这些请求结果，不能证明下载内容正确或其他所有用户操作通过。
- 未使用用户会话令牌重放写操作，未抓到该失败请求实际 `ETag/If-Match`。因此，gzip弱ETag是**完整隔离复现且与部署配置一致的高置信根因候选**，不是已经捕获线上请求头的唯一根因。旧详情版本与真实引用更新也能触发同样提示。

## 三、逐功能核验结果

|功能|本轮执行/核对|结论与缺口|
|---|---|---|
|列表、搜索、媒体过滤|实际composable请求参数、分页合并/去重、正常和失败路径；线上目录200|正常路径通过；加载中换条件及失败后旧cursor存在缺陷（F05）|
|资料/成果/回收站分类|真实Vue组件挂载与点击，状态切换延迟回包；来源本地过滤源码|加载中切回收站可显示ACTIVE结果（F05）；来源分类分页有“继续读取”提示，不能当全量服务端筛选|
|上传资料|文本上传、空/octet-stream MIME推断、拒绝HTML；现有音频/现代图片矩阵；后端创建/存储/幂等服务测试|正常路径通过；回执丢失重试可重复创建（F04），提交成功与详情读取失败未分层（F10）|
|查看文件、来源、详情切换|真实组件+composable；先后两个GET与迟到写入对比|GET已有防串页保护；写操作没有等价防护（F03）；详情中的空relations/derivation不应被解释为完整来源/引用目录|
|重命名|强ETag成功、弱ETag412、真实冲突不自动重试；线上PATCH412|受F01/F03/F04影响；服务端保留版本和原始字节的逻辑正确|
|追加新版本|expectedPreviousVersion传参；后端版本CAS、旧版本保留测试|正常CAS路径通过；页面下个版本显示拼接错误（F02）；不确定结果恢复不完整（F04/F10）|
|历史版本选择|真实下拉框从v2切v1；预览/下载/起草联动|确定失败（F02）；100条以外历史没有前端分页入口（F08）|
|文本/图片/音频预览|现有前端9个多媒体文件样例、受控Blob URL、音频controls；后端内容/renderer测试|基础路径通过；切版本失败（F02）、部分预览警告隐藏（F09）|
|Word/Excel/PPT/PDF预览|后端11项真实渲染/提取测试，含多页/多sheet、外部关系不访问、损坏文件、文本截断；前端分片导航/URL释放|渲染测试通过，但HTTP旧契约用例失败；不能当生产Office全链路已验收（F11）|
|下载固定版本|显式字符串版本读取Blob与文件名；服务层ACL/存储完整性；线上一次200|基本路径通过；下拉框切换后静默不下载（F02）。未做真实浏览器落盘文件哈希比对|
|用于新委托/交给Agent|真实组件固定版本emit；现有执行/资料关联前端回归和后端34项execution service测试|初始固定版本路径有覆盖；切版本后按钮无响应（F02）；未调用收费Provider或真实Agent|
|任务/会话关联与解除|两个前端composable现有测试、两个后端各5项服务测试；HTTP测试|服务层回归通过；HTTP部分仍未通过（F11）；usage未汇总会话关系且有无提示截断（F07）|
|引用影响确认|usage与旧ETag组合复现；源码核对100条限制和返回结构|快照不一致、失败后旧确认仍可继续使用（F06）；影响摘要不完整（F07）|
|回收/恢复|强前置条件正常、弱ETag失败，后端metadata CAS测试|同受F01/F03/F04/F06影响；逻辑回收不删除原始字节、历史快照保留是设计行为，不应改成强制物理删除|
|身份切换/授权隔离|已有迟到请求清空、补充迟到PATCH隔离；后端owner/client服务层和文件篡改/符号链接测试|所执行保护用例通过；HTTP完整安全链和第二个生产账号未验收，不宣称无所有越权风险|
|操作回执/失败恢复|已知operationId只读查询通过；断网后丢回执与新key重试复现|原operation查询入口存在，但无ID未知结果及页面恢复尚未闭环（F04/F10）|

格式范围：文本、PNG/JPEG/WebP/GIF、MP3/OGG/WAV/M4A/MP4音频/WebM、DOCX/XLSX/PPTX/PDF；前端多媒体测试使用合成Blob，不能替代真实媒体解码。Office renderer测试使用真实构造文件。加密/损坏文档预览不可用时应明确提示并允许授权下载，不能伪报完整预览。

## 四、问题清单与根因

### F01 — P1：表示层ETag直接用于业务写入

- 入口：`usePersonalWorkspace.js:191–205,269–280`；后端 `PersonalWorkspaceWriteService.java:140–143`。
- 当前详情保存响应ETag，mutate原样用作If-Match；后端只接受 `"fileId:metadataRevision"`。同一nginx二进制隔离实验中，JSON压缩把它变为 `W/"fileId:metadataRevision"`。
- 强ETag同版本成功，弱ETag同版本回收/重命名/恢复都失败；文件不必真的发生变化。
- **修复**：在资料模块按已验证的fileId和十进制字符串metadataRevision构造业务前置条件；若核对响应ETag，只接受与该业务版本对应的强/弱表示，不无条件剥除任意 `W/`。继续保留后端精确比较、ACL和事务锁。不通过关闭所有gzip或接受任意版本解决。
- 缺少线上失败请求头仍须补只读取证，避免把真实并发冲突误判为gzip问题。

### F02 — P1：版本号字符串契约在组件中被破坏

- 入口：`PersonalWorkspace.vue:31,158,239,264`；`usePersonalWorkspace.js:328,346`；`PersonalWorkspaceWire.java:9–13`。
- 协议version/latestVersion/byteLength为十进制字符串。`v-model.number`强制转数字后，VERSION校验静默返回null，保留之前预览；selectedExecutionVersion严格比较也找不到项，无法起草。
- 同根因的展示错误：latestVersion='2'加1显示v21；byteLength='1024'显示“大小未知”。download/previewVersion默认参数传了latestVersion对象，不是其.version。
- **修复**：版本状态始终为D1字符串，移除`.number`，默认使用`.latestVersion.version`；仅显示层在规范范围校验后做BigInt或安全整数计算，再输出字符串。byteLength按D0/64位范围安全格式化，不统一粗暴Number化。版本切换时先标记“正在读取该版本”，失败也不得保留旧内容冒充新版本。

### F03 — P1：写回执和文件详情缺少资源级异步隔离

- 入口：`usePersonalWorkspace.js:244–280`，`PersonalWorkspace.vue:302–306,365–369`。
- 请求只记录身份generation，未固定当前fileId/detailGeneration。A重命名开始→查看B→A返回，detail被写成A.file + B.versions。
- **修复**：每个操作绑定身份、目标fileId、详情代次和操作ID，响应需校验所属文件；迟到回执可以更新A缓存/操作记录，但不能覆盖B详情或导航。关闭详情/切文件使视图代次失效。请求已发出时“离开页面”不等于服务端操作取消，仍需记录未知/提交状态。每个文件的写按钮和回收确认按操作状态互斥，不只依赖一个共享actionState。

### F04 — P1：不确定写入结果重新生成幂等键

- 入口：`usePersonalWorkspace.js:221–280,402–415`，同类关联动作需一并检查。
- 上传服务端已提交但客户端丢回执→再点上传生成新key→可能创建第二份。模拟两个提交已复现。服务端“同key不重复”测试通过，不代表客户端正确复用key。
- **修复**：用户一次明确意图生成一次key，绑定身份/目标/动作/输入摘要；双击共用进行中intent。断网进入UNKNOWN，保留key，不伪报失败或成功。已有operationId使用原GET查询；首个回执完全丢失时，补齐owner-scoped原key查询能力，或在已确认的幂等合同下显式重放完全相同输入和key，不能换key盲重试。涉及上传字节不可恢复时要求用户重新选择并核对摘要。明确终态和新用户意图才开新key；身份切换清除本地跨身份状态。

### F05 — P2：目录切换与游标没有绑定查询条件

- 入口：`usePersonalWorkspace.js:157–189`；`PersonalWorkspace.vue:345–350`。
- loading时refresh直接false，用户切到回收站后请求被丢弃，旧ACTIVE回包仍写入列表。新搜索失败又保留旧cursor，随后“更多”用新q配旧cursor。
- **修复**：以identity+q+mediaFamily+state生成queryKey和列表代次；切条件使旧响应失效，并执行最新条件，不丢请求。cursor绑定queryKey；失败明确显示旧结果/不可追加，不将旧cursor用于新条件。保留分页去重、来源分类的“尚未读取完整”提示。

### F06 — P2：回收确认用的是两个不同时间的快照

- 入口：`usePersonalWorkspace.js:294–312`；`PersonalWorkspace.vue:343–369`。
- usage返回新的impactRevision，但If-Match仍取旧详情ETag；412后trashUsage不失效，重复确认继续带旧值。重命名/追加/切文件也可能使已显示确认失效。
- **修复**：确认态固定fileId、metadataRevision、impactRevision和显示过的引用摘要。获取同一可确认快照；必要时由usage返回同一事务读取的业务版本。412应使确认失效、读取最新摘要并明确要求用户重新确认，绝不自动删除。文件/身份/相关写操作变化时撤销旧确认。

### F07 — P2：引用影响摘要不完整，不能当精确总数

- 源码确认：`PersonalWorkspaceServiceImpl.java:246–256`只查询任务引用/活跃执行，各最多100条；未查询会话关联，返回中没有截断标识。前端直接把数组长度之和显示成关联引用总数。会话关联写入却会增加metadataRevision。
- **修复**：按已冻结业务schema补充会话引用，任务/会话/活跃授权分组；返回精确计数或明确hasMore/分页，不能简单提高硬编码100。与F06共享一致快照。提示“移入回收站不等于撤销已授权执行”，已固定快照继续按原授权生效；停止/撤销走既有明确动作。
- 本项为源码级确定缺口，未在生产造101条引用；补测0/1/100/101、仅会话引用、确认期间新授权与解除。

### F08 — P2：历史版本只展示详情最近100条

- 后端 `versionsPage`已有100+1探测及fileId绑定cursor；但FileDetail.versions只读最近100条，前端仅用这个摘要，没有读取版本分页接口。
- **修复**：接入已有版本分页，不新建重复API；表明已加载窗口/下一页，追加后不悄悄替换用户选中的固定旧版本。101版本及分页期间追加新版本必须验证无漏项、重复或跨文件cursor。

### F09 — P2：部分预览警告被UI隐藏

- adapter已保存 `partial/reason` 为preview.message；实际文本/图片/音频/parts成功分支没有渲染该提示。
- **修复**：所有预览类型固定展示部分/截断警告和下载原件入口；分页失败、受保护/不支持、损坏文件分别显示。不得用扩大无证据大小上限或无限加载来掩盖不完整。

### F10 — P2：提交成功与详情刷新失败混成一个状态

- upload/appendVersion收到提交回执后调用select，却不检查返回；详情GET失败时仍返回成功且设ready。已复现“有成功回执、详情为空、ready、同时有错误”。
- **修复**：分别保存“文件已提交”和“当前详情读取状态”；成功回执不可因后续GET失败而否认，但不能标ready或导航到空详情。提供仅刷新该文件的按钮，不再次提交上传。旧页面的回执不能改变新页面导航（F03）。

### F11 — P1（验收基础）：旧测试给出了不完整的安全感

- 后端17 suites共104项，11项失败，见下节。旧HTTP用例仍读根`$.operation/$.parts/$.items`、`message`及数字version，实际当前接口已经使用统一信封和字符串版本。
- 组件现有mock又使用数字版本；70项前端绿灯没有覆盖真实D1字符串经下拉框后的行为。旧 `juyiting-workspace-browser-smoke.mjs`的mock缺现行统一信封/hasMore并使用数字版本，不能当作当前版本端到端证据。本轮没有为凑绿灯修改这些业务测试。
- **修复**：先统一真实接口fixture，贯通JSON→useHttp→composable→真实组件；改正确断言，不放宽生产解析器/恢复旧兼容。保留强/弱ETag、串页、延迟、断网、101条、身份切换等新回归。鉴权先后用例必须覆盖完整Security Filter链，不能只把401改400就算通过。

## 五、后端测试失败分析（不能跳过或涂绿）

|suite|执行/失败|原因及影响|
|---|---:|---|
|PersonalWorkspaceControllerPreviewTest|2/1|旧`$.parts`路径，当前为信封data；上传MIME测试通过|
|PersonalWorkspaceConversationFileLinkControllerTest|4/3|1条无完整安全链且旧请求body的401/400顺序问题，2条旧`message/executionSnapshotsPreserved`路径|
|PersonalWorkspaceTaskFileLinkControllerTest|4/3|与会话关联同类|
|PersonalWorkspaceExecutionControllerTest|7/2|旧`$.executionId/$.items`路径|
|PersonalWorkspaceHttpPersistenceIntegrationTest|2/2|旧`$.operation`断言；另一条用`/file/fileId`提取空ID导致H2查不到行，尚未走到其owner隔离断言|
|其余12 suites|85/0|service11、execution service34、task/conversation link各5、write1、storage boundary3、preview renderer11、output validator2、schema合计13|

注：93通过包含上列有失败suite中仍通过的8项。H2/MockMvc不是生产MySQL+网络E2E；所有测试0 skipped。11失败中9条由旧响应解析/断言导致，2条鉴权/参数绑定顺序需要完整安全链进一步验证。没有证据据此声称生产授权已失效，也不能将其宣称验证通过。

前两次启动未运行测试：默认Gradle缓存metadata缺失、切换依赖home后消费凭据init缺发布DSL占位属性。未删除共享缓存、未修改全局配置；依照归因矩阵使用既有local_init/credentials辅助函数、独立外部build root后成功执行测试。完整命令见backend-command.json。因测试失败，单独执行validateLayering并通过；不把分层通过当作整体测试通过。

## 六、建议实施顺序与修改边界

本轮只给方案。后续仍一个Owner连续推进，阶段完成不是逐次审批点，也不创建独立Reviewer。

### 批次A：先解决用户可见的核心失败

修改边界：`web/src/composables/usePersonalWorkspace.js`、`web/src/components/workspace/PersonalWorkspace.vue`及相应测试；必要的资料模块业务版本helper复用现有工具，不全站重构。

- 修F01/F02/F03/F05/F09/F10，并将F06现有确认在412后强制失效。
- 将操作目标、列表查询、预览/详情代次分开管理；防错对象优先于仅加按钮disabled。
- 补真实字符串fixture和强/弱ETag链路回归。后端严格CAS不改，不直接关闭生产压缩。

### 批次B：补齐资料生命周期的完整合同

- F04原意图幂等恢复（需要的只读恢复能力同步接口目录/schema/前端）。不得在待定结果下生成新请求重复上传。
- F06/F07同一事务一致的usage快照、会话引用与可解释计数/分页；复用现行file行锁顺序，避免回头获取task锁。保留用户明确重新确认。
- F08接已有版本分页。默认不需要数据迁移；若实现最终确需新持久字段，另列迁移、备份与恢复授权，不先假设可以改生产表。

### 与A/B同步：修验收证据链F11

- 将11条HTTP失败迁到规范v1.2，并重新真正走到H2持久化、幂等重放、owner/client断言。
- 关联鉴权用例跑完整安全链；真实MySQL隔离fixture验证事务/锁/版本CAS；不使用生产数据库。
- 同批真实浏览器验证桌面/手机：点击、切版本、下载落盘、回收确认/恢复；使用隔离账号/合成文件，不修改用户资料。
- 既有UI/browser工具先更新准确fixture；不能让mock再用已经废止的数字版本或裸响应绕过现行解析器。

### 发布

确定版本→固定Web/API commit/tree→前端Flow4403172正式测试/构建、后端干净固定源码经编排器本地测试/构建→各自同批不可变制品→按版本计划部署→隔离资料线上核验。

develop合入/push不等于部署；没有当前Flow或本地build制品证据不得报告上线。若只交付前端批次A，可单独发布，但明确F04/F07/F08是否仍未完成，不把部分修复报告为资料管理全通过。

## 七、验收矩阵（修复后必须实际跑）

1. **HTTP版本标识**：强ETag、gzip弱ETag、响应头未暴露、有真实revision变化；前3种按业务版本成功，真实冲突412不写库；重命名/回收/恢复均覆盖。
2. **版本标量**：'1'/'2'/'10'及规范上界、合法大byteLength；预览/下载/起草同一固定版本；v9→v10显示正确，不允许数字/String双轨解析。
3. **异步导航**：A写入未返回时打开B/返回列表；旧回执不换页面、不改B；身份切换后旧数据不出现。
4. **查询分页**：快速换搜索/状态/分类，首屏和更多失败；旧条件cursor不能跨查询；0/1/50/51条完整遍历。
5. **上传/追加与幂等**：双击、写前断网、提交后丢响应、服务503/PROCESSING、刷新页面恢复；同意图最多一次持久化；追加CAS保持旧字节hash。
6. **回收影响**：0/1/100/101任务引用、仅会话引用、活跃执行，确认期间关联/解除/新授权；变化必须重新确认，原执行快照保留，新授权按回收状态拒绝。
7. **历史版本分页**：0/1/100/101版本、分页期间追加、跨fileId cursor；无截断冒充全量。
8. **预览/下载**：所有声明支持格式的真实样本，损坏/加密/partial/多页文件；原始下载哈希一致、文件名安全、Blob URL清理；安全链禁止其他owner/client访问。
9. **提交与刷新分离**：POST已提交但GET详情失败，只读重查，不重复上传；恢复后正确显示已提交版本。
10. **生产边界**：隔离测试账号和合成资料，保存前后fileId/version/hash/状态；不以真实用户资料作破坏性测试；不触发收费Provider来冒充文件管理验收。

## 八、证据与当前未验项目

证据目录：`/home/isp/wsps/cyf/docs/implementation/evidence/workspace-management-audit-20261016/`。

- `frontend-tests.log`：现有70项。
- `audit-observations.test.mjs`、`audit-observations-complete.log`：真实组件/composable、现行字符串wire的20项诊断观察；9正常/保护路径、11缺陷复现。
- `backend-command.json`、`backend-tests-local-init.log`、`backend-summary.json`、`junit/`：104项、93通过、11失败，固定API tree及fixture摘要。
- `layering.log`：分层通过。
- `production-route-statuses.json`：仅聚合路由/HTTP状态，不保存用户文件ID、内容或会话令牌。
- `current-web-bundles.json`、`live-bundle-snippets.json`、`installed-fingerprints.json`：实际安装入口/相关bundle/JAR摘要，源码映射未冒充完成。
- `source-index.json`：源码落点和摘要。
- gzip隔离实验与先前412复现：`/home/isp/wsps/cyf/docs/implementation/evidence/workspace-trash-diagnosis-20261016/`。

**尚未验收**：当前源码前端正式Flow、真实浏览器全流程/移动设备布局、生产OAuth双账号、生产文件实际失败请求头、修正fixture后的HTTP全链路、当前MySQL真实并发锁序、101条引用/版本的运行时验收、真实下载落盘hash，以及全部修复后的线上版本。以上边界不能由本地绿灯替代。

此次交付是可实施的排查与修复方案，不是代码修复或上线完成。根目录其他任务脏修改保持原样。

## 九、代码级方案补充（2026-10-16）

用户要求细化到代码，详见 `/home/isp/wsps/cyf/docs/implementation/WORKSPACE-MANAGEMENT-CODE-REPAIR-20261016.md`：逐文件/函数、业务CAS helper、视图/查询代次、原key恢复接口与状态机、usage DTO和一致读事务/count SQL、版本分页、失败测试迁移、正式验收与发布顺序。该补充是拟实施设计，不表示业务实现或验证完成。

本次源码复查还确认：任务/会话关联有相同响应ETag严格校验风险；completeAppend未增加metadataRevision；usage中的活跃执行实际仅QUEUED+ACTIVE。分别并入F01/F04和F06/F07详设，尚未新增这些派生场景的运行时证明。原测试数量及未验边界不变。
