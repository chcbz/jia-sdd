# 验收范围

## 当前提交状态（2026-11-11 20:07，制品/迁移预演通过、整体未交付）

- 正式API制品c7c0f2d78d/1.1.48-SNAPSHOT：api-final-1，146项及layering通过，197.962秒。Web c453e08/1.16.134：web-final-2，101通过/2原pending，177.303秒；生产构建和包摘要通过，尚未安装。
- 额外迁移资源87ccfef032仅补首次费用报价5列升级SQL，不在上述c7c0包中，独立维护来源明确区分。schema-rehearsal-1按实际生产SHOW CREATE空结构执行11项迁移，16.597秒通过，报价结构与fresh DDL一致；生产报价表只读观察为0行，实际执行前须停writer后复核。所有生产迁移仍未执行。

### 已完成的前置链路（原19:48记录）

- API `6f1d07298a28e14ab6a758149235ecd842b5e0cd` / tree `f8b234ea6c2fd6d13ca1c79f7fecf347ead9e9ac`：`cutover-api-3` 12/12、无失败/错误/跳过，layering通过，107.361秒。真实命令入口→原账号/身份/安装MySQL查询→实际Runtime静态adopt→同事务零余额账户/免费租约/首次调度→原输入重放均已执行；原安装、绑定、投影和到期日不变，交易数0。原生executor/知识Provider是明确合成边界，不冒充生产WS/费用验收。
- 前置隔离上下文`cutover-api-2` 11/11通过（98.067秒），确认normal profile不注册维护图、专属上下文无业务worker/HTTP/schema写入。`cutover-api-1`的真实代理装配FAIL保留；修复沿生产class-based事务代理，不替换原身份服务。`transition-api-5`的65项、钱包/租期边界及layering证据仍保留，不代表生产迁移。
- Runtime 1.3.99 / bridge1.1.69，源码`7985667d1d73d3843d9f86dbc94f410a8ca520bd`，237/237；已安装到李逵固定app，PID335808，新进程connected/registered/ready与心跳ACK核验通过。attempt5启动校验失败并自动恢复旧程序；attempt6继承既有app根0700后成功，原FAIL未重标。本机现已同版本安装并核验吴用/林冲/卢俊义新PID心跳与ACK；后续控制配置后本机PID1816754、李逵PID344602。李逵mTLS真实跨机请求通过，错误scope及无客户端证书被拒绝，防火墙只放行API来源IP；本机新增卢俊义真实owner scope并逐scope验证。尚未核实扈三娘所在宿主。
- Web `c453e0898642b0aec80677df71c088f74563a349`：真实Vue/浏览器24项通过，含桌面/移动/窄屏、50/500文TRANSITION、无虚构付款和刷新不写入；HTTP/身份为合成fixture。最终Web制品见上；仍没有生产UI验收。
- 生产切换只读预演：`production-cutover-preview-1`使用已验证c7c0 JAR，4个真实安装主体身份/路由通过，25.140秒；输入及receipt固定，未apply/建租约/扣款。扈三娘无已验证控制端点明确排除，无安装关系不造租约。API客户端证书已私有安装、路由配置仍暂存未激活。
- **仍未完成：** 两种部署完整生命周期/真实混合链的最终验收、必要生产SQL/ES和API调度/收费/路由配置、扈三娘宿主核实、API/Web受控安装、真实Web/WS/资金/故障验收及集成收口。未执行生产租费迁移、实际扣费或付费模型turn。入口可运行和李逵在线不是整体上线。

证据根：`/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/`；切换命令回执在`cutover-api-3/operator-fixture/`，发布在`likui-release-attempt-6/`，浏览器在`web-transition-browser-2/`。具体此前失败及后续修复见既有handoff，不将历史FAIL改写为PASS。

## 历史提交状态（2026-11-11 16:42，本地/远程控制定向通过、整体未交付）

