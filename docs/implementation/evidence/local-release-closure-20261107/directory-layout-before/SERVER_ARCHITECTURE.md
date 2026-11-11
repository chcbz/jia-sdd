# /home/isp 服务器架构文档

## 2026-11-05 10:00：工具链单份实体上线（Run148）

- 当前Runtime1.3.55/bridge1.1.44，源码54c47019aa9ff7bd6e53181cfa9c6c9a073ea710，Flow5264702/148 SUCCESS；固定app与systemd不变，启动PID4069687。API497/Web448及模型/profile均未改变。
- 安装时只在同一候选内以硬链接共享1613个工具文件；69个外部系统文件仍独立复制，避免系统更新影响安装。仍为1682文件/3个只读顶层挂载，image manifest不变；不跨版本链接，不对运行程序原地去重，无每请求复制或新增缓存。
- 上线inode/闭包核验避免重复分配525099008字节（500.77 MiB）；新程序独占分配874729472字节，旧程序1400721408字节。旧程序和停写状态备份保留在`/home/isp/baks/cyf-agent-runtime-v1/20261105-toolchain-shared-148/`，不能把避免重复占用等同于根盘可用空间即时增加。
- 清理器`/usr/local/libexec/cyf/runtime_backup_cleanup.py`已受控更新，SHA256为7cf018f8fe61a92c14a7888d0b5f424a8d1e170e68a03a7e98aee42ef6df904b；仅允许完整链接集合落在同一已退役old-program，拒绝外部链接/占用/篡改，保留锁、pin与保留期；41项隔离测试通过。本次未运行生产清理。当前发布记录仍business-partial，原自动清理的verified-active前提未放宽，故自动退役仍受保护条件阻止。
- 7395项安装manifest/692项payload、3 Agent就绪及API/Web不变核验通过；真实host工具探针3/3通过。线上新普通议事首字8.79秒/完成9.95秒，新XLSX通过openpyxl实际读取随机验证码，首字16.96秒/完成17.14秒；两条最终回复持久化且沿用原native thread。仅本范围通过，原图片语义问题仍未解决；单次数据不是提速对照，不标全业务verified-active。
- 证据：`/home/isp/state/cyf-diagnostics/juyiting-polling-20261102/toolchain-shared-20261105/release/`，包括installed-source-verification.json、live-acceptance.json、native-smoke-evidence.json及安装/清理器证据。下节531.3 MiB复制说明为Run147历史状态，已由本节取代。

## 2026-11-05：授权历史临时文件与备份清理（已核验）

- 清理范围：23批已退役备份载荷（4.72 GiB）、58个历史Flow下载制品（毛回收7.23 GiB）、127712个临时编译/Gradle缓存/闲置测试浏览器文件（1.35 GiB）。下载包内非应用证据另存压缩归档，未删除唯一测试/来源证明。
- 根盘可用空间从0.52 GiB增加到13.49 GiB，净增加12.97 GiB（含保留审计及期间文件变化，不等于删除量简单相加）。
- 保留现用程序、配置、身份、会话/ACK/业务状态、源码/未提交工作、真实Codex聊天记录、当前Runtime/API恢复点、最近Web恢复点及数据库恢复材料；JVM dump目录因占用跳过，未知来源包不猜测删除。不是全盘备份归零。
- 无重启、无构建/发布、未修改自动清理策略。Runtime Run147/PID4012212保持，7395项安装manifest核验通过，Agent connected/registered/ready；API Run497健康UP且JAR摘要不变；Web Run448的612文件摘要不变；现用carrier证明和当前恢复点完整保留。此前图片语义验收部分失败状态未更改，不能据本次磁盘核验宣称业务全通过。
- 工具链额外占用531.3 MiB来自安装时prepare-toolchain-image.mjs以copyFileSync一次物化隔离目录；原工具目录和副本共存。请求只读挂载，不逐请求复制，不是Agent内存缓存。挂载本身不要求复制；后续可评估单一安装布局，但本次不删除任一现用目录或改安装契约。
- 此次是用户明确授权的一次性清理，不冒充自动保留策略执行；已删除备份均保留PAYLOAD_RETIRED标记，不能再视为完整恢复点。审计、逐文件摘要、保留证据、结果与核验：`/home/isp/baks/host-cleanup/authorized-history-20261105/`（summary.json、verification.json、REPORT.md及三阶段plan/result/deletions）。


更新日期：2026-10-20（Asia/Shanghai；旧章节保留各自核验范围）

## 2026-10-30：按用户授权移除 swap

- 停用并删除原 `/swapfile`（2 GiB），移除 `/etc/fstab` 对应条目；`swapon --show` 为空，重启后不会自动启用该 swap。操作前文件系统表备份于 `/home/isp/baks/swap-retirement-20261030-115320/fstab`。
- 全局 `vm.swappiness=10` 及 MySQL cgroup 的 swappiness 设置未修改；在没有其他 swap 的情况下不产生换页保护。内存不足时可能触发 OOM，需监控可用内存和业务峰值。下方 2026-10-27 “现有 swap”描述为当时历史状态。
- 操作后 API 健康检查 UP，根文件系统剩余约 4.6 GiB；未重启服务。

## 2026-10-27：MySQL 降低换页倾向（无重启）

- 主机为 cgroup v1；保持全局 `vm.swappiness=10`、现有 swap 和 MySQL buffer pool 配置不变，仅将 `/sys/fs/cgroup/memory/system.slice/mysql.service/memory.swappiness` 从60降为1，已即时写入。
- 持久化入口 `/etc/systemd/system/mysql.service.d/20-swappiness.conf`，通过 `ExecStartPre` 在每次 MySQL 启动前写入1；已校验 unit 并 daemon-reload，本次不重启 MySQL，不强制换入旧 swap，不停止其他业务。
- 该策略仅降低换页倾向，不保证内存不足时完全不换页，也不代表已证明查询性能改善。持续关注 `vmstat` 的 si/so、MySQL RSS/VmSwap 与业务延迟；不要仅以 swap 已用量判断效果。
- 回退：删除上述专用 drop-in，执行 `systemctl daemon-reload`，将现行 cgroup 的 `memory.swappiness` 写回60；无需重启。操作前文档、unit及参数保存在 `/home/isp/baks/mysql-swap-tuning-*`。

## 2026-10-26：Runtime 历史恢复载荷自动保留策略

用户已授权将Runtime历史恢复载荷纳入既有每30分钟主机清理，不再逐批手工授权。`/home/isp/bin/clear_disk.sh`在低空间判断之前运行`/usr/local/libexec/cyf/runtime_backup_cleanup.py`，因此高于5GiB也执行本阶段；clean先用df快速报告空间，不再让递归du诊断先占锁延迟回收。不新增业务发布或Codex自动任务。

- 唯一扫描根`/home/isp/baks/cyf-agent-runtime-v1`。仅退役已识别批次的`state.tar`、`state.tar.gz`、`old-program.tar.gz`及`old-program/`内文件/链接；所有目录、小型版本/manifest/恢复记录和其他证据保留。退役标记`PAYLOAD_RETIRED.json`意味着该批不再具备完整恢复能力，不保留额外完整载荷副本。
- 保留最近两批有载荷的备份，并无条件保留现行`release-records/current.json`指定的`backup`；已完成退役的批次入口不再复用、也不反复扫描其空目录或占用活动批次配额；晚于现行pin的尝试、变更未满1小时、`.keep`、占用和安全异常批次继续保护。因此“两批”是最低保护，不是强制最多两批。缺失pin/载荷、当前记录非`verified-active`或进程扫描不完整时停止，不凭目录年龄猜测发布成功。
- 同时持有主机清理锁与既有`/run/lock/cyf-wuyong-versioned-release.lock`，发布占锁时跳过，不抢占发布；两锁开机由`/etc/tmpfiles.d/cyf-host-cleanup.conf`用不截断的`f`规则创建。每100文件刷新进程占用快照，逐文件校验身份/物理父目录，保护挂载、硬链接和异常权限；归档软链接只unlink链接。删除前写入并fsync审计与退役标记，失败关闭。
- 审计`/home/isp/baks/host-cleanup/runtime-backups/audit.jsonl`（8MiB轮转、5份）；沿用`clear_disk.log`、`clear_disk.status.json`及本地syslog告警，未接外部推送。未扩大到MySQL恢复材料、其他业务备份、数据库、现用Runtime程序/state、任务源码或Flow固定回滚。
- 仓库同步`/home/isp/wsps/cyf/ops/maintenance/`：新增helper与依赖镜像、完整主机入口`clear_disk.host.sh`、保留简版兼容入口`clear_disk.sh`并增加独立Runtime阶段。规则/安全边界见该目录`RUNTIME_BACKUP_RETENTION.md`；只读预览使用helper的`plan`，隔离测试`/home/isp/bin/tests/test_runtime_backup_cleanup.py`。本次操作证据`/home/isp/baks/host-cleanup/runtime-retention-20261026/`。

## 2026-10-23：第二轮授权磁盘清理

- 已退役系统自带旧MySQL实例：`mysqld.service`已disable/mask，`/var/lib/mysql`旧数据内容已按用户授权删除，无恢复副本。现用生产`mysql.service`、`/home/isp/apps/mysql/data`及全部binlog未动。
- isp的Gradle Wrapper发行目录`/home/isp/.gradle/wrapper/dists/gradle-9.3.1-bin/e6fpmcitnr2cbhj7h6pdk7btv/gradle-9.3.1`与统一发行目录314个文件摘要一致，已去重为指向`/home/isp/apps/gradle/9.3.1`的兼容软链接。
- 清除`/root/.gradle/.tmp`和`/root/.gradle/daemon`旧内容；移除闲置临时PDF Node载荷`/root/.cache/pdf-skill-node-4fhcgvsd/node`，不再可用该v22临时路径；统一Node运行时保留。
- 两处旧应用恢复包`/home/isp/baks/jyt-external-d31-221-664b2576b49f277b3289c52e4eacf9d67f5d62ba`、`/home/isp/baks/cyf-web-flow-before-180`内容已删除，旧入口目录保留为空，不再可回滚；固定`flow-api`回滚保留。
- `/var/log/cyf-api-flow`关闭超过两天的67份未压缩日志改为gzip；已有压缩文件、近期与活动日志保留。12份大型历史清理审计同样无损压缩，原路径改为`.gz`，各目录`COMPRESSED_FILES_20261023.md`及本轮actions.json保留引用映射与内容摘要。这是一次性清理，不代表已新增自动轮转规则。
- 本轮未扩大到测试数据库、源码/工作树备份、未完成任务或其他缓存。审计：`/home/isp/baks/host-cleanup/authorized-second-pass-20261023/`。

## 2026-10-23 14:00：旧本地API准入完整退役（覆盖后文历史章节）

经用户明确授权，旧本地API制品准入及本地安装/离线维护路径已停用，相关专用制品、原始证据与授权资料已删除，无完整载荷副本，不再可作为安装输入或完整复核档案。正式发布仍使用获授权的Flow，当前生产JAR、Flow记录、固定回滚与数据库未动。

