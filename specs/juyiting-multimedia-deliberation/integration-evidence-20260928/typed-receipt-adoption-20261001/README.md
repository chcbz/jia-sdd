# Typed回执领域分离：本次详设与真实源码核验

2026-10-01；所有文件由本轮只读核验产生或从原精确组合回执字节复制。不是运行台账，不是产品验收/发布证明。

- `branch-readback.json`：四仓远端 HEAD、tree 和本地 ancestry；当前 fast 与本次观察到的 develop 均已包含。不重复创建分支、merge 或变更组件 pin。
- `web-13-regression.stdout.gz`：891a1ec 精确候选13文件实际193通过/0失败，旧语音 harness 两失败不再复现。原189通过/2失败历史仍在上一证据目录。
- 五份原固定 probe 及其 stdout/exit：原六边界、UNKNOWN恢复、同版本OPEN轮询、七项回执测试通过；合法请求进展 probe 1通过/2失败。mock transport，不是 live API/browser。
- `api-typed-v3-composition.json`：8fc61c 无冲突、byte-exact组合；本轮未跑API。源码中的receipt状态混用未修。
- `manifest.json`：精确候选、命令、结果、文件摘要与剩余范围。193项套件通过不抵销两项真实状态失败，候选不晋升。

复跑：已安装本仓依赖时，在精确候选worktree执行manifest中的argv；`WEB_TYPED_WT=<exact-worktree> node <absolute-probe-path>`执行probe。测试输入均是假传输/固定ID，不调用Provider、不读取真实资料。
