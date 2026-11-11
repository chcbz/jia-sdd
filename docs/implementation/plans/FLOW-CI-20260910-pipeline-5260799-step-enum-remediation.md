# Flow 5260799 step-enum remediation

**Date:** 2026-09-10 (Asia/Shanghai)

## Newly attributed root cause

The Flow editor/runtime enum supplied by the user excludes `SetupJava` but explicitly includes `JavaBuild` and `Command`. The saved candidate used the unsupported `SetupJava` step before `Command`; Run 1 then failed before any step log was emitted.

## Single repair

- Remove the unsupported `setup_java` step entirely.
- Change the sole `cold_build` step from `Command` to supported `JavaBuild`.
- Configure Java 21 through `with.jdkVersion: "21"` and retain the audited command, ticket payload, source, no-deploy boundary, and encrypted Maven variable-group association.

This is configuration-only; it does not alter source, ticket, Gradle tasks, private credentials, deploy behavior, or artifact publishing.

## Required gate

A Terra read-only reviewer must approve the exact regenerated YAML before one update/readback attempt. Run 1 is never retried.
