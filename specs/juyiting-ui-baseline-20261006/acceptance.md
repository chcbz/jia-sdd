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
