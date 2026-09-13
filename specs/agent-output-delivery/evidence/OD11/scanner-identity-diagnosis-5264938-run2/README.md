# Scanner identity diagnosis — actual result

Pipeline5264938/run2, job514732040, order69532572: SUCCESS and one host Success. Source078f2bba, corrected YAML8d73b7be, controller63fff644; full readback accepted before one start. Old resource-check run1 evidence is retained separately.

Dedicated account and effective daemon/bootstrap units all resolve to UID/GID986; both units are inactive/disabled with NRestarts0. New daemon journal entries from failed activation5264943 show PID3720689 running as UID/GID986 and reaching signed-database loading before operator compensation stopped it. This establishes correct observed daemon identity, but the earlier rejected `/proc` UID tuple was not recorded, so a transient systemd pre-exec child remains a hypothesis.

A repaired activation should record pre-readiness UID/GID tuples before checking them, allow only a bounded initial credential transition under the exact verified unit and same PID/startTicks/NRestarts0, and require strict dedicated UID/GID plus exact executable inode before any readiness acceptance/scan. No root or replacement process may qualify as ready.

Snapshot1789304438: MemAvailable1636532224bytes; disk2717790208bytes. Scanner's existing reservation barely fits; MinIO's2862452920byte initial gate does not. Storage remains uncreated and requires capacity investigation, not a lowered reserve. No scanner/storage/file mutation occurred in this diagnostic.
