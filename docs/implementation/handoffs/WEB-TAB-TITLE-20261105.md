# WEB-TAB-TITLE-20261105

- 日期：2026-11-05；Owner：当前聊天。
- 目标：替换浏览器标签页中的 CYF Web Kit，命名为「聚义厅 · AI 协作工作台」，子页面保留名称；避免品牌重复，空标题恢复产品名。
- 非目标：页面布局/交互、分享SEO文案、后端/API契约、构建和部署。本次仅浏览器标题元数据调整，无页面原型变化，不触碰其他任务正在修改的原型。
- 工作区：复用 `/home/isp/wsps/cyf/web`，branch `codex/juyiting-ui-workflow`；base HEAD `ca22ac29de657971b12a71f3a99d2d9ecfc67c1c`，tree `962e513205e4805a601022285bdff557c71f37ac`。已有无关脏文件保留。
- 远端：只读取本地 origin/develop 引用 `b3de23bf40e7b8fdc7976a6a68aa706bcce5b33f`，未联网确认最新；线上版本未查询。
- 责任层与影响：Web `.env` 产品名称及 `src/App.vue` 现有标题监听器；不改变服务端契约，不要求API/Runtime联动。静态首页既有描述性标题保持不变。
- 本机轻量验证：`node ./node_modules/mocha/bin/mocha.js --no-config tests/app-title.test.js`，3 passing；定向 ESLint 和 diff whitespace 检查通过。不是 Flow 正式构建或发布证据。
- 状态：源码修改及定向自检完成，未提交/合入/发布，未触发Flow。发布后还需核对真实浏览器标签页；本次不宣称线上已更名。

## 2026-11-05 正式发布补记

浏览器标题 **聚义厅 · AI 协作工作台** 已随自动分页发布：Web1.16.112 / Flow4403172 Run449，commit `54418fe5bddee1805d5d03d030a54c326dad172a` / tree `619013131f3ef6b84b3d6f9ba8b22987d2901041`。同Run405项相关测试通过；公网index/入口与hall懒加载资源大小及SHA匹配制品，真实浏览器首页和登录后的聚义厅标题正确。独立主机安装及online_verified完成；详见同目录 `TASK-SCROLL-20261105.md` 正式发布节与 `/home/isp/state/cyf-title-scroll-release-20261105/flow/online-verification.json`。
