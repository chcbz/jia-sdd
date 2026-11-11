# 文件回收 412 只读诊断（2026-10-16，Asia/Shanghai）

## 基线与范围
- 唯一 Owner：当前 Codex 聊天。目标为调查，不修改业务源码、网关配置或用户文件，不执行生产写请求、部署、重启。
- Web HEAD `2c8d6703eead623f555029341101cb688b9d448a`；实际查询远端 develop `421f628c245b83466cafb70510ff69188180bdee`（差异为本聊天前项未推送的议事输入框改动）。
- API HEAD/实际查询远端 develop `fc399976710f5b724916013926be2cbff899af8c`。
- 已读根项目规则、web 规则、编排工具索引；API 仅源码只读，未运行 Gradle。接口基线 api/docs/interface-standard.md v1.2（2026-10-14）。未核对生产包源码摘要，不以本地源码冒充生产版本。

## 证据
1. `/home/isp/hosts/cyf/api/logs/root.log`：13:24:42、13:25:22 的 POST `/agent/personal-workspace/files/{fileId}/trash` 均 412；13:26:41 PATCH 文件同为 412。
2. `/home/isp/logs/access/api.chaoyoufan.cn.log`：相应回收之前详情 GET、usage GET 为 200。日志不含实际 ETag/If-Match，不据此断言哪一个版本值发生冲突。
3. 当前网关配置 `/home/isp/apps/nginx/conf/nginx.conf`：gzip on、gzip_min_length 1000、gzip_types 含 application/json；API /agent 代理未关闭继承压缩。
4. 使用主机同一 nginx 二进制，独立临时配置/仅回环监听/合成上游响应隔离复现：不压缩为 `"diagnostic-file:1"`，gzip 后为 `W/"diagnostic-file:1"`。全部自有临时进程已停止，未修改生产 nginx。见 nginx-reproduction.json。
5. 当前前端 usePersonalWorkspace.select 保存响应 etag；mutate 将其原样发为 If-Match。后端 PersonalWorkspaceWriteService.requireMatch 仅接受精确 `"fileId:metadataRevision"`。
6. 真实前端 composable + 合成 API 按后端实际校验条件复现：强 ETag 成功；同 revision 的弱 ETag 返回与截图一致错误；旧详情 ETag + 新 usage revision 也返回同错。见 adapter-reproduction.log。此为诊断，不是正式 Flow/API 测试或线上写入验证。

## 结论与边界
- 已确认线上写入被版本前置条件 412 拒绝，不是直接因为存在一个关联引用；trash 在确认引用且版本匹配时允许回收。
- 高度怀疑 gzip 弱化 ETag → 前端原样回传 → 后端严格校验失败；隔离环境完整重现，且同时解释回收/重命名失败。缺少实际失败请求头，尚不能将其判定为截图请求的唯一已证实根因。
- 独立确认的第二问题：usage 只刷新引用影响版本，不刷新详情 ETag；确认失败也不清除旧 trashUsage，真实并发更新后重复点击仍会使用旧状态。
- 修复方向：使用文件元数据契约的乐观锁版本构造写入前置条件，避免直接复用压缩表示的弱 ETag；回收前固定一致的详情/引用快照，412 后刷新并要求重新确认，不自动重试删除、不放宽后端版本/ACL校验。覆盖强/弱 ETag、真实并发变化、重命名/恢复与跨文件确认状态。
- 下一步：按以上边界实施前端修复与定向回归，再走正式 Flow 验证/版本化发布。本次仅诊断，未修改或发布业务代码。
