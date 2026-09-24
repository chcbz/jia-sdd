# 聚义厅界面细节优化 acceptance

## Acceptance criteria

### 导航与键盘

- [x] 390×480 输入聚焦时，底部导航在一个渲染周期内隐藏。
- [x] 输入失焦但视口仍缩小时底栏保持隐藏；视觉视口恢复到退出阈值后，一级页面底部导航恢复。
- [x] 390×844 与 320×740 的事项详情均不显示底部导航。
- [x] 移动嵌套详情恰好显示一个可见返回入口，且由正确的 Hall/子组件 owner 提供。
- [x] 移动根级非一级弹层只显示一个关闭入口。
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

- 验证日期：2026-09-24。
- API revision：`3426f40aab364ab98519c20a66145bf076733e2c`（无代码变更，当前 `origin/develop`）。
- Web revision：`2f528d5280ca41b0dfde81d8e83178f0bce97e0c`（已推送 `origin/feature/ui-optimization`）。
- 目标测试：导航展示、体验模式、组件行为、草稿编辑器、案卷阅读器、竖屏首页测试组合，结果 `252 passing (43s)`。
- 构建：`cd web && npm run build`，Vite 生产构建通过（1257 modules transformed，49.08s）；仅保留既有动态/静态混用及大 chunk 非阻断告警。
- 浏览器矩阵报告：
  - `/tmp/cyf-juyi-audit-after-20260924/report.json`
  - `/tmp/cyf-juyi-surfaces-after-20260924/report.json`
  - `/tmp/cyf-juyi-direct-draft-20260924/report.json`
- 浏览器联系表：
  - `/tmp/cyf-juyi-audit-after-20260924/contact.jpg`
  - `/tmp/cyf-juyi-surfaces-after-20260924/contact.jpg`
- 浏览器结论：事项详情与键盘态隐藏底栏；引导态隐藏底栏；根级好汉/资料库/消息弹层仅关闭；目录和嵌套草稿仅返回；概览直达草稿仅关闭；审计视口无页面级溢出。
- 独立代码审查：APPROVE，无 P0/P1。
- 独立多模态视觉审查：APPROVE，无范围内 P0/P1。
- SDD 门禁：`./sddw pin juyiting-ui-optimization` 与 `./sddw verify juyiting-ui-optimization` 通过。
- Result：accepted。
