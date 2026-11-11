# Runtime 程序瘦身与必要状态备份（2026-11-09）

## 当前结果（2026-11-09 08:50 +08接续）

用户后续“继续”已接续为新版本受控安装：Runtime **1.3.69** 已在固定app启用并verified-active，源码`fb9aafbd4c334efe7633f147d5b986de084f45df`、tree`9cd28d72987b671c3be942563b4b9260d306bdca`。当前程序877,481,984→719,044,608字节（约837→686MiB，减少151MiB/18%）；本次实际使用**仅硬链接去重**，不改Python字节、不分离符号，不能把前期211MiB探测上限当作本次收益。真实新备份已使用必要状态策略，排除143个入口、未压缩内容446,546,905字节（约426MiB），未删除源状态。三个通道及现有材料/原生能力核验通过，身份/配置不变、无付费模型调用。

恢复备份仍保留，所以程序减少不等于主机净释放：收尾可用1,677,955,072字节（约1.56GiB）；本次新增恢复点占空间。保留策略plan没有可回收批次，没有删除历史载荷。以下原“未发布/不停启”描述是**第一阶段历史事实**，不是接续后的线上状态。完整接续见本文末节与`docs/implementation/evidence/runtime-footprint-20261109/release-closeout.json`。

## 第一阶段：Owner、范围与固定输入

- Owner：本会话；任务`RUNTIME-FOOTPRINT-20261109`。用户要求一起处理程序占用及必要信息备份，不继续以压缩旧程序为优化主线。只改准备/归档/维护适配；不改Web/API合同，不操作数据库业务数据、不停启Runtime、不发布新应用版本、不转换既有真实备份。
- 已读CYF根AGENTS、工具索引、maintenance说明及外仓AGENTS。技能的旧Flow-only口径由CYF 2026-11-06/08本地规则覆盖；未启动付费Flow。源码、输出和TMP均在普通磁盘，不用tmpfs。
- CYF工作区branch develop，HEAD`c311a4dfb439c88e7ea61aa4aa25064be6ce6ac4`、tree`eae38803fd39dc44599bf6876d60802d91ed5139`。维护文件原已未跟踪，其他大量脏修改未动；本次按实际文件SHA绑定，未提交/合入，不冒充该基线commit已包含本改动。
- 外仓`/home/isp/wsps/chcbz/isp-install`原branch`codex/hall-three-fixes-20261106`，HEAD`c1fc18174b256c90051874485c8c77967efad62a`，原有README/install.sh及new-api脏文件未动。只修改两个Python适配器、对应两份测试及现有self-host文档。未改变他人branch、index或worktree。
- 当前生产Runtime1.3.68/source`92df9eb8de9abf523dd7224e575c43329139a98b`、tree`31d4d7e0899f1692e924c248702fb3f19e2e48fd`；源文件/测试的原版与该生产commit一致，`runtime-source.patch`已通过独立临时index对该commit的`git apply --cached --check`。本地develop仍是旧1.3.9，且不包含生产92df9；未盲合并整条历史，也未声称远端最新（本任务未查询远端）。后续Owner须在真实当前集成基线上接入，不把旧工作区HEAD当生产基线。

## 职责与真实依赖

程序构建/安装准备层负责Python去重/符号分离；归档适配层负责内部硬链接安全提取；状态存储适配层负责确定备份成员。Web/API业务契约不变，无须联动。复用既有freeze/pack/extract、Runtime维护入口、host→release锁和原子切换；无新runner/守护服务/审批或全局台账。

