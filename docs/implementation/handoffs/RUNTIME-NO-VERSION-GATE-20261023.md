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
