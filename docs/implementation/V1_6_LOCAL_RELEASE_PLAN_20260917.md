# 2026-09-17 本地验证与 release 分支发布安排

用户最新指令：云效暂时不可用，后续继续采用本地部署；允许先合入 develop，达到上线条件后，从验证过的 develop 提交创建 release 分支发布。本安排覆盖此前“云端验证通过才合入”和“云效唯一构建”规定，直至用户明确恢复云效。不是跳过测试，也不授权生产数据变更、付费 Provider 或默认开启语音。

## 当前结论（12:51）

**API/Web已发布并完成线上readback**，两组件健康、Web入口资源摘要一致，发布/lifecycle锁已释放。最终报告见`docs/implementation/V1_6_LOCAL_RELEASE_RESULT_20260917.md`；不可变结果`/home/isp/wsps/cyf/deliverables/releases/v1.6.0-local-20260917/release-outcome.json`。下面按时间保留实施历史，不表示仍在等待。生产语音Provider激活/付费/设备验收仍未执行。

## 执行顺序

1. 各组件 Owner 自检后非覆盖式合入组件 develop，核对远端 SHA；不操作脏主工作区。
2. 在干净隔离工作区做本地相关回归与生产构建。Gradle 仍必须经 orchestrator 和全局 Gradle 锁执行；锁只等待，不抢占。对实际磁盘占用做容量核算，不加无依据固定预留。
3. 回归和构建成功后，分别从验证过的 API/Web develop SHA 创建 `release/1.6.0`（若已存在且不同则不覆盖，改用带日期的明确新分支）。这不是目录复制，也不随 develop 后续提交移动。
4. 发布清单绑定两组件各自 commit/tree、测试报告和本地产物 SHA-256，明确 `build_origin=local_user_authorized`，不得伪造 Flow Run 或云端成功。
5. 按当前宿主实际安装路径、精确进程身份和发布互斥进行可恢复安装；API 健康后再切 Web，保留当前回退产物。新失败必须先归因，不盲目重启。
6. 线上核验成功才标“已发布”。语音生产总开关和 Provider 默认保持现状，不把代码发布视为真实语音激活验收。

## 09:53 已执行

- Web develop：`c5fe7484b455843f6e9beeb49573fcc54e729043`，tree `28bc296d73e183459cb6ba4d37bc8d1c31bf1638`。从旧 develop fast-forward，25 项本地定向自检已有证据。
- API develop：`ab7ba3f610edb4bf9ec91f8124ee1cc254dfc821`，tree `472fab9c370e4e249a861c41f7e85fdfef72ec3c`。保留 Persona Catalog 先行修复，从旧 develop fast-forward。
- 两仓推送成功，并已 ls-remote readback。无 force push、无重置主目录、未创建 release 分支或部署。
- 两现有 Flow 已核对仍无 deploy；无需恢复云效才继续推进。原 Run85/Run116 失败证据保留，不改写为成功。
- 09:49 首次磁盘观测可用 0；稍后读回约 843 MiB。依赖共享目录也已消失。先核对可回收内容和实际制品/构建需求，再做本地验证，不读取或删除其他任务证据目录。

## 10:29 本地回归整改（尚未发布）

- Web 首轮完整 Mocha：2079 passing / 47 failing / 2 pending，另 56 个因前置失败 skipped；不能标全量通过。6 个成果验证/W11失败由 `9fa5e8b691c7261d99c817a448fd10bffd2ac00b` 修复，相关两文件 77 passing；其余集中于真实 Chromium 启动环境、Git clone、E14基准溯源。E14正在真实重采，不改哈希冒充通过。
- API 原 95 个编译错误已消除：`cfc21e4a` 修复 JDK HttpHeaders，`77d092df99bea8e30241627b85a40e064ef7ec72` 集成9个旧chat测试的tenant作用域签名修正。第三次执行已通过 compileTestJava，阻塞于本机离线缓存缺少固定版本 embedded-redis7.4.1，尚无断言结果；已归因，第四次允许配置仓库解析缺失依赖。测试仍使用隔离H2/自有Redis，不访问生产。
- 仅清理已完成任务 PERF-W03/PERF-W04/JY-SESSION-WEB 的可再生依赖并无损压缩已关闭日志；未删除源码、证据、在线及回退制品。磁盘空间持续有并发变化，构建/安装前按实际需求重算。
- 本任务未改动在线进程；发现其他API发布活动，因此发布前需重新确认线上精确归属与 release 锁，不复用旧PID判断。
- 本轮证据目录：`/var/tmp/cyf-v1-6-local-release-20260917`。release分支尚未创建，验证未完成，不宣称ready/released。

## 10:44 线上并发版本保护

读取规范部署记录发现线上已由另一任务更新至 API `e95ecfad0570834648be8cf3d2cd350b2f2fe9e8`（schema validator与owner作用域对齐），JAR `001d054f5ce220c885d2f699bc91c5f422dff0c93fb427985b2daf95b5c064e3`。该提交尚不是当前 `develop ab7ba3f6` 的祖先；不能发布旧候选覆盖这项恢复。已发送只告警协调，待当前测试自然结束后把恢复提交非覆盖式集成，纳入最终验证/制品清单。未操作其他任务的进程或证据目录。

