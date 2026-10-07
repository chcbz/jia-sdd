# 典籍阁 Agent 任职与内容维护：源码交付记录

日期：2026-10-01。当前状态：**implementing / NOT_COMPLETE**。以下提交与测试为已推送的上一轮局部基线，不是完整特性完成证明。独立审计确认的源码缺口及串行修复顺序见 [completion-audit.md](completion-audit.md)；旧局部结果保持不变。
用户请求中的无前缀 `archive-agent-maintenance` 在远程不存在；沿用已有设计分支 `codex/archive-agent-maintenance`，不混入其他任务 develop 更新。
原工作区 `D:/workspace/chaoyoufan/project/cyf-web-kit` 未被覆盖；实施在独立工作树，未部署、生产激活、真实典籍上架或调用付费模型。

## 1. 可复现组件提交

| 仓库 | 远程分支 | Commit | Tested tree |
| --- | --- | --- | --- |
| API | codex/archive-agent-maintenance-api | `62223001dfeff648989efb0a79a6e28addb404a3` | `fbc4a8f9b89c0bb410fcd7df5e3f8590fb17cbb5` |
| Web | codex/archive-agent-maintenance-web | `bdff47863a99318a991e2dffb6073b8db872b5fc` | `b3d0ac34e4a08a75d1d6420d702d19264126becd` |
| Client (isp-install) | codex/archive-agent-maintenance-client | `bc035b3757b97aac90c59c06386a7ebfa3d71162` | `191d8fc8d6285d3f0614a656f729657688a29204` |

三个组件均先提交/普通 push，再用 `git ls-remote` 核对 exact SHA；原件 `evidence/delivery/component-remote-verification.json`。根仓随后 pin API/Web gitlinks 与 Client SHA，运行 `sddw verify` 后提交/推送同名根分支。根仓提交基线 `01f7599ed28e84c1a44d2cc6c3dec13f7ddbeb67`；最终 root SHA 由推送回执报告，不能自嵌。

## 2. 实现范围

- 通用多书/不可变版本 Reader 与兼容迁移，保留旧水浒字节、ID/hash/anchor及私人数据隔离。
- 服务端任职、岗位/书目范围、管理/native分道鉴权、撤任与发布事务、CAS/幂等/恢复/取消。
- 平台维护技能目录、安全安装/回执、实际受控 command 路由与 Client NativeRunner；复用共享执行/存储/安装底座，不创建第二套调度或收费技能订单。
- 草稿、确定性校验、MANUAL显式管理发布及AUTO授权交集、唯一publication/event与真实Reader读回。
- 宋江受限工具与直达任职Agent通道；Web管理面板/授权重查会话卡、权限撤销清理、404降级和未确认/恢复状态。
- API `archive.maintenance.execution-enabled`、平台安装/catalog gate、Client安装/维护执行gate仍默认关闭，需部署环境和精确业务授权后启用。

## 3. 实际验证与未通过项

| 验证 | 实际结果 | 原件 |
| --- | --- | --- |
| API强制隔离MySQL四套（全程共享Gradle lock） | 定向173/173PASS；archive258/247PASS/**11既有FAIL**/0skip，Gradle exit1 | evidence/native-lifecycle/final-api-regression/ |
| Web六真实selectors / production build | **245/245PASS**、0skip / exit0 | evidence/web-wiring/web-final-attempt3/ |
| Client exact Git archive Linux full npm test | 443/442PASS/**1既有FAIL**/0skip，failure delta空 | evidence/client-runner/archive-runner-attempt3/ |
| 有界真实HTTP/JDBC/POSIX/Client跨组件夹具 | **1/1PASS**、0skip；MANUAL/AUTO/replay/唯一publication+event/Reader读回 | evidence/crosscomponent/crosscomponent-fixture-attempt5/ |
| 历史文档checker | **exit1**，client_historical_source_sha256:agent-client.mjs | evidence/documentation/delivery-history-audit/ |

API最新与直接已批准66061b5树 comparison：全部套件 introduced=[]、removed=[]，before/after相同且fresh XML，无stale。Client唯一既有失败是 `test/config-runtime.test.mjs#post-rename session-map failure reconciles committed disk state before later writes`。不声称全回归绿色；历史246 proof源hash不改成当前值造绿，当前提交/pin检查单独记录。

独立只读复审：Web最终范围、Client runner修复、API recovery-context及跨组件fixture均局部 ACCEPT，最后fixture P0/P1/P2=0。每份原回执带scope；不外推成全功能安全认证。失败轮、REJECT和修复后原件均保留。

## 4. 有界 fixture 的精确边界

真实组件：Tomcat/DispatcherServlet HTTP、admin/native/reader Controller、runtime filter、MaintenanceService、JDBC store/transaction、Linux POSIX私有artifact、production command codec、Client approved ZIP/19-entry证明/真实atomic activation/NativeRunner。
Prerequisite doubles：identity/bootstrap/account、registration、execution admission/command transport、installation download/result transport。没有真实Rabbit/WebSocket握手及active-slot/outbox全链，**不是完整Runtime E2E**。

