# 连续议事原型检查 · 2026-10-16

最新方向：一条连续议事主线。修改的是原有 `../../prototype/`，没有新增应用或第二套交互原型。

- `baseline.json`：根 commit/tree 和修改前原型摘要；原修改备份在相邻旧轮证据目录，不覆盖无关修改。
- `prototype-checks.json`：93 项 JSDOM 文档/交互检查。
- `browser-checks.json`：12 组原生 Chromium 操作，21 布局记录。
- `regression/browser-checks.json`：12 组既有近期回归，66 布局记录，与专项有重叠。
- `screenshots/`：现有桌面与手机界面的结果、澄清、修改及入口截图。
- `resolved-diagnostics/`：修复前手机输入区附加提示挤压布局的诊断；已修复，最新通过报告为准。

全部为离线固定示例，没有 API/Provider 调用，没有收费或产品发布。没有复用被用户否定的双起点候选作为当前通过证据。
