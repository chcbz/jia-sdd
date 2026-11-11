# 聚义厅必做收口：统一 Runtime 与原事项恢复编码详设

- 核对日期：2026-10-09，Asia/Shanghai；本轮约20:04起定向核源码。
- 修订决定（2026-10-09）：按用户明确要求，**2.0.0前只采用最新契约，取消分阶段安全切流设计，改为一次直接切换**；不新增旧版兼容、灰度、双轨或旧客户端回退。
- 状态：**设计待实施**。本轮仅新增本文和本地合成诊断证据，未修改运行代码、生产配置、数据库、服务或任务指派。
- 目标：不增加产品功能，恢复吴用、林冲、卢俊义的现有执行入口，最终同一 Runtime、多 subject 独立状态；续验原事项432，不重复创建或点将。
- 任务归属：接续现有UR06/统一Runtime收口；下文R1～R4只是本文工作切片，不是新增任务ledger。实施时原Runtime Owner唯一认领源码，Main负责生产直接切换和验收；不新增Reviewer，不接管活动ACK侧聊。
- 执行规则：[项目规则](/home/isp/wsps/cyf/AGENTS.md)、[已有工具入口](/home/isp/wsps/cyf/ops/orchestration/README.md)、[开发流程](/home/isp/wsps/cyf/docs/sdd-workflow.md)。本文不扩大生产授权。

## 1. 必做范围与完成口径

| 切片 | 必须完成什么 | 性质 | 本轮必要性 |
|---|---|---|---|
| R1 | 去掉“等待所有Agent激活后才启动全局心跳”的屏障，保留关闭顺序和锁归属 | **需编码及定向测试** | 单Runtime下一个subject等待注册不应拖住其他subject；本轮合成复现已证实 |
| R2 | 固定统一Runtime制品；逐subject准备最新manifest/profile/凭据/工作区策略和必要业务状态 | **已有实现的交付** | 旧客户端不符合新API认证契约；缺的是匹配客户端及配置，不是新API |
| R3 | 一次直接切换：停止范围内旧入口，安装/启用唯一unified Runtime，三角色一起采用最新契约 | **已有实现的部署，不开发切流功能** | 不做灰度、逐角色试切或新旧并行；停止确认、备份和任务数据保全仍保留 |
| R4 | session→WS→真实typed READY→原432自动接续；按原业务授权继续执行/交付 | **生产验收，出现具体断点才修对应代码** | 当前已发布API/Web健康不等于办事恢复 |

**不预设所有未完成项都要开发。** R1是本文唯一已定位、给出确定修改方案的新增运行代码修复。R2/R3不是另写安装器、迁移框架、认证或调度系统的理由。不以完整迁移所有历史数据为上线门槛；完成记录备份归档，未完成任务按现有权威状态处理，不能编造通用迁移器或旧格式运行分支。

以下从本轮必做清单排除：MQ provision接线/启用、付费托管暂停恢复、F01 context-pack适配、文件成果跨重启report-only补强、旧health自动恢复脚本收口、telemetry框架、旧E13提案、历史PhaseA扩列。它们保留于[完整缺口详设](/home/isp/wsps/cyf/docs/implementation/UR05_PRODUCTION_CLOSEOUT_DETAILS_20261009.md)，不作为R1～R4的预置门槛。

- **直接切换顺序：固定新制品和配置 → 备份 → 停止范围内旧实例并确认退出 → 启动唯一新Runtime → 生产实测。** 允许切换窗口内服务短暂不可用，不增加无停机要求。
- 不启MQ、不新增DDL、不恢复旧认证；不重复构建已经发布且未改变的API/Web。
- 不宣称文件任务断电恢复、付费托管恢复、四profile全恢复或整个UR05全部完成。
- F01或文件恢复如果在原432真实链路上成为确定阻塞，再凭具体失败请求/状态采用原详设的相应切片；不能先把全套需求加回来。
- **安全边界必须保留**：ACL、完整subject、持久ACK、原执行结果、发布锁、备份、制品完整性；这些不是可选功能。

## 2. 固定基线与证据时效

