# 聚义厅界面细节优化详细设计

- 状态：Ready for implementation
- 日期：2026-09-24
- 基线：Web `a70d1e013f6e7a73e4d84a311d18a26173b468c0`
- 范围：仅聚义厅前端视觉与导航行为

## 1. 用户流程

### 1.1 一级工作台

一级工作台包括：

- 办事概览 `overview`
- 事项 `tasks`
- 资料/百宝箱 `treasure`
- 我的 `mine`

在移动竖屏且无键盘、无嵌套详情时，底部导航显示。切换一级页面不改变既有业务状态。

### 1.2 嵌套详情

嵌套详情由统一展示解析器判定，而不是仅依据 `panelDepth`。解析器覆盖：

- `panelReturnPanel`：面板帧之间的父层返回。
- `formalTaskRef`：事项正式交付结果子层。
- `activeDraftEditor()?.canGoBack`：草稿材料、预览和确认子层。
- `bountyPanelRef?.canGoBack`：事项详情。
- `treasurePanelRef?.canGoBack`：宝库上传、预览和管理子层。
- `libraryPanelRef?.canGoBack`：案卷阅读、目录和笔记子层。
- `renderedPanel === 'workspace'`：事项协作工作台。
- `portraitTaskDetailOpen`：概览中的榜文详情。

`panelDepth` 只用于描述逻辑深度和测试，不单独决定按钮归属。移动竖屏嵌套详情隐藏底部导航，内容扩展到安全区底部，并确保恰好一个可见的前导返回动作。

### 1.3 根级弹层

从概览直接打开招贤令、提出需求等根级弹层时：

- 移动竖屏：隐藏底部导航，只显示关闭动作。
- 桌面居中弹层：显示关闭动作。
- 若弹层拥有明确父层，则显示返回动作并隐藏关闭动作；返回后仍可由父层关闭。

### 1.4 软键盘

用户聚焦 `input`、`textarea`、`select` 或 `contenteditable` 且视觉视口相对稳定基线缩小至少 120px 时，判定软键盘打开：

- 隐藏底部导航。
- 移除内容的底部导航预留，仅保留安全区。
- 不主动模糊输入框，不改变草稿或筛选状态。
- 失焦、视觉视口恢复、路由/方向切换后退出键盘状态。

## 2. 导航状态模型

在 `useHallPanels.js` 增加纯函数 `resolveHallNavigationPresentation()`，由 `JuyiHall.vue` 传入现有业务状态，集中解析界面 chrome。展示状态不得直接修改 `panelFrames`、草稿、阅读器、事项或工作台业务状态。

### 2.1 页面与层级

```text
isPortraitMobile = isMobileCoarse && experienceMode === 'portrait-command'
isPrimarySurface  = isOverviewHome && (renderedPanel is null or renderedPanel in {tasks, treasure, mine})
hasChildDetail    = formalTaskRef
                    or activeDraftEditor()?.canGoBack
                    or bountyPanelRef?.canGoBack
                    or treasurePanelRef?.canGoBack
                    or libraryPanelRef?.canGoBack
                    or renderedPanel === 'workspace'
                    or portraitTaskDetailOpen
hasFrameParent    = Boolean(panelReturnPanel)
```

### 2.2 返回动作归属

`canGoBack` 是能力，不代表谁渲染按钮。解析器明确输出：

```text
returnOwner = none | self | hall
```

| 子层 | returnOwner | 说明 |
| --- | --- | --- |
| Bounty 事项详情 | `self` | 已有“返回事项” |
| HallDraftEditor 内部步骤 | `self` | 保持材料/预览/确认内部返回顺序 |
| ArchiveReader 阅读/目录/笔记 | `self` | 保持笔记→目录→书架顺序 |
| 概览榜文详情 | `self` | 将现有“关闭”统一改为“返回” |
| 正式交付结果 `formalTaskRef` | `hall` | 子组件无统一返回 chrome |
| 宝库子层 | `hall` | 由 Hall 调用现有 `back()` |
| `workspace -> tasks` | `hall` | 面板帧父层返回 |
| 其他 `panelReturnPanel` | `hall` | 面板帧父层返回 |

