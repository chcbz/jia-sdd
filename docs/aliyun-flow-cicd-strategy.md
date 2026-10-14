# CYF 构建、测试与部署策略：前端 Flow / 后端本地

更新：2026-10-08，按用户最新授权调整 **CYF 项目内** 的交付默认规则；不修改 Codex 全局、其他项目或共享技能。本节为当前规范；下方历史证据不恢复旧的双端 Flow、自动部署或本机前端发布路径。本次只更新规则与指南，未修改云端配置、构建、部署或重启服务。

## 当前交付路径

- **前端**：阿里云云效 Flow 正式测试、生产构建、制品生成与部署；复用 `4403172`。本机只做开发预览、控制面及轻量诊断，不运行生产 Vite 打包，不因 Flow 失败回退本机构建。
- **后端**：本地正式测试、构建、制品生成与部署；在固定完整 commit/tree 的干净源码目录或独立 worktree 执行，不在生产安装目录编译、不从脏工作区发布。所有 Gradle 操作先读最新相关 `build.gradle`，经 `python3 ops/orchestration/cyf_orchestrator.py gradle ...` 串行协调。
- **develop 不自动部署**：push/合入只用于集成与验证；不由旧定时任务发布最新 develop。后端不再默认启动 Flow 验证/发布，现存 webhook/流水线是否调整需另有配置 readback，规则写入不等于云端已改。
- **统一版本化部署**：确定版本 → 固定源码 commit/tree → 对应环境测试/构建 → 同批不可变制品 → 部署 → 在线核验。前端绑定真实同 Flow Run 制品，后端绑定真实同本地 build ID/日志与制品摘要。任一步失败记录真实失败，构建通过不等于已上线。
- 按具体版本安排发布时机，不要求每次重复构建或独立 Reviewer，不新增流水线或无依据门禁。本规则不授权立即发布、重启、迁移、生产数据写入或扣费，沿用任务已有授权与恢复要求。

## 固定入口与执行边界

| 入口 | 当前用途 |
| --- | --- |
| `4403172 / cyf-web-release` | 前端 Flow 验证及明确版本的发布；develop 不自动部署 |
| `ops/orchestration/cyf_orchestrator.py gradle ...` | 后端本地正式测试、构建与诊断的唯一 Gradle 入口 |
| `/home/isp/hosts/cyf/api/cyf-api-kit.jar` | 后端最终实体安装目标；构建与安装分离 |
| `5260799`、`5263690` | 既有后端 Flow 入口，非默认交付路径；保留历史与明确需要的云端诊断，不因本次规则调整删除或覆盖 |
| `5263692 / cyf-web-ci` | 前端按需 CI-only 诊断，不部署 |
| `5264702 / cyf-ops-manual` | 临时运维入口，默认只读；复用不增加操作授权 |

## 制品安装契约

- 前端继续使用真实 Flow Run、完整 commit、版本及同 Run 归档 SHA-256；现行 `/usr/local/sbin/cyf-web-flow-deploy PIPELINE RUN COMMIT VERSION ARTIFACT_SHA256` 不改为本地打包入口。制品 manifest 的 `package_version` 必须匹配发布版本，并核验来源、receipt 与文件完整性。
- 后端本地测试及构建绑定同一固定源码输入；记录 build ID、commit/tree、版本、命令/selector、fixture、工具链、依赖来源、测试摘要及日志。对唯一构建 JAR 与安装包（如使用）分别记录 SHA-256，部署只消费该批已核验字节，不在安装时重编译。
- 后端安装仍保留统一锁及锁顺序、互斥等待不抢占、可信 root 管理的 JAR/配置、`cyf-api` 运行身份、备份、原子替换、可恢复安装、必要的 schema 检查与实际健康/业务核验。数据迁移不因构建位置变更自动获准。
- **本地发布入口须适配与验收**：现行 `/usr/local/sbin/cyf-api-flow-deploy` 是真实 Flow Run 下载契约，不能以本地 build ID 冒充 Run。为本地制品提供版本/源码/摘要绑定的安装输入并验证恢复路径后，才能实际执行本地部署；这次规则修改不宣称适配已完成，也不恢复旧 pull/build/restart 脚本或旧 M1/M2 发布输入。
- 生产 JAR 与 cwd 固定 `/home/isp/hosts/cyf/api`；`/opt/cyf/service/api` 仅兼容链接。构建产物/日志留在源码或任务证据目录；既有 Flow 下载/状态留在 `/var/lib/cyf-api-flow`，备份留在 `/home/isp/baks`。

