# API362 推荐400定向诊断

核对时间：2026-10-29 10:22 CST。Owner：API发布本会话。范围：正式环境认证后只读打开既有task538详情，捕获缺字段推荐请求；不指派/重放任务、不调用模型、不付费、不改生产配置。Runtime发布由原Owner负责。

## 2026-10-29 11:04 CST 配套发布处置（当前结论）

协调Owner已复用Web4403172/371制品，在主机独立安装fa8d7f1/1.16.72。已读取核验其证据：公网index及聚义厅JS/CSS摘要与制品一致；正式登录/overview、task539进行中详情、task533待验收历史成果通过；非ASSIGN推荐调用0、观测HTTP错误0、付费模型调用0。因此本报告下方“未部署/修复方案”是10:22历史诊断状态，**不再代表当前线上状态**。混合版本故障已由配套Web上线处置；实际ASSIGN/付费模型E2E仍未执行。API未重启，API362仍CANCELED，新增Run0。

证据：`/home/isp/state/cyf-gray-safe-integration-20261029/web-release/public-resources.json`、`/home/isp/state/cyf-gray-safe-integration-20261029/browser/verification.json`。Runtime由同一协调Owner独立安装c3f973c/1.3.21（bridge1.1.12），93仍FAIL；11:04记录三Agent registered/ready及672文件摘要通过，证据`/home/isp/state/cyf-gray-safe-integration-20261029/runtime-release/runtime-online.json`。本API会话只读核对证据，不冒称亲自执行Web/Runtime安装或无通道中断。

## 原10:22诊断结论

**属于此次API80739发布与尚未更新的Web之间的契约不兼容，不能归为无影响旧故障。** 直接原因是缺少必要输入expectedTaskVersion；这是旧Web程序发出的请求，不是用户漏填表单。源码变更在本次发布范围内的2f0b800399/5eb70edaf7，不是声称80739单个合并commit才引入。

此前记录的“recommend GET400”不准确：旧摘要只有URL/status，没有method。真实为 **OPTIONS200 + POST400**，不是同一业务请求时好时坏。

## 真实请求/响应

- 线上Web：Flow4403172/368，commit `a6e2edc0923122b63b21ea0ea5fdf56df178ef84`；浏览器加载`JuyiHallEntry-DxwiMOR3.js`，与安装文件对应，SHA256 `ac73a87521369f3de4c2daa6e1eddf4aaaf4dab0952c0ae5411eb446282e9a4d`。
- API：Flow5260799/362安装的`80739ebb0d25be5e713bd1c82209cfea089d3600`；prod，不是灰度。
- 时间：10:22:57请求，10:22:58响应；ziyue认证后查看既有task538进展。
- `POST https://api.chaoyoufan.cn/agent/tasks/538/recommend`

```json
{"protocolVersion":1,"requestId":"3805d492-5a72-48c6-8ed2-e5206e1f9014","data":{}}
```

HTTP400：

```json
{"protocolVersion":1,"requestId":"3805d492-5a72-48c6-8ed2-e5206e1f9014","data":null,"msg":"BAD_REQUEST","code":"BAD_REQUEST"}
```

原始脱敏证据：`/home/isp/state/cyf-native-skills-20261028/release-api-develop-20261029/recommend-request-response.json`。未保存认证头/令牌。浏览器仅允许缺版本且源码确定会在模型前拒绝的POST通过；任何带有效版本的推荐POST均拦截，防止推理费用。没有修正参数后再次调用生产模型。

## 因果链/影响

1. 上一API3bca7cbd的AgentController同一路径也是POST，无请求体必填参数，返回旧推荐数组。
2. 当前API的AssigneeRecommendationController改为JsonRequest<Request>；服务入口在任何任务查询/候选查询/model.judge之前检查expectedTaskVersion，空值返回400 BAD_REQUEST。故本次失败未进入模型。
3. 线上Web a6e2edc/useHallData仍`agentApi.create(..., {}, ...)`，且仅检查task.id，对已承办事项也自动请求；响应仍要求Array。
4. 新API同时改了请求和响应契约，仅在API补默认版本也不能修复旧Web的数组消费，并可能意外触发模型；不应恢复旧规则推荐或伪造当前版本。
5. 用户可登录、读取事项/资料的既有结论保留；承办推荐受到影响，**撤销任何“生产功能完全不受影响”的外推**。task538本身已承办，不需要再次推荐；不把此次400说成该事项执行失败的根因。

## 最小修复方案（未部署）

- 正确既有候选：`fa8d7f1793392918bd0d1531c6f029cbaff8daeb`（10:20远端查询）。其中16a63ae已实现：仅权威动作包含ASSIGN才请求；传expectedTaskVersion；解析新推荐对象；区分stale/error，不用旧本地打分兜底。
- API不降低身份/任务版本检查，不恢复退休接口，不重启API；本次仅提供方案，不擅自扩大为Web发布。
- 发布前固定Web候选并走原Flow同Run测试/制品/授权安装；此前371 CI成功只能作为历史候选证据，不能代替本次上线。
- 必需回归：已承办task538打开详情不发送recommend；可承办事项携带字符串版本及正确envelope；新对象解析/409状态/身份切换/失败不伪造推荐；测试使用mock，不调用付费模型。既有`tests/juyiting-assignee-recommendation.test.js`覆盖版本输入/对象消费/身份切换等。
- API362同Run已有Controller5、Service8、Model3项通过，但没有旧线上Web与新API的混合版本浏览器验证；因此不能据其全绿断言跨组件兼容。应补充缺版本400且model无交互的直接断言及配套上线检查。
