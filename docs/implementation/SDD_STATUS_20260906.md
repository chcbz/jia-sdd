# SDD 全量交付盘点 — 2026-09-06

文档任务：`SDD-ARCHIVE-20260906`；截止 2026-09-06T09:21:00.295553+08:00，运行台账更新时间 2026-09-06T09:19:31+08:00。

## 口径

- 唯一当前执行台账仍是 `TASKS.yaml#runtime_ledger_json`；本报告及归档是静态证据，不承载 claim 或第二 Owner。
- 归档八个历史交付包，其中五个是本次确认的发布/运维记录，另三个为原 SDD 已有完整发布验收的功能。历史发布归档不代表整个需求完成。
- source ACCEPT ≠ build PASS ≠ artifact deployed ≠ feature activated ≠ 全部业务/真机验收通过。旧风险接受和失败证据不能重写为 PASS。
- 核心 economy 五件套受 bundle SHA 绑定，保持原字节，以 delivery-status.md 补充当前 V0 进度；生产草案不等于 V0 未开始。
- 只做文档和证据索引，不改源码、生产配置、运行台账或 root gitlink，不停止任务，也不删除证据。

## 需求总表

| 需求 | 状态 | 归档/剩余边界 | SDD |
| --- | --- | --- | --- |
| 账号安全基础与全局撤销 | implementing | Cookie 修复包已在运行台账行政收口，但只记录 manifest 校验，缺 exact Git 绑定与 credentialed 生产验收；不能把整个账号安全需求标为完成。 | `specs/account-security-foundation/delivery-status.md` |
| Agent 客户端技能刷新 | released | 已交付并归档原 2026-08-23 功能；原验收记录 API108、Client97 与运行 smoke，未在本次重复执行。 | `specs/agent-client-skill-refresh/spec.md` |
| Agent 工作目录能力刷新 | released | 历史 acceptance 与 release 均有依据，统一原顶层 accepted 与 release.released 的陈旧状态，归档 2026-08-23 交付。 | `specs/agent-workspace-capability-refresh/spec.md` |
| 案卷阁典籍阅读 | implementing | H01–H05W 已接受，H06 已发布；旧 reader 修复随 Web101ac4c 发布，CORS 补丁也已部署并通过可信/非可信预检，剩余 authenticated adapter/真实阅读闭环未完成，整体不归档。 | `specs/archive-pavilion-reader-mvp/delivery-status.md` |
| 聚义厅横竖屏体验 | implementing | O00–O04 已源码接受；高度修复已发布但台账仍有 integration 缺口，旧屏幕修复已发布；新循环/屏幕 follow-up 尚未验收。 | `specs/juyiting-dual-orientation-experience/delivery-status.md` |
| OAuth 公共客户端加固 | released | 按原 SDD 中独立审查与 2026-08-24 发布记录归档；不扩大为所有账号安全/公共公测需求已完成。 | `specs/oauth-public-client-hardening/spec.md` |
| 银两交易、技能市场与托管租金 | implementing_preview | V0 正在实施，W01/W02/W03/R00 已 accepted；余项依次处于实现、审查、验证或依赖/根因阻断。生产完整 SDD 与 V0 预览验收严格区分，未部署/未启用收费。 | `specs/agent-economy-marketplace/delivery-status.md` |
| 聚义厅语音输入与会话 | implementing | API/Web 源码、集成和独立构建材料已有 accepted；语音生产启用与真实 Provider 证明尚未完成。 | `specs/juyiting-voice-conversation/delivery-status.md` |
| 公共公测发布与安全整合 | implementing | 托管隔离、任务 ACL、离线 preflight、onboarding 等源码已 accepted，存在历史 API/Web 发布记录；尚不足以宣布整包公测安全验收完成。 | `specs/public-beta-release/delivery-status.md` |
| 聚义厅悬赏榜与可靠多 Agent 协作 | implementing | M1/M2 的任务定义记录大量 accepted/integrated；D06/D08/D09 与 M3-IR 已 accepted，M3-RG 有历史 API 上线记录。M4/M5 仍规划未完成，不能据此把整个悬赏榜高级协同归档。 | `specs/juyiting-task-collaboration/delivery-status.md` |

## 全部运行任务（66 项，截至快照）

