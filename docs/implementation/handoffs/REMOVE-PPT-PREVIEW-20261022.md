# REMOVE-PPT-PREVIEW-20261022

- Owner：本聊天；用户明确删除上轮解释的PPT在线预览功能。删除PPT/PPTX在线预览及逐页PNG渲染、对应契约/测试与专属字体bootstrap；保留PPT上传、下载、生成/交付能力及格式合法性校验，保留其他格式预览、原身份/ACL/摘要校验。无生产部署授权。
- 已读根/home/isp/wsps/cyf/AGENTS.md、组件AGENTS、ops/orchestration/README.md、Flow入口和共享技能（冲突旧自动部署条款不用）；接口规范/home/isp/wsps/cyf/api/docs/interface-standard.md v1.2，public envelope不变，仅PPT预览UNSUPPORTED。
- 根基线5e6ab2b6f1a156c320189f17d76941fbe623738a，主组件checkout是他人活动分支且前端原型有脏修改，禁止覆盖。独立任务worktree：/var/tmp/cyf-remove-ppt-preview-20261022/api、web，分支codex/remove-ppt-preview-20261022；fetch origin/develop后从API7841057b057c012cfa203fb658c1043500be055e/Web669bdc9d6439d1bd7eb71df5ed401202a648f419起步。工作区为本Owner自行读取规则，不派子Agent。
- 本机磁盘余量较少，仅对本任务web worktree开启sparse checkout排除public静态资产，不删除其他Owner内容，不本机生产构建。
- 最早验证：定向源码/契约与Python流水线工具测试、JS语法；正式Java/Node全测试及构建使用原Flow。先明确删除边界再维护流水线，不能先去掉字体导致旧PPT测试失败。必要测试更新为PPT预览不支持、原文件下载/权限不变。

## 源码与本机轻量验证

- API `683adf775fafce7ac0cc275cf0584543976149f8` / tree `68e5a4a6944e96b90f579c96ce6c266cfbcde69b`；Web `232a32ffe32d941a8e546db407fc85697b3b6c8c` / tree `9fb2c2085eb4eb9fdc43effc94ff56ee706ee19c`。两端已普通快进push到develop，未切换/覆盖主checkout。
- 前端定向Mocha 26/26，文档预览静态合同及浏览器smoke脚本语法检查通过；未运行浏览器smoke，不将mock/静态检查当实际浏览器验收。后端CI工具6项及资源分工3项通过。
- 默认service:test源集仍编译全部测试，新增两个 --tests selector（PersonalWorkspacePreviewRendererTest/AgentTaskDeliverableControllerTest）到既有policy，不新增重复隔离编译任务。旧Run235未选这两个测试，不冒充本次证据。
- 后端云端配置已保存前值并readback为APPLIED；candidate SHA256 ca2dab162c49207b5f854c528a2e15c957a95f32df4008f3159cfb8c6d1070aa。未改前端云端配置；两端均无部署阶段。控制记录 /var/tmp/cyf-remove-ppt-preview-20261022/。

## Flow验收收口（2026-10-23 00:03 CST）

- 两端push后只读确认无自动Run，再各手动触发一次；创建初期源信息未就绪返回UNKNOWN（API236/Web297），仅查询该返回Run，未重复触发。终态均SUCCESS且源码完整SHA一致。
- Web297：108秒（1分48秒），3253通过、2 pending、0失败，613个dist文件逐一核对同Run manifest；源commit/tree均匹配。前次Web296为127秒，两次源码不同，不将时间差全部归因于删除功能。
- API236：328秒（5分28秒），2849项中2727通过、122跳过、0失败/错误；本次相关三套回归34/34通过且无跳过（renderer9、deliverable12、workspace13）。保留validateLayering、fresh bootJar及原测试；比旧默认显式增加21项预览/成果接口测试。
- 同Run制品以流式方式核对来源、完整manifest/receipt/metadata/sidecar摘要，未在低磁盘主机落大压缩包。Web压缩包SHA256 `3a08321c2e550ff1c0a28cb707263d38fd837506d0fb6d4969e0b5f5dc05f7f1`；API压缩包 `b1a0290dd99a3a4f0a016861255bfd3d9bcdf1151ab4ac9b00406ce68a995381`，JAR `68fbc431242bae2518caf7b1ead820dbfce66640d2b5bd291097a187788b479a`。
- API字体安装阶段已消失，但本轮总耗时比Run235的293秒增加35秒，不能宣称整条流水线提速。Gradle从147.789秒增至213.921秒；当前源码变动重新执行service compileJava约33.49秒、compileTestJava约34.21秒等，旧Run同源码热缓存不能作为同条件对照。仍需同源码热缓存样本才能评估稳定耗时，本任务不为凑缩时数字追加Run。
- 紧凑证据见同目录 `REMOVE-PPT-PREVIEW-20261022.evidence.json`；完整控制面/日志/summary/前值保留 `/var/tmp/cyf-remove-ppt-preview-20261022/`。未执行生产安装、重启、卸载服务器字体、取消他人Run或浏览器业务验收。
- 两端develop已快进集成，主checkout仍保留其他Owner活动分支/脏改动，根gitlink未强行移动。根Flow配置和业务文档为在原有脏工作区上的局部更新，未捎带提交其他Owner修改。开发与云端测试/构建完成，生产未部署。