- 已删除 `/usr/local/sbin/cyf-api-local-admit`、`/usr/local/libexec/cyf-api-local`、`/usr/local/libexec/cyf/admission_payload_cleanup.py`，仓库对应入口/实现/旧专用测试同步移除。
- 已删除 `/home/isp/state/cyf-api-local-admission`、`/home/isp/state/cyf-api-local-authority`；正常卸载并移除对应 `/var/lib` 两处绑定挂载、空目录及fstab配置。其余Flow等迁移挂载不变；下文“剩余12个”是历史基线，本次再撤除这两项。
- 生产及仓库 `cyf-api-flow-deploy` 移除本地制品读入/准入/安装/离线维护实现，旧`--local-*`明确拒绝；安装器拒绝本地v3安装授权。仅保留历史v3记录的无I/O格式/绑定校验，供Flow回滚和清理解析历史记录，不构成可用本地发布路径。
- 主机及仓库清理入口不再运行准入清理阶段，不重建登记表或旧目录。Flow、旧临时载荷、缓存、日志等既有清理规则保留。
- 本次不是取消Flow制品校验、发布互斥、数据库授权或健康检查；未进行应用构建/发布/服务重启。后文旧准入“保持保护”“必须Owner登记”“证明保留”等规则仅记历史，现已被本节覆盖。

核验与删除审计：`/home/isp/baks/host-cleanup/retire-local-admission-20261023/REPORT.md`；流程说明：`/home/isp/docs/API_ADMISSION_RETENTION.md`。

## 1. 总览

当前目录 `/home/isp` 是服务器运行目录，不是单一源码仓库。整体按运行时、中间件、业务部署、脚本和日志分层：

```text
/home/isp
├── apps/        # JDK、Nginx、MySQL、Redis、RabbitMQ、Elasticsearch、Logstash 等运行时和中间件
├── conf/        # 主机配置（Runtime v1唯一配置根，自2026-10-11迁入）
├── state/       # 持久化运行数据（既有stateRoot未全部归拢）
├── bin/         # 服务启停、部署、证书和清理脚本
├── hosts/       # 业务应用 jar、静态站点、上传/素材目录
├── logs/        # Nginx、MySQL、业务访问日志
├── baks/        # 统一备份：生产 API、旧版 API/Web、Flow API 回滚 JAR
├── pkgs/        # 安装包归档
└── docs/        # 本文档所在目录
```

从当前进程看，正在运行的核心组件包括：

- Nginx：反向代理和静态资源服务。
- MySQL：本地 3306，数据目录在 `/home/isp/apps/mysql/data`。
- Redis：本地 6379。
- RabbitMQ：AMQP 和管理后台，管理后台经 Nginx 暴露。
- `cyf-api-kit.jar`：Spring Boot 服务，监听 `10018`。

`hosts/jia` 中保存了一组 JIA 微服务 jar，但当前进程列表未看到这些 jar 正在运行。

## 2. 目录职责

### `/home/isp/apps`

这里放服务器本地安装的运行时和中间件：

| 目录 | 用途 |
| --- | --- |
| `/home/isp/apps/jdk8` | 旧版 Java 服务默认 JDK，`bin/jia.sh` 和 `bin/jenkins.sh` 使用它。 |
| `/home/isp/apps/jdk21` | 旧版/本地 Java 21 工具链；现行 `cyf-api-kit.jar` 使用 `/opt/cyf/runtime/temurin-21-jre`。 |
| `/home/isp/apps/gradle/9.3.1` | 统一的 Gradle 9.3.1 发行目录；原 Root Wrapper 与旧 `/run` 验证工具入口保留兼容软链接，载荷位于实际磁盘，不放回 tmpfs。 |
| `/home/isp/apps/nginx` | Nginx 主目录，配置在 `conf/`，vhost 在 `conf/vhost/`。 |
| `/home/isp/apps/mysql` | MySQL 程序、socket、pid 和数据目录。 |
| `/home/isp/apps/redis` | Redis 程序、配置和 pid。 |
| `/home/isp/apps/rabbitmq` | RabbitMQ 程序、插件、mnesia 数据和日志。 |
| `/home/isp/apps/elasticsearch` | Elasticsearch 程序、配置、数据和日志。 |
| `/home/isp/apps/logstash` | Logstash 程序和同步任务配置。 |
| `/home/isp/apps/node` | Node.js 运行时。 |
| `/home/isp/apps/maven` | Maven 构建工具。 |
| `/home/isp/apps/arthas` | Java 诊断工具 Arthas。 |

注意：`apps/mysql/data`、`apps/elasticsearch/data`、`apps/rabbitmq/var` 都是运行数据目录，排查时可读，默认不要编辑或清理。

### 2026-10-20 开发环境与旧制品人工退役

用户确认删除磁盘候选A～E后，已按精确清单人工退役；不改变自动清理策略，不将此授权泛化为所有目录“两份保留”。

- Java 11（Oracle 11.0.8）目录 `/home/isp/apps/jdk11` 和 Java 17（GraalVM 17.0.9）目录 `/home/isp/apps/jdk17` 已删除。指定配置/脚本与进程检查无引用；未保留完整离机副本，不承诺精确旧环境可恢复。Java 8、Java 21和生产API的 `/opt/cyf/runtime/temurin-21-jre` 保留，生产启动路径未改。
- Runtime当前服务仍使用 `/home/isp/apps/cyf-agent-runtime-v1/releases/runtime-ui-workflow-1.16.17`，直接上一版 `/home/isp/apps/cyf-agent-runtime-v1/releases/runtime-ui-workflow-1.16.16` 保留；安装链已核对且两版只读闭包校验通过，未做真实切换回滚。旧1.2.6、1.2.7、1.16.12、1.16.15四个release已退役。以下旧日期章节是历史核验，不代表现行release。Agent state、身份、会话、ACK和Runtime迁移恢复包均未删除。
- 6任务/7个已合入工作副本经Git worktree机制退役；分支与共享Git对象保留。4个Web依赖链接只移除链接，主工作区 `/home/isp/wsps/cyf/web/node_modules` 保留；两处未合入任务继续保留。
- `/home/isp/wsps/private-maintenance/mmd-cloud-ci-20261005` 下的API5260799、Web4403172两个旧CI原包已退役；全部非载荷成员及原verification已在下述审计目录保留并摘要/成员读回验证。这些是证据档案，不是完整可安装包，未制作离机完整载荷副本。原任务的其他文件与证明未删。
- 浏览器仅清理批准的1262个纯缓存子目录中的普通文件；profile、登录/会话、截图和证据保留，5个权限异常缓存子目录仍排除。编译产物候选F、Elasticsearch/Logstash候选G未动，生产数据库和必要回滚备份未动。未发布、重启或变更服务配置。
- 明细、摘要和核验：`/home/isp/baks/host-cleanup/delete-A-E-20261020/REPORT.md`。退役后恢复工作副本可依保留的commit/分支重建；不承诺恢复原缓存或重建字节完全相同的历史CI载荷。

### CYF Runtime固定程序目录（2026-10-23局部核验；覆盖下方旧路径快照）

- 唯一活动Runtime服务仍为`cyf-agent-runtime-v1@unified.service`，实际cwd/Node/入口固定到`/home/isp/apps/cyf-agent-runtime-v1/app/`；旧`releases/`和`current`已退役，应用根只保留一套现用程序。静态角色目录仅留现行manifest/runtime-state，身份与业务状态未按旧版本清理。
- 程序仍为Runtime1.2.6 / 源码`7dd120f5d3a61559ebf4347aa63b638f7e6a4153`；本次仅重定位4个venv生成路径，未换业务代码、Node或依赖。安装入口/模板的源码候选1.2.7（develop `297272f5e7af49c6bda703b37f0fc8a6a830a4a7`）并未部署。
- 当前版本来源、安装转换与制品摘要以`/home/isp/apps/cyf-agent-runtime-v1/release-records/current.json`和`current.manifest.json`为准，主机RELEASES.md已同步。旧记录保留原发布路径/事实，通过归档映射追溯，不当作当前路径或持续健康证明。
- 历史程序、完整停写状态备份及恢复信息位于`/home/isp/baks/cyf-agent-runtime-v1/20261023-fixed-dir/`，版本数字不作为现用/归档批次目录名。身份/配置/授权及4份RECOVERY_REQUIRED记录核对未变，完整HOME和会话保留；新PID三个静态通道注册、ready及新鲜回执已核验，未调用付费模型或重做业务验收。
- 备份/比对09:10—09:57造成较长停写，程序09:58启动；随后受另一任务的API启动失败影响拒连，API恢复后自动重连，10:31完成新鲜通道核验。本任务没有重启或发布API/Web。详情见`/home/isp/wsps/cyf/docs/implementation/handoffs/RUNTIME-FIXED-DIR-20261023.md`，其他章节仍保留各自基线，不代表其余状态路径迁移完成。

### Runtime v1 现行目录与服务（2026-10-11局部核验）

- 当前唯一活动服务：`cyf-agent-runtime-v1@unified.service`；源码 `isp-install` commit `5b902c1bcd3efced9720e015e3b8240d39ce0738`，Runtime包版本1.0.2，release `/home/isp/apps/cyf-agent-runtime-v1/releases/runtime-conf-image-20261011-5b902c1bcd3e`。模板和实例drop-in仍由`/etc/systemd/system`管理。
- 配置唯一根 `/home/isp/conf/cyf-agent-runtime-v1`，私有根0700、私有文件0600。原`/etc/cyf-agent-runtime-v1`已移出，无兼容软链接；备份`/home/isp/baks/runtime-conf-image-20261011`。升级须沿用新路径，不执行历史第14节的独立实例恢复操作。
- `unified.host.json`引用现行Agent profiles和hosting配置。静态subject的图片凭据从`unified.conf`显式指定的`providers.json`按完整subjectKey读取，仅吴用启用；不把密钥放在普通profile或继承进程环境，不复制其他账号HOME。
- `state/unified/host`保存host状态，`state/unified/agents/<角色>`保存工作文件等；截至2026-10-11，既有静态Agent `apps/cyf-agent-runtime-v1/<角色>/runtime-state`与托管状态根未迁移；2026-10-12托管根变更见下一节，静态Agent状态仍不变。原4个subject、6份运行写锁在同一新PID恢复；旧3个独立角色服务未启用。
- 真实task440能力接口显示图片执行READY/GENERATE_IMAGE，仍要求任务级OWNER_EXACT_CONSENT_REQUIRED；没有实际Provider调用或图片产物验收。Web/API安装记录未变，不把本次Runtime升级当连续问答前后端发布。
- 实施和恢复边界：`/home/isp/wsps/cyf/docs/implementation/handoffs/RUNTIME-CONF-IMAGE-20261011.md`；证据`/var/tmp/cyf-runtime-conf-image-20261011`。本文其余部分保持各自旧核验日期。

### 统一 Runtime 目录收口（2026-10-12 22:39核验）

原 `/home/isp/apps/codex-ws-agent` 与 `/home/isp/apps/codex-ws-agent-instances` 已完整移出应用根，无兼容软链接；退役载荷保存在 `/home/isp/baks/runtime-path-unify-20261012/retired/`，不是第二套运行服务。

