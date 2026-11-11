# 1.9.1 统一发布跟进

用户已授权发布后回归，通过后通知验收。1.8不单独发布。

## 发布前发现与修正

此前只核对bugfix命名分支与已知补丁，未覆盖实际运行记录中的后到hotfix4744acd4/a105dd6d。发布前只读发现线上a105dd6d含新的WS Origin处理/注册失败阶段诊断，避免覆盖回归后补齐；原release/1.9.0保持不变、不部署。

- API修订14f3ec867397c29eac24128e7ce0da8f832b1542/tree8813a596c97869e3c5bdafc886716f56c910f2b9，Web不变41ca32b72fda97e8066783dc702b1218305ca395/tree0edb17f4f5420670630ab2b0f713a644a8af4bbd。
- 两仓develop/release/1.9.1已非force推送和readback。Handler/其runtime auth测试/生产properties与实际线上a105dd6d的Git blob完全相同。
- runtime auth6/6、capability6/6、D09 ACL4/4；bootJar成功。公共制品验证64为未变验证器测试证据，新JAR验证完成；不冒称全API套件。
- 新JAR SHA256：9ee73ac6817a0761b45b4040a28923a6c4d181e24db5c5bff7fe0271bfacbd1f，221450151 bytes。
- Web复用已验证制品aa66fa27a93228ded4708877b4393477b5c6042c508791d6e3a73a17f84813f5，308+7相关测试及99隔离浏览器证据保持原树绑定。
- 主控证据：`/home/isp/wsps/cyf/deliverables/releases/v1.9.1-verification-20260918/`。

## 当前动作（部署尚未宣布完成）

唯一运行Owner01a0af7b-859c-7c82-aba0-2eeb9137f17d准备可恢复API→Web安装，用户与主控明确授权接管canonical运行目标，但必须锁内复核当前PID/startticks/JAR、无foreign生命周期在途、真实容量及健康。只等待互斥，不终止其他任务。主控协调/文档，不控制进程。

验证Owner01a0afdd-97ce-75b0-91c9-da9cda13eb47准备真实HTTPS/OAuthPKCE/Chromium回归，部署后才执行。无DB数据/结构变更、权限授予、ops开关、语音或付费Provider激活授权。新看板保持原受控启用边界，不能将无权限账号无法读运维数据当作修复失败。

尚未得到生产健康/线上业务回归结果，不通知用户验收通过。后续实际回执追加到本文件，不改写1.9冻结历史。

## 停机恢复归因与主控交接（部署前）

运行Owner读到 kernel OOM 证据：2026-09-18 00:14:09 旧API PID2077380已被系统OOM杀死；当前无10018监听，不是发布重启失败。外置经济只读配置当前不存在，不能直接宣称原线上能力仍在。

主控于本次继续执行时明确授权该 exact Owner 按 ABSENT_OOM 停机状态接管并安装/启动新制品，仅恢复 `economy.read-only-preview.enabled=true`。这是恢复此前已上线配置（依据 `docs/implementation/V1_7_LOCAL_RELEASE_RESULT_20260917.md`），不新增交易、语音、收费或ops权限；保留配置原不存在证据和恢复路径。锁内重新校验，若出现foreign生命周期不抢占。准备验证通过不是安装完成；实际结果待追加。

## 实际发布完成（2026-09-18 01:42 CST核验）

- API→Web 已完成；API canonical record创建于01:37:50，启动1次、无回退；Web于01:40:08完成，实际HTTPS首页/聚义厅/入口JS字节与制品一致。API为UP，PID2160063/start_ticks3123921946，JAR与上述候选一致。三把发布/生命周期锁已释放。
- API source `14f3ec867397c29eac24128e7ce0da8f832b1542`；Web source `41ca32b72fda97e8066783dc702b1218305ca395`，冻结分支均为 `release/1.9.1`；包含1.8/1.9与后到热修，不覆盖1.9.0冻结分支。
- Web index SHA256 `cdf2aa63cdbe4ceacb5fee380cfd941a0fbf9199fa48b4402d0279be9fdd9628`；dist tree SHA256 `71cf89effe55c7639c36e8f61e47ba6c4817db44ac3c9f14a6bba9d37a955596`，入口 `/static/index-Dvxp0grB.js`。
- 最终运行回执：`/home/isp/wsps/cyf/deliverables/releases/v1.9.1-local-20260918/release-outcome.json`，SHA256 `8139312ff108e513f96d4fa108a66e1d4ab6642f405fa8b1b5526859a5143a52`。其中记录精确canonical record、恢复副本、摘要、OOM归因和配置授权；未执行回退/生产DDL/DML/付费调用。
- 本地授权发布 `build_origin=local_user_authorized`，`flow_run=null`；没有伪造云效成功。部署后已向回归Owner发送真实认证API/Chromium执行GO；业务通过结果稍后追加。
- 观测root余量约62MB、MemAvailable约1.07GB。通过同盘硬链接避免重复JAR峰值并保留恢复副本，不将固定10GB作为发布门槛；磁盘容量仍需后续专项治理，不代表风险已解除。


## 后续归档引用

1.9.1实际回归暴露既有OAuth同FQCN Controller遮蔽，`/resource`404保留FAIL。已通过1.9.2最小修复并真实API46/浏览器113通过；当前应验收**1.9.2**，不是重新发布/覆盖1.9.1。最终见 `docs/implementation/V1_9_2_RELEASE_RESULT_20260918.md`。
