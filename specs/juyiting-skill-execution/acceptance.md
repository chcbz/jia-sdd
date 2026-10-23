# 验收矩阵

状态：全部业务用例 NOT_RUN。本轮的文档/JSON结构检查不作为应用验收。

| ID | 场景 | 必须观察到的事实 |
|---|---|---|
| A01 | 新建办事任务，真正上传一张新PNG | 非“从已有资料选取”；task link/file版本/hash绑定；文件名不泄露识别答案 |
| A02 | 识别该图可见标记/颜色/对象 | 公共资料载体/分析技能的真实输入与hash一致，描述匹配；不能只凭文件名作答 |
| A03 | 修改同一上传图指定元素 | EXECUTE_SKILL→正确包/版本→真实编辑调用；输出hash、尺寸、保留/修改区域经查看验证 |
| A04 | 再修改刚生成成果 | 精确producer/output来源与replaces；其余交付不丢失 |
| A05 | 后续消息不重复勾选资料 | TASK_DEFAULT目录含有效任务资料，不读取无关个人/历史文件 |
| A06 | EXPLICIT/NONE/澄清继承 | 范围正确，临时资料不无限继承；超现行数量明确选择而不静默截断 |
| A07 | 林冲/吴用分别测能力 | 安装、视觉、编辑工具状态各自真实；未就绪明确原因，不因角色名伪报 |
| A08 | 安装新skill | 任务启动/回执/普通议事不变；未知平台协议仍拒绝 |
| A09 | costInfo缺失/UNKNOWN/FREE/METERED | 缺失被规范成UNKNOWN；不查余额/consent、不冻结、不预扣；未知不显示免费 |
| A10 | 技能包购买与悬赏回归 | 不因取消运行费用审批改变既有交易/结算 |
| A11 | source/manifest/参数伪造 | 越权资料404；不匹配digest/版本409；错误参数400；无Provider请求 |
| A12 | 同key同输入/不同输入 | 前者同执行同child回放；后者409；无额外副作用 |
| A13 | 并发effect START | 单一NEW；其他读原记录；跨Runtime/会话fence生效 |
| A14 | START后崩溃、HTTP结果丢失 | 无幂等或查询能力时UNKNOWN，不直接二次生成 |
| A15 | 已有Provider jobId恢复 | 只查询已有job，不能新建任务；模拟异步视频adapter即可，不需付费视频实跑 |
| A16 | 上传/commit/归档分别失败 | 重传同outputId/hash、读回同manifest；不重新生成；界面状态如实 |
| A17 | 撤销、任务转派、session换代 | 新资料读取/副作用被拒绝；已发出的外部结果按真实情况报告 |
| A18 | 路径逃逸/恶意包/网络 | 包摘要校验、无shell拼接、无宿主token、输入只读，未批准外网无法访问 |
| A19 | PDF交付 | 可解析页数/内容，与manifest对应；走统一索引/下载 |
| A20 | XLSX交付 | 可打开、单元格/结构正确；接入提交不修改核心任务/授权/成果代码 |
| A21 | 不支持预览的MIME | 文件卡片与安全下载；不inline HTML/SVG，不以扩展名冒充真实格式 |
| A22 | 索引延迟 | execution定向结果不等全历史；登记耗时独立记录，无SLO拒绝/强制deadline |
| A23 | SQL约束/事务 | 主附属原子、精确scope、phase CAS；SQL NULL不绕过历史协议校验 |
| A24 | 历史记录/新协议切换 | 原摘要/证据不变，旧写入口关闭，旧任务按当前Owner/assignment合法升级 |
| A25 | 重启回读 | 生效provider binding/安装摘要/技能版本一致，价格变化不重写旧执行快照 |

## 证据组成

每次验收保存 source commit/tree、Runtime制品hash、技能包hash、输入file/version/hash、execution/request/step/run/output/manifest、真实HTTP/事件回执、截图与产物。无token/credential/session secret。价格未知如实记录。

第一层：跨Java/JS/Web共享的纯协议正反fixture；第二层：真实服务/HTTP/DB事务与Runtime故障注入；第三层：浏览器真实上传识图编辑；第四层：同批不可变制品在线验收。每层证据不可互相冒充。

前端正式证据仅Flow4403172精确commit；本地浏览器仅诊断。后端按项目本地固定源码/Gradle编排/validateLayering。价格信息展示测试不需要实际收费。外部paid调用只在实际执行验收阶段发生，本设计未发起。

