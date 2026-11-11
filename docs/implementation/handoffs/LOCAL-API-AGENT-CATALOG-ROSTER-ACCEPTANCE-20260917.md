# 聚义厅目录/点将册：可验收交付（2026-09-17）

## 结论与范围

本次两个接口及关联列表恢复，可交用户验收。按用户授权本地测试、构建、发布；未调用/恢复云效发布，未做数据库回填、DDL/DML、角色申领/解绑、任务派发或付费调用。不是全站/微信真机验收。

## 精确线上来源

- API branch：`codex/bugfix-agent-catalog-v16-20260917`，已推送远端并 readback。
- Commit：`4451c30034c1bb31b346ca6b4c0ff6bc7ebb1aca`。
- Tree：`b1e5398970d31c838c0e38f8d65aa2f224942fa0`。
- 基于当前 v1.6 `a8e9170873062165176626775d66c92dfc2e7a1a`，没有用旧基线覆盖 v1.6。
- 线上 JAR：`/opt/cyf/service/api/cyf-api-kit.jar`。
- SHA-256：`8ee8c8cfcbd53bb50f3e8f4b60220fe6310019fa8c983498414073d162666869`，221386209 bytes。
- 发布回执：`/opt/cyf/service/api/release-records/catalog-v16-4451c300-20260917/record.json`；PID 1810738，规范 launcher 的身份/制品核验及实际健康 UP。
- 发布持有等待式 API release 锁；保存上一个已部署 JAR 的 inode 作为回退材料，原子替换、不原地改写。v1.6 与本轮第一候选均有恢复材料。锁已释放。
- 本次未发布 Web；线上 Web 仍是既有 v1.6。远端 develop 仍为 a8e91708，**尚未包含此次 bugfix**；下次从 develop 发布前必须先合入本分支，不能覆盖此修复。此次不推 develop、不主动启动 Flow。

## 两个根因

1. 单租户身份已规范为 tenant `0`，Persona DAO 的旧检查仍拒绝 `0`。删除这一旧拒绝，保留 tenant/client 精确格式校验。
2. 同租户其他用户的角色绑定应显示“已占用”但不能披露身份/运行详情。SQL 的 reference CASE 在 identity 被隐藏时返回 0 而非 NULL，触发服务层正确的权限检查。改为 identity 不存在时返回 NULL；没有删除或放宽权限检查。

只改两个生产 Java 文件、两个相关测试文件。

## 验证证据

- 经 orchestrator 串行执行：DAO 4、真实 mapper SELECT 的隔离 H2 测试 3、批量 mapper 合同 3、目录缓存 6，共 **16/16 PASS**。
- SQL 测试先真实复现 `expected null but was 0`，修复后变绿；覆盖精确 owner 可见、foreign owner 脱敏、其他 tenant/client 不可见。
- bootJar 成功，公共制品安全扫描保留并通过；64 项未变更 verifier 测试复用 Gradle UP-TO-DATE 结果，不宣称本轮重新执行了64项。不宣称整个历史 mapper suite 全绿。
- 公网真实 OAuth2 Authorization Code + PKCE 使用授权测试账号，TLS 正常校验，未记录口令、JWT 或 authorization code。
- `GET /agent/personas/catalog`：HTTP 200 / E0，108 个角色，角色 code 无重复；4 个本人绑定，foreign 绑定不暴露 agentId/owner 或操作权限。
- `POST /agent/roster`：HTTP 200 / E0，4 条，扈三娘、李逵、林冲、吴用。
- `GET /agent/map`：HTTP 200 / E0，本轮6条（实时在线状态数量可能变动）。地图公有投影不套用招贤令的隐藏 agentId 规则。
- 公网 OPTIONS 允许 `https://kit.chaoyoufan.cn` / authorization；真实 Chromium 从 kit 页面跨域读取 catalog、roster 均成功，无 mock/路由响应替换/忽略证书。
- 桌面浏览器：108 张招贤令卡片实际渲染。
- 竖屏浏览器：默认可见4位可点将好汉；从可见入口打开招贤令，渲染108张卡片；整页刷新后仍可见4位，无空列表。
- 竖屏最终证据：`/var/tmp/cyf-catalog-v16-regression-20260917/portrait-final/report.json`，状态 `API_AND_UI_REGRESSION_PASS`；同目录有 `initial.png`、`catalog.png`。
- 测试汇总：`/var/tmp/cyf-catalog-v16-regression-20260917/tests-summary.json`。

## 回归工具归因与未覆盖项

- 第一次 headless renderer/CDP 停滞，未当作功能失败或通过；关闭自身诊断进程，改用实际可用的 shm/TMPDIR 并保存 stderr 后浏览器通过。没有操作其他任务进程。
- 前两次竖屏模拟只设 viewport、未设置 screen orientation，导致进入横屏模式、隐藏列表不计可见；最终明确设置 portraitPrimary/430×932，再检查真实可见列表与刷新，结果通过。保留中间失败报告，未改写成成功。
- 页面重载/场景切换记录过 `ERR_ABORTED`（tmx 与事件流等）；最终接口业务结果和可见列表成功，不据此声称整个会话没有任何网络取消。
- 桌面招贤令中已绑定角色的按钮会挤压文字列；已观察、尚未修复，属于独立显示问题，不把本轮接口恢复宣称为全功能无 BUG。竖屏截图未出现该挤压。
- 未执行生产申领/除名/扣费，未进行第二用户真实登录和微信真机验证；跨 tenant/client 与 foreign owner 的负例为隔离 SQL 测试加当前账号实际目录脱敏核验。

## 用户验收步骤

用 chcbz 登录并刷新聚义厅，竖屏首页应默认看到4位可点将好汉；打开招贤令应显示108个角色、不再报 scope 或目录异常；刷新后再检查列表。
