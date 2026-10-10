# GSS-REJOIN-20261010：公孙胜除名下山并重新入伙

- 2026-10-10 Asia/Shanghai，Owner Main；用户在六任务取消完成后明确“好，继续下一步”。范围仅当前账号的公孙胜（personaCode gongsunsheng，原agentId agt_510b7fea20564b52bc70b3a08d2c6c4f），走已有业务API/前端流程；不改其他角色/任务，不操作其他聊天进程，不确认新租金/付款。
- 既有六任务取消证据见GSS-CANCEL-20261010；本轮仍先fresh读取，不靠历史成功代替当前前置。只读源码API develop `36d9e5452ab8beb64b97e5570da6ede10ec38797`，Web HEAD `17ecf1c0b581cab1456acff4db097a6a4d335e3d`；07:46安装record仍API1.14.2/相同commit。此为本地源码与线上记录核对，不宣称新fetch远端。
- 已读AGENTS、ops/orchestration/README与既有handoff，复用原本线程浏览器driver，只建立新owned临时Chromium，不使用/关闭用户in-app浏览器。证据 `/var/tmp/cyf-gongsun-rejoin-20261010-G2uKp5`。
- 非目标：不直接改DB，不绕绑定/租约/授权，不为重入伙强杀共享Runtime，不选择免费local来伪报server入伙成功，不以202或付款预留冒充Runtime就绪。
- 验收：除名前后catalog/所属账号/任务状态；正常DELETE成功后确认bound=false；随后原UI重新入伙，若需新租约，最多读取真实报价，停在确认付款前。当前状态：读取前置，尚未除名或重新绑定。

## 2026-10-10 07:50 前置实测：发现既有付费租约，除名前等待用户选择
- 六任务fresh GET仍cancelled/v2；公孙胜catalog仍boundToMe=true、offline、无currentTask。
- 原agent hosting-lease真实GET200：managed=true，lease `hrl_31485bed-d6d5-4f15-be31-b3511aeafe95`，ACTIVE/v2，binding15；已付1000 SILVER/30固定天，租期2026-09-26 01:37:21至2026-10-26 01:37:21（北京时间），admission=ALLOWED。UI同步显示“免费重整接应（不续租，不延长到期日）”按钮可用，钱包可用与预留均0。
- 同部署源码核对：HostingRentApplicationService.lookup/reprovision均要求当前active binding；AgentHostedBindingTransaction.suspendDatabase会暂停binding/identity并清除runtime绑定，未提供剩余租金退还/迁移。INITIAL的currentBinding仅查active，除名后会生成新canonical ID/新初租报价。故旧租约仍有效时先除名会失去原绑定的免费重整路径，不能假定重新入伙自动承接剩余租期。
- 因新增明确成本后果，在破坏性除名前停下询问用户是否改为现有租约免费重整；未擅自替换用户指定步骤。尚未DELETE除名、未POST bind/REPROVISION、未获取新租金报价/确认/扣款，不把UI打开租约面板当作重整成功。
- 证据：persona-before.json、six-tasks-current-before.json、lease-before.json、existing-lease-ui.json，均在本轮临时目录。下一动作：用户选择是否保留现有租约免费重整；如仍明确要求除名，按正常DELETE后再预览新租约，付款仍须另确认。

## 2026-10-10 07:56 用户明确要求两场景顺序验收
- 用户在已获知旧租约不自动继承、新入伙走付费流程后明确：“两种场景都验一下，先跑一遍除名后重新入伙，然后再跑一遍重整接应。”本轮按此顺序推进，不擅自改为只做旧租约重整。
- 新证据目录 `/var/tmp/cyf-gss-two-scenarios-20261010-Trb3FE`，复用原driver，Main独占本轮owned Chromium。原07:50无变更结论保留。
- 验收分别记录除名、重新绑定受理、租约与真实服务就绪、免费重整受理与完成。确认既有接口/报价/余额，不进行外部充值、人工增发资金、直接SQL补状态或重启共享Runtime；若遇真实业务阻塞先定位，不伪报两场景通过。

