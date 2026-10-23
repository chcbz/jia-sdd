# JYT-SKILL-BASE-RT-5H-20261013

Owner/profile skill_se2_runtime5h；本轮唯一Runtime源码Writer，不接Reviewer。
已读：CYF AGENTS.md、ops/orchestration/README.md、design-se2.md及Runtime AGENTS.md。项目新规则覆盖共享旧双Flow/自动部署。
唯一源码worktree /home/isp/wsps/worktrees/skill-execution-20261013/runtime；branch codex/skill-execution-se2-20261013。
base b79558e4f18b431c1ff698432b3d6a7c07aac8d5 / tree b1b1b172be58c1d48667eb380619084a6cd68028。2026-10-13 21:19+08:00只读查询HEAD/tree/worktree clean、远端develop相同。线上版本未核验。
开发窗口2026-10-13 21:14:52至2026-10-14 02:14:52+08:00，不是请求/模型deadline。
写集：Runtime仓conf/codex-ws-agent及Runtime-v1精确route/catalog/受影响tests；本专属handoff。不写API/Web/主Runtime仓/全局skills/生产配置。
目标I13/I22/I23/I24/I26/I36/I56。非目标PDF/XLSX/video新增包、付费Provider实跑、服务重启、push/merge/deploy、费用审批/扣费。
验证复用Node20.20.2+Ajv8.17.1；先最小定向，再受影响回归。不是正式安装/上线证据。
21:28父Owner恢复时已回报归属和当前未提交进展；请求补充lease/resume/effect/result-commit及inputRefs/outputs精确结构。按冻结合同先实现独立路径不空等。

## 切片证据
- 8a110cbf033833e765fb4feedb708a91ea64ac6a / tree 8c1e9122df9a256e090c96a54cb4ae3fbf825296：action-v4、Ajv参数、通用executor、registry；30/30。
- ac16808d093d3a4279218a19bd8c36d7da9664cc / tree 14abc61186d779e51c2d9500c33b58be7f3c35c2：fsync effect/result store；仅NEW发副作用、未知不重发；36/36。
- 79f471a34b3ea8325707603b042731082c37c02c / tree 6f259f32b0fb8a62f6e404943c15b67ea3363cd0：共享bindings、旧HTTP codec提取、native/image runner、materials载体；26/26（全部Provider mock）。
- 1ca9cfc0fba2b2ed25897b9f49e38ca14f619621 / tree 1160bb7e968d4e5bd1c3e5e4a686269ae8f2633c：同poll protocol4、lease/session/stage/commit、exact HTTP白名单；组合212/212。
- 11b51eb9d0f821a15c89176c6293f45bab9ed8ce / tree 46ae4d16ddf4969f3ad992dc48e955f6b32186c1：父精确inputs/result wire；fence{version,token}、sourceKind/sourceIdentity、安全Java byteLength；result第五字段inputReceipts；canonical digest={schemaVersion:1,data,artifacts[{outputId,sha256,byteLength:number}],inputReceipts}；data支持标量/数组/null；严格effect/result ACK；持久command同poll恢复（服务端QUEUED inbox不需重发运行中的command）；已提交server envelope恢复不需本机输出字节/runner；实际native finishReason接线；共享配置候选/原full-subject凭据源。308/308，54.24s。

日志目录：/home/isp/wsps/worktrees/skill-execution-20261013/runtime/conf/codex-ws-agent/evidence/skill-execution-base-5h-20261013/。slice1/2/3/4.log及wire-and-config.log是上述定向成功；affected-all-initial.log记录首次完整engine回归927项、885通过/32失败/10跳过（旧v3 fixture与旧registration assertions，尚未全部修复）。wire-r1.log与wire-r2.log保留首次wire自检失败及实质修正过程，不将失败日志当成功。
22:12父明确扩result第五字段inputReceipts并允许Object data，Runtime已按唯一合同实现，不留四字段兼容。
待对齐：公共CHAT contextSnapshot.facts.materials冻结格式/受权下载exact路径、host回执上报；已向父提供具体字段/路径建议。当前不声称原生CHAT资料端到端闭环。
当前全部验证为固定Runtime源码本机诊断/受影响回归，未正式安装、未运行真实付费Provider、未生产切换或服务重启；父Owner统一集成验证。下一片修正受影响旧fixture/registration，并接入冻结公共CHAT materials。

