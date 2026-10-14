# AC12 Main 接续自检（2026-10-03）

- API候选 `dca432d8fa2b1477b24f415baa86f3927028c86b` / tree `eb39f3928a41f081e8f79e4cd73f41cc6fd28e21`，已推 `codex/ac12-integration-main-20261003`，保留 cabb8 已发布 RESULT 修复祖先。**尚未合 develop/生产构建/生产迁移/上线。**
- 41项 archive（含7真实隔离MySQL用例）及11项 workspace，共52项0失败0跳过；最终41新执行、11以未变输入的Gradle UP-TO-DATE复用，非重测52的声称。fixture仅Main自有33793/mmd_ac12main_*，无Provider。
- 修复继承候选的生产/测试编译错误、Mockito重复stub NPE及CHECK目录表达式误判。实际MySQL额外探针证明SQL UNKNOWN会放行NULL来源，修复为source union `IS TRUE`；保留原红证据，并增加9字段NULL拒绝、布尔/字面量漂移拒绝及DDL中断恢复。
- 生产只读预检：MySQL8.0.21，旧归档表0行、与新约束不兼容记录0、原417文字消息满足读取前置的计数1；只读事务ROLLBACK，无生产DDL/DML。该计数不等于真实保存成功。
- 迁移保留既有列与CHECK名称，旧API57初始化只检查原CHECK存在/启用，不因新增约束数量直接失败；仍须发布前绑定恢复包与实际安装，不声称旧程序回退全链路已实测。
- 当前正式Web仍1.13.56 / 78b83f / Flow158；API仍1.13.57 / cabb8；Client已1.13.57 / ed6f。AC12 Web候选8e9809也尚未上线。
- 下一步：配对版本化发布AC12，再做真实浏览器选区保存/下载；原417仍缺鸟图，结果恢复/无spool业务终止与完整34项不可宣称完成。