- 唯一入口仍为 `cyf-agent-runtime-v1@unified.service`，原Runtime1.0.2/源码 `5b902c1bcd3efced9720e015e3b8240d39ce0738` 制品未更换；旧 `codex-ws-agent.service` 及模板已mask，两份旧bin启动脚本移入同批备份。
- 三个静态subject各自原HOME完整迁至 `/home/isp/state/cyf-agent-runtime-v1/unified/agents/{wuyong,linchong,lujunyi}/codex-home`；不复制其他角色凭据，不重新enroll，不清空会话/锁/ACK。
- `model-catalog.json`、`workspace-policies.json` 统一位于 `/home/isp/conf/cyf-agent-runtime-v1/`；吴用旧workspaces迁至其state目录下`workspaces`。
- 旧历史客户端数据分别保留于统一state下`history/shared-client-data`与`history/wuyong-client-data`。59个Codex会话索引仅事务更新`threads.rollout_path/cwd`绝对路径列，线程数不变、3份SQLite integrity_check通过；原会话原文作为历史记录未改写。
- 本次核验：三静态subject同一新Runtime instance在线、session generation20；旧目录进程引用为零，现用配置无旧根引用。吴用图片识别原证据/模型/权限未变，无模型调用重测`contractReady=true`。托管subject原先离线（last_seen 20:56）未因此恢复，不把服务active当全员在线。
- 健康监控的Agent只读检查改为统一服务；源测试82项通过，未触发健康恢复或API/Web发布。现行静态Runtime授权stateRoot仍在apps/cyf-agent-runtime-v1/<角色>/runtime-state，未扩大本次迁移。
- 恢复与详细证据：`/home/isp/state/cyf-diagnostics/runtime-path-unify-20261012/`；任务交接 `/home/isp/wsps/cyf/docs/implementation/handoffs/RUNTIME-PATH-UNIFY-20261012.md`。回退须保持当前业务状态，仅逆向路径迁移，不恢复旧数据库快照或启用旧服务。

新Runtime制品内部的`codex-ws-agent/`仍是内嵌执行库，不是独立部署；不得全局重命名/删除这个内部库。

### CYF 持久状态路径迁移（2026-10-12，未全部收口）

- 原 `/var/lib/cyf*` 的13个实体目录已移至 `/home/isp/state/`，同名保留，未复制大数据；这不是磁盘回收操作。
- **Runtime 托管根已完成无兼容迁移**：现行 `/home/isp/conf/cyf-agent-runtime-v1/unified.hosting.json` 的 `managedRoot` 为 `/home/isp/state/cyf-agent-runtime-v1-managed/unified`。既有托管 `profile.json` 的 HOME/workdir 已同步；原 managedRoot 绑定挂载、fstab 条目及空目录已删除，不保留旧入口。Journal、manifest、身份、ACK/授权状态均保留，静态 Agent 的 apps 内 stateRoot 不在本次迁移范围。
- Runtime 程序仍使用上述已核验 release，从配置读取 managedRoot，无需重建；旧 release 中示例是历史制品，不作为新安装配置。`isp-install/conf/cyf-agent-runtime-v1` 安装示例和验收源码已改新路径。
- `wsps/cyf/ops` 的部署/安装/准入、schema、发布锁、清理与健康监控源码默认路径已改 `/home/isp/state/cyf*`；E05 runner 字节变化后的源码精确摘要 pin 已同步，不放宽校验。
- 2026-10-12剩余挂载核验：7个可优先撤除、Web/扫描器2个须先切换工具/沙箱、API3个须处理发布摘要闭包；检查时均无进程占用。具体收口约束见 `/home/isp/docs/CYF_STATE_CLOSEOUT_20261012.md`。本轮未执行这12个卸载。
- **其余12个旧入口仍是迁移中的临时绑定挂载，不是最终架构**。主机现行 API 部署工具与已批准发布记录含旧绝对路径及不可变摘要闭包，尚未一并转换；不可直接用新默认值工具覆盖后宣称完成，也不可批量替换历史证据。源头修改不等于现行安装记录已迁移。
- MySQL 的运行/persist 与 `/home/isp/apps/mysql/my.cnf` 均使用 `binlog_expire_logs_seconds = 259200`（3天），不再保留普通配置中30天的旧值。轮转已触发过期日志自动回收；未手工删除 data 内文件。

### API 准入档案载荷清理（2026-10-12）

主机自动清理新增显式退役准入载荷阶段。只有Owner确认登记、且摘要核验历史安装链证明已被替代的批次才可清理；当前/previous、未消费现行approval、活动使用、`.keep`及安全异常继续保护。只删除`package.tgz`和`payload/application.jar`，保留原始admission/authority/evidence及小证明，另写退役记录；剩余目录是证据档案，不是完整可安装输入。未登记批次不会因日期旧自动删除，不能泛化为“准入目录最多两份”。规则与Owner登记/撤回命令见 `/home/isp/docs/API_ADMISSION_RETENTION.md`。用户保护的Runtime迁移恢复备份不受本规则影响。

### `/home/isp/hosts`

业务部署目录：

| 目录 | 用途 |
| --- | --- |
| `/home/isp/hosts/cyf/api` | 现行 API 实体部署目录（2026-10-07 从 `/opt` 迁回），root:root 0755；保留旧辅助文件和业务日志，`bak/` 仍是旧备份兼容链接，`backups/` 指向生产备份。 |
| `/home/isp/hosts/cyf/web/www` | `chaoyoufan.cn` 主站静态页面。 |
| `/home/isp/hosts/cyf/web/kit` | `kit.chaoyoufan.cn` 和 `task.chaoyoufan.cn` 静态页面。 |
| `/home/isp/hosts/cyf/static/material` | `mat.chaoyoufan.cn` 静态素材站。 |
| `/home/isp/hosts/jia` | JIA 微服务 jar 和静态站点。 |
| `/home/isp/hosts/jia/web/www` | `jia.chaoyoufan.cn` 静态页面。 |
| `/home/isp/hosts/jia/web/wx` | `wx.chaoyoufan.cn` 静态页面。 |

### `/home/isp/baks`

统一备份根目录（实体目录均在此处）：

| 目录 | 用途 |
| --- | --- |
| `/home/isp/baks/production-api` | 现行 API 发布备份、`release-records/` 发布记录及 `voice-stt-redis4-20261001-records/` 旧发布证据；原 `/opt` 入口保留兼容软链接。 |
| `/home/isp/baks/legacy-api` | 旧版 `/home/isp/hosts/cyf/api` 的备份和发布记录。 |
| `/home/isp/baks/legacy-web` | 旧版 CYF Web 的静态站点备份和发布记录。 |
| `/home/isp/baks/flow-api` | Flow API 的回滚 JAR；Flow 状态实体位于 `/home/isp/state/cyf-api-flow`；旧入口和发布记录仍在迁移收口中。 |
| `/home/isp/baks/host-cleanup` | 主机磁盘清理脚本与架构文档修改前的备份，按时间戳分目录。 |

兼容路径 `/home/isp/hosts/cyf/api/backups`、`/home/isp/hosts/cyf/api/bak`、`/home/isp/hosts/cyf/web/bak` 和 `/var/lib/cyf-api-flow/backups` 都是指向上述实体目录的软链接。保留这些链接以支持历史发布记录与旧 Flow 写入，不能删除或替换为新的实体目录。

`hosts/jia` 当前包含这些 jar：

- `cyf-api-kit.jar`
- `jia-api-material.jar`
- `jia-api-point.jar`
- `jia-api-task.jar`
- `jia-api-user.jar`
- `jia-api-wx.jar`
- `jia-server-config.jar`
- `jia-server-eureka.jar`
- `jia-server-gateway.jar`

### `/home/isp/bin`

运维脚本集中在这里：

| 脚本 | 用途 |
| --- | --- |
| `/home/isp/bin/nginx.sh` | Nginx `start|stop|restart|reload`。 |
| `/home/isp/bin/mysql.sh` | MySQL `start|stop|restart`。 |
| `/home/isp/bin/redis.sh` | Redis `start|stop|restart|status`。 |
| `/home/isp/bin/rabbitmq.sh` | RabbitMQ 启动脚本，目前 stop/restart 分支未实现实际停止逻辑。 |
| `/home/isp/bin/elasticsearch.sh` | Elasticsearch `start|stop|restart|status`。 |
| `/home/isp/bin/logstash.sh` | Logstash `start|stop|restart|force-reload`。 |
| `/home/isp/bin/jia.sh` | JIA jar 通用启停脚本，参数形式见下文。 |
| `/home/isp/bin/cyf_api_kit_start.sh` | isp 生命周期兼容入口，转交 `/home/isp/bin/cyf_api_kit.sh`；源码部署已禁用。 |
| `/home/isp/bin/jenkins.sh` | Jenkins 启停脚本，默认端口 `49001`。 |
| `/home/isp/bin/arthas.sh` | 启动 Arthas。 |
| `/home/isp/bin/certbot.sh` | 续期证书，使用 DNS TXT 验证和 Nginx restart hook；由 `/etc/crontab` 每天 03:17 检查续期。 |
| `/home/isp/bin/alidns.sh` | Certbot DNS 验证用的阿里云 DNS hook。 |
| `/home/isp/bin/clear_disk.sh` | 磁盘恢复入口（每 30 分钟由 crontab 运行）。先执行受部署状态和锁保护的 Flow 保留策略；低于 5 GiB 时，逐文件清理已核验的旧临时发布载荷、精确白名单缓存、旧日志及超过 30 天的非发布 deliverables。临时目录不再整树删除；源码、证据、数据库、当前部署与固定回滚保持保护；恢复目标 8 GiB，执行日志持久化。 |

## 3. Nginx 架构

主配置：`/home/isp/apps/nginx/conf/nginx.conf`

关键点：

- 运行用户：`isp isp`。
- pid：`/home/isp/apps/nginx/nginx.pid`。
- 全局错误日志：`/home/isp/logs/nginx.log`。
- vhost 引入：`include vhost/*.conf;`。
- 证书统一引用 `/etc/letsencrypt/live/chaoyoufan.cn/` 下的 `fullchain.pem` 和 `privkey.pem`。

域名映射：

| 域名 | 类型 | 后端/目录 | 日志 |
| --- | --- | --- | --- |
| `api.chaoyoufan.cn` | API 反代 | `http://127.0.0.1:10018` | `/home/isp/logs/access/api.chaoyoufan.cn.log` |
| `chaoyoufan.cn`, `www.chaoyoufan.cn` | 静态站 | `/home/isp/hosts/cyf/web/www` | `/home/isp/logs/access/chaoyoufan.cn.log` |
| `task.chaoyoufan.cn`, `kit.chaoyoufan.cn` | 静态站 | `/home/isp/hosts/cyf/web/kit` | `/home/isp/logs/access/kit.chaoyoufan.cn.log` |
| `mat.chaoyoufan.cn` | 静态素材站 | `/home/isp/hosts/cyf/static/material` | `/home/isp/logs/access/mat.chaoyoufan.cn.log` |
| `dwz.chaoyoufan.cn` | 短链跳转 | 重写到 `https://api.chaoyoufan.cn/dwz/view/$1` | `/home/isp/logs/access/dwz.chaoyoufan.cn.log` |
| `deploy.chaoyoufan.cn` | Jenkins 反代 | `http://127.0.0.1:49001` | `/home/isp/logs/deploy.chaoyoufan.cn.log` |
| `eureka.chaoyoufan.cn` | Eureka 反代 | `http://127.0.0.1:10016` | `/usr/logs/eureka.chaoyoufan.cn.log` |
| `jia.chaoyoufan.cn` | 静态站 | `/home/isp/hosts/jia/web/www` | `/home/isp/logs/jia.chaoyoufan.cn.log` |
| `wx.chaoyoufan.cn` | 静态站 | `/home/isp/hosts/jia/web/wx` | `/home/isp/logs/wx.chaoyoufan.cn.log` |
| `mq.chaoyoufan.cn` | RabbitMQ 管理后台反代 | `http://127.0.0.1:15672` | `/home/isp/logs/mq.chaoyoufan.cn.log` |

