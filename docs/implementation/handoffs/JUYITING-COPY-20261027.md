# JUYITING-COPY-20261027 内测工作台文案实施

## 范围与Owner

- 用户2026-10-27确认实施既有审计方案；唯一Owner copy-owner-20261027，角色developer；不派独立Reviewer，不部署。
- 方案：`/home/isp/wsps/cyf/specs/juyiting-ui-baseline-20261006/optimization/copy-audit/recommendations-20261027.md`。97条包含保留项与事实待核实项，不等于97项全要改。
- 已读根/Web AGENTS、编排README、项目地图、当前UI方案；技能旧自动部署口径服从根2026-10-22规则。
- Web基线1102350543846e59f2c31dfc36145155da4f7773/tree1a1b113107e810c52be45b3d59199098e4af24a8，2026-10-27 fetch/ls-remote核对develop；旧主工作区HEAD ca22ac2，原型与规则有他人脏改，不切换或覆盖。
- 仅因旧checkout与develop差异且原型脏改，无法安全复用；使用本任务唯一隔离工作区`/home/isp/wsps/cyf/.worktrees/juyiting-copy-web`，branch codex/juyiting-copy-20261027，结束保存证据后清理，不动他人worktree。
- 接口规范固定`/home/isp/wsps/cyf/api/docs/interface-standard.md` v1.4（2026-10-24）；无API/Runtime或wire变更。
- 目标：统一轻量主线命名，精准表达资料授权、费用未知、验收完成后果、恢复查询与重放区别；保留地图文化名、技术接入资料、身份/ACL/幂等/摘要与锁。
- 非目标：新增内测资格/价格/退款承诺、改权限或业务流程、移除功能/校验、改公共范围、整站框架重构、生产发布。
- 最早定向验证：现有原型预览三尺寸检查；Web文案及状态映射/真实SFC针对性回归；正式完整测试和构建固定源码走Flow4403172 CI-only，总Run≤600秒。
- 唯一台账：TASKS.yaml#runtime_ledger_json，本文件不另记运行gate。

## 实施、验证与边界

- 原型先于产品：唯一原型沿用18786预览，精确补丁未覆盖原脏改。旧交互45项、文案5页×3尺寸48项通过，异常0；最后投影同步仍走同一原型，不另建页面。
- 首轮候选Web1.16.60，commit30d258a931711026f67454795ec734e29bad28e9/tree daf1509a128f34c5bdedbec768f5c6bd0aa9dddb；66文件（含34产品源码、原型/规格、测试、版本元数据）。AST去中文文案后脚本一致、条件/事件绑定仅文案变化、CSS无差异；Vue编译通过。
- 定向测试先发现旧文字断言，保留原业务断言并精确更新：批次350pass/4旧断言失败，4项修正回归通过；新增范围110pass；语音/预览修正后2pass；其他分批明细见原日志，重叠不相加冒充唯一测试数。完整正式测试以Flow当次结果为准。
- lint最初31文件对固定基线：356errors/112warnings，规则与消息集合完全一致，非lint全绿；未借文案任务格式化旧代码。历史专用O03测试固定旧worktree，不修改或拿本任务目录冒充其历史验证。
- 97条审计处置矩阵：`specs/juyiting-ui-baseline-20261006/optimization/copy-audit/implementation-20261027.md`；正式事项/公共议事/维护权限真实可见范围仍待认证核实，内测规则/价格/反馈渠道不虚构。
- 证据目录`/home/isp/state/juyiting-copy-implementation-20261027/`，包含before原型快照、所有失败与修复日志、AST/编译、lint基线对比、浏览器截图与检查。未部署。
- 已读与沿用现有Flow控制工具，启动前核对CI-only无deploy作业、远端基线及所有历史Run/活动Run；不覆盖流水线配置、不取消他人Run。
- Flow终态与清理见下方收口记录。

### 首轮CI归因与新候选

Flow4403172/345测试3444pass、2pending、2旧文案断言失败，未执行构建；精确源码30d258a。仅修正juyiting-hall-deliverables与juyiting-prototype-draft-flow的文字预期，原业务断言不删，8项定向通过。新候选f0d1eca00e5c7e8f3ec59aed80a9d2783eee123a/tree e8f0f4b9243760e2d98b8fc10cec8550f0ea37bb，版本仍1.16.60，产品源码与首轮一致；总68个差异文件。原失败日志/run345上下文保留，不原样盲重试。


### 最终CI收口（2026-10-27）

