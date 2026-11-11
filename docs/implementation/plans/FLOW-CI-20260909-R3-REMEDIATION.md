# R3 有界整改：复用5256653并补回原私仓

用户最新决定：使用新流水线；复用既有5256653，不再新建、不修改1466118或4403172。本轮仅云端定向测试/构建、无部署。既有两次失败保留；不是对旧ticket原样retry。

## 原因与基线

- Run2缺少OpenCV不是用户未提供制品。19:39认证核实原私仓org.opencv:opencv:4.5.5 POMGET200/JARHEAD200；新工具遗漏私仓及认证。
- 工具基线e091630a50a09dfc7906b5b5d6848844ac910aa1/tree d53d0450995c4c1b14298cb80fcda8495e0f9f77，原Owner原worktree。
- API仍固定6267f3b16fe7b672a3c8479f058a662d9c75216c/tree936d6e4bcf3d7a4cc23cde62fa0e697be93d659b；不随develop移动。

## 源码整改唯一Owner及路径

原critical_worker Knuth，仅ops/orchestration/flow_remote.py、ops/ci/aliyun-flow/cold-init.gradle、该目录tests及README。不得改API、主控orchestrator基础逻辑、主控docs或其他worktree。

1. 在受审cold-init中增加原组织固定release/snapshot Maven仓库，禁止调用者任意指定仓库地址，凭证仅附着这两个HTTPS Packages仓库；pluginManagement/settings/project repositories保持一致。保留同源composite settings插件、公共仓库、外置缓存和无发布任务约束。
2. Gradle子进程env增加且仅增加CYF_MAVEN_USERNAME、CYF_MAVEN_PASSWORD；缺失/仅一项必须在Gradle前fail-closed。不得放入argv、ticket、fixture digest的原值、receipt、源码或制品；错误信息不得包含实际secret。发布属性不应携带私仓消费凭证，不增加publish权限或步骤。
3. 主控先只读流式取得私仓OpenCV POM/JAR SHA256（不落JAR或私钥）；该公开摘要可固定到受审工具/fixture绑定。云端对实际解析的OpenCV JAR验证此SHA256，拒绝同版本内容漂移，并在receipt可引用的非敏感证据中记录模块坐标和摘要；不是把控制机缓存搬到云端。
4. fake-wrapper测试覆盖两个秘密仅传Gradle、其他env不传、缺失拒绝、receipt/ticket/日志中无secret、私仓endpoint和OpenCV摘要约束；无真实本地Gradle。stdout/stderr若含实际secret需在写盘和输出前流式脱敏，并测试跨chunk边界；不放松构建native rc/测试门禁。
5. 一次针对性轻量自测后独立delta review，复用未变逻辑review证据。任何新失败先归因，第二次失败停止。

## 云端认证配置（仅主控）

- 从原1466118读取既有repoUsername/repoPassword到内存，沿用用户现有授权凭证，不声称其服务端权限是read-only。
- 通过官方CreateVariableGroup创建一个专用组cyf-flow-ci-maven-auth-5256653（若同名已存在先核对，禁止覆盖未知组）；变量CYF_MAVEN_USERNAME/CYF_MAVEN_PASSWORD均isEncrypted=true。
- 只关联5256653，不关联旧生产流水线；不会将AK或私仓凭证写入临时文件、命令行、报告或新YAML。
- 创建前列出既有组并记录请求时间；异常写只读对账，不盲目重发。读取组只输出id/name/isEncrypted，不输出value或完整API响应。链接关联的API字段按官方schema验证。
- Reviewer接受本计划后可创建该专用加密组；最终新工具+新ticket+变量组ID+精确无部署YAML仍须delta review，不能把本计划ACCEPT当作直接运行放行。

## 运行边界

- 原ticket已过期，不复用：新nonce、TTL、tool/fixture digests、云端cwd/toolroot/runbase。
- 手动触发一次新的构建；无triggerEvents，无deployment，保留失败证据上传和最终native退出门禁。
- 本轮成功仅表示定向cold构建通过，不是全量API/集成/生产发布通过。云端取源tip与实际固定6267单独核实。
