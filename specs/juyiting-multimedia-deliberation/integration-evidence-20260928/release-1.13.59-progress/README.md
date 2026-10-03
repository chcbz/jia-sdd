# Web 1.13.59 — app-shell freshness

候选 `359b1b961c923cad6080da9f1aeabc1d8d218aee` / tree `f40cbd319df89ef097de7df12b775f31c7f336ab`。仅修改 public/sw.js 与 tests/pwa-shell-freshness.test.js。保留 e58644a voice SVG，控件逐字节相同。

- 实际问题：Run159已部署，但原profile的SW从CacheStorage返回旧无query入口；navigation使用默认HTTP cache。不是构建或图标源码丢失。
- 修复：shell在线重验证；真实网络异常才回退离线；no-store失败不伪报旧成功；HTTP503与重定向不污染入口。无性能deadline，无清空缓存方案，无CACHE_VERSION强制涨号。
- 自检：13 targeted PASS；旧源11用例中8FAIL/3PASS；ESLint/diff PASS。真实系统Chromium133对精确旧源复现、原registration升级（不清缓存）、同SW连续发布、HTTP max-age、导航、503、连接故障与no-store共7检查PASS。诊断server/tab已关闭，0Provider。
- Flow4403172/160已启动且官方checkout为候选；测试/制品/发布最终结果待核验。不能宣称整体可验收。
- 原417旧结果丢失/无spool，result-only恢复和owner事务终止尚未实现；完整AC01–AC22 +FD01–FD12仍未通过。