- API `c2f717dac45cb122192f8cedd0cb68f55fbe00fb` / tree `0f3f5cafb5e3aff4c27747c31e9f3811d55f6344`，Runtime `8e556e9f7611c69593e09a6fe486eb47554ebb2b`：`tls-api-3`真实执行99项，**97通过、2失败**，486.248秒，layering通过。实际Java→mTLS→Runtime静态探测/adopt/current/停止/证据/私有清理通过，缺客户端密钥及错误服务端身份被拒绝；应用28项和免费重整H2事务5项均通过。
- 未通过项是原本地UDS握手的精确字段断言（fixture新增remoteAddress:null）和静态清理第一次调用返回false。前者已改为只在TLS fixture返回该字段；后者未猜测为成功或超时，增加直接exchange异常/响应和Runtime安全阶段耗时诊断，保持原超时/清理断言。
- 修正候选API `897e5095800f7fc294b0858f04b2767a4954d654` / tree `0f6e6875110780d84ba03e3eff39f9a29d0dc7ea`，Runtime `bd73fe4`（测试fixture变更）：`tls-api-4` **29/29通过、0失败/错误/跳过、layering通过**，489.176秒（全部计入本次600秒）。实际Java TLS链8.793秒、原托管UDS链30.095秒、静态UDS链1.979秒。本地UDS同样增加选中hostId回显核对，避免错主机库存进入报价。静态首次清理本次CLEANED实测32.997ms，原false未复现；初轮无原因信息，不能反推成已证明的超时或重写原FAIL。此前通过的70项未重标为本候选完整验收。当前本任务无在途构建/测试。
- `tls-api-1`是任务源码pin未更新而在Gradle启动前被拒绝；`tls-api-2`是新增fixture缺Map引用而编译失败。原FAIL与归因保持，不能并入后续成功。每批独立600秒、串行、普通磁盘短tmp，无应用超时调整。
- API候选已接入可信host路由和Spring SSL bundles；李逵仍运行此前Runtime1.3.71、PID306359、没有hostingControlPath/TLS端点，未新增生产扣费/清理/发布。自部署50文计价与Web确认、两模式存量30天过渡/首次调度、legacy canonical ID重邀及最终迁移/发布/真实验收仍未完成。

## 先前子链状态（2026-11-11 16:08，Runtime端通过、整体未交付）

- API `b49120979dc04eec629a443fa20492932dea2358` / tree `ad0595efb45132b58887e5a3af5b29ee557db012`：`adoption-api-1` **62/62通过、0失败/错误/跳过、validateLayering通过**，356.945秒。包含实际Java→UDS→Runtime的静态adopt/current/停止/证据/私有清理、原托管UDS链，以及安装锁与免费重整无注册元数据；未生成最终JAR。原生注册/执行器和知识provider仍明确fixture。
- Runtime `2488e71dfb869572937eb0fc97fe364d563aea91` / tree `8de91ed2d655a87d3a3dc51d24d9b0fed73257d4`：`adoption-runtime-2` **232/232通过、0失败/取消/跳过**，124.130秒，依赖摘要前后一致；包含实际私有目录清理、同HOME重新邀请和旧关联失效。后续 `e54aa6c`只新增Java跨端静态fixture，已随上述API62项运行；未把前轮232项重标为新源码全量通过。
- Runtime远程控制候选1.3.98：`121efd99924846b7cc8d4116f731e5a5d58d2548` / tree `c29cd9bae595acbd519895ef717df095cb42dd87`，`tls-runtime-1` **235/235通过、0失败/取消/跳过/待办**，150.318秒。实际TLS双向认证和原UDS共享journal，Agent停止后宿主仍可回收证据；覆盖客户端缺证书/不可信证书、服务端身份不匹配、超大帧、私钥权限错误及启动失败清理。
- 后续`6ccbfcbb41cc26ecbd635cd66d56c5cbda4e796b` / tree `b6d47b9fad36c33ff2eaedde6a31252ec2f11bde`只补TLS配置边界测试与运维指南，`tls-runtime-2` **12/12通过**，9.426秒；含凭证不得放入Agent可写目录、别名和不安全CA权限。两批各核对582个Git blob及相同依赖摘要；第二批没有重标第一批为最终源码全量验收。使用本地临时证书，不是李逵远程实测。
- 存量身份入口 `cac049e991` 28项通过；续费套餐绑定 `0c583d6c77` 20项通过。证据分别为`existing-identity-api-1`、`renewal-plan-api-2/report-audit.json`；不改写后者原汇总误判FAIL。
- **剩余真实缺口**：API远程宿主路由与TLS客户端接线、自部署50文报价/确认与套餐路由、存量两种模式30天过渡租约和首次调度登记；随后生产DDL/ES mapping迁移、最终fresh制品/受控发布、真实Web/WS/钱款/故障与混合容量验收。
- 李逵本次仅已升级到已生产验证的Runtime1.3.71/bridge1.1.59，在线ready通过；未安装本轮1.3.98候选，未接入收费或执行真实清理。主任务没有新增生产扣费。
- 证据根仍为`/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/`；`adoption-runtime-1`保留原7项失败及归因，第二批才通过。当前无本任务在途构建/测试进程。

