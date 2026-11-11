# API Metaspace OOM 只读调查（2026-10-29 08:32 CST）

## 固定对象与操作范围

生产 PID480152，Temurin/OpenJDK21.0.12.1，现行安装记录Flow335、源码3bca7cbd719c3a331cc36ac26020f59183a0c839。本轮未重启、改内存参数、部署、改数据库、主动GC或生成新heap dump。以cyf-api身份执行jcmd VM.metaspace / VM.classloader_stats / Thread.print、jstat，读取已有GC日志。首次attach等待超时，socket建立后成功；未强制attach。

原始证据目录：`/home/isp/state/cyf-native-skills-20261028/metaspace-20261029/`。已有OOM dump `/home/isp/state/cyf-api-dumps/java_pid480152.hprof` 保持原处，不复制/上传；未运行高内存堆分析工具。本报告不声称完成堆对象保留链分析。

## 元空间实际内容

- MaxMetaspaceSize=192MiB；committed=196608KiB（192MiB），used=194103.42KiB（189.55MiB）。Non-class=172240.16KiB（168.20MiB），Class=21863.27KiB（21.35MiB）。committed达到上限；非堆对象数据撑满Java heap。
- 唯一Spring Boot LaunchedClassLoader：28074类，used159166.53KiB（155.44MiB）。包含业务及应用依赖，不能将其全部记作业务代码。
- bootstrap：5519类，27011.16KiB（26.38MiB）；隐藏类2574个合计6412.41KiB（6.26MiB）；app/platform两加载器合计1511.18KiB（1.48MiB）。ClassLoader统计另有一个0类Tomcat加载器，实际Java ClassLoader共5个，不是数万套应用加载器。
- 应用已加载类按包前缀计数：Spring Boot2470、cn.jia.agent1951、Kotlin reflection1288、Spring Security1069、cn.jia.chat1023、Spring Data971、Jackson2(com.fasterxml.jackson)830、Jackson3(tools.jackson.databind)678、MyBatis453。这些是类计数，不是对应包的元空间字节数；类别含内部/动态类，应用列表也含1284数组类。
- 动态类模式：CGLIB219、JDK代理387、Lambda4434、LambdaForm/BoundMethodHandle2583；未匹配ByteBuddy或SpEL generated类。该命名统计不能单独证明有/无泄漏。
- 大量hidden CLD中存在约3.2万个0类节点，两次采样仍有增加；不能把它们当成3.2万个应用ClassLoader，也不能据此认定全部正常。其零元空间分配不是此次189.55MiB的主要来源，原生结构/失败后增长的关系还需独立验证。

## 时间线与故障机制

- 2026-10-27 09:12:56，启动接近完成时used147510KiB（144.05MiB）。09:12:58应用Started，startup325.956秒。
- 10:00 used178496KiB（174.31MiB）；11:00 used188123KiB（183.71MiB）；23:00 used192458KiB（187.95MiB）。启动后业务/依赖类继续加载，额度逐步耗尽。
- 首次Metadata Full GC：10月27日23:30:52；首次明确Metaspace allocation failed及OOM：23:31:13，随后生成现存235MiB heap dump。故障不是10月29日才出现，更不是尚未部署的本轮代码引入。
- 当前堆约132MiB/384MiB，而元空间commit达到192MiB。jstat采样累计Full GC约76958次、耗时113166秒（31.44小时）；多轮Full GC前后元空间几乎不变，符合存活加载器中的类元数据无法通过这些GC释放足够空间。
- Thread.print中Notification Thread位于GcInfoCompositeData.toCompositeData → Field.get → MethodHandleAccessorFactory → LambdaForm.compileToBytecode → ClassLoader.defineClass0。GC通知构造也在尝试生成辅助类；结合分配失败计数/连续Full GC，支持“耗尽后连GC通知/反射路径也受阻，故障持续放大”的判断。单次线程栈不证明它是最初增长源。

## 结论与未证实项

**已确认直接原因：192MiB元空间硬上限已耗尽，主要承载单个正常应用加载器的业务/框架/依赖类元数据。不是Java堆耗尽，也没有多套应用加载器泄漏的证据。**

增长曲线和当前类构成更支持“应用体量、业务热身/懒加载与192MiB限额不匹配”，而非明显CGLIB/热部署ClassLoader爆炸。但饱和后类加载受阻、指标稳定不能反证不存在持续动态类增长；不能宣布所有泄漏已排除。若需定位具体类的时间增量，需要恢复后跨业务热身采样，或在资源适当的环境分析现存dump；不在本机强行运行重型堆分析。

处置建议（未执行）：先按完整业务热身峰值与主机余量重定元空间容量，经受控流程恢复；增大-Xmx不针对当前命中的上限。随后比较类数/加载器/元空间随请求增长是否收敛，按实际功能审计双Jackson、Kotlin reflection等较大的常驻依赖，不为省内存盲删现有能力。单纯扩容不能作为已证实根治。

额外发现：OOM附近有PositionSkillStore链路的 `Table 'jia.agent_position_state' doesn't exist`。这是独立的部署/schema一致性错误；未查当前DB，不断言目前仍缺表，也不能据此直接认定OOM由该查询引起。只调内存并不证明该功能已恢复。

主要证据：metaspace-basic.txt、metaspace-classes.txt、classloader-stats.txt、class-summary.json、log-timeline.json、jstat-gc.txt、threads.txt、thread-summary.json、investigation-summary.json。
