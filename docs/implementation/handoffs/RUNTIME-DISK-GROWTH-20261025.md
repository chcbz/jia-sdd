# RUNTIME-DISK-GROWTH-20261025

- Owner：本聊天，单一 developer；用户授权：“好，落实下去”。目标是减少公共程序/可重建缓存的重复占用及重启遗留，不保证业务数据零增长，不按容量拒绝新增 Agent。
- 规则：已读 `/home/isp/wsps/cyf/AGENTS.md`、`ops/orchestration/README.md`、`/home/isp/wsps/chcbz/isp-install/AGENTS.md`、Runtime self-host 指南。接口基准 `/home/isp/wsps/cyf/api/docs/interface-standard.md`，版本1.4（2026-10-24）；本任务不改 wire。
- 工作区：复用 `/home/isp/wsps/chcbz/isp-install`，develop；仅既有未知归属 `specs/` 未跟踪内容，保留。不创建 worktree/子 Agent，不发布API/Web，不调用付费模型，不清身份、HOME、会话、inbox/outbox、ACK或业务事实。
- 源码：本地与2026-10-25本次 ls-remote 的 develop 均为 `c4688cf792a2a24668b601fab6e5cea624df7e0c` / tree `f550488e1cfeb1a344e579d5622c3a48896bda5f`；线上 current.json 是Runtime1.3.6，同commit/tree，Flow5264702/50。根HEAD `5e6ab2b6f1a156c320189f17d76941fbe623738a`，大量无关脏内容不覆盖。
- 基线：21:44三份快照1,240,240,128字节；`.tmp/plugins`三份321,814,528字节；app310,415,360字节；Runtime备份22,233,088字节。初始6.1GiB备份下降属于其他操作，不记为本任务收益。
- 已核实根因：binaryMeasurementCache 已跨profile复用同一来源身份的快照，但回收只在创建新快照时扫描当前HOME。三份owner PID分别3561946/3627888/3438981，当前统一服务PID3627888；命中缓存的其他HOME漏扫历史遗留。插件三份是同一Git0722921d历史副本，源码新managed HOME仅写config、不复制旧HOME；不能把它们冒称已证实的每Agent自动生成泄漏。
- 实施范围：测量入口在缓存命中前回收每个准确profile根；年轻失效快照在原保护窗口后做有界后续回收；补新增Agent/重启/共享/活进程/归属/完整性回归。共享只复用受信程序，不放松HOME和授权隔离。
- 最早定向验证：Node内建test的快照/worker合成fixture，轻量运行；不执行全量构建/生产打包。本机快照维护仅调用已有安装模块的受控回收，保护PID/starttime、实际执行引用、属主、权限、前缀和年龄；未证实安全的插件副本先保留。
- 验收：合成多Agent不增加程序快照份数；缓存命中不漏扫其他HOME；重复重启与短间隔重启后旧快照收口；当前/他人活进程和未知不安全目录不删；来源、伴随程序、资源和snapshot篡改仍拒绝。程序行为变更升版；源码交付、Flow制品、安装和线上核验分别记录。
- 非目标：不把整个HOME共享/迁到公共目录，不建全局可写插件仓库，不按天数盲删备份，不修改其他任务的清理/发布。备份去缓存必须有恢复闭包验证，不能仅凭目录名删减完整HOME保护。
- 定位/实现/验证/等待：待汇总；状态：实现中。

## 实施、自检与集成（2026-10-25）

