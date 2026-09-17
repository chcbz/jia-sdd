# 1.7.0 本地发布与上线回归（2026-09-17）

## 当前结论（18:15 CST）

用户授权“现在发布，发布后回归，通过再通知验收”。**API/Web 均已实际部署且健康，但新预览功能认证回归发现503，尚不可通知用户全部验收通过。** 修复正在进行；不回写冻结制品，不把健康检查当功能验收。

| 组件 | exact commit / Git tree | 实际制品 SHA-256 | 发布完成时间 CST |
|---|---|---|---|
| API | `9aaf2a315b0365ccf801012b100cf7b38cf47c62` / `b4bffe1e298d9c445ff370b4c19ce3cf3f750a14` | `3e516826a863d6ab281639df7ff17818903e32cc757b24b4d8a089ee9537e5eb` | 18:08:04 |
| Web | `7c4902983974b748ea01d7c88e2403fa636691e6` / `ae9cd58d4adb7ee16678ba92b1e67de5ecb84141` | `02775873e9498af7e17df11d6dfa4e8454296b1be030c0ffee617b594f0beef7` | 18:11:35 |

- `build_origin=local_user_authorized`，没有 Flow Run。前后端冻结 `release/1.7.0`，未强推/覆盖旧release。
- API→Web，通过实际发布互斥、精确运行身份、制品摘要、恢复备份与健康检查。API当前PID1947477是本次记录值，不授权后续直接复用。
- 启用独立 `economy.read-only-preview.enabled=true`，不开启购买/交易/安装/收费/语音。
- 必要新增 Nginx 路由仅 `^~ /economy/preview/` → 10018；不开放整个旧 `/economy` 域，原其他路由与兜底拒绝保留。
- Web入口 `/static/index-7G2znfg1.js`，dist tree SHA-256 `44c412cd177acf8c3b026ecf6144ae28cbddd18e22cddca92330ae729ff1bb8c`。

## 已执行真实回归

授权测试账号通过真实 OAuth Authorization Code + PKCE，公网TLS正常校验；无JWT伪造、无响应mock、无生产DML、无真实购买/安装/Provider调用。

- 预览能力：200/E0，正确的只读contract与actions。
- 预算试算：200/E0，重复输入结果一致、charged=false、persisted=false、示例费率标识正确；错误输入400。
- 托管参考方案及4位本人Agent租约读取：200/E0。
- 匿名401、未知Agent404、非法scope查询/分页400；生产第二身份/另一client凭据未提供，不能冒称线上双身份已测，隔离fixture证据仍保留。
- **失败**：钱包、流水、技能目录/详情及4位本人Agent权益返回503 `PREVIEW_DATA_UNAVAILABLE`。保留真实错误，不用空目录/0余额掩盖。已分配专门API Owner归因实际MySQL/schema与映射，不擅自迁移或填数据。
- 聚义厅旧功能：发布前catalog为`BAD_REQUEST: tenantId is invalid`，本次候选包含已修复代码，发布后恢复108个角色；roster4条。真实Chromium竖屏初次/刷新均显示4位好汉，招贤令108张卡片，跨域认证读取200/E0。
- 典籍：目录、序言、当前账号阅读进度均200/E0；不改阅读进度/笔记。
- 悬赏列表200/E0但当前open列表为空。历史任务378成果仍404 `DELIVERABLE_NOT_FOUND`，该任务不在当前可见open列表；记录为无可见验收夹具，既不冒充成果读取通过，也不据此直接断言ACL错误/擅自恢复可见性。
- 新页面真实浏览器五区、4Agent选择、试算均可操作；430×932与932×430可纵向滚动，无水平溢出，无交易按钮。503在真实页面复现，故整体回归未通过。

## 工具观测归因

