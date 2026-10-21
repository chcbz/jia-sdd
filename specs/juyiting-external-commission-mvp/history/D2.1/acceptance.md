# 验收矩阵 D2.1

全部状态：**NOT_RUN**。本轮文档检查不是业务测试，不复用历史图片验收当外单成功。

## 1. 固定夹具

A=下单人，B=两个测试 Agent 的真实归属用户（示例 chcbz 拥有吴用、林冲），C=同平台另一已认证用户（可独立下单，但无权读取A的任务）；另设普通用户名/无关角色名 Agent 和不同tenant/client身份作反例，不把示例名称当授权配置。合成环境与真实账号分别记录，不在文档存凭据。

固定 task/requirement revision、Agent canonicalId/binding、policy/delegation/grant、skill/package/manifest、Provider非秘密描述、source file/version/hash、Runtime installation/session generation、三端commit/tree。线上账号须有真实授权；A/B不可用同一个JWT改body模拟。真实执行沿既有获授权模型连接；不得新增成本确认/支付前置条件。本轮有生产只读页面复核与离线原型诊断，均不计外单业务验收，不实际调用Provider。

## 2. 用例

| ID | 行为 | 必须可观察的结果 |
|---|---|---|
| AC01 | B开启某Agent接外单 | readback只反映该Agent开关/修订；无需客户名单/技能/费用配置，未改变归属/安装/凭据 |
| AC02 | A与C发现同一开放Agent并各自委派 | 两人均可见脱敏摘要并对本人任务下单；A/C任务、资料与会话互不可见 |
| AC03 | A委托自己的任务（有/无附件） | 一个assignment/delegation/grant，taskOwner=A、executor=B；不要求图片输入或serviceCode |
| AC04 | 同key重复、响应丢失后查key | 同一回执，无新事件/执行；同key异payload冲突 |
| AC05 | 不同key并发委托同任务 | 仅一个活动委派；失败事务无半条grant/assignment |
| AC06 | 入单后浏览器关闭、刷新 | 恢复“已接单待指令”；不自动再次下单或假称运行 |
| AC07 | A发任务指令、吴用澄清/执行 | WS投递到B，delta/final/SSE与消息归A；B/C不收到A正文 |
| AC08 | 普通私聊/密议与任务讨论分离 | 无委派的普通密议仍拒绝；委派不能授权其它会话 |
| AC09 | 能力不足推荐与实际工具权限 | 低分/未知能力仍可派单；执行时只能调用真实已有且本单授权的工具，不能伪造READY或读取私人资料 |
| AC10 | B native session领取A任务 | 原真实凭据领取成功；无taskOwner伪装；非目标Agent、C伪冒Runtime或真实跨平台/租户身份拒绝；同平台客户端映射另见AC44 |
| AC11 | 输入固定版本与撤权 | 仅指定fileId/version/hash；其它文件、后续版本、撤销链接拒绝 |
| AC12 | 完整真实图片任务 | 真实Provider完成，输入回执/输出PNG格式、长度/hash、manifest一致，不以文字回答代替图片 |
| AC13 | A下载并正式验收 | 下载字节hash匹配，现有finalization链完成且delegation COMPLETED；运行完成与验收完成不同 |
| AC14 | B/C调用A下载/会话/资料API | 拒绝；B仅能看精简接单列表和自己政策 |
| AC15 | 相同意图重复与多个新合法动作 | 相同action/effect重投无重复副作用；不同合法动作可在同委派下形成多个execution，不设整单一次限制 |
| AC16 | 接单后B关闭开关 | 只阻止新外单；存量外单和本人任务继续，不杀共享Runtime；无移除客户白名单功能 |
| AC17 | 政策/任务/需求/资料版本竞争 | admission精确CAS冲突，不能用旧快照成功 |
| AC18 | effect/start前A取消或B撤回 | grant/委派撤销；没有新Provider副作用 |
| AC19 | effect/start与取消并发 | 按持久顺序决定；已开始可保留真实成本/未知结果；不声称必定中止 |
| AC20 | 撤销后迟到回执/文件 | 仅原已准入效果可受限归档审计；不恢复输入读取/新效果/任务成功 |
| AC21 | 断连、重连、重复投递、旧session回报 | 现行fence生效；只恢复同一执行；旧fence不得写新结果 |
| AC22 | Provider成功回包丢失 | RESULT_UNKNOWN保留并可诊断；无自动第二次调用 |
| AC23 | stage成功后commit响应丢失 | 按原execution/manifest恢复一份结果，正式交付不重复 |
| AC24 | Agent重绑、技能/Provider配置变化 | 重绑不能继承旧委派；已冻结动作不偷换配置，新合法动作可解析当前配置，不以成本变化拒绝接单 |
| AC25 | A/C使用相同会话ID/线程污染尝试 | 完整scope/task/delegation/generation隔离；B私人上下文不进入任务 |
| AC26 | 前端账号切换、迟到GET/SSE/下载 | 旧响应无越权UI写入；重新登录按真实身份重读 |
| AC27 | Web PC与移动端统一选择承办 | 我的+他人已开放Agent统一列表；低分可选、默认ALL、分页可达、不误引导至他人管理或普通密议 |
| AC28 | 原同主任务/技能/资料/安装管理 | 原功能正常，原ACL/锁/幂等/取消回归均保留 |
| AC29 | 数据库迁移与恢复演练 | 新政策默认关；历史终态可读；非终态处理有明确记录；不重写历史snapshot/hash |
| AC30 | 取消与正式验收并发 | 当前taskVersion/assignment决定；取消任务不会被迟到完成复活 |
| AC31 | 费用与成本分离 | 无报价/余额/冻结/扣费/费用确认；真实模型成本只展示，未知为null/UNKNOWN，不影响执行/交付/验收，非交付价格 |
| AC32 | 完整受测/发布证据 | API/Web同Run制品摘要与安装摘要、Runtime固定制品、实际线上三端版本相符 |
| AC33 | chcbz分别切换吴用/林冲的开关 | 关/关、开/关、关/开、开/开四种组合均正确；UI/readback/实际入单按目标Agent独立判断 |
| AC34 | 修改吴用开关，林冲有活动单 | 林冲开关revision/能力配置/活动委派均不变，共享Runtime不被重启或停止 |
| AC35 | 同用户同时修改两个Agent政策 | 各自expectedRevision/CAS/幂等回执正确；请求不能因同用户而覆盖另一Agent |
| AC36 | 非chcbz用户和非水浒角色名Agent | 同等归属权限下功能一致；源码/SQL/前端无用户名、角色名、personaCode或固定试点ID白名单 |
| AC37 | Agent改显示名、同名不同绑定、他人Agent | 改名不影响政策；同名不共享政策；B不能修改不属于自己的Agent，重绑不继承旧开通意愿 |
| AC38 | 开关、推荐、派单与运行分离 | 离线/忙碌/缺技能/成本未知可开启和委派；低分不拒单；运行等待或真实工具错误如实展示，关闭无需Provider在线 |
| AC39 | 非图片任务完整交付 | 无附件文本、非图片文件/结构化结果沿原真实成果/验收链完成；不被IMAGE_EDIT或输入张数限制 |
| AC40 | 同任务多步与返工 | 多个真实动作合法执行；需求/资料修订后授权快照更新；历史不覆盖、旧回执不写新修订 |
| AC41 | 推荐服务不可用/能力未知 | 返回全部有权限候选并明确推荐不可用，手动选择仍成功，不伪造匹配分数 |
| AC42 | 本人Agent关闭外单且能力不匹配 | 仍可承办本人任务；他人新单拒绝；本人也不受validateAbility硬门槛 |
| AC43 | 模型用量/成本数据缺失或估算 | 不记为0、不误标实际、不重复累计、不直接作为交付费用；获取失败不阻断结果/验收 |
| AC44 | 同平台不同登录客户端 | 按可信平台域映射判断，而非客户端名称/客户名单排除；真实跨平台/租户数据仍隔离 |
| AC45 | 失败/未发指令/换承办 | 无自动过期或伪完成；可按原状态继续/取消/换承办；旧执行回报不能复活旧委派或覆盖新承办 |
| AC46 | 原D1限制字段不进入实现 | 开关写入只有state/expectedRevision；外单无allowedRequesterIds/serviceCode/skillSelection/cost门禁；拒绝旧提案字段，不保留双合同 |

