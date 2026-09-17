# V1.7 本地API验证异常归因（2026-09-17）

1. `5350b29f/49a301df` 新主源码compileJava成功，但compileTestJava报旧测试签名不匹配（FundedBountyActor/TaskScope/legacy assign/report）。尚未执行preview断言。主控独立worktree提交`f53a0f0e`仅适配19个既有测试的显式owner参数，未减断言/改生产签名；须集成后重新定向编译及验证。
2. `2de9a52a/25607e` bootJar在项目求值阶段因缺少`ext.repoUsername`失败。与第一项不是同一根因。该字段只出现在根build.gradle的publishing仓库credentials闭包（109/110行），本轮不执行publish；本机未配置这两个Gradle属性。
3. 可执行整改：本地test/bootJar显式提供非敏感占位属性`-PrepoUsername=local-unused -PrepoPassword=local-unused`，先使用已有依赖缓存`--offline`。不需要索取生产凭据、不发布Maven、不改共享Gradle配置。若实际出现缺失依赖，按精确依赖错误另行归因，不盲重试同输入。
4. 保留两次失败原始记录。orchestrator累计失败门槛把不同根因也累计为2，本次只授权已明确整改的新输入，不删除历史、不修改其脚本治理逻辑。
5. 用户目标仍是验证后合develop/冻结release，不部署、不启动API、不操作生产数据。

## 17:10 编译范围收敛（不伪报全量测试成功）

主控`f53a0f0e`整模块compileTestJava消除了首批调用错误，但暴露后续100条既有command transport/state/artifact/event测试与现行接口不匹配。证据：`/var/tmp/cyf-v1-7-integration-20260917/compile-existing-tests-r2.log`。大部分报错文件相对develop并未被本轮修改；这是现有全量测试源码债，不是新预览功能断言失败。

不把本次功能发布扩展为整个历史测试体系改写，也不删除旧测试或给生产接口加不安全兼容参数。主控已用`c4edc150`撤销自己的19文件试探适配，保留分支/失败记录。验证改为显式独立sourceSet：完整编译并运行所有本次preview新增测试（含实际SQL fixture/事务代理/HTTP协议/ACL/无写入），另选已部署catalog/owner修复相关回归。此模式复用1.6的`schema-targeted.init.gradle`，不修改默认测试集，不允许对新测试设exclude/ignoreFailures。

API结论只能写“指定范围验证/生产构建结果”，不得写“全API测试通过”。全量既有agent测试源码编译债仍未解决，留给独立维护任务；本次release记录应明确披露。新功能任一定向失败必须先修复，不能因历史测试问题被笼统豁免。
