# OD00 outstanding gates and handoff

Independent architect decision (2026-09-09): OD00 may become **development prerequisites accepted / runtime-release gates pending** only after the minimum local evidence below passes. This is not a full OD00 PASS or release approval. OD01 opens no file-write endpoint.

| Gate | Owner / due | Current evidence |
| --- | --- | --- |
| Local agent/chat targeted compilation and application-component cross-module transaction commit/rollback | OD00 verifier, before OD01 | JDK/wrapper ready; compile bootstrap running; opt-in real MySQL probe being added |
| Canonical contract/fixtures load | OD00 verifier, before OD01 | design static schema/example/reference checks passed; implementation tests must consume applicable fixtures |
| Strict source owner, no tenant=0 fallback, persisted trusted conversation and bounty run dispatch, WS auth unicast and revoked/cross-binding negatives | OD01 writer/reviewer, before OD01 accepted | not implemented |
| Real private storage and clean/infected/oversized scanner transport | OD00 verifier, before OD02 | real local probes PASS; see prerequisites.md |
| Scanner unavailable cannot mark upload READY; durable verification retry and resource bounds | OD02 writer/reviewer, before OD02 accepted or any file publication enabled | no file writer exists yet; application negative test pending |
| Actual deployment agent/chat same database + transaction manager; migrations on disposable production-version schema | OD06 release guard, repeated for OD11 | local slice is not proof of production configuration |
| Actual production private bucket credentials/policy, scanner health/signatures, backup/restore/retention | OD06 release guard | local development services only; production pending |
| Effective output route body size >=50 MiB + overhead, hard upload timeout 10 minutes, same-origin API | OD06 release guard | installer template body size known; effective deployment config pending |
| Trusted live conversation + bounty dispatch, offline byte-identical download, supported mobile/browser route | OD06 release guard | requires integrated API/client/Web; pending |

User has already authorized continued serial implementation and independent reviews. Routine task progression does not require renewed confirmation. Production release remains subject to the concrete release scope and actual verification; it must not be inferred from local PASS results.
