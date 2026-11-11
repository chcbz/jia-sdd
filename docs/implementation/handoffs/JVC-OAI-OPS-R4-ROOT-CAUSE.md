# JVC-OAI-OPS R4 root-cause matrix

Date: 2026-09-04
Rejected R4 commit/tree: `17d9d39b3547c96e84653ab0454831895453b06a` / `fb04e2f622130a4f53c4e40421a0f13bf1ae216c`
Status at creation: `failed_attribution_required`; no production action and no 100-case verifier execution are authorized.

| ID | R4 review finding | Required bounded R5 closure |
| --- | --- | --- |
| P0-1 | Post-current-link-switch replay recreates the same transaction snapshot with `current=candidate`, which conflicts with the original `current=previous`; `activate-release.sh` cannot reach recovery/finalization. Helper-only tests do not prove the entrypoint. | Generation snapshot must be immutable and reused by transaction ID on replay; preflight must validate the recorded snapshot against the generation-aware allowed link state rather than republish it. Add real `activate-release.sh` fault injection before/after link swap and terminal record renames, including rollback/failed partial records and same-command replay. |
| P0-2 | `--external-manifest-sha256` is optional, so a caller can invent a valid-looking manifest and seal/verify it. | The controller-owned manifest SHA and path identity must be mandatory inputs supplied outside the candidate-controlled evidence directory; absence/mismatch must fail before execution. Test forged but syntactically valid fields with a non-controller hash. |
| P0-3 | The named 100-case inventory counts helper calls, not the required production-entrypoint crash/race matrix; snapshot races omit several security-sensitive classes/phases. | Inventory must enumerate and enforce every required entrypoint fault and per-phase mutation: passwd/group/NSS, JDK/JAR/config/unit, Nginx main/includes/snippets/selectors, release links/directories, environment and exact lock FD/inode. Any helper-only substitute must be rejected for an entrypoint-required case. |
| P1-1 | Evidence gate ignores unexpected directories/FIFOs/nonregular entries outside the manifest. | Treat evidence root as a closed tree: reject any nonregular, symlink, hardlink, unexpected or unmanifested entry at every depth; manifest every allowed regular file exactly once. Add directory/FIFO/socket/symlink/extra-file tests. |

## Scope and gate

- R5 may modify only `ops/juyiting-voice-production/**`.
- No apply/deploy/service or Nginx action, no key or voice-flag action, and no use of production evidence.
- A fresh GPT-5.6 Terra owner may make one bounded R5 remediation after the controller records this matrix; then a fresh independent review must return `0/0/0` before a Terra verifier may execute the complete named inventory.