| 对象 | 核对来源 | 本文用途 |
|---|---|---|
| Runtime源码 | `/home/isp/wsps/chcbz/isp-install`，commit `5489c0e946114ec601e246a4eb93a0bff3b57c24`，tree `66424e5e9063f316869b00c952a3859625ece77f` | 本文Runtime行号及R1编码基线 |
| API源码/本轮已发布 | `/home/isp/wsps/cyf/api`，commit `1e9111028fbdff1ae5452f64aec843e85e81ad59`，tree `0416b722d735c58af4653892b6ee269e8f9d1498` | 认证、数据库和bootstrap契约；本设计默认不改API |
| Web本轮已发布 | commit `c6ae76010c43153659cc6d55c902a1765c620932`，Flow4403172/Run186 | 已发布证据；不把后续侧聊commit当已上线 |
| 本轮文档核对时root/Web HEAD | root `952744d439727ac90e43390e34f2628ad9f2f72a`；Web `3e9b0aff365c25faab524e905b7c2f1aff53c3f1` | 仅本地观察，其他侧聊仍可推进；本轮没有重查远端或证明新Web已发布 |
| 旧共享客户端磁盘文件 | `/home/isp/apps/codex-ws-agent/agent-client.mjs`，SHA256 `58eadc5cb885fbf6fb39fec7de5fed4d26cbf999a201ab9436b3cfc21915d410` | 仅旧切流风险审计；不是新候选，不等于已证明运行内存版本 |

生产历史事实（不是本轮实时查询）：17:45左右四主体fence为NULL、三原installation ACTIVE、公孙胜无自身native installation；真实浏览器看到原432的bootstrap RETRY/BOUNTY_RUNTIME_AWAITING。执行R2前必须刷新精确只读投影，不能照搬上述快照写数据。

既有证据：
- [生产安装/13DDL/配置回执](/home/isp/baks/cyf-develop-consolidation-20261009T1558/versioned-production-release-readback.json)
- [认证归因](/home/isp/baks/cyf-develop-consolidation-20261009T1558/runtime-auth-diagnosis/ur04-production-runtime-auth-diagnosis-20261009.md)
- [原432生产浏览器结果](/home/isp/baks/cyf-develop-consolidation-20261009T1558/production-browser/production-acceptance-report.md)

所有源码行号绑定上述commit；Owner开工若HEAD变化，应先比较指定函数，保留他人改动，不能整文件覆盖或按旧行号机械打补丁。

## 3. R1：多Agent激活等待不得阻塞健康subject心跳

### 3.1 精确问题与证据

