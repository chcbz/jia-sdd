# SKILL-UNKNOWN-BACKOFF-20261022

- Owner: 当前聊天 Codex；2026-10-22（Asia/Shanghai）。已读取 CYF AGENTS.md、ops/orchestration/README.md、组件 AGENTS.md；不委派。
- 范围：Runtime UNKNOWN 逐执行退避、安全错误诊断及定向回归；不改 API/wire、权限/租约/幂等，不重放未知副作用，不安装或重启生产。
- 组件：/home/isp/wsps/chcbz/isp-install；原本地 HEAD 5e8742aac6b9261a8d6cc94f77da1175e8ae74e2；本日实际查询并 fetch 的远端 develop 0e96676d80e1c10917376a99ce2322ce7951c968，作为候选基线，tree 58d4b8a589808c368940a565b351be58e0c61ce3。
- 独立 worktree：/home/isp/wsps/chcbz/isp-install-worktrees/skill-unknown-20261022；branch codex/skill-unknown-backoff-20261022。不改原工作区。
- 固定接口：/home/isp/wsps/cyf/api/docs/interface-standard.md，v1.2，SHA256 7dc50a51b5c3faa2d5311dd0f749ed2000365c34febc3c3714ba2a945180548f；本次无 wire 变化。
- 线上观察：1.2.4，进程使用 releases/1.2.4；不等于本次候选。吴用 UNKNOWN 为本地持久化状态、无 result/receipt。此次不更改记录。
- 最早定向验证：node --test conf/codex-ws-agent/test/skill-conversation.test.mjs 与新增诊断测试；覆盖其他执行不饥饿、延期无重处理、退避到期、恢复清理、安全异常立即停止、重建不重放外部调用。
- 前后端不变，不启动其测试/构建；Runtime 本地 Node 回归为源码证据，非部署证据。
- 定位/实现/验证/等待耗时：未统计。

## 自检与候选收口

- 源码提交 `2d7650a77b058c7d80bec95e5511ef1faf6126cb`，tree `6f4ea323b263a3a984a3ceaf8441fb1683dcbcf3`；Runtime 候选版本 1.2.5。后续 `7b37f5b` 仅追加现有运维文档的局部核对说明。
- Node 定向源码回归：diagnostic + skill-conversation + skill-execution-store 共33通过；skill-local-script 10通过；Runtime payload catalog 定向1通过（86项按 selector 跳过），共44通过，无失败。agent-client 语法检查、git diff --check 通过。
- 最终证据：`specs/juyiting-skill-execution/evidence/unknown-backoff-20261022/` 三份日志；非生产制品/上线证据。早期42项日志不作为最终输入证据。
- 范围实际：UNKNOWN 单执行内存退避，12–15秒起步、最高240–300秒；冷却期不调用 process，不阻塞其他任务；非 UNKNOWN 不吞错，安全边界异常立即停止；重建 lane 仍不重放已记录 effect。诊断区分 ABSENT/REDACTED、保留安全结构码/退出码/信号/执行ID/首次effect异常阶段；payload catalog已纳入新增模块。
- 边界：仍有每3秒 inbox查询及本地checkpoint扫描；到期恢复仍走原完整路径，未新增轻量服务端查询协议。退避不持久化，重启核对一次；不宣称CPU实测改善、不宣称首次历史异常已找回、不宣称卡住任务已恢复。未安装、重启、改线上配置或删除任何执行记录。
- 下一步：如发布，按Runtime既有版本化安装与激活说明固定上述候选、制品摘要，核验实际进程与channel后再做负载/日志对比；不能把本地测试当成已上线。
- 集成结果：已普通 fast-forward push 到组件远端 develop，readback `7b37f5b2b09672c1e989c4284555d27e425068f4` / tree `401c5320c059251458fc8f704cbab39fdfa0d347`；独立候选工作区干净。未切换或覆盖原组件工作区，也未触发部署。

## 用户指定联合发布（2026-10-22）

用户要求：Runtime 1.2.5 合入“排查 metadata OOM 原因”聊天一起部署，由该聊天统一协调发布；本聊天不单独部署或重启。

接收 Owner 请读取本 handoff、/home/isp/wsps/cyf/AGENTS.md、组件 AGENTS.md、/home/isp/wsps/chcbz/isp-install/docs/cyf-agent-runtime-v1-self-host.md 及上述固定接口规范。Runtime 改动已在远端 develop：源码 2d7650a77b058c7d80bec95e5511ef1faf6126cb，含文档集成点 7b37f5b2b09672c1e989c4284555d27e425068f4。基线包含这些提交时不要重复 cherry-pick；若联合候选增加源码需固定新的 commit/tree，重新核对受影响验证和版本，不覆盖已有不可变制品。44项本地源码回归及证据路径见上文；未生成本次生产制品、未安装激活，线上观察仍是1.2.4，发布前重新核验。前后端若随OOM修复发布仍遵守Flow正式路径，不将Runtime测试代替前后端Flow证据。

交接状态：本聊天已记录用户意图；本轮工具发现未提供 list_threads/send_message_to_thread，尚未向目标聊天实际投递，也未取得接收确认。不要将此记录当成目标Owner已接单或联合部署已完成。

### 联合发布 Owner 已接收（2026-10-22）

PDF-SKILL-20261022 本聊天已读取并接收上述交接及用户联合部署授权；组件规范与接口 v1.2 已核对。已 fetch develop 并通过 merge 纳入 `7b37f5b2b09672c1e989c4284555d27e425068f4`，没有重复 cherry-pick。仅文档追加位置冲突，保留双方说明；版本均为1.2.5。此前基于旧 develop 的本任务制品仍在临时 stage，已精确停止该 stage 的依赖安装，由安装器清理；`releases/1.2.5` 尚未生成，没有覆盖不可变制品。将固定联合 commit/tree，以 Node24.22.1 覆盖 UNKNOWN/诊断/local-script/PDF 与载荷目录回归后再准备和激活；当前仍未上线。

### 联合发布激活核验（2026-10-22 18:00 +08:00）

联合 Runtime 1.2.5 已激活，源码 `6c2cadc6d2e30c711cf682be0e70eef6d1a34c89` / tree `ca8d24a0919c86bff076ce3803ca3410444c4561`（含7b37f5b，已在远端develop）。真实制品 `/home/isp/apps/cyf-agent-runtime-v1/releases/1.2.5`，Node24.22.1；systemd unified PID699562。停写完整备份后切换，三Agent通道registered/ready及新鲜presence ACK通过，current已原子更新；身份与配置摘要未变，原image-edit RESULT_UNKNOWN数据库记录逐字段未变、不清理不重放。日志实际出现新安全diagnostic；尚未作稳定窗口CPU对比，不宣称原未知执行恢复。

机器可读记录 `/home/isp/apps/cyf-agent-runtime-v1/release-records/1.2.5.json`，manifest SHA256 `a41ed11c1e8731594fbc8732ac46f8e397fc8a79e975420e621f1cb2de9bb3cf`；通道证据 `/var/tmp/cyf-pdf-skill-20261022/release/continued/runtime-channel-health.json`；恢复备份 `/home/isp/baks/cyf-pdf-joint-runtime-1.2.5-20261022/`。新付费Provider/业务事项未提交。API/Web配对发布仍等待API正式Flow通过，不把Runtime上线等同于整批上线。其他Owner旧Node进程未强制重启，全系统实际进程收口尚未完成。
