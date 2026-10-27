# 引导期间导航消失修复（2026-10-27）

- 任务JUYITING-GUIDE-NAV-20261027；唯一Owner guide-nav-owner-20261027。已读根/Web AGENTS、编排README、cyf-quick-iterate/aliyun-pipeline；接口规范api/docs/interface-standard.md v1.4（2026-10-24），此次不改接口。
- 目标：引导期间手机底栏可见可定位、PC侧栏保持可见，背景不可交互；关闭恢复。保留详情、软键盘及普通业务模态原有导航隐藏规则。
- 非目标：API/Runtime/业务写入、生产部署。用户“好，执行”授权修复，非新版本上线授权。
- 2026-10-27远端develop只读核实1fdae7355dc19dea90186251de11ad19e4402758 / tree e2209ab2d286ecbf8066d4ddc7d5769acf733cc7（1.16.62）；线上历史观察350，不作为本次线上核验。主checkout ca22ac2且脏，保留；必要隔离复用唯一.worktrees/juyiting-guide-nav-web，分支codex/juyiting-guide-nav-20261027。
- 根因：JuyiHall将onboardingVisible传给externalRootModalOpen，resolver按普通模态主动隐藏dock。先前只造始终可见导航的shell，未覆盖宿主计算，导致漏检。
- 原型：唯一web/prototypes/juyiting/index.html help状态；先更新引导保留导航且inert的状态/规格，再修改产品；保留主原型他人脏改，精确补丁同步候选。
- 验收：真实宿主computed/模板导航链路＋实际HallOnboarding定位联动；320/390/760/761/PC与低高度，键盘/详情/普通模态、关闭恢复；本机轻量定向，正式测试构建Flow4403172 CI-only，总≤600秒。不启动重复构建、不取消他人Run。
- 证据目录/home/isp/state/juyiting-guide-nav-20261027/；阶段结果/耗时实测追加，未知留空，不承诺缩时。

## 实施与定向验证

- 原型先精确修改既有help状态：手机底栏显示、两端导航inert、规格标明引导不等于业务模态；HTTP预览18786可达，1440/390/320截图无横向溢出且移动导航保留。主原型其余脏改未覆盖。
- 产品仅移除onboardingVisible→externalRootModalOpen错误映射，给底栏/PC侧栏显式绑定引导inert；未改resolver的普通模态、详情、返回、软键盘规则。版本1.16.63。
- 新增宿主导航回归不是全量挂载JuyiHall：从真实JuyiHall取computed、根class及导航模板，沿用真实resolver，再与实际HallOnboarding组件联动。测试覆盖5断点、4一级根、引导可见性、inert、四步高亮、关闭释放、导航恢复、键盘/详情/非一级页隐藏；保留原有模态/地图回归。
- 27项定向测试通过（targeted-verified.log，标准10000ms单测timeout）；首次27通过后，最终复跑因命令--no-config误用Mocha默认2000ms导致一既有用例超时，恢复项目既有10000ms后27通过，无产品改动或删测试。ESLint JuyiHall与基线完全相同的1项既有error，未新增，不宣称全绿。
- Chromium6视口1440×1000/390×844/320×568/760×700/761×700/844×390，共24引导状态：真实导航模板/计算/CSS＋真实引导组件通过，无缺失目标/横溢/业务跳转，焦点留在引导；native inert阻止背景聚焦与导航，关闭后真实鼠标点击可导航，键盘状态仍隐藏dock。手机第2步截图已明确保留并高亮“事项”。这是离线真实导航子集，不是认证整站或线上验收。
- 浏览器诊断原始失败保留：初次启动未等到page target；随后误将点击背景（既有“稍后”收起行为）当成引导仍打开；再发现低高度fixture缺少真实页面父级高度，导致文档滚动挤出导航。修正诊断启动/预期/父级布局后重跑通过，未借此修改产品点击关闭或几何逻辑。证据browser-layout-final.log、browser-results.json、guide-*.png、prototype-help-*.png。
- Node语法与git diff --check通过。未本机生产构建、未调用安装器、未操作API/Runtime或真实业务。