## 2026-10-10 08:01 两场景实测结果：第一场景除名通过，重入伙被资金前置阻塞
- 正常UI点击“除名下山”，唯一DELETE `/agent/personas/gongsunsheng/bind` HTTP200；fresh catalog bound=false / boundToMe=false / canBind=true / agentId=null，UI变“请上梁山”。六个cancelled/v2任务除名后owner GET仍200，未删除历史。
- 随后UI“请上梁山→山寨安顿”自动获取INITIAL报价并尝试迎新金（不是本轮另发POST bind）。真实报价 `hrq_2e294751-ddfb-40e3-84e9-0806750a0c80`，预拟agent `agt_631bda37e4684ae897f077335ca24b53`，1000 SILVER/2592000秒，未确认。报价中的预拟agent不代表绑定或Runtime已创建。
- 钱包GET：availableMicro=0、heldMicro=0、version8；UI确认付款按钮disabled，提示“迎新安顿金到账后余额仍不足，未提交租金”。根因已核：GET ledger只有四条旧流水（nextCursor=null），一次性hosting-welcome-v1迎新金 `etx_c5030036-d455-4483-8178-4e76e5438323` 在2026-09-26已发1000 SILVER，后续退款/再预留形成当前旧租约且余额为0。本次迎新POST200只是既有一次性活动幂等回执，不增发余额；源码按scope/actor/campaign固定幂等键。
- **未发送任何新POST persona bind/REPROVISION；未新扣款、未外部充值、未手工改余额。** 第二场景依赖第一场景新绑定/租约完成，因此尚未执行，不能报告两场景通过。当前公孙胜确实已除名，尚未重新入伙。
- 不调用 `/economy/preview/issuances` 绕过：当前源码要求显式dev/test且排除prod/production，不是生产补款入口；钱袋UI目前只读余额/流水。需确定正常测试资金补充办法，缺口1000 SILVER，而不是盲重试迎新金或免费local伪成功。
- 证据均在本轮目录：catalog-before/after-unbind、old-lease-before、rejoin-quote-and-grant-ui、wallet/ledger-after-quote、final-network、six-tasks-after-unbind、summary.json。已清除浏览器内未确认报价（未付款）并关闭本轮owned Chromium。下一动作待用户决定生产测试资金来源或资金入口缺口处理方案，再继续同顺序验收。

## 2026-10-10 08:24 新授权补款，资金前置解除（场景仍未执行）
- 用户新授权直接数据库向所有用户各补2000，并要求分析后续新用户默认2000；该授权覆盖前文“不直接DB增发”的旧边界，本轮无应用部署。
- 310条用户记录中309条有效身份已各+2000，共618000 SILVER，309笔完整交易/618条平衡分录；id94缺jiacn未发，未擅自修身份。批次ops-all-users-plus2000-20261010。
- 2026-10-10 08:21:10.528已提交；账本/余额及交易摘要核对差异0。正常登录后线上钱包GET200，chcbz availableMicro=2000000000、heldMicro=0、version9；原迎新1000规则未变。
- 证据 `/var/tmp/cyf-all-users-plus2000-20261010-GtEkIc`；分析文档 `/home/isp/wsps/cyf/docs/implementation/NEW-USER-2000-GRANT-ANALYSIS-20261010.md`。本轮owned Chromium已关闭，无绑定/租金确认/免费重整请求。
- 下一动作：在原两场景授权下重新获取公孙胜当前报价，按先重入伙、再免费重整接续；旧过期报价不能复用。不因资金到账重标两场景通过。

