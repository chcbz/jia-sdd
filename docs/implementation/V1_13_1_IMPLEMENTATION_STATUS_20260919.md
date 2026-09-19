# 1.13.1 实施状态（2026-09-19）

状态：**实现候选，非发布、非MVP验收通过通知。**

## 已实现的闭环能力候选

- 工作空间固定版本可关联本人悬赏；悬赏可回到空间选材并进入对应厅内议事。
- 议事以显式Agent、会话、任务和固定输入版本创建执行；任务模式接入真实work-item lease，不用私人执行回执冒充正式交付。
- 执行成果归档到空间；任务成果映射artifact与formal delivery，并在议事/悬赏/空间读取同一版本。支持正式验收、要求修改与返工恢复。
- 输入材料与输出格式分离：PNG/JPEG/PDF/DOCX/XLSX/PPTX可作为固定输入；输出仍只由服务端allowlist开放。
- 图片可安全原样预览；PDF Blob预览；DOCX/XLSX/PPTX走受控文本抽取预览，明确不宣称版式、分页或公式计算预览。

## 精确候选

| 组件 | Commit / tree | 已做自检 | 未完成 |
| --- | --- | --- | --- |
| API | `bf5adc386429f73a427722f25fc392312bd9d998` / `92cb053a6f7c8df2f3ea2050fed099b7cea51655` | Git whitespace、W09静态合同与手工`javac` | 精确Gradle/集成测试；实际部署 |
| Web | `68f9eab7e3bdec7f3d711b735d2767085feb2d3f` / `6c96e8dc8d1413718d06f47accdeeb1021802e72` | 80项聚焦Mocha、PDF/文档预览合同、`node --check`、`git diff --check` | 权威Flow测试/构建/同Run制品/实际部署 |
| Agent runtime | `c5b1ea43f8a54599d38b08d377d1f6f53f76b18b` / `36e27d3fab582dc8617780e364cedfdbbd4af527` | `node --test`: 323 pass / 0 fail | 与精确API/Web的真实联调和受控部署 |

本机API Gradle会在根构建评估阶段因缺少受批准的`repoUsername`配置停止。Web已在可复用测试依赖下完成80项聚焦Mocha、PDF/Office预览合同、静态语法和空白检查；精确命令与结果见 `handoffs/V1_13_1_WEB_CONTRACT_RECHECK_20260919.json`，但这不是生产构建或部署证据。2026-09-19 原始候选曾进入无部署 Flow 验证：API `5260799` Run 88、Web `4403172` Run 140 均在checkout/test/build前终止为`FAIL`，来源commit未知且作业日志为空（`more=false`）。Web随后已有新提交`68f9eab…`，可作为新的精确候选，但当前执行环境没有可用的Flow控制面凭据，无法只读确认push自动Run或安全地手动启动；未对旧失败输入盲目重试。因此仍没有云端测试、制品或部署证据；原失败详情见 `handoffs/V1_13_1_FLOW_CANDIDATE_ATTEMPT_20260919.json`。

## 不能跳过的发布条件

1. 精确API/Web候选完成权威测试、构建、同源制品和健康核验。
2. A01–A20完成端到端验收。
3. B01–B08必须取得明确授权后由真实Agent/Provider执行：Provider账户或测试Agent、非敏感测试文件、可外发数据范围、调用次数/用量或金额上限。当前没有该授权，因此没有调用Provider，也没有虚构图片或文件修改成功。
4. 之后才可冻结`release/1.13.1`、发布并执行C01–C03。

唯一运行台账：`docs/implementation/TASKS.yaml#runtime_ledger_json`。