- 最终Web1.16.60：f0d1eca00e5c7e8f3ec59aed80a9d2783eee123a / tree e8f0f4b9243760e2d98b8fc10cec8550f0ea37bb，已推送并readback远端develop；不是旧主checkout的运行版本。
- 首轮345总耗时97秒，3444通过/2pending/2旧文字断言失败，构建未运行。第二轮346总耗时105秒（02:10:10—02:11:55，Asia/Shanghai），3446通过/0失败/2既有pending/0 skipped，构建、扫描、制品上传SUCCESS。未改选择器、跳过测试或云端配置，不部署。
- 346同Run制品SHA-256 5176b209b095eff5566ac0ec6a2be2184e4254ef4612690d8161d06a4a80bdb9，109567344字节；源码/版本/Run一致，612项dist摘要核对通过。报告、release manifest、源码commit/tree及提取文件摘要保留run346/；完整验证索引verification-final.json。云端日志为脱敏尾段，未宣称完整。
- 实施矩阵70已实施/17保留/6部分实施或收窄/4待事实核实；最终所有明细见implementation-20261027.md。权限/公共可见范围、内测规则/价格/反馈渠道不以文案替代认证验收；如需上线需另行授权、固定候选并走版本化部署。
- 本任务只记录文案实现及候选CI完成，不改变API/Runtime/生产基线。当前状态：安装未执行、线上健康/业务验收未执行。

- 清理完成：本任务唯一隔离worktree、node_modules符号链接、浏览器profile及临时制品下载已删除；源码在远端develop/本任务分支，最终补丁与摘要、612项manifest、测试报告、浏览器证据、原型修改前快照与Run345失败证据保留。cleanup.json与source-closeout.json为收口索引。未清理其他任务工作区、主checkout脏改、预览服务、共享依赖、生产状态或备份。

### 用户继续：剩余事实核对与R05补改（2026-10-27）

- 继续授权仅用于剩余核实和文案修正，不解释为部署授权。唯一Owner仍为copy-owner-20261027；接口规范固定v1.4（2026-10-24），无接口/权限/业务行为改动。
- 07:55 +08:00只读ls-remote：Web develop=f0d1eca，API develop=6dbb9cfe2fb105632c49568e9d62556bc5752bf5；本地Web ca22ac2仍旧且原型/规则脏，本地API516267bf与远端不同且文档脏。API只对已存在的固定6dbb9cf Git对象读源码，不将本地HEAD或远端源码视为线上部署证明。
- 新证据fact-check/r05-result.json：实际固定SFC+实际草稿adapter挂载，隔离HTTP/storage，6项通过。412保留当前输入；读取目录不替换；打开服务端草稿会fill替换，未保存输入没有单独持久副本。原“先恢复再决定是否重填”次序会误导，需先提示复制。
- R05新增目标：只精确修正两处冲突提示，明确“本次修改未保存，重新载入会替换当前输入，请先复制需要保留的内容”，不新增备份/自动恢复承诺；补组件回归，保留If-Match与身份隔离。非目标：改加载行为、新增本地敏感正文存储、修改ACL/资费或部署。
- 第一阶段已按要求清理隔离工作区。此次新增修正仍因主checkout旧且脏无法安全复用，复用原任务分支及原位置，仅恢复一个必要隔离工作区用于这次新改动，不按测试阶段/失败重试重复建工作区；结束继续清理。验收先本机轻量冲突回归，再固定新源码走现有Flow CI-only，600秒总上限不变。

### 续办交付

- 最终源码 `f4e7f779304ee20efa3e6f29a6830a03d20ec88a` / tree `fcd31763d8fd2484eb1ac03d4f7f5c28497ec34c`，已集成并readback远端develop；未部署候选版本仍1.16.60（未升新发布版本）。
- **Flow4403172/347 SUCCESS**，2026-10-27 08:08:37—08:10:39 +08:00，总耗时 **122秒**；release profile **3447通过、0失败、2既有pending、0 skipped**，Vite生产构建、JavaScript扫描及制品上传均成功，无部署作业。未改测试selector或独立资产/性能专项范围，未删回归。
- 同Run制品109566527字节，SHA-256 `f4a0c48868541cd22c018794524ac8ad942f5a596094dfc4e776d90dd8d15816`；源码commit/tree/版本/Run匹配，612项dist文件摘要逐项匹配release.json，冲突提醒与既有主线文案在产物中采样命中。测试、manifest与源码标识保留fact-check/run347/；verification-final.json、web347-meta.json、web347-artifact.json为索引。
- 真实生产账号ACL/外部Provider/商业规则没有验收，生产安装、线上健康与业务验收均未执行。Flow346仅代表上阶段f0d1eca，不覆盖本轮新候选。
- 轻量定向50项通过；真实SFC+真实adapter隔离挂载6项通过；2文件AST去中文后相同、CSS/绑定无差异、Vue编译通过。新组件用例首轮共享状态污染导致旧测试1项失败，已在新用例finally恢复原状态后整组50通过。失败及修复日志保留fact-check/，无删除原断言。
- R05对应已实施，整体71/17/6/3；其他权限仅明确到源码层，生产账号验证仍缺本轮授权身份/fixture配置。需要用户提供安全配置入口及确认内测对象、费用未知展示、反馈渠道；不要求在聊天中发送凭据。

本轮必要隔离工作区、依赖符号链接、临时制品下载及编译临时文件已清理；精确源码/补丁与所有必要证据保留，见fact-check/cleanup.json。未动他人工作区或生产。
