# 极窄／极短复排 · 候选布局预检（非实际缩放验收）

对象：Web 候选 `8f47a1289bf501616ba234638192a5303d3155d7` 的 `/juyiting` 实际 Vue 页面。使用本机 Chromium 142、Python Playwright；单纯把 CSS 视口缩至原四尺寸一半，DPR 设为 2，配合**合成且不联网的本地 token**与空 `/api` 响应。**这是 200% 等效复排预检，不是 Chrome 真的调到 200%、系统软键盘、真实账户或指定 Chrome 133 CI 验收。**

|CSS 视口 (截图物理分辨率)|页头/菜单/底栏|议事消息区高|输入可达性|
|---|---|---:|---|
|160×370（320×740）|均在视口内；底栏前三项只显示图标但保留中文 `aria-label`；右下“典籍阁”保留可见文字|62.06px|工具栏内部横向滚动至末项可聚焦；输入底缘≤底栏顶缘|
|195×422（390×844）|同上|97.06px|工具栏可滚动、输入不被底栏遮挡|
|422×195（844×390）|均在视口内|100px，位于工作窗滚动内容里|视口高度不足以同时显示完整标题/消息/输入；工作窗可滚动至输入与发送按钮，底栏不压住按钮|
|720×450（1440×900）|均在视口内|129.06px|消息区独立滚动、输入底缘与底栏顶缘对齐|

四尺寸均无 document 横向溢出；脚本先比对本地 `web` HEAD 为 `8f47a12`，再对实际渲染的导航逐项检查命中区域非零、`aria-label`、前三项文字在 ≤240 CSS px 隐藏而末项“典籍阁”文字可见；这并非 Vite 服务源码的密码学身份校验；菜单末项滚动后可聚焦，对话框 `aria-labelledby` 仍取得“厅内议事”。原始值在 [`compact-reflow-fixture.json`](compact-reflow-fixture.json)；同步截图：[160×370（物理320×740）](compact-reflow-160x370.png)、[422×195（物理844×390）](compact-reflow-422x195.png)。截图使用空 API，因此没有真实消息，不能用来判定长对话或服务故障。

复现：在工作树启动 `cd web && npm run dev -- --host 127.0.0.1 --port 61360 --strictPort`，从仓库根运行 `python specs/juyiting-lightweight-workbench/tools/check-compact-reflow.py --url https://127.0.0.1:61360 --out /tmp/cyf-compact-reflow.json --screenshots /tmp/cyf-compact-screens`；若需重采提交内截图，将 `--out`/`--screenshots` 改为本目录目标路径。脚本仅接受 loopback 入口；跨源请求优先中断，同源所有 XHR/fetch（包括 `/chat`、`/agent` 等）在浏览器拦截为空响应且阻止网页 Service Worker，**不发送真实身份、不会执行真实写请求**。本地七份相关组件测试 **146 passing**、`npm run build` 通过；独立只读审查另复验 146 passing、四视口 JSON/截图可重复生成且一致，但**未独立重跑 build**。真机软键盘/实际缩放与受控 amd64 全量测试仍待进行。
