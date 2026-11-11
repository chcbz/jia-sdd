# Run40 部署与启动细分（2026-09-13）

流水线5260799，源码`564e50fa6bb4889d6f0b7221de57b4c22116a810`。本报告只读追溯，不是重新运行实验。所有时间为北京时间。

**表格是相邻可证实里程碑之间的墙钟时间，不是每个函数独占耗时。** 日志没有记录的函数时长保留未知。

## 部署13分18秒：可连续对账的区间

| 开始 | 结束 | 秒 | 区间工作 | 证据边界 |
| --- | --- | ---: | --- | --- |
| 13:02:58.000 | 13:03:11.000 | 13.000 | 部署作业启动、下发和下载完成 | API与下载完成日志 |
| 13:03:11.000 | 13:03:53.413 | 42.413 | 下载后准备：受控包、Flow/源码/回执/JAR校验，到自动授权前值备份 | 备份文件名和mtime佐证；不是函数计时 |
| 13:03:53.413 | 13:04:28.000 | 34.587 | 自动授权收尾、重复下载副本处理及installer解包验证，到安装事务STAMP | 安装器把STAMP放在候选解包/身份验证之后；前一里程碑不是installer精确入口 |
| 13:04:28.000 | 13:04:49.262 | 21.262 | 旧JAR摘要、准备记录及回退JAR复制，到备份最后数据写入 | 备份文件名STAMP与mtime；mtime不代表fsync完成 |
| 13:04:49.262 | 13:05:10.250 | 20.988 | 备份持久化收尾、停止旧进程、替换JAR、启动前JRE/权限校验及启动 | 首次JVM GC时间戳；其中停止进程日志为4s，其余无单独计时 |
| 13:05:10.250 | 13:05:21.408 | 11.158 | JVM早期引导到Spring内部计时起点 | 起点由Started计时反推 |
| 13:05:21.408 | 13:13:43.359 | 501.951 | Spring启动 | 框架报告501.951s |
| 13:13:43.359 | 13:14:49.000 | 65.641 | 启动Runner/健康等待/启动稳定核验及首次status前置，到第一次ps采样 | ps lstart+etime反推，秒级近似；13:13:58仍有main线程启动日志 |
| 13:14:49.000 | 13:15:37.000 | 48.000 | 第一次status剩余检查、finalize候选摘要、第二次status前置，到第二次ps采样 | ps lstart+etime反推，秒级近似，不是一次health耗时 |
| 13:15:37.000 | 13:16:00.000 | 23.000 | 第二次status剩余检查、消费自动授权、安装完成记录持久化、命令收尾 | 结束有部署日志时间戳 |
| 13:16:00.000 | 13:16:16.000 | 16.000 | Flow执行结果收集、机器与作业状态结束 | 机器结束13:16:02，作业结束13:16:16 |

下载后至首次JVM日志119.250s；Started后至命令结束136.641s；两个完整status的ps采样约在13:14:49和13:15:37，相隔48s。不是首次status严格耗时48s。

## Spring 501.951秒：里程碑区间

| 开始 | 结束 | 秒 | 从 | 到 |
| --- | --- | ---: | --- | --- |
| 13:05:21.408 | 13:05:32.316 | 10.908 | Spring计时起点，由Started耗时反推 | Starting JiaApplication |
| 13:05:32.316 | 13:06:36.372 | 64.056 | Starting JiaApplication | Spring Data扫描开始 |
| 13:06:36.372 | 13:06:39.312 | 2.940 | Spring Data扫描开始 | JDBC/LDAP/Redis仓库扫描结束 |
| 13:06:39.312 | 13:06:48.344 | 9.032 | JDBC/LDAP/Redis仓库扫描结束 | 首条重复Mapper告警 |
| 13:06:48.344 | 13:06:51.272 | 2.928 | 首条重复Mapper告警 | 最后一条重复Mapper告警 |
| 13:06:51.272 | 13:07:40.382 | 49.110 | 最后一条重复Mapper告警 | WebApplicationContext初始化里程碑 |
| 13:07:40.382 | 13:08:38.321 | 57.939 | WebApplicationContext初始化里程碑 | ChatClient MCP禁用确认 |
| 13:08:38.321 | 13:09:25.323 | 47.002 | ChatClient MCP禁用确认 | Redisson版本日志 |
| 13:09:25.323 | 13:09:43.290 | 17.967 | Redisson版本日志 | Redisson连接初始化完成日志 |
| 13:09:43.290 | 13:10:00.388 | 17.098 | Redisson连接初始化完成日志 | Hikari Starting |
| 13:10:00.388 | 13:10:10.295 | 9.907 | Hikari Starting | Hikari Start completed |
| 13:10:10.295 | 13:11:08.260 | 57.965 | Hikari Start completed | MyBatis insert注入检查日志 |
| 13:11:08.260 | 13:11:42.271 | 34.011 | MyBatis insert注入检查日志 | Camunda事务隔离检查日志 |
| 13:11:42.271 | 13:12:34.367 | 52.096 | Camunda事务隔离检查日志 | Camunda引擎创建完成 |
| 13:12:34.367 | 13:13:41.296 | 66.929 | Camunda引擎创建完成 | Tomcat started |
| 13:13:41.296 | 13:13:43.359 | 2.063 | Tomcat started | Started JiaApplication |

