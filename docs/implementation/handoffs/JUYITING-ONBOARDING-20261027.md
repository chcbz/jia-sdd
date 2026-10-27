# 新版工作台使用指导（2026-10-27）

- 唯一Owner onboarding-owner-20261027；任务JUYITING-ONBOARDING-20261027。已读根/Web AGENTS、编排README、现行接口规范v1.4（2026-10-24）与cyf-quick-iterate；技能旧自动部署规则不适用。
- 目标：按新版办事/事项/资料/我的导航更新手机与PC四步使用指导、实际可见入口定位、入口缺失提示与重开；保留地图/虚拟横屏兼容。
- 非目标：真实提交/委派/发送/付费、接口/Runtime/ACL改动、生产部署。
- 固定基线Web f4e7f779304ee20efa3e6f29a6830a03d20ec88a / tree fcd31763d8fd2484eb1ac03d4f7f5c28497ec34c；2026-10-27只读ls-remote核实。主checkout ca22ac2且原型脏，不切换/覆盖；仅一处必要隔离worktree `.worktrees/juyiting-onboarding-web`，分支codex/juyiting-onboarding-20261027。
- 原型唯一入口web/prototypes/juyiting/index.html，help状态；先精确更新现有脏原型，保留其他修改，再将相同补丁应用候选原型。不另建平行页面。
- 验收：定向Node/SFC测试；1440/390/320及760断点两侧、低高度与虚拟横屏检查；正式测试/构建走Flow4403172 CI-only，每Run总时长≤600秒，不改他人配置/Run，无部署授权。
- 本地HEAD/远端候选不是线上版本证明；本任务不查询或修改生产安装。时间/定位/实现/验证/等待记录按实际证据，不承诺缩时。

## 实施与定向回归

- 原型help状态先更新文案/两端区分、44px按钮和字体，预览18786既有服务HTTP200；三尺寸真实入口截图可达。保留原有其他脏改，不另开原型副本。
- Web候选1.16.61：bb9978876a6fe1d8e5bc284e4b4737f654b9caa0 / tree75d9f8cceae61901c5fa38bd4e54e8176c24f8d6。仅10文件，引导版本v3，身份/ACL/接口与业务提交函数未改。
- 本机25项Node状态/存储/焦点/几何、13项真实SFC/草稿流程定向通过。新增7项SFC覆盖5个断点尺寸、隐藏/缺失入口、跨断点重置及无业务按钮点击；旧虚拟横屏/纯说明/焦点回归保留。
- Chromium实际编译HallOnboarding组件+离线shell fixture：1440×1000、390×844、320×568、760×700、761×700、844×390，4步共24状态，dialog在视口、无横溢、焦点在弹窗、可见入口高亮、业务按钮点击计数0；Tab/Esc/背景隔离释放通过。不是整站认证或业务E2E验收。
- 浏览器首轮发现贴底固定导航被8px滚动留白误判：已改为真实视口边界，滚动只尝试一次；增加贴底节点定向用例并重跑24状态。初次浏览器工具依赖缺失、ESM导入配置错误属于诊断脚本问题，改用既有原生CDP通道，不安装依赖、不计作产品失败。
- ESLint三产品文件与基线错误/消息集合一致（3既有error），未新增，不宣称lint全绿。node语法、git diff --check通过。
- 证据根`/home/isp/state/juyiting-onboarding-20261027/`：node-tests-final.log、sfc-tests-final.log、lint-results.json、browser-results.json、guide-*.png、prototype-help-*.png；最后文案按真实HallMinePage将“消息”精确称为“待办提醒”，完整候选以Flow结果为准。
- 已核对现有Flow为CI-only无部署作业；未改配置。先全分页快照347历史Run/无活动Run，再推develop并等待35秒核查无自动触发，才单次手动启动。600秒上限沿用自己的570秒受控取消watcher，不取消他人。

## 正式CI与收口（2026-10-27）

- Web1.16.61已推送并readback远端develop=bb9978876a6fe1d8e5bc284e4b4737f654b9caa0；tree75d9f8cceae61901c5fa38bd4e54e8176c24f8d6。主checkout仍保留旧HEAD与原有脏改，未切换/覆盖。
- **Flow4403172/348 SUCCESS**：2026-10-27 08:38:45—08:40:48 +08:00，总耗时**123秒**。正式release测试**3454通过、0失败、2既有pending、0 skipped**；锁定安装/测试/Vite生产构建、JavaScript扫描与同Run制品上传均SUCCESS，无部署作业。
- 启动首响应UNKNOWN仅因checkout来源暂未填充，实际returnedRunId348；后续只读取得同一Run真实源码匹配并收口CONFIRMED，未重复启动。web-start-resolved.json保留归因。
- 同Run制品109578058字节，SHA-256 `681725993c3acbc70a0b6ea080a46da5b403564425370880c94a27c4e8506b51`。commit/版本/Run一致，**612项dist文件摘要逐项匹配**；手机/PC标签、四步标题、待办提醒等标记在制品中命中。原始失败与诊断证据保留，不把本地壳体测试称作线上验证。
- `verification-final.json`汇总Run/源码/tree/测试/摘要/标记；run348/release.json与mochawesome.json、浏览器24状态截图和source-check.json保留。没有生产安装、线上健康或真实账号业务验收；上线须另行授权并固定候选。
- 稳定知识已按源码范围回写现有runbook、新版原型规格及既有优化方案。根runbook/方案/台账与主Web原型已有其他任务修改，保留工作区，不整文件纳入本次提交；根收口仅提交本任务handoff与已核验Web gitlink。
- 清理仅限本任务隔离worktree、node_modules符号链接、Chromium临时profile与制品下载；源码远端/完整补丁、报告、manifest、截图和原型修改前片段保留。既有18786预览、主checkout/其他任务目录、共享依赖与生产状态不动。具体完成readback见证据cleanup.json。

