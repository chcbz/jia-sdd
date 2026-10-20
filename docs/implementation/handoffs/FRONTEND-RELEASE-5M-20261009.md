# FRONTEND-RELEASE-5M-20261009：前端构建发布 5 分钟目标

核对日期：2026-10-09；唯一实施 Owner：本聊天。本文记录范围与证据，不新增第二任务状态台账，不声明正式验收。

## 范围与基线
- 目标：定位 Flow4403172 的端到端耗时，修复无效缓存，保留完整测试、E14 固定采样、SHA/签名、同 Run 制品及部署锁；目标从触发到在线核验 ≤300秒，不以超时取消伪造达标。
- 非目标：API、业务功能、生产安装；不接管/取消/修改其它聊天 Run，不恢复 develop 自动部署。
- Owner 隔离源码：`/home/isp/wsps/cyf-worktrees/frontend-release-5m-20261009`，branch `codex/frontend-release-5m-20261009`。
- Web base commit `c6ae76010c43153659cc6d55c902a1765c620932` / tree `f82ac5739135e6e7fe0f2e4f0edbcb17dbb06fa2`。
- 2026-10-09 约17:00 +08:00 查询远端 develop，确认为上述 SHA；不是线上版本声明。
- 根源码 HEAD `e0e2023b65d993be83f5a6d65fa065a58348f505` / tree `b460684313c6f098584d16b9b299e59f8cc65dd5`；共享根脏工作区保留，不修改现有 TASKS.yaml。
- 受测历史输入：Run185 commit75766a3；Run186 commitc6ae760。线上发布成功与在线字节核验分开，不把 Run SUCCESS 当作本聊天线上核验。
- 最早定向检查：原 `tests/ci-test-bootstrap.test.js`，不下载、不运行本机 Vite、不替代 Flow。

## 证据
`../evidence/frontend-release-5m-20261009/`：API job timing、脱敏日志、同 Run 制品中的测试耗时。
- Run185：build job763秒；Run186：build job833秒、deploy job45秒。
- Vite11.63/11.70秒；完整Mocha约6分钟；缓存保存77/76秒，2011339927/2011337113字节超过云端2000000000字节上限，实际未上传。
- API日志即使 more=false，仍内嵌平台 omitted-lines 标记；前置安装/准备耗时暂不能逐项精确分解。`*-full.log` 指未做本地tail裁剪，不代表平台原始完整日志。

## 接续与验收边界
- 专项工具：`ops/orchestration/README.md`、`ops/ci/aliyun-flow/README.md`、`web/scripts/ci/README.md`；以2026-10-08项目规则为准，技能旧双端Flow/自动发布文字不适用。
- 修复候选需同源码Flow验证后才能宣称有效；5分钟必须真实端到端测量，不能用诊断/推算代替。
- 阶段时间：定位开始约16:57 +08:00；实现、验证、云端等待分别以实际证据补充；未知留空。

