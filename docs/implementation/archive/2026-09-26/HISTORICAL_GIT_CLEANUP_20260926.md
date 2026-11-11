# Historical Git Cleanup — 2026-09-26

## Scope

Local branches and completed development worktrees only. Remote branches, release artifacts, production records, and runtime-owned agent workspaces are retained.

## Session summary

- `api` — 2026-09-26 username integrity — merged into v1.13.41; `codex/username-encoding-chat` at `8a1cd673ea80f3d21b08dab78b4e56bc97e7f224`.
- `api` — 2026-09-26 username integrity — merged into v1.13.41; `codex/username-encoding-oauth` at `188bf0c0e85afed82c1258b63f298491d669d575`.
- `api` — 2026-09-25 hosted-agent release — deployed historical snapshot; `release/1.13.35` at `aa27965c1f4ba7316b03d51ce86078315e182c02`.
- `api` — 2026-09-26 hosted-handshake release — deployed historical snapshot; `release/1.13.39-hosted-handshake-20260926` at `3873dd6ab18992c70800658102d492c606216d63`.
- `api` — 2026-09-26 v1.13.41 release verification — published; release ref retained; `release/1.13.41-username-integrity-20260926` at `fe413d778d222e1aa9129b23ca7c14be8a9451fb`.
- `web` — 2026-09-26 username integrity — merged into v1.13.41; `codex/username-encoding-web` at `c2af3ce30e7ced1e3d4d93234a1538e13bd73585`.
- `web` — 2026-09-26 v1.13.41 release verification — published; release ref retained; `release/1.13.41-username-integrity-20260926` at `3e7f81366381442625d26bf4d2b5a9b776cfd27a`.
- `web` — 2026-09-25 UI optimization release build — deployed historical snapshot; `codex/release-1.13.37-build-20260925` at `95ce14d54c19f4a7d6aa64d1fb547eb8c03d72fb`.
- `web` — 2026-09-26 hosted point-general flow — superseded by merged release; `codex/juyiting-hosted-point-complete-20260926` at `d030a200d95eac6cea7fb0d91c0dd915aacf3ada`.

## Deletion policy

- Only local refs already reachable from `origin/develop` are eligible for bulk deletion.
- Remote refs and immutable release artifacts are retained.
- Current `develop`, `master`, v1.13.41/v1.13.42 release refs, active/incomplete work, and runtime-owned agent workspaces are retained.
- Dirty worktrees are never force-removed.

## Planned cleanup

- `root`: 0 merged, unattached historical local branches eligible for deletion.
- `api`: 61 merged, unattached historical local branches eligible for deletion.
- `web`: 31 merged, unattached historical local branches eligible for deletion.

## Retained dirty worktrees

- `/home/isp/wsps/cyf/.worktrees/release-web-1.13.18-hall-identity-hydration-local-20260923-r3` — dirty worktree; no force removal.
- `/home/isp/wsps/cyf/.worktrees/release-web-1.13.18-hall-identity-hydration-local-20260923-r4` — dirty worktree; no force removal.

The machine-readable inventory is `historical-git-cleanup-20260926.json`.

## Execution

- Deleted **98** local, merged historical branches (API: 64; Web: 34; the initial unattached bulk was API: 61 and Web: 31).
- Removed **9** clean completed worktrees.
- Pruned stale worktree registrations for root, API, and Web.
- No remote branches, release artifacts, production records, or runtime-owned agent workspaces were deleted.
- Retained `api:codex/username-encoding-chat` because it is not an ancestor of `origin/develop`; retained the two dirty v1.13.18 Web worktrees without force-removal.