## 构建与验收证据

- 保留身份/ACL、幂等、事务、锁归属、依赖与制品完整性及相关回归；后端 `validateLayering`、相关定向测试和发布 JAR 构建在本地执行。真实数据库集成使用隔离 fixture，不触碰生产数据。
- 证据按 tree SHA、精确 selector 与 fixture 复用，接受有效命中时不重复执行。同根因同输入连续失败两次停止盲重试，经归因或实际修复后再验证。
- 发布记录包含版本、完整 commit/tree、前端 Flow Run 或后端本地 build ID/日志、测试及制品摘要、目标、部署顺序、恢复信息和在线核验。后端本地正式证据不再被默认排除，历史 Flow 成功仍只证明其原输入。
- Flow 写入先备份前值、固定候选并 readback；有活动 Run 等待，不覆盖、不取消他人任务。资源/包大小/等待时限不增加无证据阈值，详见 `docs/aliyun-flow-gate-policy.md`。
- Flow 模板及主机工具维护源仍位于 `ops/ci/aliyun-flow/`。目录名、配置保存、历史 status 或候选成功均不等于当前版本已部署。

## 后端本地构建缓存提速（2026-10-09）

正式本地后端构建通过既有 `cyf_orchestrator.py gradle` **默认**复用受控私有Gradle依赖缓存，并启用compile-only输出缓存：识别本地release opt-in与匹配的固定metadata init，无缓存参数即可选择 `/var/cache/cyf-gradle-local` 并加入 `--build-cache`；显式诊断/隔离参数可覆盖，Flow和普通诊断不变。仅在干净固定commit/tree及新输出目录执行。compile-only策略：仅JavaCompile按内容指纹复用，其余任务禁用输出缓存，测试禁止up-to-date；仍执行同批定向测试、`validateLayering`、依赖来源/SHA与fresh bootJar完整性检查，不缓存测试结果/生产JAR、不删除安全回归。home信任边界与参数冲突检查见 `ops/orchestration/README.md`。

2026-10-09授权收尾已按既有锁、备份与原子安装同步主机admission白名单（当前SHA `49ff62e470beadf5c5c570b007d1d30a6dd18b1f32df217274d89121ff77728b`）；cached/skipped测试、分层和bootJar仍拒绝。应用未发布/重启，历史helper catalog与authority/receipt不改写，后续发布生成新批次catalog。默认策略实现源码 `638777ed`，证据与恢复原值见原handoff。

10分钟是“测试/构建/安装核验执行时间”的优化目标，不是强制超时或减免安全门禁。历史安装约307秒来自日志文件起止，未包含排队与批次中间等待；本次没有授权/触发生产安装，因此新构建加历史安装仅用于评估，不冒充完整发布达标。固定输入、实测结果与证据见 `docs/implementation/handoffs/BACKEND-RELEASE-10M-20261009.md`。冷缓存和其它源码/selector不作无实测承诺。

## 历史控制面与适配器记录（截至 2026-10-06，非当前执行规范）

以下原记录保留不改写；其中双端 Flow 发布契约不作为后端本地发布输入，也不能证明新本地发布入口已验收。

2026-10-06 经用户授权完成控制面调整：前端单次 Update/readback 移除部署阶段；后端当前配置原已仅验证，未写入。两端 develop push 保留测试、构建与制品，不部署；两个旧 nightly timer 均 disabled/inactive，无下一触发时刻。本地 develop 模板同步移除部署阶段，7 项静态测试通过。实际证据见 `docs/aliyun-flow-versioned-deployment-switch-20261006.json`。

