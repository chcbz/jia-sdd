# 聚义厅 Realtime 语音启用与设备验收（2026-09-30）

## 授权及范围

用户已确认“启动吧，我具体怎么验收？”。本次启用沿用临时本地测试、构建、发布授权；保留身份隔离、运行归属、发布互斥等待、可恢复安装与实际健康核验。语音 Provider 验收预算最多两次、不自动重试、不购买或充值；两次全部保留给用户真实浏览器的一次转写与一次回复朗读。主 Agent 与实施 Owner 不先发付费 smoke。

本次不重建已发布 API，不更改其业务 SHA；配置及 launcher 变更单独绑定摘要。前端从最新远端 develop 隔离制作 enabled build，保留其他已合入变更，非覆盖推进 develop 并冻结新的 release 分支。旧 `release/1.13.45-voice-realtime-20260930` 不变。

## 当前状态

**最新结论（2026-10-01）：用户验收失败；Redis4 修复候选尚未成功上线，随后两次真实服务自验语义闭环也失败。不能宣称功能已完成。** 先前启用与健康证据仅代表当时配置状态。 首次失败及第二次成功分别留存，不将默认关闭的 1.13.45 发布或已有网关能力证明写成设备验收成功。配置候选及启用证据只写在本聊天私有 `/var/tmp/cyf-voice-implementation-20260930/activation/`；凭据不写进本文、聊天或 Web。

## 用户验收操作（生产启用成功后执行）

1. 使用电脑浏览器登录聚义厅 HTTPS 页面，刷新到已启用版本；选定自己可操作且在线的 Agent，进入私聊，清空输入框，保持此 Agent/会话不变。
2. 不勾选“自动发送”，勾选“语音回答”（播放内容为 AI 生成语音）。
3. 点击“语音”，允许麦克风，说：“你好，请只回复：语音验收成功。”点击“停止并转写”。此次转写计一次语音 Provider 调用。
4. 核对“语音转写”内容；若正确，点击新增加的“确认发送”。若不正确，先停止本轮并反馈，不重复录音/自动重试。追加/替换是普通文字编辑路径，不代表语音回合关联朗读验收。
5. 等待选定 Agent 在同一会话给出回复，确认随后自动播放此回复。回复合成计第二次语音 Provider 调用。不能要求不存在的“手动朗读”按钮。

通过条件：真实麦克风录音、转写语义正确、文字未提前发送、明确 Agent/会话收到并回复、真实扬声器播放与文字回复相符。服务器健康和 oscillator/worklet 测试不代替这五项。

失败反馈只需：浏览器/设备、发生步骤、页面错误、发生时间；如有 Network 证据，提供 `/chat/speech/transcriptions` 或 `/chat/speech/synthesis` 的状态码与 requestId。不要提供 Authorization/JWT、API Key、原始含凭据 HAR。失败先归因，未经新的范围确认不超过两次验收调用。

## 结果

实际启用结果见下方第二次结果及不可变 outcome。设备端到端验收须由用户实际反馈，当前 pending。

## 启用候选与自检

