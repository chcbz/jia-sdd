# 会话成果保存请求的悬挂状态恢复（2026-09-30）

Web 特性分支已快进并远端回读 `ebae2341ebc1226a0e0396b983ba3e679c8dc7c5` / tree `a1a3c3a64ed77d8c15b7f385b1929139b71c075d`。同身份会话内收到服务端操作 ID 后，用户点击“继续原保存”会**先按原操作 ID 查询**；若服务端仍为 pending/saving 且保有最初的幂等键，再以**原键及原资产引用**显式重发 POST，供服务端对账/恢复。GET 返回 saved 时不再发 POST；网络/身份/状态回执不明确时不盲重试，也不将本地记录视为保存成功。此举修复页面刷新后仅重复读取永远 pending 的操作而无法主动恢复的情况。

本地 Owner 定向执行 `node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --reporter dot` 加 7 个聚义厅多媒体/归档/展示测试文件：**30/30 通过**；两处改动 ESLint 与 `git diff --check` 通过。未运行生产构建/浏览器，服务端归档 POST/GET 仍在实施；不代表归档完成、需求交付或可验收。
