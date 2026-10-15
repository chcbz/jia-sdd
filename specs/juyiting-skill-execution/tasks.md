# 直接实施任务（方案已在本轮确定）

> 2026-10-16收口：下方分包与日期状态是历史执行计划，不作为当前待办。图片基础链已按integration.yaml所列三端版本上线，修改/下载通过，OCR两次错误，整体仍PARTIAL；不把所有I包或A01–A34重标完成。当前证据见acceptance.md末节，稳定实现见整体SDD的image-skill-contract章节。


日期：2026-10-13。设计/代码定位工作已完成，不再列为未来任务。唯一本聊天 Owner 连续执行；当前合同为design-se2.md；SE-1已作历史保留。以下是本特性工作包编号，不冒充已登记/运行的 orchestration ledger ID。实际开工沿现有 handoff/ledger 工作流绑定真实任务与固定源码，不新增台账系统。

每项含实现及最小定向自检，预计20～30分钟主动工作；是切片粒度而非硬 timeout/完工保证。等待单列，不取消他人流程。超出时只拆剩余具体实现，不重开“设计阶段”。依赖含共享协议就用 design-se2.md，不重复制定。

| ID | 具体代码任务 | 最小交付/自检 | 依赖 | 分钟 |
|---|---|---|---|---|
| I01 | Java SkillManifestCodec：可执行扩展字段/路径/身份 | 正常/未知字段/路径逃逸fixture | 已定详设 | 25 |
| I02 | Java标准schema库封装与固定方言 | 类型、required、额外字段、safe integer负例 | I01 | 25 |
| I03 | JS标准schema库封装与同组fixtures | 与Java接受/拒绝集合一致 | I01 | 25 |
| I04 | SkillPackages接不可变包存储，seed仅内置 | 新包不依赖classpath；包hash仍核验 | I01 | 25 |
| I05 | 安装侧manifest摘要绑定 | 普通包不强制manifest；执行包摘要一致，篡改失败 | I03,I04 | 30 |
| I06 | agent_skill_execution DDL与Entity/Mapper | scope唯一键、CAS、空值约束测试 | 已定详设 | 30 |
| I07 | 协议4 PWE CHECK及schema detector | 历史不变；4含RESULT_COMMITTED、假grant拒绝 | I06 | 30 |
| I08 | SkillCapabilityLookup接口与session registry | 会话切换旧目录失效 | I05 | 25 |
| I09 | RT skill-registry就绪与摘要缓存 | 缺工具/缺绑定不会READY | I05 | 25 |
| I10 | Runtime注册消息接线 | 可信session目录报送，非自报权限 | I08,I09 | 25 |
| I11 | ChatActionCapabilityService目录投影 | 多技能、带资料文本能力、缺依赖原因 | I08,I10 | 25 |
| I12 | Java action-v4 codec/validator | 无法伪造skill/version/参数 | I01,I02 | 30 |
| I13 | RT action-v4 schema/instructions/validator | 规划回合不直接执行；同fixture | I03,I12 | 25 |
| I14 | discussion-v2有效资料选择 | TASK_DEFAULT/EXPLICIT/NONE/澄清继承 | 已定详设 | 30 |
| I15 | 通用资料resolver | 上传图/会话成果各自ACL与来源验证 | I14,I52 | 30 |
| I16 | EXECUTE_SKILL baseline与旧任务升级 | 当前Owner/assignment下新版本；旧key不重跑 | I07 | 30 |
| I17 | createSkillConversation与快照落库 | 主/附属/源快照原子提交 | I06,I07,I15,I16 | 30 |
| I18 | ChatActionExecutionService统一接纳 | child/step/link/admission/outbox原子性 | I11,I12,I17 | 30 |
| I19 | 通用command/inputs映射与队列筛选 | QUEUED但UNKNOWN不再执行 | I17 | 30 |
| I20 | effect start/result接口与CAS | 并发一个NEW，重放不NEW | I06,I19 | 30 |
| I21 | resume与原生路由白名单 | 旧session拒绝；新session不能重发未知副作用 | I20 | 30 |
| I22 | RT skill-executor与runner注册表 | 同入口支持多skill，无skill名称switch，runner为native-model | I09,I19 | 25 |
| I23 | RT effect恢复与持久结果留存 | 登记/发出/回执丢失的故障注入 | I20,I21,I22 | 30 |
| I24 | 提取图片HTTP runner | 复用编解码；无consent；binding与出口保留 | I22,I23 | 30 |
| I25 | 封装image-generate/image-edit包 | 参数/资料/费用说明；不真实付费调用 | I04,I24 | 25 |
| I26 | 源text-file接通native-model runner | 保留源HEAD实现；可带资料、无图片分支 | I22 | 30 |
| I27 | local-script runner隔离 | argv不拼shell、无token/env泄漏、输入只读 | I22 | 30 |
| I28 | 数据/文件统一result commit及MIME策略 | 零文件真完成；文件hash验证，unknown MIME安全下载 | I07,I17,I23 | 30 |
| I29 | 定向结果projector与COMPLETE投影 | 数据不造asset；文件幂等，登记失败不重跑 | I18,I28 | 30 |
| I30 | ChatActionFinalService进度去特例 | 读真实childId/phase，不按技能猜 | I18,I29 | 25 |
| I31 | Web启动回执schema2 | 新skill不影响议事；未知平台协议拒绝 | I16 | 25 |
| I32 | Web discussion-v2/资料范围 | 一次任务资料后续可用，NONE明确 | I14,I15 | 25 |
| I33 | Web action-v4/通用进度 | 对话可恢复，不将归档中报完成 | I12,I30 | 30 |
| I34 | Web移除费用审批，展示costInfo | 费用信息独立更新不影响就绪；包购买保持 | I11,I33,I55 | 25 |
| I35 | Web成果定向读取/通用下载 | 不等待全历史索引，无预览可下载 | I29,I33 | 30 |
| I36 | skill-bindings加载与候选转换工具 | 输出候选/diff，不改在线profile；保密readback | I09,I24 | 30 |
| I37 | PDF中文字体制品与就绪接入 | 复用现有reportlab；字体许可/hash与中文fixture | I27 | 25 |
| I38 | pdf-export技能脚本与包 | 内容/文件可读fixture，统一结果协议 | I04,I27,I37 | 30 |
| I39 | XLSX参数与工具就绪接入 | 复用openpyxl；值类型/公式安全定向测试 | I27 | 25 |
| I40 | xlsx-export技能脚本与包 | 结构/数据fixture，核心业务文件零改动 | I04,I27,I39 | 30 |
| I41 | 移除旧图片/费用写入口及死分支 | 新写入口单轨；审计读取保持；无安全校验丢失 | I18,I24,I34 | 30 |
| I42 | 后端HTTP/事务定向回归执行 | 真实身份/DB/rollback；复用Gradle编排入口 | I20,I21,I28,I29 | 30 |
| I43 | Runtime断线/恢复/取消回归执行 | 费用不参与；未知结果不盲重发 | I23,I24,I27 | 30 |
| I44 | 浏览器候选场景诊断 | 新上传→识别→修改→下载；非正式前端证据 | I25,I32,I35,I56 | 30 |
| I45 | 提交前端正式Flow验证 | 精确commit和同Run制品；等待另记 | I31～I35,I41 | 20 |
| I46 | 后端固定源码正式验证/构建 | 先读build.gradle、串行orchestrator、validateLayering | I42 | 25 |
| I47 | Runtime版本化制品与配置候选校验 | 含源码/二进制/manifest摘要；未安装不说上线 | I36,I40,I43,I53,I54,I56 | 25 |
| I48 | 发布批次与恢复包准备 | 绑定同批制品、锁、备份、在途执行状态 | I45～I47 | 20 |
| I49 | 协调窗口执行切换 | 不抢停；新旧写入口不同时开放 | I48 | 25 |
| I50 | 线上真实验收与证据归档 | 输入/输出字节证据、3种产物、真实错误状态 | I49 | 30 |
| I51 | 既有指南收口与旧配置readback | 新配置生效、旧写入口关闭、未通过项如实保留 | I50 | 20 |

