# 生产图片流程浏览器回归（2026-10-23）

## 结论

**部分通过，不能认定完整流程验收完成。** 使用ziyue真实登录，承办人为吴用（跨用户候选），只创建本次普通测试事项517；未使用李逵、未发资金榜。PDF按用户要求不验。

- 上传→列表刷新→自动选中→移动端预览开关→办事页直接预览→创建事项→指定吴用→真实生成/交付红色PNG：通过。
- 精确尺寸：失败。输入JPEG为256×256，要求保持尺寸，实际PNG的IHDR与浏览器naturalWidth/naturalHeight均为1254×1254。中心像素RGBA250/2/2/255，颜色修改正确；不是仅凭缩略图判断。
- 自然二次修改：已发送“改成绿色并精确调整256×256”，服务端请求持续RUNNING、turn为DISPATCHED、lastDeltaSeq=0；最后权威观察时间见result.json。未有终态，不能把已接收当修改完成。
- 最终验收/完成态刷新：未执行。活跃请求使“验收此版”禁用；没有绕过保护、验收旧成果充数、重复发送、自动重启或因等待时长取消请求。

## 精确源码、上线与文档集成

- 本轮文档已正常push根develop `627675d6fc775feac533666680ed0461ad974582` 和Web develop `638084d26ec9a193240566bf45b33602cef8e0e0`，远端readback一致；根API gitlink未改。共享脏checkout未切换或回退。
- 生产Web **1.16.43 / Flow295**，源码`669bdc9d6439d1bd7eb71df5ed401202a648f419`，包含图片修复`9dbd132e8bc25119c0532cbed672ab7fa4a214b3`。入口、主JS/CSS、实际加载的Hall JS/CSS共5个文件与安装清单字节/SHA/大小一致，见[资源核验](loaded-assets-verification.json)。
- API **1.16.30 / Flow246**，源码`b0735f57a7b454fa7a6fb9886fa3914131986779`。Flow安装记录与现行JAR SHA一致，localhost actuator/health为UP；实际PID的-jar为canonical实体目录。相关Flow与原记录查询证据位于`/var/tmp/cyf-doc-chain-fix/`，不把最新CI-only Run当发布。
- 本次未触发应用构建/部署；文档改动不要求上线，不顺带发布其他会话最新develop的档案阅读器/PPT变化。

## 浏览器检查结果

| 检查 | 结果/证据 |
|---|---|
| 上传后立即刷新列表并选中 | PASS，[PC截图](pc-upload-success-list-refreshed-auto-selected.png)；新文件1146字节、v1 |
| 移动端预览可打开/收起 | PASS，390×844，[预览开关](mobile-jpeg-preview-toggle-open.png)，图片实际256×256 |
| 办事页附件直接预览 | PASS，[独立预览](mobile-home-direct-attachment-preview.png)；未跳回选择资料 |
| 指派吴用 | PASS，task517 assignedTarget.displayName=吴用，agentId尾缀wuyong；只POST一次point-and-deliberate |
| 真实图片处理与读取 | PASS，ACTION_REQUEST→EXECUTE→COMPLETE；PNG1159811字节，[红色成果](pc-first-delivery-red-preview.png)，SHA见result.json |
| 图片精确尺寸 | FAIL，要求256×256，实际1254×1254 |
| 详情返回列表 | PASS（进行中分支），[手机列表](mobile-in-progress-list-task517-present.png)有7条进行中及517；待点将筛选0为空是正确结果，不冒充已测待点将返回分支 |
| 自然修改、离开后重入原会话 | 请求与原用户消息保留，未另建会话；修改结果仍BLOCKED |
| 移动端活跃请求时的验收保护 | PASS，[按钮禁用](mobile-followup-still-running-acceptance-disabled.png)；最终验收未执行 |
| PC/移动端最终完成态 | NOT_VERIFIED，依赖二次请求终态与实际验收 |

## 异常边界与下一步

1. 尺寸不是CSS缩放：PNG二进制IHDR和自然尺寸均1254。安装Runtime1.2.6的`controlled-image-gpt-cli-executor-v3.mjs`使用`--size auto`，回执只要求宽高为正整数；实现不存在按任务自然语言强制精确尺寸的保证。该源码观察不足以单独证明本次所有尺寸偏差的唯一原因，仍需将本执行绑定到实际调用/回执。应在执行能力/输出契约定位，不能把图片尺寸限制加入通用存储层，也不能直接归咎模型。
2. 二次请求无增量：requestId `mmd-typed-request_19cec82a0f508c99029d91d1593c5b5bb3465154`，dispatchId `dispatch_316811d9069cd61435511be4c1df49e56e337f03`。吴用通道connected/registered/ready且presence新鲜；这只排除当次明显离线，不能证明模型已执行。继续按dispatch→实际执行者/turn→上游响应逐层归因；未定位根因前不标“模型问题”。
3. 待二次请求终态和图片质量问题解决后，继续选定成果→确认验收→COMPLETED→刷新持久化→办事/事项入口一致性及PC/移动端最终截图。当前没有写入虚假的验收成功。
4. 浏览器写保护曾拦截漏带`/agent`的首次上传和自动recommend POST；前者通过原上传幂等核对成功恢复，后者未影响显式选择吴用。这是诊断工具行为，不是产品故障；初次失败截图未作为PASS证据。

