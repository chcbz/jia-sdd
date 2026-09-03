# Account self-service closure design

Status: draft.

The contract, state machine, retention policy, dependency ownership, transaction/outbox strategy, idempotency keys, recovery window, authorization model, migration and rollback must be frozen before implementation. The self-service subject must come only from the authenticated security principal; client-supplied user IDs must never select the closure target.
