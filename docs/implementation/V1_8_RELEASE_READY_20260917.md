# 1.8.0 发布分支就绪（未部署）

日期：2026-09-17。用户要求持续推进开发、达到分支冻结条件后创建release并通知；本轮不执行生产部署。

## 已完成

- 聚义厅桌面/手机横竖屏个人中心入口；可见文字、头像回退与离开保护。
- 个人中心、经济只读预览、聚义厅双向导航；刷新后重读当前身份，错误可重试，丢弃旧身份响应。
- 保留1.7 API完整基线，同时精确整合其他任务已经实现的配置/注册诊断热修复；不增加API/表/迁移/收费功能。

| 组件 | develop和release/1.8.0远端SHA | tree |
|---|---|---|
| API | `0b5cfe8cbcafcadca7dcef07874d6b397f0ab1e4` | `39df5045b8e644379b81bab01bd8d3f7f06c114a` |
| Web | `7099b176e06e2322c6a79f258a4ad74d6221c358` | `8648f749295ee2ef44dd0f379b86fa3cddbe4b46` |

上述两仓采用非force、仓内atomic push，远端readback一致。原release/1.7.0与codex/bugfix/1.7.0保留，脏primary checkout不reset、不改动他人文件。

## 验证与制品

- Web相关294/294，策略7/7；新空目录生产构建成功。
- 最终生产bundle Chromium38/38：桌面/移动端竖横布局、可见可点入口、反复往返、旋转、刷新/直达；API全mock，未访问生产。
- API相关118/118，bootJar成功；全模块历史compileTestJava债务未解决，不能宣称全量green。
- `build_origin=local_user_authorized`，Flow Run为空；没有伪造云效记录。
- API JAR SHA-256：`2b567012c614f811b33550712b4c6e30fbb4e9f477d5cb6229d5fb2c06caae11`。
- Web tar SHA-256：`e31f53971be0fe02f2efc8eb70f69d00657aa20885c80bca77dbad595b3e34ea`。
- 本机交付包：`/home/isp/wsps/cyf/deliverables/releases/v1.8.0-local-ready-20260917/`。包含readiness.json、远端回读、最终文件清单、制品、原失败及最终测试/截图证据、SHA256SUMS。

## 明确未完成/未操作

- 未生产安装/重启、未生产DML/迁移、未Provider调用、未开放经济写入或语音。
- 未真机/线上双真实身份/非空经济业务验收；部署后按授权账号补真实健康及导航回归，再通知用户验收。
- 其他任务仍在进行的生产登录/Agent注册问题不由本次分支freeze宣称闭环。
- 发布前重新核对实际运行版本、Owner、并行热修复及可恢复安装空间。磁盘在并行任务中波动；按新Web约106MB/API约221MB和实际副本复用测算，不用固定10G阈值。

本轮结论：**开发、相关自检、制品和远端release分支已完成；下一动作是按用户安排部署冻结制品，不在此记录冒称已经上线。**
