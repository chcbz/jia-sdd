# CODEX-BRIDGE-REPAIR-20261026

Owner：当前单 Agent。2026-10-26用户授权“现在就改，顺便把这次的问题修复”。

## 固定范围与基线
- Runtime `/home/isp/wsps/chcbz/isp-install`，`codex/architecture-convergence-runtime`，base `336d92c2ad97afd3c7ac0979873eb4e324fff574`。
- API `/home/isp/wsps/cyf/api`，`codex/architecture-convergence-api`，base `9be98646383a6a3d55511d59faf9be0cd741303f`。
- Web复用 `/home/isp/wsps/worktrees/architecture-convergence-web`，`codex/architecture-convergence-web`，base `e43d8bc6914330ce00a7d75abe95f73cb1e24b71`。
- 共同接口规范 `api/docs/interface-standard.md` v1.4；保留现行v5不可变成果报文和v6读取投影，不改历史摘要。
- 目标：codex-ws-agent源码/安装路径改称codex-bridge；精确媒体成果替换；失败规划回合不阻塞后续发送。
- 非目标：通用codex-adapter抽取、新UI、多区域、无关校验清理、401未定位故障重构。保留无关dirty与现有工作区。
- 原ARCHITECTURE-CONVERGENCE任务未在09:00前完成验收；本任务不重标原整改完成，不执行未经确认的回滚。

## 修复合同
1. ACTION_REQUEST可REPLACE冻结deliveryTargets中的真实outputSource成果批次，必须同时带targetOutcomeId/targetFinalDigest。ANSWER仅替换文字。父链、任务/指派、ACL、摘要、实际执行输出验证不删除。
2. REPLACE是在真实执行完成后替换目标outcome的全部保留输出，保留其他文字/媒体，不按文件格式特判。执行失败/未知/未完成不删除旧成果、不伪造replaces来源、不自动重放Provider。新增成果来源仍为真实execution输出。
3. 无outcome且权威turn FAILED/CANCELLED时读取返回该终态，而不是PENDING。存在digest却无outcome仍视为事务不完整；UNKNOWN/PARTIAL不视作可忽略失败。前端只忽略已验证空终态；终态不被迟到PENDING覆盖。
4. 改名仅程序目录与活动引用。历史日志、摘要、旧发布记录不改写；运行时身份/state/ACK/codex-home不迁移。生产实体app不变；新候选内部使用codex-bridge。生产迁移必须同批制品、重建绝对路径工具链、备份/锁/可恢复安装；源码rename不代表线上已迁移。

## 验收与证据
- 最早定向：既有Runtime outcome/model-schema回归、安装脚本语法；Web状态投影与发送回归；API真实输出保留链回归。
- 正式测试/构建走既有Flow，单Run≤600秒。本次三组件正式CI已通过（见下表），未安装新候选。
- 业务：task530失败历史之后可发新消息；吴用对红圆执行绿圆替换，保留文字；PC/移动预览及验收。不能用APPEND冒充替换。
- 源证据：`specs/architecture-convergence/evidence/task530-root-cause-reproduction.json`。
- 仍未闭环：API重启后通道connected但401的具体解绑触发；本任务不声称已修复。

## 2026-10-26 收口：源码已集成，生产未部署

| 组件 | 已合入远端develop | 正式Flow | 结果 |
| --- | --- | --- | --- |
| API | `516267bf7b19bfc03581ae580704af9246ffb622` | `5260799/324` | 选定回归、分层及bootJar通过；约254秒 |
| Web | `86698d4e2e871315fbb1fe045c7117b7f5b5f991` | `4403172/323` | 3344通过、2项既有pending；约122秒 |
| Runtime | `d97449ca0b5085d97e589e3a821746d968f9e7c9` | `5264702/63` | 538通过、0失败；约252秒 |

Runtime正式Run固定源码为`5695a68a3025c243769ee9cababe776a261156fa`。随后d97449c仅修改根安装入口旧别名拒绝、对应既有测试及自托管说明，8项定向检查通过；制品内97个非依赖应用源文件与develop逐字节一致。不能把Flow63写成验证了d97449c完整tree。

- Runtime候选1.3.11，内嵌codex-bridge 1.1.5。task530原失败输入离线重放已通过schema及Runtime校验；没有执行Provider，不代表已生成绿图。
- 三条Flow配置均已恢复原值并读回核对。远端develop三项提交于收口时再次只读确认。
- 失败Run如实保留：API322/Web322为CI分支准入限制；API323为本次CI候选生成器错误截取嵌入bundle，修正并检查shell/嵌入Python后API324通过，不是应用功能回归失败。
- 脱敏证据：`specs/juyiting-skill-execution/evidence/codex-bridge-repair-20261026.json`。私有完整日志/制品：`/home/isp/state/architecture-convergence-20261026/bridge-repair/`。API制品未另行下载核验摘要，不冒充安装证据。

### 剩余发布与验收

1. 本次Run均为CI-only，无生产安装。最近已知生产API1.17.8、Web1.16.50、Runtime1.3.10及旧内嵌目录仍是旧发布基线，不作为本次实时健康证明。
2. 新生产发布应固定授权与版本，按 **Web → API → Runtime** 顺序，使消费者先兼容新终态和媒体替换，再切换生成方。Web/API须为本次发布正确升版，执行同Run构建/制品/受控安装，不将已有CI-only制品擅自跨Run安装。Runtime迁移遵守备份、锁、固定app、绝对路径工具链及状态保留要求。
3. 发布后以ziyue/吴用验证task530可继续发送、红圆改绿圆并替换原媒体且保留文字、PC/移动预览与验收；不重放历史Provider，不以离线fixture或APPEND代替真实业务通过。PDF按用户要求不验。
4. API重启后connected/ready但HTTP401的服务端解绑触发仍未定位，本次未扩修；原架构整改不得据此重标完整验收或按期完成。