所有 Hall 拥有的返回继续调用现有 `returnPanel()`；所有关闭继续调用现有 `closePanel()`。离开可编辑草稿帧必须继续经过 `guardPanelLeave`，草稿内部返回不得触发离开保存。

### 2.3 底栏与面板 chrome

```text
showWorkbenchDock = isOverviewHome
                    and isPrimarySurface
                    and not hasChildDetail
                    and not hasFrameParent
                    and not isKeyboardActive
```

语音锁定继续只通过 `inert`/禁用控制交互，不隐藏底栏，避免额外布局跳变。

| Surface | 移动竖屏 | 桌面/横屏 |
| --- | --- | --- |
| 一级工作台根页面 | 底栏；无返回/关闭 | 侧栏；无返回/关闭 |
| 一级工作台 self-owned 子层 | 子组件返回；无关闭 | 子组件返回；无关闭 |
| 一级工作台 Hall-owned 子层 | Hall 返回；无关闭 | Hall 返回；无关闭 |
| 非一级根弹层 | 关闭 | 关闭 |
| 非一级 self-owned 子层 | 子组件返回；无关闭 | 子组件返回 + Hall 关闭 |
| 非一级 Hall-owned 子层 | Hall 返回；无关闭 | Hall 返回 + 关闭 |
| 沉浸地图无面板 | 无底栏 | 无底栏 |

对于工作台一级面板，仍保持非模态 `region` 语义；只有 Hall-owned 子层需要显示轻量返回标题栏，不能重新引入“关闭整个一级页面”的动作。

### 2.4 安全区与底部占位

```css
--hall-safe-bottom: env(safe-area-inset-bottom);
--hall-dock-height: 62px;
--hall-dock-reserve: 0px;
--hall-content-bottom-inset: calc(var(--hall-safe-bottom) + var(--hall-dock-reserve));
```

仅 `.has-workbench-dock` 设置 `--hall-dock-reserve: var(--hall-dock-height)`。该变量统一作用于：

- `HallPortraitHome` 底部留白；
- 一级面板 overlay 的 bottom；
- 更多菜单最大高度；
- 短屏消息区域；
- 详情内容安全区 padding。

底栏显示由 `renderedPanel` 和子层状态派生，在面板关闭过渡完成前不得提前闪现。

## 3. 视觉视口与键盘检测

扩展 `useHallExperienceMode.js`，保留现有实时 `viewport` 和 `hallViewportHeight` 行为，新增仅用于展示的键盘状态：

```text
keyboardPhase = closed | open | closing
enterThreshold = 120px
exitThreshold  = 40px

closed -> open:
  editable focused AND stableHeight - liveHeight >= enterThreshold

open -> closing:
  editable focus离开，但视口仍缩小

open/closing -> closed:
  stableHeight - liveHeight <= exitThreshold
  OR 物理/展示方向 generation 明确重置
```

实现约束：

- 暴露 `viewport`、`stableViewportHeight`、`isEditableFocused`、`keyboardPhase`、`isKeyboardActive`。
- `isKeyboardActive` 在 `open` 和 `closing` 阶段均为真，防止键盘退场期间底栏提前出现。
- 稳定高度在 `open/closing` 期间不得降低；同一方向观察到更大高度时允许提高。
- 只有确认的物理方向或展示方向 generation 变化才能重建较小基线。
- 监听 `visualViewport.resize/scroll`、`window.resize`、`document.focusin/focusout`。
- `focusout` 延迟一个动画帧读取 `document.activeElement`，避免输入框之间切换时闪烁。
- 不支持 `visualViewport` 时使用 `innerHeight`，仍必须满足“编辑焦点 + 高度差”。
- 键盘状态不得修改物理方向、`experienceMode`、`requestedMode` 或面板布局；`hallViewportHeight` 继续使用实时高度。
- 组件卸载时移除监听并取消待执行动画帧。