## 12:13 通过项与最后收尾

- API最终集成 `a8e9170873062165176626775d66c92dfc2e7a1a` / tree `7ed64de0a3519b18b14f1ea8fe82463fa0993679` 已推送develop，包含已在线的e95ecfad恢复，未丢失其他任务修复。
- API锁内本地验证：voice/chat **146/146**、独立定向schema **5/5**、public-artifact-verifier **64/64**，均0失败/0skip；bootJar成功。不是整个API多模块全量测试。制品221386227 bytes，SHA-256 `82ef8e26fe7745a9a6a01d83560ddd2d7dd7846aea1425b2c0ac89ec4f2714fb`。
- Web第二次全量 **2185 PASS / 1 FAIL / 2原有pending / 0 skipped**。最后1项是跨本机browser路径的历史manifest字节比较，并非像素/功能失败。`74420db`修正测试：仍要求所有PNG/SVG与冻结基线字节一致，JSON只允许真实浏览器路径及其推导manifest ID变化，并要求两次fresh生成的所有文件完全一致。未伪造原launcher溯源；49/49相关测试通过，现执行最终全量及生产构建。
- 归属协调：已成功写conflict-alert；应用消息工具返回不再支持当前入口，跨任务消息未送达。只读快照中“修复登录认证失败问题”仍active，因此生产生命周期交接仍需确认，不将提醒写入等同对方ACK。
- 当前本任务没有创建release分支、部署或启用语音。release准备将绑定上列真实本地证据，不能写Flow成功。

## 12:29 本地就绪、分支冻结与运行权交接

- Web最终全量 **2186 PASS / 0 FAIL / 2原有pending / 0 skipped**，Vite生产构建成功；两个pending为原有小程序入口/方向合同，不计为通过。生成声明文件未产生受控文件改动。
- 组件远端develop与新建`release/1.6.0`已逐一readback：API `a8e9170873062165176626775d66c92dfc2e7a1a` / tree `7ed64de0a3519b18b14f1ea8fe82463fa0993679`；Web `74420db2c82fb2f5dee673f337c13bb546d53f93` / tree `4e4b4924ea7bb3a26b649726424f3ae2b81a4202`。未force、未覆盖旧release。
- 冻结输入 `/home/isp/wsps/cyf/deliverables/releases/v1.6.0-local-20260917/release-input.json`；双制品、metadata、SHA侧车均0444。Web tar SHA `d8c5c0778821aaf37996cdc42906665a3cf9ad932485755d0ceab3075d462cc9`，dist tree SHA `acb84f6600445c66b43506a443b36db4b0dd3d1dd87019119a44524995932b2d`。联合verify及API/Web dry-run均PASS。
- 原API恢复任务只读快照已是idle/turn completed；不是交接消息ACK。主控已指定Shannon为本次runtime Owner，授权只在发布锁内核验规范API PID/start_ticks/JAR符合后接管。旧进程仍为1672765，健康UP，无生命周期在途；主控不操作进程。
- 容量按旧API备份+新API暂存计算峰值 **442777600 bytes**，无任意预留。仅清理自身成功API可再生build子目录及与immutable archive逐文件一致的Web dist，回收后观测可用约500MB；所有结果、源码、在线与回退件保留。安装前还需实时重算。
- 此时仍**未部署**。执行Owner正在处理标准入口的锁内旧runtime精确校验及等待锁语义；不得以准备完成冒充上线，不启用Provider。

## 12:43 API已上线、Web暂存前归因

- API规范发布已成功：PID **1759469** / start_ticks **3119227686**，JAR SHA仍`82ef8e26...`；canonical launcher实际健康等待47秒后UP，已保留checksummed旧JAR及发布记录。不是仅dry-run成功。
- 为不改动已密封工具，runtime Owner生成任务私有审计入口，只将原单次nonblocking锁替换为阻塞锁+锁内旧runtime精确检查，其余安装/恢复逻辑不变。入口及diff/guard/policy摘要见`/var/tmp/cyf-v1-6-local-release-20260917/runtime-entry/runtime-entry-manifest.json`；不得把原工具摘要冒充私有入口摘要。
- Web第一次锁内预检发现launcher相关活动，**在任何Web变更前停止**；Owner正在区分真实生命周期与只读命令匹配。API无需重启。
- 并发占用曾令磁盘从约247MiB降至35MB，后自行回落。主控另对已合入release的sender-name工作树仅清理独立node_modules（无symlink consumers、进程cwd/fd，源码与证据保留），回收254271488 bytes；12:42观测可用505126912 bytes。实际Web新暂存约106643456 bytes，Owner重新锁内核验再推进，不删除当前/回退制品。
- 跨任务发送消息仍不可用，未送达，不当作ACK；已记录conflict-alert，未改动foreign ledger/进程。
