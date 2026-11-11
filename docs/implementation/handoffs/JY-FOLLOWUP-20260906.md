# 聚义厅后续修复（2026-09-06）

用户反馈前一版 web101ac4c 的二次横屏、空按钮、微信横屏和阅读保存仍失败。本任务新建独立worktree，不触碰主web未提交修改。当前状态只看 TASKS.yaml runtime_ledger_json；本文件只记证据。

## 已应用：阅读进度 CORS 根因修复
- 生产预检仅返回 authorization/content-type，漏掉写入必需 Idempotency-Key，浏览器阻止PUT；不是 createApi.put 缺失。
- 根因证据 `/tmp/cyf-jy-followup-reader-20260906/evidence/`：preflight-command.txt、preflight-response-headers.txt、config-provenance.txt。
- Java默认声明在 `api/common/jia-common-service/src/main/java/cn/jia/core/config/CorsConfig.java`。本次不走未验收的API源码发布管道、不重启Java。
- Critical Owner产出、Raman独立ACCEPT0/0/0的边缘配置：`/home/isp/apps/nginx/conf/vhost/api.chaoyoufan.cn.conf` 的 `location /archive` 仅加入：
  ```nginx
  proxy_hide_header Access-Control-Allow-Headers;
  add_header Access-Control-Allow-Headers "Authorization, Content-Type, X-API-Key, Idempotency-Key" always;
  ```
  严格Origin/Methods/Credentials仍由上游决定，不短路OPTIONS、不改变JWT/ACL/幂等请求处理。
- 原配置 SHA256 `f0e73d1b949d3b0b41d762133c367802fe89a4f5a36ac247aed1ceb2d27740d5`；新配置 `2211351ee8b2bd608bc8cfb620b0f2085e7cf4e1fe52e4a6c0ea2dda89e9e65e`。
- 主控精确hash复核后于09:15应用、nginx -t及reload成功；合法Origin预检HTTP200、唯一Allow-Headers包含key；非法Origin预检403且没有Allow-Origin。
- 应用及备份证据 `/var/tmp/cyf-jy-followup-main-20260906-0whiSH/`：nginx-api.before.conf、nginx-api.approved.conf、nginx-test.log、nginx-reload.log、nginx-deployed.sha256、cors-positive.headers、cors-negative.headers。本次不宣称真实用户认证写入已实测。

## 屏幕/浏览器证据约束
- web候选21a44c/ad1c596a6因globalpause/observer-scale/hostevent变更3项P1被独立REJECT，尚未部署。
- 源码整改矩阵 `/var/tmp/cyf-jy-followup-main-20260906-0whiSH/screen-review-r1.md`。
- 已有真实Chromium启动和本地模拟API的baseline截图，但baseline按钮2/3、ready后像素0/3，不能作为通过依据。
- `/var/tmp/cyf-jy-followup-verify-20260906-5odWxM/`记录全部harness故障、登录重定向和有界整改。绝不把mock保存和微信UA仿真称为生产用户/微信真机验证。

## Reader 源码回归闭环
- Critical Owner仅新增 `web/tests/archive-reader.test.js` 的真实adapter/fetch边界测试，source `fa672f80922f95b2d0d8692b3f5994d47233c3ab` / tree `d7c86c21d79fc041e32edb8400666bf35711c48f`。Raman已独立ACCEPT0/0/0；新selector1PASS，全reader55PASS且既有teleport fixture超时单跑1PASS。
- 与screen初候选无冲突字节级集成到Web `5bf6b119507fc44b2625d854987208a23ba825c1` / tree `1b951fc13e1e05f7c4c02fb9fd2e59303ffd2d71`；未部署screen。
- Reader新review-owner admission遭共享readonly3limit拒绝，已conflict-alert；没有抢占foreign任务。随后仅消费Reviewer已完成的独立证据作terminal accepted promotion，不新增read-onlyowner、不重复review。

