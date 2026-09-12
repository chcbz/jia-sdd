# CYF 阿里云 Flow 构建、测试与部署策略

更新：2026-09-12。按用户最新要求，日常发布以可用、轻量为准。

## 唯一默认路径

**功能具备上线条件 → 合入组件仓库 develop → Flow 自动测试 → 构建 → 同 Run 制品 → 自动部署 → 核验。任一步失败停止，不假报成功。**

| 组件 | 默认发布流水线 | 触发分支 | 云端验证 | 迁移状态 |
| --- | --- | --- | --- | --- |
| 后端 | `5260799 / cyf-api-kit-ci` | develop push（包括合并） | 59 个相关测试类、validateLayering、bootJar、私仓 OpenCV 摘要 | Run23 测试/构建/部署成功，精确制品与运行 PID/health 已核验；push 配置存在，触发行为仍待实际事件验收 |
| 前端 | `4403172 / cyf-web-kit` | develop push（包括合并） | JavaScript 扫描、npm ci、完整 npm test、Vite build | develop push 配置已保存 readback，Run92 已测试/构建/部署成功；实际 push 触发仍待验收 |

- 不再逐次签 ticket、改 YAML、排 Reviewer、人工放行或转 master 才发布。
- 合并前可按需使用 `5263690` / `5263692` 的 CI-only 诊断，不是必经前置步骤；它们不监听 push，避免同提交自动重复构建。
- Flow checkout 的完整 commit/tree 才是运行源码；不发布本地脏工作区，不用本地 Gradle/Vite 替代云端。
- 数据迁移、身份/ACL、事务或生产数据变更按自身风险在合并前处理；不把它们的独立审查套到所有普通发布。

> 2026-09-12：用户补充连接使用权限后，前端以原流水线的当前配置为基线，仅恢复 Gitee 服务连接和 develop push 触发，保存/readback 成功；没有覆盖已有测试/构建/部署修复，也没有重复启动 Run。Run92 部署单69505789及目标主机成功；它发生在本次触发规则修改前，不等于新 webhook 已验收。

## 固定流水线配置与部署

- 后端：`ops/ci/aliyun-flow/templates/backend-develop-release.yaml`。
- 前端：`ops/ci/aliyun-flow/templates/frontend-develop-release.yaml`。
- 后端打包脚本：`ops/ci/aliyun-flow/auto/package-api.py`；标准安装适配器：`ops/ci/aliyun-flow/host/cyf-api-flow-deploy`。
- 前端制品清单：`ops/ci/aliyun-flow/auto/package-web.cjs`；安装脚本：`ops/ci/aliyun-flow/host/cyf-web-flow-deploy`。
- 每次运行自动绑定 pipeline/run/commit/tree、制品哈希；不接受测试失败的制品进入部署。
- 后端保留既有事务安装、互斥、制品验证、磁盘检查和健康检查。旧 installer 的 `ticket_sha256` 字段仅兼容承载本次运行身份摘要，不代表人工审批、不含期限或固定提交。
- 两端下载到 Run 独立路径。主机只安装制品，不做源码编译；部署互斥，旧 Run 不覆盖已安装的新 Run。
- 前端仅部署 dist；逐文件校验，先资源后入口，入口文件原子替换；测试报告留在 Flow。暂保留旧哈希资源供已打开页面使用，不擅自清理其他任务文件。

## 操作与验收

1. 改配置前备份、固定候选 SHA；只写一次，再读取云端配置对账。
2. 普通发布由 develop push 自动触发；不要为同一次 push 再手动开一条 Run。
3. 需要手动诊断或验收时先查询现有 Run，明确目标分支与 SHA；不重试旧配置快照冒充新配置运行。
4. 查询/日志直接由主 Agent 执行，不读取 Reviewer 历史、不排队等门禁线程。
5. 成功必须有精确 Run、源码、测试、同 Run 制品、部署单/主机及线上校验。配置保存成功不等于部署成功。
6. 同输入同根因连续失败两次就停止盲重试，修正根因后再试。

## 配置迁移状态

新自动发布配置的实时保存/验收结果见 `docs/aliyun-flow-develop-auto-status.json`。以下为迁移前历史证据，**不是新配置成功证据**。

## 2026-09-12 CI-only 验收证据

### 后端 Run 1

