# 1.7 验收矩阵

状态（2026-09-17 18:47 CST）：已部署，授权12表修复后本轮API40/40及Chromium15/15通过，可交用户验收；用户最终回执待补。以下为完整验收标准，不能把本轮单账号/空业务数据范围扩大为每项全覆盖。

完整版本交付要求每个纳入功能至少有隔离fixture成功路径及线上认证读取证据；合法空目录/无租约可以为空，不能让全部卡片均不可用却宣称1.7完成。缺表/缺数据阻碍业务验收时保持任务未完成，不擅自DML或静默缩减范围。

1. 新开关开、老交易/安装/收费开关关：用户可进入新页；新API无需开启老交易gate；陌生身份不自动获得scope。
2. 用户A/B、同tenant不同client、同client不同actor：余额/流水各自独立；Agent状态/租约跨owner统一404；目录不跨tenant/client。覆盖case/trailing-space/prefix/legacy0。
3. 连续刷新所有读取和多次试算，隔离fixture中账户/账本/托管/订单/报价/安装意图/outbox快照无写入；publisher/provisioner/Provider mock零调用。readOnly事务注解不代替断言。
4. 未开户可正确读零但不创建账户；DB错误显示不可用不显示假零。流水分页不重复游标/越权；不把历史流水标成模拟。
5. 试算输入边界、long溢出、duplicate JSON key、unknown field、cached-input分离、expected>worst、重复请求确定性。与既有计算器相同输入结果一致，响应不含quoteId、charged=false、persisted=false、示例费率来源明确。
6. 技能无商品显示空；目录与版本状态过滤、权限/价格字符串正确；客户端不出现购买/安装按钮、也不调用旧quote/purchase；无seed。
7. 有权益无可靠安装证据显示未确认；离线不当作安装失败，历史ACK不当作当前健康；Agent切换丢弃旧响应。
8. 托管local不适用；server无租约不假开通；有效参考方案与实际租约分开，未配置/缺表不是0元；不开通/续费/重整。
9. 登出/换用户/换client后立即清空，迟到响应不串号；不读写交易journal，不自动重放历史订单；协议畸形关闭预览功能但不影响聊天。
10. Web相关既有钱包/技能/租金、悬赏、成果、阅读、移动端与API ACL回归；横竖屏可滚动、详情关闭正常；性能慢仅观测，不以无依据deadline取消请求。
11. 部署证据：exact API/Web commit/tree、测试selector/fixture摘要、制品hash、build_origin=local_user_authorized、冻结release/1.7.0、健康及认证新页/读API验证；不包含真实扣款/生产DML或付费探针。

用户最终只需：登录查看钱包→试算预算→浏览技能权限→选择自己的Agent看证据状态→查看租金说明，再换另一个账号确认隔离。技术测试与发布由Owner先完成，不要求用户代做后端测试。


## 2026-09-17 源码/构建验收补充（不是线上验收）

API `9aaf2a31`：完整新增preview26、scope/catalog/schema12、制品安全64均通过；bootJar成功。Web `7c49029`：全量2195通过/2既有pending/0失败，policy7通过，生产构建成功。九类契约静态对齐，MockMvc/Spring事务、实际H2 SQL、Vue组件和异步隔离均有执行证据。前后端已合远端develop并冻结release/1.7.0。

矩阵1–10已有相应源码/隔离fixture证据，不等于各项线上认证读取均已完成；真实移动设备、生产MySQL和双身份上线读取仍待部署后验证。矩阵11仅制品/exact分支部分完成，健康与生产新页部分未执行。默认agent全量测试仍有历史编译债，因此仅声明约定changed-scope API验证，不声明全API通过。详见`docs/implementation/V1_7_RELEASE_READY_20260917.md`及本机交付包。

## 2026-09-17 发布后认证回归

API/Web已部署健康；预览wallet/ledger/catalog/Agent skills真实503，整体未通过。试算、租约/参考方案、既有目录/roster/典籍只读验证通过。浏览器横竖屏可滚动；第二身份/另一client及非空成果夹具尚无线上完成证据，不伪报全功能通过。详见`docs/implementation/V1_7_LOCAL_RELEASE_RESULT_20260917.md`，待有界修复与回归后再通知用户验收。

18:22归因：生产缺基础5表+技能市场7表，需明确生产DDL授权后补齐；不是要求用户先验收503。源码/JAR不变，回归仍blocked。另2张托管表缺失单列，当前配置/local成功不代替server租约正例。最小12表未执行候选见发布结果文档。

## 2026-09-17 18:47 授权修复后回归（最新）

用户明确授权精确12表新增DDL，已执行并核对canonical结构。API40/40、真实Chromium15/15通过，原wallet/ledger/catalog/Agent skills503解除；12张经济表回归前后行数均0，未重启/重新发布/启用交易或语音。通知用户可以开始经济只读预览验收，未替用户确认最终验收。

矩阵11本轮源码/制品/安装/健康/认证读取证据齐备。矩阵1–10保留源码/fixture覆盖并增加单授权账号在线空钱包/空目录/4自有Agent/纯试算/配置参考/local租约、相关旧功能与触控横竖屏仿真证据；双真实账号/另一client、非空商品与成果fixture、server租约和真机不冒称已测。另2张hosting表仍缺失、不属于已授权12表；后续涉及server路径时需先另行补齐。详见发布结果最新版，首次失败/比较器别名/触控模拟归因不抹除。
