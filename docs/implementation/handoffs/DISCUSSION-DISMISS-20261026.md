# 议事临时工具收起（2026-10-26）

- Owner：当前聊天；范围：话头记录、＋设置、现有引用资料面板外点/Esc关闭；非目标：改变选材流程、发送、删除授权、录音生命周期或后端接口。
- 已读取根/Web AGENTS、ops/orchestration/README及接口规范 api/docs/interface-standard.md v1.4（2026-10-24）。
- 原Web工作区HEAD ca22ac2，原型脏改与上游重叠，不能安全快进；唯一必要隔离工作区 /home/isp/wsps/cyf-dismiss-20261026，分支 codex/juyiting-dismiss。
- 2026-10-26只读ls-remote基线 develop 45b0368436571b14cf5dfc7e7f800806f80d7df5，tree 6b2838d1e39bfb61454f02fb9311ccff0bdff2b4。延续办事5条及消息成果验收修复。不覆盖原工作区脏文件。
- 原型先行：唯一 web/prototypes/juyiting/interaction-completion.js 已有外点/Esc收起示例，本次补充输入/切换/焦点与子级确认边界，规格同路径 specs/prototype-spec.md；只迁移本次最小补丁，不提交原型其他Owner脏改。
- 最早验证：真实History/Composer jsdom；内部/触发/外部、Esc、删除确认、录音保留、资料关闭不写、卸载清理及前两项定向回归。轻量诊断非正式Flow证据。
- 不部署；不启动生产打包。线上版本未查询。定位/实现/验证/等待分项耗时未采集。

## 完成与集成

- Web源码 `7806f7656cc27c72906d5d36b30ac2fdab069341`，tree `590008a60b87bb962d6f42a7022883cc4ed7137c`；从45b0368快进push develop，2026-10-26 ls-remote回读一致。原Web工作区分支/HEAD及其他Owner原型脏内容不覆盖；本任务只同步已有原型上的最小交互补丁。
- History增加局部dismiss事件，外点/Esc收起；触发按钮和内部操作豁免，Esc恢复入口焦点，外点不抢焦点。删除确认/删除中阻止卸载；话头/身份/任务切换按既有安全作用域关闭旧列表。
- Composer的外点范围缩小到实际菜单/入口，不再把整个输入区当内部；引用资料同步支持关闭但不重置暂选/草稿。工具切换含键盘click，录音/转写必要控件继续可达；独立议事实例键盘事件不误关其他实例。
- 子级native/Varlet语义弹窗优先；隐藏弹窗不阻塞收起。保留已有HallVoiceControls子级Escape处理，不修改录音与发送生命周期、删除授权、资料写入及wire接口。
- 原型先更新唯一目录的既有script/规格并同步任务方案；复用预览HTTP200及JS语法检查通过。原型其他未提交依赖不整包引入组件提交。无新浏览器截图，不宣称PC/移动视觉实测或生产验收通过。

## 验证证据

- 新增 `tests/juyiting-transient-tools.test.js` **12项**：组合真实Chat/History/Composer，覆盖外点/输入框/Esc/内部/触发、键盘工具切换、引用关闭不写、录音可达、删除确认/删除中、子级弹窗/隐藏弹窗、多议事实例、作用域切换与卸载。
- 最终源码6个定向suite **91 passing**（transient-tools、composer-more-menu、chat-terminal-layout、bounty-inline-results、portrait-home、voice-conversation），日志 `discussion-dismiss-20261026/final-tests.log`。
- 前项办事5条回归（hall-overview、hall-overview-component）**42 passing**，`home-regression.log`。
- 较早同逻辑阶段6个suite **162 passing**（另含component-behavior、finalization-task-refresh），随后仅加closed-state早返回及调整新增模板属性顺序，并运行上述最终91+42项；不把162项冒充最终精确tree独立正式验证。日志 `targeted-tests.log`。初始新增测试有2项测试夹具断言错误（暴露属性代理和卸载后VTU事件缓存），已修正并全绿，初始输出保留。
- 三个改动SFC ESLint基线及候选均 **53 errors / 1 warning**，无新增；既有紧凑SVG属性等不在本任务全量格式化。`lint-baseline.json`、`lint.log`；`git diff --check`通过。
- 全部为本机低开销jsdom/静态定向诊断；未运行Flow、未生产打包、未部署、未改变线上状态，根gitlink不更新。正式验证待固定该commit由Flow4403172执行；发布须另有授权，保持同Run制品与600秒总时限，再独立核验线上关闭及触屏/焦点体验。
- 任务隔离worktree在push及证据保留后清理；分支/远端提交保留。根handoff/优化方案/模块知识为本地留存，未声明根仓提交。

