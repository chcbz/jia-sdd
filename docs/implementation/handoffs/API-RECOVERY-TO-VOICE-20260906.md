# API 恢复结果与语音运行权交接 — 2026-09-06

## 用户授权与边界

用户要求“确认 API 恢复结果，更新恢复任务台账，将运行权交接给聚义厅语音发布线程”。本主控只读核验和原子控制面登记；不执行 START/STOP/RESTART、不发布 JAR、不改 Nginx/数据库或语音开关。接收运行权不等于阶段1执行 GO。

## 当前恢复观察（10:04–10:09 CST）

- `/usr/local/sbin/cyf-api-kit status` 自然退出 rc0：RUNNING、HEALTH=UP、ARTIFACT_ATTESTATION=MATCH、10018=LISTENING_BY_PID。
- PID `1222845`，start ticks `3021456883`，PPID=1，身份 `cyf-api(987:1000)`，启动时间 `2026-09-06 05:00:26 +08:00`。
- 当前 JAR SHA-256：`246520c53387b90c8b57640702bdc42130cca013903b6c1f1c4f3773d6c5a2c0`；canonical status 已核对当前文件 SHA 与受控 runtime record 一致。
- canonical lifecycle SHA-256：`56537824cd33f6333f199ea1cebda90b127b39c079e08daad6d164607f788ef5`。
- 用户统一入口 SHA-256：`c84e6202dc4ef6c60ae66b3315f49012b52ec2ff9d7280683b01d87cf3b18e1b`。
- 本机 health HTTP200/UP；公网 `/actuator/health` HTTP403，不是公开 UP 证据，不把它当成502或完整业务 smoke。
- 核验完成后无 canonical lifecycle START/STOP/RESTART/status 命令在途；旧 PID877327/877855 均不存在。
- 共享核验包：`/var/tmp/cyf-api-recovery-handoff-20260906-main/baseline.json`、`canonical-status.txt`、`lifecycle-observation.json`。仅分享本主控自己的证据，未读写外线程证据目录。

## 旧记录与终态归因

旧 `OPS-API-RECOVERY-20260905-1932` 仍登记 Peirce `01a07194-ec7d-72a3-b848-468578832164`，引用 bash877327/Java877855。当前健康进程不是该旧 PID；不能从当前UP伪造旧 START rc0，或把05:00的后继启动归给未知线程。旧 Owner 的自然终态/释放回执未能通过现有通道取回：read_thread只暴露completed/idle而正文为空；显式共享写回执与一次权限限定修正均exit1且stderr被屏蔽，无有效回执。停止重试，不将exit未知标为原START成功。

聚义厅 BUG follow-up 主控已明确回执：未执行 Java 生命周期/JAR/Gradle、不持10018运行权。其09:15五行 archive CORS Nginx修改已完成，与 API启动无关，不需要停止其Web修复。

## 接收方与顺序

语音发布主控确认 exact thread `01a055d5-2588-7192-adff-5be7788ec623`，身份是协调者而不是runtime Owner。其先创建仅待命的唯一runtime Owner并回exact ID；本主控随后在同一控制锁内完成旧恢复记录收口与新runtime登记。独立阶段1审查仍需 flags-OFF、local-consumer proof、已安装/候选生命周期身份。阶段2真实STT/TTS、阶段3enabled Web最后发布均不因本次运行权交接豁免。

## 交接状态

接收方已确认为 JVC-OAI-RUNTIME-PHASE1 / Turing6 / critical_worker `01a0747e-d530-73d2-ba10-58b3f923712e`。原START退出码保持 UNKNOWN；本次收口仅确认后继服务当前可用，不宣称恢复了原调用收据。按用户明确移交授权，基于旧PID消失、旧线程idle/completed、当前exact运行包与健康核验、无生命周期命令在途，实施控制面行政移交；不伪造旧Owner ACK，也不授权任何进程操作。最终是否已转移以唯一运行台账及本主控 handoff.json 为准。

## 历史回执缺口与有界归因

- 原START rc/结束时间/后继启动来源：UNKNOWN，未用当前UP或线程completed替代原调用终态。
- 读取线程回执正文丢失；改显式共享文件后两次写失败。首次root目录对isp不可写为发现的条件，限定权限纠正后仍失败，因此最终原因未被证明；不声称权限修正已成功。
- 旧进程877327/877855已不存在；旧线程最后可见回合completed且idle。无需/未对其任何进程发信号。
- 用户明确要求运行权移交；因此只关闭“当前服务恢复可用”的工作项并行政释放陈旧认领。原历史缺口保留，phase1审查仍可要求更多启动来源/安全证据；未自动出具阶段执行GO。
- BUG/CORS主控与API运行无关；独立Web任务不受此次移交影响。

## 已完成控制面交接

- 时间：`2026-09-06T10:28:00+08:00`；原恢复项 `done / owner=null`，仅表示当前服务恢复可用。
- 新运行权：`JVC-OAI-RUNTIME-PHASE1` / `01a0747e-d530-73d2-ba10-58b3f923712e`（Turing6，critical_worker），`claimed` 待命。
- 原START退出码/明确旧Owner ACK仍缺失；用户授权的行政移交，不伪造原调用成功。
- 同一控制锁内CAS检查两侧Owner/gate/新候选SHA，核对当前runtime record/ticks/health/端口和无在途生命周期命令，仅修改这两个运行记录。
- `handoff.json` SHA-256：`f3f4853c2eaa29459d991500c3b7855ec2eb219f195487c1ef4c304560c49d5d`；允许语音主控只读消费这一明确共享回执及 baseline.json。
- ledger交接时SHA-256：`81599901a8f9e6740dc0d96425c64276e42cb0421073e4c887cfd82ace5fe48a`；validator VALID。当前执行仍只用唯一台账，不用本文作为第二运行队列。
- **没有执行GO**，无START/STOP/RESTART/部署/激活；下一步由语音主控针对真实历史证据缺口与phase1合同安排独立只读审查。