## Owner 自检与后续动作
- 候选 commit `b10ee3ce9c0471cae732fce40fa5f6220156a1e2` / tree `c5554b28df1ccd2d5efe0823ce5ca13cd183764f`；独立分支保存，未push/合入/启动Flow/部署。
- 改动：`scripts/ci/prepare-runtime.mjs`、`scripts/ci/README.md`、`tests/ci-test-bootstrap.test.js`。新解压目录移出Flow缓存；仅删除当前独占worker恢复出的历史 `run-XXXXXX` 实体目录，不追随链接，不修改全局/生产缓存。SHA、签名、Chrome133路径/provenance、完整测试和E14合同未变。
- 定向本机诊断：19 passing (663ms)，`git diff --check`通过。依赖复用原web node_modules；不作为正式Flow证据。
- Run186同Run制品SHA `5fdf413389f4e944a9508b30983df5ec8c9fb1736c15a51516600827094baec9`：3193 registered / 3191 passing / 2 pending / 0 failing；Mocha369.062秒，E13独立重算115.450秒。
- 从列表触发时间至最后部署job完成880秒（14分40秒）；不含本聊天未执行的额外在线字节核验。
- 平台CustomEnvironmentBuild开始至Mocha开始约296秒，包含依赖安装、runtime准备和E14；平台省略1142行，不能将该296秒全归因安装，也不能量化各子项。
- 下一条动作：取得未省略的原始步骤日志，并在同固定源码非发布候选中验证缓存修复；随后预置按摘要固定/保留完整性验证的云端测试环境，按耗时分布将重回归在隔离目录并行，保留每项测试覆盖对账及fresh E14依赖顺序。不能直接全局开启Mocha parallel（共享fixture/报告/launcher未经隔离验证）。
- 5分钟尚未达成；上述缓存补丁不是完整解决方案。候选正式Flow、冷/热缓存、排队和部署在线核验仍待测；不通过缩短采样、跳过测试、强制deadline或取消他人Run制造达标。
- 未修改流水线配置、服务、其它聊天源码、TASKS.yaml或生产数据；根工作区原修改保留。

## 2026-10-09 用户追加范围与集成

用户明确授权删除非必要/耗时测试并检查依赖。该授权更新本任务的“普通发布必须原完整套件”假设：普通发布保留业务、身份/ACL、幂等、交付、恢复与真实游戏运行时回归；离线资产作者工具/E13重算/E14性能测试单列assets/all，不缩短其内部断言、采样或完整性检查。涉及资产、生成器、renderer、E13/E14、fixture/验收工具的变更须固定SHA执行all-profile Flow；普通release PASS不能覆盖资产验收。

- 源码 `81f49518c3f23f794f9d37f4ac0be024d65d9f55` / tree `5595dab02479b49b3ef803eda6c84c67ef22ecb9`，已Owner自检后fast-forward组件develop并push；未修改Flow配置、未部署。
- 自检：21项bootstrap/profile检查；含身份隔离、交付和恢复的定向集37 passing (464ms)，语法及diff检查通过。复用现有node_modules是诊断，不是干净安装/正式构建。
- 真正删除：3个HelloWorld脚手架测试；合并1个重复270-shot正向完整重算，将其unique live/review/pending断言并入隔离黄金测试。E13负向篡改断言保留。
- 普通入口移出16个资产/历史工具测试文件，保留`test:assets`及`test:all`、三份明确profile配置；Flow报告附带ci-profile.json，不能声称release运行了原3193项测试。默认release不安装无关Chrome/RPM工具链、不执行E14，assets/all仍固定版本、签名/SHA及10秒预热/60秒采样。发布测试入口仍清理当前独占worker恢复的旧runtime目录。
- 删除6个无运行源码/配置消费者的直接devDependency：@babel/register、@testing-library/jest-dom、@testing-library/vue（仅已删脚手架）、@varlet/import-resolver、babel-plugin-transform-vue-jsx、lodash。npm package-lock-only卸载移除95个lock entries，无新增项；保留项的version/resolved/integrity完全未变。不删除仍由配置/源码使用的Babel核心、postcss、TypeScript、Vue、melonjs等。
- 缓存只读流式清单（不落盘/解压整个缓存）：2026-10-09 17:12:47 +08:00 当前mutable object压缩1860847314 bytes；uncompressed runtime4504437703、npm cache43730490、npm logs11558。10份run-XXXXXX各414511691 bytes，总4145116910 bytes；DNF219807399，Chrome archive113060974，Node archive26169540，WebP archive282880。重复提取物占未压缩缓存约91%，依赖下载不是2GB根因。对象SHA及目录汇总见cache-inventory.json。清理旧run后现有保留内容理论403062841 bytes，实际新缓存归档大小/传输耗时须由候选Flow核验。
- 配置readback 17:23 +08:00：Flow4403172只有CustomEnvironmentBuild/ArtifactUpload及JS扫描，develop push已配置，无部署；仅查配置不等于webhook触发成功。17:26:06初次post-push列表尚未出现新Run，继续只读对账，不重复Start。
- 当前真实状态：已集成/推送，候选正式Flow待关联；5分钟端到端与资产专项候选断言未验收。

