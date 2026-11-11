# 语音输入区整改（2026-10-02）

## 用户反馈与范围

- 用户已确认转写/发送正常；启用“语音回答”报 Window.fetch `Illegal invocation`。
- 去掉文本输入下常驻语音栏，改为输入区麦克风、按需语音设置和原位录音/转写确认。
- 仅修改前端共享 composer/voice presentation 与定向测试；不变更 provider、后端、身份、冻结会话/CAS 或自动发送默认值。

## 原因与设计

- `defaultBrowser()` 保存裸 `globalThis.fetch` 后以 `browser.fetch()` 调用，receiver 不再是全局对象；修复绑定 `globalThis`。修复 commit `3a4cdf272be01842173a3cb2d72087c7e0e7d52f`，tree `7b0eba7a6f6769909ece470efa602c2bcebfb955`。
- 输入区就地控制、发送前检查、取消/丢弃和次要设置渐进披露；借鉴 Apple 官方 Messages 音频操作指南，但本功能仍发送转写文字，不变为音频消息，不展示虚假声量波形。
- 保留转写确认、明确议事对象/上下文改变后的手动采用、停止等待不撤回已发送文本、AI 生成语音披露；地图 compact HUD 不丢失能力。

## 验证边界

- receiver 回归新增测试先 red，修复后 green；此前定向 voice 文件 32 pass、ESLint/diff PASS。这只是轻量诊断，不是发布证据。
- 本机原生浏览器诊断未执行成功：Chromium wrapper 指向已删除 runtime；未改共享 launcher/cache、不重试同输入。不能声称真实浏览器或设备已通过。
- Flow `4403172 / Run148` checkout 为旧 `8c0643b2cabb1807ccba290a1978f7c607b6af08`，不含 receiver 修复。共享 Main 通报全局 before hook 的 SFC loader 残留 import，`Cannot use import statement outside a module`，0 passing / 1 failing；不是本修复的测试结果。
- 共享 Flow Main `01a0dde8-fd03-7ee0-be21-293ca13bb336` 仍独占控制、保留 build-only/deployment hold。UX 最终 SHA 将与 loader 修复统一集成后云端验证；本线程不覆盖配置、不 start/cancel、不本地生产构建或发布。
- 本轮没有 provider 调用；沿用历史累计 33/500。用户真实麦克风/扬声器验收尚未通过此次候选。

## 完成状态

进行中。必须补最终 source/tree、对应 Flow Run、测试/构建、同 Run 制品摘要、部署和线上资源核验后，才可标记上线。

### 12:16 补充：真实原生诊断与布局发现

- 找到系统 `/usr/bin/chromium-browser`（133.0.6943.141），不改共享 smoke wrapper/cache。用本线程 profile 的离线 `data:` fetch 复现旧代码原生 Window `Illegal invocation`；绑定版 200、响应内容正确。此前 missing runtime 失败保留；本次是已验证可用的不同 binary，不是盲重试。
- UX feature `3d6e66b1f8eaa600008eae1fe9437cf401199d0d` / tree `5cc11cde2342b0c508a07f23d116751a0aeb4319` 经 Owner 32 voice、ESLint/diff 自检并独立分支推送。共享 Main 与 fixture 修复合成 `9124fe008b92406080fae723f0ff2518886eee74`，Flow Run149 正在正式验证（12:16 查询：build RUNNING、scan SUCCESS）。无部署证据。
- 主控低成本 dev 态两组件真实 Chromium 布局诊断（图标20px stub、非整个产品/非生产构建）实测：760px idle 控件宽143px、文字遮挡41px；390px idle 遮挡13px；active review 右侧普通发送/清空按钮被 grid 拉伸到转写卡全高。已交同一 Owner 做最小布局修复；Run149 不取消，不能代表尚未提交的修订。
- 布局证据：`/var/tmp/cyf-voice-fetch-receiver-20261002/main/voice-layout-browser-results.json` 与同目录截图。该 dev fixture 不调用麦克风/网关，不证明扬声器或真实设备通过。

### 最终源与布局复验（待云端发布）

- 最终 Owner feature：`b9a97695214c11b824a3ec501957a5ea017157f4`，tree `24e49b76682c4cc16de615d55e87dad48df25853`，parent `72a3abe95e74f6bef10830581c4b7897e9148e34`（包含 3d6、原 UX 和 receiver 修复）；remote feature readback 一致、工作树 clean。32 voice 定向诊断、ESLint、diff check PASS。
- Idle 改自然 grid 给 textarea 与 icon-only 控件各自空间，删除 absolute overlay/固定 padding 预留；录音/转写/确认状态按需展开；普通发送/清空 actions 不再被 active 卡片拉伸。
- 系统 Chromium DevTools 定向 dev 布局重测：760px desktop idle、390px mobile idle/settings、recording、review 均无文字遮挡和页面横向 overflow；截图检查确认 review 右侧 actions 恢复正常高度。图标为20px stub、voice 为本地状态 fixture，不能代替生产图标、完整产品、真实录音/扬声器验收。
- 最终 SHA 已交共享 Flow Main，等与 loader 修复合并并验证。Run149 不含本节最新布局修复，不能复用作其正式验证。

