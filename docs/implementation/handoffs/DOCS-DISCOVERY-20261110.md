# docs/specs全量分类与Agent发现收口（2026-11-10）

Owner：本会话。用户要求完整梳理docs/specs、现行有效且Agent能发现。范围为文档、既有只读发现/检查工具及其定向测试；不构建、不部署、不付费调用、不操作业务/生产状态。最终检查结果在本任务完成时写入下方。

本地基线与原始字节：`/home/isp/state/cyf-docs-discovery-20261110/before.json`和`before/`；根/API/Web均有既有脏修改，不覆盖无关内容、不fetch或假称远端/线上最新。原冻结合同、JSON/YAML/fixture/pin/receipt不为整理改写。可变指南原文另保存在本仓archive及专题history，按原路径解释相对引用。

## 最终结果

**文档发现/分类/现行导航整理完成，工作区已落盘；未Git提交、推送或合入，未构建、部署或跑业务回归。** 新会话在此根工作区遵循AGENTS即可沿入口发现；其他分支/克隆/主机须同步本任务文件，不假称未提交内容已经全局分发。外部Runtime工作区仍须显式携带CYF规则。

### 实际整理

- 根AGENTS、根README、docs/README、docs/AGENTS、specs/AGENTS、specs/INDEX/README串起唯一发现链；全局119项回归从这些入口及聚义厅Runbook均可到达。
- 全量分类1196份Markdown（docs/specs 1194份，加根AGENTS/README 2份），覆盖40专题；209份默认检索入口/选定细则/带边界的旧基线均从根AGENTS可达，0无归属/未核实角色项。分类完整不等于逐条业务事实已全部与源码或线上复验。
- 收敛聚义厅Runbook/功能指南、项目地图、部署/构建策略、检查边界/发布安排、实施及知识库入口；不再把SILVER、无条件不兼容、旧Flow-only、旧角色/排期混作现行指令。经济主spec/design/tasks/acceptance改为当前WEN专项入口；被取代技能管理SM-1说明直接降为历史。
- 原可变指南/主文档共14份保留逐字节快照与SHA：docs/implementation/archive/2026-11-10-documentation，以及经济、多媒体专题history/2026-11-10-documentation；相对引用按原路径解释。原冻结核心手册/基线/fixture/checker四份及全局119项定义不改。
- 复用既有sdd-document-map的discovery选择、sdd_docs/check-docs及kb-search，不另建任务/发布台账或测试平台。默认项目搜索排除历史/未选版本；显式project-all才纳入。

### 验证（仅文档与发现工具）

| 检查 | 结果与边界 | 原件 |
| --- | --- | --- |
| `./sddw check-docs --all-docs` | DOCUMENT_NAVIGATION_PASS：40专题、214检查文档、1655本地目标；209默认文档可达，0不可达；旧API来源缺失单列1项警告，不假称全链接无历史问题 | `/home/isp/state/cyf-docs-discovery-20261110/final-navigation.json` |
| 原`./sddw check-docs` | DOCUMENT_NAVIGATION_PASS，旧入口兼容 | 同目录`final-legacy-navigation.json` |
| 发现工具定向测试 | 32 PASS，含当前/历史分流、缺失/孤立入口、证据不可升格、旧基线显式告警、只读、symlink、检索argv | 同目录`tool-tests.log` |
| Bash语法 | `bash -n sddw docs/knowledge-base/kb-search.sh` PASS | 已执行，无构建/业务操作 |
| 实际检索 | 当前检索找到全局119项；专属历史句默认无匹配/显式全历史1匹配 | 同目录`search-*.txt` |
| 原文/机器合同保护 | 7491份原文本/合同扫描；本任务仅扩展sdd-document-map，原映射键不变；原pin/fixture/receipt和冻结核心四份保持；14快照原字节匹配 | 同目录`final-integrity.json`及`before.json` |
| 全量Markdown路径扫描 | 1196份、3089个本地引用；389个缺失引用＝388个历史/未选版本引用+1个旧API源码引用，留原文与来源，不以重造证据修绿 | 同目录`all-markdown-link-audit.json` |
| 本任务新增行空白检查 | PASS，只比较开工前dirty快照，不把他人修改计入本任务 | 同目录`own-whitespace-check.json` |

### 已知边界与并行改动

知识库生成基线仍为2026-08-15，API/Web checkout SHA不同且根/API/Web为dirty；没有重建API全清单、fetch远端或读取今日线上版本。旧resource AuthenticationController路径不存在，明确列STALE_BASELINE_SOURCE_MISSING而不是换同名Controller伪造来源。历史缺失引用不作为当前导航；需要复现时查原候选/备份，不从当前分类推断旧来源已恢复。