## 正式Flow收口（2026-10-09 17:44:48 +08:00）

- develop push后未观察到自动Run；只读分页对账无活动/同SHA新Run后，单次启动187。原控制面start helper遇>100历史须额外对账；专项SDK调用只处理本管线，固定配置哈希/branch/SHA/selector/请求时间与完整已有Run集合，未建新runner/pipeline。
- **失败矩阵**：Run187、Web81f4951/tree5595dab、release selector、配置2fcc386：2790测试通过且Vite11.60秒，失败发生于manifest的旧x.y.z-only版本校验，拒绝合法的既有1.14.0-consolidated.20261009；不是删依赖或测试导致失败。未盲Retry，不发布。
- 修复：保存原Flow0600快照；仅改manifest版本正则以支持严格SemVer prerelease/build，保持非法格式拒绝。candidate SHA719b28019ba51985a11a60dd2af99ed3a336d4de760004301dd0c2336e2a65a3，单次update/readback APPLIED；sources、测试/制品阶段、部署行为不改。根模板同步；16种版本输入检查、6项模板回归、18项隔离制品安装回归通过（后者仅临时目录mock，不是生产安装）。
- 材料变化明确后单次启动188；实际取源81f4951/tree5595dab，SUCCESS。服务端Run开始17:41:52，最后job结束17:44:48，**总验证176秒=2分56秒**；build job175秒、并行scan127秒。
- 同Run下载归档106555144 bytes，SHA256 d9f96867af6f0d6e26c9c6be17f75b6e5f5a9ed273614e6936cb3119ea54c930；已核对manifest及source commit/tree/version和profile。正式新锁干净安装、测试、Vite及制品上传/扫描成功；Mocha2790 pass / 2 pending / 0 failures，duration72298ms；Vite11.28秒。普通release覆盖，不冒充all-profile。
- 新缓存355911787 bytes（约356MB），17:44:40至17:44:45归档并上传成功，约5秒；旧Run186归档2011337113 bytes且未上传、76秒。根因确为10份重复runtime提取物而非npm依赖。
- **边界**：已集成/推送并完成普通构建验证；没有部署、重启或线上字节核验。仅证明本次验证<5分钟，完整版本化发布及冷缓存/其它候选的<=5分钟未实测。修改后的资产golden断言/all-profile未正式运行，后续资产相关变更必须选择all-profile。
- artifact reconcile脚本两次因`helper-release.json`与`release.json`后缀匹配混淆而失败；确认原因后改为唯一完整成员名，已取得同Run元数据。该诊断错误不属于应用/Flow失败，也未重复触发流水线。
- 无Owner交接/新Reviewer，无当前任务ledger覆盖；原共享根/后端修改保留。

- 根控制面SemVer源码已提交 `9b66f9bd16f995223088e3dc1f7fdd9c23d5b99f` / tree `fa3298a08a38ef01a1b6ecd51338e8f00c546bc1`；仅模板和16输入专项回归，无其他根修改纳入该提交。

## 2026-10-20 前端耗时接续：TMX 重复解析

