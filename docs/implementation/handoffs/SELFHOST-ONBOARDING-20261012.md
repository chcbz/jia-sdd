# SELFHOST-ONBOARDING-20261012 自家接应补全

任务状态以 TASKS.yaml 为准。Main负责isp-install与集成；Faraday负责API；Hopper负责Web。范围、源码和验收以 specs/runtime-self-host-onboarding/ 为准，三个独立组件工作区均develop、开工干净。父仓无关脏文件不覆盖。

- 交接入口：AGENTS.md、ops/orchestration/README.md、冻结design已给两位Owner。API Owner已明确读完并发现旧Scope限制；Web待确认。
- API Scope原有限制tenant0不在本轮放宽，避免把文书修复扩成权限重构。
- Main最早验证：node --test /home/isp/wsps/chcbz/isp-install/tests/cyf-runtime-enrollment-prepare.test.mjs，7项通过；覆盖真实manifest摘要/登记摘要格式、非默认scope、私密文件权限、不覆盖、symlink、CLI不泄漏。工作区诊断，未登记正式accepted证据。
- 当前磁盘仅78MiB，正式Gradle/构建不得冒险启动；没有清理他人文件或旧制品。阶段通知不停止源码落实。
- 本任务不执行真实installation登记、付费调用、服务停止或发布。

## 自然接续 2026-10-12
- isp-install e3d7b30aeba7b9b36f49bf6372956d78254a3ca2 / tree86b19e3d7871d47b66e5c63fda3f7c2ce225952d 已推远端develop并ls-remote核实。8项离线测试通过，新增第8项从完整指南提取实际profile/host生成片段并交真实Runtime readers校验；无网络/enroll/服务操作。证据 evidence/selfhost-onboarding-20261012/installer-tests.log。
- API原Owner在Scope冲突裁定后继续，完成da4d4bf与9eb150d两提交；修正local不再虚构旧安装目录。Gradle因实际磁盘容量未运行，不能标accepted。
- Web第一版ba97098有2项定向失败，已回原Owner修复（不新增Reviewer）。Main发现真实useHttp双层JsonResult与测试mock不符、文件读取跨scope回包防护不足，已给原Owner同slice补齐，不以假mock通过代替真实契约。
- 磁盘一度降至1.3MiB后自行恢复约70MiB，本任务未清理其他进程/文件；主机容量不足仍阻塞大型验证/制品构建。

## 最终自然接续点（源码完成，正式验证待办）
- API最终0fe830d1ea/tree b365003e，已推develop；将原有Provisioning测试纳入既有managedHostingRegression，不新建验证框架。原Owner工作已交付，无后台开发等待。
- Web最终3d0e9ef/tree f0ca2607，已推develop。原Owner完成真实JsonResult/身份与文件异步防护、shell quoting、可移植fixture，Main补匹配查询后禁重复create及复制失败反馈。133项定向诊断PASS/exit0，证据见source-status.json和web-targeted-tests.log。正式Flow尚未跑。
- 本任务实际未修改生产配置、数据库、安装登记、服务或版本；新UI尚未上线。目标机可取isp-install develop新工具/指南，不需要为仅新增仓内prepare工具重复构建既有1.0.3制品。
- 真实阻塞：主机根盘约59MiB空闲；正式API Gradle与制品构建未运行，不以低成本源码/前端测试替代。下一步在明确归属和恢复要求下处理磁盘容量，然后由Main经现有编排器运行managedHostingRegression + validateLayering；前端Flow4403172验证候选；版本发布须另行实际执行，不自动发生产。
- 初次Main测试未带项目常用--exit，132个测试已完成但留事件句柄；精确停止本任务PID后，修正最终源码并以--exit完整重跑133项退出0。没有按耗时强杀生产/其他任务。
- optional技能quick_validate缺宿主PyYAML而未执行，未装新依赖、未冒称该校验通过；产品prepare工具的8项测试真实通过。
