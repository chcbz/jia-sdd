# 后端 502 / 健康恢复链路修复（2026-09-30）

所有时间为 Asia/Shanghai。本次是用户明确授权的现有制品恢复及监控修复，**无源码构建、无新发布、无 Flow Run**。

## 事实与时间线

- 09-28 21:56:48：内核 global OOM 杀掉生产 Java PID `392701`；10018 无监听，API 502。
- cron 健康检查一直运行。旧恢复 carrier 固定的规范入口 SHA 为 `63a7ba18…`，实际入口为 `570ac546…`；只读校验复现 `canonical_hash_mismatch`。三次恢复返回 `125`、未取得 native 调度收据，随后熔断。
- 邮件单次诊断复现 `SMTPAuthenticationError: 526 Authentication failure`；不能声称告警已送达，也不能仅凭此判断密码过期。
- 09-30 13:25 启动原 JAR；88 秒后健康，公网 `/agent/map` 返回预期未登录 401。但 13:30:59 同一 PID `1786131` 再次被 global OOM 杀掉。该进程继承交互 user.slice，swappiness=0；未重复相同裸启动。
- 修复后的监控在新故障 `I000129-1790746381` 的第 1 次恢复中通过独立 system.slice carrier 启动 PID `1792103`。13:35:04 获得 dispatch/invoked/terminal 全部确认、native/carrier RC=0 和 `success_health_up`；该 scope swappiness=60，沿用既有配置，未修改其他 scope。
- 后续探测 local API=UP、公网预期 401、Web/MySQL/Redis/agent 全部健康；当前状态以同目录 evidence 最新快照为准。

## 修改与验证

- 固定已自检规范入口 SHA，保留 root 权限、不可写父目录/文件、单链接、制品哈希和互斥检查。
- 新增只读 `--check`，在主监控预留恢复次数前核验 carrier 内部规范入口 pin；失配给出明确原因且不耗尽恢复次数。
- 邮件错误不再仅报 `helper_failed`，安全输出 `smtp_authentication_failed_526` 到状态及系统日志；不输出凭据/地址。
- 15 项 Python 3.6 离线回归通过，覆盖只读检查、权限/哈希负例、无效 carrier 不执行、预检失败不耗恢复次数、SMTP 错误脱敏。
- 在 `monitor.lock` 内安装并 readback 两个固定候选；后续获得真实恢复成功，不以模拟替代线上核验。
- API JAR SHA-256 始终为 `cf583138ae7fdc102d9fc482a7db088f02d9e68c0c459035b6e7ff2de6e67a12`。
- 修复源码位于 `ops/maintenance/health_monitor/`，本次未提交；安装以 evidence manifest 的 SHA-256 绑定，不冒称 Git tree 已发布。

## 未完成 / 风险

1. **SMTP 认证/提交已恢复（13:49:18）**：用户于 13:48:16 更新凭据，权限保持 root:root 0600；随后仅发送一封“【监控】邮件恢复验证”，返回 `helper_accepted`。这证明 SMTP 接受，不证明收件箱送达；未加速或清空历史告警队列。
2. **宿主全局内存压力仍存在**：本次没有扩容、抢占或清理其他任务进程/证据。已通过 orchestrator 给当前共享主机验证 Owner 发 alert-only 协调通知；没有证据断言某个特定任务导致 OOM。
3. 13:39:20 规范 status 曾单次报 NOT_READY，随后直连 actuator 为 HTTP200/UP（0.58849s）；未证明该次探测原因，不声称持续无抖动。
4. 未执行登录后业务、生产数据变更或付费操作；401 只证明匿名鉴权边界和代理/后端恢复，不代表完整业务验收。

证据目录：`/home/isp/wsps/cyf/docs/implementation/evidence/api-502-health-20260930/`。
原文件与安装备份（root-only）：`/root/cyf-incident-20260930-502/`。

## SMTP 凭据更新后复核（13:49）

本机 actuator HTTP200/UP、公网匿名接口 HTTP401、监控无活动故障、恢复熔断已解除。单次测试邮件获 SMTP 接受，未记录任何凭据值。收件箱/垃圾箱需收件人确认；原认证失败证据作为历史保留。新回执：`/home/isp/wsps/cyf/docs/implementation/evidence/api-502-health-20260930/mail-verification-after-credential-update.json`。