- `freeze-python.py`：冻结自包含Python后、生成sandbox image/制品manifest前，只合并内容、mode、uid/gid、xattr相同的Python/libpython别名。保留全部功能依赖，拒绝外部链接、不安全目录、运行目录和备份目录。兼容既有安装器独占`.cyf-agent-runtime.stage.*`，避免误拒正常暂存。
- `CYF_PYTHON_DEBUG_OUTPUT`为显式全新磁盘包外目录时，先保存符号及原始/输出摘要，只对实际含`.debug_info`的ELF移除调试信息。没有变量只去重。符号是独立包外成本，不把“挪出app”全算成主机净收益；正式发布需保留符号并绑定来源。本次探测原始程序仍有完整符号，验证后回收自身临时符号副本。
- `python-artifact.py`原提取器拒绝tar硬链接，直接去重会让下一阶段失败；现已一并补齐。继续读schema1普通历史包，硬链接须指向同包直接普通成员且摘要/模式一致；拒绝逃逸、悬空、链接链、软链接目标及目录穿越。先解普通文件，再建立内部硬链接，最后清单校验。新包须使用新提取器。
- `runtime_backup_scope.py`/既有helper：未知文件默认保留，仅排除schema已核实的Codex诊断logs库及其WAL/SHM、精确布局下的isolated/execution启动探测临时目录。**requests、conversations、private-runs包含恢复事实，不能整体删或排除。**其余HOME、身份、授权、会话/队列SQLite、ACK、幂等、用户成果及未知临时目录均保留。
- 证据依据：生产`isolated-engine-profile.mjs`的`_prepareEphemeralState`每次mkdtemp；同文件`_prepareRequestState`与`typed-inspection-profile.mjs`的恢复路径使用持久会话/请求。实际只读检查logs表/列，未读取日志行或凭据。新增列/表或不可读即保留，未将所有SQLite推断成可丢弃。
- 备份由明确成员列表生成，禁止tar递归重新纳入排除项；保留ACL/xattr/模式/链接/稀疏文件，tar compare与前后选择快照一致才写该批receipt。保留原tar/tar.gz容器，空间收益只归于少备份成员，不重压缩历史载荷。receipt保留选择摘要/数量、排除依据、归档摘要及发布绑定，不重复保存数万条stat元数据。

## 实测与验证（不是发布）

证据根：`docs/implementation/evidence/runtime-footprint-20261109/`。

1. `real-python-result.json`：从现行生产Python**隔离复制**，别名去重＋调试符号分离，完整Python目录364,728,320→143,831,040字节；Python标准模块、ssl/sqlite/ctypes及docx/openpyxl/pptx/pypdf/reportlab/lxml/Pillow导入，真实生成/读取PDF、图片均通过。该早期实测所用函数后续只补目录保护/正常安装暂存兼容，最终源码另外通过真实freeze→移动目录→重新导入回归。
2. `sandbox-result.json`/`sandbox-rebuild.log`：补齐同版现行代码及Node/browser，以瘦身Python重新生成并校验整个sandbox image（1682文件、1613共享、69复制）。完整隔离程序877,481,984→656,613,376字节，即约837→626MiB，减少220,868,608字节（约211MiB、25%）。不是生产app实占变化，也不是有版本/commit的新正式发布包。
3. `python-artifact-result.json`/`python-probe-manifest.json`：真实pack→新目录extract→使用恢复Python导入通过，Python/libpython别名仍共享inode；包SHA`cd084bc3ea6a9285b516922edee789f37d79cd95a873c3f0d3e375b5b637f68e`。探测包/恢复树已回收，保留精确manifest及日志，不把探测包登记成正式发布制品。
4. `state-inventory.json`：原只读清单已收口为摘要、数量及逐项排除理由。排除131项，未压缩内容446,350,681字节（约426MiB）：诊断库及sidecar434,005,704字节，5个启动探测临时目录12,344,977字节。保留内容约1,039,525,308字节。活状态仍在变化，这只是该时点清单，不是事务一致快照；不承诺最终gzip包减少同等字节，不声称这些源数据已删除。
5. 最终`batch05-result.json`输入不变且全部通过：归档11项、冻结12项（常规入口1项需显式解释器而skip）、Runtime80项（既有64＋新scope16）。随后`real-freeze-tests.log`用真实解释器补跑全部12项无skip，最终合计**103项不同用例通过**。`final-probes.json`另含实际已安装scope/helper的16项隔离用例和只读plan-state。安装/读清单不冒充应用测试或部署。
6. 失败如实保留：batch01 socket fixture绝对路径超AF_UNIX长度，改为受控相对绑定；batch03新入口fixture漏paths.root_device/mountinfo，补全fixture不削弱校验；初次真Python瘦身对无debug_info的小shim执行strip会略变大，先识别debug_info后才strip，`real-python-failure01.json`保留。均改变已证实输入/实现后再试，不原样盲重试。

## 主机维护入口安装及实际线上边界