常用命令：

```bash
/home/isp/apps/nginx/sbin/nginx -t
/home/isp/bin/nginx.sh reload
/home/isp/bin/nginx.sh restart
```

## 4. 业务服务

### `cyf-api-kit.jar`

现行部署目录：`/home/isp/hosts/cyf/api`

现行生命周期脚本：`/usr/local/sbin/cyf-api-kit`

- 使用 JRE：`/opt/cyf/runtime/temurin-21-jre/bin/java`。
- 监听端口：`10018`，由 `api.chaoyoufan.cn` 反代。
- 运行 pid、运行时记录在 `/run/cyf-api/`；生命周期日志实体位于 `/home/isp/logs/cyf-api/`，`/var/log/cyf-api` 是兼容软链接。
- 发布备份实体目录：`/home/isp/baks/production-api`；旧路径 `/home/isp/hosts/cyf/api/backups` 仅为兼容软链接。

常用排查：

```bash
/usr/local/sbin/cyf-api-kit status
ps -ef | grep -w /home/isp/hosts/cyf/api/cyf-api-kit.jar | grep -v grep
tail -n 200 /home/isp/logs/cyf-api/*
tail -n 200 /home/isp/logs/access/api.chaoyoufan.cn.log
```

`/home/isp/hosts/cyf/api` 已是现行部署目录，不再标作旧版目录。`/home/isp/bin/cyf_api_kit_start.sh` 仅转交 isp 的生命周期包装入口；root 使用 canonical 命令，不从旧 `package.tgz` 解包部署。

### JIA 微服务

部署目录：`/home/isp/hosts/jia`

通用脚本：`/home/isp/bin/jia.sh`

脚本参数形式：

```bash
/home/isp/bin/jia.sh start <jar文件名> <应用参数>
/home/isp/bin/jia.sh stop <jar文件名>
/home/isp/bin/jia.sh restart <jar文件名> <应用参数>
/home/isp/bin/jia.sh init <域名> <本地端口>
```

脚本内部默认使用 `/home/isp/apps/jdk8`，启动日志写到 `/home/isp/hosts/jia/logs/startup.log`。

注意：`init` 会在 `/home/isp/apps/nginx/conf/vhost/` 下生成 `<域名>.conf` 并 reload Nginx。该脚本生成的 access log 路径是 `/usr/logs/...`，和当前主要日志目录 `/home/isp/logs` 不完全一致，改动前要确认。

## 5. 中间件

### MySQL

- 程序目录：`/home/isp/apps/mysql`
- 数据目录：`/home/isp/apps/mysql/data`
- socket：`/home/isp/apps/mysql/mysql.sock`
- pid：`/home/isp/apps/mysql/mysql.pid`
- 端口：`3306`
- 日志：`/home/isp/logs/mysql.log`
- 启停：`/home/isp/bin/mysql.sh start|stop|restart`

当前数据目录中可见数据库包括 `jia`、`jia_dev` 等。不要直接编辑 `*.ibd`、`ibdata*`、`ib_logfile*`。

### Redis

- 程序目录：`/home/isp/apps/redis`
- 配置：`/home/isp/apps/redis/etc/redis.conf`
- pid：`/home/isp/apps/redis/var/redis.pid`
- 端口：`6379`
- 启停：`/home/isp/bin/redis.sh start|stop|restart|status`

### RabbitMQ

- 程序目录：`/home/isp/apps/rabbitmq`
- 依赖 Erlang：`/home/isp/apps/erlang`
- 启动脚本：`/home/isp/bin/rabbitmq.sh start`
- 管理后台：本机 `15672`，经 `mq.chaoyoufan.cn` 反代。
- 数据和插件展开目录：`/home/isp/apps/rabbitmq/var/lib/rabbitmq`
- 日志：`/home/isp/apps/rabbitmq/var/log/rabbitmq`

`/home/isp/bin/rabbitmq.sh` 的 stop/restart 分支目前没有实际停止命令。需要停止时优先使用 RabbitMQ 自带工具确认，例如 `rabbitmqctl stop`，不要只依赖当前脚本。

### Elasticsearch

- 程序目录：`/home/isp/apps/elasticsearch`
- 配置：`/home/isp/apps/elasticsearch/config/elasticsearch.yml`
- 数据：`/home/isp/apps/elasticsearch/data`
- 日志：`/home/isp/apps/elasticsearch/logs`
- pid：`/home/isp/apps/elasticsearch/pid`
- 启停：`/home/isp/bin/elasticsearch.sh start|stop|restart|status`

脚本使用 `su isp -c` 以 `isp` 用户启动。

#### Elasticsearch 关键服务监控（2026-10-30核验）

- 既有聚义厅健康监控 `/usr/local/libexec/cyf-juyiting-health.py` 已将 `elasticsearch` 纳入组件，由 `/etc/cron.d/cyf-juyiting-health` 每分钟调度。使用受保护的本机凭据检查集群健康及 `chat_memory` 零结果检索、分片完成情况；连续3次失败确认故障，纳入既有事件通知流程。
- 此监控的自动恢复仅覆盖 API，不会自动启动或重启 Elasticsearch；不应将进程存活当作搜索健康。监控状态命令：`/usr/bin/python3 -I /usr/local/libexec/cyf-juyiting-health.py --status`，与执行中检查共用锁，忙时可能返回 deferred。
- 12:04 本机独立调用现行探针返回 `es_search_ok_green`；之前监控已记录 ES 故障，待定时检查连续健康后按既有规则恢复。监控通知是否实际送达未在本次验证。12:06检查发现定时监控正等待 API 发布锁，快照暂未更新；有其他 API 启动操作持锁，不抢占或终止，释放后需确认定时检查恢复。ES 日志显示磁盘超过90%高水位，须尽快扩容，避免再次触发索引只读。

#### Elasticsearch 堆精简（2026-10-20）

- `/home/isp/bin/elasticsearch.sh` 的 start/restart 两个入口统一 `ES_JAVA_OPTS='-Xms256m -Xmx256m'`，覆盖原 `-Xmx384m`；`config/jvm.options` 原本已为 256m/256m，未改数据目录、安全配置或索引。
- 新PID `3811742` 已核对最终 JVM 参数为 256m/256m。认证集群健康 GREEN，15 个主分片全部就绪、无未分配分片；生产 API `/actuator/health` 返回 HTTP 200。启动期间发生过 GC overhead 告警，不据此承诺长期负载稳定或总 RSS 仅256MiB。
- 首次启动因本次操作工具的100秒等待阈值触发回退；延长启动等待至300秒后重试成功，不是修改Elasticsearch自身启动超时。后续启停须等待旧PID退出，避免直接restart分支的未等待行为造成重叠启动。
- 修改前脚本、JVM配置、架构文档及检查证据：`/home/isp/baks/host-cleanup/es-heap-256m-20261020-233525/`。回滚应只恢复该批原 `elasticsearch.sh`，经受控停止/等待/启动恢复原256m/384m；不要恢复数据快照。

### Logstash

- 程序目录：`/home/isp/apps/logstash`
- 主配置：`/home/isp/apps/logstash/config/logstash.yml`
- pipeline 配置：`/home/isp/apps/logstash/config/task/`
- pid：`/home/isp/apps/logstash/logstash.pid`
- 启停：`/home/isp/bin/logstash.sh start|stop|restart|force-reload`

当前脚本启动 `bin/logstash -f config/task/`。

## 6. 日志位置

| 日志 | 路径 |
| --- | --- |
| Nginx 全局错误日志 | `/home/isp/logs/nginx.log` |
| Nginx access 日志 | `/home/isp/logs/access/*.log`、部分 vhost 在 `/home/isp/logs/*.log` |
| MySQL 日志 | `/home/isp/logs/mysql.log` |
| `cyf-api-kit` 生命周期日志 | `/home/isp/logs/cyf-api/`；原 `/var/log/cyf-api` 保留兼容软链接 |
| 旧版 `cyf-api-kit` 启动/GC 日志 | `/home/isp/hosts/cyf/api/logs/` |
| JIA 启动日志 | `/home/isp/hosts/jia/logs/startup.log`；历史 `/usr/logs` 的实体统一位于 `/home/isp/logs/jia-legacy/` |
| RabbitMQ 日志 | `/home/isp/apps/rabbitmq/var/log/rabbitmq/` |
| Elasticsearch 日志 | `/home/isp/apps/elasticsearch/logs/` |
| Logstash 日志 | `/home/isp/apps/logstash/logs/` |

磁盘清理脚本：

```bash
/home/isp/bin/clear_disk.sh
```

该脚本提供 `check`、`plan`、`clean` 三种模式。保留原有低于默认 5 GiB 才触发、恢复目标 8 GiB 的策略；`plan` 不删除文件。先委托 `/usr/local/libexec/cyf/flow_host_cleanup.py` 处理 Flow 指定备份/下载目录，API 回滚 JAR **总计最多保留 2 份（固定回滚 1 份计入总数，另保留最新 1 份不同内容的历史 JAR）**，API/Web 各最近 2 个下载包。Flow 发布状态未完成时安全停止其保留策略，不扩大清理范围。

#### 2026-10-07 自动清理修复

- 文件类型判断改为 Shell 类型判断与 `stat` 数字字段，不再比较会被中文 locale 翻译的 `%F`。中文 Cron 与英文交互环境行为一致。
- **禁用一般临时目录递归删除**：不再因 `/tmp/cyf-*`、`/var/tmp/cyf-*` 或 `tmp.*` 等顶层名称和年龄就 `rm -rf`。普通 `/var/tmp` 数据库、源码和验证目录不进入通用清理。
- 通用临时清理仅逐文件处理 `/tmp/tsx-0`、`/tmp/node-compile-cache` 下超过 `TMP_KEEP_DAYS`（默认 2，`find -mtime +2` 即满 3 天）的安全缓存，以及同龄、确实为空的 `/tmp/.org.chromium.Chromium.*` 目录（仅 `rmdir`）。保留缓存父目录，跳过 `.keep`、软链接、硬链接、额外挂载、权限不安全及占用中的文件。
- 旧发布载荷由 `/usr/local/libexec/cyf/release_payload_cleanup.py` 独立逐包核验。仅识别 `/var/tmp/cyf-mmd-release-<数字版本>-main-<8位日期>/` 下的直接子文件 `candidate-api.jar`、`rollback-api-<8至64位小写十六进制>.jar`，以及 `/var/tmp/cyf-mmd-integration-cloud-main/run<数字>-artifact.tgz`。文件保留期 `RELEASE_KEEP_DAYS` 默认 2，满 3 天后才考虑；不以父目录修改时间判断包年龄，其他包默认保护。
- 临时包清理持有主机清理锁、发布载荷清理锁和现有 API/Web 部署锁；API 状态必须是已安装且无恢复要求，Web 必须已完成在线验证。校验当前部署和固定回滚内容 SHA256、进程命令/cwd/FD/mmap、受限运行配置及外部软链接引用。硬链接只在**整个 inode 的所有别名都是同批合格候选**时删除，否则全部保留；回收量按 inode 去重。
- 云构建包含测试结果或发布证据时，先将除唯一 `application.jar` 外的所有普通文件/目录成员保存在 `/home/isp/baks/host-cleanup/release-payload-records/<时间戳-PID>/`，逐成员内容哈希验证成功才删除旧包。拒绝路径穿越、软/硬链接、设备文件、未知嵌套载荷、超出记录大小/数量限制的归档；不向文件系统解包。清理计划、逐文件删除审计、结果一起保存在该目录。
- 不删除临时发布目录或其中的源码、数据库、部署脚本、报告、记录；不修改中央 API/Web 备份、Flow 保留策略或 Codex 会话。删除前刷新引用/部署状态并检查文件身份，通过不跟随软链接的目录 FD 逐文件 unlink；达到恢复目标停止。
- `/usr/local/libexec/cyf/host_cleanup_log.py` 在 `clean` 执行时持久化 stdout、stderr、开始/结束时间和退出码到 `/home/isp/logs/clear_disk.log`，即使现有 Cron 仍重定向 `/dev/null`。日志为 root:root 0600，拒绝软链接/硬链接/不安全文件，8 MiB 轮转并最多保留 5 个轮转文件；日志不可安全打开时不执行清理。Cron 的每 30 分钟频率保持不变。
- 隔离回归测试：`/home/isp/bin/tests/test_clear_disk.sh`、`/home/isp/bin/tests/test_release_payload_cleanup.py` 、`/home/isp/bin/tests/test_flow_host_cleanup.py` 和 `/home/isp/bin/tests/test_host_cleanup_processes.py`；测试仅删除自行创建的夹具，不清理真实数据库、发布包或 deliverables。

