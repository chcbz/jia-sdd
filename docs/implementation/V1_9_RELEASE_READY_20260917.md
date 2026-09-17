# 1.9.0 统一候选可发布（未部署）

用户指令：1.8不单独发布；1.9包含1.8，达到条件后通知，不自动操作生产。

## 已完成

- API/Web 已分别非 force、原子推送 `develop` 与冻结 `release/1.9.0`，远端 readback 一致；原 `release/1.8.0` SHA 未改，祖先关系已验证。
- API `ca74c55899fe91dbecb138a8a5bafe6481176b13` / tree `7335b3c5bd63a733e651dea1f160d5560e4967fa`；Web `41ca32b72fda97e8066783dc702b1218305ca395` / tree `0edb17f4f5420670630ab2b0f713a644a8af4bbd`。
- 1.8聚义厅个人中心入口、横竖屏与经济预览往返包含在本候选。
- 1.9个人中心「协作运行看板」：指标概览、失败/死信列表、操作审计；手动刷新/重试/分页，只读、不提供重投/终止动作。
- 新 capabilities 接口始终可发现但鉴权 fail-closed；既有身份/客户端隔离不放宽，撤权清空、旧响应拒收。

## 验证

| 范围 | 结果 | 限定 |
| --- | --- | --- |
| Web相关回归 | 308/308 PASS | 最终exact源码 |
| 经济只读策略 | 7/7 PASS | 保留1.8功能 |
| API能力/既有D09 ACL | 10/10 PASS | changed-scope，非全量API |
| bootJar公共制品验证 | 64/64 PASS | exact JAR |
| 实际生产bundle Chromium | 99/99 PASS | 隔离mock API/假身份，桌面及手机横竖屏；不算线上真机验收 |
| Web压缩包 | 420文件逐项摘要一致 | 无旧输出混入 |

Owner自检，无独立Reviewer。原六项集成问题已修复并有mounted点击回归。浏览器前两轮分别暴露harness桌面溢出假设与OPTIONS注入错误，归因/修正后最终通过，未改写历史失败。API首轮构建真实OOM已留证，通过限制本任务子JVM资源修复。API历史全量测试编译债务仍明确保留。

## 发布与启用边界

- 本轮**未部署**、未操作生产API/DB/flags/权限，无收费Provider调用；云效只读复核两条流水线仍仅cloud_ci，无部署阶段，未启动Run。
- 候选包：`/home/isp/wsps/cyf/deliverables/releases/v1.9.0-local-ready-20260917/`；manifest `readiness.json`，摘要 `SHA256SUMS`。
- 开关 `agent.rabbit-operations.read-enabled` 默认false，权限 `agent-command-ops-read` 未授予；上线不会自动让普通账号看到受保护数据。实际启用对象需另行确认。
- 仅本任务未上线且被替代的1.8大制品已回收；冻结分支/历史SHA/测试保留，见 `superseded-v1.8-binaries.json`。未清生产或回退包。
- 当前剩余磁盘紧张，发布前按真实安装与回退字节再测算；已有持久封存制品，不依赖tmpfs。此处“可发布”指候选已满足范围内测试/构建条件，不伪称生产安装空间与业务验收已经完成。

下一动作：用户安排统一发布后，发布Owner核对当前进程归属/空间，按固定制品先API后Web可恢复安装并健康验证；不复用过期进程授权。
