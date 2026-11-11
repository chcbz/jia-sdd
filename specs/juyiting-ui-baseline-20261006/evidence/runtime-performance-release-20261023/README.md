# Runtime 1.2.8 上线与生产回归（2026-10-23）

## 结论与范围

Owner：当前会话，单Agent。授权：用户“部署并重新验证”。**Runtime已部署、三通道在线；图片两轮生成与选定成果验收可走通，但“基于上一版图片修改”的语义回归未通过。不是全部业务验收通过。** 未发布API/Web、未改Provider/身份配置，PDF按用户要求不验，事项517不重放、不修数据。

## 固定发布链

- Runtime **1.2.8**，isp-install commit `3c993e58033d901622c24126028199cdf4e2c76f`，tree `d502f8656fd876d1d671fd0bbe4f67062b75bcc7`；运行代码与已测`040991f180e54cdad818840bafb59d368320ae47`一致。
- Flow **5264702 / Run26 SUCCESS**，构建job541738448、部署job541738449、部署单71694237（一台Success/healthy）。临时Flow配置事后已恢复readback APPLIED，私有回执`/var/tmp/cyf-runtime-perf-release-20261023/ops-restore-result.json`。Run25因云镜像缺bubblewrap失败且未安装；补齐环境后Run26测试25通过、0失败、1显式skip。skip为需凭据完整native握手，不等于本轮生产图片流程跳过。
- 同Run制品SHA-256 `d13d2ad2fca8ac1c16d842d6cf08ece6fa60a591ba85d2251580a1cd09e3f718`；71项engine源文件+22项Runtime文件精确匹配Git。依赖锁未变；先核验现用4108项manifest，再复用Node/JS/Python依赖，不本机生产打包。云测试Node20.20.2、生产Node24.22.1；不能混为相同工具链。上一轮本机293通过/1skip证据见原性能handoff。
- 实体程序`/home/isp/apps/cyf-agent-runtime-v1/app/`；unit `cyf-agent-runtime-v1@unified.service`；PID1404284。最终manifest4110项，SHA `d9dd85d9eb861c94cadb6b92df5516417b7dc22442cb3a77a9e8d74396bb975e`。未启用旧版本目录或独立@wuyong服务。
- 17:18:43左右停服，17:23:42启动新PID；17:29:02完成三通道注册/ready/ACK核验。安装、通道健康和业务验收分层记录，`installation.json`的pending表示当时安装阶段，不覆盖历史。
- 完整停写未压缩tar备份+compare、旧程序归档及恢复说明位于`/home/isp/baks/cyf-agent-runtime-v1/20261023-performance/`。状态tar SHA `fc0313003d564bc61afbc9b8968581ea6c53880f5f4746058c0ed819815c92cb`。沿用原发布锁，身份/配置/unit不变；首次通道核验7份恢复记录摘要未变，既有2份RESULT_UNKNOWN未清理。恢复不能用旧DB覆盖新业务事实。

## 生产浏览器回归

ziyue测试账号，跨用户指派**吴用**；PC1440×1000、移动390×844。新事项**518**、会话**1760458007065**；只创建/指派一次，两轮议事分别仅发送一次。未把旧517当本轮样本。

| 核验 | 结果 | 证据/边界 |
| --- | --- | --- |
| 资料上传与选择 | PASS | JPEG上传后列表刷新且自动选中；移动预览可展开/收起 |
| 办事附件直接预览 | PASS | `mobile-home-direct-preview-loaded.png`，不是跳回选择资料 |
| 待点将返回列表 | PASS | `mobile-waiting-task-list-loaded.png`，518卡片加载 |
| 吴用在线、指派 | PASS | `mobile-task518-wuyong-selected.png` |
| 首轮蓝色→红色PNG | PASS（可见颜色、可交付） | 1175509字节，1254×1254，中心RGBA(252,2,1,255)；不是逐像素纯色证明 |
| 自然语言第二轮产生绿色PNG | PASS（执行/输出） | 1175931字节，1254×1254，中心RGBA(3,248,3,255)；`mobile-green-output-preview.png` |
| 在红色上一版基础上改绿 | **FAIL（语义/来源）** | 实际再次引用原始蓝图，`inputReceipts.sha256=a79877a9…959d`，不是红图SHA；typed outcome为ACTION_REQUEST+APPEND，`replaces=null`。两张图可生成不等于上一版改稿正确 |
| 选择绿色成果→正式验收 | PASS（含恢复路径） | finalization仅SUBMITTED/REVIEWING；后续review操作COMMITTED、任务COMPLETED v4、交付ACCEPTED v1；红图未选入正式交付 |
| 刷新后状态持久化 | PASS | 完整reload后办事显示518已完成，详情及事项列表一致；完成后的议事仅查看，无验收按钮 |

