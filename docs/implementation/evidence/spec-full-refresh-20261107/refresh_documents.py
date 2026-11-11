"""One-time documentation reconciliation for the user's 2026-11-07 request.
No source, fixtures, existing integration pins or release records are rewritten.
"""
from pathlib import Path
import json,hashlib,re,os
ROOT=Path('/home/isp/wsps/cyf'); E=ROOT/'docs/implementation/evidence/spec-full-refresh-20261107'
contracts=json.loads((E/'feature-contracts.json').read_text())
changes=[]
def write(path,text):
 p=ROOT/path; old=p.read_text() if p.exists() else None
 if old==text:return
 if old is not None:
  before=E/'originals'/(path+'.txt');before.parent.mkdir(parents=True,exist_ok=True)
  if not before.exists():before.write_text(old)
  assert p.read_text()==old,'Concurrent document change: '+path
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
 changes.append({'path':path,'before_sha256':hashlib.sha256(old.encode()).hexdigest() if old is not None else None,'after_sha256':hashlib.sha256(text.encode()).hexdigest()})

def block(feature,kind):
 c=contracts[feature]; is_hist=feature=='codex-history-closeout-20261023'
 common='[统一开发约束](../architecture-convergence/development-principles.md)'
 detail=c.get('detail','design.md')
 status=c.get('status','本轮更新实施约束与文档入口；交付状态按下方注明日期的原验收/交接记录读取，未核实今日线上，不能把文档修订号当应用版本。')
 heading='现行规格' if kind=='spec.md' else {'design.md':'现行设计边界','tasks.md':'当前实施与收口方式','acceptance.md':'当前验收合同'}[kind]
 lines=['<!-- CYF-CURRENT-CONTRACT-20261107 -->',f'## {heading}（2026-11-07）','',f'**本专题：{c["purpose"]}。**',f'**文档与交付状态：** {status}','']
 if kind=='spec.md':
  lines += ['### 责任与业务流程',c['owner'],'',c['flow'],'','### 明确边界',c['boundary'],'',f'共用{common}：本地固定源码测试/构建，获授权受控安装；一次规则一个责任层；性能预算不拒绝/强杀；历史兼容不变成执行双轨。业务字段、状态、错误及测试细节仍由本专题下文和详设维护。','',f'### 验收落点\n{c["verify"]}']
 elif kind=='design.md':
  lines += ['### 最小责任链',c['owner'],'',c['flow'],'','### 实施约束',c['boundary'],'',f'性能/安全/可靠性/审计/运维按{common}分工；只在真实网络/存储/进程边界做其必要检查，不在可信调用链重复认证、重算整份合同或新增通用兜底层。','', '只在本专题实际改变协议或数据语义时同步生产者/消费者/必要迁移；接口不变的内部修复不默认修改Web、API、Runtime全链。表/索引修改须说明其查询或一致性职责，不新建CHECK/触发器代替业务规则。']
 elif kind=='tasks.md':
  lines += [f'**实施目标：** {c["flow"]}',f'**责任落点：** {c["owner"]}','', '按当前获授权的变更范围执行，不自动重开后文历史未勾选任务或旧版本排程：','',f'1. 核对当前合同及实际责任层调用链：{c["boundary"]}', '2. 复用现有任务/工作区和验证入口实现最小差异；被替代临时路径与对应过时测试同批收口，不新增Reviewer/审批/独立台账。',f'3. 运行实际受影响回归：{c["verify"]}', '4. 记录精确源码/测试/未覆盖项；获部署授权才按当前本地来源工具发布，健康与业务验收分开。未获得新范围授权不重放历史任务、迁移或收费调用。','',f'共用规则：{common}。原任务ID、失败样本、未覆盖需求与历史证据保留；未核实的旧待办先对照后续交付，不直接重做。']
 else:
  lines += ['### 必须验证的业务结果',c['verify'],'','### 不回归边界',c['boundary'],'','### 证据如何判定', '- 绑定实际commit/tree、测试selector/fixture和输入；真实返回/数据库事实/页面行为只证明各自层，mock不冒充跨层验收。', '- 必要身份/ACL、幂等、事务、锁及完整性保护按责任层覆盖；不在每个消费者复制同一防御矩阵。', '- 性能使用真实同一请求/场景：请求数、查询数、读取字节、首字与完成时间分别记录；超标记录待优化，不用快速失败计成功。', '- 以当前规则本地执行必要测试/构建并保存日志/制品摘要；本页历史Flow记录只证明当时输入，不要求重新付费Run。', '- 源码接受、测试、安装、健康、业务验收分别写结果；不把历史PASS迁移到新tree，不补填未实测指标。','',f'责任与DFX：{common}。']
 links=['[需求](spec.md)']
 if not is_hist:links += ['[设计](design.md)','[实施](tasks.md)','[验收](acceptance.md)']
 if detail not in ('spec.md','design.md'):links += [f'[当前专项细则]({detail})']
 lines += ['', '**入口：** '+' · '.join(links), '', '**下文适用方式：** 业务细则中未被本节或后续明确合同替代的条款继续有效；原日期的状态、版本、日程、Owner安排、测试/发布记录仅作历史，不授予今天的执行权限。冲突按本节指定的继任合同和根AGENTS处理，不按文件名的新旧或旧任务勾选状态猜测。','<!-- /CYF-CURRENT-CONTRACT-20261107 -->','']
 return '\n'.join(lines)

