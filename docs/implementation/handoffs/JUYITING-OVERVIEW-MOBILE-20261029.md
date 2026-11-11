# 办事首页移动端事项操作（2026-10-29）

- Owner：当前任务；范围：办事首页事项列表移动端并排操作，不改消息页和事项语义，不授权部署。
- Web 工作区 `/home/isp/wsps/cyf/web`，branch `codex/juyiting-ui-workflow`，基线 HEAD `ca22ac29de657971b12a71f3a99d2d9ecfc67c1c`，tree `962e513205e4805a601022285bdff557c71f37ac`；本地 origin/develop 引用 `fa8d7f1793392918bd0d1531c6f029cbaff8daeb`，未查询远端；工作区已有大量无关改动，未覆盖或提交。线上版本未核验。
- 原型：`web/prototypes/juyiting/`，办事首页事项列表；移动端内容与按钮并排，长标题换行。规格见原型 `specs/prototype-spec.md` 和 `specs/juyiting-ui-baseline-20261006/optimization/spec.md`。产品实现 `web/src/components/juyiting/HallOverview.vue`。
- 静态 `git diff --check` 通过；既有原型预览 `http://127.0.0.1:18786/` HTTP 200，未完成浏览器布局验收。定向组件测试启动后无输出，已主动中断，非通过；尚需浏览器对照移动端长标题、不同按钮和桌面/消息页，以及精确候选的正式 Flow 验证。未构建、未部署、未核验线上。

## 构建和部署（2026-10-29）
- 以远端 develop fa8d7f1793392918bd0d1531c6f029cbaff8daeb 为基线，在任务隔离工作区仅移植本任务布局并升版，提交并 push Web develop `3236adc8bbe08b9b436cbcef5cfa3dadd52e2bba`，tree `e9acb3d6aad9d30af21bedb667013652d6ff2e84`，版本 1.16.73；原工作区无关改动未纳入。根仓 gitlink 未调整。
- Flow 4403172/372 SUCCESS：构建与JS扫描作业成功；制品报告3515 passing、2 pending、0 failures；受监测 Run 约129秒。制品源 commit/tree 匹配，归档 SHA-256 `a81d3e9f6465a328e4962915c3a0173fd5dc3f4ed10feb41e1c9b8553e0e9b5d`。为本次固定提交临时更改的 CI-only 配置已恢复前值并 readback；未添加 Flow 主机调用。
- 主机主动下载并使用现有安装器独立安装，安装器核验612文件及公网入口通过；旧 Run 371 站点备份并 tar compare，备份 `/home/isp/baks/cyf-web-flow/20261029-mobile-overview/`，归档 SHA-256 `474de19f193814ebfd7eb21b8625fcbecb7c1ec7f45b9c16a503aefc85a83fa3`。主机安装记录为372/1.16.73。公网 index、JuyiHallEntry JS/CSS 与 Run 372 安装清单摘要一致。证据 `/home/isp/state/cyf-web-mobile-20261029/`。
- 尚未进行登录态移动端浏览器视觉验收，公网资源匹配不代表实际交互已目视验证。