### 共享 Main 已接收（12:22）

- 最终 b9 已非 force 合入融合 feature `1ee859df89ae06de450b5772f15e2411a2ff8fcc` / tree `d29b47f307b9902a57b34896a099aca299dc4864`（parents 9124 + b9），三份 voice 文件与 b9 逐字节一致；loader 修复保留。主控独立 `git diff --exit-code` 验证三文件相同。
- Run149 于12:20 FAIL。共享 Main 提供 Mocha 2809 passing / 2 pending / 64 failing、scan SUCCESS；已越过148初始化 loader 错误，无发布制品。可见失败包含缺 mock/typedForMessage/XMLSerializer 和身份测试；仍需准确归因，不将64项总失败推定为 voice 问题。主控只读 log tail 有 `outputTruncated: true`，没有声称读完整日志。
- 当前 develop 仍9124、未启动150、deployment hold维持。Main 修复实际全套失败后冻结共同 SHA、执行正式云端回归；不得复用149证明最新 b9，不能本地生产构建兜底。
- 本线程 dev server / Chromium 已按精确所有权关闭，未留下预览进程；本轮 provider 0、累计仍33/500。代码整改已完成，云端验证和上线尚未完成。

### 12:39 云端回归启动

- 共享 Main 将149实际失败修复与最终 voice 合入 remote develop/feature `c74a3864b0909c8db4489c5938a590952a56d555` / tree `fd23ba55cc1294523b62b7f3d44618fe6d3719a9`。本线程独立核对三份 voice 文件与 b9 字节相同，预览仍对应最终 voice 代码。
- Owner 修复149的定向283 passing / 2 pending 是辅助诊断，不替代正式云端。共享 Main 在 push 前后未见自动 Run 后，12:39:05单次 Start 返回 Run150；三flags/hold未变。
- 本线程官方只读查询12:39:48：Run150 RUNNING，build527220690、scan527220691均RUNNING；来源 develop 的 commits 此刻为 null，实际 checkout SHA 尚未知。目标 c74 不能冒充实际 checkout。
- 正式测试/构建、同 Run 制品和发布均待实际证据；本线程不重复启动、不取消、不操作共享配置。

### Run150 实际源码确认（共享 Main 通知）

- Main 已核对 build527220690 实际 clone/CI 日志：12:39:29 Commit收集及增量范围终点为完整 `c74a3864b0909c8db4489c5938a590952a56d555`，`CI_COMMIT_SHA` / `CI_COMMIT_SHA_1` 同为该 SHA。实际来源确认不再仅依赖目标分支或可能为 null 的 sources.commits。
- 原日志由 Main 私有保留，后续提供脱敏正式证据；本线程未读取其他线程私有证据。测试/构建未终态、无成功制品结论、hold 不变。

### Run150 正式测试／构建通过（12:53–12:55）

- 共享 Main 官方12:53:13查询Run150 SUCCESS；本线程12:55:10独立官方只读复核 SUCCESS，build527220690、scan527220691均SUCCESS。实际源码为已确认的 c74；最终 b9 voice 文件保留。
- Main正式日志摘要：完整 Mocha 2873 passing（6m）/ 2 pending / 无 failing；Vite12:50:55 built11.14s；12:51上传同 Run 制品106562526 bytes成功。
- **仅正式测试／构建与上传成功**：Main仍在取同 Run 制品校验内部source/tree/SHA256，尚未给出制品完整性通过结论。部署hold保持，API/Client实际运行及双模式依赖未齐；没有上线或真实设备验收成功结论。

### Run150 同 Run 制品已验（共享 Main 12:57:58通知）

- 包106562526 bytes；SHA-256 `fb3b3b7858eccca5215c08f0fc367e6c2576bf898490e166eca19e2358c8c2c6`。
- 包内release.json绑定pipeline4403172/run150/source `c74a3864b0909c8db4489c5938a590952a56d555`，source-tree `fd23ba55cc1294523b62b7f3d44618fe6d3719a9`一致；全部364个dist文件size/SHA256逐项校验且集合完整，archive无越界/链接；包内报告再次确认2873 PASS / 2 pending / 0 FAIL。
- 准确交付状态：最终 voice 源码已随共同候选通过正式云端测试／构建，并有完整性已验的同 Run 制品。上述核验由共享 Main提供，本线程未重复下载或访问其私有证据。
- deployment / online仍NOT_RUN；hold的实际API/Client运行与身份依赖尚未解除。不能标记上线或设备验收完成。

### Run150 pending 范围补充

