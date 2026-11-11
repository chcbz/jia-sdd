# HTML / Markdown 前端预览

- Owner本聊天，用户2026-11-03要求增加前端html/md文件预览。范围：唯一原型先行，资料详情、成果目录/正式交付及议事成果复用共享静态文档渲染；不改变业务身份、权限、版本、下载与服务端预览契约，不扩展为脚本运行器，不部署。
- 主Web旧HEAD ca22ac2且资料/成果相关重叠脏改动，不能安全复用。仅一份隔离worktree `/home/isp/wsps/worktrees/html-md-preview-web-20261103`，base/develop d091940a22dadc670fbc954f797ba100f7a098e4 / tree dba66595bf1ceeda9a22283fec89459d25aa10bd（已fetch）。不接管其他任务worktree。
- 规格依据：现有接口固定版本读取内容；HTML/MD使用原内容授权读取，不增加后端转换格式。Web负责不可信文件安全呈现：清洗+无脚本/无同源权限iframe+CSP禁外部资源/表单/导航；保留现有身份代际取消。针对风险验证HTML脚本/事件/外链不执行及预览关闭/切换、MD格式、空白与失败、固定版本读取。不新增通用门禁。
- 现有依赖marked、DOMPurify复用，不新增npm依赖。现有预览尺寸限制不扩大成新硬门禁。最早验证原型1440/390/320、安全renderer及workspace/output/Bounty消费者定向轻量测试；正式重型验证须Flow。

## 实现与定向核验（2026-11-03）
- 原型先完成，唯一在用目录 `web/prototypes/juyiting/` 新增document-preview.js、HTML样例，MD改为格式展示。1440/390/320通过（prototype-results.json）。主原型目录包含其他任务未提交变更，本任务在隔离候选只提交自己的原型增量，不收纳其他任务内容。已请求在Codex打开18786，返回queued，不代表桌面页面已加载。
- 产品共享 `src/utils/richDocumentPreview.js` / `src/components/outputs/RichDocumentPreview.vue`：marked格式化Markdown，DOMPurify清洗HTML，空权限sandbox+srcdoc CSP阻止脚本、外部资源、表单与链接导航。保留内联CSS/安全内嵌位图，不支持运行HTML应用。
- 消费者：OutputPreview（成果目录/正式交付）、PersonalWorkspace（嵌入与完整资料详情）、BountyExecutionOutputs（议事成果）。固定版本授权内容读取及既有下载入口、MIME/摘要校验、身份切换和迟到响应取消均保留。议事HTML/MD保持服务端download-only契约，通过原授权downloadUrl读取字节作本地静态预览，不伪造previewUrl。
- API只读核对本地origin/develop `eb8df08946cf7f150c9c86d20b8eb97fbea50fcd`（非本任务实时fetch）：AgentTaskDeliverableController使用content.contentMimeType；AgentTaskCollaborationServiceImpl返回material.mimeType，不是强制octet-stream。未因某测试的octet-stream fixture放宽类型校验。原文本响应charset参数按同一文档MIME兼容，JSON错误体仍拒绝。API无需修改。
- 候选版本1.16.97，Web `83262731b0d3b520e8a3fa3a7ef1a318bc021e5f` / tree `b2776a90f9689173ab27637058954cfb53bba5e7` 已非强制push至远端develop；本地主工作区旧分支/脏内容不切换、不覆盖，根gitlink未替换为旧主工作区HEAD。
- 本机轻量反馈：13组相关consumer/renderer套件159通过（targeted-tests-final.log）；后续仅同源MIME charset兼容用例已包含其中。真实Chromium使用产品renderer模块，HTML/MD×1440/390/320六组通过：格式、表格/内联样式、MD强调/列表、opaque sandbox、无脚本/无外部请求（含清洗中途、CSS import/url）、父页隔离、页面无横向溢出（browser-results.json）。不是整站线上业务验收。
- 新renderer/组件ESLint通过；既有触及文件有历史lint问题，按固定base对比未新增error（lint-baseline-comparison.json），未顺手全文件格式化。output-preview-document.test.mjs通过。output-preview-pdf.test.mjs旧文案静态断言在base与候选均失败，属已有问题，未为本功能改PDF文案或删除断言；正式Flow结论另记。
- Flow预检4403172配置无VMDeploy/SSH/主机安装，triggerEvents为空。旧flow-control 1.1.0因运行历史超过100条在发请求前拒绝（RUN_HISTORY_REQUIRES_RECONCILIATION），只读确认未创建Run后，任务专用SDK脚本分页读完400条历史、固定配置hash及远端SHA再单次启动412；不改公共控制器、不重试不明写入。来源/终态/制品见后续核验。
- 本次用户仅要求功能，不安装、不启动生产服务；线上状态不随develop或Flow成功改变。

