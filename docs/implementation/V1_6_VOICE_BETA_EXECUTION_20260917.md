# 1.6.0 聚义厅语音会话 Beta：实施与验收计划

更新时间：2026-09-17。用户已要求启动下一版本；已外派的 Persona Catalog / 任务 378 问题不在本包重复修复。本文件是范围与证据索引，不是第二份 Owner 台账。

## 最新发布授权与进度（2026-09-17 12:51）

用户已明确云效不可用期间改为本地验证/构建/部署，先合组件develop、再从已验证SHA冻结release分支；下文早期“等待Flow、不含API重启”已被本次可恢复发布授权替代，Provider/付费/生产DML边界仍保留。

API215项相关测试、Web2186项全量测试通过（另2既有pending）；双生产构建通过，远端`release/1.6.0`已固定API `a8e91708`、Web `74420db`。制品、dry-run、本地实际部署及线上健康readback均通过，**代码发布已完成**。当前事实及后续发布结果以`docs/implementation/V1_6_LOCAL_RELEASE_PLAN_20260917.md`和唯一runtime ledger为准，不声称真实语音Beta已激活。

## 1. 基线与结论边界

- 路线图依据：`docs/implementation/VERSION_PLAN_20260915.md`，下一列车为 1.6.0 语音 Beta；不采用已被替代的 2026-09-14 编号。
- 本轮已 fetch：API develop `e4b2bb346e4cc6617ef34ddc2aa25c6bd92218f2`；Web develop `08f2cfc2927c90010c7ec0d15bd46606340ca2a5`。这是源码基线，不是新发布证明。
- 既有回归为 20/22：悬赏搜索与统计回填后恢复；Persona Catalog 和任务 378 不通过。额外的 378 deliverables 返回 404。不能仅凭空的 open 列表和 TASK_NOT_FOUND 断言任务真实归属；任务归属、存在性及迁移映射由外派修复 Owner 核实。
- 已过回归覆盖登录、阅读相关只读接口及聚义厅入口/地图/成员；不代表语音、完整交互、下载、多身份负向、资金或全部 1.5 协作流程已验收。
- 不修改主 Web 脏工作区，不重复开发既有语音基础设施，不触碰 isp-install。

## 2. 本轮交付范围

1. 保留已有录音 → STT → 转写预览/编辑 → 当前上下文确认 → 消息发送 → 可选 TTS 的流程。
2. 修复已发现的可用性缺口：`useHallVoiceConversation.js` 在发送后 120 秒递增 generation 并关闭 reply correlation，导致仅因慢回复丢弃后续语音响应。移除这个任意总耗时终止，不换成更大的阈值。
3. 在 sending、waiting_reply 两阶段保留可到达的“停止等待”。停止语音等待不宣称撤回已发文字，也不自动重发。
4. 保留身份/上下文切换、卸载、方向切换、用户取消的异步隔离与音频资源释放；保留实际网络错误和已配置传输超时。
5. 整理已有 HTTP 契约和离线/真实验收矩阵。录音内容大小/时长限制不是请求性能 SLO；本轮不擅改既有音频协议。

不包含：生产 Provider 调用或额度授权、默认全量启用、钱包/扣费、新增 allowlist 绕过、生产 DML、API 重启。文档里的 allowlist 目标不能冒充已实现身份准入；当前 API 配置中的 compatibilityGatewayAllowlist 是网关地址名单，不是用户名单。

## 3. 现有 HTTP 契约（依据当前 API 源码）

根目录：`api/chat/jia-chat-service/src/main/java/cn/jia/chat/voice/`。

| 接口 | 请求 | 成功响应 | 身份/副作用 |
| --- | --- | --- | --- |
| POST `/chat/speech/transcriptions` | multipart：`audio` 单文件；`requestId` 必须；`language`、`durationMs` 可选。未知/重复字段拒绝 | HTTP 200，JsonResult `code=E0/status=200/data={requestId,text,detectedLanguage,durationMs}` | JWT 精确 jiacn/client_id/sub；服务启用时可能发生付费 STT，非只读探针 |
| POST `/chat/speech/synthesis` | JSON `{requestId,text,voice,format}`；未知字段拒绝；text 非空且最多 2000 Unicode code points；voice 来自配置，format=mp3 | HTTP 200，`audio/mpeg` 二进制、Cache-Control=no-store、X-Voice-Request-Id、Content-Length；不是 JSON 包 | 同上；服务启用时可能发生付费 TTS |

