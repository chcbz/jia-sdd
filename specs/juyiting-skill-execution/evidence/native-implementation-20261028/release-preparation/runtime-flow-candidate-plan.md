# Runtime 5264702 CI-only 候选准备（2026-10-28；未运行）

## 确认与边界

- 只读 `getPipeline` 2026-10-28 19:07 CST：`cyf-ops-manual`，canonical 配置 SHA256 `1fc8acb3e9dd8718da40eec866394b016a0b5b09b1b9335a01ce8b668f4eca12`，sourceCount=0；当前实际 stage 是 Startup diagnostics tooling / Verify startup diagnostics，`VMDeploy`、`executeUser=root`、`downloadArtifact=false`。**不能直接以当前配置作为本轮构建 Run**。本次未修改或启动，未来实际临时候选须经 Owner 协调活动 Run、保存/读回/恢复原配置，且不得包含 VMDeploy/生产安装。只读 run 列表快照 `runtime-flow-runs.json` 不是当前排他状态，未来启用前重新查询。
- 既有历史模板 `/home/isp/state/architecture-convergence-20261026/bridge-repair/runtime-candidate.yaml` 是私有历史资料，Run63 为源码测试+`collateExecutionPayload`+同 Run npm 依赖+ArtifactUpload，并非完整自包含 Node/Python 制品；只能参考结构，不能直接粘贴历史提交、版本、URL/SHA、旧结果或生产动作。旧 selector `skill-native-host.test.mjs` 当前不存在，需删除该旧 selector，并覆盖 v5、新恢复测试。历史测试 538 PASS 仅对历史 commit，不能复用当本轮结果。
- 本地候选 commit `22b4511945d7ef7e6cfbda0f482f6c8910ce8306` / tree `d8529e3ba852dc541b527c46d556dd8126b7d527`，父提交 `15483d554a0fd6b01c3413d68c80e5367654a942`；`conf/` 无本地未提交改动，仅无关 `?? specs/`，图片包 12 文件已跟踪。含 Owner 最近的 `native-skill-config` I/O 错误及 `skill-conversation` 恢复测试；先前 payload SHA 不再是最新候选。此前 19:04 fetch 仅证明父提交当时等于 origin/develop；本候选尚未 push/Flow，未来推送和使用前须重新核对远端及实际 checkout。不得混入脏工作区、历史 payload 或历史哈希。
- 使用 Flow 临时 CI-only 构建作业及同 Run ArtifactUpload（历史 `filePath: _runtime_export/`），不使用 VMDeploy；依赖下载固定来源和校验，不改变现有完整性/身份保护。不得读入真实密钥和生产环境，避免真实模型/付费调用；`env -i` 测试、所有 opt-in probe 未设置，不改变测试源码。受影响的必要测试不能为凑 600 秒删除，耗时无法预先保证：包含准备、下载、测试、制品输出/上传和排队等 Run 总耗时，Owner 需按 Flow 正常受控终止机制确保 ≤600 秒，达限记录实际失败，不分 Run 重置计时、不盲重试。

## 待固定输入与同 Run 命令草案

下面命令是 **CI worker 方案，不是已执行脚本**。已绑定下列本地候选 commit/tree；本次受信 Node 工具/来源与校验和、私有 HOME/TMP 及依赖源需由 Owner 根据冻结候选和实际 worker 填入；不将临时目录设到生产。实际 Flow 需确保 source checkout 与下述断言相同，使用同一 job/artifact，保留真实日志及 skip 明细。此方案基于历史 Node 24.22.1/并发2，仅为容量参考，不保证本候选耗时或当前环境兼容。

