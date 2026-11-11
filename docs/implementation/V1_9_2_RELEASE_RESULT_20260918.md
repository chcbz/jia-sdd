# 1.9.2 统一发布与回归结果

**已发布，本轮范围内线上回归通过，等待用户验收。**

## 来源与边界

用户授权发布1.8+1.9+bugfix后回归，通过后通知验收。本轮先发布1.9.1并恢复OOM停机，真实API回归发现 `/resource` 404，故继续最小修复；1.9.0/1.9.1冻结分支与失败证据不覆盖。语音、交易、付费Provider、运维权限/开关及生产DDL/DML不在授权中。

## 1.9.1实际回归（保留历史）

- API45PASS/1FAIL；5项未测、1项旧范围外，唯一FAIL是已认证 `/resource` 返回404/E404。认证PKCE、`/user/my`、roster4、catalog108、任务空列表、典籍目录/正文/阅读进度GET、经济预览相关均实际通过。
- 浏览器111PASS/2FAIL；两项采用DOM存在性代替可见性，既有横屏/桌面保留隐藏DOM被误判。定向修正后21PASS/0FAIL，未改产品或回写首次报告。
- 首轮 `/actuator` 公网关闭连接属探针假设问题，已改用合法公网业务/匿名鉴权边界探测；未放开管理端点、未放宽TLS。
- 原始封存：`/var/tmp/cyf-v1-9-online-regression-20260918/live-summary.json` 与 `LIVE-SHA256SUMS`。

## 真实根因与最小修复

`oauth/jia-oauth-client-starter` 与 `oauth/jia-oauth-resource` 同时定义 `cn.jia.oauth.api.AuthenticationController`。1.9.1及前一实际线上JAR的classpath均先加载client模块（位置12），后加载resource模块（位置28），造成只见 `/token`、不见 `/resource`；新运行日志确认 `No static resource resource`。不是新增ACL限制、不是用户fixture缺失。

- 仅把resource类改名 `OAuthResourceIdentityController`，保持 `/resource` 路径、JWT校验、允许输出字段与Unicode空白校验不变；client `/token` 行为不改。
- 新增真实双模块test classpath的Controller共存/唯一class/route测试，原身份与安全测试改为引用唯一类名。
- API候选 `e15f7020bf77153912aafce15fc11c67b2f06e11` / tree `551c452f1a81bbc6f6b198452891d2189b967fd8`；Web保持 `41ca32b72fda97e8066783dc702b1218305ca395` / tree `0edb17f4f5420670630ab2b0f713a644a8af4bbd`。
- 工作证据 `/var/tmp/cyf-v1-9-2-release-20260918/`。R1缺构建属性、R2未获Gradle门禁、R3候选改名遗漏方法引用均如实保留；R4为新代码/修正配置的有界验证，不是盲目重试。

## 空间处理

仅对本任务1.7旧发布件逐字节核验后去重硬链接，两个发布路径与内容保留，移除其本任务旧worktree可再生build JAR，释放221,450,240实际分配字节；源码/测试证据/生产/恢复副本未清理。依据：`owned-v17-artifact-deduplication.json`。1.9.1恢复件保持完整。

## 当前状态

以下为发布前历史阶段，已由末尾实际发布/回归回执取代；旧失败与归因仍保留。

### 后续构建工具归因

R4组合classpath测试缺显式client API编译依赖，R5测试发现阶段launcher1.10.1/engine6.0.1不匹配。分别补testImplementation既有client starter与testRuntimeOnly launcher6.0.1，不改生产依赖。实际worker classpath与R5二进制报告保留；R6是修正candidate的新验证，不能称此前测试成功。


## 最终发布与线上回归

- API `e15f7020bf77153912aafce15fc11c67b2f06e11` / tree `551c452f1a81bbc6f6b198452891d2189b967fd8`；Web `41ca32b72fda97e8066783dc702b1218305ca395` / tree `0edb17f4f5420670630ab2b0f713a644a8af4bbd`。两组件远端develop与release/1.9.2均readback一致，未覆盖旧冻结分支。
- OAuth身份7+安全7+组合classpath1，**15/15 PASS**；bootJar成功，只有`jia-oauth-resource`生产依赖库改变，其余生产lib与1.9.1逐字节相同。不是API全量测试。
- API制品221,450,178B，SHA256 `4830c94eafff0e8650dcbd0accbb451ff2288e557726c8c0f6c7a7994916431e`；唯一运行Owner通过canonical launcher执行1次stop/start，PID2205187/start_ticks3124159032，健康UP/制品MATCH，无回退，发布锁释放。保留1.9.1可恢复副本与经济只读配置。
- Web保持1.9.1安装，不重建不重复安装；dist tree `71cf89effe55c7639c36e8f61e47ba6c4817db44ac3c9f14a6bba9d37a955596`，index SHA256 `cdf2aa63cdbe4ceacb5fee380cfd941a0fbf9199fa48b4402d0279be9fdd9628`。1.9.2是整套发布版本与组件exact关联，不伪造一次新的Web安装。
- 最终发布回执：`/home/isp/wsps/cyf/deliverables/releases/v1.9.2-local-20260918/release-outcome.json`，SHA256 `de50855ab6750440e28485df3dc4aef8b47766435b0730c24558458dd93ea279`；`build_origin=local_user_authorized`，无Flow Run。
- 新API上线后，主控自行执行真实OAuth/HTTPS **API46 PASS / 0 FAIL**，`/resource`已恢复200，匿名401保持；**完整本轮浏览器113 PASS / 0 FAIL**，无HTTP/JS异常，自有Chromium已退出、临时profile已删除。无伪token/响应mock、无业务写入/付费调用。
- 回归持久封存：`/home/isp/wsps/cyf/deliverables/releases/v1.9.2-regression-20260918/final-summary.json`；源码/构建证据：`/home/isp/wsps/cyf/deliverables/releases/v1.9.2-verification-20260918/`。交付清单：`docs/implementation/handoffs/V1_9_2_DELIVERY_20260918.json`。
- 两个执行Agent均关闭释放。运行台账技术任务done，`V1-9-2-USER-ACCEPTANCE-20260918`明确等用户本人验收；不是等待Reviewer或另一个Agent。

## 用户验收

1. 登录站点，进入**聚义厅 → 个人中心**，检查桌面与手机横竖屏下入口、返回、刷新。
2. 进入**经济预览**，查看本人钱包/流水、预算试算、技能目录与Agent权益，返回个人中心/聚义厅。试算不扣费。
3. 复看典籍目录/阅读；本轮自动回归只GET目录/正文/进度，不代替用户交互与真实手机验收。
4. 协作运行看板对当前普通账号应明确显示无权限；生产实际验证分支为FORBIDDEN，不是故障。未授予ops-read或开启read-enabled，不声称已验证特权非空看板。

边界：生产第二身份/另一client、真机、DISABLED分支及特权看板、非空商品/任务成果正例未新增证据；任务378缺可见fixture，旧server-hosting两表缺口仍是独立待办。语音与真实交易继续未启用。18个第三方来源浏览器资源由只读回归安全策略排除；不将本次159项通过扩大为全站全场景验收。

容量风险：根盘仍只约60MB可用；本次按实际制品字节完成可恢复安装，没有固定余量门槛。OOM历史和磁盘容量治理不是“回归通过”即可消除的风险，另行保留运维跟进，不在本次擅自删除恢复副本/其他任务数据。

SDD集成冻结分支：`codex/v1-9-2-sdd-release-20260918`，固定上述API/Web gitlinks；主工作区原index/无关修改保留。