- requestId：`[A-Za-z0-9][A-Za-z0-9._:-]{15,127}`；不能通过更换 ID 盲目重复不确定结果的 Provider 调用。
- STT `durationMs` 是可选客户端声明，不代替服务端音频验证；language 默认为当前配置语言。
- 身份取自 JWT，不从请求提交的用户/租户字段信任；用户身份与 client 的隔离不能被 Beta 范围控制替代。
- 幂等由既有 VoiceRequestCoordinator 管理：operation + identity scope + requestId 及请求摘要；相同已完成请求回放，冲突或未知不假报成功。
- 错误使用真实 HTTP 状态和 JsonResult：400 INVALID_REQUEST；401 UNAUTHORIZED；409 IN_PROGRESS / IDEMPOTENCY_CONFLICT / RESULT_UNKNOWN；413 TOO_LARGE；415 UNSUPPORTED_MEDIA；422 INVALID_AUDIO / NO_SPEECH / TOO_LONG；429 RATE_LIMITED；502 PROVIDER_ERROR；503 DISABLED / UNAVAILABLE；504 PROVIDER_TIMEOUT。业务 code 均带 `VOICE_` 前缀，data 可含 requestId；安全层拒绝可能早于 Controller。
- Controller/DTO：`api/SpeechTranscriptionController.java`、`api/SpeechSynthesisController.java`、`api/VoiceSynthesisRequest.java`、`api/VoiceTranscriptionResponse.java`、`api/VoiceExceptionHandler.java`；身份校验：`validation/VoiceIdentityResolver.java`。
- 开关基线：VoiceSpeechProperties 总开关和 STT/TTS 子开关默认 false，provider 默认 disabled。源码默认值不等于线上运行值；本轮不修改运行配置或读取密钥。

## 4. 执行包与顺序

| 包 | 当前安排 | 完成条件 |
| --- | --- | --- |
| V16-W1 语音等待可用性 | 独立 Web worktree；动态任务 ID `V1-6-VOICE-WEB-AVAILABILITY-20260917` | 确定性慢回复/取消/迟到回调测试通过；提交精确 SHA/tree |
| V16-D1 合同与验收收口 | 主任务在根仓维护本文件及语音 SDD 补充 | 路径、HTTP 形状、权限、错误、上线边界有源码依据 |
| V16-I1 集成与正式验证 | W1 自检后非覆盖式集成最新 develop；不新建 Reviewer | 云端相关语音/聊天测试、构建，同 Run 制品与实际线上核验；若 Flow 额度仍未恢复，记录待验证，不自动沿用旧本地发布特批 |
| V16-A1 受控激活 | 等实际 Provider、身份范围、额度、样本及必要授权明确 | 真 STT/TTS、跨身份缓存隔离、取消、设备麦克风/播放、会话回写实测；此前只称源码就绪，不称 Beta 上线 |

开发/合同整理并行，真实启用最后进行。后台 develop 发布遵循现有定时规则；不把用户“开始开发”推导为生产开关或付费授权。

## 5. 最小验收矩阵

- [ ] 慢发送在原 120s 边界之后依旧等待；接受/拒绝均正确处理，不误标成功。
- [ ] 等待回复超过原 120s 后仍能处理本回合的精确回复，最多一次 TTS。
- [ ] sending / waiting_reply 均可手动停止等待；迟到响应不能污染下一回合。
- [ ] 身份/上下文变化、卸载与方向切换保持隔离；录音 tracks、定时器、音频 URL 被释放。
- [ ] 转写失败保留文字通道；显式网络失败/传输超时有清楚错误，不自动重复付费。
- [ ] API/Web 正式测试与同 Run 制品核验。小范围本地单测仅为开发自检。
- [ ] 真实麦克风和 TTS 设备体验、授权 Provider 成本/审计与 STT/TTS readback。

## 6. 首轮状态

2026-09-17：已确认新版本范围、创建独立 worktree 并通过 orchestrator claim 实施包。实现结果、测试数量、候选 commit 以完成后的实测补记；当前不声明新版本开发完成、合入或发布。

### 首个实现包结果（2026-09-17）

