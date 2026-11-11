# 聚义厅指导登录时机（2026-10-27）

- Owner：本任务；范围：登录成功且身份已确认前不自动或手动展示指导，身份失效立即关闭；不改登录协议、已有引导完成记录或部署。
- Web工作区：`/home/isp/wsps/worktrees/onboarding-auth-20261027`，分支 `codex/onboarding-auth-20261027`；基线及查询时远端 develop 均为 `960841394c5f671b5615b6b1bef9e802722cd1ec`，tree `0075126da5adae6096528f3a14397b75d567fdf4`。原工作区有无关脏改且落后，未覆盖。线上版本未查询，不作上线声明。
- 原型：`prototypes/juyiting/interaction-completion.js` 的 help 状态和 `prototypes/juyiting/specs/prototype-spec.md`；PC/手机共用的离线指导注明模拟已登录，产品仅在认证及身份确认后打开。仅执行 JS 语法检查，未执行浏览器预览或对照。
- 最早定向验证：`node --test tests/hall-onboarding.test.mjs`，25 通过；`node --check prototypes/juyiting/interaction-completion.js`、`git diff --check` 通过。测试包含源码契约检查，不等同于真实登录浏览器回归。
- 待完成：真实登录/重定向及身份切换浏览器回归，固定候选后 Flow 4403172 正式测试构建、集成 develop；未部署。预计故障边界：身份信息获取失败不展示引导。时间记录未测量。

## 用户授权合入及部署（2026-10-27 23:54 +08:00）
- Web develop `a6e2edc0923122b63b21ea0ea5fdf56df178ef84` / tree `1d2276019af2bf7b87f17efa56ef32c6c8718afd`，版本1.16.70；未改API/Runtime。原型脚本及规格在上述Web提交中。未执行真实账号登录浏览器交互验收。
- Run367测试1项失败，原因是旧portrait测试对入口组件标签的字符串预期未包含新增事件；部署未启动。修正测试后推送新提交，Run368完整验证及同Run部署SUCCESS，监控首次终态237秒；制品内测试报告3492通过、2 pending、0失败，扫描成功。
- 部署单71926388，1批1台Success/healthy；主机record标online_verified，commit/version/run与候选一致。同Run归档SHA-256 `9a5fcd35dd5cb5bf9adb4a6ce949abaa4080fc21e77b04f686c12f87c2529ead`，包内commit/tree及测试报告与候选一致；公网index和JuyiHallEntry JS与安装record摘要一致。生产备份`/home/isp/baks/cyf-web-onboarding-auth-retry-20261027-368`；恢复由原安装器、备份record及锁保护流程处理，不回放业务状态。
- Flow默认CI-only配置已CAS恢复，canonical SHA `d40133eacfd9616ae8737e2462c366ce11565235c5b3fb8fdec1f38bf9dd18cd`。证据 `/home/isp/state/juyiting-onboarding-auth-20261027/` 和 `/home/isp/state/juyiting-onboarding-auth-20261027-retry/`；原工作区其他脏内容未覆盖。下一步可用真实账号验证未登录跳转及登录后完整引导。