首轮CHAT `mmd-typed-request_fa9b65dfe93f9deac47cd1d47fbd0e11041810ee`，EXECUTE `1b9e9a5fb5e2e76084cbb6aeabab268e05165beb52e031b7117c101c7640a5e6`；红图SHA `81c65a18dc17a7b4ae45be97474455f8942fdd879d47ce11b24361dab354df38`。

二轮CHAT `mmd-typed-request_d307f0ba59286b4411fc064c790a7dcd02b313a5`，EXECUTE `4357f6c70b0e4bbaee7e1e34b18a1f46275f4e43a0fc345010955faab5a89486`；绿图SHA `d0a77bc89b4ab8657b98d501de36b5acc68b90faabbda60ba99040c20515454c`。

验收finalization `fin_36ed8cb44e423224f4389430b052965b4ed61193655898f5115af5e36b40adc5`；review `review_6ae19830448cd355c8ecfdac228038c8748cc4688e43e4542fcdc1f9021a605d`；delivery `finalization_delivery_1fab887c5eee0b7b1fcc1d9817beb33b32dcf78519126e0b7f05ee1510e077d4`。

测试Driver的默认写保护拦截了首次自动`POST /agent/tasks/518/delivery-review-operations`，并非线上接口故障。先通过UI“查询原验收”确认404不存在，再一次性放行原路径、UI“继续原验收”，真实回执成功。未重发finalization、未手工改数据库。故本轮验证了正常提交与中断恢复闭环，不冒称无中断的一键验收。弹窗保留拦截产生的错误，关闭后刷新无该错误。

## 性能与仍存问题

- 本轮两次生产图片执行均完成，未再复现旧canary的隔离启动超时；三通道在业务后仍ready且ACK新鲜。**没有同输入前后端到端性能对照，不宣称整体耗时下降比例。** 首轮仍经历数分钟排队，启动时原生历史恢复读回占用chat lane；本任务未主动重放历史请求。
- 17:55—17:57日志存在重复`ACTION_SELECTION_INVALID`，日志只带profile无requestId，当前两轮已完成，不能把此日志强行归因到518。未清理历史记录/绕过校验；该恢复/错误归属问题保留待定向定位，不作为本次性能改动已修证据。
- 明确待修：上一版成果引用/改稿语义（本轮已证实）；517旧状态闭合；精确尺寸/逐像素纯色履约（本轮不承诺256×256，中心采样也非精确RGB）。没有扩修到API/Web或Provider策略。
- 来源偏差后续应先固定“上一版成果”输入身份与语义契约，再用包含可辨识局部图案的样本检验保留上一版内容；不得用纯色最终颜色正确掩盖原图引用错误，不直接给所有改稿强制APPEND/REPLACE。
- Python成果重开、技能安装辅助、Git子进程、资料解析/图片衍生、初始化探测、队列扫描仍是已识别未重构的同步路径；本次不是整个Runtime彻底异步化。

## 证据与隐私

本目录保留云测试、发布摘要、93源文件核验、通道、仅518的业务响应与UI截图。生产截图仅测试账号/测试资料；无密码、JWT、Provider凭据。完整私有状态/云配置/浏览器profile留私有运维目录，不入库。响应捕获有一次进程中断（首轮完成后至二轮处理中），后续重新挂接取权威GET和实际结果，不伪称连续完整网络抓包。截图加载态不作为PASS。
