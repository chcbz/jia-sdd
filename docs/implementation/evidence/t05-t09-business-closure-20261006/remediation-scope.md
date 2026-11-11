# 客户端修复与启用范围（用户已授权；已实施 scope 修复与共享客户端更新）

- 目标：`/home/isp/apps/codex-ws-agent` 共享客户端中的测试 Agent `agt_510b7fea20564b52bc70b3a08d2c6c4f`，任务 423。
- 源码：从已安装精确 commit 建独立 worktree；不改主源仓现有脏文件。最小修复 managed CHAT/typed 控制传递，补禁用、显式覆盖与隔离测试。
- 启用必须限定测试 Agent，CHAT 目录及权限独立，不共享模板 workdir；无法限定则停止。INSPECT 另行核验隔离/carrier；不伪造 READY 或放宽 admission。
- 已授权的 live 操作：核对精确 Owner、进程归属与活动任务；保存配置前值、release 指针及摘要；通过既有发布路径安装固定候选，在已协调窗口重启共享客户端，readback 并验证 measured readiness。
- 不包含：重启 wuyong-local/API/Web、新增付费配置、生产直接 DML、清数据、历史 START 重放、覆盖其他聊天运行或进程。扩大范围需再次确认。
- 恢复：恢复配置与原 release 指针，按相同归属边界协调重启，核对重新注册与健康；保留失败证据和任务 423。
- 修复通过后经 orchestrator authorize-remediation 记录实质变化，再继续原 intent，覆盖 T05–T09 未运行的业务用例。

2026-10-06 续办：用户明确“继续，有问题则修复后重新验证”。已备份到私有维护目录；候选 d6fb80271d7cfb4e4b165daad7319dc3b459ce7f 安装，57文件摘要匹配。仅共享服务更新，wuyong-local PID1145032 未变化；测试 scope 精确绑定 generation。0.160.0 协议摘要与已有0.159.2一致，新契约通过实际初始化测量，未绕过信任检查。

2026-10-06 最新状态：共享客户端固定候选62a556dfbe7f9004349790c460b5f4c6ca87809c 已按空闲/无lease校验后由既有installer安装，57文件摘要匹配，实际READY及只读native身份GET200。API新根因是后台taskFacts缺失身份上下文，修复4e0091ea16已合develop，Flow113正式云测/构建SUCCESS，新增3项回归PASS；未安装；API发布仍遵循夜间时段，不因此扩大即时重启、生产DML或时段例外授权。

2026-10-06 16:46追加现状：API113已按用户明确提前发布授权通过既有ops Run10安装并正常重启，临时控制已恢复；不是未授权API操作。当前客户端fe2583已按同一共享客户端scope更新安装，原423自动请求已真实文本完成。Web89b7cfa通过现有release Run169修复实际缺失的指派上下文，普通已授权develop发布，不本机生产构建、不重启Web服务、不重复创建/点将/首条请求。T05–T09仍未全部验收。

2026-10-06 17:34：635431客户端ACK按原共享测试范围经空闲核对安装，不扩大服务或权限；Web170已上线。原423同key恢复及多成果编辑、真实精确验收服务端完成。最新实测Web receipt null-slot缺口已修复1e5b21c并经release171正式云测，当前仍候选。INSPECT仅做当前精确profile隔离及受限网络测量，尚无当前carrier准入，不启用或伪造READY。原最终验收已完成，后续必须GET-only恢复。

## 2026-10-06 18:13新增边界

Web172已正式上线并完成原fin GET-only浏览器恢复；原task423不再POST验收/点将/重放START。当前client4597安装但systemd主机cgroup拓扑缺失导致Node执行前失败，共享服务MainPID0后仅停止失败自动重试；API/wuyong不操作。图文2case证据真实通过并仅oneAgent授权，不开启失败audio。主机cgroup挂载恢复超出既有installer/普通restart范围，等待用户明确授权；不自行全局mount/unmount、重启主机或其他服务，不直接生产DML。


2026-10-06 19:08追加：用户授权cgroup恢复已执行，只重启共享服务，主机12hierarchy保留。client16b490f修复private mount/netns路径与stdout排空，单Agent图文carrier通过，当前PID1727606。原423不动，新task424只创建/点将各一次；两个INSPECT child因后端旧capability判断FAILED，禁止同输入第三次发送。后端fba46c候选合入develop，release5260799 Run114云测构建中；历史API113提前安装授权不转移到114，未动发布intent或生产数据。

2026-10-06 20:16追加：新AGENTS替换旧自动/定时发布规则。用户已精确授权Run114同Run原制品通过Flow安装，仅API正常restart及既有backup/recovery；未授权清理历史下载。实际空间预检缺89944501bytes，未启动部署。候选仅旧Run78下载199106859bytes，云端原件全字节SHA核对PASS；需明确授权该精确文件删除，保留所有回退JAR、数据、证据及其他服务。
