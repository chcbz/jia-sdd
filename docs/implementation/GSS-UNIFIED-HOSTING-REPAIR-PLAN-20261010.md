# 公孙胜初租/免费重整接入统一 Runtime：修复方案

- 2026-10-10，Owner Main。**已按用户2小时要求派发开发（09:02—11:02 CST目标窗口）；两端编码中，尚未完成验证/迁移/发布。**
- 只读源码核对：API `36d9e5452ab8beb64b97e5570da6ede10ec38797`；Runtime `2ce6fedf34832048e248fde3e07222f5ed867b7a`。2026-10-10开工只读ls-remote已核对两仓origin/develop与此基线相同；未fetch。
- 原实测和资金事实：`/home/isp/wsps/cyf/docs/implementation/handoffs/GSS-REJOIN-20261010.md`；`/var/tmp/cyf-gss-rejoin-funded-20261010-yBc9aH/summary.json`。本文不以静态源码检查替代新的线上状态读取。

## 1. 冻结范围和目标

修复现有“山寨安顿→真实就绪→免费重整”的缺口，不开发新用户赠款、不改租金规则、不新增用户侧入口、不恢复旧broker/API-key协议、不另起第四个Runtime。

继续原新订单：
- persona=`gongsunsheng`；canonical agent=`agt_5e283360939b4ddead4e69859355db08`；binding=`16`。
- lease=`hrl_0fa0c7b0-bf62-4524-88fa-bed7459b795d`。
- initial intent=`hri_063977b3-1143-4d9b-8703-fbd0e56b466a`。
- 原reserve transaction=`etx_7977c18a-cc8f-4051-ab5f-bb2bb043d463`，1000 SILVER已预留；08:50最终回读可用1000/预留1000，未capture。

不能重新点将、重建binding、再下一张初租单、再补款，不能直接SQL改ACTIVE。对账器在修复后消费原intent，服务真正可用才结算/起租。

## 2. 采用的结构

```text
原“山寨安顿”UI / 原bind接口
  -> 原租约、预留账本、provisioning intent
  -> HostingRentReconciler
  -> RuntimeV1托管适配器（替换旧UnixManagedHostingProvisioner实现）
  -> 统一Runtime进程内部的私有本机控制socket
  -> 同一RuntimeHost按subject添加/重建公孙胜executor
  -> 原RuntimeV1 installation / enroll / session / WebSocket注册确认
  -> 精确operation就绪回执
  -> 原租金状态机capture并把租约置ACTIVE
```

建议socket：`/run/cyf-agent-runtime-v1/unified/control.sock`。它是**现有统一Runtime进程内部的控制入口**，不是恢复旧managed-host.mjs，也不是第二个服务/执行进程。支持同host多个owner，各自scope、授权、HOME和工作目录隔离。

## 3. 必须改的代码

### A. API托管适配器和安装授权

基准目录：`/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/`

- `hosting/UnixManagedHostingProvisioner.java:39–54,108起`：用RuntimeV1托管适配器替换旧API-key/observe/ensure协议实现；保留`ManagedHostingProvisioner.Preparation`里的tenant/client/owner/agent/binding/intent/lease/operation精确关联。不并行保留旧实现作fallback。
- `hosting/ManagedHostingCredentials.java:118–162`：托管执行不再创建/读取cdx_旧API key。新安装调用`service/impl/AgentRuntimeV1ServiceImpl.java:56–76`现成installation校验和创建能力，传入持久订单核实的scope/owner，而不是伪造用户JWT。
- 为installation增加内部“同ID精确输入一致则读回”的ensure语义：原create当前是直接insert，不能假设已支持重试。身份、manifest和secret digest任一不一致必须拒绝，不覆盖安装授权。
- 复用`AgentRuntimeV1Controller`既有enroll/session/heartbeat，不新增公开发钥接口，不让前端拿到enrollment secret/runtimeAuthorization。
- `hosting/HostingRentReconciler.java:89–113,116–170`：初租与免费重整消费新适配器，沿用原状态机与账本服务；所有socket、HTTP和文件I/O在DB事务外。

### B. 统一Runtime内部控制和单Agent生命周期

基准目录：`/home/isp/wsps/chcbz/isp-install/conf/`