版本发布需先准备绑定明确版本、完整 commit 的固定发布候选配置，复用上述入口；发布完成后恢复 develop 仅验证配置。2026-10-06 已通过 `5264702 / Run13` 安装版本化部署适配器，移除午夜 intent 与旧分时版本限制；运维配置已恢复。36 项本地定向测试通过，Flow 安装器执行固定的 15 项回归后完成安装；日志接口未返回测试明细，依据固定测试摘要与安装回执核验。证据见 `docs/aliyun-flow-versioned-adapter-migration-20261006.json`。本次只更新部署工具，未发布、重启应用或执行数据库变更，不能视为应用版本端到端验收。

初次审计把后端历史 Run 的部署阶段误当作当前配置，已纠正；当前 YAML 才是自动部署配置证据。

## 版本发布适配器契约

- 前后端统一调用：`/usr/local/sbin/cyf-{api|web}-flow-deploy PIPELINE RUN COMMIT VERSION ARTIFACT_SHA256`。版本与完整 commit 必须固定；旧三参数调用不再有效，不创建 nightly intent。
- `ARTIFACT_SHA256` 是该 Run 完整下载归档的 SHA-256，不是单独 JAR、dist 文件或目录的摘要。仍须校验 Run、commit、manifest/receipt 与文件完整性；前端 `VERSION` 必须等于制品 manifest 的 `package_version`。
- 发布候选必须同步更新制品内嵌适配器及 helper 升级调用的接口和哈希，不能复用旧模板中冻结的三参数 helper。当前 develop 模板仅 CI，不因安装新适配器恢复部署。
- 后端记录版本/commit/Run/制品绑定，安装与既有 schema 检查成功后才标记 verified；前端保留互斥等待、分阶段发布与实际在线核验。

## 历史证据（非当前执行规范）

以下保留历史 Run、迁移与部署记录；其中 develop 自动发布、旧本机例外及定时安排已不作为当前发布依据。历史事实不能代替当前版本的 Run 与在线核验。

## 2026-09-12 CI-only 验收证据

### 后端 Run 1

- Pipeline：`5263690 / cyf-api-kit-develop-ci`
- 状态：`SUCCESS`
- commit：`a9d3e7417447a9f5f59a12523e582a8e8f1818f6`
- tree：`3352d0049871b588108eba0af990091a80fd965c`
- 门禁：定向测试、`validateLayering`、`:starter:bootJar`、OpenCV 私仓来源与摘要校验、`ArtifactUpload` 全部成功
- JAR SHA-256：`bbb6006e9abf611cea8168820d62558b2ebfef0d9d6f14a6987291edacb33fc9`
- 配置 canonical SHA-256：`0d63636ee01976630e0b51bf63fe9b82c4793967a0049ad12ab1c68d783f646b`

### 前端 Run 7

- Pipeline：`5263692 / cyf-web-kit-develop-ci`
- 状态：`SUCCESS`
- commit：`c9cbdccb7ceaa1cecab59bb4f2d6cd441042b2c3`
- tree：`2f82fca468197608cdaa7061d58d11785c6ca7ef`
- 运行时：Node `20.20.2`；Chrome for Testing `133.0.6943.141`；固定 WebP `1.2.0` 来源、ABI 与 SHA 校验成功
- E14：五项 gate 全通过；固定 10 秒 warmup、60 秒 sample，total p95 `0.8000000119 ms`、p99 `0.9000000060 ms`
- Mocha：`2118` tests，`2116` passing，`2` pending，`0` failures；mochawesome HTML/JSON 已上传
- Vite：`6.4.3` production build 成功，`8.84s`
- 制品：`104195319` bytes，SHA-256 `c62e9b9c4a3fea77b51e026bce10431844599b03d5250760f1fb216001c0dc37`
- 制品内部绑定同一 commit/tree，包含 `dist/`、`mochawesome-report/`、`source-commit.txt`、`source-tree.txt`
- 配置 canonical SHA-256：`1707fbf7191de5b4028063ee41c752e13c56eef1bb45b1d9ab554c82de71dfbf`