原始范围内网络/状态证据保留`/var/tmp/cyf-external-flow-20261021/browser/sdd-image-regression-20261023/live/`，登录凭据/Token/浏览器会话不纳入仓库。本文和result.json均按最后观察时点记录，不表示请求此后不会完成。

## 根因续查（2026-10-23 15:20 CST）

本节修正上文初查范围，不重标业务验收通过。唯一Owner仍为当前会话；只读生产记录与现行程序、使用ziyue重新登录查询；未重发/取消请求、未重启或部署。基线：线上API b0735f57a7b454fa7a6fb9886fa3914131986779；Runtime1.2.6源码7dd120f5d3a61559ebf4347aa63b638f7e6a4153。五个相关安装模块与该源码逐字节SHA匹配，见runtime-source-verification.json；不是依据共享checkout HEAD推断。

### 1. 尺寸不符：实际走Skill HTTP，不是旧CLI路径

本次execution `pwe_835057c81738e5cd6ff961b2120fb026289127cdd255a776ebc6462d53b5`的command/result/effect与实际PNG的SHA闭合，见execution-chain.json。已安装image-edit1.0.0的entrypoint为`image-http.edit`，runner为provider-operation，parametersSchema只接受空对象；绑定model为gpt-image-2.5。`skill-runners/image-provider.mjs:15-37`只把256×256留在prompt，HTTP body没有尺寸字段，响应直接交付；`image-http-codec.mjs`只验证PNG签名/传输封套等，没有尺寸履约校验或确定性缩放。因此系统把“能解码/能归档”当作执行成功，却未保证用户要求的精确尺寸。模型实际输出1254×1254后，该结果被原样成功提交。上文CLI的`--size auto`不是本次直接根因，不能继续用于归因。

修复落点是image-edit能力的参数/输出处理：明确尺寸约束，在图片执行适配器按约定处理并核验实际像素，保留原/最终摘要及效果幂等；不是为通用存储增加格式或尺寸白名单，不需要逐格式改主流程。能力变化应同步skill版本、manifest/package摘要和契约测试；不要仅靠提示词承诺。

### 2. 二次请求停止位置：模型启动前的网络自检

14:37:55接收二次dispatch，14:37:58资料准备完成；14:40:17 Runtime写入`RECOVERY_REQUIRED`，原因`CHAT_FAILURE: connected  blocked blocked`。同秒服务journal给出`TYPED_INSPECTION_EGRESS_CANARY_FAILED`。该record有preparation但没有engine/runningAt/engineThreadId/终稿字段，见runtime-recovery.json。这不是“模型已经生成但没流式传回”，也不是当前心跳离线。

`typed-inspection-network.mjs:249-251`的负向探针要求：到受控代理可建TCP且收到HTTP403、其他主机端口及直连互联网被阻断。本次读到的是“代理TCP已连接、HTTP响应为空、另外两路被阻断”，故启动失败；`typed-inspection-profile.mjs:355-367`在attach失败后清理尚未启动的请求适配器。不能把空响应直接归因为模型服务故障，也不能将其认定为已证实的隔离绕过。

**尚未证实的下层原因**：本次探针吞掉recv异常并统一为b''，既不记录异常类型，也不区分EOF、超时和响应片段；无法从现有历史证据唯一还原为什么没收到403。本轮只在独立本地代理实例验证相同拒绝分支能返回403，未重放生产请求/探测生产namespace，不能把这个替身检查写成生产网络已修复。后续应在原探针记录分阶段结果及真实socket原因，再对隔离通道定向复现；不取消安全自检、不盲增等待时限。

### 3. 一次启动失败变成永久“正在回话”：恢复与后端状态缺口

- Runtime先保存资料preparation再openAdapter（agent-client.mjs:4765-4769）。此处失败仍按一般CHAT_FAILURE进入恢复。
- `canResumePreEngineInspection`（chat-runtime.mjs:212-218）只覆盖INSPECT且无preparation；本次为带资料的CHAT，无法走该分支。
- `recoverMaterialsChat`（agent-client.mjs:4871-4875）发现没有engineThreadId，只回ACCEPTANCE_UNKNOWN；调度器按recovery_required继续读回，未把“明确尚未启动”与“上游是否接受未知”分开。这种读回不能凭空补出一个从未创建的模型turn。
- Runtime发recovery_required ACK后，API线上`AgentWebSocketHandler:1216-1236`仅对七类确定模型合同错误更新FAILED；本次网络自检码不在`ChatDeliberationService:831-836`集合内，随后只确认dispatch收到，没有推进业务turn状态。14:40:18已见ACK回执。
- 15:20:37北京时间重新认证GET200，仍RUNNING / DISPATCHED / lastDeltaSeq=0，见request-readback.json。前端据此保留忙态、禁用验收，属于下游表现，不应通过强开按钮或验收旧图规避。

