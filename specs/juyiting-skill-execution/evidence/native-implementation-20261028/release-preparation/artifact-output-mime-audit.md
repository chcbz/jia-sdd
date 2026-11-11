# 原生输出 MIME / 下载只读核对（2026-10-28 19:58 +0800）

范围：当前 API/Web 工作区源码、API 主机配置文件；未修改生产或 Owner 文件，未运行重型构建/真实端到端。API HEAD 516267bf7b19bfc03581ae580704af9246ffb622、Web HEAD ca22ac29de657971b12a71f3a99d2d9ecfc67c1c，均有共享未提交改动，HEAD 不是当前全部源码的固定 tree。下列摘要固定所核对关键文件，正式候选另行冻结。

## 配置与调用链

只读 `/home/isp/hosts/cyf/api/application.properties`：personal-workspace storage enabled，10,485,760 bytes；execution MIME 显式列表有 PNG/JPEG/PDF/DOCX/XLSX/PPTX/plain，缺 HTML/Markdown/JSON。task-artifact-storage enabled，16,777,216 bytes，显式列表含 Markdown/JSON，缺 HTML。运行进程 PID 480152 的 cmdline/environ 未发现相应直接配置键；这不能排除其他 Spring 配置来源、导入或运行时覆盖，因此以上为文件值，**并非已经确认的 effective 配置**。

| 环节 | 当前源码事实 / 按上述文件值的结果 |
|---|---|
| 可用能力 | `ChatActionCapabilityService.availableNative()` 取服务端 `nativeLocalFileCapabilities()`、runtime 广告和固定支持集合交集；正常广告不提供三种新 MIME。需授权、session/fence 等其他条件；不能把配置等同授权。 |
| v5 对话 stage/commit | `PersonalWorkspaceExecutionServiceImpl.stageConversationOutput()` 验证冻结 outputs MIME、大小、UTF-8 等后经 `FileSystemPersonalWorkspaceStorage` 保存；`commitResult()` 核对绑定、lease、已暂存行和内容摘要后提交。该链不是 task-artifact-storage。若执行配置和 Runtime 广告均允许且其余条件满足，源码支持三种 stage/commit；尚无真实端到端证据。`PersonalWorkspaceOutputFormatValidator` 检查非空有效 UTF-8 / 无 NUL，并不解析 JSON 或净化 HTML。 |
| 已提交成果转正式任务成果 | `AgentSelectedOutputFinalizationServiceImpl.prepare/publishAll/publish` 经 `AgentTaskArtifactService.publish` 进入 `FileSystemAgentTaskArtifactStorage.requireAllowedMime`；按文件值 HTML 被拒，Markdown/JSON 的 MIME 被允许，仍须满足 ACL、绑定及其他校验。task-artifact 默认白名单也不含 HTML；只改源码默认值不能解决显式配置。 |
| 下载/预览 | `ChatBountyMediaController.outputs/content` 对三者生成下载 URL、无 inline preview，验证用户/会话绑定、提交状态、长度及 SHA；attachment、nosniff、no-store，HTML 不作 inline 渲染。`ChatSkillResultController.result` 有完成/关联校验。`AgentTaskArtifactController` 另提供经身份/ACL 检查的附件接口，不假设其可被普通浏览器直接使用。未实测在线端到端。 |
| 聚义厅 UI | `web/src/components/juyiting/BountyExecutionOutputs.vue` 显示文件信息，仅为可预览类型显示预览按钮；当前未见下载按钮。`bountyOutputCatalog.js` 的下载扩展映射不含三种类型，回退 octet-stream/bin；目前未找到这些 helper 在生产 UI 的下载调用。不能以 API 有 URL 宣称用户已有可用下载入口；其他 UI 入口未全面核实。 |

## 最小候选与回归（交 API/Web Owner，不在此修改）

1. 核验实际 effective 配置和来源，授权后保留所有既有条目，execution 列表增 `text/html`、`text/markdown`、`application/json`；task-artifact 显式列表增 `text/html`，保留现有 Markdown/JSON。保存前值、应用后 readback；现有 workspace 10 MiB 上限仍约束对话 stage。配置不是技能/工具授权。
2. Web 现有聚义厅目录增加经认证的安全下载入口，沿 API 精确 URL/身份保护和长度、摘要校验，补三种真实 MIME 和扩展名映射；HTML 只作为附件下载，不用 iframe/innerHTML 预览。其他现有下载入口应先核对再复用。
3. API 定向建议：`ChatActionCapabilityServiceTest` 覆盖能力交集；`SkillExecutionServiceTest` 覆盖三 MIME 的 stage/commit、未允许类型及 lease/ACL；`PersonalWorkspaceOutputFormatValidatorTest` 保持 UTF-8/无 NUL 合同；`AgentTaskArtifactStorageF02Test`、`AgentTaskArtifactStorageConfigurationF02Test` 和 `AgentSelectedOutputFinalizationServiceImplTest` 覆盖显式列表、HTML 拒绝及追加允许后的正式发布。为 `ChatBountyMediaController` 补三格式 attachment/nosniff、认证越权、摘要篡改及 GET/HEAD/Range 回归。Web 的 `juyiting-bounty-output-gallery.test.js` 和 `juyiting-bounty-output-catalog.test.js` 覆盖下载入口、真实 MIME/文件名、完整性及 HTML 不预览。实际可用 Gradle selector/source set 和 600 秒总时限需 Owner 在正式 Flow 核实，不能凭此报告承诺通过。

## 关键文件 SHA-256（当前工作区字节）

- API `PersonalWorkspaceExecutionServiceImpl.java`: ee9cb5f5ec54261fd1476fcb05bff9093065120be9105e771ce1abab3ed82d5d
- API `FileSystemPersonalWorkspaceStorage.java`: 5305689d2dd749d94a150bf8525dd34529ef0bb729e79308258488b45f4816e3
- API `AgentSelectedOutputFinalizationServiceImpl.java`: a3f827bef775146e82cc3c5a862da2a488932468a6aa4c14710521c1b56f508d
- API `FileSystemAgentTaskArtifactStorage.java`: bbf20ca3c44a8bbb737185cc1a50a428e4fe259b94bfb3485023642146bb5a0f
- API `PersonalWorkspaceOutputFormatValidator.java`: 4578d0e7f5a23b39fc9f0d3dc9957bdb9431476f4fb800b0a18f6ab064d7f208
- API `ChatBountyMediaController.java`: 50ce19cb6841991faffb19a10b95442144cb020628893794710c338b694efd6a
- API `ChatActionCapabilityService.java`: db8b2899ad253236ba032f192d2deafb55da667095480824606f83967ac8c275
- Web `BountyExecutionOutputs.vue`: bd41e73290c7f006de9ccad775c01f8b51548875f53619aef24d12953c8a3df1
- Web `bountyOutputCatalog.js`: 9616dbf3d021dd3fe88e5a0c40b40be76f8c9f478c992066bf64f4d15cd79d55

## Runtime YAML 修复记录核对

`runtime-ci-candidate-22b4511.yaml` 当前 SHA-256 `1be699c4e4ee346112133bd1417c478168ebfdc1af82367cd129748263f7635f`，与 `runtime-flow-candidate-plan.md` 中 Python 3.6 修复记录一致。合成 fixture 实执行日志为 `runtime-ci-python36-synthetic.log`；不是生产 ZIP 或 Flow 验证。
