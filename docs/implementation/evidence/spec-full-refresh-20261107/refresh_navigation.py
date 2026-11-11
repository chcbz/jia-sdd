from pathlib import Path
import json,hashlib,re
R=Path('/home/isp/wsps/cyf');E=R/'docs/implementation/evidence/spec-full-refresh-20261107';C=json.loads((E/'feature-contracts.json').read_text());changes=[]
def write(path,text):
 p=R/path;old=p.read_text() if p.exists() else None
 if text==old:return
 if old is not None:
  b=E/'originals'/(path+'.txt');b.parent.mkdir(parents=True,exist_ok=True)
  if not b.exists():b.write_text(old)
  assert p.read_text()==old
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
 changes.append({'path':path,'before_sha256':hashlib.sha256(old.encode()).hexdigest() if old is not None else None,'after_sha256':hashlib.sha256(text.encode()).hexdigest()})

write('specs/AGENTS.md','''# CYF规格维护规则（2026-11-07）

适用范围：本目录全部专题、子目录详设/合同/模板及参与本项目的Agent；与根AGENTS共同生效，不修改全局/其他项目。文档规则不是生产迁移/收费/发布授权。

## 唯一入口与优先级

1. 当前用户明确决定和根AGENTS；跨专题原则见 `architecture-convergence/development-principles.md`。
2. `INDEX.md`指向专题主spec，其2026-11-07现行合同说明目的、责任、流程、边界及验收；design/tasks/acceptance分别负责细则、实际改动、可观察结果。
3. 被明确指定为继任的专项合同优先于旧同范围方案：文钱包取代旧SILVER/预览报价；环境租户取代字面tenant0迁移；RB-1/原生执行取代旧runner；议事20条页级投影取代全量/逐条补查；用户最终选择保留完整最终回复。
4. 原冻结合同、schema/fixture、integration pin、测试/发布receipt、旧任务和历史会话保持原字节/来源。它们证明当时输入，不是当前版本或重新执行授权。旧日程/角色/Run命令不可直接续跑。

## 如何写清可落地的规格

- 同一责任规则只在明确Owner层维护；业务文档补该业务风险/触发条件/失败域/回归，不复制一套认证/租户/校验/DFX框架。
- 修改真实目标/非目标、流程、权威事实、输入输出/权限/状态、当前数据读取方式及必要错误语义。契约未变不强制三端修改；契约改变更新真实消费者，不新增统一审批。
- 一次验收应能找到实际入口、固定输入和可观察结果；复用已有测试，不为局部修复全仓堆防御测试。事实、推断、未知分开，未测即未测。
- 新规则写入当前正文并处理同范围旧要求，不再只在末尾追加“最新”补丁。历史记录可保留但明确日期和适用范围；无法证明被替代的业务条款不随意删除。
- 发布默认本地固定源码/独立输出/必要测试/真实批次与SHA；600秒是完整墙钟目标，不是强杀。develop合入不自动发布。不伪造云效身份，不自动启动Flow。
- 修改公共边界时检查根/组件规则、相关业务详设、模板和原型；不为文档修订伪更新应用版本、全库BASELINE或现行生产状态。
- 本目录的“2026-11-07”是规格整理版本，不是每个特性都在该日上线。具体交付沿原Owner/handoff，不新建状态台账。

## 文档验证

复用根 `./sddw check-docs` 检查现行入口。导航通过不等于源码/发布验收通过；`sddw verify/pin`只用于适合其格式的真实候选，不为了文档绿色重写历史SHA。历史证据/冻结材料保持摘要不变。
''')

intro='''# CYF规格索引（2026-11-07）

本索引覆盖全部39个专题（38个业务/架构专题及1个历史来源），另有新特性模板。**文档修订版本不等于软件版本、全部实现或线上验收。** 当前责任、业务链、边界和验收从各专题主文档开始；不按旧文件日期、任务未勾选项或历史Run推断今天的状态。

## 开发先读

- [根规则](../AGENTS.md) · [规格维护规则](AGENTS.md) · [统一性能/职责/校验/兼容/DFX约束](architecture-convergence/development-principles.md)
- [当前交互原型](../web/prototypes/juyiting/specs/prototype-spec.md) · [实现知识库](../docs/knowledge-base/README.md) · [SDD工作流](../docs/sdd-workflow.md)
- 默认本地测试、构建和受控部署；精确源码/测试/制品摘要、锁与恢复保护保留。600秒是完整墙钟目标，不因超标拒绝业务或强杀；不自动启动Flow或发布develop。

## 全量专题

表中内容为现行合同目的，不是交付状态。每个主spec已说明责任层、业务流程、边界与验收落点，并导航到原设计/任务/验收和必要继任合同。原始测试/发布状态仍查对应日期证据。

| 专题 | 现行目标 | 同范围专项合同 |
| --- | --- | --- |
'''
rows=[]
for f,c in C.items():
 detail=c.get('detail');d=f'[细则]({f}/{detail})' if detail else '主spec及design'
 rows.append(f'| [{f}]({f}/spec.md) | {c["purpose"]} | {d} |')
