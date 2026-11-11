# AGENT-ROLE-REPLAN-20261023：项目开发 Agent 精简与重规划

## 范围与固定输入

- 用户授权：删除历史开发 Agent，按当前 CYF 项目重新规划；唯一 Owner 为当前主会话。不是聚义厅产品 Agent 删除、技能卸载或 Runtime 部署授权。
- 范围：项目 `.codex/`、当前 MODEL_ROUTING、角色说明入口及本交接；不修改全局配置/共享技能、业务源码、活动 ledger、生产或其他会话。
- 本地根仓 `develop`：base commit `5e6ab2b6f1a156c320189f17d76941fbe623738a`，tree `9e1221b3aa7c70ca7f80670ec5ce7ef695af05f2`；工作区已有他人修改，根 AGENTS 只做定向增量。
- 2026-10-23只读 `git ls-remote origin refs/heads/develop` 返回 `690a69d093b67959f6062c22eb8f4a1de606ae65`，不同于本地HEAD；不fetch/覆盖、不声称本地是远端最新，不改应用线上版本。
- 测试候选为本轮文件字节与SHA-256，不把base tree当作已包含本轮改动。最早验证：TOML/YAML解析、注册与文件/路由一一对应、停用角色无活动引用，随后既有编排器离线测试。
- 统一接口规范：`api/docs/interface-standard.md` v1.2（2026-10-14）；委派外部Runtime任务需明确传达根规则及固定版本。

## 设计决定

- 从16个自定义角色收敛为5个：architect、ux_designer、developer、test_runner、explorer；主会话协调不是第6个注册角色。
- 删除13个历史/重叠角色文件，保留并改写architect/explorer/test_runner，新增ux_designer/developer；不提供旧名到新名的调度兼容层。
- UX负责设计与原型；developer负责跨Web/API/Runtime实现与自检。测试按需辅助，不另设独立Reviewer或发布审批者。3 Writer、1只读辅助、总线程容量5不变，不要求全员出场。
- 历史路由完整快照转存 `docs/implementation/archive/2026-10-23-agent-roles/`；当前路由不再混入M2/M3任务表、Reviewer、旧后端本地发布或无实测提速目标。历史ledger中的旧角色是来源记录，不批量重写或抢占。
- 不启动子Agent、不切换当前主模型、不改变任何活动会话；新配置需在后续实际加载后验证，不以文件更新证明热重载或模型调用成功。

## 备份与恢复

- 前值备份：`/home/isp/baks/cyf-agent-role-replan/20261023T184309+0800`；包含逐文件SHA-256。
- 若需恢复，只按本任务变更文件逐项对比恢复，先确认没有后来修改；不整仓reset，不改任务记录/生产/其他聊天。历史配置仅供恢复取证，不能默认重新启用。

## 验证与收口

- 2026-10-23 Owner自检完成：12项配置检查全部通过，TOML/YAML可解析，注册/角色文件/路由精确对应5项，13个退役角色无活动注册或别名；模型/权限/容量一致，原型先行与接口/Flow/Runtime安全边界齐全。
- 使用实际解析器：现有Python3.11标准库tomllib、Web已安装的js-yaml；不安装依赖、不启动应用。定向检查脚本与候选SHA-256：`/var/tmp/cyf-agent-replan-20261023/check_roles.py`、`role-config-check.json`及同目录日志。readback逐一匹配；相对前值的根AGENTS只改角色路由一行。
- 既有 `python3 -B -m unittest discover -s ops/orchestration/tests -p test_cyf_orchestrator.py -v`：19/19通过，隔离临时ledger/锁/通知；另验证五个新profile和历史profile可被既有validator读取。真实TASKS.yaml与编排器源码摘要未变；这不是新角色白名单的运行时强制校验，原工具仍将profile作为来源字符串。
- `./sddw check-docs`：36个特性、157个Markdown、438个本地目标，errors为空；仅文档导航范围。任务文件 `git diff --check`通过。
- 原MODEL_ROUTING归档字节与备份一致；历史证据与活动任务未重写。项目目录没有遗留孤立角色文件，没有修改全局设置/共享技能/API/Web/Runtime业务代码或生产。
- 官方文档读取尝试未返回可用正文（直连返回Forbidden），没有引用未读内容或宣称官方确认；本轮沿用已有项目TOML字段，基于实际文件解析与引用闭包核验。
- 未派发Agent或调用模型，未实测宿主加载/热重载；当前会话工具清单可能仍保留旧快照。后续加载项目新配置时核验5个角色；模型实际可用性单独记录，不静默改模型。
- 本轮为本地项目配置与文档完成，未commit/push、未构建/部署、未改活动任务状态；不把脏工作区base tree登记为accepted构建证据。残余边界是宿主加载与真实调用尚未验证，不影响已完成的文件清理。
- 定位/实现/验证时间未汇总，不补造耗时；发布等待不适用。已主动通知用户配置收敛与生效边界。

## 后续实际使用核验（2026-10-23）

- 用户随后明确要求UX审视原型，本会话工具发现已显示5个新项目角色；实际 `spawn_agent(agent_type=ux_designer)` 成功，Agent `01a1686b-5fdb-7592-9c25-60fcd9eff976`（Pascal）完成任务并返回带截图/浏览器证据的结果，确认读到现行规则。此项补充此前“未验证实际加载”的边界，不改写原配置交付时的事实。
- 仅证实该宿主会话已可调度并完成UX角色工作，不推广为其他四角色或全部模型可用性验证，不改变全局/当前主模型/活动任务。具体证据见 `SKILL-MANAGEMENT-20261023.md` 的UX专项及 `/var/tmp/cyf-skill-management-20261023/ux-audit/ux-findings.md`。
