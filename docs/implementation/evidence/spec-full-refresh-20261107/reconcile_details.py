from pathlib import Path
import json,hashlib,re,os
R=Path('/home/isp/wsps/cyf');E=R/'docs/implementation/evidence/spec-full-refresh-20261107';changes=[]
def write(path,s):
 p=R/path;old=p.read_text()
 if s==old:return
 b=E/'originals'/(path+'.txt');b.parent.mkdir(parents=True,exist_ok=True)
 if not b.exists():b.write_text(old)
 assert p.read_text()==old
 p.write_text(s);changes.append({'path':path,'before_sha256':hashlib.sha256(old.encode()).hexdigest(),'after_sha256':hashlib.sha256(s.encode()).hexdigest()})
def repl(path,pairs):
 s=(R/path).read_text()
 for a,b in pairs:
  if a not in s:raise RuntimeError('missing expected passage '+path+': '+a[:60])
  s=s.replace(a,b)
 write(path,s)

repl('specs/account-security-foundation/spec.md',[
('这是 P0 identity/ACL/concurrency/migration 变更，API 必须由 `critical_worker` 单独写入，并由独立只读安全 Reviewer 审查。','这是身份/ACL/并发/迁移变更，由本任务Owner对实际风险自检并完成必要回归；不指定已退役角色或创建独立Reviewer。')])
for name in ('spec.md','design.md','tasks.md','acceptance.md'):
 p='specs/api-performance-3s-slo/'+name;s=(R/p).read_text()
 s=s.replace('普通发布仍保留云端功能/安全回归、同 Run 制品及健康核验','普通发布仍保留本地必要功能/安全回归、同批次制品及健康核验')
 s=s.replace('新增路由默认进入普通同步 3 秒门禁','新增路由默认进入普通同步3秒观测分类').replace('规避门禁','规避观测')
 s=s.replace('每批有独立 commit、Owner 自检和云端测试','每批有固定commit、Owner自检和本地必要测试').replace('并补云端回归','并补本地定向回归')
 # Names in historical task tables are not active model/role assignments.
 s=s.replace('（balanced_worker）','（Owner负责；旧角色已退役）').replace('（critical_worker）','（Owner负责；旧角色已退役）').replace('（critical_worker；','（Owner负责；')
 write(p,s)

repl('specs/architecture-convergence/design.md',[
('检查在Flow随既有任务执行，不单独建流水线。','检查在本地固定源码随既有必要验证执行，不新增流水线或检查服务。'),
('API/Web/Runtime版本、候选SHA、安装文件SHA和线上结果分别记录；Flow成功不能替代业务通过。每Run≤600秒，超时受控结束，不以拆Run凑时限、删关键回归或回本机构建规避。','API/Web/Runtime版本、候选SHA、安装文件SHA和线上结果分别记录；本地构建成功不能替代业务验收。完整同批600秒为优化目标，超出如实记录，不强杀应用/构建、不删除关键回归。')])
repl('specs/architecture-convergence/acceptance.md',[
('先读取候选build.gradle，再通过现有编排/Flow入口设置对应参数，不在本机执行这些重任务。','先读取候选build.gradle，再通过现有orchestrator入口在本地固定干净源码执行定向测试及分层检查。'),
('建议加入现有Flow候选selector（不是直接在本机复制运行）：','使用既有测试selector，在本地固定候选和fixture后经编排入口运行：'),
('复用Flow4403172现有release profile；本次重点是：','复用Web现有必要测试及生产构建命令；本次重点是：'),
('在现有Runtime Flow的固定源码目录，以现有测试入口执行对应`conf/codex-ws-agent/test/skill-conversation.test.mjs`和`agent-client.test.mjs`，并保留既有effect/store关键测试。完整组合负载按Flow策略安排；不把正式打包搬回本机。','在Runtime固定干净源码本地执行现有对应测试；当前内部目录为`conf/codex-bridge/`，先核实实际测试路径，保留受影响effect/store测试。串行安排高内存任务，不照搬旧codex-ws-agent路径或恢复Flow-only。')])
# Historical execution schedules are explicitly contained, not restarted or rewritten as new runs.
for f,why in {
'architecture-convergence':'2026-10-26 B0–B5的固定候选排程/发布记录，不重启旧截止与旧Flow步骤；当前新增改动按上方现行方式执行。',
'juyiting-skill-execution':'SE-2旧runner/协议设计与实施记录，保留来源但不作为新的执行/恢复入口；当前以RB-1及原生详设为准。',
'single-tenant-role-isolation':'旧单租户归零迁移方案，仅保留追溯；不得重跑，当前合同转full-tenant-gray。',
'agent-economy-marketplace':'旧SILVER经济方案及其范围，冻结历史合同仍供取证；新内测同范围只实施beta-wen-billing，不并存两套资金语义。',
'juyiting-codex-fast-context-20260925':'2026-09-25快速议事提案与阶段记录，不恢复旧codex exec/新引擎/全历史推送方案；当前原生会话和页级展示遵循现行合同。',
}.items():
 for name in ('spec.md','design.md','tasks.md','acceptance.md'):
  p=f'specs/{f}/{name}';s=(R/p).read_text();marker='<!-- /CYF-CURRENT-CONTRACT-20261107 -->'
  # Keep current architecture specification's business constraints; only its old tasks/acceptance are historical schedules.
  if f=='architecture-convergence' and name in ('spec.md','design.md'):continue
  if f=='juyiting-skill-execution' and name=='spec.md':continue
  s=s.replace(marker,marker+'\n\n## 原有材料的适用范围\n\n'+why+' 后文所有旧“当前/最新/待实施”仅指其原时间，不是2026-11-07状态。\n',1)
  write(p,s)