- Pipeline：`5263690 / cyf-api-kit-develop-ci`
- 状态：`SUCCESS`
- commit：`a9d3e7417447a9f5f59a12523e582a8e8f1818f6`
- tree：`3352d0049871b588108eba0af990091a80fd965c`
- 门禁：定向测试、`validateLayering`、`:starter:bootJar`、OpenCV 私仓来源与摘要校验、`ArtifactUpload` 全部成功
- JAR SHA-256：`bbb6006e9abf611cea8168820d62558b2ebfef0d9d6f14a6987291edacb33fc9`
- 配置 canonical SHA-256：`0d63636ee01976630e0b51bf63fe9b82c4793967a0049ad12ab1c68d783f646b`

### 前端 Run 7

- Pipeline：`5263692 / cyf-web-kit-develop-ci`
- 状态：`SUCCESS`
- commit：`c9cbdccb7ceaa1cecab59bb4f2d6cd441042b2c3`
- tree：`2f82fca468197608cdaa7061d58d11785c6ca7ef`
- 运行时：Node `20.20.2`；Chrome for Testing `133.0.6943.141`；固定 WebP `1.2.0` 来源、ABI 与 SHA 校验成功
- E14：五项 gate 全通过；固定 10 秒 warmup、60 秒 sample，total p95 `0.8000000119 ms`、p99 `0.9000000060 ms`
- Mocha：`2118` tests，`2116` passing，`2` pending，`0` failures；mochawesome HTML/JSON 已上传
- Vite：`6.4.3` production build 成功，`8.84s`
- 制品：`104195319` bytes，SHA-256 `c62e9b9c4a3fea77b51e026bce10431844599b03d5250760f1fb216001c0dc37`
- 制品内部绑定同一 commit/tree，包含 `dist/`、`mochawesome-report/`、`source-commit.txt`、`source-tree.txt`
- 配置 canonical SHA-256：`1707fbf7191de5b4028063ee41c752e13c56eef1bb45b1d9ab554c82de71dfbf`

这些证据只证明各自固定 Run 的云端测试、构建和制品，不表示已生产部署。旧验收不能作为新自动发布配置已跑通的证据。

## 2026-09-12 当前生产验收证据

以下两个生产 Run 由其它执行者触发；本次流水线优化只做只读关联和产物核验，不将其归因于本线程，也没有重复触发生产。

### 后端 Run 18

- Pipeline：`5260799 / cyf-api-kit-ci`；状态 `SUCCESS`
- commit：`a8489561586400af049eee625d90b6e98e834f04`；tree：`1fd1cb7f60e279e4e934239434d4a3a7c8c59cdc`
- 构建 Job `513927230`：74 tests，0 failures/errors/skipped；`validateLayering`、`:starter:bootJar`、PublicArtifactVerifier、OpenCV provenance 与制品上传成功
- 发布 JAR：`220206485` bytes，SHA-256 `aa64ddf1be41147156236aa3d4f70121e2b95918d8dd2024d0cd3d0fec4df090`
- 下载包：`198144927` bytes，SHA-256 `2c04f7b03f37fc70fc7d673c486f0cc2f97813e0b7ba790c168c68a69ef12ffd`；内部 receipt SHA-256 `52afc26bee8438202ca45b9f986e74756ff79fe803465b1efff2d75752519286`
- 部署 Job `513935436`；部署单 `69495567`；主机组 `28833`；一批一台 `Success / healthy`
- 部署机日志确认 `ARTIFACT_ATTESTATION=MATCH`、运行用户 `cyf-api`、端口 `10018` 由目标 PID 监听、loopback `HEALTH=UP`，最终 `CYF_API_FLOW_INSTALL=PASS`
- 公网 `https://api.chaoyoufan.cn/actuator/health` 在本次核验中返回空响应，未独立证明公网反向代理 health；这不改变部署机 loopback health 已通过的结论
- 当前配置 canonical SHA-256：`919eb67be40c379507306633f224ce291f7338e216125df4dc7a956403672da3`

### 前端 Run 91

