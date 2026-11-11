# OPS-RESOURCE-TELEMETRY R10 Root-Cause Matrix

Date: 2026-08-29

Exact rejected candidate:

- Commit: `9de2030f1d5c48638146aa177427f7c61523da05`
- Tree: `5dd3ed0882f5ed0dfcf62b624267e102d9de7aa8`
- Authoritative reviewer: `01a04cd6-3f7d-7fa3-ae6b-567b256f9f18`
- Verdict: `REJECT P0/P1/P2=0/2/1`

## Failure matrix

| Symptom | Root cause | Required R11 remediation | Required proof |
|---|---|---|---|
| Sixteen consecutive final-active `EEXIST` races exhaust the bounded loop, leave the exact original only under `.recovery-*`, and make immediate same-nonce retry report a missing external record. | `cyf_orchestrator.py:1214-1245` treats retry exhaustion as terminal cleanup instead of completing restoration of the controller-owned original. | Recovery must continue fail-closed until the exact original is restored to active or preserve a retryable controller-owned state that reload recognizes. It must never unlink a foreign replacement. No fixed retry ceiling may strand the original outside active. | Adversarial test wins more than the old retry bound, then releases contention; exact original is active with expected dev/ino/type, `nlink=1`, no recovery/stage/consume residue, foreign objects preserved/quarantined, and immediate same-nonce retry passes. |
| Re-running an already registered evidence key can overwrite artifact/envelope before registry collision rejection, leaving registry SHA values inconsistent with files. | Evidence artifact/envelope publication occurs before registry lock/reservation and collision comparison in `cyf_evidence_envelope.py`. | Reserve/check the key and all destination identities under the registry lock before publication. A duplicate key with non-byte-identical inputs must fail without mutating artifact, envelope, registry, or existing hashes. Identical replay may return the existing immutable record only after byte-exact verification. | Duplicate-key adversarial test snapshots all bytes and hashes, invokes conflicting replay, expects failure, then proves every existing artifact/envelope/registry byte and digest is unchanged and independently revalidates. |
| Residue assertions pass while actual dot-prefixed `.recovery-*` and `.consume-*` files could remain. | Tests use glob patterns beginning `.*.recovery-*` / `.*.consume-*`, which do not match the implementation's `.recovery-*` / `.consume-*` names. | Fix path patterns and assert exact absence/presence semantics for recovery, stage, consume/consumed, snapshot, quarantine and active names. | A negative-control fixture deliberately creates each real residue name and proves the assertion fails; normal recovery proves zero forbidden residue. |

## Scope and invariants

R11 is limited to:

- `ops/orchestration/cyf_orchestrator.py`
- `ops/orchestration/cyf_evidence_envelope.py`
- `ops/orchestration/tests/test_cyf_orchestrator.py`
- `docs/implementation/README.md` only where the corrected preservation/publication contract requires it.

Preserve all existing invariants:

- parent-directory-fd plus exact `(dev, ino, regular-type)` binding before unlink;
- foreign replacement is never deleted as controller-owned data;
- no process preemption or production action;
- exact-tree evidence keys include tree, selector and fixture digest;
- stock CLI remains fail-closed;
- K1/K2, executor capability and no-preemption tests remain passing.

## Promotion gate

R11 may enter fresh Review only with a clean exact commit/tree and independently recomputable evidence for:

1. continuous-EEXIST exhaustion/release recovery;
2. duplicate-key non-mutation;
3. selected acceptance suite;
4. full orchestration suite;
5. `py_compile`, ledger validation and `git diff --check`.
