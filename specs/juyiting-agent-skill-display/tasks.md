> 2026-10-17 发布收口补充：1.16.8已由API Flow152、Web Flow224部署并完成范围内在线验收。当前结果见 `release-1.16.8.md` 和 `integration.yaml`；下文旧NOT_RUN/阻塞/估算为历史阶段，不代表当前状态。

> 历史D1：已由 `design-d4.md`、`plan-d4.md`、`acceptance-d4.md` 替代，不再作为当前开发计划。

# 开发切片（D1）

唯一Owner：本聊天Owner。所有路径相对各自固定仓库根，实际使用绝对路径；基线见design.md第1节。预计分钟数仅为主动开发时间，正式Flow/Gradle运行与排队单列，不能为了30分钟切片删回归。

此清单没有“再核实接口/再决定方案”项目；核实结论已在详设中。实现之前登记真实执行ledger，读取适用AGENTS.md和规范v1.2。禁止在当前有其它修改的根仓库批量暂存。

| ID | 固定改动与交付物 | 完成条件 | 预计 |
|---|---|---|---:|
| D01 | API：在AgentProfileCapabilitiesService定义3个record和只读方法签名；新增错误类型/映射常量 | 字段逐项符合design 3.2；不引入第二套信封 | 15分钟 |
| D02 | API：SkillCandidate增加installationVerified，更新所有构造点 | 既有TaskCatalog wire不变；布尔值不由reason前缀推断 | 20分钟 |
| D03 | API：提取共用目录投影，增加inspectInstalledSkillsWithoutRuntime | 不伪造fence；无proof保留安装事实；重复版本明确不可用 | 30分钟 |
| D04 | API：实现聚合服务owner校验、proof→fence与末尾owner复查 | 非ForUpdate；proof scope全匹配；不触发任何写入 | 30分钟 |
| D05 | API：实现partial-source失败、DTO白名单及时间类型校验 | 源失败不变空目录；不暴露metadataJson/host/凭证 | 20分钟 |
| D06 | API：新增GET Controller、query/body拒绝、HTTP错误映射 | HTTP与业务code一致，no-store，统一requestId | 25分钟 |
| D07 | API测试：安装/在线/离线/无proof/变更/重复版本 | acceptance S01—S10具有可运行断言 | 30分钟 |
| D08 | API测试：真实HTTP信封、owner隔离、无副作用 | acceptance H01—H08具有可运行断言 | 30分钟 |
| D09 | Web：新增纯投影和原因映射 | 合法/非法数据、计数、字符串版本测试具备 | 20分钟 |
| D10 | Web：新增详情composable及请求竞态测试 | A→B、身份切换、关闭重开、旧finally均不能串状态 | 30分钟 |
| D11 | Web：AgentPanel技能/本领两区、状态、刷新按钮 | 合法空本领覆盖旧值；非owner不泄露目录 | 30分钟 |
| D12 | Web：JuyiHall接线及卸载，当前列表行展示覆盖 | 不改名册存储和派单；保留不预填草稿提交 | 20分钟 |
| D13 | Web测试：挂载组件、既有按钮、窄屏/键盘与错误态 | acceptance U01—U10全部覆盖 | 30分钟 |
| D14 | 证据整理、既有本领文档定点纠错、固定候选及验证输入 | 源码/测试/发布状态分开；不把未知标PASS | 20分钟 |

合计主动实施估算约350分钟（约5小时50分）。这是拆分后的估算，不承诺单项遇到编译/契约问题仍必然在30分钟内完成；新增问题必须带具体证据另拆修复，不用“继续核实”作为空任务。

## 正式验证与发布（不计入上述主动编码分钟数）

1. 定向测试先取得反馈；按固定tree/selector/fixture保存证据，不复用其它任务ID。
2. 后端读取当前build.gradle，经cyf_orchestrator gradle串行运行测试与validateLayering，保持依赖完整性；失败归因后再修复。
3. 前端正式测试/构建使用Flow4403172；本机仅诊断，不做生产打包。
4. 发布版本与窗口另行明确；先API后Web，同批不可变制品，在线只读验收。无Runtime发布、DDL、订单或Provider调用。
