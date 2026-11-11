# OPS-RESOURCE-TELEMETRY R11 Root-Cause Matrix

Date: 2026-08-29

Rejected exact candidate:

- Commit: `03ef9edbee4b00339559d39a202901a6de4f1b7b`
- Tree: `713c191998f03e347ab7f3145763e4a5cef35525`
- Authoritative reviewer: `01a04cfd-9537-74d0-9f92-183f697cec69`
- Verdict: `REJECT P0/P1/P2=0/1/0`

## Failure matrix

| Symptom | Root cause | R12 remediation | Required proof |
|---|---|---|---|
| During final-active restore, swapping a foreign active between `_preserve_entry()` `lstat` and quarantine rename raises `SystemExit`; active becomes absent, exact original remains only as `.recovery-*` with `nlink=1`, and immediate same-nonce retry reports the external record missing. | Final-active restore reuses strict pathname provenance handling intended for named snapshots. A changed pathname makes `_preserve_entry()` fail closed after moving a different foreign inode. The rollback call chain catches only `OSError`, so it exits instead of revalidating the still-owned recovery link and continuing. Existing prolonged-EEXIST coverage uses a stable foreign and never injects the `lstat -> rename` replacement window. | Add final-active-only retry-safe cleanup. Every actually moved foreign inode/type/bytes must remain in quarantine. A provenance mismatch during active cleanup must not terminate restoration while the exact recovery link remains valid. Revalidate recovery `(dev, ino, regular-type)` every iteration and continue until contention releases. If an exact-original alias is encountered, remove only that extra alias after parent-fd identity proof. Do not weaken named snapshot or generic owned-entry strict identity behavior. | Deterministically exceed the old retry bound, repeatedly swap foreign active specifically between preserve `lstat` and rename, then release. Prove exact original restored at active with exact bytes/dev/ino/uid/gid/mode/size and `nlink=1`; consumed, actual `.recovery-*`, `.consume-*`, stage and snapshot residues absent; every foreign object preserved in quarantine; ledger bytes unchanged; immediate same-nonce reload and consume pass; named-snapshot replacement tests remain passing. |

## Exact code scope

R12 may modify only:

- `ops/orchestration/cyf_orchestrator.py`
- `ops/orchestration/tests/test_cyf_orchestrator.py`
- `docs/implementation/README.md` only if wording must be clarified without weakening the accepted contract.

`ops/orchestration/cyf_evidence_envelope.py` is out of scope unless a new independent defect is demonstrated; R11 duplicate-key reserve-before-publish behavior must remain unchanged.

## Promotion gate

R12 requires a clean exact commit/tree and immutable independently recomputable evidence for:

1. the new lstat-to-rename swap adversarial test plus all prior prolonged-EEXIST/duplicate-key/residue controls;
2. selected acceptance;
3. the complete orchestration suite;
4. py_compile, ledger validation and `git diff --check`;
5. fresh independent read-only Review.
