# Account self-service closure tasks

## Discovery and policy

- [ ] Inventory all user-linked data and credentials across SQL, LDAP, Elasticsearch, files, Agent, Chat and Task modules.
- [ ] Freeze legal-retention, erasure/anonymization, recovery-window and operator-escalation policy.
- [ ] Define a P0-reviewed closure state machine, authorization contract, transaction/outbox boundaries and idempotency semantics.

## API and Web

- [ ] Implement dedicated self-service request/confirm/status/cancel endpoints without reusing generic delete-by-id.
- [ ] Revoke sessions, authorization grants and API keys at the correct lifecycle transition.
- [ ] Implement accessible confirmation, recovery-window and final-status UI.

## Integration and release

- [ ] Add production-shaped migration, concurrency, partial-failure, retry, rollback and data-erasure verification.
- [ ] Obtain independent security/privacy review and execute SDD pin/verify before release.
