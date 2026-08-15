# Multi-repository SDD workflow

## Source-of-truth rule

| Question | Authoritative location |
| --- | --- |
| What should be built and accepted? | `specs/<feature-id>/` in the root repository |
| What does the system currently do? | `docs/knowledge-base/` and the pinned submodule source |
| How does it run or get deployed? | `docs/` runbooks and deployment material |
| How is it implemented? | `api/` and `web/` submodules |
| Which backend/frontend pair is an integrated baseline? | The root commit's `api` and `web` gitlinks |

`specs/` is the intended future state. `docs/knowledge-base/` is a reverse-engineered current-state reference. Neither replaces source code for implementation details.

## Required feature artifact

Use one directory per cross-repository feature:

```text
specs/<feature-id>/
├── spec.md             # Problem, goals, non-goals, scope
├── design.md           # UX, API/event/data/security and compatibility contract
├── tasks.md            # Explicit API/Web/integration owners and work items
├── acceptance.md       # Observable acceptance criteria and evidence
└── integration.yaml    # Candidate submodule SHAs and verification state
```

The API contract in `design.md` must state method/path, request/response/event shape, error behavior, authentication/authorization, compatibility, and version/replay semantics when it is asynchronous.

## Lifecycle

1. **Draft** — Create the feature: `./sddw new <feature-id> "title"`; define the problem, goal, non-goal and scope.
2. **Ready** — Agree the contract and split `tasks.md` into `api/`, `web/`, and integration work. Identify migrations, ACL, transactions, SSE/WebSocket replay, and rollback constraints before implementation.
3. **Implementing** — Implement in each submodule on independently reviewable commits. Do not commit one repository's source into the other or into the root.
4. **Integration-ready** — Check out the intended API/Web commits locally, run the relevant tests, then execute `./sddw pin <feature-id>` and `./sddw verify <feature-id>`.
5. **Accepted** — Record test commands/results in `acceptance.md`; set `integration.yaml` status to `accepted`; commit the spec update and both submodule gitlinks together in the root repository.
6. **Released** — Add deployment/release evidence only after the actual deployment process succeeds. The root SHA is the reproducible delivery baseline.

## Daily commands

```bash
# Inspect coordinated and implementation state
./sddw status

# Start a cross-repository feature
./sddw new agent-task-collaboration "Agent task collaboration"

# After API and Web commits are checked out locally
./sddw pin agent-task-collaboration
./sddw verify agent-task-collaboration

git add specs/agent-task-collaboration api web docs
git commit -m "feat(sdd): integrate agent-task-collaboration"
git push origin master
```

## Integration gate

A root integration commit must include all applicable items:

- `spec.md`, `design.md`, `tasks.md`, and `acceptance.md` are current.
- `integration.yaml` contains the exact API and Web commit IDs currently checked out.
- API, Web, and integration verification commands/results are recorded.
- Breaking behavior, schema migrations, access-control changes, and async replay semantics are explicitly assessed.
- The root commit updates the submodule gitlinks only after the submodule commits are pushed and reproducible.

For P0 identity/ACL/transaction/migration changes, use the project routing policy and obtain an independent read-only review before user confirmation. Every Gradle command on this host must use `/tmp/cyf-gradle.lock`.
