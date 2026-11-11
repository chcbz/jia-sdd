# HALL-PROTOCOL-CONVERGENCE-20261009 旧协议收敛

- Owner: hall-protocol-owner，同一 Owner 实现/自检，不新增 Reviewer。
- 用户目标：1小时内完成；首次时钟2026-10-09 20:09:03 +08:00，目标21:09前；实际结果据实记录，不以时间跳过必要验证。
- 目标：聚义厅发送仅当前durable协议，移除能力失败时旧payload回退、旧取消入口及UI接线，同步测试。
- 非目标：删除当前/stream、普通文本流、SSE/poll恢复、身份/ACL/幂等/事务/锁；不改后端、不部署、不重启。
- 已读：/home/isp/wsps/cyf/AGENTS.md、ops/orchestration/README.md、项目入口、相关技能；项目新前端Flow/后端本地规则优先。
- web worktree: /home/isp/wsps/cyf-worktrees/hall-protocol-convergence-20261009；branch codex/hall-protocol-convergence-20261009。
- web base/local HEAD/远端develop：3e9b0aff365c25faab524e905b7c2f1aff53c3f1；tree a69de0ca2698a7e3c5d33c7e7f63c32689640cdd；2026-10-09 20:09 +08:00 ls-remote核对。tracked干净，原有untracked不操作。
- api只读契约基线：1e9111028fbdff1ae5452f64aec843e85e81ad59；tree 0416b722d735c58af4653892b6ee269e8f9d1498，远端同。ChatController capabilities声明schema2；relay当前为durable admit，/stream不是废弃入口。
- 活动ledger已查询；无owned_paths映射不能宣称无冲突；合入前再次核对develop。线上本轮未查询，不将历史版本当当前证据。
- 最早定向验证：node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --exit --timeout 10000 tests/juyiting-codex-fast-deliberation.test.js tests/juyiting-hall-conversation.test.js tests/juyiting-component-behavior.test.js。
- 验收：失败不降级/不丢草稿、稳定requestId及幂等、重复发送锁、身份/作用域隔离、当前cancel CAS、断线仅GET恢复；相关组件/语音/悬赏回归。
- 正式验证：固定新commit，复用Flow4403172且实时核查无部署配置；本机仅定向诊断，不生产打包。证据目录docs/implementation/evidence/hall-protocol-convergence-20261009。

## 实施/诊断
- 20:14首轮定向210通过/13失败，归因为旧测试mock未声明当前capability及以transport-open推断忙碌。当前durable合同测试通过；已经编排fail记录，未重试同输入。
- 20:17迁移fixture后232通过/1失败；13项旧fixture问题已解决。剩余失败揭示只轮询消息历史不足以更新durable请求终态，而非能力mock问题。保留测试原有“新最终回话后解除等待”验收，不删除断言。
- 针对真实恢复缺口：复用既有2秒poll与同request GET/去重/身份guard，先读请求再读消息；不新增timer或POST。发送入口检查durableBusy，未知请求无conversationId时也不能再次POST；旧payload/旧cancel入口删除。
- 能力失败或不支持当前契约时保留草稿/metadata，不乐观插入消息，返回false、明确反馈且下次可重试能力检查；没有生产mock例外。当前普通文本、SSE/poll、CAS取消、身份切换仍保留。
- 扩大到所有useHallConversation直接消费者及面板/草稿/取消展示：538 passing（最终候选21秒），exit0；`targeted-candidate.log`与`targeted-command.txt`。已有Vue测试桩warning保留，不是零warning或线上视觉验收。
- Owner自检：身份/作用域guard和durable cancel CAS原逻辑保留；能力失败重试不发旧POST；POST未知恢复后追加guard避免身份切换污染新消息；同request readback过期不替换新请求；未知状态阻止重复POST。
- 最终Web候选e3afb42dc69272f43699c2c423b06da7539f0671，tree f5c93a7329ee127291708ca264c1d991c38a2542。13文件+156/-115；业务源码6文件+35/-83（净减48行），增加的是当前协议fixture和失败/恢复行为回归。
- 20:20实时核对Flow配置SHA256为719b28019ba51985a11a60dd2af99ed3a336d4de760004301dd0c2336e2a65a3，仍仅CI/build/upload/scan；唯一flow-deploy文本是打包installer helper，不执行部署。配置未写入。
- 自检后fast-forward合入develop并push；正式验证仍待本轮精确Run，未以538本机诊断代替Flow，也不复用上一任务Run190。
- 20:22及20:23 push后两次只读查询无自动新Run；按既有分页限制说明复用官方SDK读取全部190个历史Run，确认无活动前端Run及配置未变，固定context后单次start。20:23:07 +08:00明确返回Run191；不改配置、不取消其他Run。context/result保留本任务目录。

