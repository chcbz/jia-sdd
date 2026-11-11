# 1.9.6 聚义厅横屏个人中心入口修订发布记录

日期：2026-09-18。状态：**已发布、线上静态健康通过；最新视觉微调待用户刷新后确认。**

## 变更范围

这是 `personal-center-navigation-v1-8` 已发布导航能力的前端补丁，不新增接口、数据库迁移、生产数据操作、交易、语音或 API 重启。

- 竖屏保留“个人中心”入口，替代独立“点验刷新”入口的既定布局不变。
- 横屏个人中心入口保留在左侧工具组，避免与小程序关闭按钮重叠。
- 横屏入口仅保留当前用户圆形头像；移除“我的”文字及外层圆角长方形的边框/背景，按钮尺寸与相邻工具统一为 `30×30`。
- 保留 `aria-label/title=个人中心`、头像加载失败回退、键盘/指针事件隔离与原有路由行为。

## 实际发布链

| 项目 | 事实 |
| --- | --- |
| Web develop / release | `737506e7af06bb4ea4ec2386dc507ec745297481` / tree `05f1c965cd07bb02ef5caaf551f5ab4c87fbfc21`；`origin/develop` 与 `origin/release/1.9.6` 一致 |
| API（未变更、未重启） | `e15f7020bf77153912aafce15fc11c67b2f06e11` / tree `551c452f1a81bbc6f6b198452891d2189b967fd8` |
| Release | `v1.9.6-local-20260918`，`build_origin=local_user_authorized`，仅 Web 安装 |
| Web 制品 | SHA-256 `466e56949fc699884a38668a32aa01d97d53a4c1d696a6055a35fb2559c888d0`；dist tree `1473f9daf0c1fc93f04b9f55123376ee291d00ae5a87a0746b2e2b6864beaa42` |
| 联合验证 | release record SHA-256 `8aa3ce498c1dc5603d244e4aa1cd53b7f320ac48a7bed16177b27550fe16c162` |
| 部署记录 | `/home/isp/hosts/cyf/web/bak/release-records/web-deploy-20260918T020658Z-737506e7af06bb4ea4ec2386dc507ec745297481-05f1c965cd07bb02ef5caaf551f5ab4c87fbfc21-v1.9.6-local-20260918.json`，状态 `DEPLOYED_HEALTHY` |

## 验证与线上核验

- `tests/hall-account-navigation.test.js` 与 `tests/pwa-service-worker-localhost.test.js`：**4 passing**。
- Vite 生产构建：PASS。
- 发布前 `verify-release.sh` 与 `deploy-web.sh --dry-run`：PASS。
- 实际部署后：`https://kit.chaoyoufan.cn/`、`/juyiting`、`/sw.js` 均为 HTTP 200。
- Service Worker 缓存版本：`cyf-pwa-v20260918-hall-account-avatar-only-r2`，用于让已打开的 PWA/WebView 获取本次布局资源；用户需完全退出并重新进入，必要时经站点 `/reset-cache.html` 清除旧站点缓存。

## 缺陷归因与闭环

1. 1.9.5 已先隐藏横屏文字，但把“去除外框”的 CSS 写为组件根元素的后代选择器；Vue 组件 class 实际落在该根按钮本身，因此规则没有命中外框。
2. 用户视觉回报后，1.9.6 将规则改为命中 `.stage-landscape-account` 根按钮，明确设置 `border: 0`、`background: transparent`、`padding: 0` 与 `30×30` 尺寸；子头像维持 `28×28`。
3. 该修订不改变身份 scope、路由目标、地图交互锁或 API 权限。最新视觉效果仍应由用户在实际小程序横屏环境确认；此前功能性个人中心导航验收记录不被改写。

## 关联

- 原规格：`specs/personal-center-navigation-v1-8/`
- 1.8/1.9.2 历史发布与回归：`docs/implementation/V1_9_2_RELEASE_RESULT_20260918.md`
- 本次冻结输入与结果：`deliverables/releases/v1.9.6-local-20260918/{release-input.json,release-outcome.json}`
