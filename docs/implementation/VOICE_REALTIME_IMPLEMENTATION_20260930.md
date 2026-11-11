# 聚义厅 Realtime 语音实施（2026-09-30）

用户要求落实已升级 CLIProxyAPI 的真实语音能力。独立能力证明见 `VOICE_REALTIME_VERIFICATION_20260930.md`；本文件为合同/结果索引，不是第二台账。当前 Owner/gate 只在 TASKS.yaml runtime ledger。

## 合同与授权

- 新 SDD：`specs/juyiting-voice-realtime/`。保留当前 Agent 的录音→转写确认→文字传令→关联回复朗读，不以通用语音模型替换选定 Agent。
- 现有 CYF authenticated speech HTTP API 保留，后端上游换成 Realtime。密钥只在服务器，录音/回复改为 PCM16 mono24k WAV；后端保留身份、Redis 准入、加密幂等缓存和锁归属。
- 开发隔离 worktree 基线：API `e15e1a9d947e86e5f81a3288948087466a8a879c`，Web `9854173f7f409ca2f1c862eb153b0e3574ee58ff`。不修改 api/web 脏主 checkout。
- 沿用用户临时本地验证/构建/发布授权，Gradle 经 orchestrator 全局串行；没有新的 Flow 成功声明，没有新增付费 Provider 测试或生产数据操作。生产语音开关仍未启用；此前一次付费测试授权不扩张成默认全量额度授权。

## 已形成的证据（执行中）

- Web 首个候选 `2d4f7e64c2aa5b8326de5548a5dbd8ce03a4d1f2` / tree `32d0b33e784a2edbd5e8b733f8c4cd2e8c60f5bc`，29项定向 PASS。Owner集成自检发现96kHz/127样本分块实际重采样错位、初始化取消/旧blob验证回调清理缺口；后续修订单独测试，不能沿用29项代表新tree。
- Host launcher source原只接受 legacy provider/model。为新profile补最小枚举与WAV格式配置，不修改任何已安装运行入口；13个隔离配置解析用例 PASS。首次测试提取了无关诊断heredoc，3失败；定位后按 VOICE_ENV_ENCODED 锚定，输入实质变更后13/13通过，失败不写成PASS。
- API实现/最终集成验证、制品与发布结果待完成；禁止根据当前部分证据称页面语音已上线。

## 证据位置

本次临时构建/验证证据只用 `/var/tmp/cyf-voice-implementation-20260930/`；网关既有能力证据用本聊天自己创建的 `docs/implementation/evidence/voice-realtime-20260930/`。不读取、修改其他任务的私有证据或控制其进程。

## Web最终源码就绪

最终 Web `8902c5aa0482fdd5e22d697ec2933c2ecae486d7` / tree `32eb9cf7bf449f86c569c9b3e5f271b49eab9887` 已非force推送并读回 origin/develop。36项voice/PCM测试、47项周边Hall会话测试PASS；Vite生产构建28.14s成功。实际本聊天自有Chromium加载构建产物内的worklet，96kHz本地oscillator生成24kHz/mono PCM WAV，12000 samples、24044 bytes、非静音，模块加载/容器验证通过，无Provider请求；不冒充真实麦克风/扬声器验收。生产flags仍false，API/联合制品与发布未完成。

## 最终源码、验证与冻结（16:18）