最新Node selector由API tree `fbc4a8f9...` 的Git archive导出；Java沿用attempt4编译tree `4e9598...` 的相同blobs/JVM。两个tree的唯一差异是Node fixture resolver参数，source-binding明确记录，不能称全部JVM由最新tree重编译。final-result passed后核验自有PID/mainClass并TERM释放资源；launcher shutdown退出码不是fixture判定。

批准技能v1.0.0保持19 resources / ZIP40563 bytes / SHA256 `8894d96341067dd7f9e2f45696eef44057dc61346255a0323b2d713a3c7ea081`。批准负例刻意包含尾随空格/CRLF，部分源码保留EOF空行，因此完整diff-check有警告（原件保留）；排除byte-addressed包并仅忽略EOF空行的其余check通过，未改批准字节或冻结tree。

## 5. 未执行与下一步

84项 `acceptance-cases.json` **全部not_run/evidence=null**。真实管理员/吴用binding/底本与公共发布用途授权、真实Runtime全链/真实浏览器与设备交互、部署与实际《三国演义》上架均未执行。下一步须单独核对环境与授权，再做部署前Runtime验证和业务验收；Git push不构成这些授权或成功证据。


## 6. 最终交付一致性与资源清理

`sddw verify archive-agent-maintenance` exit0，API/Web pins与当前commit一致。单独current-delivery gate实际通过109项提交/tree/远程SHA/gitlink/XML digest/失败delta/原始fixture字节/业务not_run一致性检查；它不重跑应用、不替代失败的历史checker或真实业务验收，原件 `evidence/delivery/current-delivery-check.json`。

首次current gate发现Node selector SHA标签误用：原记录f5e3为Windows mixedEOL disk bytes，不是运行文件。实测Git blob SHA3c1aa、Git archive导出/实际Linux运行SHAc07144，差异逐字节证明仅CRLF转换；批准技能包不变。原绑定与原review均备份保留，正确字节绑定及实际导出tar见 `evidence/crosscomponent/crosscomponent-fixture-attempt5/selector-byte-binding-audit.json`。

有界fixture自有Java已停止；Windows host-only DB relay经独有脚本路径+PID+监听地址核验后停止。原exec stdin已关闭，未恢复accepted/rejected计数，不编造；清理回执 `evidence/delivery/owned-relay-cleanup.json`。没有停止隔离MySQL或其他任务服务。

根仓 evidence 目录以 .gitattributes -text 保留原始字节；2373份已stage证据逐一核对磁盘原字节与Git blob相同（见staged-evidence-byte-proof.json）。Windows深层证据路径需Git core.longpaths=true；本次仅使用命令级 -c core.longpaths=true，未修改系统或全局Git配置。


## 7. 当前用户交付顺序（2026-10-03）

本文件前六节是已推送旧局部基线的历史事实。当前增量遵循 `delivery-order.md`：原规格功能源码收口并更新文档 → 本地必要定向自检 → 组件特性分支提交/push与远程SHA核验 → Root更新gitlinks/pins并push → 服务端全面验证与必要后续修复。全面本地回归、Runtime/browser不再是首轮完整源码push前置条件；“开发完成/已推送”和“服务端全面验证待执行/结果”必须分开声明。现阶段功能缺口仍在实现，新完整源码交付未完成。

## 2026-10-07 最新接续（覆盖历史当前状态）

原D2源码与文档已收口并普通推送，全部局部源码包独立接受。API `5722e7fa2ee0d1f6a5eeb84ccf18dcfe009ae4e7` / Web `6dd4553c276c34a1d694a06a3daf11849dca0e64` / Client `9426030d4a9411429bbc1ad2bd154356a0287e3b`；Root源码交付提交 `8d77bcd325bd3cb4e6d589bc6add8071a3ceb09b` 已核对远端。最后生命周期Client Linux104PASS，API同树Chat76PASS及Agent17Windows环境失败原件保留。

**服务端全面验证 BLOCKED，尚未完成。** 独占工作区已检出上述精确源码；attempt1–3配置失败且tests=0，attempt4主动停止本任务JVM，attempt5最后观察到compileJava，其后退出码/XML/结果与自有进程、MySQL关闭和Gradle锁释放均未确认。前次SSH曾公钥认证成功但session open超时，本次只读重试仍exit255/连接超时；不据此认定认证错误或唯一资源根因。完整回归、实库迁移/并发selector、真实Runtime/浏览器结果不可标PASS，远端原始attempt日志尚未取回。

原件 `evidence/delivery/resume-20261007/{root-source-remote-receipt.json,server-validation-status.json,ssh-resume-readonly-20261007.log}`；恢复后先只读核本任务进程parent/cwd/argv、独占datadir及锁，不能按旧PID盲目kill或重启生产。准备脚本不是已完成验证，运行前须重新绑定真实完成尝试与精确源码。生产发布/迁移/真实任职与上架/付费调用未执行，84业务用例仍not_run/evidence=null；whole-feature accepted=false。
