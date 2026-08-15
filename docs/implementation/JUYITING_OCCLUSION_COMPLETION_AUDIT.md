# 聚义厅遮挡系统 V2 — E0–E18 完成审计

## 审计结论

- 审计日期：2026-08-14
- 设计完成定义：`docs/juyiting-occlusion-system-design.md` §23
- 执行计划：`docs/juyiting-occlusion-system-execution-plan.md`
- 权威账本：`docs/implementation/JUYITING_OCCLUSION_TASKS.yaml`
- 最终候选：`4127e7af8fe5c5325d0715fbfc826937f48f41bb`
- 结论：**COMPLETE**

当前证据证明 E0–E18 的实现、独立审核、视觉门禁、性能门禁、部署、线上 smoke 和发布均已完成。23 个任务卡（含 A/B 子阶段）全部处于 `accepted`、带已接受 finding 的终态或 `done`；23/23 handoff 存在；账本 58 个提交引用全部可解析且是最终 HEAD 的祖先。

## 最终外部状态

| 项目 | 权威证据 | 结果 |
| --- | --- | --- |
| 本地代码 | `/home/isp/wsps/cyf/web` | clean `develop`，HEAD `4127e7a` |
| 远端代码 | `origin/develop` | `4127e7a`，与本地 0/0 divergence |
| Release Guard | E18 handoff | GPT-5.6 Sol High `GO` |
| 生产部署 | release record | commit `4127e7a`，tree SHA `15ef96f8...89a7` |
| 线上入口 | `/`、`/juyiting`、entry JS | HTTP 200 |
| 线上地图 | `/juyiting/hall.tmx` | SHA `885471a1...d9f`，与候选一致 |
| 深层 smoke | `/tmp/cyf-e18-smoke-4127e7a.json` | PASS；无截图复跑 |
| 回滚能力 | retained backup | `/home/isp/hosts/cyf/web/bak/kit_bak_20260815_003122_4127e7a` |

release/smoke 文件使用主机跨午夜后的 `20260815` 文件名；本轮权威控制日期为 2026-08-14，执行顺序和候选身份未改变。

## E0–E18 阶段审计

| 阶段 | 状态 | 关键完成证据 |
| --- | --- | --- |
| E0 | accepted | Agent/model 路由、串行单 Writer、只读 Reviewer 和账本/handoff 体系建立。 |
| E1 | accepted | 生产等价 TMX/资产、37 mask、5 prop、路线/热点及视觉 V0 历史基线冻结。 |
| E2 | accepted | schema、canonical IR、XML/预解析规范化和 structured fatal 完成。 |
| E3 | accepted | runtime agent ID 使用原始 source ID，SHA-256/base32 stableId、反查和冲突门禁完成。 |
| E4 | accepted | 1/256 定点 polygon、even-odd、signed distance、3px 迟滞和退化 validator 完成。 |
| E5 | accepted | 统一世界排序、稀疏 constraint resolver、cycle fail-closed 和 spatial grid 完成。 |
| E6 | accepted | shadow renderer/debug overlay 与 active scene 隔离完成。 |
| E7 | accepted | staging/commit/rollback 原子激活与 fault injection 完成。 |
| E8A | accepted | 五个 prop 的接地点、四方向和右上悬赏桌排序规格经视觉/技术审核。 |
| E8B | accepted | 五个 prop 迁入 TMX canonical object；声明/插入顺序不影响结果。 |
| E9A | accepted | 32 fragment 独占 248,283 个 canonical opaque pixels，无遗漏/重叠。 |
| E9B | accepted_with_findings | 六个 PNG lossless atlas；RGBA 1,544,192 pixels exact，missing/overlap/channel mismatch 均 0。 |
| E10A | accepted_with_findings | 37/37 mask 语义映射、九宫视觉规格和 111 probes 完成。 |
| E10B | accepted | TMX manifest：37 bindings、32 targets、111 probes、0 anonymous binding/target。 |
| E11 | accepted | 111/111 固定排序 probes 通过；当前地图无需额外 constraint zone，zones=0 为校准结论。 |
| E12 | accepted | HallScene V2 全接线、renderer band、交互和回滚集成完成。 |
| E13 | accepted | 48/48 机器矩阵、GPT V4/V5/V6 视觉证据及最终 Chromium/线上 camera/interaction smoke 闭环。 |
| E14 | accepted_with_finding | Chromium 108 agents/50 fragments/37 zones；p95 1.8ms、p99 2.3ms、scanCount 0。 |
| E15 | accepted | 整图 atomic V2 switch；失败保留完整 previous scene，无 partial publish。 |
| E16A | accepted | 生产 `behindMask` 双公式、`propDepth += 0.5` 和 legacy snapshot runtime 移除。 |
| E16B | accepted | duplicate foreground asset 不再加载；V2 正常运行时 legacy full-map layers detached。 |
| E17 | accepted | full test 1482、game 790、build/typecheck/validators PASS；独立 Reviewer ACCEPT。 |
| E18 | done | GPT Release Guard GO；pinned 原子部署、线上分级 smoke、成功 push 和回滚备份完成。 |

