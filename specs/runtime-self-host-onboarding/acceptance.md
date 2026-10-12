# 验收（待执行）
- 本机生成真实manifest和摘要可被Runtime校验；密钥不输出，权限0600，不覆盖旧目录。
- 非默认tenant/client正确贯通，不从owner或旧任务猜租户。
- UI仅明确动作登记；错误scope/含凭据导入被拒；查询不重复创建；状态不伪报在线。
- local文书/技能不再推荐旧API Key/codex-ws-agent或Node版本门槛。
- 所有生产登记/上线/业务验收未执行，不以源码测试替代。

## 2026-10-12 源码交付核对
- isp-install e3d7b30：8项离线测试PASS；实际manifest/host/secret读取器验证，指南中配置生成片段也实跑。完整指南和prepare工具已推develop。
- API 0fe830d1ea：文书投影真实Scope、无旧凭据/虚构路径；新增DTO及回归已提交推送；既有managedHostingRegression纳入本测试。仅静态diff自检，Gradle/validateLayering未运行，磁盘约59MiB不足以正式构建。不能标后端测试PASS。
- Web 3d0e9ef：133项本机低成本定向诊断通过，真实SFC挂载/JsonResult双层契约、跨身份回包、错误scope/密钥字段拒绝、同ID查询不重复创建和原页面行为覆盖；无本机生产构建。
- Web fixture来自真实prepare工具且有源码SHA/文件摘要，不把服务器绝对路径写入Flow测试。最终常规测试独立于isp-install仓库。
- 三仓develop源码已推送不等于部署。前端Flow、后端正式构建及真实安装/业务验收尚未执行；未执行生产DDL、enroll或服务切换。
- 证据：../../docs/implementation/evidence/selfhost-onboarding-20261012/source-status.json 及同目录日志。没有登记为accepted跨端证据。
