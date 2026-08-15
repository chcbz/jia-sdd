# SDD Specifications

This directory is the cross-repository source of truth for feature intent, design, execution, and acceptance.

Create one directory per cross-cutting feature from `_template/`. Keep implementation in the `api/` and `web/` submodules; record the tested submodule revisions in the coordinating root-repository commit.

## Suggested lifecycle

1. Write `spec.md` before implementation.
2. Record cross-service and UI decisions in `design.md`.
3. Split the work by repository in `tasks.md`.
4. Validate the agreed behavior in `acceptance.md`.
5. Commit the relevant submodule pointers together with the specification update.
