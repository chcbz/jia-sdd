# UR05 本地不可变 API 制品安装接缝（只读）

2026-10-08；唯一 readonly support，非 Reviewer。仅输出本报告与JSON；未执行测试/构建/安装/服务/HTTP/MySQL/Flow，不是验收或上线证明。

根HEAD仅上下文：`cd2c6ef361f6cccee9a83b2a678dac7d19f9320a`。三host源文件modified、orchestrator untracked；实际源字节按文件SHA绑定，不当作HEAD已提交内容，不覆盖他人修改。

## 核心结论

不是加一个下载参数即可：真实local producer + root local admission + 同一durable安装事务的精确local来源绑定，并同步schema验证/一次性授权。buildId不能伪装FlowRun。同版本必须绑定commit/tree/JAR+包摘要和同批日志/验证证据；不从脏源码/生产目录编译，不恢复pullbuildrestart。最低新增建议local-deploy和local packager，复用事务/lifecycle，不复制状态机。五份source/installed SHA全部不同；线上实现与恢复未知。

## 每条实际路径/行/SHA证据（SOURCE_ONLY不外推线上）

### F01 项目规则与源码归属 [SOURCE_ONLY]

后端本地串行正式验证/固定干净源码/同批不可变制品，前端Flow；无自动部署/生产目录编译。根HEAD仅上下文；三host源文件modified、orchestrator untracked，本报告绑定实际文件SHA，不覆盖他人文件。
  - `/home/isp/wsps/cyf/AGENTS.md:34-34 ; SHA256=bfaa0f2eedae4d07f5c221a49ccd3d4de15120aa503fb7e9b0a54a14e4e81f36`
  - `/home/isp/wsps/cyf/AGENTS.md:38-38 ; SHA256=bfaa0f2eedae4d07f5c221a49ccd3d4de15120aa503fb7e9b0a54a14e4e81f36`
  - `/home/isp/wsps/cyf/AGENTS.md:39-39 ; SHA256=bfaa0f2eedae4d07f5c221a49ccd3d4de15120aa503fb7e9b0a54a14e4e81f36`

### F02 受信输入/下载边界 [SOURCE_ONLY]

deploy root-only五参数pipeline/run/commit/version/artifact_sha256，固定API pipeline、正整数Run、40hex commit，root-controlled prepared downloads/<run>/package.tgz。它不是下载API调用器；本次有界source搜索未定位上游真实artifact download调用，UNKNOWN。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy:1097-1132 ; SHA256=ea0ab49b7ef90c2b7e9cc31d64e772f764396cfa50ac0f29e1a8c24a784f2ac7`

### F03 包/源/JAR与version绑定 [SOURCE_ONLY]

协调mutex内数字Run stale guard；外部包SHA→copy/fsync/replace incoming→再核SHA。精确五payload，receipt真实Flow org/pipeline/job/run、clean develop/commit/tree/success gates、实际JAR hash/size，root approval绑定source/run/receipt/JAR/consumed；versioned release外部version/commit/tree/package/JAR/receipt。没有证明外部version等于JAR实际应用版本。buildId不能伪装run_id或沿用Run数值排序。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy:1134-1166 ; SHA256=ea0ab49b7ef90c2b7e9cc31d64e772f764396cfa50ac0f29e1a8c24a784f2ac7`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy:1168-1255 ; SHA256=ea0ab49b7ef90c2b7e9cc31d64e772f764396cfa50ac0f29e1a8c24a784f2ac7`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy:1261-1279 ; SHA256=ea0ab49b7ef90c2b7e9cc31d64e772f764396cfa50ac0f29e1a8c24a784f2ac7`

### F04 root ownership [SOURCE_ONLY]