| 任务 | 截止时点记录 | commit / tree | 证据摘要与剩余动作（历史快照） |
| --- | --- | --- | --- |
| `D06` | accepted | `f02bb1167fd0` / `3b5b519c2010` | D06 R8 authoritative ACCEPT 0/0/0 on exact API f02bb1167fd09825b02ec399c077699933b144a6/tree 3b5b519c201047d71eaf212c61fb53deb743ffb3 paired with A06 test-only 4db501816abf/tree 527c02ce9e13. Source Writer released. D08 stale candidate remains non-promotable and must be rebuilt later; no deployment is authorized. |
| `D08` | accepted | `cc5e03205d78` / `0efc5a51dca6` | D08 remains accepted on exact cc5e03205d7842768892c0c962d103a5e6f90022/tree 0efc5a51dca6085936306764d6d302a607e1ba64 with focused ownership-denial evidence 5ae746d20350a332f271cf5809ce3f16a0d1dc45aeea468289d614cdb8099c6e and isolated MySQL restart/concurrency evidence 0af7529498cbc1a806c1e7dd6d999e487cc067aa96458f5ee7d5a6536da36ca3. Cleanup removed only an unregistered stale fixture; no source/test/production action. |
| `D09` | accepted | `2d935f64ccaf` / `f4ff2d9a444b` | Authoritative sol_reviewer 01a03f09-9b7f-7921-baef-3d16d78742e0 ACCEPT P0/P1/P2=0/0/0 on exact 2d935f64/tree f4ff2d9a with fresh isolated MySQL evidence fixture 1737656840f1 and XML 5/0/0/0; R8-2 accepted, R8-3/4 remain forbidden. Dependencies D06/D08/D09 are now accepted, so M3-RG may run read-only. |
| `M3-RG` | done | `7f7360e3f65a` / `1bce97d41705` | 已按用户发布优先指令上线：API 运行包 SHA-256 c70a1e348bed6a4293a90fa6ca27cad1c1b6d1a9a77e7f1ac6b2cac93bab1271，127.0.0.1:10018/actuator/health 已返回 UP。后续仅按上线后缺陷处理，不再阻塞已发布功能。 |
| `H06` | done | `66f30bc530f9` / `56cc82235e51` | 案卷阁 H06 已随当前 API 发布并通过线上 API 可用性复核。旧离线 ArchiveContentImporterTest gate 需 >=5368709120 字节可用磁盘，当前主机不足；该发布前门禁由用户发布优先决策以实际线上可用性验收替代，根因记录保留，不重跑重型 Gradle。 |
| `ASF-COOKIE-P1` | done | `未绑定` / `未绑定` | 按用户继续推进/发布优先指令收口：已核对发布目录候选 manifest SHA-256=017e147eadafda4f87b35b3b4fa6bbafaf27334614452adefcccef37124cfc39 及 manifest-root SHA-256=a6e085773b75a100230cf4a32b59353e18000e479bdf9dfa3e8b055990a58845，清单校验通过；不执行 credentialed/生产 smoke。 |
| `PWA-HOSTED-P0` | accepted | `790f2e98b1b8` / `5bef450d3e0d` | Accepted candidate remains unchanged. Both exact confirmed-stale disposable PWA MySQL fixture roots were safely removed after separate no-reference checks. No source/test/Gradle/production/cross-task action. |
| `PWA-TASK-ACL-P0` | accepted | `ae3e04f00675` / `532d662020d4` | Fresh sol_reviewer 01a03a63-0c30-7a11-ada4-c96ec1fc9265 ACCEPT 0/0/0 on exact ae3e04f00675cf6adb99d8caa283b01748b9d3fd/tree 532d662020d44b5e607d76a57c956631989dd0e8, reusing focused evidence d56899ef. Test-only R1 closes authentication-before-DAO and contaminated-result regressions; owners released. No production access or deployment authorized. |
| `PWA-PREFLIGHT-SAFETY-P1` | accepted | `8034f4bdcc9e` / `e5ae35694f5e` | ACCEPT 0/0/0 by fresh sol_reviewer 01a03a01-be64-72d3-8f78-b8a85bd10e93 on exact 8034f4bdcc9e37961fe397494159b65dd6e51ac6/tree e5ae35694f5e5a5fb217ca8f4e22d61c95ce5cd2; offline 44/44 and targeted close/barrier/liveness 4/4 PASS. Source/reviewer owners released. Real Chromium remains a later separately authorized fail-closed availability gate; no deployment authorized. |
| `PWA-ONBOARDING-V1` | accepted | `a9034be7d4bc` / `7ffae26a8bdd` | Fresh sol_reviewer 01a03b4a-184d-76c3-bc0e-31ddb4fd3341 ALLOW 0/0/0 on exact onboarding a9034be/tree 7ffae26 after independent executable 19/19 PASS. All original P1/P2 plus R2 phase/reflection/Escape findings are closed; owner released. Real Chromium remains a separate SHA-bound availability gate; no production/deployment action authorized. |
| `O00` | accepted | `d289f120cbdc` / `afa783a95015` | O00 remains authoritative ACCEPT 0/0/0 on exact d289f120/tree afa783a9. Its clean registered worktree was safely removed non-force, freeing 256266240 bytes while preserving branch refs/heads/codex/o00-juyiting-web-convergence and commit/tree. No source/test/process/deploy action. |
| `O01` | accepted | `832dc9fd5c80` / `27b5c44904a2` | O01-R5 authoritative ACCEPT 0/0/0 by Godel the 3rd 01a03a64-b677-7093-9418-d6f100ab512f on exact 832dc9fd/tree 27b5c449. Dependency-free R4/R5 probes passed; one missing-timestamp legacy probe is obsolete under the accepted R4 fail-closed contract. Official Mocha remains pre-load infra-blocked with 0 executions. O02 may be claimed from this exact base. |
| `O02` | accepted | `fd515acf22d6` / `78779a6fc8a1` | O02 remains authoritative ACCEPT 0/0/0 on exact fd515acf/tree 78779a6f. Two fail-closed cleanup probes removed nothing; /tmp/o02-verifier-ad33b112b3f1e6a5664b0dde66eea5088d2abd31 is intentionally preserved. O03 progression remains independent; no source/test/deploy action. |
| `O03` | accepted | `0f8c243a7e32` / `ada2b911ff85` | O03 R5 authoritative ACCEPT 0/0/0 by unique sol_reviewer 01a04065-60c8-7821-a10f-e6faa58a27ac on exact 0f8c243a/tree ada2b911. Accepted evidence: V1 9/9 selectors, 144 identities, imports13 and zero resources; V2 16/0; V3 COW bundle build GO with donor/O03 identity and cleanup PASS. Owner released; O04 dependency is now satisfied and may enter read-only preparation. |
| `O04` | accepted | `965d60393fcc` / `f31118c5b522` | Fresh independent sol_reviewer 01a0467e-ecd5-7d20-a776-cbb39c6d5a32 ALLOW P0/P1/P2=0/0/0 on exact O04 commit 965d60393fcc589f691dfa1533e4855b5c13ff20/tree f31118c5b522ddbf3c4355abc466323030d7fd0f. Accepted R5 COPY_PASS key 3a75e513c20a9ad424fb3bbb68d1a14c408d57a3dada2f2d67980e6f6c388756 (23458 entries, digest c33a60be47b3a234669de2f4706ba0cf7d1a920dcff695b5283c83969cd6917d) and Gate 12.2 key 5c8bf63e8c4432e807d33b7771dcb8ea58edda784b3eb69eb8a0f6b0972558a9/artifact SHA 89d35d12c7cf60baedbdc5ef8d3638cf4daeb5377c77fde0fdec0ed209a34e8b/result 56/0/0. Durable contract ends at fresh Gate 12.2 review; no speculative Gate 12.3 is authorized. Owner released; no production action. |
| `PWA-INTEGRATION-WEB-RC` | accepted | `9d205884aaaa` / `9bd0051f85b0` | R10 authoritative ACCEPT 0/0/0 remains exact. Lease-bound fast-forward source promotion completed: Web origin/develop 7bc80de75f83d4cb7ca288380c3ed9eab1bc111a -> 9d205884aaaa07b34aebe5aa6e4191d7dde2aa7e, post-push ls-remote exact; evidence /var/tmp/cyf-web-r10-source-promotion-20260829T1742/evidence.sha256 SHA 0bc0fce43754399c547af32bcd92492590056d2b31ee8edee0edd078ba4c3f6b. Source only; production deployment remains unauthorized. |
| `PWA-INTEGRATION-API-RC` | done | `2599de3c2bdf` / `bad28da5c05d` | 发布闭环完成：该 R39 仅是离线静态封装验证夹具，R38 的 optional-field comparator 根因已保留。当前核心 API 已由直接发布版本提供服务并经本机 health=200/UP 验证；以生产可用性验收替代需 >=5GiB 磁盘的旧 R39 封装运行，不再重跑或阻塞业务发布。 |
| `M3-IR` | accepted | `828ef2e2f35c` / `f7e53c955734` | Authoritative sol_reviewer 01a03f8f-a8df-75a3-a108-ff76f9a95fe2 ACCEPT P0/P1/P2=0/0/0 on exact 828ef2e2/tree f7e53c95 with immutable addendum fc393688, fixture=N/A evidence f1c42469, XML 82/0/0/0, 50 executed tasks and BUILD SUCCESSFUL. M3-RG is now unblocked for one fresh release_guard; no deployment/activation is authorized. |
| `OPS-RESOURCE-TELEMETRY` | accepted | `d136cb7abf76` / `bc88c1b0239a` | R16 exact d136cb7a/tree bc88c1b0 accepted: fresh sol_reviewer ACCEPT 0/0/0 and fresh gpt_test_runner 58/58 PASS, Python 3.6 py_compile PASS, git diff --check PASS; verifier evidence /var/tmp/cyf-ops-resource-telemetry-r16-verifier-20260829T144208Z. First command-path failure remains attributed and preserved. Owner released; controller promotion may proceed without host probes or production action. |
| `FINAL-RELEASE-PREP-R1` | done | `397a28ab4fbc` / `05c00ec5dfc7` | 发布闭环完成：离线 deploy-pair fault-injection fixture 的 postcommit runtime mismatch 已保留为维护历史。实际 API/Web 发布已完成，API health=200/UP、Web=200、MySQL ping 成功；以真实上线可用性验收替代旧夹具复跑，不重启或改动生产服务。 |
| `JVC-API` | accepted | `492adc7e8ff3` / `ef888807fb3b` | Accepted exact API tree is now fast-forwarded to origin/develop at 492adc7e8ff386013264c4eef4c0bf67adf34add. Evidence remains voice suite 48/0/0/0 plus ChatControllerTest 9/0/0/0 and review ACCEPT 0/0/0. No deployment/provider activation. |
| `JVC-WEB` | accepted | `97c2f8bd439d` / `162fc64e5d8a` | Accepted exact Web tree is now fast-forwarded to origin/develop at 97c2f8bd439dc6f7876a4d26c91d485ea7750cda. Authoritative evidence remains 23 voice tests, production build, and review ACCEPT 0/0/0; disclosed baseline/harness debt remains non-blocking. No deployment. |
| `JVC-INT` | accepted | `c9b2318140a2` / `8d194c684562` | Reviewed merge ACCEPT 0/0/0 is now pushed to origin/codex/juyiting-voice-conversation-integration and fast-forwarded to origin/master at c9b2318140a2142cff7bc312ec995c6f6b1af14a; sddw verify passes and gitlinks pin the accepted API/Web commits. Production deployment and Provider activation remain unauthorized; disclosed baseline UI regression harness gap remains non-blocking/open. |
| `JVC-OAI` | accepted | `92c5ec3ffb89` / `fa067814f123` | ACCEPT 0/0/0 on 92c5ec3f/tree fa067814; Voice 81/81 key 0928aee5 and Chat 9/9 key 17cb84fc sealed. Atomic non-force push promoted exact candidate to origin/develop and origin/feat/juyiting-openai-voice-provider from remote base 492adc7e. Local develop dc039b34 auth fix untouched and must be retained in release integration. No production activation. |
| `PROD-API-RECOVERY-502` | done | `13471b08617c` / `cc76c5a8eae3` | 502 恢复完成：当前 API 进程存活，127.0.0.1:10018/actuator/health 返回 200/UP，公网 Web 返回 200，MySQL ping 成功。若出现新异常，作为新线上缺陷单独归因。 |
| `ECO-V0-W01` | accepted | `未绑定` / `未绑定` | V0 preview contract frozen at specs/agent-economy-marketplace/v0-plan.md sha256=fafa497c307a48df94d81e00eb912053bc9ed58ca9fe66a11af78c3002a5d37f; frozen production bundle manifest remains c5c5a715d027c87e74617b07c0a2ee3cb33c9d71cd69db7f95b80775f74a735c. Proceed with W02. |
| `ECO-V0-W02` | accepted | `70ec1dfb1fb7` / `354f06b70be2` | Independent sol_reviewer 01a07051-2528-7c23-9a12-e64ea94365c6 ACCEPT P0/P1/P2=0/0/0 on 70ec1dfb/tree 354f06b7. No-DB 8ad6088f and MySQL c75ef1fc PASS; MySQL 11/0/0/0 including 100 requests; temporary users/databases zero. Promote W03 wallet/ledger/preview issuance implementation; no deployment yet. |
| `ECO-V0-W03` | accepted | `97df61a13616` / `1ec7d890b0dc` | W03 ACCEPT on97df61a1/tree1ec7d890: independent source0/0/0 plus34 tests PASS incl dev/grey/prod JWT chains; evidence538f3342. Unlock W04 and requested R01 paid rent. No deployment or live charging. |
| `ECO-V0-W04` | awaiting_verifier | `ea1eb579a532` / `fb32f4592b17` | R3 exactea1eb579/treefb32f459 independent sourceACCEPT0/0/0; prior source/provider exceptions resolved, historical matrices retained in W04 handoffs. Runtime gate pending. W05 owner now integrates corrected source parent in separate claim-r2 worktree; plan focused combined verification after its review, no duplicate full suite or deploy. |
| `ECO-V0-W05` | waiting_dependency | `fbee63956118` / `dcef936f4c8a` | OriginalW05owner nowW06 has expanded combinedsource scope for4fullreviewfindings in eco-v0-bounty-settlement; originalfbee6395 frozen/rejected. Await cleancombinedcandidate then separate W05/W06reviewpromotion. Preparedrun-w05-r2-nodb.shNOTGO; W09mustnotrepairsharedfunding concurrently. |
| `ECO-V0-W06` | implementing | `fbee63956118` / `dcef936f4c8a` | W06sourceowner continues isolatedsettlement plus4inheritedW05fullreview corrections perW05R3matrix, oneactivelease. Minimal sharedposting CAPTURE_COMPUTE/FEE/PAY_AGENT and partialcapture continuation ownedW06, coordinate W09primitive needs/paths. No runtime/source promotion; cleancombinedcandidate then independentreviews. |
| `ECO-V0-W07` | verifying | `d56e205c558f` / `0a6b87991f20` | Bounded d56e205c independentSOURCEACCEPT0/0/0 recorded; GO only run-w07-r3-lifecycle-nodb.sh six new mock lifecycle cases on exacttree0a6b8799. No MySQL GO: old wrapper unsafe, main preparing retention/session-zero cleanup gate. No repair/blindretry/processcontrol, preserve prior evidence scopes. |
| `ECO-V0-W08` | review | `086a9ddea30c` / `1426b81cccb0` | Independent W08 source review on086a9dde/tree1426b81c,14additive seed/package paths vs production-source-acceptedW07b4614bd. Exact6prices/admin/defaultoff/scope/deterministicZIP/digest/drift checks; noDB/runtime/seeding/repairs. Unblock W09 promotion source dependency without duplicate schema review. |
| `ECO-V0-W09` | claimed | `086a9ddea30c` / `1426b81cccb0` | Original rental critical owner handed offR01, now exclusive W09 source owner in NEW eco-v0-skill-purchase. Merge immutableR01aa81221b to preserve shared guards; implement exact-scope capabilities, durable Agent CAS, purchase/package/install-result/activation/refund with tests. Frozen W05 integration later; no runtime/DB/other-tree writes. |
| `ECO-V0-W10` | blocked_root_cause | `3b337d22ee4e` / `3302bf9f6bbb` | Stop second-failure loop; original installer owner bounded fixture mode correction and R01 managed-host staging integration in new tree after admission, independentreview then target retry. Reuse exact installer47PASS honestly. |
| `ECO-V0-W11` | waiting_dependency | `c6945cff137f` / `8a096b870bd5` | W11 source defects join W12-owned combined Web remediation packet WEB-R2 in new worktree; no second active lease for same Agent. Preserve original candidate. After combined clean corrected commit, independent review/test evidence promotes W11 and W12 separately; W12 owner includes minimal W11 integration paths. |
| `ECO-V0-W12` | source_review | `06875878bd21` / `b6f892934d96` | Clean R4 Web candidate06875878/treeb6f89293: explicit quote confirm/cancel and immutable claim receipt+canonical readback/retry fencing, static-only. Entire combined R2-R4 independent review and focused tests/build pending. Original combined worktree now immutable; no deployment. |
| `ECO-V0-W13` | blocked_dependency | `未绑定` / `未绑定` | Wait for accepted API/Web/Agent candidates plus requested hosting-rent R01/R02/R03 integration evidence, then run targeted combined verification and independent review. Rent scope is specs/agent-economy-marketplace/v0-hosting-rent.md; no automatic real charging before price/period configuration. |
| `ECO-V0-W14` | blocked_dependency | `未绑定` / `未绑定` | Wait for accepted candidates, then deploy development preview and smoke test. |
| `JVC-OAI-WEB` | accepted | `ce45b898cd19` / `25cdcab21e71` | Independent review ACCEPT 0/0/0; 23/23 exact voice tests and production build pass. Exact commit is fast-forwarded to origin/develop. No production deployment or voice flag activation until API/provider and host-security gates pass. |
| `JVC-OAI-OPS` | deferred | `fff17bf91930` / `5a8a6d66ecfe` | Legacy /opt/cyf/api+cyfapi/current.jar packet is not deployable on canonical host; no more namespace retries or full131 claims. Preserve R19/R20 unexplained checkpoint failures and accepted staged proof. JVC-OAI-HOST-ADAPT replaces deployment path only after independent new-host coverage review/verification and final release guard; not a waiver of security gates. |
| `OPS-API-UNIFIED-ENTRY` | accepted | `未绑定` / `未绑定` | Unified /home/isp/bin/cyf_api_kit.sh installed; fresh independent Reviewer 01a07006-452e-7162-931a-751817e8d3cc ACCEPT 0/0/0. Exact unified SHA256 c84e6202dc4ef6c60ae66b3315f49012b52ec2ff9d7280683b01d87cf3b18e1b; canonical SHA256 56537824cd33f6333f199ea1cebda90b127b39c079e08daad6d164607f788ef5. Evidence /tmp/cyf-api-unify-verify-oyn0sywi/review-accept.json; 59 applicable checks PASS (48 unchanged reused +11 fresh). Next: isp may run /home/isp/bin/cyf_api_kit.sh status; production OOM recovery remains separate, controller alert already sent. No live restart/build/deploy performed. |
| `OPS-JUYITING-HEALTHMON` | accepted | `94f95f7e5a84` / `635ea853863d` | Fresh Leibniz3 ACCEPT0/0/0 exact94f95f7e/635ea853; focused45/45+syntax PASS; /tmp/ops-healthmon-r3-authoritative-accept-20260905.txt. Source closed; installation/cron/real mail not yet delivered, next independent runtime activation with maintenance until Peirce releases startup. |
| `OPS-API-RECOVERY-HEALTHMON` | done | `未绑定` / `未绑定` | Runtime owner completed one accepted canonical start naturally rc0, PID611386 cyf-api(987:1000), start2026-09-05 13:49:21+08, ready454s, HEALTH=UP and ARTIFACT_ATTESTATION=MATCH. Own evidence /tmp/ops-api-recovery-healthmon.dd7YCb. Verifier slot released; no retry/source deployment. Next admit existing monitor reviewer. |
| `ECO-V0-R01` | source_review | `aa81221be06e` / `5d4d87fe8864` | R4 clean APIaa81221b/tree5d4d87fe and companion Agentaf40adbe/tree21aaef68 committed: concrete private readiness adapter and durable free reprovision. Full R3-R4 independent review/compile/runtime pending; packaging must add managed-host.mjs on integration. No sockets/services/rent activated. |
| `ECO-V0-R02` | source_review | `53e12c87c03b` / `9b4c58d40863` | Terra capacity recovered once; clean53e12c87 parentWebR406875878: explicit rent quote/confirmation, immutable receipts and canonical lease recovery, paid manual renewal/free reprovision, no server fallback. Static-only. Independent full corrected Web+rental review and focused tests/build pending; no deployment. |
| `ECO-V0-R03` | blocked_dependency | `未绑定` / `未绑定` | After R01/R02 accepted, run targeted rent API/MySQL/Web verification and independent review before combined W13/W14 preview delivery. |
| `JVC-OAI-INTEGRATION-API` | accepted | `34b67fed9606` / `fb42c46c1f63` | ACCEPT: source reviewer01a0707b0/0/0, exact four-suite13/13 evidence4e0b5ebc verified XML hashes and sealed0555/0444. Atomic non-force push promoted origin/develop plus codex/juyiting-voice-release-api from92c5ec3f. Both voice/auth parents retained; local develop untouched. No production deployment/flag activation; next OPS containment and new-host release path gates. |
| `ECO-V0-R00` | accepted | `6623e4c3eebb` / `9db6898cdf0f` | Admission-only R00 ACCEPT: independent source0/0/0 and88 tests PASS on6623e4c3/tree9db6898c; evidence d4e6ba49. Preserve local/no-charge behavior and closed server path. R01 full paid lease remains blocked on W03; no deployment. |
| `O01-LANDSCAPE-HEIGHT` | accepted | `7872fc68a340` / `d89936e967ae` | Fresh authority Godel ACCEPT0/0/0 on7872fc68/d89936e9; focused2/2, build6m19s, CDP20/20 PASS. /tmp/o01-r3-authoritative-accept.txt. Source complete; exact artifact activation authorized separately. |
| `O01-LANDSCAPE-HEIGHT-RELEASE` | deployed_pending_integration | `7872fc68a340` / `d89936e967ae` | DEPLOYED20:08CST7872fc68/d89936e9, manifest827f5fc7; sourceACCEPT0/0/0, focused2/2, CDP20/20, HTTPS42/42; fix branch pushed. Evidence /tmp/o01-landscape-height-release-N4DjKohh. Remaining code promotion: main-controller notified to assign owner for nonforce integration of diverged develop1488e844 with7872fc68 and verify before future deployment. No backend touched, voiceOFF. |
| `JVC-OAI-HOST-ADAPT` | accepted | `9f98694e3949` / `00ae5a9ef66c` | SOURCE0/0/0 + COMPOSED_OFFLINE_COVERAGE_COMPLETE: R10newbuildrc0 and activation/installer/nginxrc0 fullterminalmetadata, R9locks/transactionsPASS reused via independentexactfunction/fixture/productionproof. No R10allrun/claim. HOSTtooling accepted only; finalmerge/Webremaining/runtimehandoff/APIhealth/providerrealproof/releaseguard required beforeproduction. |
| `JVC-OAI-INTEGRATION-WEB` | accepted | `101ac4c6a2b4` / `93c561b90b8d` | Godel independent SOURCE_INTEGRATION ACCEPT0/0/0 on latestdeployed101ac4c/tree93c561: voice/depsbyteexact, ancestor6d88, neworientation/onboarding retains recording locks and cleanup. No repeatedforeignreview/test/evidence access. Own currenttreevoicecheck+enabledbuild remains separate artifact gate. |
| `JVC-OAI-ARTIFACT-API` | accepted | `34b67fed9606` / `fb42c46c1f63` | Original orchestrated bootJar rc0 179tasks(1executed/178uptodate), cache4e635e02;217605642-byte immutable JAR SHAfa808e633e985551e66168b1d70c488d8cf01361662f630e9f48ccab265038d5 sealed with full log+metadata. Accepted34b/treefb42 clean, nested voice classes present. No rebuild/tests; NOT_DEPLOYED, host R2 review+offline+release gates pending. |
| `JVC-OAI-ARTIFACT-WEB` | accepted | `101ac4c6a2b4` / `93c561b90b8d` | Latestaccepted/deployed101ac/93c561 voice23PASS+oneenabledbuildrc0; ownworktreeclean. Finalartifact2ffaf4b427dec3304d98225231a45917bf020b96ffd3dd381cc7e7be8478fe04 102796425bytes0444nlink1; mainexactarchive403files/manifest/voicebundle proofPASS. Oldinvalidpackagingshistorical, nobuildrerun. Notdeployed; APIhealth/runtimehandoff/provider/Webremaining/finalguard stillrequired. |
| `JVC-OAI-WEB-DEPLOY-ADAPT` | accepted | `3af2426a6c5e` / `6db336401dd8` | COMPOSED_OFFLINE_COVERAGE_COMPLETE accepted independently Godel0/0/0: R3 actual36PASS plus R5 primitive1/guard13/deploy26/rollback18 PASS, originalcollector38194 naturalterminal. Rollbackcache2f18b2423350229c82c58ebfe675d6e81c7024a2bc141cb085baab5f4bbfb410. FinalR6c408/2225 currentpin mapping accepted; never newtreeall/fullentrymutationPASS; oldUNKNOWN retained in evidence. NOT_DEPLOYED. See CONTINUATION-R4-CLOSEOUT.md; originalAPIrecoverycontroller must supply actualterminal/runtimehandoff/currenthealthybaseline/localconsumerproof before phase1 flags-OFF release GO. |
| `OPS-API-RECOVERY-20260905-1932` | implementing | `未绑定` / `未绑定` | Per explicit main-controller handoff: unique ACTUAL runtime Owner Peirce01a07194 owns existing canonical START bash877327/Java877855 since20:41:45. Await natural outcome, no second start. Knuth3 preflight refusedrc1 and executed0starts; released. This thread coordination-only, no process/lock/evidence operations on Peirce. Main-controller reports health/terminal attribution. |
| `OPS-JUYITING-HEALTHMON-ACTIVATION` | done | `94f95f7e5a84` / `635ea853863d` | Activation complete: monitor installed, explicit notify helper accepted, exact cron active with real paused and post-resume ticks, maintenance false, stored local API UP, no lifecycle action. Continue ordinary observation; do not claim inbox delivery. |
| `JY-BUG-SCREEN-20260905` | accepted | `a4bc9b0a1e57` / `cbe846b46e74` | Independent Leibniz ACCEPT0/0/0 screenR2, replaybothshells/focus+desktopno-op closed native preserved.49intended unitcases passed, broadlegacycomponent/O03 not accepted; actualbrowsercycles pending integratedrelease verifier. SourceOwner released no deployment yet. |
| `JY-BUG-READER-20260905` | accepted | `bf718343e068` / `b4de556921b0` | IndependentLeibnizACCEPT0/0/0 onbf718/b4de5569 with55/55evidence; bookmark/note/draft/progress retryidentityfences closed. Exactreaderblobs included inf850/fe716. SourceOwnerreleased; productionbuild/staticpreviewrunning, no deployment yet. |
| `JY-BUG-RELEASE-20260905` | done | `101ac4c6a2b4` / `93c561b90b8d` | DEPLOYED and pushedorigin/develop101ac4c: authentic57screen+55readerPASS, productionbuildPASS, independentsourceACCEPT0/0/0, all403deployedfilesexactdigest63f535b7, publicindex+JuyichunkHTTPS200byteexact. NoAPI/foreignprocess/main-dirtycheckoutchanges. Nextaction: refresh/reenterWeChat and manuallycycle3times+close/reopenreading; realdevice/browsercyclesunverified, no falsePASS. |
| `JVC-OAI-WEB-CURRENT-PINS` | accepted | `c40805e6d6e9` / `2225ea172ad6` | GodelpinSOURCE0/0/0 accepted7c631/257855; exactR6c408/2225 union HOST9f986+pin7c631 correct17paths/parents/common/test/currentartifactpins cleanPASS. Coordinatorinvalidgateattributed(no source/runtimewrites), no remerge. R5fixtureevidence onlyreuseeligible untilactualterminalPASS; no newtreeall or oldproductionguard reuse. NOT_DEPLOYED. |
| `JY-FOLLOWUP-SCREEN-20260906` | remediating | `21a44c79c873` / `ad1c596a6443` | Run one known30sec tsx baseline selector + changed component file with logs/sourceSHA/exit; source review continues independent; no source edits without reviewer handoff |
| `JY-FOLLOWUP-READER-20260906` | implementing | `101ac4c6a2b4` / `93c561b90b8d` | CORS exact5line patch independently ACCEPT and production applied: nginx-t/reloadPASS, legitimate OPTIONS200 includeskey singleallowheaders; untrusted403noAllowOrigin. Main evidence0whiSH. NoAPIrestart/authenticatedsaveclaim. Owner complete realadaptertest. |
| `JY-FOLLOWUP-VERIFY-20260906` | remediating | `101ac4c6a2b4` / `93c561b90b8d` | Bounded new attempt authorized: local exact baseline dist preview + pre-start fake auth/intercepted API, sequential CDP no recursive queue; 3 real canvas cycles. Then integrated build only when notified. |
| `JVC-OAI-API-PACKAGE-R6` | targeted_verification | `c40805e6d6e9` / `2225ea172ad6` | Terra fallback for unavailable Mini verifier, artifact-only not product-source Writer. Prepare unexecuted collector first, main independent review before execution. Contract JVC-OAI-API-PACKAGE-R6-CONTRACT.md; original accepted JAR/cache, no Gradle/build/production. Stop on any further failure, threshold2 applies. |

