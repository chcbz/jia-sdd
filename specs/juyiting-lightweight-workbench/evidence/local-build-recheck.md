# 当前候选本地生产构建复核（不是部署/全量门禁）

对象：Web HEAD `8f47a1289bf501616ba234638192a5303d3155d7`。在独立 worktree 的 `web/` 运行 `npm run build`，**exit 0**、`vite build` 完成耗时 45.05s；仅有动态/静态导入及超过 650kB 的 chunk 警告（本次懒加载 `JuyiHallEntry` JS 946739 B）。本机为 aarch64，不能据此推断固定 amd64/Chrome133 的 CI 测试、扫描或部署通过。

|构建资源（本次实际 `dist/static`）|字节数|SHA-256|
|---|---:|---|
|`JuyiHallEntry-0rIVEhN6.js`|946739|`db81cecc72c2d4cc70ccebde6e52f6a5106537aaaf547d73c2fc8672916e45aa`|
|`JuyiHallEntry-B1dY6iu6.css`|213849|`d0a6e1733a151253052ec6b94892c7f51fedc4c335e3bd0d14b400dd65c24131`|

源代码标签“办事概览、我的事项、厅内议事、典籍阁、点将册、百宝箱、厅中实景”均存在于本次懒加载 JS，`workbench-mobile-nav`、`hall-messages` 规则存在于对应懒加载 CSS。字符串/规则存在只证明**打包内容**，不是业务可达、服务读写或真机可用的证据；业务布局证据仍见 `ui-detail.md` 与此前隔离浏览器检查。构建期间自动生成的 `web/src/components.d.ts` 已核对为 Vite 开发产物，并从 Web HEAD 恢复；未改动前端源码。构建命令的 stdout/stderr（Vite 摘要）保留 `/tmp/cyf-workbench-current-build.log`（SHA-256 `5ba7dd539eb87cd65a5b65a22cb793ecb889adfe45db7c3e6bfad099d934c9b3`），未提交打包文件或无关仓库改动。

只读 Flow SDK 查询在 `2026-09-23T20:18:25.677Z`（UTC）列出最近六次运行，最新仍为 **147 / FAIL**；随后在 `2026-09-23T20:18:29.327Z` 读取该运行详情，来源为 `develop`、提交未知，两个作业 FAIL，**不是**本候选。保留经字段筛选的[只读查询摘要](flow-readonly-snapshot.json)；没有保存带凭证的请求或未筛选原始响应。列表限于最近六次，不能由此排除更早的候选运行，但分支触发过滤器不含本分支，也没有取得本候选的无部署门禁结果。未触发、重试或修改任何流水线；安全扫描、固定浏览器全量测试及授权真实服务联调仍待执行，`integration.yaml` 保持 `implementing`。