## 先前子集状态（2026-11-11 14:08，托管组合验证通过、整体未交付）

用户本轮两小时目标截止北京时间14:55；不是应用请求超时。仍需完整产品与上线证据，不能以测试通过替代交付。

| 范围 | 最新可核实结果 | 尚缺 |
|---|---|---|
| 托管关闭→重邀 | `closure-api-5`完整API/MySQL/UDS组合PASS：500文首费、停止/私有清理、旧租约关闭与安装撤销、保留技能、新报价550文/新关系ACTIVE及扣费、旧回执不影响新关系、账目平衡；分层通过 | `closure-api-6`已在默认60秒窗口重复通过全链，冷库存30019.752ms、后续2893.541ms。账户目录、executor注册、知识Provider仍为明确fixture，不是线上验收 |
| Runtime冷库存与完整性 | bba4f8b：去掉同次测量重复全量哈希，保留文件前后状态及实际执行身份核验；测量期间同size/mtime篡改有拒绝回归。固定source7组合135个唯一用例PASS，原生库存用例28.95秒 | 完整组合默认窗口现已通过；未安装，不承诺任何生产负载都低于该时长 |
| API线上基线 | f3a97a5224已合并当前部署cbeab0d8c5，避免回退已上线session/WS刷新修复 | 合并后实际执行101项全部通过（0失败/错误/跳过），含认证/WS/维护权限与真实Redis客户端失联接管；未生成最终JAR |
| 生产Redis与Memory | 有独占Redis/ES定向测试；本机Redis进程/监听已只读观察 | 只读INFO已确认Redis4.0.6单机master/无副本，生产JAR默认127.0.0.1:6379/db0；不等于故障接管验收。Memory生产mapping及数据库迁移未执行 |
| 未实现业务 | 平台托管首费、周期费、已有技能首费及维护账本有分层证据 | 自行部署50文完整生命周期、存量Agent收费切换仍未实现，不是改价格即可 |
| 交付 | 源码与原失败/成功证据保留 | 最终fresh包、受控安装、真实Web/WS/资金与故障验收未完成；没有新生产扣费或付费模型调用 |

证据目录：`/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/`。`closure-runtime-7`仍记134PASS/1SKIP的FAIL；同一源码和依赖的`closure-inventory-8`补跑全部6项后，组合记录为`closure-runtime-combined-acceptance-8.json`，不改写原失败。当前API回归记录为`closure-api-6/result.json`：101/101 PASS、分层通过、1866.891秒；API完整commit `f3a97a5224bf29f3f7a2761b2385e8690b888d45`、tree `f06853285388dc837abe29b460dd129e24ada96c`，Runtime完整commit `bba4f8b3913721bd6a2124b365b1477296bd645a`、tree `dd52728fec8636c47e7e664a5a858d320a0256c4`。

以下11:58记录保留为历史；不得据其将已通过的重邀组合再次列成同一个未修复故障，也不得把诊断窗口成功当默认窗口成功。

## 历史提交状态（2026-11-11 11:58，验收未通过、尚未上线）

本轮“去过度设计/临时旧路径”整改已提交代码，但未完成完整收费闭环，不能作为上线验收通过。

