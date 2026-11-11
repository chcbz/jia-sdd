# 资料管理：代码级修复设计


> **发布后剩余问题的当前详设与实施计划见§17**（2026-10-16）。§5/§6/§11/§12的扩展性旧拟案不直接作为实施指令；前端1.16.2已由Flow215发布，§16未发布状态为历史。
> **当前交付：§16为已实现的必要前端修复；本地自检/原型检查通过，正式Flow待完成，未部署。其余拟方案仍按§15收敛。**

> **最新范围决策（2026-10-16 16:10）：以§15为准。撤回默认全量返回值重设计、强制持久化门禁、select自动加载历史及追加选择行为改变；F13生产等价性待证，不再默认先改公共层。前述方案中冲突内容保留作历史。**

核对日期：2026-10-16（Asia/Shanghai）。Owner：本聊天 Codex。任务沿用 `WORKSPACE-MANAGEMENT-AUDIT-20261016`，本次交付为设计补充，**未实施、未编译设计片段、未部署**。

基线：Web `2c8d6703eead623f555029341101cb688b9d448a`；API `fc399976710f5b724916013926be2cbff899af8c`，本次复查两组件干净。远端基线沿用原查询；续核验补了7个安装类SHA一致证明，但没有整包安装回执闭包，不声称当前线上与源码整体一致。接口权威 `/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.2（2026-10-14）。

原审计与测试证据：`/home/isp/wsps/cyf/docs/implementation/WORKSPACE-MANAGEMENT-AUDIT-AND-REPAIR-20261016.md`。以下示例均为**拟实现代码/契约**，不是已存在 API；须与实际 DTO、schema、测试同时落地。

## 1. 是否全部核实（15:12续核验更新）

可执行的隔离调查已完成补证，**不能回答“所有功能已验收通过”**。最新完整证据矩阵见审计报告开头“继续核验收口”：旧后端fixture已迁移并104/104通过；新增真实MySQL/资源安全链聚合诊断通过，14条观察包含6条已知错误复现；真实浏览器8条观察包含2条错误复现。F07/F08、usage混合快照、追加revision和关联弱ETag现已取得运行证据，不再仅为源码推断。

新增F12同key竞争异常及F13公共关联头重复，代码级方案见本文§11–12。原始浏览器链被F13阻断；下游UI通过只成立于测试代理显式去重同值请求ID头的诊断条件，正式修复验收必须去掉干预。生产15:07:43仍502/10018无监听，不能完成在线登录验收；历史日志不记录If-Match，无法据此重建原失败请求头。

以下原源码补充保留，执行证据以上述更新为准；拟修实现仍未落地。

### 本次代码复查补充（源码事实，未新增运行证明）

1. 两个关联 composable 也校验响应 ETag：任务关联只接受精确强ETag（特定缺头分支另有处理），会话关联要求响应强ETag；弱头可能使**已提交关联被前端报为无效回执**。并入F01/F04范围，不能只修文件删除。
2. `PersonalWorkspaceWriteService.completeAppend`更新latestVersion但不增加metadataRevision；如果回收确认显示了旧latestVersion，追加完成不会必然使旧确认CAS失效。方案明确把追加纳入metadataRevision变化，并补并发用例。
3. 活跃执行查询实际是 `grant_state='ACTIVE' AND execution_state='QUEUED'`，不是所有历史授权；新UI必须写明“待执行授权”，不能把它称为全部引用/撤销全部授权。

## 2. 修改文件地图

|绝对路径|修改函数/类型|对应问题|
|---|---|---|
|`/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspace.js`|select、refresh/loadMore、upload/appendVersion/mutate、usage/trash、download/previewVersion；增加版本分页/关闭详情/恢复意图入口|F01–F10|
|`/home/isp/wsps/cyf/web/src/components/workspace/PersonalWorkspace.vue`|selectedVersion、byteText、nextVersion；所有预览分支；open/close/upload/confirmTrash/restore；两个展示模式同步|F02/03/05/06/08/09/10|
|`/home/isp/wsps/cyf/web/src/components/personal-workspace/TaskMaterialLinks.vue`|selectedVersion下拉、canAttach字符串校验、关闭/版本分页消费者适配；§13新增源码定位|F02/共享消费者回归|
|`/home/isp/wsps/cyf/web/src/components/juyiting/HallDraftEditor.vue`|resultPreviewVersion下拉、成果历史previewResultVersion、版本分页消费者；§13新增源码定位|F02/08|
|`/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspaceTaskLinks.js`|etagFor/validEtag、attach/detach的幂等意图|F01/04扩展|
|`/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspaceConversationLinks.js`|同上；禁止已提交操作因弱头伪报失败|F01/04扩展|
|`/home/isp/wsps/cyf/web/src/utils/personalWorkspaceProtocol.js`（拟新增）|提取现有DECIMAL/VERSION/REVISION及业务CAS构造，不新增全站解析器|F01/02|
|`/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspaceWriteIntent.js`（拟新增）|单意图key/在途promise/UNKNOWN恢复；存储沿用execution recovery的身份隔离与readback模式|F04/10|
|`/home/isp/wsps/cyf/api/agent/jia-agent-api/src/main/java/cn/jia/agent/service/PersonalWorkspaceService.java`|operationByKey服务方法；usage返回新摘要|F04/06/07|
|`/home/isp/wsps/cyf/api/agent/jia-agent-core/src/main/java/cn/jia/agent/entity/PersonalWorkspaceViews.java`|UsageView/UsageCounts，保持服务层整数类型|F06/07|
|`/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/PersonalWorkspaceController.java`|新增只读原key查回执；usage继续统一信封|F04/06/07|
|`/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/PersonalWorkspaceWire.java`|usage显式投影D0/D1字符串|F06/07|
|`/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/PersonalWorkspaceServiceImpl.java`|operationByKey复用现有DAO；usage委托一致快照服务；同步构造注入/测试fixture|F04/06/07|
|`/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/PersonalWorkspaceUsageService.java`（拟新增）|独立代理事务读取usage，避免同类自调用失效|F06/07|
|`/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/PersonalWorkspaceWriteService.java`|completeAppend增加revision；保留requireMatch；trash不靠读取100行证明确认完整|F06/07|

Mapper层修改的确切类：`PersonalWorkspaceTaskLinkDao`/`PersonalWorkspaceConversationLinkDao`及各自`Impl`，`PersonalWorkspaceExecutionDao`/`Impl`，`PersonalWorkspaceTaskFileLinkMapper`、`PersonalWorkspaceConversationFileLinkMapper`、`PersonalWorkspaceExecutionInputMapper`，均在 `/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/java/cn/jia/agent/` 下。新增count接口不使用默认返回0的实现掩盖漏接线。

## 3. F01/F02：业务版本与字符串标量

### 3.1 不把HTTP表示ETag当业务版本

复用现有校验并提取到上述protocol helper；ID用于头值还须拒绝双引号、反斜杠及控制字符，避免非法ETag，不扩大现有fileId wire格式。

```js
export const decimal = value => typeof value === 'string' &&
  /^(0|[1-9][0-9]*)$/.test(value) && BigInt(value) <= 9223372036854775807n
export const revision = value => decimal(value) && BigInt(value) >= 1n
export const version = value => revision(value) && BigInt(value) <= 2147483647n

