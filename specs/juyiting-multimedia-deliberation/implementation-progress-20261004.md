# 分版本开发：第一批源码进度

2026-10-04。用户已明确恢复开发并要求按版本节奏落实；本记录是源码与验证回执，不是第二套运行台账，不是发布/用户验收证明。

## 分版本节奏

1. **入口与输入增量（T01–T04）**：复用现有创建/点将/资料/语音，先让主入口清楚、点将直接议事、＋输入方便、仅附件可发。
2. **成果与验收增量（T05–T06）**：明确本次成果与替换关联，补纯文字交付，去掉验收多选，复用现有 finalization。
3. **实际闭环与发布收口（T07–T09）**：边做边验证 Agent/媒体/保存/恢复，改动组件走既有正式 Flow，核对上线后业务闭环。

具体发布编号在就绪时读取线上版本、release refs 和在途 Run 后分配，不预留或覆盖历史 1.13.45–1.13.47。不为凑版本发布空增量，不增加审批或第二条流水线。未完成的第一批不抢先上线。

## 本轮已经改源码

Web 独立候选 `codex/mmd-ui-input-v1-20261004`：`58d631da0b0c1cccebf152f2f95b350db4bbe9a9` / tree `b7b81093d8796578c78c871fe443ebd8a005a872`，已推送并独立远端读回。基于任务清单指定 Web 候选 `12edde24`，不是旧根 checkout；未更新 SDD gitlink/pin，未合 develop。

- T01：事项主入口合为“提出需求”，正文必填；既有正式/私人领域编辑路由仍保留。资料选择器不再要求用户挑版本，沿用精确版本冻结、预览与下载。
- T02：点将册新增针对待点将事项的“点将并议事”；按钮传显式 Agent，父级传当前真实 task 并复用原 point-and-start。无待办只留密议；密议不调用点将接口。
- T03：资料、工作空间、历史/重取/另起话头和语音操作收进＋；资料目录与语音位于输入区域，顶部保留状态与取消。菜单支持外侧/ESC关闭、焦点恢复和上下文切换收起；语音停止转写先追加可编辑草稿，不自动发送，不改变其他语音入口的自动发送偏好。

以上为上一批 T01–T03 源码记录，验证仍非真实 API/Agent 产品验收。T04本轮已配套实现，最新候选及验证见下节；第一增量尚未发布。

## 实际验证

- 精确提交上 8 组定向 Web 测试：**229 PASS / 0 FAIL**。包含真实挂载组件与新增菜单、Agent CTA、转写入草稿回归；既有 HTTP/Agent mocks 不冒充真实 Provider。
- 本地 `npm run build` 通过，只作研发验证；有既有 chunk-size warning，未新增大小门禁，未发布本地制品。
- 改动小组件/voice composable和新增测试 scoped ESLint通过；BountyPanel既有11条、JuyiHall既有187条诊断保留，与原候选比较新增0。不宣称全仓 lint 全绿。
- `git diff --check`通过；原主工作区的脏 api、日志及其他分支未覆盖。

原始测试/构建/ lint日志及基线比较用gzip保留原始字节，manifest同时绑定压缩文件与解压原件SHA-256，避免Git换行归一化破坏回执；证据：[一次合并回执](implementation-evidence-20261004/ui-input-v1/manifest.json)。

## 本轮继续：T04附件-only已形成配套源码候选

Web `codex/mmd-ui-input-v1-20261004`：`f927f344ff24c07f92030a8c35140475b35a35b9` / tree `326034da26c72f9b3f37d926349596938abcd815`。
API `codex/mmd-attachment-only-v1-20261004`：`7a9418c3c4dfa5d4850b7eb02b091bdbaa2de88b` / tree `a6e4f83f0d4f17fead130c85e7467ac586e6ef8a`。
两个候选均已推送并独立远端读回；原统一资料候选分别是父基线，不覆盖其分支，不更新SDD集成pin/gitlink。

- Composer仅在typed bounty有选中精确附件时放开空正文发送；公议/密议及交互锁仍按原限制。Wire保留schemaVersion1及数量/长度合同，双空、坏引用仍拒绝。空白正文按实际字节留存，不补造用户文字。
- 后端仅由服务器鉴权解析后的typed目录允许空正文；客户端metadata不能放行普通chat。保留 task/owner/target/generation 校验、精确版本、原正文及附件的幂等摘要、澄清关联。
- 原USER保存解析后的精确资料引用，前端显示对应资料卡和版本，历史空正文不丢ID/hash；资料卡不出现在密议或其他事项。历史metadata只作展示，不能作为读取/执行授权。
- 原USER续办仍核对所属request/turn/snapshot和真实正文hash；INSPECT复用原USER、原请求键，不插入人工正文或把Agent指令当用户许可。网络未知恢复不自动换键重发。

