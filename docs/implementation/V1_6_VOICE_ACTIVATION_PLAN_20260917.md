# 1.6 语音真实验收推进（2026-09-17）

用户最新要求：继续既定OpenAI语音实现，达到可交付验证时通知。此任务独立于已经完成的1.6.0代码发布，不把源码/普通health成功当成语音可用。

## 当前事实与范围

- 已发布API `a8e9170873062165176626775d66c92dfc2e7a1a`，JAR SHA `82ef8e26fe7745a9a6a01d83560ddd2d7dd7846aea1425b2c0ac89ec4f2714fb`；Web `74420db2c82fb2f5dee673f337c13bb546d53f93`。release/1.6.0已冻结，不覆写。
- 14:07精确runtime为PID1759469/start_ticks3119227686；任何后续生命周期必须由指定Owner在锁内重新确认。
- 实际JAR的Spring AI公共连接为`https://codex.chcbz.net/v1`，key为ENC配置存在；这不是官方OpenAI直连。不能把此网关的密钥送到另一host，也不能把聊天模型支持推断成音频接口支持。
- STT固定`whisper-1`、TTS固定`gpt-4o-mini-tts`。`.voice-runtime.env`不存在，运行开关尚未启用；安全状态默认关闭。
- 不更换现有聊天模型/连接，不生产DML、不新增供应商/购买、不公开密钥、不绕身份隔离。不生成用户录音；最小联调只使用公开无敏感短句及其合成音频。

## 执行安排

唯一Owner/gate仍只在`docs/implementation/TASKS.yaml#runtime_ledger_json`。

1. `V1-6-VOICE-ACTIVATION-20260917`：API Owner复用现有同host连接，安全解析既有ENC，不输出明文。先非计费能力/权限预检；如可用，再经主控限定真实探针范围（单个短句TTS、同音频STT，结果不确定不自动重放）。不得将失败吞成PASS。
2. `V1-6-VOICE-USER-ACCEPTANCE-WEB-20260917`：Web Owner核对实际编译开关、入口、录音→预览→确认发送→播放、取消与错误提示。必要改动独立worktree，测试通过后合develop，新发布分支，不移动已有release。
3. 运行配置只由唯一API Owner执行：独立HMAC/缓存密钥、既有Provider连接继承、认证smoke；保存前值，根目录0600、不可把配置当shellsource。需要重启时精确runtime+发布互斥+可恢复安装；主控不直接操作进程。
4. 按配置启动成功、认证STT/TTS真实成功、接口身份负向、Web入口可操作、线上健康核验分别出证据。未全部达到不能通知“可验收”。浏览器麦克风权限及真实设备体验最后交用户确认。

## 交给用户时的最小验收

- HTTPS登录聚义厅，允许麦克风；看到语音入口且有明确AI生成语音提示。
- 录音一句短话，停止后显示可编辑转写；不经确认不发送。
- 确认发送到当前明确上下文；慢回复保持等待，可手动停止等待；停止等待不声称撤回已发文字。
- 开启朗读时播放本回合回复；身份/上下文切换、退出或取消不播放上一回合音频。
- 网络/Provider失败有清晰提示，文字聊天仍可用；不自动重复计费。

若既有网关不支持音频或缺少凭据，先交付明确的HTTP/模型/路由证据及单一用户动作，不让用户重新做技术选型，不持续盲重试。

## 前端核验结果（14:12）

实际已部署入口包内嵌`VITE_JUYITING_VOICE_ENABLED:false`，目前用户看不到语音入口。录音/STT预览/发送关联/可选TTS/取消和迟到隔离代码均已齐全，无需另写UI。用户在预览中也可自行选择自动发送模式；默认验收先用手动确认，不能概括成系统绝不允许自动发送。

下一步须先证明真实API语音能力，再对相同已验证Web source显式`VITE_JUYITING_VOICE_ENABLED=true`构建一个新不可变制品，记录构建环境差异，不覆盖1.6.0的flag=false制品或固定分支。前端Owner已释放，不占位等待。

核验证据：`/var/tmp/cyf-v1-6-voice-web-acceptance-20260917/frontend-acceptance-audit.md`。此为入口审计，不是新的生产构建或真机验收。

## 14:26 真实能力探针：外部前提缺失，尚不可交付

- 复用实际加密公共凭据对同host`GET /v1/models`成功200，共8个公开模型，无`whisper-1`和`gpt-4o-mini-tts`；目录缺失本身不等同接口失败，因此只据此不下结论。
- 主控依据用户继续真实联调指令，额外限定一次无敏感短句TTS以及仅成功后的一次STT；不买额度、不换host/模型、不自动重试。
- 实际`POST https://codex.chcbz.net/v1/audio/speech`返回 **404 text/plain**，18字节响应；这是一次真实请求，不是mock。TTS失败后严格停止，**STT未调用**，不宣称转写也已测失败。
- 当前没有证据证明现有网关支持音频。缺口在外部连接能力，不能通过开启API/Web开关解决，也不能把这个网关key发给官方host尝试。
- 本机nginx配置未找到该域vhost；没有更改远端网关、运行配置、API进程或Web上线包。无需重建当前flag=false制品，前端继续等待API真实成功。
- 需要外部前提：现有网关开通相应音频接口，或提供受授权的音频专用连接及凭据。若采用官方连接，仅配置Spring AI音频专用base-url/api-key，不修改现有聊天公共连接。密钥仅写服务器私密配置，绝不发聊天或提交Git。
- 取得可用连接后再继续真实应用认证联调、激活、Web新制品及用户设备验收。当前状态 **NOT_READY_FOR_USER_ACCEPTANCE**，不是交付完成。

证据目录：`/var/tmp/cyf-v1-6-voice-activation-20260917-api`，摘要文件`gateway-models-summary.json`与`provider-audio-probe-summary.json`；所有持久化报告仅含脱敏元数据，不含Provider key/Jasypt密码。
