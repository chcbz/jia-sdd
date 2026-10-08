# 图标一致性定向复验 · 2026-10-07

当前原型已统一：**20×20px SVG、1.8px描边、38×38px点击区域**。＋不再使用字体字符；发送保留强调色，但尺寸与其他图标一致。仅原型修订，不改Web/API或发布。

- 真实Chromium定向16组、11项布局检查通过：1440/390/320下三种会话的七个操作图标均实测为20px、按钮38px；工具栏仍靠右且同排。
- 原生点击＋菜单、直接添加资料、语音停止/取消均保留草稿；等待与完成状态禁用保持，未记录异常或外部请求。
- 新一轮72项文档检查通过。报告：[本轮定向浏览器](prototype/icon-consistency-checks-20261007.json)、[本轮文档检查](prototype/prototype-checks.json)。
- 下方31组/70布局属于上一轮简化版证据，保留原source hashes，不改记为本轮全面验收。修订前文档/截图保存到checks-history/before-icon-consistency-*。

---

# 厅内议事简化复验 · 2026-10-07

本轮为用户截图提出的**离线原型新提案**，不是Web上线。完成：上部三个话头图标靠右且不另占整行；底部左侧＋/资料回形针，右侧语音麦克风/发送；资料入口外置，＋不再重复显示资料；图标保留名称、焦点及禁用反馈。

- 实际Chromium全流程复验31组、70项布局检查通过，1440/390/320三种宽度均验证新的工具栏同排与输入操作顺序；无脚本异常或外部请求。
- 72项轻量文档检查通过；资料选择、语音草稿、话头记录、会话隔离、成果与验收恢复均保留。
- 旧历史样式的窄屏单列覆盖已定位并用当前原型局部样式修正；不改冻结source-ui.css、hall-view-tabs.css与共享来源。失败记录保留在checks-history，不改记PASS。
- 最新截图：[手机议事](prototype/screenshots/390-chat.png)、[桌面议事](prototype/screenshots/1440-chat.png)；报告仍为prototype下本轮重新生成的browser-checks-20261007.json与prototype-checks.json。修订前记录见checks-history/before-chat-simplification-*。

新布局以 [design.md的厅内议事简化提案](design.md) 为准；下方交互补全说明保留历史。真实业务R01仍待实现，没有API/Web构建、部署或业务能力完成结论。

---

# 交互补全验收 · 2026-10-07

## 本轮结论

**离线原型补全通过；真实产品业务仍 NOT_COMPLETE，不是发布。** 唯一基准为本目录 `prototype/index.html`，不是多媒体SDD中的历史 `complete-20261007`。

- 真实 Chromium 133：18页 × 桌面1440/手机390/窄屏320；31组交互检查、70项布局检查通过。
- 检查无横向溢出、可见破图；输入区文本/按钮纵向排列且共享边界；保留三个顶部话头操作和优化标签。
- 原生点击覆盖附件-only创建、取消/确认、同事项澄清、成果预览/示例下载/音频播放、引用修改、可选保存、详情验收、完成后刷新只读。
- 创建失败/未知、发送待核对、验收失败/未知均不自动重复写入；保留草稿、原操作及冻结成果。等待刷新不自动重发，录音示意取消恢复可编辑。
- 公议/每Agent密议/正式事项隔离，话头快照与恢复，资料重命名/回收/恢复，检索空态/结果与阅读书签/手札持久化均通过。
- R01独立root关联恢复仍被明确阻塞，不能点击完成验收。
- JSDOM轻量文档检查72项通过；补充3组浏览器索引/样式检查，18页/15状态的链接经HTTP核验有效，选中态实际计算样式为8px圆角/浅色背景/无下划线。脚本语法检查通过。
- 记录中的脚本异常0、外部请求0；所有业务模拟均离线。未执行应用构建、Flow、部署、API、Agent、Provider或真实麦克风。

证据：[浏览器报告](prototype/browser-checks-20261007.json) · [轻量报告](prototype/prototype-checks.json) · [索引/样式核验](prototype/preview-checks-20261007.json) · [桌面议事截图](prototype/screenshots/1440-chat.png) · [手机议事截图](prototype/screenshots/390-chat.png)。截图是本地示例，不是当前线上采样。

## 复验方式

