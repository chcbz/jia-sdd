# 优化界面原型 · 交互补全 2026-10-07

[打开原型](index.html#home) · [18页/15状态索引](pages.html) · [交互说明](../interaction-guide-20261007.md) · [浏览器证据](../acceptance.md)

这份原型在10月6日最新优化基准原地补全，是后续提出新需求的唯一界面入口。离线示例，不是生产应用、上线事实或真实业务通过；R01仍待实现。

保留圆角选中标签。议事顶部三个话头图标靠右；输入栏左侧为＋/添加资料图标，右侧为语音/发送图标，＋内仅保留语音回答设置，资料入口外置。不启用麦克风、不读取账号、不连接API。状态按场景保存在当前标签页，普通刷新保持；索引链接reset=1只重置该场景一次。

静态预览：执行 `python3 /home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/tools/serve-preview.py --port 18766`（Python 3.6兼容、多线程处理本地资源）。

轻量检查：`node /home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/tools/check-prototype.mjs`。真实浏览器：服务启动后 `node /home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/tools/check-browser.cjs`，只启动并清理自己的临时Chromium，不运行构建或真实业务。

索引/样式浏览器核验：`node /home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/tools/check-index.cjs`。