## 4. 返回与关闭规则

`JuyiHall.vue` 消费展示解析器输出：

- `showWorkbenchDock`
- `showHallReturn`
- `showHallClose`
- `showPrimaryChildHeader`
- `returnOwner`
- `hasChildDetail`

优先级：

1. 子组件 self-owned 返回优先处理其内部状态。
2. Hall-owned 返回调用 `returnPanel()`，其中 `formalTaskRef`、宝库和 workspace 使用既有分支。
3. 非一级弹层离开调用 `closePanel()`，继续受草稿保存保护。
4. Escape 保持现有 `returnPanel()`/`closePanel()` 顺序，不新增直接栈操作。

移动竖屏返回与关闭互斥；桌面/沉浸横屏仅在非一级嵌套弹层中允许“返回 + 关闭”，两者语义分别是回父层和退出整个弹层。一级工作台无论桌面或移动均不显示关闭整个页面的动作。

## 5. 聚义厅语义设计变量

在 `.juyi-page.home-overview`（以及明确标记为 `theme-workbench` 的一级工作台 overlay）定义浅色工作台通用变量，原有 `--work-*` 作为兼容别名逐步收敛。地图模式和地图上打开的历史羊皮纸弹层不继承这些浅色值：

```css
--hall-canvas: #f5f4f0;
--hall-surface: #fffefa;
--hall-surface-subtle: #f3f3ed;
--hall-surface-brand: #f6eee8;
--hall-text: #242e2b;
--hall-text-muted: #68716b;
--hall-border: #e3e5dc;
--hall-border-strong: #ccd2c5;
--hall-brand: #923f30;
--hall-brand-hover: #793326;
--hall-positive: #36643b;
--hall-warning: #87551c;
--hall-danger: #a13f35;
--hall-info: #21604d;
--hall-radius-sm: 7px;
--hall-radius-md: 10px;
--hall-radius-lg: 12px;
--hall-control-height: 44px;
--hall-page-gutter: 16px;
--hall-focus-ring: #923f3052;
```

组件局部变量必须提供羊皮纸兼容回退，确保同一组件从地图入口打开时保持原有风格。业务状态色保留语义，不把成功、警告、失败全部改为品牌红。

## 6. Tab 与筛选规范

### 6.1 一级内容 Tab：`.hall-tabs`

用于概览、资料库等页面级内容切换：

- 高度至少 44px。
- 透明背景、底部分隔线。
- 选中项使用品牌色文字和 2px 下划线。
- 窄屏 `overflow-x:auto`，Tab 不压缩换行。

### 6.2 筛选 Chip：`.hall-filter-tabs`

用于事项状态、Agent 状态：

- 38–40px 高度。
- 未选中使用次级表面与边框。
- 选中使用品牌浅底、品牌文字与品牌弱边框，不再使用整块深红。
- 数量徽标保持同一行高。

### 6.3 详情子 Tab：`.hall-detail-tabs`

用于草稿事项内容和案卷子视图：

- 与一级 Tab 共用字体、焦点环和选中下划线。
- 允许更紧凑的水平间距，但不得小于 40px 点击高度。

为避免一次性重构组件结构，本次以 `.juyi-page.home-overview :deep(...)` 和组件局部变量兼容既有类名，后续可再抽取基础组件。

## 7. 页面细节调整

### 7.1 概览

- 页面边距统一：桌面 30–36px，移动 16px。
- 卡片、文本框与操作按钮右边线对齐。
- 输入区聚焦时保持可见，底部操作不被导航或键盘遮挡。

### 7.2 事项

- 搜索、能力筛选和动作按钮在移动端改为可换行工具区。
- 主操作与筛选操作分层。
- 状态 Chip 横向滚动，不挤成不等宽多行。
- 事项详情使用完整可视高度，底部增加安全区 padding 而不是固定 96px 导航占位。

### 7.3 宝库、资料库、好汉、招贤令、草稿和消息

