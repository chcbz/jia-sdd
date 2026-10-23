# SDD-DOC-CHAIN-20261023 文档链路修正与轻量检查

## 范围与基线

2026-10-23，唯一Owner：当前会话。用户授权继续修正链路；不派发子Agent、不新增Reviewer。此文件为文档/工具变更记录，不创建或更新运行任务台账，不冒称应用任务已完成。

- 工作区：`/home/isp/wsps/cyf`，根branch develop，HEAD `5e6ab2b6f1a156c320189f17d76941fbe623738a`；工作区原有大量修改，未覆盖或暂存无关内容。
- 本地API HEAD `94b4c8a5e5b1402ef44097b5a337a75431a0ec1b`；Web HEAD `9dbd132e8bc25119c0532cbed672ab7fa4a214b3`。未fetch，不声明远端最新；未查询生产。此次不修改业务接口，公共接口标准路径仍为`api/docs/interface-standard.md`。
- 非目标：业务功能、正式测试/生产构建、发布、Runtime安装、全YAML解析器、改写历史pin或冻结验收。
- 已读根/组件AGENTS、orchestration工具入口和SDD workflow；规则以本次用户提供的固定目录迁移完成版本为准。

## 实施

1. Web规则和原型规格指向现行optimization/spec.md；Flow生产构建口径同步根规则。
2. 项目地图/WS指南更新本机固定app下codex-ws-agent目录；仅引用既有迁移证据，不进行生产操作或将1.2.7候选当线上。
3. 三份integration的7个旧文档引用更新，SE-1原稿指向已核验备份；只改文档导航及解释注释，不改源码/制品/发布字段。
4. 既有sddw增加check-docs；仅当前导航/目录完整性检查，严格候选verify仍独立。复用标准库及现有tests目录，无新依赖/框架/台账。
5. SDD规则、索引和知识入口说明历史快照、旧来源缺失及工具边界；原证据保持原样。

## 验证与恢复

审计来源：`/home/isp/baks/cyf-sdd-documents/chain-audit-20261023-133842/`。
本次变更前原文、文件摘要及实际测试结果统一存放：`/home/isp/baks/cyf-sdd-documents/chain-fix-20261023/`，只按manifest逐文件恢复，恢复前先比较现值，不能覆盖后续修改。

最早定向验证：当前文档check-docs；工具回归使用合成临时目录，无应用/网络/数据库副作用。完成结果见该备份目录validation.json；不把本机文档检查标为正式Flow测试/上线。

## 遗留边界

- sddw verify仅模板双端pin，非模板/N/A候选的源码一致性仍由Owner按真实格式核对，不自动推断字段或批量pin。
- 两处历史来源（旧工作台feature-coverage、旧API resource Controller）当前不存在；保留明确缺口，不伪造替代原文。
- 所有历史快照/冻结合同/测试发布证据未因导航修正重写；当前导航通过不代表全量历史相对链接在快照目录可直接打开。
- 定位/实现/验证的可比耗时未采集，不估算节省时间；无部署等待。


## develop集成与生产回归（2026-10-23续核）

- 后续已fetch/readback：根origin/develop `5e6ab2b6f1a156c320189f17d76941fbe623738a`；Web原origin/develop `203e00c7f8d9bb9c3f494349350e24419e0901cc`；API origin/develop `b0735f57a7b454fa7a6fb9886fa3914131986779`。前述“未fetch/未查生产”仅描述清理当轮，不覆盖本续核。
- 采用独立根worktree `/var/tmp/cyf-doc-chain-fix/integration/root` 及其Web worktree，只应用各轮备份原文到整理结果的差量；6份根文档/2份Web文档原有本地修改已隔离，不覆盖共享脏工作区。补齐远端未纳入版本的现行规格五件套及其导航依赖，原始证据按原字节纳入；未将历史记录改成当前验收。
- Web两份文档已提交并正常push develop：`638084d26ec9a193240566bf45b33602cef8e0e0`。根候选同步此Web gitlink，API gitlink保持原值；这不是新的双端业务验收pin，也不代表最新Web develop已部署。
- 干净候选导航：36目录、157个Markdown入口、429个本地目标通过；工具13项隔离测试通过。本轮原工作区433目标与干净候选429目标的差异来自未纳入的原有文档增量，不据此声称源码/发布验收通过。新增历史smoke-test-cases原文的3处空白告警保留，不为diff洁净改写历史材料。
- 生产记录：Web1.16.43 / Flow295，源码`669bdc9d6439d1bd7eb71df5ed401202a648f419`，已包含图片修复`9dbd132e8bc25119c0532cbed672ab7fa4a214b3`；API1.16.30 / Flow246，源码`b0735f57a7b454fa7a6fb9886fa3914131986779`。后续Web档案阅读器/PPT等独立develop变更未因本任务发布；本次文档无需应用构建部署。
- 本次生产浏览器证据目录：`/var/tmp/cyf-external-flow-20261021/browser/sdd-image-regression-20261023/live/`；使用ziyue，测试任务517，指定吴用。最终业务结论以本目录回归结果为准，不以此段进行中记录替代。
