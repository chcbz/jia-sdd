# 生产验收入口核验（2026-10-17）

## 核验范围
已登录用户指定测试账号，只读访问当前生产事项、详情与成果页。未点击验收通过、要求修改、点将、执行或结算；未改原型/生产源码、未构建部署。详细版本和边界见 verification.json。

## 实际页面
当前账号事项筛选有1条待验收：405「画一只鸟」。详情错误显示「已受理」，实际入口为「查看正式成果与验收」。进入后有正式交付第1版（2026-09-26 22:10:22），展示result.pdf及manifest，页面底部有「验收通过」「要求修改」，修改说明必填。按钮可用，但此次没有提交决定。
截图：reviewing-list.png、reviewing-detail.png、reviewing-results-final.png。旧reviewing-results为只读守卫误拦读接口的诊断，不是生产故障证据。

## 版本绑定源码规则
前端公网index与Hall chunk SHA和既有1.16.4 / Flow220 / c84c5a2记录一致。实体API JAR SHA与1.16.7 / 58b4b5f发布记录一致，运行进程指向该实体JAR；此为已有版本只读核对，不是本轮发布。
- 正式交付submit成功，交付状态submitted，事项进入reviewing。
- 普通会话产生文字/文件不等于正式提交，不自动保证reviewing。
- 议事成果「确认验收」走prepare→submit→accept操作，所以reviewing可能只为过程状态，成功直接completed。
- 对应API四个服务文件与已安装版本commit对比无差异；不是把本地HEAD当线上。
- BountyPanel.simpleMatterStatus遗漏reviewing（只含review/submitted），因此已有承办Agent时详情回落「已受理」。

## 原型差异与待修正
此前原型按有成果自动待验收，并在同一议事增加验收条，是目标方案，不是生产现状。应明确「成果就绪」与正式「待验收」语义，补齐统一状态映射与可发现入口。不能仅改文案就声称后端流转一致。

## 诊断边界
只读守卫最初误拦POST查询引起0计数和Failed to fetch，核实search/status-counts/conversation/list为读取后放行重跑成功。recommend写请求始终阻止。未验证本轮新交付写入、验收成功或结算；生产截图证明入口和当前待验收实例，而非全链路写入验收。