## 2026-10-10 08:42 用户要求先完成公孙胜两场景
- 最新明确指令：“那先完成公孙胜的流程，再继续讨论新用户资金功能。”连续接续已授权的除名→付费重新入伙→免费重整验收；不再次除名、不修改新用户资金逻辑、不再批量补款。唯一Owner Main，证据 `/var/tmp/cyf-gss-rejoin-funded-20261010-yBc9aH`，复用既有owned browser driver。
- 已重读项目规则、验证工具索引、runbook和本handoff；本地API/Web HEAD仍36d9e545/17ecf1c0。08:44只读生产安装record与实体JAR SHA仍匹配1.14.2原批次；本轮未fetch远端，不将该检查说成最新远端源码。
- fresh正常登录钱包HTTP200可用2000/预留0/version9。只操作chcbz的gongsunsheng；核对新报价1000/30天后经既有UI确认一次，跟踪租约/intent与Agent注册；之后既有免费REPROVISION跟踪至真实就绪，并核对不扣款/不延长租期。若受理结果未知，先回读原请求，不创建第二张初租单。

## 2026-10-10 08:50 实测真实阻塞：托管路径尚未接入统一Runtime

### 本轮实际操作及财务状态
- 唯一新报价POST200：hrq_83b09f5a-3072-4ab9-a165-150e811ff434，1000 SILVER/30固定天，目标公孙胜新canonical ID `agt_5e283360939b4ddead4e69859355db08`。正常UI仅确认一次，POST `/agent/personas/gongsunsheng/bind` HTTP202，未直接SQL写业务状态。
- 08:45:41预留成功：交易 `etx_7977c18a-cc8f-4051-ab5f-bb2bb043d463`；新binding16 ACTIVE；租约 `hrl_0fa0c7b0-bf62-4524-88fa-bed7459b795d` PROVISIONING/v1；intent `hri_063977b3-1143-4d9b-8703-fbd0e56b466a` PROVISIONING_UNKNOWN/v2。
- fresh最终GET：钱包可用1000、预留1000、version11；仅一笔初租预留，尚未capture、未退款、起租/到期均空。catalog boundToMe=true但offline，不把绑定或202当成安顿成功。
- 六任务417/421/424/429/431/433 fresh GET均cancelled/v2。未复活旧任务，未对卢俊义进行业务测试，未创建事项。
- **两场景未全部完成**：既有除名PASS，本轮重新入伙仅到受理/预留；第二场景免费重整尚不符合ACTIVE租约前提，未发送REPROVISION、不强行绕过前提。

### 已确认根因，不继续盲等/重复付款
- 生产API1.14.2的 `application.properties:28` 仍配置旧 `/run/cyf-agent-host/managed-host.sock`。08:48核对本机及API进程mount视图均无该路径；socket监听查询也没有该listener。
- API `UnixManagedHostingProvisioner.java:39–54,108起` 仍采用旧API-key credential及observe/ensure UDS协议；`ManagedHostingCredentials.java:118–162` 已给本intent配置managed API key（只核对存在，不输出凭据）。不存在的socket阻断后续真实provision。
- Runtime当前commit `2ce6fedf34832048e248fde3e07222f5ed867b7a` 明确移除了旧managed-host.mjs；`conf/codex-ws-agent/test/managed-host.test.mjs:13起` 有退役回归；`conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs:205起` 明确禁止携带旧broker。不是单纯“服务掉线后重启旧服务”能修复。
- 当前 `unified.host.json` 仅吴用、林冲、卢俊义3个profile，公孙胜没有RuntimeV1 installation（DB count0），没有host/instance/session generation。`agent_runtime`有1条offline占位行，lastSeenAt等于绑定初始化时间；不能把该行计数或lastSeenAt当真实注册/心跳证据。
- 初租入口 `HostingRentApplicationService.java:296–298` 调用availableFor；现实现 `UnixManagedHostingProvisioner.java:39–42` 仅验证配置/凭据服务/scope，不验证broker运行就绪。因此入口仍接受资金预留，而后台永远无法从缺失broker取得就绪证明。
- 该缺口与之前UR06“付费托管恢复移出必做范围”（`UR06_REQUIRED_RUNTIME_CLOSEOUT_DESIGN_20261009.md:33`）一致：统一三角色的新任务验收并不证明招贤令付费新入伙已接通。

