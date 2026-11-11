# 本轮诊断证据（2026-10-16）

这是隔离分段回放，不是整站OAuth、正式Flow或真实Provider/PDF交付验收。完整方案与边界见 `/home/isp/wsps/cyf/docs/implementation/REQUIREMENT-EXECUTION-REPAIR-PLAN-20261016.md`。

## 可重跑方式

1. `baseline.json`固定三仓源码与实际安装API JAR摘要。Java探针只调用已安装库的DTO/serializer，不启动服务或Gradle；依赖提取目录 `/tmp/cyf-requirement-20261016/` 的库来自该生产JAR。
2. 序列化：`/home/isp/apps/jdk21/bin/java -cp '/tmp/cyf-requirement-20261016/*' /home/isp/wsps/cyf/docs/implementation/evidence/requirement-execution-20261016/replay/FlowFixture.java`。合成值不是数据库事实。
3. Vue脚本复用原测试harness；将本目录 `step-replay.test.js` 或 `ui-defect-replay.test.js` 复制到 `/home/isp/wsps/cyf/web/tests/` 下本任务独有临时文件。于 `/home/isp/wsps/cyf/web` 执行既有 `node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --timeout 10000 --reporter spec tests/<临时文件>`。结束仅删除本次创建文件，不覆盖已有文件。
4. Runtime消费者探针：使用 `/home/isp/apps/cyf-agent-runtime-v1/releases/runtime-interface-20261015-1.2.7-6a9d8d3/node/bin/node` 运行 `/home/isp/wsps/cyf/docs/implementation/evidence/requirement-execution-20261016/consume.mjs`；无生产HTTP调用。
5. 成果错回执探针：同一Node运行 `/home/isp/wsps/cyf/docs/implementation/evidence/requirement-execution-20261016/replay/commit-receipt-probe.mjs`；只创建和删除自己mkdtemp目录，HTTP回复全为替身。
6. Runtime原测试使用 `git archive 6a9d8d3... conf/codex-ws-agent conf/cyf-agent-runtime-v1` 的隔离副本 `/tmp/cyf-requirement-replay-20261016/`，node_modules只读指向已安装制品。未安装新依赖、改生产文件或启动Runtime。`runtime-targeted.log`使用 `--test-name-pattern='workspace|Workspace|native queue'`（29通过/199跳过）；`bridge-wire-full.log`完整运行workspace-file-bridge/agent-message-wire（62通过，无跳过）。两组有重叠。

## 结果语义

- `step-replay.log` 1 passing：证明合成API事实下，实际UI操作会进入QUEUED，且最新完成状态被旧receipt遮盖；不证明真实执行完成。
- `ui-defects.log` 3 passing：三个“缺陷存在”断言成立，不是修复后验收绿。
- `real-consumer-result.jsonl`：stub接受/真实processor拒绝的对照。
- `commit-receipt-result.json`：错误output/manifest被bridge接受，诊断反例，不是成功交付。
- `frontend-targeted.log`：110项现有局部测试，不是前端正式Flow。
- `original-case-readonly.tsv`：原事项当时QUEUED/0输出，只读查询，不证明Provider从未执行。
- `runtime-log-summary.txt`：日志聚合不带原执行关联，不能单凭它确定线上首个解析错误。

本轮没有常驻服务/浏览器。临时源码诊断副本保留以便复查；生产API、Runtime、原用户事项和组件源码均未修改。