repl('specs/juyiting-agent-skill-display/design.md',[
('前后端正式测试、构建、制品和部署分别复用Flow4403172/5260799。固定发布版本及每端commit/tree，各端同Run不可变制品及SHA256；不是把两端误说成同一个Run。develop不自动部署。本机仅预览/定向诊断，禁止本地正式打包或源码到生产路径。API先健康再Web；复用发布锁、备份及可恢复安装，不改变Runtime或DB。','前后端正式测试、构建和打包默认本地固定干净源码执行；固定每端版本/commit/tree、真实批次及SHA256。develop不自动部署，生产目录不编译。按实际接口依赖安排API/Web安装顺序；保留锁、备份和恢复，不因本专题文档更新改变Runtime或DB。')])
repl('specs/juyiting-assignee-recommendation/spec.md',[
('重型验证Flow，当前源码结果不等于上线。','必要验证在本地固定候选执行，当前源码结果不等于上线。')])
repl('specs/archive-agent-maintenance/spec.md',[
('重型API验证仍走Flow。','必要API验证按根规则在本地固定候选、经orchestrator执行。')])
repl('specs/full-tenant-gray/spec.md',[
('主机独立拉取固定真实Run不可变制品，按coordinator→release→lifecycle锁、身份/ACL、摘要、备份及恢复流程安装。精确源码/测试/制品一致时复用，下载/安装重试、文档、重启不重复付费构建；不得把重型任务搬回本机。','本地固定源码生成不可变制品，按coordinator→release→lifecycle锁、身份/ACL、摘要、备份及恢复流程安装。精确源码/测试/制品一致时复用；下载/安装重试、文档、重启不重复构建。此规则不重新开放已冻结灰度范围。')])
repl('specs/juyiting-skill-execution/acceptance.md',[
('轻量自检与正式验证分开。重型测试/构建/打包使用既有Flow，每Run≤600秒；固定源码、制品、安装、线上验收分别记录。下文历史后端本地构建等口径仅供历史追溯，不覆盖现行AGENTS规则。','最早定向反馈与正式验证分开记录；必要测试/构建/打包默认本地固定源码执行。完整同批600秒为目标而非强杀；源码、制品、安装、线上验收分别记录。旧Flow和旧本地准入步骤均不能覆盖现行工具和根规则。')])

# Current supplemental contracts: update live execution guidance, preserve dated probe results.
repl('specs/juyiting-skill-execution/native-execution-technical-design-20261027.md',[
('重型测试/构建/打包走既有Flow，每Run总计≤600秒。','必要测试/构建/打包默认在本地固定干净源码执行，复用既有工具；完整同批600秒是优化目标，不强杀、不删必要回归。')])
repl('specs/juyiting-skill-execution/native-execution-extensions-20261028.md',[
('正式重型验证/部署沿既有Flow，每Run≤600秒。','正式必要验证/打包默认本地固定源码，获授权后受控安装；完整同批600秒为观测目标，不强杀。')])
repl('specs/juyiting-skill-execution/native-execution-4plus1-20261028.md',[
('正式重型验证沿既有Flow规则。','正式必要验证沿根AGENTS本地固定源码规则。')])
repl('specs/juyiting-skill-execution/reusable-packages-20261102.md',[
('固定源码后，Flow worker测试/打包/上传不可变技能制品即结束；主机拉取并核对来源Run与SHA。不得把本机测试fixture ZIP当正式制品。','固定干净源码后，本地执行必要测试并打包不可变技能制品，记录真实构建批次/工具链/源码及SHA；受控安装核对同批来源。临时fixture ZIP仍不能冒充正式制品。')])
repl('specs/juyiting-unified-experience/business-discussion-test-cases-20261027.md',[
('重型应用测试/构建走Flow；每Run总时限600秒，不搬回本机、不删必要保护。','必要应用测试/构建在本地固定候选执行；完整同批600秒是目标，不强杀、不删必要保护。'),
('正式重型验证复用Flow。','正式必要验证复用当前本地工具。')])

