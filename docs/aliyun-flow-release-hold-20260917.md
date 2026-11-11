> **2026-09-17 最新覆盖指令**：云效不可用期间允许先合 develop，再本地测试/构建，达到上线条件后从精确提交创建 release 分支本地发布；不等待云效。见 `docs/implementation/V1_6_LOCAL_RELEASE_PLAN_20260917.md`。历史 Flow 失败与部署暂停记录保留，不作为本地发布禁令。

# 2026-09-17：统一上线前暂停自动部署

用户最新要求：继续完成 1.6.0，达到上线条件后合入 develop；后续另行统一安排上线。本记录优先于此前自动部署/夜间自动发布规则，不改变质量与身份隔离要求。

## 已执行的控制面变更

北京时间 09:06，原有 `4403172 / cyf-web-release` 与 `5260799 / cyf-api-release` 均只保留 cloud_ci 阶段。没有新增流水线。

- 源仓库、develop push 触发、云端测试/扫描/构建/上传未变。
- 只删除 deploy 阶段，保存前值、固定候选 SHA、核对无活动 Run、单次 UpdatePipeline、readback 成功。
- Web 生效 canonical SHA-256：`31c486ab65001337ddaa5977f39f9f5edc0494f35a0eea900dbcb757ba815908`。
- API 生效 canonical SHA-256：`1af23b526688c49f8fb1d9d65f5c6c35e698b9168886edf823ac7f48216f7fc8`。
- 本操作未启动 Run、未取消其他作业，未构建、部署、切换 flags、重启 API 或调用付费语音服务。
- 既有定时控制器只启动这两条 Flow；按当前配置运行也无 deploy 阶段。未操作定时器/进程。

控制面私有前值/候选及回执：`/var/tmp/cyf-v1-6-readiness-20260917.jYZRGu/`；目录 0700，YAML/回执 0600。完整 YAML 可能含连接配置，不复制到公开文档。

## 后续规则

1. 合入不等于发布；正式测试未执行或失败的候选不得标记“已满足上线条件”。
2. 统一上线需用户重新安排；届时重新核对现有配置和待发 exact SHA/制品，再恢复必要部署阶段。不得直接用旧自动发布模板覆盖此次暂停。
3. 本轮最新历史 Web Run115/API Run83 均 FAIL，作业日志为空；只能报告未执行成功，不能凭空日志证明当前额度已恢复或具体根因。
4. 本地定向自检不代替正式云端验证；云端受阻时保留独立候选与测试证据，不擅自本地重建发布。

## 09:15–09:25：候选分支正式验证准备

在保持无 deploy 阶段的前提下增加本任务两个精确候选分支准入，API 测试增加 `cn.jia.chat.voice.*` selector 并按真实 branch 生成来源证明。初次 readback canonical SHA-256：Web `26a3426aaf18a8e13d0527df9ab64c16897e917109c8d83add9b5a7b72cd6424`；API `1eb952083b912f0cb65e3054ca762f5484c50d79f375174239984b7004749e4c`。

09:24 只读复核发现 API 被其他控制面依次加入 `bugfix/agent-catalog-roster-20260917`，随后将 source branch/filter 临时改到该分支；本任务没有覆盖。观测 canonical SHA-256 `5b77b950facac8fc1d5f4bdc6a0c0b186de75d497d5697c187c8ae263e0f1fc0`，仍仅 cloud_ci。对应 Run84 为其他任务且 FAIL，不作为语音候选证据。配置和源码在 Start 前不匹配时，本任务不发起请求。

Web 单次 Start 返回 code=-1，无 Run ID；截至本次分页 reconciliation 未发现新 Run，结果待归因，不盲目重发。私有目录保留启动上下文/结果及 readback；没有运行时副作用。

## 09:36：实际 CI-only Run 与最新生效配置

在 source 默认分支仍为 develop、无活动 Run 的基础上，仅把 `branchesFilter` 放宽为 develop 或各自 exact 语音候选分支，解决服务端明确返回的过滤拒绝。保存前值、固定候选、readback 均完成；未恢复 deploy。

- API canonical SHA-256 `f5e349f744c45b39f9c9d984537f0748d3580aba354e594fe89e988e3a518c8d`，Run85 已创建且分支匹配；FAIL，无测试/制品。
- Web canonical SHA-256 `425f28e502b4c96126ea957273fa3fccb6fc9ec2369ea2565ed3584efd89bec3`，Run116 已创建且分支匹配；FAIL，无测试/制品。
- 两个 Run 的源码 SHA 返回未知、作业日志空且 more=false；不得把“分支匹配”当作 checkout 验证。当前平台根因仍未暴露；不擅自认定为额度，不重复启动。
- 后续准备合入前需重新读取最新远端 develop 和流水线配置；并发更改不可覆盖。统一上线之前始终保持无 deploy，用户安排上线后再按实际最新配置恢复。
