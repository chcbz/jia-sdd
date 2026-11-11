> 2026-09-09 最新用户决定已改为复用新流水线5256653。本文件只保留历史方案，不授权修改或触发旧1466118。当前方案见 FLOW-CI-20260909-R3-REMEDIATION.md。

# 原流水线1466118优化：私仓核查与归因修正

## 已核实

- 用户已明确OpenCV在既有私仓，并同意优先直接优化原流水线1466118/cyf-api-kit，不再增加流水线。
- 本次认证API查询最新历史Run167仍为SUCCESS，开始于2026-06-21 23:45:19 +08。它不是本次验证运行，也不能证明当前develop通过。
- 原构建命令在Gradle properties/init.gradle中配置现有release/snapshot Packages私仓及认证；目前仍有`./gradlew build -x test`。
- 使用原流水线既有凭证（仅内存）对release私仓中org.opencv:opencv:4.5.5执行只读核查：POM GET200，389字节，坐标匹配；JAR HEAD200/application/octet-stream。未完整下载JAR，不声明JAR摘要已核验。凭证未输出、未复制到仓库/日志/命令行。
- 非敏感证据：docs/implementation/plans/FLOW-CI-20260909-private-maven-verification.json。

## 正确归因

Run2失败不是用户缺少OpenCV制品，也不需要用户重新发布或替换依赖。新cold-init只添加公共仓库，并把repoUsername/repoPassword设为空，远端环境allowlist也未承接Maven认证，遗漏了原流水线的私仓依赖配置。这是本次迁移实现遗漏。

保留两次失败历史，不将纠正归因视为新运行成功，不清除blocked_root_cause或盲目发Run3。

## 优化范围与当前操作边界

1. 优先复用1466118的私仓release/snapshot和原有OpenCV坐标，先改构建相关配置；不更换OpenCV、不另建流水线、不复制本地缓存。
2. 私仓认证应通过受保护的构建变量/临时配置传递，限制到明确的Packages仓库；不进入ticket、receipt、日志或上传制品。现有写权限未知，不能宣称凭证已最小权限化。
3. 继续保留扫描，补充云端测试与精确制品摘要；验证构建和生产部署必须有明确分离开关，不能为验证直接启动目前含主机部署的旧流水线。
4. 私仓配置可复用不代表旧部署脚本安全问题已经解决；root-owned安装器、联合promotion和schema门禁仍按原评估。
5. 本次API显示原flow为`schema: tb`旧格式；官方UpdatePipeline文档明确“只支持更新YAML化流水线”。当前未调用任何原流水线写API，也未尝试把新YAML强行覆盖旧流水线。需要控制台编辑，或先确认是否支持原ID转换为YAML；目前没有核实转换入口，不能要求用户点一个假定存在的按钮。
6. 新流水线5256653仅保留历史诊断证据，不继续运行、不删除；现有两条生产流水线未修改/未触发。

下一步：在原流水线控制台确认可用的编辑方式；随后冻结最小构建配置改动并独立审查，再原地写回。当前仅完成私仓核查和方案归因修正。
