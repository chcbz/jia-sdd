# CYF 版本化部署与发布安排

更新：2026-10-06，时区 `Asia/Shanghai`。本文件替代旧 develop 自动/分时发布规则。

## 当前规则

- develop 仅开发集成与云端测试/构建，不自动部署；不按午夜定时任务发布最新 develop。
- 前后端统一版本化部署：明确版本与精确 commit，在 Flow 内测试、构建、生成同 Run 制品、部署并核验在线状态。
- 发布时机与触发方式按具体版本安排，不沿用后端每日 00:00、前端大版本 00:30 或 patch/minor 自动立即部署的旧规则；不新增未经确认的固定时刻或审批门槛。
- 复用 `5260799`、`4403172`，发布互斥等待、不抢占或取消其他 Run。具体构建、授权与证据要求见 `docs/aliyun-flow-cicd-strategy.md`。

## 历史与执行状态

- 2026-09-14 的时段/版本分类与 timer 安装记录仅为历史证据：`docs/aliyun-flow-release-schedule-activation-20260914.json`。
- 2026-09-17 暂停部署与本地例外记录不恢复旧自动发布；前端本地构建例外已被 2026-10-02 Flow 指令覆盖。
- 2026-10-06 经用户授权，两个旧 timer 已 disabled/inactive，无下一触发时刻；保留原 unit/控制脚本作恢复参考，不自动调用。前后端当前 Flow 均无部署阶段；证据见 `docs/aliyun-flow-versioned-deployment-switch-20261006.json`。版本化适配器已通过 `5264702 / Run13` 安装，移除午夜 intent 规则；运维配置已恢复。本次未执行应用版本部署。适配器契约与迁移证据见 `docs/aliyun-flow-cicd-strategy.md`、`docs/aliyun-flow-versioned-adapter-migration-20261006.json`。
