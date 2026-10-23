# 停止本轮回复：源码修复与云端核验

核对日期：2026-10-19。Owner：当前会话。任务：CHAT-STOP-FIX-20261019。

## 固定输入与结论

|组件|固定提交 / tree|正式证据|结果|
|---|---|---|---|
|API|`5aa8efc2462cd0dc1dce531bdbfccaa5cae390c6` / `dea4965743bc640939074d535edaae12fc62e554`|Flow5260799 / Run155|2397次执行：2302通过、95跳过、0失败错误；分层检查、fresh JAR、上传成功|
|Web|`7b0d2be8feb34a366403d7d728a91be625a42166` / `12319a5d082de1c0e4d9b85d173eac04d3af5782`|Flow4403172 / Run227|3049通过、2pending；Vite构建、代码扫描、上传成功|

两端均以受测精确提交快进组件develop，未发布生产；远端核验见本轮handoff。API候选包含此前密议requestRevision字符串解析修复。没有重新构建或把旧Run153当作新提交证据。

## 修复范围

- 后端：delta/final/recovery/cancel事件携带准确的turn state/stateVersion，使用十进制字符串；持久化成功后先更新投影再发事件；不覆盖question等其他资源的版本。不删除ACL、事务锁或expectedStateVersion校验。
- 前端：请求级取消去重，身份/会话/请求隔离；409只读原请求并给出明确提示；网络结果未知时只读核对、不自动重复POST；允许等版本终态幂等回执；读回终态后释放发送会话。
- 新增后端版本测试4/4、取消HTTP测试4/4、密议HTTP测试6/6通过；前端70项议事定向测试包含新取消边界，已纳入本次云端全量运行。
- **不包含**生产停止图标从工具栏移到输入区的接线；现有原型和规格已表达目标，不把这次composable修复说成全部UI完成。

## 失败归因及重验

- Run154：新增测试夹具误用setContextSnapshotId；按ChatTurnEntity实际字段改为setSnapshotId后固定新提交，再运行Run155。不跳过测试。
- Run226：3049测试通过、Vite成功，但原打包身份校验遗漏本次候选分支；仅把临时候选校验固定为本分支，保留commit/tree/Run与制品完整性校验后Run227通过。
- 两次终态后均按无活动Run/无配置冲突检查恢复原云端配置，并readback。最终摘要见api-config-restored.json、web-config-restored.json；未改线上服务、未重启、未写新生产测试数据。

## 证据边界 / 未完成

- API诊断摘要SHA-256：`152c7645adfe713c4731d82517128f74ce962bb8fc4b4d7762bdf5fdf1a0a609`，已解码重算；JAR日志SHA-256：`a18ab09a9579300222adfbb6c731db05292fc04d75c3073dc2da340dfec88e6f`。
- Web日志报告366个制品清单文件；helper摘要不是整包摘要。此次未独立下载两端制品，不宣称发布摘要闭包完成。Web日志返回截取片段，不宣称完整审阅所有日志；测试汇总及构建/上传终态已核对。
- 生产仍沿用上次两次409的失败基线。高频delta仍可能合法发生版本竞争，读回并不承诺下一次POST必成功；需版本化发布后用吴用真实验证CANCELLED、历史保留、下一轮发送及多turn边界。
- 本次仅完成源码候选验证与develop集成；发布授权、生产验收及整体界面优化仍未完成。