比较期间发现非本任务4份文件变化：docs/implementation/EVIDENCE_CACHE.json、TASKS.yaml、handoffs/TASK-SCHEDULING-UNIFICATION-20261109.md及specs/agent-economy-marketplace/beta-wen-billing.md。未写入/还原这些并行修改，单列摘要，不纳入本任务diff或声称原字节未变；当前经济入口继续引用其真实权威正文。

文档新增/合同变化后，维护责任主文档链接与discovery选择，运行`check-docs --all-docs`及所影响工具测试。定义、实现、源码测试、安装与业务回归分别报告；下一次119项回归仍须实际授权/资源并绑定当轮精确部署，不能继承旧17项PASS。

## 后续：去重退役与远端develop核对（2026-11-10）

本节接续用户“40个专题是否都有用、清理无用/过期信息及确认最新develop”的要求，覆盖上文仅导航整理的最终数字，不改写原验证证据。未提交、合入或部署。

### 实际精简

- 39个业务/架构入口收敛为35个现行责任专题；经济只读预览、单租户迁移、2026-10-08流程修复、2026-09-23正式流程bugfix四个专题退役，另有1个历史会话来源。物理40目录保留是为了不破坏原要求、验收和证据路径，不再当40套现行方案。
- 删除12份可变spec/design/tasks中280行重复且误导的“现行合同”包装，换成退役指示。未删除独有业务要求，仍有效的只读副作用、owner授权、流程状态/固定资料/返工和启动就绪约束分别归并到WEN、环境租户、整体体验主spec。四份原acceptance、integration pin/receipt/冻结材料不改。
- 12份旧源码基线保留定位价值，但退出默认当前项目检索；所有退役目录含未来新增文档也不得被自动升为CURRENT_SPEC。历史来源/缺失旧源码仍显式报告，不伪造替代链接。
- 本轮是有明确继任关系的收敛，不声称其余35专题的每条陈述已全部对照最新develop源码。旧状态、失败及未实现要求不因退役变成完成。

### 真实验证

发现工具37项PASS；legacy/all-docs导航PASS（1196份分类，181份默认当前文档均可达，0错误；旧API基线来源缺失仍显式1警告）。Bash语法PASS。冻结核心四份、全局回归两份及退役四份acceptance摘要保持。旧迁移专属句默认搜索0、显式全历史1匹配。证据在`/home/isp/state/cyf-docs-discovery-20261110/cleanup/`，本轮精确差异与原文独立于已有脏工作区保存。未执行应用构建或业务回归。

### 分支事实（查询约2026-11-10 11:00 CST）

实时ls-remote及fetch --no-tags origin refs/heads/develop仅取得远端提交/对象，不切换checkout、不合并、不覆盖脏改。下列ahead/behind相对本次真实远端完整SHA，不用旧tracking摘要冒充实时。

| 仓库 | 工作分支 | 本地HEAD | 远端develop | ahead / behind |
| --- | --- | --- | --- | --- |
| `/home/isp/wsps/cyf` | `develop` | `c311a4dfb439c88e7ea61aa4aa25064be6ce6ac4` | `31231899bf1b68c75cb53cce2f02e4f64f334410` | 49 / 37 |
| `/home/isp/wsps/cyf/api` | `codex/architecture-convergence-api` | `516267bf7b19bfc03581ae580704af9246ffb622` | `c661e6421346d610ee063b0fb9b614e282e7bcca` | 0 / 333 |
| `/home/isp/wsps/cyf/web` | `codex/juyiting-ui-workflow` | `ca22ac29de657971b12a71f3a99d2d9ecfc67c1c` | `8b1b77cc0d600f67e55861b39926034cb583bf3f` | 1 / 266 |
| `/root/.codex/worktrees/runtime-public-web-egress/isp-install` | `codex/runtime-public-web-egress` | `01914a4f8b1777e0e7496548d240cb46d138efde` | `92df9eb8de9abf523dd7224e575c43329139a98b` | 15 / 0 |

根仓在develop但已分叉；API/Web并非最新develop。Runtime在功能分支，已包含本次远端develop，但额外15提交，不等于干净同步到develop。根/API/Web均有大量既有脏修改（查询时2004/94/63条状态记录），未直接pull或合入，Runtime查询时干净。未查询/断言线上版本；本轮文档变化仍仅在根工作区，不能当已入远端develop。后续同步须先保护并分离各Owner修改，再按真实差异集成，不能全目录暂存/reset。