// validId复用现有ID约束；不从任意响应头删W/后充当写凭证。
export const revisionTag = (id, rev) => {
  if (!validId(id) || /["\\]/.test(id) || !revision(rev)) {
    throw new Error('资料版本标识无效，请重新读取。')
  }
  return `"${id}:${rev}"`
}
```

- `select`存 `businessTag = revisionTag(data.file.fileId, data.file.metadataRevision)`。可另存responseEtag用于诊断，不用其生成写请求。
- `mutate`发起前固定fileId/revision/tag，不能等回包时再读当前detail。rename/restore取详情快照；trash取用户确认的usage快照。
- 写回执必须验证 `data.fileId === intent.fileId`；upload的fileId/version.fileId一致、append的目标fileId一致；detail的file/latestVersion/所有versions.fileId必须匹配请求目标。
- `replaceFile`拆成只更新列表和显式有guard的详情更新，避免辅助函数偷偷绕过视图隔离。
- Task/Conversation link用 `relationId+relationRevision` 构造业务tag。有效body足以处理回执；响应强/弱/缺失ETag不能改变已提交结论。若头与body不一致，记录协议异常并只读复核，不重复发写请求。
- 后端 `requireMatch`继续严格比较；不接受`*`、任意弱tag，不关闭gzip，不删除ACL/CAS。

### 3.2 组件字符串修正

```vue
<select v-model="selectedVersion" @change="preview(selectedVersion)">
  <option v-for="item in workspace.versionItems.value"
          :key="item.version" :value="item.version">v{{ item.version }}</option>
</select>
```

```js
const selectedVersion = ref('1')
const nextVersion = computed(() => {
  const current = workspace.detail.value?.file.latestVersion
  return version(current) && BigInt(current) < 2147483647n
    ? (BigInt(current) + 1n).toString() : null
})
// download/previewVersion默认参数都改成：
// version = detail.value?.latestVersion?.version
```

- 达INT上界禁用追加并明确说明，不显示溢出版本；服务端追加预校验上界，避免Math.addExact溢出被归为存储故障。
- `byteText`使用BigInt整数缩放（B/KiB/MiB/GiB/TiB/PiB/EiB），小数用余数计算；0显示0 B；非法值才显示未知，绝不直接Number转换64位字节数。
- selectedExecutionVersion、download文件名查找均使用版本分页缓存。找不到所选版本时先读对应版本页或明确报未加载，不偷偷回退latest的文件名/元数据。
- 预览在参数校验失败时也清旧内容并显示错误；正常请求开始即记录 `{fileId, version, kind:'loading'}`。成功、失败、下载、起草绑定同一字符串版本，不允许标题是v1但内容是v2。

## 4. F03/F05/F10：拆开三类异步状态

### 4.1 详情视图与写入意图

```js
const captureView = () => ({
  identityGeneration: generation,
  epoch: currentEpoch.value,
  detailGeneration,
  fileId: detail.value?.file.fileId ?? null
})
const ownsView = s => !disposed && s.identityGeneration === generation &&
  s.epoch === currentEpoch.value && s.detailGeneration === detailGeneration &&
  s.fileId === (detail.value?.file.fileId ?? null)
```

实际请求仍走现有`request/useHttp`身份和AbortController链，不另造认证客户端。

- 新增`closeDetail()`：增加detailGeneration，清详情/预览/确认；组件所有返回路径调用。开始选B即使B尚未返回，也必须使A写回执失去视图归属。
- mutation按fileId保存状态，不能一个actionState混装详情加载/预览/上传。建议 `detailState`、`preview.kind`、`writeIntents`，旧actionState仅由它们派生，最终移除重复状态赋值。
- 每个写意图保存请求目标、输入、businessTag、viewToken。A迟到结果可以记入A的操作记录，不能覆盖B、关闭B详情或改当前列表筛选。列表更新也须匹配当前query/state；无法可靠局部重排时使当前列表失效并按当前条件重查。
- 同一fileId写操作串行；不同文件可以独立。旧revision回包不得倒盖新revision；成功写后若视图仍归属原操作，重新读详情。追加期间保持用户选定旧版本，只有用户明确打开最新版本才切换。
- 组件`uploadTreasure/restoreTreasure/confirmTrash/openTreasureFile`各自捕获UI导航代次（不仅composable详情代次），await后校验，防止迟到回执重置用户新选条件/新填表单。旧表单只在原意图匹配时清空。

写函数目标返回形状（内部JS，不是新的HTTP信封）：

```js
{ status: 'committed', operationId, fileId, version,
  viewApplied: false, detailStatus: 'not-requested' }
// detailStatus亦可loading/ready/error；status亦可unknown/failed/processing
```

成功回执先记COMMITTED；GET失败只标detailStatus=error，文案“已保存，详情读取失败”，按钮只发GET。禁止将已提交变成“上传失败”或再次POST。若服务端回执格式无效，即使HTTP200也先UNKNOWN并查回执。

### 4.2 查询代次和游标

- `queryKey = JSON.stringify([identityScope, normalizedQ, mediaFamily, state])`。每次新查询递增listGeneration，清items/cursor/error并立即执行，不再`if (loading) return false`丢弃新意图。
- capture `{generation, epoch, listGeneration, queryKey}`；成功/catch/finally均按完整token判断。旧请求finally不能关闭新查询loading。
- 游标存 `{queryKey, value}`。`loadMore()`不再接收任意外部过滤条件，直接消费已提交queryKey及其cursor；分页进行中禁止同一cursor重复加载，切条件则使其失效。
- 首屏失败不显示旧查询结果；同查询更多失败保留本页和同条件cursor供重试。任何失败不能跨条件复用cursor。
- 来源分类仍为已加载数据本地筛选；有nextCursor时保留“继续读取”提示，不能显示“全部无结果”。本方案不擅自新增originKind服务端筛选。

## 5. F04：原意图恢复，确定采用原key只读查回执

### 5.1 文件写操作新增接口（拟定）

`GET /agent/personal-workspace/operations?operationType=CREATE|APPEND|RENAME|TRASH|RESTORE`，原key放`Idempotency-Key`头；不放URL或日志，不接受客户端owner/client。已有`GET /operations/{operationId}`保留其明确职责，不是兼容层。

Controller复用`scope(authentication)`、`json`、`ApiJsonResponses.success`、`PersonalWorkspaceWire::from`；校验单值查询、拒绝未知参数/操作类型。未找到返回现有统一404错误，不虚构成功operation。

```java
// PersonalWorkspaceService
PersonalWorkspaceViews.OperationView operationByKey(
    Scope scope, String operationType, Idempotency idempotency);

// ServiceImpl的实现轮廓：复用validateScope、key、operation投影
var row = dao.findOperationByIdempotency(scope.tenantId(), scope.clientId(),
        scope.ownerJiacn(), operationType, key(idempotency));
if (row == null) throw new PersonalWorkspaceException(
        PersonalWorkspaceException.Reason.NOT_FOUND);
return operation(row);
```

已有operation表、按scope/type/key查询和唯一约束复用，**文件操作恢复不需要新增持久字段/表**。查询不暴露requestHash、存储路径、正文、密钥；保持private,no-store。COMMITTED返回当前已有OperationView，可再读fileId+fileVersion；它不承诺返回当年的文件显示名。

### 5.2 前端状态机与持久化

`PREPARED → SENDING → COMMITTED | FAILED | PROCESSING | UNKNOWN`。

- 一次明确提交只生成一次随机key。准备阶段就注册intent/promise，防止计算文件摘要的await期间双击生成两个key。并发点击共享同一Promise。
- 发送前用身份scope分区写入最小journal并readback成功。复用execution recovery store模式，不把文件名/正文/令牌写localStorage；只存key/type/operationId/状态和必要的不可逆输入摘要，不保存原始文件。
- 新helper接受显式`identityScope`；由可信登录状态给出，不能仅用刷新会变化的epoch作为持久分区。注销/切账号清旧身份状态，晚到响应不重新写入旧数据。普通组件卸载/页面刷新保留待恢复journal。
- 原始File、displayName、If-Match、expectedPreviousVersion在内存intent中不可变；摘要覆盖操作类型、目标、字节hash、MIME、文件名、显示名、前置版本、回收确认。后端现有requestHash仍为权威，前端digest不作为授权凭证。
- 存储不可用明确提示“无法保存恢复标识，尚未提交”，不悄悄降级为不可恢复的新写入；不影响只读功能。
- journal使用每意图独立记录避免不同标签页整表覆盖。恢复页展示本身份未终结操作；相同意图跨页必须共享原key，两个用户明确独立的上传允许不同key。不能承诺仅凭localStorage实现跨标签原子互斥。

|结果|处理|
|COMMITTED|保存终态，只读刷新文件/版本；不重发写入|
|PROCESSING|保留key，可只读继续查询；不因等待时间长自判失败/换key|
|超时、断网、503、无效回执、发送后abort|UNKNOWN；先按原key查，再决定动作|
|查询404|只是“此刻未查到”；原请求可能尚未claim。不得据此新建key|
|原key未查到且用户要求重试|只允许完整同输入、同key、同前置条件重放；claim唯一约束防并发重复|
|刷新后原始文件丢失|先查回执；确需重放时重新选文件并核对digest，完全匹配才用原key发起|
|明确FAILED/确定未发送的校验错误|显示稳定原因；修正输入后是新用户意图。412须重新读取并重新确认，不自动重放旧删除|

即使查询暂时404，原请求随后开始、重放同时到达，也应只产生一个claim；必须加真实并发用例。进程崩溃遗留PROCESSING不在此轮自动抢占/强制失败，保持“处理中/需核对”并提供只读排查，不设置无证据的到期重试。

### 5.3 任务/会话关联不能漏掉

两个composable也每次randomKey；纳入同一intent机制。它们使用独立操作表，不能错误查询文件operation表。

拟在各自Controller/Service增加父资源限定的只读lookup（`GET /agent/tasks/{taskId}/file-links/operations`、`GET /agent/conversations/{conversationId}/file-links/operations`，原key放头，operationType限定现有CREATE/DELETE）；DAO新增`findOperationByIdempotency`纯SELECT，不调用`reserveOperation`冒充查询。响应投影 `{operationId,state,relationId}`，不得泄露requestHash。查询先校验父task/conversation的owner权限，并确认relation属于该父资源；未找到/跨父资源统一404。

复用各自现有操作表type值和唯一键，不自行改存量type命名；若当前operation row未存父ID，查relation后核验父ID。事务未提交查不到仍按UNKNOWN处理，不换key。精确重放之前固定原body/关系revision；一旦DETACHED回执确认，不因为列表刷新失败再DELETE。新增DTO及lookup使用上述确定路径更新接口目录/fixture，此处不把拟新增lookup当作现有功能。

## 6. F06/F07：回收用一致摘要，而不是截断数组

### 6.1 选定契约：精确计数，不返回伪完整引用名单

现有UI仅需数量和确认，本轮usage改为精确分组摘要；不新增三套明细分页。已有任务/会话页面负责查明细，不再对旧usage数组长度求和。示例完整响应：

```json
{
  "protocolVersion": 1,
  "requestId": "workspace-usage-example",
  "code": "E0",
  "msg": "成功",
  "data": {
    "fileId": "pws_example",
    "metadataRevision": "12",
    "impactRevision": "12",
    "counts": {
      "taskReferences": "101",
      "conversationReferences": "2",
      "queuedExecutions": "1"
    },
    "executionSnapshotsPreserved": true
  }
}
```

- 两个revision均D1，counts为D0；计数单位分别为ACTIVE关系条数和去重待执行execution数。不要把三者之和称为去重任务/会话数量。
- 固定文案：“101条任务关联、2条会话关联、1个待执行授权。移入回收站不会删除历史版本或撤销已授权执行。”数量是读取时快照，不承诺确认点击瞬间绝对不变。
- 修改core `UsageView(String fileId,long metadataRevision,long impactRevision,UsageCounts counts,boolean executionSnapshotsPreserved)`；`UsageCounts(long taskReferences,long conversationReferences,long queuedExecutions)`。wire层逐项`Long.toString`，不让Jackson猜标量类型。
- 删除原taskReferences/activeExecutions wire字段，不保留双解析；所有消费者/fixtures/schema同批切换。

### 6.2 快照事务及SQL

新增独立 `PersonalWorkspaceUsageService.snapshot(scope,fileId)`，通过Spring代理调用，使用：

```java
@Transactional(readOnly = true, isolation = Isolation.REPEATABLE_READ,
        propagation = Propagation.REQUIRES_NEW)
public PersonalWorkspaceViews.UsageView snapshot(
        PersonalWorkspaceService.Scope scope, String fileId) { /* ... */ }
```

这里选**单个MVCC一致读事务**，不将锁定读的当前revision与旧一致读结果混用；file与三个count都用同事务普通SELECT，第一条查询建立快照。REQUIRES_NEW避免继承调用方已建立的旧快照；controller正常调用时无外层事务。不得在该事务中锁task/conversation/execution，不改变现有写锁顺序。生产数据库隔离行为必须在真实MySQL测试中证明，H2不能代替。

新增DAO方法（各自既有scope参数）：`countActiveByFile(...) -> long`（task/conversation）、`countQueuedExecutionsByFile(...) -> long`（execution）。Mapper查询轮廓如下，参数全部绑定；task/conversation注解必须拼接既有EXACT_SCOPE/EXACT_FILE常量（不能只复制下方基础SQL而丢掉精确匹配）：

```sql
SELECT COUNT(*) FROM agent_personal_workspace_task_file_link
 WHERE tenant_id=#{tenantId} AND client_id=#{clientId}
   AND owner_jiacn=#{ownerJiacn} AND file_id=#{fileId} AND link_state='ACTIVE'
 -- Mapper注解拼接本类已有EXACT_SCOPE + EXACT_FILE，保留大小写/长度精确匹配
 AND CAST(link_state AS BINARY)=CAST('ACTIVE' AS BINARY)
 AND OCTET_LENGTH(link_state)=OCTET_LENGTH('ACTIVE');
-- conversation表同样条件，表名agent_personal_workspace_conversation_file_link；
-- 两类Mapper的实际状态列均为link_state；不得漏掉上面的精确匹配常量。

SELECT COUNT(DISTINCT e.execution_id)
 FROM agent_personal_workspace_execution e
 JOIN agent_personal_workspace_execution_input i
   ON i.execution_id=e.execution_id AND i.tenant_id=e.tenant_id
  AND i.client_id=e.client_id AND i.owner_jiacn=e.owner_jiacn
 WHERE i.tenant_id=#{tenantId} AND i.client_id=#{clientId}
   AND i.owner_jiacn=#{ownerJiacn} AND i.file_id=#{fileId}
   AND i.grant_state='ACTIVE' AND e.execution_state='QUEUED';
```

查询无LIMIT；执行数用DISTINCT防同文件多个input重复计数。沿用已存在的owner/file过滤与身份校验。先在隔离MySQL数据上EXPLAIN，只有实测需要才另列索引迁移，不擅自生产DDL。

新引用/解除引用及新授权必须与file revision同事务变更；现有task→file锁序保留，严禁usage或trash先锁file再获取task锁。执行自然结束使待执行数下降可不强行增加file revision：其结果不新增删除影响，UI已明确计数为读取时快照，不自动撤销历史授权。

`completeAppend`在现有file锁内：

```java
file.setLatestVersion(version.getVersion());
file.setMetadataRevision(Math.addExact(file.getMetadataRevision(), 1L));
dao.updateFile(file);
```

版本溢出作为确定前置校验失败处理；其余revision自增也使用可检测溢出而非wrap。trash现有无使用返回值的`listActiveByFile(...,100)`不再当安全保证；安全性来自同file锁和revision CAS，移除该多余查询时保留全部关联/授权并发回归。

### 6.3 前端确认对象

`confirmation = { fileId, metadataRevision, impactRevision, counts, identityToken, detailToken }`，只在usage请求返回仍属于当前文件/视图时展示。

- `prepareTrash`先清旧确认再读取；新usage失败则确认按钮不可用。
- `confirmTrash`传整个确认快照；If-Match从快照构造，不读取可能旧的detail.etag。
- 请求体仍 `{impactRevision, acknowledgeExistingReferences:true}`，经useHttp封装Q；确认fileId必须匹配当前目标。
- 412：清confirmation，只读刷新详情/摘要，提示“引用或文件已变化，请重新确认”；不能自动再次POST。新确认是新意图，旧key保留终态。
- 切身份/切文件/返回/rename/append/restore或确认期间任何相关状态更新，都撤销旧确认。双击确认共用同intent，不发送两次不同key。

## 7. F08/F09：版本分页和可见预览状态

### 历史版本

复用现有 `GET /files/{fileId}/versions?cursor=...`，不增加服务端重复端点。

- composable新增 `versionItems/versionNextCursor/versionListState/loadVersions(fileId)/loadMoreVersions()`；独立代次和fileId归属。
- detail.versions只是首批摘要，不能推断hasMore；打开详情后请求已有分页接口首屏，用其items/hasMore/nextCursor建立正式版本列表。首屏失败显示“历史版本未读取完整”，当前latest仍可预览。
- option的key/value为版本字符串；去重后按BigInt版本降序；分页保留选中版本，不在每次返回时自动切latest。
- 101条测试：100+1探测，第二页必须得到v1；中间追加v102时旧cursor仍遍历旧窗口，刷新首屏合并新版本但不跳选中项。
- cursor校验用专用不透明cursor约束，不复用100字符业务ID约束；后端保持文件绑定及非法cursor拒绝。

### 预览

两个UI模式的全部成功分支外层都加独立提示（文本插值，不v-html）：

```vue
<p v-if="workspace.preview.value.message" role="status" class="workspace-preview-notice">
  {{ workspace.preview.value.message }}
</p>
```

部分预览显示“预览不完整，可下载原件”；错误区域避免重复相同提示。保留图片/音频/文本/分片各自渲染、安全Blob URL释放、当前文件/版本归属。格式不支持、损坏、分片失败不能显示完整成功；下载固定原版本。没有证据不增加资源限制、不提高硬编码上限、不引入不可信HTML预览。

## 8. F11：测试应具体怎么改

### 8.1 既有失败用例

路径根：`/home/isp/wsps/cyf/api/agent/jia-agent-service/src/test/java/cn/jia/agent/api/`。

|测试文件|精确整改|
|---|---|
|PersonalWorkspaceControllerPreviewTest.java|`$.parts`→`$.data.parts`，保留MIME/header断言，增加完整R信封断言|
|PersonalWorkspaceTaskFileLinkControllerTest.java|请求改Q信封；业务路径加data；`$.message`→`$.msg`；executionSnapshotsPreserved在data；鉴权用例不能仅改401为400|
|PersonalWorkspaceConversationFileLinkControllerTest.java|同上；关联版本/relationRevision字符串断言|
|PersonalWorkspaceExecutionControllerTest.java|executionId/items等改`$.data.*`，保留错误code根字段、响应状态和ACL断言|
|PersonalWorkspaceHttpPersistenceIntegrationTest.java|`/file/fileId`→`/data/file/fileId`，首先assert非空再查库；所有业务路径加data；version/latestVersion断言字符串；重放比较业务data与operationId，不比较不同HTTP请求的requestId|

完整安全链新增用例必须实际装配项目SecurityFilterChain/统一错误处理，而不是只standaloneSetup(controller)：匿名+合法body、匿名+非法body、认证+非法body、正确owner、不同owner/client、资料内容/预览分片/usage/operation恢复均覆盖。预期按规范区分401/403/404/400，不为凑绿灯修改生产授权语义。

### 8.2 前端和边界用例

修改 `/home/isp/wsps/cyf/web/tests/personal-workspace.test.js`、`personal-workspace-multimedia.test.js`、两个`personal-workspace-*-links.test.js`、相关execution component用例和 `/home/isp/wsps/cyf/web/tests/juyiting-workspace-browser-smoke.mjs`。

所有fixture使用统一信封、hasMore、D0/D1字符串；最少一条链必须经过真实useHttp解包→真实composable→挂载组件，不是把裸mock直接喂UI就声称跨端通过。

|场景|必须断言，不只是返回200|
|---|---|
|gzip强/弱/缺ETag，真实冲突|前3种构造同业务CAS；真实revision不同仍412；文件和关系回执均覆盖|
|字符串v1/v2/v10/上界、byteLength超JS安全整数|切换后preview/download/起草完全同版本；v9下一个为v10；字节正确显示|
|A写→B读、A写→退出、同A新操作、身份切换|不串详情、不跳导航、不盖新revision、不泄漏旧身份|
|ACTIVE加载中切TRASHED；q1加载中q2；首屏/更多失败|只接纳最新条件，cursor不串查询，旧finally不清新loading|
|提交后丢包/双击/刷新页面/404后原请求晚到|同意图一个key、最多一个file/version/关系；COMMITTED不重复提交|
|storage不可用/重选文件digest不同|写入未发出或拒绝重放，不能静默生成新key|
|usage 0/1/100/101及仅会话引用|精确计数；同execution重复input只计一次；非QUEUED不算待执行|
|usage读期间关联提交、追加、确认后新授权|快照内部一致；新增影响使确认412且必须重确认；历史快照可读|
|101版本与并发追加、跨文件cursor|全遍历无遗漏，当前选择不跳变，跨文件cursor拒绝|
|partial文本/图片/音频/Office分片|警告实际可见；损坏/受保护文件有明确错误和授权下载入口|
|提交200/201但详情GET500|显示已保存+详情失败，仅GET恢复，不再次POST|
|真实浏览器下载|落盘SHA256与对应版本一致，文件名安全，URL释放，无跨身份访问|

后端在现有ServiceImplTest/WriteServiceTest/HTTP集成测试补计数、原keylookup、同key不同输入409、scope隔离、append revision、新确认CAS；新增真实MySQL测试复用项目已有隔离数据库工具，覆盖MVCC快照和锁序，绝不连接生产造101条数据。

### 8.3 正式验证入口

前端本机仅低成本定向诊断；正式测试/构建走Flow4403172。后端读最新build.gradle，通过 `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle`串行运行固定干净源码，复用现有 `:agent:jia-agent-service:v1131Acceptance --tests '*PersonalWorkspace*'`并检查新增测试确被该sourceSet包含；新增MySQL selector按实际build配置登记，不能假设通配符已覆盖全部。保留依赖完整性与validateLayering。

现有104项结果可作为修复前基线，不复用为变更源码的验收结果；证据必须绑定新tree/selector/fixture。旧20项缺陷观察在修复后改成正确行为断言，不继续以“错误现象仍存在”为成功条件。

## 9. 实施依赖和发布闭环

1. **先契约fixture与最小反例**：真实字符串、统一信封、F01/F02/F03/F04反例；同步修旧HTTP断言，保留完整鉴权链待验项。
2. **前端核心修复**：F01/F02/F03/F05/F09/F10与F06确认失效；同批修两个关联composable的ETag和目标归属，不改全局useHttp解析策略。
3. **跨端闭环**：原key只读lookup+前端journal、usage一致摘要+count SQL、append revision、历史版本分页。契约目录和schema与同一fixture同步；不保留旧/新usage双轨。
4. **真实边界验证**：完整安全链、MySQL并发、101边界、真实浏览器与下载hash；失败按实际原因修，不绕门禁。
5. **版本化发布**：确定版本，固定两端commit/tree；Web同Flow Run制品、API同本地build ID及JAR SHA；按项目最新契约的统一切换计划部署。跨端usage有破坏性字段变化，不能API先换新usage后让旧Web继续使用；在授权发布窗口两端就绪后一起开放入口。数据库此方案不默认迁移。
6. **线上核验**：只用隔离测试身份和合成资料验证上传→历史预览/下载→重命名→引用提示→回收→恢复；记录版本/哈希。实际用户失败请求头需脱敏只读取证；不保存令牌/用户内容。

若A批单独发布只能报告对应子集修复，F04/F07等不能标完成。不得将合入develop、push、本地测试通过或设计文档齐全报告为已上线。

## 10. 当前交付状态

已完成：既有证据复核、代码落点/状态机/DTO/SQL/测试/发布顺序设计。未完成：业务代码实施及全部修复后验收。未修改Web/API业务源码、生产资料、生产服务或流水线；续核验仅在独立分支整改/增加测试，结果和边界见§1及审计报告。后续实现的第一条动作是固定修复任务源码并建立现行wire fixture与F01/F02最小回归。


## 11. 继续核验新增：F12 同幂等键竞争的事务快照问题（2026-10-16）

**新增实际失败，不是原F04前端换key的同义问题。** `completion/verification-4.log`及`completion/junit-run4/`记录：真实MySQL两个同key、同内容CREATE并发时，一个请求在`PersonalWorkspaceWriteService.claim`抛出`DuplicateKeyException`。原服务虽然catch唯一键异常，但在同一事务内再次普通查询仍可返回null，于是重新抛出。此前偶然调度得到COMMITTED/PROCESSING不能证明这一竞争安全。数据库唯一约束并未失效；不能把异常推断为已经产生重复文件。

源码落点：
- `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/PersonalWorkspaceWriteService.java`：`claim`第29–48行，`REQUIRES_NEW`内“先普通读→INSERT→重复键后再普通读”。
- `/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/impl/PersonalWorkspaceDaoImpl.java`：`findOperationByIdempotency`为普通SELECT，不是当前读。MySQL重复读快照中，首次查无记录后另一个事务提交，唯一约束能看到冲突，但旧读快照不保证看到新记录。

### 11.1 修复选择：失败事务退出后再读，不在原事务里盲重试

拟新增 `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/PersonalWorkspaceOperationClaimTx.java`，独立Spring bean，避免self-invocation；迁移原claim的构造和scope初始化，保留完整唯一键及requestHash校验。

```java
// PersonalWorkspaceWriteService：编排入口；不是在已失败的事务里重读。
@Transactional(propagation = Propagation.NOT_SUPPORTED)
public Claim claim(Scope scope, String type, String key, String requestHash) {
    try {
        return claimTx.claimOnce(scope, type, key, requestHash);
    } catch (DuplicateKeyException raced) {
        // claimOnce代理已完成回滚；独立事务/SqlSession取得新的数据库快照。
        var existing = claimTx.findAfterRace(scope, type, key);
        if (existing == null) throw raced; // 非预期约束冲突不能冒充成功
        return existingClaim(existing, requestHash);
    }
}

// 独立bean，不能通过this调用以下方法。
@Transactional(propagation = Propagation.REQUIRES_NEW, rollbackFor = Exception.class)
public Claim claimOnce(Scope scope, String type, String key, String requestHash) {
    var existing = dao.findOperationByIdempotency(
        scope.tenantId(), scope.clientId(), scope.ownerJiacn(), type, key);
    if (existing != null) return checkedExistingClaim(existing, requestHash);
    var operation = newProcessingOperation(scope, type, key, requestHash);
    dao.insertOperation(operation); // 不在此catch重复键；让代理先退出事务
    return new Claim(operation, true);
}

@Transactional(propagation = Propagation.REQUIRES_NEW, readOnly = true)
public PersonalWorkspaceOperationEntity findAfterRace(Scope scope, String type, String key) {
    return dao.findOperationByIdempotency(
        scope.tenantId(), scope.clientId(), scope.ownerJiacn(), type, key);
}
```

上面的`checkedExistingClaim`提取原有hash一致性校验，`newProcessingOperation`原样迁移UUID、PROCESSING、createdAt及三个scope字段构造；`Claim`继续采用原类型。构造注入和所有isolated fixture同步迁移，不新增默认null/no-op依赖。此为设计片段，未作为业务补丁编译。

- 不删除唯一约束，不把所有SQL异常吞成PROCESSING，不通过全局降低隔离级别解决；一次竞争回读不是重新创建文件。
- 回读COMMITTED走既有结果重放；PROCESSING返回既有处理中语义；FAILED按原失败语义；同key不同hash必须409。
- 保留同scope完整tuple，另一owner/client不可查到或重放该operation。重新开事务查不到时保留真实异常并记录脱敏诊断，前端仍按F04进入UNKNOWN和原key恢复，不换key。
- 验收必须用真实MySQL屏障固定两次“查无记录”先发生，再允许INSERT：同输入一个文件/一个operation且无SQL异常；不同输入一个成功、一个IDEMPOTENCY_CONFLICT；至少覆盖PROCESSING/COMMITTED重放与scope隔离。
- 相邻执行服务也存在catch重复键后普通读的代码形态，但本轮未运行完整执行创建竞争，**不直接认定为同一已复现缺陷**；实施时按实际事务/锁顺序定向审计，无需调用收费Provider。

F12纳入跨端恢复批次，与F04共同验收。前端保留同key是必要条件，不足以替代后端竞争修复。


## 12. 继续核验新增：F13 公共响应关联头重复（2026-10-16）

真实Chromium经实际`useHttp`读取列表得到HTTP200，但失败为`PROTOCOL_INVALID_RESPONSE`。`completion/browser-failure.json.run7`保留合成数据的原始wire：请求及JSON中的requestId均为单个ID，浏览器读取的响应头却是`id, id`。这不是ETag问题，不能用F01修复替代。

- `/home/isp/wsps/cyf/api/common/jia-common-service/src/main/java/cn/jia/core/filter/RequestIdFilter.java`在进入链时写入Servlet响应头。
- `/home/isp/wsps/cyf/api/common/jia-common-service/src/main/java/cn/jia/core/config/ApiEnvelopeAdvice.java:34`又向Spring响应头写同一值；实际Servlet HTTP输出出现重复字段。
- `/home/isp/wsps/cyf/web/src/utils/apiEnvelope.js:92–104`正确要求请求、JSON、响应头一致，不应放宽为任取逗号前半段。
- 安装JAR中上述两类及`RequestIdFilterConfig`与当前未改业务的编译字节SHA256完全一致（`installed-correlation-class-comparison.json`）。这不等于证明线上有效配置或运行状态；检查时生产接口502，不能完成线上登录验收。

### 12.1 拟改代码：统一Servlet响应头写入位置

`ApiEnvelopeAdvice.beforeBodyWrite`在设置JSON requestId后，替换原`response.getHeaders().set(...)`：

```java
if (!(response instanceof ServletServerHttpResponse servletResponse)) {
    throw new IllegalStateException("PROTOCOL_SERVLET_RESPONSE_REQUIRED");
}
// 清除Spring待提交header map中的同名值，避免随后再addHeader。
response.getHeaders().remove(RequestIdFilter.HEADER_NAME);
// 与RequestIdFilter操作同一个Servlet header，set而不是追加。
servletResponse.getServletResponse().setHeader(RequestIdFilter.HEADER_NAME, requestId);
```

补import `org.springframework.http.server.ServletServerHttpResponse`。保留`RequestIdFilter`对二进制/认证失败/error/async分支的相关ID保障；不能简单删除filter，也不能依赖请求结束finally才写header（那时可能已提交）。原来对JSON requestId不一致的异常保持；Controller显式冲突ID应诊断拒绝而非任意覆盖。该片段为拟实施方案，需针对实际Spring版本编译、真实Tomcat验证，不是已修复证明。

### 12.2 必须新增回归

1. 真实Tomcat+Filter+Advice：JSON列表/详情/分页/写回执的`headers.allValues("X-Request-Id")`长度必须**恰好1**且与请求、JSON一致；只检查`firstValue`会漏掉本问题。
2. 有/无传入header、仅Q.requestId、header/Q不一致、认证401/403、业务412、错误分派、二进制下载、bodyless204/304与async路径；保持各自协议，第三方回调不套本站Q/R。
3. 浏览器读取原始头，实际`useHttp`不得报协议异常；经过nginx压缩再验F01，两个故障分别覆盖。
4. 涉及公共边界，补公共接口定向回归，不只跑资料模块；不改全局前端严格解析规则。

为继续调查下游UI，补充浏览器诊断在**先断言原始链失败后**，只在本任务Vite代理中把完全相同的重复头合成单值；不同值不处理，不修改Java/Web业务源码。该干预必须从正式验收删除；之后的UI检查只能标为“隔离了F13阻断的下游诊断”，不能称未修改链全通过。F13应先于资料模块功能修复验收。


## 13. 影响范围分析（2026-10-16 15:32源码复核）

范围：只读源码/调用关系分析与设计补充，无新测试或线上请求。API HEAD仍`fc399976710f5b724916013926be2cbff899af8c`，Web HEAD仍`2c8d6703eead623f555029341101cb688b9d448a`，两组件干净；远端和线上状态沿用各自历史查询，不宣称最新。统一接口规范仍v1.2。下面明确区分“实测复现”“直接代码调用范围”“尚未逐端点验证”。

### 13.1 公共层范围最大，不能只回归资料页

**F13条件性覆盖所有经过该Filter+Advice并返回JsonResult的接口，而不是所有HTTP响应。** Advice没有限定Controller包，遇到JsonResult即写关联头；Web公共`useHttp`严格比较请求、JSON、响应头。因此列表/详情可能HTTP200却前端报协议异常；写接口可能已经提交、只在消费回执时报错，不能据此提示用户重新提交。

- 资料目录真实链已复现；源码中agent、chat、task、user、economy等域存在JsonResult Controller，构成公共修复回归范围，不代表已逐一证明这些线上接口失败。
- 用户档案、聚义厅读取、任务详情/创建回执、执行状态/结果、会话归档等JSON链需要代表性覆盖。涉及费用/结算的接口仅做不产生真实扣费的fixture验证；不能因为共用Advice就声称发生重复扣费。
- 成功blob/text/raw-byte、SSE、WebSocket帧和第三方回调不一定进入JsonResult分支，不直接套同一故障结论。但其前置JSON查询可能阻断入口；非2xx回包也可能经JsonResult，需要单独覆盖。不要把“成功流分支不同”解释为无需回归认证错误/异步分派。
- 修复落点公共`ApiEnvelopeAdvice`/`RequestIdFilter`边界，保留前端`useHttp`/`apiEnvelope`严格比较，**不改全站解析为宽松模式，不用关闭gzip解决**。

**可用性502是独立的更广范围风险。** 检查到的nginx配置将`/login`、`/user`、`/chat`、`/task`、`/economy`、`/agent`及`/ws`等代理到10018；所以该上游无监听时影响不只资料管理。实测502仅覆盖前述3条匿名路径，其他路由属于配置推断。静态前端及nginx本地响应不能因此判定全停；本节未重新探测服务，15:07记录不能当作当前状态。

### 13.2 资料层与聚义厅调用图

`usePersonalWorkspace`直接使用者：
- `/home/isp/wsps/cyf/web/src/components/workspace/PersonalWorkspace.vue`：独立/嵌入资料管理。
- `/home/isp/wsps/cyf/web/src/components/juyiting/HallMaterialPicker.vue`：事项资料选择、预览、下载。
- `/home/isp/wsps/cyf/web/src/components/juyiting/HallDraftEditor.vue`：交付成果预览、下载及历史版本。
- `/home/isp/wsps/cyf/web/src/components/juyiting/ChatPanel.vue`：会话/任务资料处理。
- `/home/isp/wsps/cyf/web/src/components/personal-workspace/TaskMaterialLinks.vue`：任务资料选择、关联、正式执行输入。
- `/home/isp/wsps/cyf/web/src/composables/juyiting/hallTaskLinkedReferenceInputs.js`、`hallReferenceImageSelection.js`：任务关联输入与参考图。

任务/会话关联adapter还影响`useHallQuickMatter.js`等事项创建流程。以上是共享逻辑/回归覆盖集合；并非每个入口都调用rename/trash，所以不能把F01–F10的全部症状套到每个调用方。

|问题|直接影响|数据/安全边界|
|---|---|---|
|F01弱ETag|文件重命名/回收/恢复412；任务及会话关联/解除已提交回执被拒绝|不等于删除了文件；关系可能已提交，需查回执而非换key|
|F02字符串版本|资料历史预览/下载/起草；新增确认任务资料关联及成果历史选择也有类型冲突|可能展示错误版本或阻断提交；不能推断实际执行已经使用错误字节|
|F03异步写回|同一实例内快速切文件、关闭详情、迟到结果影响新视图/表单|已复现UI串文件；未证明跨账号泄漏或后端把A写成B|
|F04/F10恢复|上传/追加/关系写的丢回执、重试、提交后详情加载失败|可能重复业务提交；已提交应与详情失败分开|
|F05目录条件|搜索、分类、回收站和共享目录选择器的请求/游标切换|显示不符合当前条件的结果，不等同跨租户越权|
|F06/F07引用摘要|回收确认、任务/会话/待执行授权影响提示、追加后的确认有效性|遗漏/过期摘要；回收不是撤销已授权固定快照|
|F08历史分页|资料详情、使用detail.versions的选择器/成果历史超过100条|历史不可达，不是历史内容被删除|
|F09预览警告|消费partial预览状态的资料/成果/选择器UI|不完整内容被误当完整；原文件未证明损坏|
|F11旧测试|HTTP测试信封/字符串/preview断言及验证可信度|隔离分支已修fixture，主仓尚未合入；不是生产功能修复|

### 13.3 本次新增定位：F02必须扩大修改文件地图

原§2仅列资料组件还不够，本次源码确认另两处同类问题，尚未新增浏览器复现：

1. `/home/isp/wsps/cyf/web/src/components/personal-workspace/TaskMaterialLinks.vue:68,179,217–235`：select使用`v-model.number`；选文件后`selectedVersion=detail.latestVersion.version`为字符串，但`canAttach`要求`Number.isSafeInteger`，初始按钮可能直接禁用。改选后变数字虽满足UI，却被`usePersonalWorkspaceTaskLinks.js:199–201`的字符串VERSION拒绝。**必须同时去掉.number，并把canAttach改用共享字符串version校验**，不能只改下拉框。
2. `/home/isp/wsps/cyf/web/src/components/juyiting/HallDraftEditor.vue:66,151–152`：成果历史`resultPreviewVersion`用`.number`，`previewResultVersion`却要求`validMaterialVersion`字符串，切版本后不发新预览。移除.number，保留固定成果版本上界限制，预览失败不可冒充新版本成功。

拟改核心：
```js
// TaskMaterialLinks.vue：复用§3拟新增protocol helper，而非Number转换
const canAttach = computed(() => Boolean(
  selectedFile.value?.state === 'ACTIVE' &&
  version(selectedVersion.value) && links.actionState.value !== 'saving'
))
// 两组件的select都用v-model，不带.number；状态保存原wire字符串。
```

共享composable新增`closeDetail`/版本分页缓存后，检查HallMaterialPicker当前直接清`workspace.detail.value`的关闭路径，使取消/关闭能增加代次并释放preview；不要只更新资料主页面而让其他入口绕过新隔离机制。

### 13.4 F12覆盖七类claim，不包含所有归档

`PersonalWorkspaceServiceImpl`调用同一`writes.claim`的operationType有：`CREATE`、`APPEND`、`RENAME`、`TRASH`、`RESTORE`、`ARCHIVE_ASSET`、`ARCHIVE_TEXT`。因此事务修复涉及上述7类回执声明/重放；目前真实竞争只复现CREATE，其余是直接调用关系确定的受影响范围，尚未分别跑竞争。

会话归档真实调用者为 `/home/isp/wsps/cyf/api/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/conversation/ChatConversationArchiveService.java:130,169`；必须加入“会话附件/文本转资料”的回归，不能只测上传入口。

执行产物归档在`PersonalWorkspaceExecutionServiceImpl:2133,2210`调用的是`writes.archiveRuntimeOutput`，**不是claim**，不能把本次F12断言为所有执行归档已复现。它与WriteService共享类/注入，仍需相关回归；执行创建自身幂等事务是另一条链，按§11单独核查。任务/会话关联服务也不是文件operation claim同一实现。

### 13.5 修复变更范围与发布配合

1. 公共协议修复：公共API响应边界+真实Tomcat/浏览器测试；做跨域代表接口回归，不扩大为重写认证/费用系统。
2. 前端资料修复：原三个composable、资料主组件，**追加TaskMaterialLinks和HallDraftEditor**；资料选择器、会话面板、参考图/任务输入作为共享消费者回归。正式任务/私人交办仅验证输入绑定，不启动收费Provider。
3. 跨端业务修复：usage DTO/Wire、精确count mapper、一致读事务、append revision、原key查询和前端恢复journal。usage有契约变更，两端按统一新契约同步上线，不留双轨解析。metadataRevision增长会使旧确认合理412，客户端必须重读并由用户重确认。
4. 幂等事务修复：拆独立claim事务bean，同步构造注入/测试；回归七类操作、同key异hash、scope隔离、已提交/处理中/失败回执，保留原唯一约束及锁。
5. 不默认需要迁移/重算历史版本、重写原始字节、全量重建文件或修改用户关联。若实施后发现DDL必要，单独设计授权与恢复方案；本影响分析不授权迁移。
6. 先独立核查服务可用性，再处理公共F13、资料关键F01/F02与状态隔离，接续幂等/usage/分页；测试代理去重必须从正式验收撤除。前端Flow4403172、后端固定干净源码本地串行测试/validateLayering，版本化发布后再在线验证，不能用“13组已定位”代替修复完成。

## 14. 用户追加约束：视觉/交互变化同步现行原型（2026-10-16）

用户明确要求“样式变化要更新到最新的交互原型上”。作为本修复交付条件执行：

- 原地更新现行原型 `/home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/prototype/index.html` 及其页面索引`pages.html`，不另建独立旧版/平行原型。当前定位依据为该目录README顶部的2026-10-16事项内容纠正及既有19页入口；实际修改前重新核对最新文件和活动Owner，不覆盖已有未提交修改。
- 同步可见变化：历史版本加载更多、不完整/失败预览提示、写入确认中及恢复入口、回收引用分组与过期重确认、版本/大小显示及按钮可用状态；覆盖资料管理、任务资料关联、成果历史以及实际受影响的资料选择入口。
- 保留既有布局、配色与视觉风格；桌面1440、手机390/320及相关横屏状态按现有工具检查，新增状态补入coverage/交互说明并保存本候选证据，不能直接复用旧截图为新验收。
- 后端ETag、幂等事务、公共请求ID修复无需为展示而编造新界面；原型中的状态均明确为离线模拟，不写生产资料、不冒充接口已修复。
- 本条仅落实同步交付约束，当前未修改原型；后续完成状态须分别报告原型更新、业务实现、正式验证与发布。

## 15. 必要性与范围再复核（2026-10-16 16:10，优先于前述拟方案）

**结论：不是原方案中的每项机制都有必要；存在扩大范围和未闭合影响。以下收敛决策覆盖§2–13中冲突的拟实施要求，不把历史诊断改写成产品验收。** 本轮只读源码/安装包依赖和本地缓存字节码，更新设计；没有新增运行测试、产品改码、原型修改、构建或部署。

基线复核：16:08 API HEAD已由`fc399976710f5b724916013926be2cbff899af8c`前进至`ab379ba8f27a3b1481fc426d6d007ae76b096b2e`，两提交仅差执行schema initializer及其测试（2文件），不是本任务修复；Web仍`2c8d6703eead623f555029341101cb688b9d448a`，两组件干净。历史测试仍绑定原测试候选`cf37f8e36f6c0ecbdd5894450812fe49cd01d9af`，不能移标新HEAD。未查询远端或当前服务健康。

### 15.1 保留的必要修复目标，不等于批准原实现方式

|问题|最小必要变化|不自动扩大到|
|---|---|---|
|F01|文件业务CAS从明确revision构造，任务/会话关联回执不依赖传输强ETag；保留严格业务校验|关闭gzip、放宽全站协议、为修ETag新增三套查询API|
|F02|版本保持字符串；资料页、TaskMaterialLinks的.number及canAttach、HallDraftEditor成果历史一起适配|把所有数值字段改类型、改变固定版本选择语义|
|F03/F05|请求绑定身份、文件/视图代次与目录条件；迟到响应不能写入新视图；游标与查询绑定|统一改造所有composable返回类型、重写全局状态管理|
|F04|一次用户意图复用原key及请求内容；未知结果不能换key冒充新提交|默认强制持久化、通用跨页跨标签恢复平台|
|F06/F07|引用摘要准确完整、一致读；追加和影响确认有效性的授权变化纳入revision核查|改为回收即撤销全部授权、重写执行/计费系统、未经契约评估删除旧字段|
|F08/F09|历史入口接既有分页；实际消费partial预览的UI显示不完整提示|每次select都请求历史、全站通知框架或视觉重设计|
|F10|提交结果与详情加载失败分开；已提交后提供详情重试，避免误导再次上传|把此次复现说成“上传接口失败”：实际观察是ready/成功回执但detail为空且error保留|
|F12|同key竞争后在正确事务视图读取回执，保留唯一约束、scope/hash、锁|重写所有归档、默认新建通用事务框架|
|F11|将旧fixture与现行协议对齐，固定源码验证|宣称测试修复就是生产修复|

### 15.2 从默认方案撤回的四类扩展

1. **撤回全量返回值重设计。** `usePersonalWorkspace.js`现有调用方读取`result.file.fileId`、`result.version.version`、`result.displayName`或仅判断`if(result)`。把失败/UNKNOWN也改为truthy的`{status: ...}`会产生误成功、清空表单/关闭视图的新BUG。优先保留既有成功返回形状/失败返回约定，通过独立响应式operation/detail状态表达未知结果；如必须改返回协议，先枚举并迁移所有调用方，不夹带实施。
2. **撤回“localStorage写入/readback失败就禁止全部写入”的默认门禁。** 未取得其必要性证据，会引入隐私模式/空间不足时新的功能不可用。当前会话内原key复用是必修；刷新后恢复另行明确持久化、身份隔离、清理与不可用降级。不把纯内存实现称为跨刷新恢复完成。
3. **撤回每次`select()`自动加载版本列表。** 只在真正打开历史选择器时分页。固定版本预览、参考图、会话资料和任务输入不应平白增加历史请求依赖。优先保留`loadMore(options)`调用签名，在内部绑定查询条件，不无故扩大消费者迁移。
4. **撤回“追加成功也必须保留旧选择”的新交互要求。** 同一有效视图内用户主动追加成功，维持原先选中新版本的行为；只禁止迟到/后台结果劫持其他文件或视图。局部提示和分页沿用原样式，不增加toast框架。

### 15.3 F13公共修复必要性下调为待证，不能先改全站

安装包`/home/isp/hosts/cyf/api/cyf-api-kit.jar`此次只读清单包含`spring-webmvc-7.0.2`、`spring-websocket-7.0.2`、`spring-webflux-7.0.8`、`spring-web-7.0.8`。缓存字节码显示7.0.2的`ServletServerHttpResponse.writeHeaders`使用Servlet `addHeader`，7.0.8实现不同。**尚未取得原fixture实际运行依赖清单，不能声称它确实用了7.0.2，也不能声称7.0.8已经解决了本应用的问题。** 安装包亦未绑定当前运行进程。

因此：此前“7个业务类SHA一致”不足以证明公共头问题能外推到安装包/线上；F13保留为**原隔离链实测缺陷、生产等价性和公共改码必要性待证**。撤回§12/§13“必须先修公共层再实施所有资料修复”的默认前置。先在固定候选的真实依赖与原始头上复现，若仍重复再决定公共层最小补丁及跨域回归；不默认升级/降级Spring，不修改前端严格解析，不将测试代理去重带入正式验收。证据：`docs/implementation/evidence/workspace-management-audit-20261016/scope-review/dependency-boundary.json`及两版本字节码摘录；这是静态依赖检查，不是新运行通过证明。

### 15.4 尚未闭合的具体影响，实施前必须定向补证

- **授权变化→回收确认revision链未全覆盖。** `PersonalWorkspaceExecutionServiceImpl.create`会增加文件revision；`createConversation`的455–477行插入ACTIVE输入时，本段未见对应revision更新。需沿`admitControlled`/V3/普通分支核查锁与调用链，在私有fixture验证“读usage→新增会话执行输入→用旧revision回收”是否被拒绝。当前只是源码发现的覆盖缺口，不能新增一个“线上实测BUG”。一致读本身不能保证后续授权变化使旧确认失效；不得借此调用收费Provider或修改费用规则。
- **原key查询并非三个域一刀切。** 文件operation、任务关系、会话关系的事务/状态不同。关系服务已有同key事务重放，不能硬套文件PROCESSING六态；原DELETE提交后关系又被重新关联时，“历史回执已提交”不代表“当前关系已解除”。新增lookup仅在现有重放/operationId不能满足明确丢回执恢复用例时落地；先定义历史/当前语义、父对象ACL、未提交404、requestHash校验，不默认新表。§5三个接口从“已定必须”改为待此决策的候选。
- **claim修复跨七种操作，运行竞争目前只覆盖CREATE。** APPEND/RENAME/TRASH/RESTORE/ARCHIVE_ASSET/ARCHIVE_TEXT补同key/异hash/回放。`ChatConversationArchiveService`还有SAVING→文件COMMITTED→SAVED两阶段收口，须测文件已提交而会话回执未完成后重试。`archiveRuntimeOutput`不走claim，不能顺手重构。独立bean或现有事务模板二选一，以事务退出及新视图实证为准，不以拆类数量作为修复目标。
- **usage契约与共享UI。** 精确计数/会话引用字段按v1.2规范同步服务DTO、Wire和消费者，不把截断列表伪装完整数；资料主页面之外的任务关联、成果历史、选择器、会话面板、参考图和输入校验按实际使用路径回归。源代码影响范围不冒充逐页实测。

### 15.5 收敛后的实施次序与完成边界

先实施低耦合F01/F02及局部请求隔离/错误提示/懒加载；F04恢复、F06/F07确认契约、F12事务按上述边界定向设计验证后落地，避免捆绑通用平台改造。F13先核实依赖等价性，再决定是否改公共层；服务可用性由服务Owner另行核查，历史502不代表当前状态。

用户要求的可见交互同步现行原型仍有效，按§14执行，但只同步最终保留的状态，不把已撤回的交互扩大做进原型。本次未修改原型及产品代码。前端正式Flow、后端固定源码本地验证、发布各自另报；本轮不能声明“全部必要、影响已完全闭合”。

## 16. 必要修复实施交付（2026-10-16 16:47）

**本节是实现状态；§1–15未实施片段和最初“全部未改”的描述为历史，不代表当前候选。** 唯一Owner本聊天。30分钟窗口内完成下列必要前端代码、定向自检、develop集成及现行原型局部同步；正式Flow和发布未完成，不报全功能验收。

- 最终Web commit `1e779e9798c2d93098cb27a9c9916dcc6eeed505`，tree `0ec29574f57dccd4fbe5c4c88f377aba93f43776`；业务修复commit `b3cb681edbc4bc0856fba7bba9cfb5bb46c6432e`，后续为新增控件格式及测试fixture生命周期对齐。独立worktree `/home/isp/wsps/worktrees/cyf-workspace-essential-web-20261016`，分支`codex/workspace-essential-20261016`，自检后快进合入组件develop。未改API。
- F01：`usePersonalWorkspace.js`从已验证body的fileId/metadataRevision构造If-Match；任务/会话关联仍严格检查body及目标版本，强/弱/未暴露的传输ETag不再改变业务成功结论。未删除后端CAS/ACL，不关闭gzip、不放宽全站协议。
- F02：复用现有`materialVersion.js`字符串校验，修复资料主页面、任务关联canAttach和成果历史选择；默认预览/下载使用`.latestVersion.version`；独立helper以BigInt显示字节数/下一版本，前端达到int32版本上限时明确不可追加。未改后端溢出分支。
- F03/F05：详情/关闭和目录查询各自代次隔离；写回执只更新原文件列表，旧视图不得被重新打开/覆盖；组件表单完成回调核查视图与输入；回收摘要绑定原选择（兼容Vue响应式包装而非添加wire字段），筛选改变不复用旧cursor。修的是已确认前端竞态，不宣称跨事务并发已修。
- F08：既有版本分页按需接入资料历史、任务资料历史及成果历史，不在每次select或中性固定版本选择器新增请求；缓存绑定当前文件，切换/关闭丢弃迟到页。F09在成功单页/分片预览旁独立显示partial提示。
- F10：保留原成功返回结构，单独显示“已保存但详情读取失败”，提供只读重读详情；迟到完成不清空新视图输入。没有加入localStorage硬门禁或跨刷新恢复平台。
- 本地定向诊断 **229 passing / 0 failing**，其中21个新增缺陷回归；JS lint通过。四个Vue文件的原基线仍有83条存量lint问题，本次新增控件的6条格式问题已纠正，未全文件格式化/放宽规则；不能声称全项目lint清零。诊断中的旧测试回执/缺失mock接口错误已修复并保留失败记录，不重标失败轮次。
- 原型在现行`specs/juyiting-ui-baseline-20261006/prototype/interaction-completion.js`局部更新，保留原文件此前改动；资料详情提供历史100+2、部分预览、提交后详情失败/重读的离线演示。93项文档检查、1440/390/320三组交互与布局通过，浏览器错误/外部请求均0；不是产品浏览器端到端或19页新全量验收。README/source metadata/校验清单及既有覆盖说明已更新。
- 正式Flow4403172当前配置只含cloud_ci、无部署阶段/自动触发。16:40对业务候选的启动调用回执不明确，之后列表未出现新Run，状态保留UNKNOWN，没有盲重发。**最终候选没有正式Flow通过证据，未部署、未在线验收。** 首次调用使用的既有脚本来自已用控制入口，但其异常包装没有保留足够根因；后续先只读核查请求/运行归属，再对最终候选完成正式验证，不伪造成功或自动发布。
- 待拆分讨论：F04未知结果/跨刷新恢复、F06/F07引用一致性与精确统计、F12幂等事务、F13运行依赖等价性。F11旧后端fixture仍在原隔离分支，不纳入本次前端交付。不能将本轮标成13组全部修复。

完整证据目录：`/home/isp/wsps/cyf/docs/implementation/evidence/workspace-management-audit-20261016/essential-repair/`。各层状态和最终固定源码见`result.json`。

## 17. 剩余问题详设与实施计划（2026-10-16，发布1.16.2后）

**状态：设计交付，未实施。本节优先于§5/§6/§11/§12中冲突的旧拟案，延续§15收敛边界。** 用户要求输出详设和计划，不授权本轮继续产品改码、构建或发布。§16中的“正式Flow待完成”是历史：前端1.16.2已由4403172/Run215发布，详见既有handoff及release-1.16.2-r2证据。

### 17.1 固定基线、目标与非目标

- 唯一Owner：本聊天`codex-workspace-audit`，沿用`WORKSPACE-MANAGEMENT-AUDIT-20261016`。本轮只更新既有设计及handoff，不新建实施台账/Reviewer。
- 本地Web HEAD `828460c9c1ce90d083ef9f82f9ce7622bdf4830d` / tree `47b212675e478b9d0fb8f0c4fd849b706dab188c`，与本聊天17:10发布证据相符；不因此声称此后线上未变化。
- 本地API HEAD `ab379ba8f27a3b1481fc426d6d007ae76b096b2e` / tree `26a19ddaf4b375a21177b0c82a4f3b714e8a2cf9`，当前工作区干净。旧真实MySQL证据仍绑定历史fixture候选，不移标到该HEAD。本轮未重新查询远端/API生产版本。
- 公共接口固定 `/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.2；规范版本不是应用版本，公共`protocolVersion`仍为1。设计片段不是已编译代码。
- 目标：准确、可并发校验的回收确认；文件claim并发安全；当前页面实例内原意图安全重试；查明公共响应头是否确需修复。
- 非目标：永久删除、回收撤销全部历史授权、计费/Provider调用变更、全站事务/返回值/通知框架、强制浏览器持久化、默认新增三套lookup、Spring版本调整、自动部署。

### 17.2 交付分组与证据等级

|工作包|证据与性质|计划交付|不得宣称|
|---|---|---|---|
|A：F06/F07|截断计数/遗漏会话/混合快照有既有证据；授权变化revision链仍未全覆盖|后端精确摘要和并发闭环；前端确认与原型同步|已证明所有会话分支都是线上BUG|
|B1：F12|真实MySQL CREATE同key竞争复现DuplicateKeyException；唯一约束未失效|后端事务边界修复，七类调用及会话归档回归|已经产生重复文件、所有归档均同根因|
|B2：F04|当前文件/关系写每次生成新key已源码确认；网络丢回执组合需定向实测|当前实例内固定key/输入、安全重试及未知状态提示|跨刷新/跨标签恢复已实现|
|C：F13|原隔离链原始头重复；生产依赖等价性待证|先补证；复现才做公共层最小修复|公共层必改或7.0.8已自动解决|

F06/F07及F12是正确性BUG；F04的同意图换key是可靠性相关功能缺陷，跨刷新恢复是另议增强。F13目前为待证问题，不是获准的公共改造。

### 17.3 A：准确回收确认（F06/F07）

#### A1. 用户语义与计数口径

保持“移入回收站仍可恢复，不永久删除，不自动撤销已授予的固定版本引用/执行授权”。此句不承诺失效、到期或已撤销的授权仍能访问。

确认展示文件名称、可恢复说明、三类摘要、保留历史授权说明及取消/确认按钮。计数建议为：

|字段|定义|注意|
|---|---|---|
|taskReferences|本scope/file的ACTIVE任务关联行数|是引用条数，不是不同任务数；同任务不同版本可能多条|
|conversationReferences|本scope/file的ACTIVE会话关联行数|是引用条数，不是会话数|
|queuedExecutions|该文件具有ACTIVE输入授权且状态QUEUED的去重executionId数量|是执行数，不是输入行数，同执行多个版本只计一次|

**三类不相加为“总共有N项影响”**，它们不是同一种计量单位，也可能关联同一业务。UI分别写“任务引用N条、会话引用N条、待执行任务N项”。零值明确显示；加载失败不可当0，不出现确认按钮可提交状态。

#### A2. Wire合同（拟定替换现有usage，不新增平行API）

路由沿用现有`GET /agent/personal-workspace/files/{fileId}/usage`。公共信封不变，`data`拟为：

```json
{
  "fileId": "pws_example",
  "impactRevision": "12",
  "counts": {
    "taskReferences": "3",
    "conversationReferences": "2",
    "queuedExecutions": "1"
  }
}
```

- `impactRevision`复用文件`metadataRevision`，不新增同义revision字段/数据库列；计数按非负十进制字符串投影，禁止前端Number精度丢失。
- 旧`taskReferences`/`activeExecutions`明细数组停止作为usage合同；实施前全仓枚举实际消费者，同批迁移测试和接口目录，不保留双解析。文件详情现有relations等字段不随之删除。
- 回收请求仍使用`impactRevision`及`acknowledgeExistingReferences:true`；`If-Match`由**同一次usage返回**的fileId/impactRevision构造，不混用旧详情revision。不绕过身份、ACL、If-Match及业务revision校验。
- 现有412/METADATA_CHANGED继续表示需重读确认；401/403/404保持原权限/资源语义。不得把所有409/5xx都解释为“已确认失败”，未知回执按B2处理。

#### A3. 具体代码修改地图

1. `/home/isp/wsps/cyf/api/agent/jia-agent-core/src/main/java/cn/jia/agent/entity/PersonalWorkspaceViews.java`：将UsageView改为fileId、impactRevision、UsageCounts；服务内部计数用long，wire字符串投影。
2. `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/PersonalWorkspaceWire.java`：明确投影及边界测试，不让Jackson默认数值类型泄漏到wire。
3. `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/PersonalWorkspaceServiceImpl.java`：usage委托一致读入口，删除使用两份limit100数组长度提供摘要的逻辑。
4. 拟新增 `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/PersonalWorkspaceUsageService.java`：独立代理事务，scope校验、文件存在性、revision和各COUNT在同一MySQL REPEATABLE_READ只读新事务中读取。不能this自调用；首先读取文件建立一致快照，后续计数全部普通一致性读，不混入当前读。
5. `/home/isp/wsps/cyf/api/agent/jia-agent-mapper/src/main/java/cn/jia/agent/dao/PersonalWorkspaceTaskLinkDao.java`、`PersonalWorkspaceConversationLinkDao.java`、`PersonalWorkspaceExecutionDao.java`及对应impl/mapper：增加scope完整限定的精确COUNT查询；执行使用COUNT(DISTINCT execution_id)，JOIN同时约束tenant/client/owner，禁止跨scope连接、LIMIT或读取所有明细再计数。
6. `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/PersonalWorkspaceWriteService.java`：completeAppend在同事务内更新版本与metadataRevision，使用受检加法；trash保留行锁和revision校验。现有丢弃结果的limit100引用查询在完整锁链证明后删除，不把它当并发安全依据。
7. `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/PersonalWorkspaceTaskLinkServiceImpl.java`、`PersonalWorkspaceConversationLinkServiceImpl.java`及`PersonalWorkspaceExecutionServiceImpl.java`：按A4逐条核查并补缺失的revision更新；不先假定每个方法都缺失。
8. `/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspace.js`：严格校验摘要和目标fileId，确认上下文保留原视图/身份与usage revision，trash接受内部捕获的If-Match，不允许调用方任意注入绕过校验；412销毁旧确认并重读，用户再次确认后才生成新意图。
9. `/home/isp/wsps/cyf/web/src/components/workspace/PersonalWorkspace.vue`：两个呈现分支一起迁移，移除数组length求和；内嵌区域及浏览器confirm入口使用相同的摘要/后果文字，不强制顺手重做整个弹窗系统。

上述短文件名均指同一已列绝对目录下文件；实施时以定向检索确定mapper XML/注解实际落点，不凭文件名假设数据库表名。

#### A4. 一致快照与“确认后又变了”是两项不同保证

一致性读只能保证用户看到的是某个真实快照，**不能单独保证确认时还有效**。实施前必须生成实际写链矩阵：

- 追加版本、任务关联新增/解除、会话关联新增/解除；
- 普通执行、会话执行、受控/V3等实际创建入口新增授权；
- 撤销授权及QUEUED进入其他状态导致queuedExecutions变化的入口。

每条影响摘要的写事务都需在既有锁顺序下锁定同一scope/file行、修改关系/状态并在同事务推进revision；无实际变化的幂等重放不重复推进。多文件执行先核查现行锁图，确定稳定文件锁顺序及与execution/operation锁的顺序，不能机械加锁造成反序死锁。

关键验收：先读usage，再并发新增关联/授权，旧revision回收必须412；回收先拿锁时，后到的新关联按现行ACTIVE条件校验，不因新增锁忽略文件已回收。

**范围闸口：**queuedExecutions依赖执行状态，不能只给createConversation补一行revision就宣称闭环。如果状态迁移涉及未分析的运行调度路径，先补齐写链/锁图和无Provider的测试；不能顺带改计费、调用Provider或无限扩大状态机。若为避免该影响拟把UI改为“现存输入授权数”，属于计数语义变更，需更新本合同后再实施，不能静默换指标。

#### A5. UI状态与原型

- 初始 → 读取摘要 → 可确认；读取失败 → 显示错误/重试，不提交。
- 提交中禁止重复确认；取消或切文件销毁该视图确认，晚到usage不得重新打开。
- 412 → “文件或关联情况已变化，请查看更新后的信息再确认。”读取新摘要但不自动提交；新摘要按新用户确认生成新key。
- 网络丢回执 → B2 UNKNOWN，不把确认框关闭当回收成功。
- 原地同步 `/home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/prototype/interaction-completion.js` 及现行index/pages入口；示例覆盖0/多类/超过100/读取失败/确认过期/提交未知，保留原布局与颜色。原型示例标为演示，不冒充真实引用。

### 17.4 B1：claim并发事务修复（F12）

采用§11.1的**失败事务退出后、新事务读取已有operation**方案，不降低全局隔离级别、不移除唯一约束、不无限重试。

代码落点：现有 `/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/PersonalWorkspaceWriteService.java` 的claim变为无事务编排入口；拟新增同目录`PersonalWorkspaceOperationClaimTx.java`承载被Spring代理的两段REQUIRES_NEW方法。claim入口使用NOT_SUPPORTED避免继承外层快照。保留原Claim返回类型、scope/type/key唯一约束、requestHash和PROCESSING初始化。

```java
// 设计轮廓，非已编译补丁
public Claim claim(Scope s, String type, String key, String hash) {
    try {
        return claimTx.claimOnce(s, type, key, hash);
    } catch (DuplicateKeyException raced) {
        // 此处claimOnce事务已经通过代理回滚退出。
        var row = claimTx.findAfterRace(s, type, key);
        if (row == null) throw raced;
        return existingClaim(row, hash);
    }
}
```

- claimOnce只做查/插操作记录，不持有文件I/O、预览或Provider调用；不可在其内部catch再用同一快照查。
- 原key原hash：按现有PROCESSING/COMMITTED/FAILED语义返回；原key异hash：409/IDEMPOTENCY_CONFLICT；冲突后查不到该scope/type/key：保留异常，不伪造已处理。
- 不能只根据DuplicateKeyException认定为幂等竞争；必须查得完整匹配键再复用现有hash校验；其他唯一约束冲突不能吞掉。
- 构造注入及真实Spring/单测fixture同步更新，不新增null/no-op回退构造掩盖缺依赖。
- 覆盖CREATE、APPEND、RENAME、TRASH、RESTORE、ARCHIVE_ASSET、ARCHIVE_TEXT；`archiveRuntimeOutput`不走claim，不顺手重写。
- `/home/isp/wsps/cyf/api/chat/jia-chat-service/src/main/java/cn/jia/chat/archive/conversation/ChatConversationArchiveService.java`补“文件COMMITTED、会话SAVING未收口”的重试测试；仅发现真实缺陷时才改其业务代码。
- B1为B2安全重放的发布前置；B1不改变wire，可独立部署，也可随A的后端包合并一次正式构建发布。

### 17.5 B2：同意图安全重试（F04）

#### B2.1 本期范围与数据模型

只保证**当前存活页面/composable实例内**的恢复；不承诺刷新、关闭页面、跨标签恢复。采用局部helper，不引入全局恢复平台/强制localStorage。

拟新增 `/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspaceWriteIntent.js`，由文件、任务关联、会话关联三个composable实例持有，依赖显式传入身份scope/epoch。不复用文件operation表查询关系operation。

```js
// 内存结构；不落浏览器持久化，不向日志输出key/文件内容
{
  key, type, target, identityEpoch,
  input,           // 固定body/原File/前置版本/If-Match/确认revision
  state,          // PREPARED | SENDING | UNKNOWN | PROCESSING | COMMITTED | REJECTED
  operationId,
  pendingPromise
}
```

- 通过用户提交创建意图，必须在首个await之前登记key与promise；双击同一在途操作共享promise。完成后用户明确发起的新操作才是新key，不能按文件内容永久去重。
- 原File对象/字段/前置条件固定；每次发送重建FormData，不能重新从当前表单读取已修改的内容。
- 修改表单不等于可以把UNKNOWN旧请求当新请求自动提交；同一目标有未确认意图时明确提示先处理。不同目标正常使用，不封锁全部写操作。
- 前端输入摘要不是授权或幂等权威；后端requestHash校验保留。原文件已不在内存时不声称可以安全重放。
- 注销/切身份时取消后续恢复并清除内存，晚到结果不更新新身份UI；abort不能证明服务端回滚。关闭详情不得让晚到结果重新选中文件。

#### B2.2 恢复策略：先复用已有协议，不默认新增lookup

|情况|动作|
|---|---|
|明确有效成功回执|COMMITTED，按原成功返回形状交付；后续详情失败仅GET重读，不重发写入|
|已获得operationId|复用现有按ID的只读查询，保持原key和请求内容|
|回执丢失、没有operationId|用户点“重试原操作”时，同key、同输入、同前置条件重放；依赖B1及各关系服务已有重放契约|
|明确PROCESSING|保留原意图，展示处理中；不因时间长自判失败/换key，不自动忙轮询|
|断网/超时/发出后abort/5xx/格式错误|UNKNOWN，不能清空表单或显示失败已回滚|
|可信明确业务拒绝|按具体错误码处理；412重新读取并再次确认，409异hash保留冲突信息，不静默换key|
|恢复查询404|只能说明当前未查到；不得据此生成新key|

文件操作和任务/会话关联分别核对“同key重放是否先于当前revision前置校验”及历史回执语义。例：解除关联已提交后又被重新关联，重放旧解除只能说明**原操作已提交**，不能显示“当前已解除”；必须读取当前关系状态后展示，禁止将旧回执覆盖新关系。

只有定向测试证明现有重放不能安全恢复某一明确操作，才增加**该域**只读lookup，并补充父资源ACL、未提交404、原key/原hash及历史结果语义。旧§5三个新API不再是默认实施清单。本期不新增表。

#### B2.3 调用方与UI

- 修改 `/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspace.js` 的upload/appendVersion/mutate，以及`/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspaceTaskLinks.js`、`/home/isp/wsps/cyf/web/src/composables/usePersonalWorkspaceConversationLinks.js`的attach/detach。
- 保持成功对象及失败null约定；新增独立响应式writeIntent状态与retryOriginal入口，不返回truthy的失败对象。
- 全部调用方逐项确认：何时关闭面板/清空输入/刷新关系、卸载是否销毁composable；确认结果仅更新原意图目标，不越过已上线的视图代次检查。
- 提示“提交结果尚未确认，请重试原操作核对结果，勿重复新建”；无operationId时按钮明确“重试原操作”，不能标成“仅查询”。已经确认COMMITTED的按钮才可“重新读取详情”。
- 同步当前交互原型，桌面/窄屏检查长文件名、未知状态、禁用/恢复按钮和焦点；不新增通知框架。

### 17.6 C：公共关联头问题补证与条件修复（F13）

先产出三份可比证据：

1. 固定源码测试fixture的实际resolved运行依赖/类来源，而不是仅看build.gradle声明；
2. 正式候选JAR中的依赖清单与Filter/Advice/Servlet响应实现来源；若声称生产等价，还须绑定实际运行进程加载的JAR；
3. 不经去重代理的原始响应头、多值原样及body.requestId，对比请求值；认证错误/普通成功/业务错误分别观察。

只读或隔离请求，不借此启动Provider、改生产资料或重启服务。历史安装包和历史502均不当成当前线上状态。

**判定与实施：**
- 真实目标依赖下无重复：保留原fixture缺陷历史，修测试环境/依赖固定及误导说明；不改公共层。
- 真实目标依赖下仍重复：定位重复写入点，再在 `/home/isp/wsps/cyf/api/common/jia-common-service/src/main/java/cn/jia/core/filter/RequestIdFilter.java` 与 `/home/isp/wsps/cyf/api/common/jia-common-service/src/main/java/cn/jia/core/security/SensitiveResponseBodyAdvice.java` 之间明确唯一header写入责任；另一层只保持body/request上下文一致，不能在多处对同header追加。
- 不直接认定上述Advice就是唯一来源；先追完整过滤器/Advice链及错误dispatch。公共JSON成功、业务错误、鉴权拒绝、异常、204、下载/流、CORS暴露分别测试。不对非JSON响应统一包信封。
- 前端`useHttp`严格一致性检查保留，正式浏览器fixture撤除重复头代理去重。回归发现波及无关链时先划清问题，不用全站放宽解析换绿灯。

### 17.7 最小验收矩阵（计划，未执行）

|层|最小用例|通过条件|
|---|---|---|
|A计数|0/1/100/101/多版本、同执行多输入、DETACHED/REVOKED、另一owner/client|精确分类；无截断、无跨scope泄漏、无重复JOIN计数|
|A快照|在文件revision与COUNT间穿插关系提交|返回同一快照，不混合新旧计数|
|A并发|usage后新增/解除任务会话引用、普通/会话执行授权、追加、撤销、QUEUED状态迁移|按冻结口径更新revision，旧确认412；多文件锁无反序|
|A浏览器|两种资料入口、取消/切文件/身份、摘要失败、412后再确认|不默认0，不自动提交，不复活旧确认；UI与原型一致|
|B1竞争|真实MySQL屏障保证双方先查空，再放行INSERT|七种操作同key同hash无SQL泄漏/无重复副作用；异hash409|
|B1事务|外层已有RR快照、PROCESSING/COMMITTED/FAILED、scope隔离、其他唯一冲突|新事务可见，不能吞未知异常或跨域回放|
|B1归档|文件COMMITTED但会话SAVED未写、重试及事务回滚|一个文件、可正确收口，不伪造会话已完成|
|B2恢复|服务端提交后丢响应、提交前断网、无效回执、连续点击、修改输入、切身份|同意图key/input保持，结果未知不报成功；不清新表单|
|B2关系|解除已提交后重新关联，再重放旧解除|区分历史回执与当前状态，不再次解除新关系|
|C协议|真实依赖原始多值头、认证/业务错误、下载/流/204|同一requestId，不重复/矛盾；非JSON行为不变|

沿用已有HTTP/MySQL/组件/Chromium测试基础设施，历史失败证据保留。新增fixture必须覆盖正式过滤器/Advice；若需绕过某处阻断做诊断，结果单独标注，不能当全链验收。

### 17.8 实施顺序、交付物与发布计划

|阶段|动作|交付与退出条件|
|---|---|---|
|0 范围冻结|重新核对远端develop/源码/生产版本，独立worktree，读取最新AGENTS、工具索引及build.gradle；完成A写链/锁图和B重放语义核查，同时做C依赖补证|固定候选、实际调用图、可重复最小反例；不满足条件的项标明待证，不扩成公共改造|
|1 B1后端基础|按新事务回读修claim；补七类操作/归档真实竞争|竞争及相关事务/权限回归通过；无wire变化，供B2依赖|
|2 A跨端修复|先定usage DTO与计数口径，再补COUNT/一致读/revision闭环，迁移两个UI入口和原型|所有摘要影响写路径闭合；旧确认被拒绝；接口目录、fixture、原型一致|
|3 B2恢复|局部意图helper、三个composable及实际调用方适配|丢回执/原key重放/关系历史语义通过；不包含持久化恢复|
|4 C条件修复|只有阶段0证实公共层缺陷才实施最小责任收敛|未复现则以补证报告收口；复现则公共边界回归通过|
|5 正式验证与版本交付|Owner自检合入组件develop；固定发布版本、commit/tree；后端本地，前端Flow4403172；关联同批不可变制品|记录各层真实结果，发布授权另行取得，不能因本设计或合入自动上线|

上述是执行依赖顺序，不要求每阶段新增人工批准或Reviewer；相同Owner在实际实施授权内连续推进。A可独立于B2交付，B1必须在B2安全重放上线前验证就绪。C不作为默认挡住其他工作的前置，仅在真实链被它阻断时成为必要依赖。

**验证入口：**后端先读最新相关build.gradle，在干净固定源码通过`python3 /home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py gradle ...`串行执行定向测试、依赖完整性和validateLayering；正式制品使用同本地build ID及SHA256。前端本地只定向诊断，正式完整测试/构建/制品/部署用Flow4403172，不本机生产打包。

**A改变usage合同，不能直接“后端先上线、旧前端先凑合”。** 两端先完成验证和制品准备，沿用项目统一切换要求，在已授权维护窗口限制受影响业务入口，再安装匹配API/Web、核验后开放。若没有安全限制入口的现成能力，不临时加兼容双轨或擅改网关；在发布计划中明确短暂停用方案并取得授权。B1无wire变化可以先发；是否拆两个正式版本按实际发布时机确定，不为阶段划分重复构建。

**恢复：**无新表/DDL是本方案目标。发布前保存前后端旧制品、版本及配置；A回退必须恢复匹配前后端合同，不只回退一端。保留新增版本/引用/operation业务数据，不清表撤销用户动作；revision单调推进不回减。源码/制品/部署记录分别留证，失败先归因、同输入同根因两次停止盲重试。

**收口：**实现后把已验证语义回写既有端到端指南和runbook；设计与失败证据保留本路径。UI状态变化必须同步当前原型，原型浏览器检查与产品真实HTTP/浏览器验收分开。总工时目前无可靠实测，不承诺固定分钟数；沿用handoff记录实际定位、实现、验证、等待，未知留空。

### 17.9 实施前仍须闭合的三项决定

1. queuedExecutions所有状态迁移的revision/锁链是否可在不改执行业务规则的前提下完整覆盖；未闭合不能宣布回收确认并发安全。
2. 文件及两类关系原key重放是否足够处理已提交回执丢失；需要lookup必须有具体不能恢复的反例，不默认三域新接口。
3. F13在真实目标依赖下是否存在；无证据不改全局Filter/Advice。

这三项属于明确的前置核查任务，不是让用户决定事务技术实现；由Owner在阶段0取证并回填结果。跨刷新持久恢复、永久删除及历史授权撤销不在本轮计划内。

### 17.10 用户确认的计数调整（2026-10-16 18:19，覆盖17.3）
用户同意“现存输入授权N条”替换“待执行任务N项”。字段counts.activeInputGrants统计scope/file下grant_state=ACTIVE的输入记录，不JOIN执行状态、不按执行去重。执行开始/完成不改该计数，不为QUEUED状态迁移改调度锁链；授权创建/撤销仍须同事务revision。集中开发后统一验证，保留最小检查；本轮不发布。

### 17.11 实现细化（候选，待统一验证）

- F06/F07 使用 `PersonalWorkspaceFileMapper.selectUsage` 单 SELECT + 三个相关 COUNT 读取 revision/完整计数，代替新增服务和多次查询事务。无需执行状态 JOIN；需要真实 MySQL/MyBatis record 映射验证。
- F12 `PersonalWorkspaceOperationClaimTx` 独立代理 REQUIRES_NEW；原 WriteService.claim 在 NOT_SUPPORTED 边界外捕获唯一冲突，失败事务退出后 fresh transaction 查竞争者。七条现有 claim 调用共用此修复，不改业务操作状态机。
- F04 `usePersonalWorkspaceWriteIntent` 仅组件实例内 Map，冻结参数与键；COMMITTED 在后续 GET 前确认，未知保留、终态释放。新 `WorkspaceWriteRecovery` 在资料页/任务关联/议事关联提示“重试原操作”，不假称只读查询。
- 最新原型仍为 `specs/juyiting-ui-baseline-20261006/prototype/interaction-completion.js`；原位补充分项引用计数、过期确认和未知结果重试，明确离线演示。


### 17.12 实施与统一验证收口（2026-10-16 19:26，未发布）

A/B1/B2已实现并合入双端develop：API `58b4b5f408257c6d5103d915e13c7927c1571e20`；Web `0bc9af441e10c714dca54dc2fca572dde477cbfe`。C/F13通过固定源码starter运行依赖解析确认原夹具7.0.2与应用7.0.8不同；只让测试图跟随应用解析，不升级生产依赖、不改公共头、不放宽前端校验。33条真实原始响应涵盖200/400/401/404/412，单请求ID与JSON信封一致；浏览器无去重代理通过。此结论是候选隔离实测，不是生产进程绑定证明。

后端147测试（107服务/HTTP契约单测、1真实MySQL+浏览器组合测试、39议事执行测试）与validateLayering PASS。前端正式Run217：3000通过/2pending，CI-only测试/构建/制品/扫描成功。UI及最新原型已同步精确计数、保留授权提示、确认过期和实例内原操作重试；原型仍为离线演示。

不纳入：跨刷新持久恢复、新lookup接口、全局响应处理重构、生产DDL/Provider操作/发布；基线空库初始化顺序问题另议，不以预置目录测试冒充修复。最终固定输入、XML、原始HTTP/浏览器、截图及日志在 `remaining/final-verification-summary.json` 和 `remaining/final-evidence-sha256.json`；完整历史失败日志保留。

### 17.13 用户授权发布收口（2026-10-16 20:06）

在§17.12开发验证后，用户明确授权发布。API1.16.7（58b4b5f408）先经本地同批293项测试/构建/原安装链完成；Web1.16.3（3a6b2ba739）随后经Flow4403172 Run218测试3000通过、2pending及构建部署完成。线上制品与健康核验通过，CI-only配置已恢复。最新原型保持离线参考并绑定发布源码。生产写交互未执行；生产发布前OOM故障已恢复但内存根因/监控问题未修，冷空库初始化问题仍为既有独立问题。完整记录：`docs/implementation/evidence/workspace-management-audit-20261016/release-remaining-20261016/release-summary.json`。

### 17.14 发布后页面验收发现（2026-10-16）

本次验收有两项实测缺陷，不以之前构建/测试成功覆盖：A01资料原操作重试成功后error未清；A02普通事项取消版本号跨端类型不一致（原资料改动之外）。代码落点、建议修复与回归边界已列`docs/implementation/evidence/workspace-management-audit-20261016/online-acceptance-20261016/REPORT.md`。仅执行验收、未修改产品或再次发布；A01与A02须各自闭环后才能标全部通过。

## 线上验收A01/A02补充修复（2026-10-16；Web c84c5a2a279b2a662b4b6b2f1b26c4708317b1ab）

仅前端1.16.4，API1.16.7不变；公共接口标准`api/docs/interface-standard.md` v1.2。

- **A01根因**：原操作首次调用清理error，但同key重试调用保留的execute，不重进mutate；成功notice与旧error并存。`usePersonalWorkspace.js`在execute每次尝试开始时，仅在原snapshot仍拥有当前视图的情况下清空旧error；不在异步成功后无条件清空，避免擦掉期间产生的新校验错误。请求key/If-Match/payload、身份代际、旧目标回执隔离均保留。更名/回收/恢复共用该实现；不改公共写意图工具和关联适配器。
- **A02根因**：`useHallOrdinaryCancellation.js`把服务端字符串版本转Number，POST输出数字，且回执校验仅接受Number；后端当前请求/回执均是规范十进制字符串，导致真实页面400。复用`taskEventVersion.js`的parse/compare/next，通信仍为字符串，比较/增量内部BigInt无精度丢失；不改变后端字段或JSON序列化、不新增兼容分支。拒绝非规范值/数字/超过Java Long范围；MAX只能是成功回执/回读，不可再发取消。现有资金取消不变。
- **代码范围**：两个composable、两组行为测试及两处既有UI消费者断言、package/lock根版本；无依赖、样式、布局、公共协议和后端修改。
- **定向证据**：258项受影响行为回归、42项真实SFC消费者回归及产品文件lint通过。Flow219全量发现两处旧数字断言（3023通过/2pending/2失败，未部署），在第二提交只将旧断言更新成字符串并修正测试标题，未降低校验。完整失败保留在`release-acceptance-fix-20261016`；新固定提交Flow220正式测试/构建/部署和线上复验结果单独收口，不能以此段实现说明视为已上线。

### A01/A02发布与验收结论（2026-10-16）
上述c84c5a2候选已作为Web1.16.4发布：Flow4403172 Run220 SUCCESS，3025pass/2pending/0fail，部署单71272066一批一台成功；366个安装文件和11个公网资源与同Run包SHA256 `abd9ef25c332120d4bb58fba116353776211d58e4e08d4ed6fb9b9605edbdab5`匹配。真实页面两缺陷PASS：A01同key/If-Match/payload重放后的旧错误消失/成功通知存在，revision只到2；A02任务463按字符串版本0取消、回执及GET版本1/cancelled，重开无重复POST。原CI-only恢复readback一致，后端PID/JAR/health未变；无CSS/布局变更，不扩改交互原型。完整证据`release-acceptance-fix-20261016-r2/release-summary.json`（位于本任务evidence目录）；自动化长整型/身份/回收恢复边界不冒充生产同类全部实测。