### Flow412真实失败归因
- 412来源确为上述8326273；主作业在执行测试前被云端配置残留 `test "$CI_COMMIT_SHA" = 74d53da9962201ae59d0b0ec6eab17f771c6f409` 拒绝，代码扫描成功，Run终态FAIL。不将其作为必要测试通过，不复用其制品。
- 配置hash匹配预检但预检未检查硬编码旧SHA，首跑产生不必要缓存准备费用；以后本任务启动先检查此固定来源guard，不修改项目/共享技能规则。保留来源锁定而非删除guard，仅将该值换为获本任务授权的固定候选。配置写前分页核对无活动Run、私有state保存完整前值；readback与后续Run另记。
- 日志API含环境声明，现有脱敏器未完全识别转义敏感字段，落盘证据已收口为失败guard/ERROR尾部，不保留凭证声明，不修改共享技能。

### 正式回归修复及最终候选
- 413实际执行3709通过/2pending/2失败，未构建可发布包。两处失败均为受影响旧测试未同步：Bounty inline-results测试桩缺少真实richDocumentKind依赖；multimedia测试仍将HTML视为UNSUPPORTED且未模拟授权原内容响应。已补真实依赖/Blob fixture，HTML断言改为静态document并验证脚本被清洗，SVG/ZIP/视频/未知格式仍unsupported；不删除原权限、MIME、摘要及大文本保护断言。相关96项本机通过。
- 补齐资料上传/追加版本的file input accept，允许.html/.htm/.md/.markdown及对应MIME；完整资料组件验证实际文件选择器属性。嵌入与完整资料详情继续使用同一accept定义。15组受影响轻量套件最终198通过（targeted-tests-final.log）。
- 等待期间其他Owner占用Web414（startup-perf），没有改其配置、取消或重复启动。本任务只读确认414成功及原配置已恢复；其源码13d56e4整合了本功能早期候选4df3044，但缺少最终选择器修复，不用作本最终制品。远端develop并发前进后本任务一次rebase保留其全部修改；没有强推或重写他人提交。
- 最终Web版本**1.16.98**，develop **b0404c4042c90d6bf862b54db2b2ff9ee3405bf3** / tree **9a1d856b163501a87486ff15d9c3b1ecf4e51fff** 已push。将现有来源guard精确换到该SHA，私有state保存前值、同400条历史核对无活动Run及readback成功；配置其余测试/worker-only/上传不变。
- 唯一最终正式Run **4403172/415**，启动05:04:24 UTC（13:04:24 CST）；前412/413失败保持，不标成功。完整终态、制品摘要及收尾见后续记录。本任务没有部署授权，不安装、不操作生产服务。

## 最终收口（2026-11-03）
- **Flow4403172/415 SUCCESS**，来源develop `b0404c4042c90d6bf862b54db2b2ff9ee3405bf3` / tree `9a1d856b163501a87486ff15d9c3b1ecf4e51fff` / Web1.16.98。3712 passing、2 pending、0 failures；测试报告duration58243ms，Vite构建13.18s，JS扫描成功，制品上传成功。首次观察Run SUCCESS距开始小于200秒，满足600秒总上限。pending为既有状态，未删除必要用例来过构建。
- 通过本Run的GetPipelineArtifactUrl元数据取得制品，签名URL仅在内存使用。包109709062字节，SHA-256 **afb8d712e716e83db4cc64b282b00dfc35d9149990c56a05c1bc7482f0892be8**；存于 `/home/isp/state/html-md-preview-flow-20261103/web415.tgz`（0600）。只读扫描归档路径/类型、核对固定commit/tree/version及612个dist文件全部SHA/size；不解压安装、不运行生产服务。后续获授权安装可复用该固定制品，不为下载/安装重跑构建。
- 完整证据：`docs/implementation/evidence/html-md-preview-20261103/final/{flow-status.json,flow-job-summary.json,source.json,artifact-download.json,artifact-verification.json}`；前412/413真实FAIL及他人414归属另存，不冒充本次最终验证。
- 稳定使用与安全边界已回写既有 `docs/juyiting-runbook.md`，原型/任务规格已同步。主根/Web的其他Owner脏变更和旧主工作区分支保持原样，不整体stage，不以旧主工作区HEAD更新gitlink。
- 本任务正式构建通过，**未部署、未安装、未做线上业务验收**；不推断其他Owner的生产操作状态。来源/配置前值和制品在任务私有state可追溯。定位/实现/等待未单独计量，不能宣称整体缩时或成本收益。

- 已确认最终候选在远端develop；本任务唯一worktree、node_modules链接及本地任务分支已清理。未清理其他任务、生产状态或备份，既有原型18786服务继续复用。