#### 2026-10-07 补充审计修复

- 配置引用扫描区分部署 JAR/归档/二进制与文本配置，避免生产大 JAR 被误判为超大配置而阻断旧包清理；文本配置仍有 2 MiB 安全上限。读取软链接配置/服务单元的实际内容，目录软链接在深度剪枝前检查；扫描范围仍有限，不声称覆盖全磁盘引用。
- 通用临时缓存计划显示安全跳过项，清理区分占用和其他安全跳过，不再将过滤后的零候选误报为零跳过。
- `clean` 参数校验前接入持久日志；输出实时写入，不再等待满 4 KiB 或子进程结束。整数参数按最多 9 位十进制解析，允许前导零，拒绝超范围值。
- 清理完成后仍低于最低可用空间时退出码为 3，避免磁盘未恢复却报告成功。独立阶段因保护规则安全停止仍按原策略警告，不代表所有跳过均为失败。
- 本轮不扩大删除白名单、不更改阈值/定时频率/Flow 保留和锁策略。当前服务日志主动轮转、Flow 锁长期等待告警、低空间通知尚未接入，需单独设计；数据库、源码、会话、证据和中央回滚备份继续保护。

#### 2026-10-07 深度审计补充

- 修复 Flow 去重与历史保留计划相互冲突：固定回滚优先，同内容选择最新副本；保留计算排除已计划删除的重复副本，当时按最近 **10 个不同内容的历史 JAR** 计算（已由下述“两份总上限”规则替代）。固定回滚、API/Web 各 2 个下载包和部署锁顺序/等待策略不变，不增加删除目录。
- Flow 保留目录及下载子目录的 `.keep`（含悬空软链接）生效；通过 mountinfo 拒绝文件/目录绑定挂载及非根挂载下的载荷。删除前再次检查目录、挂载和文件完整身份，逐级 `O_NOFOLLOW` 打开父目录，通过目录 FD unlink 和 fsync，不经可替换的绝对路径直接 unlink。
- NPM 缓存不再整树 `rm -rf`：仅扫描 `/root/.npm/_cacache`、`/root/.npm/_logs` 最大 12 层，逐文件清理满 `TMP_KEEP_DAYS + 1` 天、root 所有且安全/未占用的文件；保留全部目录，跳过 `.keep` 子树、保护名称、硬链接、软链接和绑定挂载。journald 200 MiB vacuum 与 DNF/YUM 自带缓存清理沿用既有策略。
- 旧日志候选收窄为 `*.log.gz`、数字轮转（含 `.gz`）及 `*.log.<8位日期>T<6位时间>[.gz]`，最大扫描深度 4；不将任意 `.gz` 或 `.log.*` 当作可删日志。保留当前日志、证据/回滚等保护名称、`.keep` 子树、挂载及占用文件，删除前重验年龄和身份，达到恢复目标停止。
- `plan` 补齐上述 NPM 缓存与旧轮转日志的候选数量、跳过数量和预计回收量；移除一直未分类累加的“挂载跳过 0”字段，将其明确计入安全/挂载/keep 汇总。
- 日志接入对 FIFO 非阻塞打开并拒绝，轮转前完整检查整条链避免发现危险条目时已部分改名，失败路径关闭 FD/释放锁。清理子进程使用独立进程组；日志写入失败或 logger 收到 TERM 时停止该组，避免 Flow 子进程留下继续清理。错误区分“未启动”与“已启动”，不把运行中日志故障误报成从未执行。
- 新增隔离 Flow 回归测试 `/home/isp/bin/tests/test_flow_host_cleanup.py`。本轮只读检查生产目录，未主动执行真实 `clean`；无服务重启。未接入新的通知、主动服务日志轮转或部署锁超时策略。不同属主/未知格式日志继续保护，不为增加回收量放宽权限和格式判断。

#### 2026-10-07 进程与日志边界审计

- 新增只读元数据扫描器 `/usr/local/libexec/cyf/host_cleanup_processes.py`，缓存、日志、deliverables 与 Flow 使用 FD/cwd/exe/mmap 路径和设备/inode 键保护占用文件；即使 FD 已关闭、文件仅被内存映射或通过别名打开，也不按闲置删除。只读进程元数据，不读取命令参数、环境或文件内容。
- 权限不足、无可见进程、畸形映射等导致快照不完整时拒绝将其解释为“无占用”。Shell 接收 NUL 分隔完整快照和末尾成功标记；失败将占用状态置为未知并保护全部候选，即使外层条件表达式抑制 Bash errexit 也不能继续按闲置删除。正常消失的进程/FD允许跳过；路径中的换行不再拆成多条。
- 日志打开逐级通过 `O_NOFOLLOW` 目录 FD，拒绝任意父目录软链接；轮转操作锚定同一父目录 FD，并重验预检条目身份。每次输出检查日志路径仍对应已打开 inode，fsync 后才继续；父路径/日志条目替换或写入故障停止清理组，不向替换目标继续写入。
- logger 监测 Bash 非正常结束，不等待孤儿子进程持有的输出管道自然关闭；停止其清理进程组，并将信号退出转换为常规 `128+信号编号`（例如 TERM 为 143）。业务服务不加入该独立清理组，也不重启业务服务。SIGKILL/掉电无法执行异常处理，不承诺全局事务或跨命名空间完整引用分析。
- 新增隔离扫描器测试 `/home/isp/bin/tests/test_host_cleanup_processes.py`；既有缓存/Flow/logger 测试增加失败快照、仅 mmap 占用、软链接父目录、路径替换、信号退出及孤儿清理验证。
- 补齐白名单根目录上方的祖先挂载检查：缓存、临时文件、日志、deliverables 只允许根挂载 `/` 下的候选；不只检查白名单内部的挂载，避免通过祖先绑定挂载或独立卷删除其他存储的数据。与根分区 5/8 GiB 空间目标保持一致。
- 只增强保护，不扩大删除白名单；5/8 GiB 阈值、默认保留期、Flow 保留数量、cron 频率和部署锁顺序不变。主动日志轮转/通知/锁等待告警仍未新增。

#### 2026-10-07 备份保留数量调整（当前生效规则）

- `/home/isp/baks/flow-api` 的合格回滚 JAR **总计最多 2 份**：`record.json` 固定回滚占 1 份，另保留最新 1 份不同内容的历史 JAR；不是固定回滚外再保留 2 份。内容重复时可能只剩 1 份，不补足数量。
- API/Web 下载包仍各保留最近 2 份。Flow 数量保留阶段不受 5 GiB 空间触发条件限制，沿用每 30 分钟 Cron、部署状态、锁、去重、逐文件审计和删除前复核。
- 两份是正常合格、未占用文件的保留目标，不凌驾于安全保护之上：`.keep`、占用、挂载、权限/身份异常或部署状态不完整时跳过/停止，可能暂时超过两份。发布记录、批准记录、审计证据、兼容软链接不作为可删除的 JAR 备份。
- 本次仅修改现有 Flow 自动规则。`production-api` 当前有 2 份 JAR 备份，旧版 API/Web 当前部署备份未超限，但这些目录**尚未接入自动两份保留规则**；不能宣称整个 `/home/isp/baks` 已有统一数量上限。其他发布目录、配置备份、Agent 备份及脚本修改备份不因本次调整进入删除白名单。
- 本次通过隔离测试及真实只读 `plan` 核验；未主动执行生产 `clean` 或重启服务。后续 Cron 会按新规则执行。

### Deliverables 清理范围（2026-09-27）

- 固定目录：`/home/isp/wsps/cyf/deliverables`。它是工作区保护策略中的**有限例外**，不递归删除整个目录。
- 仅考虑修改时间超过 `DELIVERABLES_KEEP_DAYS`（默认 30，使用 `find -mtime +30`，即满 31 天后）的 `.jar`、`.zip`、`.tgz`、`.tar.gz`、`.tmp`、`.part` 普通文件。
- 无条件保留 `releases/`、`release/`、`verification/`、`design/`、`maintenance/`、`cleanup/`、`diagnostics/`、`records/`，以及证据、备份、回滚、报告、源码、隐藏目录和依赖目录。发布目录尚未接入当前部署/回滚引用识别，**不能按文件年龄直接删除发布包**。
- 任意父目录的 `.keep` 标记均保护其子树。跳过符号链接、硬链接、多余挂载点、非 root 所有或权限不安全的文件/父目录；候选文件保持“非组/其他可写”要求。现有 root:root 0775 目录允许 root 组写权限，不更改目录权限。
- 跳过进程打开/内存映射的候选文件及进程工作目录下的候选文件；进程扫描不完整时保护候选；删除前刷新进程状态、重验文件身份，并通过不跟随符号链接的目录描述符只删除该文件。保留所有目录及非白名单文件。
- 沿用低于 5 GiB 才触发、达到 8 GiB 停止的规则；`plan` 展示候选数量和预计回收量，不删除文件。Flow 的计划失败不妨碍展示独立临时文件和 deliverables 计划。
- 隔离回归测试：`/home/isp/bin/tests/test_clear_disk.sh`，只对自行创建的临时夹具测试删除，不操作真实 deliverables。

只读预览：

```bash
/home/isp/bin/clear_disk.sh plan
# 可按需调整保留期（仅本次调用）：
DELIVERABLES_KEEP_DAYS=60 /home/isp/bin/clear_disk.sh plan
```

## 7. 证书和 HTTPS

证书路径：

```text
/etc/letsencrypt/live/chaoyoufan.cn/fullchain.pem
/etc/letsencrypt/live/chaoyoufan.cn/privkey.pem
```

续期脚本：

```bash
/home/isp/bin/certbot.sh
```

该脚本使用 DNS TXT 手工挑战流程，实际 DNS 增删由 `/home/isp/bin/alidns.sh` 调用阿里云 CLI 完成，续期后执行 `/home/isp/bin/nginx.sh restart`。

## 8. 常用巡检命令

