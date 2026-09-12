# Real browser resource retrieval: 4 runs, 8 viewports passed

Accepted APIf1978b09/Web212bfe4 with Root probe41250f4 and the task-local standard JWT resource URI/CORS configuration. The synthetic Agent stayed stopped. Each of four exact resource routes ran at1440x900 desktop and390x844 mobile simulation:

| Resource | Preview | Download |
| --- | --- | --- |
| CONVERSATION3 report.md | Exact103-byte Markdown text | Source SHA matches |
| TASK3 report.md | Exact125-byte Markdown text | Source SHA matches |
| TASK3 evidence.png | Decoded4x4 PNG with exact title/size | Source SHA matches |
| TASK3 changes.zip | Download-only, as declared | Source SHA matches |

All four original observation.json reports contain succeeded=true, two viewport results, zero terminal/cleanup errors and the reviewed local clean-close compatibility observation. Buttons were scrolled into view, hit-tested and clicked through CDP mouse events. The exact authorized download endpoint returned200, and Root independently reread all eight downloaded files to verify hashes/sizes. Root inspected all eight screenshots: output cards/actions fit the viewport, correct target was highlighted, and task files were labeled shared/not formally accepted. No task Chromium process remained after the runs.

Each subdirectory contains the original report and screenshots. root-observation.json ties candidates and independent byte checks together. Earlier failed runs are retained under browser-navigation-diagnosis and browser-conversation-text-r5; they are not relabeled as successful runs.

Limits: JWT was obtained through real OAuth and bootstrapped into isolated localStorage, not through browser OAuth login. Mobile simulation uses mouse input and is not a physical WeChat/touch test. Files are tiny synthetic fixtures; PNG visual content is only4x4 pixels. Auxiliary HTTP statuses do not prove their business envelopes succeeded. These checks cover exact standalone conversation/TASK resource links, not all Hall/bounty navigation, identity/history switches, recovery, canonical packaging or release gates.
