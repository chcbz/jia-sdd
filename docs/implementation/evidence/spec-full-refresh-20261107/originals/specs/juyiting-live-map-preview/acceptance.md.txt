# 验收矩阵

以下均为计划标准，尚无本功能 PASS/ACCEPT/发布证据。计数必须分别记录 tests/pass/fail/error/skip 与命令、日志、exact commit/tree，不能用历史 57/55 项替代。

| ID | 可观察结果 | 验证方式 |
|---|---|---|
| A01 | 真地图 TMX/图层/遮挡与横屏相同，不是色块/截图；角色在连续帧有位置/朝向变化 | 真实 Canvas 截图序列 + 运行态采样 |
| A02 | 竖屏全部 world bounds 被 contain；非零原点、超宽/高地图不裁剪 | 几何单测 + 320/390/430 CSS px 浏览器截图 |
| A03 | 预览区域单指上下滚动正常；拖拽/双指/滚轮/键盘不操作地图 | 组件/输入测试 + 浏览器触摸事件，微信真机 |
| A04 | 横屏按钮只调用已有方向入口一次，pending 禁用，错误显示提示 | 组件事件测试 + 浏览器 |
| A05 | 横竖屏至少 10 个往返无空白、无自动回竖屏；一个 Canvas/宿主/runloop | 真实浏览器诊断 + 截图 + DOM/计数断言 |
| A06 | 运动中的人物切换前后 ID/坐标/进度连续，不随机重生；地图过滤仍独立于名单 | 状态单测 + 浏览器世界坐标采样 |
| A07 | 竖屏 contain 不覆盖横屏镜头；显式入口目标、modal/voice/loading 输入锁仍生效 | 镜头/锁定回归 + 浏览器 |
| A08 | 冷竖屏没有额外业务写请求/命令消费者；切换不增加订阅、不吞/重复既有命令 | spy 网络/driver 行为测试；浏览器只用合成身份和拦截 API |
| A09 | 后台/离屏/弹框正确暂停绘制；恢复无超大 dt/瞬移；横屏不被离屏预览错误暂停 | 假时钟/可见性测试 + 真实运行循环观测 |
| A10 | 资源冷缓存/热缓存、异常/超时/重试、快速切换时迟到回调不覆盖新状态 | loader/lifecycle 定向回归 + 网络拦截 |
| A11 | 路由离开清理 observer/listener/runloop；再入不重复订阅；主体切换无旧状态泄漏 | 生命周期计数 + 主体切换测试 |
| A12 | 20fps 为预览可见目标，验证实际绘制而非只验证配置；横屏性能不被改坏 | 时间窗口帧计数及资源观测，未测则不宣称达标 |
| A13 | 读屏可识别加载/错误/暂停与按钮；状态浮层不重建 slot；无无效焦点 | 组件 DOM/键盘测试 |
| A14 | 新定向测试、被触及既有定向回归、真实 production build 通过 | 测试计数、退出码与日志，精确 tree 绑定 |
| A15 | 唯一独立 Reviewer ACCEPT，并确认源码与测试/构建对应同候选 | 权威报告、完整 SHA/tree |
| A16 | 发布源与构建产物精确匹配，公网入口和资源正常；微信至少 3 次往返、滚动/后台恢复正常 | 发布清单 + 公网烟测 + 真机确认，分别记账 |

P1 基础包只能关闭其覆盖的纯函数/组件子项，不能关闭 A01/A05/A06/A08/A12 等集成要求。
禁止使用生产真实凭据执行派单/移动等写入验收；浏览器合成身份/API 拦截必须在页面启动前建立。实际设备未测就标未测。

## 证据记录模板
- phase / baseline / candidate full commit / tree：
- selector / fixture digest / command / elapsed / exit code：
- executions / pass / failure / error / skip：
- tests/build/browser log paths（由 exact Owner 分享摘要，禁止跨线程读取私有证据）：
- reviewer ID / candidate / verdict / P0,P1,P2：
- deployment artifact digest / backup / public smoke：
- pending device acceptance / residuals：
