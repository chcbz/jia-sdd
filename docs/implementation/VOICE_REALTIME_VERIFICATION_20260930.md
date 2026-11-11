# CLIProxyAPI Realtime 单次真实语音验证（2026-09-30）

## 结论

北京时间 **2026-09-30 14:19:05–14:19:12**，使用 CYF 已配置的同域网关凭据，对 `wss://codex.chcbz.net/v1/realtime?model=gpt-realtime` 完成一次真实音频输入→音频回复测试。会话 `response.status=completed`，正常关闭。网关语音链路已验证；**不是 CYF 浏览器集成、真实麦克风/扬声器或生产启用验收**。

## 范围与结果

- 用户在本聊天明确允许：使用现有账号额度测试一次，不新增购买、不启用生产语音。客户端连接尝试 1 次、`response.create` 1 次、自动重试 0 次。
- 使用线上已部署 JAR 的既有 `spring.ai.openai` 配置；密钥只在进程内解密并经 stdin 传给探针，不写入日志、证据或命令行，不向其他域发送。
- 输入：公开 speech_recognition English 测试音频，转为 PCM16 / 单声道 / 24 kHz，2.744958 秒，131758 bytes；不是用户隐私录音或真实麦克风采集。
- 收到 `session.created`、`session.updated`、`input_audio_buffer.committed`、音频及转写 delta、`response.done`；协议为 Realtime GA，服务回报 model=`gpt-realtime`。
- 回复转写：`1, 2, 3`。音频 PCM 108000 bytes / 2.25 秒，封装 WAV 可解析、RMS 4555、peak 27680；未声称已通过人工听音或设备扬声器验收。
- 用量回执：input 51 tokens（text 24 / audio 27），output 62（text 17 / audio 45），total 113。没有金额回执，不能据此声称免费或确切费用。
- 没有修改业务代码、运行配置、进程、数据库或前端开关。

## 能力边界与下一步

此前未认证探测：`/v1/realtime` 返回 401，旧 `/v1/audio/speech` 与 `/v1/audio/transcriptions` 返回 404。此次成功只证明 **Realtime 会话**，不证明独立 STT/TTS 地址恢复。旧 2026-09-17 任务针对独立 STT/TTS 的历史 404 仍是真实记录，不能再用它概括升级后的全部语音能力。

CLIProxyAPI 部署版本未从响应中取得；探针参考上游源码 SHA 见证据，不能作为线上版本证明。下一步是单独适配 CYF 的 Realtime 会话、身份隔离、取消与音频播放，并验证浏览器设备链路；不要只启用旧 STT/TTS 开关或宣称完整语音功能已上线。

## 证据

同目录 `evidence/voice-realtime-20260930/`：`result.json`、`events.jsonl`、输入来源及摘要、输入/输出 WAV、探针源码、`sha256.json`。该目录属于本次验证，不依赖临时目录长期保留。执行准备时 GitHub raw TLS reset，改用同 commit 的 GitHub contents API 读取源码；该异常没有产生额外网关会话。