- `cyf-agent-runtime-v1/agent-runtime.mjs:38–59`：在现有host生命周期内启动/关闭本机控制入口；后台心跳不等待某个新Agent注册完成。
- `cyf-agent-runtime-v1/lib/runtime-host.mjs:54起`：增加按完整subject的`ensureAgent`、`reprovisionAgent`生命周期操作；串行同一Agent，保留host/Agent锁及所有权核验，不通过释放他人锁或重启整host来实现正常重整。
- `cyf-agent-runtime-v1/lib/execution-adapter.mjs:13起`：支持附加/关闭指定subject的adapter、独立session和注册确认，正确移除旧attached状态；不能只往host.agents里塞一项。
- `codex-ws-agent/agent-client.mjs:6411起`：现有execution host把entries/profiles固定在构造时，且closed entry不能重用；须同步增加受控add/recreate接口，清理本subject的执行器、transport及profileStates引用，保留其他Agent不变。
- `cyf-agent-runtime-v1/lib/runtime-client.mjs:147起`：复用既有enroll→私有授权落盘→session逻辑。不取消“可能已消费secret时禁止盲重试”的约束。
- manifest/config/制品清单/installer定向更新，新的持久托管subject在重启后仍能载入；只改内存Map不算完成。

新profile由明确的托管模板生成：独立state/HOME/workdir；模型Provider配置来自获准的托管模板，不复制吴用或卢俊义的私人HOME、凭据和任务文件。

### C. 新订单受理前检查

- `HostingRentApplicationService.java:117–125`现在在事务内调用requireProvisioner；`ManagedHostingProvisioner.available/availableFor`的契约是纯检查，**不能直接塞socket调用进去**。
- 拆成：已提交请求先精确幂等回读 → 新请求在事务外检查Runtime控制通道/协议/该scope托管能力 → 原事务重新核对身份、报价、并发与余额后预留。
- 已知控制通道缺失明确返回503，不能再仅因“配置写了路径”就接受新付款。检查后通道仍可能掉线，不能承诺消除所有异步未知状态；该情况仍保留原intent待核实，不凭超时退款/重建订单。

## 4. 私有控制契约与持久化

建议内部操作：`capabilities`（只读可用性）、`prepare`（落盘安装候选但不启用）、`ensure`（安装授权确认后启用）、`observe`（精确回执查询）。免费重整使用相同operation框架、不同requestId，不另建付款通道。

### 固定关联

每个操作绑定：tenantId、clientId、ownerJiacn、canonicalAgentId、bindingId、leaseId、initialIntentId、operationId、operationKind、requestedAt、validUntil（免费重整时）。同operationId内容不同拒绝。同一Agent的不同操作按subject生命周期队列执行。

- socket目录和文件权限只允许受信API进程身份；Runtime校验peer/固定scope授权，不能接受任意shell、路径、外部URL或任意profile文件内容。
- operation/subject专属私有journal先落盘再产生不可逆副作用，目录按完整scope派生，不按persona昵称派生；重复ensure查原journal，不能重新执行一次重整。
- `prepare`在Runtime侧生成并持久化installationId、manifest和一次性enrollment secret，仅向API返回manifest摘要和secret摘要。API事务创建/绑定installation后才`ensure`；Runtime自行通过既有enroll接口提交secret，安装授权只留私有文件。
- 候选prepare不自动等于付款或授权。API未提交关联时不得启动executor；重复prepare返回原候选。API已创建但ACK丢失，按同installation精确回读，不再新建。
- enrollment结果丢失、API已ACTIVE但本地授权未落盘：沿用明确RECOVERY_REQUIRED，不能无限重试已消费secret。只针对该installation核实/撤销后产生新generation，不触碰租金预留和其他Agent；不得把该异常标为SERVICE_READY或FAILED_NO_EFFECT。

### 建议最小DB改动（实施前需更新schema/entity/mapper与迁移一致）

不增第二套账本，不新建通用任务框架。