```bash
ps -ef | grep -E 'java|nginx|mysql|redis|rabbit|elastic|logstash' | grep -v grep
ss -lntp
df -h
du -sh /home/isp/baks /home/isp/apps/* /home/isp/hosts/* /home/isp/logs 2>/dev/null | sort -h
/home/isp/apps/nginx/sbin/nginx -t
tail -n 200 /home/isp/logs/nginx.log
```

## 9. 操作注意事项

- 这里是生产式运行目录，优先读配置和脚本，再执行启停。
- 不要直接编辑中间件数据目录：`apps/mysql/data`、`apps/elasticsearch/data`、`apps/rabbitmq/var`、`apps/redis/var`。
- Nginx vhost 修改后先执行 `/home/isp/apps/nginx/sbin/nginx -t`，通过后再 reload。
- 旧版 `cyf-api-kit` 部署脚本依赖 `JAVA_HOME`，执行前确认当前 shell 的 `JAVA_HOME`；现行生产 API 使用 `/usr/local/sbin/cyf-api-kit`。
- Flow API 回滚 JAR 的保留策略由 `/usr/local/libexec/cyf/flow_host_cleanup.py` 直接管理 `/home/isp/baks/flow-api`；其状态、下载缓存和锁仍在 `/var/lib/cyf-api-flow`。
- 脚本中存在业务密钥/加密参数，文档只记录位置和用途，不复制明文敏感值。
- 如果发现 `ps` 中的运行参数和脚本文档不一致，以当前运行进程和最近部署脚本为准，再回写本文档。


## 10. 系统目录与业务资产边界（2026-10-04，服务器本地时间）

- `/usr` 保留操作系统/RPM 文件及正常的 `/usr/local` 全局工具、云安全/云助手/云效组件；不能按体积或“未见进程”直接删除或搬迁包管理器管理的文件。自建日志不继续放成 `/usr` 下的实体目录。
- `/var/lib` 保留系统状态、Flow 部署状态及扫描器数据库等运行资产；`/var/tmp` 里的正在运行的测试数据库、源码与验证证据不自动删除。目录名带 tmp/cache 不等于可删。
- 现行 `/home/isp/hosts/cyf/api` 与 `/opt/cyf/runtime/temurin-21-jre` 是既有生产架构的明确例外，保持原位，避免影响生命周期管理；厂商的 `/opt/alibabacloud/hbrclient` 保持官方目录和配置，不移动运行中的客户端缓存。
- 自建可复用工具链归 `/home/isp/apps`；业务部署归 `/home/isp/hosts`；日志实体归 `/home/isp/logs`；发布记录、备份和审计归 `/home/isp/baks`；源码、任务证据和工作树留在工作区，不因磁盘压力一概删除。
- 统一日志父目录 `/home/isp/logs` 保留原多角色写权限及属主，增加 sticky bit（1777）保护日志目录条目；迁入子目录保持原有属主/权限，不能无条件 chmod 成全员可写。

本次归档整理后的兼容关系：

| 兼容入口 | 实际磁盘目录 |
| --- | --- |
| `/var/log/cyf-api` | `/home/isp/logs/cyf-api` |
| `/usr/logs` | `/home/isp/logs/jia-legacy` |
| `/home/isp/hosts/cyf/api/release-records` | `/home/isp/baks/production-api/release-records` |
| `/home/isp/hosts/cyf/api/.voice-stt-redis4-backups-20261001` | `/home/isp/baks/production-api/voice-stt-redis4-20261001-records` |
| `/root/.gradle/wrapper/dists/gradle-9.3.1-bin/e6fpmcitnr2cbhj7h6pdk7btv/gradle-9.3.1` | `/home/isp/apps/gradle/9.3.1` |
| `/run/cyf-pwa-api-r19-static-verifier-r35-preparation/gradle-9.3.1` | `/home/isp/apps/gradle/9.3.1` |

原 `/var/lib/cyf-memory-recovery` 已完成分类处理，不再是需要保护的现存载荷目录：Gradle 发行包只保留统一磁盘副本；其余六处经完整迁移清单/内容校验、进程与当前运维引用复查后，按用户不保留更早回滚和闲置旧任务产物的授权清理。只删除对应旧依赖/构建产物及其原临时软链接，未删除原任务源码、证据、Git或数据库；原隐藏 tmpfs 的进程和挂载未改变。

旧迁移清单、日志、校验记录保留在 `/home/isp/baks/host-cleanup/authorized-layout-cleanup-20261003T235401+0800/memory-offload-records`。本次仅整理位置并删除已明确退役的旧包，不代表其他数据库、会话历史、ACK反回退状态或现行服务可以按日期直接删除。


## 11. Agent 旧发布载荷清理（2026-10-06）

按用户“不保留旧版本”的明确授权，本次删除 47 个未使用的 Agent 历史发布目录，不额外保留旧版回滚载荷。范围仅限：

- `/home/isp/apps/codex-ws-agent/releases`：保留主 Agent 的 `current` 所指版本。
- `/home/isp/apps/codex-ws-agent-instances/wuyong-local/releases`：保留吴用本地实例的 `current` 所指版本；不能因其发布日期早于主 Agent 就视为可删。

清理前核验 `current`、外部部署软链接、配置引用和运行进程；清理期间持有发布/主机清理锁，并逐文件检查身份，不跟随符号链接、不跨挂载点。当前两个 Agent 的发布树核验未变，进程 PID 未变，未重启服务。

旧发布的证据、发布清单及依赖清单作为历史记录迁至 `/home/isp/baks/host-cleanup/agent-old-releases-20261006/records`，删除清单和结果位于同级目录。这些记录不是可运行的旧版本备份。Agent 的 `data`、`managed-host`、各 Codex home、会话和工作区均未清理。

该授权不扩大为删除 API/Web 回滚备份、数据库、其他运行时、源码或任务证据；未新增定时清理任务，也未修改现有 Flow 保留策略。

## 12. API 部署目录迁回（2026-10-07）

- 现行实体目录为 `/home/isp/hosts/cyf/api`；`/opt/cyf/service/api` 为指向该目录的兼容软链接，不存在第二套运行 JAR。迁移使用同一已安装 JAR，不构建、不发布新版本、不改数据库或 Nginx。
- 保持 root 管理的 JAR/配置/密钥、`cyf-api` 非特权运行身份、Temurin 21 JRE、`/run/cyf-api` 记录、现有端口/发布锁和 Flow 回滚状态。启动、安装、Schema、监控及临时载荷清理工具同步使用新路径。
- `/home/isp`、`/home/isp/hosts`、`/home/isp/hosts/cyf` 及部署目录改为 root:root 0755，防止非特权用户替换可信目录。没有递归修改业务子目录权限；isp 仍可使用其既有可写工作区，受保护父目录的新建/改名需 root。
- 新路径的 `backups`、`release-records` 和历史记录链接沿用统一 `/home/isp/baks/production-api`；`bak` 继续指向 `/home/isp/baks/legacy-api`。旧 `/opt` 兼容路径通过新路径到达同一份备份。
- 迁移前被覆盖的旧版文件位于 `/home/isp/baks/legacy-api/before-api-relocation-<时间戳>`；原 `/opt` 小型配置/证据保存在本次私有迁移审计目录，已移除其中重复的现行 JAR。旧日志保留，新复制的历史发布日志位于 `/home/isp/hosts/cyf/api/release-history-logs`。
- 旧发布归档 `/home/isp/hosts/cyf/releases` 最新普通文件 mtime 为 2026-09-16 22:07:08；`/home/isp/releases/cyf` 为 2026-08-01 17:56:34。受限现行运维脚本/Nginx 引用检查未发现使用；这是历史归档状态证据，不代表仅凭年龄即可整树删除。未删除两个旧发布目录。

### API 唯一部署路径约束（2026-10-07）

- 新版 API **安装后的最终 JAR** 只能写入 `/home/isp/hosts/cyf/api/cyf-api-kit.jar`；生产进程的 `-jar` 与工作目录必须分别为该 JAR 和 `/home/isp/hosts/cyf/api`。Nginx 仍将请求转发到其本机 10018，不直接指向磁盘目录。
- 正式测试/构建仍在 Flow 云端；构建目录、同 Run 云端制品、`/var/lib/cyf-api-flow` 下载/状态、`/home/isp/baks` 备份不强制搬进生产目录。不能将“唯一部署目录”误解为在生产目录本机构建或把备份写在此处。
- `/opt/cyf/service/api` 只能是到唯一部署目录的兼容软链接，不再生成独立实体部署。旧 `/home/isp/hosts/cyf/releases`、`/home/isp/releases/cyf` 不作为新生产 API 的安装目标。
- 已同步 installed 与仓库 `ops/ci/aliyun-flow/host/` 的生命周期、事务安装和 Schema 默认路径；只修改本次路径/祖先安全/FD 关闭变化，不用较旧源码覆盖现行脚本的其他修复。
- 重装主机控制脚本、修改发布路径或发布后，应运行只读一致性检查：`/usr/bin/python3 -I -B /home/isp/bin/tests/test_cyf_api_canonical_path.py`。检查生产/仓库默认路径、物理目录权限、兼容链接、控制器入口和运行进程；不能只看配置保存成功。

## 13. 用户授权的旧载荷清理（2026-10-07）

- 按用户“都删除”的授权，逐文件删除生产目录的旧 `package.tgz` 与 rejected-schema JAR、`/home/isp/releases/cyf` 历史 JAR、`/home/isp/wsps/cyf/deliverables/releases` 历史 API/Web 包，以及 `/var/tmp/cyf-voice-implementation-20260930` 闲置 JAR 和展开依赖。未整树删除源码、证据或工作区依赖软链接。
- 共删除 2216 个文件，按唯一 inode 释放 2.361 GiB；依赖与发布包硬链接按完整合格别名组处理，不把多个别名重复计为释放空间。
- `/home/isp/hosts/cyf/releases` 有 bash 工作目录占用，本次保留其三份旧载荷，未停止该进程。`/var/tmp/cyf-mmd-web-inspection-main-probes` 主要是源码、测试夹具和截图证据，保留；指向工作区的依赖软链接不跟随、不删除目标。旧目录仍存在，不能据此声称六个目录全部删除。
- 生产 `/home/isp/hosts/cyf/api` 目录、现行 JAR、配置、统一备份和兼容软链接保留。清理持有主机/Flow/API/Web 协调锁，未重启服务，完成后 API 健康 UP，现行 JAR 与固定回滚校验未变。
- 本次是一次性授权清理，不扩大定时清理白名单。审计：`/home/isp/baks/host-cleanup/authorized-old-payload-cleanup-20261007T204252+0800`。

### 旧 releases 载荷补清理（2026-10-07）

用户将 SSH 终端移出 `/home/isp/hosts/cyf/releases` 后，完整进程快照确认占用解除。继续按既有授权删除两份旧 API JAR 和一份旧 Web tar.gz，共释放 520.4 MiB；仅保留该目录中的小型源码/证据/发布记录，目录本身未删除。持有既有主机和发布协调锁，生产 API 健康 UP，现行 JAR 与固定回滚 SHA256 均未变，未重启服务。审计：`/home/isp/baks/host-cleanup/old-release-payload-cleanup-20261007T205749+0800`。前述因终端占用而跳过三份载荷的状态已解除；不扩大定时清理白名单。


## 14. Runtime v1 Agent 租户清单修复（2026-10-08历史记录，现行架构见第2节）

