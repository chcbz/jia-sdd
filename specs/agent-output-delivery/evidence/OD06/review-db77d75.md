# OD06 API independent review: REJECT

Candidate db77d75f6ac5dbbb82b9b66ec6b2874a6fa5f321; independent read-only reviewer /root/od05_review_fallback. Inspected remerge diff,22 overlapping files, uploaded-text preview, event writers, schema initializers and preserved starter/canonical build controls. No product/root edits or Gradle run by reviewer.

**P1: deleted conversation remains authorized for output operations.** ChatConversationMapper.findExactOwnedById (line39) lacks deleted_at IS NULL. ConversationOutputSourceAuthorizer (line75) and ConversationOutputVersionProvider (line37) also omit deletedAt checks. Existing trusted output runs/tickets and UserJwt output reads can pass their source checks after soft deletion changes only tombstone/generation. Reject the candidate's entry into live R1 verification until repaired.

The archived Java probe uses candidate compiled classes, a controlled DAO and actual mapper-annotation reflection. It observed MUTATION_ALLOWED=101, OUTPUT_READ_OWNER_ALLOWED=true, SQL_FILTERS_DELETED_AT=false. probe.exit0 means the probe completed and exposed the defect; this is not a passing security test, actual MySQL or HTTP E2E. No other new blocker was found in this review scope.

Sole writer repair scope: exact query plus locked authorization and read-provider deletion validation, preserving exact tenant/client/owner rules and lock order; negative deletion-before-ticket/publication/read combinations with real MySQL and undeleted positive controls. Recheck with the same independent reviewer after a separate frozen repair commit.

Development packaging passed with64 verifier tests, but wider regression remains1539/6fail/121skip (five merge findings separately repaired, historic Rabbit3.6.11 host prerequisite unavailable). Original private dependency403, canonical packaging, actual TCP/WS/browser/offline/device and release gates remain open.
