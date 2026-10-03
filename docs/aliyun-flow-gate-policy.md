# Flow 门禁依据与精简（2026-09-13）

用户指令：**把没有依据的检查去掉，后面遇到问题了，有依据再增加。** 历史脚本常量、重复文档和“测试证明常量生效”都不能替代依据。

## 本次删除

- 安装器的固定 5GiB 额外预留，以及启动器的默认 5GiB 磁盘/1GiB 可用内存硬门槛。资源指标仅输出观测值。
- 固定压缩包、解压体积、单成员/清单大小和 JAR 条目数等未经测算的上限。
- 因发布锁被占用而立即失败、或等待 60 秒后失败。保留互斥与锁顺序，排队后再次核对是否已被更新 Run 超越。
- 停止请求后的固定 60 秒自动强杀、启动等待超过 20 分钟自动判败。等待真实进程退出或健康；进程提前退出立即报错，Flow 作业提供取消出口，不以年龄代替失败证据。

## 保留及依据

- 云端测试、精确 commit/tree、同 Run 制品及线上核验：用户明确要求。
- 制品摘要、来源、路径/权限、进程身份、端口归属：防止发布错误字节、越界写入或操作其他进程。
- 停机前按实际解压字节和回退副本大小检查可用空间；不足会使必要写入无法完成，不加固定运行预留。
- 备份、原子替换、持久化状态与恢复：处理已经开始的部署中断，不将此扩展为日常独立审查或手工审批。
- 健康与功能验收分开。HTTP 200/health UP 不代表登录成功。

## 后续增加规则

先记录实际问题及证据，再增加能针对该问题的最小检查；数值须有测量和推导，不以“保险起见”自设阻断项。调整等待行为不代表可以假报成功：没有健康证明就保持运行中/未验收。

当前维护源：
- `ops/ci/aliyun-flow/host/cyf-api-flow-deploy`
- `ops/ci/aliyun-flow/host/cyf-api-flow-install`
- `ops/ci/aliyun-flow/host/cyf-api-kit`（本次将现行生命周期脚本纳入版本管理）

验证：`python3 -m unittest discover -s ops/ci/aliyun-flow/tests -p 'test_api*.py' -v`。这些是隔离临时目录中的控制面测试，不调用生产生命周期，不替代应用 Flow 回归。

## 2026-10-03 已证实的监控/发布锁反序

API1.13.66发布已实际复现：monitor持monitor.lock调用canonical status等待release锁，而deploy持release锁调用monitor CLI，造成互等；此前CLI `75 / monitor_lock_busy`还被误判为应用失败并回退健康实例。证据见`specs/juyiting-multimedia-deliberation/integration-evidence-20260928/release-1.13.66/`。

所有monitor CLI（包括status）必须放在release锁外：维护Owner先pause/status确认maintenance与无in-flight，再取发布/生命周期锁，内部仅做marker与精确CAS、安装、健康/归属检查；释放发布锁后才做status/resume/readback。明确的锁忙只表示等待，不新增任意超时，也不得以无限等待掩盖锁反序；不抢占foreign进程。此次仅精确自有FD解环是有据恢复，不应作为日常安装步骤。