| AC47 | 关闭政策后从任务列表/刷新直接进入原外单 | assignedTarget独立于新单候选/本人名册；可继续本单，仍不能私人密议或管理Agent |
| AC48 | 本人Agent离线、忙碌、低推荐/能力未知 | 真实普通单目标入口可先指派并等待；不误走funded或自动重派 |
| AC49 | 外单接单与准备会话重放 | 一个委派/授权/准备回执；首条指令未发送时无CHAT dispatch/Provider，PENDING/READY/FAILED如实读回 |
| AC50 | B的dispatch ACK、receipt、invalid outcome、stop ACK | 经持久关联回到A原请求；重放不重复，伪dispatch/错误binding/旧fence不能越权 |
| AC51 | 任务已有多个文件但委托inputRefs为空或子集 | 不隐式全授权；仅明确固定版本可读，后续新增不自动进旧快照 |
| AC52 | 同平台不同OAuth client主体 | task与executor client分别持久/使用；可信映射通过，未知映射不得伪放行；不以同client覆盖全平台验收 |
| AC53 | B撤回与A取消整单区别 | B只能结束服务关系，不能代A取消任务；原需求/成果保留、actions与受限恢复真实 |
| AC54 | 换承办时旧final/文件/Unknown效果 | 新assignment和会话授权generation推进；旧回包只归旧审计，不转发前承办完整thread、不自动重做未知效果 |
| AC55 | 开关PUT结果未知、另一标签页更新 | 查原key回执而非猜最新state；同key重放、异body冲突、expectedRevision冲突可恢复 |
| AC56 | 开关加载失败/切换Agent或账号后迟到响应 | 不伪装关闭或覆盖另一Agent；仅当前行pending，四组合独立，焦点与移动详情正常 |
| AC57 | 候选无本人但有他人、空态、推荐失败、分页失效 | 合法候选可达；不静默更换所选目标，提供方仅公开昵称/状态，不泄露私有目录 |
| AC58 | 首条指令已受理而执行方离线，刷新/重连 | 与“尚未发指令”区分；原request/key恢复，不重新入单或自动产生第二条指令 |