install零参数固定state/incoming/approval/record/canonical/lifecycle及生产root脚本路径。private offline模式隔离，生产fault禁用。state/incoming/backups root:root0700，lifecycle物理单链接不可非root写，canonical祖先物理root不可非root写，目录root:root0755，JAR root:isp0640单链接，approval/record root0600。这是源码要求不是本次线上权限验收。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:23-38 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:40-108 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:129-140 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`

### F05 锁顺序与持有方 [SOURCE_ONLY]

coordinator父持auto-approval-v2 mutex/noninheritable；installer持release FD8排他flock、inode proof，lifecycle核device/inode/held及实际fdinfo排他FLOCK，独立调用自己取FD8，再lifecycle FD9。installer退出后coordinator仍持协调mutex，重取同release并复核installed，F06后E05；不是FD8无缝覆盖所有schema阶段。local必须共享相同锁及顺序，禁止独立本地锁绕开/反向持锁调用。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy:1134-1139 ; SHA256=ea0ab49b7ef90c2b7e9cc31d64e772f764396cfa50ac0f29e1a8c24a784f2ac7`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:110-127 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit:339-416 ; SHA256=2b241e42b7c3e2b3a725e32f78ad70823f33b3b2e99980a744f440ba8322357b`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy:475-496 ; SHA256=ea0ab49b7ef90c2b7e9cc31d64e772f764396cfa50ac0f29e1a8c24a784f2ac7`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy:1053-1093 ; SHA256=ea0ab49b7ef90c2b7e9cc31d64e772f764396cfa50ac0f29e1a8c24a784f2ac7`

### F06 payload与容量 [SOURCE_ONLY]

unpack前闭合archive和实际candidate+rollback字节，区分FS，不新增任意资源/包/等待限额。same-FS canonical旁WORK仅清自己目录；五payload禁duplicate/traversal/link/nonregular；receipt/metadata/sidecar/provenance/Boot JAR结构/hash验证，candidate root:isp0640复hash。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:203-294 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:297-506 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`

### F07 backup与原子切换 [SOURCE_ONLY]

durable prepared先backup和生命周期，backup核旧hash/temp copy fsync/hardlink publish/dirfsync/remove temp，正常结束root0600单链接，已有backup必须完全匹配。activating落盘先stop+精确STOPPED proof，核candidate与old hash，再same-FS os.replace canonical/dirfsync；record root0600 temp/fsync/replace/dirfsync。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:515-574 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:602-625 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:627-721 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:1038-1079 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`

### F08 恢复源码与未知 [SOURCE_ONLY]

hash/health→durable active_pending→consume approval→installed。exact installed重入须consumed/hash/health；foreign unfinished拒绝；rolling_back只能rollback；active_pending exact健康可finalize；activating candidate/absent rollback-only。rollback intent先持久再stop/detach/restore；stop未证不start旧版，旧start/status失败durable保留；exact failed不自动重发、consumed无record拒绝。当前全crash-point测试覆盖未证明，已安装实现不同SHA，线上恢复UNKNOWN。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:724-905 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:913-1035 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`

### F09 backup路径未证 [SOURCE_ONLY]

源码/var/lib/cyf-api-flow/backups，项目指引/home/isp/baks；未读实际directory/link/record/backup，physical mapping UNKNOWN。冻结local时须明确布局和durable路径校验，不猜symlink/迁移。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy:21-25 ; SHA256=ea0ab49b7ef90c2b7e9cc31d64e772f764396cfa50ac0f29e1a8c24a784f2ac7`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install:23-30 ; SHA256=d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`
  - `/home/isp/wsps/cyf/AGENTS.md:56-56 ; SHA256=bfaa0f2eedae4d07f5c221a49ccd3d4de15120aa503fb7e9b0a54a14e4e81f36`

### F10 health/business接缝 [SOURCE_ONLY]