### 本轮实际验证

- Web **311 PASS / 0 FAIL**，12组定向测试，包含挂载附件卡、空白发送限制、原键/原正文/精确版本恢复以及既有入口、点将、语音回归。
- 当前Web源码 `npm run build`通过，仍仅是本地研发验证；保留既有chunk warning，不冒充正式发布制品。
- 本次生产源码和小测试scoped ESLint通过。两个改动的大测试文件既有5/7条诊断仍是5/7，新增0；不宣称全仓lint全绿。
- API通过既有锁定orchestrator、普通Gradle依赖/编译图执行5组定向JUnit：**50 PASS / 0 FAIL / 0 ERROR / 0 SKIP，natural exit0**。涵盖Wire、durable admission、原USER续办、context鉴权及精确引用；这是无数据库单测，不是Flow正式云测、真实Provider或业务验收。
- 原始失败保留：API v1新缓存缺settings plugin，改用源码include-build与已有test-only发布占位；v2新增测试错误引用constructor局部sender，按真实编译错误修复。挂载附件卡发现误用函数名，修复后311项通过。未禁用AP、覆盖旧class、伪造skip或重跑付费动作。

原始日志及JUnit XML合并保存并校验压缩/解压SHA-256：[本轮回执](implementation-evidence-20261004/attachment-only-v1/manifest.json)。

## 本轮继续：T05改稿关联子增量（部分完成）

Web `codex/mmd-ui-input-v1-20261004`：`b1f807c717714f0eebc0b98014ad9b8a2084a6cb` / tree `c90a562e6a78c35429a4e86518397cb06f87a02f`。
API `codex/mmd-attachment-only-v1-20261004`：`0ff0322b08ab5c01208e7bb764be72ce3d4849e3` / tree `434913fd4dd7fefe06cd5ed3060c5805b1aeec5c`。
两个候选已推送并独立远端读回；不更新SDD集成pin/gitlink，不覆盖原脏工作区。

- 现有成果目录补可选 `replaces` 精确来源（request/step/output/hash），仅来自服务端持久v3 EDIT_IMAGE输入清单并核对原摘要；新生成时的参考图、工作空间图片编辑不会冒充替换旧会话成果。读取仍经过owner/task/assignment/grant与真实字节校验，Chat另外检查父成果请求的相同会话generation/task/Agent。
- Web目录验证、冻结上述关系，成果卡显示改稿关联并保留历史稿。新增纯函数仅对**已明确的初始清单**应用精确替换，保留其他项，拒绝失效父稿/歧义分叉；重建后冻结所见引用，不从历史或MIME猜测当前集合。
- **生产验收尚未接入该重建函数；初始交付清单来源仍需明确持久引用。** 当前没有隐藏checkbox后自动选择历史成果，也没有声称T05/T06完成。纯文字完成消息的鉴权/快照正式交付分支仍待实现。

### 实际验证

- Web8组相关定向测试 **208 PASS / 0 FAIL**，包含目录/真实挂载gallery/恢复/inline results/finalization/任务刷新及会话组件；`npm run build`自然exit0。仍为本地研发验证，既有chunk和mock环境警告保留。
- 目录源码与小测试scoped ESLint通过；gallery既有诊断baseline13/current13，rule/message元组一致，新增0。不宣称全仓lint通过。
- API通过既有orchestrator/Gradle锁、普通依赖与AP编译图执行3组定向JUnit：**55 PASS / 0 FAIL / 0 ERROR / 0 SKIP**，Agent与Chat任务均natural exit0。包括真实服务方法的owner/root/source digest路径与原有回归；无数据库/真实Provider，不是Flow或业务验收。
- 原始Web失败保留：v1测试用URL.pathname造成Windows重复盘符，改为fileURLToPath；v2两项静态测试依赖旧self-closing slot和空行，用真实标签定位纠正后208通过。没有改生产逻辑规避断言。

原始日志、JUnit XML、来源Git blob/测试工作文件hash及压缩hash见[本轮合并回执](implementation-evidence-20261004/output-lineage-v1/manifest.json)。Windows CRLF工作文件与LF blob只允许换行归一化差异，分别记录原始SHA-256。

## T05/T06：事项详情媒体验收接线子增量（2026-10-04，部分完成）

