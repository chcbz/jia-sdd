# 工作包与实施顺序

> **2026-09-22收尾更新：** 当前已发布 `1.13.10-uxfix4`，用户确认本轮UI并授权收尾；最新实现、精确SHA、302/39/6/37测试分层与尚未验证项见 `session-closeout-20260922.md`。横屏保留沉浸地图；竖屏仅地图“横屏看全景”，不显示其他方向／地图控制按钮。本补充覆盖下文旧方向入口设计；不改写历史失败或宣称整套业务／真机验收完成。

本表保留设计WBS与原人日复杂度，不是第二运行台账。2026-09-21已按用户指令派发Agent实施，最新执行分包见`agent-execution-plan.md`，claim/精确SHA/状态只写唯一runtime ledger。目标版本为1.13.10；旧人日不作为Agent日历工期。API/Web/Runtime各由明确Owner负责，无独立Reviewer。最多两名并行源码Writer，路径冲突需分开worktree/协调。

| ID | 工作包 | 责任角色/主要路径 | 依赖 | 交付与自检 | 人日 |
|---|---|---|---|---|---|
| D01 | 合同冻结与交互补样 | 产品/设计+Owner；本规格目录 | 无 | 方向控制、保存失败、私人/正式差异补样；API DTO与宿主/授权确认 | 2–3 |
| W01 | 统一窗口/地图/方向 | Web；JuyiHall、HallWorkWindow、useHallPanels/useHallExperienceMode | D01 | 保留原地图引擎，单活动层，横竖切换/键盘/资源归属自检 | 4–6 |
| W02 | 统一草稿/选材/确认 | Web；RequestEditor/Confirm/MaterialPicker/useHallDraft | D01；整合依赖W01/B01 | 四种来源连续、三级返回、明确版本/范围/授权 | 4–6 |
| W03 | 事项/进展/成果/恢复 | Web；CaseDetail/ResultList/useHallCaseAdapter | W01；真实整合依赖B01/B03/R01 | source-aware，未知不重提、旧新版本、正式动作不混 | 3–5 |
| W04 | 百宝箱/议事/点将/阅读整合 | Web；既有PersonalWorkspace/Chat/Library/Agent相关组件 | W01/W02；W03来源链接 | 文件全操作/来源返回、会话范围、阅读手札；不重建这些服务 | 4–6 |
| W05 | 概览/消息/失败空态 | Web；HallOverview/useHallOverview | W01/B02 | 独立于榜单筛选、下一步、部分失败、埋点接线 | 2–3 |
| B01 | 草稿/私人事项/原子提交 | API；agent service/api/core/mapper及迁移 | D01 | 草稿CAS/ACL、case关联、TASK适配、幂等事务/兼容测试 | 5–8 |
| B02 | 最近/需处理读模型 | API；hall查询服务/Controller/mapper | D01；真实整合依赖B01 | 独立读模型、分页/部分失败、动作重验、脱敏事件 | 3–5 |
| B03 | 成果查询/私人修改谱系 | API；现有execution/output/formal服务适配 | B01 | 绑定真实manifest/version，新run不覆盖旧输出，旧运行懒关联 | 3–5 |
| R01 | 终态可靠回报/目录隔离 | Runtime Owner；isp-install/conf/codex-ws-agent源码及test | D01，沿用已补failure接口 | 持久待报/ACK、只重报不重跑、scratch隔离；不处理旧生产DML | 4–7 |
| Q01 | 跨层联调回归 | 测试+各Owner；Web/API/Runtime测试 | 分包到达即测；收口需W03/B01/B03/R01 | API/事务/身份/文件格式/异步/真实授权闭环，非全平台重测 | 4–6 |
| Q02 | 真机/方向/无障碍 | 测试；浏览器/真机脚本与记录 | W01后先测；收口需完整链路 | Android/iOS/实际微信渠道，键盘/系统返回/下载/焦点 | 3–5 |
| P01 | 目标用户试点与结论 | 产品/测试 | M2候选+W04 | 同脚本可用性/可用成果/回访、改进清单与业务结论 | 2–3 |
| L01 | 隔离构建/迁移/发布核验 | 发布Owner+组件Owner | 相关自检与Q01/Q02、环境/授权就绪 | exact SHA/制品/兼容DDL/安装恢复/健康；本地授权不启Flow | 2–3 |

表中路径相对Web/API/Runtime各仓；完整仓根见 `source-audit.json`。按最终exact worktree写代码，不在脏root checkout上合并全部变更。

## 并行与关键路径

```text
D01 ┬→ W01 → W02 → W03 → W05 → W04
    └→ B01 → B03 → R01 → B02
                各包完成即Q01/Q02，不等最后一周才测
W03/B03/R01/W05/B02 + Q01/Q02 → L01 → M2受控候选
M2 + W04 → P01 → M3整套体验结论
```

上图API/Runtime共用一名核心Owner时串行；如果人员不同且路径独立可并行，但不是默认无成本增加人手。W02/W03可基于冻结契约本地mock开发，不能将mock通过当正式完成；Q02方向测试可在W01后提前，不增加第三名源码Writer。

## 里程碑

| 阶段 | 包 | 累加工作量 | 对用户可交付 |
|---|---|---|---|
| M0 冻结 | D01 | 2–3 | 补齐方向/异常样例，接口与范围冻结 |
| M1 交互骨架 | W01/W02/W03 | 11–17（阶段新增） | 真应用壳中可走完整流程，依赖未齐时明确开发态，不扩大推广 |
| M2 真实闭环 | W05/B01/B02/B03/R01/Q01/Q02/L01 | 26–42（阶段新增） | 至少一个真实授权文件业务链可试点，可恢复/可修改 |
| M3 整套收尾 | W04/P01 | 6–9（阶段新增） | 全入口连续、辅助模块回归、业务试点结论 |

M1/M2为依赖视图，不意味着两阶段完全串行；B/R可与Web骨架并行。基础总量45–71人日，风险与日历工期见 `estimation.md`。