kit只start现有canonical JAR、无git pull/Gradle；PID/startticks/argv、listener归属、runtime user、JAR/runtime record与localhost200 JSON UP及稳定复验。spawn sanitized env/降权cyf-api/cwd canonical/关闭FD5–9。UP不证明身份授权/Runtime/动态撤销/在途安全/真实业务；仍待具体维护和业务授权。未执行kit/HTTP或读配置秘密。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit:23-51 ; SHA256=2b241e42b7c3e2b3a725e32f78ad70823f33b3b2e99980a744f440ba8322357b`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit:578-616 ; SHA256=2b241e42b7c3e2b3a725e32f78ad70823f33b3b2e99980a744f440ba8322357b`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit:694-737 ; SHA256=2b241e42b7c3e2b3a725e32f78ad70823f33b3b2e99980a744f440ba8322357b`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit:829-878 ; SHA256=2b241e42b7c3e2b3a725e32f78ad70823f33b3b2e99980a744f440ba8322357b`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit:892-930 ; SHA256=2b241e42b7c3e2b3a725e32f78ad70823f33b3b2e99980a744f440ba8322357b`

### F11 schema也严格Flow [SOURCE_ONLY]

两runner严格installed schema2/numeric run、receipt.flow固定org/pipeline/job/source、clean develop、record/receipt/JAR/provenance/source绑定，只认Boot nested mapper固定SQL/resource/hash/table catalog。local producer+entry之外必须适配真实local verifier和wrapper context/admission，不能fake Flow或跳过；此处不重复UR06 DAO调查。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-additive-schema:34-56 ; SHA256=f7d72fd9ea1dbc38ddca8caf7df4f38b635bcf5a0a82becdc3d6ec16709f18a8`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-additive-schema:424-506 ; SHA256=f7d72fd9ea1dbc38ddca8caf7df4f38b635bcf5a0a82becdc3d6ec16709f18a8`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-e05-additive-schema:34-51 ; SHA256=b4ec40a0da7f5620da167038c4f3a419d28396f64862ceeaac75d03bd26a70a9`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-e05-additive-schema:366-461 ; SHA256=b4ec40a0da7f5620da167038c4f3a419d28396f64862ceeaac75d03bd26a70a9`

### F12 schema锁/一次性/partial恢复 [SOURCE_ONLY]

wrapper重取release复验installed，runner root0600 filelock→MySQL named GET_LOCK(-1)，不取lifecycle。durable attempt/running，partial/interrupted不盲重试同Run；E05无exact admission可not_admitted返回0，绝非schema/feature完成。秘密不入installer/lifecycle/JVM仅runner。DDL autocommit保留partial，JAR回滚不撤表。local schema resume/admission未实现UNKNOWN待授权。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy:391-436 ; SHA256=ea0ab49b7ef90c2b7e9cc31d64e772f764396cfa50ac0f29e1a8c24a784f2ac7`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy:989-1093 ; SHA256=ea0ab49b7ef90c2b7e9cc31d64e772f764396cfa50ac0f29e1a8c24a784f2ac7`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-additive-schema:894-908 ; SHA256=f7d72fd9ea1dbc38ddca8caf7df4f38b635bcf5a0a82becdc3d6ec16709f18a8`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-additive-schema:1061-1088 ; SHA256=f7d72fd9ea1dbc38ddca8caf7df4f38b635bcf5a0a82becdc3d6ec16709f18a8`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-additive-schema:1234-1264 ; SHA256=f7d72fd9ea1dbc38ddca8caf7df4f38b635bcf5a0a82becdc3d6ec16709f18a8`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-e05-additive-schema:847-860 ; SHA256=b4ec40a0da7f5620da167038c4f3a419d28396f64862ceeaac75d03bd26a70a9`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-e05-additive-schema:1014-1041 ; SHA256=b4ec40a0da7f5620da167038c4f3a419d28396f64862ceeaac75d03bd26a70a9`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-e05-additive-schema:1187-1218 ; SHA256=b4ec40a0da7f5620da167038c4f3a419d28396f64862ceeaac75d03bd26a70a9`

### F13 历史completion不可直接作local恢复 [SOURCE_ONLY]

complete-installed-schema固定历史API_BINDING Run49/source/receipt/JAR且需opsFlow；coordination→release，exact installed证明、fixed runners/双plan/F06后E05、partial保留/no lifecycle/no feature。不是已证通用local recovery，不能历史binding冒充新build。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/auto/complete-installed-schema.py:27-43 ; SHA256=713df4d87bf410b7e1257f47553eb5866e8a901a6471e612d720a0ae21850a93`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/auto/complete-installed-schema.py:375-441 ; SHA256=713df4d87bf410b7e1257f47553eb5866e8a901a6471e612d720a0ae21850a93`
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/auto/complete-installed-schema.py:670-735 ; SHA256=713df4d87bf410b7e1257f47553eb5866e8a901a6471e612d720a0ae21850a93`

### F14 真实local packager缺失 [SOURCE_ONLY]

