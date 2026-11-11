# RUNTIME-FIXED-DIR-20261023

- Owner：本聊天。授权：用户2026-10-23“继续”，承接固定目录规则、安装器适配及受控迁移；不发布API/Web、不调用付费模型、不变更身份/配置/业务状态。
- 规则：已读取 `/home/isp/wsps/cyf/AGENTS.md`、`ops/orchestration/README.md`、组件AGENTS及self-host指南。接口规范固定为 `/home/isp/wsps/cyf/api/docs/interface-standard.md`（2026-10-14冻结版）；本任务不改变接口。
- CYF根本地HEAD：`5e6ab2b6f1a156c320189f17d76941fbe623738a`；已有大量无关脏改动，不覆盖、不整仓提交。远端develop未查询，不声称最新。
- Runtime源码基线：`7dd120f5d3a61559ebf4347aa63b638f7e6a4153` / tree `a1ad4c9980b962865f2fe50f70e48171549d30df`，与现行1.2.6记录匹配。
- 源码worktree：`/home/isp/wsps/chcbz/isp-install-worktrees/runtime-fixed-dir-20261023`；branch `codex/runtime-fixed-dir-20261023`。主checkout保持原状，无子Agent。
- 目标：固定 `apps/cyf-agent-runtime-v1/app/`；历史程序归档到 `baks/cyf-agent-runtime-v1/20261023-fixed-dir/`；保留版本来源及制品摘要。
- 非目标：迁移静态Agent stateRoot/HOME、清除UNKNOWN或队列、重新enroll、更新Codex CLI/Python基础环境、部署新业务版本。
- 验收：定向安装入口/存储规则/工具链重定位测试；原1.2.6制品逐文件核验；实际配置validate；停写备份；精确服务切换、各subject新鲜心跳/注册/ready；状态身份保留；历史目录仅无引用后归档。
- 证据与恢复：`/home/isp/baks/cyf-agent-runtime-v1/20261023-fixed-dir/`（私有）；完整原状态备份验证后才切换，磁盘空间不足则不强行执行。
- 当前：盘点与实现准备。线上PID856671，三静态通道ready；磁盘余量约1.1GiB，需控制备份/制品临时占用，不删除他人文件。
- 耗时：定位/实现/验证/等待未汇总；开发完成与迁移等待分别记录。

## 实现与迁移进展（2026-10-23）

- 在固定源码独立worktree完成默认`app/`安装入口、两份systemd模板、CYF限定规则/指南及Python生成路径重定位工具；工具拒绝未知引用、符号链接旧路径、被共享硬链接的生成文件或候选漂移，默认只读。
- 自检：Node定向20项通过；Python重定位5项通过；shell语法与git diff whitespace通过。首次源测试中新增regex误覆盖conf中的`%i`，已收窄到apps路径后重跑最终候选通过，不是安装失败。无本机Node/Gradle重型构建、无Flow或API/Web发布。
- 源码候选与远端develop：`297272f5e7af49c6bda703b37f0fc8a6a830a4a7` / tree `6358a3862b7339de372de79b349a846fe2db3032`；已fast-forward push并ls-remote回读一致。原主checkout未切换/覆盖。源码声明1.2.7为后续制品候选；本任务不部署1.2.7，现用1.2.6只做生成路径安装转换。
- 原1.2.6制品4108条全部摘要/权限与源manifest一致，无增删文件。盘点无执行中条目；4份RECOVERY_REQUIRED原样保留，不重放。现用配置无版本目录直接引用；现行主机工具扫描仅unified受管drop-in引用1.2.6程序路径。
- 磁盘可用空间曾降到约571MiB；未强行停服写入超出空间的备份。先对1.2.4、1.2.5及legacy-unified纯程序目录逐项检查进程引用，压缩归档、xz测试、tar全量compare后退役原副本，空间恢复约1.6GiB。历史内容未丢弃；摘要映射见证据`prearchived-programs.json`。
- 现用完整原程序已归档并全量compare。迁移复用既有`/run/lock/cyf-wuyong-versioned-release.lock`非阻塞互斥；精确停止unified服务、所属子进程退出、host/subject writer锁正常释放后，正在生成全量私有状态备份（完整HOME/SQLite、static/managed、配置、身份、inbox/outbox）。未修改状态或解除任何他人锁。
- 详细操作/恢复与实时状态见私有证据`migration.json`、`RECOVERY.md`、`migrate.py`；完成前不把规则/源码合入或程序归档宣称为迁移/健康验收成功。

