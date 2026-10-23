# 任务派发与路径归属
运行状态唯一源：/home/isp/wsps/cyf/docs/implementation/TASKS.yaml#runtime_ledger_json；本文件只冻结范围，不另建状态台账。

## JYT-FLOW-BE-20261008 — critical_worker / gpt-6.1-sol high
职责：修复点将原意图启动接续与对应回归，自检后提交独立commit。
worktree：/home/isp/wsps/cyf/.worktrees/jyt-flow-bootstrap-20261008
owned paths（相对该worktree）：
- chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatBountyBootstrapRelay.java
- chat/jia-chat-service/src/main/java/cn/jia/chat/config/ChatTypedDeliberationSchemaInitializer.java
- chat/jia-chat-service/src/main/java/cn/jia/chat/service/ChatTypedDeliberationContextService.java
- chat/jia-chat-service/src/chatDeliberationTest/java/cn/jia/chat/service/ChatBountyBootstrapRelayTest.java
- chat/jia-chat-service/src/chatDeliberationTest/java/cn/jia/chat/config/ChatTypedDeliberationSchemaInitializerTest.java
- chat/jia-chat-service/src/chatDeliberationTest/java/cn/jia/chat/service/ChatTypedDeliberationContextServiceTest.java
需要新增测试文件或改其他路径先向主控报告，不擅自扩大。

## JYT-FLOW-WEB-20261008 — balanced_worker / gpt-6-luna medium
职责：SF02首页事实刷新、SF03提交后草稿、SF04完成态操作限制、SF05已证实重复正文；SF01自动进入/返回路径静态核对与回归，最终真实路径随BE恢复后测试。
worktree：/home/isp/wsps/cyf/.worktrees/jyt-flow-ui-20261008
owned paths：src/components/juyiting/、src/composables/juyiting/、src/components/world/JuyiHall.vue、tests/juyiting-*.test.js。修改仅限本任务必要文件，具体清单随交付报告。
不处理R01来源契约；不增加面板、API/鉴权/状态机语义。跨模块状态语义不清时停下该子项交接Sol，不猜测。

## JYT-FLOW-MIXED-20261008 — explorer / gpt-6-luna medium（只读）
职责：R01图文范围不明确的来源追踪；读取已发布git对象与424证据，列现有契约、可证实根因、最小修复文件及回归要求。不要将未重测流程判为坏或好。
无源码写权限，无台账写权限，无独立Reviewer职责。仅在 /var/tmp/cyf-jyt-flow-mixed-20261008/ 写本任务报告。主控收到后决定是否交现有Owner或另开第三个非重叠Writer。

## JYT-FLOW-VERIFY-20261008 — 主控
先准备验收矩阵和发布证据要求，不与子任务重复实现。合并需固定SHA与自检结果；正式前后端测试/构建走Flow5260799/4403172；未达验收不发布。选择版本→源码commit→同Run制品→部署→在线核验。
再独立后台浏览器登录测试账号：先只读核对429恢复，不重发原需求；新增唯一标识纯文本事项完整验收，补图文/返回/刷新回归。保存版本、时间、动作、脱敏网络与截图；失败与NOT_RUN分开。

## 公共执行规则
最多3源码Writer+1只读辅助，单Owner、独立worktree、不重叠路径；他人dirty代码/进程/证据不动。旧台账owner保留，冲突只告警协调不抢占。子任务不得push、部署、改生产数据、调用付费接口；本地不做生产构建，不直接Gradle。正式验证主控走Flow，不沿用技能旧版develop自动部署描述。无独立Reviewer，Owner自检优先。
