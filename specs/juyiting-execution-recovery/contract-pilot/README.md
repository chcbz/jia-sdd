# 执行历史共享契约试点

范围：既有只读 `GET /agent/personal-workspace/executions`。不新增产品行为，不访问生产、不登录真实账号、不调用 Provider。

## 两种验证，不混淆证据

|入口|实际覆盖|定位|
|---|---|---|
|`check-consumer.mjs`|生产 Vue composable + 注入 JSON 响应，30条断言|快速消费者诊断，不证明 HTTP/数据库|
|API `:agent:jia-agent-service:executionHistoryHttp` + `check-http.mjs`|签名 JWT → loopback Tomcat/Spring Security → 生产 Controller/事务 service/DAO/MyBatis → 独占 MySQL8；生产 createApi/useHttp/fetch → Vue 状态|真实只读跨端链路；前端部分仍是本地低成本诊断|

共享期望/种子唯一来源是 `execution-history.json`。schemaVersion2 将旧的不可能分页样例（limit20、只有1条却返回游标）修正为20+1条；没有修改产品逻辑迎合测试。JSON `source` 是基线，**实际受测 commit/tree、输入摘要见 evidence**。

真实链路检查：五类响应逐字段比对、20+1分页、空页与503区别、非法游标400、缺失/错误JWT401、缺失scope400、owner/client大小写及跨租户数据不泄漏、切换身份清空前端状态、`private, no-store`。应用数据库用户只授 SELECT，MyBatis禁止写操作，前后全表快照一致。未使用模拟 HTTP/SQL 返回值；历史查询之外的协作者采用失败即停的桩，防止生成/派发副作用。

## 单命令入口（2026-10-08）

不再手工拼装7个环境变量和临时runner。Owner先按既有流程固定API干净commit/tree和任务验证阶段，然后执行：

```bash
python3 -B /home/isp/wsps/cyf/ops/orchestration/execution_history_check.py \
  --task-id EXECUTION-HISTORY-CHECK-20261008 \
  --api /home/isp/wsps/worktrees/cyf-execution-history-http-integrate-20261008 \
  --web /home/isp/wsps/worktrees/cyf-contract-consumer-20261008 \
  --credentials-init /root/.gradle/init.gradle
```

- 日常任务换成自己的task-id、固定API/Web工作区。Web必须与共享JSON的基线匹配，不自动改JSON或切分支；本地develop与候选差异只作提示，不假定远端/线上同步。
- 加 `--check-only`：检查干净源码/台账SHA、合同、JS语法、任务定义、依赖与工具指纹；不提取凭据、不构建、不启动服务、不写证据、不改任务状态。`PRECHECK_OK`不代表测试通过。
- 真正执行前，现有任务必须由Owner处于 `targeted_verification`/`verifying`。工具不创建/认领任务、不自动转阶段、不授权解除两次失败停止。完整证据命中时仅只读复用，完成任务也能查询，无需为了查证据重新开工。
- 凭据优先取 `CYF_MAVEN_USERNAME/PASSWORD`；`--credentials-init`是显式选择已有消费型配置的可选备用。不复制/打印凭据，不修改全局配置；Java/Node测试子进程剥离Maven凭据。不需要凭据就能预检/读缓存。
- 执行顺序：JS语法/合同/源码检查 → 可验证的缓存 → 注入式消费者廉价回归 → 现有编排器/全局Gradle锁 → 真实HTTP/MySQL链路及 `validateLayering` → 结果、JUnit和输入稳定性复核。所有Gradle都走编排器；不在本机生产打包前端。
- 缓存miss才执行Gradle。证据键覆盖API tree、selector、JSON/脚本、Web tree、Vue/consola实际安装依赖闭包、工具链、本地init和编排/入口脚本摘要；根目录普通文档变化和临时目录名不使键失效。已声明测试结果文件为Gradle输出，防止只报UP-TO-DATE却没有本批结果。
- 缓存hit还会验证manifest/result/JUnit/log摘要，缺失或篡改直接报告，不把历史exit0当本次通过，也不静默重建。旧的临时runner证据不自动冒充新入口的完整缓存。
- 输出只保留 `PASS` / `REUSED` / `FAILED` 与统计、证据路径；失败输出首条诊断（根因仍须Owner确认），经现有编排器归因，不自动重试。未触发Gradle的失败也不能当链路通过。

证据默认保存在 `/var/tmp/cyf-execution-history-check/run-*`，每次新运行独占目录，复用同tree的编译输出；完整日志不灌入聊天。记录首次有效反馈和本次命令耗时，未知的人工作业/等待时间不补造。Java fixture负责正常完成/断言失败时关闭自己创建的MySQL/Tomcat/Node，不扫描或终止其他任务进程。验收后需要长期保留的证据按既有handoff归档。

仍可单独运行原30条消费者快速诊断；它不需要Java/MySQL，但不是实际HTTP验收：

```bash
node /home/isp/wsps/cyf/specs/juyiting-execution-recovery/contract-pilot/check-consumer.mjs \
  /home/isp/wsps/worktrees/cyf-contract-consumer-20261008
```

## 证据与边界

- 本轮结果及源码身份见 `evidence/20261008-http.json`，执行/修复/集成记录见根目录任务handoff `EXECUTION-HISTORY-HTTP-20261008.md`。
- 这是**执行历史只读接口**的真实链路，不代表整个聚义厅全部跨端功能已验收。
- JWT为合成签名身份，安全链为测试专用 Spring Security 配置；不证明生产OAuth登录或整站安全配置。
- Vue响应式状态在Node运行，不是浏览器页面渲染/E2E；复用已有node_modules，不声称依赖安装完整性验证。
- 未运行前端正式Flow，未部署；不得当作发布门禁通过或已上线。
