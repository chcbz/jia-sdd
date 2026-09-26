# 聚义厅界面细节优化 acceptance

## Acceptance criteria

### 导航与键盘

- [x] 390×480 输入聚焦时，底部导航在一个渲染周期内隐藏。
- [x] 输入失焦但视口仍缩小时底栏保持隐藏；视觉视口恢复到退出阈值后，一级页面底部导航恢复。
- [x] 390×844 与 320×740 的事项详情均不显示底部导航。
- [x] 移动嵌套详情恰好显示一个可见返回入口，且由正确的 Hall/子组件 owner 提供。
- [x] 移动竖屏根级非一级弹层只显示一个 `← 返回` 入口，且点击后关闭根级弹层。
- [x] 隐藏底栏后内容使用释放的空间，提交操作不被安全区遮挡。

### 视觉与布局

- [x] 浅色工作台页面使用同一语义色板、边框、圆角和焦点环。
- [x] 页面 Tab、筛选 Chip 和详情子 Tab 各自样式一致。
- [x] 移动端主要控件点击高度至少 44px。
- [x] 320px 宽度下无页面级横向溢出。
- [x] 地图继续使用深色沉浸风格且不显示工作台底栏。
- [x] 案卷阅读器的安全区和胶囊避让无回退。

### 回归

- [x] 地图/名册数据隔离契约保持通过。
- [x] 任务指派继续显式传入目标 Agent。
- [x] 草稿未保存保护、面板焦点陷阱和焦点恢复保持通过。
- [x] 聚义厅相关目标测试通过。
- [x] 前端生产构建通过。

## Verification evidence

- 当前验证日期：2026-09-25。
- API revision：`3426f40aab364ab98519c20a66145bf076733e2c`（无代码变更，当前 `origin/develop`）。
- Web revision：`d79af65ed0c493b31a82f8d26206b949ea662bf4`（已推送 `origin/feature/ui-optimization`）。
- 目标测试：导航展示、体验模式、组件行为、草稿编辑器、案卷阅读器、竖屏首页测试组合，结果 `252 passing (43s)`。
- 构建：`cd web && npm run build`，Vite 生产构建通过（1257 modules transformed，49.08s）；仅保留既有动态/静态混用及大 chunk 非阻断告警。
- 浏览器矩阵报告：
  - `/tmp/cyf-juyi-audit-after-20260924/report.json`
  - `/tmp/cyf-juyi-surfaces-after-20260924/report.json`
  - `/tmp/cyf-juyi-direct-draft-20260924/report.json`
- 浏览器联系表：
  - `/tmp/cyf-juyi-audit-after-20260924/contact.jpg`
  - `/tmp/cyf-juyi-surfaces-after-20260924/contact.jpg`
- 浏览器结论：事项详情与键盘态隐藏底栏；引导态隐藏底栏；初始根级好汉/资料库/消息弹层仅关闭；目录和嵌套草稿仅返回；概览直达草稿仅关闭；审计视口无页面级溢出。
- 独立代码审查：APPROVE，无 P0/P1。
- 独立多模态视觉审查：APPROVE，无范围内 P0/P1。
- SDD 门禁：`./sddw pin juyiting-ui-optimization` 与 `./sddw verify juyiting-ui-optimization` 通过。
- Result：accepted。


## 2026-09-25 圈选细节复核

- 范围：仅复核用户圈选的聚义厅移动端细节，不扩展到其他页面。
- 一句话需求：字数计数固定在输入框右下角，预留底部空间并增加实色衬底；输入框不再出现与计数重叠的拖拽手柄。
- 事项与百宝箱 Tab：活动项统一为透明背景、品牌红文字和 2px 下划线；百宝箱窄屏允许横向滚动。
- 草稿主操作：`下一步：确认交办` 在 390px 竖屏独占整行且不换行。
- 文件预览：版本标签、选择器和下载按钮使用明确网格布局，390px 下无横向溢出。
- 详情导航：Hall 与事项详情统一显示 `← 返回`；文件预览和事项详情保留对应页面标题，返回按钮高度 44px。
- 目标测试：5 个受影响测试文件，结果 `131 passing (57s)`。
- 构建：`cd web && npm run build` 通过（1257 modules transformed，47.74s）；仅有既有动态/静态导入与大 chunk 非阻断告警。
- 浏览器证据：`/tmp/cyf-juyi-highlighted-20260925/report.json`、`01-overview.png` 至 `06-draft-action-bottom.png`。报告确认计数位于输入框内、Tab computed style 正确、版本区无溢出、返回按钮 44px、CTA 不换行、页面无横向溢出。
- 独立只读审查：ACCEPT，无 P0/P1；审查提出的计数衬底和主题变量 P2 已收敛，真实渲染风险由浏览器 smoke 覆盖。


## 2026-09-25 根级弹层返回统一

- 移动竖屏的点将册、招贤令、消息、会话、提出需求等非一级根级弹层统一显示单一 `← 返回`，不再同时或单独显示关闭图标。
- 根级返回的无障碍名称为“返回聚义厅”，点击复用 `closePanel()`；嵌套详情仍显示“返回上一层”并调用 `returnPanel()`。
- 桌面/横屏根级弹层继续保留关闭按钮；移动竖屏返回与关闭保持互斥。
- 草稿保存保护、语音交互锁、Escape、焦点陷阱与焦点恢复路径保持不变。
- 目标测试：导航展示、组件行为、地图预览桥接与语音会话四个文件，结果 `133 passing (33s)`。同时补齐相关测试 harness 的最新生产依赖。
- 构建：`cd web && npm run build` 通过（1257 modules transformed，约 1m06s）；仅有既有动态/静态导入与大 chunk 非阻断告警。
- 浏览器证据：`/tmp/cyf-juyi-root-return-20260925/report.json` 与 `01-agents-root-return.png`；确认返回文案、`aria-label=返回聚义厅`、44px 高度、透明品牌色样式、无关闭按钮且点击后弹层关闭。
- 独立只读复核：ACCEPT，无 P0/P1。
