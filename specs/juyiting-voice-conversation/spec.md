# 聚义厅语音对话

- Feature ID: `juyiting-voice-conversation`
- Status: Ready for implementation
- Contract freeze date: 2026-09-01

## Problem

聚义厅当前只支持文本输入。在横屏沉浸模式中，用户需要打开右侧议事抽屉、拉起软键盘并手动发送，打断场景体验；Agent 的回复也只能阅读，不能像自然聊天一样听取。

## Goals

首个可交付版本（V1）实现：

1. 在三种讨论范围（public/private/bounty）的 Composer 中提供按键录音。
2. 在横屏且聊天面板关闭时提供紧凑语音 HUD。
3. 使用浏览器 `getUserMedia + MediaRecorder` 采集最长 45 秒、最大 5 MiB 的单声道短音频。
4. 音频通过独立认证接口转写；转写接口不创建会话、不写消息、不调用 Agent。
5. 支持手动采用转写，以及用户显式开启后的 1.5 秒倒计时自动发送。
6. 自动发送必须使用录音开始时冻结的显式会话上下文；发生任何上下文或草稿冲突时降级为手动预览。
7. Agent 文字回复仍通过现有 `/chat/stream` 产生并作为权威记录；用户可显式开启“语音回答”，在完整回复结束后调用独立 TTS 接口并播放。
8. 语音失败、供应商关闭或浏览器不支持时，现有文本聊天、地图、任务和 Agent 路由不受影响。

## Non-goals

V1 不实现：

- 自动执行高影响 Agent 操作或绕过既有确认流程；
- 根据语音内容自动推导、切换或补充目标 Agent；
- 连续免按键 VAD、边答边说、用户打断、全双工 WebRTC；
- 音频、转写或 TTS 音频的业务持久化；
- 长音频、说话人分离、离线识别；
- 将 Web Speech `SpeechRecognition` 作为主路径；
- 修改 `/agent/map`、`/agent/roster` 数据流或恢复 `/agent/active`。

## Scope

### API

- 新增认证的 `POST /chat/speech/transcriptions`。
- 新增认证的 `POST /chat/speech/synthesis`。
- 新增 provider-neutral 的 STT/TTS SPI、配置、错误模型、超时和默认关闭开关。
- 身份直接来自已认证 JWT，不依赖 `EsContextHolder`。
- 应用层限制上传大小、媒体类型、请求并发和速率；测试不得调用真实收费供应商。
- 无数据库迁移。

### Web

- 新增唯一的 `useHallVoiceConversation`/等价 composable，由 `JuyiHall.vue` 创建。
- Composer 与横屏 HUD 作为同一状态机的薄视图。
- 新增上下文快照、draft revision、generation fence、AbortController 和媒体资源清理。
- 自动发送仍复用现有 `handleSendHallMessage`/`sendHallMessage`，但必须允许显式传入冻结的 content/context。
- 回复完成后可调用 TTS 并播放；文字消息始终保留。

## Constraints and risks

- public/private/bounty 当前共用一个 draft，必须 CAS 校验，禁止迟到转写覆盖新草稿。
- Composer 的 Enter 当前会发送，转写预览不得进入该 submit 路径。
- `getUserMedia` 权限 Promise 不可可靠中止，取消通过 generation fence 实现；迟到 stream 必须立即停止 tracks。
- 当前 `EsContextHolder` 是未见 finally 清理的 ThreadLocal；新端点不得读取它。
- 当前全局 Nginx body limit 和 `/chat` timeout 对语音过宽；生产启用前需要精确 endpoint 配置，但不在 V1 源码交付中直接修改生产配置。
- 当前 OpenAI-compatible chat base URL 不保证支持音频端点；默认开关关闭，供应商能力需单独灰度验证。