## 全部原始规划任务（82 项，运行记录优先）

| ID | 原始需求 | 原始定义状态 | 本次有效口径 |
| --- | --- | --- | --- |
| `A01` | 定义稳定 Agent ID 规则和历史映射 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `A02` | 实现身份注册/alias Schema 与历史检测修复 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `A03` | 拆分 chat、command、progress、result 协议 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `A04` | WebSocket 按 tenant/client/task/target 过滤 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `A05` | Agent 客户端持久 Inbox/队列 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `A06` | Agent commandId/ACK/幂等协议 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `A07` | 编码 Agent 独立 worktree 管理脚本 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `A08` | 补齐稳定身份签发、解析与运行时授权 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `B01` | 新增 member/work item/request/artifact 表 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `B02` | 新增 Entity/DAO/DTO/Mapper | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `B03` | 实现任务与成员状态机 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `B04` | 实现 work item claim/lease/heartbeat | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `B05` | 实现任务聚合状态计算 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `B06` | 实现诉求和成果服务 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `B07` | 建立 task-thread 与共享会话 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `B08` | 改造旧 assign/report 兼容层 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `B09` | 历史任务成员/工作项回填 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `M2-00` | M2 基线收敛与安全启动门禁 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C01` | 新增 task event 表和版本分配 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `C01B` | 接入全部协作业务写路径的状态 + task event 原子写入 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `C01H` | 建立 B09 历史任务 event baseline 与幂等迁移 | integrated | 仅历史 integrated；无当前部署/激活证明 |
| `C02` | 实现 TaskEventBroker 和 after-commit 唤醒 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C03` | 实现历史 replay、连续性检查、resync | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C04` | 实现 workspace snapshot API | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C05` | 实现 task events SSE API | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C05F` | 实现 M2 后端 feature flag 与默认关闭策略 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C06` | 实现前端 useTaskEventStream | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C07A` | 接入 TaskWorkspace 数据、连接状态和恢复状态 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C07B` | 实现 TaskWorkspace/Timeline 纯展示 UI | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C07C` | 完成 TaskWorkspace 响应式、可访问性和组件测试 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C07` | TaskWorkspace/Timeline 前端集成门禁 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C07F` | 实现 M2 前端 feature flag 与安全降级入口 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C08A` | M2 API 累计基线集成与回归门禁 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C08W` | M2 Web 累计基线集成与回归门禁 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C08` | M2 部署候选最终 GO/NO-GO | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C09A` | M2 API develop successor 收敛 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C09W` | M2 Web develop successor 收敛与回归门禁 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `C09` | M2 develop 合流总门禁与 root pin 准备 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `M3-00` | M3 基线、离线 Rabbit 隔离与启动状态门禁 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `D01` | 新增 outbox/inbox/delivery 表 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `D02` | 业务事务写 task event + delivery + outbox | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `D03` | 实现 Outbox Relay | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `D04` | 配置 RabbitMQ exchange/queue/retry/DLQ | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `D05` | 实现 Rabbit command consumer + WS dispatcher | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `D06` | 实现 WAITING_AGENT 和重连补投 | accepted | accepted（当前运行快照） |
| `D07` | 实现服务端 Inbox 幂等 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `D08` | 替换 HallActionDispatcher 内存 mailbox | draft | accepted（当前运行快照） |
| `D09` | Rabbit 运维指标、DLQ 查询和重放工具 | draft | accepted（当前运行快照） |
| `E01` | 统一候选硬约束和评分 | draft | 仅历史 draft；无当前部署/激活证明 |
| `E02` | 实现多 Agent 贪心组队算法 | draft | 仅历史 draft；无当前部署/激活证明 |
| `E03` | 实现自动拆解工作项接口和人工确认 | draft | 仅历史 draft；无当前部署/激活证明 |
| `E04` | 实现依赖解析和 ready 调度 | draft | 仅历史 draft；无当前部署/激活证明 |
| `E05` | 实现超时、失败和重派策略 | draft | 仅历史 draft；无当前部署/激活证明 |
| `E06` | 实现自主等级和风险策略 | draft | 仅历史 draft；无当前部署/激活证明 |
| `E07` | 实现前端团队推荐/确认/解释 UI | draft | 仅历史 draft；无当前部署/激活证明 |
| `E08` | 实现前端工作项看板与协作操作 | draft | 仅历史 draft；无当前部署/激活证明 |
| `F01` | 实现 Context Pack 生成器 | draft | 仅历史 draft；无当前部署/激活证明 |
| `F02` | 实现 artifact 文件存储和 hash 策略 | draft | 仅历史 draft；无当前部署/激活证明 |
| `F03` | 修复 Elasticsearch 服务和 prod 配置 | draft | 仅历史 draft；无当前部署/激活证明 |
| `F04` | 实现任务级 ACL 语义索引 | draft | 仅历史 draft；无当前部署/激活证明 |
| `F05` | 实现派生索引重试和全量重建工具 | draft | 仅历史 draft；无当前部署/激活证明 |
| `F06` | 实现成果冲突、accepted/superseded 标记 | draft | 仅历史 draft；无当前部署/激活证明 |
| `G01` | 建设后端状态机/ACL/幂等测试套件 | draft | 仅历史 draft；无当前部署/激活证明 |
| `G02` | 建设 Rabbit 故障注入和恢复测试 | draft | 仅历史 draft；无当前部署/激活证明 |
| `G03` | 建设前端协作流测试 | draft | 仅历史 draft；无当前部署/激活证明 |
| `G04` | 建设 E2E 多 Agent 场景 | draft | 仅历史 draft；无当前部署/激活证明 |
| `G05` | 实现灰度 feature flags 和回退开关 | draft | 仅历史 draft；无当前部署/激活证明 |
| `G06` | 编写数据迁移执行手册 | draft | 仅历史 draft；无当前部署/激活证明 |
| `G07` | 建设 Dashboard 和告警 | draft | 仅历史 draft；无当前部署/激活证明 |
| `G08` | 安全审计和容量压测 | draft | 仅历史 draft；无当前部署/激活证明 |
| `H01` | 冻结案卷阁阅读契约与120回内容包 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `H02` | 实现案卷阁正文schema、确定性导入与catalog API | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `H03` | 实现阅读进度、书签和私人手札 exact-scope API | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `H04` | 实现案卷阁完整阅读垂直切片 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `H05A` | 实现选文问案卷书吏后端与持久恢复 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `H05W` | 实现选文问案卷书吏前端与断线恢复 | accepted | 仅历史 accepted；无当前部署/激活证明 |
| `H06` | 案卷阁阅读MVP集成与发布门禁 | in_progress | done（当前运行快照） |
| `O00` | 聚义厅横竖屏 Web 高风险收敛基线 | review | accepted（当前运行快照） |
| `O01` | 唯一体验模式与真实方向请求 | blocked_dependency | accepted（当前运行快照） |
| `O02` | 竖屏轻应用首页 | blocked_dependency | accepted（当前运行快照） |
| `O03` | 地图 destroy/remount、camera 恢复与目标聚焦 | blocked_dependency | accepted（当前运行快照） |
| `O04` | Panel 状态、可访问性与横竖屏集成门禁 | blocked_dependency | accepted（当前运行快照） |