# Active common policy: CHECK is no longer a persistence requirement.
p='api/docs/interface-catalog/validation-policy.md';s=(R/p).read_text()
s=s.replace('CHECK表达式、触发器/外键和迁移基线检查保护持久状态和自动DDL','外键、列类型、唯一约束和迁移基线继续保护持久状态；按2026-11-02决定不新增/依赖CHECK，不以触发器替代业务规则，生产旧CHECK仅经获授权迁移处理')
s=s.replace('根AGENTS/Flow策略、现有安装器；保留完整性/锁/备份，600秒Run上限为用户明确要求而非推测性能阈值','根AGENTS本地来源规则及现有安装器；保留完整性/锁/备份。完整本地批次600秒是目标，不是强杀/请求deadline；仅另获授权Flow才使用其Run规则')
notice='''\n## 现行适用边界（2026-11-07）\n\n本政策的风险/条件/失败域/回归要求继续有效。业务tenant由环境配置及公共持久化隔离承担，不层层透传重验；资金、身份和幂等保护不删。旧表中2026-10-24保留CHECK、旧runner、Provider专用通道及Flow-only描述只证明当时裁定，同范围分别由根2026-11-02数据库规则、RB-1原生执行和2026-11-06本地规则替代；既有历史表达式和测试记录不重标。具体开发仍按[统一约束](../../../specs/architecture-convergence/development-principles.md)。\n'''
s=s.replace('\n', '\n'+notice,1);write(p,s)

# Explicitly connect live supplemental design entry points without rewriting frozen wire/receipt files.
extras=[
'specs/juyiting-skill-execution/responsibility-boundaries.md',
'specs/juyiting-skill-execution/native-execution-technical-design-20261027.md',
'specs/juyiting-skill-execution/native-execution-extensions-20261028.md',
'specs/juyiting-skill-execution/management-mvp.md',
'specs/juyiting-skill-execution/management-design.md',
'specs/juyiting-skill-execution/management-requirements.md',
'specs/juyiting-skill-execution/management-plan.md',
'specs/juyiting-skill-execution/reusable-packages-20261102.md',
'specs/juyiting-skill-execution/skill-economy-responsibility-separation.md',
'specs/juyiting-creative-delivery-mvp/workspace-design.md',
'specs/juyiting-ui-baseline-20261006/optimization/spec.md',
'specs/juyiting-ui-baseline-20261006/optimization/detailed-design.md',
'specs/juyiting-ui-baseline-20261006/optimization/tasks.md',
'specs/juyiting-ui-baseline-20261006/optimization/acceptance.md',
'specs/juyiting-ui-baseline-20261006/optimization/README.md',
'specs/username-encoding-integrity/data-repair-plan.md',
]
for path in extras:
 p=R/path;s=p.read_text();parts=p.relative_to(R/'specs').parts;main=R/'specs'/parts[0]/'spec.md'
 rel=os.path.relpath(main,p.parent);rules=os.path.relpath(R/'specs/architecture-convergence/development-principles.md',p.parent)
 note=f'> **现行适用范围（2026-11-07）：** 本文是[所属专题]({rel})的细则，不独立定义发布/角色/DFX规则；共用[统一开发约束]({rules})。旧日期候选/测试/安装仅代表当时范围，未核实部分不改成今日完成。业务协议/冻结输入不因文档整理改写。\n\n'
 write(path,note+s)

# An active billing Owner is writing its detailed contract; route to it without overwriting their live status.
# The primary spec/index already records its supremacy; no write to beta-wen-billing.md or its handoff.
(E/'detail-changes.json').write_text(json.dumps(changes,ensure_ascii=False,indent=2))
print('detail edits',len(changes))
