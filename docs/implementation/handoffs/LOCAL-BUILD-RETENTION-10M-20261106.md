# LOCAL-BUILD-RETENTION-10M-20261106

## 范围与固定输入（2026-11-06）

- 唯一 Owner：local-build-retention-owner / developer；状态以 TASKS.yaml 中同名任务为准。
- 工作区 `/home/isp/wsps/cyf`，develop；base commit `136e0682c6436f7ad3122dfd9a5fffee7698c82e` / tree `2057f8e0ae1b5ebcb1980390f496070f80258e74`。仅本地引用，未查询远端，不声称远端最新。保留既有脏修改，未创建新 worktree。
- 目标：复用既有 completed-tasks.json 和 rebuildable_cache_cleanup.py，让 Owner 明确完成的本地包进入既有低磁盘自动清理范围；重申本地完整构建发布600秒优化目标。最早验证为纯 Python/临时文件隔离测试。
- 非目标：不重建已退役本地准入；不构建应用/发布/重启/DDL；不导入或删除历史未知归属包；不新增流水线、审批、台账或通用发布框架。
- 责任层：主机清理适配器负责目录/文件/进程/锁/保留；任务 Owner 宣告完成和构建来源，不由文件年龄猜测任务完成；不改 API/Web/Runtime 业务合同。
- 已读根 AGENTS、ops/orchestration/README、ops/maintenance 既有保留说明；共享 cyf-quick-iterate 中 Flow-only 口径按根 2026-11-06 规则覆盖，不改共享技能。

## 已确认审计

- /etc/crontab 每30分钟调用 /home/isp/bin/clear_disk.sh clean；源码 clear_disk.host.sh 与主机 SHA-256 相同 `da6ff37ea5b5d46f8c9063650c8f837a20e7d8195ab7f74883d2422c16ec9b7c`。
- 已装 rebuildable helper 与源码相同 `cef95677c461100daf73e4a438c403e7b14b7b7894b93d5fa539a5c13a71b661`；原登记仅支持完成任务的 node_modules，不处理本地最终包。
- 现有 Flow 下载仅数字 Run/package.tgz；deliverables/releases、任意本地任务目录不被通用包清理兜底覆盖。不能宣称“所有历史包已自动覆盖”。
- 2026-10-09后端构建打包156.492秒；加历史安装估算463.849秒，不是同批全程实测；endToEndRelease10m=NOT_MEASURED。证据沿用 evidence/backend-release-10m-20261009，不触发重复构建。

## 实现、自检与主机状态

待完成后补充实际结果；源码、维护工具安装、自动触发、删包及完整发布达标分别报告。

### 源码与验证（2026-11-06）

- 扩展既有 helper / completed-tasks 记录的可选 artifacts 字段；不新增台账/runner。Owner显式完成、包外证据保留、最终文件身份/摘要、每组件最近两批、既有24h与低空间条件，记录未知/锁忙保护；Runtime同时读取固定backup/current.json保护前版源码/制品绑定，API使用Owner从同批证据取得的application JAR摘要匹配回退。
- 回归：本地包/原缓存59项，Runtime使用候选safety模块41项，完整主机脚本83项，合计183项通过。日志见 evidence/local-build-retention-20261106/{tests,runtime-candidate-regression,shell-regression}.log。首轮fixture发现 lock循环局部变量遮蔽mode导致plan不再只读，修正为lock_mode后59项含plan零删除通过；只影响临时fixture，未在主机运行候选clean。
- 只读实况：API/Web/Runtime三种现行权威记录均能识别；主机目前没有completed-tasks登记，不擅自生成历史包清理声明。具体记录识别结果 current-record-readonly.json。
- 规则已重申600秒同批完整墙钟优化/验收目标，包含准备、测试、构建、打包、安装、健康/必要业务冒烟；排队/间隔不得隐藏。未执行应用构建/发布，完整发布仍NOT_MEASURED，不把156.492秒构建或463.849秒混合估算重标达标。
- 候选文件SHA与只含本任务维护工具改动的patch见同目录summary.json / maintenance-tools.patch；既有未提交内容没有整体提交/覆盖。

### 主机适配：待现有清理释放锁

- 18:40非阻塞取得既有host cleanup lock失败，写入前停止，实际helper/脚本仍为原值。读取确认18:30:03启动的原cron清理仍持锁（PID1784567，子进程du），未抢占、未取消、未清理锁。
- 尚未安装/启用本地包新逻辑，不能宣称下一轮自动任务已消费它；源码通过与主机安装分开。
- 下一步：原清理自然完成后，核对原helper/脚本SHA、保存原值，在同host lock下原子安装候选并readback。仅维护工具安装，不执行clean、不登记/删除历史包；下一次真实获授权发布再实测600秒目标。

## 历史清理与持久化闭环（2026-11-07）

按用户“先清理历史临时文件和备份文件，再完成闭环”执行。精确回收1,591,824,384 allocated bytes：2个过期API备份503,287,808、3个已废弃未发布构建中间JAR755,277,824、2个旧Web载荷及1个孤儿stage333,258,752。保留当前、回退、最新两份Web备份、数据库/Runtime/未知格式及包外证据；不是清空全部历史。

JDK已完整核验迁至`/opt/cyf/toolchains/dragonwell-21.0.11.0.11+10-GA`，缓存原子迁至`/home/isp/state/cyf-local-build/gradle-home`；当前API/回退/Web包字节一致镜像持久保存于`/home/isp/wsps/private-maintenance/cyf-local-archive-20261107-*`。历史安装record原路径不改写，仍绑定的内存盘原件保留。

现有维护工具已安装并回读，支持原生API schema4/Web schema2、完成包登记及组合输出组件子根；4个完成任务已进入原registry。维护隔离回归61+67+41+84=253项。原每30分钟cron实际入口已执行，清理末尾不再递归du长持锁；最终exit3准确表示容量仍低于5GiB、没有可删候选，非未知schema失败。持久化亦占用磁盘，当前仅约1GiB余量，下一批必须复核备份峰值，不能宣称磁盘问题完全消除。

当前策略、部署说明、工具README及保留规则已同步本轮状态。具体安装/清理/登记/验证见`docs/implementation/evidence/local-release-closure-20261107/`；版本化结果以`version-control.json`实际远端回读为准。本轮无新应用构建、部署、重启或Flow，不覆盖原435.314秒成绩，也不将它泛化为未来冷构建保证。
