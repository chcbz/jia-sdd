# 网络自检隔离复现（2026-10-23）

直接导入当前安装Runtime1.2.6的RestrictedProviderEgress，原身份校验/nft默认拒绝/15秒超时均保留。真实Codex app-server从现有快照只读挂载，HOME在新tmpfs，无凭据、不initialize、不发模型turn。每路独立bwrap/slirp/netns，同一个诊断Node进程承载三路代理与身份校验，模拟生产共享事件循环的启动竞争，不代表完整生产turn回放。

原始脚本保持运行时字节，不作为通用runner：固定安装模块/快照路径，输出只允许/var/tmp/cyf-doc-chain-fix/rootcause-repro-20261023/。必须先核对路径、源码摘要与工具权限，不能盲目在其他主机运行。三路脚本第三实参codex选择真实大文件holder，省略则是/usr/bin/sleep对照。仅清理自身子进程；不读取生产身份文件、不修改生产namespace/防火墙。

```bash
node reproduce-three.mjs /var/tmp/cyf-doc-chain-fix/rootcause-repro-20261023/owned-output.json codex
# 对照：同样三并发与检查，仅换小体积可执行文件
node reproduce-three.mjs /var/tmp/cyf-doc-chain-fix/rootcause-repro-20261023/owned-control.json
```

诊断spawn包装只把Python原探针吞掉的recv异常输出到stderr，不改变判定/重试/超时；观察HTTP connect/finish/close事件与原_assertOwner耗时，不跳过任何校验。小文件单路baseline未增强recv异常日志。脚本注释中的dummy holder适用于小文件模式；codex模式实际运行真实Codex holder。holder提示临时HOME不创建PATH aliases、缺PATH bwrap但可用bundled bwrap，不是本故障原因。

summary.json聚合结果；原始JSON保留每次事件和attestation，不含凭据。事件时间为父Node进程相对时间，Python stdout/stderr可能缓冲，不作为精确网络包时间。探针实际捕获timeout，不能将打印时间误作recv超时发生时间。

三并发真实Codex：2 FAIL / 1 PASS，复现同样connected [空HTTP] blocked blocked；两个失败recv异常都是timeout。proxy CONNECT回调较对应Python spawn晚31.988秒、24.143秒；共享循环最大停顿32.112秒。三并发小文件全部PASS，最大停顿0.722秒。单个真实CodexPASS但最大停顿9.311秒；两路PASS但14.034秒。未注入人工sleep/CPU负载；180秒只用于小文件诊断holder自身存活，不是业务deadline。

可确认同源码在此机器上出现同步身份测量挤占代理事件循环的故障机制；不能唯一重建14:40历史现场并发/调度：旧探针没有异常/时序日志。不是模型故障或隔离绕过证据。本轮没有修复、重发517、发布或验收通过。
