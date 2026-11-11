# JVC-OAI-OPS R5 root-cause matrix

Date: 2026-09-04
Rejected candidate: `95636383df6163a64e9452be8fd813444d05200d` / `def0a4faac0bb88092095a65ff0c51328483839c`
Status: `blocked_root_cause`; no source retry, verifier, host action or deployment is authorized by this matrix alone.

| ID | Root cause | Required next remediation proof |
| --- | --- | --- |
| R5-P0-1 | External manifest path and SHA remain caller-supplied values; root mode/format does not establish controller ownership. | Bind the manifest through a fixed controller-owned absolute path/FD and independently recorded controller SHA outside candidate/evidence control. The candidate must not accept arbitrary path/SHA CLI inputs. Test a syntactically valid forged manifest plus forged matching SHA. |
| R5-P0-2 | Fault tests re-write a copied release module and omit genuine shell-entrypoint rollback/failed partial-record replay; snapshot races omit required inputs/phases. | Add exact production-entrypoint fault seams that do not mutate source/modules at runtime. Execute `activate-release.sh` end-to-end through activating, switch, activated/finalizing/finalized, rollback and failed partial-record boundaries. Build a named matrix covering every sensitive input (identity/NSS/group, JDK/JAR/config/env/unit, Nginx main/includes/snippets/dump, selectors/release/state dirs and lock FD/device/inode) at every required phase. |
| R5-P1-1 | Closed-root implementation lacks regression coverage for FIFO/socket/symlink/hardlink evidence entries. | Add named tests for each nonregular/unexpected entry and prove fail-closed before manifest/seal/verify use. |

A fresh remediation needs a new explicit authorization bound to this matrix and the R5 tree. The first valid post-matrix retry remains limited to `ops/juyiting-voice-production/**`; independent review must be `0/0/0` before any full inventory execution.
