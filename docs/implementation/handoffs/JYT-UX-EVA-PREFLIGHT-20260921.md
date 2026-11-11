# eva隔离构建预检交接（2026-09-21）

## 已授权与实际尝试

用户允许尝试在Codex的eva远程项目新建测试打包任务。授权不扩大到生产写入、Provider或部署eva现有服务。

- `list_projects`确认eva项目 `/home/chc/wsps/cyf`，projectId `0d05e42c-1080-4194-98d6-93c2f67c9ad1`，hostId `remote-ssh-codex-managed:eva`。
- 向该hostId的只读任务记录查询成功；这不证明当前远程命令执行、资源或构建能力已核实。未读任务正文，未复用/恢复任何无关任务。
- 当前工具检索未提供可调用的`create_thread`或`send_message_to_thread`。没有创建任务，不能报告已派发。
- 业务主机`ssh -G eva`只有默认hostname eva/user root/port22，无主机别名配置；本机名称解析无结果。一次保留StrictHostKeyChecking的BatchMode SSH探测退出255：`Could not resolve hostname eva: Name or service not known`。没有到达远端或进行登录。
- 没有安装软件、发起构建、生产DB/Provider调用或改动线上服务。后续需通过桌面手动创建eva任务，或提供明确可用且已授权的远程执行入口；不猜IP/用户名、不绕过主机密钥校验。

## 在eva → cyf新建任务可直接粘贴

为CYF聚义厅1.13.10做隔离构建环境预检。项目目录 `/home/chc/wsps/cyf`。先只读确认主机身份、是否承载生产服务、Git仓库及worktree/脏改动、CPU/内存/磁盘、Java/Node/npm/Python与项目声明的版本、现有依赖缓存，以及与CYF交付主机之间已有的源代码和制品传递方式。不要输出密码、Token或私钥，不修改SSH信任配置。不要构建、安装依赖、启动Flow、访问生产数据库、调用Provider、部署或操作任何已有进程/工作树。不得只按任意剩余内存数字判定安全；核对实际隔离与现有工作负载。报告实际结果、可执行的下一步和本任务ID。正式测试打包待原任务交付冻结候选SHA/tree与测试选择器后执行；Gradle必须经项目orchestrator串行，保持隔离数据库与确切源码证据，制品标记build_origin=local_user_authorized。

## 源码状态与边界

1.13.10仍在实现，当前W01/B01A候选不是完整发布版本。不要从eva本地develop推断当前发布候选，不重建1.13.9冒充1.13.10。原协调项目是 `/home/isp/wsps/cyf`，任务 `01a0bcc8-db16-7ca2-9b0a-715533e8f004`；唯一运行台账在原协调项目`docs/implementation/TASKS.yaml#runtime_ledger_json`。没有跨主机工具时通过用户转交精确结果，不宣称消息已送达。

## 后续实测：WS 通讯成功（2026-09-21）

用户指定扈三娘后，已通过当前账号绑定且可操作的 Agent `jyt-jiafewnnv58ec2379c-husanniang` 单次私聊完成只读预检。会话 `1760458004732`，标识 `JYT-UX-EVA-PREFLIGHT-20260921-A1`；收到 delivered=true、同 Agent/runtime 回复，随后 GET 会话读到持久化最终回复 `1570472`。此前 SSH/跨线程入口失败仍属实，但不再阻断只读消息通讯。

Agent 回报实际 hostname=Eva、用户chc、项目目录存在；4核、内存可用3757MiB、swap已用3984/4095MiB、磁盘剩余766M（98%使用）。执行环境未找到Java/Docker；有Node22.22.0、npm11.17.0。system bus访问被拒绝，进程/端口快照不能证明主机没有业务服务。尚未验证隔离构建与制品回传路径，也未测算最终依赖/源码/制品所需空间；不把766M设为无依据的硬门槛，Docker本身不是必需门禁。

本次只验证私聊 chat.message 的送达和回复，不代表 command.dispatch 隔离任务执行已打通。未构建、测试、安装、清理eva、部署或重启。流式诊断客户端编码错误导致其中文输出乱码，GET持久化回复正常；不能据此认定产品乱码。已保存脱敏规范化结果至 `deliverables/verification/juyiting-unified-experience-20260921/eva-preflight/final-result-normalized.json`（非原始命令日志）。下一步先核对受信隔离任务入口、真实Java位置/工具链及空间用量、制品回传方式，再确定必要环境变更范围；不覆盖eva已有脏工作区。1.13.10仍未发布。

### A2实际结果与有界A3诊断

A2同会话新请求送达（message1571060 / causation e8e8ca56-990f-4587-a719-0362e80dcb8e）。HTTP200/delivered=true，随后诊断客户端遇到ChunkedEncodingError；没有重发A2。GET原会话最终读到reply1571178，但只有“先核验hostname”的计划，无任何命令结果，不算检查完成。请求到回复900.322秒，与仓库客户端默认900000ms执行计时器及partial-text finalization路径相符，仅是推断，未核验Eva部署配置/退出码。

已记录新输入A3：全新会话1760458004733，causation 2ab89b9d-2f8d-4158-9d07-339471c385f9；只要求一次hostname/架构/现成JDK release/工具位置只读查询，不再扫磁盘或读配置。不是重启、不改超时、不创建构建工作区、不重复A2。后续只核对原会话；若仍无实际结果，不继续相同输入盲试。证据目录新增a2-outcome.json/a3-dispatch-intent.json。

当前候选源码的tracked内容字节：Web252659374、API25849861；本机x86_64依赖donor磁盘占用248256KiB，不能直接作为Eva未知架构的可用依赖或正式构建峰值。上次API1.13.8制品metadata记载Java21.0.8；只是既有验证基线，不据此认定Eva已有该工具链。

### A3已收到真实只读结果

通过GET会话1760458004733取回持久化reply1571295，causation与单次A3派发一致。扈三娘返回stdout=`Eva / aarch64 / /usr/bin/chromium / git / ssh / scp / rsync / curl`及退出码0；PATH没有java/javac，指定常见JDK目录未返回目录/release项。该结果证明当前只读命令可执行并在SSE断开后回收，不代表构建入口已验证。原始会话在a3-conversation-reconcile-2.json，脱敏归纳在a3-final-result.json。

Eva是aarch64，本业务机x86_64；不能直接复用本机平台相关JDK/node_modules/native二进制。已有Chromium可执行文件，但未启动测试，不能声称浏览器可用。未核验受信workspacePolicy、可写隔离位置、源码/制品实际传输认证或足量空间；JDK尚未定位。下一步需要可执行的已授权运维入口来核对/准备隔离构建环境（不能通过普通chat越过workspace管理机制）；当前仍无构建、安装、清理、重启或发布。
