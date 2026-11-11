# develop本地构建与发布复验（2026-11-07）

## 集成与固定源码

- 本地根develop与远端已分叉，主工作区存在其他任务的大量脏文件。为不夹带48个本地历史提交、不覆盖远端30个提交，隔离控制树从远端d000cb43精准挑拣本任务4个策略提交；README/策略文档冲突保留双方内容。没有强推、没有修改原主工作区HEAD/index或未提交字节。
- 远端develop控制面03fa59380dc5df32e2e98e24ee9b269b48117165，补齐已获授权的本地规则与本任务精确登记，并将gitlinks固定API638896a16cbf3f6df602a65f9a6c97b4ceb4889b / tree50384c91391b7e5b3f71931996ec53ab7dcb8fd8、Webc1e478f633845a448833a3973e732a12a75874aa。组件源码无新增修改、未重复触发Flow。
- 原本地develop仍保留原历史与脏修改；这里“合入develop”指已正常快进推送并readback的远端develop，不谎称已清空/重置原工作区。

## 实际执行与耗时

| 阶段 | 实耗秒 | 结果 |
| --- | ---: | --- |
| Web依赖 | 12.434 | npm ci |
| Web测试 | 4.216 | 50通过、2pending |
| Web生产构建 | 23.501 | 原Vite配置，完整生产资源 |
| Web打包／完整性复核 | 9.267 / 1.669 | 同批全文件摘要核对 |
| Web构建包装墙钟 | 53.900 | BUILT |
| API Gradle | 168.287 | 107通过、0失败/错误/跳过；分层、公共artifact/POI及fresh bootJar |
| API打包 | 36.635 | 原producer及来源/摘要证明 |
| API构建包装墙钟 | 213.060 | BUILT |
| 本批构建总墙钟 | 269.094 | 4分29秒，含阶段衔接；不含未执行的安装 |

- API builder内部墙钟212.942秒；与外层213.060秒差异为启动/控制开销，不把并行Gradle任务耗时相加当墙钟。67个JavaCompile任务命中缓存，测试/最终JAR/分层检查均fresh。此次不是全功能计费回归证书，也不是冷缓存承诺。
- 共同600秒预算仅约束本任务构建cgroup；Web结束后API分到543秒剩余预算。未在限时构建cgroup里启动生产JVM。
- 首轮22.428秒即失败：我准备的Web稀疏输入遗漏接口契约mjs，41通过/2pending/1失败。原result、日志、报告保存于attempt-01；补齐mjs及interface-standard fixtures后另起02批，未改测试、未将旧失败标成功。269.094秒只代表02批，不将跨批相加伪装完整发布。

## 发布阻塞，不伪报成功

- 只读information_schema核验：生产jia.economy_account仍为balance_micro，economy_escrow仍为gross_micro/captured_micro/refunded_micro；当前develop mapper/DDL已使用balance_wen等WEN列。
- 直接安装会导致资金SQL不兼容；当前任务未擅自转换/重置余额、改生产DDL或启用资金活动。因此API/Web均未切换，完整发布600秒验收为NOT_MEASURED，不是PASS。
- API仍为原PID2168125，原API/Web安装记录SHA未变；原生产健康UP、签名就绪、未认证场景401。这里只验证旧生产未受影响，不作为新候选线上验收。
- 下一步先明确并演练带备份/可恢复的MICRO→WEN切换及受影响计费/托管回归，再在授权范围安装上述固定包。不能只凭快速基线和健康200忽略资金语义。

## 目录与收口

- 工具链`/home/isp/apps/dragonwell-21.0.11.0.11+10-GA`；缓存`/home/isp/state/cyf-local-build/gradle-home`；构建任务`/home/isp/state/cyf-local-build/tasks/cyf-develop-release-20261107-02`。
- 新包已原子归档到`/home/isp/pkgs/cyf/cyf-develop-release-20261107-02/{api,web}/package/`，包外证据复制后删除自有API编译中间产物；不增加临时软链接、不将运维归档放回wsps。原result的构建路径是历史事实，archive.json记录映射，不重写历史。
- 两包均已显式mark-complete，保留原24h/每组件最近两批/当前回退/锁/摘要保护；清理plan本次0可回收。不是按目录年龄自动删除新包。
- 已有主机helpers保留其独立演进历史，未用仓库候选整文件覆盖；安装与仓库SHA分别记在integration.json，不宣称两者完全相同。控制器24、API原生LOCAL28、Web原生LOCAL37项隔离测试均通过。
- 证据：`/home/isp/wsps/cyf/docs/implementation/evidence/develop-local-release-20261107/`；私有执行原件`/home/isp/state/cyf-local-build/evidence/develop-release-20261107/`。目录内不含运行包或生产数据库数据。
