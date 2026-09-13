# Flow release target preflight — 2026-09-13

Read-only observations from 03:12–03:16 UTC using the aliyun-pipeline SDK skill. No push, pipeline start/retry/configuration change, hook change or deployment was performed by this task. Credentials were read in memory from the existing configured file; raw Flow YAML, callback URLs and signed artifact URLs were not exported.

Organization: `5fb7d76ee6f9d07f148529c7`. API and Web deploy to machine group `yjctjhskhk1ti9t4`; observed deployment orders resolve to host group `28833`, one batch and one healthy machine. Host command execution uses `root`.

| Pipeline | Source / trigger configuration | Actual deployment command |
| --- | --- | --- |
| `4403172` / `cyf-web-release` | `https://gitee.com/chcbz/cyf-web-kit.git`, `develop`, push, `^develop$` | `/usr/local/sbin/cyf-web-flow-deploy "$PIPELINE_ID" "$BUILD_NUMBER" "$CI_COMMIT_SHA"` |
| `5260799` / `cyf-api-release` | `https://gitee.com/chcbz/jia.git`, `develop`, push, `^develop$` | `/usr/local/sbin/cyf-api-flow-deploy "$PIPELINE_ID" "$BUILD_NUMBER" "$CI_COMMIT_SHA"` |
| `5263690` / `cyf-api-ci` | API `develop`, filter `develop`, events absent | No deployment stage observed |
| `1466118` / `cyf-api-legacy` | API `master`, push, wildcard `.*` | `/home/isp/bin/cyf_api_kit_start.sh`; stage `AUTO`, pause strategy `FirstBatchPause` |

Release pipelines download the artifact from their own build job to `/var/lib/cyf-{api,web}-flow/downloads/${BUILD_NUMBER}/package.tgz`, with one batch and no batch wait. The host helpers themselves have not yet been read or verified. A configured source filter does not prove effective webhook behavior; `isTrigger` is absent, not false. Retain the unresolved legacy-hook boundary described in `../OD06/integration-baseline-watch.md` before any API push. Do not use the legacy pull/build script as the output feature's release path.

Observed Flow YAML SHA-256:

```text
4403172 416ab6938483486f3f9a8e06b80d5c0a9b0a67a4381d7077038fb639d9cd811f
5260799 967530e94558159747a7fb03c3f79afb000ff23cb246992b07839e4cb37eadb8
5263690 984e26604ee34f93364aaa4f28480ecc8dac2a1990285144fd03098c2e87094e
1466118 ed03fefb1818cd0a947a8f3ed3e9ddf2b794c1035ef38d99f3b0bc13c0414d57
```

## Concurrent release baseline, not output validation

- Web run `98`, source `441c39fe914438bf128b117b69b70b7a32be3b2f`, build/test and scan jobs `514516774`/`514516775`, deployment job `514516776`, order `69520737`: previously read jobs SUCCESS; deployment independently read at `2026-09-13T03:12:11.664Z` as Success, one of one batch, one healthy/Success host. Artifact and online bytes were not compared here.
- API run `37` read at `2026-09-13T03:15:20.381Z`, source `e54f579e62d7009ab0177aa1074e095eac4ea16e`: run and build/test/bootJar job `514519669` SUCCESS, deployment job `514519670` SUCCESS. Order `69520789` independently read at `2026-09-13T03:16:02.057Z` as Success, one of one batch, one healthy/Success host. Runtime artifact and business behavior were not verified here.
- Read-only remote refs at approximately 03:16 UTC: API develop `e54f579e62d7009ab0177aa1074e095eac4ea16e`, master `982259abfe333439c062f46d047e1e04276d7cdc`; Web develop `edace747484dc01e39664485ec81b6ae2c1fd7b7`, master `c9cbdccb7ceaa1cecab59bb4f2d6cd441042b2c3`. Web develop already differs from run 98. Integrate concurrent changes into final reviewed candidates and recheck ancestry immediately before push; never overwrite these changes or label their successful runs as this feature's validation.

The local host has no production SSH configuration or either `/usr/local/sbin/cyf-*-flow-deploy` helper. An asynchronous request for the existing production operations entry/configuration path was sent while implementation continues. API/Web Flow access alone does not establish access for output schema migration, private storage/scanner setup, proxy configuration or backup/restore verification. No password was requested.

Follow-up read-only observations:

- At `2026-09-13T03:24:23.688638Z`, Gitee still reported exactly one hook `2096597`, push events enabled, tag-push events disabled, callback SHA256 `9ca0d748ff2f2c1f716dc63bb02bb7465523e970876b630c7782b6efb9aa6895` (legacy pipeline). No branch/filter keys were returned. This does not resolve the effective develop/feature-branch trigger. No hook mutation or test delivery was sent.
- At `2026-09-13T03:43:28.857Z`, Flow `getHostGroup(28833)` identified one Alibaba ECS target: region `cn-shenzhen`, instance `i-wz9j3ip2unzhwij0bs30`, name `chaoyoufan.cn`, private IP `172.18.151.236`. This establishes the deployment target, not OS command access.
- A single correctly constructed read-only ECS `DescribeCloudAssistantStatus` request for that instance returned `Forbidden.RAM`. No ECS command was executed, no RAM permission or credentials were changed, and the denial was not retried. An earlier local SDK constructor mismatch made no API request. Continue through the existing authorized Flow interface for pipeline operations; production host setup still needs the existing operations entry requested above.
