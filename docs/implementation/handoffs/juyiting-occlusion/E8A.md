# Task Handoff: E8A 五个 Prop 排序规格

## 状态
- 状态：accepted
- Writer：deepseek_pro_worker / DeepSeek V4 Pro
- Visual Reviewer：vision_reviewer / GPT-5.6 Sol（只读）— `ACCEPT-V1`
- Technical Reviewer：adversarial_reviewer / DeepSeek V4 Pro（只读）— `ACCEPT`
- Base：`7144d9260b3905ce0335d037d3b1a3589d3a88a1`
- Accepted commit：`da3d9600bd322e3a85d93ebfeaf07cd04a76f33d`
- 日期：2026-08-09

## 冻结规格

| Prop | TMX | sortAnchor | fixedPointY | tieBias |
| --- | ---: | --- | ---: | ---: |
| main-seat | 90 | `(872,268)` | 68608 | 0 |
| agent-roster | 91 | `(178,737)` | 188672 | 0 |
| bounty-board | 92 | `(1446,379)` | 97024 | -4 |
| library-shelf | 93 | `(1558,719)` | 184064 | 0 |
| roster-book（完整发光讲台/柜体） | 94 | `(306,384)` | 98304 | 0 |

- 五 prop 顺序：main-seat < bounty-board < roster-book < library-shelf < agent-roster。
- bounty north=`(1446,351)`；behind/boundary/front Y=`370/379/420`。
- boundary 由 table tieBias `-4` 与 agent `0` 确定为 `prop<agent`，不依赖 agent hashed stableId。
- mask 58 保持 E10A 强制视觉复查；drawable、canonical occluder、mask geometry、hotspot 继续严格分离。

## 证据与验证
- 规格：`tests/fixtures/juyiting/occlusion-v1-props/prop-sort-spec.json`
- 自包含视觉证据：`tests/fixtures/juyiting/occlusion-v1-props/contact-sheet.svg`
- generationId：`4a47753cf81ef0219f6e1914ff818be291158bc100d4d2c639cb0c23a8a0f8c6`
- 视觉矩阵：20 个五-prop N/S/W/E 单元 + 14 个 bounty 双角色单元；真实卢俊义/扈三娘 idle/down/frame-0，W/E alpha AABB 零相交且至少 4px guard。
- Directed：47 passing；E1 baseline：41 passing；`test:game`：698 passing；完整 `npm test`：1061 passing；build PASS；`git diff --check` PASS。

## Reviewer 记录（不阻塞 E8B）
- WebP alpha 扫描依赖 `/usr/local/bin/chromium-headless-smoke`；环境变化时 fail-closed。
- `stableJson` 依赖规范化 JS 属性插入顺序。
- 同输入并行 WebP 扫描存在同名临时文件的 P2 风险；当前阶段串行执行。
- SVG 根属性验证依赖生成器固定属性顺序。

## Exit Gate
- GPT V1：`ACCEPT-V1`。
- Technical Reviewer：`ACCEPT`。
- E8B 已解锁；不得自行改变以上 anchor、tieBias、probe 或角色帧。