- 在host→Runtime release锁下保存旧helper、原子安装scope后再安装helper并readback；未改cron、服务环境、生产程序或状态。
- 最终08:24:37 +08安装：`runtime_backup_scope.py` SHA`b05d63e386f056e99ec71d0162f68c8fe5f6f7c9b8f1ae147f6cef7de9b59a98`；`runtime_backup_cleanup.py` SHA`07d80fa5a8d38066d347d89bb3b1bcb3c3e9a510373d750c505e81649f9f988b`。均与最终batch05相同。证据`helper-installation.json`；先前中间安装如实保留`.previous`，原8923helper为`installed-helper.before.py`，可在相同锁下恢复它，scope新文件可留存但不会被旧helper调用。
- 前后生产current record SHA始终`be58c79a93f4268fdca427430fac3107e801e9ad1ad236f3c3ab8cc70b36a669`，MainPID3607269、NRestarts0、active。这是无重启观测，不冒充新程序健康/业务验收。
- 显式`plan-state`可用；`backup-state --batch <NEW_BATCH>`可用但本次**未对生产执行**，要求Owner已停单元、无cgroup/状态占用，工具不主动停服务、不覆盖当前pin或既有备份。现行自动/历史一次性安装器仍未切换精简范围；历史prepared与安装器SHA未改写。
- 已回收本任务约937MiB私有探测程序、恢复树、包和临时符号，保留包外manifest/日志/摘要；这只是回收自身探测成本，**本轮没有实际线上程序/真实备份节省额**。不把原保留流程退休的旧备份或磁盘波动归功于本实现。无正式最终应用包需mark-complete，无新worktree，无他人缓存/进程/目录清理。

## 下一实际发布接续（仍未完成）

1. 以真实当前Runtime集成分支/源码固定新版本，应用本任务patch并按实际源码集成；旧本地develop不能用于覆盖当前生产。程序变化必须正确升版、记录原始工具链与转换前后SHA、包外符号和新manifest，不把本轮诊断树冒充1.3.68的新同版本制品。
2. 既有本地发布Owner准备工具链时，先复用freeze/slim及新归档适配器，显式设置包外符号目录，再生成sandbox与最终manifest。复用旧工具链不会自动调用freeze，需要在该既有准备位置接入，而不是对已生成sandbox或运行目录原地改写。
3. 在既有停止写入、归档原程序/切换之前，直接复用已安装`runtime_backup_scope.write_state_archive(...)`替换全目录tar，并传入真实发布绑定。已持release锁的安装事务不能再次运行独立backup-state抢自身锁。保留原程序原子rename恢复、兼容判断及身份/锁/健康验收。
4. 只有正式安装/新进程通道及必要业务验证完成，才能报告真实节省和现行备份切换。本轮源码/维护入口完成不等于以上应用发布完成；不修改历史prepared来伪造自动接线，不请求为这些备份/安装操作延长600秒构建预算。

## 耗时收口

`timing.json`汇总全部已记录测试/打包/探测（含失败和多轮回归）103.244秒。首次失败真工具链探测未输出精确耗时，以脚本创建至失败目录退休的68.876秒作为保守上界（含诊断/实现等待，不冒充实际执行耗时）；合计保守受限阶段172.120秒，小于600秒，未按阶段/重试重置。完整交付墙钟1169.535秒另记，包含实现、只读盘点、维护工具安装、文档和清理，不把它误算为应用deadline或单次受限构建耗时。最终源码/测试/文档摘要及实际未发布状态见`closeout.json`。


## 第二阶段：实际接入、安装与验收（2026-11-09）

### 固定源码及策略取舍

- 基于重新核实的生产1.3.68/92df9eb8，在唯一隔离worktree创建`codex/runtime-footprint-20261109`并固定1.3.69/fb9aafbd、tree9cd28d7。只含两份Python适配器、两份对应测试及Runtime版本；bridge执行代码、依赖锁、Python/browser功能包不变。原工作区有无关脏修改，本地develop仍旧，均未checkout/覆盖；无远端最新或develop合入声明。完成后已移除本任务干净worktree，保留commit/branch及发布patch。
- 现有材料认证绑定toolchain完整摘要。显式strip会改变认证输入，不能重标历史认证；因此本次采用默认去重，不设`CYF_PYTHON_DEBUG_OUTPUT`。Python别名节省158,490,624字节，程序含新增源码后的净减少158,437,376字节（151.10MiB/18.06%）。sandbox manifest与基线相同，最终路径两组别名共享inode，逐文件字节与归档的1.3.68一致。可选符号分离仍只是受测能力，未对线上启用。

