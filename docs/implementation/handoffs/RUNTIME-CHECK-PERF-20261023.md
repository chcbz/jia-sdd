# RUNTIME-CHECK-PERF-20261023

2026-10-23，唯一Owner：当前会话，单Agent。用户授权检查整个Runtime并减少非必要检查、提升性能；不授权生产升级、请求重放或业务状态修复扩展。

- 已读取CYF根AGENTS.md（2026-10-23固定app规则）、orchestration工具索引、SDD workflow及外部isp-install AGENTS；CYF后续固定app规则覆盖外部旧releases/current规则。公共接口固定api/docs/interface-standard.md v1.2（2026-10-14）；本次不改变业务wire。
- 源码：2026-10-23 fetch origin/develop=297272f5e7af49c6bda703b37f0fc8a6a830a4a7，tree6358a3862b7339de372de79b349a846fe2db3032；候选Runtime1.2.7未部署。现行安装仍1.2.6/7dd120f5，和开发基线分开。
- 独立worktree /home/isp/wsps/chcbz/isp-install-worktrees/runtime-check-performance-20261023，branch codex/runtime-check-performance-20261023。共享Runtime原分支与untracked specs不动，CYF根/API/Web脏工作区不切换、不mass-stage。
- 目标：审核启动/重连、网络隔离、心跳、消息/恢复、资料/技能执行/结果验证的同步重操作和重复校验；只优化证据充分的路径。保留身份/ACL、代际、幂等、锁、摘要、持久化及错误关闭。
- 首个定向反馈：既有typed-inspection-network owner/nft测试、原三并发隔离复现。轻量单测本机串行，正式重型构建另走既有规则；不调用模型、不操作生产namespace/身份状态。
- 非目标：减安全保护、加超时掩盖阻塞、扩展业务功能、修517历史状态、源码到生产安装、把候选当已上线。

## 实施与收口

- 源码候选1.2.8：040991f180e54cdad818840bafb59d368320ae47，tree6225395c62ebe932aea66e72bec155bf2e7d9901。证据提交3c993e58033d901622c24126028199cdf4e2c76f；2026-10-23普通push后readback确认isp-install远端develop为该证据提交。未触发部署。
- 全量静态扫描现行72个自有JS/Python模块，权威payload71项；按热点调用链审查，不等于穷尽第三方依赖和全部动态分支。完整清单及摘要：`/home/isp/wsps/chcbz/isp-install-worktrees/runtime-check-performance-20261023/docs/evidence/runtime-check-performance-20261023/audit-inventory.json`。
- 异步分块摘要、精确文件身份/stamp缓存、单worker执行大文件复制/版本/schema测量；普通启动/重连/资料启动均await，异步前后复核进程身份及取消。移除同一无异步间隙的重复网络owner检查；heartbeat仅复用同次调用durable结果。不取消身份/ACL、PID/startticks、namespace、幂等、锁、持久化、文件完整性和fail-closed保护。新worker与摘要模块已纳入权威交付清单。
- 精确040991f的15入口串行Node定向回归：294项，293通过、0失败、1显式skip（带凭据完整native profile握手）。源码语法、71项payload/相对import及worker引用闭包、diff检查通过。首次测试环境缺magick-wasm，后仅在本任务worktree只读复用与lock摘要一致的现行依赖；无生产依赖写入。不是正式Flow/全业务验收。
- 原1.2.6隔离三并发：1通过/2失败、事件循环最大停顿32.112秒；精确候选3/3通过、最大751.829ms。保留原15秒超时、真实292,309,256B Codex、独立bwrap/slirp/netns和nft拒绝。实验候选脚本减少fixture自身同步hash，不能将总启动时间当严格同输入吞吐对照。
- 最终真实测量：Codex0.161.0，首次冷测58,899.98ms、同进程精确缓存5.904ms，最大事件循环停顿853.541ms；264次本地HTTP观察全部403，最大724.987ms。冷测仍有成本，负载影响不能外推保证。无凭据/模型turn，自有临时HOME和holder已清理。
- 证据与脚本、日志、SHA清单：`/home/isp/wsps/chcbz/isp-install-worktrees/runtime-check-performance-20261023/docs/evidence/runtime-check-performance-20261023/README.md`；稳定操作知识见同仓`docs/cyf-agent-runtime-v1-self-host.md`性能审查节。证据JSON/清单逐项核验通过。

## 真实边界与后续

- 未制作/安装/部署候选；生产仍1.2.6，不能以develop已合入替代线上修复。完整native握手、真实二次图片修改和最终业务验收未执行；517恢复分类/API永久RUNNING及图片尺寸履约不属于本轮修复。
- 已识别但未重构的同步路径：Python成果重开、技能安装原子辅助、Git工作区子进程、资料解析/图片衍生、初始化版本探测、队列扫描。不能无证据删除边界或宣称整个Runtime完全非阻塞。
- 后续如获生产升级授权，使用固定app安装入口、绑定精确来源/制品和原锁/恢复保护，分别记录安装、通道健康、真实图片业务验收；不得直接重启旧@wuyong模板或以releases目录启动。
- 定位/实现/验证/等待精确分段耗时未独立测量，留空；本次只证实上述隔离热点改善，不宣称全业务端到端缩时。