- API 复用已发布 `fb79b180b6c6e5432c69c73b870954498d98a7a6` / tree `c78a0ce31614268056dd28418956534f2fc73a6c`、JAR SHA-256 `739154e07faa28dbc2f7042f8597f39f8ecb225ce680f5682fb41d163ab3e247`，不重建。
- Web `33a73aa043985739c59f865fafd18ad2b92f0038` / tree `7ec42016ecd336326f975e64c8f60b8a590c5a27` 已非 force 推送 develop，并冻结 `release/1.13.46-voice-realtime-activation-20260930`；新增确认发送并 enabled build，84 项相关测试 PASS、生产构建 PASS。外部 release ID 为 `v1.13.46-voice-realtime-activation-local-20260930`，不是 package.json 的版本号（仍为 1.0.1）。Web archive SHA-256 `b6046bd5ec3e1a8472d4b1965f6cb65fd624becdbceed7c055cf6ebce4b01237`；dist tree `c7e20eccc4162548fd19103200ba123d5704f3d792eb4ca8effa593f9f203234`。
- 最终 runtime env SHA-256 `acde055e7b997c3ec5f2c43b3b130b3778e886b032c645d079f0af188626e09f`，root:root 0600/single-link。只覆盖 audio-specific gateway/key，复用 live JAR 既有生产凭据；不改变 common Spring/文字 Agent 的凭据。独立 HMAC/AES key、provider/model/format/voice、allowlist 及精确 launcher 候选离线解析均 PASS。首次候选用 Codex Agent 凭据/common override，Owner 自检后改为精确生产来源；未安装首次候选。
- 实施入口自检修正真实缺陷：canonical launcher 路径、GO parse 错误传播、原子安装与失败恢复、发布/生命周期锁顺序、status 继承 FD8 避免自锁。最终入口 SHA-256 `4e5c30d18c5eb35a6cc6479d1ec1685a05ce3feb804d2549a109e6afea3d7930`，未使用脏 root launcher 整体替换生产。
- 主 Owner 已给冻结 exact-target GO（`runtime-main-activation-go.json`，SHA-256 `79ffbca47b4716b788b34710c2a4aacfd365945e3e6447129581f85aed4909c5`）：固定当前 canonical PID/ticks/argv/JAR、旧 Web tree、配置/launcher/产物/入口摘要；runtime Owner `01a0f102-cd90-7270-9677-e7c47198a8f6` 锁内核验后执行。此 GO 不是实际成功结果；成功必须看后续 outcome。

## 第一次启用失败及整改（真实记录）

首次 exact-GO 安装后，canonical launcher 在停止旧进程前验证配置时报 `authenticated smoke credential is missing`，Web 尚未切换。Owner 自动恢复旧 launcher 与原来不存在的 voice env 并重启核验健康 UP；JAR、Web tree 未改，Provider 调用仍为 0。不可变失败 outcome：`deliverables/releases/v1.13.46-voice-realtime-activation-local-20260930/activation/activation-outcome.json`（SHA-256 `8db2f214ea91c8092ad50db4c96cc70437616ee067ea942909cbce8cf8ea61e7`）。不能将本次写为启用成功。

根因：launcher 历史解析器把仅用于外部 authenticated smoke、从不传给 Java 的令牌强制为启动必填，配置准备 Owner 的离线 PASS 用了 fixture sentinel，未验证实际无 JWT 候选。整改是令 smoke token 可选并验证真实候选原字节；不是填假令牌、获取用户登录凭据或修改 HTTP 鉴权。新增测试绑定此次真实失败与最小检查范围，保留身份 HMAC、AES cache、provider allowlist 及真正 JWT 身份检查。改变 launcher 候选并重新绑定实际恢复后的 runtime 后才允许第二次尝试；不重用旧 GO、不覆盖失败 outcome。

## 第二次启用实际成功（最终运行结果）

