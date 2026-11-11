# Runtime 配置目录迁移与吴用图片能力（2026-10-11）

## 冻结范围
- 用户授权：将 `/etc/cyf-agent-runtime-v1` 迁移到 `/home/isp/conf/cyf-agent-runtime-v1`，然后启用图片能力。唯一Owner Main；不发布Web/API、不迁stateRoot、不更改其他账号Provider配置。
- 源码：`/home/isp/wsps/chcbz/isp-install` develop/base `aa6b96aa983f47b4a4d8daff64eaf717b5781978`（17:25本地/远端匹配）；独立工作树 `/home/isp/wsps/worktrees/runtime-conf-image-20261011` / `codex/runtime-conf-image-20261011`。
- 当前服务：`cyf-agent-runtime-v1@unified` PID2069517；现行release `jyt-control-receipts-20261011-aa6b96aa983f`。原3个独立角色服务已failed，不启动它们。
- 已确认配置缺口：CLI main未将静态subject的Provider环境映射传给已有执行器注入点；不从进程全局环境/其他角色HOME回退。增加显式私有配置文件、按完整subjectKey映射的最小读取链并回归。
- 验收：配置路径单入口，原身份/状态/托管关联不变；原installer构建完整制品；共享发布锁与备份下温和停止/启动一次，保留原release和配置备份；API读取吴用图片能力，续验原440不重复创建。
- 证据 `/var/tmp/cyf-runtime-conf-image-20261011`。配置备份写 `/home/isp/baks`，不输出密钥。


## 17:35 完成迁移与能力启用（不是生图验收）
- 源码`5b902c1bcd3efced9720e015e3b8240d39ce0738` / tree`7f6e8944e052071cadd0760fa38df07f2c38db58`，已FF合入并push isp-install/develop。Runtime版本1.0.2；前后端源码/生产安装未变。
- 改动：两个systemd模板的配置根；CLI主入口与security私有配置读取；runtime.env.example、运维说明、对应测试。Provider映射显式文件、完整subjectKey、每subject仅匹配profile的CYF_PROVIDER_*图片key；未配置图片的subject不需要映射，不继承进程环境、无跨subject fallback。
- 最终7个selector共140 PASS、0FAIL、0SKIP，bash语法及diff检查通过。首次测试失败为新工作树缺npm依赖及新测试fixture缺目录/subjectKey，明确修正后最终通过；没有把失败标通过或省略测试。日志`final-tests.log`。
- 原installer在固定干净源码完成完整npm/独立Python venv安装和closure validation；本批从现行global pip源解析并固定显式index与全局配置SHA，未借宿主包。3038文件、66源码文件字节匹配；catalog SHA `4380ffef7ce222828b959f7ffcdfd3d9cb4da4b23a2234b0d79fa6804320d581`。Node实际20.20.2、Python3.11.13，仅记录不设版本门禁。
- 新release `/home/isp/apps/cyf-agent-runtime-v1/releases/runtime-conf-image-20261011-5b902c1bcd3e`。既有coordinator→release锁下变更，旧进程SIGTERM后3秒退出，原6把运行写锁自行释放；未强杀、未删锁/会话/托管journal。新PID2341655，NRestarts0；4个subject的6份写锁已在同PID重新持有。本人吴用/林冲/公孙胜线上可用；未做卢俊义账号业务操作。
- 新根`/home/isp/conf/cyf-agent-runtime-v1`；原`/etc/cyf-agent-runtime-v1`已移入备份，无遗留入口或软链接。systemd模板和实例drop-in均引用新根；所有stateRoot/manifest/installationId保持原值。吴用图片账本独立放在`/home/isp/state/cyf-agent-runtime-v1/unified/agents/wuyong/controlled-image`。
- 备份`/home/isp/baks/runtime-conf-image-20261011`含config-before、retired-etc-config、unit.before、dropin.before及停止后的journal私有快照；后者仅审计，不覆盖之后的新journal/session floor。若需恢复，必须同锁核对当前版本、温和停止当前唯一Runtime，恢复原unit/drop-in与原配置路径并验证，再启动原release；不得同时启动新旧实例，不从快照回退业务状态。
- 真实事项440接口HTTP200/E0：serverLaneREADY、controlledExecutionREADY、GENERATE_IMAGE、binding/mode匹配。任务级授权仍CONSENT_REQUIRED/OWNER_EXACT_CONSENT_REQUIRED，尚未Provider调用、生成PNG、下载或验收；不把启用能力写成完整生图流程通过。前端页面本轮未点将，不新增事项或资金动作，专属浏览器已关闭。
- 已将稳定路径/凭据规则回写服务器架构和项目runbook。最终证据`apply-result.json`、`final-artifact-verification.json`、`final-readback.json`、`capability-ready.json`、`roster-after.json`，均位于本轮证据目录。下一步按原440的现行业务确认入口取得精确调用同意，再进行一次生图及产物验收；不绕过门禁自动扣费。
