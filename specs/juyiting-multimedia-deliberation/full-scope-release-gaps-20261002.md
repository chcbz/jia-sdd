# 完整交付缺口核对（2026-10-02 12:00 Asia/Shanghai）

本记录是交接证据，不替代 TASKS.yaml 的唯一运行台账。

## 本次接受

Client installer `b1e8cceac3e064f6d6759ac8d9c085f21374e8e1`，tree `fa630138c96a77f60bce23edd331f8356cecffd6`，parent `9f78b95baab69609f8954785d9baa2d199f62797` 已 byte-exact FF 到融合特性分支并推送、远端 readback。完整 payload 43 文件、runtime import closure 28 文件，无缺失；每文件摘要和原子 current 切换，保留持久状态。Owner 隔离安装 selector 为 10 PASS、0 FAIL、35 未选中 SKIP，不表述为45项全通过；Main核验原证据摘要，未重复测试。证据见 `integration-evidence-20260928/client-installer-b1e8cce-20261002/`。尚未安装生产。

## 不能缩小的剩余范围

- Client：Owner只读查明V3声明/就绪固定关闭且缺生产poll lane。必须补真实GENERATE_IMAGE/EDIT_IMAGE能力、源revision及重启幂等接线，不以已有inspect或V2生成代替编辑；typedInspectionCaBundlePath须核对normalize。已由原Client Owner继续实现。
- Web：源码确实读取 `VITE_JUYITING_FOLLOWUP_EXECUTE_V3_UI`；下一共同候选须在现有两flag之外启用该编辑UI。尚未修改云端配置。正式构建仅Flow。
- API：生产relay构造器修复候选 `d0b1eee8770bf1e2ab80dfe1d52da9b3303d540d` 已存在，真实迁移/完整Spring接线与最终JAR仍待Owner验证；不以此前SKIP或恢复旧JAR健康冒充通过。
- 安装启用：必须包含workspace及formal artifact两个私有存储、typed inspect、媒体/归档/交互、bootstrap/execution、selected-output finalization/formal delivery、controlled-image V3。只读预检方案不能当作最终发布方案。
- 身份：冻结测试账号既有local/server精确目标及归属。无授权不创建身份、不bind/reprovision、不操作foreign服务；当前403须定位真实原因而非泛化为不可用。
- 产品：AC01–AC22、FD01–FD12仍未完成验收，须真实理解、生成、原图编辑、版本/血缘、预览下载保存、正式交付和完成任务；两种接应均须证据。已有额度授权不是伪造consent/grant的许可，亦不能将CONSENT_REQUIRED当作任务成功。

## Web协作

voice UX Owner `01a0faaf-fa6c-7771-8b57-d50ff13a447a` 独立树负责Composer/VoiceControls/必要Hud及voice test；本任务Web Owner `01a0fa90-6916-75c3-aca8-f5638c515f82` 独占component-behavior loader fixture。共同基线3a4cdf，最终由Main集成后冻结exact SHA，先核查自动Run再触发，保持4403172控制权与deployment hold。不使用历史Reviewer作为门禁。

## 12:24 身份与合同补充

- Runtime Owner只读确认测试账号既有local身份wuyong(binding1)、linchong(binding2) ACTIVE且owner/client/tenant匹配；候选选择wuyong，不新建身份、不并发注册同agentId。安装仍需现存服务custody确认，Main未控制foreign服务。
- server既有binding15和identity为SUSPENDED，hosted-profile缺失。403为有效key后的WebSocket归属拒绝，不是公网匿名入口限制。已向用户询问仅恢复既有身份和必要关联记录的授权；尚未收到明确授权，不DML、不repair、不reprovision、不充值。不能以本次自动goal continuation推导授权。
- Runtime Owner报告12:19 API10018无listener，原恢复Owner正在只读归因，未自动重启。
- API候选9ab62 Owner确认producerRequestRevision由服务端解析、持久化并在执行前对照归档权威复核，不能开放Client伪造输入。Main只读验证resolver确有比较。现有Client wire绑定version/generation/assetRevision/digest，无需盲目新增字段。

## 12:32 运行故障已归因