- 2026-09-30 北京时间约 17:47，R2 changed-candidate activation PASS；只将测试用 smoke token 改为可选且绝不传给 Java，不改产品 HTTP JWT 身份/ACL。14 项 parser 测试及实际无 JWT 配置原字节解析 PASS。安装 launcher SHA-256 `94de2c8af2745d25a9cec82276d54e52c85a63ae7349f4204b36ba5f5f5b930f`；production env SHA-256 仍 `acde055e7b997c3ec5f2c43b3b130b3778e886b032c645d079f0af188626e09f`。
- 正常启动 PID `1962484` / ticks `3233411549`、JAR 不变，实际健康 UP；主 Owner 另从受保护的运行环境逐项确认 16 项配置与安装候选一致，只记录结果、不输出秘密。实际冷启动约 57 秒，不以性能目标拒绝后续步骤。
- API 健康后 enabled Web 原子切换 PASS，live tree `c7e20ecc…f203234` 与制品一致；公网 index/引用 JS 已逐字节摘要核验。备份路径绑定不可变结果，未覆盖原冻结 release 或第一轮失败证据。
- 无付费探针的浏览器形态公网检查：两个 `/chat/speech/*` 路由 OPTIONS 200 且允许 kit Origin/Authorization/Content-Type；无 JWT 的 POST 401，鉴权保留，未进入 Provider。默认 curl UA 公网 API 403 为既有 nginx UA 拦截（浏览器 UA 正常），未修改 nginx/ACL，不能将其误归因为本次 speech/CORS 回归。
- 不可变最终结果：`deliverables/releases/v1.13.46-voice-realtime-activation-local-20260930/activation/activation-outcome-r2.json`；额外公网证据 `activation-public-api-readback-r2.json`、主 Owner 独立核验 `main-live-verification-r2.json`，均附 SHA-256。`build_origin=local_user_authorized`，Flow Run=null；未宣称云效成功，未重建 API、做生产 DB 操作、购买/充值或发 Provider smoke。

**结论：ACTIVATED_DEVICE_ACCEPTANCE_PENDING。自动验收 Provider 调用 0，用户一次真实转写 + 一次关联回复朗读所需两次预算仍完整保留。** 页面步骤如上；完成真实设备反馈后才能记录端到端验收通过。

## 用户真实验收失败（2026-09-30 晚间，当前结论）

用户反馈点击“停止并转写”提示“语音服务暂不可用”，**真实端到端验收未通过**。Production log 可见已认证 `POST /chat/speech/transcriptions` 返回 `VOICE_UNAVAILABLE / 503`，不是旧 audio endpoint 404。当前 JAR 仍是冻结739154…，16项 voice env与配置匹配，健康检查UP不能代替接口可用性。

只读 INFO 确认线上 Redis 4.0.6；用相同线上 binary 在私有隔离实例已复现：语音 Lua 的 TIME 后写入被拒绝（non-deterministic write）。候选 `b2986836` 仅在四个读服务器时间并写入的脚本首行添加 `redis.replicate_commands()`；补丁后隔离 Lua 的准入、请求预留与续租成功，Java Redis4/Redis7 及完整 voice 回归已通过（107 tests，0 failure/error/skip），同 tree 生产构建成功，`b2986836` 已合入远端 develop 并冻结新的 API release 分支；发布尚未完成。保持服务器时钟、锁归属、幂等及身份隔离；不访问生产数据、不追加Provider探针、不要求用户连续重试。晚间错误与安全证据保存在本聊天私有 `transcription-failure-20260930/`。计费/剩余额度未经网关回执不能凭503断言；本轮自动Provider调用仍为0。

## Redis4 修复候选及发布失败（运行证据 2026-10-01）

