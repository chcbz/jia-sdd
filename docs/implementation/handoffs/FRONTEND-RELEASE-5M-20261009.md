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
