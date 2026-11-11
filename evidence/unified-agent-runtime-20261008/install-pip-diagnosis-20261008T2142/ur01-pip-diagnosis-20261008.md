# UR01 pip 慢安装只读诊断/交接

2026-10-08；support，非Reviewer/Writer。固定client `7594fd72251d38b6e1d23a1a3cca184ae0d085e7` / tree `0827ce904179862ab55648fe99b780cea94faf98`，harness f3d；不改live consumer83600/target/source/config，不控制原进程。

## 已证原因（历史下载区间，不是编译）

- 21:42:04→21:42:20 同PID686606/fd6/Pillow tar：37,089,280→37,345,280B，256,000B/约16s≈16,000B/s；无children。21:46仍41,226,240B、无compiler。
- 活动fd5 ESTAB 151.101.192.223:443；旧fd4 CLOSE-WAIT不能单独证明当前挂死/失败。env index=pypi.org，无凭据、无proxy键。
- private Python3.11.13 / pip21.3.1 / OpenSSL3.5.3；actual pip支持cp311 tags。Pillow8.4.0当时选中49,368,411B源码包，没有适用cp311/Linux wheel；reportlab3.6.8同样没有。后续进度见下节，不能仍称当前在Pillow。pip升级本身不会补出固定版本wheel。
- 先前support只读stat（历史观察，不代表当前文件）：`{"at": "2026-10-08T21:53:12.471343+08:00", "pid": 686606, "fd": 6, "filename": "reportlab-3.6.8.tar.gz", "bytes": 593920, "children": []}`。不读fd正文/原stdout/socket。
- 公开Pillow对象HEAD200、Content-Length49,368,411；无body下载。这不是吞吐测试或active文件完整性证明。

## 21:53进度更正（交接仍completed）

- 主控21:52:49：同pip686606已转`reportlab-3.6.8.tar.gz`（71,680B），无children。
- 主控21:53:14：完整Pillow **49,368,411B**，实际SHA256 **b8e2f83c56e141920c39464b852de3719dfbfb6e3c99a2d8da0edf4fb33176ed**，与官方exact元数据一致。
- 证据 `/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/install-pip-diagnosis-20261008T2142/pillow-complete.json` SHA256 `a6321d34fa6771facc0e379b5b21472aea91d58423aa19ca972301428b084c7c`；本support只读核对这些固定字段。
- 因此下载已从Pillow进入ReportLab，不是Pillow挂死/源码编译；上文fd/Pillow大小是观察区间，不是现在状态。ReportLab后续下载/编译/安装/验收终态仍待主控收证，不控制active run。

## 六pin exact官方PyPI发行文件

JSON保存全部官方release files（含Requires-Python、tags、SHA256、size）及metadata响应SHA。下表仅列当前适用wheel；无wheel列sdist。没有发行wheel不等于必然不能源码编译；Requires-Python可选取也不等于全栈实测支持。

| Pin | Requires-Python | 当前cp311适用wheel数 | 文件 | 字节 | 官方SHA256 |
|---|---|---:|---|---:|---|
| python-docx==0.8.11 | 未声明 | 0 | python-docx-0.8.11.tar.gz | 5561613 | 1105d233a0956dd8dd1e710d20b159e2d72ac3c301041b95f4d4ceb3e0ebebc4 |
| python-pptx==0.6.23 | 未声明 | 1 | python_pptx-0.6.23-py3-none-any.whl | 471575 | dd0527194627a2b7cc05f3ba23ecaa2d9a0d5ac9b6193a28ed1b7a716f4217d4 |
| openpyxl==3.1.3 | >=3.6 | 1 | openpyxl-3.1.3-py2.py3-none-any.whl | 251340 | 25071b558db709de9e8782c3d3e058af3b23ffb2fc6f40c8f0c45a154eced2c3 |
| Pillow==8.4.0 | >=3.6 | 0 | Pillow-8.4.0.tar.gz | 49368411 | b8e2f83c56e141920c39464b852de3719dfbfb6e3c99a2d8da0edf4fb33176ed |
| PyPDF2==1.28.6 | >=2.7 | 1 | PyPDF2-1.28.6-py3-none-any.whl | 87076 | d7118f0187153257b1f906dcfcd8236608f4987b6a9999b7c5ad49114706a1ad |
| reportlab==3.6.8 | >=3.6, <4 | 0 | reportlab-3.6.8.tar.gz | 4503191 | dc7657fcb0bc3e485c3c869a44dddb52d711356a01a456664b7bef827222c982 |

