# 地图破图排查：旧 Vite 服务缓存（2026-09-23）

场景：本地空 API 浏览器从概览进入地图，再返回概览。不能代替真实后端地图快照/模拟/声音验收。

1. 旧端口 8890 的 Vite 进程启动于 20:56；`public/juyiting/images/occluders/east-upper-v2.png` 写入时间为 21:39。旧进程返回 `HTTP 200 text/html`（Vite index fallback），页面捕获 `drawImage` 输入 `HTMLImageElement src=/juyiting/images/occluders/east-upper-v2.png complete=true naturalWidth=0`，堆栈来自 `HallScene.js` 片段渲染第 1873 行。磁盘源 PNG 由 PIL 核实可解码为 534×425。
2. 22:25 另起全新同 worktree Vite 8891：相同 URL 返回 `HTTP 200 image/png`，`Content-Length: 131700`。Playwright/Chromium 142 中 `Image.decode()` 返回 naturalWidth=534、naturalHeight=425；进入地图后 `.hall-stage` 与 canvas 各 1；返回概览后 Stage 仍同一 DOM 实例；捕获 `pageerror/console error/requestfailed` 均为空（探针日志 `/tmp/cyf-wb-map-smoke-8891.log`）。测试后已停止新服务。
3. 源和 production `dist/juyiting/images/occluders/east-upper-v2.png` 的 SHA256 均为 `d3692591b3759e377f4a87c6e818148fd51077210ea1c29f5061acaefc10b846`。**原因**：复核期间旧开发服务所见静态文件缓存过期，并非本次工作台引入的图片路径改变；可用重启开发服务重现修复，仍需真实环境回归素材加载。
4. 进一步运行同一构建产物 `vite preview`（8893）：PNG 同样返回 `image/png`/131700 bytes；本地路由拦截空 API 时进入实景 Stage+canvas 各1、`Image.decode()` 534×425、返回概览 Stage 同实例；真实运行时未观测到 `pageerror`。生产环境需要正确的 API origin/证书与真实授权；此项不覆盖这些业务联通性。另在构建产物的 390×844 页面上从“全部入口”首次打开“百宝箱”后关闭，Playwright 确认焦点返回 `button[aria-label="全部入口"]`，页面错误为空。