end='''

## 明确替代关系

| 旧口径 | 现行合同 | 不变的保护 |
| --- | --- | --- |
| 云效为默认正式前置、禁止本机重型构建 | 根AGENTS本地固定源码执行；Flow仅另获授权使用 | 身份、精确制品、互斥、恢复和真实验收 |
| SILVER/微银两、合成预览价、旧报价TTL | [文钱包与人民币成本账](agent-economy-marketplace/beta-wen-billing.md) | 资金事务、幂等、金额精度、切换授权 |
| 字面tenant0、请求/JWT决定业务tenant | [环境租户](full-tenant-gray/spec.md) | 个人owner权限、公共持久化隔离；冻结剩余不重启 |
| 按技能/Provider编排通用Runtime、旧runner执行恢复 | [RB-1](juyiting-skill-execution/responsibility-boundaries.md)及原生详设 | 执行隔离、完整性、旧事实只读、新方案恢复 |
| 全量历史、50条、逐条/ID集合补查 | [20条页级投影及连续窗口](juyiting-ui-baseline-20261006/optimization/detailed-design.md) | 游标连续性、固定成果版本、身份切换隔离 |
| 取消最终回复、流缓存拼接落库 | 保留完整最终回复；流仅实时预览 | 最终事实事务与幂等 |
| 3秒/启动预算硬终止 | 性能观测与优化目标 | 真实网络错误、传输超时、用户取消 |

## 历史与模板

- [模板](_template/spec.md)：新特性填写真实业务责任、输入输出、最小失败域和验收，不复制旧资金/调度/发布方案。
- [历史会话归类](codex-history-closeout-20261023/summary-20261107.md)和[旧路径承接映射](../docs/sdd-document-map.json)保留来源；已删除旧D2/D3/UI提案不得重新生成作为当前方案。
- `integration.yaml`原有精确pin及冻结bundle/fixture/receipt不为这次整理改写。新补推荐专题未虚构SHA；未填写表示本次没有候选绑定。
- 文档检查：`./sddw check-docs`。全量文件分类/未改证据摘要及本轮差异见[收口记录](../docs/implementation/handoffs/SPEC-FULL-REFRESH-20261107.md)。
'''
write('specs/INDEX.md',intro+'\n'.join(rows)+end)
write('specs/README.md','''# CYF规格入口

规范修订：2026-11-07。覆盖全部39个专题；文档最新不代表全部功能已实现或上线。

## 从这里开始

1. [全量专题索引](INDEX.md)：找到唯一责任专题，不并行维护第二套同义规格。
2. [统一开发约束](architecture-convergence/development-principles.md)：性能、事实归属、必要校验、兼容边界、DFX与验证口径。
3. 专题 `spec.md` → `design.md` → 实际受影响的 `tasks.md` / `acceptance.md`；专项合同以主spec明确指向为准，不默认读全部历史。
4. [当前实现知识](../docs/knowledge-base/README.md)与固定源码用于确认实现；原handoff/receipt用于确认测试、安装及业务验收，不能互相替代。

## 文档角色

| 文档 | 负责什么 | 不能当什么 |
| --- | --- | --- |
| spec/design | 当前目标、责任、流程、协议与数据细则 | 全部实现/上线证明 |
| tasks/acceptance | 实际改动范围、可观察验收及历史结果 | 自动重开所有旧待办、历史发布授权 |
| integration.yaml | 对应批次的精确候选关联 | 当前checkout/线上版本的自动跟踪器 |
| schema/fixture/冻结bundle | 具体版本协议及测试输入 | 可以静默覆盖的“旧文档” |
| 报告/日志/receipt/历史会话 | 当时输入与事实 | 今日实施步骤或新的用户授权 |

默认本地固定源码验证/构建；按真实授权安装。单Owner自检，契约变化才联动实际消费者。文档维护要求见[本目录规则](AGENTS.md)，操作流程见[SDD工作流](../docs/sdd-workflow.md)。

`./sddw check-docs`仅检查文档导航。不要为通过检查运行pin重写历史SHA；不要以批量改日期冒充全仓源码和业务复验。
''')

