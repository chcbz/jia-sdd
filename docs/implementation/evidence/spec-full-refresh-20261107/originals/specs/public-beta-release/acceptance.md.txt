# 公共公测发布与安全整合 — 验收

托管隔离、任务 ACL、离线 preflight、onboarding 等源码已 accepted，存在历史 API/Web 发布记录；尚不足以宣布整包公测安全验收完成。

## 未完成验收

- [ ] 关联 exact API/Web 安全修复与实际部署 artifact
- [ ] 账号/迁移及 credentialed 浏览器安全验收
- [ ] 实际用户 onboarding 可用性与隔离验证
- [ ] 记录公测 release baseline 后才关闭整体需求

## 证据边界

源码 Review、selector 测试、build、推送、部署、运行时激活分别验证。当前阶段不能整体标记 PASS；既有测试只引用，不重跑，不操作其他线程证据目录。逐任务 SHA 与证据摘要见 delivery-status.md。
