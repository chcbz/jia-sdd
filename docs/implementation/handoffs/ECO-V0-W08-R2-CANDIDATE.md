# W08 corrected package candidate — 2026-09-06

Clean `eco-v0-skill-seeds-r2`: commit `6619aae27fd8a31c9ea1dec429a738236ea8a252`, tree `0b869eb0acf78068a97790785f50228da06431ff`, parent `086a9ddea30c31d0922b700ef134a4a7521b4f42`. Main verified Git identity/clean state. Eight paths: six ZIPs, PlatformSkillPackageCatalog.java, PlatformSkillPackageCatalogTest.java. Original candidate tree unchanged.

All six packages now have supported name/description/metadata.version frontmatter; unsupported top-level version removed. Product IDs, external1.0.0 version, prices, admin/default-off/scope unchanged. No live seed/product version was mutated.

| Skill | Bytes | SHA256 |
| --- | ---: | --- |
| code-editor | 688 | 25f80edca5ac1f88c7007712bba92a8d82a61e679c07ed08f5b57e19dd100b39 |
| code-reviewer | 687 | aa0efdf4a561bf0ccfed96a7a5f48c096c9321ba563e7f89e9a1b968d9c79eb1 |
| deploy-runner | 715 | fde2e6c59228972aee0a8b3823f9316feed0084bda7d53454c276710c68f73e9 |
| repo-inspector | 687 | 4cd173b1fd6606fbfa9d416a4858c914440552d9ac188d398d31a4454f79a4ed |
| repo-test | 660 | 5448a1d231272617085cc6be255d14296ea10c8087d436a0e182a9a4eadb501a |
| web-builder | 714 | b655e9d7c4214d517feaf819e094b4627103f1b9ed15c5e6d73ce81386db6e63 |

Original Terra reports Python3.6-stdlib restricted generated-metadata/negative checks, unchanged body, deterministic repack and catalog digest/size match6/6PASS; whitespace/scope/clean checks passed. These are static claims tied to the source tree, not official quick_validate/Java/DB/installation evidence. Two earlier incompatible-validator failures and authorization remain in W08R2 root-cause matrix. Independent bounded delta review and focused runtime tests still required.

W09 may consume corrected package/catalog source at its clean checkpoint. W10 original owner is implementing metadata.version parser + corresponding fixtures and managed-host packaging in `eco-v0-agent-integrated`; current old installer47PASS does not prove this new metadata integration.
