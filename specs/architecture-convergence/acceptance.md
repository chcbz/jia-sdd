# 验收、关键回归与当前证据

## 1. 当前真实状态

- 文档/静态盘点：已完成，具体检查结果见[evidence/document-check.json](evidence/document-check.json)。
- 应用代码变更：B0–B4已进入候选，尚未整体交付。边界collector合成夹具/生产源码解析通过；正式validateLayering结果待最后API Run核对。
- 新候选Flow：Web319及Runtime59成功；API315/316/317失败原因与修复已留证，318测试/构建通过但export失败；319验证中。安装、生产回归未执行。
- 原task526/529生图/识图/改图/验收和短连接中断是历史业务证据，不用来给本包未来候选盖PASS。
- 本包不新增PDF验收，沿用用户此前暂不验PDF的边界。

## 九小时交付判定（2026-10-25用户更新）

用户2026-10-26最新指令覆盖旧排程，硬截止改为北京时间2026-10-26 09:00；00:18:52已开始B0核对。全部AC条款、必要正式测试、集成和获授权发布/业务验收均须有真实证据；未验、失败、跳过或仅部分完成不能替代完成。PDF继续暂不验。截止未完成则整体废弃，按tasks.md第1节安全撤回本任务改动并保留证据，不自动延期。发布授权仍独立核对，缺失时不发布也不宣称全部完成。

## 2. 规格到实现到验证

| 条款 | 行为/结构断言 | 关键入口 | 必须观察 | 当前 |
|---|---|---|---|---|
| AC-01 | 短断线≠永久拒绝，未知reason不授权 | TaskSkillPolicyServiceTest；ChatActionDispatchReviewGuardTest；既有skill用例 | 不写永久Rejected；恢复后同action一个child；真实拒绝仍失败 | pending |
| AC-02 | 相同标识不同owner/版本不串用；读取期间撤销生效 | 既有TaskLink mapper/service；TaskLinkedMaterialReader*（拟） | 精确SQL范围、真实DB可见性、hash/bytes不变；无Provider启动 | pending |
| AC-03 | GET合并、末尾事件读回、旧scope响应丢弃 | juyiting-hall-conversation.test.js | 同一scope并发只一次读；读期间final发生后有补读；reset后旧响应无写入 | pending |
| AC-04 | 部分失败不等于lane不可用 | skill-conversation.test.mjs / agent-client.test.mjs | report及日志分层；shared错误throw；effect调用次数不新增 | pending |
| AC-05 | 不能新增跨域实现/mapper、身份隐式输入或已迁走SQL | validateLayering + 精确例外 + 新模块ESLint限制 | 新违规报路径/符号，旧债不扩；两处SQL确实删除 | pending |
| AC-06 | 规范可取得、selector真实运行、无越界文件 | Git差异、integration、Flow报告 | 精确SHA、执行数/skip/失败、同Run制品；文档与候选一致 | pending |

仅增加本次风险缺口用例；不新增纯“超过旧数量上限”测试，不扩到全地图/所有格式/新Provider。

## 3. 正式测试选择，避免“文件存在＝执行过”

### API

先读取候选build.gradle，再通过现有编排/Flow入口设置对应参数，不在本机执行这些重任务。

建议加入现有Flow候选selector（不是直接在本机复制运行）：

```text
:agent:jia-agent-service:test
  --tests cn.jia.agent.skill.TaskSkillPolicyServiceTest
  --tests cn.jia.agent.skill.SkillExecutionServiceTest
  --tests cn.jia.agent.service.impl.PersonalWorkspaceTaskLinkServiceImplTest
  --tests cn.jia.agent.service.impl.TaskLinkedMaterialReaderTest
  --tests cn.jia.agent.service.impl.TaskLinkedMaterialReaderMySqlTest
:agent:jia-agent-mapper:test
  --tests cn.jia.agent.dao.PersonalWorkspaceTaskFileLinkMapperContractTest
:chat:jia-chat-service:test
  --tests cn.jia.chat.service.ChatActionCapabilityServiceTest
  --tests cn.jia.chat.service.ChatActionDispatchReviewGuardTest
validateLayering
```