最小修复应跨Runtime/API明确“启动前确定失败”的阶段证据与处理契约：匹配原request/turn/dispatch/身份和代际、幂等记录可恢复失败并同步业务状态/事件；只有证明未启动才允许原请求受控恢复，接受未知只能读回、不可盲重执行。保留身份/ACL、锁与重复执行/扣费保护。必须覆盖启动前失败、接受未知、重复ACK、恢复成功和页面重入，不能仅加前端提示或把所有recovery_required一律FAILED。

**当前结论**：尺寸履约缺失、恢复分类错误及后端失败状态未闭合均已定位到线上对应源码；触发本次自检空响应的更下层传输原因尚未唯一确定。最终验收仍未完成，本轮没有代码修复/应用测试/发布。


## 网络自检同症状复现与原因（2026-10-23 15:51 CST）

证据见[复现说明](network-canary-reproduction/README.md)、[汇总](network-canary-reproduction/summary.json)及原始时间序列。直接使用已核对的安装Runtime1.2.6网络模块和真实Codex app-server二进制，独立HOME、私有网络namespace、禁止CONNECT目标及原15秒接收超时；无凭据、无模型调用，不重发517，不改生产模块/防火墙/服务。三路共享诊断Node事件循环，但不是完整生产多Agent turn回放。

| 实验 | 结果 | 最大事件循环停顿 |
| --- | --- | --- |
| 小文件holder单路 | 1/1通过 | 0.296秒 |
| 真实Codex单路 | 1/1通过 | 9.311秒 |
| 真实Codex两路并发 | 2/2通过 | 14.034秒 |
| 真实Codex三路并发 | **2失败、1通过** | **32.112秒** |
| 小文件holder三路并发 | 3/3通过 | 0.722秒 |

**已复现直接原因**：`typed-inspection-network.mjs:8,25`的身份测量同步readFileSync并SHA-256整个可执行文件（本次Codex292,309,256字节）；`_assertOwner:183-200`及bind反复调用，`_nsenter:226-229`在异步命令前后重复校验。各路校验在同一Node主线程串联，`start:203-205`建立的代理HTTP403回调也要等这个线程。三路实验中，失败两路从Python启动到代理CONNECT回调分别31.988/24.143秒，原recv超时15秒已经过期；增强诊断捕获两次`timeout: timed out`，复现原`TYPED_INSPECTION_EGRESS_CANARY_FAILED / connected  blocked blocked`。代理后来仍执行403分支，不代表客户端此前已收到403。TCP可以由内核/slirp完成握手，不能据此推断Node HTTP层及时响应。其余两个禁止通道仍blocked，没有关闭安全策略或发现隔离绕过。

**历史确定性边界**：证明了相同源码/同机可自然触发该机制，未人工注入阻塞；但14:40历史日志没有socket异常、精确并发和事件循环计时，不能断言历史故障的每一步已经唯一还原。三并发是诊断输入，不是已证实历史当时恰有三路启动。旧报告“下层未确定”的边界现缩小为“同症状和机制已实证，历史现场仍缺唯一因果证据”。不能把本轮复现当修复成功或最终验收。

### 最小修复方向（尚未实施）

1. 把重复大文件读取/哈希移出代理所在主事件循环（异步流式/worker测量或代理独立执行域，需按实际实现选定），保留PID/startticks/父子关系、namespace、可执行文件完整性检查及异步前后归属重验证。不能简单删校验、仅按路径缓存摘要或通过加长超时掩盖主线程阻塞；重读的TOCTOU和worker生命周期必须覆盖。
2. 原探针记录连接/发送/接收阶段、timeout/EOF/错误类型和HTTP首行，保留真实传输超时；不能吞成统一空字符串。HTTP状态行读取应按边界累计，不能假定一次recv完整。
3. 同步修复上节明确的Runtime启动前确定失败分类与API业务状态闭合；证明未启动才允许同请求受控恢复，接受未知仍不得重放。不能只修网络后把517永留RUNNING，或直接强开验收按钮。
4. 定向回归保留本次失败fixture，覆盖真实大文件并发、拒绝403、禁止端口/直连、owner丢失/漂移、重复ACK/恢复及页面重入；正式安装与实际业务验收另行执行，依旧按固定app目录和授权部署契约。

诊断子进程已自行清理，生产统一服务readback仍active/running，MainPID1183474未变。本轮未代码修复、未应用发布；事项517二次修改和最终验收仍未标通过。
