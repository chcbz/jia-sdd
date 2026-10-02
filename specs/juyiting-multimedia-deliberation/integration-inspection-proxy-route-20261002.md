# INSPECT 代理路由修复与实际验证边界

日期：2026-10-02。这里只补充本次真实故障及源码修复，不替代运行台账或产品验收。

- 首次 exact `d082e1c` 图片理解只提交一个 turn。原生客户端未启用 system proxy，而隔离网络仅允许固定 CONNECT 代理；实际请求持续 connect failure，没有 Provider HTTP 回执。原生 interrupt 后 readback 为 interrupted，未重复提交，费用仍 unknown。
- 修复 `42e7b1f919b32ff1153c0db8044b45f2ab91778a` / tree `15c4cef8037309b078ed1ca269b6631b182e7874`：受限 profile 显式启用 `features.respect_system_proxy=true`，初始化核对原生配置实际读回，绑定策略摘要。固定代理、nft 和文件系统隔离未放宽。
- Owner 定向测试报告 3 pass、1 native skip；Main 核对两文件 diff 并字节一致 fast-forward，已推送并直接读回 feature 同一 SHA。后续非付费原生读回已 PASS，Main 验证前后文件摘要一致并匹配 exact Git 对象；零 thread/start、零 turn/start。真实图片 turn 随后暴露另一具体故障：sandbox 内 CA bundle 的绝对符号链接指向未挂载目录，TLS 未完成。路由修复生效不等于图片理解通过；没有 Provider 回执，费用 unknown，正在停止故障循环并修复可信 CA 物化。
- 生产旧 API 于 09:07 恢复，Main 曾独立检查 health HTTP 200/UP；但 09:35:45 再被 host global OOM 杀死，09:43 检查10018已拒绝连接，**当前 STOPPED**。内核记录 API PID3101853、SwapFree=0；atd 未重启，故不是临时 carrier 的 KillMode 触发。自动恢复亦因缺失 cgroup 挂载而在 launcher 前失败，现已熔断。没有重复人工启动。恢复未部署本特性，基础设施容量和 cgroup 问题仍须实际整改。
- 真实浏览器仅提交一次测试账号登录，随后目标页为 /juyiting；两次 CDP 读取超时，未验证完整页面互动。已关闭本任务浏览器，未进行平台收费生成或成果验收。

下一步：在原失败 turn 已终态的前提下，用修复后 exact profile 验证真实图片理解；并行收口最终 API 源码的隔离 MySQL 迁移、完整应用接线与可冻结制品，再运行完整 34 项产品验收。版本号须发布前重新核对，不能沿用已占用编号。
