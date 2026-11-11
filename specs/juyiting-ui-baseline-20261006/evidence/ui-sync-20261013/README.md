# PROTOTYPE-UI-SYNC-20261013 · 离线 UI 同步证据

## 固定范围

- 来源：Web `cb730681570688e0051b5cd79737a3c004817881` / tree `6e4620d9c55600f4f4376c4964c839d8cccdc9d0`。
- 候选：`candidate-source-hashes.json`；最终检查必须前后哈希一致。来源文件摘要另见 `../../prototype/baseline-source.json#ui_sync`。
- 目标：事项搜索/本领/44px刷新紧凑工具栏，移除重复创建；普通取消区布局/确认/未知查询；已取消历史双重读按钮/只读；独立正式成果不显示 panel-workspace-link；招贤令 Runtime v1 文书、首次登记/已有安装查询/未知/非法材料示例。
- 点将册按钮保留回归；P03 从旧榜内表单替换为 HallDraftEditor 私人草稿/保存/确认交办/回执界面。不是全站逐像素镜像，不重判当前产品所有能力。
- 唯一 Owner：本聊天；handoff `docs/implementation/handoffs/PROTOTYPE-UI-SYNC-20261013.md`。

## 复用命令

在项目根目录运行既有静态服务，端口 18773 为本任务所建，仅用于本轮检查：

```sh
python3 specs/juyiting-ui-baseline-20261006/tools/serve-preview.py --port 18773
node specs/juyiting-ui-baseline-20261006/tools/check-prototype.mjs
PROTOTYPE_ORIGIN=http://127.0.0.1:18773 node specs/juyiting-ui-baseline-20261006/tools/check-browser.cjs
PROTOTYPE_ORIGIN=http://127.0.0.1:18773 node specs/juyiting-ui-baseline-20261006/tools/check-index.cjs
PROTOTYPE_ORIGIN=http://127.0.0.1:18773 node specs/juyiting-ui-baseline-20261006/tools/check-icons.cjs
```

- `prototype-checks.json` / `document.log`：JSDOM 状态与离线安全检查，不是视觉测试。
- `browser-checks.json` / `browser.log`：自己的 Chromium、实际点击、页面布局、下载、音频与无外部请求检查。
- `preview-checks.json` / `index.log`：19页、23状态索引与静态链接。
- `icon-consistency-checks.json` / `icons.log`：原有七图标的尺寸、排列与禁用状态回归。
- `screenshots/`：当前候选截图；旧轮停止/人工修正原因和报告在 attempt-1/2/3/4/5，不复用为最终 PASS。

## 边界

不访问真实业务 API、账户、Provider、麦克风、支付、安装、enroll 或注册服务；文件导入使用脱敏 fixture，不消费真实 handoff。示例 PENDING/ACTIVE 不是 Runtime 在线；UNKNOWN/读取失败不会自动转成功。无产品构建、Flow、部署或线上版本验收。旧外壳/美术与历史 R01 等场景保留原来源日期，不表示当前产品仍存在当年的缺口。

定向诊断复用同一 `check-browser.cjs` 的 `PROTOTYPE_FOCUS=recent`，报告会标记 `focus: recent`，不能替代 `focus: all` 的全量证据。新增此选项是为了对已发现的表单遮挡选择器/历史 grid-column 继承问题取得更早反馈，没有新 runner 或产品构建。

## 最终结果

最终 focus: all 检查通过：92 项文档、37 组浏览器/115 布局、16 组图标/11 布局、3 组页面索引检查；1440/390/320px，无运行异常和外部请求。11 个候选运行文件在全量执行前后 SHA 一致，报告摘要和工具 SHA 见 summary.json。定向/中途修正报告不替代本轮全量结果。