## 用户追问：议事与选择资料入口补漏（2026-11-03，实施中）
- Owner：当前任务；目标为原型上传/议事附件/选择资料（含已选资料独立弹窗）的HTML与MD实际预览，非目标为API合同或生产部署。先更新唯一原型及规格，再补产品消费者。
- 读取远端develop于本轮开工，基线ea1c2e8；主Web脏工作区不覆盖。因组件与原型路径有其他任务脏改，使用唯一隔离树 `/home/isp/wsps/worktrees/preview-entry-fix-20261103`，分支 `codex/preview-entry-fix-20261103`。
- 已确认：HallMaterialPicker两处模板仅支持图片/音频/文本，遗漏workspace现有document结果；HallMessageMedia将HTML/MD归为file而不加载。原型内置HTML的议事弹窗可生成srcdoc，但上传保存占位文字、无MIME的html/markdown未读正文；必须补真实入口回归，不能拿renderer的六组测试当全部入口验收。
- 责任层：Web展示，复用既有RichDocumentPreview和固定版本/会话授权内容读取。保留MIME检查、身份/版本切换取消；不改API、Runtime，不部署。
- 基线纠正：进一步核对隔离树，ea1c2e8（并行议事修复）已在HallMessageMedia接入共享HTML/MD渲染及PDF/文本；前述“归为file而不加载”为主工作区旧源码现象，并非远端基线。保留其实现，补实际消息入口验证，不重复实现。HallMaterialPicker远端两处模板确实仍缺document分支。本轮原型脚本资源版本也同步更新，避免页面ui参数变了但子脚本仍复用旧缓存。
- 沿消费者扫描另确认HallDraftEditor私人事项成果固定版本区遗漏document（含parts）；已复用同一组件补齐。不改缩略图文件图标策略，不改身份/ACL或内容接口。议事的当前远端实现保留并通过真实组件入口验证。
- 本机定向8套140通过（`entry-fix/targeted-tests-final.log`），覆盖选择资料两处模板HTML/MD、空文件/错误/身份切换、固定旧版本、私人事项成果及原媒体回归。早期新增断言错把身份切换清空引用当失败，已修正为预览不改选择、身份切换按原规则清空；早期2秒测试超时受并行本机诊断影响，最终串行按原测试选择重跑，无业务校验放宽。
- 浏览器：真实HallMaterialPicker（侧栏/手机、已选固定版本弹窗）与HallMessageMedia，使用真实RichDocumentPreview/DOMPurify/marked、仅文件I/O fixture，1440/390/320共15入口，opaque sandbox、正文/脚本清洗、无页面溢出、授权会话路径和固定v1通过（`entry-fix/product-browser/results.json`）。不是认证线上业务验收。
- 唯一在用原型18786：24入口预览（HTML/MD/无MIME HTM/Markdown ×议事附件/选择资料×三宽度）通过，补实际上传保存正文、旧上传data URL恢复正文、自定义显示名称和空文件；原型资源版本随文件摘要更新。原型启动/iframe需等待实际就绪，早期固定短等待已改为就绪条件，不用延时失败宣称页面缺功能。
- 远端并行前进至5efec28；保留对方流式消息修复后rebase，冲突仅规格末节同时保留双方条款。候选Web1.16.100，develop `fcbdf0fd1a26b5f1231e41b1d49a01d0243ff603`，正式云端结果另记；不复用415包冒充本轮。
- 候选独立原型也在18787临时只读静态服务执行同一24入口、上传/旧上传/自定义名称/空文件回归通过（`entry-fix/candidate-prototype/prototype-results.json`）；已停止本任务18787服务，保留原18786服务。避免把脏工作区原型结果直接当候选源码结果。候选上传路径复用新抽取的readPrototypeFiles，既有其他Owner的主工作区助手函数不直接当作候选已存在。
- Flow启动前重新分页核对无活动Run（417为其他Owner已成功），私有state保存当前配置前值，仅将原固定5efec28 guard替换为fcbdf0f，不改变全量测试/worker-only构建/上传；readback APPLIED。真实Run4403172/418于08:16:45 UTC启动，无安装或主机调用；600秒总限保持，终态另记。控制面证据`entry-fix/flow-*.json`，完整配置前值在`/home/isp/state/html-md-preview-entry-fix-20261103/`（不公开凭据/原始完整日志）。

### 入口补漏最终结果（2026-11-03）
- **Flow4403172/418 SUCCESS**，确认为develop `fcbdf0fd1a26b5f1231e41b1d49a01d0243ff603` / tree `66c4b500bbefb878bdfee6fd2a9adcf0bdeccfa3` / Web1.16.100。**3726 passing、2 pending**；必要全量回归、Vite（13.70s）、JS扫描及612文件的制品导出/上传均成功。08:16:45 UTC启动响应，08:20:21已观察到SUCCESS，小于600秒总限。
- 固定来源与入口指纹见`entry-fix/source.json`；权威源码/作业状态见`entry-fix/flow-detail.json`；仅摘取非敏感测试/构建摘要，不保留原始完整环境日志。418新制品未下载/安装，未做生产认证业务验收；不得把415包用于本轮版本。后续如获部署授权，从418固定制品读取并核对SHA/manifest，不再重复构建精确已验证输入。
- 本轮唯一候选已推送develop；主工作区与其他Owner脏改保持，根gitlink不以其旧HEAD更新。原型18786继续服务。本任务候选临时服务已停，证据保留，唯一任务worktree与分支随后清理。
- 清理已执行：仅删除本任务node_modules链接、干净worktree及任务本地分支；不清理其他任务、生产状态或备份。远端develop仍为fcbdf0f，源码可恢复，证据保留。原型资源服务18786不变。
