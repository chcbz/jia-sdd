# 实施拆包与时间估算

2026-09-17；20:34已派发N1/N2两个并行实现任务，精确活动Owner见唯一台账。运行时exact owner仅记入 `/home/isp/wsps/cyf/docs/implementation/TASKS.yaml#runtime_ledger_json`，运行台账已通过orchestrator登记/claim，本文不复制动态Owner。

| 包 | 计划责任 | 范围及输出 | 依赖 | 初估净执行 |
|---|---|---|---|---|
| N0 | 集成Owner | 最新develop、两模式header可见性、认证/guard及离开流/草稿语义盘点；固定事件和路径 | 无 | 0.5–1小时 |
| N1 | Web Owner A | 共享头像入口、竖横挂载、JuyiHall导航/离开保护、定向测试 | N0 | 2–4小时 |
| N2 | Web Owner B | UserProfile整理、返回路径、预览返回、能力失败提示、定向测试 | N0；不写N1文件 | 2–3小时 |
| N3 | 集成Owner | 合并兼容、真实浏览器往返、身份/布局/旧功能回归、修复首轮缺陷 | N1+N2 | 2–3小时 |
| N4 | 发布Owner | exact develop/release、本地Web构建/安装、线上回归、通知验收 | N3通过及实际发布授权/互斥 | 1–2小时 |

预估首个可验收版本 **8–12小时墙钟窗口**（按上述并行开发、串行集成，加1–2小时首轮返修余量）；不是人天折算，也不是24小时模型必然完成承诺。构建/发布资源排队及用户验收耗时单列。只改Web，不为本需求启动Gradle；若发现全局路由重构、身份API改动等超出假设，先重估/拆包，不悄悄放大版本。20:34启动开发，不承诺固定完成时刻。

- [ ] N0固定契约/最新基线。
- [ ] N1入口和保护自检。
- [ ] N2双向导航和错误提示自检。
- [ ] N3集成与覆盖限制记录。
- [ ] N4合develop、冻结release、发布与回归。
- [ ] 通知可验收并记录用户实际回执。

不重复开发1.7只读五区，不强制再次全量验证未变API；复用需绑定tree/selector/fixture。1.7新真实缺陷独立修复，旧平台/模型治理/收费任务不混入。

## 20:34 启动记录

- API/Web `codex/bugfix/1.7.0`已推送并readback，精确对应既有release/1.7.0，不夹带1.8。
- N1：`V1-8-HALL-NAV-20260917`，分支`codex/v1-8-hall-navigation-20260917`。
- N2：`V1-8-PROFILE-NAV-20260917`，分支`codex/v1-8-profile-navigation-20260917`。
- 两worktree均从已fetch的远端develop `7c490298`创建；本机主checkout有历史/其他任务改动，不reset、不挪用。N3等待两份自检candidate，不等待独立Reviewer。
- 本轮未建release/1.8.0、未构建/发布、不操作API；每项仅完成自检后再集成推进。