拟新增测试尚不存在，不能现在声称selector有效。B0固定候选时核对默认test源集是否仍编译、已有fixture要求及是否需要复用现有已包含该文件的任务；**不得新增隔离sourceSet掩盖原编译失败**。若必要文件迁移到既有sourceSet，连任务filter一起写入本表。

特别注意：`skillManagementContract`有自己的include/filter，不自动覆盖所有SkillExecution测试；`nativeSkillResultRegression`最终filter只选一个native结果用例，不能因为compileClasspath含另一个test就声称它运行过。

真实MySQL用例要核对非skip和数据库实际创建/使用；不得靠环境变量缺失跳过后写PASS。结果摘要要有选择器、发现数、执行数、成功/失败/skip；测试重复覆盖按真实风险裁剪，不删除原ACL/资金/幂等保护。

### Web

复用Flow4403172现有release profile；本次重点是：
- `tests/juyiting-hall-conversation.test.js`
- `tests/juyiting-typed-deliberation-interaction.test.js`
- `tests/juyiting-typed-deliberation-page-routing.test.js`
- `tests/juyiting-selected-output-review.test.js`
- `tests/personal-workspace-task-material-links.test.js`

这些`.test.js`在当前`.mocharc.json`的spec范围内，但仍要检查实际报告。`.mjs`文件不自动被上述glob覆盖，不能遗漏而声称“全部契约测试通过”。不为本任务运行无关assets性能套件。

### Runtime

在现有Runtime Flow的固定源码目录，以现有测试入口执行对应`conf/codex-ws-agent/test/skill-conversation.test.mjs`和`agent-client.test.mjs`，并保留既有effect/store关键测试。完整组合负载按Flow策略安排；不把正式打包搬回本机。

## 4. 统一业务回归（未来已授权候选上线后）

测试账号使用用户已授权的`ziyue`，指派“吴用”；登录密码从已授权凭据来源使用，不写入规格/日志。跨账号负例使用已授权另一测试主体；未取得第二主体会话则记未验，不能仅改请求里的owner伪造登录。

| 步骤 | 观察点 |
|---|---|
| 创建事项并附资料→选择承办→进入议事 | 页面、指派、任务/会话绑定正确；无多余新入口 |
| 上传/选择一张图片→识图 | 上传后可见且选中、预览正确；Provider取得该版本而非同名/最新文件 |
| 生图→引用修改→再次识图 | 每步独立request/effect，修改来源明确；不重复生成、不因旧历史空取消卡住 |
| PC和移动端预览→选择成果→正式验收 | 与既有原型一致，验收绑定实际选中版本/摘要；task完成而非仅消息完成 |
| 议事读回期间切会话/切身份再返回 | 旧响应不污染新scope；无空列表/错误终态回退 |
| 对同资料执行未授权读取 | 服务端拒绝且不泄露内容，另一用户的结果不出现在目录 |
| 受控短断连/重连 | 同execution续行或明确待核对；不产生新Provider副作用；PARTIAL/整体故障日志可区分 |

生产断连实验需明确目标/授权/恢复，不因为本表存在就停止全部Agent或用管理员权限绕开。无法安全注入时使用隔离实连环境覆盖，生产该项记待验；不复用历史task529作为新候选实测。

用截图、HTTP业务readback、原始制品SHA及任务/执行/交付记录共同证明；截图 alone 不能证明幂等或资金正确。供应商requestId/账单未核验时不得写“扣费恰好一次已证明”。

## 5. 反腐化检查（合入前）