启动本目录的 `tools/serve-preview.py`，然后运行 `tools/check-browser.cjs`。索引补充检查为 `tools/check-index.cjs`，轻量检查为 `tools/check-prototype.mjs`。浏览器检查只启动、操作和关闭自身临时Chromium；源码/资源摘要绑定本次报告，原冻结共享资源及source-ui.css/hall-view-tabs.css不改。

修复了旧布局选择器压窄文本区、页面切换清存储与pagehide竞争、录音取消未解锁。测试侧修正了弹窗后点击后台同名按钮的选择器以及固定延迟导致的reload初始化竞态；预览改用多线程静态服务。失败/历史记录保存在checks-history，未改记为PASS。

## 限制及后续

不声称真机、软键盘、真实SSE/重连、账号权限、Agent/Provider、支付、数据库事务、真实典籍同步或实时地图通过。目标交互演示与实现能力分别记录；新需求可按P/S编号提出。R01及完整真实业务验收继续见多媒体SDD待办。

---

## 下方为10月6日历史验收（不代表本轮）

# 文档原型自检（2026-10-06）

## 已完成

- 原型、CSS、脱敏 DOM 与素材均保存在 SDD 目录，无 `/var/tmp` 或独立工作树运行依赖。
- 18 个页面 × 手机/桌面两种 viewport：36 项 DOM / 图片资源检查通过。
- 9 个议事状态检查通过，包括四项最新布局、等待/错误/录音/成果状态。
- 3 组交互链检查通过：＋/资料/历史/语音草稿；多媒体/详情/验收；我的/典籍/资料管理。
- 合计 **48 项轻量文档原型检查通过**，原始记录：[prototype-checks.json](prototype/prototype-checks.json)。
- JavaScript `node --check`、新增文件 whitespace 检查、内部入口和 CSS 静态资源路径检查通过。
- 精确 Web commit/tree、源文件 SHA-256、历史 DOM 来源、最新议事改动和补充结构页边界均已保存。

## 命令

```bash
node specs/juyiting-ui-baseline-20261006/tools/check-prototype.mjs
node --check specs/juyiting-ui-baseline-20261006/prototype/prototype.js
node --check specs/juyiting-ui-baseline-20261006/prototype/baseline-ui.js
```

## 限制

- 本次使用 JSDOM 检查 DOM 和模拟交互；设置两个 viewport 不等于已经完成 Chromium 的 CSS 排版、截图或真机适配验证。
- 当前机器的既有 Chromium launcher 指向不存在的二进制，未安装新浏览器，也没有把历史截图改记为本次通过。
- 新补充页面是当前源码入口/字段对齐的结构原型，不承诺逐像素还原。请在后续对应页面视觉优化前补最新组件截图。
- 文档保存不代表最新 Web 已上线，未执行本任务的 Flow Run、生产构建或部署；没有改变 API/Web gitlink，也没有产品功能 accepted/released 结论。

## 同类标签修订自检 · 2026-10-06

- 本次重新检查 **49 项文档原型检查通过**（新增共享样式资源与百宝箱选中态检查）；原始 48 项基准记录保存到 `checks-history/prototype-initial-20261006.json`，不改记为本次验证。
- 前端轻量定向诊断：5 项共享样式/编译检查及 37 项首页、详情、资料执行组件检查，共 **42 项通过**。这不是 Flow 正式测试或视觉截图验收。
- 对比父提交确认四个组件 template/script/scriptSetup 内容不变；仅引入 scoped CSS。原型及源码共享样式一致。
- 开发提交及云端结果见 `implementation-checks.json`；本次不部署，不把 develop 合入或制品成功报告为已上线。

## 产品 UI 版本发布追加验收 · 1.0.6

这是后续真实产品发布，不改变上方离线原型及历史“未部署”的范围。Flow4403172/Run180 以 `ee6ca1b6beba562e0c7fa13d422857f554644471` 完成扫描、3181通过/2pending/0失败、构建、同Run制品与正式部署，部署单70689069单机Success/healthy。完整364文件安装/公网HTTPS字节匹配，登录正式页面后1440/390/320七图标尺寸与点击区、顺序、手机同排、资料直接打开及＋菜单通过；没有发送、录音、Provider、任务创建或验收动作。原始证据见 [发布记录](release-1.0.6.md)。完整业务仍NOT_COMPLETE；R01、重复正文与完成态恢复未修改。
