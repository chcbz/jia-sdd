# JVC-OAI OPS R20 verifier preflight remediation — 2026-09-05

Second consecutive failure stopped the ledger at blocked_root_cause. No R20 namespace invocation occurred. Sourcefff17bf91930bd6a16da6f950cca50be3256ed7c / tree5a8a6d66ecfe5c262b7ad62e4821fc78c127fbba remains unchanged and reviewed0/0/0.

| Observation | Attribution | Bounded correction |
|---|---|---|
| R19 first readiness20s timeout; drained143; inner stderr lost | Target startup reason unknown, not failed-terminal proof | R20 source preserves fixture stderr; exactly one diagnostic target run remains pending |
| R20 static parse FileNotFoundError literal `$evidence_dir/wrapper.py` | Quoted heredoc filename interpolation error; zero target invocations | Use literal absolute wrapper path supplied in argv, no shell interpolation in Python |
| Unexecuted wrapper contains future annotations but system Python3.6.8 | Static additional incompatibility found by main before execution, not another runtime failure | Remove only future-annotations line from verifier-owned wrapper |
| Wrapper does not set exit status from returned run_case status | Static receipt correctness defect, not source defect | Append `raise SystemExit(0 if status == "PASS" else 1)` |

Same verifier01a07127 owns `/tmp/jvc-oai-ops-r20-failed.AZI84o`. Preserve original wrapper as `wrapper.preflight-original.py`, update only its wrapper, chmod0600. No source edits. TMPDIR existing fresh0700`/tmp/jvc-oai-ops-r20-failed.AZI84o/tmp` has no target artifacts. Exact invocation still approved by reviewer01a07123.

Static parse/compile without execution or pycache:

```sh
/usr/bin/python3 -I -B -c 'import ast,sys; p=sys.argv[1]; s=open(p).read(); ast.parse(s,filename=p); compile(s,p,"exec"); print("STATIC_PASS")' /tmp/jvc-oai-ops-r20-failed.AZI84o/wrapper.py
```

If static checks pass, run exactly once:

```sh
TMPDIR=/tmp/jvc-oai-ops-r20-failed.AZI84o/tmp /usr/bin/python3 -I -B /tmp/jvc-oai-ops-r20-failed.AZI84o/wrapper.py
```

Capture rc/stdout/stderr externally to this evidence root, print summary and preserve diagnostic JSON/stderr/poststate plus owned drain proof. No main(), selector, monkeypatch, timeout/assertion changes, tracing, other process/evidence actions or production. Stop at first new failure and attribute before any further action. No full131 run authorized.