- 当前用户授权：先优化；无收益时可删除未应用的TMX相关测试。当前优先保留覆盖，不删测试、不改运行时/业务行为。
- 唯一Owner：本聊天；范围为TMX编辑器的调用内解析复用及定向回归。非目标：扫描门禁、全局Mocha并行、生产发布、其它聊天源码。
- 独立Web worktree：`/home/isp/wsps/cyf-worktrees/frontend-tmx-timing-20261020`；branch `codex/frontend-tmx-timing-20261020`；base commit `50107f38a757a5ce58d298965a953a353d7b48b1` / tree `2adbc30cdc5cdbd7db3f41375751113e22e448b8`。2026-10-20再次ls-remote确认develop同SHA；线上版本未另行核验。
- 已读根/组件AGENTS、orchestration及Flow工具说明、scripts/ci/README；遵守统一接口规范`api/docs/interface-standard.md` 2026-10-14冻结版本，本任务无接口变更。不修改共享TASKS.yaml或其它Owner脏文件。
- 基线调查：Run257测试73.095秒，TMX编辑/快照33.030秒；build143秒、并行scan133秒，部署49秒，总193秒。不同Run不当作受控对照；脱敏只读材料`/var/tmp/cyf-web-flow-timing-20261020/timing-audit.md`。
- 最早验证：自有worktree复用已安装依赖，原TMX编辑测试定向诊断；补充跨调用/变更后缓存失效回归；不本机生产构建。正式验证须同固定SHA的Flow无部署候选；当前云配置包含发布阶段，禁止直接启动。开发完成不等于云端性能验收或发布。

- 17:04 +08实时readback修正：当前云端配置SHA `31883fd59c9a33ef4847979fd99147375fda555d99498f17bc8cc5a6b94c389b`，解析后只有cloud_ci（build及scan），**当前无deploy阶段**；前述“当前含发布阶段”是误把Run257历史配置当成现行配置，已纠正。正式启动仍先保存/readback并全分页检查活动Run。
- 实现候选：每次apply独立、单条目、仅字节相同文档的解析复用；变更后重解析、无跨调用状态，replaceRange无变化时返回原字符串；新增偏移刷新/异常后恢复与重入回归，未删测试。
- 本机诊断：旧15项106.885秒，14pass/1 CLI 60秒超时；初版15项59.040秒，14pass/1默认2秒超时（命令未带正式10秒默认）。最后按10秒默认检查29项：编辑17项均通过；快照10pass/2原20秒case超时，总235.074秒。本机负载不可比，不能归因为算法错误或宣称流水线已提速，不再盲重试；需要干净云端固定源码验证。
- 修改两文件ESLint及diff检查通过。typecheck:game存在基线cameraController.ts:208三处candidate possibly undefined，修改文件无新诊断；本轮不改无关相机代码。

- 候选源码已推送独立分支：commit `8ece5a25a850ca5bf85a6ce91a0e6be30ab20edd`，尚未合入develop。无接口或生产版本变更。
- 启动前全量分页查询257条历史，无活动/未知状态；保存私有原配置，固定candidate与来源，单写readback APPLIED。原CLI start对>100历史拒绝，复用原SDK窄调用先全分页核对既有Run集合/配置，然后仅启动一次；未修改共享runner。
- 本次CI仅临时改来源到候选分支、加完整SHA断言并执行test:all（资产作者工具变化按原规则），其它build/scan/helper/制品合同不变，无deploy阶段。配置candidate SHA `cc84db0fceb783c821bd045b602b6d4c9bb4dbb16fe5e00d97839ad5a96f2fcc`，保存readback canonical相同。
- 2026-10-20 17:15:36 +08单次启动Flow4403172 Run258；17:18 API确认实际source head为完整候选SHA。此时build运行中、scan SUCCESS135秒。all专项耗时不能与普通release Run257总耗时直接比较；不据此声称已发布/整体提速。结束后仅在配置仍为本候选且无活动Run时恢复原配置。证据私有目录`/var/tmp/cyf-web-flow-timing-20261020`。

### Run258 归因（17:34 +08）