### 完成本需求需要的修复范围（尚未实现/发布）
1. 用原RuntimeV1 installation/enrollment/session身份替换托管旧API-key broker链，初租intent映射真实installation；保留原tenant/client/owner/canonical/binding校验。不能恢复旧broker、单独起第四Runtime、手工写ACTIVE或直接免租冒充本场景。
2. 让统一Runtime可接收公孙胜配置并返回精确关联intent/lease/operation的真实注册及能力就绪证明；新入伙与免费重整共用同一Runtime主体生命周期。现CLI只加载启动配置，不能假称写一份profile就会自动生效。是否动态配置或受控共享服务重载需在详设中冻结，不能为本账号流程擅自重启他人运行上下文。
3. 修正付费受理前的provisioner可用性判断：通道不可用时明确拒绝，避免继续产生“已预留但不能安装”的新订单；现已预留的原intent由对账器在修复后续办，不生成第二张初租单。
4. 按原本地后端/版本化Runtime发布规则交付；续验**同一**新binding16/lease/intent，ACTIVE后再发一次免费重整，核对同lease、paidThrough不变、金额0及真实就绪。

- 证据：本轮目录 `summary.json`、`hosting-wiring-diagnostic.json`、`pending-db-readback.jsonl`、`runtime-row-readback.json`、`lease-final.json`、`wallet-final.json`、`ledger-final.json`、`network-final.json`、`pending-final-ui.json/png`。网络仅1次公孙胜报价POST及1次bind POST；本轮owned Chromium已关闭。未修改应用/Runtime源码、服务配置、生产状态或原租约，不存在已经派出或后台继续开发的子Agent。新用户资金功能继续搁置。

## 2026-10-10 09:02 开发窗口（用户：2小时，单项半小时内）

- 目标窗口09:02—11:02 CST，开发/定向自测/集成与发布/生产验收分开记录。未新增生产重启授权；资金功能不在范围。
- 09:07只读ls-remote核对两组件origin/develop与本地相同：API36d9e5452ab8beb64b97e5570da6ede10ec38797/tree28a9350c3dcf9c1a3179720250d2bef9f07fd42e；Runtime2ce6fedf34832048e248fde3e07222f5ed867b7a/tree1d610486cbbe14ff410ee85e6ba1ee6e7c8e6163。两组件tracked clean，未fetch/改远端。
- API唯一任务GSS-HOSTING-API-20261010，worktree /home/isp/wsps/worktrees/gss-hosting-api-20261010，branch codex/gss-hosting-api-20261010；owns本API仓相关实现/测试/迁移。
- Runtime唯一任务GSS-HOSTING-RUNTIME-20261010，worktree /home/isp/wsps/worktrees/gss-hosting-runtime-20261010，branch codex/gss-hosting-runtime-20261010；owns本Runtime仓相关实现/测试/模板/installer。
- Main只写项目文档/控制面、冻结合同、核查集成和发布准备，不与Owner重复源码开发。协议见 ../GSS-HOSTING-CONTROL-CONTRACT-20261010.md。
- 切片：合同10m；并行API字段/幂等25m、Runtime动态生命周期25m；并行API适配/事务外探测25m、Runtime控制/持久化25m；两端各定向回归25m；联调集成25m；机动10m。单片完成即连续下一片，不逐片等待批准。最早验证为各自纯协议/生命周期定向测试；Gradle经原串行入口。
- 资源观测：开工查询内存available1883MiB、swap已用1014MiB、文件系统余744MiB。只记录不新增无依据门禁；不删除别人文件/缓存/证据。实际空间失败再精确归因。
- 派单/接收确认待填；本条不是派单完成或源码已完成证据。