| 范围 | 已完成/可核实 | 未完成 |
|---|---|---|
| 去旧流程整改 | 删除旧托管文件开通状态机、publisher及无调用写DAO/Mapper；保留历史只读表/实体及现行投影通知。生产责任层不新增框架，复用同事务锁定绑定 | 最终应用JAR尚未产出；不把源码删除当部署完成 |
| 受影响API测试 | 121个独立单测/Mapper用例通过，报告及与最终候选未变输入已核对 | 不包含失败的组合生命周期用例 |
| Runtime测试 | e543c40候选61/61通过，87.993秒，依赖前后摘要不变 | 最终20e2b7c仅新增组合fixture安全时序日志；真实生产WS/Provider验收未完成 |
| 真实API/MySQL/UDS组合链 | 走到首次收费、旧关系停机/清理/关闭、保留技能后重新报价550文及确认 | 新关系未到ACTIVE，最终扣款/重新准入断言未通过；不得称完整闭环 |
| 统一调度/维护成本 | 持久领取、协调、CONTROL容量与已迁移消费者有分批证据；平台维护账本已有真实SQL验证 | 生产配置、Redis故障接管、ES迁移及真实混合负载未验收 |
| 其余收费及发布 | 规则已有记录 | 自部署50文、存量切换尚未接入；真实Web端到端、最终包、受控安装和线上资金验收未完成 |

**最后一轮明确失败，不是PASS。** `closure-api-4`：1个组合用例FAIL，分层检查已执行；fresh bootJar因前置用例失败未执行。原生库存实测首次60074.081ms、后续965.988ms，首次超过默认60000ms传输窗口；测试临时显式使用120000ms后走过报价，但不修改生产配置、不据此宣布性能问题解决。新的失败点是Java组合fixture的RuntimeHost未接`admitRelationship`（只读运行诊断为`undefined`），而真实RuntimeHost重新准入要求该适配器；不能用无条件成功stub绕过。

API候选 `71b8033dea9de91bdfcb470068e004b43d1e7bc1` / tree `bbe36b797a9c222fdba35e7afd1ece038b0ae51d`；生产整改在其父候选 `ed5010e882450222eb59814a68a16a4f9dc04b68`，后续仅组合测试窗口变化。Runtime测试候选 `20e2b7cf55a017a278c72e6df2ca7d785d319f87` / tree `6ae6292b619fdf45000f36caea048b38f19af75e`，本轮相对7a7089d仅测试fixture变更。

证据根：`/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/`。保留`closure-api-{1,2,3,4}`原始FAIL、`closure-runtime-2/result.json`、`closure-api-unchanged-unit-evidence.json`、`closure-readmission-wiring-diagnostic.json`及时序日志。账户目录、executor注册与知识Provider仍为明确合成边界，不冒充真实WS/付费模型验收。本轮未生产安装、迁移、真实扣费或付费模型调用。

下一步只补组合fixture的真实重新准入接线并验证，再定位默认窗口下的冷启动；不扩大业务改造、不放宽身份/资金/私有隔离断言。完整上线仍受上表独立余项阻塞。

## 验收要求

1. 同一scope/业务键重复登记不生成重复执行；不同租户、用户及节点任务互不串扰。
2. 业务事务回滚不留下余额待办；提交后进程立即崩溃/通知失败，重启或兜底仍能恢复。
3. 事件在领取前、执行中、完成并发时到达均不会丢；旧claim不能覆盖新revision或取消状态。
4. 两容器争抢、所有者宕机/失锁、旧执行者迟到，钱款只按同一期次扣一次，状态写回有正确归属。
5. 入账登记与续费并发，真实MySQL验证没有钱包/调度反向锁序；不能用Mock替代资金原子性。
6. 无待办不反复查询业务表；余额事件仅检查对应用户。记录真实查询计数，不承诺零Redis协调或零数据库兜底。
7. 最近dueAt提前、取消、批量到期与重启恢复均正确；慢处理器不阻塞时间唤醒。
8. 未知handler不丢任务；重复注册不静默覆盖；异步失败能查到真实结果；无通用参数绕过收费授权。
9. Memory等迁移项只有一个定时入口；旧TaskPlan创建/修改/提醒查询不受新表影响；灰度禁用继续生效。
10. 节点文件恢复不被另一容器消费；连接心跳和执行续租不误变全局单例。
11. 费用消费者另验证可用余额、自动续费排序、欠费恢复起租、锁定超15天移除竞争、旧事项继续及技能预占结算。

