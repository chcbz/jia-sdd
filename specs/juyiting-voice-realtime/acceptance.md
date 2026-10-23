# 验收

- [x] API 新模式只连接 Realtime；离线协议/错误/清理及 WAV/身份/缓存回归通过。
- [x] 浏览器可生成 24k mono PCM16 WAV，转写确认与明确 Agent/上下文发送语义保留。
- [x] 正确识别 WAV 回复，取消/迟到/身份隔离与旧相关测试通过。
- [x] exact API/Web commit/tree 的构建及制品摘要，采用用户授权本地发布时标 build_origin=local_user_authorized。
- [x] 已验证 SHA 非覆盖合入 develop，冻结新 release 分支，按既有互斥/可恢复安装/健康规则发布。
- [x] 生产 Realtime 语音启用：R2 配置/launcher/Java 环境、API health、enabled Web live tree、公网浏览器形态 CORS/认证及引用 JS 摘要核验 PASS。
- [ ] 真实用户设备端到端验收：两次 Provider 调用预算保留，尚未发起，不冒充麦克风/扬声器验收。

已有网关能力证据：docs/implementation/VOICE_REALTIME_VERIFICATION_20260930.md。不是本实现的页面验收。

代码发布记录：`deliverables/releases/v1.13.45-voice-realtime-local-20260930/release-outcome.json`。105 API/83 Web相关测试与两组件构建PASS，API UP、Web / 与 /juyiting 200，production voice=false。浏览器worklet为oscillator验收，不冒充物理设备验收。

当前已启用结果：`docs/implementation/VOICE_REALTIME_ACTIVATION_20260930.md`；不可变 `deliverables/releases/v1.13.46-voice-realtime-activation-local-20260930/activation/activation-outcome-r2.json`。Web 新增显式确认发送，84 项相关测试及 enabled production build PASS；API 复用原 105 项测试/原制品，14 项配置解析与 actual no-JWT env PASS。首次 missing-smoke gate 失败已恢复并保留 outcome，R2 最小修正成功。自动 Provider 调用0、用户真实设备验收pending。