## 轻量与扩展性测量

记录新增核心文件/配置数量、部署单元数（目标不新增）、技能发现/资料解析/Provider/提交/索引各段耗时、加载技能上下文大小、第三技能接入diff。不设没有实测依据的硬时限，不预先声称提升比例。

## SE-2新增必须覆盖项（2026-10-13历史初始状态；现状见文末）

| ID | 场景 | 必须观察到的事实 |
|---|---|---|
| A26 | 只返回data的分析技能 | RESULT_COMMITTED/COMPLETE真实闭环，零output/asset伪造；结果可读 |
| A27 | 原生模型直接看图 | 实际图片载体/回执绑定；不强制额外识别子任务；交付证据不冒充理解正确 |
| A28 | 普通SKILL.md说明包 | 不强制执行manifest；仍可安装使用，不被错误暴露为可执行动作 |
| A29 | 费用说明变更 | 不重打包/重发应用，不失效在途执行；原费用快照不改；未知不拒绝 |
| A30 | 新包维护发布 | 使用同runner、不改应用制品；package digest正确，普通Agent无发布权；seed不回退指针 |
| A31 | 技能升级并有在途执行 | 旧执行继续使用固定旧版本；安全撤销明确区别于正常升级 |
| A32 | 分析→生成 | EXECUTION_RESULT引用有scope/digest/provenance；无额外工作流引擎，拒绝未完成/越权引用 |
| A33 | 自动化边界 | 自动调用已安装技能；不自动购买安装/换Agent/换账号；没有费用审批弹窗 |
| A34 | Java/JS标准schema | 同方言和正反语料一致；外部ref/类型强转/隐式默认值不生效 |

## 2026-10-13 第一层协议证据（不重标应用验收）

53组Java/JS共享manifest/参数语料接受拒绝一致；Java56、Runtime172 PASS，后端分层PASS。固定source/tree与字节摘要见 evidence/implementation-20261013/proof.json。A34的纯codec/schema部分和A18/A28的Runtime安装局部已定向验证；尚未接完整HTTP/DB/技能目录、正式前端或线上场景，A01–A34整体不因此标PASS。

## 2026-10-16 交付核验收口（核验发生于2026-10-15）

固定发布源码见integration.yaml；原A01–A34条件保留，不批量改为PASS。

| 已实际执行范围 | 结果 |
| --- | --- |
| API固定本地构建/分层/制品 | 362 tests，0 failure/error/skip；API1.16.5已安装 |
| Runtime全套回归/制品 | engine985 PASS/10skip，host221 PASS/1skip；Runtime1.2.7已安装 |
| Web正式发布 | Flow4403172/213，1.16.1；本次末轮未改前端源码 |
| 原任务459上传图片及形状/颜色/位置识别 | PASS（原图固定版本及摘要，未新建任务） |
| 原图字符识别 | FAIL：Q7Z5两次误读0725；复验未提示正确字符 |
| image-edit实际调用、归档、页面下载 | PASS；RESULT_COMMITTED，PNG953064字节，与manifest摘要相同 |
| 修改质量 | 三角形蓝→黄，其他图形/文字/相对布局保留；尺寸800×600→1448×1086，有轻微纹理，不是像素级无损 |

**总结果PARTIAL_NOT_FULL_ACCEPTANCE**。不能将请求完成、构建成功或图片下载通过写成文字识别通过；PDF/Excel/视频、多技能及其他负例未在本轮线上重验。费用UNKNOWN不是免费，无重复安装/购买/改图重试。