# Update existing current development instructions in-place, not only an appended precedence banner.
p='docs/codex-project-map.md';s=(R/p).read_text()
s=s.replace('构建/部署以 `docs/aliyun-flow-cicd-strategy.md` 为准。','构建/部署以根AGENTS的2026-11-06本地执行规则和现有 `ops/orchestration/README.md` 入口为准。')
s=s.replace('不替代前端正式Flow、整站/OAuth验收或发布授权。','不替代前端正式构建、整站/OAuth验收或发布授权。')
a=s.index('Develop is for integration and verification, not automatic deployment.')
b=s.index('## Common Search Targets',a)
s=s[:a]+'''Develop用于集成和验证，不自动部署。CYF默认在本地固定干净源码及独立输出位置串行执行必要测试、构建和打包，使用真实LOCAL来源及SHA；不编译生产安装目录，不自动启动Flow。准确来源相同且证据完整时可复用制品。

已有工具入口见 `ops/orchestration/README.md`。Gradle先读相关build.gradle并经orchestrator；Web复用现有测试/生产构建命令。保持身份、锁、备份、可恢复安装，测试/安装/健康/业务验收分别记录。600秒是完整同批墙钟目标，不是应用或本地强杀deadline。

'''+s[b:]
s=s.replace('authoritative resource-based Flow/local division and versioned release policy.','historical Flow implementation and the current local-policy override; root AGENTS governs execution.')
write(p,s)

p='docs/sdd-workflow.md';s=(R/p).read_text()
s=s.replace('`integration.yaml` contains the exact API and Web commit IDs currently checked out.','`integration.yaml` binds the exact candidate actually tested; documentation-only edits preserve existing historical pins and do not run pin against a dirty checkout.')
a=s.index('For P0 identity/ACL/transaction/migration changes,')
b=s.index('## 2026-09-14 reconciliation',a)
s=s[:a]+'''For identity/ACL/transaction/migration changes, the single Owner self-checks the actual affected boundary and recovery behavior. Do not add an independent Reviewer or repeated approval stages. Ordinary component integration goes to develop after self-check; deployment requires the actual release authorization.

CYF uses local tests, builds and packaging on fixed clean source with independent output. Preserve exact commit/tree, real LOCAL build evidence, tests and artifact SHA-256, identity, locks, backup and recoverability. Read the relevant build.gradle before Gradle and use the existing orchestrator; reuse Web test/build commands. Cloud Flow is not the default prerequisite. The 600-second local target measures the whole authorized batch including waits and acceptance; it is not a process-kill or application deadline. Record build, install, health and business acceptance separately. Production data and paid operations remain scoped to actual authorization.

'''+s[b:]
write(p,s)

# Resolve an already broken root-rule path; keep the actual database business policy unchanged.
p='AGENTS.md';s=(R/p).read_text().replace('`docs/interface-catalog/database-check-rules-20261102.md`','`api/docs/interface-catalog/database-check-rules-20261102.md`')
s+='\n## 全量规格维护（2026-11-07）\n\n- 全部专题由 `specs/INDEX.md` 导航，按 `specs/AGENTS.md` 维护；主spec/design/tasks/acceptance的现行合同与原历史证据分开。后续变更直接更新责任专题正文、实际消费者及必要验收，不再仅追加“最新”补丁，不批量改冻结schema/历史pin/receipt。\n'
write(p,s)

for p in ('api/AGENTS.md','web/AGENTS.md'):
 s=(R/p).read_text();s+='''
## 全量规格与职责收口（2026-11-07）

- 本项目现行专题入口为 `/home/isp/wsps/cyf/specs/INDEX.md`，跨专题性能/校验/兼容/DFX约束为 `/home/isp/wsps/cyf/specs/architecture-convergence/development-principles.md`；历史阶段规则不能覆盖当前明确合同。
- 只在真实责任层实施规则；契约不变的内部修复不机械联动所有组件，既有公共机制已覆盖的检查不逐调用方复制。身份/ACL、事务、幂等、完整性与必要恢复仍保留。
- 本地固定源码必要测试/构建及受控发布为默认；600秒是完整墙钟优化目标，不是强杀。规则、源码整改、安装及业务验收分别报告。
'''
 if p=='api/AGENTS.md':
  s=s.replace('请求中的租户标识不得覆盖可信身份中的租户信息。','业务租户来自后端环境配置，请求scope只作一致性准入，不得覆盖配置；账号/client身份与业务tenant分开。')
  s+='\n- SQL业务分区由既有公共持久化机制负责；后台发现/领取先分区再排序LIMIT/加锁，仅补原生SQL或独立存储实际绕过点。不因DAO无显式tenant参数机械重写全部主键接口。数据库CHECK按根规则不新增/依赖。\n'
 else:
  s+='\n- 议事消息每次接口返回20条及页级展示投影；不逐条/按ID集合二次补齐，不全量历史加载；流预览与完整最终回复分开，页面销毁/身份切换释放订阅并丢弃迟到结果。\n'
 write(p,s)