## §23 完成定义逐项证明

| 完成定义 | 当前证据 | 判定 |
| --- | --- | --- |
| 37 个旧 mask 全部迁移和验收 | `mask-tmx-manifest.json`: 37 bindings、111 probes；E13 mapping 37/37 | PROVED |
| 不再存在全局 `behindMask` 双公式 | production `src/`/TMX 搜索无命中；E11 report `hasGlobalBehindMask=false` | PROVED |
| 不再使用 `propDepth += 0.5` | production 搜索无命中；五 prop 进入统一固定排序键 | PROVED |
| 不再同时绘制两张相同全图遮挡图 | duplicate foreground resource 引用移除；V2 active 时 legacy full-map layers detached | PROVED |
| 普通世界对象使用统一稳定排序键 | `worldOrder.ts` + schema：band/floor/elevation/fixedPointY/tieBias/stableId | PROVED |
| 复杂区域只影响当前 agent/targetFragment | resolver 使用 per-agent/zone/target edge；当前校准 zones=0，无全局状态 | PROVED |
| constraint 冲突/cycle fatal | canonical/activation/runtime validator 和 E4/E5/E7 tests | PROVED |
| 六 atlas decoded RGBA exact | `rgba-golden-report.json`: atlasCount 6，missing/overlap/channel mismatch 0 | PROVED |
| XML/预解析 canonical IR 字节一致 | E2 schema-canonical tests 与 E17 full verification | PROVED |
| runtime Agent identity 确定、无碰撞、可反查 | `runtimeAgentAdapter.ts` + 96-case final reviewer rerun | PROVED |
| 3px signed-distance 与退化 polygon validator | `polygonGeometry.ts`/`validation.ts` + E4 tests/reviewer | PROVED |
| canonical source identity gate | assetRef/path/SHA frozen；atlas/report/TMX provenance 链完整 | PROVED |
| 右上桌及九宫视觉通过 | E13 48/48、V5 12 screenshots GPT APPROVE、线上 depth smoke | PROVED |
| UI/camera/hit-test/pointer/routes/hotspots/mobile 回归 | full suite、V5 desktop/portrait/landscape、线上 CDP；5 hotspots、world-ui/halo PASS | PROVED |
| 108 人性能通过 | E14 report gates all true，p95/p99 低于阈值，full-grid scan 0 | PROVED |
| V2 原子激活且无 partial scene | E7/E12/E15 fault tests、E17 Reviewer ACCEPT、线上 V2 active | PROVED |
| 独立 Reviewer 与 Release Guard 通过 | E17 `ACCEPT`；E18 GPT `GO` | PROVED |
| 文档、TMX schema、测试和生产一致 | 23/23 handoff、58 commit refs、TMX/V5/deploy/online hashes一致 | PROVED |

## 冻结证据说明

- `tests/fixtures/juyiting/occlusion-e13/machines-gate.json` 的 `releasePass=false` 是冻结候选中的历史 `independent release_guard pending` sentinel；E18 Release Guard 已返回 GO，不能为改一个历史字段而改变已审核 HEAD。
- `tests/fixtures/juyiting/occlusion-e14/environment-blocker.json` 保存 2026-08-13 的历史 accepted run；当前权威性能报告是 2026-08-14 `benchmark-report.json`。
- `npm run inventory:juyiting-map` 默认比较当前 TMX 与 E1 immutable baseline，因此迁移完成后的 current TMX 会报告 baseline mismatch；它是历史基线工具，不是 E18 current-map validator。当前地图门禁使用 `validate:juyiting-map`、E10B/E13 provenance 和线上 TMX hash。

## 已接受但未关闭的后续债务

这些项目不改变完成判定，但必须保留追踪：

1. E17 六项 P2 hardening finding 保持开放，不得重分类为已修复。
2. 真实后端 E2E 未验证；本地 10018 refused，公共 API 根路径 403。
3. Chromium 性能证据使用 restricted-host 单进程兼容模式；正常主机 multiprocess baseline 可补充。
4. `dompurify`/`postcss`/`nanoid` 临时安全例外仅适用于该 commit/pinned 路径，2026-09-14 到期，不得自动续期。

以上均已由最终 Release Guard 明确接受为非阻断残余风险。