- 独立分支 `codex/v1-6-voice-availability-20260917` 已形成两个提交 `70ae6e1be2899e26b42da4a61a2d9db588267cd4`、`d46fc56b62844cb3280fe6276ce13f03685d9660`；最终 tree `0ea795a71e9841f5a5bf659d17e7ece3e2059336`。主任务已核对变更范围、clean 工作区及 diff --check。
- 去掉等待回复 120 秒自动结束；发送中/等待回复中均提供停止等待，不撤回文字。确定性时钟分别跨过 120001ms 验证慢发送、慢回复、一次 TTS 与取消后隔离。
- Owner 本地定向回归 **24 passing / 0 failing**：`node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --reporter spec tests/juyiting-voice-conversation.test.js`。复用既有 node_modules，只读依赖，不安装新依赖。
- 首次运行因本 worktree 无依赖失败；发现可复用依赖后首次真实运行暴露旧测试要求停止语音同时取消文字，已按“停止语音等待不撤回文字”的目标语义修正并复验。不能将首次失败写成通过。
- 这是已提交的本地候选与自检，不是云端正式验证或发布。未推送/合入 develop、未启用生产语音、未调用 Provider、未操作 API 进程。下一步由主任务收口版本集成和正式验证，不等待独立 Reviewer。

### 最新候选与上线安排（2026-09-17 09:25 CST）

用户最新要求为**先完成、验证达到上线条件再合入组件 develop，后续统一安排上线**。本节覆盖此前“合入即部署”执行语义；本轮不发布、不启用生产语音、不调用付费 Provider。

| 组件 | 已推送候选 / tree | 实现与自检 | 正式状态 |
| --- | --- | --- | --- |
| Web | `c5fe7484b455843f6e9beeb49573fcc54e729043` / `28bc296d73e183459cb6ba4d37bc8d1c31bf1638` | 3 文件；慢发送/慢回复、停止等待、取消 TTS/播放、旧回调隔离及清晰按钮文案；25 项定向自检 PASS | 尚未合入 develop，云端验证待执行 |
| API | `ab7ba3f610edb4bf9ec91f8124ee1cc254dfc821` / `472fab9c370e4e249a861c41f7e85fdfef72ec3c` | voice 范围 9 文件；TTS reservation 隔离、尊重显式传输超时、匹配 Redis 租约；静态检查 PASS | 新增回归尚未执行；尚未合入 develop |

API base 为 `5ebe423be8bbdb9cc94b9419e568818128563cad`，保留其他 Owner 的 Persona Catalog 改动；不重复修复。Web base 仍为 `08f2cfc2927c90010c7ec0d15bd46606340ca2a5`。

前端证据：`/var/tmp/v1-6-voice-availability-20260917-ui-clarity-focused-test.log`，SHA-256 `75c51752a996f70f62746bbb1faeb1ef9a09e7d98fae758cbb6a8e37d1bc816b`。本地通过不冒充 Flow 或设备验收。

两个现有 Flow 已去除 deploy，仅保留云端测试/构建/制品；配置前值及 readback 见 `docs/aliyun-flow-release-hold-20260917.md`。Web Start API 一次请求返回异常 code=-1，无 Run ID，分页只读复核暂未出现新 Run，不能重复启动或编造结果。API 因并发配置变化在发送 Start 前停止；其他任务 Run84 的源码分支为 `bugfix/agent-catalog-roster-20260917`，不是本候选验证。当前核查启动参数并协调配置，不根据历史失败推断当前额度根因。

软件候选达到上线条件需精确 SHA 的 Flow 测试/构建成功与制品绑定；真实麦克风/Provider/设备验收和生产激活仍在单独安排的上线阶段，不作为已完成结果。

### 09:36 最终云端回执（覆盖上文“未启动”状态）

- 已确认并修复 Start 分支过滤问题：API 返回 HTTP400，精确原因是 `branchesFilter=^develop$` 不允许候选。仅放宽为 develop 或各自唯一候选分支，默认 source branch 保持 develop，仍无 deploy。
- API `5260799 / Run85`、Web `4403172 / Run116` 已创建，source branch 分别匹配已推送的语音候选；两者均在数秒内 FAIL，日志为空（more=false），未返回 checkout commit、测试报告或制品。**不能宣称精确 SHA 验证通过，也不能据此判断单测失败或确认额度不足。**
- 当前候选依然未合入 develop；生产未改变。没有盲目 Retry、没有本地 Gradle/Vite 重型验证替代、没有付费 Provider 调用。
- 下一步：从云效运行详情/管理员取得执行启动失败的确切原因并修复；有实际补救后才重试精确候选测试/构建，成功后合入 develop，继续保持部署暂停。
- 可复核证据：`docs/implementation/handoffs/V1-6-VOICE-CLOUD-VERIFICATION-20260917.json`；唯一运行台账保持未完成。