- 包内报告两项pending仅为 paired Mini Program entry contract 的 cold launch portrait/context、native landscape/portrait recovery；对应 `web/tests/public-entry-navigation.test.js:73-74` 的 `MINIPROGRAM_PROJECT` 未提供时 `describe.skip`。
- 不是 voice32 或 fetch receiver 回归被跳过，不证明小程序真机已验。正式口径仍2873 PASS / 2 pending / 0 FAIL；没有因此重复全套测试或改变部署hold。

### 正式终态同步（共享 Main 2026-10-02 13:13，北京时间）

- 官方Run150、build527220690、scan527220691均SUCCESS；sources现明确含c74，与既有checkout日志、包内release.json及source-tree fd23一致。最终b9及三份voice文件字节一致，原全suite及364文件制品核验结论保持；2项pending仅为小程序配套测试。
- deployment / online / productAcceptance均NOT_RUN。当前阻塞是共同发布依赖，而非voice回归：API全应用迁移fixture CHECK drift修复与制品、API恢复授权及健康、Client安装控制权和完整真实配置、双模式目标可用性。
- 共享Main保留控制及hold；不新增Run、不重测相同树、不读其私有证据目录。后续仅按实际部署／线上／产品验收证据推进，不标记上线完成。

### 发布路径纠正（共享 Main，SDD cefbb39a）

- **Run150是最终b9的正式云端CI证据，不是未来发布Run证据。** 成功测试／构建及制品核验结论不变。
- Main只读核实现有4403172 VMDeploy模板与安装器：150本身没有deploy stage，不能事后补加；安装器强校验当前run_id，不允许把150包伪装成新Run制品。此前任何“等待150同Run部署”的表述均按本节纠正。
- 实际API/Client、授权及目标可用性依赖满足并由Main解除hold后，需一次真正包含deploy stage的最终Flow发布Run，绑定该Run自己的source/tree、测试、构建、制品摘要、部署与线上证据；不能拿150证据替代。
- 当前不重复触发、不改配置、不修改或取消150，继续Main独占控制。部署／线上／产品验收仍NOT_RUN。

### 依赖进展（共享 Main 通知）

- API候选前缀0a4d4299/tree5036922已完成真实MySQL旧库升级、完整JiaApplication两次启动及负向CHECK回归（1 PASS / 0 FAIL / 0 SKIP），Main核验bootJar摘要前缀b4e53624并FF推feature。只记录Main提供的前缀，不补造完整API SHA或制品摘要；重型窗口已移交Runtime Owner。
- 已有授权限定相关服务接管/API恢复/现有binding15原托管免费恢复。fresh CAS发现历史offline runtime scope投影不一致，额外单行修正仍待明确用户授权，未DML；本线程不推导新增生产数据写入授权。
- Provider配置合同尚未冻结，因此4403172 hold仍有实际依赖。Web150正式CI及已验制品结论保持；不新增Run、不改配置、不部署，未来仍需真正含deploy stage的最终发布Run。

### 恢复授权门禁已解除（共享 Main 依赖状态更新）

- API**旧版本**已恢复HTTP200 / UP，不是新源码0a4d已上线。binding15经已授权精确三行CAS，14:12:41由原managed service自动registered；未重启、未reprovision、未扣款。目标当前有task，不打断。
- 覆盖此前“额外修正授权待用户”状态：恢复授权门禁已解除，不再重复请求用户恢复授权。
- 新API0a4d真实MySQL回归1 PASS / 0 SKIP及JAR已验；Client407db0a来源校验22 PASS。两者仍未版本化安装，源码／制品验证不得冒充当前运行版本。
- 真实图片Provider合同／配置和新能力读回尚未闭合；4403172 hold继续、无新Run或配置变更。Web150既有正式CI／已验制品证据保持，后续仍由Main控制真正含deploy stage的最终发布Run。

### Run153 正式部署成功（共享 Main 通报：10月3日02:55，北京时间）

- Run153 SUCCESS；actual Web `4dc65cbcd382bd4e4094fa8a66a25a8f44dbedda` / tree `969db749dfd885254d21cbf5daf33887093733c1`。build527570069 SUCCESS（2878 passing / 2 pending）、scan527570070 SUCCESS。
- 本次真正包含部署阶段：deploy527570071 SUCCESS / order70593938，单主机healthy；部署日志INSTALL PASS且入口hash最终匹配。不复用150或152冒充本次发布。
- 本Run制品经Main流式全量hash和manifest核验，SHA-256 `7b4dd9f327ac717918b83073b1240409a40cff5a32066a3f68782273d76d4cf1`。
- 本线程独立Git核对4dc source/tree及三份voice文件：与final b9 diff exit0。最终语音修复和样式已正式部署；此前“尚未部署”的状态由本节更新。
- Main仍在独立核验线上资源及业务浏览器验收。**部署成功不等于独立线上核验或完整语音／设备／产品验收通过**；本线程不追加Run，不接管Flow控制。
