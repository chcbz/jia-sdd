# 1.6.0 本地代码发布结果（2026-09-17）

## 发布结论

前后端已从各自组件`develop`固定到远端`release/1.6.0`，使用本地已验证制品完成发布。API于北京时间12:36:34、Web于12:48:34获得`DEPLOYED_HEALTHY`记录。不是Flow发布，也不代表生产语音Provider已经激活。

| 组件 | 远端develop / release/1.6.0固定提交 | tree | 实际发布制品SHA-256 |
| --- | --- | --- | --- |
| API | `a8e9170873062165176626775d66c92dfc2e7a1a` | `7ed64de0a3519b18b14f1ea8fe82463fa0993679` | `82ef8e26fe7745a9a6a01d83560ddd2d7dd7846aea1425b2c0ac89ec4f2714fb` |
| Web | `74420db2c82fb2f5dee673f337c13bb546d53f93` | `4e4b4924ea7bb3a26b649726424f3ae2b81a4202` | `d8c5c0778821aaf37996cdc42906665a3cf9ad932485755d0ceab3075d462cc9` |

版本号为联合发布列车标识，分别绑定前后端commit/tree/制品，不改写历史组件包版本。上述develop为冻结时读回，develop后续可继续前进，release分支不得随之漂移。

## 交付内容

- 语音慢发送/慢回复不再仅因120秒关闭回合；发送中、等待回复中可停止等待，迟到响应隔离，不冒充撤回已发送文字。
- API语音身份、租约和传输配置整改及真实HTTP回归；修复两处任务会话查询错误传入tenant而非owner身份的问题。
- 成果正式交付版本校验修复，补齐W11夹具，修复本机真实Chromium测试执行/溯源问题。
- 保留已经上线的`e95ecfad` owner-scoped schema恢复；没有用旧基线覆盖其他任务修复。

## 验证及边界

- API：voice/chat **146/146**、独立定向schema **5/5**、public-artifact verifier **64/64**，0失败/0skip；bootJar成功。不是整个API多模块全量测试。
- Web：全量Mocha **2186通过、0失败、2既有pending、0 skipped**；Vite生产构建成功。两项pending为原有小程序入口/方向合同，不伪报通过。
- 实际API进程PID **1759469**，start_ticks **3119227686**；canonical launcher启动后47秒健康UP。
- Web实际dist tree SHA `acb84f6600445c66b43506a443b36db4b0dd3d1dd87019119a44524995932b2d`，入口`/static/index-dLN-B6Gr.js`；规范发布健康检查通过。
- 未做生产DML、Rabbit操作、付费Provider调用或启用配置。真实STT/TTS与设备体验验收仍单独待办，不能称完整语音Beta已验收。

## 中间异常与修复

第一次Web预检在任何变更前停止：旧guard仅匹配launcher路径文本，无法区分健康cron只读status与生命周期操作；原PID已退出，保留归因为UNPROVEN，不补造历史。自然样本确认健康cron会执行status并短时持锁。r2根据可执行文件、脚本argv位置及真实subcommand判断，并按API→Web顺序阻塞取得实际锁后重新检查。未暂停健康检查、未抢锁、未操作foreign进程，API成功后未重复启动。

磁盘曾受并发写入降至约35MB；按实际制品暂存/回退容量核算，安全清理本次可再生构建输出及已合入且无进程使用的独立依赖缓存后继续。未删源码、证据、在线文件和回退包。发布后磁盘仍偏紧，后续构建前继续按实际用量核算，不设任意固定预留。

## 证据

- 冻结输入：`/home/isp/wsps/cyf/deliverables/releases/v1.6.0-local-20260917/release-input.json`。
- API记录：`/opt/cyf/service/api/release-records/api-deploy-20260917T043450Z-a8e9170873062165176626775d66c92dfc2e7a1a-7ed64de0a3519b18b14f1ea8fe82463fa0993679-v1.6.0-local-20260917.json`。
- Web记录：`/home/isp/hosts/cyf/web/bak/release-records/web-deploy-20260917T044819Z-74420db2c82fb2f5dee673f337c13bb546d53f93-4e4b4924ea7bb3a26b649726424f3ae2b81a4202-v1.6.0-local-20260917.json`。
- 原始验证/归因/执行证据：`/var/tmp/cyf-v1-6-local-release-20260917`。
- 审计入口：`runtime-entry/runtime-entry-manifest.json`（API）及`runtime-entry-web-r2/runtime-entry-manifest.json`（Web）。相对路径均位于上述原始证据目录；原sealed工具未变，私有入口额外摘要单独保留。
- 后续执行：开发继续合组件develop；达到条件再新建对应版本release分支，并用该精确提交的已验证本地制品发布。云效恢复须明确切换，不把本次本地成功写成云端成功。

## 12:51 最终收口

最终Owner回执与digest已由主控逐项核对，API/Web均`DEPLOYED_HEALTHY`，所有发布/lifecycle锁释放、无JVM锁FD泄漏。未认证公共API请求403仅证明访问被拒绝，不算认证业务回归。最终时点可用磁盘391991296 bytes（约374MiB）。

不可变最终结果：`/home/isp/wsps/cyf/deliverables/releases/v1.6.0-local-20260917/release-outcome.json`；选定测试摘要、执行入口/归因、实际发布记录与线上readback已复制到同目录`evidence/`并逐项校验摘要，不依赖仅保存在/var/tmp的证据。Provider激活和真实设备验收仍待单独安排。
