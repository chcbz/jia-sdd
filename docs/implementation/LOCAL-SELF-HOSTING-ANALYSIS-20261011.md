# 招贤令「自家接应」现状与最小闭环方案

核对日期：2026-10-11 21:36 Asia/Shanghai。范围：只读源码、远端引用与已安装对应文件，不触发绑定、installation/enroll、收费、安装或服务变更。本文为分析，不是开发完成或生产实测报告。

## 固定基线与同步结论

- isp-install `/home/isp/wsps/chcbz/isp-install`：本地HEAD与本次实时`ls-remote origin refs/heads/develop`均为`5b902c1bcd3efced9720e015e3b8240d39ce0738`，工作区干净；Runtime1.0.2。
- 已提交配置根迁移到`/home/isp/conf/cyf-agent-runtime-v1`、systemd两份模板、静态subject图片Provider映射读取、runtime.env.example、相关测试和README。已安装release `runtime-conf-image-20261011-5b902c1bcd3e`的agent-runtime.mjs、lib/security.mjs、runtime.env.example逐SHA与源码相同。
- 真实主机host/profile/Provider密钥属于部署私有配置，不复制进Git；不以“已同步源码”冒充真实凭据已入库。既有迁移发布证据见`/home/isp/wsps/cyf/docs/implementation/handoffs/RUNTIME-CONF-IMAGE-20261011.md`。
- 当前Web1.14.8/621b87a1、API1.14.7/cf140272已发布；本次local分析基于对应本地组件源码，未再触发构建发布。

## 已确认断点

1. 前端仍展示旧安装链。`/home/isp/wsps/cyf/web/src/components/juyiting/PersonaCatalogPanel.vue:158-200`指向master的codex-ws-agent-install教程，要求OPENCLAW_API_KEY、codex-profiles.conf、旧service和已不存在的shell/codex_ws_agent_install.sh，并遗留Node>=20说明。其`--profile agent`实际已改指统一Runtime，需要显式实例/解释器输入；与页面所述不是同一套安装。
2. 后端local分支只绑定名册并输出旧配置。`/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/service/AgentPersonaProvisioningService.java:167-196`仍输出旧workdir/API-key配置；没有在本分支衔接Runtime installation、manifest和enrollment。不能把“自家接应文书已备/已入名册”当Agent已在线。
3. 新Runtime安装skill也有旧内容。`/home/isp/wsps/chcbz/isp-install/skills/cyf-agent-runtime-v1-install/SKILL.md:23-40`描述安装服务模板、使用根目录`node agent-runtime.mjs validate --manifest`，并称仅heartbeat。当前shell只准备制品、不激活服务；真实CLI为制品内Node + runtime/agent-runtime.mjs + `--config host.json`，enroll另需精确`--subject`。教程不能直接照搬，需对齐现行可执行入口。

以上是确定的契约/入口不一致，不是本轮新入伙端到端失败实测。不扩历史恢复、不恢复旧API-key认证。

## 可复用的现有能力

- 绑定：现有`POST /agent/personas/{personaCode}/bind`的mode=local，保留owner/client/tenant身份和local不收托管租金。
- 安装登记：`/home/isp/wsps/cyf/api/agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentRuntimeV1Controller.java:40-65`已有本人JWT保护的installation create/status/revoke；不是管理员专有接口，不在浏览器返回安装密钥。
- `AgentRuntimeV1InstallationRequest`已有installationId、canonicalAgentId、manifestVersion、manifestSha256、enrollmentSecretSha256、enrollmentExpiresAt。安装侧保留明文secret，仅以digest登记；`enroll`消费一次性secret，服务运行使用独立installation/session授权。
- 统一Runtime已有manifest/profile/host校验、按subject enroll、session、实际执行器、在线注册与能力声明。单台自家机器可以在一个Runtime中管理多个Agent；不同物理机器各自Runtime，不把远端机器接进本生产host的进程。

## 最小实现方向（尚未编码）

1. **统一自家接应契约**：local响应输出非秘密的精确scope/Agent身份及新Runtime配置说明；前端删除旧安装命令、旧API-key示例和旧教程，不保留双轨。区分已绑定/待接入和实际在线可执行，利用现有状态来源。
2. **补齐安装侧交接**：目标机器生成并持久化installation/manifest/一次性secret候选，使用既有本人授权路径登记摘要，再精确enroll，写入host/profile及独立stateRoot。页面到目标机器的非秘密候选交接/本人授权方式须在编码前固定，不能让用户手算摘要，也不把密钥打印到命令/浏览器/日志。优先复用现有CLI和安装登记，不另建认证或安装表；未知响应先查询原installation，不反复新建。
3. **对齐isp-install文档和模板**：与真实制品布局、`--config`、`--subject`、配置根、服务安装/启动边界一致；记录实测工具版本，不另加项目Node版本门禁。目标机器自己的模型配置单独提供，不能复用生产吴用私有密钥。
4. **正常流程验收**：使用一个当前未占用的本人角色和明确指定的目标机器，实际UI自家接应→安装登记/enroll→在线/执行能力→连续两轮文字密议→一个新普通事项交付并验收。不得用测试机心跳或绑定成功替代真实业务。先验证文本正常链路；图片作为该角色单独配置的可选能力，不默认为开通自家接应就可生图。

不增加第二套Runtime、不接托管租金、不做旧流程兼容或边缘恢复。尚未指定目标机器和新角色，本文没有使用现有生产Runtime模拟另一台自家机器，也没有自动除名任何已绑定角色。

## 2026-10-11 22:19：李逵目标机实测补充

前文“尚未指定目标机器/角色”为21:36分析时的历史状态。之后用户指定李逵并确认173.230.149.118，已用现有正式installation/enroll完成远端统一Runtime1.0.2接入，连续两轮密议以及新事项446文字交付/正式验收通过。源码未修改，详证见`/home/isp/wsps/cyf/docs/implementation/handoffs/LIKUI-SELFHOST-20261011.md`。

新增确定断点：公网Nginx缺少`/internal/agent/`反向代理，来自李逵主机的Node原生文件轮询在真实access log返回444，客户端表现UND_ERR_SOCKET。因此普通文字成功不代表文件/技能/图片通道通过；本轮未扩大公网路由。原三个页面/文书/安装交接产品缺口仍未开发，不能用操作者带外接入结果消掉待办。

## 2026-10-11 公网网关后续修复

用户授权后已按API cf140272白名单补本机Nginx原生路由并reload（根仓配置f6f34cd0），李逵真实轮询由444恢复200，鉴权反例仍拒绝；该网关断点已闭合。前端旧文书/安装交接缺口未开发。新事项448真实文件需求返回CLARIFY：当前议事能力清单只有资料读取/图片动作，没有通用文本文件生成适配；不得将网关通畅或文字业务通过改标为文件流程完成。范围/生产备份/证据见 `docs/implementation/handoffs/LIKUI-SELFHOST-20261011.md` 后续记录。
