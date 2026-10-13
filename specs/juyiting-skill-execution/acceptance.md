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

## SE-2新增必须覆盖项（均NOT_RUN）

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
