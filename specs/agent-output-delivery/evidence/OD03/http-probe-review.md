# OD03 HTTP probe extension review

Independent read-only fallback reviewer `/root/output_design_review` approved root commit `5a47ed7355d9f809ad3aad98dd04fa846bd56ab9` for **tool correctness only**.

The probe binds returned list entries to the exact source and version entries to source/outputId. New-publication mode requires version 1 in both first pages; read-only mode makes no claim about an older version's first-page position. Optional cross-user checks require a separate environment token, a successful authenticated capabilities response, then nonretryable 404 with absent/empty `details` on list, version list, detail and download routes. Existing loopback/no-prefix/no-proxy/no-redirect, bounded-response and credential-redaction controls remain intact.

`python3 specs/agent-output-delivery/tools/test-http-probe-controls.py` exited 0: four methods, sixteen synthetic subcases. No live CYF endpoint was run.

Limits: distinct token strings do not independently prove distinct principals; provisioning an authenticated unrelated user remains an execution precondition. The generic Error schema and probe do not detect resource text leaked through `code`/`message`; privacy tests of those fields remain product acceptance work. This review does not approve product ACL, deployment or release.
