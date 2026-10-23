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
