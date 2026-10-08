# Web 1.13.59 — app-shell freshness

候选 `359b1b961c923cad6080da9f1aeabc1d8d218aee` / tree `f40cbd319df89ef097de7df12b775f31c7f336ab`。仅修改 public/sw.js 与 tests/pwa-shell-freshness.test.js。保留 e58644a voice SVG，控件逐字节相同。

- 实际问题：Run159已部署，但原profile的SW从CacheStorage返回旧无query入口；navigation使用默认HTTP cache。不是构建或图标源码丢失。
- 修复：shell在线重验证；真实网络异常才回退离线；no-store失败不伪报旧成功；HTTP503与重定向不污染入口。无性能deadline，无清空缓存方案，无CACHE_VERSION强制涨号。
- 自检：13 targeted PASS；旧源11用例中8FAIL/3PASS；ESLint/diff PASS。真实系统Chromium133对精确旧源复现、原registration升级（不清缓存）、同SW连续发布、HTTP max-age、导航、503、连接故障与no-store共7检查PASS。诊断server/tab已关闭，0Provider。
- Flow4403172/160正式SUCCESS：2927PASS/2pending，制品SHA25666babbade4af0e6e86185ea1a7069a80e1f7698e561718ea02fb341190cdbb13，部署单70598991成功健康，364文件逐字节匹配。原profile普通导航自动更新SW，不清缓存、不加query，入口/entry/HallJS/CSS/实际加载资源全匹配。不能宣称整体可验收。
- 原417旧结果丢失/无spool，result-only恢复和owner事务终止尚未实现；完整AC01–AC22 +FD01–FD12仍未通过。

## 真实UI文字保存验证

原会话1760458004760、持久消息1675335，选择codepoint[19,24)“画一只鸟。”，由实际保存按钮发起一次POST（没有直接API写/重放）。UI已保存pws_d2fd7f2eea9f4fcc800dc9bb84357074 v1；根入口“资料→查看”预览正确；实际下载15 UTF-8字节，SHA2560e37dde510c7d680e0b69a5e2d1c935f0926208c5a687f0479e0eb7bba2cf27a，与冻结选择相同。初次观测器在busy状态提前退出，后续只读确认成功与下载；没有留存原POST完整响应，不补造HTTP回执。

尚需修正UI来源文案：用户文字片段当前被泛称“Agent交付”；嵌套三级会话打开百宝箱被已有层数限制阻止，根资料入口可用。原417生成图片未交付，整体仍不可验收。
