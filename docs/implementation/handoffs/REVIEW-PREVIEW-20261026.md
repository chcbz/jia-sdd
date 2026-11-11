# 验收选择弹窗条目内预览（2026-10-26）

- Owner当前聊天；用户要求解决“选择成果并验收”中预览集中在列表底部、无法辨识所属成果。仅实施和验证，不部署。
- 目标：每条成果下展开预览，一次一个；按钮收起/展开与无障碍状态、预览标题含序号/名称；保持多选、历史版本、固定身份、原确认/幂等，防异步旧结果显示到新条目。不改API/Runtime或整批旧验收语义。
- 基线：本轮远端develop `2f90a708c3fece1d6e7872e9a5589a4cb6193a07`，主Web旧checkout及原型脏文件不覆盖。唯一隔离工作区`.worktrees/review-preview-web`、branch `codex/review-inline-preview`；根/Web AGENTS、现有编排索引/Flow入口已读，接口规范api/docs/interface-standard.md v1.4（2026-10-24）。
- 原型先行：唯一prototypes/juyiting/现有delivery-entry/image-turn验收弹窗，增加两稿定位演示；先验证PC/手机再对照产品。最早测试为真实Dialog DOM展开/切换/关闭/选择不变，附加异步串图回归。完整构建/应用测试走Flow4403172 CI-only，600秒总时限。
- 私有证据`/home/isp/state/juyiting-review-preview-20261026/`；耗时分项未采集。线上版本本次未查询，不把远端或之前Flow339当上线。

## 原型及实现验证

- 唯一原型delivery-entry已有验收窗口改为条目内展开，新增review-preview两稿场景；本地原型只定向改相关函数/样式和资源版本，不覆盖其他脏内容。独占Chromium固定候选资源验证1440/390/320宽度：展开第一项、切换第二项、收起、勾选保持独立共12项通过，无脚本异常或横向溢出。首次导航未完成时测试取不到按钮，浏览器仍about:blank；重新导航后完整12项通过。截图保留私有目录。
- 产品HallDeliveryReviewDialog只改变selectionMode：带原item的scoped slot在被展开的li内渲染，一次一项，标题和aria-expanded/controls明确所属。整批旧验收分支未改。
- JuyiHall按原selectionKey与sha绑定预览内容，开始即显示该项加载状态；收起/关闭/身份上下文改变清空。缺加载器/失败明确反馈。BountyExecutionOutputs原固定输出loader加最新预览序号，较早异步响应不覆盖较新的选择；任务epoch仍生效。没有新增查询/提交/验收接口或权限变化。
- 真实Dialog DOM及原源码预览路由/异步序号定向20项通过；JuyiHall真实挂载、验收与完成刷新相关135项通过。首次本机集成命令遗漏现有tsx loader导致before hook解析resizePolicy.ts失败，改用项目原node --import tsx入口后通过；未改产品或删测试来绕过。正式全量测试和构建仍走Flow。
- 已发出浏览器打开review-preview原型请求，工具回执queued，不冒充实际桌面渲染。原型浏览器检查为自有Chromium，不操作用户生产数据。

## 最终收口（2026-10-26；未部署）

- Web develop已合入并push/readback `c660e9b4f94ef37154965a6b9c88fe36c409ef2f`，tree `433de4636b15c945dda88d1829f1eb045776fc06`。变更仅限本任务原型/规格、Dialog/JuyiHall/Gallery展示与对应测试，包含上轮事项详情源码但不部署。
- Flow4403172/340 **SUCCESS**：**3428 passing、0 failing、2既有pending**，466 suites；扫描、全量release profile测试、Vite构建及上传成功。平台创建至终态106秒；控制面观测约122秒，不超过600秒。初始UNKNOWN是回读提交尚未填充；后续只读状态和同Run制品确认候选，未重复启动。
- 同Run制品109553436字节，SHA-256 `78e0d09c698875d83f36d63d01fa0de18d95bf1788f54e4fb723cdab88160eed`；核验release.json、source-commit/tree及Mocha报告均匹配。完整私有证据目录包含启动上下文/监控/状态/日志/制品；简明记录见本目录review-preview-20261026/verification.json。
- 三个修改SFC相较固定基线无新增lint问题；未全文件格式化旧问题。原型12项与本机20+135定向测试范围见上文，不能替代真实生产登录端到端。
- 现有Flow保持CI-only，本任务没有修改流水线配置、部署、改变API/Runtime或用户业务数据。自有Chromium已退出，工作区保存diff后移除，原主工作区和其他任务脏内容保留；唯一原型预览服务继续复用。稳定行为回写runbook。

## 用户授权发布（2026-10-26）

- 用户本轮明确要求部署；Owner仍为当前聊天。发布仅Web，包含事项详情状态区与验收弹窗条目内预览；API/Runtime不变。
- 发布前线上1.16.57 / Flow4403172/337，commit 8cdf33af185ae466f048f8ec4c814d2e873fe19b。候选1.16.58，commit `3c95bfeef3826cb439c3da92ddfd82e642a507fe`，tree `93d9c9c7338ef34440a040d4d0713f3a18ba6a5f`；相较c660e9b仅三个根版本字段变更。私有index生成提交，未触碰脏主checkout。
- 复用Flow4403172同Run测试/构建/制品/部署，保留锁、摘要和备份；600秒总时限，仅监控和受控取消本任务Run。结束后恢复归属匹配的CI-only配置并核验安装文件与公网资源。证据 `/home/isp/state/juyiting-matter-preview-release-20261026/`。

## 发布完成（2026-10-26 20:58 CST）

- Web **1.16.58** / commit `3c95bfeef3826cb439c3da92ddfd82e642a507fe` / tree `93d9c9c7338ef34440a040d4d0713f3a18ba6a5f` 已通过 **Flow4403172/341 SUCCESS** 发布，两轮功能同时包含；API/Runtime未操作。
- 同Run扫描、3428测试通过（0失败、2既有pending）、构建及安装全部成功；平台创建至终态321秒，监控观测约331秒，低于600秒。启动首次UNKNOWN仅为源码回读尚未就绪，后续核对唯一Run源码一致，未重发。
- 部署单71839447：1/1批次，主机Success、client healthy。制品109555073字节，SHA-256 `be2d2ca23be3081f3bee92cf68c2befd7e9f6591b386065c6c8212c2ba479301`；同Run manifest/source commit/tree/Mocha匹配。612个安装文件逐个摘要一致，公网首页、聚义厅及入口/相关懒加载资源共9项摘要一致。未执行真实登录业务端到端或移动真机验收。
- 已受控恢复原CI-only配置并readback APPLIED，未改变他人Run。备份 `/home/isp/baks/cyf-web-juyiting-matter-preview-release-20261026` 保留原入口及record；旧hashed资源按原安装器策略保留，恢复须使用受控安装入口，不手工覆盖状态。完整证据在发布私有目录；精简记录在 `review-preview-20261026/release-*.json`。
- 上述“未部署”描述为实施时历史状态，本节补充本次实际上线事实；本轮仅版本字段提交并push，主脏工作区及其他任务内容未覆盖，无新worktree或本机生产构建。