| I52 | 数据结果引用selector与来源校验 | EXECUTION_RESULT已提交/摘要/ACL，拒绝自引用 | I12,I14 | 25 |
| I53 | 普通说明技能与可执行包共存回归 | 不强制manifest、不伪造就绪、固定版本在途保留 | I05,I08 | 25 |
| I54 | 维护方包发布和seed指针收敛 | 原子包存储+既有版本表；新包不重发应用，旧seed不回退指针 | I04,I05 | 30 |
| I55 | 费用说明独立覆盖与快照 | informationRevision不影响bindingRevision；报价/实返分开 | I11,I36 | 20 |
| I56 | 公共资料载体/分析技能接线 | 去顶层INSPECT；原生可读不加回合，分析可返回零文件 | I13,I15,I22 | 30 |

正式流水线、下载、测试和部署可能超出上述主动操作分钟，单独记录，不以30分钟终止。I44/I50中真实外部调用属于实际验收，不在仅设计授权下提前执行。价格展示不额外弹出平台审批，基础运维/身份操作边界仍遵守项目规则。

## 2026-10-13 实际实施状态（20:48更新）

| 包 | 状态 | 证据边界 |
|---|---|---|
| I01–I03 | RELEASED 基础切片 | API1.14.12/0833bfe与Runtime1.0.3/6325af1；release-20261013/summary.json，不是完整技能执行验收 |
| I04 | SOURCE+TARGETED_PASS，develop已push，NOT_RELEASED | 281ee445；112 tests、layering；i04-proof.json；维护发布入口属于I54 |
| I05 | SOURCE+TARGETED_PASS，develop已push；API新增绑定NOT_RELEASED | b62d6e96；119 tests、layering；i05-proof.json；Runtime基础已在1.0.3发布 |
| I06 | SOURCE+TARGETED_PASS，develop已push，NOT_RELEASED | 7b0e2504；130 tests（11项新SQL）、layering；i06-proof.json；无生产DDL |
| I08 | SOURCE+TARGETED_PASS，develop已push，NOT_RELEASED | 16fe9f92；11 tests（8项新registry）、layering；i08-proof.json；注册消息接线I10尚未实现 |
| I09 | SOURCE+TARGETED_PASS，develop已push，NOT_RELEASED | faa5005；262 tests；i09-proof.json；具体runner/binding加载尚未实现 |
| I10 | SOURCE+TARGETED_PASS，双端develop已push，NOT_RELEASED | API02faad300b：46 tests+layering；Runtimeb79558e：416 tests；i10-proof.json；不是安装/任务授权证明 |
| I11 | PARTIAL：I11a SOURCE+TARGETED_PASS，develop已push，NOT_RELEASED；I11b未完成 | 2fb221ae；171 tests+layering；i11a-proof.json；仅安装/Runtime观察，不是任务可调用目录/HTTP/执行授权 |
| 其余包 | NOT_STARTED | 不因基础切片上线而标完整功能完成 |

当前真实ledger任务JYT-SKILL-SE2-20261013仍由skill_se2_owner连续实施。现网API仍1.14.12/0833bfe，完整上传→识图→编辑场景NOT_RUN；未发布无关Web，未调用付费Provider。


## 2026-10-14 五小时基础能力实际结果（不重标完成）

窗口截止2026-10-14 02:14:52。**整体未完成**：源码候选/Runtime制品准备已交付，正式API完整批次因validator依赖约束失败；前端Flow209测试/构建/扫描通过但未部署。迁移、Runtime生产激活、四包合法安装及新图片UI闭环均NOT_RUN。主任务已按原orchestrator归因并deferred，不继续后台自动安装。下一次工作从handoff末节5项接续；保留既有I项/历史证据，不把准备与子集PASS标为正式完成。