这些证据只证明各自固定 Run 的云端测试、构建和制品，不表示已生产部署。旧验收不能作为新自动发布配置已跑通的证据。

## 2026-09-12 当前生产验收证据

以下两个生产 Run 由其它执行者触发；本次流水线优化只做只读关联和产物核验，不将其归因于本线程，也没有重复触发生产。

### 后端 Run 18

- Pipeline：`5260799 / cyf-api-kit-ci`；状态 `SUCCESS`
- commit：`a8489561586400af049eee625d90b6e98e834f04`；tree：`1fd1cb7f60e279e4e934239434d4a3a7c8c59cdc`
- 构建 Job `513927230`：74 tests，0 failures/errors/skipped；`validateLayering`、`:starter:bootJar`、PublicArtifactVerifier、OpenCV provenance 与制品上传成功
- 发布 JAR：`220206485` bytes，SHA-256 `aa64ddf1be41147156236aa3d4f70121e2b95918d8dd2024d0cd3d0fec4df090`
- 下载包：`198144927` bytes，SHA-256 `2c04f7b03f37fc70fc7d673c486f0cc2f97813e0b7ba790c168c68a69ef12ffd`；内部 receipt SHA-256 `52afc26bee8438202ca45b9f986e74756ff79fe803465b1efff2d75752519286`
- 部署 Job `513935436`；部署单 `69495567`；主机组 `28833`；一批一台 `Success / healthy`
- 部署机日志确认 `ARTIFACT_ATTESTATION=MATCH`、运行用户 `cyf-api`、端口 `10018` 由目标 PID 监听、loopback `HEALTH=UP`，最终 `CYF_API_FLOW_INSTALL=PASS`
- 公网 `https://api.chaoyoufan.cn/actuator/health` 在本次核验中返回空响应，未独立证明公网反向代理 health；这不改变部署机 loopback health 已通过的结论
- 当前配置 canonical SHA-256：`919eb67be40c379507306633f224ce291f7338e216125df4dc7a956403672da3`

### 前端 Run 91

- Pipeline：`4403172 / cyf-web-kit`；状态 `SUCCESS`
- commit：`c9cbdccb7ceaa1cecab59bb4f2d6cd441042b2c3`，与前端 CI-only Run 7 相同
- 扫描、单测、构建、部署全部成功；Mocha `2118` tests，`2116` passing，`2` pending，`0` failures；Vite `6.4.3` build `9.77s`
- 生产包：`102898255` bytes，SHA-256 `da53366b2f302eb50cc1f63cd17783447aa36a7fe529787bc272fe28d8ce59b4`，Flow 日志 MD5 `e11298669fa2f73ae75697afaf81463e`
- 部署单 `69495496`；主机组 `28833`；一批一台 `Success / healthy`
- 包内 410 个文件全部存在于部署目录且逐文件字节一致；无缺失、无差异。部署目录另有 143 个不属于本次包的历史文件，当前入口不引用它们，但后续应改为 staging + 原子切换或按 manifest 清理
- 首页、`/juyiting` 均 HTTP 200；入口 HTML、主 JS/CSS、聚义厅懒加载 JS/CSS 共 5 个关键文件与同 Run 制品逐字节一致
- 当前配置 canonical SHA-256：`6feb2c10d5609b93f9e19fca8a09905ef3db91ba2ddba74d6693014c54c5c718`

完整非敏感机器可读摘要见 `docs/aliyun-flow-cicd-evidence-20260912.json`。


## 2026-09-12 18:54 CST 增量

