# MMD-U1-INITIAL-OPERATION-20260930 API Owner candidate

Date: 2026-09-30 Asia/Shanghai
Owner/profile: `01a0f0d8-8202-7040-9d9c-becce02f7a3f` / `critical_worker`
Branch/worktree: `codex/juyiting-mmd-initial-operation-v1` / `/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/api-initial-operation-v1`
Base: `8d4ab3f82f7e924e561690e758e85a6a33d8493a` / tree `2693f3e247820042325093a4c703d1073685e1dc`
Candidate: `05ace019fc10cd481928c2b21859554709e448e0` / tree `ac989e116a42bec1c0ebb09bd4ba21902aa831ae`

## Changed paths

- `agent/jia-agent-core/src/main/java/cn/jia/agent/entity/AgentTaskAssignDTO.java`
- `agent/jia-agent-service/src/main/java/cn/jia/agent/service/impl/AgentTaskExecutionGrantServiceImpl.java`
- `agent/jia-agent-service/src/test/java/cn/jia/agent/service/impl/AgentTaskExecutionGrantServiceImplTest.java`

## Implemented contract

- Added optional, exact `initialOperation` to the v2 assign-and-start DTO.
- Explicit selector is accepted only when it is an existing operation enum and an exact member of the complete canonical `requestedOperations` set; no trim, case folding, text classification, or order-derived selection.
- Explicit `GENERATE_IMAGE` or `INSPECT_INPUTS` selects one persisted bootstrap action while the grant retains the full set, including `EDIT_IMAGE` where requested.
- Missing selector preserves the original compatibility rule: exactly one non-`INSPECT_INPUTS` action, or `INSPECT_INPUTS` as the sole action. Ambiguous missing-selector requests fail before assignment mutation.
- Grant and bootstrap remain one root transaction and one outbox. Replay cannot recreate a missing outbox.
- Existing outbox `permitted_operation` is treated as the fixed persisted action. Replay validates payload integrity, exact request-selected action, and membership in the persisted complete grant set; it never re-derives and overwrites the action.
- Same-key selector addition, removal, or value change uses a different request hash and returns the existing idempotency conflict behavior.
- Existing authority behavior is unchanged: no Provider, tools, cost authority, paid authority, or own-derived-assets authority is introduced.

## Request-hash normative form

Canonical values use the existing UTF-8 JSON serialization and canonical operation/input order.

Missing selector, unchanged legacy domain and bytes:

```text
ASSIGN_AND_START\n
{taskId}\n
{canonicalAgent}\n
{expectedTaskVersion}\n
{requirementRevision}\n
{operationsJSON}\n
{inputsJSON}
```

Explicit selector, new domain:

```text
ASSIGN_AND_START_INITIAL_OPERATION_V1\n
{taskId}\n
{canonicalAgent}\n
{expectedTaskVersion}\n
{requirementRevision}\n
{operationsJSON}\n
{inputsJSON}\n
{initialOperation}
```

There is no final newline after the last field in either form.

## Hash fixtures

```text
legacy-generate
preimage bytes: 74
ASSIGN_AND_START\ntask-1\nagent-1\n0\n1\n["GENERATE_IMAGE","INSPECT_INPUTS"]\n[]
sha256=db82df399bed89b72c4bacb5d3e0616d4745fcf1e314bf55e4713f4c9f76e963

legacy-inspect
preimage bytes: 57
ASSIGN_AND_START\ntask-1\nagent-1\n0\n1\n["INSPECT_INPUTS"]\n[]
sha256=37b778f9ffac39db3881ddd585c10dc6f63ba44cf8dc080c744b55c6e555a43f

explicit-generate
preimage bytes: 123
ASSIGN_AND_START_INITIAL_OPERATION_V1\ntask-1\nagent-1\n0\n1\n["EDIT_IMAGE","GENERATE_IMAGE","INSPECT_INPUTS"]\n[]\nGENERATE_IMAGE
sha256=7725b9e4962fab28e928a45052eeade3ee9e89a3d10f63bdb5af6077f56f221d

explicit-inspect
preimage bytes: 123
ASSIGN_AND_START_INITIAL_OPERATION_V1\ntask-1\nagent-1\n0\n1\n["EDIT_IMAGE","GENERATE_IMAGE","INSPECT_INPUTS"]\n[]\nINSPECT_INPUTS
sha256=0a999a29f38b5682654947762bc7a2d620de192e2a75591350142c07af3a3599
```

## Focused verification selectors for Main

- `:agent:jia-agent-service:mmdU1Grant`
- `:agent:jia-agent-service:mmdU1BootstrapOutbox`
- Related finalization regression: `:agent:jia-agent-service:mmdU3Finalization`

The modified test class now contains 24 tests. New cases cover full-set explicit generate, explicit inspect, canonical order replay, legacy hash byte preservation, legacy inspect-only behavior, strict unknown/blank/case/padding rejection, same-key selector value/presence conflicts, rehashed persisted-action drift, missing action, missing/half outbox, grant-set drift, one-outbox replay, and unchanged cost/own-derived authority.

## Static self-check

- `git diff --cached --check` before commit: PASS.
- `git show --check 05ace019`: PASS.
- Exact staged tree matched final tree `ac989e116a42bec1c0ebb09bd4ba21902aa831ae`.
- Allowed-path scan: PASS; no build.gradle, Chat, snapshot, DAO, schema, controller, or read-projection path changed.
- Standalone Lombok `javac` for `AgentTaskAssignDTO` plus `AgentTaskGrantInputDTO`: PASS; generated `getInitialOperation` and `setInitialOperation` confirmed by `javap`.
- Independent Python SHA-256 recomputation of all four fixtures: PASS.
- Worktree clean after commit.
- No Gradle, push, deploy, Provider call, schema change, or production operation was run.

## Residual verification risk

Main/test runner still needs serialized Gradle compilation and focused tests. This candidate intentionally does not implement the disjoint original-operation read projection; its handoff must validate old-domain hashes only for old deterministically selectable sets and new-domain hashes against the persisted outbox action, using the existing assignment-version and assignment-version-minus-one candidates.
