# 近期前端 UI 同步 · 2026-10-13

[打开原型](index.html#home) · [19页/23状态索引](pages.html) · [本轮验收](../acceptance.md) · [固定源码来源](baseline-source.json)

本轮以 Web `cb730681570688e0051b5cd79737a3c004817881`（tree `6e4620d9c55600f4f4376c4964c839d8cccdc9d0`）为只读来源：
- 同步取消区间距/全宽按钮、确认/保留/未知只核对；取消终态禁发送、点将、改稿及验收。
- 正式成果改为独立页面 P19；隐藏页面工作空间入口（保留全局资料导航），历史成果双重读按钮窄屏纵排。
- 招贤令补 Runtime v1 接应说明、首次登记/已有安装仅查询/未知/材料不匹配状态；真实文件导入禁用，只载入脱敏 fixture。不运行安装、enroll、注册、支付或复制秘密。
- 事项工具栏同步为搜索/本领/刷新单行，移除重复的榜内创建入口；点将册按钮顺序沿用已有设计。复核发现旧 P03 虽有独立地址，内部仍为任务榜内嵌表单；本轮已替换为 HallDraftEditor 的独立草稿编辑、保存、资料/格式、选人授权和回执样式。私人交办仅本地示例，不创建悬赏事项、不写入账号。

这是**局部源码同步的离线交互原型**，不是全站逐像素重建或线上发布证明。旧截图/报告与未重建外壳仍属于 10 月 6–7 日基线；历史 R01 等场景不据此重判当前产品能力。新证据在 `../evidence/ui-sync-20261013/`，旧报告不覆盖。原型场景存储键已更新，旧演示状态不混入新版本。

复用下方既有预览及检查命令。检查工具的新报告默认写入本轮 evidence 目录；可通过 `PROTOTYPE_EVIDENCE_DIR` 显式指定新证据目录，通过 `PROTOTYPE_ORIGIN` 指向自己启动的预览端口。

---

## 以下为 2026-10-07 历史说明（不代表本次同步范围）

# 优化界面原型 · 交互补全 2026-10-07

[打开原型](index.html#home) · [18页/15状态索引](pages.html) · [交互说明](../interaction-guide-20261007.md) · [浏览器证据](../acceptance.md)

这份原型在10月6日最新优化基准原地补全，是后续提出新需求的唯一界面入口。离线示例，不是生产应用、上线事实或真实业务通过；R01仍待实现。

保留圆角选中标签。议事顶部三个话头图标靠右；输入栏左侧为＋/添加资料图标，右侧为语音/发送图标，＋内仅保留语音回答设置，资料入口外置。不启用麦克风、不读取账号、不连接API。状态按场景保存在当前标签页，普通刷新保持；索引链接reset=1只重置该场景一次。

静态预览：执行 `python3 /home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/tools/serve-preview.py --port 18766`（Python 3.6兼容、多线程处理本地资源）。

轻量检查：`node /home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/tools/check-prototype.mjs`。真实浏览器：服务启动后 `node /home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/tools/check-browser.cjs`，只启动并清理自己的临时Chromium，不运行构建或真实业务。

索引/样式浏览器核验：`node /home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/tools/check-index.cjs`。

议事图标统一20px、1.8px描边，点击区域统一38px。定向浏览器检查：`node /home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/tools/check-icons.cjs`。

## 正式环境对照（2026-10-07）

[本轮差异报告](../production-diff-20261007.md)：真实页面与当前唯一原型分开取样，记录未同步提案、完成态/正文重复问题与生产更完整模块；不代表再次业务验收或上线。