- Web `4403172 / Run92`：develop `1ac5cb1e4973919bacf054e961b43ff24d47e832`，2117 passing / 2 pending / 0 failures；部署单 `69505789`，410 文件及 9 个线上响应哈希匹配。制品 SHA-256 `ab289e2791709f70202e161b57db2a35e24e55271148a67114019d5ec1285741`。手动发布已实成；自动 push 尚未启用。
- API Run22：58 类范围的测试/构建成功，但启动缺 `javax.mail.MessagingException`，发布器已自动恢复旧 Run18 JAR，health UP；不是新功能上线成功。
- 新候选 `688a3e65` 将 SMS mail 从 compileOnly 改为 implementation，新增隔离主运行 classpath 回归。Run23 已单次启动；59 类范围和 bootJar 实际 mail/activation/provider 类检查在制品导出前执行。未取得新运行健康证明前，不标后端发布完成。
- 安装保留锁与回退；仅将瞬时锁冲突改为固定 60 秒等待。同 Run 下载副本在验证身份及完整摘要后回收，保留 incoming、云端制品和回退 JAR，当时保留 5GiB 运行余量；该固定阈值已按 2026-09-13 用户指令取消。

## 2026-09-12 19:24 CST 发布闭环与并行推进

- API `5260799 / Run23 SUCCESS`：develop `688a3e6546dcacba116f76cbec7e1d91f72764f4` / tree `608e799ad81ab3c4876b376119af322901a903ef`；59 类 selector 范围、bootJar 实际 mail/activation/provider 检查通过。Build `514133208` 复用，未重复构建；部署 Job `514138578` / order `69507020` 单机 Success/healthy。
- JAR `a5cc9db17022291bc129b0536d5b8c785dac9efec4bf437ea503f3e183be721d` 与 canonical 文件一致；receipt `c9559c37aec9b1010d17e54a577e0eb5079b38377cb3abd32367129602819c08`；PID `2607082` 监听 10018，loopback `UP`。公开 `/agent/map` 命名只读探针获未登录 401；默认 curl 被既有 Nginx 规则拒绝，公网 actuator 未暴露，不能宣称已验证登录业务。
- 原 Run23 deploy 在 installer 前因协调 FD 继承失败。修复父 coordinator 持有 v2 mutex、installer `close_fds=True`；17 项控制测试通过，单次只重试部署 Job，新 JVM 无协调 mutex FD。未解除旧锁或手动终止服务；生命周期由 Flow 安装器完成。helper SHA `d3c7bb4fa94c5628068bdac3b9ecb2b332031811c42dfd15a8b48e1113ccd311`。
- 19:24 只读云端配置确认两组件均为 Gitee/develop/push/^develop$，webhook 已存在；此前“前端 push 未启用”描述已过时。配置存在不等于实际 push 自动触发已验收，下一次真实 push 先对账，不重复手动 Start。
- API 发布包、A03/A16 只读增量及 mail 运行依赖修复已闭环；完整 A16、M4/M5、案卷阁登录验收及付费业务仍未完成。A16/E01/F03 已分别派给并行 Owner，无独立 Reviewer。邮件监控已观察 SUCCESS，但三次邮件 helper 未接受，不能宣称邮件已发达。
- 完整精确证据：`/home/isp/wsps/cyf/docs/implementation/handoffs/FLOW-API-RUN23-DEPLOYED-20260912.json`。

## 2026-09-12 20:36 CST 增量

- API Run25 SUCCESS：develop `ef1a9659`，JAR `ea9de1bd`，order69508149，PID2659818/healthUP。63类范围测试构建成功；E01评分及顺序修复已发布，F03仅增加默认健康隔离测试。完整证明见 `docs/implementation/handoffs/FLOW-API-RUN25-DEPLOYED-20260912.json`。
- Web Run93 **Flow FAIL / installed+online verified**：develop `b58d3727`，2119pass/2pending；410安装文件及9线上哈希全部匹配。原20:23:23首页校验不匹配，之后同请求已匹配，原因尚未知；不改写失败、不重复部署。实际自动push触发已证实。详见 `docs/implementation/handoffs/FLOW-WEB-RUN93-ONLINE-WITH-FAILURE-20260912.json`。
- Web安装器反复gzip随机seek的独立性能问题由Owner改为有界顺序staging，并补最终只读重验诊断；不降低制品、路径或身份校验。A16异步受理基础 `9672b4bc` 已push，保持default-off，不声称执行器已完成。


