# 真实 CHECK catalog 与原生引擎兼容推进（2026-10-01）

本记录继续完整用户目标，不替代工作空间/多媒体/双接应/正式验收与版本发布。最新源码 pin 仍以 `integration.yaml` 为准；未验证候选不得提升。运行状态只在主工作区 TASKS.yaml 的 runtime_ledger_json。

## 1. 真实数据库观察已取得，原失败保留

API 组合基线 `642e73238edde3354a8b23654e561a496a2691f3` / tree `b529963ae8ece8f916917e998cd25db9c7fd77f6` 的原 V3 测试仍是34通过/3真实MySQL失败，后续未运行，不因诊断取得资料改成通过。

同一真实 Source Owner 的隔离诊断，先后出现 Python3.6 subprocess 关键字、MySQL列头及函数切片错误；这些停止记录保留，未盲目重试相同输入。Stage5改为完整控制流 mock 自检后执行新的单次候选：

- 实际 MySQL8.0.21、UUID/datadir身份匹配；事前 schema 不存在；CREATE成功后才取得 ownership。
- 来源精确抽取的25条SQL全部实际 exit0，包含原23条及两张后续表的精确CREATE；没有手抄或弱化原CHECK。
- 四张表的 SHOW CREATE 与 tables/checks/columns/indexes 原始catalog已经捕获。
- 原Stage5 receipt **仍是FAILED**：最后汇总以小写 `table_name` 读取真实大写列头 `TABLE_NAME`，产生KeyError。这是汇总脚本错误，不是25条DDL执行失败。
- cleanup实际PASS：只删除本次已ACK的私有schema，前后identity匹配并确认该schema消失。

Main随后仅对冻结raw TSV/JSON做离线读回：按真实header构造小写键别名、保持所有值/谓词不变；逐行raw与JSON相符，四种catalog都覆盖四表，得到 **4表、27个ENFORCED=YES CHECK、136列、89索引行**。没有再次执行DDL，没有把原FAILED receipt覆盖为PASS。

该观察允许 Source Owner 基于真实CHECK rendering修复限定initializer及测试两条路径；不能去掉所有括号、放宽predicate、接受same-name弱CHECK或重写共享canonicalizer。Source Owner 已提交精确 child `354f736a09b0e89d52306616245ba86e16897d85` / tree `15b9015a5734d7d46899788c904659c73535852b`，parent 为原 `642e732`。只改 `ControlledImageFollowupV3SchemaInitializer.java` 及对应测试；三条 catalog literal 与真实观察逐字匹配，原SQL、legacy修复和共享canonicalizer保持不变。新增测试覆盖14个owned CHECK及弱化/TRUE/extra/missing/unenforced拒绝。

Owner静态自检和Main独立路径/摘要/literal核对通过，**仅接受为新的验证输入**，不是正式JUnit通过或产品接受。新验证Owner已经实际READY、绑定唯一ledger并获GO，按完整正常图V3→V2→typed 11类/真实MySQL串行验证；最终fresh XML结果尚待返回。原34通过/3MySQL失败不改写；feature及integration pin仍保持已接受 `87c0acc`。

## 2. Client原生协议兼容是实际阻断项

当前已接受Client `2f6907274ea5395980df0643c6b3898fa522a54f` 的适配器固定CLI0.153.4/schema `b06f77062369d481a59cc70720c12b89cb9dd49c385863923262102d3ad6c978`。

本机全局launcher的优先嵌套native实际为CLI **0.159.2**，binary SHA-256 `1748767b230ebfc3d4ab7e4e254920d0c0ad9691fd8c11f190e7d44511a4a92e`。在清空环境、独立HOME/CODEX_HOME下生成的完整schema bundle SHA-256为 `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5`；这不是兄弟包0.156.0的结果。

对**未修改的真实Client public measurement方法**使用显式私有snapshot/schema根实测，得到 `APP_SERVER_BINARY_UNTRUSTED / CODEX_APP_SERVER_SNAPSHOT_FAILED:APP_SERVER_BINARY_UNTRUSTED`，childCalls=0、私有snapshot清理完成，未启动app-server/模型/Provider。旧包装先取error.code，掩盖具体内部错误；不能把该结果误写成已经隔离证明的 VERSION_MISMATCH。

另按现源码同序枚举实际资源：40个regular文件共78101808 bytes，明确超过旧64MiB硬上限；这是确定存在的拒绝条件。长期修复不回退全局CLI，也不把上限随意调大：按实测登记版本化schema，移除无依据count/size硬拒绝，保留资源清单/摘要/身份/私有复制/符号链接及真实错误处理，且保留具体cause。旧0.153.4合同及所有既有wire保持不变；新合同由本地profile显式选择，未知版本/schema仍拒绝，不自动换Provider或模型。

准备工作树与源包合同已存在，但本轮真实spawn被thread limit拒绝，**没有新Client Owner、没有开始实现**。唯一ledger新增等待条目准确记录此事实；不修改max_threads、不抢占其他Agent。完成当前已拥有的verification工作、关闭其已完成Owner后再领取。

只读进一步发现 `juyiting-typed-outcome.mjs` 的 readiness 仍硬匹配旧CLI/schema；仅修adapter测量会使新原生版本永远UNAVAILABLE。已新增不可变源包补充v1.1（原合同保留），最小写集增加该模块及其runtime测试：readiness、声明和runFastChat必须核对**本地profile显式选定**的registered exact合同与真实已测量、已初始化且未关闭adapter，不允许“任一已登记版本/仅measured=true”通过。typed schema1、输出union、sidecar、既有golden wires均不变。新版本兼容仍未开始实施。

## 3. INSPECT及严格无工具能力不能伪报

0.159.2本地schema包含text/localImage/localAudio输入，不包含通用本地文件输入；schema可用不证明模型理解或source物化已经实现。当前Client `runReadOnlyInspection`仍明确NOT_ENABLED，typed v1仅NONE/AVAILABLE。后续须实现独立受权input-only materializer、精确来源/字节摘要和真正输入adapter；普通文件按实际解析器能力处理，不能靠文件名回答。

本轮离线features实测shell_tool默认true；显式关闭该项确实变为false，但其它工具相关feature仍存在。该结果不是“严格无工具”证明。现有read-only-constrained声明继续如实保留；不能用空dynamicTools、只读sandbox、approval=never或单个feature关闭推导strictNoToolsVerified=true。

讨论仍以冻结 `interactions/discussion` typed v1及回执v1.1为准，EXECUTE保持独立v3；不实现早期schema-3讨论候选，不增加第二套问题状态机。

## 4. 发布前仍须完成

新API精确child相关正常图测试通过后才提升feature/pin；Client原生引擎兼容与真实INSPECT、多轮来源和完整媒体、双接应、真实登录/正式交付/验收/完成仍按原范围推进。当前loopback10018实际连接拒绝，已向canonical Runtime协调入口发alert-only，Main未重启foreign服务；旧健康记录不作为当前UP证据。

尚无本特性develop合入、冻结release、生产制品/部署或产品验收。不能发送“可以验收”的通知。所有上述原始回执与离线派生见[便携manifest](integration-evidence-20260928/catalog-and-native-runtime-progress-20261001/portable-manifest.json)。