## 未映射到独立功能 SDD 的运维事项

OPS 资源遥测、统一启动入口、监控、API 恢复由上方全部运行任务与归档包追踪；不虚构新的业务需求。磁盘清理脚本修改不在本次运行快照中，不能据上一轮讨论认定已验收归档，后续需实际脚本与执行结果。

## 版本与核验限制

源 ledger SHA-256 `e90988c19a0b2ec0aa24834d9e143fa3e17ac63b89648fbe8f7aba160db66705`；root HEAD `8b6bcbab4a8146c1502447a8bd5e28c22892a559`。root 索引 pin：

```text
160000 c4d8aebd77b122100e562576e40a158c26c1dff4 0	api
160000 0ac7ea756ad59c91c1110e3d635846a4c665ece6 0	web
```

保留原 gitlink，未运行 sddw pin，不制造新交付基线。历史 feature 的 pin 与本地旧 checkout 不同，sddw verify 不能用当前工作树替代历史版本验证。健康检查仅使用前次 09:10 观察 API200/UP、Web200 作上下文，不作本次逐功能验收。

## 里程碑口径差异（本次显式披露）

历史 `TASKS.yaml.tasks` 将 F03/F04/F05 标为 M4，而 `MASTER_PLAN.md` 里程碑表将知识检索 F03–F05 归 M5。不可修改只读快照来掩盖这个差异。本轮 SDD 展示采用主计划的产品阶段口径：M4=E01–E08、F01/F02/F06；M5=F03–F05、G01–G08；执行依赖和任务身份始终以 exact task_id 为准。该展示裁决不变更台账归属、依赖、Owner 或完成状态，F03–F05 仍未完成；历史元数据统一留给后续独立控制面维护。
