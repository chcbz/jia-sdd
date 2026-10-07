# 当前交付顺序（用户于 2026-10-03 调整）

用户指令：“先把功能开发完，更新文档，然后提交到远端特性分支。在服务端再做全面验证。”

## 顺序和边界

1. 按原 D2 完整功能范围收口源码，不删减已明确的恢复限制、分页、章节持久检查点、发布 STAGING 恢复、安装副本配额与引用回收、来源孤儿/PENDING 恢复等需求。当前仍是 implementing / NOT_COMPLETE。
2. 本地保留必要的定向行为自检、编译/语法及明显错误检查；独立只读源码审查保持。**反复本地全套回归、隔离 Runtime 和浏览器全面验证不再是首次完整源码推送的前置条件。** 已产生的局部结果、原始失败和 REJECT 记录原样保留。
3. 更新功能/接口/恢复/迁移与使用文档，明确“开发完成”“源码已推送”和“服务端全面验证”是不同事实。API/Web/Client 在现有特性分支先提交并普通 push，核对 exact 远程 SHA 后更新 Root gitlinks/Client pin，再提交并推送 Root 特性分支；不合并 master/develop，不 force-push。
4. 推送后，在任务隔离的服务端开发工作区开展完整回归、真实共享 Runtime/Client/HTTP/浏览器验证。逐项记录实际结果和既有失败；发现问题继续修复并推送同一特性分支。Gradle 始终使用共享 `/tmp/cyf-gradle.lock` 且串行执行。
5. 服务端全面验证未完成时只声明“开发完成/已推送，服务端全面验证待执行”，不声明整体已验收。84 项真实业务验收与部署/激活单独记录，不用组件或开发 fixture 的 PASS 冒充生产业务 PASS。

## 授权范围

本指令授权功能开发、文档、特性分支提交推送及服务端开发验证，不授权生产部署、生产数据库迁移、真实典籍上架、生产任职/安装激活或付费模型调用。原工作区和其他任务的数据、进程与分支均保留。

## 当前源码状态

Native 精确合同与 RECOVERY-13 三项恢复边界修复均已局部审查接受并本地提交，尚未推送完整增量；新增 MySQL 恢复/升级 selectors 仅编译，待服务端执行。连续分页已定向自检与独立窄审接受并本地提交。章节持久断点已完成77 API / 80 Client定向PASS及独立审查并本地提交；发布 STAGING 恢复已77 API定向PASS及独立审查并本地提交；唯一 Writer 正在补配额/引用回收与来源清理，完整文档尚未收口，因此本轮完整源码 push 未发生，服务端全面验证尚未执行。紧凑剩余路线见 remaining-source-plan.md，机器状态以 integration.yaml 为准。

## 2026-10-07 最新接续（覆盖历史当前状态）

原D2源码与文档已收口并普通推送，全部局部源码包独立接受。API `5722e7fa2ee0d1f6a5eeb84ccf18dcfe009ae4e7` / Web `6dd4553c276c34a1d694a06a3daf11849dca0e64` / Client `9426030d4a9411429bbc1ad2bd154356a0287e3b`；Root源码交付提交 `8d77bcd325bd3cb4e6d589bc6add8071a3ceb09b` 已核对远端。最后生命周期Client Linux104PASS，API同树Chat76PASS及Agent17Windows环境失败原件保留。

**服务端全面验证 BLOCKED，尚未完成。** 独占工作区已检出上述精确源码；attempt1–3配置失败且tests=0，attempt4主动停止本任务JVM，attempt5最后观察到compileJava，其后退出码/XML/结果与自有进程、MySQL关闭和Gradle锁释放均未确认。前次SSH曾公钥认证成功但session open超时，本次只读重试仍exit255/连接超时；不据此认定认证错误或唯一资源根因。完整回归、实库迁移/并发selector、真实Runtime/浏览器结果不可标PASS，远端原始attempt日志尚未取回。

原件 `evidence/delivery/resume-20261007/{root-source-remote-receipt.json,server-validation-status.json,ssh-resume-readonly-20261007.log}`；恢复后先只读核本任务进程parent/cwd/argv、独占datadir及锁，不能按旧PID盲目kill或重启生产。准备脚本不是已完成验证，运行前须重新绑定真实完成尝试与精确源码。生产发布/迁移/真实任职与上架/付费调用未执行，84业务用例仍not_run/evidence=null；whole-feature accepted=false。
