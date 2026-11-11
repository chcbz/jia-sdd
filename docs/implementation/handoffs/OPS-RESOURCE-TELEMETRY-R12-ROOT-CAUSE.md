# OPS-RESOURCE-TELEMETRY R12 Root-Cause Matrix

Date: 2026-08-29

Rejected exact candidate:

- Commit: `3ecc02ff2e958758b5ec8c04fa76d4c6d3a28f5d`
- Tree: `80d13d31e214fab341ba1d521ebce39e5f252fc6`
- Authoritative reviewer: `01a04d1c-4c37-7500-871d-0aa549606ef3`
- Verdict: `REJECT P0/P1/P2=0/1/0`

## Failure matrix

| Symptom | Root cause | R13 remediation | Required proof |
|---|---|---|---|
| After recovery pathname identity is validated, a competitor can replace `recovery_name` before `rename_noreplace_at(recovery_name, active_name)`. The rename then promotes a foreign inode, clears the recovery variable, and only afterwards detects that active is not the exact original. The rollback path does not re-enter recovery, so the exact original can be lost or stranded, active remains foreign, and the nonce cannot be immediately reused. | R12 hardened the active-to-quarantine race but still treats the pathname observation of `recovery_name` as if it bound the subsequent recovery-to-active rename source identity. The rename primitive moves by pathname, not by the already-held exact descriptor. Post-rename mismatch is terminal and the tests inject only `active_name -> quarantine`, not `recovery_name -> active_name`. | Make final recovery-to-active restoration source-race convergent. After every attempted recovery-to-active rename, verify the moved active identity before discarding recovery state. If a foreign source was moved, preserve/quarantine that exact foreign and continue using the still-held exact-original descriptor/link state; if the exact recovery pathname was moved/unlinked/replaced, deterministically recreate or retain one owned exact link from the verified descriptor using parent-fd-safe operations, then retry. Never close the last exact-original reference until active is verified exact with `nlink=1`. Do not weaken generic/named-snapshot strict provenance. | Add deterministic adversarial tests that repeatedly replace/unlink/move `recovery_name` specifically between its identity check and recovery-to-active rename, including a successful foreign promotion. After contention releases, prove: active is the exact original `(dev, ino, regular-type)` with exact metadata/bytes and `nlink=1`; every actually moved foreign is quarantined; no actual `.recovery-*`, `.consume-*`, stage or snapshot residue; ledger bytes unchanged; same nonce reload and consume pass immediately; all R11/R12 active-quarantine, prolonged-EEXIST, duplicate-key and named-snapshot tests remain passing. |

## Exact code scope

R13 may modify only:

- `ops/orchestration/cyf_orchestrator.py`
- `ops/orchestration/tests/test_cyf_orchestrator.py`
- `docs/implementation/README.md` only if the contract wording must be clarified without weakening accepted behavior.

`ops/orchestration/cyf_evidence_envelope.py` remains out of scope. No Gradle, DB, Rabbit, production, process control, runtime ledger editing, or evidence deletion is authorized for the Writer.

## Stop and attribution rules

- Attribute the first focused failure before retrying.
- A second consecutive failure stops at `blocked_root_cause`; no blind continuation.
- Preserve every prior evidence bundle; R13 evidence must use a new non-overwriting root and bind the exact commit/tree.

## Promotion gate

R13 requires a clean exact commit/tree and independently recomputable evidence for:

1. new recovery-source replacement/unlink/move adversarial tests;
2. all prior final-active, prolonged contention, duplicate-key, residue and named-snapshot controls;
3. selected acceptance and the complete orchestration suite;
4. `py_compile`, ledger validation and `git diff --check`;
5. fresh independent read-only Review.