## 用户授权部署（2026-10-27）

- 用户在本聊天明确回复“部署”，授权仅Web1.16.61 / bb9978876a6fe1d8e5bc284e4b4737f654b9caa0 / tree75d9f8cceae61901c5fa38bd4e54e8176c24f8d6；不扩成API/Runtime或最新develop自动部署。
- 发布前只读确认远端develop仍是候选，线上安装记录为Web1.16.59 / Run344 /1102350543846e59f2c31dfc36145155da4f7773；旧主checkout ca22ac2与原脏改不动，无需新worktree。实际helper摘要匹配既有版本化适配器，发布锁与控制器锁查询空闲；不抢占他人。
- 现有适配器要求同Run制品，故沿用当前CI测试/构建再同Run部署，不把Run348制品伪装新Run输入；原348保留为开发验收。固定候选源/版本/完整tree，临时云端部署配置保存前值、readback后单次启动，570秒受控结束保护600秒总上限。结束后恢复归属匹配的原CI-only配置。
- 保留同Run摘要、完整性校验、发布锁、assets先行/index最后、旧hashed文件与入口/record备份。恢复沿既有受控发布流程，不手工复制旧index/状态。安装、Run终态、公网资源与真实业务验收分别记录。
- 发布证据根`/home/isp/state/juyiting-onboarding-release-20261027/`，唯一Owner不变；本次不改应用源码或主机安装器。

### 发布完成（2026-10-27）

- Web **1.16.61 / bb9978876a6fe1d8e5bc284e4b4737f654b9caa0 / tree75d9f8cceae61901c5fa38bd4e54e8176c24f8d6** 已发布；API/Runtime未操作。开发CI348为历史验证，正式部署为**Flow4403172/349 SUCCESS**。
- 当次Run 08:52:17—08:56:01 +08:00，总**224秒**（CI约126秒、安装阶段97秒），满足600秒；3454通过/0失败/2既有pending/0 skipped，扫描、测试构建上传及部署均SUCCESS。初始UNKNOWN为来源未就绪，后续真实Run源码/制品/安装闭包核实，无重复启动或取消。
- 部署单**71853086 Success**，单批单机Success/healthy。安装record=349/1.16.61/bb99788/online_verified。同Run归档109578775字节，SHA-256 **cb4a8a13305fe76f57706f876026312ff6b1ad5c93370528e25231c8db8c2545**；独立核对源码commit/tree、manifest/报告及**612项安装文件摘要**，公网首页/聚义厅路由/引导所在懒加载JS等**9项摘要匹配**。手机/PC与四步标题在已安装且公网匹配资源中命中。
- 配置已按原候选归属受控恢复，readback **APPLIED**，默认CI-only canonical SHA `d40133eacfd9616ae8737e2462c366ce11565235c5b3fb8fdec1f38bf9dd18cd`，无develop自动部署。
- 备份`/home/isp/baks/cyf-web-juyiting-onboarding-release-20261027`的index/record与发布前基线精确匹配，原1.16.59/Run344归档和旧hashed文件保留。无需回退；后续恢复走授权版本化安装，不手工覆盖旧状态。
- 验收边界：本次独立核验同Run制品、实际安装、公网资源；未登录执行真实办事/委派/付费/验收。匿名Chromium/CDP诊断未获得稳定引导/初始页面target，原始工具日志保留，不记作手机/PC线上交互通过，也不据此归因为应用或身份故障。同源码的离线两端指导回归仍是发布前证据。
- 汇总`docs/implementation/evidence/juyiting-onboarding-release-20261027.json`；完整证据在发布私有目录的release-summary.json、verification.json、web349-meta.json、web-deploy.json、web-restore.json、run349/报告/manifest/源码标识。仅清理本任务Chrome临时profile，生产下载归档、备份与其他任务/预览均保留。本次无新worktree、无本机生产构建/部署；根仅提交本任务handoff增量与精简发布证据，不覆盖既有脏文档。

### 随后的其他发布观察（2026-10-27 09:08—09:09 +08:00，只读）

本次349已成功完成；最终readback发现其他发布已将线上更新为 **Web1.16.62 / Flow4403172/350 / 1fdae7355dc19dea90186251de11ad19e4402758**（线上record=online_verified，Flow SUCCESS）。经Git祖先关系与三引导文件精确diff核对，350继承bb99788，HallOnboarding/HallOverview/useHallOnboarding源码未变化；当前公网入口和引导JS/CSS共3项摘要与350安装manifest匹配。本任务未启动/重试/回退350，不把它归于本次349。09:09再次只读确认默认CI-only无部署stage、canonical SHA不变。当前线上为1.16.62而非1.16.61，本次优化仍包含在内；证据later-release-observation.json及根精简发布记录保留观察时间与归属。