- all-profile测试执行 **3547 passing / 2 pending**，已到Vite且Vite成功11.72秒；build job最终FAIL1123秒，scan SUCCESS135秒。不是TMX断言失败，也不是默认release耗时。
- 实质失败在测试/构建后的manifest：`Wrong Flow identity`。本聊天改候选来源时仅改开头branch gate，遗漏manifest内原develop/旧候选分支白名单。旧校验正确拒绝新候选分支；不得删校验或把该Run标SUCCESS。没有上传合格制品，也未部署。
- all测试通过只依据固定源码Run的已完成测试阶段/日志；完整all-profile制品/JSON报告缺失，不冒充完整all Run验收。完整原始材料仍私有，公开仅保留脱敏数值/源码/日志摘要。
- 修正路径：保留全部测试与原身份校验；Owner自检后同源码fast-forward远端develop，再恢复原无部署配置，以标准develop来源进行release验证。正常release fresh测试/构建/同Run制品重新验证，不复用失败Run制品，也不因配置失误重复无关资产基准；整体性能结论只看可比release Run。

- 17:38 +08 全分页258条均终态且配置仍为本候选后，单次恢复原配置并readback APPLIED：raw SHA `31883fd59c9a33ef4847979fd99147375fda555d99498f17bc8cc5a6b94c389b` / canonical `390998968e302677f3be6dc525036ff352506b14e81ff56e3f29e38cb9133c10`，与前值完全一致，无deploy、无自动触发。未放宽原manifest branch/commit身份校验。
- Owner基于已通过17项定向及Run258已完成的all测试阶段，将Web同一提交`8ece5a25a850ca5bf85a6ce91a0e6be30ab20edd` fast-forward推送develop；tree `0debe9937c72892d6762edfef9af16f0873f77eb`。主共享Web分支/AGENTS/prototypes未改动，未切换其它Owner工作区。
- 后续正式release CI用于校验标准来源身份/同Run制品并测量普通CI性能，是不同selector/修正配置输入，不盲重试失败all候选。后续Run号及最终结果以证据补充；没有应用部署授权扩展。

### Run259 正常release CI收口（2026-10-20）

- 原配置/同源码develop上单次启动Run259，**SUCCESS**。实际源码commit `8ece5a25a850ca5bf85a6ce91a0e6be30ab20edd` / tree `0debe9937c72892d6762edfef9af16f0873f77eb`；release profile **3144 passing / 2 pending / 0 failure**，注册3146（原3144+新增2），0测试删除。
- 同Run制品106711160 bytes，SHA256 `d01df4f9f78c321446b5dc917cde587eadf2ad656581233f632e63d0306a00e6`；已独立读出source commit/tree、release manifest及ci-profile/test JSON核对。报告SHA256 `dbcb4ac38b3f0f3077f67424026d09c94b8dfe7cc678ac5b47b9323c10244f51`。不以该CI制品宣称已安装/线上验证。
- Run257→259：TMX编辑15→17项，21.905→5.220秒；快照12项11.125→11.894秒；两文件合计33.030→17.114秒。完整release Mocha73.095→59.278秒；构建作业143→135秒，扫描133→138秒（并行）。触发→CI结束144→139秒，**不计Run257原部署49秒**；Run259无部署阶段。
- 两个Run不同worker/时间，仅为实测前后样本，不能承诺固定缩时；当前扫描已是关键路径，继续删测试不能等比例缩短整体。用户授权的“优化不行可删除TMX测试”后备方案未启用，覆盖保留。
- 17:43:47 +08 最终配置readback仍与原值完全相同：raw `31883fd59c9a33ef4847979fd99147375fda555d99498f17bc8cc5a6b94c389b`，无自动触发、无部署。不再修改scan范围、门禁或默认profile。
- 脱敏稳定证据：`../evidence/frontend-release-5m-20261009/tmx-parse-reuse-20261020.json`；原始配置/日志和归档仅在0700私有目录。Python报告解析首次因主机3.8不支持removeprefix失败，修正本地解析脚本后成功；未下载第二份制品或重跑Flow。
- 结论：本轮算法优化、develop集成与普通CI验证已完成；Run258只确认已完成的all测试阶段，仍保留Run FAIL/无制品事实。未发布、未重启、未线上核验，完整发布耗时目标不在本轮新增验收内；共享Web工作区/根gitlink不因远端集成而挪动。稳定实现说明已在组件scripts/ci/README.md。
