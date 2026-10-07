# 2026-10-07 源码交付与服务端验证证据

- `component-remotes.json`、`root-source-remote-receipt.json`：源码交付精确远端SHA；Root8d77bcd为源码交付提交，不是未来证据更新提交。回执中的running_isolated_environment仅描述当时状态，当前以server-validation-status.json为准。
- `source-delivery-check.{cjs,json}` / `sddw-verify-attempt4.log`：提交/tree/远端/pins及局部证据一致性检查，不运行服务端应用测试，不证明整体验收。
- `server-validation-status.json`：最新BLOCKED状态；`ssh-session-observation.log`保留前次认证成功后session open超时，`ssh-resume-readonly-20261007.log`保留本次连接超时。不能把认证、连接或session open成功混为远端命令执行。
- `server-comprehensive*.sh` / `environment.gradle`：原尝试控制脚本，保留失败与环境修复过程；远端原始attempt日志因SSH阻断尚未取回。attempt5的退出码/XML与清理未经确认。
- `server-runtime.sh` / `runtime-driver.py` / `run-browser-server.mjs`：仅准备、未运行，不是Runtime/browser结果。

## 重新执行前必须修正的控制面绑定

不要直接重跑这些历史脚本：runtime脚本仍检查attempt3/api-result.json，而attempt3失败；attempt2–5摘要Python仍从evidence根目录读取/写入而不是attempt目录。创建新的尝试，在真实完成的回归记录、fresh XML、实际退出码和exact source binding核实后再接Runtime/browser。原尝试脚本不静默覆盖。

SSH恢复后先只读核当前parent/cwd/argv与任务独占datadir，不能凭旧PID停止进程；不重启生产、不杀其他任务、不改认证/host检查。全程共享Gradle锁、串行构建。84业务用例保持not_run/evidence=null，无生产部署、任职/上架激活或付费模型授权。