## 2026-09-12 23:00 CST 增量

- Run31/f6554168 已 SUCCESS，初次容量拒绝发生在停机前，same-artifact retry69510726部署成功。canonical JAR/record/healthUP 已复核；API push 自动触发仍未证明。
- 后端配置当前66selectors，canonical05d595b2；云端显示名并发变为cyf-api-release，ID5260799与YAML未变。E02 develop00db已提交，单次Run32观察中；Web develop1b3自动Run94观察中。仅云端终态+制品+在线证据可更新发布gitlink。


## 2026-09-13 登录修复与门禁精简验收

- 删除无测算依据的固定资源/大小阈值及本地超时判败，24 项相关控制面回归通过；三个线上 helper 的候选摘要与 readback 一致，未清理历史备份。
- API Run36 SUCCESS，commit `5ece9141e66f27aa2d5443dada1ea816e44ca95c`，deploy order `69520177`；JAR SHA-256 `1c073e3bf7928bf9f057d81d33265fe8323384247a112ab5cd2111df811925b9`，PID3257882/health UP，包含 `80383a07` 登录表单与 CORS 修复。
- 公网预检明确包含 x-request-id，未登录 map 返回可读401，无效 code 的 token 表单返回400 invalid_grant而非302登录页；真实账号及第三方/微信交互仍需用户重试确认。
- 精确证据：`docs/implementation/handoffs/FLOW-AUTH-GATE-FOLLOWUP-VERIFIED-20260913.json`。


## 前端发布验证范围与缓存（2026-10-09 核验）

核验源码：Web `81f49518c3f23f794f9d37f4ac0be024d65d9f55` / tree `5595dab02479b49b3ef803eda6c84c67ef22ecb9`；Flow4403172 Run188 SUCCESS，普通验证总176秒（2分56秒），2790通过/2pending/0失败、Mocha72.298秒，Vite11.28秒，制品及并行JS扫描成功。**本次未部署/未在线核验**；不据此宣称完整版本发布或所有候选均在5分钟内。

按用户追加授权，默认release profile保留业务/身份/ACL/幂等/交付/恢复及实际游戏运行时回归；16个离线资产作者工具/E13重算/E14性能验收文件单列assets/all。涉及`public/juyiting`、资产生成器、renderer、E13/E14或其fixture/验收工具修改，Owner必须在固定SHA选择`CYF_TEST_PROFILE=all`的Flow，不得用release成功代替资产验收。assets/all保留原签名/SHA及10秒预热/60秒采样。覆盖以同Run `ci-profile.json`为准（旧job标签含full tests不代表all-profile）。不改版本化发布、制品来源/摘要、部署互斥/恢复/健康或develop不自动部署规则。

只读清单确认旧缓存10份历史runtime提取目录总4.145GB（未压缩），npm下载缓存仅43.73MB。新提取目录移出Flow缓存，仅清理当前独占worker恢复的旧实体目录、不跟随链接。Run188缓存归档355.91MB，归档与上传约5秒且成功；旧Run186归档2.011GB、76秒并因平台2GB上限未上传。删6个无消费者直接开发依赖，lock减少95项，保留包版本及完整性未变；删除脚手架测试并合并重复正向重算，负向篡改测试在assets/all保留。

Run187的manifest原只接受x.y.z，拒绝合法既有prerelease；已保存前值、修正严格SemVer校验并单次update/readback，根模板同步，Run188证明该配置候选成功。Flow SHA `719b28019ba51985a11a60dd2af99ed3a336d4de760004301dd0c2336e2a65a3`。详细scope/失败/授权及未验证项：`docs/implementation/handoffs/FRONTEND-RELEASE-5M-20261009.md`；正式摘要：`docs/implementation/evidence/frontend-release-5m-20261009/summary.json`。