- 修复已提交并push组件develop：`0425c11db88ed66ce1192d5215217ff82fabbd02` / tree `feaff4928666b53deb946ba0fe2fb043118fd21f`；push后ls-remote回读相同。Runtime声明候选1.3.7；原主checkout既有`specs/`未跟踪内容保留，未创建工作树。
- 测量入口在缓存返回前扫描每个准确HOME；窗口内孤立快照只安排去重、unref的延迟回收，并重新核对全部原有保护。HOME/身份/授权/会话/业务状态不共享。没有删除摘要校验、来源独立inode、伴随工具/资源、PID/startTime/实际执行引用或权限保护。
- 新增5项轻量合成回归，加原worker完整性测试共6项本机通过；覆盖100 HOME共享、缓存命中根回收、延迟收口、owner变活后保留、三轮独立进程重启及实际活执行引用/危险权限/符号链接保留。源码的更广CHAT测试初次因缺`@imagemagick/magick-wasm`在import阶段不可运行：没有借生产node_modules、没有删测试，转Flow固定lock安装执行。
- 云效5264702 Run51 SUCCESS，job542669625；精确上述commit/tree，Node24.22.1、同Run `npm ci`。新增长/worker6项及既有完整性7项，共13通过、0失败、0skip。Run createTime至terminal updateTime共220秒（总耗时，不是单作业）；本机控制面另保留560秒受控取消保护，未触发。Run不部署，不等待外部验收，不调用模型。
- 同Run证据压缩包SHA256 `83e70499dd54246e12852b141c4a6326847c10d08190c610d9c1abc6052f8e52`；内部受测源码包SHA256 `809af634df657b268cbcbb4185f59746b062f025393898d572df1d7b1421e19c`。下载核对source.json、内层每个成员与Git commit字节完全一致；这是测试与源码证据包，不冒充可安装生产制品。
- 借用前确认无活动Run、保存原配置；结束后确认无他人活动Run且配置仍是本任务候选，已恢复原配置并readback APPLIED。恢复canonical SHA256 `1fc8acb3e9dd8718da40eec866394b016a0b5b09b1b9335a01ce8b668f4eca12`。首个start响应因INIT暂无sources为UNKNOWN，但真实返回Run51；仅只读核查后续精确来源，没有二次启动。

## 线上回收与生效边界

- 仅调用现行已安装模块`reclaimStaleCodexAppServerSnapshots`，按三个明确HOME执行：删除林冲旧PID3561946和吴用旧PID3438981的两份失效程序快照；当前陆俊义目录中PID3627888的共享快照保留。释放801,153,024字节，即764.039MiB（约0.746GiB）。不删除插件目录、备份、临时任务、会话或业务数据。
- 回收前后服务PID3627888相同、现行程序摘要相同，三个通道connected/registered/ready。没有重启或安装新程序；这是缓存维护与通道健康证明，不是新版本上线或付费业务验收。
- **当前运行仍是Runtime1.3.6/c4688cf；1.3.7自动回收修复尚未发布生效。** develop合入和CI成功不授予生产发布。后续在明确版本化发布授权及恢复闭包下，由Flow生成并安装同Run生产制品，不能把本次源码证据包当可安装包或本机补打生产包。
- 插件占用原估算约200MiB的额外收益未实现：三份为历史Git副本，源码新managed HOME不克隆旧HOME。未核实的外部消费者不能猜测，保留现状，不把这部分宣称为新Agent的已证实线性泄漏。备份去缓存同理，未削弱完整HOME一致恢复保护。
- 稳定知识回写组件`docs/cyf-agent-runtime-v1-self-host.md` §9.5。证据目录：`docs/implementation/handoffs/runtime-disk-growth-20261025/`，含summary、线上维护明细、本机与云端测试、同Run证据包。控制面私有原值/日志保存`/home/isp/baks/cyf-agent-runtime-v1/20261025-disk-growth-control/`；本任务临时目录收口删除，不清理其他任务文件。
- 状态：开发/自检/组件集成和一次线上安全回收完成；生产自动回收启用待受控发布。定位/实现/验证分项耗时未完整计量，Flow执行220秒不冒充端到端周期。

## 用户追加授权：历史插件副本清理（2026-10-25 22:42 +08）

