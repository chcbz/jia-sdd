# Web238归因与更正候选

核对时间：2026-10-19T19:08:27+08:00。Owner chat-stop-main；单Agent，无部署。

| 现象 | 源因 | 更正及定向证据 |
| --- | --- | --- |
| funded/requirement intake/requirement integration 的真实SFC装载失败 | 新增共享projectHallTask依赖未注入这些既有loader；没有关闭业务断言 | 所有BountyPanel真实loader注入实际共享模块；UNKNOWN和终态均只读 |
| Agent关闭图标/任务资料路由静态断言失败 | 仍匹配旧条件SVG、raw terminal判断 | 按统一SVG及canActOnTask表达式核对；路由表达式实跑继续阻止终态/UNKNOWN |
| 资料选择旧样式/PC预览按钮断言失败 | 旧测试强制存在已按用户要求删掉的PC预览按钮和精确压缩CSS | 仍检查同token/PC自动预览的实际字节/音频元素、仅GET、固定版本；手机保留切换 |

Flow238：3071通过、2pending、10失败；构建未执行。未改生产权限或跳过失败测试。更正候选另含HallDraftEditor收敛现有HallMaterialPicker，删除并行选材/预览界面；老固定版本跨页加载、丢失不换新、取消不提交、同身份草稿保存和私人事项流程继续回归。

本地10文件117通过，日志`/var/tmp/cyf-optimization-impl-20261019/web/shared-picker-final.log`；实际选择器4尺寸Chromium32项通过，证据`/var/tmp/cyf-optimization-impl-20261019/browser/picker-latest/`。这些不是正式Flow/全站验收；真实旧交付入口、v5自然修改、outbox自动提交及MySQL闭环仍未完成。

Web238终态后，原配置恢复readback APPLIED。下一次只验证精确新SHA/tree，不重发238输入、不将本次验证当部署。

### 后续正式验证
Web4403172/239 SUCCESS：精确d2fcebc/tree3e9ae964，3085通过/2pending/0失败，Vite/扫描/制品上传通过，原配置恢复APPLIED。未部署；不等于完整方案完成。控制证据/var/tmp/cyf-optimization-impl-20261019/web/shared-picker/。