## 3. 验证层级与已有入口

1. 静态/合同：DTO字段、wire字符串版本、schema/digest、前端能力与后端授权语义一致。先为现有失败链写回归。
2. Agent 服务与真实隔离数据库：参考现有 `AgentTaskExecutionGrant*Test`、`TaskSkillPolicyServiceTest`、`SkillExecutionServiceTest`、`PersonalWorkspaceExecution*Test`、mapper contract、取消和正式交付测试；新增委派并发/ACL场景，不删旧用例。
3. Chat：现有 `ChatDeliberationOutboxCommitTest`、`AgentWebSocketRuntimeAuthenticationTest`、`AgentWebSocketTypedDeliberationTest`、`ChatSelectedOutputFinalizationServiceTest`；新增双Owner真实WS/SSE消息去向测试。
4. Runtime：在所属仓现有node测试集扩展 message-wire、skill conversation/store/provider、thread key、重连恢复和受限议事；测试不用真实密钥/付费Provider。
5. 浏览器：复用既有组件与整站入口；合成API组件检查不替代真实OAuth/双账号验收。执行历史若受影响才使用 `/home/isp/wsps/cyf/ops/orchestration/execution_history_check.py` 对应固定任务/源码。
6. 正式：API Flow5260799、Web Flow4403172，保留validateLayering与fresh制品；Runtime依所属仓现行控制面。无本机生产构建替代。
7. 在线：按A/B/C真实授权账号跑完整外单与关键越权反例；无测试账号凭据或合法运行连接则标NOT_RUN/真实阻塞；不新增费用审批门禁，不能改数据库绕过。

具体Gradle/Node selector由实施Owner读取当前build.gradle/package配置后固定，不在设计阶段编造可执行命令或执行成功数量。

## 4. 证据与完成标准

证据放本特性 `evidence/`（已有原型及生产只读复核批次，不是业务验收），按候选/批次留：baseline、测试摘要/原始报告路径、scope脱敏映射、事件关联、输入输出hash、Flow Run、制品与安装摘要、浏览器结果。密钥/JWT不入仓；失败证据不重标成功。

通过条件：范围内用例完成且无未解释身份/数据/效果风险，真实AC03/07/10/12/13/14连成一条闭环，并完成非图片、多动作和独立开关AC33/39/40/42。API health、单账号成功、目录READY或代码已合并均不能单独判定外单完成。