## 正式验证与收口

- **2026-10-09 20:26:15 +08:00**查询Flow4403172 Run191为SUCCESS，build531697890和scan531697891均SUCCESS。release profile正式2795 passing、2 pending、0 failing；Vite生产构建11.38秒。
- 实际checkout marker与producer的pipeline/run/commit均对应e3afb42dc69272f43699c2c423b06da7539f0671；本地HEAD、固定tree、再次ls-remote的develop一致。具体核对时间及各证据SHA256见`verification-summary.json`。
- CLI日志tail100000显示outputTruncated=true，已保留为`run191-tail-log.json`，不当完整日志。只读SDK获取同job全量、复用原redact后保存`run191-complete-log.json`：119820字符，more=false、outputTruncated=false；未改写内容、未再次启动Flow。
- 汇总脚本首次使用Python新版本的subprocess `text`参数在本机3.6失败，改为兼容的`universal_newlines`后完成只读核对；不是应用/Flow失败，没有重跑应用测试。
- **开发与正式验证完成，未发布**。无后端改动、无本机生产打包、无配置改写/部署/重启，不声称生产版本变化。归档下载/制品digest安装核验、线上业务验收、assets/all专项本轮未做；以后版本发布须另按同批制品链执行。
- 稳定知识局部回写既有05前端架构和06聚义厅专题（核对日期、commit、范围均明确）；历史基线不整体覆盖。本轮仅会话发送协议及取消接线收敛，不宣称全仓历史API/全部其他旧协议已删除。
- 时间观察：20:09开始定位，20:13注册隔离worktree，20:14实现后首轮诊断暴露旧fixture，20:17暴露并修复原durable polling缺口，20:22完成538项定向、自检/合入/push；20:23单次启动正式Flow，20:26成功，随后证据/文档收口。开发与云端等待分别记录，不外推长期提效比例或冷构建时限。
- 20:28:03 +08:00经原编排器accepted并发completed通知；从本轮首次时钟到验收约19分钟，在用户1小时窗口内。根仓仅提交本任务台账/handoff/证据/稳定知识及已验证web gitlink；其他untracked与API不操作。

## 2026-10-11 厅内议事首轮只读分析接续

用户新要求“开始处理厅内议事问题，先分析”，Main只读分析，无代码/生产变更。当前Web线上21ded98/1.14.5，local/remote13c1cb1（新增密议预填修复未上线）；API local/remote/安装33e2344a/1.14.3。目标为public连续对话、拒绝反馈与点名路由，不扩多人广播/事项创建。原2026-10-09验证仅其当时覆盖范围，不作为本轮通过证据。

实际Vue函数+合成API已复现：业务终态但POST流不结束时隐藏发送token阻止第二问；明确SSE拒绝被会话引用分支吞掉留下SUBMITTING；public点名chip与真实target脱节。已用已部署commit的会话源码重复诊断，未调用线上Provider。详见 `docs/implementation/HALL-DISCUSSION-ANALYSIS-20261011.md`，证据 `/var/tmp/cyf-hall-discussion-analysis-20261011-mnhtZD`。下一动作：向用户说明已复现范围及最小修复顺序；本轮不将分析授权当成实现/发布授权。

### 2026-10-11 15:56 详设保存与图片证据核查

用户要求将连续问答方案写入详设，并询问其他问题/图片生成是否跑通。已保存 `docs/implementation/HALL-DISCUSSION-ROUND-CLOSEOUT-DESIGN-20261011.md`（待实施）：现有表字段、后端request有限流/订阅竞态、前端session收尾/迟到隔离、回归与≤30分钟计划切片。没有修改业务代码、生成图片或发布。

历史10月7日真实蓝鸟生成/预览/保存/同字节下载通过；随后混合文字与图片两独立根的改单项/验收未通过。当前Web1.14.5/API1.14.3/统一Runtime没有本次新版完整图片验收，不把历史证据重标当前成功；不恢复已取消task424，不将历史兼容/多根恢复作为用户新功能前置。详设第8节记录后续最小新流程验证范围及授权边界。
