# INSPECT 代理路由修复与实际验证边界

日期：2026-10-02。这里只补充本次真实故障及源码修复，不替代运行台账或产品验收。

- 首次 exact `d082e1c` 图片理解只提交一个 turn。原生客户端未启用 system proxy，而隔离网络仅允许固定 CONNECT 代理；实际请求持续 connect failure，没有 Provider HTTP 回执。原生 interrupt 后 readback 为 interrupted，未重复提交，费用仍 unknown。
- 修复 `42e7b1f919b32ff1153c0db8044b45f2ab91778a` / tree `15c4cef8037309b078ed1ca269b6631b182e7874`：受限 profile 显式启用 `features.respect_system_proxy=true`，初始化核对原生配置实际读回，绑定策略摘要。固定代理、nft 和文件系统隔离未放宽。
- Owner 定向测试报告 3 pass、1 native skip；Main 核对两文件 diff 并字节一致 fast-forward，已推送并直接读回 feature 同一 SHA。后续非付费原生读回已 PASS，Main 验证前后文件摘要一致并匹配 exact Git 对象；零 thread/start、零 turn/start。真实图片 turn 随后暴露另一具体故障：sandbox 内 CA bundle 的绝对符号链接指向未挂载目录，TLS 未完成。路由修复生效不等于图片理解通过；没有 Provider 回执，费用 unknown，正在停止故障循环并修复可信 CA 物化。
- 生产旧 API 于 09:07 恢复，Main 曾独立检查 health HTTP 200/UP；但 09:35:45 再被 host global OOM 杀死，09:43 检查10018已拒绝连接，**当前 STOPPED**。内核记录 API PID3101853、SwapFree=0；atd 未重启，故不是临时 carrier 的 KillMode 触发。自动恢复亦因缺失 cgroup 挂载而在 launcher 前失败，现已熔断。没有重复人工启动。恢复未部署本特性，基础设施容量和 cgroup 问题仍须实际整改。
- 真实浏览器仅提交一次测试账号登录，随后目标页为 /juyiting；两次 CDP 读取超时，未验证完整页面互动。已关闭本任务浏览器，未进行平台收费生成或成果验收。

下一步（下文已补记图片理解通过）：在原失败 turn 已终态的前提下，用修复后 exact profile 验证真实图片理解；并行收口最终 API 源码的隔离 MySQL 迁移、完整应用接线与可冻结制品，再运行完整 34 项产品验收。版本号须发布前重新核对，不能沿用已占用编号。

## CA 字节物化修复（源码整合）

`1f95df2` 已固定受信公共 CA 的实际字节，以独立只读资源提供给 sandbox，并绑定摘要；不扩大主机目录可见范围，也不关闭 TLS 验证。初稿 `050c13a` 的 Python TLS 探针模板被 Main 实际复现 CRLF 转义语法错误；该失败保留，`1f95df2` 增加修复和解析回归。Owner 定向结果 11 pass、1 native skip，Main 复用结果并完成四文件 byte-exact fast-forward、推送与远端读回。原生 TLS 和真实图片理解尚未通过；原 Owner handle 已不可用，已明确交接给新实现 Owner，先对账既有请求而非重新执行。


## 10:37 真实图片理解通过（限定范围）

exact `1f95df25b9d073a514ba135a08fa94859723a7e8` 已完成非付费原生 TLS/代理/隔离核验，随后使用既有额度执行一次真实 localImage turn。模型正确识别参考图从左到右的红色正方形、蓝色圆形和绿色三角形，返回 ANSWER v2；终态 completed、进程 exit0，无重启或重复提交。未充值，实际费用未观测。

Main 核验 portable SHA256SUMS 全部通过、七份源码前后摘要均匹配 exact Git 对象，并比对参考图、实际答复和终态帧。证据：`integration-evidence-20260928/client-real-image-1f95df2/manifest.json`。原两次失败及费用未知记录保留，不重跑。

此结果仅证明该配置的真实图片理解；不是生产 capability 持久 readiness、客户端安装、平台鸟图生成/编辑、双接应方式或 AC01–AC22/FD01–FD12 完整验收。下一步收口实际 readiness 接线和 API 最终迁移/应用接线验证，再进入版本制品及平台流程验收。

基础设施授权更新：用户已允许临时约703 MiB swap、恢复原 cgroup 挂载和归属验证；上述整改已执行，API 是否恢复另以实际健康结果更新，不能将基础设施变更当作功能发布。
