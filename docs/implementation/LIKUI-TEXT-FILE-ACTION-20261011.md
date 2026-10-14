# 李逵：议事到文本文件执行最小接入

核对日期2026-10-11；Owner Main。API基线cf140272、Runtime基线5b902c1b。状态：源码与定向测试完成，API候选制品已生成；发布被实际磁盘空间阻塞，未上线、未业务验收。
工作区：`/home/isp/wsps/cyf-worktrees/likui-textfile-api-20261011`、`/home/isp/wsps/cyf-worktrees/likui-textfile-runtime-20261011`。

## 冻结范围
- 新版普通点将授权增加 `GENERATE_TEXT_FILE`；不是付费图片权限，不复制其他Agent密钥。
- 动作 `generate-text-file`/`EXECUTE`/`GENERATE_TEXT_FILE`，无输入（minSources=maxSources=0），输出仅 `text/plain`。
- 只在精确tenant/client/owner/agent的活动Runtime声明实际文本执行器ready时广告；并在创建时再次核对。
- 主聊天仍read-only。执行器在独立run目录内运行已授权Codex命令，生成真实 `outputs/result.txt`，严格UTF-8、非空、无NUL、无符号链接；实际字节经过现有上传/提交/成果投影，不从聊天答案冒充文件。
- 不支持本轮附件转换、DOCX/PDF生成、文件编辑、图片启用、通用任意仓写入，不增设新表/新HTTP入口/新网关路径。
- 原事项448的持久grant不含该操作，不回填、不以DELIBERATE替代文件授权；留原CLARIFY状态。新授权以新事项实测。

## 现有表与字段复用
- `agent_task_execution_grant.permitted_operations_json`：新点将写入GENERATE_TEXT_FILE；既有grant版本、任务指派epoch、固定需求版本仍校验。
- `agent_personal_workspace_execution`：execution_mode=CONVERSATION、permitted_operation=GENERATE_TEXT_FILE、output_content_mime_type=text/plain；复用task_grant_id/version、assignment_revision、instruction、idempotency_key/request_hash、租约和provider-start单次标记。命名以实体/mapper实际映射为准，不做DDL。
- 原input/output表无新字段；输出仍output_1、byte_length/content_hash/storage_uri及STAGED→COMMITTED。
- `chat_request`、`chat_interaction_step`、`chat_step_execution_link`、typed admission沿用动作父摘要派生的稳定request/step/intent；执行ID由OwnerScope+intent的SHA-256前60位加pwe_前缀稳定派生（64字符，适配原link字段），创建服务返回后严格对照；不变重放只读持久绑定，不重复创建。
- `chat_conversation_asset`及正式成果验收沿用已提交真实字节投影，不新增文本假成果。

## 编码切片与边界（每项目标≤30分钟，不承诺验证/发布等待时长）
1. Agent API定义只读NativeTextFileRuntimeLookup；Chat WS注册/移除精确会话声明，当前身份检查复用现有Runtime绑定。能力清单增加上述动作，null/旧Runtime不广告。
2. 原grant普通点将增加操作；原createConversation仅为该操作接受text/plain且无references，入场/每阶段复核使用该明确操作及paid=false；图片仍paid=true，绝不一并放宽。MIME白名单与UTF-8验证补齐。
3. Chat增加文本文件动作适配，从原父final+user+grant建立唯一执行、request/step/link/admission；原Executor分派，图片分支不改。所有写入沿用原事务/root锁/幂等摘要，重放不重复调用。
4. Runtime文本执行器、profile开关、ready声明及原native HTTP poll分发；单独run输出实文件，不开启图片，不把主聊天切成workspace-write。
5. 定向测试：身份跨scope/过期session/未声明不可用、旧grant拒绝、重复action不重建、文本编码/格式不匹配拒绝、图片原回归、native租约/上传/提交测试。
6. 固定新版本源码→后端本地正式测试/validateLayering/构建→原本地installer发布；Runtime原installer固定制品仅部署李逵（备份/互斥/读回），前端无必要不发布；新事项真实文件下载/内容/hash/正式验收。