Web `f0f4d1fced43effbb37a216351e7e145813ff7d0` / tree `84d5b90a894cebab4243ba5656208ecfdda439f9`，仍在 `codex/mmd-ui-input-v1-20261004`，已推送并独立远端读回。API源码未改，沿用上轮 `0ff0322b08ab5c01208e7bb764be72ce3d4849e3` 的有效来源合同/55项测试证据，不宣称本轮重跑API。

- 验收操作移到事项详情，议事卡保留历史稿、预览/下载/可选保存，不再有checkbox。事项页只读本次成果，复用原finalization；点击确认时提交当时实际显示的精确来源，保存不是前置。
- **当前支持边界**：现有持久输出中仅有一个独立committed manifest批次时，将该明确批次及精确改稿关联接入生产页面；按request/step/output/hash替换一项，保留其他图/音频/文件。多轮改稿依父链重建，不依网络到达顺序。多个独立原始批次、分叉改稿或失效父稿一律提示回议事澄清，**尚未实现澄清后追加/重置交付意图的持久读取**；不是通用当前清单完成，不自动并集所有历史或挑同MIME最新版。
- 已开始/完成的验收继续显示冻结原引用，晚到新稿、刷新或remount不替换原内容；未知响应仍查/恢复原operation与key/body，不重跑工具。
- 事项页只读原owner/task作用域下的现有conversation/list和requests。冷读来源不唯一不猜最新；明确原会话在既有分页中查找，身份/任务/会话切换立即清理并隔离晚到响应。非法目录/权限或读取失败不能降级到旧验收路径。没有原生请求记录的既有正式事项仍由原FormalTaskDeliveryPanel领域服务处理；资金榜和明确delivery review路由保持原样，私人事项路由未改变。
- “继续修改”只返回原会话；正在同一会话时不重置对象/草稿，跨分页只选择原history条目，身份切换或正在处理其他会话时停止切换。不点将、不创建/发送、不插入新草稿、原成果不改写。

精确提交上10组相关测试 **235 PASS / 0 FAIL**；本地build自然exit0，仍保留既有chunk及mock环境警告，非Flow/真实Agent/发布验收。小组件/新增hook/catalog与相关测试scoped lint通过；与上一提交比gallery13→12、BountyPanel11→11、JuyiHall187→187、大组件测试7→7，rule/message无新增诊断。最终Git blob与测试工作文件只允许CRLF/LF差异，回执见[合并记录](implementation-evidence-20261004/task-acceptance-v1/manifest.json)。

## 下一实际缺口

第一增量T01–T04的最小源码差异已接齐，**尚未整体联调/发布/用户验收**。第二增量T05/T06已接通上述单批次媒体清单、只读事项验收及返回原会话，但仍需补多独立批次的明确交付意图与纯文字来源分支；不能将该子增量标成T05/T06整体完成。仍复用现有finalization，不自动勾选全部历史成果，不新建交付集合服务。

随后在实际闭环中核对T07/T08，并按T09使用既有正式Flow测试/同Run制品发布及上线验收。Client本轮未改源码，真实空正文到Agent的配对闭环尚待联调；不将静态检查或mocks算成产品通过。未新增付费Provider调用、生产数据/迁移、Flow Run、release ref或部署。

## T05：纯文字可信来源与现有正式交付内部适配（2026-10-04，部分完成）

API `codex/mmd-attachment-only-v1-20261004`：`a847c3d42421ecf61c9828b23744b951cd997fb7` / tree `0b7e10d17d5e898ec091bb50fe8b8d7a654964c3`，已推送并独立远端读回。Web未改，沿用 `f0f4d1fc` 的235项既有证据，不冒称本轮重跑。

- 只读来源直接校验已有v3 CHAT完成消息、typed admission、任务/owner/client/会话generation、实际快照及重建的finalDigest；读取原ASSISTANT字节，中文多行/末尾空白不改写。未完成、CLARIFY/ACTION_REQUEST、消息/快照/正文/摘要/任务或assignment不一致均拒绝。不会扫描/自动选择回答，寒暄不自动成为交付。
- 实际自然议事没有interaction-step行，故文字来源使用真实request/turn/message/snapshot，**不伪造stepId、executionId、runId或outputId**。媒体保留原step/output链；文字不要求先保存空间或生成文件。
- Agent可信内部来源union支持文字和混合来源；复用现有真实lease/artifact/正式提交/owner验收。当前grant/assignment仍由原promotion机制校验，不把文字读取结果当执行授权；原媒体摘要已有独立固定值回归，不更换在途原键/原正文。
- **本轮尚未改公开HTTP媒体-only合同、existing-items持久字段或接上事项页文字验收**。当前仅可信来源及Agent内部适配完成，不能声称用户已能纯文字直接验收，T05/T06整体仍是部分完成。

