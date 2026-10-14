# 2026-10-07 真实浏览器页面走查（非再次业务验收）

## 范围

本任务原有已认证Chromium标签，线上聚义厅。正常UI只读浏览首页/需求表单/资料选择取消/点将册查看/资料/我的/既有426、424/390px。没有创建、点将、发送、保存、上传、资金、正式验收业务动作。不重启共享进程；没有应用构建或部署。

## 证据映射

| 文件前缀 | 页面 |
|---|---|
| 01-initial / 02-return | 原426成果完成态、返回详情 |
| 03-returned-items / 04-material-picker / 05-create-form | 事项列表、资料选择、需求表单 |
| 06-home / 07-agents / 08-agent-detail / 09-workspace / 10-items | 首页、点将册、好汉详情、资料、事项 |
| 11-open-completed-card-chat / 12-completed-chat | 426卡片直接进入议事；同一气泡重复正文可见 |
| 13-detail / 14-reopened-result / 15-readonly-status | 原426详情、重开恢复提示、查询原operation |
| 16-mixed-chat / 17-mixed-detail / 18-mixed-roots / 19-mixed-loaded / 20-mixed-terminal | 原424；成果页观察时仍读取中，无新验收成功结论。文件名中的loaded/terminal不表示已读到终态，以JSON正文为准 |
| 21-mine / 22-mobile-home / 23-mobile-items / 24-mobile-chat / 25-mobile-detail / 26-mobile-result | 我的与390px路径；成果重开仍显示继续验收/尚未完成 |

每页有截图和带时间的DOM/按钮观察，脚本记录method/无查询参数URL，不存token/password/header/body。CDP请求观察窗口不同，不声称完整网络计数；查询型POST不能算业务写入。

`sf05-visible-dom.json`记录同一USER消息中两个相同段落的非零尺寸与display/visibility，`12-completed-chat.png`能同时看到两份需求。**SF05已确认可见重复；不能推断服务器重复请求或Agent重调用。**

首个探针错误是将事项卡片点击误当作详情入口，再查找`.matter-primary-action`失败；真实卡片直接开议事，随后正常返回取得详情。没有重复业务操作。本轮424没有在记录窗口读到成果终态，仅保留观察，不重新生成或验收，也不凭加载提示断言新后端故障。

## 与离线原型分离

离线可点击原型与检查：[原型](../../../../specs/juyiting-multimedia-deliberation/prototypes/complete-20261007/index.html)、[浏览器检查](../../../../specs/juyiting-multimedia-deliberation/prototypes/complete-20261007/prototype-checks.json)。原型检查通过只证明示例交互、布局和字节下载，不证明生产缺口修复。完整产品仍NOT_COMPLETE。

线上走查、原型模拟和此前task426真实写入闭环三类证据各自保留，不能混用。后续真实实现按版本化Flow发布，原有SF01–SF05与R01–R05仍待完成。

## 本轮最终复核结果

Chromium真实点击/渲染：33项交互检查通过，37项布局观察通过，0浏览器异常；覆盖1440、390、320px及8个分支入口。测试绑定源文件SHA，见prototype-checks.json；这里只是离线原型PASS，线上缺口与全产品验收仍NOT_COMPLETE。
