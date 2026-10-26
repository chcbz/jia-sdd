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

## 2026-10-26 用户“继续”授权发布

- 本轮按Web→API→Runtime推进生产发布与原业务验收；仍由当前单Owner执行，不扩展401根因专项。
- 发布固定候选：Web1.16.51 / `1e1f94a488a04014841527fac22cd3a931581b4c`（仅package及lock升版，已FF到develop）；API1.17.9 / `516267bf7b19bfc03581ae580704af9246ffb622`（版本由既有部署记录绑定）；Runtime1.3.11 / `d97449ca0b5085d97e589e3a821746d968f9e7c9`（内嵌codex-bridge1.1.5）。
- 发布证据私有目录：`/home/isp/state/architecture-convergence-20261026/bridge-release/`。原Flow配置先保存，单次Run受600秒总上限监控，安装使用同Run制品；未到终态不声称已部署。
- Web324在应用测试前失败：修复分支CI脚本仍限定`codex/architecture-convergence-web`，实际发布输入为develop；部署作业未执行。已保存原Run和日志、恢复配置后将分支检查修正为本次develop输入再启动，不按原输入盲重试。
- Runtime沿既有受控安装器准备候选：保留身份/state、锁、旧程序/状态备份与失败恢复；仅将生成的Python venv四处已识别路径从旧内嵌目录更新为新目录，记录前后摘要，并在暂存及最终实体位置校验。此说明不是安装成功声明。
- Web325测试/构建通过，但制品元数据身份检查仍限定修复分支：首次修正只覆盖shell分支检查，遗漏了制品校验。本轮Owner责任，部署未执行；已改为复用原develop正式CI整段而非继续逐处改名。Web326随后正式测试/构建/安装成功，总耗时约185秒；同Run制品SHA-256 `3d8314d01037378b831aaf6155dc5a2f47c8e7ab39f2d040d1f456b4dc63fdf8`，11项线上入口/JS/CSS（含聚义厅懒加载模块）与安装清单字节匹配；Flow配置已恢复。API325已启动，Runtime尚未安装；后续状态以最终证据为准。
- API325正式测试/构建/安装成功，安装JAR与同Run留存归档一致，健康端点UP，规范路径8项只读检查通过，Flow配置已恢复。实际任务530失败回合经浏览器读取为FAILED、outcome/actionProgress为空（2026-10-26T02:50:37Z），不是PENDING。
- Runtime64未部署：镜像dnf刷新alinux3-plus（42MB）、updates（41MB）等仓库元数据消耗约5分钟，构建330秒受控超时，安装作业INIT，原Runtime未改。该Run约396秒终态FAIL；控制面曾返回一次ServiceUnavailable，只恢复同Run只读监控，没有重复启动。候选已按实际依赖来源缩到alinux3-os与alinux3-updates，保留gpgcheck、全部538回归和总600秒上限；不是削减测试或搬回本机构建。

## 最终收口：三端已发布，本次业务验收通过（2026-10-26）

- Web1.16.51 / `1e1f94a488a04014841527fac22cd3a931581b4c` / Flow `4403172/326`；API部署版本1.17.9 / `516267bf7b19bfc03581ae580704af9246ffb622` / `5260799/325`；Runtime1.3.11、bridge1.1.5 / `d97449ca0b5085d97e589e3a821746d968f9e7c9` / `5264702/65`。源码已集成develop，三个部署单均Success、主机healthy，配置均恢复并readback。
- Runtime65完整候选538/538通过，覆盖d974完整源码；约401秒，Web/API成功Run分别约185/440秒。固定实体`/home/isp/apps/cyf-agent-runtime-v1/app/codex-bridge/`已启用，旧组件目录不存在，身份/config保持不变；备份保留在`/home/isp/baks/cyf-agent-runtime-v1/20261026-codex-bridge-repair/`。安装快照的业务pending字段保留其当时事实，最终业务结论以本节独立证据为准。
- ziyue/吴用/task530：原失败回合读取FAILED；原会话成功发送一次改图请求；真实ACTION_REQUEST精确REPLACE红圆成果，执行COMPLETED，1536×1024绿圆白底，保留原识图文字。已检查实际图像及像素，不以模型回复代替执行结果。
- PC、390×844移动端预览/放大/关闭通过。移动端仅选原文字与新绿图，2026-10-26T03:13:59Z确认验收。恢复独立验证浏览器并重新加载后，首页与事项详情均显示已完成、吴用、2份成果；原红图仅保留历史。未捕获验收HTTP响应，不编造响应或交付清单。
- 浏览器旧进程在验收后退出，原因未明；复用原profile恢复，未操作其他任务浏览器。验证脚本修正了同Run包留存路径、测试日志格式及空输入发送按钮判断，没有因此再次发布或重复发送。
- 脱敏完整证据：`specs/juyiting-skill-execution/evidence/codex-bridge-release-20261026.json`。PDF未验、401具体解绑触发未定位；不能据本次通过宣称全站/多账号验收或原架构整改按时完成。