# Fill actionable templates while preserving the existing integration schema.
write('specs/_template/spec.md','''# <Feature name>

## 目标与非目标

填写用户可观察目标、当前授权范围及不做事项，不把文档完成写成已上线。

## 责任与业务流程

写出权威事实归哪个已有模块、输入→业务转换→输出；指出与相邻专题的接口，不新增同义状态机。

## 输入、状态与数据

明确字段/权限/幂等/状态转换/分页及事件语义。一个检查由所属责任层实现；新增校验写具体风险、触发条件、失败范围和回归入口，不能只说防御性。

## 兼容与性能

说明被替代路径和必要消费者；无害扩展兼容，未知执行不猜补，旧执行是否退役按实际决定。列出要减少的查询/复制/等待及测量方法，不将性能目标做请求deadline。

## 验收与来源

给出可观察场景、实际测试入口、固定输入和未验证项。来源/交付分开；继承[统一开发约束](../architecture-convergence/development-principles.md)，不复制一套发布/DFX框架。
''')
write('specs/_template/design.md','''# <Feature name> design

## 最小责任链

具体输入/权威Owner/输出/实际消费者；框架身份止于入口，公共持久化承担已有隔离。

## 协议与数据细则

只写真实受影响的字段、状态、事务/幂等、查询与索引；若不改wire，明确无需全链改造。

## 失败与恢复

必要失败域、真实错误/取消、已有恢复来源；不新建无依据兜底表或通用重试层，不重放未知副作用。

## 兼容与切换

新旧实际交集、被删临时路径、制品/数据恢复边界；历史冻结输入保留，不把旧执行无限兼容。

## 验证

关联acceptance的具体场景和既有代码/测试入口。UI变化先更新唯一原型；只有后端内部变更不要求无关原型修改。
''')
write('specs/_template/tasks.md','''# <Feature name> tasks

任务沿用既有Owner/handoff，不新增Reviewer/审批或台账；以下仅填本次真实改动。

## 固定范围与输入

- 当前责任专题/目标/非目标：
- 仓库、commit/tree、实际影响调用方：
- 最早定向反馈入口与fixture：

## 实施与旧路径收口

- 实际修改点及替代/删除路径：
- 契约变化才需要同步的消费者：
- 必要回归及明确未覆盖项：

## 交付

本地固定干净源码和独立输出执行必要测试/构建；真实批次和SHA，精确证据匹配可复用。获授权才受控安装，健康与业务验收分开；600秒是完整墙钟目标而非强杀。完成后保存包外证据，按现有维护规则登记可回收产物。
''')
write('specs/_template/acceptance.md','''# <Feature name> acceptance

## 场景与可观察结果

| 场景/固定输入 | 预期业务结果 | 真实入口/测试 | 实际结果与证据 |
| --- | --- | --- | --- |
| 待填写本次范围 | 不用泛化PASS代替业务断言 | 复用现有入口 | 未执行不得填写通过 |

## 必要保护

按责任层覆盖实际身份/ACL、事务、幂等、完整性和恢复风险；不在每个调用方复制公共机制用例。

## 性能观测

记录请求/查询/字节及用户边界耗时、冷/热/样本数/失败；超过目标记录问题，不拒绝请求凑数字。

## 固定证据与未覆盖

- 源码commit/tree、selector/fixture/工具链：
- 本地批次、日志/测试、制品SHA：
- 安装/健康/业务验收（分别记录，未授权则未执行）：
- 未验证/残留与责任专题：

历史原始失败/冻结输入不改写。文档检查不等于应用或线上验收。
''')
(E/'navigation-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
print('navigation/rules/templates updated',len(changes))