## 固定候选与云端验证准备

- Web1.16.63已提交`8a3826b6e71ac3e3b25de75dfeeca39e98779fd5` / tree `0bfa1d2de77cbdb11f70ad5597097bd53d8b02ec`，9文件。已推develop并ls-remote精确readback；旧主checkout未切换。
- 实时读取Flow4403172默认CI-only配置，canonical SHA仍d40133eacfd9616ae8737e2462c366ce11565235c5b3fb8fdec1f38bf9dd18cd；未改云端配置。启动前全分页350条历史无活动Run；推送后等待35秒再分页只读核实无自动Run，随后才单次手动启动。仅本任务570秒受控超时watcher，不取消他人Run。
- 首次只读snapshot进程以143中断，未push/未start；通过远端仍1fdae73且无pre-push/start文件核实后，仅重做只读snapshot成功，不是重复启动。Flow安装/Run/线上状态仍分开记录。

## 云端首轮失败归因与修正

- Flow4403172/351 **FAIL**，10:12:26—10:14:17，共111秒；真实源码8a3826b，测试3461通过/1失败/2pending。唯一失败是旧真实组件用例`suppresses the focusable workbench dock while the root onboarding modal is visible`要求隐藏导航（tests/juyiting-component-behavior.test.js:2940）；这是本次规格变化必须同步的回归，未完成构建/制品，不宣称本轮通过。
- 已经编排器fail记录归因，保留attempt351/源码、启动context、真实Run与日志；未盲重试旧输入。将该用例改为真实JuyiHall手机/PC两用例，断言导航显示、底部预留与inert、关闭释放；没有删安全断言或改生产代码。定向2通过（real-component-nav.log）。原27项与24浏览器状态所对应产品源码/模板/CSS/引导均无变化，证据保持原范围。
- 修正后的最终Web1.16.63候选`00b1a6b367ded7764a416a065e49c409360fbfba` / tree`3031a68acc36f4cd610ddceef2da160ddb3fbd90`。只增加上述测试修正，产品源码与8a3826b完全一致；后续正式CI须以这一精确候选为准。

## 正式验证通过，待授权部署（2026-10-27）

- 最终Web1.16.63 / `00b1a6b367ded7764a416a065e49c409360fbfba` / tree`3031a68acc36f4cd610ddceef2da160ddb3fbd90`已推develop并readback。相对原基线共10文件，未改API/Runtime/身份/业务提交。旧主checkout与其他worktree保持原样。
- **Flow4403172/352 SUCCESS**，10:20:40—10:22:41，总**121秒**；完整release测试**3463通过、0失败、2既有pending、0 skipped**，锁定依赖安装、测试、Vite生产构建、JavaScript扫描及同Run上传成功。没有部署作业。351的失败证据独立保留，不改写成通过。
- 同Run制品109575796字节，SHA-256 **149a891c1a41177cbb5ca8bf08fa4f22a2a465c7c0187e495b6f0a12f97ae420**。独立核对真实Run源码、manifest版本、source-commit/tree与**612项dist文件摘要**全部匹配；引导两端/第二步标记命中。首响应UNKNOWN只因来源未填，终态真实源码核对后CONFIRMED，无重复启动。web-start-resolved.json保留。
- 本机定向27项＋真实JuyiHall两端2项，浏览器6视口24状态通过。最终仅测试修正的候选与原浏览器/27定向输入7文件逐字节一致，source-check.json记录摘要与范围；不把树变化后的旧报告无条件当新证据。线上认证业务未执行。
- 10:24:29只读配置readback仍为默认CI-only，canonical SHA d40133eacfd9616ae8737e2462c366ce11565235c5b3fb8fdec1f38bf9dd18cd，无deploy stage；本任务从未改云端配置或安装器，无需restore。
- 稳定知识已定向回写既有runbook、原型规格和优化方案；这些主工作区文件混有既有任务脏改，保留且不整文件提交。本轮根收口只纳入本任务handoff、精简验证证据和已核验Web gitlink。正式证据`docs/implementation/evidence/juyiting-guide-nav-20261027.json`；完整报告/manifest在私有目录run352/，日志、截图、初次失败与候选补丁保留原路径。
- **未部署**：用户本轮授权为修复；当前验证制品不代表生产已更新。后续需明确授权这一版本，通过Flow同Run版本化发布并在线核验，不能本机直发或把本次CI制品伪装成另一次Run输入。