- 统一输入框、按钮、卡片、分隔线、空/错状态颜色。
- 移动页面使用相同 16px 左右边距和 44px 触控尺寸。
- 草稿与招贤令不再同时显示返回、关闭、底部导航。
- 保留业务组件的结构、事件和表单验证。

### 7.4 地图与案卷阅读器

- 地图保持深色沉浸风格，只统一按钮高度、圆角和焦点反馈。
- 案卷阅读器保留现有全屏、虚拟横屏和胶囊避让逻辑；嵌入工作台时仅继承浅色语义变量。

## 8. 无障碍与交互

- 导航使用 `aria-current="page"`。
- Tab 继续使用现有 `role="tab"` 或 `aria-pressed` 契约，不在本轮强制改动事件模型。
- 所有可点击控件目标尺寸不小于 44×44px，紧凑筛选至少 40px 高并有足够横向间隔。
- 返回和关闭均保留明确的 `aria-label`。
- 键盘隐藏导航时使用条件渲染/隐藏状态，确保不可聚焦，不只做透明处理。
- 面板背景继续使用 `inert` 与 `aria-hidden` 防止焦点穿透。

## 9. API、数据、安全与兼容性

### 9.1 API

无新增或修改接口。以下契约保持不变：

- 地图：`GET /agent/map`
- 名册：`POST /agent/roster`
- 事项：`POST /agent/tasks/search`
- 指派：`POST /agent/tasks/{taskId}/assign`，显式携带 `agentId`
- 会话：既有聚义厅 stream/events 契约

### 9.2 兼容性

- 不支持 `visualViewport` 的浏览器退化为不隐藏导航或使用 `innerHeight` 联合焦点判断，不阻塞输入。
- CSS 变量提供默认值，避免嵌套组件脱离聚义厅时失去颜色。
- 不改变 URL、路由、localStorage key、草稿格式、会话 metadata 和方向桥接。

### 9.3 发布与回滚

- 仅 Web 子模块变更，可通过回退 Web commit 完整回滚。
- 无数据迁移与后端回滚步骤。
- 推送到远端 `feature/ui-optimization`，不直接合入 `develop` 或 `master`。

## 10. 验证矩阵

| 视口 | 页面/场景 | 关键断言 |
| --- | --- | --- |
| 1280×800 | 概览、事项、宝库、我的 | 侧栏、卡片和工具栏对齐，无移动底栏 |
| 390×844 | 四个一级页面 | 底栏显示且内容不遮挡 |
| 390×844 | 事项详情 | 底栏隐藏，只有一个返回入口 |
| 320×740 | 事项详情、草稿 | 无横向溢出，动作可达 |
| 390×480 | 输入聚焦 | 键盘态隐藏底栏，输入和提交按钮可达 |
| 844×390 | 地图 | 沉浸地图保持，无工作台底栏 |
| 390×844 | 招贤令/提出需求 | 返回与关闭互斥，底栏隐藏 |
| 390×844 | 资料库/消息/好汉 | 控件、Tab、边线和安全区一致 |

自动验证至少覆盖：

- 键盘状态：先聚焦后缩小、输入框间切换、失焦但视口仍缩小、延迟恢复、阈值滞回、方向重置、缺少 `visualViewport`、监听清理。
- 展示解析器：四个一级根页面、事项详情、正式交付结果、宝库子层、案卷阅读器、草稿内部步骤、workspace、`portraitTaskDetailOpen`、agents/messages/catalog 根弹层。
- 草稿未保存：移动返回、桌面关闭、Escape、保存失败、重试与放弃均保留原 pending action。
- 旋转连续性：面板、草稿和 reader 不重挂载，`hallViewportHeight` 与 `panelLayout` 继续使用实时高度。
- 既有聚义厅体验模式、组件行为、草稿、事项和案卷相关测试。
- 前端生产构建。
- 浏览器截图证明布局和层级；人工缩短 viewport 只作为布局诊断，不宣称等同真实软键盘证据。