```bash
set -euo pipefail
EXPECTED_COMMIT=22b4511945d7ef7e6cfbda0f482f6c8910ce8306
EXPECTED_TREE=d8529e3ba852dc541b527c46d556dd8126b7d527
: "${CI_NODE_BIN:?verified private Node required}" "${CI_NPM_CLI:?matching npm CLI required}" "${CI_PRIVATE_HOME:?private HOME required}" "${CI_PRIVATE_TMP:?private TMP required}"
test "$(git rev-parse HEAD)" = "$EXPECTED_COMMIT"
test "$(git rev-parse HEAD^{tree})" = "$EXPECTED_TREE"
test -z "$(git status --porcelain --untracked-files=all)"
NODE="$(readlink -f "$CI_NODE_BIN")"
NPM="$(readlink -f "$CI_NPM_CLI")"
# 私有工具链的来源/摘要及安全父目录在作业前核验；不拷贝或更改共享生产Node。
export PATH="$(dirname "$NODE"):/usr/bin:/bin"
mkdir -m 700 _runtime_export
OUT="$PWD/_runtime_export"
# 锁定 bridge 依赖，不执行安装脚本。
(cd conf/codex-bridge && env -i PATH="$PATH" HOME="$CI_PRIVATE_HOME" TMPDIR="$CI_PRIVATE_TMP" "$NODE" "$NPM" ci --ignore-scripts --no-audit --no-fund)
# 本候选依既有 Run63 核心选择器，替换已删除旧测试并加入 v5、隔离 profile、恢复和 wire。
env -i PATH="$PATH" HOME="$CI_PRIVATE_HOME" TMPDIR="$CI_PRIVATE_TMP" \
 "$NODE" --test --test-concurrency=2 \
 conf/codex-bridge/test/juyiting-action-model-schema.test.mjs \
 conf/codex-bridge/test/juyiting-action-outcome.test.mjs \
 conf/codex-bridge/test/juyiting-typed-runtime.test.mjs \
 conf/codex-bridge/test/juyiting-review-v5.test.mjs \
 conf/codex-bridge/test/skill-conversation.test.mjs \
 conf/codex-bridge/test/skill-execution-store.test.mjs \
 conf/codex-bridge/test/skill-executor.test.mjs \
 conf/codex-bridge/test/conversation-native.test.mjs \
 conf/codex-bridge/test/skill-install-manager.test.mjs \
 conf/codex-bridge/test/skill-management-wire.test.mjs \
 conf/codex-bridge/test/skill-registry.test.mjs \
 conf/codex-bridge/test/archive-position-skills.test.mjs \
 conf/codex-bridge/test/agent-client.test.mjs \
 conf/codex-bridge/test/skill-registration.test.mjs \
 conf/codex-bridge/test/native-single-entry.test.mjs \
 conf/codex-bridge/test/native-execution.test.mjs \
 conf/codex-bridge/test/native-execution-profile.test.mjs \
 conf/codex-bridge/test/native-artifact-session.test.mjs \
 conf/codex-bridge/test/native-artifact-snapshot.test.mjs \
 conf/codex-bridge/test/native-skill-config.test.mjs \
 conf/codex-bridge/test/app-server-native-execution.test.mjs \
 conf/codex-bridge/test/app-server-native-handshake.test.mjs \
 conf/codex-bridge/test/typed-inspection-profile.test.mjs \
 conf/codex-bridge/test/typed-inspection-network.test.mjs \
 conf/cyf-agent-runtime-v1/test/install-entry-convergence.test.mjs \
 conf/cyf-agent-runtime-v1/test/runtime-host.test.mjs \
 conf/cyf-agent-runtime-v1/test/hosting-config.test.mjs \
 conf/skills/native-image/test/image.test.mjs > "$OUT/tests.log" 2>&1 || { cat "$OUT/tests.log"; exit 1; }
cat "$OUT/tests.log"
```

该显式清单是**待 Owner 审定的最低受影响候选**，不是全量回归或已执行证明。`skill-conversation` 中 nonstarve 修复及 `native-skill-config` 的文件 I/O 错误均由对应完整测试文件覆盖；须核对新测试实际纳入冻结 tree。`env -i` 将真实模型、原生/图片/typed probe 的 opt-in 留空，真实 probe 是 skip，历史实测须按精确输入单独归属；若某测试依赖其他必要 fixture，则显式以无秘密 fixture 配置，不得绕过真实失败。图片测试使用模拟服务，不是付费调用。必要其他受影响回归、工作流/runner 的现有完整 suite 由 Owner 在实际 600 秒安排内纳入，不将此列表误作全部验证。

## 同 Run payload 与普通技能 ZIP

