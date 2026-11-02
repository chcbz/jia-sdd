# JUYITING-POLLING-20261102

Owner：本聊天；2026-11-02用户要求全面排查Web/API/Runtime轮询，去掉不必要轮询或提出优化策略。

## 范围与边界

- 全仓扫描定时器/调度/递归重试，沿真实网络/数据库调用区分数据轮询、事件驱动补读、连接保活/租约、动画/计时器、后台可靠任务。
- 先盘点频率、触发/停止、可见性、在途串行、失败退避、身份取消、已有推送；只对确认冗余点做局部修复，不把大范围排查扩为全项目重构。
- 不删除身份/撤销/fence/幂等、租约与恢复，不以关闭后台任务/丢事件/屏蔽真实错误换性能，不自动重放旧任务。不新增统一框架、性能拒绝阈值或业务deadline。
- 本任务未授权新的生产发布/数据迁移，不接管其他任务安装和锁；重型测试构建仍走Flow，各Run<=600s，worker-only。不在本机编译/打包应用。
- 规则：/home/isp/wsps/cyf/AGENTS.md；RB-1 /home/isp/wsps/cyf/specs/juyiting-skill-execution/responsibility-boundaries.md；接口规范在固定API aa6ecf935343caed76f6d0c657f9847025de4600的docs/interface-standard.md。外部Runtime本任务显式遵守上述CYF职责与分层规则，但不修改其他项目/共享技能规则。

## 固定基线（16:18 fetch成功）

- Web origin/develop `339f3be8af09e09ba46e0b29a8e68d8fc30d8576`；本地HEAD ca22ac29、有其他任务脏改动，不能当当前源码。
- API origin/develop `aa6ecf935343caed76f6d0c657f9847025de4600`；本地HEAD516267bf、有大量其他任务改动，保留。
- Runtime `/home/isp/wsps/chcbz/isp-install` HEAD及origin/develop `32416ed5bbde7ee25ba199ad586dbd0e4386e89c`，主仓当前干净。审查仅CYF相关conf/codex-bridge及conf/cyf-agent-runtime-v1。
- 实际线上记录：Web401/1.16.90/5470363fc33d7689890763a54eb0ee23ac8d84d2；API439/8ad42be7815e499077c6a97439f0f13c96c7650e；Runtime RELEASES记载116/1.3.33/32416ed。源码盘点与线上版本分别核对，不将最新develop行为冒充已上线。
- 轻量入口：ops/orchestration/README.md；用git show/grep读取固定源码，暂不创建worktree或修改共享脏源文件。
- 证据：/home/isp/state/cyf-diagnostics/juyiting-polling-20261102/，baseline.json、各层timer命中和定向源码快照。命中数量不是轮询数量，排除测试/历史证据/资源生成物后人工分类。

## 验收

交付按层/功能的轮询清单与处理建议；实现范围明确，定向验证覆盖在途不重叠、隐藏/卸载/身份切换、断连恢复、终态与失败语义；源码修改/测试/集成/上线分别记录，不以源码静态搜索代替生产流量测量。

## 本轮实施

- 审计报告：`JUYITING-POLLING-AUDIT-20261102.md`，覆盖Web网络读/恢复、API持久发现/SSE后台扫、Runtime双命令lane及心跳派生对账；timer文本命中不当作请求数。
- 共享Web源在旧branch且有本任务相关脏改动，已最小隔离到 `/home/isp/wsps/worktrees/juyiting-polling-web-20261102`，branch `codex/juyiting-polling-20261102`，base339f3be8。继承本任务根规则与Web AGENTS；不覆盖原工作区。
- 仅内部无界面/协议改变：场景singleflight+隐藏页跳过；回复poll在途保护+停止回调隔离；修正正文出现但请求仍busy时提前停核对。
- 两个既有测试文件定向75项通过（轻量Mocha、无build）。首轮暴露旧停止条件，已归因修复，不跳过测试。正式Flow未运行；API/Runtime未修改、未部署。
- 待验候选commit：`5eaf8e1191abc859043953bdc4e01f53a9e2cb79`，tree：`8ac2352b615d58fe1fe63ec33d7b4c9b61aae9ed`；仅提交本任务4文件，未push/合入/发布。工作树保留供后续Flow与集成使用，未清理他人工作树。
- 定向ESLint返回2项错误；对固定base用stdin重跑确认两项均原有（scene未使用parseVersion、conversation属性简写），未新增规则豁免或顺手清理。详见证据web-eslint.log和web-eslint-baseline.log；不能宣称lint全绿。git diff --check通过。

## 用户收口：先完成前端（2026-11-02）

- 用户明确先落地前端，后端/Runtime方案再讨论；本轮不修改两端源码、调度、参数或服务。前述“唤醒+退避”仅候选讨论，不是已采纳设计。
- 复用原Web worktree，fetch后将本任务首批commit rebase至远端develop `4ea31bb`（1.16.92），保留其他任务议事图片/工具栏修复。最终完整SHA以候选回执为准。
- 本轮范围：技能市场无待办停timer，活跃操作只查原change且终态合并目录刷新；打开/返回前台/匹配跨页签存储通知重新读取权威目录；不自动重放未知写入。补技能结果、议事、成果目录、验收、个人执行、点将等待、案卷问答的页面可见性/在途/停止代次保护。
- 不改界面布局、控件、操作路径、报价确认或展示语义；沿用现有刷新按钮和错误展示。本轮为内部网络生命周期优化，不新增无关交互原型或新轮询框架。权限仍由服务端核对，展示结果不做跨身份全局缓存。
- 技能结果仅在本轮后台tick跳过已终态引用；手动刷新/返回前台/作用域改变仍全量重新核验。完成正文和持久request终态仍区分。
- 必要降级/未知结果核对/失败重连保留，不以性能预算取消执行、不新增业务等待截止时间；PWA更新与本地动画/倒计时不是本次高频业务网络轮询整改目标。

