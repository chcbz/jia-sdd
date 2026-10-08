# 执行历史共享契约试点

范围：既有只读 `GET /agent/personal-workspace/executions`。不新增产品行为，不访问生产、不登录真实账号、不调用 Provider。

## 两种验证，不混淆证据

|入口|实际覆盖|定位|
|---|---|---|
|`check-consumer.mjs`|生产 Vue composable + 注入 JSON 响应，30条断言|快速消费者诊断，不证明 HTTP/数据库|
|API `:agent:jia-agent-service:executionHistoryHttp` + `check-http.mjs`|签名 JWT → loopback Tomcat/Spring Security → 生产 Controller/事务 service/DAO/MyBatis → 独占 MySQL8；生产 createApi/useHttp/fetch → Vue 状态|真实只读跨端链路；前端部分仍是本地低成本诊断|

共享期望/种子唯一来源是 `execution-history.json`。schemaVersion2 将旧的不可能分页样例（limit20、只有1条却返回游标）修正为20+1条；没有修改产品逻辑迎合测试。JSON `source` 是基线，**实际受测 commit/tree、输入摘要见 evidence**。

真实链路检查：五类响应逐字段比对、20+1分页、空页与503区别、非法游标400、缺失/错误JWT401、缺失scope400、owner/client大小写及跨租户数据不泄漏、切换身份清空前端状态、`private, no-store`。应用数据库用户只授 SELECT，MyBatis禁止写操作，前后全表快照一致。未使用模拟 HTTP/SQL 返回值；历史查询之外的协作者采用失败即停的桩，防止生成/派发副作用。

## 运行

先查看项目 AGENTS 和最新相关 build.gradle。API 在固定干净 commit/worktree 经编排器串行执行；本机不做前端生产构建。

```bash
node /home/isp/wsps/cyf/specs/juyiting-execution-recovery/contract-pilot/check-consumer.mjs \
  /home/isp/wsps/worktrees/cyf-contract-consumer-20261008
```

真实链路的 Gradle Test 环境输入：

- `CYF_HISTORY_CONTRACT`：共享JSON绝对路径。
- `CYF_HISTORY_NODE_SCRIPT`：`check-http.mjs`绝对路径。
- `CYF_HISTORY_WEB` / `CYF_HISTORY_WEB_COMMIT`：干净Web工作区及固定SHA（脚本还核对JSON中的Web基线）。
- `CYF_HISTORY_MYSQLD`：MySQL8 mysqld绝对路径；只初始化自己的临时datadir、随机loopback端口，不连接已有库。
- `CYF_HISTORY_NODE`：Node20可执行文件绝对路径。
- `CYF_HISTORY_RESULT`：本次独占结果文件绝对路径。

使用项目本地消费型 Gradle init（仓库、OpenCV完整性校验不变、外置构建输出、子进程剥离Maven凭据），经 `cyf_orchestrator.py gradle` 执行以下 selector：

```
:agent:jia-agent-service:executionHistoryHttp validateLayering
```

编排证据键包含精确API tree、selector与fixture digest；digest至少覆盖JSON、Node脚本、本地init、Web commit/lockfile。结果绑定manifest、Gradle完整日志、JUnit XML与JSON；不要用新SHA描述旧测试。临时Node、Tomcat、MySQL由创建它们的测试负责关闭，不操作其他任务服务。

## 证据与边界

- 本轮结果及源码身份见 `evidence/20261008-http.json`，执行/修复/集成记录见根目录任务handoff `EXECUTION-HISTORY-HTTP-20261008.md`。
- 这是**执行历史只读接口**的真实链路，不代表整个聚义厅全部跨端功能已验收。
- JWT为合成签名身份，安全链为测试专用 Spring Security 配置；不证明生产OAuth登录或整站安全配置。
- Vue响应式状态在Node运行，不是浏览器页面渲染/E2E；复用已有node_modules，不声称依赖安装完整性验证。
- 未运行前端正式Flow，未部署；不得当作发布门禁通过或已上线。
