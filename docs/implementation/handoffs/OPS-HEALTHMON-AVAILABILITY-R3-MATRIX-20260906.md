# OPS-HEALTHMON availability R3 bounded remediation — 2026-09-06

User requirement: production recovery must not wait for old soft memory/disk thresholds; stop after three unsuccessful attempts and send clear Chinese alerts. Main remains coordination-only. API recovery continues independently under the voice controller's exact Turing owner; monitor remains maintenance.

## Two-review failure attribution

- R1 `53f05b9d` / tree `8f344415`: unique reviewer Raman `01a07656-6c6f-7882-aa76-eddfe37f6dec` REJECT 0/3/1. Missing post-mail maintenance/dependency revalidation, interrupted-third urgent notice, and full priority outbox protection; mixed snapshot timestamp.
- R2 `68b84d6eca8dc95f6acbc99640bd394d528b65f7` / tree `1bd0f8304077478811774ccde45786427637054c`: same reviewer confirms all prior findings closed and actual 60/60 offline tests with shared-log SHA `60526754ec25efc63ac53308a6df0906348dbb1c9fc2c35713b38e82b319c3cc`. REJECT 0/1/0 for a specific new regression: the three-UP reset now requires in_flight=null, but interrupted attempts 1/2 never clear that field. An old incident can close while its budget fence leaks into a new incident.

## Explicit bounded repair authorization

After recording second failure / blocked_root_cause, authorize exact Knuth `01a0763d-3a60-7782-9ad5-898e24525d88` to repair only interrupted attempts 1/2 followed by three trusted UP observations, with exact regression tests. Preserve interrupted-third UNKNOWN/latch/urgent semantics, no fourth invocation, and old-to-new incident isolation. Do not invent failure or success for an unknown native terminal. No blind repeated test loop. New candidate, real offline test log, and same unique read-only reviewer are required. No new features or broad refactors.

Source ownership remains ops/health/** in the existing health-monitor worktree. No install/reconcile/resume/mail, API lifecycle, or other thread's files/process/evidence operations are authorized by this matrix. Production/API exact owner does not wait for this source work.
