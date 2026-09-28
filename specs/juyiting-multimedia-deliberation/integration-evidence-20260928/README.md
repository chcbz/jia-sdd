# 本次整合的便携证据

日期：2026-09-28。新feature分支整合证据，不是多媒体业务已验收/上线证明。

- baselines.json：各仓develop/fast输入与本线程独占worktree。
- webclient-owner-self-check.json、web-targeted-tests.log：Web最终树与初始Client merge回执，Web86通过。
- client-targeted-tests.log：**历史**Client初始merge d79896e的167项日志；不是最终wire收敛树。
- wire-client-manifest.json、client-final-tree-tests.log：最终Client33e38de，167通过；API源bc4bd8b与Client夹具字节一致。
- web-merge-regression-and-remediation.log：首次Web身份/metadata回归失败归因，未删除失败历史。
- webclient-push-readback.json / wire-client-push-readback.json：新feature远端SHA回读，非develop发布。
- api/：Owner最终回执、冲突解决、F1边界、历史失败归因与定向验证摘要；`.log`明确为事后摘要，不冒充原始终端日志。xml-suite-case-summary.json来自Gradle XML保留suite/case状态，省去可能含环境信息的stdout；详细原始XML仍在API独立工作树build/test-results。
- api-push-readback.json：最终API推送、fixture与Client一致性的主Agent复核。

checksums.json列本目录其余文件SHA-256，不包含自身。根仓最终提交和四仓最终远端核验回执存放在线程evidence/final-delivery-receipt.json，避免自引用提交哈希。

API选择器可能重叠，不将总和称为独立用例数；chatDeliberation在最终tree调用UP-TO-DATE，保留同source set既有56项通过证据，见该selector摘要。未来34项产品验收保持NOT_RUN。