## 收口

已保留远端精确源码、candidate.patch、报告/manifest、源码标识/摘要、日志和截图后，清理本任务唯一worktree/分支、共享依赖符号链接（不删共享依赖）、Chrome临时profile和已核验下载副本；cleanup.json readback通过。主Web旧HEAD/原有脏改、唯一原型预览、其他任务工作区及生产状态未动。开发与正式CI完成，部署等待另行授权，不把等待部署记成开发阻塞。

## 获授权发布（2026-10-27）

- 用户后续明确要求“部署”，发布范围固定Web1.16.63 / 00b1a6b367ded7764a416a065e49c409360fbfba / tree3031a68acc36f4cd610ddceef2da160ddb3fbd90，唯一Owner guide-nav-owner-20261027；不涉及API/Runtime。
- 10:36 +08实时核对远端develop仍为固定候选，线上record仍1.16.62/350；主checkout及其他脏改不动。本次复用既有4403172临时授权配置，同Run完整测试构建部署，不直接发布352制品。
- 原CI-only配置先保存、候选固定并readback，无活动Run才变更；570秒受控取消仅本任务Run，总≤600秒。安装器摘要核对、原index/record备份、原发布锁及可恢复安装不变；异常不手抄旧状态回退，走受控恢复。完成后按配置归属恢复原CI-only。证据/home/isp/state/juyiting-guide-nav-release-20261027/。

## 发布完成与线上核验（2026-10-27）

- **Flow4403172/353 SUCCESS**，10:39:43—10:45:01 +08，总**318秒**（Run创建至终态，低于600秒）；源码精确00b1a6b367ded7764a416a065e49c409360fbfba，版本1.16.63。完整release测试3463通过/0失败/2既有pending/0 skipped，Vite构建、JS扫描、同Run上传及部署作业均成功。启动初响应UNKNOWN仅因source未填，最终来源已核实并单独记录CONFIRMED，没有重复start。
- 部署单71861980，1批/1台主机Success、client healthy。生产record为353/1.16.63/online_verified；同Run制品109576000字节，SHA-256 `29f99a0166df31da0093ddb0de143d702217c6100035ccea755ce4d2da7d2011`，不是352制品。archive source-commit/tree、manifest版本和**612项实际安装文件摘要**全部匹配；公网根入口、/juyiting及相关JS/CSS共9项响应200且摘要匹配，两端引导标记命中。
- 已核对备份`/home/isp/baks/cyf-web-juyiting-guide-nav-release-20261027/`的原index摘要与原350/1.16.62 record一致；恢复仍须走受控流程，不直接复制状态覆盖新事实。保留安装制品`/home/isp/state/cyf-web-flow/downloads/353/package.tgz`和原备份，不按临时目录清理。
- Run结束后按候选归属恢复原CI-only配置，update/readback APPLIED；10:47:35 +08再次实时核对canonical SHA d40133eacfd9616ae8737e2462c366ce11565235c5b3fb8fdec1f38bf9dd18cd，无deploy stage。未改生产安装器、未运行本机构建/直发、未触碰其他Run。
- 安装执行、Run终态和公网资源已分别核实；**未执行线上认证后的手机/PC业务交互**，不将离线24状态或静态资源核验写成线上业务E2E通过。精简发布证据`docs/implementation/evidence/juyiting-guide-nav-release-20261027.json`，完整控制面/恢复/公网摘要在私有发布目录。部署作业日志API返回空内容，保留原响应，不声称已读完整安装日志；安装成功依据部署单、生产record与独立摘要核验。