官方metadata来源（无凭据）及响应摘要：
- `https://pypi.org/pypi/python-docx/0.8.11/json` SHA256 `530716dfba0bf781408816f883eb1444626c5d5bcd10787a1dcf15dd71fe17df`。
- `https://pypi.org/pypi/python-pptx/0.6.23/json` SHA256 `599ac790c7608b2124cc2b3e95d4e38b1478f5ddf3f2a3e376e07aec4757ad77`。
- `https://pypi.org/pypi/openpyxl/3.1.3/json` SHA256 `381539f1e1039a77a15382152aac26155f90cd52f29236f8e412714263c136c6`。
- `https://pypi.org/pypi/Pillow/8.4.0/json` SHA256 `8b388a8b466796bd7d93d6985c816c8f3c9617cffe77c86e0b1763d9d94306b5`。
- `https://pypi.org/pypi/PyPDF2/1.28.6/json` SHA256 `ccdfe781549931714fac1cffff5fa30e7ed846daadc262faa23809b6b2ae33dd`。
- `https://pypi.org/pypi/reportlab/3.6.8/json` SHA256 `943fa3686c724a4b30d65635db8b734812cdcfb060bde7dbbeea56f1d9b7ecb4`。

## 真实支持契约/API与ready依赖

- requirements注释写Python3.6；installer accepts --python但仅检查executable/venv，Node则精确20.20.2；然后强制pip<22再six requirements，不是明确已验Python3.11契约。
  - `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/codex-ws-agent/toolchain/requirements.txt:1-8 ; SHA256=d0d6d95c2f8b56d28c34d6cb98625fe2468d04b39be25ae5e8f3083ba1fd1f1d`
  - `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/cyf-agent-runtime-v1/install.sh:6-37 ; SHA256=2f68d98982fa6ebdb3eb0620475e497b02890547af66eb0d54eaf9133487697d`
  - `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/cyf-agent-runtime-v1/install.sh:55-61 ; SHA256=2f68d98982fa6ebdb3eb0620475e497b02890547af66eb0d54eaf9133487697d`
- validate核six exact distribution version和helper实际health，pre/post publish均保留。当前private isolated探针中lxml/docx/pptx/openpyxl/PIL/PyPDF2/reportlab全未找到，尚不ready；是in-progress状态，非安装失败回执。include-system-site-packages=false，不借宿主模块。
  - `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/cyf-agent-runtime-v1/lib/execution-adapter.mjs:288-304 ; SHA256=ccbf56efa9f8f56fc29459289e1b5b7706165f8e38d8596394549346d479e775`
  - `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/cyf-agent-runtime-v1/install.sh:145-152 ; SHA256=2f68d98982fa6ebdb3eb0620475e497b02890547af66eb0d54eaf9133487697d`
  - `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/cyf-agent-runtime-v1/test/clean-target-install.acceptance.mjs:192-204 ; SHA256=ef438909494e7f30195c6bcc54c3fd05cc8590be4331a7685c2bd10eb21cba21`