- API `fb79b180b6c6e5432c69c73b870954498d98a7a6` / tree `c78a0ce31614268056dd28418956534f2fc73a6c`；Web `8902c5aa0482fdd5e22d697ec2933c2ecae486d7` / tree `32eb9cf7bf449f86c569c9b3e5f271b49eab9887`。两个 develop 已非 force 推送并读回；两个新 `release/1.13.45-voice-realtime-20260930` 从已测 SHA 冻结并远端读回，无覆盖旧 release。
- API voice slice **105/105 PASS，0 failure/error/skip**；涵盖离线 Realtime、GA 结束事件、异步 send、握手取消、WAV、lease、身份、缓存及 HTTP 合同。不是整个 API 全量。bootJar 最终 PASS，所有 Gradle 经 orchestrator 串行。
- Web 补做独立 `npm ci`，不再复用共享依赖；83项定向 PASS、生产构建 PASS。364个产物与此前浏览器 worklet smoke 所用产物逐文件完全一致，无需重复相同 browser 验证。
- 真实失败记录保留：两个 Mockito wildcard 编译错误及一个旧 overload mock 已最小修正；kernel OOM 杀死本任务 Gradle daemon 后改 SerialGC/两处理器低 native 占用，测试成功；全量 build 的160m堆 MapStruct OOM改为256m build-only JVM后成功。未删/改业务源绕过失败，未抢占或终止 foreign 进程，期间线上 health UP。控制面参数/gate 错误已分别归因，不能写成测试失败或 Flow 成功。
- 制品目录：`deliverables/releases/v1.13.45-voice-realtime-local-20260930/`。API SHA-256 `739154e07faa28dbc2f7042f8597f39f8ecb225ce680f5682fb41d163ab3e247`；Web archive `3695fe9d03634041775ac7a6050b89993861b969f73c63d3b9d18a01436070e8`，dist tree `9b3dc688677014ed46ade66b314015c774f2cc972319258f9c97ec316b5073d3`。0444 immutable metadata/sidecars 与联合 verify PASS；`build_origin=local_user_authorized`，Flow Run=null。
- runtime Owner仅获默认关闭代码发布 GO：API health后 Web；按实际 PID/start_ticks/argv/JAR 与旧 Web dist 摘要锁内核验，等待锁而非抢占。使用已审计私有入口，真实私有 tool SHA `f9bef60e44be9416a5ae9a4faeed9b94f02cf9db166bf4c2d454b7b4b4ea46b7`，metadata另记原 source tool SHA，未冒充原入口。实际部署结果尚待返回。

## 启用仍单列

- `/opt/cyf/service/api/.voice-runtime.env` 在发布前不存在；已安装 launcher 未改。前端 `.env.production` voice=false，后端默认关闭。代码发布不等于语音已可用。
- 已基于实际 installed launcher生成仅 Realtime profile差异候选：`/var/tmp/cyf-voice-implementation-20260930/installed-launcher-realtime-candidate`，13项解析 PASS，SHA `20c011c2367e5e28cf81b9042d6eda81163d0c78e20fec0d9ac091bcecc4d91b`。未安装、未写 production env。不能将含其他既有脏改动的整个 launcher source直接安装。
- 后续须另获生产启用/额度授权：安装精确候选，显式 cliproxy-realtime/gpt-realtime/WAV、codex gateway allowlist与服务端密钥/独立HMAC及缓存加密配置，并用 voice=true的单独前端构建发布。完整一轮录音转写+Agent回复朗读至少是两个 Provider 请求，不复用已消耗的一次网关能力测试授权；本实现 text-only 转写与 alloy配置还没有真实付费验收。
- root api/web主 checkout/gitlinks仍为用户已有脏/旧状态，不做宽泛重置或 `sddw pin`，不声称 `sddw verify` 已过。本文绑定独立worktree、远端ref及制品证据。

## 已发布默认关闭代码（16:30）

Runtime Owner已实际完成 private dry-run PASS → API 部署健康 UP → Web 部署 PASS。主 Owner独立再读线上 API JAR SHA `739154e0…3e247`、Web dist tree `9b3dc688…073d3` 与冻结制品一致，API health UP；部署记录及公网 `/`、`/juyiting` 的200证据在 release-outcome.json。Canonical launcher SHA仍 `570ac546…3d31c`，`.voice-runtime.env` 仍缺失；Web编译 voice=false，未安装候选 launcher、改配置/flags、新增 Provider调用或执行生产 DB/Rabbit 操作。

不可变完整结果：`deliverables/releases/v1.13.45-voice-realtime-local-20260930/release-outcome.json`（附SHA侧车）。API/Web同一冻结输入、准确顺序与源/制品摘要已绑定。Runtime补充健康断言首次只匹配status字符串而遗漏实际code=UP，未触发后续Web安装；按标准健康合同最小修正并归因后继续成功，未因此重复API重启。

**开发适配与默认关闭代码发布完成；生产启用和真实语音设备端到端验收未完成、需单独授权。** 下一步授权后以 cliproxy-realtime/gpt-realtime/WAV精确profile与服务端凭据配置启用，另构建voice=true前端，验收调用范围单列；此前单次能力测试不再次借用。

## 后续授权启用完成（当前状态）

用户随后确认启动，生产 Realtime 语音已通过新的 enabled Web release 与 exact runtime config/launcher 于 2026-09-30 启用且健康。首次启动 smoke token gate 失败真实保留、R2 最小修正后成功。完整结果及具体验收步骤见 `VOICE_REALTIME_ACTIVATION_20260930.md`，不可变 `deliverables/releases/v1.13.46-voice-realtime-activation-local-20260930/activation/activation-outcome-r2.json`。前文 default-off 为当时历史状态；现 **已启用、真实用户设备验收pending**。自动 Provider 调用0，两次留给用户转写+关联回复朗读。
