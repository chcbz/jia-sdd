# 候选 Web 本机全量 Mocha 复跑（不是项目固定环境门禁）

对象：独立工作树 `web` HEAD `8f47a1289bf501616ba234638192a5303d3155d7`。从该工作树 `web/` 执行 `env -u CI -u PIPELINE_ID -u CYF_CI_BOOTSTRAP npm run test`，退出码 **1**；报告的 `2384` 个测试中 `2341 passing / 41 failing / 2 pending`。本机环境为 **aarch64 / Node 22.22.0**；因显式关闭 CI bootstrap，本次**没有**新 E14 性能门禁报告，也没有项目规定的 Node 20.20.2 / amd64 / Chrome 133 验证。全量结果不得记为通过。

|本机失败类别|数量|报告中的共因或尚缺证据|
|---|---:|---|
|E9A 遮挡碎片|27|`/usr/local/bin/chromium-headless-smoke` 不存在，首轮 canonical decode `ENOENT`；后续预期语义错误断言因此失败。|
|E9B 六区图集|6|同一固定浏览器解码工具 `ENOENT`；冻结像素及错误诊断不能由本机 Chromium 142 替代。|
|E8A 道具排序视觉门禁|6|帧 alpha 扫描依赖同一浏览器解码工具，`ENOENT` 后另出现预期语义消息不匹配；尚未验证固定环境中的真实结果。|
|TMX 编辑 CLI、快照/预览|2|Mocha 测试内设 **60 秒**、**20 秒**各一次超时；先前隔离复测也出现，需在固定环境区分性能瓶颈与代码缺陷，不能放松阈值掩盖。|
|本次工作台相关测试|0|前次全量中失败的账户离开守卫、SelectedAgentCard、任务工作台实例、两项语音和 E1 baseline 重定向共 **6 条**在本次报告均为 passing；这不等于剩余业务路径已实测。|

复核入口是 [`local-full-recheck-summary.json`](local-full-recheck-summary.json)：包含报告的统计、41 个失败测试的 Mocha `fullTitle` 原字段及以 `/` 分隔的套件路径（两者不可混用）、E8A 两类失败阶段、6 个本轮已通过的历史失败标题及运行环境、报告 SHA256。原始本机忽略产物 `web/mochawesome-report/mochawesome.json` 的 SHA256 见 JSON；进程日志位于本机 `/tmp/cyf-wb-full-recheck.log`（不随提交长期保存）。此前 `2331/47` 来自另一批运行，测试登记数不同，不能简单把 pass 差值当作本分支修复数。

**TMX 超时定因补测（仍非通过）**：在此 aarch64/Node22 本机、`web` 同一 SHA 下，以 `TemporaryDirectory` 复制提交的 `hall.tmx`，从独立 Python 进程顺序重放同一 CLI `node scripts/juyiting/apply-map-ops.mjs <临时TMX> tests/fixtures/juyiting/hall-movement-ops.json` 两次，分别 **30.124s / 29.487s**，均 exit 0，首轮 `updated`、第二轮 `unchanged`；空操作数组 `[]` 对同一 TMX 只需 **0.819s**（exit 0）。失败的 CLI 用例（`tmx-edit-ops.test.ts:284`）设 `this.timeout(60_000)`；重放使用 Python stdout/stderr 管道而不是测试 `spawnSyncCaptured` 的临时文件捕获，两轮仅 CLI 耗时约 59.611s，另有复制/断言/框架开销，足以在此宿主机引发超时；这是对本机故障的**性能解释**，不证明固定 worker 上能通过，亦不准放宽超时。`git diff c19ac81..8f47a12 --` 检查 TMX 编辑实现、CLI、两条测试及 spawn helper **没有本分支差异**；运行逻辑保持基线，不为通过本机旧测试修改地图编辑业务语义。另一条快照/预览超时仅有下段限定条件定时复测，仍须固定 worker 复验，不能将其原因据此判定相同。

**快照/预览超时补测**：以与测试 `withScriptFixture` 相同的临时 `hall.tmx` + 4 个 1px 图片字节和隔离环境变量，依次运行原 `node --import tsx scripts/juyiting/render-map-preview.mjs` 缺失态、`--update`、成功检查；分别 **2.156s / 2.171s / 2.168s**，对应退出码 1/0/0，文案符合预期。超时测试在单个 20s 用例内调用该子进程 **10 次**（还要改写资源/校验失败/清理），约 2s 的本机单次耗时已足以解释 20s 门槛风险，但未完整重跑该 10 调用测试的单次耗时分布，也不证明固定 worker 上通过；现有业务、断言与 20s 限额均未更改。

**下一步门槛**：仅在获得 `no-deploy-amd64-qa.md` 列明的独立 Alinux3/amd64/root worker 授权后，针对**相同 Web SHA** 执行固定浏览器、E14、全量测试、构建与扫描；候选部署上的 OAuth、文件版本、SSE、写入和实体键盘仍按 `real-service-qa.md` 另验。本次不改动任何现有 E8/E9/TMX 源码、超时或历史基线。