## 前端集成与正式验证（2026-11-02，17:41 CST）

- 最终基线更新至Web develop `98f7682c9928ec7d1f91b50519b0a20263a1049c`，保留其他Owner同期修复。Web1.16.95，候选 `362f2fc094e89eff853d81c0e3c2b9f086356b55`，tree `ecf667b7a2e083119821af211709ee1cd4b0470f`；task branch与develop均已push成功。此前5eaf8e1/4ea31状态仅历史，不是最终候选。
- 正式Flow `4403172/407` SUCCESS；固定上述SHA，安装依赖/完整测试/Vite构建/制品上传及代码扫描作业成功，Run创建至更新终态134秒（17:38:05—17:40:19 CST）。扫描成功不表示无告警，不能宣称全仓ESLint全绿。没有Flow SSH/VMDeploy/主机等待，没有安装或线上业务验收。
- 控制面保留原配置备份，只更新已有expected SHA；readback一致。原flow-control start因历史分页在写请求之前拒绝；随后按SDK文档完整分页只读核对所有历史及无活动Run，核对原配置摘要，再单次启动返回407。没有对模糊启动盲重试，未改公共控制工具。证据flow-full-history.json、web-start-context-reconciled.json、flow-start-sdk.json。
- 本机轻量回归：frontend-core-final.log 184通过；demand-tests.log 133通过（与前者重叠，不相加）；market-component-final.log实际组件2通过；archive-visibility-tests.log实际组件1通过；scene-final-tests.log最终scene20通过。后者命令同时指定不存在的workspace测试文件，只有scene真正执行，不能声称workspace通过。正式覆盖以407制品内报告为准。
- JS生产源码定向ESLint未报错；两Vue文件既有155错误/131警告按rule/message与基线一致。追加检查测试文件发现14项风格/既有诊断，保留js-eslint-final.log与test-eslint-baseline.json，不声称所有测试文件lint通过。git diff --check通过。
- 后端/API与Runtime仅保留审计建议；未实施唤醒、退避、队列或缓存改造，方案须另行讨论。尚无生产请求量/CPU改善实测。

### 制品与收口

- 407同Run不可变制品读取核验：commit/tree/version/run均匹配；完整Mocha报告3686 passing / 2 pending / 0 failing，508 suites，61.275秒。制品109696700字节，SHA-256 `9841368e2fcae537e6f7e566d547d7acc5bd9095dcb00f97896b01d3593b2bbb`，612个dist文件；仅验证来源和报告，不安装。证据 `frontend-final-evidence.json`、`flow407-test-report.json`、`flow407-release.json`。下载首次网络超时，按同一不可变对象Range续传并核对完整大小/归档/来源，无重复构建。
- 补充lint边界：测试文件14诊断中基线已有9项，本轮新增5处多余空行风格提示；生产JS无错误。保留真实结果，不将云端scan SUCCESS宣称全仓无诊断，不为纯风格追加付费构建。
- 17:47 CST只读远端核对develop与task branch均为362f2fc；本任务worktree干净且只有共享node_modules符号链接，保存证据后移除链接并删除本任务worktree，保留已推送commit。未动共享Web/API脏工作区、他人进程/工作树、生产安装及身份状态。
- 稳定知识追加至docs/juyiting-runbook.md“前端后台观察生命周期”；该文档既有其他任务改动未整体提交，根gitlink保持不动。后端/Runtime方案等待后续讨论；前端已集成及正式验证，未部署、无生产性能改善百分比。

## 用户授权部署（2026-11-02 18:32 CST）

- 用户明确“部署”，只部署本轮Web1.16.95；复用Flow4403172/407固定362f2fc及原SHA-256制品，无新增构建/运维Run。安装前实时查询407仍SUCCESS，线上原Web406/1.16.94/98f7682。
- 在现行deploy.lock下备份原612文件与record，tar compare成功。备份 `/home/isp/baks/cyf-web-flow/20261102-polling-web407`；归档SHA-256 `c84da377cfe02e1efb60d00a052f1cd45091a3663b063201a4502b3aea9ec47d`，RECOVERY.md保留恢复说明。固定来源复制至现行downloads/407/package.tgz并复核摘要；未本机源码构建。
- 原受控 `/usr/local/sbin/cyf-web-flow-deploy` 安装exit0，record为407/362f2fc/online_verified。公网首页最初两次返回已知旧入口，第三次匹配新摘要；未绕过验证或重新构建。
- 独立只读核验612个安装文件全部匹配；公网首页/入口资源/聚义厅/技能管理及市场路由共11项HTTP200、长度/SHA-256匹配，并核实相关JS从当前入口依赖图可达。证据 `/home/isp/state/cyf-diagnostics/juyiting-polling-20261102/deployment/deployment-verification.json` 与web-public-resources.json。
- API/Runtime未修改或重启；没有数据库操作。该结果为安装与线上资源核验，不冒充登录业务全流程或生产请求量/CPU收益测试。已打开旧页面需刷新加载新版本。本节替代本任务此前“未部署”的当前状态，历史CI记录保持原貌。
