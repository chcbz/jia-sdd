# DISCUSSION-FEEDBACK-20261023

- Owner：本聊天；用户“继续”授权四项反馈的排查、原型与源码修复/验证，不部署、不重启、不重放生产请求、不调用付费模型。
- 已读取根/前端AGENTS、ops/orchestration/README.md、cyf-quick-iterate、Flow技能；CYF根2026-10-22规则覆盖共享技能旧自动发布口径。接口规范：api/docs/interface-standard.md，2026-10-14冻结版；本任务不放宽身份、资料授权、幂等或未知结果恢复。
- Web主checkout：codex/juyiting-ui-workflow，9dbd132e8bc25119c0532cbed672ab7fa4a214b3 / tree adacb21c069236c728ecd494f425210495153ee5，已有无关原型/文档改动，保留。
- 2026-10-23查询fetch远端Web develop=638084d26ec9a193240566bf45b33602cef8e0e0；独立源码worktree=/home/isp/wsps/worktrees/discussion-feedback-web-20261023，branch=codex/discussion-feedback-20261023。API本地94b4c8a5e5b1402ef44097b5a337a75431a0ec1b，远端先前只读查询b0735f57a7b454fa7a6fb9886fa3914131986779，不当成本任务受测候选。
- Runtime当前安装记录1.2.6 / 7dd120f5d3a61559ebf4347aa63b638f7e6a4153，程序固定app/。本任务只读运行记录，不修改生产文件/状态/锁；未部署1.2.7。
- 目标：成功点将不再常驻恢复黄框，异常恢复保留；话头/更多面板外部点击与Esc收起、互斥、不抢焦点/丢草稿；议事资料入口复用已确认原型共享选择器，不删资料范围语义；关联吴用具体失败请求并修复确定性故障。
- 原型：仍在web/prototypes/juyiting原有文件做最小补丁，不覆盖其他任务脏改动；先验证原型，再修改产品。任务方案增量回写optimization/spec.md。
- 最早验证：Vue SFC编译加定向轻量Mocha DOM测试（弹层边界/键盘/草稿、终态、资料固定版本、点将恢复）；不本机全量测试或生产构建。正式Web验证走Flow4403172，源码与Run绑定；无部署授权。
- 验收：原型PC/390/320交互；新增行为真实组件定向回归；Runtime安全合成fixture、不以真实生产请求重放代测；正式Flow结果单独记录。
- 定位发现：事项516、会话1760458007017，13:55和15:12发送的原请求均进入RECOVERY_REQUIRED，原因为ACTION_SELECTION_INVALID。可信dispatch给image-edit声明仅PNG/JPEG、恰好1份；可用资料实际为GIF（后续GIF+AVIF）。资料可上传/模型可看不等于编辑技能接受该格式。完整私有记录保留原路径，不复制用户上下文入仓。
- 定位/实现/验证/等待耗时：未汇总；开发完成和发布等待分开。当前未宣称修复或上线。

## 用户追问后的归因纠正

2026-10-23继续核对10月22日提交0e96676：不仅原生读图放开，image-edit技能包也已从1.0.0升级1.1.0，接受PNG/JPEG/WebP/GIF/BMP/TIFF/HEIC/HEIF/AVIF，image-provider已接规范化。因此不能将旧包限制认作当前产品规则，更不能只收紧模型选择掩盖升级漏项。固定源码候选包已为1.1.0（app下没有该源码toolchain路径，不推定携带该包），但吴用codex-home实际安装包仍1.0.0；原请求availableActions绑定旧包摘要/版本，故拒绝GIF。下一动作：沿已有技能发布/安装/激活链路只读核对1.1.0为何未落到吴用，保留原授权/安装摘要，不手改已安装manifest。先前模型schema收紧方向暂停，不能替代技能版本一致性修复。