package-api.py固定Flow env/BUILD_NUMBER/build目录/preclean/post git diff，真实flow+source receipt/metadata/sidecar、mail runtime实际在bootJar及固定OpenCV provenance验证。不能假Flow env调用当local producer。需真正clean pre/post、同批logs/tests/validateLayering/JAR/provenance/应用version；干净checkout本身不证明外来JAR同批。
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/auto/package-api.py:30-105 ; SHA256=165887c1e50d6db286359e7c6de9a04098440634ff542267ba84edf5bc21d84a`

### F15 orchestrator不是安装器 [SOURCE_ONLY]

owner/gate/tree与actual cwd HEAD/tree/status严clean，Gradle lock前后两次核；短evidence lock/cache accepted能skip，artifact只是调用者给的引用非bytes/hash。local producer区分cached tests与实际本批bootJar/logs并绑定实际digest；本次不执行orchestrator或查active任务/锁。
  - `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py:19-28 ; SHA256=704b98df2e7f72f4ce3f5c6f548800d09f149d2235310fb562a20cea75ee4d6e`
  - `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py:548-575 ; SHA256=704b98df2e7f72f4ce3f5c6f548800d09f149d2235310fb562a20cea75ee4d6e`
  - `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py:626-710 ; SHA256=704b98df2e7f72f4ce3f5c6f548800d09f149d2235310fb562a20cea75ee4d6e`
  - `/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py:855-855 ; SHA256=704b98df2e7f72f4ce3f5c6f548800d09f149d2235310fb562a20cea75ee4d6e`

### F16 已安装只核接口/hash [INSTALLED_INTERFACE_ONLY]

五份installed对应脚本root:root0755物理单链接，source/installed全部SHA不同；public接口deploy五参数/install零参数+canonical/kit start-restart-stop-status+canonical与锁。仅静态metadata/hash/public constants核对，未读installed恢复实现/执行脚本，不外推线上等价、不覆盖。
  - `/usr/local/sbin/cyf-api-flow-deploy:21-34 ; SHA256=f4f07ce3330eca1b843ba720615e415d1f0addc5258d45795f03636c4e015b72`
  - `/usr/local/sbin/cyf-api-flow-deploy:1153-1153 ; SHA256=f4f07ce3330eca1b843ba720615e415d1f0addc5258d45795f03636c4e015b72`
  - `/usr/local/sbin/cyf-api-flow-install:23-38 ; SHA256=180f43cf0381c55dedd52a367d78f73f9713703b3794bd058432b22f992aed46`
  - `/usr/local/sbin/cyf-api-kit:25-47 ; SHA256=9685c35b8bff293f474d5f1684312ecff4f88d0cd6f87450ae6b433a992356c2`

## 已安装与source hash漂移（metadata 无源码行；仅stat/hash）

- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy` SHA256 `ea0ab49b7ef90c2b7e9cc31d64e772f764396cfa50ac0f29e1a8c24a784f2ac7`
  - installed `/usr/local/sbin/cyf-api-flow-deploy` SHA256 `f4f07ce3330eca1b843ba720615e415d1f0addc5258d45795f03636c4e015b72`：root:root0755、物理单链接，字节不同；implementation UNKNOWN。对应public接口行见F16。
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install` SHA256 `d5ba79b7d9bd8dd1c28d57f8d57d8d27cb5107d624b902cc56cfa99e6bc47ffb`
  - installed `/usr/local/sbin/cyf-api-flow-install` SHA256 `180f43cf0381c55dedd52a367d78f73f9713703b3794bd058432b22f992aed46`：root:root0755、物理单链接，字节不同；implementation UNKNOWN。对应public接口行见F16。
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit` SHA256 `2b241e42b7c3e2b3a725e32f78ad70823f33b3b2e99980a744f440ba8322357b`
  - installed `/usr/local/sbin/cyf-api-kit` SHA256 `9685c35b8bff293f474d5f1684312ecff4f88d0cd6f87450ae6b433a992356c2`：root:root0755、物理单链接，字节不同；implementation UNKNOWN。对应public接口行见F16。
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-additive-schema` SHA256 `f7d72fd9ea1dbc38ddca8caf7df4f38b635bcf5a0a82becdc3d6ec16709f18a8`
  - installed `/usr/local/sbin/cyf-api-additive-schema` SHA256 `7b028f665d466f52ae0237d71f5fe2574c79e6072fe3826d7dd746fdd8e4aa19`：root:root0755、物理单链接，字节不同；implementation UNKNOWN。对应public接口行见F16。
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-e05-additive-schema` SHA256 `b4ec40a0da7f5620da167038c4f3a419d28396f64862ceeaac75d03bd26a70a9`
  - installed `/usr/local/sbin/cyf-api-e05-additive-schema` SHA256 `d6ef15041ce84f4f7d1ecd65c8af3fa56c7bad198703afeea965150db787532f`：root:root0755、物理单链接，字节不同；implementation UNKNOWN。对应public接口行见F16。

## 最小source-only适配路径（主控待冻结，非已实现）

