# FLOW-CI-01：Python-only 自测停止与有界整改

Writer Knuth (`01a0856a-40b0-7ce2-8322-48bbda53af81`) 位于独立 worktree `.worktrees/aliyun-flow-ci-20260909`。未跑真实 Gradle、未 push、未修改任何生产或云效配置。

| 轮次 | 已确认失败 | 当前状态/整改 |
| --- | --- | --- |
| 首次自测 | fixture 未创建 /tmp/cyf-flow-* 父目录；argparse help 透传错误 | Writer 已修复后做第二轮 |
| 第二次自测 | git grep -E 收到 PCRE `(?:...)`，正则编译失败 | 8项6PASS/2ERROR；均发生在伪Gradle前，停止重试；改为明确的POSIX ERE或标准库逐blob扫描 |

原通知 ID：`ca1284f43035de7a2bd6b9c0564c3984780c1eb35d432bfd30ac46e93c1967d7`、`d580e8e1d7cc63dcc6e1c23230481aa3f43656a4397cf754613fbd302951a59f`。源码尚未提交，HEAD为 `ee7a863b79c9ee636b0f90afb41c6be94dfd051a`（baseline）。

主控额外静态确认了一个实施阻塞：issue_ticket 当前要求 controller 整仓 clean 且 HEAD/tree 等于 task exact_sha_tree。这不适用于唯一主控脏工作区/多任务账本，且把工具仓库树错误当作 API 验证树；绝不能为通过它复制 ledger 到 worktree。

拟有界整改（需独立Reviewer确认后原Writer执行）：

1. 修正 scanner 的正则方言，不执行第三轮真实/伪Gradle直到授权；补捕获回归。
2. ticket issue 必须读唯一实际主控 ledger，校验 task owner/gate 和 **API source commit/tree**；不要求包含其他任务修改的主控整仓 clean，也不能复制账本。工具单独按已审查精确文件摘要绑定；如记录 controller Git HEAD/tree，明确仅为控制仓快照，不冒充工具源码摘要。可选择显式 clean tool-worktree 输入并核对实际入口字节，但不得新增第二当前账本。
3. 补最小测试：主控dirty但已固定工具且source匹配可签发；source/task不匹配拒绝；被篡改工具/票据拒绝；无ledger复制。补README实际CLI、Flow环境变量和产物取回步骤，清理仅本任务生成的pycache，不扩大到通用发布系统。
4. 原Writer允许一次 Python标准库自测，不运行真实Gradle/完整套件。之后提交允许路径，独立源码Review与独立轻量验证通过才集成。

独立 Raman (`01a08578-b014-78b0-ad28-ac9397bc08ad`) 对上述有界整改 ACCEPT P0/P1/P2=0/0/0：只修 scanner、API tuple/唯一ledger绑定、对应Python测试/README和本任务pycache；不授权真实Gradle、云端运行或主控清理。提交后另行完整Review。
