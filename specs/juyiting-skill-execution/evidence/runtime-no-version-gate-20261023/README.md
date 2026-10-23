# Runtime取消Codex版本／协议门禁

2026-10-23，源码候选Runtime1.2.9，isp-install cbc1050825a40378313f283e9f25dc46d44c1ea4。该目录只记录本次改动，不替代既有API上线/业务证据。

- 移除CLI版本注册表、版本精确匹配、生成协议schema及其摘要门禁，typed就绪不再比较这些值。
- 文件/资源完整性、身份授权、业务数据校验和沙箱保持；运行中换包仍需受控重新测量。
- 定向单测、真实CLI0.164.0空白HOME无模型握手通过；各本机套件有交叉，不能累加计数。
- 完整隔离探针TLS阶段未通过，原始失败记录保留；未改变产品超时/网络规则，未执行模型turn，也未验证多轮图片。
- Flow27/28测试前失败，第二轮诊断确认cache restore生成ossutil.log导致源checkout不干净。第三轮改用固定commit独立干净worktree，不忽略脏文件、不删缓存日志；Run29 SUCCESS：354项中352通过、0失败、2项明确opt-in native跳过；其中CLI初始化另有本机真实通过，完整隔离TLS不伪报通过。临时Flow配置恢复APPLIED且readback一致。
- 21:13的生产1.2.8为发布前基线；21:39后已通过Flow30安装1.2.9，见下方发布补记。未重放519、未改变历史业务状态。

当前交接：[RUNTIME-NO-VERSION-GATE-20261023](../../../../docs/implementation/handoffs/RUNTIME-NO-VERSION-GATE-20261023.md)。原始Flow控制和日志放`/var/tmp/cyf-runtime-no-version-gate-20261023/`；不复制凭据/完整宿主配置。

## 授权发布补记（21:42）

Flow5264702/30固定同一cbc1050源码，354项中352通过/0失败/2跳过；93项程序文件由同Run制品安装到固定app，部署单71709927成功。PID1507807，三Agent通道connected/registered/ready和ACK新鲜度核验通过；配置身份未改，8条recovery摘要保持。临时Flow配置恢复APPLIED。完整版本、制品/安装摘要及恢复路径见[release-flow30.json](release-flow30.json)。

通道就绪不等于识图就绪：上线重新测量后旧carrier证据绑定不匹配，启动日志为TYPED_INSPECTION_CARRIER_EVIDENCE_INVALID；恢复消息还出现inputPolicyDigest空引用。保留真实阻塞，不改历史状态或伪造carrier摘要；正在独立目录用当前程序执行9种图片载体实测，随后才能启用新证据。

## 当前carrier恢复（22:07）

9种现有图片载体真实模型识别全部PASS；运行中1.2.9代码的正常证据加载器再次测量contractReady=true。Flow5264702/31仅安装新实测证据与吴用profile引用并受控重启（未重复构建/部署程序），部署71710512成功，配置已恢复。PID1516365；93项程序摘要未变、三通道通过、8条旧恢复记录仍未修改。启动不再出现carrier无效或inputPolicyDigest空引用；旧510/513 UNKNOWN的轮询提示不因此视为修复。见[carrier-refresh-flow31.json](carrier-refresh-flow31.json)。旧1秒TLS测试失败保留，新结果使用生产既有15秒网络超时，不改变产品超时。

新浏览器任务520/会话1760458007122由ziyue指派吴用，首轮识图正确，inputReceipt命中原图SHA a8017615…；不将其当多轮改图/生图完成。

## 浏览器回归最终状态（22:39）

ziyue/吴用，任务520的两轮识图均正确，三轮输入回执均匹配原图SHA；第三轮请求改原图时返回REVISION_REQUEST，随后review outbox持续RETRY/SourceUnavailable，尚无childRequest。日志与已部署API041548f源码对应的根因：ChatDeliveryRevisionService第87行用任务owner准备目标Agent技能包，跨账号校验失败；普通讨论入口则已用dispatchAuthority.admissionTarget解析executor owner。此问题未修改API，也未绕ACL/改DB/重放519。详细输入回执、最终回复、投影与调度状态见[business-task520.json](business-task520.json)，调用栈见[task520-revision-stack.log](task520-revision-stack.log)。

无输入生图、原图编辑产物、连续两轮上一版改图、图片成果PC/移动验收与完成态重入仍未验证；不要用9载体/两轮识图替代。测试浏览器曾阻止一次discussion写请求，授权正确路径后重试成功，不计产品缺陷。

浏览器证据：[PC首轮识图](520-first-inspection-pc.png)、[PC修改阻塞](520-revision-blocked-pc.png)、[移动端排队状态](520-revision-queued-mobile.png)。截图仅覆盖显示的局部状态，不代表移动端图片处理完整流程验收。自有浏览器/网络采集已关闭。