## 区间内的具体工作与不能下的结论

- Starting→Spring Data：配置类/自动装配解析路径，没有可归属的Bean步骤，64.056s不能全部写成扫描CPU时间。
- 三类Spring Data仓库均找到0接口，各自自报扫描1025ms、54ms、910ms。它们处于2.940s墙钟区间内。
- Repository结束→首条重复Mapper警告9.032s缺少细分；1070条重复Mapper警告跨2.928s，不是整个Mapper配置成本。
- Mapper警告结束→Web容器里程碑49.110s内有Jasypt属性源包装、日志系统重新初始化、Rabbit/Redis/AI BeanPostProcessor依赖装配和Tomcat初始化。Web日志所报127062ms起点更早，不能另加127s。
- Web里程碑→ChatClient确认57.939s，观察到Jasypt加密器创建与AI配置；不能说解密独占58秒。
- ChatClient确认→Redisson版本日志47.002s中间缺少Bean级记录。Redisson版本→连接完成17.967s，有1+24个连接的完成日志；这不是逐个连接的时间。
- Redis连接完成→Hikari开始17.098s未细分。Hikari Starting→Start completed9.907s是同一组件明确起止。
- Hikari完成→MyBatis注入检查57.965s、该检查→Camunda隔离检查34.011s均有观察空白，不能全算到SQL或Camunda。
- Camunda隔离检查→引擎创建52.096s，是引擎初始化后半段观察区间，非完整引擎创建独占耗时。
- 引擎创建→Tomcat真正启动66.929s，依次有认证管理器、欢迎页映射、actuator端点、MyBatis上下文、MCP工具提供器等日志。
- Tomcat启动→Started2.063s内可见Rabbit一次连接超时及随后连接成功、DispatcherServlet初始化；没有证据说Rabbit卡了数分钟。
- GC的168次/29.213s分布在以上区间中，不另加。
- Started之后Runner还在做schema/内容初始化，13:13:58注册计划任务；但并没有每个Runner的开始/结束，不声称全部在这15秒完成。
- start健康成功后已做5秒稳定观察、JAR摘要和PID/端口/身份再核验；installer随后调用status，finalize_candidate又算canonical摘要并再次status。每次status还读全JAR摘要、运行记录、进程/端口归属与health。JRE整树校验只在start要求中，不是每个status都会执行。
- 安装器的“自动授权”是从同Run制品自动生成的机器校验数据，不是人工审批或Reviewer等待。

## 来源与局限

- 部署原始查询：`/var/tmp/cyf-api-flow-timing-20260913-3HlYKb/run-40-machine-0.log.json`、`/var/tmp/cyf-api-flow-timing-20260913-3HlYKb/run-40.json`。
- 应用日志：`/var/log/cyf-api/startlog_20260913_130509.7dQyDT.log`。
- 自动授权前值备份文件名时间为13:03:53.413259、mtime13:03:53.417499；只查看路径/元数据，未读取密钥。
- Run40对应旧JAR备份文件名STAMP13:04:28、mtime13:04:49.261675。文件mtime是旁证，不是整次备份完成时间。
- 日志两条ps行显示同一PID3392969的lstart13:05:08、etime09:41/10:29，推算两个采样时刻；秒级近似，不混用JVM GC计时起点。
- `/usr/local/sbin/cyf-api-flow-install`、`/usr/local/sbin/cyf-api-kit`当前mtime均早于Run40（09:51）；未取得执行时内容哈希，因此源码用于解释调用路径，原运行日志用于确认执行现象。
- `/usr/local/sbin/cyf-api-flow-deploy`当前mtime14:36，晚于Run40，不能把其后来增加的schema步骤算入Run40；早期区间的更细函数时间没有证据。

下一步最小测量补齐：同一既有Flow发布中为prepare、package-validation、backup、stop、activate、JRE-validation、exec、runner、health、status、commit加单调时钟起止，为Spring步骤/SQL组补计时。不为补历史数字重启生产，不重跑本机构建。
