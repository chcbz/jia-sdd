# RUNTIME-PATH-UNIFY-20261012

- Owner: 当前聊天 01a13076-049a-75f2-a84f-7d53194ffe9e；用户明确授权统一迁移旧 Agent 目录。
- 已读 /home/isp/wsps/cyf/AGENTS.md、ops/orchestration/README.md、/home/isp/AGENTS.md、/home/isp/docs/SERVER_ARCHITECTURE.md 和 Runtime self-host 指南。
- 范围：本主机旧 codex-ws-agent / codex-ws-agent-instances 的现用 HOME、workspace policy 迁移到统一 Runtime 的 state/conf；退役旧启动入口和旧部署目录，保留统一备份。不是升级/构建，不改内部执行库名称，不改远端李逵，不动身份/凭据内容、enroll、ACK、业务数据，不重新生成成果。
- 根仓当前 main checkout HEAD 0be55d3da4e5ee72e1d7bfc8473d9f89ce556c90 / tree 7cf493f8ccb677553dfbc6886059a50f6b1a64c0；isp-install HEAD 5d2d3f8bec903a87eed684936efc3f3d21e891e2 / tree 2351f07341d1fec59d070aa7d9860f7fbb9fdc0c。未查询远端最新；脏区保留，不构建或提交他人变更。
- 线上 Runtime 制品 runtime-conf-image-20261011-5b902c1bcd3e；受测输入为该原制品+精确备份配置+路径候选，不以源码 HEAD 冒充线上版本。
- 验收：相同身份/认证摘要；原数据完整迁移；旧路径无活动引用或进程持有；同一制品重新启动，静态/托管注册及现有图片能力保留；旧独立服务不再可启动；文档同步。
- 最早验证：只读配置与进程路径图、完整HOME权限和符号链接、安装器 validate；证据 /home/isp/state/cyf-diagnostics/runtime-path-unify-20261012；备份 /home/isp/baks/runtime-path-unify-20261012。
- 运行窗口：图片识别聊天 01a12ff0-5536-7591-99eb-41b16347a472 正在共享Runtime验收，已send_input非抢占协调；未取得安全窗口前不改现用配置/重启/迁走旧目录。其新增 typedInspection 配置必须保留。
- 空间：盘余约908MiB，旧目录约2.7GiB；采用同文件系统rename保留完整旧载荷到备份，不复制大目录/不删数据；认证与配置另存备份，停止所有原写者后迁移，失败恢复配置和目录映射而非回滚业务状态。
- 定位/实现/验证/等待耗时：待实测，不填推测值。

## 切换前确认（2026-10-12 22:27）
- 图片验收Owner已明确给出安全窗口：任务450读图完成、28个队列空、浏览器退出；切换仍重查实时队列。保留其最新配置与证据，并在迁移后无模型调用重测。
- 额外依赖：林/卢 model_catalog_json、旧工作区策略及根目录、59个历史thread的rollout_path与12个cwd引用。停机后仅事务更新SQLite threads的绝对路径列，完整会话原文保留；旧历史工作数据迁入统一state/history，不清空、不重放。
- 单次实施脚本 /home/isp/state/cyf-diagnostics/runtime-path-unify-20261012/migrate.py 已通过语法检查；恢复边界见同目录 RECOVERY.md。使用既有coordinator→release锁，SIGTERM精确主进程并等所有旧路径写者退出，不用stop超时强杀。

## 已执行与验收（2026-10-12 22:41，Asia/Shanghai）
- 运维迁移完成，原版本制品未换，统一服务PID3127402、自22:34:26运行、NRestarts=0；三静态Agent同一instance `67a3bb65-9701-4d25-85d6-42a1dbe89878` online/generation20。没有API/Web发布、enroll、模型付费调用或历史请求重放。
- 原子迁移8个现用根/文件，各项移动前后inode/内容/模式/属主摘要匹配；精确路径见plan.json/result.json。原HOME认证摘要、manifest/installation授权、host/hosting配置、Provider文件、吴用图片识别原证据摘要不变。只改三个codexHome、统一policy文件位置/root和林卢catalog/历史受信路径。
- 59个历史线程的SQLite路径列迁移；三个DB完整性通过、线程数保持25/12/22、索引旧路径0、rollout文件缺失0。会话原文未改、DB状态未回滚。历史数据完整保留在state/unified/history。
- 两个旧apps目录移到备份retired，无兼容链接。旧systemd service/template已mask，旧两个bin脚本归档。内部执行库不改名、不删。
- 无模型调用的实际隔离/网络/输入承载重测`contractReady=true`；nativeProbeDigest仍为`sha256:0d0745828bbd0a55ccdb049638ef501a75c06b5e2248d1b13feeaaba220c3b15`，没有伪造证据。结果measurement-summary.json。
- `verification.json`核验当前配置无旧目录引用、进程FD/cwd/exe旧根引用0、三静态Agent在线；原已离线托管subject last_seen20:56，未恢复/重标在线。静态Runtime stateRoot仍在apps/cyf-agent-runtime-v1/<角色>/runtime-state，非本次旧名目录范围。
- 健康监控现行文件和两份源码只把is-active目标改为统一Runtime；安装摘要同步，82项测试通过，现行Effects.agent只读返回agent_active；未执行全量健康检查/恢复。保留已有脏区其他路径修改，没有整文件回退。
- 稳定知识同步 /home/isp/docs/SERVER_ARCHITECTURE.md、docs/juyiting-runbook.md、docs/codex-ws-agent.md历史提示、ops/health/CONTRACT.md。清理Owner与图片验收Owner均已收到路径更新。

### 失败归因与边界
- 单次迁移中主机Python3.6 SQLite没有Connection.backup；已停止在可恢复阶段，空备份留证。确认所有写者已退出后按DB/WAL/SHM逐字节备份继续，未从头重跑迁移。
- 单独validate首次未带systemd现行的Provider配置路径，报RUNTIME_PROVIDER_CONFIG_INVALID；配置本身合法。补入精确providers.json环境入口后验证通过，不修改制品/权限。具体continuation脚本与原错误保留在证据目录。
- 初次健康测试81通过/1失败原因是源monitor变更后的installer摘要pin未同步，已同步精确SHA，最终82/82通过。
- 日志既有RUNTIME_FRAME_GENERATION_MISMATCH与MESSAGE_TYPE_REQUIRED在迁移前后均存在；比较证据journal-warning-comparison.json。本次无runtime-agent-isolated/runtime-error，不将旧协议警告声称为已修复。
- /usr/local/libexec/cyf/release_payload_cleanup.py仍列旧路径作为可选保护扫描候选（现目录不存在）；不是运行依赖，本次不扩改清理器。历史文档/证据及原会话文本允许保留旧路径，不篡改历史记录。
- root develop有多任务既存脏区；本次运维修改已实际生效，但文档/health源码及新增定向测试尚未Git提交，未宣称远端develop最新或源码发布完成。集成时只取本任务增量，不提交他人变更。