- P01 `PROPOSED_NEW_SOURCE_ONLY_NOT_FROZEN`：`/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-local-deploy`
  - 最小新增显式root local入口，消费local release manifest+包路径+独立expected packageSHA；无pipeline/run伪值，不下载/编译/pull，不含默认服务动作。最终CLI待主控冻结，当前不存在可执行local入口。 源码依据：F02,F03,F04,F05。
- P02 `PROPOSED_NEW_SOURCE_ONLY_NOT_FROZEN`：`/home/isp/wsps/cyf/ops/ci/aliyun-flow/auto/package-api-local.py`
  - 最小新增真实本地同批producer，绑定fixed clean source/version/actual build logs/test evidence/validateLayering/bootJar/provenance，保留mail/OpenCV完整性；可保留五payload，不假Flow env。 源码依据：F14,F15。
- P03 `NECESSARY_EXISTING_SOURCE_ADAPTATION`：`/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-install`
  - 复用唯一durable transaction engine，以最新精确local admission/receipt/record身份代替numericRun作为local恢复身份；不caller env降级、不local→fakeFlow重写、不复制第二状态机。root/locks/backup/fsync/stop/hash及全部recovery条件保持。若主控另冻结common core提炼可用cyf-api-artifact-install，但非最低必要新增路径。不保留产品旧契约兼容双轨；历史真实Flow诊断入口范围由主控明确。 源码依据：F03,F04,F05,F06,F07,F08。
- P04 `NECESSARY_EXISTING_SOURCE_SEAMS_FOR_SCHEMA_COMPLETE_LOCAL_RELEASE`：`/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-additive-schema`、`/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-e05-additive-schema`、`/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-flow-deploy`
  - 两runner需要真实local installed/receipt/source/JAR verifier；wrapper既有context/admission/attempt可供local入口复用，重锁复验、F06先E05、child-only秘密、固定SQL/resource/grants/metadata/partial保留。没有E05 admission不称完成。此接线不是自动DDL/feature授权；若冻结范围仅artifact安装，schema必须明确NOT_RUN，不能声称完整业务发布。 源码依据：F11,F12,F13。
- P05 `REUSE_NO_PRODUCTION_LOGIC_CHANGE_PROVEN_NECESSARY`：`/home/isp/wsps/cyf/ops/ci/aliyun-flow/host/cyf-api-kit`
  - 最低方案复用可信canonical lifecycle；未证明必须修改生产逻辑。保留身份/锁/FD/健康回归，source-installed差异先保存归属，不复制source整文件覆盖installed。 源码依据：F05,F10,F16。
- P06 `REUSE_EXISTING_CONTROL_PLANE`：`/home/isp/wsps/cyf/ops/orchestration/cyf_orchestrator.py`
  - 串行build/source/gate/evidence可复用；producer绑定实际本批bytes与logs，区别cached test与fresh build。没有证明须改orchestrator生产逻辑，不绕现有owner/exact-tree约束。 源码依据：F15。

## 显式local输入契约建议（非现行接口/安装授权）

root入口消费local manifest、包路径、独立expected packageSHA；最终CLI/schema待冻结，当前不提供可误执行安装命令。建议producer.kind为local-build-v1（不是当前wire）。

- release version derived from actual same-build application metadata, not external label alone
- actual local buildId, opaque; never flow.run_id or fabricated FlowRun
- 40 lowercase hex source commit/tree + actual pre/post clean proof
- test selector/fixture digest/results-report digests + validateLayering result evidence
- same batch build logs SHA256 and actual bootJar production evidence
- application.jar SHA256 and byte size
- dependency.provenance.json SHA256 and byte size
- receipt SHA256
- external package SHA256 and byte size

包内可保持精确五成员：`application.jar`, `application.metadata.json`, `application.sidecar.json`, `dependency.provenance.json`, `receipt.json`。

