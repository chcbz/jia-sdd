# R6 direct-native update block

At 2026-09-10 09:57 UTC, the authenticated `UpdatePipeline` request for the direct native `java_build` candidate returned HTTP/API error `-1 / 400`: `system error, please try again later` (request ID recorded in `FLOW-CI-20260910-update-r6-response.json`). The request did not provide YAML validation details, so it cannot be attributed to Gradle, OpenCV, Maven credentials, or the candidate's runner execution.

No second update attempt and no new run were made. The prior R5c pipeline remains the last readback configuration and Run 6 is not retried.

## Root-cause matrix / next remediation

1. Obtain a platform-side Flow validation event for request `01A08AC0-05E3-5C63-B25E-90DC63BB8EFA`, or wait for a documented platform recovery signal.
2. Before any new write, re-read pipeline `5256653`, source configuration, and encrypted variable-group association.
3. Re-run independent reviewer when reviewer service is available, then make exactly one versioned update attempt. Do not retry the same API request blindly.
