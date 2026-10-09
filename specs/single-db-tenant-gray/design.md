# 单库多业务区域与测试区域总体设计

版本 2.0-draft；本版取代原单库双环境模型。完整开发契约见 [详细设计](detailed-design.md)，设计审查与实施验收分开记录。

## 1. 三个维度

| 维度 | 作用 | 关系 |
| --- | --- | --- |
| client_id | OAuth 调用应用 | 与可访问 tenant 多对多，不决定用户权限 |
| tenant_id | 业务区域、数据隔离 | 0 华南区、1 华南测试区、2 华北区仅为示例；0 非公共 |
| deployment_id / stage | 运行实例与技术环境 | 共享实例可多区域，本地可限制为 1；版本不由 tenant 推断 |

同一数据库和业务表；同一套应用可以提供 NORMAL 和 TEST 区域。独立本地 client/进程只是可选部署安排。TEST 区域能力按注册属性限制，不写 if tenant=1。

## 2. 身份和选区

用户成员权限、应用区域/数据域授权、token scope、区域能力、部署范围与资源 ACL 共同决定准入。

OAuth 保留授权码/PKCE，中央登录页提供区域选择；tenant_hint 仅是期望目标。授权事务绑定 client、用户、tenant、回调、PKCE、成员/grant 版本，兑换和刷新再次核验。一个 token 只有一个 tenant，切区重新授权，SSO 可免输密码。

| 接口 | 目标契约 |
| --- | --- |
| /oauth2/authorize、/oauth2/token | 既有端点扩展选区授权，不能在兑换/刷新时改 tenant |
| GET /oauth2/tenant-options | 中央会话及同会话授权事务，列出成员与应用授权交集 |
| POST /oauth2/tenant-selection | 中央会话、CSRF、绑定授权事务的选区操作 |
| GET /resource | 保留现有字段，新增 tenantId/Name/Kind、issuer 与区域/成员/grant 版本；no-store |
| GET /agent/tenant/capabilities | 当前区域能力与状态，仅 UI 提示，每次业务请求独立鉴权 |
| /internal/tenants/{tenantId}/control、/transitions | 内部区域状态查询/变更；明确管理权限、版本与幂等 |
| POST /internal/deployments/{deploymentId}/drain | 只排空部署，不暂停其服务的区域 |

旧无 tenant token 仅限明确单区映射和截止期；多区 client 启用切区前结束兼容。机器凭据依注册归属验证，不开放用户任意选区。

## 3. 数据归属与迁移

目标范围为 tenant + dataDomain + owner/成员 ACL。dataDomain 是稳定业务产品边界，首期 cyf，不等于 OAuth client。client 用于调用鉴权及来源审计，凭据与应用专属配置仍可归 client。

旧数据不能直接扩大可见范围。各域先保持 LEGACY_CLIENT，只有审核归属和共享权限、回填 data_domain、解决自然键/幂等/账本冲突、文件旧 locator 兼容并统一发布后才能切 DOMAIN。同库tenant/module控制行持久维护 LEGACY_CLIENT→QUIESCING→DOMAIN、modeRevision/migrationEpoch；关联组停写停领、排空并seal后才迁移，再CAS切换。部署登记支持模式，启动及每次业务/领取检查，旧准入和回执拒绝。更早无门禁实例须退出并撤销凭据/连接。新区域所开放域必须是DOMAIN，不能请求选择模式或查询失败回退。

采用显式 Scope repository；无范围 ById/batch/map/update/delete 禁止业务使用。所有 SQL、JOIN、锁、分页、统计、清理带精确范围；公共目录只有逐方法只读白名单，不使用 OR tenant=0。

## 4. 前端

共享 Web 支持选区；本地默认1、可 fixed 限制。区域身份与技术部署标签分开显示。

候选 token 在 /resource 验证前不持久化、不提供业务请求使用。IndexedDB 事务以 authRevision、authSetRevision、viewRevision、transactionId 完成跨窗口 CAS；登出保留 revision 墓碑。目标未知的中央选区使用 authSetRevision 防迟到覆盖，具体协议以详设第8节为准。

认证存储按 issuer/origin/client/tenant 分开；浏览器业务状态按 issuer/origin/client/tenant/domain/owner，并校验成员/grant/scope等权限指纹；跨应用服务端共享不等于本地缓存共享。任何授权开始/取消/提交/登出都会推进authSetRevision，未知选区不会覆盖较晚开始但尚未提交的定向登录。每个窗口保留自己的当前区域；切区取消流、上传、语音、轮询、Blob URL 和旧上下文，晚响应检查持久 revision 后丢弃。

## 5. 区域控制与部署控制

区域 control、模块迁移门禁、成员、client grants 在同库受控管理；部署注册、工作器代次和tenant/domain/pool授权单独维护。业务锁顺序为tenant control → 按moduleId排序的module control → client grant → membership/机器授权 → deployment → 原业务顺序。Agent凭据单租户；共享worker凭据绑定部署及受信任授权元组集合，每次明确选择并核验一个元组。

区域状态：ENABLED → AUTH_CLOSED → WRITE_CLOSED_CLAIM_CLOSED → DRAINING → DISABLED。紧急可直接关闭写入/领取。期限从关闭写入起算，BEGIN_DRAIN 不延长或扩大集合；cutoff 时有效 lease 须有持久事实证明。恢复递增区域身份/工作准入代次，不自动改变所有部署代次或复活旧积压。

控制变更持排他锁，锁内当前读幂等记录后才检查 If-Match；与操作快照同事务提交，重试返回原结果。部署 drain 使用独立持久控制记录，不改变 tenant 状态。客户端与中间件故障均不回退 ENABLED/tenant0。

## 6. 异步、文件与副作用

后台扫描先按 tenant/domain/pool 过滤；非本范围不锁定、领取或标 DEAD。同 tenant 的本地新代码验收使用独立执行池和 Agent，避免与共享 worker 随机争抢。

消息依既有 canonical codec 分配新版本；权威记录校验 tenant/domain/pool、admissionEpoch、执行者部署代次、lease/attempt。旧版适配只对受审历史范围开放，不默认补值。SSE/WS/replay/缓存/检索/存储全链保持范围。

历史文件保留含 client 的旧 locator，在新业务元数据授权后读取，不按当前调用 client 重算路径。TEST 区域默认禁止真实资金/生产外部操作，允许真实 LLM 时设置预算；不能伪造成功。

## 7. 发布门槛与实际状态

盘点 → 归属/授权映射 → 同库兼容扩展 → 全部实例严格租户基线 → 各域 DOMAIN 切换 → 注册业务区/成员/grants → 小样本开放。旧 tenant=owner、0/1/2 占用及跨 client 数据共享必须有确定证据。

同库没有数据库级行安全保证；本地账号不授 DDL。区域测试不能隔离 schema/资源故障。回退仅限当前租户与数据域模式兼容版本，不清库、不批量归零。

独立 worktree 中仅有部分实施；现场 DDL/成员/客户端/部署仍待核验，不声称已合 develop，不执行迁移或部署。详设第14节列出设计基线源码证据，实施进展与阻断点见验收及盘点文档。
