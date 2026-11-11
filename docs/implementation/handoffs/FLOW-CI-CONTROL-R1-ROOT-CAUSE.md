# FLOW-CI-CONTROL：停止写请求后的有界诊断方案

2026-09-09。用户授权实施云效迁移；此阶段不含生产执行。

| 失败 | 确认根因/边界 | 修复/下一步 |
| --- | --- | --- |
| 本地 bootstrap 构造 SyntaxError | 单行嵌套 Python mapping 漏闭合；未写文件/请求 API | 已拆分 source/step/job 映射，JSON roundtrip PASS |
| 一次 CreatePipeline 返回 1209300 | 2026-09-09T09:15:36Z 开始；未保留错误正文，不能确定服务端根因 | 17:19 完整列举组织仍只有原两条，未发现新建同名流水线；不自动重发 |

账本已由 orchestrator fail 进入 blocked_root_cause。只读查阅官方 CreatePipeline 与 YAML source/job 文档确认：content 文档示例是直接 YAML，source gitee 有效，不提供 triggerEvents 默认不自动触发，旧组织支持 public/cn-beijing 默认环境。

R2 是一次新的、需独立审批的最小诊断请求，而非原请求盲重试：使用人工可审阅 YAML（不是 JSON 子集）、仅默认环境 Command 步骤，去除 JavaBuild/指定容器/规格/JDK 等可选维度。命令只打印无副作用文本并 exit73。配置无部署、无源码事件触发、无启动请求。不能宣称这些变更已证明服务端根因。

独立 reviewer 需审核 `docs/implementation/plans/FLOW-CI-20260909-bootstrap-r2.yaml`。批准后主控通过 authorize-remediation 解锁一次 CreatePipeline；创建前重新完整列举同名流水线，若出现同名或不确定则停止。下一次调用保留脱敏 code/message/requestId 以及请求前后时点，原始 exception/headers 不落盘。任何错误保持可诊断状态、不自动重试；成功后只读核对 sources/events、完整作业结构、无实际 Run，再等待完整构建脚本独立验收。

证据：`docs/implementation/plans/FLOW-CI-20260909-create.json`；本方案是准备记录，不是第二执行账本。

独立 Reviewer Raman (`01a08578-b014-78b0-ad28-ac9397bc08ad`) 对 R2 最小创建诊断 ACCEPT P0/P1/P2=0/0/0；仅允许一次 CreatePipeline，不允许运行。主控按用户本轮实施授权接受该边界。

## R2 实际结果及归因

2026-09-09 17:25:35 +08:00，单次请求仍返回 `1209300`，现已捕获明确服务端原因：`sources.cyf_api.certificate.serviceConnection` 指向的服务连接 `149709` 不存在。请求 ID：`01A0857C-A7B6-55B8-B0E6-AAA7F093A29B`。因此 R2 已确认的云端阻塞是旧配置服务连接引用无法用于新 YAML 编译；R1 错误码相同但原正文缺失，不追溯补造其根因。不能据此归咎于 JDK、JSON 子集或内存。未请求运行。

下一步仅先验证不携带 Git 凭证能否读取目标公共仓库。如果成功，拟使用官方支持的通用 `git` source、去掉 serviceConnection，无需迁移或创建凭证；仍无 triggerEvents、无运行、无部署。修改后的 R3 必须独立复核，且创建前再次完整查重。若仓库匿名不可读，则不尝试绕过认证，转为核对可用服务连接。

17:27 匿名 Git 查询（credential.helper 清空、askpass 禁用，且未配置 HTTP extraheader/url rewrite）实际成功读到 develop=`97ae8ef12c0a0306a40a04017f44139e1ca27823`。R3 仅把 source type gitee 改为 git 并删除 certificate，其余 R2 字节不变；不运行。首轮真正构建仍计划固定原6267，不能因分支移动自动换候选。

R3 独立 Raman ACCEPT P0/P1/P2=0/0/0；准确配置 SHA-256 `43539361e09465d3715726568eaaed77677399a23e81913605141b6614ca3731`，仅批准一次创建、禁止运行。主控接受此有界修复。

## R3 已成功创建（未运行）

2026-09-09 17:33:04 +08:00，新流水线 `cyf-api-kit-ci` / `5256653` 创建成功；只读 GetPipeline 回读 generic git、develop、无 triggerEvents、仅 fail-closed Command；ListPipelineRuns 返回0且无下一页。完整创建回执在 `docs/implementation/plans/FLOW-CI-20260909-create-r3.json`。旧两条未修改。R2 的服务连接阻塞已通过无凭证公共源替代解决；不代表完整CI或生产迁移完成。
