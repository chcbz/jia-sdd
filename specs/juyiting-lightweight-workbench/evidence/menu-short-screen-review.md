# “全部入口”展开态 · 本地候选极窄屏复核

对象：Web 提交 `a9354407c3216efe75a16959afe522bb127e1a19`；本地 HTTPS Vite `/juyiting`、系统 Chromium 142.0.7444.175（默认查找可执行文件，支持 `--chromium`，**不是** CI 固定 Chrome 133）。仅用短时**假本地 token**与空 `/api` 响应检查 Vue 布局，没有真实账号数据/写 API。本轮将菜单宽度由 `100vw` 改为相对定位祖先 `.juyi-page` 的 `100%`（兼容经典滚动条占据的视口宽差）；浏览器确认该祖先运行时 `position:relative` 且是菜单 `offsetParent`，实测菜单宽 `min(330px, 容器宽 - 30px)`。原 28 场景 CSSOM 采的是菜单关闭态，不能推断展开布局合格。

发现并修复：修复前 320×320 展开菜单 `x=-11..305`、`y=62..325.75`，左右超出视口且下方与底栏重叠；原因为菜单声明的 290px 是 content-box，另加 24px padding + 2px border，且没有最大高度与内部滚动。现在改为 `border-box`、与页头对齐（常规 top64，矮屏 top58）、最大高限于页头与底栏之间并自行滚动。

|视口 CSS px|修复后菜单 x 左..右|y 顶..底|底栏顶缘|滚动内容/窗口高度|
|---|---:|---:|---:|---:|
|320×320|15..305|58..258|258|262/198|
|320×740|15..305|64..328|678|262/262|
|390×844|45..375|64..328|782|262/262|
|640×390|295..625|58..321.75|328|262/262|
|720×450|375..705|58..321.75|388|262/262|
|760×390|415..745|58..321.75|328|262/262|

复现：从本工作树执行 `cd web && npm run dev -- --host 127.0.0.1 --port 61360 --strictPort`，再从仓库根运行 `python specs/juyiting-lightweight-workbench/tools/check-mobile-menu.py --url https://127.0.0.1:61360 --out /tmp/cyf-menu-candidate.json --screenshots specs/juyiting-lightweight-workbench/evidence`。脚本只允许 loopback、隔离假 token/空 API 并阻断非本地请求；依赖本机 Python Playwright 与系统 Chromium（可用 `--chromium` 指定路径），不是固定版本 CI；不强制关闭浏览器沙盒。

六个视口全部：10 个菜单按钮均存在；document 水平 `scrollWidth` 不超过视口；菜单始于页头下、终止于底栏前；滚动后最后按钮能取得键盘焦点。原始值见 [`menu-short-screen-fixture.json`](menu-short-screen-fixture.json)，当前候选截图 [`320×320`](menu-candidate-320x320.png) 与 [`640×390`](menu-candidate-640x390.png) 由上述脚本与 JSON **同次**生成；320×320 截图滚到底部，辅助入口可见。历史截图 [`320×320`](menu-short-screen-320x320.png) 与 [`640×390`](menu-short-screen-640x390.png) 仍归属上一提交 `4feaa7d`，不混作本轮证据。当前候选七份相关测试合计 145 passing（单份 89 passing 属上一 SHA，当前未单独重跑），Web `npm run build` 通过；真实键盘/安全区、授权状态和固定浏览器全量仍未验收。旧 28 场景的控件 CSSOM 仍属于前序 `fe43ebc5`，不混作本轮重新测量。

独立只读复核确认 Web 菜单包含块、断点及 CSS 规则，无 P0/P1；提出的本候选截图无法复产、定位祖先断言不足已由可重跑脚本和同批候选 PNG 补齐。另两条 P2 涉及原始工作区 `/home/chc/wsps/cyf` 未提交的 `juyiting-unified-experience` 文档更改，**不是本独立 worktree 的改动**，保留原工作区用户修改不跨分支修复。此审查不替代业务验收。
