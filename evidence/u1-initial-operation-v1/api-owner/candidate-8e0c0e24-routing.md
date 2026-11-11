# MMD-U1-INITIAL-OP-ROUTING-20260930 API Owner candidate

Date: 2026-09-30 Asia/Shanghai
Owner/profile: `01a0f0d8-8202-7040-9d9c-becce02f7a3f` / `critical_worker`
Branch/worktree: `codex/juyiting-mmd-initial-operation-v1` / `/home/isp/wsps/cyf/.worktrees/juyiting-multimedia-deliberation-20260928/api-initial-operation-v1`
Parent: `05ace019fc10cd481928c2b21859554709e448e0` / tree `ac989e116a42bec1c0ebb09bd4ba21902aa831ae`
Candidate: `8e0c0e24dfb0beb31ea4dec62feb7ce0c0f60d5e` / tree `885b6f4beac05ea470e3af69c5d00749139a8666`

## Changed paths

- `agent/jia-agent-service/src/main/java/cn/jia/agent/api/AgentController.java`
- `agent/jia-agent-service/src/test/java/cn/jia/agent/api/AgentTaskExecutionGrantControllerTest.java`

## Implemented

- `AgentController.hasV2GrantFields` now treats any non-null `initialOperation` as a v2 grant field.
- Selector-only requests therefore require authenticated JWT owner/client scope before reaching the grant service and can no longer fall through to legacy `AgentService.assignTask`.
- The controller does not classify, trim, or validate selector content; valid, blank, and unknown non-null values all route to the existing v2 validator.
- A truly absent selector with no other v2 fields retains the legacy assignment route.

## Test additions

The existing controller test now proves:

- selector-only `GENERATE_IMAGE`, blank whitespace, and `UNKNOWN` requests without JWT fail `UNAUTHENTICATED` before either service;
- the same three requests with JWT invoke `AgentTaskExecutionGrantService.assignAndGrant`, propagate its validator rejection, and never call legacy assignment;
- a truly absent `initialOperation` still uses the legacy path.

Focused selector for Main: `:agent:jia-agent-service:mmdU1Grant`.

## Static self-check

- `git diff --cached --check` before commit: PASS.
- `git show --check 8e0c0e24`: PASS.
- Exact staged tree matched final tree `885b6f4beac05ea470e3af69c5d00749139a8666`.
- Allowed-path scan: PASS; exactly the two assigned paths changed.
- Source assertion scan confirmed selector detection, JWT/validator routing tests, legacy no-interaction assertions, and explicit absent-selector assertion.
- Brace balance check for both touched Java files: PASS.
- Worktree clean after commit.
- No Gradle, push, deploy, DTO/grant/schema/DAO/Chat/snapshot/Provider change or production operation was run.

## Residual verification

Main/test runner still needs serialized compilation and `:agent:jia-agent-service:mmdU1Grant`. No contract difference or additional feature is introduced.