每批必须答出并附对应证据：
1. 本次哪条spec要求了这个变化？不在allowlist的文件为何变化？
2. 同一状态/决策是否又新增了一个owner？是否只是搬出一个更大的Support类？
3. 新路径替换后，旧判断/SQL/Map是否真实删除？例外是否同步缩小？
4. 所有调用者/事件消费者是否迁移？错误码/摘要/wire是否保持？
5. 必要校验是否写明风险、条件、失败范围及关键测试？是否恢复了用户已取消的门槛？
6. 报告中是否真的执行了所声称的测试？skip和mock覆盖是否如实披露？
7. 文档能否从固定commit取到，而非仅在本机？生产部署和源码状态是否混写？

缺少答案只阻止该批标记完成，不添加生产请求门禁、不新增人工审批链。

## 6. 版本兼容/回退验收

本包不改变wire/数据库。对已固定的旧Web+新API、新Web+旧API、旧Runtime+新API、新Runtime+旧API做受影响合同核对；不要求所有应用版本完全一致。以实际组合和执行结果为准，不能因理论兼容就自动PASS。

回退不恢复旧数据库或checkpoint；确认本批无额外迁移、按已有锁/备份/安装流程切程序。当前角色、文件授权和资金事实不得随程序版本倒退。

## 7. 本轮文档检查与证据限制

`./sddw check-docs architecture-convergence`只验证导航，不验证上述Java签名、测试可运行性或业务。额外只读检查核对JSON/YAML解析、证据commit、allowlist已有/拟新增路径、空白差异。

文档导航检查不替代应用验收；实际结果追加如下，生产尚未验证。不另建日期版“最终方案”，不覆盖历史失败证据。

## 8. 实施验证记录（2026-10-26）

- **Web319**：候选`2fbab52ff621da7005016d69182be5b820947a29`，release profile发现3344条，3342通过、0失败、2条小程序入口pending。5个本期指定测试文件均出现在报告中，本期读回调度54条通过。两个pending不作为通过，非本期PC/移动浏览器行为证据。制品612个dist文件逐个匹配同Run清单；详见[evidence/web319-report-audit.json](evidence/web319-report-audit.json)、[制品摘要](evidence/web319-artifact.json)。现有整仓扫描并非零告警，不以Run成功宣称历史lint/扫描债已清零。
- **Runtime59**：候选`cc7181cdb790376b250d175377f6125c78ed03b8`，5个指定文件262通过、0失败、0跳过，覆盖局部错误报告、caller、execution store/executor与原生会话；[TAP](evidence/runtime59-tests.tap)、[制品摘要](evidence/runtime59-artifact.json)。输出为已测源码和报告，不是可安装Runtime制品；无版本升级/安装/线上验收。
- **API315**：现有CI分支精确策略拒绝本任务候选，Gradle未运行；仅增加本任务分支到原policy与flow_ci_context，未绕源码和身份约束，已有编排9条回归通过。
- **API316**：真实编译发现B2删除了仍供effectiveSelectors使用的text/number助手；恢复原方法，不扩大任务默认选择逻辑。
- **API317**：2288条发现，80跳过、1失败；失败为本次真实MySQL I/O后撤权用例。NOT_SUPPORTED之外还需处理MyBatis会话缓存；本期授权SELECT显式flushCache/useCache关闭，保留原撤权断言，候选`9be9864638`待318验证。80跳过如实保留，涵盖旧环境依赖MySQL/Redis测试，不冒充正式覆盖；本期新增MySQL两条确实执行、无skip。
- 上述都不是生产验证；AC条款整体仍待候选最终API验证、兼容/业务验收及获授权发布完成。

### API318复验

`9be98646383a6a3d55511d59faf9be0cd741303f`：385份JUnit报告，3275条发现、3111执行通过、164条旧环境条件跳过，0失败；新增真实MySQL撤权两条均通过。Gradle含validateLayering及fresh bootJar成功；Run因后置制品导出同一旧分支名单失败，故不能称Run成功或同Run制品已可交付。只补导出精确分支范围，319重新执行完整必要任务并导出，不复制318的JAR冒充319。