- lxml为transitive未pin：docx>=2.3.2、pptx>=3.1.0；pptx另依赖XlsxWriter，openpyxl依赖et-xmlfile。不能把six pin称完整依赖锁或已安装lxml ready。
- 实际Pillow调用：Image.open/verify、font.truetype/load_default；验收new/putpixel/save/open/load。ReportLab调用A4/canvas.Canvas/setTitle/setFont/drawString/save，PDF重开沿用PyPDF2旧PdfFileReader/Writer。未发现这些工具使用Image.ANTIALIAS，但未运行新候选，不作兼容PASS。
  - `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/codex-ws-agent/toolchain/delivery_tool.py:28-42 ; SHA256=173d156c16f65e45b754077bf8ba466ecb4cc198d5c511228adc88817573226f`
  - `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/codex-ws-agent/toolchain/delivery_tool.py:54-67 ; SHA256=173d156c16f65e45b754077bf8ba466ecb4cc198d5c511228adc88817573226f`
  - `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/codex-ws-agent/toolchain/delivery_tool.py:172-197 ; SHA256=173d156c16f65e45b754077bf8ba466ecb4cc198d5c511228adc88817573226f`
  - `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/codex-ws-agent/toolchain/delivery_tool.py:123-143 ; SHA256=173d156c16f65e45b754077bf8ba466ecb4cc198d5c511228adc88817573226f`
  - `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/cyf-agent-runtime-v1/test/clean-target-install.acceptance.mjs:244-274 ; SHA256=ef438909494e7f30195c6bcc54c3fd05cc8590be4331a7685c2bd10eb21cba21`

## 原Owner下一最小源码切片（未实施/未冻结）

保持Python3.11.13和私有venv。原Knuth下一固定源码切片优先仅更新已证缺cp311 binary的Pillow/reportlab pins及Python3.6旧备注；可选已核metadata候选Pillow10.4.0+reportlab3.6.13（所有匹配wheel/SHA/size已列），不是安装通过承诺。不默认换回3.6/借宿主包。

- 明确当前Python支持契约与private pip bootstrap；pip<22 cap不是当前下载根因，不为解决本次慢包单独升级pip或宣称其不识别cp311。若下一slice更新bootstrap，必须保留pkg_resources validation依赖/私有site来源，具体pip/setuptools pin待原Owner验证，不猜latest。
- 不要全局--only-binary=:all:：python-docx0.8.11仅sdist，当前正确功能会被误拒绝。若要固定依赖bytes，可按包选择已验证wheel/私有hash-bound材料，pure-python sdist保持允许；不是改变active任务或新增硬时限。
- 不删six dependencies/工具功能；不顺手升级PyPDF2主版本，其原PdfFileReader/Writer/API有真实调用；不放宽C1-C4或业务/身份断言。
- 保持7594/f3d固定现行active run不改、不kill/restart。当前继续下载不是死锁，变更仅下一固定候选，完成/错误由主控收终态。

### 公开metadata已匹配的候选（无试装/大包下载）

| 候选 | Requires-Python | 适用wheel | 字节 | SHA256 |
|---|---|---|---:|---|
| Pillow==10.4.0 | >=3.8 | pillow-10.4.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl | 4452804 | 5e84b6cc6a4a3d76c153a6b19270b3526a5a8ed6b09501d3af891daa2a9de7d6 |
| Pillow==10.4.0 | >=3.8 | pillow-10.4.0-cp311-cp311-manylinux_2_28_x86_64.whl | 4533541 | 76a911dfe51a36041f2e756b00f96ed84677cdeb75d25c767f296c1c1eda1319 |
- metadata `https://pypi.org/pypi/Pillow/10.4.0/json` SHA256 `57d97d865df4aa2f611a01f0f2165546f8b156786dac41b1080709baf2b28640`；状态METADATA_ONLY_NOT_INSTALLED_NOT_FROZEN。
| reportlab==3.6.13 | >=3.7,<4 | reportlab-3.6.13-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl | 2767420 | d95fc8bc177a009053548c6d851a513b2147c465a5e8fea82287ea22d6825c4e |
- metadata `https://pypi.org/pypi/reportlab/3.6.13/json` SHA256 `d8630998b97110ee39558e312bd468e37a123edb480390159d0d5d8eb22c0351`；状态METADATA_ONLY_NOT_INSTALLED_NOT_FROZEN。