### 派发与接收回读（2026-10-10 09:12 CST）
- API：Knuth，Agent `01a12359-97db-7621-9088-0ac06b21dc18`，critical_worker/Sol；ledger Owner alias `gss_api_sol_20261010`，已claim并明确回读规则/合同；worktree已有字段、mapper、installation ensure与迁移源改动，尚未测试/提交。
- Runtime：Shannon，Agent `01a12359-f327-7db3-968f-66ca8ca2b18e`，critical_worker/Sol；ledger Owner alias `gss_runtime_sol_20261010`，已claim并明确回读规则/合同；worktree已有动态生命周期/adapter/engine源改动，尚未测试/提交。
- 共享合成wire fixture：`/home/isp/wsps/cyf/docs/implementation/fixtures/gss-hosting-control-v1.json`，SHA256 `5c4b833e6db5bab3122c6dee17ef49198462aee3c3edf58f628ed8571e241403`；不是生产或已通过测试证据。
- 只读权限核查：现Runtime root:root，API cyf-api:isp，group isp GID1000；root-only0600 socket不可用，已通知两Owner采用明确受信组的受限socket及父目录遍历权限，保留API端uid/mode检查。现unified.host没有托管模板，当前service未配置RuntimeDirectory；源码/config/installer需明确接线，不只写单元测试替身。未修改生产。

### 固定验证清单 / 发布前待办（开发中，非完成回执）

| 检查 | API Owner | Runtime Owner | 当前 |
|---|---|---|---|
| 相同operation重放；不同owner/scope/绑定拒绝 | 持久intent/installation精确CAS | 完整association与journal | 待测试 |
| 新预留前通道检查在事务外；历史回执不重复reserve | admission/账本定向回归 | capabilities真实配置 | 待测试 |
| prepare不激活；ensure丢响应同候选续办 | 安装事务幂等 | journal与私有secret | 待测试 |
| 消费过secret但授权丢失不盲重放 | 不误capture/refund | RECOVERY_REQUIRED | 待测试 |
| 初租精确WS代际就绪 | currentRegisteredProof核验 | 当前ACK/执行器/持久状态 | 待测试 |
| 免费重整同installation、新session、零账本变化 | 不改paid period/资金 | 只重建目标、不影响其余 | 待测试 |
| 重启动态subject保留；旧READY不可直接重用 | 拒绝旧代次 | 受控重载与当前会话证据 | 待测试 |
| schema字段/唯一键/check与迁移一致 | 源码/测试/迁移 | 不适用 | 待测试 |
| 制品完整性和动态模块都包含 | 后端固定制品 | 原唯一installer清单 | 待测试 |

后续发布准备（本轮不执行）：固定候选commit/tree及版本；Runtime原installer产生同批制品；后端本地原串行构建；备份/锁下执行精确schema迁移；配置私有control路径/受信组/托管provider模板；受控安装与共享Runtime一次重启、API安装；在线核对版本后仅续原公孙胜订单、初租ACTIVE后再原UI免费重整。不重测旧线上版本、不重下单、不补款、不建第二Runtime。共享重启涉及其他账号角色，不能冒称仅影响公孙胜。旧钥匙只按原intent精确审计停用，不批量操作。

## 2026-10-10 09:53 开发交付（不是生产验收）

用户目标窗口09:02—11:02；本轮约51分钟完成实现、自检、控制通道联调及双仓develop集成/推送。各微任务连续推进，不因阶段汇报或可修复失败停工；无独立Reviewer。

| 仓库 | 原develop / merge parent | 已推送develop / source SHA | source tree = merge tree |
|---|---|---|---|
| API | 36d9e5452ab8beb64b97e5570da6ede10ec38797 | 24eb4ba863fb1fffdd04f7899a264ccf2b7317df | 883b559fae4bd5e5bc16780b7e93837a21e216e8 |
| Runtime | 2ce6fedf34832048e248fde3e07222f5ed867b7a | 80eadc9247132a9d6c6b3b9d7fe7b7f965e094de | ac7ffd578f1a719071be6cb0ce3d3bdc0022c841 |