源码/selector/fixture和实际测试、安装证据沿handoff记录。已有基础/存储应用测试结果；没有生产迁移或发布结果。

## 已验证子集与未验证边界（2026-11-09）
- `ScheduledWorkStoreMySqlTest`：生产DDL/Mapper、实际租户插件、Spring事务，独占本机MySQL8.0.21测试实例；20项全部执行，无跳过；还覆盖提交后通知合并、回滚无通知、嵌套事务、通知失败不影响提交、最近期限、worker/未知handler与关闭语义。业务事实与登记同时提交/回滚、存储失败回滚业务事实、独立连接可在回调前登记、新事件保留、并发worker唯一领取、SKIP LOCKED不等待、并发事件合并、分区在LIMIT前生效、节点归属、接管后旧token拒绝、取消/改期优先、CAS、续租、禁止worker嵌入钱包事务、精确字符串键和索引/无CHECK均覆盖。
- 存储恢复测试是**重新创建store并接管数据库过期claim**，不是容器重启/Redis故障演练；并发是独立数据库连接，不声称已运行多个生产容器。
- 早期存储测试只用最小业务事实表；后续HostingRentRenewalMySqlTest已接入真实EconomyPostingService/租费服务/调度store验证同库事务和锁序，不代表关系交接/生产多容器故障验收完成。
- 首轮真实测试暴露重复租户解析导致锁定SQL语法错误；保留失败证据，限定新Mapper跳过重复改写后回归通过，旧Mapper公共隔离未改。
- 新增Redis双客户端6项、runner查询计数3项、手动执行边界2项、条件装配/灰度禁用3项；与原有core22和Task业务14项共70项。Redis失败无降级为注入异常测试；真实网络分区、容器宕机及混合慢任务负载仍未验收。
- 经济posting及旧hosting共43项H2事务测试，通过余额增加同步事件、重放不重复发、观察者登记失败回滚、非可用资金增加不触发。Agent订阅适配4项为mock调度接口/真实条件装配验证；后续真实钱包→调度→租约自动扣费MySQL15项已通过，详细范围和局限见下项。
- `HostingRentRenewalMySqlTest`15项验证生产DDL/catalog、真实发放与幂等重放、可用余额扣款、最早期限、不足不阻塞、同到期稳定排序、101项欠费后的可支付尾项、严格15天、FINISHING仍保留实例slot、失败同回滚、并发付款一次、并发入账锁序及分区；与适配4项/原资金43项同候选共62项零跳过。FINISHING只登记待办，没有关系解除或Runtime隔离验收。
- cron、旧任务切换、关系移除/私有交接和发布尚未完成。上述完整条目不能据此全部勾选。

准入候选c800400c3d的Agent租期门禁3项、授权54项、既有事项领取34项通过；同轮Chat源集编译失败，未执行派发/密议测试，失败记录保留。d06503d0c3已补现有测试辅助类及最近用户期限同事务登记/两个MySQL回归，尚未运行，不冒充最后候选已全面通过。


### 2026-11-11 双模式收费入口候选验证
API3fdfb9d724的54项覆盖两种mode共用真实HTTP信封/资金应用边界、缺省/null/free请求拒绝、50文套餐、原套餐续租、库存/主机类型变化、免费重整事务及lease.planId投影。Gradle257.117秒exit0/layering通过；外层driver exit143原因未明，原result保留，独立completion-audit核对全部XML及摘要，不宣称外层或发布通过。Webbf6d870定向51项及1440/390/320三视口18检查通过，包括报价类型不匹配禁确认、200文首费/50文周期及local确认字段；浏览器HTTP为合成fixture。证据：`/home/isp/state/cyf-local-build/tasks/task-scheduling-20261109/pricing-http-3/completion-audit.json`、`pricing-web-1/result.json`及`pricing-web-1/browser/result.json`。当前未迁移生产、未发布、未新增扣费，存量过渡/最终李逵全链仍待验收。