- 用户明确要求清理历史副本。三个准确 HOME 的 `.tmp/plugins` 均为 Git0722921d，同一文件内容清单，无修改/未跟踪/忽略文件；定向扫描配置、代码、技能链接及进程 cwd/exe/fd/maps/mountinfo 未发现运行引用。只删除这三个目录，未触碰当前共享快照、会话、身份或业务状态。
- 删除前保留一份压缩恢复包并逐成员核对工作树 SHA256；包位于 `/home/isp/baks/cyf-agent-runtime-v1/20261025-plugin-history-cleanup/plugins-recovery.tar.gz`，SHA256 `01ce696686ab07acb1d739f3901f662db3739d8f1130c960713517c70498cdb0`。清单、准确路径和恢复方式见同目录 `cleanup.json`。
- 状态目录释放321,810,432字节（306.90MiB）；单份恢复包占51,859,456字节（49.46MiB），净释放约257.44MiB。状态目录实测789,041,152字节（752.49MiB）。没有声称备份也释放了307MiB；本次恢复包不按Agent复制。
- 共享快照仍在首个创建它的profile HOME，由进程内cache供其他profile复用；本次不在线迁移运行中的快照、不调整共享路径。1.3.7自动回收修复仍未部署。

## 用户调整：直接使用系统Codex（2026-10-25 22:50 +08）

- 用户最终要求：“那就不要搞共享快照了，使用系统的codex可执行程序即可”。覆盖上一条公共目录迁移意向；尚未提交/部署的公共路径改动已只撤回本任务自己的差异，无线上迁移。
- Owner仍为本聊天；复用isp-install develop基线0425c11/tree feaff492。候选1.3.8：不复制程序、资源或伴随工具，测量/缓存与spawn直接指向profile所绑定系统CLI解析出的native executable；保留来源权限、完整性、真实/proc inode/hash、身份/HOME和沙箱隔离。内部snapshotPath/Identity旧字段仅为消费者兼容名称，不再表示程序副本。
- 验收：100独立HOME/重复重启0份新增程序；旧失效快照按原owner/live-process/年龄保护回收；系统程序/伴随工具/资源漂移在spawn前拒绝，真实进程身份仍验证；typed inspection只读挂载系统vendor根、隔离与网络约束不变。系统更新不再有私有不可变副本保障，需要受控更新、重新测量与协调运行中进程，不声称消除全部TOCTOU。
- 授权范围为Runtime直接执行模式切换与无引用旧快照收口，不更新系统Codex版本、不发布API/Web、不调用付费模型、不重建身份或回放任务。走现有5264702同Run测试/打包/受控安装，单Run总上限600秒；准备/安装/通道健康/业务验收分开记录。

### 直接执行候选与正式验证进行中

- 组件develop已push并远端回读：`187f3a91fb2445610ea6aa4092751fbf6f9797e6` / tree `48d7b644db076fb13a9f5f6b414a6029412d3ee1`，Runtime1.3.8。本机最终8项轻量回归通过；更广CHAT import仍缺本地Magick依赖，未借生产node_modules，正式全集转Flow。
- 实际本机系统CLI只读测量通过：`/usr/local/bin/codex`解析到npm发行的native可执行文件，版本0.164.0、主程序SHA256 `b93f6811d3f653f0fb83be4050d857fb9abbb111dfa2ce160563327daff7f306`；没有创建程序副本。probe的tmp由CLI版本命令自行创建，不作为程序快照。
- Flow候选前三次配置写入被`FLOW_API_INVALID_YAML`明确拒绝，读回原配置未变，没有启动Run。之后复用既有已部署Runtime YAML结构（含gitee/serviceConnection、既有job形状），只替换固定源码/测试打包/安装命令后readback APPLIED；未将未确认的具体schema字段原因冒称已定位。正式只启动Run52一次，INIT返回UNKNOWN仅因sources尚空，沿返回ID只读核查，无重复启动。
- 正式5264702/52固定上述commit/tree，复用既有Runtime回归selector与collateExecutionPayload/同Run npm ci生产payload合同，增加0副本增长测试；受控安装沿固定app、相同发布锁、完整停写状态备份、已验证Node/Python保留与同Run代码/npm输入闭包执行，不迁移身份/业务状态。安装完成后Run结束，通道验收另在本机记录。当前仍待真实Run结果，不能据此宣称已上线。

### 首次正式Run归因与修正