历史脚本的生产代码入口为 `collateExecutionPayload(sourceBridge, payload/codex-bridge)`；随后从本 Run `npm ci` 的 `node_modules` 拷贝到 payload，按本候选 `conf/cyf-agent-runtime-v1/install.sh` 两个 `for file ... install -m ...` 列表拷贝 Runtime 文件并保留模式，递归输出每文件 SHA256/mode、lock SHA、Node版本和 **实际** `PIPELINE_ID`/`BUILD_NUMBER`/HEAD/tree。候选版本必须按本次两 package/lock 实际值断言；历史脚本的旧版本硬编码应替换为本次固定输入。上传 `_runtime_export/` 时含 `tests.log`、payload 与 manifest。历史做法为代码+JS依赖 payload；**不含 Node/Python venv，不是可直接运行的完整制品**，不能只凭该目录或历史安装复用证明跨机器完整依赖。未来完整候选若需自包含，应在 CI 私有新目录执行当前 `conf/cyf-agent-runtime-v1/install.sh --target <CI绝对新路径> --node <校验的CI Node> --npm <匹配npm CLI> --python <校验的CI Python> --engine-root <当前checkout/conf/codex-bridge>` 并调用制品内 `runtime/validate.sh --root <CI路径>`；此为 CI 本次制品准备而非生产安装，需评估同 Run 资源/时间、依赖来源完整性和输出上传。不能使用生产目录作为 target 或省略校验。已有脚本的 Python requirements 固定顶层版本，但不能据此声称所有传递依赖、pip 及工具二进制已不可变：须记录并核验实际依赖闭包/来源。

同 Run 可作为 **独立** ArtifactUpload 目录中的 ZIP 产物，不将其并入 bridge `EXECUTION_PAYLOAD_FILES`：在同一冻结 checkout `conf/skills/native-image/`，安全核对其 `SKILL.md scripts vendor` 全为已跟踪的预期普通文件/目录、拒绝符号链接和秘密后，CI 用 zip 工具从该目录以根成员 `SKILL.md scripts vendor` 建立 `"$OUT/native-image.zip"`；`unzip -t` 与路径/条目检查确保无绝对路径、`..`、链接、重复项、测试和 manifest；输出该 ZIP 实际 SHA256 和字节长度并绑定本次 commit/tree/run，连同其测试日志由同一 ArtifactUpload 上传。命令形状：

```bash
# 以下安全检查和 zip/unzip 的 worker 可用性须先落实；不得将其当已完成验证。
(cd conf/skills/native-image && zip -qr "$OUT/native-image.zip" SKILL.md scripts vendor)
unzip -t "$OUT/native-image.zip"
sha256sum "$OUT/native-image.zip" > "$OUT/native-image.zip.sha256"
wc -c < "$OUT/native-image.zip" > "$OUT/native-image.zip.bytes"
```

若需要新安全条目检查或 zip 工具，放同一 CI 作业内并保留日志；本轮不本机生成 ZIP、不借历史测试 ZIP 的摘要。ZIP 与 Runtime payload 各自版本/身份不同；上传同 Run 并不等于 API 发布、安装、授权或技能端到端成功。ArtifactUpload 的实际可用性、是否同时上传大 ZIP、当前网络/资源/超时均未在本次验证。

## 2026-10-28 Python 3.6 输入修复

Owner 确认 Alinux3/本机 Python 为 3.6.8：候选 YAML 的 `IMAGE_PACKAGE` 不再向 `ZipFile` 传 `compresslevel`，并以 `universal_newlines=True` 取代 `text=True`。修正后的 `/home/isp/wsps/cyf/specs/juyiting-skill-execution/evidence/native-implementation-20261028/release-preparation/runtime-ci-candidate-22b4511.yaml` SHA256 `1be699c4e4ee346112133bd1417c478168ebfdc1af82367cd129748263f7635f`；旧 YAML 摘要不再适用。已用本机 Python 3.6.8 实际执行 YAML 提取出的打包段，仅使用独立临时合成 Git fixture，条目/内容/CRC/摘要/长度/fixture commit-tree-run 校验通过；日志 `runtime-ci-python36-synthetic.log`，其中 ZIP 摘要仅属于合成 fixture。其他嵌入段是 JS 和 shell；静态语法检查已重做。未执行 Flow、未打真实包，CI 环境和 600 秒总时限仍待正式验证。