- 源码 `b298683605c5549ee6c76836166baa1f4887a0b1` / tree `67913fd89feca1b370d095c7b6d32e7a8ef84015` 已非覆盖推送 develop，冻结 API `release/1.13.46-voice-stt-redis4-20260930`。四个 Lua 兼容性补丁保持服务器时钟、原子准入、锁归属和幂等。完整 voice 107/107 PASS、0 failure/error/skip（含真实 Redis4/Redis7），同 tree bootJar PASS；不是 API 全模块全量测试或真实设备验收。
- 候选 JAR SHA-256 `040996afc1a09980cc21c8d390e38235eab53513f19c2637645b73cb8a0a7c99`，252194299 bytes；`build_origin=local_user_authorized`、Flow Run=null。本轮主 Owner 已独立核对 XML、源码/制品绑定及远端 release/develop。
- R1 在变更线上 JAR 前拒绝既有 `/opt/cyf/service/api/backups` 符号链接；不是目录暂时消失。R2B 改为受保护 API 目录下的任务专用物理备份目录，保留旧入口、失败回执及原有链接/目标；目录检查不错误套用文件 nlink=1。
- R2B 发布失败：内核 global OOM 于 00:57:27 杀掉新候选 Java `2150705`，又于 00:59:21 杀掉恢复 Java `2152596`。原生 entry exit=70、不可变回执 `RECOVERY_FAILED`；不能标“新版本已上线”或将其改写为慢启动/SLO 拒绝。
- 随后独立 healthmon 恢复的是旧 JAR `739154…3e247`：主 Owner 01:03:52 只读观察 PID `2155473` / ticks `3236020880`、HTTP200/status.code=UP。这是后续旧服务可用性，不是 R2B 成功，也不证明稳定或语音已修复。未操作其他任务进程/monitor，未追加 Provider 调用、生产 Redis 数据修改或 Web 切换。
- 当前结论 **FIX_TESTED_NOT_DEPLOYED_HOST_OOM**；真实验收仍未通过。唯一 ledger 已记录 `blocked_runtime_oom`。须先协调实际资源 Owner，在适当授权范围内释放资源，再核对新健康代际和 exact GO；不盲目重复部署，也不要求用户继续录音。证据：本聊天私有 `transcription-failure-20260930/main-final-deploy-attribution.json`、`main-deploy-oom-evidence.log` 和 runtime recovery 回执。


## 用户新增有限调用授权后的主 Owner 自验（2026-10-01，最新）

- 用户要求“修改完你自己先验证，允许有限的语音服务调用”。本轮重新限定最多两次、TTS/STT 各一次，无自动重试；不同于此前留给用户的设备验收预算。本轮已实际尝试两次，余额归零，不新增调用、不充值。
- 不启动完整生产应用、不伪造 JWT：从 SHA-256 `040996af…c99` 的冻结候选 JAR 提取原始依赖，最小 Java harness 调用真实 `SpeechSynthesisService` / `SpeechTranscriptionService` 及 Realtime Provider；使用任务自有 loopback Redis4.0.6、独立随机 HMAC/AES 和隔离测试身份，不读写生产 Redis/数据库。私有证据 `transcription-failure-20260930/main-real-service-selftest-20261001/`。
- 离线预检首轮因 harness 缓存 fixture 错用 MIME `offline` 失败（Provider 0 次），修正为服务合同 `application/json` 后准入/预留/续租/终态/释放 PASS；保留两轮证据，不将此误写成候选代码失败。
- 真实 TTS 将“语音验收成功。”生成 WAV（24kHz、单声道、16bit、7.05 秒、338444 bytes、非静音；SHA-256 `5cb9250a2406982ea85241005f603ae90a7f8d96d7323a0b77d127e319a112ee`）；STT 随后输入该自产 WAV。两次调用返回且两个服务的加密缓存回放 PASS、没有额外 Provider 调用。
- **语义闭环 FAIL**：STT 结果为“好的，我明白了。接下来您需要我帮您进行什么样的协助呢？”，与固定期望文本不符。仅据该回合不能分辨 TTS 念错文本还是 STT 作了对话回复；未捕获 TTS transcript，不能单独宣称任一操作语义通过。Redis4 回归通过、网络返回结果和非静音都不能替代正确内容。
- 不追加付费重试、不再部署此候选；宿主 global OOM 发布阻塞仍保留，生产 JWT/浏览器麦克风/扬声器链路均未验证。下一步先离线核查操作/响应语义与最小诊断证据，修正后再获取新有限预算复验；不要求用户重新录音作为首次实验。唯一 ledger 当前 `blocked_voice_semantics_and_runtime_oom`；失败证据已经 orchestrator 登记，不覆盖107项通过、此前OOM或用户失败记录。

- 主 Owner 最终只读核验（2026-10-01 01:29:48）：canonical PID `2161724` / ticks `3236110861`、HTTP200/UP、live JAR 仍 `739154…3e247`。代际变化只作观察，未据此推断新 OOM或稳定恢复；不是修复已上线。证据 `main-real-service-selftest-20261001/production-readonly-final.json`。
