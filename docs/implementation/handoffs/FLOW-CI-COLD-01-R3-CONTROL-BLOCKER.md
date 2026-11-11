# R3 source accepted; cloud configuration blocked before Run3

## Completed, not deployment acceptance

- User chose existing new5256653/cyf-api-kit-ci; no third pipeline, old1466118/4403172 unchanged.
- Original Owner755537fc1113c7d329ddf1d16df63c1e58cf977b / tree21acb3b52351da54cafa28eea08ddc9fe2955f2d, independent Raman SOURCE ACCEPT0/0/0 and inherited verifier20PASS/native0. Exact source integration recorded in ../plans/FLOW-CI-20260909-integration-r3.json. No actual local Gradle/npm/DB build.
- Existing private OpenCV authenticated full GET722802bytes, SHA323d40119548134b0966d3735e97a78d1edbc79bd91e7fb1074e5152392095f4. Credentials used only in memory. Cloud runner now pins actual resolved artifact before consumption, sanitizes output/XML and rejects secret-bearing JAR exports.
- Dedicated group44254/cyf-flow-ci-maven-auth-5256653 created once; CYF_MAVEN_USERNAME/PASSWORD both encrypted. API Get/List confirms it exists, relatedPipelines remains empty. No secret persisted in code/YAML/ticket/evidence.

## Actual configuration failure — not a third Gradle failure

Approved exact R3 YAML c6f945707afb9f267d5d77c5b88c23e63c3d69dec534829620e9e0f22303f188, ticket1960965f99c78e47e373415df9b3400f8f9a499cc3998b8397a464494ef19190. Single UpdatePipeline rejected400/error1209300: variableGroups:["44254"]不存在, request01A086EF-27AC-57D1-9D4E-A90F8696E439.

Authenticated readback at2026-09-09T16:12:04Z remains oldR2 flowSHA34a83dddf7c29810f0c27e2990841fac50e734a6eb43f878aa0ea6a4d56913d1; only EOF CR/LF normalized comparison confirms oldR2, notR3. No StartPipelineRun called. The one-write approval is consumed; no retry, alternate quoting/name, re-created group, plaintext variable, or speculative association permitted.

| Evidence | Observation | Limit |
|---|---|---|
| Authenticated legacy2021 API Create/Get/List | numeric id44254, encrypted two vars, correct org | no business/reference identifier exposed even before SDK cast |
| Official variables YAML documentation | pipeline-level variableGroups:[IDs] supported | does not establish old numeric id maps to current YAML reference |
| Official common-variable-group UI documentation | variable group ID can be filled/default generated | possible identifier namespace mismatch; not proven root cause |
| Actual UpdatePipeline validation/readback | resolver rejects44254; no config change | not source/Gradle regression or new cloud build attempt |

Current official developer reference separately labels2021 API as legacy/not recommended and offers new token-based API reference. No new token obtained/requested in chat; never ask for secret values here.

## Next bounded action

User can log in to Flow, locate cyf-flow-ci-maven-auth-5256653 under common variable groups and provide only the console-displayed variable-group ID (or a redacted screenshot); if absent, report that. Do not run the pipeline or copy any secret. Alternatively server support can investigate the recorded requestID.

Once the true mapping is established, prepare a diagnosed control-only delta and separate independent review. Reuse accepted source20PASS; no source rebuild. Ticket expires2026-09-09T19:05:28Z and has never run; any later attempt must use fresh nonce/TTL/payload with new review. Preserve the two historical failed cloud runs and this separate control failure.

## R3b identifier correction resolved (authenticated2026-09-09T16:44Z)

User supplied console group reference `q37x7n8snxqq744z`. Independent control delta ACCEPT; one corrected update succeeded request01A0870D-4E75-5E45-A1C8-1E4A4CB551EE. Exact EOF-normalized R3b readback matched; GetVariableGroup44254 still encrypted2 and now relatedPipelines=[5256653], proving the reference-to-numeric mapping in this case. No group recreation or secret transfer.

New config12a834a6415fb214c2c0f8384818fd592f23985394e0bc9b65b0657f9bab87ab / ticket04fb38e1d81ade959f2e0dc8b9f3464d16a51805064c2dc84548e3098528d22f, source tools unchanged. One manual Run3 successfully started2026-09-09T16:47:46Z, request01A08711-7CA6-5149-89ED-AB88EA1074E5, job512076522. Build result pending; no deployment. Prior rejected numeric-reference attempt retained, no longer waiting for user identifier.

Run3最终结果已核验：nativeGradle0/72PASS，制品扫描bridge70导致整体FAIL，无交付JAR；详见`FLOW-CI-COLD-01-R3-RESULT.md`。变量组问题已解决，不再等待用户ID。
