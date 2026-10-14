# 验收（更新与版本发布完成；新用户生产登记E2E未执行）
- 本机生成真实manifest和摘要可被Runtime校验；密钥不输出，权限0600，不覆盖旧目录。
- 非默认tenant/client正确贯通，不从owner或旧任务猜租户。
- UI仅明确动作登记；错误scope/含凭据导入被拒；查询不重复创建；状态不伪报在线。
- local文书/技能不再推荐旧API Key/codex-ws-agent或Node版本门槛。
- 本轮不创建新生产installation或执行enroll；已发布源码的正式测试与上线核验见末节，不把它等同新用户登记E2E。

## 2026-10-12 源码交付核对
- isp-install e3d7b30：8项离线测试PASS；实际manifest/host/secret读取器验证，指南中配置生成片段也实跑。完整指南和prepare工具已推develop。
- API 0fe830d1ea：文书投影真实Scope、无旧凭据/虚构路径；新增DTO及回归已提交推送；既有managedHostingRegression纳入本测试。仅静态diff自检，Gradle/validateLayering未运行，磁盘约59MiB不足以正式构建。不能标后端测试PASS。
- Web 3d0e9ef：133项本机低成本定向诊断通过，真实SFC挂载/JsonResult双层契约、跨身份回包、错误scope/密钥字段拒绝、同ID查询不重复创建和原页面行为覆盖；无本机生产构建。
- Web fixture来自真实prepare工具且有源码SHA/文件摘要，不把服务器绝对路径写入Flow测试。最终常规测试独立于isp-install仓库。
- 三仓develop源码已推送不等于部署。前端Flow、后端正式构建及真实安装/业务验收尚未执行；未执行生产DDL、enroll或服务切换。
- 证据：../../docs/implementation/evidence/selfhost-onboarding-20261012/source-status.json 及同目录日志。没有登记为accepted跨端证据。

## 2026-10-12 23:38 统一更新与发布
- isp-install `a39c085`：19项测试及Bash语法通过，指南、安装入口提示、README、AGENTS与Skill统一程序/配置/状态目录；既有HOME与SQLite索引迁移第9节明确保留身份和会话、不重新登记。已push develop。
- Web `aad2ae9` / **1.14.11**：Flow4403172 Run206成功，2932 passing / 2 pending / 0 failures；同Run不可变包部署，364安装文件和11公网响应摘要匹配，自家接应统一目录/prepare/不自动升级提示存在于同Run线上JS。原CI-only配置已恢复。
- API `0fe830d` / **1.14.11**：固定干净源码经原串行Gradle完成175项（0失败/错误/跳过）、validateLayering、依赖完整性及fresh bootJar；build ID `cyf-selfhost-onboarding-api-20261012-r2`。原准入/发布锁/备份/安装器完成，canonical JAR与制品SHA匹配，PID3160131、healthUP；公网/loopback受保护只读API均401，F06/E05只执行existing_equivalent，无新DDL。
- 期间主机OOM杀死原API，已记录原始证据并经canonical入口恢复，再完成本次安装；不是隐去的构建成功。现行Runtime进程未重启、二进制仍1.0.2，不宣称所有目标机自动升级。
- 新生产installation/enroll、付费调用、本人登录完整新用户接入E2E未执行；离线/隔离回归与已发布字节核验不替代这些业务动作。
- 精确摘要、制品、原日志路径和异常恢复见 `../../docs/implementation/evidence/selfhost-onboarding-20261012/unified-release-status.json` 及主handoff。
