# Task Handoff: E9A Fragment Ownership 与 Atlas 输入规格

## 状态
- 状态：accepted
- Writer：deepseek_pro_worker / DeepSeek V4 Pro
- Visual Reviewer：vision_reviewer / GPT（只读）— `ACCEPT-V2`
- Technical Reviewer：adversarial_reviewer / DeepSeek V4 Pro（只读）— `ACCEPT`
- Base：`a700d1c57a15026a362db535f97fb6baff47e9f7`
- Accepted HEAD：`47b7242341c1353e779b56dd1bd2aaca9736e5bf`
- Commits：`672f522005b425bb4713d1865616e1a5424a194f`、`61d3da07ccaea19a5065f05d9e0b0032e60c4870`、`47b7242341c1353e779b56dd1bd2aaca9736e5bf`
- 日期：2026-08-09

## 冻结输入
- Canonical source：`public/juyiting/images/liangshan-hall-mid-occluders-v3.webp`
- Canonical SHA-256：`3e4f3f90b4d84411a844978237a7d3530bd481c37a62bcd73b9d694a7d2dd432`
- E8B current TMX anchor：`291a38cc66ebd60c8577500a5afc18ce5398570fe4c35ca66d9eebe818826a97`
- E9A generationId：`7f8bbdd8f3ca49952d0bcfceadf60a50ad998fc7033e370cbef665ee331f3d3b`

## 已交付
- Ownership model：`alpha-rle-v1`，region 仅为 `homeRegion/chunkId`，不再裁切连续像素。
- 六区：west-upper 7、center 1、east-upper 6、west-lower 8、entrance 4、east-lower 6。
- 32 semantic owners；31 single-component，1 个经 GPT 视觉确认的 east worktable 双 component owner。
- Canonical opaque ownership：248283/248283；unowned、overlap、transparent-owned、opaque cut edge 均为 0。
- destination 为 source-coordinate identity；E9B 必须只复制 ownership runs，并把 sourceRect 内其他像素清透明。
- 自包含 contact sheet 已含 32/32 legend、cards、8 个 seam/blocker inset 和全部 provenance。
- 视觉语义经过三轮 GPT 审核后冻结；E9B 不得改名、移动边界、重新归并或自行判断结构。

## 验证
- E9A suite：45 passing。
- E1/E8A/E8B 相关 suite：51/50/24 passing。
- `npm run test:game`：698 passing。
- `npm test`：1143 passing。
- `npm run build`、validator、reproducibility、`git diff --check`：PASS。
- Technical Reviewer 无 P0–P2；仅有不阻断的行尾空白 P3。

## Exit Gate
- GPT V2：`ACCEPT-V2`。
- Technical Reviewer：`ACCEPT`。
- 可进入 E9B 机械 atlas 与 RGBA 金线生成。
