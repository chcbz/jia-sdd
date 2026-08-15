# Task Handoff: E8B 五个 Prop TMX/Manifest 迁移

## 状态
- 状态：accepted
- 原始 Writer：deepseek_flash_worker / DeepSeek V4 Flash
- Provenance Follow-up Writer：deepseek_pro_worker / DeepSeek V4 Pro
- Reviewer：adversarial_reviewer / DeepSeek V4 Pro（只读）
- Base：`da3d9600bd322e3a85d93ebfeaf07cd04a76f33d`
- Accepted HEAD：`a700d1c57a15026a362db535f97fb6baff47e9f7`
- Commits：`d53187cda2174053e3611560bda0d882943d82a8`、`5ccbf7293afb66d3b99904bacc97285919f39182`、`a700d1c57a15026a362db535f97fb6baff47e9f7`
- 日期：2026-08-09

## 已交付
- TMX 90–94 已严格写入 E8A 冻结的 V2 prop 属性；active scene 仍保持 V1，TMX 无 `renderSchemaVersion`。
- `prop-tmx-manifest.json` 升级为 E8B-owned provenance overlay：
  - E1 immutable baseline anchor：commit `2424f51f...`，TMX SHA-256 `e2b79085...`；
  - E8A spec binding：source commit `7144d926...`，accepted commit `da3d960...`；
  - E8B current anchor：TMX SHA-256 `291a38cc...`。
- E1 历史、E8A 已接受证据和 E8B 当前迁移三层职责已分离；未重写 E1 fixture、E8A spec/contact sheet。
- manifest/snapshot update 使用 `atomicWriteUtf8Batch`；当前 public tree 相对 E1 只允许 `hall.tmx` 一个精确 hash replacement。
- E8A verifier 默认读取冻结 Git blob；显式 `--tmx` 验证 live TMX 时继续 fail closed。

## 验证
- baseline suite：51 passing
- prop-sort suite：50 passing
- E8B migration suite：24 passing
- `npm run test:game`：698 passing
- `npm test`：1098 passing，0 failing
- `npm run validate:juyiting-map`：PASS
- `npm run build`：PASS
- `git diff --check`：PASS
- 独立 Reviewer：ACCEPT，无 P0–P3 finding

## Exit Gate
- TMX/manifest/snapshot 与 E8A 逐项一致：PASS。
- 5×N/S/W/E 与 bounty probes：PASS。
- 历史/current provenance 分离并全量测试绿色：PASS。
- 允许进入 E9A。
