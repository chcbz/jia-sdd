# 三端发布接续（2026-10-05 23:30 CST）

## 当前结论

Agent 已升级；API 的现有 Flow 部署已恢复、尚未启动最终发布；Web 仍 CI-only。真实业务验收 **NOT_RUN**，T05–T09 未完成。不要将 API109 / Web167 的 CI-only SUCCESS 写成正式上线。

用户最新决定：**直接升级到新版本，不兼容旧版本**。已放弃两阶段兼容包装；不得恢复该方案。新版失败保留候选、诊断与原备份，向前修复，不自动重启旧 JAR，不降级 schema。

## 已完成及证据

统一回执：[manifest](implementation-evidence-20261004/runtime-release-20261005/manifest.json)。

- Client `4e70c4fc90aaf72ee6a1e58aae7703853af449f1` / tree `4fe55783502e027ba226babea6301a0c720ec02f`，已推 feature/develop。修复真实安装失败：显式 payload 缺少导入模块 `juyiting-action-outcome.mjs`；补 relative-import 闭包回归，53 PASS，56文件。
- 共享 `codex-ws-agent.service` 与独立 `codex-ws-agent@wuyong-local.service` 于22:16:30安装上述确切提交；持久配置原字节保留，manifest与安装器hash已读回。共享全部profiles及本地实例先证实空闲再维护，无真实Provider调用。
- 现有零点调度 `flow-control.cjs` 只修 listRuns 分页。18回归通过，实际109条完整读回且无活动Run；没有创建新Run。
- API安装器增加显式 `CYF_API_FLOW_FORWARD_ONLY=1`：候选切换后失败只写原failed记录并保留候选，不 detach/restore/旧JAR start。默认其他发布行为不改。故障记录写失败也不落入旧版恢复。
- 实际备份根是已有别名 `/var/lib/cyf-api-flow/backups -> /home/isp/baks/flow-api`。只允许该精确root:root别名，物理目标仍root:root0700；其他别名/离线fixture别名拒绝。保持逻辑backup路径，不搬移目录、不改历史记录。
- 两个主机helper以**实际已安装的新基线**作最小patch，在 `/tmp/cyf-release-api.lock` 下CAS/备份/原子安装/hash读回；不覆盖脏主仓库、不改launcher、不重启应用。实际主机候选26回归PASS/0失败/0跳过，bash语法通过；SDD确切源码另外在隔离Linux fixture中26回归PASS/0失败/0跳过。SDD代码是对应最小差异，不是整份主机文件的替换来源。
- 23:23恢复API5260799原deploy段，明确forward-only；原CI源码、测试、同Run制品和主机组不变。实际配置SHA256 `a2e5d4617e110fba303a18e02115714880a4cef09a72b6858e1b08cd8d9667ed`，已normalized readback验证。未调用Start。

## 下一步（必须按顺序）

1. 由已有 `cyf-flow-backend-nightly.timer` 于**2026-10-06 00:00北京时间**启动API5260799；不要提前手动启动，不重复触发。核对现有timer/最新Run/实际intent；未知Start结果只读reconcile。
2. API目标 `329d44fd7f8d0b2402853f5eac4cf47c99fcbed9` / tree `69d2cb5448aa165b35ead9794bac0971736f1a7d`。只认新最终Run的云测、同Run制品、部署单/主机、安装record、实际运行JAR及健康。当前旧API PID19026/source b8053da6不等于目标。若失败保留证据并修新版，不自动降级。
3. API完整健康确认后，才在私有 `flow-forward-only/api-final-release-healthy-verified.json` 写真实回执，再用已有准备脚本恢复Web4403172的原deploy；脚本此门禁不可提前伪造。Web目标 `f6b81b40ee4a579c579af4cb7ab1e0e76e362173` / tree `3f70c8a345ef09359b0169785ec66d5f8cdf5102`。00:30 Web major timer仍存在，API未健康则Web不得恢复deploy。小版本仅在API健康后依既有规则启动。
4. Web同Run制品和线上dist逐字节核对，再做chcbz真实验收：无素材→明确选真实Agent→结果→同会话改稿→预览下载→不保存直接验收；混合图片/文件/音频及仅附件实际读取；纯文字/单项修改保留兄弟；刷新同确切原源且不生成；可选保存空间重开同字节；跨用户/任务及密议隔离；桌面和实际窄屏“＋”。既有预算/模型/工具，不新增付费服务。
5. 浏览器：Chrome控制桥报auth method错误；已通过现有IAB安全替代打开聚义厅，当前到登录页（tab1，api.chaoyoufan.cn/login/index.html）。用户已被通知登录chcbz，密码不要发到聊天。不要读取/导出浏览器秘密或用脚本绕过浏览器安全。API/发布仍可继续，不因页面登录阻塞而停全部工作。
6. 记录观察和失败/修复，更新SDD、目标特性分支；未实际满足的验收不标PASS。状态无变化保持安静，只在真实阻塞/用户行动/全部完成时通知。

## 接续位置与限制

主机私有根 `/home/isp/wsps/private-maintenance/mmd-runtime-release-20261005-payloadfix`：`forward-only`包含helper安装前后/26回归，`scheduler-fix`包含分页安装/18回归，`flow-forward-only`包含新的单次更新intent/config读回。

`/var/tmp/restore-mmd-forward-flow-deployment.cjs` 是新的单次配置更新上下文。API已APPLIED，不可再次apply；Web仅API健康后prepare/apply一次。旧 `/var/tmp/restore-mmd-flow-deployment.cjs` 的API更新已尝试、无forward-only，**不得重跑**。

SDD `D:\workspace\mmd-plan-1004`，自有分支 `codex/mmd-version-progress-20261004` 推 `HEAD:refs/heads/codex/juyiting-multimedia-deliberation`。API/Web/Client worktrees及远端脏主目录保留。正式测试构建发布Flow-first；不得把CI-only制品手工安装冒充Flow发布；不使用子Agent或Reviewer；不抢占/取消别人的Run；未知写入只读核对。

chcbz历史清理已完成，不再删除、不重放419/420、不全局重启ES/Redis。监控 `--status` 只读；`--check-once`可能恢复/发邮件，不用作只读探测。

## 2026-10-05 23:37:40 CST 只读跟进

既有00:00/00:30 timer仍active，Agent双实例active，API/Web/MySQL/Redis监控健康，无维护/恢复动作。IAB tab1已由用户登录；通过个人中心可见账号 `chcbz` 已核对，随后返回聚义厅并保留页签。登录阻塞已解除，不再请求用户登录。未创建事项、调用Agent/Provider或启动Flow；等待00:00既有发布调度，业务验收仍NOT_RUN。
