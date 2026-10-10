# GSS-REJOIN-20261010：公孙胜除名下山并重新入伙

- 2026-10-10 Asia/Shanghai，Owner Main；用户在六任务取消完成后明确“好，继续下一步”。范围仅当前账号的公孙胜（personaCode gongsunsheng，原agentId agt_510b7fea20564b52bc70b3a08d2c6c4f），走已有业务API/前端流程；不改其他角色/任务，不操作其他聊天进程，不确认新租金/付款。
- 既有六任务取消证据见GSS-CANCEL-20261010；本轮仍先fresh读取，不靠历史成功代替当前前置。只读源码API develop `36d9e5452ab8beb64b97e5570da6ede10ec38797`，Web HEAD `17ecf1c0b581cab1456acff4db097a6a4d335e3d`；07:46安装record仍API1.14.2/相同commit。此为本地源码与线上记录核对，不宣称新fetch远端。
- 已读AGENTS、ops/orchestration/README与既有handoff，复用原本线程浏览器driver，只建立新owned临时Chromium，不使用/关闭用户in-app浏览器。证据 `/var/tmp/cyf-gongsun-rejoin-20261010-G2uKp5`。
- 非目标：不直接改DB，不绕绑定/租约/授权，不为重入伙强杀共享Runtime，不选择免费local来伪报server入伙成功，不以202或付款预留冒充Runtime就绪。
- 验收：除名前后catalog/所属账号/任务状态；正常DELETE成功后确认bound=false；随后原UI重新入伙，若需新租约，最多读取真实报价，停在确认付款前。当前状态：读取前置，尚未除名或重新绑定。

## 2026-10-10 07:50 前置实测：发现既有付费租约，除名前等待用户选择
- 六任务fresh GET仍cancelled/v2；公孙胜catalog仍boundToMe=true、offline、无currentTask。
- 原agent hosting-lease真实GET200：managed=true，lease `hrl_31485bed-d6d5-4f15-be31-b3511aeafe95`，ACTIVE/v2，binding15；已付1000 SILVER/30固定天，租期2026-09-26 01:37:21至2026-10-26 01:37:21（北京时间），admission=ALLOWED。UI同步显示“免费重整接应（不续租，不延长到期日）”按钮可用，钱包可用与预留均0。
- 同部署源码核对：HostingRentApplicationService.lookup/reprovision均要求当前active binding；AgentHostedBindingTransaction.suspendDatabase会暂停binding/identity并清除runtime绑定，未提供剩余租金退还/迁移。INITIAL的currentBinding仅查active，除名后会生成新canonical ID/新初租报价。故旧租约仍有效时先除名会失去原绑定的免费重整路径，不能假定重新入伙自动承接剩余租期。
- 因新增明确成本后果，在破坏性除名前停下询问用户是否改为现有租约免费重整；未擅自替换用户指定步骤。尚未DELETE除名、未POST bind/REPROVISION、未获取新租金报价/确认/扣款，不把UI打开租约面板当作重整成功。
- 证据：persona-before.json、six-tasks-current-before.json、lease-before.json、existing-lease-ui.json，均在本轮临时目录。下一动作：用户选择是否保留现有租约免费重整；如仍明确要求除名，按正常DELETE后再预览新租约，付款仍须另确认。

## 2026-10-10 07:56 用户明确要求两场景顺序验收
- 用户在已获知旧租约不自动继承、新入伙走付费流程后明确：“两种场景都验一下，先跑一遍除名后重新入伙，然后再跑一遍重整接应。”本轮按此顺序推进，不擅自改为只做旧租约重整。
- 新证据目录 `/var/tmp/cyf-gss-two-scenarios-20261010-Trb3FE`，复用原driver，Main独占本轮owned Chromium。原07:50无变更结论保留。
- 验收分别记录除名、重新绑定受理、租约与真实服务就绪、免费重整受理与完成。确认既有接口/报价/余额，不进行外部充值、人工增发资金、直接SQL补状态或重启共享Runtime；若遇真实业务阻塞先定位，不伪报两场景通过。

## 2026-10-10 08:01 两场景实测结果：第一场景除名通过，重入伙被资金前置阻塞
- 正常UI点击“除名下山”，唯一DELETE `/agent/personas/gongsunsheng/bind` HTTP200；fresh catalog bound=false / boundToMe=false / canBind=true / agentId=null，UI变“请上梁山”。六个cancelled/v2任务除名后owner GET仍200，未删除历史。
- 随后UI“请上梁山→山寨安顿”自动获取INITIAL报价并尝试迎新金（不是本轮另发POST bind）。真实报价 `hrq_2e294751-ddfb-40e3-84e9-0806750a0c80`，预拟agent `agt_631bda37e4684ae897f077335ca24b53`，1000 SILVER/2592000秒，未确认。报价中的预拟agent不代表绑定或Runtime已创建。
- 钱包GET：availableMicro=0、heldMicro=0、version8；UI确认付款按钮disabled，提示“迎新安顿金到账后余额仍不足，未提交租金”。根因已核：GET ledger只有四条旧流水（nextCursor=null），一次性hosting-welcome-v1迎新金 `etx_c5030036-d455-4483-8178-4e76e5438323` 在2026-09-26已发1000 SILVER，后续退款/再预留形成当前旧租约且余额为0。本次迎新POST200只是既有一次性活动幂等回执，不增发余额；源码按scope/actor/campaign固定幂等键。
- **未发送任何新POST persona bind/REPROVISION；未新扣款、未外部充值、未手工改余额。** 第二场景依赖第一场景新绑定/租约完成，因此尚未执行，不能报告两场景通过。当前公孙胜确实已除名，尚未重新入伙。
- 不调用 `/economy/preview/issuances` 绕过：当前源码要求显式dev/test且排除prod/production，不是生产补款入口；钱袋UI目前只读余额/流水。需确定正常测试资金补充办法，缺口1000 SILVER，而不是盲重试迎新金或免费local伪成功。
- 证据均在本轮目录：catalog-before/after-unbind、old-lease-before、rejoin-quote-and-grant-ui、wallet/ledger-after-quote、final-network、six-tasks-after-unbind、summary.json。已清除浏览器内未确认报价（未付款）并关闭本轮owned Chromium。下一动作待用户决定生产测试资金来源或资金入口缺口处理方案，再继续同顺序验收。