for feature in contracts:
 folder=ROOT/'specs'/feature
 assert folder.is_dir(),feature
 names=['spec.md'] if feature=='codex-history-closeout-20261023' else ['spec.md','design.md','tasks.md','acceptance.md']
 for name in names:
  p=folder/name
  if not p.exists():continue # recommendation missing documents are written below with real detail
  old=p.read_text()
  if '<!-- CYF-CURRENT-CONTRACT-20261107 -->' in old:continue
  match=re.search(r'^# .+$',old,re.M)
  if match:
   # Preserve content exactly except for an explicit, authoritative current section after the title.
   pos=match.end();text=old[:pos]+'\n\n'+block(feature,name)+old[pos:]
  else:text=block(feature,name)+'\n'+old
  write(str(p.relative_to(ROOT)),text)

# Missing recommendation documents: derive from the existing contract, not fabricated test results/pins.
f='juyiting-assignee-recommendation'
extra={
'design.md':'''\n## 接口与职责\n\n- 既有 `POST /agent/tasks/{taskId}/recommend`；请求携带字符串expectedTaskVersion；响应字段/逐人评级/顺序/错误分类以spec.md为准。\n- agent服务取得授权候选、资料固定版本元数据和可披露能力；chat的模型适配执行一次无工具推理；API校验候选/引用并组装权威Agent投影，不在Web重评分。\n- READY/NO_MATCH/NO_CANDIDATES与模型/传输错误分开；409表示输入事实已变化，不自动重新发起收费请求。\n- Web按身份/事项隔离及合并在途请求，旧作用域迟到结果丢弃；手选与确认不依赖推荐成功，也不绕原承办授权。\n- 文钱包扩展复用同次推荐的工作量判断，报价由费用模块计算；不保留旧预览报价为第二收费路径。\n\n## 当前相关入口\n\n接口/Service/Model/Test名见[spec.md](spec.md)“当前源码职责”和“必要校验”表；详细过程见[原交接](../../docs/implementation/handoffs/JYT-MODEL-RECOMMEND-20261028.md)。单次耗时及候选问题不自动扩展成向量/DAG方案。\n''',
'tasks.md':'''\n## 本次文档补齐\n\n- [x] 从既有spec补齐职责、任务和验收入口。\n- [x] 保留推荐事实与文钱包估算的责任分离。\n- [ ] 后续有产品变更时再按实际候选执行Service/Controller/Model及Web定向回归；本轮没有运行或重标应用测试。\n\n## 未完成效果的处理\n\n原交接中业务/性能未通过的样本继续保留；诊断候选输入、输出和页面链路后才能判定是否修复。安装健康或静态Prompt断言不能关闭模型语义问题。新模型联调/发布按相应实际授权，不因为补齐本文件而启动。\n''',
'acceptance.md':'''\n## 场景矩阵\n\n| 场景 | 可观察结果 | 原测试入口 |\n| --- | --- | --- |\n| 事项/候选推理中变化 | 409，不据旧结果派单 | AssigneeRecommendationServiceTest/ControllerTest |\n| 缺失/重复候选、跨候选引用 | 502，不用默认评分填平 | ServiceTest |\n| 无候选/无匹配/不可用 | 明确不同状态，不伪装成功空列表 | ServiceTest及Web推荐测试 |\n| 自有与外部候选 | 沿模型返回顺序展示；用户仍须确认 | ModelTest及Web component-behavior |\n| 身份/事项切换 | 旧请求取消/结果丢弃，不污染新页面 | useHallData相关测试 |\n| 实际模型效果与耗时 | 固定输入逐人理由有依据，报告真实样本 | 获准真实推荐探针，不以静态Prompt替代 |\n\n## 历史证据\n\n[spec.md](spec.md)和[原交接](../../docs/implementation/handoffs/JYT-MODEL-RECOMMEND-20261028.md)含历次候选、失败、部署与未验范围。本文件不重算历史PASS，也不把源码清单当今日线上状态。\n'''}
for name,body in extra.items():
 path=f'specs/{f}/{name}'
 if not (ROOT/path).exists():write(path,'# '+contracts[f]['purpose']+' — '+name[:-3]+'\n\n'+block(f,name)+body)
path=f'specs/{f}/integration.yaml'
if not (ROOT/path).exists():write(path,'''# 文档补齐（2026-11-07），不是新的候选或发布记录；不伪填历史SHA。\nfeature_id: juyiting-assignee-recommendation\nstatus: documentation_reconciled\ncontract:\n  current_design: design.md\n  current_plan: tasks.md\n  current_acceptance: acceptance.md\npinned_revisions:\n  api_commit: null\n  web_commit: null\n  root_base_commit: null\nverification:\n  documentation: pending\n  api: not_run_this_revision\n  web: not_run_this_revision\nacceptance:\n  status: historical_evidence_only\n  evidence: ../../docs/implementation/handoffs/JYT-MODEL-RECOMMEND-20261028.md\n''')
(E/'primary-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
print('features',len(contracts),'primary documents written',len(changes))