两组件FF集成，无语义改写；受测worktree均全clean。Main回读校验源码/tree、XML和证据摘要后复用原结果，不重跑相同输入。独立worktree/branch保留本轮固定源与证据引用，未删除其他任务目录。

### 实际结果与证据
- API：最终同tree 83测试、0失败、0错误、0跳过，`validateLayering`通过。
  - `/var/tmp/cyf-gss-hosting-api-20261010-owner-r9/delivery.json`，SHA256 `b581c8a2fcab16a9e5d16b8e63b823de6a9aa205945bf7e680d8efb4540a38c6`。
  - touched-hosting-bridge evidence key `d6800280bf3f8a1790fd9dd03669b6a855482ec62f4dafb0b02e728e03718640`；financial-schema key `749ff8e145e5171e00f71369fb87a2c83f5a354a5364dc28adc278518a9a18ec`。
  - 真Java `UnixManagedHostingProvisioner` ↔ AF_UNIX ↔ 真Node `HostingControl`/journal/RuntimeHost，覆盖初租、同operation重放、同installation免费新session及旧代次拒绝。API授权/currentRegisteredProof、native enrollment/session/executor使用独立合成替身；不是实际Provider/生产API/资金验收。
- Runtime：157 PASS、0 FAIL、1既有SKIP；独立bridge 2 PASS；静态检查PASS。
  - `/var/tmp/gss-hosting-runtime-20261010-evidence-fEccWg/delivery.json`，SHA256 `826fe1f7ec0e3268211f63401a376dba718ffffa7054ee5fc872beaaac07b579`。
  - skip原文为历史M3跨端HTTP ACK/恢复条目NOT_RUN，保留不重标；本次控制通道测试不能替代它。
  - 测试含真实本地子进程provider环境透传与受信组UID/GID socket访问；模型/网络服务仍未实际调用。
- 实际工具记录：Node v20.20.2（无版本门禁）；API Java21.0.8、Gradle9.3.1、测试runner Python3.6.8。文档/核验辅助使用Python3.11，不改解释器或全局配置。
- 测试失败按事实闭合：首次runner的Python3.6不接受text关键字，改已有universal_newlines；fixture Integer/Long通过真实JSON roundtrip比较；H2 RR真实raw行证实本事务locking-read为空/外部已提交1行，与MySQL current read不能等同。保留独立RR诊断，H2竞争测试明确READ_COMMITTED，生产CAS未放宽。旧失败日志及根因历史保留原r1/r2/r7/r8目录，最终候选未复用失败为成功。

### 本轮完成 / 未完成边界

已实现：installation精确ensure及schema/迁移源码；原intent安装/代次关联；事务外新预留能力检查；统一Runtime动态加入/单subject重建；私有control/journal/独立模板/权限及installer清单；当前注册证据结算与免费重整零资金、原租期不变；受影响定向回归及真Java-Node控制通道联调。

未执行：MySQL RR/实际迁移/catalog验收、整模块回归、正式版本化制品/安装、生产配置/旧关联钥匙精确停用、共享Runtime受控重启、原公孙胜订单ACTIVE与线上免费重整。自动授权修复、凭据轮换、遗留锁强占不是本轮交付功能。前端无改动/无Flow；新用户赠款继续搁置。

下一步是发布与原单生产验收，不是继续重复写一版接线：固定版本与制品、完成适用DB验证和迁移/配置，按原发布锁/备份边界安装；只续 `hrl_0fa0c7b0-bf62-4524-88fa-bed7459b795d` / `hri_063977b3-1143-4d9b-8703-fbd0e56b466a` / binding16；原初租确认后才免费重整。本轮没有生产重启、订单/资金/数据库更改。生产最后已知仍API1.14.2/旧Runtime，此处不是新的线上实测。