- Root admission independently binds expected version/buildId/commit/tree/receipt/JAR/provenance/package/consumed state; JSON self-assertions/checksums do not authenticate a build or authorize production.
- PackageSHA outside its own archive/receipt avoids circular hashing; internal metadata/sidecar bind identical receipt/source/JAR, external trusted admission pins archive bytes.
- Root0700 stage, noalias physical regular ingress, stable opened/copied bytes, root0600 singlelink private snapshot, package/hash recheck before lifecycle; no producer-writable path fed directly to runtime.
- Share current coordination/release FD8/lifecycle FD9 order; root owns durable state, JVM never owns locks. No independent local lock bypass.
- No numeric or lexical buildId stale order. Explicit root decision binds expected currently-installed JAR under shared lock; another build cannot adopt unfinished transaction.
- Backup layout must reconcile /home/isp/baks with historical record/backups constraints, not a guessed symlink or silent record migration.
- Fixed clean worktree build via orchestrator, never /home/isp/hosts/cyf/api. Only immutable canonical /home/isp/hosts/cyf/api/cyf-api-kit.jar install; do not restore pullbuildrestart.
- Existing actual dependency integrity/mail runtime/provenance preserved; no invented resource/package/time hardlimits.
- Schema/feature admission, production maintenance/inflight checks and business verification remain explicit separate authorization; partial DDL retained, JAR rollback is not DB rollback.
- No credentials/config bodies in manifest/package/build evidence or public logs; use existing private runner secret channel, retain identity/ACL/env boundary.

## 必须同步的已有测试（全部NOT_RUN）

这些覆盖静态/私有离线fake lifecycle或数据库fixture；不是线上安装、真实MySQL或业务证据。保留原全部断言。

- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_gate_policy.py` / `ApiGatePolicyTest`：NOT_RUN。
  - actual容量/不同FS/篡改/source/traversal/无任意limits，补local receipt负例
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_gate_policy.py:27-167 ; SHA256=99c44fce272d05ed38486255a081cd48c84e16f33904ece04f0a71464497a9e2`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_flow_install_lock.py` / `ApiFlowInstallLockTest`：NOT_RUN。
  - contention等待不变record/package；local-真实Flow同锁及FD继承
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_flow_install_lock.py:14-104 ; SHA256=0e5f0d502d92a2a7e4ac41370417bb60c8ea1e62076eafc640a19ee2e0df879e`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_canonical_path.py` / `CanonicalApiPathTests`：NOT_RUN。
  - canonical/root祖先/禁旧opt/FD5–9；补local入口
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_canonical_path.py:6-28 ; SHA256=a2da89b806245fabc1e1609a376dad57301081924a16f985b5f2d2eb7c3239c7`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_flow_deploy.py` / `ApiFlowDeployF06Test`：NOT_RUN。
  - F06一次/installed绑定/partial-interrupt不retry/child-only秘密；local context同步
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_flow_deploy.py:155-313 ; SHA256=a488842f460a70e22f0b959f5994b35dad0ccc741caceeb67ff32fe659db243e`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_e05_flow_deploy.py` / `ApiFlowDeployE05Test`：NOT_RUN。
  - durable admission-before-lock/partial/notadmitted/秘密/F06先E05；buildId不fakeRun
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_e05_flow_deploy.py:209-470 ; SHA256=2088a2c482db6d2f701f4fe98c1e500ce6d2b2370829a3a054c05e9ad3f886ba`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_additive_schema.py` / `ApiAdditiveSchemaTest`：NOT_RUN。
  - 固定SQL/两表/metadata/grants/locks/partial/binding；local source receipt JAR mismatch
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_additive_schema.py:453-941 ; SHA256=73a7614e4c02886403506b96ec1dd84931d19f5f33bcb949655837672aae8715`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_e05_additive_schema.py` / `ApiE05AdditiveSchemaTest`：NOT_RUN。
  - E05 exact resource/DDL等价/metadata/locks/partial/binding；local来源
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_e05_additive_schema.py:406-840 ; SHA256=6740303da48065ea0d7ee9de2a6ef59a85269623c4c1f1c2a16210cfdb2bfaf3`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_complete_installed_schema.py` / `CompleteInstalledSchemaTest`：NOT_RUN。
  - historical artifact/fixed runner/双plan/partial/one-shot/no lifecycle；不冒充local恢复
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_complete_installed_schema.py:285-504 ; SHA256=449f60be4fdd0aae0486aef0ba3e70a4c5a9b9c177cacbbfd739bac1df0ac2ff`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_versioned_deploy_adapters.py` / `VersionedAdapterTest (API)`：NOT_RUN。
  - 显式version+包SHA/失败非verified；local version-buildId-commit-tree-JAR-receipt-package负例，不改web
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_versioned_deploy_adapters.py:73-157 ; SHA256=67eec6fd8f041b5ce937c4bac5778176078e8b062893593e401432ca16fca420`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_startup_diagnostics.py` / `StartupDiagnosticsShellTest + StartupDiagnosticsInstallerTest`：NOT_RUN。
  - fixed诊断/错误不被掩盖/阶段/allowlist，common事务保留
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_startup_diagnostics.py:13-107 ; SHA256=1dbed77e5e0ef57d881f4f4d138f1aeaf126e533a295a8356aa9069b7961fd17`
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_develop_auto_release.py` / `AutoReleaseTest (bootJar only)`：NOT_RUN。
  - 实际bootJar mail runtime而非test classpath，local producer保留
  - `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_develop_auto_release.py:85-124 ; SHA256=ccf51b53a171ba8b9a2aebededa8192509fd7bea81c86ad838c1a19c6202bd70`
- `/home/isp/wsps/cyf/ops/orchestration/tests/test_cyf_orchestrator.py` / `OrchestratorTest`：NOT_RUN。
  - source clean/exact key/selector/fixture/cache/child identity；artifact引用或cachehit不能当本批JAR证明
  - `/home/isp/wsps/cyf/ops/orchestration/tests/test_cyf_orchestrator.py:120-299 ; SHA256=44667ca9892754ff367402e426f6c83ae8e00189c7cbbd50ae0091106ba5003c`

## 最小新增定向测试建议（新建议路径不存在，故无源码行/SHA）

- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_local_deploy.py`：PROPOSED_NOT_RUN
  - genuine local root admission, no fake flow/run fields
  - tamper version/buildId/commit/tree/receipt/provenance/JAR/package/digest/size/build evidence -> fail before lifecycle/schema
  - unsafe owner/mode/symlink/hardlink/path replacement/producer writable ingress -> failclosed
  - local/retained genuineFlow shared-lock contention, foreign unfinished release cannot adopt
  - install/schema/business distinct status; no failed verified, no secret inheritance/output
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_local_package.py`：PROPOSED_NOT_RUN
  - clean exact same-build source/version/log/results/JAR/provenance -> exact fivepayload bytes
  - dirty source/staleJAR/wrongversion/fakeFlowenv/failedvalidateLayering/missingmail/provenance -> no package
  - cached tests alone cannot claim fresh bootJar produced
- `/home/isp/wsps/cyf/ops/ci/aliyun-flow/tests/test_api_artifact_install_recovery.py`：PROPOSED_NOT_RUN
  - private fake lifecycle for low-cost fault injection only, not true readiness proof
  - fault prepared/backup/activating/stopproof/replace+dirfsync/active_pending/approvalconsume/installed record
  - activating rollback-only; commitpending exact healthy mayfinalize; differentbuild/consumed without record failclosed
  - rollbackintent/detach/restore/fsync/oldstart/status interrupted -> durable canonical old-or-absent; stopunverified never startold
  - partial schema cannot be reverted by JAR restore; explicit recovery not blind retry

## 未证/恢复UNKNOWN

- Actual upstream Flow artifact download API caller not located; inspected deploy consumes prepared run-scoped package only.
- Five source-installed hashes differ; installed implementation/recovery/why drift UNKNOWN, interfaces/metadata only.
- Actual canonical JAR/version/live process/release-lock holder/currenttransaction/schema state/backups NOT_READ. Report lock custody is source design, not current runtime holder.
- /var/lib/cyf-api-flow/backups vs /home/isp/baks physical mapping/recovery layout UNKNOWN.
- Local producer/admission/receipt/record/CLI exact scope not frozen or implemented; new source paths are proposals without existing line/SHA.
- Full crash-point coverage not proven in located tests; tests NOT_RUN; actual installed recovery UNKNOWN.
- Historical fixed schema completion cannot be claimed generic new local build recovery.
- Dynamic identity/revocation/inflight maintenance/business proofs still pending explicit authorization; actuator UP insufficient.
- UR03 H2 elsewhere does not prove MySQL/installer/fullGoal/E05/enroll or production; UR06 seams not repeated.

## 下一步（由主控冻结/调度）

冻结local provenance/admission/receipt/record、实际backup布局和源码Owner范围；先私有离线完整性/共享锁/断点恢复回归，再经orchestrator正式串行后端验证和同批不可变产物证明。真正安装、DDL、生产维护、动态身份/在途核对、业务请求仍须具体授权；本报告不触发它们。

自检仅报告JSON结构、引用行范围和所有snapshot摘要稳定。实际测试通过数0，NOT_RUN。
