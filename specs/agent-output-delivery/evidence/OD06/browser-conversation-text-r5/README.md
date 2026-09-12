# Real browser output behaviors observed; overall probe not passed

API43e6bb94/Web212bfe4, source CONVERSATION3, output1cb4b8ca6f3a829713d544bce1b25747 version1. Actual desktop1440x900 and mobile simulation390x844 both rendered the highlighted output, displayed exact Markdown preview and downloaded report.md through visible hit-tested CDP mouse clicks. Owner output list/detail/download returned200. Root inspected both screenshots and reread both download files:103 bytes and the same SHA256 as the source. The synthetic Agent remained stopped.

Keep the original observation.json: `succeeded=false`, solely due to `cdp_close`; both viewport observations were collected with no handler error. Root is diagnosing the close-handshake compatibility separately and does not retroactively mark this run passed. `/api/chat/conversation/list` and `/api/phrase/get/random` returned403, while output retrieval succeeded; their authorization/fixture cause is not yet determined.

The tool received independent static APPROVE before live operation. It used a real OAuth JWT injected into an isolated browser profile, not browser login. Mouse-driven mobile emulation is not a physical phone/WeChat touch test. This covers exact standalone resource retrieval, not Hall/bounty/history navigation or the full R1 gate.