证据原字节副本及路径摘要见[evidence/release-20261015/source-index.json](evidence/release-20261015/source-index.json)；现行知识入口为[聚义厅整体SDD](../../docs/knowledge-base/06-juyiting-end-to-end.md#image-skill-contract)。发布日志和不可变制品留原位置，不因临时脚本清理删除。

## 上一版成果来源的局部复核（2026-10-23）

固定API `041548f601385a3463fbba06b929991371d93d9c`，仅补A04/A05的来源部分，不将来源单测代替完整改稿/替换/生产验收。

- `ChatRetainedOutputSourcesTest`：有效来源合并/去重、NONE/EXPLICIT、原来源上限、未就绪拒绝、真实resolve的输入SHA/载体/能力目录、多个输出按producer/output/SHA映射。
- `ChatRetainedOutputAdmissionTest`：发现来源在冻结之前，冻结映射入dispatch，失败无新admission/dispatch，原key重放不重新发现。
- `JuyitingWorkflowMySqlTest.retainedOutputLookupRequiresExactLiveOwnerAndCommittedLineage`：现行自有MySQL8临时库，精确owner/tenant/client/task/generation/target、SHA、执行状态、删除和歧义；不能用默认跳过的外部MySQL套件代替。
- Runtime1.2.8现行消费者：关联随完整facts透传，篡改后contextHash校验拒绝；不修改Runtime协议。
- 生产仍待本次API发布后，用ziyue/吴用及带可辨识细节的图核验第二轮inputReceipt SHA=第一轮输出SHA、预览和最终验收。PDF、精确尺寸、517历史状态不在本轮。实绩以[handoff](../../docs/implementation/handoffs/PREVIOUS-OUTPUT-REVISION-20261023.md)及同Run证据为准。

正式CI结果：Flow5260799/248 SUCCESS，3047项中2921通过、126跳过、0失败/错误；本节新增10项单测和1项真实MySQL查询用例均实际执行通过。validateLayering/fresh bootJar通过；Runtime消费者2项轻量检查通过。配置已恢复，尚未部署；详见[证据摘要](evidence/previous-output-revision-20261023/README.md)。

### 后续授权发布及生产复核（2026-10-23）

Flow5260799/249 SUCCESS，API1.16.31/041548f6同Run制品安装与health/readiness通过，测试计数同上且本次11项均实际执行。当前不是“未部署”，也不是完整验收：ziyue/吴用新事项519上传/预览/指派成功，但首轮识图被Runtime的`CODEX_APP_SERVER_CONFIGURED_EXECUTABLE_DRIFT`拒绝。共享Codex已为0.164.0，Runtime仍绑定0.161.0测量且没有0.164.0合同。多轮识图、生图、改图、逐轮SHA及最终验收仍NOT_VERIFIED；不因API上线重标通过。详见[发布与阻塞证据](evidence/previous-output-release-20261023/README.md)。

### Codex门禁取消候选（2026-10-23后续，未部署）

isp-install develop cbc1050/Runtime1.2.9已取消版本/schema静态门禁。未知/缺失版本不拦截、源文件与快照篡改仍拒绝、租户/主体授权及typed解析定向测试通过；真实0.164.0空白HOME的无模型初始化1/1通过。完整隔离probe未通过Provider TLS阶段，Flow27/28因缓存日志污染checkout在测试前失败，改用固定commit干净worktree后的Flow29成功（352通过、2项opt-in native跳过）；不能把CI通过当完整业务通过，多轮识图/生图/改图及519闭合仍待验证。后续Run与最终状态以[交接](../../docs/implementation/handoffs/RUNTIME-NO-VERSION-GATE-20261023.md)为准，不改写先前生产阻塞证据。

### 取消门禁发布补记（2026-10-23 21:42）

Runtime1.2.9由Flow5264702/30同Run测试/打包/安装，352通过、0失败、2 opt-in跳过；部署71709927成功，93项源文件/实际PID/三通道ACK通过，配置与8条恢复记录未改。旧carrier证据失效导致吴用识图暂不可用，当前进行真实重测，不将通道PASS等同图片业务PASS。参见[本次发布证据](evidence/runtime-no-version-gate-20261023/release-flow30.json)。

### 生产浏览器回归及阻塞（2026-10-23 22:39）

新carrier 9/9真实模型PASS、当前安装loader contractReady=true；Flow31仅配置启用成功。ziyue/吴用新任务520两轮识图PASS，精确输入SHA一致。转改图后跨账号revision入口技能包owner解析错误，REVIEW_REQUESTED持续SourceUnavailable，无子请求；这是未修复API缺陷，不是Runtime版本门禁，也不是测试浏览器写保护失败。多轮生图/改图及图片验收仍未通过，见[business-task520.json](evidence/runtime-no-version-gate-20261023/business-task520.json)。

## 跨账号成果续办修复：正式CI已通过，生产待验（2026-10-24）

详见[证据](evidence/revision-authority-20261023/README.md)。API b86d8cf4、Flow5260799/252，2962通过/126跳过/0失败；本次8组定向93/93、其中真实MySQL36/36。覆盖原grant解析执行方、权限永久失败回执、暂态恢复、事务回滚、重复投递与既有来源映射；没有取消ACL/幂等/锁。未部署，不重标原图编辑/上一版多轮输入/正式图片验收为通过；PDF仍按用户要求排除。
