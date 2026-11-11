# 聚义厅语音输入与会话

> 文档收口（2026-10-23）：保留语音基础合同/历史发布与未验边界，Realtime增量单列，不重复建旧STT/TTS接入。 本轮仅核对文档归属与覆盖，不重新验证源码/上线；执行规则以根AGENTS为准。


## 目标与范围

录音输入、转写、消息发送、语音输出、方向切换中断和录音资源释放；目标合同遵循 `docs/implementation/handoffs/JVC-OAI-SPRING-AI-REFACTOR.md` 的冻结音频架构/安全要求与本目录 design.md 的发布验收约束。accepted 源码只用于核对当前实现，不能替代应建/应验合同。本次只补齐跨仓 SDD 入口，不发明接口或扩大范围。

## 2026-09-06 状态

API/Web 源码、集成和独立构建材料已有 accepted；语音生产启用与真实 Provider 证明尚未完成。

## 非目标

本次文档更新不创建新功能实现、不允许跳过现有安全合同、不宣布未验证的生产交付。

## 权威输入

- `docs/implementation/handoffs/JVC-OAI-RELEASE-COMPATIBILITY-20260905.md`
- `docs/implementation/handoffs/JVC-OAI-RELEASE-CONTINUATION-R4-CLOSEOUT.md`
