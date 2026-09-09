# OD01 candidate review — interim blocking finding

Candidate: `8e009b9d241979abb072d4b5b12d42b0476450dc`. Independent reviewer: `/root/output_design_review`, read-only. Review is still in progress; this is not its final report or approval.

## Command bytes are rewritten after persistence

The reviewer identified `chat/jia-chat-service/src/main/java/cn/jia/chat/handler/AgentWebSocketHandler.java:1093` and its output-context enrichment path. With output authorization enabled, `dispatchExactRawCommand` parses and reserializes the supplied bytes before sending them.

The existing contract in `agent/jia-agent-api/src/main/java/cn/jia/agent/service/AgentRawCommandDispatcher.java` explicitly requires: “Implementations must send the supplied bytes without JSON reserialization or compatibility wrapping.” The changed transmission can therefore differ from persisted outbox/inbox `wire_payload` and its hash.

Existing raw-command regressions do not inject the new output authorization service. The new output-context dispatch test proves repeated enrichment is stable, but does not prove sent bytes equal the persisted input bytes.

Required correction direction: preserve the exact transmission boundary and establish trusted output context before durable command encoding/hash capture, using the existing transaction and lock conventions. The final review will identify the minimal safe integration point. Add an enabled-feature case that asserts byte equality against persisted input and retains retry/hash behavior; do not weaken the raw-command contract to make the new test pass.

## Test/source association resolved separately

The two source files modified after initial tests received final-candidate verification: seven authorization unit tests and six real MySQL tests passed without skips on the clean frozen commit. Their source/report digests are in `candidate-8e009b9d-test-results/observation.json`. An earlier environment-gated MySQL run skipped all six cases and is excluded from passing evidence. These passing tests do not close the command-dispatch finding above.
