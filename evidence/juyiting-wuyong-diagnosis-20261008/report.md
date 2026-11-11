# 吴用离线与 codex-ws-agent 版本核验

核验时间：2026-10-08 09:30–09:31 Asia/Shanghai。只读检查；未启动、重启、启用服务或升级部署。

## 当前直接核验
- JuyiHall.vue:1135 将 offline 显示为“出征”；不是 busy/办事。
- codex-ws-agent@wuyong-local.service: inactive/dead，MainPID=0，UnitFileState=disabled；当前 boot journal 无记录。
- cyf-agent-runtime-v1@wuyong.service: failed/failed，MainPID=0，enabled；这是独立 Runtime 服务，不等同于 websocket 客户端。
- codex-ws-agent.service: active/running，MainPID=2237，enabled。
- 吴用实例 current 指向 releases/20261005221604-1143943，provenance sourceCommit=4e70c4fc90aaf72ee6a1e58aae7703853af449f1。
- 共享客户端 current 指向 releases/20261007102637-2215064，provenance sourceCommit=f29c2ad3693229e14a7cd279cb86d9e7293166ff。
- git ls-remote origin refs/heads/develop 实时返回 5b71067f7bcbc7ca7f1076f5a9e10321b400785a。
- git rev-list --left-right --count f29c2ad...5b71067 返回 21 / 2：双方分叉，不能以 develop 直接覆盖共享版本。

## 本轮此前检查记录
- 吴用 profile 属于独立 wuyong-local 实例；共享实例仅配置卢俊义、林冲，不包含吴用。
- 当前主机 boot 始于 2026-10-08 07:52:40；disabled 实例未随本次启动恢复。无法由此证明最初离线时间或是谁停用了实例。
- Runtime 日志仅 generic runtime-v1-error，尚不能确定其失败根因。
- 已校验吴用56项、共享57项制品清单，均无哈希不符。
- develop 的两个新增提交为 ACK high-water checkpoint 与 durable legacy ACK cleanup；共享分支另有 typed CHAT/INSPECT/recovery 修复，不能丢弃。

## 结论及边界
吴用当前没有运行的 websocket 客户端，离线显示有实际进程证据；未重新登录业务页面，不将旧业务响应描述为本次实时 API 结果。安装与开发版本不统一，不能称功能已全部最新。下一步需限定吴用实例的恢复授权，并独立整合分叉功能、固定版本、通过正式发布流程部署验证；本报告不表示已修复或已升级。

## 继续排查（2026-10-08 09:34）
- 只读调用实际 Runtime 客户端 loadAuthorization（fetch 被禁止网络的替身替换）成功；manifest 校验成功，凭据文件权限0600、installationId匹配。未输出凭据，未发session/heartbeat POST。
- API日志在07:29:57.666记录开始优雅关闭；Runtime在07:30:19首次退出，07:30:21快速重启耗尽。时间相符，支持“后端退出期间网络请求失败引发Runtime退出”的推断，但客户端吞掉了具体异常，不能将推断当作已确认错误码。
- Runtime run循环未捕获session/heartbeat/flushAcks异常；systemd RestartSec默认100ms，6次快速重启后进入failed。API当前只读health返回UP，而Runtime未自行恢复。
- 吴用本地inbox扫描：pending目录5个、文件0；processing目录2个、文件0；recovery-required目录1个、文件0；execution-report-outbox除scope元数据外文件0；Runtime pending ACK为0。chat-ack-outbox仍有1个文件，尚不据此断言服务端不存在待投递任务。
- 仍未启动、启用或升级任何服务。修复方向为限于吴用实例的恢复、可恢复网络故障重连、脱敏错误分类与避免systemd快速重试耗尽；不改共享客户端、不伪造HEALTHY、不清空ACK/任务状态。

## 用户授权后的恢复（2026-10-08 09:35–09:36）
用户明确授权仅启动吴用独立客户端、恢复开机自启并核验。执行 systemctl enable --now codex-ws-agent@wuyong-local.service 成功。
- ExecStartPre配置校验成功；注册日志由pending_ack进入registered。
- 恢复后PID258538、active/running、enabled、NRestarts=0，09:36复核仍保持。
- 共享客户端PID2237保持不变；未操作独立Runtime v1服务，其仍failed。
- 未升级制品、未修改任务/ACK文件、未手动重放历史任务、未发布代码。
- 本次确认的是客户端进程及协议注册；尚未在认证业务页面独立验证“候命”显示，不将注册成功等同完整业务验收。

## 授权继续完成后的修复与发布
- 客户端以正常merge整合原共享分支f29c2ad的21项typed CHAT/INSPECT修复与develop5b71067的2项ACK修复，保留双方能力。解决payload清单/README/安装回归冲突，不覆盖原脏工作区。
- 发现HOME隔离测试使用未normalize的fixture，修正为生产normalizeProfile路径；不放松隔离断言。整合套件820PASS/10SKIP/0FAIL；最终metadata payload回归64PASS。
- Runtime Owner提交8cc6990：临时网络/HTTP408、429、5xx指数退避至60s；认证/rebind/TLS永久错误固定exit78，systemd不循环重启；停止可取消网络/等待，不重放业务。13项定向回归通过。
- 两个包均固定1.0.1，最终整合源码0d80e588be271891348e38b8892d9b9a9b0bb436/tree a1c58d192db3eeb58181f20f29346d49d6ab1403，已push任务分支。
- 认证浏览器原生操作：点将册吴用显示“候命”；详情为“正在厅中候令，可从悬赏榜点将”。见browser/06-wuyong-online-verified.json及png。未新建业务任务。
- Runtime只读GET installation返回ACTIVE，但lastHeartbeatAt仍1791415758963（旧值），不能用ACTIVE冒充本次恢复。
- Flow5264702 Run22在测试阶段失败，817PASS/3FAIL/10SKIP，未停止任何生产服务。归因：压缩包不是Git checkout，git archive权限导致源evidence group-writable，umask077使故意公开的fixture变私有；此外预查发现默认Node22与Runtime要求20不符。
- 修复发布输入而非跳过测试：固定Git bundle checkout，外层控制目录0700下以022运行临时fixture，正式状态恢复077；客户端用已安装Node22，Runtime精确/usr/bin/node20。原3失败定向3/3通过。新Run23执行相同源码的全量测试/制品/备份/迁移/部署。
- 独立真实子进程loopback故障夹具：一次连接中断、一次503后第三次session恢复并发出heartbeat，SIGTERM11ms退出0；不含真实身份/凭据，不请求生产。详见runtime-native-reconnect-fixture.json；不能当作生产断网演练。
