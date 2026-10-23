# Runtime取消Codex版本／协议门禁

2026-10-23，源码候选Runtime1.2.9，isp-install cbc1050825a40378313f283e9f25dc46d44c1ea4。该目录只记录本次改动，不替代既有API上线/业务证据。

- 移除CLI版本注册表、版本精确匹配、生成协议schema及其摘要门禁，typed就绪不再比较这些值。
- 文件/资源完整性、身份授权、业务数据校验和沙箱保持；运行中换包仍需受控重新测量。
- 定向单测、真实CLI0.164.0空白HOME无模型握手通过；各本机套件有交叉，不能累加计数。
- 完整隔离探针TLS阶段未通过，原始失败记录保留；未改变产品超时/网络规则，未执行模型turn，也未验证多轮图片。
- Flow27/28测试前失败，第二轮诊断确认cache restore生成ossutil.log导致源checkout不干净。第三轮改用固定commit独立干净worktree，不忽略脏文件、不删缓存日志；Run29 SUCCESS：354项中352通过、0失败、2项明确opt-in native跳过；其中CLI初始化另有本机真实通过，完整隔离TLS不伪报通过。临时Flow配置恢复APPLIED且readback一致。
- 当前未安装Runtime1.2.9；2026-10-23 21:13回读生产仍1.2.8/PID1404284。未重放519、未改变历史业务状态。

当前交接：[RUNTIME-NO-VERSION-GATE-20261023](../../../../docs/implementation/handoffs/RUNTIME-NO-VERSION-GATE-20261023.md)。原始Flow控制和日志放`/var/tmp/cyf-runtime-no-version-gate-20261023/`；不复制凭据/完整宿主配置。