### 同批证据与受控事务

- 批次`runtime-footprint-20261109-runtime`，正式包`/home/isp/state/cyf-local-build/tasks/runtime-footprint-20261109/release/package/runtime.tgz`，SHA`3912934a5d34a5065a90d05c8a9511436b0919794d624d6af0190026e30274d9`。保留原1.3.68包的逐文件完整性、未变调用方测试证据链及真实历史失败，不把旧测试改标新源码全量测试。
- 新前瞻安装器复用native-readiness已验证事务，复制到本批install而非改写历史prepared。安装前验证当前record/manifest、干净候选/来源/包/依赖摘要、真实host能力及启动声明；host-cleanup→Runtime release锁贯穿prepare/apply；锁忙不抢占。保留原在途任务检查、精确停止单元/cgroup、writer对象归属、状态全局进程占用检查、原子rename、pre-start仅程序恢复和后启动不回放旧状态边界。
- 已停止写入处直接调用已安装scope函数并带同批build/commit/tree/artifact及前代record摘要；不再子进程抢自身锁。选择清单前后相等、归档compare及SHA通过才切换。旧脚本额外compare仍真实执行并留日志；今后调用scope函数时无需重复实现其内部compare职责，不能为减少重复去改写本批prepared。
- 本批备份`/home/isp/baks/cyf-agent-runtime-v1/20261109-runtime-footprint-local/`：原1.3.68完整old-program及必要状态快照。state.tar.gz **581,168,665字节（554.25MiB）**，SHA`f9d31d225b7332e654bc7f999ad18f7ebf36c12c7db6eec1d4f4af5beb3004d9`；scope receipt原位置绑定143项排除、保留内容1,037,671,727字节。停服期间额外统计排除434,201,928字节诊断库及12,344,977字节启动探测。426MiB是少纳入的原始内容，不是压缩包差值或源磁盘已回收量；保留原gzip1容器不以压缩作优化主线。
- 服务约08:43:12停止、08:46:13重新active，MainPID3821968、NRestarts0；current于08:48真实验收后变verified-active。原配置/身份critical摘要相同；linchong/wuyong材料各10种输入保留原认证；lujunyi在实际最终路径真实文档/浏览器/PDF/脚本声明passed；3/3通道connected/registered/ready，随后heartbeat ACK亦已确认。没有付费模型turn、Web/API发布或业务数据库操作。
- 定向109项（Python12、归档11、Runtime维护80、本批安装接线6）全部通过；另有3项真实host能力probe及原生启动/材料读回。受限测试/构建/打包累计**354.311秒**，包括第一阶段172.120秒保守上界及本阶段完整候选准备，不重置重试预算；安装/备份/启动/验收独立且未下传应用deadline。接续setup至收尾墙钟约793.57秒另记。

### 收尾与没有做的事

- 证据副本`docs/implementation/evidence/runtime-footprint-20261109/release/`含实际安装器/prepared、测试/包证据、源码patch、scope及最终验收。原历史记录未改写。已删除本任务37MiB解包输入及26MiB隔离worktree；当前绑定的13MiB正式包保留，未声明为可回收、未增加嵌套路径清理例外。
- 原保留策略仍保留最近两批与current pin。本次plan在验收持锁时首先busy无操作，释放锁后再次plan没有eligible批次，故未执行额外删除。新old-program继承原基线runtime目录0775，现有安全清理器将其标为unsafe并保留；不能以此绕过权限保护、修改原manifest或宣称以后必能自动回收，该兼容点仍须单独对账。未知/缺证据历史目录未清理。
- 实际两项优化已在本版安装完成，但不代表其他一次性历史安装器或所有未来发布自动接线；下一Runtime Owner应复用本批前瞻适配的调用点，不复制早期整目录状态tar。未来可选strip仍须重新核验材料认证输入，不能冒用本次“字节未变”的验收。
