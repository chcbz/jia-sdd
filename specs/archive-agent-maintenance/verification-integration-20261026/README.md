# 典籍岗位完整性复核（2026-10-26）

## 范围与授权
Owner：本会话；用户要求检查四个岗位分支完整性，满足条件后合develop、统一部署验证。本次先复用现有工作区只读核验，未切换分支、覆盖脏文件、重复合并或启动发布。跨端接口基线为 `/home/isp/wsps/cyf/api/docs/interface-standard.md`（2026-10-14冻结及现有后续兼容补充）。不包含多区域租户、不默认给业务账号新增公共典籍管理/发布权限、不自动任命林冲。

## 已确认
- 四个用户指定提交均是刷新后origin/develop的祖先，已无需再次合并。source-audit.json固定完整SHA。旧2026-10-24 NO-MERGE不是当前合入结论。
- API已有8047850b等后续当前管理生命周期适配；Runtime当前PositionSkillReconciler复用parseManagementMessage、manager.handle与持久真实回执，没有恢复旧removeGranted安装器。
- Web已有ArchiveMaintenance界面和useArchiveMaintenance；API controller会将内部View映射成扁平wire DTO，与页面读取结构一致。Runtime nativeFetch统一包装HTTP请求，因此业务result信封外HTTP包装不是缺失；不能只看片段误判不兼容。
- 本机轻量定向：当前Runtime d97449ca，`node --test conf/codex-bridge/test/archive-position-skills.test.mjs`，9通过/0失败/0跳过，约3.1秒；含真实临时目录PREPARE/ACTIVATE journal、撤回结果隔离、确定性文本解析及发布冲突处理。非生产安装、非正式Flow、更不是线上业务验收。
- 当前生产JAR已包含两个SQL资源，逐字节匹配API516267bf，摘要见production-preflight.json；不是源码遗漏。

## 当前部署缺口（只读生产证据）
1. 五张表全部不存在：agent_position_state、agent_position_authority、agent_position_operation、archive_skill_maintenance_job、archive_skill_maintenance_action。源码只提供受控SQL，不自动启动DDL。须用精确SQL/制品来源执行有恢复记录的加表迁移，不能靠重复部署补齐。
2. 生产商品版本目录无archive-maintenance技能。源码1.1.1包标记PREPARED_NOT_PUBLISHED，尚不能供岗位安装。需要原包审核/发布服务及摘要，不直接伪造安装/订单/权益。
3. 岗位权限表缺失，因此未建立此功能的管理/公共书库授权。上线并不授权自动给任意业务账号授予ARCHIVE_WRITE/ARCHIVE_PUBLISH，不能默认任命林冲。需明确验收管理账号、任职Agent和发布范围后才能做生产写闭环。
4. 当前版本的浏览器登录→定义岗位→任命→实际安装→草稿→明确授权发布→读回→撤任/GENERAL保留，尚未取得整套生产证据。旧Flow296及当前9项本机诊断不替代它。

## 下一批最小交付顺序
- 复用既有Flow5260799，固定API516267bf与Runtime d97449ca（如再有改动重固定），补positionSkillsTest、archiveMaintenanceTest及受影响reader/security专测；独立MySQL fixture，不连生产测试。
- 复用受控迁移/安装工具，核对五表精确DDL及已存在典籍reader表，不对旧表执行破坏性DDL；迁移只创建结构，不自动授予权限。现有F06专用schema工具仅允许F06固定SQL，不能直接用它运行岗位SQL。
- 使用既有技能发布服务注册固定1.1.1包，按用户明确的业务权限主体初始化最小岗位定义；不创建假商城订单。
- 若应用字节不变，不为“统一部署”重复替换已验证程序；迁移、包/岗位配置、程序安装、业务验收分别记录。若需源码修复则固定新版本走同Run制品发布，每Run≤600秒。
- 真实页面验证无岗位Agent普通技能安装不依赖岗位；选定任职Agent验证任职/维护/撤任和历史读回。原林冲UNKNOWN记录不重放、不伪改成功。

结论：代码已合入；当前不是完整可用部署。已完成本轮静态/轻量/生产只读核验，生产迁移、技能发布、权限初始化和端到端验收尚未执行。缺少业务授权主体时不自行赋权。
