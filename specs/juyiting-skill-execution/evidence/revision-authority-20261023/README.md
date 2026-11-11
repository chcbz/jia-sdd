# 跨账号成果续办修复验证

本目录记录task520暴露的原授权/执行方身份和永久失败重试修复。源码及Run见summary.json。

- 单元层：实际revision consumer与回执解析；存储/外部IO mock。共享dispatch授权服务另有原grant、撤销、范围和代际测试。
- MySQL层：复用JuyitingWorkflowMySqlTest实际事务/DAO/续办入库；外部授权及技能包仍为fixture，不冒充真实跨账号生产执行。新增跨账号资源scope提交、准备后撤权不写child，保留原回执写失败整体回滚、恢复、并发验收和claim等回归。
- 资料层：既有RetainedOutputSources/Admission、FormalDeliveryRetention以及真实MySQL资料授权用例保留；不以它们替代实际模型选择原图/上一版及精确输入回执。
- 生产未部署、不改测试任务业务状态；PDF仍不验。

## 最终CI（2026-10-24）

API develop b86d8cf4/tree499e0829；Flow5260799/252 SUCCESS，2962通过、126跳过、0失败。受影响8套件93/93（含真实MySQL36/36）与本次新增16项均未跳过。validateLayering、fresh bootJar成功，同Run制品及JAR摘要已核对。临时Flow配置已恢复APPLIED并回读。250分支准入失败、251新增测试fixture编译错误保留，不重标成功。

只完成源码/正式CI；未部署API，未重验task520、无输入生图、连续两轮改图输入SHA或PC/移动最终验收。下一步需固定本候选的版本化发布授权，再按同Run测试/构建/安装和上线业务验证收口，不将本CI包或既有Runtime上线证明当作本次API发布。
