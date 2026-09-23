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

**下一步门槛**：仅在获得 `no-deploy-amd64-qa.md` 列明的独立 Alinux3/amd64/root worker 授权后，针对**相同 Web SHA** 执行固定浏览器、E14、全量测试、构建与扫描；候选部署上的 OAuth、文件版本、SSE、写入和实体键盘仍按 `real-service-qa.md` 另验。本次不改动任何现有 E8/E9/TMX 源码、超时或历史基线。
