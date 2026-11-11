# ECO source delivery to develop integration — 2026-09-07

This is a source/evidence handoff, not a second execution ledger or runtime authorization. The Voice integration controller may read the three source worktrees/Git objects below and this public handoff to integrate in its own worktree. Private original logs/XML/evidence directories are not included in this sharing grant. Do not modify the frozen source worktrees or dirty main checkouts.

## Complete source candidates

| Repository | Source worktree (relative to CYF root) | Commit | Tree |
|---|---|---|---|
| API | `.worktrees/eco-v0-api-release-r1` | `8a9875859776d2e67954f0d04e60255b37c9dac8` | `f800243a93668da2ad9135535c00f441353f470b` |
| Web | `.worktrees/eco-v0-web-closure-r8` | `38cf586e7f866671e745bb493eabb4c4c4a273c1` | `c66750ef692cd3744f718c390afdf96fab2789a0` |
| Agent (existing isp-install repository) | `.worktrees/eco-v0-agent-integrated` | `4bd0c257abe9a767f8398e5d4474395161cb9364` | `7600bc8a53fd04b529895fbcf81eb42bde602d34` |

API and Web clean at the latest September 7 read-only check. API parent is `fed01982176b4edfc093099e22b69da833f9bda8`. API ancestry was verified for all completed ledger API slices: W02 `70ec1dfb1fb7c613a66441dd8b046e17eeaf0920`, W03 `97df61a1361645d23096de28d822494a24b5242d`, W04 `ea1eb579a5329f563bc97ba143c16c855cea2875`, W05 `01037b00b2b35896915948e5f8d8346f8f525102`, W06 historical test pin `3a0f05f40df3a0c6235536584700affeb3747561`, W07 `d56e205c558fb2370c80921ce9ca4e9d2aea07a7`, W08 `6619aae27fd8a31c9ea1dec429a738236ea8a252`, R00 `6623e4c3eebbb64f51f2d2af195ce2425e7bccb9`, R01 `d875ccfa0ba31187a29362f7ac454832af3e0e25`, baseline `34b67fed96061bf9c3132106ca219fc6f5f6ba05`, and W06 correction `fb2c7733c003b306e419120e7d78c23d9551183b`. W09 is the final candidate itself. No known completed ECO API slice is missing. W01 is a root-repository contract, not an API commit. Other threads' newer work must still be retained during integration.

Included: wallet/ledger/test issuance; bounty escrow/token quote/explicit-agent claim/settlement/refund; six skill products/purchase/install receipt/activation; hosting rent quote/renewal/expiry admission/managed provisioning/compensation and exact managed-key disable. Agent delivery is separate from API and must not be omitted; `/home/isp/apps/codex-ws-agent/` remains a deployment copy, not a new repository.

## Evidence boundaries and known defects

- API final source independently accepted, **no tests run on final 8a987**. Latest actual R3 run was on `3a0f05/479e9`: 149 tests, 117 pass, 32 fail, 0 error, 0 skipped. Quote/settlement account for 19 failures with the original SQL cause still unknown. Final source retains the original cause for the next diagnostic; it does not establish a fix. Skill fixture accounts for 13 failures; SQL parser and H2 audit-trigger fixes are source-reviewed but unexecuted. Downstream chat/economy/oauth selectors did not execute.
- API minimum next probes: `FundedBountyQuoteClaimServiceTest.quoteInsertIntegrityFailureWithoutCollisionKeepsPublicConflictAndRetainsCause`, `FundedBountyQuoteClaimRealTransactionTest.productionSpringConstructorCreatesRealQuoteClaimBean`, `SkillMarketplaceRealTransactionTest.paidPurchaseInstallsCapturesAndReplaysOriginalReceipt`, and `SkillMarketplaceRealTransactionTest.operationAuditRowsRejectUpdateAndDeleteAndRemainUnchanged`. Use a new exact-tree wrapper, never the old R3 wrapper.
- Web final source accepted, but the focused run hung with zero-byte final reports for over 100 minutes and was stopped by its exact owner. **No final-tree testcase totals or build PASS exist.** Do not rerun the unchanged 11-file wrapper: bounded groups, incremental progress and an outer deadline are required first. Previous dependency loan is RELEASED; existing facade links confer no renewed permission.
- Agent final scoped verification: installer92 + packaging9 + client/managed-host83 = 184 PASS; independent source acceptance. This is not deployed evidence.
- Real MySQL coverage remains incomplete for funding, quote, settlement, skill application and hosting rent schema initializer classes, plus the unexecuted skill fixture lifecycle noDB class. W02 fixture unknown-CREATE cleanup requires reviewed containment before reuse. Do not point an old wrapper at canonical DB by default.

