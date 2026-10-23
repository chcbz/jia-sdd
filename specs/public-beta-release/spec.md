# 公共公测发布与安全整合

> 文档收口（2026-10-23）：保留跨功能公测安全与实际onboarding未完成验收，不当作单次版本发布临时稿。 本轮仅核对文档归属与覆盖，不重新验证源码/上线；执行规则以根AGENTS为准。


## 目标与范围

按认证 tenant/client 隔离托管 Profile 与任务列表/计数，服务器运行密钥不出浏览器；公测 onboarding 与安全 preflight 集成。账号注销、交易、语音启用不随本包自动纳入。

## 2026-09-06 状态

托管隔离、任务 ACL、离线 preflight、onboarding 等源码已 accepted，存在历史 API/Web 发布记录；尚不足以宣布整包公测安全验收完成。

## 非目标

本次文档更新不创建新功能实现、不允许跳过现有安全合同、不宣布未验证的生产交付。

## 权威输入

- `docs/implementation/handoffs/PWA-PREFLIGHT-SAFETY-P1.md`
- `specs/account-security-foundation/design.md`
- `specs/oauth-public-client-hardening/design.md`
