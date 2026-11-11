# 议事预览移除下载入口（2026-10-26）

- Owner当前聊天；用户明确议事“预览”无下载按钮。只移除会话媒体预览的下载入口及误导下载文案，保留图片/音频预览、错误重试、关闭/焦点恢复、身份切换取消。百宝箱/资料管理下载不动，不新增下载权限校验或接口。
- 继承 MATERIAL-PICKER-PARITY-20261026.md 的工作区、固定源码、公共规范v1.4和未部署边界，复用唯一 `/home/isp/wsps/cyf-input-switch`，不新增隔离。
- 原型先行：唯一原型prototype.js的preview按chat页面省略下载footer，其他资料/工作空间预览仍保留；C09补充议事例外，覆盖旧“预览窗口下载保留”的冲突描述。
- 最早验证：真实HallMessageMedia的图片/音频/不支持文件预览无下载按钮，重试、关闭恢复焦点、身份切换释放资源；已有页面原型编译、成果及多媒体提示测试。本机定向不等于Flow或线上/真实设备验收。

## 实现与定向核验（2026-10-26）

- 集成候选Web `1eceae1dce92159f8ca81a1226d060823b10e3fd` / tree `43fa061941ca521d183235fb90ecec61a36fbbfa`；输入切换前置commit经rebase为`e6b3827`。已保留并发develop `7749a78`的技能管理改动和原型规格追加；不覆盖原Web脏工作区。
- 13组定向本机回归163 passing / 0 failing（集成后源码，28秒）；涵盖真实Composer/Voice/Chat/Picker组合、固定版本关联/取消/范围暂存/失败恢复/身份切换、终态、预览无下载/音频nodownload/错误重试/焦点恢复及既有需求资料链路。完整日志和源码摘要见`material-picker-parity-20261026/integrated-regression.log`与`verification.json`。
- 原型JS语法、git diff --check通过，既有18786预览HTTP200。目标ESLint既有错误保留，基线/候选规则计数无新增；不宣称全量lint通过。尚未真实PC/手机浏览器逐项体验验收，也未运行Flow/生产构建或部署。定位/实现/等待分段耗时未采集。
- 共享选材器额外28项本机回归通过（35秒，含手机预览切换/返回、PC自动预览、上传未知结果核对、身份切换），本次独立选择器合计191项通过。已push并readback组件develop `1eceae1dce92159f8ca81a1226d060823b10e3fd`；本聊天没有触发Flow或部署。保存必要证据后清理本任务隔离worktree/node_modules软链，原Web脏工作区及他人工作区不动。

## 用户追加部署授权（2026-10-26）

- 用户明确要求“现在部署”；仅发布本批Web，API/Runtime不在范围。
- 候选Web1.16.54，commit `cbd8f2d43b42a38b5314c4749ad9b05564031176` / tree `c6064d039857e8f43329c6909bd5eb74373322f1`，仅在功能源码1eceae1上更新package/lock版本。独立临时Git索引提交并push develop、远端readback一致，不创建新worktree、不改变旧脏工作区/index。
- 查询时现网1.16.53 / 7749a78，Flow329终态SUCCESS、无在途Run，Web部署锁空闲，现行安装器SHA未变。候选复用同Run部署适配器，独立备份路径`/home/isp/baks/cyf-web-juyiting-input-material-release-20261026`；保存CI-only原配置，部署后恢复。私有证据`/home/isp/state/juyiting-input-material-release-20261026/`。
- 保留全套release profile测试/构建/扫描/摘要/锁/可恢复安装；Run总时限600秒，沿用570秒受控取消留出终态余量，只监控/取消本聊天新Run。线上健康和资源核验在Run终态后执行，不挂外部等待。

## 本批发布完成（2026-10-26 15:22 +08:00）

- Web **1.16.54** / commit `cbd8f2d43b42a38b5314c4749ad9b05564031176` / tree `c6064d039857e8f43329c6909bd5eb74373322f1`，Flow **4403172/330 SUCCESS**；源码来源终态API已返回并与同Run manifest一致。扫描、全套release profile测试/构建及同Run安装均成功，3390 passing / 0 failures / 2 pending。
- Flow createTime `2026-10-26T15:16:38+08:00` 至终态updateTime `2026-10-26T15:19:50+08:00` 共 **192秒**，低于600秒。监控终态观察约204秒（从本机请求时间计），不以作业时长冒充Run总时长。部署单 **71807860**，1/1批、目标主机Success/healthy；API/Runtime未部署。
- 同Run制品SHA-256 `0d7a42ebd21c9c2aa14ef99aa29d4d8abfb08280d5f9a561b30df1147b8b13b1`；612份安装文件与manifest一致，线上首页、/juyiting及入口/聚义厅JS/CSS共9项HTTP200且逐字节摘要匹配。核验时间 `2026-10-26T07:21:55.385266+00:00`。这不是登录后PC/移动逐项业务体验验收。
- 备份 `/home/isp/baks/cyf-web-juyiting-input-material-release-20261026`；CI-only配置已恢复并readback SHA `0189ce8daf20d156f02fff89d859cd23afbfd3a63eafa0ce0f5cdf4992e0f47b`，不将本次授权延伸为develop自动部署。
- 脱敏证据：`docs/implementation/handoffs/material-picker-parity-20261026/release/verification.json`；私有控制面/归档证据仍在本任务state目录。实现阶段“未部署”是历史状态，不改写其原始验证记录。重复“议事答复”的去重尚未实现，不属于此次已发布修复。
- 原Web脏checkout/index及根gitlink未强推或覆盖；临时版本索引已清理，无本任务残留worktree。定位/实现分项耗时未采集。
