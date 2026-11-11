# 停止回复专项发布核验（2026-10-19）

## 发布与覆盖边界
- API 1.16.9：commit `5aa8efc2462cd0dc1dce531bdbfccaa5cae390c6`，tree `dea4965743bc640939074d535edaae12fc62e554`，Flow5260799/156成功；2302通过、95跳过、0失败/错误。安装JAR与同Run制品一致，健康UP。
- Web 1.16.10：commit `bca42d2ea65d65255d1a5b6efdaefb9674b0e32d`，tree `d1d643eed1ad9f5c781ed3d315a06046f8ee1250`，Flow4403172/230成功；3053通过、2pending、0失败。366个安装文件匹配；浏览器16个已加载资源与安装清单摘要/大小全部一致（browser/loaded-assets-verification.json）。
- 两端临时Flow配置已恢复并回读。仅停止回复、版本传播和密议报文修复上线，不代表全量原型优化上线；历史“未上线”记录保留为当时状态。

## 已通过的真实业务核验
使用吴用、未使用李逵。密议conversation1760458005622：字符串requestRevision请求正常回复，无原400。
停止请求`1405a316-ab55-432a-a835-f79f457d0037`第一次遇409后只查询权威状态，用户显式再次点击后200/CANCELLED，历史保留、输入框恢复并获焦；下一请求`4abfea51-7818-4947-a8bd-5da9a030a3c1`正常完成，回复“停止后继续发送成功”。按钮桌面/移动端44×44、SVG20×20。证据见browser/native-stop-*、after-stop-ready.*、next-send-completed-*。

## 未通过/未闭环
1. 正式事项467创建、指定吴用、初次回复完成；conversation1760458006508后续两个不同问题均返回“收到。”，界面未展示对应后续用户消息。请求`mmd-typed-request_bbdc4805a5cf19306c8799850509bd1dae00e799`及`mmd-typed-request_da1899c5c4075c4c690c9cd52b9f93840cde9ff9`的typed-outcome均READY/ANSWER，后者assistantMessageId1858653。不是仅凭界面猜测；但尚未定位到持久化、调度上下文、Runtime或展示层。证据browser/formal-followup-residual.*及response-2672849.316.json。正式议事停止尚未成功实测，完整验收链路不得标通过。
2. 长流请求曾进入RECOVERY_REQUIRED，reason `DELTA_GAP_EXPECTED_318_GOT_319`；随后停止成功不等于序列缺口已修复。应独立定位生产者序列、传输重放和消费处理，不放宽连续性/版本校验掩盖异常。
3. 首次点将被诊断脚本写保护拦截，后按原操作幂等继续完成；此拦截不是生产缺陷。初次错误健康地址亦不是生产故障。

## 后续代码级核对入口
固定以上源码，从ChatTypedDiscussionAdmissionService（command.content→input）、ChatDeliberationService（用户消息持久化、dispatch快照、acceptDelta）逐层核对task467两条请求；对照实际Runtime输入后再确定修复归属。禁止盲目重发测试、伪造完成或将本次部署扩展成其他UI全量上线。

结论：专项版本发布完成、密议停止闭环通过；正式事项后续交互异常及长流序列缺口待修，整体业务核对未完成。
