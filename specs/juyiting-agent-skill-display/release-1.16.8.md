# 点将册 1.16.8 发布收口

核验时间：2026-10-17T12:47:52.083902+08:00；任务 `JYT-AGENT-SKILL-DISPLAY-20261016`，唯一 Owner `current_chat_owner`。状态：**已部署，范围内正式与在线验收通过**。

## 固定源码与正式交付

| 组件 | develop commit / tree | Flow / 部署单 | 正式测试 |
|---|---|---|---|
| API | b76a1d0aeda572767a6d4734d050121d985bd9c9 / 82b7ff2f49d23ec99af3a190ba1433b3704c1780 | 5260799/152 / 71288035 | 2333通过、95跳过、0失败错误；23项新测试全过；layering、fresh bootJar通过 |
| Web | da59a4b8e98920386e7ab52a77463613c2ae5a92 / 0c40c37f577836bcb77778ac8a22bdbf43769ccd | 4403172/224 / 71288193 | 3041通过、2 pending；构建和扫描作业SUCCESS |

两条Run及原生部署单均SUCCESS，各1台主机Success/healthy；先API后Web，没有本机生产打包或部署。API本地develop已有8提交现已合入，本轮没有新增删例；继承的历史84项删除、95跳过不代表未裁剪测试覆盖恢复。之前148/149失败及151/223未部署而CANCELED的证据保留，不改成成功。

- API同Run archive SHA256 `939268c1433669f887e711f95fb9c3cb7867f08f6dd6d2ec0be3eabb884df741`；JAR SHA256 `d487704e014b1cfcb631c90a484f9f27a404cb24a9cbcc5368b50f5ef1dc3cc0`，canonical安装、现行receipt/record和运行进程一致，healthUP。
- Web同Run archive SHA256 `2793e16059b9d7e92207dc0d8b178e8bc6ab15a0882babf446f715452b84d23d`；366个安装文件逐个与manifest一致，公网入口及其引用/聚义厅懒加载JS/CSS等9文件字节摘要一致。
- 原schema helper确认两张F06表existing_equivalent，本次无DDL/DML；不是旧历史发布闭包修复或该功能激活。
- 两流水线已无活动Run时精确恢复原CI-only配置并readback，**develop不自动部署**。

正式证据：`evidence/api-flow152-artifact.json`、`api-release152.json`、`web-flow224-artifact.json`、`web-release224.json`、`flow-restored-5260799.json`、`flow-restored-4403172.json`。

## 真实线上验收

通过正常授权码+PKCE新登录的测试账户，未伪造JWT/借他人会话。重启前旧测试令牌不能匹配新key；重新正常登录后验证，不将此误报为新GET缺陷。

- 5个本人Agent的GET200；原权威本领0/16项均一致；实际1项已核验、Runtime就绪技能为**图片编辑**，不写成图片生成，不创建订单凑数据。
- 非owner404，无JWT/无效JWT401，private no-store；不购买/安装/重扫描/重注册/派单或点击密议写业务状态。
- **完整生产应用**5视口：1440×900、390×844、320×568、390×480、720×480；技能与本领显示、真实刷新GET、底部密议按钮几何及命中、短屏实际长内容滚动、移动返回/关闭/同ID重入通过；28次profile GET全200，无浏览器Runtime异常。
- 最新名册POST /agent/roster只有本人5项，线上非owner卡片用例NOT_APPLICABLE，没有合成一行；越权由真实API404与挂载夹具测试覆盖。
- 浏览器先前失败来自诊断脚本没有处理新手引导/身份初始化、文档导航与移动真实入口，原FAIL记录保留；修正的是本任务浏览器诊断，不是替换DOM/CSS/数据或修改已发布产品。移动端实际从“我的→好汉名册”进入。

证据：`evidence/online/api-result.json`、`evidence/online/result.json`；实页截图：`evidence/online/screenshots/`。无实机安全区/软键盘验收；没有把桌面Chromium模拟视口宣称为iPhone实机。

## 职责和范围

技能为真实安装/Runtime核验事实；本领复用原Agent投影。新owner-only详情GET只读，不取代任务技能授权、不改变派单算法；旧名册/地图/Agent详情/能力索引保留本领。刷新读取最近入库记录，不主动刷新Runtime工作区。≤720px名册→详情、常驻动作；桌面分栏。

稳定知识归于 `docs/juyiting-runbook.md` 的“点将册技能／本领与响应式详情”段，历史D1—D4设计/失败证据仍在原处。当前唯一原型入口已由其他任务迁到 `/home/isp/wsps/cyf/web/prototypes/juyiting/index.html`；其迁移/新样式不属于本次发布，不覆盖其未提交改动。

30分钟全部最终代码目标未达到，计时沿 `evidence/coding-final.json`；不以首轮24分钟冒称达标。主动编码/验证/等待未连续分离计时，不编造缩时收益。

安全后续：先前排障误回显的云效仓库消费凭据建议轮换，已主动告知用户；未回显到本记录、未擅自轮换。凭据原始响应/配置仅私有证据目录保存，浏览器私有profile与测试令牌清理情况见handoff收尾记录。