- Kernel精确证据：2026-10-02 11:57:28（Asia/Shanghai）global OOM killed Java PID3155665/uid987，所属本任务旧API恢复scope；不是正常应用退出。Main已核验Owner证据SHA256SUMS，12:32仍无该PID。
- 先前一次恢复健康是历史事实，不能当作当前可用性。唯一台账MMD-U4已记录environment_resource故障；现有API fixture PIDs3223665/3223691/3223733仍live，Main未控制、取消或重启。
- 原一次canonical start授权已消耗，已向用户请求新的精确一次启动授权，尚未收到明确回复。不得以goal自动继续消息推导授权。
- Client历史service Owner Agent句柄不可用，不代表foreign服务无主；未完成custody交接，不修改或重启该服务。已授权开发和现有额度测试继续执行，生产恢复/身份修复分别等待必要授权。

## 12:59 Client安装静态候选接受

- 融合Client feature现为 `7d1d7eb6e552a1a5c68e106ccc3ec02e815c5579` / tree `81d53d246752199a8614e14184a34e8d9259532f`，包含a7ea生产接线与48文件安装payload候选（28runtime模块）。Owner定向候选16PASS；installer1PASS、40非目标SKIP。
- Main指出并纠正原候选的1/2/15硬编码persona黑名单和预期能力/实测就绪混用；现在区分provider-binding namespace来源证据，模板仅STATIC_VALID/SYNTHETIC_EXPECTED_REGISTRATION，真实捕获比对仅READBACK_MATCH。Main同tree现有依赖环境直接静态调用确认providerBindingEvidenceStatus=UNVERIFIED、fullInstallationReadiness=false。
- endpoint/model/binding/policy/identity/secret仍需冻结，provider局部policy不是正式成果存储、归档、selected-output等完整启用策略。未安装、未重启、未付费调用；不能以静态模板通过解除运行依赖。

## 13:22 定向发现：真实生成配置与双模式目标缺口

Runtime Owner完成现有配置及精确测试账号范围只读枚举，无生产写入/Provider探测/服务操作：

- 现有Responses通路只证明文本/理解路径；已安装环境缺专用controlled-image key，模型目录39项未发现gpt-image/DALL-E名称。这不证明上游永不支持图片，但当前没有已验证生成/编辑endpoint/model、provider binding ID/epoch及operator政策，不得据此宣称生成就绪。
- 精确账号范围9个persona bindings、0个hosted profiles；4条online runtime标记停在11:57:21.951，不能证明当前健康，也不能作为server模式替代目标。没有找到既有ACTIVE hosted/server目标；binding15仍SUSPENDED。双模式验收不得缩成仅本地模式。
- 完整inactive API配置已由Owner生成并明确NOT_READY，缺失值保留MISSING占位，未安装。配置范围包含workspace/formal storage、bootstrap/execution/media、typed INSPECT、archive、selected-output/final delivery及受控图片V3，而非仅单个provider开关。
- 需要Provider/account custodian提供真实生成/编辑绑定及专用秘密安全引用；需要服务custody移交和既有server身份/必要关联配置的明确修复授权。不得将普通开发授权扩展为新租赁、充值、创建新身份或操作foreign服务。
- API工程继续推进：CHECK literal大小写及typed schema先于父表初始化的真实缺陷已形成修复，当前候选3080dc7b/tree0105e845，完整fixture与bootJar结果尚待Owner交付，不宣称通过。

只读发现不改变hold，不构成发布或34项验收证据；最小下一步是补齐真实Provider配置/运行授权，同时完成正在推进的API工程验证。

## 13:32 恢复路径澄清：不将缺hosted_profile误判成必须新增

- Owner补查发现binding15有合法原managed-hosting来源：唯一ACTIVE lease/initial intent、有效entitlement、原managed key及scope一致的既有claim。该路径不依赖agent_hosted_profile；此前没有可直接使用的ACTIVE目标结论仍成立，但恢复不必迁移到另一种profile发布机制。
- 最小待授权动作是fresh CAS恢复现有binding15及同一identity生命周期，随后调用一次已有零账本扣款free reprovision恢复原managed runtime。需要明确production DML、reprovision及managed service custody授权；不新建identity/profile/key、不重绑、不租赁/充值。此时仍未授权、未执行。
- 不应调用要求hosted_profile的通用repair端点来代替原managed-hosting恢复；新建profile属于更广迁移，不在最小方案内。Provider生成/编辑真实绑定仍独立缺失，不因身份修复自动就绪。
- Owner明确允许共享的四份脱敏证据已校验SHA256并保存于integration-evidence-20260928/runtime-recovery-scope-20261002；其余私有配置/凭据指纹未复制。
