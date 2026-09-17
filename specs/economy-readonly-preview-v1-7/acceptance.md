# 1.7 验收矩阵

状态：未验收、未发布。以下是待执行标准，不是PASS报告。

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
