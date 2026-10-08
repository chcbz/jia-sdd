# F1 closure and residual risk

## F1 status: closed for the scoped API durable path

- Human identity is resolved by `HumanSenderIdentityResolver` and passed as `ServerResolvedSender` through controller -> relay -> durable admission.
- Durable user row, metadata, dispatch payload and canonical hosted wire use trusted type/displayName/jiacn/clientId; client body and metadata sender fields cannot override them.
- Agent delta/final identity is resolved from the authenticated WebSocket session plus `AgentSenderIdentityResolver`; payload `senderName`/`agentName` cannot override persisted or published durable identity.
- Builtin SongJiang uses a fixed server-created `ServerResolvedAgentSender`.
- Task materials are owner/client/task scoped, active INPUT/REFERENCE-only opaque references; lookup failure yields an unavailable marker and grants no file access.
- Adversarial regressions cover spoofed HTTP sender, spoofed durable callback names, trusted material filtering and canonical wire exclusion of the forged identity.

## Residual

- F2 capability negotiation remains incomplete.
- F3 complete reconstructable context remains incomplete.
- F4/INSPECT execution semantics remain incomplete.
- No isolated-MySQL migration run, module-wide suite, bootJar, deployment, production DDL/DML or paid model call was performed.
- This is an integration baseline, not a merge-ready/release-ready claim.