| 表 | 新字段 | 用途 |
|---|---|---|
| economy_hosting_provisioning_intent | runtime_installation_id VARCHAR(100) NULL | 原initial intent绑定RuntimeV1 installation |
| 同表 | runtime_manifest_sha256 VARCHAR(64) NULL | 绑定候选manifest摘要，不以可变路径作为身份 |
| 同表 | runtime_provision_generation BIGINT NOT NULL DEFAULT 0 | 安装候选/授权恢复CAS代次，不等于租约版本 |
| economy_hosting_reprovision | runtime_target_generation BIGINT NULL | 本次免费重整目标代次，防旧在线回执冒充本次重整完成 |

installationId在同scope非空唯一（一个初租intent对应一个当前安装）；字段组合完整性校验及CAS写入。免费重整的installation和manifest从原initial intent读取，requestId沿用现有唯一键，不重新reserve。

旧`managed_api_key_id`只保留原订单审计引用，不作为新授权fallback。当前公孙胜该钥匙应在受控迁移中精确核对scope/owner/description/关联intent后停用，不能批量吊销他人钥匙；既有历史交易/租约不删除。

### 就绪证明

必须同时匹配installation、完整subject、hostId、runtimeInstanceId、sessionGeneration、当前operationId/目标代次；该operation之后的WebSocket注册确认、durable state和实际执行能力就绪均成立。API还须与自己持有的安装、当前会话/Agent注册代际核对。

仅profile文件存在、进程启动、绑定ACTIVE、某个旧lastSeenAt或旧agent在线，均不足以结算。新回执不用旧broker的engineThreadId字段冒充证明；初次尚未接任务不应被要求伪造任务线程。需要的是本次执行器真实可用及注册确认。

## 5. 初租与免费重整的完整行为

### 初租（续原单）

1. 读取原intent，核对仍PROVISIONING_UNKNOWN、原租约/binding/owner一致及预留未结算。
2. prepare→精确创建/关联installation→ensure→enroll/session/register，添加到**同一**unified Runtime。
3. observe本operation真实就绪；走原confirm-ready/capture路径，租期从真实serviceReadyAt起算30天。
4. 应得到可用1000/本次预留0；只发生一次原1000预留对应的capture，不再出现第二笔reserve。

### 免费重整

1. 等原租约ACTIVE且未过期，经原UI发REPROVISION，同一lease、金额0。
2. 只暂停/关闭并重建公孙胜的executor/transport，复用有效installation授权申请新session；不重放一次性enroll、不重建支付订单。
3. 用新requestId与runtime_target_generation证明本次重建完成；不能用重整前的online快照直接回成功。
4. 原paidFrom/paidThrough/租金流水/可用余额均不变；完成后同Agent恢复就绪。其他Agent的实例、连接和状态不得因这个操作被重启。

## 6. 实施顺序和验收边界

1. 冻结上面内部契约及字段；Runtime与API可在非重叠路径并行实现，各自一个Owner，不加Reviewer或新调度框架。
2. Runtime完成单subject增加/重建、持久化和精确回执；API完成installation关联/新适配器/事务外探测。联测同固定输入，受影响回归保留身份、幂等、账本一致性。
3. 按版本化制品部署Runtime及后端（后端本地受控构建）；默认无需修改Web/启动前端Flow。如果发现现有UI无法正确呈现状态才单独限定修复。
4. **首次部署新Runtime代码需要一次受控共享服务重启**，会涉及现有三角色，必须在发布步骤明确影响/归属，不能把“只重整公孙胜”当成无限授权。运行期新入伙/免费重整则走单Agent动作，不再重启整个host。当前方案没有执行任何重启。
5. 发布后只续本文件固定原单，不再除名/报价/预留。第一场景ACTIVE并真实就绪后才执行第二场景免费重整。

最小回归：scope/owner串线拒绝；同operation并发与丢响应幂等；缺少控制通道的新reserve拒绝；安装创建回执丢失；enroll可能消费后的恢复边界；原pending订单续办；同一host添加一个Agent不影响另外三个；免费重整确实产生新代次且零资金变化；新旧回执错代拒绝；进程重启后已添加subject不丢失。

完成标准不是“代码写完”或“202”：公孙胜真实注册/可用、原租约ACTIVE、只有一次1000租金、免费重整成功且到期时间不变。若只完成接线开发但未发布/未达到该条件，分别报告，不标流程完成。
