# 事项详情状态区收敛（2026-10-26）

- Owner：当前聊天；用户授权实施，不部署。目标：成功状态不显示黄色恢复区；准备/未知/失败融入进展，历史与技术信息折叠，查询/原意图恢复不改语义。不改API/Runtime/扣费/权限。
- 根/Web规则和编排索引已读取；接口基线 api/docs/interface-standard.md v1.4（2026-10-24），只消费原字段。
- 远端develop于本轮查询为8cdf33af185ae466f048f8ec4c814d2e873fe19b；线上本聊天上次核验1.16.56/fe53b812/Flow336，不据远端变动推断线上。
- 原Web checkout旧HEAD且原型脏，保留不覆盖；唯一隔离工作区 `.worktrees/matter-status-web`，branch `codex/matter-status-ui`，基线8cdf33a。修改原型时只定向追加本任务脚本/样式引用和规格，不覆盖他人原型。
- 先更新唯一原型 scenario=matter-status#detail，PC/移动状态覆盖；再修改BountyPanel展示及真实SFC测试。最早验证：成功无警告、未知查询不自动重发、失败原因、终态/任务切换隔离；完整应用测试构建走Flow4403172 CI-only，单Run<=600秒。
- 私有证据 `/home/isp/state/juyiting-matter-status-20261026/`。定位/实现分项耗时未采集。

## 实现和轻量验证

- 原型已在唯一目录加入matter-status场景；1440/390/320宽度×六种状态18项通过，0脚本异常，无横向溢出。沿用现有18786服务；原型为离线示例，不进行业务提交。截图/检查在私有证据目录。
- 产品BountyPanel仅重排展示：成功/历史折叠，准备中性，未知黄色，失败真实错误；保留原查询和UNKNOWN显式恢复事件/原任务参数。终态不恢复，身份切换原逻辑关闭详情。非embedded视图仍保留同一恢复能力。
- 现有发送投影无资料名称，显示数量而非新增查询或猜配；好汉名称仅同ID读取。缺资料事实显示待核对而非假定0份。新增未知状态兼容展示只提供查询，不猜测恢复语义。
- 新增真实SFC状态/按钮/折叠/隔离/转义/忙碌/终态回归，旧mixed-material测试移到新选择器，保留固定版本与事件断言。首次新增测试误以为身份切换仍保留详情，实际原组件关闭整个详情；已修正测试并确认该更强隔离，不改原产品行为。原型首次检查的加载等待和选择器转义错误已修正，最终18项通过；失败日志不作为通过证据。

## Flow首轮及兼容修正

- 已合入Web develop `3b237ff22b2d86433a9d0932ee52ff23db71d0a9`，tree `967570f7bba474927d15de5b143c480e9582b492`。本机126项定向回归通过，BountyPanel lint相较基线15项既有问题无新增；未本机生产构建。
- Flow4403172/338 FAIL：3415通过、2失败、2 pending；失败为旧测试仍引用point-and-start-error类、精确旧matter-advice-card的v-if文本。已将断言改为实际折叠详情/新显示条件，保留错误内容、警告状态与原讨论路由断言，没有删除测试。日志web338-build-log.json保留。控制面约114秒观测失败，未超600秒。
- 源码复核增加SENDING/CONFIRMED正常中间态中性展示，COST_CONSENT_PENDING说明旧费用确认边界，不新增恢复权限；补充原型/规格/组件测试。相关兼容定向91项通过，后续完整Flow重新固定候选，不复用失败Run结果。

## 最终收口（2026-10-26，未部署）

- 最终Web develop已push/readback：`2f90a708c3fece1d6e7872e9a5589a4cb6193a07`，tree `99fed1d93158dca2f2291780dcddbda9393bf4d6`。只包含本任务源码、原型/规格及回归修正；API/Runtime未改。
- Flow4403172/339 **SUCCESS**，**3420通过、0失败、2既有pending**，465 suites；代码扫描、完整release profile测试、Vite构建、制品上传成功。平台创建至终态126秒，控制面最终观测约142秒，小于600秒，未取消/重试他人Run。使用现有CI-only配置，本任务未写流水线配置，无部署作业。
- 同Run制品已核验源码commit/tree、release manifest和Mocha报告；SHA-256 `219ab71bb3a8380abbb63806f8ebd58679d531c279036f44ed665e48e4e4549e`，109548143字节。完整日志/制品位于私有证据目录，摘要在本目录matter-status-20261026/verification.json。
- 最终原型按工作区固定候选资源拦截验证：1440/390/320三宽度×九状态共27项通过、无脚本异常/横向溢出，技术详情默认关闭、按钮按状态出现。保留截图；预览复用原服务，已发出桌面浏览器打开matter-status场景请求（回执queued，不宣称桌面已实际渲染）。实际浏览器检查为独占Chromium。
- 最终BountyPanel lint与基线相同15项已有问题，无新增，不顺手改其他行。定向126项及兼容修正91项的检查范围/历史见私有日志，正式最终以Flow339为准。
- 稳定知识回写既有juyiting-runbook；原型规格和根优化方案同步。自有Chromium退出，隔离工作区保存diff后清理，保留唯一原型预览服务及其他任务脏文件。未部署，真实登录生产会话/移动真机未验收；不得用本轮CI成功重标线上版本。

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