- Run52 FAIL（createTime至终态以原始run52/run-status-last.json为准，控制面请求耗时249秒），没有进入安装、线上仍1.3.6。546项中534通过、10失败、2继承skip：1项资源符号链接测试仍期待已删除的SNAPSHOT_FAILED错误包装；9项local-script因本次简化CI解压Node未沿用原脚本`--no-same-owner`，与trustedFile精确属主保护冲突。未删除测试或放松源/脚本权限保护。
- 只修测试预期至实际RESOURCE_SYMLINK拒绝；CI恢复既有Node解压`--no-same-owner`，不是更改运行文件属主或权限。最终候选`4f3fe43feba4cc1d177a1ee87f1d95a0cddc9326` / tree `1ec810bc255d94479b2ecb9bf5b0706586adfdbf`已push。程序版本仍未安装的1.3.8，生产行为与187f3a直接执行实现一致。
- 修正后只启动Run53一次，仍固定完整源码与同Runpayload/npm来源，不重复原输入盲重试；保留完整Run52失败日志与配置。控制面状态仍待终态，安装/健康另记。

### Run53补证与CI布局修正

- Run53终态FAIL，完整日志more:false：546项，535通过、9失败、2继承skip；全部剩余失败为local-script探针。未进入安装，生产未变。前文将9项直接归因归档UID证据不足，予以更正：恢复`--no-same-owner`未解决，不能声称属主已定位为根因。
- 未原样重试。对照Run50已成功脚本，本轮简化版将Node放入CI工作区，与原HOME私有mktemp布局不同；trustedFile检查整条祖先的world-write。恢复已验证HOME私有Node布局、保留no-same-owner，新增真实Node及工作区祖先UID/mode、probeTool诊断；尚待新Run实证，不放松保护、不删除测试。
- Run54在准备阶段被精确源码断言终止：develop被另一任务推进至cda100a/Runtime1.3.9；未执行测试和安装，未覆盖/回退该任务。为不擅自带入其技能管理改动，创建本任务固定候选分支`codex/runtime-system-codex-20261025`指向4f3fe43；Flow来源、触发上下文、预期分支及安装前断言一致调整，随后仅启动Run55一次。程序候选仍1.3.8；不把develop当前版本冒称本次候选。
- 已收到技能管理Owner协同通知：其cda100a基于4f3fe43、候选1.3.9，未借用本任务5264702；本批继续固定1.3.8，不联合带入补丁，不中断其他任务。释放入口前须恢复原配置并通知可借用。
- Run55 FAIL、未进入安装：诊断已实证CI祖先`/root/workspace`为root:root 0777，原工作区Node不满足trustedFile；新Node位于/root私有0700临时目录、整条祖先非world-writable。但本次新增probe诊断放在npm ci之前，导入skill-manifest缺ajv而停止，尚未跑回归。将完整诊断移到同Run锁定依赖安装之后，源码/测试与保护不变，再启动Run56验证；不是原样重试。

## 直接使用系统Codex：已安装与核验