## 后续授权：部署与重新验证（2026-10-23）

用户追加“部署并重新验证”，授权本次Runtime1.2.8受控安装及原ziyue/吴用图片业务回归；PDF仍排除，不重放517、不清UNKNOWN、不改API/Web或Provider配置。Owner仍单Agent。

- 固定发布源码为isp-install `3c993e58033d901622c24126028199cdf4e2c76f`，其运行模块与已测040991f相同；生产基线1.2.6/PID1183474。查询远端develop一致，不自动跟随后续变更。
- 复用Flow5264702，初查无活动Run；原云端配置已私有保存。云端打包71项权威执行模块及安装器指定Runtime文件，部署消费同Run制品。现用Node/JS/Python依赖逐文件摘要核验且锁/requirements完全未变，安装时复用，不在本机重新生产打包。临时安装操作沿用原激活脚本的锁、盘点、备份与身份保护，适配固定app；操作脚本SHA固定于云端配置。
- 4108项现用manifest通过；三个通道ready；本地pending/processing均空。盘点实际有7份RECOVERY_REQUIRED（不是旧迁移时的4份），以及既有2份RESULT_UNKNOWN；精确摘要保留，不修改或重放。服务器DISPATCHED旧记录单独保留。
- 恢复点采用完整停写、未压缩tar并逐项compare，覆盖完整static/managed HOME及SQLite、授权、队列、配置；原程序归档至`/home/isp/baks/cyf-agent-runtime-v1/20261023-performance/old-program`。不启动备份目录，不用旧DB覆盖新事实。当前磁盘空间足够，避免前次压缩造成47分钟窗口；最终耗时以实际证据为准。
- 临时证据：`/var/tmp/cyf-runtime-perf-release-20261023/`。初次配置schema校验被拒，readback未变；补齐步骤/作业name并规范YAML后通过，随后启动Run25。Run25精确源码正确、24通过/1失败/1跳过，失败为云镜像缺`/usr/bin/bwrap`，未进入安装；补齐bubblewrap环境依赖后Run26，禁止跳过失败测试。Run26进行中时不宣称已部署。
- 浏览器自有会话：`/var/tmp/cyf-external-flow-20261021/browser/runtime-perf-release-20261023/`，ziyue真实登录；上传蓝色256×256 JPEG、列表即时刷新/自动选中、移动预览开关已复核。待通道恢复后再发起新事项，验收本轮色彩修改与自然二次修改链路；精确尺寸问题不属于本次性能代码，不重标已修复。

### 部署与回归实绩（2026-10-23，后续授权执行）

- **已部署Runtime1.2.8**：精确3c993e5/tree d502f86，Flow5264702 Run26 SUCCESS，25通过/0失败/1skip；job541738448/541738449，部署单71694237成功。同Run制品SHA `d13d2ad2fca8ac1c16d842d6cf08ece6fa60a591ba85d2251580a1cd09e3f718`。临时Flow配置已恢复readback APPLIED。
- 固定app/PID1404284，93源文件逐项与Git匹配，依赖锁未变且复用已校验依赖，未本机生产打包；原锁、完整停写未压缩tar+compare及旧程序归档保护保留。备份`/home/isp/baks/cyf-agent-runtime-v1/20261023-performance/`，恢复见其RECOVERY.md。身份/config/unit不变，首次通道核验7恢复记录摘要不变，未清UNKNOWN。
- 三通道吴用/林冲/卢俊义connected/registered/ready且ACK新鲜。17:23:42安装启动，17:29:02通道核验；18:07业务后读回仍同PID在线。安装与业务分别记录，不把Flow成功当整体验收。
- ziyue/吴用新事项518：上传刷新自动选中、移动资料预览开关、办事直接预览、待点将返回列表通过；红/绿两轮执行都产出1254×1254 PNG且PC/移动实际可见；选绿色成果完成正式验收，权威review COMMITTED、task COMPLETED v4、delivery ACCEPTED v1，刷新后状态持久化。
- **尚有明确语义失败**：自然要求“把刚交付的红图改绿”实际仍使用原蓝图source/SHA并APPEND，不是基于红色上一版修改。因此本轮只通过两轮生成/成果验收，不宣称完整二次改稿正确。纯色样本不足以掩盖此来源问题；后续须以含可辨识细节的上一版成果验证。精确尺寸/逐像素纯色、517历史状态闭合仍未修。
- 首次review POST被自有浏览器写保护拦截，查询不存在后由UI继续原验收成功；这是测试工具注入中断，不是生产网络BUG，也不能报无中断一键验收。存在profile级ACTION_SELECTION_INVALID日志但未绑定request，不强行归因518；历史恢复仍会占chat lane，不宣称全业务耗时已优化。
- 完整分层结论与去凭据证据：`specs/juyiting-ui-baseline-20261006/evidence/runtime-performance-release-20261023/README.md`。不发布API/Web、不改Provider/模型、不重放517、不额外扩修。PDF不验。
