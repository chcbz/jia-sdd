# 点将册 1.16.9 小范围视觉修复发布

核验：2026-10-17T15:57:16.738908+08:00。任务 `JYT-AGENT-SKILL-DISPLAY-20261016`；Owner `current_chat_owner`。**已发布，范围内正式与在线核验通过**。

## 范围与源码

依据用户已确认原型 `/home/isp/wsps/cyf/web/prototypes/juyiting/index.html#agents` 和 `visual-audit-20261017.md`，仅修正：密议朱红通栏／双动作主次色、移动详情内缩留白、68px不收缩缩略头像、技能卡片和本领说明、刷新布局及真实读取时间、44px关闭入口和移动名册工具栏。详情正文滚动与底部动作继续分离。

- Web develop：`6fbdb6618b1132316a95db87cca9402de83138e8`；tree `212194b370ec40c2c8b1e4184ad09c5f01c1a3bb`，已push并实际核对远端。
- 仅2组件、2测试及package/lock版本共6文件；原型和web/AGENTS其他任务脏改动未纳入。
- API仍1.16.8／Flow152／`b76a1d0aeda572767a6d4734d050121d985bd9c9`。无接口、数据库、Runtime、派单、权限或事件流程变更。接口规范v1.2不变。

## 正式Flow与同Run部署

| 项目 | 结果 |
|---|---|
| Flow4403172 / Run225 | SUCCESS；精确commit/tree检查；扫描SUCCESS |
| 测试/构建作业537043473 | 3045通过、2原有pending、0失败；Vite生产构建成功 |
| 部署作业537043475 / 部署单71293772 | SUCCESS；主机组28833、1台Success/healthy |
| 同Run制品 | SHA256 `38ffacf954924f275f38e6b0deed446aed9d54e2e7c5971203ae348e3f043a87`；106651102 bytes |
| 安装与公网 | 366个安装文件与225 manifest逐一相同；入口及聚义厅等9个公网资源字节摘要一致 |

单次固定版本发布，未使用本机生产构建/源码发布或别的Run制品；未修改主机helper。无活动Run且候选配置未被别人改变后，已恢复本轮备份的原CI-only配置并readback，**develop不自动部署**。既有发布适配器保留锁、备份和可恢复安装；本批额外入口/record备份 `/home/isp/baks/cyf-agent-visual-web-1.16.9-20261017`。

## 实际线上验收

正常PKCE登录本任务独立测试会话，在实际完整应用验证7视口：1440×900、390×844、320×568、390×480、720×480、721×480、844×390。真实吴用详情的技能为“图片编辑1.0.0”、16项本领，不替换为原型样例数据。

- 真实计算样式验证单动作朱红通栏、头像68px、缩略图路径、关闭44px及SVG、正文16px、刷新flex；≤720详情全宽且无内缩圆角。
- 正文滚动时footer位置不变、按钮在视口内且命中可达；刷新真实GET、移动返回/同ID重入、关闭通过。
- 36次实际profile GET全部200；152个观察到的API响应均200，无浏览器Runtime exception。
- 双动作、busy/资格限制、长ID/长技能名/大量本领使用既有挂载测试及8视口真实组件+父CSS离线夹具验证，线上无待点将场景，不造任务/派单/会话来凑验收。
- 实体手机刘海安全区/软键盘未实机验收，不把桌面浏览器模拟当实机。

本机133项定向诊断通过；JuyiHall既有111 lint errors/82 warnings与base相同，本次新增0，AgentPanel clean，不宣称全量lint通过。没有删除历史测试或新增pending，历史1.16.8记录不改写。计时未按主动编码/等待连续分离，不编造30分钟全流程或提效保证。

## 证据

均位于 `evidence/visual-fix-1.16.9/`：`release-input.json`、`local-diagnostics.json`、`lint-delta.json`、`flow-status.json`、`web-flow225-artifact.json`、`deployment.json`、`web-release225.json`、`flow-restored-4403172.json`、`online/result.json`、`online/screenshots/`、`session-cleanup.json`。原始云效配置/日志/制品仅在本任务0700目录；测试令牌已删除，实际浏览器profile已清理，自有预览已停止。
