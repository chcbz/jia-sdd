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