## 切片6 / 公共合同接续
- 6ce55cef65f22b77c112ddfe6ccf29d3962eb706 / tree dd1ac6f45bc7968702aa0279024467c9b98104e2：registration/presence仅真实测量skillExecution/inputCarriers；native planning仅action-v4；media MIME必须对应真实测量carrier否则UNAVAILABLE；receipt持久后才释放隔离adapter；受影响293/293，66.10s。日志retirement-final.log。全套未重跑。
- 2026-10-13 22:48接续已读Dirac22:15冻结CHAT合同：facts.materialsInput，GET exact materials/inputs/{sourceRefId}/content，X-Materials-Manifest-Digest，原CHAT final复用inspectionInputReceipt；无需新增回合，先前待确认已解除。正在接线/自检，不声称完成。
- 四包candidate准备于Runtime toolchain/skill-packages-se2/release-inputs.json；真实ZIP及manifest SHA、size同目录索引。已有安装器真实解压/marker/replay/readiness源诊断104/104；native两包含text+PNG+WAV材料，因此缺任何声明media carrier明确UNAVAILABLE，测量缺失不会假READY。未市场发布/生产安装/付费Provider实跑。

## 23:44接续 / 当前候选（覆盖早期待确认与失败状态）
- f85862ce589f45252030d0a238f8e1048daacedd：四包真实ZIP/marker/安装104/104；未发行。
- f1936ee5816ee78ce9f21827ac43ffb3f981e5e4：递归拼接canonical JSON，UTF16 lexical对象键与portable JSON.stringify数字；40/40。
- e9e500d597d6c7e97d4f3648f8714f2e4a039ce8 / tree 3a38746acccddc26fe16f2ceda700e29ea73d0ca：原CHAT materials接入，32真实混合字节/host receipt/真实thread+turn/持久terminal恢复/ACK后cleanup，INSPECT新路由明确退休，payload catalog同步。最后定向57/57；受影响296/296；完整engine 951项=941 PASS/0 FAIL/10 SKIP，174.44s，engine-all-r2.log。早期32fail已修复/按退休新流量契约迁移，不改历史fixture。
- 9fe5a1fb7a481a3fec131cdf8df3769f28111504 / tree b5786d24982d0053e22377ad2f102af7ecfacac3：UNKNOWN单项不阻塞非重叠poll项（原error/cause保留，session/shared-store错误立即停止）；native两包新1.0.1只声明text/Markdown/JSON/PNG，未测WAV不再阻断实际图片分析；原1.0.0 ZIP保留不可变；Runtime源码1.1.0 candidate。
- 新切片：安装104/104（packages-text-image.log，13.21s）；poll/materials/runner28/28（poll-materials-r2.log，2.68s）；Runtime-v1/hosting/storage183项=182 PASS/0 FAIL/1 SKIP（runtime-hosting-r1.log，86.64s）。poll-materials.log保留首次test注入错误，修正runner闭包来源后PASS；不是实际Provider失败。
- 最新发行索引绝对路径：/home/isp/wsps/worktrees/skill-execution-20261013/runtime/conf/codex-ws-agent/toolchain/skill-packages-se2/release-inputs.json。image两包1.0.0不变；analysis1.0.1 ZIP SHA b2f283c3019b0ff2b632188ea64e6af98d2d61c753e2c0925d9f78132436b864；text-file1.0.1 ZIP SHA 16da21a3af2066100217488774e59cbe4238e3769b4f9f61f07b1916191dc915；manifest SHA/size见索引。
- 配置转换准确入口：conf/codex-ws-agent/skill-config-candidate.mjs:createSkillConfigurationCandidate(profiles, absoluteBindingsFile)。纯候选/diff/digest/readback，不写配置/凭据，不重启；共享schema只一个skill-bindings.json，凭据保留full-subject providers.json。
- 父37a96cab47已补CHAT materials exact route；父五字段result/inputReceipts/公共CHAT冻结合同已接入，早期待确认解除。当前无待父materials接口。
- 父要求补I27真实local-script runner：当前尚未实现；正补最小Node脚本/无shell/清空env/只读输入/真实bwrap隔离。现receipt允许集没有原始脚本文件载体，已请求父新增local-file，不假报native/parsed。
- 父b603c83520费用展示合同：costInfoOverrides键skillKey@skillVersion[#bindingId]，值含informationRevision正数字符串；Runtime不消费价格、不纳入binding摘要/cache/授权/副作用。
- 全部仍为源码隔离诊断，未生产安装/部署、未付费Provider实跑、未重启共享Runtime；父负责正式集成/市场发布/合法购买安装。

## 2026-10-14 00:25接续 / 最终源码冻结（覆盖上节I27待实现）

- 已续读CYF AGENTS、Runtime AGENTS、orchestration README、design-se2 §8–10；共享技能旧Flow/自动部署规则不适用。固定base与原写集不变，不接Reviewer，不派新Writer。
- `9cefc9c0864d241cf263b64bff5c4d768e373363`：真实注册local-script Node runner，实际bwrap运行，argv无shell、env无凭据、cap-drop ALL、输入/包只读、宿主HOME不可见、网络与PID隔离；真实UTF8产物及effect durable恢复。只支持受审Node .js/.mjs，其余缺工具/隔离明确UNAVAILABLE，不是Python/Shell占位实现。local-script-affected.log 52/52，local-script-caps.log 7/7且0skip。
- `ff6d645380c8c3ab0fb22aa379adf42bcb91f815` / tree `8e7add1e1963ad5cbb78eece8c59590a9fc6eeed`：local-file仅允许local-script，persist与committed恢复复验runner；Runtime1.1.0/payload旧测试同步；local-file-closure.log 39/39，closure-affected.log 134/134。
- 旧clean ff6d645完整验证：Engine 967项=957 PASS/0 FAIL/10 SKIP，121.55s；Runtime-v1/hosting/storage183项=182 PASS/0 FAIL/1 SKIP，45.55s。两日志原为未跟踪，父要求API fixture clean；00:20按原字节移到repo外，不删证据：
  - `/var/tmp/cyf-skill-base-runtime-evidence-20261014/engine-all-final.log` SHA256 `c8eb652a36b683a023781d9ab5cb7fa9e340eb2d76f6d388c318aded14087cf3`
  - `/var/tmp/cyf-skill-base-runtime-evidence-20261014/runtime-hosting-final.log` SHA256 `aaa40f3c6df4a34a609437fe9ba1bb81ca7c4b672ec27186070e09e4df1d544c`
- 最终审计发现原安装marker只校验ZIP/manifest不能发现local-script依赖文件替换。已通知父不将ff6d645作为最终发行源码；这是既有I27安装完整性闭包，不扩产品功能/HTTP/资料授权。
- **最终源码候选 `d113875bfb05d72014c0675c5439633f5fa97ef2` / tree `81b0ba68fc4351e877337ce3437d6d54b2310189`，00:23核验worktree clean。** 新私有registry+marker记录ZIP验证后script完整树摘要，可信descriptor/probe/run/launch前复验。脚本或依赖变化、硬链接/符号链接/非安全权限拒绝；同时伪造marker不能改私有registry的expected摘要。普通说明包及四首发包行为不变，不在安装HTTP wire新增字段。
- 新切片定向 `node --test` installer/local-script/manifest/registry：189项=189 PASS/0 FAIL/0 SKIP，26.10s；日志 `/var/tmp/cyf-skill-base-runtime-evidence-20261014/script-install-integrity-r1.log` SHA256 `7a8ee174352b9461f0a64774834b953d09940f27f3de642333c526c2ebf17732`。真实bwrap测试未skip；probe后换依赖证明不登记effect、不启动package进程。
- 该最终提交变更路径：
  - `/home/isp/wsps/worktrees/skill-execution-20261013/runtime/conf/codex-ws-agent/skill-install-manager.mjs`
  - `/home/isp/wsps/worktrees/skill-execution-20261013/runtime/conf/codex-ws-agent/skill-manifest.mjs`
  - `/home/isp/wsps/worktrees/skill-execution-20261013/runtime/conf/codex-ws-agent/skill-registry.mjs`
  - `/home/isp/wsps/worktrees/skill-execution-20261013/runtime/conf/codex-ws-agent/skill-runners/local-script.mjs`
  - `/home/isp/wsps/worktrees/skill-execution-20261013/runtime/conf/codex-ws-agent/test/skill-install-manager.test.mjs`
  - `/home/isp/wsps/worktrees/skill-execution-20261013/runtime/conf/codex-ws-agent/test/skill-local-script.test.mjs`
  - `/home/isp/wsps/worktrees/skill-execution-20261013/runtime/conf/codex-ws-agent/test/skill-manifest.test.mjs`
- 00:24静态发行核对 `/var/tmp/cyf-skill-base-runtime-evidence-20261014/release-catalog-audit.json`：Runtime1.1.0、61 execution payload文件、相对依赖缺失0、四包ZIP/manifest摘要与索引一致。仅静态制品输入核对，不是实际clean-target安装。
- 最终源码已冻结，完整engine+hosting正在运行，日志输出repo外，不在运行期间修改源码。下一段追加实际结果；不把旧ff6d645结果冒充d113875验证。
- 父API fixed `2ba47f3d694fc0450c3e65badaaf56bf70a1d7fa` / tree `154b438027d58db0f6f51dfefc09e2a021d2ee51` 是父提供信息，非本Writer正式验证。当前无未接线HTTP阻塞；五字段result/data任意JSON/inputReceipts含local-file已唯一对齐。local-file只传local-script原始只读字节，不加入CHAT载体、不冒称解析理解。
- Runtime不消费价格展示；costInfoOverrides缺失/无效不影响bindings readiness/digest/cache。原CHAT materials合同与身份/ACL不变。
- 四包输入仍在 `/home/isp/wsps/worktrees/skill-execution-20261013/runtime/conf/codex-ws-agent/toolchain/skill-packages-se2/release-inputs.json`：image-generate/edit1.0.0、analysis/text-file1.0.1。native只text/plain、text/markdown、application/json、image/png，未测WAV不声明。I54维护方还须批准产品版本/不可变对象提升/市场登记/current pointers/合法购买安装；Runtime没有发布该四包。
- 配置纯候选入口 `/home/isp/wsps/worktrees/skill-execution-20261013/runtime/conf/codex-ws-agent/skill-config-candidate.mjs`：`createSkillConfigurationCandidate(profiles, absoluteBindingsFile)`；不改凭据/生效配置/服务。
- `/var/tmp/cyf-skill-base-api-release-20261014-r1-preparer/prepare-release-inputs-main.py`不是本Writer任务/写集，未派子Agent、未修改该文件，不知其他Agent归属/预计完成点，已即时告知父。
- 全部仍是隔离源码诊断：没有生产安装/正式Runtime制品、付费Provider实跑、共享Runtime/服务重启、生产配置写入或push/merge/deploy。交付父统一集成及正式制品验证；不再增加功能。

## 2026-10-14 00:28最终交付 / 可合入候选

最终源码仍为 `d113875bfb05d72014c0675c5439633f5fa97ef2` / tree `81b0ba68fc4351e877337ce3437d6d54b2310189`，完整验证前后工作区clean，验证期间无源码变更，无后续证据源码提交。父可按原固定base取本Writer完整提交链至此候选；尚未push/merge或正式Runtime制品构建/发布。

最终clean候选实测：
- Engine：972项，962 PASS、0 FAIL、10 SKIP、0 cancelled；137.49s。
- Runtime-v1/hosting/storage：183项，182 PASS、0 FAIL、1 SKIP、0 cancelled；97.72s。
- 安装完整性/真实local-script/manifest/registry定向：189/189 PASS，0 SKIP；26.10s。新增local-script bwrap/进程隔离/只读真实字节/本地effect恢复/安装篡改测试全部运行，未skip。
- Engine skip：9项退役CLI/v3 opt-in测试、1项实际native app-server隔离握手opt-in测试；hosting skip：1项历史M3真实跨端HTTP/ACK/restart验收NOT_RUN。这些skip不算正式闭环成功，不冒称真实模型理解或付费Provider验证。

精确源码/selector/原始日志/日志SHA/数量/时长闭包：
`/var/tmp/cyf-skill-base-runtime-evidence-20261014/source-validation-result.json`

日志：
- `/var/tmp/cyf-skill-base-runtime-evidence-20261014/engine-all-integrity-final.log` SHA256 `74a5d8638e1b4c82bb0e20fc2fa19903f41bd36597d30be4c80eade23c5788a5`
- `/var/tmp/cyf-skill-base-runtime-evidence-20261014/runtime-hosting-integrity-final.log` SHA256 `a2056fd773ac8fbe5bc1a8a56f98558d1d82e14db9a8cf5e8e7e1042c64dfd19`
- `/var/tmp/cyf-skill-base-runtime-evidence-20261014/script-install-integrity-r1.log` SHA256 `7a8ee174352b9461f0a64774834b953d09940f27f3de642333c526c2ebf17732`
- `/var/tmp/cyf-skill-base-runtime-evidence-20261014/release-catalog-audit.json` SHA256 `ca545cb9eb8c4f4c20bf5c3fbf9eab71b335db4792ea5b244c3dea7905570412`

Runtime1.1.0源码、61文件payload catalog与四包不可变发行输入均准备完成，无新的接口待父接线。安装完整性/身份/ACL/fence/lease/NEW唯一发起/UNKNOWN不重发/结果先持久后stage/commit/读回不重跑均保留。下一步仅父统一集成正式验证、同批Runtime制品准备、I54维护发布与合法安装；本Writer冻结源码，不再增加功能，不操作共享Runtime/生产配置/其他Writer进程。

## 2026-10-14 00:42父授权正式制品准备 / 只读配置候选

父明确追加仅准备Runtime1.1.0正式制品、clean-target安装validate和配置旁路候选，不改源码/生产unit/HOME/config、不重启。已先读Runtime-v1 README、self-host §2、现存install.sh/validate.sh及旧clean-target说明；旧harness SOURCE5666fd/46catalog不能冒充当前61payload，未更改或运行其旧源固定验收入口。

- 独占制品批次根：`/var/tmp/cyf-skill-base-runtime-release-20261014-d113875-r1`，0700。
- 从clean固定d113875生成完整git archive，无prefix，提取到该根/source；378个Git blob及executable mode全匹配原tree。来源绑定在`source-archive-binding.json`，完整source-validation原字节副本在`source-validation-result.json`。
- 复用原installer从归档源码执行，隔离新HOME/cache/tmp/config，env -i不继承生产环境，Node20.20.2/npm现存CLI/Python3.11.13，npm ci固定lock/no scripts，原私有venv安装策略不变。exact argv在`installer-argv.txt`；日志`installer-r1.log`/exit文件。当前下载Python依赖，正式target尚未发布/验证，不能报告正式制品PASS。
- 不复制旧运行artifact/HOME/global依赖、不修改生产服务；PyPI/npm仅包下载，无Provider请求。
- 共享磁盘00:39实测余815MiB；仅保留一份完整Runtime目录制品，后续摘要按既有catalog/checksums记录，不额外打另一份全量artifact archive、不清他人目录。
- 四包原字节旁路目录该根/skill-packages-se2，索引和4 ZIP/4 manifest/4 SKILL.md全部匹配固定源码；installer完成后作为artifact同批顶层sidecar纳入制品catalog，不更改61个engine payload声明，也不市场登记/购买安装。

配置候选已完成：
- `.../candidates/skill-bindings.json`，目的地`/home/isp/conf/cyf-agent-runtime-v1/skill-bindings.json`（目前不存在，前值记录null）。
- `.../candidates/profiles/{linchong,lujunyi,wuyong}.json`，各自保留原迁移后的HOME/workdir，引用唯一生产shared binding绝对路径。
- `.../candidates/configuration-diff.json`与`private-readback.json`：原三个profile/host/providers SHA readback不变；实际三个full-subject中现存一个Provider凭据主体/一个image binding，未给其他角色伪造Provider能力。只有凭据key名称映射，无secret复制/打印；三profile保留原模型/身份/授权/工作根。
- `.../candidates/validate.host.json`及validate-profiles仅用于本批artifact validate，bindings引用repo外候选，而非尚未切换的生产路径；不是应安装的profiles。
- 候选目录0700/文件0600；没有账号费用信息，四包costInfo UNKNOWN/共享costInfoOverrides空，不费控、不变更有效binding摘要。所有生效生产文件仅只读，父负责保存前值、协调切换。

## 2026-10-14 01:01正式Runtime1.1.0制品与配置候选交付（未生产安装）

固定源码仍`d113875bfb05d72014c0675c5439633f5fa97ef2` / tree`81b0ba68fc4351e877337ce3437d6d54b2310189`，源码worktree clean，无新源码提交。父00:31追加授权的仅制品准备/clean-target安装validate/只读配置候选已完成。

正式目录制品（单份，不额外复制打包共享磁盘）：
- `/var/tmp/cyf-skill-base-runtime-release-20261014-d113875-r1/artifact`，root:root0700。
- 3606 regular files，193699606 file bytes / 202129408 allocated file bytes。
- 完整内容/模式/owner/link inventory digest `7d854f8aa7ef13699c6cf59aa322c47c8618446b8a97cc5a2783760db2dd11e3`；精确算法见catalog，不是tar文件SHA。
- catalog `/var/tmp/cyf-skill-base-runtime-release-20261014-d113875-r1/artifact-catalog.json` SHA256 `f2e6e66ba3cde5d1b5547f127bb1c2525c8d3ca924aa1f8a01cb3ca744e1440f`。
- regular file检查表 `/var/tmp/cyf-skill-base-runtime-release-20261014-d113875-r1/artifact-files.sha256` SHA256 `0245f6f1e353604038355fe272aa15f1f432a3251594503643e58afcc08b5094`；不能用regular check表代替mode/owner/symlink检查。
- 汇总 `/var/tmp/cyf-skill-base-runtime-release-20261014-d113875-r1/artifact-summary.json`，准确实际installer argv在同批`installer-argv.txt`；已从归档完整fixed源码执行原唯一install.sh，目标须新建，不要重复对existing target运行installer。
- source-validation原字节SHA `fb93df600695d767fe80e7549aaef3c1735911c40e93ae12c33a1c5be023a228`，已装入`artifact/release/source-validation-result.json`。仍绑定Engine972/962PASS/10SKIP、hosting183/182PASS/1SKIP及189/189切片，不冒充新的线上业务验收。
- 同批四包在`artifact/skill-packages-se2/release-inputs.json`，4 ZIP/4 manifest/4 SKILL.md精确原字节，native两包1.0.1/image两包1.0.0，无旧native1.0.0发行指针；61engine payload保持原catalog闭包，四包是顶层sidecar，非强制预安装entitlement。

真实clean-target安装与validate状态：
- npm ci从原fixed lock安装8个包、无install scripts，独立cache/home，无global packages借用。
- 原Python3.11.13私有venv、pip21.3.1、六个直接pin及真实实际transitive distributions均安装/import通过。Pin/版本/所有内容SHA记录在catalog，未将六个direct pins称作全transitive lock。
- 原installer stage validate PASS + target validate PASS（首次真实安装exit0）。完整sidecar装入后的artifact validate PASS。原artifact-local agent-runtime validate在三主体候选投影下PASS（agentCount3），原providers full-subject只读，无enroll/run/真实模型或Provider请求。
- task-only同文件系统rename后原validate/private Python imports/pip相对launcher PASS；完整inventory内容/权限/owner/link不变；原路径/dev/ino已恢复。`relocation-readback.json`及`artifact-relocated-validate.log`是实际证据。
- 辅助readback oracle r1以JSON字符串比较不同键序，在rename前失败；r2路径归一化短prefix先替换导致假差异，实际artifact已finally恢复。均保留`relocation-r1-oracle-failure.json`、`relocation-r2.log`与`relocation-r2-oracle-failure.json`，分别实质修复结构比较和长路径先替换，离线归因确认后实际r3 PASS；不删除失败、不算作原installer失败、不盲重试同根因同输入。
- same-host artifact依赖既有Pythonbase/stdlib `/home/isp/wsps/cyf/.codex-runtime/gpt-image-cli/python/cpython-3.11.13-linux-x86_64-gnu`，非self-contained Python/跨机器可移植证明。使用artifact-local interpreter，不source activate、不改 immutable cfg/metadata。Codex/bwrap外部工具仍需在真实protected安装路径测就绪，准备目录`/var/tmp`不冒称实际执行READY。

只读配置旁路完整candidate：
- `/var/tmp/cyf-skill-base-runtime-release-20261014-d113875-r1/candidates/skill-bindings.json` → `/home/isp/conf/cyf-agent-runtime-v1/skill-bindings.json`（前值不存在已记录）。
- `/var/tmp/cyf-skill-base-runtime-release-20261014-d113875-r1/candidates/profiles/linchong.json`
- `/var/tmp/cyf-skill-base-runtime-release-20261014-d113875-r1/candidates/profiles/lujunyi.json`
- `/var/tmp/cyf-skill-base-runtime-release-20261014-d113875-r1/candidates/profiles/wuyong.json`
- 每个profile候选目的地与before/candidate SHA在`candidates/private-readback.json`，候选引用单个最终生产bindings绝对路径。三profile的原迁移HOME/workdir/model/身份保留。实际仅一个image binding/一个image credential full-subject，其他两个不补造凭据或ProviderREADY。
- secret仅原providers文件只读/内存核验，未复制/输出。候选目录0700/文件0600。四包费用UNKNOWN、costInfoOverrides无新增账号信息，不审批/扣费，不影响bindings有效摘要/就绪。
- `candidates/validate-profiles/`和`validate.host.json`仅为此次artifact验证改引用的投影，**不要当生产安装候选**。父负责备份真实前值/协调原window/按现有锁切换，providers文件原样保留。

最终交付闭包：
`/var/tmp/cyf-skill-base-runtime-release-20261014-d113875-r1/delivery-final.json` SHA256 `11d6fe9d1061155bc6640dc74f0acb9e42d305eae35ffbbe33c29ad113d5af12`。
原始完整日志/摘要文件闭包在同批`delivery-final.sha256`；Main操作边界与准备argv/readback提示在`MAIN-INSTALL-HANDOFF.md`。Main可在既有授权/锁/备份下same-filesystem移动目录制品后再最终路径validate，不需再次下载/构建依赖。

本Writer没有生产unit/HOME/config写入、服务启动/重启、真实Provider/模型调用、市场发布/合法购买安装、push/merge/deploy。正式Runtime制品准备与clean-target验证完成不等于生产切换/线上基础闭环通过，剩余由父统一API/Web/Runtime版本化发布和业务验证。