## 用户追加部署授权（2026-10-26）

- 用户明确要求“现在部署”；仅授权本批Web，不修改/部署API或Runtime。
- 发布版本1.16.52：完整commit `8d716eab358c313b191f13744f2c221d51a5dbd6`，tree `f193ddf42d8ac2ba6ba834e1756db4dee8b7db7c`，是7806f76上仅package/lock升版，未改变功能源码；已快进push develop，未动原脏工作区/index。
- 发布前只读确认Web最近326终态SUCCESS、现网1.16.51，发布锁空闲、无在途Run；保存当时云端CI-only配置。复用前次受控同Run部署段、固定新commit/version/独立备份路径，现有安装器SHA不变。
- Flow4403172/327已返回真实Run ID并进入RUNNING，首次source.commint元数据为空，初始控制回执为UNKNOWN，不重复启动；等待固定源码日志/同Run manifest作为补充闭包。监控仅属本聊天Run，570秒触发受控取消以保留600秒终态余量，不取消其他Run。
- 本轮私有执行/原配置/制品及验证证据目录 `/home/isp/state/juyiting-ui-release-20261026/`。先前“未部署”保留为当时事实，最终状态以下续记为准。

## 发布完成（2026-10-26 13:55 +08:00核验）

- 最终版本 **Web1.16.52**，commit `8f77f4962b5cb80862115bbfd8b2a431fd0554f5`，tree `8e22bb470378e93b47b7c8d3c73a71d34794e669`；含本聊天三项UI修复。8d716ea仅升版；8f77f49仅修正旧共享绑定测试的目录替身，显式暴露refresh并新增“正式议事重读恰好刷新一次，其他模式不刷新”断言，产品源码与7806f76一致。已push develop并ls-remote回读。
- **Flow4403172/327 FAIL**：3364 passing / 2 pending / 1 failing。失败为既有共享绑定夹具未同步45b0368公开的refresh接口；部署作业INIT，线上未改。归因后修夹具，不删/跳过测试、不放宽保护，恢复原配置，再按新精确源码启动328；非相同输入盲重试。327的完整候选/输入/状态/日志保留私有run327子目录。
- **Flow4403172/328 SUCCESS**：正式发布profile全部 **3365 passing、0 failing、2 pending**（3367 registered、459 suites，报告duration51.48秒）；代码扫描、生产构建、同Run上传及安装全部成功。Flow createTime至终态updateTime149秒，控制面165秒内观察到终态，未达600秒上限，无取消。
- 同Run制品 **SHA-256 `ca7637c4f3622722a114874e72f6a0fb2c02a6d3f533d710fe7207e41a3c949c`**，109530150字节。读取Flow VMDeploy已下载的同Run归档，不二次打包/下载；manifest、source-commit/tree、packageVersion及Run ID均匹配，mochawesome报告0失败。
- 部署单 **71798391**：Success，一批一台Success/healthy；主机安装record `online_verified`，612个当前清单文件逐一SHA匹配。线上入口、/juyiting、入口JS/CSS、聚义厅懒加载JS/CSS等 **9项HTTP200且字节SHA匹配**。不是只凭入口200或文件名认定版本。
- 独立恢复备份 `/home/isp/baks/cyf-web-juyiting-ui-release-20261026/` 保存前版index/record；旧hash资产保留。既有安装器SHA、锁、完整性及可恢复发布路径不变。执行后已恢复原CI-only配置，readback SHA `0189ce8daf20d156f02fff89d859cd23afbfd3a63eafa0ce0f5cdf4992e0f47b` 一致，develop不因本次授权变为自动部署。
- 脱敏证据 `docs/implementation/handoffs/discussion-dismiss-20261026/release/verification.json`；执行详情 `/home/isp/state/juyiting-ui-release-20261026/`。线上验证是安装/公开资源闭包，**未登录逐一点击三项业务交互或取得本轮PC/移动视觉截图**，不冒充已完成真实业务体验验收。
- 未修改/部署API、Runtime，未操作其他聊天Run/进程。通过独立Git索引提交仅版本/夹具两次精确增量，不创建新worktree、不改变原脏工作区或其index；本任务临时索引及冗余语法候选已清理。根仓仍有其他Owner脏改、原Web checkout旧HEAD，根gitlink未擅自推进，根说明为本地保留。