## 真实完成条件
运行成功/模型答复不算完成。必须有实际公网Runtime命令、租约、字节上传、提交、UI成果、下载内容与SHA核对及单次正式验收。失败只报告具体断点，不自动重建事项或扩大功能。

## 2026-10-12 接续核对（候选，未上线）
- API候选 `4345f5e4c1cf86728c855ffc8f1b1efd70208568` / tree `5bb3e2c5306bdf24c11bad9cde4857a879fef265`。文本动作仅依赖普通执行开关，不依赖付费图片开关；普通点将新grant明确增加GENERATE_TEXT_FILE，旧grant拒绝。
- 232项实际测试、validateLayering、fresh bootJar已通过；该批控制器误列一个不存在的额外selector，被打包前完整性核对拦截，证据未当成可发布制品。已以真实ChatActionContinuationTest改正并固定新批，继续正式测试/打包。
- 当前正式批 `/var/tmp/cyf-likui-textfile-api-release-20261012-stwh_2e6`，构建输出在同名 `/dev/shm/` 目录；旧批真实报告持久备份 `/tmp/cyf-likui-textfile-api-release-20261012-unsfd4n4/durable-test-evidence`。不得把内存目录制品当作持久发布完成。
- 当前线上API仍1.14.7/cf140272、李逵Runtime仍1.0.2。候选计划API1.14.8、Runtime1.0.3，未写生产配置、未重启或新建事项。
- 发布配置必需：原API `agent.personal-workspace-execution.allowed-mime-types[6]=text/plain`；仅李逵profile设置 `nativeConversationTextFileEnabled=true`，保留native HTTP poll=true，图片开关false。必须在原发布备份/互斥/配置指纹边界内写入，不能仅源码通过就宣称enabled。
- 原native通道当前下载文件名是 `output.txt`，本轮新事项明确按该名称验收，不宣称支持用户任意指定文件名。
- 新实测验收顺序：新无附件非资金事项→点将李逵→广告generate-text-file且新grant有明确操作→单次START→真实文件上传/commit→Chat成果投影→正常下载内容/hash→单次确认验收。448不补授权、不复测446。
- 磁盘容量是发布前实际阻塞：00:17本机可用约409MiB，现有admission+incoming+candidate+rollback所需约1.2GB（按既有真实制品大小估算，仍需本批准确核算）；不删除其他聊天文件/制品，不绕过原installer空间与备份检查。

### 最终候选与证据（2026-10-12 00:27 +08）
- API `4345f5e4c1` 已ff合入并push develop；真实选择器修正后 **242 tests / 0 failures / 0 errors / 0 skipped**、validateLayering、PublicArtifactVerifier、POI运行类路径与fresh bootJar均通过。无需因空间问题重跑同输入构建。
- API1.14.8原producer已成功：JAR SHA `9a76c4276f44d7f8148f72dc17930df602116fbc41a8940454593fb2d8d7c246`；包SHA `0eed546197ec0965f9c56c699fc36920a74af1aff9615b456c11d7e56a0c696f`，226673346字节，位于本批package目录。34个原始证据快照已由Main按原controller保存在root-protected proofs/authority目录；这是制品准入准备，不是生产安装授权/回执。
- Runtime候选 `807b86d66153b765529bba1d547e4bcfbf0a3706` / tree `959c72f2f9578186da9819ded6fd6798e3e0bb1a`，版本1.0.3。文本/native 24项、profile/hosting 16项均通过；Main另外在固定提交选择2项实际payload闭包测试通过（其余78项未选择，不能计作全套通过）。现有依赖临时软链仅用于本机诊断、已移除，不当作正式installer证据。
- 更新后的实际容量见本批 `release-capacity-blocker.json`：包已持久保存后剩余204877824字节；原admission+incoming+candidate+rollback估算仍需1215942260字节，缺约1011064436字节。未执行必然失败的admission/安装，未删除旧制品/他人证据。
- 线上JAR仍SHA333d525e…b8c57；没有本轮生产API/Runtime配置写入或重启。下一步只需在获准清理/可用空间补足后，接续原制品准入与发布、精确配置更新、李逵Runtime原installer1.0.3部署，然后按前述新事项验收；不能将待验收标为已跑通。