- `cyf-agent-runtime-v1@linchong.service`、`@lujunyi.service`、`@wuyong.service` 已恢复运行；安装目录为 `/home/isp/apps/cyf-agent-runtime-v1/<实例>`，环境配置为 `/etc/cyf-agent-runtime-v1/<实例>.conf`，经本机 `http://127.0.0.1:10018` 使用 Runtime v1 API。
- 用户确认这三个实例的正确租户是字符串 `"0"`。原本地清单仍保留旧租户值，服务端安装记录已是 `0`，身份校验返回 `REBINDS_REQUIRED`，运行程序退出。该问题不是本次重启独有；旧心跳记录停在 2026-09-15 11:40（Asia/Shanghai）。
- 本次备份后修改三个 `manifest.json` 的 `tenantId` 为 `0`，按现有递归排序 JSON 算法重算清单哈希，并以数据库事务、原版本/原哈希/原凭据哈希条件核验，同步三条既有安装记录的 `manifest_sha256`、`version`、`update_time`。未更改数据库租户、安装 ID、客户端/Agent 身份、凭据、登记状态或 ACK 记录；未重建/发布 API。
- 清单保持原权限，由现有 Node 校验器验证；恢复后实例均为 `active/running`，Runtime v1 session 为 `ACTIVE`，租户为 `0`，实际心跳已更新。不要只改清单租户而遗漏本地与服务端哈希一致性，也不要绕过身份检查。
- 备份与修复记录：`/home/isp/baks/host-cleanup/agent-runtime-tenant0-repair-20261008T001758+0800`（私有权限，不保存明文凭据）。该修复未改开机启动顺序或 systemd 重试策略；API 应先恢复再启动这三个实例，不能据此声称整套业务已配置重启自恢复。

## 15. 磁盘告急及清理锁开机恢复（2026-10-09）

- 13:27 根分区仅剩约 150 MiB，空间不足而非 inode 耗尽。相对 10 月 7 日调查，主要增长在 `/home/isp/wsps` 工作树、`/tmp/cyf-aam-*` 合并测试目录、`/var/tmp` 任务与测试数据库，以及 Root Gradle 缓存；不是统一业务日志或 ACK 状态突然增大。
- 服务器上次启动为 2026-10-07 23:52:40 +0800。位于易失 `/run/lock` 的 `cyf-clear-disk.lock` 与 `cyf-release-payload-cleanup.lock` 缺失，两个 Python 清理器此前安全停止。检查无对应删除后仍持有的锁 FD 后，按既有 root 属主及 0644/0600 模式重建。
- 新增 `/etc/tmpfiles.d/cyf-host-cleanup.conf`，使用 tmpfiles `f` 条目在开机创建上述两锁；不用 `f+`，不截断或替换已有锁 inode。`systemd-tmpfiles --create` 已核验。主入口继续由 `/etc/crontab` 每 30 分钟运行；Flow/旧临时发布包只读 plan 已恢复成功。
- 执行既有自动清理，Flow 保留两份固定策略释放 0.572 GiB。主清理退出码 3 表示仍未达到空间恢复目标，不表示删除安全检查被绕过。DNF clean 成功但本机已无可回收软件缓存，释放 0。
- 额外逐文件清理当时无占用的 Root NPM 缓存、两处 `/tmp/cyf-aam-merge-develop-20261008` 的 `node_modules` 依赖，以及确认占用解除后的 Root Gradle 缓存，共释放 1.186 GiB。保留所有软链接、多别名硬链接、安全/占用异常文件、锁与目录。下次本地验证这些临时任务时需重新安装依赖；默认正式构建仍走 Flow。
- 总共按文件分配块释放 1.758 GiB（当前仍低于 5 GiB 触发线，未达到 8 GiB 恢复目标）。未删除源码/Git、未提交代码、测试数据库、生产数据、ACK 防回退状态、当前包和固定回滚；未停止或重启服务。API 健康 UP，唯一部署路径 8 项测试通过。
- 此次应急缓存清理不扩大定时脚本白名单或改变保留期；下一步如需退役旧工作树、测试数据库或中间件，应独立确认任务完成、未提交内容、引用与备份。审计：`/home/isp/baks/host-cleanup/disk-pressure-20261009-132722`。

## 16. 可重建产物生命周期及本地告警（2026-10-09）

- 主入口新增 `/usr/local/libexec/cyf/rebuildable_cache_cleanup.py`，仍由现有每 30 分钟 Cron 调用；低于 `MIN_FREE_GB`（默认 5 GiB）触发、恢复目标 8 GiB、Flow 两份策略不变。
- 全局白名单仅新增 `/root/.gradle/caches`：普通文件的 mtime 与 ctime 均满 `GRADLE_CACHE_KEEP_DAYS + 1` 天（默认 3 天），整个缓存根未见占用才考虑删除。保留目录、锁文件和 `gc.properties`，不删除 Gradle 发行包、插件安装或服务运行时。
- 临时任务/工作树不因年龄或无进程而自动认定完成。Root 必须显式登记完成任务及具体 `node_modules` 相对路径；登记要求任务空闲、物理目录、NPM 项目 `package.json`/`package-lock.json` 存在且安全。私有登记表 `/var/lib/cyf-host-cleanup/completed-tasks.json` 持久化，最多 256 个任务。初始没有自动登记任何既有任务。
- 合格任务基目录只包含 `/tmp`、`/var/tmp` 下直接 `cyf-*` 子目录，以及 `/home/isp/wsps/worktrees`、`/home/isp/wsps/private-maintenance`、`/home/isp/wsps/cyf/.worktrees` 的直接任务子目录。每个任务仅支持最多 8 个、最多 3 层相对路径的 `node_modules`，不支持整任务目录、源码/Git、任意 build 目录、报告、测试数据库或 ACK 状态。完成满 `COMPLETED_TASK_KEEP_HOURS`（默认 24 小时）后才考虑登记依赖中完成前存在的文件；完成后变更项目配置或新生成文件保持保护。任务恢复时先撤销完成登记。
- 新阶段持有既有主机清理锁；沿用根挂载、祖先 `.keep`（含悬空链接）、root 所有/安全权限、软/硬链接保护和扫描失败关闭策略。每次删除前刷新完整 FD/cwd/exe/mmap 快照，复核任务/依赖目录 inode、文件签名及 SHA256，沿不跟随链接的父目录 FD unlink。最多扫描 16 层、200000 个文件，超限无部分计划删除；所有目录保留。
- 删除意图先 fsync 到 `/home/isp/baks/host-cleanup/rebuildable-cache/audit.jsonl`，逐文件记录删除结果；8 MiB 轮转、最多 5 个轮转文件，日志不可安全写入则停止。正常主日志仍是 `/home/isp/logs/clear_disk.log`。
- 清理阶段失败即使空间已高于触发线也返回 4，不再静默成功；空间仍不足最低线沿用退出 3。Logger 每次结束写 root:root 0600 `/home/isp/logs/clear_disk.status.json`，记录完成时间、退出码、剩余字节和状态；低于 1 GiB 为 critical，低于 5 GiB 或退出非零为 warning。同时发送本机 syslog `cyf-host-cleanup` 标签的告警，日志打开/写入失败也有 syslog 错误。
- 这是本机日志和状态告警，尚未接入邮件、短信、聊天或外部推送；不能声称用户已自动收到通知。部署锁长时间等待超时告警、任务目录容量预算、源码/测试数据库退役和调用任务平台自动完成登记仍未实现；未扩展为整树删除。

任务生命周期命令（root；完成登记须从任务目录外执行，任务内终端也需退出）：

```bash
# 任务重开/重试前，撤销完成登记
/usr/bin/python3 -I -B /usr/local/libexec/cyf/rebuildable_cache_cleanup.py mark-active \
  --task-root /tmp/cyf-example-task

# 确认任务已完成、不再使用临时依赖，并从 /home/isp 执行
/usr/bin/python3 -I -B /usr/local/libexec/cyf/rebuildable_cache_cleanup.py mark-complete \
  --task-root /tmp/cyf-example-task --node-modules root/web/node_modules

# 仅预览，不登记也不删除
/usr/bin/python3 -I -B /usr/local/libexec/cyf/rebuildable_cache_cleanup.py plan
# 查看本地告警和最近状态
journalctl -t cyf-host-cleanup --since today
cat /home/isp/logs/clear_disk.status.json
```

新增隔离测试：`/home/isp/bin/tests/test_rebuildable_cache_cleanup.py`、`/home/isp/bin/tests/test_cleanup_alerts.py`；既有 Shell/Flow/临时载荷/logger/进程扫描回归继续核验。此次规则修改审计：`/home/isp/baks/host-cleanup/cleanup-rules-20261009T142842+0800`。


## 17. 发布记录 v3 清理兼容及 v2 历史备份退役（2026-10-10）

- `schema_version` 是安装状态 JSON 的格式版本，不是数据库 Schema 或业务版本。当前 API 记录已经是 v3；本次只升级清理器，不重新安装/发布 API、不改写安装状态记录、不执行源码构建。
- `/usr/local/libexec/cyf/flow_host_cleanup.py` 接受已确认安装的 v2/v3。v3 复用 root 管理 `/usr/local/sbin/cyf-api-flow-deploy` 的 `local_install_record` 契约校验器；安全读取固定校验器及祖先，核对 release 绑定、候选摘要、备份路径/名称，并校验实际固定回滚 JAR SHA256 等于 previous_sha256。v3 的清理审计 Run 为 null，不伪造数字 Flow Run。旧临时发布包清理器沿用同一状态读取入口。
- 已将现行主机清理器及其回归测试同步到 `/home/isp/wsps/cyf/ops/maintenance`，避免仓库旧副本重新安装后恢复不兼容状态；未修改部署工具或业务源码。
- 用户授权删除 v2 旧备份后，使用显式 `--retire-v2-backups`。此选项仅允许 plan/clean 且要求当前状态为 v3；用 v3 release 绑定的 precondition/installedRecord 引用、大小及摘要证明先前 v2 状态，复核旧备份实际摘要。不会扫描或删除任意 JSON/备份目录，现行 pin 无条件保留。清理继续持有部署锁、核验进程占用、挂载、keep、文件身份，逐文件记录审计；重复执行已退役项无操作。
- 此次移除 `/home/isp/baks/flow-api` 的两份 2026-10-07 历史回滚 JAR；保留现行 v3 记录固定的 2026-10-09 回滚 JAR。发布前提快照、审批、配置和其他小型证据保留，不把“v2备份”扩大为所有 legacy-api/production-api 目录。另按原有两份下载策略移除一份旧 Web package.tgz，总释放 614252544 字节（约 585.8 MiB）。
- 默认最多两份策略不变，这是上限而非必须补足两份；本次退役后 Flow API 回滚载荷剩一份。v2 读取能力只用于识别合法历史状态，不将现行 v3 降级。

显式历史退役命令（非新增 Cron 项）：

```bash
/usr/bin/python3 -I -B /usr/local/libexec/cyf/flow_host_cleanup.py plan --retire-v2-backups
/usr/bin/python3 -I -B /usr/local/libexec/cyf/flow_host_cleanup.py clean --retire-v2-backups
```

本次升级/退役审计：`/home/isp/baks/host-cleanup/schema-v3-cleanup-20261010T013618+0800`。

正常 clear_disk.sh clean 已实测：Flow 与旧临时载荷阶段成功，无 v3 格式错误；最终退出 3 仅因剩余约 2.0 GiB 低于 5 GiB，API 健康 UP，生产 JAR 校验不变。主机 51 项 Flow、54 项临时载荷、81 项 Shell、8 项唯一部署路径测试通过；仓库镜像 51 项测试通过，已同步其进程占用扫描依赖。


