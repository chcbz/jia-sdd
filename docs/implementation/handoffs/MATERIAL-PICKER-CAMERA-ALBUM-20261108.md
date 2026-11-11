# MATERIAL-PICKER-CAMERA-ALBUM-20261108

- 日期：2026-11-08（Asia/Shanghai）；Owner：本聊天。
- 目标：聚义厅共用“选择资料”页支持上传、拍照、相册。用户后续明确三者仅图标，无文字、无底色；实现同时去掉边框，保留44×44点击区、20px SVG、title、输入无障碍名称及焦点环。
- 非目标：不改API/Runtime合同、上传授权、资料存储或执行权限，不发布、不重启、不操作生产数据。
- 基线：Web `codex/juyiting-ui-workflow`，HEAD `ca22ac29de657971b12a71f3a99d2d9ecfc67c1c`，tree `962e513205e4805a601022285bdff557c71f37ac`。根仓及Web开工均有大量他人脏修改（含原型和本次复用测试文件）；本次仅修改命中的局部，不清理、覆盖、提交这些既有内容。未查询远端，不声称远端develop/线上最新；未合入develop。
- 责任层：RB-1 Web交互；三种系统文件输入统一复用HallMaterialPicker的串行workspace.upload及COMMITTED固定fileId/version收据。拍照image/*、capture=environment、单张；相册image/*、多张、不设置capture；上传不限原有类型。设备能力由浏览器提供，不承诺桌面强制拍照。上传中/CREATE待核对统一禁用，保留原意图核对；取消系统选择不改暂存，完成才向上带入，不自动发送。
- 原型先行：复用 `web/prototypes/juyiting/` 的prototype.js、interaction-completion.js/.css、specs/prototype-spec.md；原型多入口读文件期间统一禁用/复位，原有文件选择处理复用。已有18786预览服务HTTP200，未接管或停止他人服务。浏览器复核320/390/1440，无横向溢出、三入口44×44、纯SVG/透明/无边框。截图仅离线原型，不是生产实页或真机相机验收。
- 产品实现：`web/src/components/juyiting/HallMaterialPicker.vue`；现有需求/议事消费者自动复用，不扩为三端修改。同步现行任务方案 `specs/juyiting-ui-baseline-20261006/optimization/spec.md`。

## 本地验证（非发布构建证据）

包外证据：`docs/implementation/evidence/material-picker-camera-album-20261108/`。

- `test-input.txt` 固定最终组件/测试文件SHA256及基线完整commit/tree；工作区脏，摘要代表本地候选字节，不冒充干净commit或正式发布制品。初版输入及测试保留before-icon-only文件。
- 命令：在web运行 `node --import tsx ./node_modules/mocha/bin/mocha.js --no-config --require ./tests/setup.js --timeout 10000 --exit --reporter spec tests/juyiting-hall-overview-component.test.js tests/juyiting-requirement-materials-intake.test.js tests/juyiting-conversation-material-links.test.js`。
- 最终67 passing（测试报告3秒）。覆盖新输入属性、拍照与相册共用上传/固定版本、完成前不emit、取消无改变、三入口统一禁用及待核对恢复，复用原有晚收据/身份切换等回归。
- `prototype-browser.json`、`prototype.log`与screenshots：自有Chromium，320/390/1440全通过。复用已有浏览器工具的CDP启动/清理方法，检查脚本存check-prototype.cjs；仅本次自有浏览器已关闭，不停止已有预览服务。
- ESLint不全绿：初次直接检查失败保留lint.log；最终check-lint.mjs对同一路径HEAD/候选比较：基线51 errors/3 warnings，最终49 errors/3 warnings，新增控件区无诊断。未借机格式化无关代码。Browserslist老旧提示未顺手升级依赖。
- `git diff --check`：本次命中产品/原型/测试路径通过。
- 工具链：Node v24.22.1、现有node_modules。无npm ci、生产构建、打包或Flow Run；无可回收最终包，故不登记completed-tasks.json。目录均位于普通磁盘，无内存盘。
- 时间：测试各次约3秒，浏览器检查及等待有界；完整定位/实现墙钟和累计验证秒数未独立测量，留空，不宣称缩时或正式600秒发布验收。

## 后续

真机相机/相册系统选择尚未实测。初次实现时未发布；用户随后明确“部署”，以下记录本次实际Web发布，不扩大授权到API/Runtime。


## 2026-11-08 用户授权Web部署：已完成

- 线上前代为1.16.126 / `f694161e49ee0627ed5ad2ce873de96aabb881e6`；开工查询远端develop也为该commit。原开发目录ca22ac2落后且有他人脏修改，不能整树发布。最小隔离使用本聊天管理的一份普通磁盘worktree，以该生产同源commit为底，仅移入拍照/相册两输入、三入口纯图标样式、上传守卫、本次4项测试（含参数化执行）和版本号；保留生产新增dialogOnly/context/directUpload等功能，未用旧组件整文件覆盖。
- 固定发布：Web **1.16.127** / commit `93e2fc0b609540f03f328f6a61b04461e3963766` / tree `1a93cbb2a2596fd5e7463c7473ee1e692aea8138`。分支`codex/material-picker-camera-album-20261108`；自检通过后fast-forward push到origin/develop并readback同一完整commit，无force。原主工作区的HEAD、脏修改和root gitlink不替他人调整。
- 构建批次`material-picker-20261108-1154`，输出`/home/isp/state/cyf-local-build/tasks/cyf-material-picker-20261108-1154/web`；包外证据位于原证据目录的`deploy/`。Node v24.22.1、锁定npm ci；既有local_web_build.py、原生产Vite配置和完整public，未使用Flow/伪造CI。
- **117 tests：115 pass、2 pending、0 fail**；既有发布基线加hall-overview-component、requirement-materials-intake、conversation-material-links三个定向套件。2pending保留，不宣称全部测试通过。测试/构建/打包（包括内部排队/等待）builder墙钟**62.942秒**，systemd单元总runtime63.205秒；RuntimeMaxSec600仅用于本次构建单元。依赖11.992s、测试9.643s、构建26.091s、打包10.147s、包完整性1.754s；阶段外开销未扣除。无超限/重试/拆批。
- 最终包`package/web.tgz` SHA256 **66cc6e1cef13d4df9d109e202ab70e6aa2c4429cae5e9861294ede1b7f378756**；真实LOCAL v2 manifest绑定源码、版本、工具、测试报告和612文件摘要。
- 使用现有已安装`/usr/local/sbin/cyf-web-flow-deploy`的deploy_local入口；部署前固定前代record/index及helper SHA；原发布锁、逐文件核验、assets-first/index-last及私有可恢复备份均保留。未向安装下传剩余构建预算，未改安装器/生产服务参数。安装**15.307秒**，30个文件变更，record为LOCAL/online_verified；完整交付墙钟未独立计量，不以构建+安装之和冒充完整墙钟。
- 备份`/var/lib/cyf-web-flow/backups/ed85d35c153c1937f5fd60d2dd431e4fc6a85fa221d70e62519bcd74e7a989aa`，前代record字节及index SHA实际复核一致，可沿既有安装器恢复，不直接覆盖当前状态。
- 健康/制品验收：实际安装612文件SHA/size全部一致；安装器在线核验index及全部JS/CSS共255项。另对含拍照capture=environment、相册accept=image/*的实际线上JS与对应CSS/index共3资源HTTP200/SHA再次核对。证据`deploy/acceptance.json`和`installed-record.json`。
- 业务边界：固定源码挂载回归通过，新输入已进入线上编译资源；未冒充已登录生产资料上传、手机权限弹窗或真实相机/相册业务验收。未改API、Runtime、数据库或重启应用服务。
- 包外日志/报告/源码patch/描述符/前后发布record已保留；完成后按现有completed-tasks.json显式登记本批最终包，当前/回退绑定保护继续适用。本聊天管理worktree尝试archive_worktree，App返回“The task's primary checkout cannot be removed.”，未绕过保护删除源码。仅删除本次npm ci生成且已无构建使用的自有node_modules；干净源码工作树保留在`/root/.codex/worktrees/material-picker-camera-album/web`，待App允许归档后收口。源码已推送，未清理他人目录/进程。

### 收尾时并行后续发布核对

只读复查发现另一Owner已将Web升至**1.16.128** / `0791132b92bd81a7c0b1ea15411949c7e05d2e91` / tree `23c82263feca2eefdedefcb5d12d02355bdc597d`（报价不可用原因展示）。实际确认该commit直接继承本次93e2fc0，HallMaterialPicker.vue源码字节未变，当前record为online_verified；再次核对当前线上index及含camera/album的新JS摘要通过。未取消、覆盖或回退该Owner发布；本次1.16.127安装记录保留历史原文，当前线上状态单独保存`deploy/subsequent-release-verification.json`，不把后续发布冒充本聊天执行。
