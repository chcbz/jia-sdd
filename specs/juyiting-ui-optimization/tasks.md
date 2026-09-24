# 聚义厅界面细节优化 tasks

## API (`api/`)

- [x] 确认无 API、数据库、鉴权或事件契约变更。
- [x] 集成时记录当前 API revision：`3426f40aab364ab98519c20a66145bf076733e2c`。

## Web (`web/`)

### W1 导航与键盘（P0）

- [x] 在 `useHallExperienceMode.js` 增加带滞回的稳定视觉视口和软键盘 phase 状态。
- [x] 在 `useHallPanels.js` 增加纯展示解析器，并在 `JuyiHall.vue` 接入一级页面、详情、return owner、底栏和返回/关闭状态。
- [x] 将移动内容底部留白改为 CSS 变量驱动。
- [x] 确保软键盘、详情和非一级弹层隐藏底栏。
- [x] 确保移动返回与关闭互斥。

### W2 视觉规范（P1）

- [x] 增加聚义厅浅色语义设计变量和兼容别名。
- [x] 统一概览、事项、宝库、好汉、资料库、草稿、招贤令和消息的浅色表面与控件。
- [x] 保持地图深色沉浸主题边界。

### W3 Tab、对齐与密度（P1/P2）

- [x] 统一页面 Tab、筛选 Chip、详情子 Tab。
- [x] 统一移动页面 16px 边距和至少 44px 主触控目标。
- [x] 压缩事项移动工具区并保证横向滚动/换行。
- [x] 修正详情底部留白、安全区和短屏滚动。

### W4 测试

- [x] 新增底栏可见性、键盘检测和返回/关闭契约测试。
- [x] 运行相关聚义厅测试：252 passing。
- [x] 运行 `npm run build`：通过。
- [x] 浏览器回归验证设计矩阵并保留截图/报告。

## Integration and verification

- [x] 独立只读审查实现和测试覆盖。
- [x] 修复审查发现。
- [x] 提交并推送 Web `feature/ui-optimization`（`2f528d5280ca41b0dfde81d8e83178f0bce97e0c`）。
- [x] 使用 `./sddw pin juyiting-ui-optimization` 固定 API/Web revisions。
- [x] 使用 `./sddw verify juyiting-ui-optimization` 通过集成门禁。
- [x] 更新 `acceptance.md` 和 `integration.yaml`。
- [x] 提交并推送根仓库 `feature/ui-optimization`。