- Runtime1.3.8：固定候选分支`codex/runtime-system-codex-20261025`，commit `4f3fe43feba4cc1d177a1ee87f1d95a0cddc9326` / tree `1ec810bc255d94479b2ecb9bf5b0706586adfdbf`。Flow5264702/56 SUCCESS，请求至终态440秒（低于600秒）；546项中544通过、0失败、2原有skip，未删除或放松测试。已核验HOME私有Node布局probe ready，修复CI布局而非降低权限保护。
- 同Run不可变制品SHA256 `3f8184fa9a17a979753ef8a2d7ccf2992c9fc37ed2df5ed6f7b5a014bf812eb8`；安装保留原发布锁、完整程序清单、停写状态备份及tar compare，保留已验证Node/Python、npm来自同Run lock。固定实体`/home/isp/apps/cyf-agent-runtime-v1/app`，新PID3841558，源码/版本/manifest/current及独立1.3.8.json记录一致，安装后4114项mode/UID/GID/摘要及闭包全部复核。
- 三个静态profile均直接解析`/usr/local/bin/codex`到系统native Codex0.164.0，同主程序SHA256 `b93f6811d3f653f0fb83be4050d857fb9abbb111dfa2ce160563327daff7f306`，measurement kind=system，不再复制Codex程序、助手和资源到HOME；HOME、身份、会话和授权仍隔离。合成100 HOME/重启回归0新增副本。
- 三通道在23:39:10 +08只读确认connected/registered/ready；之后协同Owner通知API5260799/312发布1.17.7，期间观察到ECONNREFUSED/重连，未重启Runtime或重放任务。最终收口时三通道已再次全部ready，独立记录先前成功与外部重连；未调用付费模型/业务任务，不冒称业务验收。
- 静态HOME旧419MiB快照已收口；补查managed旧HOME发现约354MiB快照，其owner PID3071611已不存在，调用本次安装模块原受控reclaimer（owner/startTime/live-process/权限/年龄保护不变）删除1份。静态及managed两状态树现均0份`.cyf-app-server-bin-*`程序快照。不删除managed身份/会话/.tmp或其他任务状态；不能把未检查缓存冒称已清理。
- 完整恢复备份`/home/isp/baks/cyf-agent-runtime-v1/20261025-system-codex`：old-program.tar.gz SHA256 `8a51ab80000003a720140ec77a772de4c2e975b3c2da55793cfbbb52817bce7e`；state.tar.gz SHA256 `19f045164dbd3551571f92fec2ef7eecb6630513d0e7a7dc23ebaaf882a0107f`。备份包括此前managed状态/旧程序快照，属于一次性恢复闭包，不是运行依赖；未擅自删除，不把运行目录释放量冒称整机净释放量。禁止恢复旧状态覆盖新会话/ACK/业务事实。
- 正式证据已迁到`/home/isp/apps/cyf-agent-runtime-v1/release-records/system-codex-20261025/`：installation、test-summary、tests.log、Flow payload清单、channel-verification、managed-snapshot-cleanup、前后du、Run终态及恢复配置readback。原始SDK日志/失败Run/候选脚本等仅归档于上述备份`flow-private-evidence.tar.gz`（私有，可能含签名URL，不公开），不把原始敏感日志放项目文档。
- 确认无活动Run且配置仍本任务候选后恢复5264702原配置，readback APPLIED，canonical SHA256 `1fc8acb3e9dd8718da40eec866394b016a0b5b09b1b9335a01ce8b668f4eca12`。已通知技能管理Owner入口可借用；其下一候选1.3.9/cda100a不属于本批，后续不再写Flow配置/运行程序。临时任务目录在证据归档后删除。
- 效果边界：新增Agent/重启不再新增Codex程序副本；会话、SQLite、日志及有意保留的恢复备份仍可增长，不承诺全部磁盘零增长。当前实现不更新系统Codex；系统程序替换仍需受控更新、测量及协调，保留完整性/身份/锁保护。

### 最终容量读数与协同交接

- 2026-10-25 23:42:55 +08 du allocated：静态状态436.55MiB、managed状态105.79MiB、当前app296.00MiB、Runtime全部备份696.20MiB（随后私有证据归档另约0.31MiB）。旧程序113MiB+完整状态511MiB恢复包为本轮新增备份，未隐藏其磁盘成本；不能把删除约773MiB运行快照等同于整机净省773MiB。
- 静态状态在旧419MiB快照退出后并非预测334MiB：最终只读检查发现linchong HOME的`.tmp/plugins`重新出现约103MiB。这是新的插件缓存观测，不是程序快照；未在Agent运行时反复删除、未把原三份历史清理宣称为“缓存永不再生”。同一时点wuyong还保留业务private-runs/inspection等内容，不因容量目标删除业务事实。本次明确完成的是Codex程序零副本执行；插件缓存与业务数据总量不纳入零增长承诺。
- 23:43后已向技能管理Owner明确“可借用”，其确认采用独立1.3.9候选/备份与精确1.3.8前置；API1.17.7/Run312已由该Owner报告成功。本任务不据其报告冒称参与API验收，不再写5264702/Runtime服务/current记录。后续动态版本应查询其批次，不能把本记录1.3.8永久当成现行版本。