精确API提交上既有锁定orchestrator、普通依赖/AP编译图的9组定向JUnit：**112 PASS / 0 FAIL / 0 ERROR / 0 SKIP**，Agent/Chat任务均natural exit0。真实final reader与snapshot/finalDigest破坏测试、UTF8原文、混合来源、虚构执行/步骤拒绝及原媒体权限/恢复/严格wire/schema回归均通过；无数据库、真实Agent、Provider或Flow业务验收。保留首轮57项中的2个fixture失败及原日志/XML，按实际发布bytes修fixture；未修改生产逻辑绕过断言。原始日志、JUnit、失败记录、精确Git/远端测试源hash见[合并回执](implementation-evidence-20261004/completed-message-v1/manifest.json)。

下一步仍是将明确文字来源接入**现有**HTTP selectedOutputs及原items持久记录/恢复，再接事项页只读展示；同时补多独立批次追加/重置的明确交付意图，不新增delivery-set服务/表/状态机。未做生产迁移、Flow、发布或付费调用；本轮无新增需用户决定的范围事项。

## T05：文字验收HTTP、原条目持久化及恢复接线（2026-10-04，部分完成）

API `codex/mmd-attachment-only-v1-20261004`：`88243a317bd32f0495f8c9d9041e3e3582f764d4` / tree `3a9087b100b2737c255131a79519ace2376f97a1`，已推送并独立远端读回。生产实现位于父提交 `ba984d2b`；最终子提交只补两份组合测试。Web仍未改，不重跑未变更235项/本地构建。

- 原 `/agent/tasks/{taskId}/finalizations` POST接受原6字段媒体项或文字5字段项（requestId/sha256/title/purpose/messageSource）；文字messageSource严格含turnId/messageId/snapshotId/finalDigest。messageId保持十进制字符串，支持JavaLong最大值、不经JS数字截断；不存在伪造step/output/run或浏览器提供grant权限。支持有序混合来源，混杂字段、未知字段、重复来源、非规范/越界ID均拒绝。
- 原 `chat_selected_output_finalization_item` 补来源kind及真实消息/快照字段，文字step/output为NULL。继续原operation/key与GET按key/operation恢复，只读GET不推进；receipt校验条目重建的原requestDigest，持久引用被改写时拒绝而非偷换内容。已完成/已提交操作先恢复实际Agent记录，不重读过期来源或再跑工具。
- 文字的当前grant仅由服务器在既有owner task-root锁内解析，沿用原active grant、资料/requirement和assignment校验，Agent.prepare仍再次校验；不获得工具/付费授权。继续原lease/artifact/正式提交/owner验收，不新建交付服务、表或状态机。
- 新建表DDL及原条目表的一次升级SQL已写入源码，schema initializer核对来源列/唯一索引/check/nullable。**既有表升级不在启动时自动执行**；正式发布时须按原授权流程与API配套迁移。本轮未对生产执行DDL或数据写入。

实际验证：10组定向JUnit合计 **124 PASS / 0 FAIL / 0 ERROR / 0 SKIP**，由父提交Agent59 + 最终提交Chat65组成，三次Gradle任务natural exit0。Agent生产/测试及SQL字节在最终test-only子提交未变更，故不冒称新树上重跑Agent。新增组合用例使用真实HTTP parser、Chat store、完成来源及原final reader，确认中文多行原文/实际快照、正式进度与原键只读/重放不重复读源；JDBC、身份与Agent/grant边界仍为fixtures，不冒充部署JWT/Spring/真实Agent验收。

另在**独占新建datadir、关闭网络、独有socket**的MySQL **8.0.21**执行24项SQL检查：fresh与旧schema升级、旧operation/key/digest/媒体条目不变、文本/媒体共存、NULL/零/前导零/溢出ID/错误digest/虚构step/output/未知kind/重复消息拒绝；24项通过。两个自有测试数据库已删除，自有mysqld正常退出，不复用或操作生产及其他任务实例。原始DDL/catalog、日志/JUnit和复用字节hash见[本轮合并回执](implementation-evidence-20261004/text-wire-v1/manifest.json)。

**仍缺**：事项页纯文字的只读展示/验收接线，以及多独立批次明确追加/重置交付意图。不能据本批后端通过把任意ANSWER、最新消息或寒暄自动变成交付，T05/T06整体尚未完成。未调用Provider、Flow、生产迁移、release ref或部署；本轮暂无需用户决定的范围事项。
