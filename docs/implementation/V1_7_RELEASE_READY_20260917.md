# 1.7.0 开发集成与 release 冻结结果（2026-09-17）

## 已完成本轮目标

前后端均已将验证候选快进合入**远端 develop**，并分别创建新的 **release/1.7.0**。每个仓库使用一次非强制atomic push更新两条引用，随后ls-remote读回一致。没有移动旧release、重置脏primary工作树、调用云效Run或操作生产进程。

| 组件 | develop / release/1.7.0 固定提交 | Git tree | 制品 SHA-256 |
| --- | --- | --- | --- |
| API | `9aaf2a315b0365ccf801012b100cf7b38cf47c62` | `b4bffe1e298d9c445ff370b4c19ce3cf3f750a14` | `3e516826a863d6ab281639df7ff17818903e32cc757b24b4d8a089ee9537e5eb` |
| Web | `7c4902983974b748ea01d7c88e2403fa636691e6` | `ae9cd58d4adb7ee16678ba92b1e67de5ecb84141` | `02775873e9498af7e17df11d6dfa4e8454296b1be030c0ffee617b594f0beef7` |

开发分支后续可以前进，release分支保持此SHA。API保留最新任务owner修复`1feb687b`及此前已上线目录hotfix`4451c300`祖先。本次只冻结代码与制品，**尚未部署1.7、启用后端开关或完成线上业务验收**。

## 功能与验证

独立经济预览入口：本人钱包/流水、无落库预算试算、技能目录与详情、自有Agent权益/安装证据、托管参考方案与租约。九类新API遵循`economy-readonly-v1`，交易/购买/安装/开通/续费动作均不开放。语音仍按用户要求延期。

- API：新增preview **26/26**、scope/catalog/schema **12/12**、制品安全 **64/64**；均0 failure/error/skip；bootJar成功。源码精确绑定，XML和JAR摘要由主控复核。
- Web：完整非CI-bootstrap Mocha **2195通过、0失败、2既有pending**；独立policy Node **7/7**；相关Mocha **60通过**（旧日志文件名含96，实际以日志60为准）；ESLint0error；Vite生产构建成功。
- 集成：核对九类method/path、E0 envelope、DTO字段、decimal-string与capabilities动作/feature集合；结合真实MockMvc/Spring事务代理、实际mapper SQL隔离fixture、Vue mount/deferred/身份ABA回归。不是线上双身份联调。
- 本地构建依据用户临时授权，`build_origin=local_user_authorized`；没有虚构Flow Run。

## 真实限制与异常记录

1. **不是全API测试PASS。** 默认agent整模块compileTestJava仍因历史测试未同步owner参数而失败。主控试探适配后又发现后续100条诊断，12个报错文件中11个相对远端基线未变；已撤销自身试探适配，没有改生产接口兼容旧测试。使用明确独立sourceSet完整运行本次5个preview测试类及相关目录/schema回归；默认测试集未删除/缩减。历史编译债仍未解决，证据见`handoffs/V1-7-UPSTREAM-TEST-SOURCE-DEBT-20260917.json`。
2. H2 MySQL-mode SQL fixture证明了指定case-insensitive数据集下的隔离和表计数不变及mapper写入拦截；不冒充生产MySQL/schema已验收。上线后还需认证只读业务回执。
3. Web首轮全套受全局Chromium launcher缺少headless参数影响。保留失败日志，改用1.6验证过的任务私有wrapper后全套通过；未改全局launcher或跳过失败。
4. Gradle一次因缺少发布仓库属性在求值阶段停止；经核实只涉及publishing闭包，以非敏感local-unused属性完成本地测试/bootJar，未执行Maven发布。前后端未触及生产DML/付费Provider/语音启用。
5. 钱包tenant沿既有写入源使用JWT jiacn；市场/托管/Agent registry沿既有canonical0，额外保留exact client/owner/actor核验。不能混为全域tenant0，详见SDD集成修订。

## 可执行下一步

后续安排部署时，直接使用此冻结分支对应的已校验本地JAR/Web tar，先API再Web；按既有发布互斥/健康/可恢复安装流程操作，并启用独立后端只读开关。不要顺带启用旧交易、安装、收费或语音开关。部署与认证验收成功后再将功能标为released/归档。

本机交付包：`/home/isp/wsps/cyf/deliverables/releases/v1.7.0-local-ready-20260917/`，含`readiness.json`、`remote-promotion.json`、`activation-plan.json`、JAR/tar、原始XML/日志与`SHA256SUMS`。包内activation-plan仅为候选配置，未应用。root脏primary组件及历史gitlinks未重置，准确配对由本记录和SDD manifest保留。
