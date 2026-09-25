# Fast CHAT 引擎与工具暴露 Spike

日期：2026-09-25
状态：Implementation gate（静态能力复核完成；真实模型负向 prompt 与受控 A/B 尚未执行）

## 现场版本

- Implementation host Codex CLI: `codex-cli 0.153.4`.
- `codex app-server generate-json-schema --experimental` generated 416 schema files / 4,137,012 bytes.
- Deterministic path+content aggregate SHA-256 used by this audit: `01804576862b892c00970c9ce3f70b1c9a95001e0fe906057c258f9ad4fb1a70`.
- The design-time `0.156.0` observation remains historical evidence and is not used as implementation-host capability proof.

## Candidate verdicts

| Candidate | Static evidence | Verdict at this gate |
| --- | --- | --- |
| Existing backend `ChatClient` | `ChatClientConfig` installs task, MCP, skills, agent/domain tools, shell, grep, web fetch and todo tools by default. | Rejected for Fast CHAT unless a separate tool-free builder is introduced and tested. Current bean is not a no-tool path. |
| Existing `codex exec --json` CHAT | Starts a process per request, shares the profile workdir/session, exposes Codex capabilities and currently emits a synthetic intro plus 72-character re-chunking. | Compatibility fallback only. Not the selected fast/safe path. |
| Codex app-server | Schema includes `thread/start`, `turn/start`, `model/list`, `item/agentMessage/delta`, interrupt/steer and explicit server requests for command/file/permission/MCP/dynamic-tool/user-input. Thread/turn parameters expose sandbox and approval policy, but no implementation-host proof of a single switch that removes all built-in tools. | Selected adapter target, labelled **`read-only-constrained`** until runtime readback and negative prompts prove stronger isolation. |
| Direct Responses/provider call | Could avoid Codex tools but requires a separately authorized credential, provider retention/cost policy, model catalog and persona/streaming implementation. | Deferred; no unapproved external paid-call path will be added. |

## Safety decision

1. Product, telemetry and acceptance must use `read-only-constrained`; they must not say “无工具”.
2. `approvalPolicy=never` is not a deny-all control. CHAT safety requires all of:
   - a dedicated empty CHAT workdir;
   - `read-only` sandbox;
   - empty dynamic tools and disabled app/MCP/plugin/skill configuration where the exact runtime supports it;
   - explicit rejection of every server-initiated command, file-change, permissions, MCP, dynamic-tool or network request;
   - no project repository, execution worktree or user attachment mounted into CHAT;
   - runtime event auditing that fails the turn if tool use is observed.
3. The adapter may be implemented behind a disabled feature flag. It may be enabled for one Profile only after the negative prompt matrix proves attempts to shell, read outside the CHAT root, write, network, invoke MCP/plugin/skill/dynamic tools or request permissions are denied and recorded.
4. If the deployed CLI cannot provide this constrained profile, the system falls back to the existing compatibility CHAT path with an explicit fallback reason; it must not silently widen permissions or cost.

## Required remaining evidence

- `initialize`, `account/read`, `model/list`, config/tool-catalog readback from the exact deployment binary and Profile home.
- Negative prompt event log for command, file read/write, network, MCP/plugin/skill/dynamic tool and permission requests.
- One-Profile cold/hot TTFT/final/RSS/CPU/Swap sample.
- Persona and Context Envelope correctness fixture.
- Account usage/rate-limit/cost ownership readback.

No real model call was made by this static spike; therefore it records capability and implementation decisions, not latency or quality results.
