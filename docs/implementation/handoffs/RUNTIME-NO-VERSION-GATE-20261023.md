# RUNTIME-NO-VERSION-GATE-20261023

2026-10-23，唯一Owner：当前会话，单Agent。用户在配套升级讨论后明确“取消Runtime的版本与协议校验”。承接上一轮API1.16.31发布后的多轮图片验证，不调整API/Web，不改全局Codex或模型。

## 范围和基线

- 已读取最新CYF AGENTS、工具索引、isp-install规则；采用CYF固定实体app规则，覆盖外部旧releases/current口径。接口规范固定`/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.2；实际业务协议不变。
- 远端fetch确认isp-install develop为`3c993e58033d901622c24126028199cdf4e2c76f`。独立worktree `/home/isp/wsps/chcbz/isp-install-worktrees/runtime-no-version-gate-20261023`，分支`codex/runtime-no-version-gate-20261023`。不覆盖共享脏文件。
- 基线生产Runtime1.2.8；候选1.2.9。现用共享CLI0.164.0，上一轮519被配置文件漂移拒绝，详见PREVIOUS-OUTPUT-REVISION-20261023及原证据。不要把版本门禁与文件完整性混为一谈。
- 取消：Codex版本白名单、固定schema bundle摘要匹配、按profile合同版本判定typed就绪，以及配置必填合同ID。版本仅诊断，停止生成协议schema；未知版本以实际RPC结果为准。
- 保留：可执行文件/资源快照和摘要、身份ACL、实际初始化/消息解析、业务结构/来源授权、隔离、幂等、锁与恢复保护。文件在运行中替换仍需受控重启重新测量，不能自动接受漂移。非目标：泛化兼容层、全局CLI管理、生产历史记录修复、无关事项及PDF。

## 验证与发布边界

- 首次本机低开销串行定向测试5入口285/285通过，覆盖未知版本/schema不拦截、缓存/worker、篡改拒绝、配置/权限与typed业务解析。日志`/var/tmp/cyf-runtime-no-version-gate-20261023/targeted.log`。这是定向反馈，不是Flow或业务验收。
- 后续补真实0.164.0隔离无模型握手、受影响consumer回归，固定候选后使用既有Flow作CI-only验证；部署/重启单独确认版本与影响，本机不制作生产包。
- 尚未发布，尚未恢复519或完成多轮图片验收。源码、云端测试、安装、通道健康、业务验收逐项记录，不以取消校验宣布问题解决。

## 源码收口与当前证据

- isp-install develop普通push并远端回读：`cbc1050825a40378313f283e9f25dc46d44c1ea4`，tree `4fa8a81432bc9bc8d16d1fc12ab3c065f8d1979a`，Runtime1.2.9。旧注册表移入历史测试fixtures，不被生产源码导入。
- 本机最初5入口285/285；相关consumer另44/44；改进诊断readback后2入口复跑251/251，计数存在重叠不能相加宣称独立测试总数。
- 真实Codex0.164.0（binary SHA `b93f6811d3f653f0fb83be4050d857fb9abbb111dfa2ce160563327daff7f306`）在全新空白HOME、无凭据下初始化成功1/1，实际子进程摘要匹配，READY无版本门禁；未发模型turn。证据`native-handshake.log`。
- 完整native隔离套件两次未通过：第一次旧fixture使用provider.invalid，真实TLS失败；补可配置probe URL后采用当前配置Provider地址，首次measure成功，第二个profile测量遇到原1秒传输超时。保留失败，不修改产品网络策略/超时，也不把无模型握手当完整隔离或识图验收。证据`native-profile.log`、`native-profile-configured-provider.log`。
- Flow5264702 Run27精确cbc1050、CI-only，CustomEnvironmentBuild在测试输出前FAIL，尚无测试结论。二次只加非秘密preflight诊断并保留全部断言，不换候选/不关闭校验、不加部署作业。查询/控制证据`/var/tmp/cyf-runtime-no-version-gate-20261023/`。
- 当前生产仍1.2.8，未重启/安装、未修改共享CLI、未重放519，业务矩阵仍待执行。原API1.16.31发布事实不变。开发完成、云端验证、生产生效分开。

## 最终CI与收尾（2026-10-23 21:17前后）

- Run28确认失败根因为Flow cache restore在原checkout写入`ossutil.log`，触发干净源码断言，不是应用测试失败。没有删除该日志或忽略脏文件；Run29从精确cbc1050建立独立干净worktree再验证，相同原测试/断言保留。
- Flow5264702/29 SUCCESS，job541894956，精确commit cbc1050825a40378313f283e9f25dc46d44c1ea4 / tree4fa8a81432bc9bc8d16d1fc12ab3c065f8d1979a。354项：352通过、0失败、2项opt-in native跳过。job日志摘要显示跳过分别为空HOME真实CLI握手和完整bwrap/profile隔离探针；前者本机真实1/1通过，后者TLS失败保留。正式CI-only不含部署作业、没有生产包安装。
- 临时Flow配置已恢复至本轮原值，APPLIED+readback，未取消他人Run。生产1.2.8/PID1404284未变，完整图片业务验收/519状态仍未验证。
- [紧凑证据](../../../specs/juyiting-skill-execution/evidence/runtime-no-version-gate-20261023/README.md)包含源码、测试、真实握手、未通过探针、Flow摘要及SHA清单。后续要使取消校验在线上生效，须固定1.2.9的受控发布/重启；当前不宣称已上线。

## 受控发布接续（2026-10-23 21:30）

用户“继续”承接1.2.9待发布及图片验收，授权本候选上线。固定cbc1050/tree4fa8a814，不追随其他提交；远端develop已回读一致。生产1.2.8/PID1404284；无pending/processing，8条recovery与3条历史DISPATCHED、2条RESULT_UNKNOWN执行保持原样。配置身份与4110项基线manifest核验通过，依赖锁未变；5264702无活动Run，配置已快照。复用既有受控安装器和Run29干净源码策略，测试/打包/安装同Run执行，安装后本机核验。不更改API/Web、CLI、模型或历史业务状态。私有证据 `/var/tmp/cyf-runtime-version-gate-release-20261023/`，恢复批次 `/home/isp/baks/cyf-agent-runtime-v1/20261023-version-gate/`。

## Flow30已上线，业务继续核验（21:42）

固定cbc1050/tree4fa8a814，Flow5264702/30 SUCCESS，构建541901162、部署541901163/71709927。352通过、0失败、2 opt-in跳过，93项程序文件，同Run制品SHA `3b7c32d636bc6cfcfcf926ac8eab1a8468362ac06ee0fe2dc7b8a4d511b04bd0`。安装21:39:26结束，PID1507807，21:42三Agent通道及ACK核验通过；8条恢复记录/配置身份保持。配置已恢复APPLIED。新执行策略下旧carrier证据不匹配，真实错误TYPED_INSPECTION_CARRIER_EVIDENCE_INVALID，恢复轮询另报inputPolicyDigest空引用；不改DB、不重放旧请求。复用既有9格式carrier工具，修正异步spawn调用，在本任务独立目录真实测量，未移除隔离或伪造摘要。图片业务未完成。

## carrier重测与启用（22:07）

复用旧工具、仅修正异步spawn调用，9图片格式实际模型turn全部PASS；当前已安装1.2.9正常loader独立重测contractReady=true，无安全/网络放宽。Flow31为配置维护（无程序包/构建），安装新证据、引用及无版本号的engineContractId，71710512成功，临时Flow配置恢复。PID1516365，93项程序文件未变，其他配置/身份与8条recovery未改。证据SHA73c3e1aa199998627c13dce35c7d4b67e867edd520a23606209867f6636ea8bc；恢复 `/home/isp/baks/cyf-agent-runtime-v1/20261023-carrier-refresh/RECOVERY.md`。程序仍Flow30发布1.2.9。浏览器新任务520、会话1760458007122，ziyue/吴用；第一轮识图已正确返回，request mmd-typed-request_fa5c03c2b31b3507f6a6eae567908eac9d2e079b，turn_a14cf345b0e6bb9a95d05958e719bce88c4f63a4，inputReceipt原图SHA a80176157363cc3233eee10e3a89851cf743f70cbdbf3952d66ef534dc7b8d97，已发送第二轮位置追问。旧519未重放，510/513 UNKNOWN仍保留。

## 本轮业务阻塞收口（22:39）

任务520两轮识图PASS，原图SHA与inputReceipt匹配。第三轮请求改原图返回REVISION_REQUEST；review事件 `review_1aa227c174a6e3ebbd898819b1d5889d3ed1e8588dd75efa86f4705e8` 持续RETRY/SourceUnavailable，projection QUEUED且childRequestId=null。生产API仍1.16.31/041548f，JAR摘要67975108…与既有发布一致。本轮不修改API。

根因已从实际调用栈与固定源码确认：`ChatDeliveryRevisionService.consume:87` 用任务发起人owner而不是目标Agent真实owner调用`packages.prepare`；`InstalledSkillDescriptorService.read:33` 的合法身份域校验因此拒绝 ziyue→吴用；异常发生在review操作入库和业务catch之前，被relay当可重试错误不断回排。普通`ChatTypedDiscussionAdmissionService:105-106`已使用`dispatchAuthority.admissionTarget(...).ownerJiacn()`。模型把改原图归为修改文本成果另需回归，但不是本次队列SourceUnavailable的根因。

下一条动作（后端专项，不取消权限校验）：复用现有dispatchAuthority解析受委派executor owner后准备技能包，保留任务owner用于任务/会话事务与ACL；补同账号、跨账号、授权撤销/指派变化、永久不可用不无限QUEUED及原图/文本成果目标区分的定向回归。正式Flow后重新验证现有事件幂等续办，不手工改DB/造成功；再补无输入生图、连续两轮改上一版的SHA链、PC/移动正式验收与重入。证据在本次business-task520.json。