- Pipeline：`4403172 / cyf-web-kit`；状态 `SUCCESS`
- commit：`c9cbdccb7ceaa1cecab59bb4f2d6cd441042b2c3`，与前端 CI-only Run 7 相同
- 扫描、单测、构建、部署全部成功；Mocha `2118` tests，`2116` passing，`2` pending，`0` failures；Vite `6.4.3` build `9.77s`
- 生产包：`102898255` bytes，SHA-256 `da53366b2f302eb50cc1f63cd17783447aa36a7fe529787bc272fe28d8ce59b4`，Flow 日志 MD5 `e11298669fa2f73ae75697afaf81463e`
- 部署单 `69495496`；主机组 `28833`；一批一台 `Success / healthy`
- 包内 410 个文件全部存在于部署目录且逐文件字节一致；无缺失、无差异。部署目录另有 143 个不属于本次包的历史文件，当前入口不引用它们，但后续应改为 staging + 原子切换或按 manifest 清理
- 首页、`/juyiting` 均 HTTP 200；入口 HTML、主 JS/CSS、聚义厅懒加载 JS/CSS 共 5 个关键文件与同 Run 制品逐字节一致
- 当前配置 canonical SHA-256：`6feb2c10d5609b93f9e19fca8a09905ef3db91ba2ddba74d6693014c54c5c718`

完整非敏感机器可读摘要见 `docs/aliyun-flow-cicd-evidence-20260912.json`。


## 2026-09-12 18:54 CST 增量

- Web `4403172 / Run92`：develop `1ac5cb1e4973919bacf054e961b43ff24d47e832`，2117 passing / 2 pending / 0 failures；部署单 `69505789`，410 文件及 9 个线上响应哈希匹配。制品 SHA-256 `ab289e2791709f70202e161b57db2a35e24e55271148a67114019d5ec1285741`。手动发布已实成；自动 push 尚未启用。
- API Run22：58 类范围的测试/构建成功，但启动缺 `javax.mail.MessagingException`，发布器已自动恢复旧 Run18 JAR，health UP；不是新功能上线成功。
- 新候选 `688a3e65` 将 SMS mail 从 compileOnly 改为 implementation，新增隔离主运行 classpath 回归。Run23 已单次启动；59 类范围和 bootJar 实际 mail/activation/provider 类检查在制品导出前执行。未取得新运行健康证明前，不标后端发布完成。
- 安装保留锁与回退；仅将瞬时锁冲突改为固定 60 秒等待。同 Run 下载副本在验证身份及完整摘要后回收，保留 incoming、云端制品和回退 JAR，不降低 5GiB 运行余量。

## 2026-09-12 19:24 CST 发布闭环与并行推进

- API `5260799 / Run23 SUCCESS`：develop `688a3e6546dcacba116f76cbec7e1d91f72764f4` / tree `608e799ad81ab3c4876b376119af322901a903ef`；59 类 selector 范围、bootJar 实际 mail/activation/provider 检查通过。Build `514133208` 复用，未重复构建；部署 Job `514138578` / order `69507020` 单机 Success/healthy。
- JAR `a5cc9db17022291bc129b0536d5b8c785dac9efec4bf437ea503f3e183be721d` 与 canonical 文件一致；receipt `c9559c37aec9b1010d17e54a577e0eb5079b38377cb3abd32367129602819c08`；PID `2607082` 监听 10018，loopback `UP`。公开 `/agent/map` 命名只读探针获未登录 401；默认 curl 被既有 Nginx 规则拒绝，公网 actuator 未暴露，不能宣称已验证登录业务。
- 原 Run23 deploy 在 installer 前因协调 FD 继承失败。修复父 coordinator 持有 v2 mutex、installer `close_fds=True`；17 项控制测试通过，单次只重试部署 Job，新 JVM 无协调 mutex FD。未解除旧锁或手动终止服务；生命周期由 Flow 安装器完成。helper SHA `d3c7bb4fa94c5628068bdac3b9ecb2b332031811c42dfd15a8b48e1113ccd311`。
- 19:24 只读云端配置确认两组件均为 Gitee/develop/push/^develop$，webhook 已存在；此前“前端 push 未启用”描述已过时。配置存在不等于实际 push 自动触发已验收，下一次真实 push 先对账，不重复手动 Start。
- API 发布包、A03/A16 只读增量及 mail 运行依赖修复已闭环；完整 A16、M4/M5、案卷阁登录验收及付费业务仍未完成。A16/E01/F03 已分别派给并行 Owner，无独立 Reviewer。邮件监控已观察 SUCCESS，但三次邮件 helper 未接受，不能宣称邮件已发达。
- 完整精确证据：`/home/isp/wsps/cyf/docs/implementation/handoffs/FLOW-API-RUN23-DEPLOYED-20260912.json`。
