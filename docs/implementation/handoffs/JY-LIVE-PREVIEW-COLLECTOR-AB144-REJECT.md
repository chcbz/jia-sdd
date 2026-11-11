# Collector ab144 authoritative rejection — summary
Unique Godel native completed COLLECTOR_REJECT P0/P1/P2=0/1/1. Collector ab1447573d08bee5bb9226fa18c13faa526d265002c81c14f88ce25122b6d5ab; inner a4690066389a6120b07ce71676592085d21af36e3bbcf261e3be06b9907d4640; manifest ca432152f9a57f0baaf61e668e847658bff739ad412f5aa18e73b89874b119aa.
P1 collector276-290: native_build_pass assigned before final source snapshot; drift yields contradictory sealed PASS and exit1; after_error can even exit0. Before sealing require complete postconditions including successful after snapshot and exact before/after equality; failure sets explicit error/status; store final collector_rc, seal/print and exit consistently. Donor terminal integrity must not be silently skipped.
P2 collector32,163 and inner20: fchmod after fsync leaves mode metadata not synced before rename. Order write_all→fchmod→fsync(file)→rename→fsync(directory).
Other findings source-closed: inner strongpins/ledger3SHA, safe dist and privatevalue scan, argv/writable receipt/Popen counts, initialization fallback, dts fullwrite/atomic handling, snapshot/donor/toolpins/latch/status separation. Do not rewrite them.
No native builds occurred. Product8bf22/a6c8 SOURCE/TEST_DELTA and13fresh+73reuse remain accepted. OriginalTerra may fix ONLY these two controls in NEW own immutable scripts package, preserving all old artifacts, then sameReviewer re-review. No source/test/donor edits or native/probe/snapshot/browser execution.

Retrieved 2026-09-07T11:34:49+08:00; exact review completion time not supplied.