## Screen R2 源码验收
- Owner最终 `5fa0685a32363ad9f77e8c1b6ae61197e8ab7d4c` / tree `5be146b7c83d302ba2cb9eaeff1d3fe95a22619f`；Raman R2独立ACCEPT0/0/0。
- 闭合global renderer复用、sticky cleanup pause/resume、当前容器resize与scale复原、Pointer数字逆映射及跨owner还原、HallScene直接DOM拖拽同源mapper。
- 定向5文件58PASS，新lifecycle5PASS；日志/meta `/tmp/cyf-jy-followup-screen-20260906-evidence/{mocha-5files,p1-screen-lifecycle}-5be146b7c83d302ba2cb9eaeff1d3fe95a22619f.*`。
- 精确无冲突集成 `d81b59e2724c45e7af47c60022296b2d20793295` / tree `d712c8b59922e93189df7fcb24b996cc6896d773`，相对screen source只差已验收reader testblob。记录 `/var/tmp/cyf-jy-followup-main-20260906-0whiSH/merge-evidence.txt`。
- 10:29主控已授权独立Verifier单次最终production build，再staticpreview+180秒独立Chromium启动，禁止再coldDEV并发优化。源代码ACCEPT不代表浏览器或微信真机通过。

## API 运行权协调回执
本线程未操作Java START/STOP/RESTART/JAR/Gradle，不持有API运行权；仅上述Nginx CORS定点reload且已结束。已向协调线程 `01a02e65-990c-7e81-b574-96a41cfe8222` 回执，无API生命周期操作在途，未修改其恢复台账或foreign进程。

## 最终构建、行为验证与发布证据
- Verifier最终独立构建 `/var/tmp/cyf-jy-followup-verify-20260906-5odWxM/final-run-d81b59e-phHtJs/`：build.exit=0；Vite7m9s，generated `components.d.ts` 已留diff且仅恢复本次生成文件，exact d81/d712 source clean。`build-result.json` 和 `dist-manifest.json` 绑定403文件/105387332字节。
- Chromium mobile仿真+明确mock auth/API：browser/result.json behaviorPass=true，3/3 ready-frame且纹理pixel通过；主控读3份 `c*-03-portrait-request.dom.json`，确认物理视口尚为932x430 landscape时，点击按钮已变为portrait-command、地图canvas卸载，因此不是物理旋转代替按钮生效。
- WeChat UA仿真：browser/wechat-result.json全checks true，物理430x932内virtual旋转有纹理地图，可信拖拽camera transform发生变化，回竖屏成功，无native fullscreen/lock调用，帮助图标非空；主控实际查看第三轮地图和微信虚拟横屏PNG，地形/人物/问号均可见。
- 无app Runtime异常；仅离开页面时SSE GET取消（ERR_ABORTED）。本次browser/harness PID已退出，无own残留服务。仍不冒充微信真机或真实用户认证写入验证。
- 主控独立部署digest `1e2feeb95a039724e1b6769327db634d81329eaf1e9a5cb75a31f54608a7e363`。已审 taskcopy 保留原部署脚本backup/copy/permissions流程，使用exact HEAD/tree/clean/verified-dist保护，未重复build。
- 11:06部署成功，备份 `/home/isp/hosts/cyf/web/bak/kit_bak_20260906_110644`；目标全部403文件digest匹配；公网聚义厅index HTTP200/2907bytes和 `static/JuyiHallEntry-GQLYtwYJ.js` HTTP200/583962bytes均与本地验证产物字节一致。
- 已非force推送 `origin/develop`：101ac4c → d81b59e。发布日志、源/产物manifest、公网headers/body和digest证据 `/var/tmp/cyf-jy-followup-main-20260906-0whiSH/`。
- 下一步：用户关闭并重新进入聚义厅，微信真机连续横→竖→横，再翻典籍后关闭重开确认进度。勿清空用户存储或虚报找回此前从未保存的旧进度。