这些wheel匹配当前实际tags（glibc/platform见JSON），不等于已下载checksum/ABI/API通过。两个candidate可供Knuth定向验证，不要求改所有six pin。

### Knuth下一切片：精确最小候选diff（不再泛查）

在主控分配的Knuth UR01独立worktree应用；组件定位 `/home/isp/wsps/chcbz/isp-install/conf/codex-ws-agent/toolchain/requirements.txt`，**不是让修改该共享目录或live archive**。
基线读取文件 `/var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/codex-ws-agent/toolchain/requirements.txt` SHA256 `d0d6d95c2f8b56d28c34d6cb98625fe2468d04b39be25ae5e8f3083ba1fd1f1d`，行1/6/8：

- 行1：去除过时Python3.6备注，注明实际Python3.11.13目标及候选验收待证，不冒称可迁移完整工具链。
- 行6：候选 `Pillow==8.4.0` → `Pillow==10.4.0`。
- 行8：候选 `reportlab==3.6.8` → `reportlab==3.6.13`。
- 其余四pin保持；候选已证cp311 wheel/Requires-Python/SHA/size，未试装/API验收。
- 本次最小瓶颈patch不必改installer pip bootstrap：pip21.3.1已有匹配标签。若另改支持契约，保留pkg_resources和私有模块来源验证；不全局only-binary、不把Python回退3.6。
- 固定新client commit/archive再跑完整C1-C4（private新target、six pin及lxml等真实import、relocation/no-host、六格式create+reopen），原六E05全部保留；不重写7594/f3d或当前session83600。
- 原validate/execution-adapter/clean-target验收逻辑默认不改、不放宽断言；只有新候选实际诊断才由原Owner定向修必要API。

### 保留验证（support未跑）
- /var/tmp/cyf-ur04-local-20261008T205238/ur01-clean-install-Dgt3R6/source/conf/cyf-agent-runtime-v1/test/clean-target-install.acceptance.mjs C1-C4完整：真实新target、pre/post路径隔离、six pins/实际imports/无host模块、PNG/JPEG/PDF/DOCX/XLSX/PPTX create+reopen、原executor与迁移
- 原6E05完整selector保留，不本slice重复执行或删skip；当前consumer83600不控制。

## 未证/不得扩大结论
- 约16KB/s为何发生（CDN路径/链路限速/服务端窗口等）未证明；不能归罪proxy或pip算法。活动peer为数字IP，未读取TLS request，原TLS request exactURL未证；但Pillow最终完整SHA已由后续主控证据匹配官方metadata。
- HEAD200/Content-Length只验证公开对象存在/声明大小，不是吞吐基准，HEAD本身不证明下载checksum；Pillow完整SHA现已由主控另证，ReportLab完整SHA仍未知。
- 完整Pillow源码编译/ReportLab编译及Python3.11运行结果NOT_RUN；本slice没有compiler children。
- lxml/XlsxWriter/et-xmlfile最终版本/完整依赖ready/原验收C1-C4+6E05终态仍未证。
- 候选cp311 wheel metadata匹配，不代表下载/安装/API/ABI/业务验收通过；原Owner下一fixed candidate验证。
- installer仅检查Python可执行并venv，不明确限制Pythonminor；Python3.6备注不是已验证3.11支持声明，也不是3.11不支持证明。

## 安全操作账

只读：6个exact release JSON、2个candidate JSON、1次公开HEAD（无body）、源码/已完成小wheel metadata、/proc metadata及自身isolated import/tag探针。0 pip install、0 large artifact payload bytes、0 range、0 ptrace/signals、0 原fd/stdout/socket正文读取、0 source/target/config修改；只写这两份/var/tmp报告。

主控delta证据：`/home/isp/wsps/cyf/evidence/unified-agent-runtime-20261008/install-pip-diagnosis-20261008T2142/process-delta.json` SHA256 `6f296b697a582f628dd0f1ced75f0219236726d60ef67ec82860c056cb6aff89`；本报告不新建证据目录/ledger、不替主控收live终态。
