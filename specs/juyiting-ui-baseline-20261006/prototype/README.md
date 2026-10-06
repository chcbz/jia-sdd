# 聚义厅当前源码界面基准 · 2026-10-06

[打开原型](index.html#home) · [页面与状态入口](../coverage.md) · [最新议事成果状态](index.html?scenario=results#chat) · [来源](baseline-source.json)

这是保存到 SDD 的离线界面基准，不是生产应用、不证明上线。复用历史脱敏页面外壳，同步当前源码中的议事布局，并补全代表性入口/状态；各区域还原层级见 [设计约定](../design.md)。不是一次完整的最新线上重新采样。

## 使用

- 桌面沿用侧栏，手机沿用办事 / 事项 / 资料 / 我的底栏。更多入口从既有“全部入口”打开。
- 从首页提出需求、选资料、点将并议事；在会话查看/下载/保存/引用示例成果，通过事项详情进入验收。
- 议事顶部保留三个话头操作；输入框内有＋、语音和发送；＋展开添加资料、语音设置，无“工作空间”按钮。
- 同类下划线视图标签统一采用浅色圆角选中态；`hall-view-tabs.css` 对齐本次开发实现，原始源码 pin 不改写，开发与验证记录见 `../implementation-checks.json`。
- 所有反馈和存储都是本原型的脱敏演示。图片为示意 SVG，音频为示意音；录音不会启用麦克风。
- 素材/CSS/脚本均在本目录。建议用静态 HTTP 服务打开；不依赖 `/var/tmp`、工作树或线上资源。

```bash
cd /home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/prototype
python3 -m http.server 18766 --bind 0.0.0.0
```

## 自检

从项目根目录：

```bash
node specs/juyiting-ui-baseline-20261006/tools/check-prototype.mjs
```

此命令只读原型、执行轻量 JSDOM 演示交互并写检查记录，不运行 Vite/生产构建或真实业务。记录见 `prototype-checks.json`；它不是 Chromium 截图或真实设备视觉验收。后续修改后必须更新来源/摘要，不能沿用旧 PASS。
