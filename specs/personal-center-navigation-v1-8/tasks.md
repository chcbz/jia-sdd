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

- [x] N0固定契约/最新基线。
- [x] N1入口和保护自检。
- [x] N2双向导航和错误提示自检。
- [x] N3集成与覆盖限制记录。
- [x] N4a合develop、冻结release、制品与证据归档。
- [ ] N4b生产发布与认证线上回归（本轮不执行）。
- [ ] 通知可验收并记录用户实际回执。

不重复开发1.7只读五区，不强制再次全量验证未变API；复用需绑定tree/selector/fixture。1.7新真实缺陷独立修复，旧平台/模型治理/收费任务不混入。

## 20:34 启动记录

- API/Web `codex/bugfix/1.7.0`已推送并readback，精确对应既有release/1.7.0，不夹带1.8。
- N1：`V1-8-HALL-NAV-20260917`，分支`codex/v1-8-hall-navigation-20260917`。
- N2：`V1-8-PROFILE-NAV-20260917`，分支`codex/v1-8-profile-navigation-20260917`。
- 两worktree均从已fetch的远端develop `7c490298`创建；本机主checkout有历史/其他任务改动，不reset、不挪用。N3等待两份自检candidate，不等待独立Reviewer。
- 本轮未建release/1.8.0、未构建/发布、不操作API；每项仅完成自检后再集成推进。


## 2026-09-17 集成进展（运行时状态仍以唯一台账为准）

- N0/N1/N2已完成实现并集成；维护分支已远端确认。
- N3首轮292项相关回归及7项policy通过；真实Chromium发现刷新后用户资料未加载，修复后新增回归，当前294/294相关测试通过。最终bundle/browser重验待完成。
- 追加`V1-8-API-BASELINE-20260917`：保留远端1.7基线并整合两个已存在热修复，相关验证/制品准备中，不操作其他任务线上服务。
- N4本轮仅到合develop/冻结release/生成manifest/通知。部署、线上回归和用户验收单列，不能标作本轮已完成。
- 早期8–12小时为首次范围估算，不能将模型运行时直接当作人天；实际测试、返修和资源互斥证据逐项记录。


## 最终分支冻结结果

- Web `7099b176`：294相关回归+7策略PASS；最终干净生产bundle的Chromium38/38 PASS（显式screen.orientation/coarse pointer、横竖布局、原页旋转、刷新/直达/往返）。
- API `0b5cfe8c`：118相关测试PASS，bootJar成功；保留完整1.7并带入已存在热修复，非全API套件green。
- 两仓远端develop及release/1.8.0均readback到上述exact SHA；未覆盖原有release/1.7.0或维护分支。
- 本轮实现/集成任务结束，部署/真实认证回归/用户验收未执行。详见`docs/implementation/V1_8_RELEASE_READY_20260917.md`和交付包readiness.json。