## 迁移完成与真实边界（2026-10-23）

- 安装执行完成：原1.2.6程序转为固定`app/`实体；现行业务代码/Node/依赖不变，4个venv生成路径转换，新manifest4108条。当前manifest SHA256：`df37b5a098fc628f4c352d4b02493cb59e5b36dc0693b9a763626ab0a47debf2`。systemd实际启动路径与新PID1183474的cwd/exe一致。
- 原程序归档79MiB；全量私有状态备份747053892字节（约713MiB），SHA256 `08fd48093f895271902f16934e507891fef608b2b58a8ea7791abc43e2a08001`，xz完整性与tar全量compare均通过。历史1.2.4、1.2.5、legacy-unified均独立压缩归档并比对后退役原副本；旧静态/test程序文件归档，现行manifest/runtime-state原路径保留。历史吴用嵌套包包含未启用manifest和空runtime-state，已另做无现用配置引用/状态为空盘点并完整归档，未当作现行身份迁移。
- 当前主机索引改用`release-records/current.json`及`current.manifest.json`；原历史记录保留，不重写原来源。`releases/`和`current`已移除，不保留按版本切换的入口。恢复步骤见私有`RECOVERY.md`，不直接启动备份，不恢复旧DB覆盖新事实。
- 本机09:10:26停止并释放writer，09:57:49完整备份/比对完成，09:58:15新主进程启动。压缩与校验共47分23秒，原进程停写至新进程启动47分49秒；这不是一次轻量目录移动的耗时。初始只给本任务tar/xz低优先级，后基于实际耗时恢复本任务两个进程为正常nice0，没有调整其他聊天进程。备份窗口明显过长，尚未优化一致快照/压缩策略，不保证未来缩时。
- 新进程初始执行原有二进制/schema信任测量，健康文件一度仍为旧PID；未据此报成功。初始化后三个通道均ECONNREFUSED，确认API10018无监听、JAR在另一聊天“优化后端启动时间”任务更新，compact wait快照显示该Owner正在修复阅读进度CHECK名称不一致导致的启动失败。本任务只读观察，不接管API或修改生产数据。
- 后端恢复后Runtime原生重连。原本机收口脚本对inbox做宽泛rglob，包含无关chat workdirs，已停止本任务自己的收口/轮询进程（非Runtime服务），改为精确核对原4份RECOVERY_REQUIRED记录和身份/授权摘要，不让无关工作区大小拖住验收。10:31:19新PID1183474三个subject均连接/注册/ready，快照及presence回执在既有3个心跳周期内；10:31:20归档和当前索引完成。证据`health-after.json`、`finalize-local.py`、`migration.json`。这是一次当时通道健康证明，不是持续健康承诺。
- 未进行付费模型/业务任务复验，不发布API/Web，不重登身份、不清除UNKNOWN/RECOVERY_REQUIRED、不改运行配置或当前授权；无独立Reviewer。根AGENTS/runbook及主机架构已按局部范围回写；其余脏改动保持原状。
- 定向验证最终25项通过（Node20 + Python5），shell语法及diff检查通过。远端develop本次push后回读为297272f；后续查询单独记录，不把主checkout或先前查询冒充持续最新。
- 下一步仅为后续实际升级沿固定目录和同样完整性/恢复保护执行；备份窗口优化另按实际输入和一致恢复闭包验证，不在本任务擅自删减必要备份。

- 最终只读复核（2026-10-23 10:36:22 +08:00）：4108项现用文件摘要/权限、固定PID路径、无版本目录/current、静态状态路径及三通道新鲜回执全部通过；快照约14秒、回执约44—45秒，符合原30秒周期的3周期观察口径。证据`final-check.json`，主机current.json已绑定该证据。10:32远端develop回读仍为297272f；非持续最新保证。所有本任务执行/轮询会话已结束，不保留持锁等待进程。