[agent-runtime.mjs:38–59](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/agent-runtime.mjs#L38) 的 `runUnifiedRuntime`：45–48行并行创建激活Promise，55行 `await Promise.all(activate)`，56行才进入 `adapters.heartbeat()`。

`host.activate()` 会等待 [runtime-host.mjs:117–127](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/runtime-host.mjs#L117) 的 `executor.activate()`；[execution-adapter.mjs:105–121](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs#L105) 的activation等待有效注册回执，瞬时网络失败可持续重连。因此：A已READY、B等待注册时，A也无法进入主循环心跳/恢复调度。

2026-10-09 20:04本地合成复现：A.ready=true、B.activation未完成，事件循环让出5轮后heartbeat调用数为0；终止后两个subject均STOPPED。没有访问HTTP/WS/Provider、没有生产状态：
- [复现脚本](/home/isp/wsps/cyf/docs/implementation/evidence/runtime-required-closeout-20261009/activation-heartbeat-probe.mjs)
- [复现结果](/home/isp/wsps/cyf/docs/implementation/evidence/runtime-required-closeout-20261009/activation-heartbeat-probe.json)

这是**新发现的单Runtime可靠性缺陷，不是已观测401/400的根因**。上述5轮用于确定性让出事件循环，不是生产deadline/SLO。

### 3.2 修改清单

| 文件/行 | 修改 | 不修改 |
|---|---|---|
| [agent-runtime.mjs:38–59](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/agent-runtime.mjs#L38) | `runUnifiedRuntime`分离每subject激活Promise与全host心跳循环；保存幂等关闭Promise；终止先关闭transport解除激活等待，再await激活与host.stop | CLI参数、session/ACK协议、心跳间隔、重试策略、hostId/boot来源 |
| [runtime-host.test.mjs:542–566](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs#L542) | 保留SIGTERM不死锁及锁释放断言；原551行“任何激活未完成都不得heartbeat”的替身断言改为“未注册subject不发presence/不resume” | 不删除停机测试、不把关闭未确认的锁释放算PASS |
| 同一测试文件新增测试 | 覆盖下文R1测试矩阵，用现有fixture/channelFixture | 不新增runner或并行ACK存储 |
| [execution-adapter.mjs:125–147](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs#L125) | 默认**不改**；现有heartbeat在没有session/OPEN socket时直接返回，逐subject检查channelConfirmed | 不在未注册subject上强制ready，不扩大HTTP scope |

### 3.3 可直接实现的控制流

修改原函数内部，不新增管理类。`closeAdaptersOnce()`须缓存成功或失败的Promise，不能在catch后无条件再次close，不能吞掉失败后释放锁。示意伪代码（沿原返回值/logger编码，不能整文件替换）：

```javascript
const adapters = await createAdapters(/* 原参数完整保留 */);
const host = new RuntimeHost(/* 原参数完整保留 */);
let activations = [];
let closePromise;
const closeAdaptersOnce = () => {
  if (!closePromise) closePromise = Promise.resolve().then(() => adapters.close());
  return closePromise;
};
const onAbort = () => { void closeAdaptersOnce().catch(() => {}); };
// 此处catch只防事件回调unhandled rejection；finally必须await同一Promise暴露错误。
try {
  await host.start();
  signal.addEventListener('abort', onAbort, { once: true });
  if (signal.aborted) onAbort();
  else activations = config.agents.map(agent => {
    if (host.agents.get(agent.subjectKey).phase !== 'INITIALIZED') return Promise.resolve();
    return host.activate(agent.subjectKey).catch(error => {
      logger('runtime-agent-isolated', {
        subjectKey: agent.subjectKey,
        category: classifyRuntimeError(error).kind
      });
    });
  });
  // 不等待全体activation，不另造第二个心跳定时器。
  while (!signal.aborted) {
    await adapters.heartbeat();
    if (!signal.aborted) await waitFn(heartbeatIntervalMs, signal);
  }
} finally {
  signal.removeEventListener('abort', onAbort);
  await closeAdaptersOnce(); // 先关闭transport，解除注册等待；失败不得冒称已关闭
  await Promise.allSettled(activations);
  await host.stop();         // executor关闭确认后按原归属释放Agent锁/host锁
}
return host.snapshot();
```

实现注意：
1. 保留每Agent激活失败仅隔离自己、日志不带原error.message/token/私有body；不把401/403改成无限重试。
2. 这里先 `adapters.close()` 后 `host.stop()` 是为了不在 `withAgent` 生命周期gate后面等待永远未完成的activation；不能反转顺序。
3. `closeAdaptersOnce`失败时保留原root锁，不继续释放；不能通过清锁文件“恢复”。本轮不增加硬关闭deadline。
4. 已有heartbeat的业务含义保持：未认证socket不发送；未注册不resume；损坏durable state撤回接单但保留已知结果报告资格。
5. 保留调用方传入 `createAdapters/waitFn/signal` 的现有注入接口，不把测试控制器接入生产配置。
6. 本修改不处理任意慢Provider/任意挂起I/O，不宣称完成全系统无阻塞化。

### 3.4 R1定向测试矩阵

拟新增测试名（英文稳定selector）及断言：

| 测试名 | 输入 | 必须断言 |
|---|---|---|
| `healthy subject heartbeats while peer activation is pending` | A激活成功，B deferred未resolve；注入waitFn控制循环 | A至少两次presence/heartbeat机会；B不ready、不接任务；没有等待B成功才运行 |
| `pending subject cannot resume before registration` | B有socket但无有效agent.register回执 | 不resume、不执行，不把CHANNEL_PENDING当READY |
| `authorization failure stays per subject during heartbeat` | B session403，A正常 | B隔离、无盲重连；A继续heartbeat；日志不含凭据 |
| `abort closes pending activation before releasing host locks` | A正常、B等待；发abort | 关闭动作先于释放gate；全部已确认关闭后STOPPED；不存在遗留writer lock |
| `close failure retains writer ownership` | close明确reject | run返回失败；host/subject锁不被释放或偷换；无第二次close副作用 |
| `already aborted run does not activate subjects` | 入参signal已abort | 零activate；initialize后安全关闭；不发session/WS |
| `heartbeat failure closes transports without activation deadlock` | heartbeat抛错且B未激活 | close解除B等待后退出；不悬挂、不伪报PASS |

复用原 [runtime-host.test.mjs:488–558](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs#L488) 的channelFixture/事件控制。不要只测试替身心跳计数，还要用原adapter验证pending不发送/不resume。原551行断言仅调整含义，其停止行为全部保留。

实现后先跑（从固定源码目录执行，显式Node版本检查）：

```bash
cd /home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1
NODE=/home/isp/apps/node/bin/node
[ "$($NODE -p 'process.versions.node')" = '20.20.2' ] || exit 1
"$NODE" --test --test-name-pattern='healthy subject|pending subject|authorization failure|abort closes|close failure|already aborted|heartbeat failure|unified SIGTERM|unified runtime heartbeat' test/runtime-host.test.mjs
# 首轮通过后覆盖原配置/锁/认证/ACK/安装入口回归；不运行实际安装fixture。
"$NODE" --test test/runtime-host.test.mjs test/runtime-v1.test.mjs test/canonical-dispatch-r2.test.mjs test/install-entry-convergence.test.mjs test/unified-runtime-acceptance.test.mjs
```

保存实际tests/pass/fail/skip及源码tree，skip仍记skip；新修复后的源码不复用旧285tests作为其证明。以上命令本文未执行，只有3.1的诊断脚本已执行。

## 4. R2：现有契约直接复用，不新增表、认证或安装框架

### 4.1 必须准备的逐subject输入

沿当前handoff追加本轮映射，不新增长期台账。每一行对应完整subject：`tenantId + clientId + canonicalAgentId`，不是角色昵称。

| 输入 | 来源/校验 | 禁止 |
|---|---|---|
| `installationId/manifestVersion/manifestSha256` | 原ACTIVE installation和逐主体封存manifest一致；manifest摘要调用现有digestManifest | 按吴用昵称推导ID，改manifest后继续用旧摘要 |
| `hostId` | 本机持久配置；若已有非NULL fence，三主体必须各自符合当前host归属 | 每次开机随机hostId、直接SQL清fence |
| `runtimeInstanceId` | 原CLI每次run的randomUUID；同一Runtime内三subject共享boot，凭据/session各自独立 | 每Agent单独启动进程冒充统一Runtime；持久化boot重用 |
| `subjectKey` | [manifest.mjs:44–46](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/manifest.mjs#L44) 的runtimeSubjectKey | 使用agentId短名、截断摘要作隔离依据 |
| `runtime-authorization.json` | 原逐主体0600文件，`installationId`与manifest相同；有效性只能由真实session验证 | 输出token、共用token、重放已消费enrollment secret |
| `profile`及workspace policies | 逐subject原受支持配置；显式设置Codex路径/独立HOME/工作目录；真实能力决定开关 | 从旧`.env`整包复制、从宿主全局环境补身份/凭据 |
| 旧状态及在途 | 原ledger/inbox/ACK/report/session-map逐项映射，实际代码校验格式 | 清空队列、高水位归零、重跑unknown STARTED |

原三角色已有installation，**不调用enroll**。公孙胜缺独立installation是另外的主体交付缺口；不借用三角色身份。本轮要求保护其进程和在途，不把“未触碰”说成“已恢复”。

### 4.2 本地配置字段与目录（现有schema）

配置解析代码：[manifest.mjs:69–131](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/manifest.mjs#L69)。顶层只能四字段：`configVersion:1`、`hostId:string`、`stateRoot:absolute`、`agents:array`；agent entry只能 `manifestPath/profilePath/stateRoot`。不要向JSON塞额外的role/token/enabled管理协议。

候选布局（设计目标，非现场存在声明）：

```text
/home/isp/apps/cyf-agent-runtime-v1/unified/               # 原installer生成完整不可变制品
/etc/cyf-agent-runtime-v1/unified.host.json
/etc/cyf-agent-runtime-v1/unified.conf                     # API origin/策略文件路径，不含enrollment secret
/etc/cyf-agent-runtime-v1/subjects/<full-subject-sha>/manifest.json
/etc/cyf-agent-runtime-v1/subjects/<full-subject-sha>/profile.json
/home/isp/state/cyf-agent-runtime-v1/unified/host/          # host state，0700
/home/isp/state/cyf-agent-runtime-v1/unified/agents/<full-subject-sha>/state/
/home/isp/state/cyf-agent-runtime-v1/unified/agents/<full-subject-sha>/home/
/home/isp/state/cyf-agent-runtime-v1/unified/agents/<full-subject-sha>/work/
```

host state与Agent可写根必须是兄弟隔离目录，不能包含/嵌套；不同Agent的任何可写根不得相等、嵌套或符号链接别名。配置文件与执行UID一致、非group/other writable；state根0700，授权文件0600，按 `requireOwnedPrivateRoot` 校验，不自动chmod接管未知目录。

profile必填：`profileId`、`agentId`（等于manifest.canonicalAgentId）、`codexBin`、`codexHome`、`codexWorkdir`。保留现有profileId以免破坏旧报告scope。对原432议事能力，需匹配已有 `appServerEnabled/fastChatEnabled/chatEngine/typedDeliberationEnabled` 与真实受信CLI/schema；禁止仅改true宣称READY。

源码接点：[agent-client.mjs:6279–6336](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L6279) 实际启动/测量app-server；[agent-client.mjs:6641–6673](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L6641) 的durable/typed command/report能力不是一个通用online布尔值。

Provider凭据与Agent transport凭据分开：当前CLI调用不向 `providerEnvironments` 注入文件映射，不能在unified.conf添加任意变量就假称已传到子进程。先采用已有独立Codex HOME及原受支持认证；若真实适配器需要该Map而现有入口不能提供，记录该具体适配器为阻塞再设计最小接入，不临时继承整套process.env。

### 4.3 必要业务数据保全：不做历史版本兼容

新引擎固定状态入口为 [agent-client.mjs:6627–6632](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L6627)：`commandInboxDir = resolve(agent.stateRoot, 'inbox')`。原 `safeProfileDirectory`（892行）是agentId UTF-8十六进制，不是subjectKey；不能扁平复制。

- 原ledger/ACK根：[agent-client.mjs:6133–6139](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L6133)，相对 `<stateRoot>/inbox/<hex-agent-id>/`。
- report outbox：[agent-client.mjs:6174–6177](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L6174)，同根 `execution-report-outbox`；保留profileId/agentId/scope/原recordId。
- session map：[agent-client.mjs:6200](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L6200)，`<stateRoot>/codex-session-map.json`。
- ACK high-water：[agent-client.mjs:1984–1985](/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/agent-client.mjs#L1984) 旧格式拒绝，需要已有停止writer的显式迁移；不得把当前活动ACK专项迁移代码偷偷打进执行payload。

直接切换的数据处理规则：
1. 停止旧writer后备份原根的字节、权限、身份和在途记录。**备份不等于要求新Runtime读取所有旧格式**；已完成历史记录可只归档，不为它开发兼容层。
2. 当前installation授权、未确认ACK、已知未报告结果、未完成任务的去重事实必须保留。新契约已能读取的数据按既有路径接续；不能创建空state伪装“从未执行”。
3. 已STARTED但结果未知的记录不重新运行Provider；按原权威状态标识待处理，保全原证据。不得批量改终态、清队列或清sequence来使启动通过。
4. 对确有必要且格式不同的数据，优先已有经过验证的一次性离线转换；它不是运行时兼容。没有适用工具就列明**具体未完成记录和缺少的处置**，不把全部历史格式支持升格为必做开发，不盲改`formatVersion`或摘要。
5. 新Runtime始终只运行最新格式、最新认证；无旧协议fallback、无新旧双写。初始化会写state，不能对生产原件试运行后称“只读检查”。

### 4.4 HTTP/WS精确契约（已有，不改）

[SessionRequest.java:4–6](/home/isp/wsps/cyf/api/agent/jia-agent-core/src/main/java/cn/jia/agent/entity/AgentRuntimeV1SessionRequest.java#L4)：

```text
POST /agent/runtime/v1/session
Authorization: Bearer <该installation的rta1授权>
Content-Type: application/json
{
  installationId, tenantId, clientId, canonicalAgentId,
  manifestVersion, manifestSha256, hostId, runtimeInstanceId
}
```

八个请求字段均为string；本地manifest摘要带 `sha256:`，原 `identityOf()`（runtime-client.mjs:37–40）在请求时去前缀，不手工拼错。走现有client，不在shell命令参数/日志中放token。

`JsonResult.data`返回：上述四identity字段、hostId、runtimeInstanceId、正整数sessionGeneration、scheme=`AgentRuntime`、sessionToken=`rts1_<64hex>`、websocketPath=`/ws/agent/channel`、status=`CHANNEL_PENDING`。不含manifestVersion/manifestSha256，不把响应当READY。

WS与native请求由 [runtime-client.mjs:55–59,169–185](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/runtime-client.mjs#L55) 生成：
- `Authorization: AgentRuntime <sessionToken>`
- `X-Agent-Id`、`X-Agent-Installation-Id`、`X-Agent-Host-Id`、`X-Agent-Runtime-Id`、`X-Agent-Session-Generation`。
- 不带旧X-API-Key、不带query身份、不follow redirect；session proof只在内存，不落checkpoint。
- HTTP ACK继续 [runtime-client.mjs:190–200](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/lib/runtime-client.mjs#L190) 的 `/agent/runtime/v1/commands/{messageId}/acks`；不改回WS ACK或第二outbox。

失败行为：session400先核八字段/host proof；401/403核凭据与绑定，不无限重试；generation/installation/host冲突拒绝，不用SQL修成通过。只有原分类的transient network/HTTP走原退避。

### 4.5 表字段及允许状态变化（**零新增DDL，零手写业务DML**）

| 表 | 本次读取/既有服务更新字段 | 类型/约束与语义 |
|---|---|---|
| `agent_runtime_v1_installation` | `installation_id,canonical_agent_id,manifest_version,manifest_sha256,tenant_id,client_id,status,enrollment_consumed_at,runtime_authorization_hash,version` | ID/version字符串≤100、manifest摘要VARCHAR(72)、scope VARCHAR(50)、授权BINARY(32)、version BIGINT；原ACTIVE继续复用；不输出hash/secret，不创建替代installation |
| `agent_runtime` | `agent_id,tenant_id,client_id,owner_jiacn,binding_id` | 原identity/ACL绑定；不同subject不混用；不直接修改owner |
| `agent_runtime` | `runtime_installation_id,runtime_host_id,runtime_instance_id` | 3列VARCHAR(100) NULL；首次由既有session事务从NULL绑定；已有host冲突必须拒绝 |
| `agent_runtime` | `runtime_session_generation,token_hash,status,last_seen_at` | generation BIGINT NULL→正整数递增；token_hash VARCHAR(200)存verifier而非token；session签发先offline，真正注册后按原链更新；不能DML设online |
| `agent_task_bounty_bootstrap_outbox` | `bootstrap_id,task_id,target_agent_id,owner_jiacn,tenant_id,client_id,source_business_action_id,requirement_revision,assignment_revision,permitted_operation` | 原事项/来源动作/版本不改；判定DISCUSSION还是已授权执行，不伪造权限 |
| 同表 | `status,attempt_count,version,next_retry_at,lease_owner,lease_until,last_error_code,admitted_conversation_id,admitted_request_id,reconciled_at` | 原RETRY→CLAIMED→ADMITTED；成功时两个admitted ID非NULL，清error/lease/retry并有reconciled_at；版本及CAS由原服务推进 |

字段来源：[installation SQL:2–28](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-runtime-v1-schema.sql#L2)、[runtime schema:25–51](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/schema.sql#L25)、[fence SQL:2–5](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-runtime-session-fence-v1.sql#L2)、[bootstrap SQL:2–79](/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/resources/db/agent-task-bounty-bootstrap-outbox-v1.sql#L2)。后者具体约束以文件为准，不补造新的状态值。

既有签发逻辑 [AgentRuntimeAuthenticationService.java:53–104](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/security/AgentRuntimeAuthenticationService.java#L53) 已校验ACTIVE identity/binding/account并递增generation；正常第一次接入不需要清fence/转移API。不得重跑已经执行的13DDL或不适配的PhaseA脚本。

## 5. R3：一次直接切换统一Runtime（无兼容、无灰度）

### 5.1 安装与启动分开

1. R1自检后在干净固定源码生成候选，记录commit/tree/版本/Node/npm/Python与制品摘要。使用原 [install.sh:5–61](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/install.sh#L5)，不写第二个installer、不覆盖已存在target。
2. 原安装器参数为 `--target/--node/--npm/--python/--engine-root`，不是`--activate`。完整保留JS lock依赖与私有Python工具链；不借宿主已装包伪装完整安装。
3. 原 `validate.sh --root <artifact> --config <host-config>` 验完整payload/依赖/配置；原六格式工具链证据若精确输入一致才可复用。不得为了本文重复扩建隔离验收框架；生产业务验收直接在生产进行。
4. pip来源沿当前本机全局默认解析并固定实际生效URL与配置SHA；不读取已删除的项目专用env，不改在途批次。不因仅HEAD连通就声称下载或安装成功。
5. 使用原unit模板 [cyf-agent-runtime-v1@.service:1–24](/home/isp/wsps/chcbz/isp-install/conf/cyf-agent-runtime-v1/systemd/cyf-agent-runtime-v1@.service#L1)，实例最终为unified；本地Node固定20.20.2；exit78不盲重启。不得复制旧sidecar unit冒充统一执行引擎。
6. 路径占用、权限、发布锁、配置/原状态备份、恢复方法核对后才安装/切换。API/Web未改源码则不重发，本轮后端已有数据库变更不允许直接恢复旧JAR。

### 5.2 一次维护窗口内直接替换，不开发切流机制

1. **先备齐新版本**：三角色的最新配置、独立凭据、必要数据处理和完整制品准备完毕；不先切吴用再长期保留另外两角色旧入口，不新增动态迁移/热切换接口。
2. **备份并固定影响范围**：记录将停止的unit、PID/cgroup、各subject及其状态目录；保全配置和数据。新配置不能混入旧API key/旧sidecar运行参数。
3. **停止范围内旧服务**：正常停止吴用旧WS及HTTP sidecar，以及已确认属于本次替换范围的共享旧入口，核实实际进程退出、没有旧writer。允许短暂不可用；不等待所有历史任务自然完成、不按耗时盲强杀。未完成记录按§4.3保留处理。
4. **一次启用新Runtime**：用原installer/validate/unit交付后，启动 `cyf-agent-runtime-v1@unified.service`，三角色统一采用新认证和新执行契约；旧对应入口退出自动拉起路径，不与新Runtime并行。
5. **直接生产验收**：逐subject核session/WS/真实能力，随后续原432。失败修最新候选，不恢复旧认证、不增加兼容模式或新旧并行观察期。

停止清单的已知入口（执行前刷新实际状态，不把本表当执行回执）：

| 入口 | 影响对象 | 直接替换时的处置 |
|---|---|---|
| `codex-ws-agent@wuyong-local.service`、`cyf-agent-runtime-v1@wuyong.service` | 吴用旧WS和旧sidecar | 本次替换范围内一起停止，避免漏停其中一个 |
| `codex-ws-agent.service` | 林冲/卢俊义与managed公孙胜共享 | 先明确整个unit的影响范围；覆盖本次授权的主体可在同一窗口停旧换新，但不能把“无需版本兼容”解释为可以删除/终止其他聊天任务 |
| 公孙胜等共享主体 | 原独立owner/任务/状态；历史快照缺自身native installation | 若一起替换，先准备其自身合法新身份和配置，不能借三角色凭据；未纳入范围则明确共享unit的归属冲突，不重新引入逐profile灰度方案 |

**取消上一版的热重载/逐角色安全窗口路线。** 旧磁盘 [agent-client.mjs:6050–6065](/home/isp/apps/codex-ws-agent/agent-client.mjs#L6050) 的busy重载会触发全进程shutdown，现不再使用热重载作为切换手段，也不为旧入口补功能。共享主体的权限和真实身份是一次停旧换新的输入，不是版本兼容要求。存在实际范围冲突时只报告具体unit/主体/所缺条件，不以抽象“安全切流”框架延长开发。

### 5.3 启动后必须逐层核对

顺序：`配置校验 → 原授权session成功 → native WS升级 → agent.register有效回执 → protected executor/typed能力实际READY → 原业务链`。

每subject留存脱敏证据：完整subject、installationId、hostId、boot、generation、注册回执身份摘要、durable状态、实际readyCommandTypes/typed声明与失败分类。不要存sessionToken/Authorization/Cookie。

- 旧入口不得与新subject并行执行；状态锁失败时等待归属核对，不抢锁。
- 进程active、安装成功、HTTP心跳成功、WS101分别只是中间状态。
- 新认证失败不启用旧key fallback，不恢复旧Runtime。优先修正新配置/最新候选后重启新Runtime；安装失败按原安装器恢复本次文件变更、保留数据和诊断。不能把文件恢复当作授权重启旧协议服务；没有可用新候选时如实报告暂不可用。
- 关闭未确认/结果未知时保留state/锁/备份，不删除根目录或清空账本。

## 6. R4：原事项432的验收与最小故障定位

### 6.1 固定原业务，不重造成功样例

- taskId=`432`；历史bootstrap=`bootstrap_1180917ac6aacaae87a6fc37d7509e1b`。执行时重新核对当前owner/scope、taskVersion、指派与原sourceBusinessActionId。
- 继续原用户会话、原事项详情和原议事；不创建新任务、不重新点将、不手动SQL设ADMITTED，不手动重放原bootstrap，不发送无关聊天掩盖自动接续失败。
- [ChatBountyBootstrapRelay.java:84–135](/home/isp/wsps/cyf/api/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyBootstrapRelay.java#L84) 已有runtime-not-ready的原lease释放/退避；能力恢复后应由同一relay继续，不需新增cron/MQ/重试服务。

### 6.2 纠正“必须立刻有正式成果”的错误判据

[ChatBountyBootstrapAdmissionService.java:128–153](/home/isp/wsps/cyf/api/chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyBootstrapAdmissionService.java#L128) 对 `permittedOperation=DELIBERATE` 创建typed DISCUSSION，明确**CHAT无执行step，不制造执行ID**。

因此分开判定：
1. **恢复判定**：原bootstrap ADMITTED，关联原conversation/request，Agent真实响应，刷新/重登后结果仍存在；没有重复turn。此时可称“原议事已恢复”。
2. **办事执行判定**：若原事项已有合法执行授权，沿原执行链继续；若只有议事授权，用户从已有界面确认执行后再进入该链。不得把“等待用户正常确认”当Runtime缺代码，也不得替用户扩大执行授权。
3. **成果判定**：原授权执行完成后，`GET /agent/tasks/432/formal-deliveries`、`GET /agent/tasks/432/deliverables`与实际内容一致，可查看/下载，且刷新后持久存在。没有进入执行时列表为空不能单独证明开发缺陷。
4. **验收判定**：正式验收/拒绝/扣费等沿原用户操作及授权；不为了绿灯自动POST `/formal-deliveries/{deliveryId}/decision`。报告停在哪一步，而不是把ADMITTED或API200当全闭环。

接口源码：[AgentTaskFormalDeliveryController.java:93–142](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskFormalDeliveryController.java#L93)、[AgentTaskDeliverableController.java:65–103](/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentTaskDeliverableController.java#L65)。不新增前端按钮或数据库结果表。

### 6.3 出现断点时只处理所在层

| 最早失败点 | 首查代码/输入 | 不做什么 |
|---|---|---|
| session400/401/403 | 原manifest/authorization与8字段、host fence；runtime-client.mjs:169–177，API签发服务:53–104 | 不改API允许旧key，不重复enroll |
| WS已连但无注册确认 | execution-adapter.mjs:39–100、registration observer、当前generation | 不伪造回执/READY |
| 注册成功但typed不READY | 独立Codex HOME/二进制与实际app-server schema/适配器；agent-client.mjs:6279–6336 | 不用普通TASK能力冒充typed议事能力 |
| READY但bootstrap仍RETRY | 原next_retry_at/lease/error、relay是否运行及scope；Relay:84–135 | 不加新retry runner、不直接改ADMITTED |
| ADMITTED无响应 | 原request/turn/outbox/WS业务回执和Provider实际调用 | 不新建会话重试，不借另一个Agent身份 |
| 正常议事后无正式成果 | 先核permittedOperation/用户执行授权/原执行状态，再查结果报告 | 不把“还未授权执行”当交付代码bug |
| 具体上下文/文件恢复被拒 | 保留精确path/status/command/checkpoint，采用完整缺口详设相应最小切片 | 不无证据扩大到全部F01/所有恢复框架 |

本次必要的后端认证/relay契约已经实现；没有实际新断点不改Java、SQL或Web。若必须改API，先读受影响build.gradle，再走原orchestrator定向测试/validateLayering和本地版本化发布；若改Web，正式发布走Flow4403172。

## 7. 交付顺序、接续输入与最终DoD

### 7.1 可以直接派给Owner的任务

1. **Runtime Owner：R1编码**。输入为§2 Runtime SHA、§3指定函数/测试；输出为最小源码diff、定向与相关回归结果、新commit/tree。不改API/Web/schema/安装协议，不操作生产。
2. **Main：R2准备**。可与R1并行只读核manifest/逐subject状态/共享服务归属；输出已有handoff中的映射和阻塞。无须等代码完成才查输入，但不在旧writer live时移动其state。
3. **Main：R3直接替换**。新制品与范围内各subject配置备齐后，使用原installer/validate/unit，在一个维护窗口内停旧、启用唯一unified Runtime；不灰度、不先切单个角色、不保留旧版运行分支。保留备份、停止确认和其他主体权限边界。
4. **Main：R4生产实测**。沿原432自动bootstrap和原授权动作续验，记录每层真实结论；发生新断点回原Owner定向修复，不新增Reviewer或巡检框架。

当前明确仍缺的运行时输入（本文不捏造）：三主体凭据真实session有效性；当前fence值/host归属；每个旧writer的精确在途/ACK格式与交接目录；共享服务一次停旧换新的影响范围；protected executor当前真实typed能力。它们属于生产接续输入，**不是先增加功能的理由，也不能以文档已写好宣称已取得**。

### 7.2 最终核销清单

- [ ] R1新增测试先覆盖原缺陷，修复后通过；原停止/锁/ACK/身份隔离回归保留；记录所有skip。
- [ ] 原安装器交付固定新Runtime制品，配置与逐subject原凭据/状态匹配；未重发未变API/Web，未新增DDL。
- [ ] 吴用/林冲/卢俊义一次切换到同一Runtime，完整subject分别持有自己state/凭据/session；旧对应writer已退出且不再自动拉起，无双执行、无灰度/兼容模式。
- [ ] 一个subject注册等待/撤销不阻止健康subject心跳；无效subject不得接单。
- [ ] 共享unit受影响主体均已核对范围；未误停其他聊天任务、未共用身份；纳入切换的主体只运行新版本，未恢复的主体如实报告。
- [ ] 原432自动bootstrap/议事恢复；执行/成果/验收按原授权逐层记录。若需用户正常确认，明确下一操作，不假报业务全部完成。
- [ ] 在途未知结果没有重放；原ACK/已知结果按既有幂等链恢复；无身份绕过、锁抢占或凭据泄露。
- [ ] 更新现有handoff与任务状态，来源、源码完成、安装完成、业务恢复、最终三主体统一分别记账；不以本文产出核销实施。

证据写入现有任务目录，不另建框架/长期台账。本文是**必做项实施设计，不是实施成功回执**。
