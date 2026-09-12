# Binary upload mismatch investigation

Writer reported real task1 dispatch failed without workspacePolicy; task2 used an isolated Git workspace and reached trusted TASK run753feab8e4634be488797c37d9b3a912. Markdown published; PNG upload returned OUTPUT_SIZE_MISMATCH; ZIP remained snapshotted. These are partial observations, not bounty acceptance.

Root read the PNG109B and ZIP377B snapshots. A UTF8 string roundtrip changes both byte counts/hashes (see root-snapshot-roundtrip.json). Static API43e6bb94 source shows base UriAccessLogFilter wraps requests in common EsRequestWrapper, which reads bytes via InputStreamReader into String then returns body.getBytes(). Actual wrapper/server correspondence and repair are assigned to the sole writer; do not claim root cause confirmed solely by Python's replacement behavior.

A repair must preserve streamed upload bytes and bounded memory without disabling authentication. Tests should include the real filter/wrapper path that mock controller-only tests can miss. Preserve binary snapshots for retry and do not rerun the synthetic model solely to recover an upload failure.