## Integration and activation risks

Preserve additive schema drift checks, actor/scope/ownership, immutable ledger, idempotency/CAS, UNKNOWN funds retention, and refund plus exact managed-key disable in one transaction. Do not weaken constraints to make tests pass. Real DB migration and integrated rent acceptance remain unverified.

`economy.preview.enabled=false` and `economy.preview.test-issuance-enabled=false` remain default in dev/grey/prod; retain default-off rental switches. Test issuance rejects prod/production explicitly. A flags-off artifact release is not an enabled economy preview. Do not switch canonical to dev to bypass this guard. Development defaults share DB/Redis/Rabbit/OAuth/Agent paths and cannot be reused unchanged for an isolated preview.

1 SILVER = 1,000,000 micro-silver, decimal-string amounts; reference 100 SILVER = 1 CNY, not one SILVER per token. Current preview token pricing is synthetic, not a provider invoice. Skills: repo-inspector0, code-reviewer20, repo-test30, code-editor50, web-builder60, deploy-runner100 (admin-only). Hosting: 1000 SILVER/Agent/fixed30days, manual renewal, local free, no automatic deduction or historical collection; free reprovision does not extend rent.

ECO has not pushed/deployed these candidates or enabled charging. Voice's new source integration authorization does not grant ECO canonical service/DB/process custody. Keep source merge, artifact build, deployment, activation, and authenticated functional smoke as separate facts; a request to defer bugs must not relabel failures as PASS.

## Existing public evidence

- `ECO-V0-API-RELEASE-INTEGRATION-R1.md`: prior exact merge/source inheritance proof.
- `ECO-V0-API-R3-NODB-RESULT.md`: actual API failure matrix and diagnostic boundary.
- `ECO-V0-R03-REMAINING-SELECTORS.md`: remaining DB/noDB selectors.
- `ECO-V0-WEB-R11-TIMEOUT-ROOT-CAUSE.md`: Web timeout and bounded remediation plan.
- `ECO-V0-W14-RELEASE-PREPARATION.md`: configuration/deployment isolation gaps.
- `../../../specs/agent-economy-marketplace/v0-api-contract.md`, `v0-hosting-http-contract.md`, `v0-hosting-rent.md`: frozen contracts.

## Subsequent Web integration receipt — source only

External sole Web integrator delivered `/home/isp/wsps/cyf/.worktrees/release-all-web-20260907-sol-a2ad80a2`, commit `dcfbc93814e1d5287ab779cb1b5ab1a2d06999c9`, tree `436883f4066c0bff94469112294aefd4d12f2770`. ECO main independently checked HEAD/tree, clean status and original ECO `38cf586e7f866671e745bb493eabb4c4c4a273c1` ancestry. The integrator reports fresh562ef, LIVE8bf22 and R02 53e12 also retained, and manual conflicts only in `src/components/juyiting/HallPortraitHome.vue`, `tests/juyiting-portrait-home.test.js`, and `src/router/index.js`; these remain for the release controller's independent delta review, not an ECO acceptance claim.

Static checks are reported by the integrator only. No final build/push/deployment is claimed. Remaining external release steps: independent conflict-delta review, legitimate dependency access, one exact final-tree build and actual deployment/smoke receipt. Original ECO test pins and failures remain unchanged; integration ancestry is not full functional verification.