## 18. 本地发布产物与共享缓存的磁盘职责核验（2026-10-10）

- `/var/lib/cyf-api-local-admission/admitted/<批次>` 是已准入包、展开载荷及证据的持久化目录；三批当前约 1.35 GiB，不是三套生产服务。现行生产安装仍是唯一 `/home/isp/hosts/cyf/api/cyf-api-kit.jar`。
- `/var/cache/cyf-gradle-local` 是项目 orchestration 本地发布入口的共享 Gradle home，当前约 0.90 GiB；正式本地发布默认 home/build-cache 行为见项目 `ops/orchestration/README.md`。此事实说明不扩大本次主机清理或发布授权。
- 现行自动白名单的 `/root/.gradle/caches` 不覆盖该共享 home；完成任务 NPM 依赖规则也不覆盖 build/JAR/tgz、准入批次或源码工作树。未登记完成的任务保持保护。新增根需独立生命周期设计与引用/锁/校验保护，不能因为目录名带 cache/tmp 就整树删除。
- 10月7日深度报告的 35.075 GiB 是排除生产保护数据的 du；完整 df 为 39.388 GiB。10月10日09时调查完整已用约 48.36 GiB，净增约 8.97 GiB：主要来自 /tmp、/var/tmp、准入与共享缓存，源码工作区本身净减约 0.95 GiB。数据库文件也有约 0.61 GiB 增长；未发现 GiB 级已删未释放异常。
- 凌晨02:22新安装记录为 v3 / 1.14.2；随后新建回滚载荷，不是被删除的 v2 旧包恢复。最多两份策略维持。

详细互斥目录对账及只读元数据：`/home/isp/baks/host-cleanup/disk-growth-20261010T090537+0800/REPORT.md`。本次未删除文件、修改清理规则、停止服务或更改数据库。


## 19. 双端云效后的主机磁盘职责与清理（2026-10-19）

- 前后端正式测试、构建与版本发布按项目2026-10-17规则统一Flow；本机不再默认生产打包。2026-10-19后端已安装Run162与前端已安装Run233均实时查询SUCCESS；两端构建日志显示云端工作区`/root/workspace/repo_0`、包目录`/root/workspace/packages`、临时build位于云端`/tmp/cyf-backend-flow-5m.<随机名>/build`。云端`/root/.gradle/caches`由Flow缓存归档管理，不是本机缓存，主机定时清理不覆盖云端worker/OSS。
- 主机实体API/Web状态与下载根分别为`/home/isp/state/cyf-api-flow`、`/home/isp/state/cyf-web-flow`；现行安装helper仍引用同名`/var/lib`过渡绑定挂载，不是第二份数据，不能在本次磁盘清理中直接卸载/重写证据。API incoming包保护，生产JAR仍唯一安装路径；回滚在`/home/isp/baks/flow-api`。
- 每30分钟既有清理已覆盖Flow下载/回滚两份上限。本次修复历史0600包被仅0644规则跳过的问题，计划与执行均允许root安全的0600/0644，其他权限、身份、挂载、keep、活动使用、状态和pin保护不变；主机及仓库同步，新增3测试，Flow各54项通过。
- 用户授权单次清理：闲置共享Gradle缓存文件1.390GiB、与保留准入原件SHA256一致的临时API副本1.995GiB、旧Web包0.596GiB。保留锁/目录、源码/Git/证据、数据库、Agent状态、Runtime恢复备份、准入原件与现行/固定回滚，未重启服务。可用空间约5.02GiB，仍未达到8GiB恢复目标。
- `/var/cache/cyf-gradle-local`仅本次精确清理，不扩展自动白名单。通用临时build/JAR/tgz和未确认完成任务仍不自动删除。当前API Flow安装记录为v2，不携本地v3 installedRecord链；旧准入退役登记无法沿当前链验证，继续保护，不修改历史证明或凭年龄强删。
- 审计与完整目录/测试/回收结果：`/home/isp/baks/host-cleanup/unified-cleanup-20261019T1700/REPORT.md`。本节是2026-10-19核验，不把旧章节当作现行本地发布授权。


## 历史备份显式退役（2026-10-23）

用户确认最新版稳定并明确授权后，已删除下列8个历史备份目录内的全部普通备份文件；保留目录入口和兼容软链接，不改变目录职责和自动清理规则。合计591文件、约4.85GiB，无额外完整载荷副本；旧章节涉及这些恢复点的记录只作历史事实，不再代表可用备份。

- `/home/isp/baks/cyf-runtime-submission-1.2.2`
- `/home/isp/baks/cyf-external-runtime-1.2.3-20261021`
- `/home/isp/baks/cyf-runtime-health-20261021`
- `/home/isp/baks/cyf-common-image-runtime-1.2.4-20261022`
- `/home/isp/baks/host-cleanup/shm-unused-20261020-232338`
- `/home/isp/baks/production-api`
- `/home/isp/baks/legacy-api`
- `/home/isp/baks/legacy-web`

`/home/isp/baks/flow-api`的现行回滚包、生产文件和持久运行状态未动，未发布或重启服务。退役清单与核验：`/home/isp/baks/host-cleanup/delete-approved-backups-20261023/REPORT.md`。

### MySQL 内存在线调优（2026-10-23 12:22 CST）

- 经用户授权，MySQL 8.0.21 在线 SET GLOBAL 并同步 `/home/isp/apps/mysql/my.cnf`：max_connections=50、join_buffer_size=524288、sort_buffer_size=1048576、read_buffer_size=262144、read_rnd_buffer_size=524288、key_buffer_size=8388608、temptable_max_ram=134217728；innodb_buffer_pool_size 保持512MiB。
- `vm.swappiness` 从60降至10，持久化 `/etc/sysctl.conf`（`/etc/sysctl.d/99-sysctl.conf` 为同一配置入口）。未重启MySQL、未断开既有连接、未swapoff；连接级GLOBAL默认值仅由新连接继承，不承诺存量Swap立即下降或既有会话缓冲立即释放。
- 变更前连接数11、启动约8天内峰值17；调整后变量与配置读回一致，短采样没有持续换出，API健康HTTP200约0.57秒。此为短时核验，不代替高峰期延迟、连接数和临时表落盘监测。
- 回滚副本及原GLOBAL值：`/home/isp/baks/mysql-memory-tuning-20261023-122203/`（含my.cnf.before、sysctl.conf.before、rollback.sql、before.json及applied.json）。此目录是本次变更的回滚材料，不沿用此前历史备份删除授权。


### 五项恢复备份继续退役（2026-10-23 13:43 CST）

用户再次明确授权删除上轮列出的5项恢复备份，已清空以下备份内容，保留空目录入口；对应旧章节仅为历史事实，不再代表这些恢复点可用。未另外保存完整载荷副本。

- `/home/isp/baks/cyf-agent-runtime-v1/20261023-fixed-dir`
- `/home/isp/baks/runtime-path-unify-20261012`
- `/home/isp/baks/cyf-material-read-runtime-1.2.6-20261022-r3`
- `/home/isp/baks/cyf-pdf-joint-runtime-1.2.5-20261022`
- `/home/isp/baks/node-unified-20261022`

文件/链接分配空间约3.47GiB；现行Flow固定回滚、Runtime app与持久状态、配置、生产与数据库未动。未重启服务、未修改清理规则或MySQL保留期（运行/持久/配置仍为259200秒，即3天）。审计：`/home/isp/baks/host-cleanup/delete-five-recovery-backups-20261023/REPORT.md`。


## 2026-10-24 磁盘应急清理与MySQL故障观察

- 根分区曾仅剩约90MiB。单次回收闲置Root NPM下载缓存约186MiB；MySQL错误日志6.43GiB同目录轮转，等待旧写入进程全部释放后无损压缩至约54MiB，经解压字节数与SHA256核验后移除未压缩旧文件。归档`/home/isp/logs/mysql.rotated-20261024-1004.log.gz`；日志现行路径仍为`/home/isp/logs/mysql.log`，新文件mysql:mysql 0640。未新增自动轮转规则或修改保留期。
- 清理后根分区可用约6.5GiB、使用率89%；既有清理入口正常退出0，最低5GiB线恢复但尚未达到8GiB目标。没有删除数据库、业务部署、固定回滚、任务源码/证据或Runtime恢复备份。
- 同时观察到MySQL InnoDB space=0/page=5读失败、MY-011906/MY-011899与MY-013183断言，服务反复崩溃，10:15快照inactive/dead、NRestarts=1390；API进程在但健康未通过。此为观察时刻，不能当持续状态；本次未修复数据库、未主动停启服务，不把磁盘恢复视为业务恢复。
- 审计与校验：`/home/isp/baks/host-cleanup/disk-pressure-20261024/REPORT.md`。

## 2026-10-25 用户授权删除三批历史 Runtime 恢复载荷

- 用户针对已列出的约7.2GiB历史Runtime备份明确授权删除，实际回收7.13GiB（7,653,224,448字节分配空间）。精确范围为`/home/isp/baks/cyf-agent-runtime-v1/20261023-version-gate`、`20261024-skill-readiness-r2`、`20261024-skill-adoption`三批中的`state.tar`与`old-program`旧程序文件/链接；目录入口、小型发布与恢复说明记录保留，并新增退役标记。三批不再具备完整恢复能力，没有另行保存完整载荷副本；旧章节提及相应备份可恢复的说明已被本节覆盖。
- 清理期间新生成的`20261025-position-only`备份约2.3GiB不属于前述7.2GiB范围，完整保留。MySQL恢复包、现行Runtime app/持久状态/配置、数据库、生产及Flow固定回滚、源码/任务未动。
- 删除前确认三批无进程占用，持有主机清理及Runtime版本发布锁，严格按清单校验文件身份，符号链接仅删除链接、不跟随目标。现行Runtime发布记录及manifest摘要、MainPID 3438981前后未变；服务active/running，API健康UP；未发布或重启服务。清理后根分区可用约9.39GiB，达到8GiB恢复目标。自动清理策略未变。
- 删除清单、逐项审计与结果：`/home/isp/baks/host-cleanup/delete-runtime-backups-20261025/`。


## 2026-10-25 晚间授权退役五批 Runtime 恢复载荷

- 用户在磁盘复查后明确要求删除刚列出的Runtime备份。本次仅退役`/home/isp/baks/cyf-agent-runtime-v1/`下`20261025-position-only`、`20261025-runtime-companion`、`20261025-history-isolation`、`20261025-image-size`、`20261025-model-schema`五批的`state.tar`/`state.tar.gz`及`old-program`文件和链接；保留目录、小型记录与退役标记。五批不再具备完整恢复能力，未另存完整载荷；上文“position-only完整保留”是早间历史事实，现被本节覆盖。
- 共删除18513项文件/链接，回收11215884288字节分配空间（约10.45GiB）；完成时根分区可用约11.34GiB。
- 持有主机清理及Runtime发布锁，检查进程占用、挂载、keep及文件身份；现行Runtime发布记录/manifest摘要和PID前后一致。现用程序、Agent身份/会话/业务状态、配置、数据库、MySQL恢复材料与Flow固定回滚未动；未发布或重启服务，自动清理策略未变。Runtime active/running，API健康HTTP200。
- 删除清单与逐文件审计：`/home/isp/baks/host-cleanup/delete-runtime-backups-20261025-evening/`。
