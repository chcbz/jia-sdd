# Codex 历史会话冷归档记录（2026-09-18）

## 范围与保护边界

- 仅处理 `/root/.codex/archived_sessions/` 下的历史 `.jsonl` 会话。
- 未读取、移动、压缩或删除 `/root/.codex/sessions/` 中的活动会话，也未操作会话数据库、项目源码、生产服务、发布制品或证据目录。
- 归档为无损 gzip 冷存储，不做会话内容摘要或丢弃；每条记录保留原始 SHA-256、原始字节数、权限/属主/时间及独立 `.json` sidecar。

## 执行结果

| 指标 | 结果 |
| --- | --- |
| 历史会话文件 | 499 |
| 原始字节 | 1,990,200,740 |
| gzip 冷归档字节 | 481,482,160 |
| 实际释放空间 | 1,506,680,832 bytes（约 1.40 GiB） |
| 压缩后占原始比例 | 24.19% |
| 失败/遗漏 | 0；`archived_sessions` 剩余 `.jsonl` 为 0 |
| 活动会话触碰 | 0 |

归档索引：`/root/.codex/cold_archives/INDEX.json`；批次报告：`/root/.codex/cold_archives/ARCHIVE-20260918-historical-sessions.json`（SHA-256 `ecf6604424ac102c92e428d273d9b5c2d83ce3851cae41d31fe8fb4780d729e0`）。恢复流程沿用 `/root/.codex/cold_archives/RESTORE-ARCHIVES.md`：先流式解压到新临时文件、校验 SHA/长度，再以不覆盖方式恢复原文件；确认恢复前保留 gzip。

## 与当前产品发布的关系

本次冷归档为容量治理，不改变产品行为。当前聚义厅横屏个人中心入口的实际发布状态、源码/制品绑定与线上核验见 `docs/implementation/V1_9_6_HALL_ACCOUNT_ENTRY_RELEASE_20260918.md`。
