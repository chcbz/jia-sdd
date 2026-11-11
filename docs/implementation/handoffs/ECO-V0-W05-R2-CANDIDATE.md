# W05 corrected integration candidate — 2026-09-06

Immutable `eco-v0-bounty-claim-r2`: `fbee6395611837f3f6a08f4b32d762fa65c96037` / tree `dcef936f4c8a0d5350a06e511fd94ec2ecc77850`, parent `76b2924bf293ab44feb13679011afb3eabe94cba`.

Merge parent `76b2924b` / tree `fb749bf53bab4b107690f4cd0368310476874057` combines original W05 `acc555a2` and source-accepted W04 R3 `ea1eb579`. Writer reports byte-exact 14 W04-only + 27 W05-only paths and conflict-free automatic shared digest/legacy-guard merge (automatic tree `4a2557a4e329e0251f39385491ef1ad98336aa1f`), plus two claim transaction-fixture source paths. Genuine claim/replay/outer commit wakeup/late rollback/explicit competing Agents/surrogate rejection tests authored, not run. Rabbit and delivery disabled: these fixtures do not prove enabled outbox delivery.

Final five-path correction adds explicit nonnull claimed/completed state fields to quote/claim DDL, exact CHECK expression and ENFORCED catalog validation, SQL UNKNOWN adversarial regressions and old-catalog rejection. Legal OPEN/POSTING nulls preserved; DTO unchanged. Static checks only. Full W05 independent review (not just last delta) plus focused W04/W05 runtime still required.

Fixtures SHA256:
- W05 DDL `72f489db5f3560ddc15b8b0a42e1ed30c2cefaba9bd3d84636129eb3953f2d8f`.
- W04 H2 `9a4815f9acfa5df230e9c73251136f446434fbbfae6adcbc543a801f6f6dc644` unchanged.
- W05 H2 `f6e4d403c32d335d6d14876a0b2a34331c8b0e6d294272b26fa61048ec9b3d89` unchanged.
- W05 MySQL test source `6aa53fdac1b787fcf33772b4055e2d64ec9199c41bf178228ea16b43b0524b62`.

Preserve source evidence; downstream W06 and W09 may consume the frozen interface in separate source trees. No promotion, deployment, or charge implied.