- 最初未配置公网预览route时，Nginx兜底444被Node表现为socket closed；curl UA的403是既有独立规则。已纠正最初UA推断，未绕过鉴权/TLS或移除规则。
- 第一轮UI在固定10秒时采样聚义厅得到空壳；改为等待实际场景元素后只读复验通过。慢加载只观测，不作为产品拒绝门禁。
- 第一轮脚本把两次钱包/流水错误payload的null相等计为“未变化”；明确作废该断言，修正为四次200/E0后才可比较。首轮原报告保存，正确统计为24通过/13失败/1无结论，不能据此宣称线上零写入已验证。

## 证据与待办

- 冻结源码/测试报告：`docs/implementation/V1_7_RELEASE_READY_20260917.md`。API仅changed-scope26+12+64通过；全API默认测试仍有历史编译债。
- 发布规范记录：`/opt/cyf/service/api/release-records/api-deploy-20260917T100652Z-9aaf2a315b0365ccf801012b100cf7b38cf47c62-b4bffe1e298d9c445ff370b4c19ce3cf3f750a14-v1.7.0-local-20260917.json`；`/home/isp/hosts/cyf/web/bak/release-records/web-deploy-20260917T101119Z-7c4902983974b748ea01d7c88e2403fa636691e6-ae9cd58d4adb7ee16678ba92b1e67de5ecb84141-v1.7.0-local-20260917.json`。
- 本次交付包：`/home/isp/wsps/cyf/deliverables/releases/v1.7.0-local-20260917/`。
- 主控只读回归：`/var/tmp/cyf-v1-7-regression-main-20260917/`，含API报告及原始R1、浏览器报告/截图、归因、`juyi-r2/report.json`。
- 下一步：归因并有界修复预览503→精确测试→新不可变patch release→同一runtime Owner部署→重新认证API/浏览器回归→无阻塞再通知用户验收。若必须生产DDL/DML，先提供精确缺口及授权请求。

## 18:22 根因确认与授权边界

仅 `information_schema` SELECT 已确认生产 `jia` / MySQL8.0.21 没有经济基础5表和技能市场7表，故新读取真实503。并非已证实的SQL方言/Mapper源码缺陷；无需靠代码修改、重建或盲重启解决，前文“新patch release”只是归因前的条件预案，**现已被精确schema缺口结论替代**。

- 最小补齐范围：`economy_account`、`economy_transaction`、`economy_entry`、`economy_escrow`、`economy_escrow_funding_lot`；`economy_skill_product`、`economy_skill_product_version`、`economy_skill_purchase_quote`、`economy_skill_order`、`economy_skill_order_receipt`、`economy_skill_installation`、`economy_skill_entitlement`。
- canonical foundation SQL SHA-256 `f2cdb4bef269650f6492a908e335a96f88f00ea074ae33d83176a83b973f7618`；marketplace `4f1e827ab3370da2f06fd5036119e4e71354652d97a7e509b47acb5f3292d625`，均为新增表定义，无seed/业务DML/破坏语句。
- 已准备**未授权、未执行**候选：`/home/isp/wsps/cyf/deliverables/releases/v1.7.0-schema-repair-pending-20260917/approval-plan.json`。用户明确授权生产DDL后，实际互斥下按前值/精确SQL/新表为空/结构验证执行，再做API与浏览器回归。DDL自动提交，部分失败不能假称事务回滚；停止归因，不自动DROP。
- 另发现 `economy_hosting_rent_plan`、`economy_hosting_lease` 缺失；当前参考方案走已配置数据、local Agent走不适用分支所以200。此2表不混入本次12表最小授权，不声称server托管正例已在线验证。
- 根因原始证据 `root-cause.json` SHA-256 `d6d8a7a9fbf2d3e29cf0f18222fe7ff146eccf9863dff4783cdb6fe36889f17e`，已复制候选目录。只读归因Owner没有改API源码/提交新候选，没有Gradle，没有生产DDL/DML。等待的是用户对**新增数据库结构**的授权，不是等Reviewer或构建。
