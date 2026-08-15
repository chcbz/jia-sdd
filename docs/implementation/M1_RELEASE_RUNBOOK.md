# M1 Release Runbook — API + codex-ws-agent

> **状态：磁盘门禁已临时清理通过（2026-08-01 17:48 CST）。** 当前 `/dev/vda1` 可用约 5.8 GiB；`jia` 库 data+index 估算约 0.64 GiB，当前空间要求取最小 5 GiB。发布前仍必须重新从第 1 节开始执行 fail-closed 门禁；本文定义获批维护窗口内的操作顺序，不是单独的执行授权。

## 0. 不可绕过的边界

- 禁止从脏主工作树 `/home/isp/wsps/cyf/api` 构建。
- M1 禁止使用 `/home/isp/bin/cyf_api_kit_start.sh`：该脚本会自行 pull/build，不能证明使用锁定集成提交。
- API 唯一允许 source：`/home/isp/wsps/cyf/.worktrees/m1-integration-api`；expected HEAD：`c024126ae297f2a8b31c674d8b6530a8f96db556`。
- codex-ws-agent 唯一允许 source：`/home/isp/wsps/cyf/.worktrees/m1-integration-isp-install`；expected HEAD：`d1a71ccd46809fdc70716fab1f847ca8a24222ad`。
- **第一个生产门禁必须是第 1 节磁盘门禁。** 在它成功前，禁止 Gradle、npm、mysqldump、gzip dump、tar 或任何备份写入；唯一允许的数据库动作是估算大小的只读 `information_schema` 查询。
- 维护窗口必须停写；A08 identity migration/apply 必须先于 A08 runtime；B09 必须重新导出、审核、approve、apply。
- 不自动删除生产数据、sealed audit、identity history 或 smoke 行。任何清理必须使用变更单列出的精确主键并由第二人复核。
- 以下命令只可在已批准维护窗口执行；本轮文档修复不执行这些生产命令。

## 1. 第一门禁：输入、数据库估算与每个文件系统的磁盘检查

以下代码块应在同一个受控 root shell 中执行。目标目录尚不存在时，`nearest_existing_dir` 会向上查找最近存在父目录；门禁通过前不创建目标目录。

```bash
set -euo pipefail
umask 077

die() { printf 'M1 BLOCKED: %s\n' "$*" >&2; exit 1; }

API_SRC=/home/isp/wsps/cyf/.worktrees/m1-integration-api
EXPECTED_API_HEAD=c024126ae297f2a8b31c674d8b6530a8f96db556
AGENT_SRC=/home/isp/wsps/cyf/.worktrees/m1-integration-isp-install
EXPECTED_AGENT_HEAD=d1a71ccd46809fdc70716fab1f847ca8a24222ad
API_DEPLOY_DIR=/home/isp/hosts/cyf/api
AGENT_APP_DIR=/home/isp/apps/codex-ws-agent
API_PORT=10018
CURRENT_JAR="$API_DEPLOY_DIR/cyf-api-kit.jar"

: "${CHANGE_ID:?set approved change ticket}"
: "${MYSQL_DEFAULTS_FILE:?set 0600 DBA MySQL defaults file}"
: "${MYSQL_SOCKET:?set approved production socket}"
: "${DB_NAME:?set production database name}"
: "${APPROVED_PROD_DB_NAME:?set independently approved production schema name}"
: "${BACKUP_DIR:?set backup directory on approved filesystem}"
: "${RELEASE_DIR:?set immutable release artifact directory}"
: "${AGENT_BACKUP_DIR:?set codex-ws-agent rollback backup directory}"
: "${BUILD_ROLLBACK_RESERVE_BYTES:=2147483648}"
: "${API_JVM_ARGS_FILE:?0600 file; one JVM argument per line}"
: "${API_APP_ARGS_FILE:?0600 file; one application argument per line}"
: "${BASE_URL:?old/new API base URL, for example http://127.0.0.1:10018}"
: "${AUTH_HEADER_NAME:?approved auth header name}"
: "${AUTH_HEADER_VALUE:?approved auth header value for scope A and old-version smoke}"
: "${AUTH_B_HEADER_VALUE:?approved auth header value for scope B}"
: "${OLD_SMOKE_AGENT_ID:?known pre-change readable ordinary Agent ID}"
: "${CRITICAL_TABLE_EXPECTATIONS_FILE:?0600 TSV: table_name<TAB>PRESENT|ABSENT for all required drill tables}"

[[ "$CHANGE_ID" =~ ^[A-Za-z0-9._-]+$ ]] || die 'unsafe CHANGE_ID'
[[ "$DB_NAME" =~ ^[A-Za-z0-9_]+$ ]] || die 'unsafe DB_NAME'
[[ "$DB_NAME" == "$APPROVED_PROD_DB_NAME" ]] || die 'DB_NAME is not the approved production schema'
[[ "$MYSQL_SOCKET" == /home/isp/apps/mysql/mysql.sock ]] || die 'unexpected MySQL socket'
[[ -S "$MYSQL_SOCKET" ]] || die 'approved MySQL socket is not a socket'
[[ -f "$MYSQL_DEFAULTS_FILE" ]] || die 'MySQL defaults file missing'
[[ "$(stat -c '%a' "$MYSQL_DEFAULTS_FILE")" == 600 ]] || die 'MySQL defaults file must be mode 0600'
[[ "$BUILD_ROLLBACK_RESERVE_BYTES" =~ ^[0-9]+$ ]] || die 'reserve is not numeric'
(( BUILD_ROLLBACK_RESERVE_BYTES >= 2147483648 )) || die 'reserve must be at least 2 GiB'

for p in "$API_SRC" "$AGENT_SRC" "$API_DEPLOY_DIR" "$AGENT_APP_DIR" "$BACKUP_DIR" "$RELEASE_DIR" "$AGENT_BACKUP_DIR"; do
  [[ "$p" == /* && "$p" != / && "$p" != */ ]] || die "unsafe absolute path: $p"
  [[ "$p" != *$'\n'* && "$p" != *$'\r'* ]] || die "control character in path: $p"
done
[[ "$API_DEPLOY_DIR" == /home/isp/hosts/cyf/api ]] || die 'unexpected API_DEPLOY_DIR'
[[ "$AGENT_APP_DIR" == /home/isp/apps/codex-ws-agent ]] || die 'unexpected AGENT_APP_DIR'
[[ "$BASE_URL" =~ ^https?://[^[:space:]]+$ ]] || die 'unsafe BASE_URL'
[[ "$AUTH_HEADER_NAME" =~ ^[A-Za-z0-9-]+$ ]] || die 'unsafe auth header name'
[[ "$AUTH_HEADER_VALUE" != *$'\n'* && "$AUTH_HEADER_VALUE" != *$'\r'* ]] || die 'unsafe scope A auth value'
[[ "$AUTH_B_HEADER_VALUE" != *$'\n'* && "$AUTH_B_HEADER_VALUE" != *$'\r'* ]] || die 'unsafe scope B auth value'
[[ "$OLD_SMOKE_AGENT_ID" =~ ^[A-Za-z0-9._:-]+$ && "$OLD_SMOKE_AGENT_ID" != builtin-songjiang ]] \
  || die 'unsafe old-version smoke Agent ID'
for f in "$API_JVM_ARGS_FILE" "$API_APP_ARGS_FILE" "$CRITICAL_TABLE_EXPECTATIONS_FILE"; do
  [[ -f "$f" && "$(stat -c '%a' "$f")" == 600 ]] || die "required 0600 input file invalid: $f"
done
JAVA_BIN=/home/isp/apps/jdk21/bin/java
[[ -x "$JAVA_BIN" ]] || die 'Java binary missing'
mapfile -t API_JVM_ARGS < "$API_JVM_ARGS_FILE"
mapfile -t API_APP_ARGS < "$API_APP_ARGS_FILE"
(( ${#API_JVM_ARGS[@]} > 0 && ${#API_APP_ARGS[@]} > 0 )) || die 'empty API argument file'
for arg in "${API_JVM_ARGS[@]}" "${API_APP_ARGS[@]}"; do
  [[ -n "$arg" && "$arg" != *$'\n'* && "$arg" != *$'\r'* ]] || die 'blank/control API launch argument'
done
A=(-H "$AUTH_HEADER_NAME: $AUTH_HEADER_VALUE" -H 'Content-Type: application/json')
B=(-H "$AUTH_HEADER_NAME: $AUTH_B_HEADER_VALUE" -H 'Content-Type: application/json')

MYSQL=(/home/isp/apps/mysql/bin/mysql --defaults-extra-file="$MYSQL_DEFAULTS_FILE" \
  --protocol=SOCKET --socket="$MYSQL_SOCKET" --default-character-set=utf8mb4)
MYSQLDUMP=(/home/isp/apps/mysql/bin/mysqldump --defaults-extra-file="$MYSQL_DEFAULTS_FILE" \
  --protocol=SOCKET --socket="$MYSQL_SOCKET" --default-character-set=utf8mb4)

nearest_existing_dir() {
  local candidate="$1" parent
  while [[ ! -e "$candidate" ]]; do
    parent="$(dirname -- "$candidate")"
    [[ "$parent" != "$candidate" ]] || die "no existing parent for $1"
    candidate="$parent"
  done
  [[ -d "$candidate" ]] || candidate="$(dirname -- "$candidate")"
  [[ -d "$candidate" ]] || die "filesystem probe is not a directory: $candidate"
  printf '%s\n' "$candidate"
}

run_disk_gate() {
  local phase="$1" estimated_db_bytes required_bytes disk_report disk_failed
  local spec label target probe device_id source mountpoint free_bytes
  local -A fs_seen=()
  [[ "$phase" =~ ^[A-Za-z0-9._-]+$ ]] || die 'unsafe disk-gate phase'

  # 门禁前唯一允许的生产 DB 操作：只读估算 data+index bytes。
  estimated_db_bytes="$("${MYSQL[@]}" "$DB_NAME" --batch --raw --skip-column-names -e \
    "SELECT COALESCE(SUM(data_length + index_length),0)
       FROM information_schema.tables
      WHERE table_schema = DATABASE();")"
  [[ "$estimated_db_bytes" =~ ^[0-9]+$ ]] || die 'database size estimate is not numeric'

  required_bytes="$(python3 - "$estimated_db_bytes" "$BUILD_ROLLBACK_RESERVE_BYTES" <<'PY'
import sys
estimated, reserve = map(int, sys.argv[1:])
minimum = 5 * 1024**3
required = max(minimum, 2 * estimated + reserve)
if required < 0:
    raise SystemExit('invalid required bytes')
print(required)
PY
)"
  [[ "$required_bytes" =~ ^[0-9]+$ ]] || die 'calculated disk threshold is not numeric'

  # 对七个构建/写入/恢复目标所在的每个不同 st_dev 分别检查；同一文件系统只比较一次，
  # 但保留全部路径映射证据。
  disk_report=''
  disk_failed=0
  for spec in \
    "API_SRC|$API_SRC" \
    "AGENT_SRC|$AGENT_SRC" \
    "RELEASE_DIR|$RELEASE_DIR" \
    "BACKUP_DIR|$BACKUP_DIR" \
    "API_DEPLOY_DIR|$API_DEPLOY_DIR" \
    "AGENT_APP_DIR|$AGENT_APP_DIR" \
    "AGENT_BACKUP_DIR|$AGENT_BACKUP_DIR"; do
    label=${spec%%|*}
    target=${spec#*|}
    probe="$(nearest_existing_dir "$target")"
    device_id="$(stat -Lc '%d' "$probe")"
    source="$(df --output=source "$probe" | awk 'NR==2 {sub(/^[[:space:]]+/, ""); print}')"
    mountpoint="$(df --output=target "$probe" | awk 'NR==2 {sub(/^[[:space:]]+/, ""); print}')"
    free_bytes="$(df -B1 --output=avail "$probe" | awk 'NR==2 {print $1}')"
    [[ -n "$source" && -n "$mountpoint" && "$device_id" =~ ^[0-9]+$ && "$free_bytes" =~ ^[0-9]+$ ]] \
      || die "invalid df/stat result for $target"
    disk_report+="phase=$phase target=$label path=$target probe=$probe device_id=$device_id source=$source mount=$mountpoint free=$free_bytes required=$required_bytes"$'\n'
    if [[ -z "${fs_seen[$device_id]+set}" ]]; then
      fs_seen[$device_id]=1
      if (( free_bytes < required_bytes )); then
        disk_failed=1
      fi
    fi
  done
  printf '%s' "$disk_report"
  (( disk_failed == 0 )) || die 'one or more required filesystems are below the disk threshold'

  # 只有全部不同文件系统通过后才允许创建目录并持久化门禁证据。
  install -d -m 0700 "$BACKUP_DIR" "$RELEASE_DIR" "$AGENT_BACKUP_DIR"
  printf 'estimated_db=%s required=%s reserve=%s\n%s' \
    "$estimated_db_bytes" "$required_bytes" "$BUILD_ROLLBACK_RESERVE_BYTES" "$disk_report" \
    > "$BACKUP_DIR/${CHANGE_ID}.disk-gate.${phase}.txt"
}

run_disk_gate initial
```

门禁公式是 `free space >= max(5 GiB, 2 * estimated database bytes + build/rollback reserve)`，reserve 不得小于 2 GiB；API/agent source、release、backup、API deploy、agent live app 与 agent backup 七个路径均提供映射证据，覆盖 Gradle、npm、dump、备份和 tar restore 的写目标。**2026-07-29 已知约 2.2 GiB 的环境必须在本节退出；不得继续到 Gradle/npm/dump/tar。** 不得删除未知文件、stash、worktree 或数据库历史来绕过门禁。

## 2. 锁定 clean source 并构建可追溯 JAR

```bash
[[ -d "$API_SRC/.git" || -f "$API_SRC/.git" ]] || die 'API source is not a worktree'
[[ -d "$AGENT_SRC/.git" || -f "$AGENT_SRC/.git" ]] || die 'agent source is not a worktree'
[[ -z "$(git -C "$API_SRC" status --porcelain)" ]] || die 'API worktree is dirty'
[[ "$(git -C "$API_SRC" rev-parse HEAD)" == "$EXPECTED_API_HEAD" ]] || die 'API HEAD mismatch'
[[ -z "$(git -C "$AGENT_SRC" status --porcelain)" ]] || die 'agent worktree is dirty'
[[ "$(git -C "$AGENT_SRC" rev-parse HEAD)" == "$EXPECTED_AGENT_HEAD" ]] || die 'agent HEAD mismatch'

cd "$API_SRC"
flock /tmp/cyf-gradle.lock bash ./gradlew \
  :agent:jia-agent-mapper:test :agent:jia-agent-service:test \
  :chat:jia-chat-mapper:test :chat:jia-chat-service:test \
  :chat-starter:compileJava :starter:compileJava \
  --no-daemon -Dorg.gradle.workers.max=1 \
  -Dorg.gradle.jvmargs='-Xmx384m -Dfile.encoding=UTF-8'

flock /tmp/cyf-gradle.lock bash ./gradlew :starter:bootJar \
  --no-daemon -Dorg.gradle.workers.max=1 \
  -Dorg.gradle.jvmargs='-Xmx384m -Dfile.encoding=UTF-8'

mapfile -t JARS < <(find "$API_SRC/starter/build/libs" -maxdepth 1 -type f -name '*.jar' ! -name '*-plain.jar')
[[ "${#JARS[@]}" -eq 1 ]] || die 'expected exactly one boot JAR'
JAR=${JARS[0]}
ARTIFACT="$RELEASE_DIR/cyf-api-kit-${EXPECTED_API_HEAD}.jar"
install -m 0644 "$JAR" "$ARTIFACT.tmp"
mv "$ARTIFACT.tmp" "$ARTIFACT"
sha256sum "$ARTIFACT" | tee "$ARTIFACT.sha256"
stat -c '%s %n' "$ARTIFACT" | tee "$ARTIFACT.size"
printf '%s\n' "$EXPECTED_API_HEAD" > "$ARTIFACT.git-head"
```

变更单保存 JAR path、Git HEAD、SHA-256、size、构建命令和测试结果。部署只复制此 immutable artifact，禁止现场重新构建。

## 3. 真实停写断言、完整备份与账户证据

### 3.1 在停写前定义并验证旧栈启停/进程函数与只读 smoke

以下函数和旧版本 smoke 输入是 rollback prerequisite，必须在任何 schema migration 前定义。`agent_pids` 不依赖 systemd/tmux wrapper：它遍历 `/proc`，识别 node argv 中 basename 为 `agent-client.mjs` 的参数；绝对参数直接 `realpath`，相对参数按 `/proc/$pid/cwd` 解析，并以 cwd+basename 做竞态下的 fail-closed fallback。发现两个或更多 writer 立即阻断。

```bash
api_pids() {
  python3 - "$CURRENT_JAR" <<'PY'
import pathlib, sys
jar = sys.argv[1]
for entry in pathlib.Path('/proc').iterdir():
    if not entry.name.isdigit():
        continue
    try:
        argv = (entry / 'cmdline').read_bytes().split(b'\0')
    except (FileNotFoundError, PermissionError, ProcessLookupError):
        continue
    args = [x.decode('utf-8', 'surrogateescape') for x in argv if x]
    for i, arg in enumerate(args[:-1]):
        if arg == '-jar' and args[i + 1] == jar:
            print(entry.name)
            break
PY
}

agent_pids() {
  python3 - "$AGENT_APP_DIR/agent-client.mjs" <<'PY'
import os, pathlib, sys

target = pathlib.Path(os.path.realpath(sys.argv[1]))
target_parent = target.parent
for proc in pathlib.Path('/proc').iterdir():
    if not proc.name.isdigit():
        continue
    try:
        raw = (proc / 'cmdline').read_bytes().split(b'\0')
        args = [x.decode('utf-8', 'surrogateescape') for x in raw if x]
    except (FileNotFoundError, PermissionError, ProcessLookupError):
        continue
    if not args:
        continue
    try:
        exe_name = pathlib.Path(os.readlink(proc / 'exe')).name
    except (FileNotFoundError, PermissionError, ProcessLookupError, OSError):
        exe_name = pathlib.Path(args[0]).name
    if not (exe_name == 'node' or exe_name.startswith('node')):
        continue
    try:
        cwd_raw = os.readlink(proc / 'cwd')
        deleted_suffix = ' (deleted)'
        if cwd_raw.endswith(deleted_suffix):
            cwd_raw = cwd_raw[:-len(deleted_suffix)]
        cwd = pathlib.Path(os.path.realpath(cwd_raw))
    except (FileNotFoundError, PermissionError, ProcessLookupError, OSError):
        cwd = None
    matched = False
    unresolved_relative = False
    for arg in args[1:]:
        if pathlib.PurePath(arg).name != target.name:
            continue
        if os.path.isabs(arg):
            matched = pathlib.Path(os.path.realpath(arg)) == target
        elif cwd is not None:
            candidate = pathlib.Path(os.path.realpath(cwd / arg))
            matched = candidate == target or (cwd == target_parent and pathlib.PurePath(arg).name == target.name)
        else:
            unresolved_relative = True
        if matched:
            break
    # 如果相对 argv 已读到、cwd 恰在随后消失但 PID 仍存在，宁可作为可疑 writer 阻断。
    if not matched and unresolved_relative and proc.exists():
        matched = True
    if matched:
        print(proc.name)
PY
}

assert_api_stopped() {
  mapfile -t remaining < <(api_pids)
  (( ${#remaining[@]} == 0 )) || die "API process still running: ${remaining[*]}"
  [[ -z "$(ss -H -ltn "sport = :$API_PORT")" ]] || die "API port $API_PORT still listening"
}

assert_agent_stopped() {
  mapfile -t remaining < <(agent_pids)
  (( ${#remaining[@]} == 0 )) || die "codex-ws-agent writer still running: ${remaining[*]}"
}

assert_at_most_one_agent_writer() {
  mapfile -t writers < <(agent_pids)
  (( ${#writers[@]} <= 1 )) || die "duplicate codex-ws-agent writers: ${writers[*]}"
}

assert_one_agent_writer() {
  mapfile -t writers < <(agent_pids)
  (( ${#writers[@]} == 1 )) || die "expected exactly one codex-ws-agent writer, found: ${writers[*]:-none}"
}

stop_api_exact() {
  local pid
  mapfile -t pids < <(api_pids)
  (( ${#pids[@]} <= 1 )) || die "multiple exact API processes found: ${pids[*]}"
  if (( ${#pids[@]} == 1 )); then
    pid=${pids[0]}
    kill -TERM "$pid" || die "kill -TERM failed for API pid $pid"
    for _ in $(seq 1 60); do
      [[ ! -e "/proc/$pid" ]] && break
      sleep 1
    done
    [[ ! -e "/proc/$pid" ]] || die "API pid $pid did not exit after 60 seconds"
  fi
  assert_api_stopped
}

start_api_exact() {
  local log_file pid
  assert_api_stopped
  [[ -s "$CURRENT_JAR" ]] || die 'deployment JAR missing'
  log_file="$API_DEPLOY_DIR/logs/startlog_$(date +%Y%m%d_%H%M%S).log"
  install -d -m 0750 "$API_DEPLOY_DIR/logs"
  nohup setsid "$JAVA_BIN" "${API_JVM_ARGS[@]}" -jar "$CURRENT_JAR" \
    "${API_APP_ARGS[@]}" > "$log_file" 2>&1 < /dev/null &
  pid=$!
  sleep 5
  [[ -e "/proc/$pid" ]] || { tail -n 80 "$log_file" >&2 || true; die 'API failed to start'; }
  mapfile -t started < <(api_pids)
  (( ${#started[@]} == 1 && started[0] == pid )) || die 'started API does not match exact JAR process'
  printf '%s\n' "$pid" > "$API_DEPLOY_DIR/cyf-api-kit.pid"
}

assert_success_envelope() {
  local body="$1"
  python3 - "$body" <<'PY'
import json, pathlib, sys
obj=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
if not isinstance(obj,dict) or obj.get('status') != 200 or obj.get('code') != 'E0':
    raise SystemExit(f'invalid success envelope: {obj!r}')
PY
}

for fn in api_pids agent_pids assert_api_stopped assert_agent_stopped \
          assert_at_most_one_agent_writer assert_one_agent_writer \
          stop_api_exact start_api_exact assert_success_envelope; do
  declare -F "$fn" >/dev/null || die "rollback function missing: $fn"
done

# 旧版本恢复 smoke 所需 ID 必须在停 API 和任何迁移前，以当前旧应用做只读验证。
OLD_SMOKE_PREFLIGHT_RESPONSE="$BACKUP_DIR/${CHANGE_ID}.old-smoke-preflight.json"
curl --fail --silent --show-error "${A[@]}" \
  "$BASE_URL/agent/$OLD_SMOKE_AGENT_ID" > "$OLD_SMOKE_PREFLIGHT_RESPONSE"
python3 - "$OLD_SMOKE_PREFLIGHT_RESPONSE" "$OLD_SMOKE_AGENT_ID" <<'PY'
import json, pathlib, sys
obj=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
if not isinstance(obj,dict) or obj.get('status') != 200 or obj.get('code') != 'E0':
    raise SystemExit(f'old-version preflight failed: {obj!r}')
data=obj.get('data')
if not isinstance(data,dict) or data.get('agentId') != sys.argv[2] or data.get('systemAgent') is True:
    raise SystemExit('old-version smoke Agent missing, aliased unexpectedly, or system-only')
PY
sha256sum "$OLD_SMOKE_PREFLIGHT_RESPONSE" > "$OLD_SMOKE_PREFLIGHT_RESPONSE.sha256"

# wrapper 只负责请求停止；/proc writer 检测才是最终门禁。
[[ -x /home/isp/bin/codex_ws_agent_start.sh ]] || die 'agent service script missing'
assert_at_most_one_agent_writer
if ! /home/isp/bin/codex_ws_agent_start.sh stop; then
  die 'codex-ws-agent stop command failed'
fi
assert_agent_stopped
stop_api_exact
```

### 3.2 active modifying transaction 必须严格为零

下面查询排除本次只读检查连接自身；其他连接只有当前执行修改/锁写语句或已有 `trx_rows_modified > 0` 才计为 modifying。普通只读查询不会误算，但任何其他未提交修改行都会进入总数。shell 必须同时断言 `modifying_transaction_count=0` 和 `rows_modified=0`，不能只打印。

```bash
assert_no_modifying_transactions() {
  local phase="$1" tx_summary modifying_trx_count modified_rows extra
  [[ "$phase" =~ ^[A-Za-z0-9._-]+$ ]] || die 'unsafe transaction-check phase'
  tx_summary="$("${MYSQL[@]}" "$DB_NAME" --batch --raw --skip-column-names -e "
SELECT
  COALESCE(SUM(CASE
    WHEN COALESCE(t.trx_rows_modified,0) > 0 THEN 1
    WHEN p.COMMAND <> 'Sleep' AND (
      REGEXP_LIKE(COALESCE(p.INFO,''),
        '^[[:space:]]*(INSERT|UPDATE|DELETE|REPLACE|LOAD|CALL|CREATE|ALTER|DROP|TRUNCATE|RENAME|GRANT|REVOKE|LOCK|UNLOCK|SET[[:space:]]+GLOBAL)', 'i')
      OR REGEXP_LIKE(COALESCE(p.INFO,''),
        '[[:space:]]FOR[[:space:]]+UPDATE([[:space:]]|$)|LOCK[[:space:]]+IN[[:space:]]+SHARE[[:space:]]+MODE', 'i')
    ) THEN 1 ELSE 0 END),0) AS modifying_transaction_count,
  COALESCE(SUM(COALESCE(t.trx_rows_modified,0)),0) AS rows_modified
FROM information_schema.processlist p
LEFT JOIN information_schema.innodb_trx t
  ON t.trx_mysql_thread_id = p.ID
WHERE p.ID <> CONNECTION_ID();")"
  [[ "$tx_summary" != *$'\n'* ]] || die 'transaction query returned multiple rows'
  IFS=$'\t' read -r modifying_trx_count modified_rows extra <<< "$tx_summary"
  [[ -z "${extra:-}" && "$modifying_trx_count" =~ ^[0-9]+$ && "$modified_rows" =~ ^[0-9]+$ ]] \
    || die "invalid transaction summary: $tx_summary"
  (( modifying_trx_count == 0 )) || die "active modifying transactions: $modifying_trx_count"
  (( modified_rows == 0 )) || die "uncommitted modified rows: $modified_rows"
  printf 'modifying_transaction_count=%s rows_modified=%s\n' \
    "$modifying_trx_count" "$modified_rows" \
    | tee "$BACKUP_DIR/${CHANGE_ID}.${phase}.write-quiescence.txt"
}

assert_no_modifying_transactions pre-backup
```

### 3.3 schema 元数据、精确行数、B09 系统账户与完整 dump

`mysqldump` 必须带 `--routines --triggers --events`。业务 schema dump 不包含 `mysql.user`/grant 系统对象，因此变更前另存 B09 definer/operator 的 `SHOW CREATE USER` 与全部 `SHOW GRANTS`，并生成精确账户恢复 SQL。该证据目录为 `0700`，文件保持 `0600`。

```bash
SCHEMA_META="$BACKUP_DIR/${CHANGE_ID}.schema-meta.tsv"
"${MYSQL[@]}" --batch --raw --skip-column-names -e "
SELECT default_character_set_name, default_collation_name
FROM information_schema.schemata
WHERE schema_name='$DB_NAME';" > "$SCHEMA_META"
[[ "$(wc -l < "$SCHEMA_META")" -eq 1 ]] || die 'schema charset/collation lookup failed'
IFS=$'\t' read -r ORIGINAL_DB_CHARSET ORIGINAL_DB_COLLATION < "$SCHEMA_META"
[[ "$ORIGINAL_DB_CHARSET" =~ ^[A-Za-z0-9_]+$ ]] || die 'unsafe original charset'
[[ "$ORIGINAL_DB_COLLATION" =~ ^[A-Za-z0-9_]+$ ]] || die 'unsafe original collation'

exact_row_counts() {
  local output="$1" table count
  : > "$output"
  while IFS= read -r table; do
    [[ "$table" =~ ^[A-Za-z0-9_$]+$ ]] || die "unsafe table name: $table"
    count="$("${MYSQL[@]}" "$DB_NAME" --batch --raw --skip-column-names \
      -e "SELECT COUNT(*) FROM \`$table\`;")"
    [[ "$count" =~ ^[0-9]+$ ]] || die "invalid row count for $table"
    printf '%s\t%s\n' "$table" "$count" >> "$output"
  done < <("${MYSQL[@]}" --batch --raw --skip-column-names -e "
    SELECT table_name FROM information_schema.tables
    WHERE table_schema='$DB_NAME' AND table_type='BASE TABLE'
    ORDER BY BINARY table_name;")
  [[ -s "$output" ]] || die 'no base-table row counts captured'
}

PRE_ROW_COUNTS="$BACKUP_DIR/${CHANGE_ID}.pre-row-counts.tsv"
exact_row_counts "$PRE_ROW_COUNTS"

: "${B09_OPERATOR_USER:?approved B09 operator account name}"
: "${B09_OPERATOR_HOST:?approved B09 operator account host}"
[[ "$B09_OPERATOR_USER" =~ ^[A-Za-z0-9_.%-]+$ ]] || die 'unsafe B09 operator user'
[[ "$B09_OPERATOR_HOST" =~ ^[A-Za-z0-9_.%-]+$ ]] || die 'unsafe B09 operator host'
ACCOUNT_EVIDENCE_DIR="$BACKUP_DIR/${CHANGE_ID}.mysql-accounts"
install -d -m 0700 "$ACCOUNT_EVIDENCE_DIR"

snapshot_mysql_account() {
  local user="$1" host="$2" stem="$3" exists create_tsv grants_tsv restore_sql
  create_tsv="$ACCOUNT_EVIDENCE_DIR/$stem.show-create.tsv"
  grants_tsv="$ACCOUNT_EVIDENCE_DIR/$stem.show-grants.tsv"
  restore_sql="$ACCOUNT_EVIDENCE_DIR/$stem.restore.sql"
  exists="$("${MYSQL[@]}" --batch --raw --skip-column-names -e \
    "SELECT COUNT(*) FROM mysql.user WHERE User='$user' AND Host='$host';")"
  [[ "$exists" == 0 || "$exists" == 1 ]] || die "ambiguous account state for $user@$host"
  if [[ "$exists" == 1 ]]; then
    "${MYSQL[@]}" --batch --raw --skip-column-names \
      -e "SHOW CREATE USER '$user'@'$host';" > "$create_tsv"
    "${MYSQL[@]}" --batch --raw --skip-column-names \
      -e "SHOW GRANTS FOR '$user'@'$host';" > "$grants_tsv"
  else
    : > "$create_tsv"
    : > "$grants_tsv"
  fi
  python3 - "$user" "$host" "$exists" "$create_tsv" "$grants_tsv" "$restore_sql" <<'PY'
import pathlib, re, sys
user, host, exists, create_path, grants_path, out_path = sys.argv[1:]
if not re.fullmatch(r'[A-Za-z0-9_.%-]+', user + host):
    raise SystemExit('unsafe account')
lines = [f"DROP USER IF EXISTS '{user}'@'{host}';"]
if exists == '1':
    raw = pathlib.Path(create_path).read_text(encoding='utf-8').splitlines()
    if len(raw) != 1 or '\t' not in raw[0]:
        raise SystemExit('invalid SHOW CREATE USER output')
    create_stmt = raw[0].split('\t', 1)[1].rstrip(';')
    if not create_stmt.startswith('CREATE USER '):
        raise SystemExit('unexpected CREATE USER statement')
    lines.append(create_stmt + ';')
    grants = pathlib.Path(grants_path).read_text(encoding='utf-8').splitlines()
    if not grants:
        raise SystemExit('missing SHOW GRANTS output')
    for grant in grants:
        if not grant.startswith(('GRANT ', 'REVOKE ')):
            raise SystemExit('unexpected grant statement')
        lines.append(grant.rstrip(';') + ';')
pathlib.Path(out_path).write_text('\n'.join(lines) + '\n', encoding='utf-8')
PY
  chmod 0600 "$create_tsv" "$grants_tsv" "$restore_sql"
}

snapshot_mysql_account cyf_b09_definer localhost b09-definer
snapshot_mysql_account "$B09_OPERATOR_USER" "$B09_OPERATOR_HOST" b09-operator
ACCOUNT_EVIDENCE_SHA="$BACKUP_DIR/${CHANGE_ID}.mysql-accounts.sha256"
sha256sum "$ACCOUNT_EVIDENCE_DIR"/* > "$ACCOUNT_EVIDENCE_SHA"

DUMP="$BACKUP_DIR/${DB_NAME}-${CHANGE_ID}-$(date -u +%Y%m%dT%H%M%SZ).sql.gz"
"${MYSQLDUMP[@]}" \
  --single-transaction --quick --routines --triggers --events --hex-blob \
  --set-gtid-purged=OFF --no-tablespaces --add-drop-table \
  "$DB_NAME" | gzip -1 > "$DUMP.tmp"
[[ -s "$DUMP.tmp" ]] || die 'dump is empty'
mv "$DUMP.tmp" "$DUMP"
gzip -t "$DUMP"
sha256sum "$DUMP" | tee "$DUMP.sha256"
stat -c '%s %n' "$DUMP" | tee "$DUMP.size"

# 完整消费 gzip 流，避免 pipefail 下 gzip 因搜索消费者提前退出而产生 SIGPIPE 假失败。
gzip -cd "$DUMP" | awk '/agent_task_meta/ {found=1} END {exit found ? 0 : 1}' \
  || die 'full dump does not reference agent_task_meta'

PRE_SCHEMA_DUMP="$BACKUP_DIR/${CHANGE_ID}.pre-schema.sql"
"${MYSQLDUMP[@]}" --no-data --routines --triggers --events --skip-comments \
  --set-gtid-purged=OFF --no-tablespaces "$DB_NAME" > "$PRE_SCHEMA_DUMP"
[[ -s "$PRE_SCHEMA_DUMP" ]] || die 'pre-change schema dump is empty'
sha256sum "$PRE_SCHEMA_DUMP" | tee "$PRE_SCHEMA_DUMP.sha256"
```

### 3.4 迁移前创建并验证全部 rollback prerequisites

关键表 expectation 文件必须恰好覆盖下列 14 张表，每行 `table_name<TAB>PRESENT|ABSENT`，不得有空行、注释、重复或额外表。旧版本尚未具备的 B07/B09 表必须显式标 `ABSENT`；不能通过“查询不到就跳过”推断可选性。

```text
agent_identity_registry
agent_identity_alias
agent_runtime
agent_persona_binding
agent_task_meta
agent_task_member
agent_task_work_item
agent_task_thread
chat_conversation
chat_message
agent_task_backfill_issue
agent_task_backfill_manifest_batch
agent_task_backfill_manifest
agent_task_backfill_run
```

```bash
CRITICAL_TABLE_EXPECTATIONS="$BACKUP_DIR/${CHANGE_ID}.critical-table-expectations.tsv"
python3 - "$CRITICAL_TABLE_EXPECTATIONS_FILE" "$CRITICAL_TABLE_EXPECTATIONS" <<'PY'
import pathlib, sys
required = {
    'agent_identity_registry', 'agent_identity_alias', 'agent_runtime',
    'agent_persona_binding', 'agent_task_meta', 'agent_task_member',
    'agent_task_work_item', 'agent_task_thread', 'chat_conversation',
    'chat_message', 'agent_task_backfill_issue',
    'agent_task_backfill_manifest_batch', 'agent_task_backfill_manifest',
    'agent_task_backfill_run',
}
raw = pathlib.Path(sys.argv[1]).read_text(encoding='utf-8').splitlines()
if not raw or any(not line for line in raw):
    raise SystemExit('critical-table expectation list is empty or contains blank lines')
parsed = {}
for line in raw:
    parts = line.split('\t')
    if len(parts) != 2:
        raise SystemExit(f'invalid expectation row: {line!r}')
    table, expectation = parts
    if table in parsed:
        raise SystemExit(f'duplicate expectation: {table}')
    if expectation not in {'PRESENT', 'ABSENT'}:
        raise SystemExit(f'invalid expectation for {table}: {expectation}')
    parsed[table] = expectation
if set(parsed) != required:
    raise SystemExit(f'expectation set mismatch: missing={sorted(required-set(parsed))}, extra={sorted(set(parsed)-required)}')
if not any(value == 'PRESENT' for value in parsed.values()):
    raise SystemExit('critical-table expectation list has no PRESENT tables')
out = ''.join(f'{table}\t{parsed[table]}\n' for table in sorted(parsed))
pathlib.Path(sys.argv[2]).write_text(out, encoding='utf-8')
PY
chmod 0600 "$CRITICAL_TABLE_EXPECTATIONS"
[[ "$(wc -l < "$CRITICAL_TABLE_EXPECTATIONS")" -eq 14 ]] || die 'critical expectation count is not 14'

capture_critical_table_counts() {
  local schema="$1" output="$2" table expectation extra exists count
  [[ "$schema" =~ ^[A-Za-z0-9_]+$ ]] || die "unsafe critical-count schema: $schema"
  : > "$output"
  while IFS=$'\t' read -r table expectation extra; do
    [[ -z "${extra:-}" && "$table" =~ ^[A-Za-z0-9_]+$ ]] || die "invalid normalized critical table row: $table"
    exists="$("${MYSQL[@]}" --batch --raw --skip-column-names -e \
      "SELECT COUNT(*) FROM information_schema.tables
        WHERE table_schema='$schema' AND table_name='$table' AND table_type='BASE TABLE';")"
    [[ "$exists" == 0 || "$exists" == 1 ]] || die "ambiguous table existence: $schema.$table"
    if [[ "$expectation" == PRESENT ]]; then
      [[ "$exists" == 1 ]] || die "expected table missing: $schema.$table"
      count="$("${MYSQL[@]}" "$schema" --batch --raw --skip-column-names \
        -e "SELECT COUNT(*) FROM \`$table\`;")"
      [[ "$count" =~ ^[0-9]+$ ]] || die "invalid exact row count: $schema.$table"
      printf '%s\tPRESENT\t%s\n' "$table" "$count" >> "$output"
    elif [[ "$expectation" == ABSENT ]]; then
      [[ "$exists" == 0 ]] || die "table expected ABSENT but exists: $schema.$table"
      printf '%s\tABSENT\t-\n' "$table" >> "$output"
    else
      die "unknown normalized expectation: $expectation"
    fi
  done < "$CRITICAL_TABLE_EXPECTATIONS"
  LC_ALL=C sort -o "$output" "$output"
  [[ "$(wc -l < "$output")" -eq 14 && -s "$output" ]] || die 'critical table state output is incomplete'
}

write_present_check_sql() {
  local output="$1"
  python3 - "$CRITICAL_TABLE_EXPECTATIONS" "$output" <<'PY'
import pathlib, sys
present=[]
for line in pathlib.Path(sys.argv[1]).read_text(encoding='utf-8').splitlines():
    table, expectation=line.split('\t')
    if expectation == 'PRESENT':
        present.append(table)
if not present:
    raise SystemExit('no expected-present tables for CHECK TABLE')
pathlib.Path(sys.argv[2]).write_text(
    'CHECK TABLE ' + ', '.join(f'`{table}`' for table in present) + ';\n', encoding='utf-8')
PY
  [[ -s "$output" ]] || die 'dynamic CHECK TABLE SQL is empty'
}

verify_present_check_output() {
  local output="$1"
  python3 - "$CRITICAL_TABLE_EXPECTATIONS" "$output" <<'PY'
import pathlib, sys
expectations=[]
for line in pathlib.Path(sys.argv[1]).read_text(encoding='utf-8').splitlines():
    table, expectation=line.split('\t')
    if expectation == 'PRESENT':
        expectations.append(table)
if not expectations or len(expectations) != len(set(expectations)):
    raise SystemExit('invalid expected-present table set')
rows=[line.split('\t') for line in pathlib.Path(sys.argv[2]).read_text(encoding='utf-8').splitlines()]
if not rows or rows[0] != ['Table', 'Op', 'Msg_type', 'Msg_text']:
    raise SystemExit('CHECK TABLE output header is missing or unexpected')
actual=[]
for row in rows[1:]:
    if len(row) != 4 or row[1:] != ['check', 'status', 'OK']:
        raise SystemExit(f'unexpected CHECK TABLE row: {row!r}')
    table=row[0].rsplit('.', 1)[-1].strip('`')
    if not table:
        raise SystemExit(f'empty CHECK TABLE table name: {row!r}')
    actual.append(table)
if len(actual) != len(set(actual)) or sorted(actual) != sorted(expectations):
    raise SystemExit(f'CHECK TABLE set mismatch: expected={sorted(expectations)!r}, actual={sorted(actual)!r}')
PY
}

PRE_CRITICAL_ROW_COUNTS="$BACKUP_DIR/${CHANGE_ID}.pre-critical-row-counts.tsv"
capture_critical_table_counts "$DB_NAME" "$PRE_CRITICAL_ROW_COUNTS"

# 旧 JAR 和完整旧 agent app/config tar 必须在任何迁移前创建。
ROLLBACK_JAR="$RELEASE_DIR/cyf-api-kit-before-${CHANGE_ID}.jar"
[[ -s "$CURRENT_JAR" ]] || die 'current old API JAR missing before migration'
install -m 0644 "$CURRENT_JAR" "$ROLLBACK_JAR"
sha256sum "$ROLLBACK_JAR" > "$ROLLBACK_JAR.sha256"
sha256sum -c "$ROLLBACK_JAR.sha256"

AGENT_BACKUP_TAR="$AGENT_BACKUP_DIR/codex-ws-agent-${CHANGE_ID}.tgz"
[[ -d "$AGENT_APP_DIR" && -f "$AGENT_APP_DIR/agent-client.mjs" ]] \
  || die 'old codex-ws-agent app/config tree missing before migration'
assert_agent_stopped
tar --xattrs --acls -C /home/isp/apps -czf "$AGENT_BACKUP_TAR" codex-ws-agent
[[ -s "$AGENT_BACKUP_TAR" ]] || die 'old agent backup tar is empty'
gzip -t "$AGENT_BACKUP_TAR"
sha256sum "$AGENT_BACKUP_TAR" > "$AGENT_BACKUP_TAR.sha256"
sha256sum -c "$AGENT_BACKUP_TAR.sha256"
python3 - "$AGENT_BACKUP_TAR" <<'PY'
import pathlib, sys, tarfile
with tarfile.open(sys.argv[1], 'r:gz') as tf:
    members=tf.getmembers()
    if not members:
        raise SystemExit('empty agent backup')
    for member in members:
        p=pathlib.PurePosixPath(member.name)
        if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0] != 'codex-ws-agent':
            raise SystemExit(f'unsafe agent tar member: {member.name!r}')
PY

ROLLBACK_API_JVM_ARGS_FILE="$BACKUP_DIR/${CHANGE_ID}.old-api-jvm-args"
ROLLBACK_API_APP_ARGS_FILE="$BACKUP_DIR/${CHANGE_ID}.old-api-app-args"
install -m 0600 "$API_JVM_ARGS_FILE" "$ROLLBACK_API_JVM_ARGS_FILE"
install -m 0600 "$API_APP_ARGS_FILE" "$ROLLBACK_API_APP_ARGS_FILE"
ROLLBACK_API_ARGS_SHA="$BACKUP_DIR/${CHANGE_ID}.old-api-args.sha256"
sha256sum "$ROLLBACK_API_JVM_ARGS_FILE" "$ROLLBACK_API_APP_ARGS_FILE" > "$ROLLBACK_API_ARGS_SHA"
sha256sum -c "$ROLLBACK_API_ARGS_SHA"

ROLLBACK_DB_EVIDENCE_SHA="$BACKUP_DIR/${CHANGE_ID}.rollback-db-evidence.sha256"
sha256sum "$SCHEMA_META" "$PRE_ROW_COUNTS" "$CRITICAL_TABLE_EXPECTATIONS" \
  "$PRE_CRITICAL_ROW_COUNTS" > "$ROLLBACK_DB_EVIDENCE_SHA"
sha256sum -c "$ROLLBACK_DB_EVIDENCE_SHA"
sha256sum -c "$ACCOUNT_EVIDENCE_SHA"

load_rollback_runtime_context() {
  sha256sum -c "$ROLLBACK_API_ARGS_SHA"
  mapfile -t API_JVM_ARGS < "$ROLLBACK_API_JVM_ARGS_FILE"
  mapfile -t API_APP_ARGS < "$ROLLBACK_API_APP_ARGS_FILE"
  (( ${#API_JVM_ARGS[@]} > 0 && ${#API_APP_ARGS[@]} > 0 )) || die 'rollback API argument file is empty'
  local arg
  for arg in "${API_JVM_ARGS[@]}" "${API_APP_ARGS[@]}"; do
    [[ -n "$arg" && "$arg" != *$'\n'* && "$arg" != *$'\r'* ]] \
      || die 'blank/control rollback API launch argument'
  done
  [[ "$AUTH_HEADER_NAME" =~ ^[A-Za-z0-9-]+$ ]] || die 'rollback auth header name is unsafe'
  [[ "$AUTH_HEADER_VALUE" != *$'\n'* && "$AUTH_HEADER_VALUE" != *$'\r'* ]] \
    || die 'rollback scope A auth value is unsafe'
  [[ "$AUTH_B_HEADER_VALUE" != *$'\n'* && "$AUTH_B_HEADER_VALUE" != *$'\r'* ]] \
    || die 'rollback scope B auth value is unsafe'
  A=(-H "$AUTH_HEADER_NAME: $AUTH_HEADER_VALUE" -H 'Content-Type: application/json')
  B=(-H "$AUTH_HEADER_NAME: $AUTH_B_HEADER_VALUE" -H 'Content-Type: application/json')
}

assert_rollback_prerequisites() {
  local fn
  for fn in api_pids agent_pids assert_api_stopped assert_agent_stopped \
            assert_at_most_one_agent_writer assert_one_agent_writer \
            stop_api_exact start_api_exact assert_success_envelope \
            assert_no_modifying_transactions run_disk_gate capture_critical_table_counts \
            write_present_check_sql verify_present_check_output load_rollback_runtime_context; do
    declare -F "$fn" >/dev/null || die "rollback function unavailable: $fn"
  done
  declare -p A B API_JVM_ARGS API_APP_ARGS >/dev/null || die 'rollback curl/API arrays unavailable'
  [[ "$BASE_URL" =~ ^https?://[^[:space:]]+$ ]] || die 'rollback BASE_URL unavailable'
  [[ "$OLD_SMOKE_AGENT_ID" =~ ^[A-Za-z0-9._:-]+$ && "$OLD_SMOKE_AGENT_ID" != builtin-songjiang ]] \
    || die 'rollback old smoke Agent unavailable'
  [[ "$DUMP" == "$BACKUP_DIR"/* && -s "$DUMP" && -s "$DUMP.sha256" \
      && "$PRE_SCHEMA_DUMP" == "$BACKUP_DIR"/* && -s "$PRE_SCHEMA_DUMP" \
      && -s "$PRE_SCHEMA_DUMP.sha256" ]] || die 'rollback DB dump/schema path mismatch'
  [[ "$ROLLBACK_JAR" == "$RELEASE_DIR"/* && -s "$ROLLBACK_JAR" \
      && -s "$ROLLBACK_JAR.sha256" ]] || die 'rollback JAR evidence path mismatch'
  [[ "$AGENT_BACKUP_TAR" == "$AGENT_BACKUP_DIR"/* && -s "$AGENT_BACKUP_TAR" \
      && -s "$AGENT_BACKUP_TAR.sha256" ]] || die 'rollback agent tar evidence path mismatch'
  sha256sum -c "$OLD_SMOKE_PREFLIGHT_RESPONSE.sha256"
  sha256sum -c "$ROLLBACK_JAR.sha256"
  sha256sum -c "$AGENT_BACKUP_TAR.sha256"
  sha256sum -c "$ROLLBACK_API_ARGS_SHA"
  sha256sum -c "$ROLLBACK_DB_EVIDENCE_SHA"
  sha256sum -c "$ACCOUNT_EVIDENCE_SHA"
  sha256sum -c "$DUMP.sha256"
  sha256sum -c "$PRE_SCHEMA_DUMP.sha256"
  [[ "$OLD_SMOKE_PREFLIGHT_RESPONSE" == "$BACKUP_DIR"/* && -s "$OLD_SMOKE_PREFLIGHT_RESPONSE" ]] \
    || die 'rollback old-smoke evidence path mismatch'
  [[ "$ROLLBACK_API_JVM_ARGS_FILE" == "$BACKUP_DIR"/* && -s "$ROLLBACK_API_JVM_ARGS_FILE" \
      && "$ROLLBACK_API_APP_ARGS_FILE" == "$BACKUP_DIR"/* && -s "$ROLLBACK_API_APP_ARGS_FILE" \
      && "$ROLLBACK_API_ARGS_SHA" == "$BACKUP_DIR"/* && -s "$ROLLBACK_API_ARGS_SHA" ]] \
    || die 'rollback API argument evidence path mismatch'
  [[ "$PRE_ROW_COUNTS" == "$BACKUP_DIR"/* && -s "$PRE_ROW_COUNTS" \
      && "$PRE_CRITICAL_ROW_COUNTS" == "$BACKUP_DIR"/* && -s "$PRE_CRITICAL_ROW_COUNTS" \
      && "$CRITICAL_TABLE_EXPECTATIONS" == "$BACKUP_DIR"/* && -s "$CRITICAL_TABLE_EXPECTATIONS" \
      && "$ROLLBACK_DB_EVIDENCE_SHA" == "$BACKUP_DIR"/* && -s "$ROLLBACK_DB_EVIDENCE_SHA" ]] \
    || die 'rollback row-count evidence path mismatch'
  [[ "$SCHEMA_META" == "$BACKUP_DIR"/* && -s "$SCHEMA_META" \
      && "$ACCOUNT_EVIDENCE_DIR" == "$BACKUP_DIR"/* && -d "$ACCOUNT_EVIDENCE_DIR" \
      && "$ACCOUNT_EVIDENCE_SHA" == "$BACKUP_DIR"/* && -s "$ACCOUNT_EVIDENCE_SHA" ]] \
    || die 'rollback schema/account evidence path mismatch'
}

require_full_restore_approval() {
  assert_rollback_prerequisites
  [[ "${M1_APPROVE_FULL_RESTORE:-}" == YES_I_UNDERSTAND_DATA_REPLACEMENT ]] \
    || die 'full restore approval gate is not set'
  [[ "$DB_NAME" == "$APPROVED_PROD_DB_NAME" && "$DB_NAME" =~ ^[A-Za-z0-9_]+$ ]] \
    || die 'restore schema is not independently approved'
  [[ "$MYSQL_SOCKET" == /home/isp/apps/mysql/mysql.sock && -S "$MYSQL_SOCKET" ]] \
    || die 'restore socket mismatch'
  [[ "$API_DEPLOY_DIR" == /home/isp/hosts/cyf/api ]] || die 'restore API path mismatch'
  [[ "$AGENT_APP_DIR" == /home/isp/apps/codex-ws-agent ]] || die 'restore agent path mismatch'
  [[ "$CURRENT_JAR" == /home/isp/hosts/cyf/api/cyf-api-kit.jar ]] || die 'restore JAR path mismatch'
  [[ "$DUMP" == "$BACKUP_DIR"/* && -s "$DUMP" ]] || die 'restore dump path mismatch'
  [[ "$ROLLBACK_JAR" == "$RELEASE_DIR"/* && -s "$ROLLBACK_JAR" ]] || die 'rollback JAR path mismatch'
  [[ "$AGENT_BACKUP_TAR" == "$AGENT_BACKUP_DIR"/* && -s "$AGENT_BACKUP_TAR" ]] \
    || die 'agent rollback tar path mismatch'
  [[ -s "$SCHEMA_META" && -s "$PRE_ROW_COUNTS" && -s "$PRE_SCHEMA_DUMP" \
      && -s "$CRITICAL_TABLE_EXPECTATIONS" && -s "$PRE_CRITICAL_ROW_COUNTS" \
      && -s "$ROLLBACK_DB_EVIDENCE_SHA" ]] || die 'restore evidence missing'
  [[ "$ACCOUNT_EVIDENCE_DIR" == "$BACKUP_DIR"/* && -d "$ACCOUNT_EVIDENCE_DIR" \
      && "$ACCOUNT_EVIDENCE_SHA" == "$BACKUP_DIR"/* && -s "$ACCOUNT_EVIDENCE_SHA" ]] \
    || die 'account restore evidence missing'
}

for fn in assert_rollback_prerequisites require_full_restore_approval; do
  declare -F "$fn" >/dev/null || die "full-restore gate missing before migration: $fn"
done
load_rollback_runtime_context
assert_rollback_prerequisites
```

**此处是 migration point-of-no-return 前的最后门。** 上述命令全部通过后，`DUMP`、旧 JAR、旧 agent tar/config、API 启停参数、curl/Auth 数组、旧 Agent smoke 证据、functions 和关键表基线均已存在；后续任一迁移失败时，第 10 节在 `set -u` 下不需要补定义这些 prerequisite。

## 4. 隔离临时数据库 restore drill

恢复演练必须指向同实例的**新临时 schema**或另一隔离实例，绝不能指向 `$DB_NAME`。生产与 drill 都使用第 3.4 节同一份显式 expectation；每张 `PRESENT` 表执行 exact `COUNT(*)`，每张 `ABSENT` 表强断言不存在。两个 14 行 TSV 先排序再 `cmp`，任何缺表、额外表、查询失败、重复、空列表或行数差异均阻断。禁止在 `trap` 中自动 drop。

```bash
RESTORE_DB="m1_restore_${CHANGE_ID//[^A-Za-z0-9_]/_}_$(date -u +%Y%m%d%H%M%S)"
[[ "$RESTORE_DB" =~ ^m1_restore_[A-Za-z0-9_]+$ ]] || die 'unsafe restore-drill schema'
[[ "$RESTORE_DB" != "$DB_NAME" ]] || die 'restore drill targets production schema'

"${MYSQL[@]}" -e "CREATE DATABASE \`$RESTORE_DB\` CHARACTER SET $ORIGINAL_DB_CHARSET COLLATE $ORIGINAL_DB_COLLATION"
gzip -cd "$DUMP" | "${MYSQL[@]}" "$RESTORE_DB"

RESTORE_CRITICAL_ROW_COUNTS="$BACKUP_DIR/${CHANGE_ID}.restore-drill-critical-row-counts.tsv"
capture_critical_table_counts "$RESTORE_DB" "$RESTORE_CRITICAL_ROW_COUNTS"
LC_ALL=C sort -o "$PRE_CRITICAL_ROW_COUNTS" "$PRE_CRITICAL_ROW_COUNTS"
LC_ALL=C sort -o "$RESTORE_CRITICAL_ROW_COUNTS" "$RESTORE_CRITICAL_ROW_COUNTS"
cmp -s "$PRE_CRITICAL_ROW_COUNTS" "$RESTORE_CRITICAL_ROW_COUNTS" \
  || { diff -u "$PRE_CRITICAL_ROW_COUNTS" "$RESTORE_CRITICAL_ROW_COUNTS" >&2 || true; \
       die 'restore-drill critical exact row counts/presence differ'; }

RESTORE_DRILL_CHECK_SQL="$BACKUP_DIR/${CHANGE_ID}.restore-drill-check.sql"
write_present_check_sql "$RESTORE_DRILL_CHECK_SQL"
RESTORE_DRILL_CHECK_FILE="$BACKUP_DIR/${CHANGE_ID}.restore-drill-check.tsv"
"${MYSQL[@]}" "$RESTORE_DB" --batch --raw --column-names < "$RESTORE_DRILL_CHECK_SQL" \
  | tee "$RESTORE_DRILL_CHECK_FILE"
verify_present_check_output "$RESTORE_DRILL_CHECK_FILE"

sha256sum "$PRE_CRITICAL_ROW_COUNTS" "$RESTORE_CRITICAL_ROW_COUNTS" \
  "$CRITICAL_TABLE_EXPECTATIONS" "$RESTORE_DRILL_CHECK_FILE" \
  > "$BACKUP_DIR/${CHANGE_ID}.restore-drill.sha256"
```

恢复演练 TSV 和 `CHECK TABLE` 全部通过后仍保留临时 schema，等待 DBA 与 Reviewer 签字；只可使用本次精确 `m1_restore_...` 名称单独处置，不提供通配或批量 DROP。

## 5. 迁移前数据与 scoped UNIQUE preflight

```sql
SELECT tenant_id, client_id, task_id, COUNT(*) AS duplicate_rows
FROM agent_task_meta
GROUP BY tenant_id, client_id, task_id
HAVING COUNT(*) > 1;

SELECT task_id,
       COUNT(*) AS row_count,
       COUNT(DISTINCT CONCAT(
         OCTET_LENGTH(COALESCE(tenant_id,'')), ':', HEX(COALESCE(tenant_id,'')), '|',
         OCTET_LENGTH(COALESCE(client_id,'')), ':', HEX(COALESCE(client_id,'')))) AS scope_count
FROM agent_task_meta
GROUP BY task_id
HAVING scope_count > 1;

SELECT index_name, non_unique, seq_in_index, column_name, sub_part
FROM information_schema.statistics
WHERE table_schema=DATABASE() AND table_name='agent_task_meta'
ORDER BY index_name, seq_in_index;

SELECT lifecycle_status, COUNT(*) FROM agent_identity_registry GROUP BY lifecycle_status;
SELECT alias_status, COUNT(*) FROM agent_identity_alias GROUP BY alias_status;
SELECT status, lifecycle_status, COUNT(*)
FROM agent_persona_binding GROUP BY status, lifecycle_status;
```

第一条 scoped duplicate 查询必须返回 0 行。不得用自动 `DELETE`、`UPDATE` 或“保留最小 id”修复生产数据。

## 6. 固定迁移与部署顺序

### 6.1 A02/A08 identity schema 与 legacy apply

```bash
[[ -z "$(git -C "$API_SRC" status --porcelain)" ]] || die 'API worktree became dirty'
[[ "$(git -C "$API_SRC" rev-parse HEAD)" == "$EXPECTED_API_HEAD" ]] || die 'API HEAD changed'
IDENTITY_DIR="$API_SRC/agent/jia-agent-mapper/src/main/resources/db"
"${MYSQL[@]}" "$DB_NAME" < "$IDENTITY_DIR/agent-identity-schema.sql"
"${MYSQL[@]}" "$DB_NAME" < "$IDENTITY_DIR/agent-identity-legacy-manifest-schema.sql"

"${MYSQL[@]}" "$DB_NAME" --batch --raw \
  < "$IDENTITY_DIR/agent-identity-dry-run.sql" \
  > "$BACKUP_DIR/${CHANGE_ID}.a02-identity-dry-run.tsv"
"${MYSQL[@]}" "$DB_NAME" --batch --raw \
  < "$IDENTITY_DIR/agent-identity-legacy-snapshot.sql" \
  > "$BACKUP_DIR/${CHANGE_ID}.a08-identity-snapshot.tsv"
sha256sum "$BACKUP_DIR/${CHANGE_ID}.a02-identity-dry-run.tsv" \
          "$BACKUP_DIR/${CHANGE_ID}.a08-identity-snapshot.tsv" \
  | tee "$BACKUP_DIR/${CHANGE_ID}.identity-reports.sha256"
```

Reviewer 只允许将明确批准行按 manifest template 写入 manifest；`AUTO_ELIGIBLE` 不是自动授权，`BLOCKED_*` 保持阻断。

```bash
: "${A08_MANIFEST_BATCH_ID:?approved A08 manifest batch id}"
: "${A08_APPROVED_REPORT_SHA256:?approved 64-lower-hex report digest}"
: "${A08_OPERATOR:?reviewer/change identity}"
[[ "$A08_APPROVED_REPORT_SHA256" =~ ^[0-9a-f]{64}$ ]] || die 'invalid A08 digest'
[[ "$A08_MANIFEST_BATCH_ID" =~ ^[A-Za-z0-9._:-]+$ ]] || die 'unsafe A08 batch ID'
[[ "$A08_OPERATOR" =~ ^[A-Za-z0-9._:@/-]+$ ]] || die 'unsafe A08 operator'

"${MYSQL[@]}" "$DB_NAME" <<SQL
SET @a08_manifest_batch_id = '$A08_MANIFEST_BATCH_ID';
SET @a08_approved_report_sha256 = '$A08_APPROVED_REPORT_SHA256';
SET @a08_operator = '$A08_OPERATOR';
source $IDENTITY_DIR/agent-identity-legacy-apply.sql
SQL
```

最新 apply run 必须为 `SUCCEEDED` 或经人工解释的安全 no-op。**A08 legacy identity migration/apply 成功前禁止部署 A08 runtime。**

### 6.2 B01/B08 scoped root 与 B07 task-thread

```bash
"${MYSQL[@]}" "$DB_NAME" \
  < "$API_SRC/agent/jia-agent-mapper/src/main/resources/db/task-collaboration-schema.sql"
"${MYSQL[@]}" "$DB_NAME" \
  < "$API_SRC/chat/jia-chat-mapper/src/main/resources/db/task-thread-schema.sql"
```

```sql
SELECT index_name, GROUP_CONCAT(LOWER(column_name) ORDER BY seq_in_index) AS columns_in_order,
       MIN(non_unique) AS non_unique, COUNT(*) AS column_count
FROM information_schema.statistics
WHERE table_schema=DATABASE() AND table_name='agent_task_meta'
GROUP BY index_name
HAVING index_name='uk_agent_task_meta_scope';
-- tenant_id,client_id,task_id | non_unique=0 | column_count=3

SELECT COUNT(*) AS global_task_unique_count
FROM (
  SELECT index_name
  FROM information_schema.statistics
  WHERE table_schema=DATABASE() AND table_name='agent_task_meta'
    AND non_unique=0 AND index_name <> 'PRIMARY'
  GROUP BY index_name
  HAVING COUNT(*)=1 AND LOWER(MAX(column_name))='task_id'
) x;
-- 必须为 0。
```

### 6.3 B09 audit、definer routines、权限、审批与 apply

固定顺序：audit DDL 两遍 → locked definer routines → GRANT/REVOKE → dry-run/export → 人工 review → approve → apply。最小权限 SQL 见 `docs/DEPLOYMENT.md` 的 B09 章节。

```bash
B09_DIR="$API_SRC/agent/jia-agent-mapper/src/main/resources/db"
"${MYSQL[@]}" "$DB_NAME" < "$B09_DIR/task-collaboration-backfill-audit-schema.sql"
"${MYSQL[@]}" "$DB_NAME" < "$B09_DIR/task-collaboration-backfill-audit-schema.sql"
"${MYSQL[@]}" "$DB_NAME" < "$B09_DIR/task-collaboration-backfill-routines.sql"
```

DBA 完成 locked definer 与 operator 最小权限后，必须重新导出、审核、approve/apply；session variable 不是授权凭据。验证四张 audit 表、sealed batch、manifest digest/row count、run、issue 与 12 个 exact trigger。

### 6.4 从 immutable artifact 启动 API

`start_api_exact`、JVM/app argv、`ROLLBACK_JAR` 及其 checksum 已在第 3.4 节创建并验证；此处禁止覆盖旧 JAR 备份。

```bash
assert_rollback_prerequisites
[[ -s "$ARTIFACT" ]] || die 'immutable artifact missing'
sha256sum -c "$ARTIFACT.sha256"
sha256sum -c "$ROLLBACK_JAR.sha256"
install -m 0644 "$ARTIFACT" "$CURRENT_JAR.tmp"
mv "$CURRENT_JAR.tmp" "$CURRENT_JAR"
start_api_exact
```

### 6.5 部署 codex-ws-agent

完整旧 app/profile/policy/queue/config tar 已在第 3.4 节、agent 停止状态下创建并验证；此处不得重新打包或覆盖。保留 archive/quarantine 与 Git worktree registration，禁止 `git worktree remove/prune`。

```bash
assert_rollback_prerequisites
[[ -z "$(git -C "$AGENT_SRC" status --porcelain)" ]] || die 'agent worktree became dirty'
[[ "$(git -C "$AGENT_SRC" rev-parse HEAD)" == "$EXPECTED_AGENT_HEAD" ]] || die 'agent HEAD changed'
sha256sum -c "$AGENT_BACKUP_TAR.sha256"

cd "$AGENT_SRC"
bash ./shell/codex_ws_agent_install.sh
cd "$AGENT_APP_DIR"
PATH=/home/isp/apps/node/bin:$PATH npm ci --omit=dev
PATH=/home/isp/apps/node/bin:$PATH node agent-client.mjs --validate
/home/isp/bin/codex_ws_agent_start.sh start
assert_one_agent_writer
```

## 7. scoped UNIQUE 是 forward-only schema boundary

一旦两个不同 `(tenant_id, client_id)` scope 写入相同 `task_id`：

- 不允许只回退旧应用并重建 global `UNIQUE(task_id)`；该 DDL会失败或迫使删除合法 scoped 数据。
- 不提供自动删除、合并或改名生产任务的脚本。
- 失败处理只有：在恢复写入前恢复本窗口**完整数据库备份 + 旧应用 + 旧 agent**，或保留 scoped schema/data 并 roll-forward。
- 若已恢复业务写入并产生新数据，恢复旧 dump 会丢失窗口后数据，必须重新走完整灾难恢复审批。

跨 scope smoke 使用专用 scope、active Agent 和 `m1-smoke-$CHANGE_ID-*` task ID。smoke 行默认保留并以 change ID 标记；如需清理，先导出精确主键和关联行，经第二人批准后人工执行，不得按前缀批量删除。

## 8. M1 专项 smoke

### 8.1 凭据与普通 persona 门禁

`SMOKE_REGISTER_AGENT_ID` 必须是已批准的普通（非 system）active persona 的 canonical ID 或 legacy alias。注册响应返回的 canonical ID 和随后 `/agent/{id}` 查询返回的实际 `name/personaName` 都必须由 Python stdlib 严格解析并非空；后续 append 使用该**同一个服务端实际 senderName**。

```bash
set -euo pipefail
assert_rollback_prerequisites
: "${TENANT_ID:?scope A tenant expected from credential}"
: "${CLIENT_ID:?scope A client expected from credential}"
: "${TENANT_B_ID:?scope B tenant expected from credential}"
: "${CLIENT_B_ID:?scope B client expected from credential}"
: "${SMOKE_REGISTER_AGENT_ID:?approved ordinary active persona ID or legacy alias in scope A}"
: "${EXPECTED_CANONICAL_AGENT_ID:?approved expected canonical ID for that persona}"
: "${LEGACY_AGENT_ID:?approved ACTIVE legacy alias in scope A}"
: "${SCOPE_B_AGENT_ID:?ACTIVE canonical agent in scope B}"
: "${OUTSIDER_AGENT_ID:?valid ACTIVE agent outside task membership}"
: "${SMOKE_TASK_ID:=m1-smoke-${CHANGE_ID}-shared-task}"

for id in "$SMOKE_REGISTER_AGENT_ID" "$EXPECTED_CANONICAL_AGENT_ID" "$LEGACY_AGENT_ID" \
          "$SCOPE_B_AGENT_ID" "$OUTSIDER_AGENT_ID"; do
  [[ "$id" =~ ^[A-Za-z0-9._:-]+$ ]] || die "unsafe Agent ID: $id"
done
[[ "$SMOKE_REGISTER_AGENT_ID" != builtin-songjiang ]] || die 'system persona is forbidden for this smoke'
[[ "$EXPECTED_CANONICAL_AGENT_ID" != builtin-songjiang ]] || die 'system persona is forbidden for this smoke'
[[ "$SMOKE_TASK_ID" =~ ^[A-Za-z0-9._:-]+$ ]] || die 'unsafe smoke task ID'

REGISTER_PAYLOAD="/tmp/${CHANGE_ID}.register-payload.json"
REGISTER_RESPONSE="/tmp/${CHANGE_ID}.register-response.json"
AGENT_RESPONSE="/tmp/${CHANGE_ID}.agent-response.json"
python3 - "$SMOKE_REGISTER_AGENT_ID" "$CHANGE_ID" > "$REGISTER_PAYLOAD" <<'PY'
import json, sys
print(json.dumps({'agentId': sys.argv[1], 'endpoint': 'smoke://' + sys.argv[2]},
                 ensure_ascii=False, separators=(',', ':')))
PY
curl --fail --silent --show-error "${A[@]}" -X POST "$BASE_URL/agent/register" \
  --data-binary "@$REGISTER_PAYLOAD" > "$REGISTER_RESPONSE"

REGISTERED_CANONICAL_AGENT_ID="$(python3 - "$REGISTER_RESPONSE" <<'PY'
import json, pathlib, sys
try:
    obj = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
except Exception as exc:
    raise SystemExit(f'invalid register JSON: {exc}')
if not isinstance(obj, dict) or obj.get('status') != 200 or obj.get('code') != 'E0':
    raise SystemExit(f'failed register envelope: {obj!r}')
data = obj.get('data')
agent_id = data.get('agentId') if isinstance(data, dict) else None
if not isinstance(agent_id, str) or not agent_id or agent_id != agent_id.strip() or any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in agent_id):
    raise SystemExit('missing/non-canonical registered agentId')
print(agent_id)
PY
)"
[[ -n "$REGISTERED_CANONICAL_AGENT_ID" ]] || die 'empty canonical ID from registration'
[[ "$REGISTERED_CANONICAL_AGENT_ID" == "$EXPECTED_CANONICAL_AGENT_ID" ]] \
  || die 'registered canonical ID differs from approved identity'
[[ "$REGISTERED_CANONICAL_AGENT_ID" != builtin-songjiang ]] || die 'registration resolved to system persona'

curl --fail --silent --show-error "${A[@]}" \
  "$BASE_URL/agent/$REGISTERED_CANONICAL_AGENT_ID" > "$AGENT_RESPONSE"
ACTUAL_SENDER_NAME="$(python3 - "$AGENT_RESPONSE" "$REGISTERED_CANONICAL_AGENT_ID" <<'PY'
import json, pathlib, sys
obj = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
if not isinstance(obj, dict) or obj.get('status') != 200 or obj.get('code') != 'E0':
    raise SystemExit(f'failed agent envelope: {obj!r}')
data = obj.get('data')
if not isinstance(data, dict) or data.get('agentId') != sys.argv[2]:
    raise SystemExit('agent query did not return registered canonical ID')
if data.get('systemAgent') is not False:
    raise SystemExit('task-thread smoke requires an ordinary non-system persona')
def canonical_display(value):
    return (isinstance(value, str) and bool(value) and value == value.strip()
            and len(value) <= 100
            and not any(ord(c) < 32 or 127 <= ord(c) <= 159 for c in value))
name = data.get('name')
if not canonical_display(name):
    name = data.get('personaName')
if not canonical_display(name):
    raise SystemExit('missing/invalid service-side display/persona name')
print(name)
PY
)"
[[ -n "$ACTUAL_SENDER_NAME" ]] || die 'empty service-side sender name'
printf 'canonicalAgentId=%s\nsenderName=%s\n' \
  "$REGISTERED_CANONICAL_AGENT_ID" "$ACTUAL_SENDER_NAME" \
  > "/tmp/${CHANGE_ID}.actual-agent.txt"
```

### 8.2 进程、端口、日志、identity 与 legacy assign/report

```bash
mapfile -t running_api < <(api_pids)
(( ${#running_api[@]} == 1 )) || die 'expected exactly one exact API process'
curl --fail --silent --show-error "$BASE_URL/actuator" \
  | tee "/tmp/${CHANGE_ID}.actuator.json" >/dev/null
[[ -n "$(ss -H -ltn "sport = :$API_PORT")" ]] || die 'API port is not listening'
API_LOG="$(find "$API_DEPLOY_DIR/logs" -maxdepth 1 -type f -name 'startlog_*.log' -printf '%T@ %p\n' \
  | sort -nr | awk 'NR==1 {$1=""; sub(/^ /,""); print}')"
[[ -n "$API_LOG" && -f "$API_LOG" ]] || die 'API startup log missing'
rg -n 'Started .*Application' "$API_LOG"
if rg -n 'A02 identity|B09 audit|AgentSchemaInitializer|ChatSchemaInitializer|requires twelve|incompatible' "$API_LOG" \
  | rg -i 'error|exception|failed'; then
  die 'initializer failure found in API log'
fi

/home/isp/bin/codex_ws_agent_start.sh status
AGENT_LOG="$(find "$AGENT_APP_DIR/logs" -maxdepth 1 -type f -name 'startlog_*.log' -printf '%T@ %p\n' \
  | sort -nr | awk 'NR==1 {$1=""; sub(/^ /,""); print}')"
[[ -n "$AGENT_LOG" && -f "$AGENT_LOG" ]] || die 'agent startup log missing'
rg -n 'connected|registered' "$AGENT_LOG"
if rg -n 'WORKSPACE_ARCHIVE_RECOVERY_REQUIRED|quarantine|configuration invalid|uncaught|fatal' "$AGENT_LOG"; then
  die 'agent failure found in log'
fi

IDENTITY_SMOKE_RESPONSE="/tmp/${CHANGE_ID}.identity.json"
LEGACY_ASSIGN_RESPONSE="/tmp/${CHANGE_ID}.legacy-assign.json"
LEGACY_REPORT_RESPONSE="/tmp/${CHANGE_ID}.legacy-report.json"
curl --fail --silent --show-error "${A[@]}" \
  "$BASE_URL/agent/$REGISTERED_CANONICAL_AGENT_ID" > "$IDENTITY_SMOKE_RESPONSE"
assert_success_envelope "$IDENTITY_SMOKE_RESPONSE"
curl --fail --silent --show-error "${A[@]}" -X POST \
  "$BASE_URL/agent/tasks/$SMOKE_TASK_ID/assign" \
  --data "{\"agentIds\":[\"$LEGACY_AGENT_ID\"],\"allowQueue\":false}" \
  > "$LEGACY_ASSIGN_RESPONSE"
assert_success_envelope "$LEGACY_ASSIGN_RESPONSE"
curl --fail --silent --show-error "${A[@]}" -X POST \
  "$BASE_URL/agent/tasks/$SMOKE_TASK_ID/report" \
  --data "{\"agentId\":\"$LEGACY_AGENT_ID\",\"status\":\"running\",\"currentTaskTitle\":\"M1 $CHANGE_ID\"}" \
  > "$LEGACY_REPORT_RESPONSE"
assert_success_envelope "$LEGACY_REPORT_RESPONSE"
```

```sql
SELECT r.canonical_agent_id, r.lifecycle_status, r.client_id, r.owner_jiacn,
       r.tenant_id, r.binding_id,
       b.agent_id AS binding_agent_id, b.status AS binding_status,
       rt.agent_id AS runtime_agent_id, rt.status AS runtime_status
FROM agent_identity_registry r
JOIN agent_persona_binding b ON b.id=r.binding_id
JOIN agent_runtime rt ON rt.binding_id=r.binding_id
WHERE BINARY r.canonical_agent_id=BINARY '<REGISTERED_CANONICAL_AGENT_ID>'
  AND OCTET_LENGTH(r.canonical_agent_id)=OCTET_LENGTH('<REGISTERED_CANONICAL_AGENT_ID>');

SELECT alias_value, canonical_agent_id, alias_status, client_id, owner_jiacn, tenant_id
FROM agent_identity_alias
WHERE BINARY alias_value=BINARY '<LEGACY_AGENT_ID>'
  AND OCTET_LENGTH(alias_value)=OCTET_LENGTH('<LEGACY_AGENT_ID>');
```

### 8.3 跨 scope 相同 task ID

```bash
SCOPE_B_ASSIGN_RESPONSE="/tmp/${CHANGE_ID}.scope-b-assign.json"
curl --fail --silent --show-error "${B[@]}" -X POST \
  "$BASE_URL/agent/tasks/$SMOKE_TASK_ID/assign" \
  --data "{\"agentIds\":[\"$SCOPE_B_AGENT_ID\"],\"allowQueue\":false}" \
  > "$SCOPE_B_ASSIGN_RESPONSE"
assert_success_envelope "$SCOPE_B_ASSIGN_RESPONSE"
```

```sql
SELECT tenant_id, client_id, task_id, COUNT(*)
FROM agent_task_meta
WHERE BINARY task_id=BINARY '<SMOKE_TASK_ID>'
  AND OCTET_LENGTH(task_id)=OCTET_LENGTH('<SMOKE_TASK_ID>')
GROUP BY tenant_id, client_id, task_id;
-- 必须恰有 scope A 与 scope B 两组，各 COUNT(*)=1。
```

### 8.4 B07 task-thread ACL、实际 sender 与 byte-exact

所有正向响应都严格检查 `status=200`、`code=E0` 和 JSON shape。append payload 由 Python 使用服务端查询得到的 `$ACTUAL_SENDER_NAME` 生成；append 返回及 list 返回必须逐字节等于该名字。

```bash
THREAD_RESPONSE="/tmp/${CHANGE_ID}.thread.json"
APPEND_PAYLOAD="/tmp/${CHANGE_ID}.append-payload.json"
APPEND_RESPONSE="/tmp/${CHANGE_ID}.append-response.json"
LIST_RESPONSE="/tmp/${CHANGE_ID}.messages.json"
MESSAGE_CONTENT="M1 byte-exact $CHANGE_ID-$(date -u +%Y%m%dT%H%M%SZ)-$$"

python3 - "$REGISTERED_CANONICAL_AGENT_ID" > "/tmp/${CHANGE_ID}.thread-payload.json" <<'PY'
import json, sys
print(json.dumps({'actorAgentId': sys.argv[1], 'title': 'M1 team thread'},
                 ensure_ascii=False, separators=(',', ':')))
PY
curl --fail --silent --show-error "${A[@]}" -X POST \
  "$BASE_URL/chat/task-threads/$SMOKE_TASK_ID/team" \
  --data-binary "@/tmp/${CHANGE_ID}.thread-payload.json" > "$THREAD_RESPONSE"
python3 - "$THREAD_RESPONSE" "$SMOKE_TASK_ID" "$REGISTERED_CANONICAL_AGENT_ID" <<'PY'
import json, pathlib, sys
obj=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
if not isinstance(obj,dict) or obj.get('status') != 200 or obj.get('code') != 'E0' or not isinstance(obj.get('data'),dict):
    raise SystemExit(f'invalid task-thread response: {obj!r}')
data=obj['data']
if data.get('taskId') != sys.argv[2] or data.get('createdByAgentId') != sys.argv[3]:
    raise SystemExit('task-thread response scope/creator mismatch')
if not isinstance(data.get('conversationId'),str) or not data['conversationId']:
    raise SystemExit('missing task-thread conversationId')
PY

python3 - "$REGISTERED_CANONICAL_AGENT_ID" "$ACTUAL_SENDER_NAME" "$MESSAGE_CONTENT" > "$APPEND_PAYLOAD" <<'PY'
import json, sys
print(json.dumps({'actorAgentId':sys.argv[1], 'content':sys.argv[3], 'senderName':sys.argv[2]},
                 ensure_ascii=False, separators=(',', ':')))
PY
curl --fail --silent --show-error "${A[@]}" -X POST \
  "$BASE_URL/chat/task-threads/$SMOKE_TASK_ID/team/messages" \
  --data-binary "@$APPEND_PAYLOAD" > "$APPEND_RESPONSE"
python3 - "$APPEND_RESPONSE" "$ACTUAL_SENDER_NAME" "$MESSAGE_CONTENT" <<'PY'
import json, pathlib, sys
obj=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
if not isinstance(obj,dict) or obj.get('status') != 200 or obj.get('code') != 'E0' or not isinstance(obj.get('data'),dict):
    raise SystemExit(f'invalid append response: {obj!r}')
data=obj['data']
if data.get('senderName') != sys.argv[2] or data.get('content') != sys.argv[3]:
    raise SystemExit('append did not preserve actual service-side sender/content')
if not isinstance(data.get('messageId'),int):
    raise SystemExit('append response missing messageId')
PY

curl --fail --silent --show-error "${A[@]}" \
  "$BASE_URL/chat/task-threads/$SMOKE_TASK_ID/team/messages?actorAgentId=$REGISTERED_CANONICAL_AGENT_ID&limit=20" \
  > "$LIST_RESPONSE"
python3 - "$LIST_RESPONSE" "$ACTUAL_SENDER_NAME" "$MESSAGE_CONTENT" <<'PY'
import json, pathlib, sys
obj=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
if not isinstance(obj,dict) or obj.get('status') != 200 or obj.get('code') != 'E0' or not isinstance(obj.get('data'),list):
    raise SystemExit(f'invalid list response: {obj!r}')
matches=[m for m in obj['data'] if isinstance(m,dict) and m.get('content') == sys.argv[3]]
if len(matches) != 1 or matches[0].get('senderName') != sys.argv[2]:
    raise SystemExit('listed message sender/content mismatch')
PY
```

负向 ACL 请求必须返回 4xx 且 JSON error envelope 的 `status` 与 HTTP 状态一致、`code != E0`；任一 2xx、非 JSON 或 envelope 不一致都失败。

```bash
assert_json_4xx() {
  local body="$1" code="$2"
  [[ "$code" =~ ^4[0-9][0-9]$ ]] || die "expected 4xx, got $code"
  python3 - "$body" "$code" <<'PY'
import json, pathlib, sys
obj=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
status=int(sys.argv[2])
if not isinstance(obj,dict) or obj.get('status') != status or obj.get('code') in (None,'','E0'):
    raise SystemExit(f'invalid 4xx envelope: {obj!r}')
PY
}

CASE_AGENT_ID=${REGISTERED_CANONICAL_AGENT_ID^^}
[[ "$CASE_AGENT_ID" != "$REGISTERED_CANONICAL_AGENT_ID" ]] || die 'case variant is not distinct'
for pair in \
  "outsider|$OUTSIDER_AGENT_ID" \
  "case|$CASE_AGENT_ID" \
  "space|${REGISTERED_CANONICAL_AGENT_ID}%20"; do
  label=${pair%%|*}
  bad=${pair#*|}
  body="/tmp/${CHANGE_ID}.${label}-response.json"
  code="$(curl --silent --show-error --output "$body" --write-out '%{http_code}' "${A[@]}" \
    "$BASE_URL/chat/task-threads/$SMOKE_TASK_ID/team/messages?actorAgentId=$bad&limit=20")"
  assert_json_4xx "$body" "$code"
done

python3 - "$REGISTERED_CANONICAL_AGENT_ID" > "/tmp/${CHANGE_ID}.nul-payload.json" <<'PY'
import json, sys
print(json.dumps({'actorAgentId':sys.argv[1]+'\x00', 'content':'must reject'},
                 ensure_ascii=True, separators=(',', ':')))
PY
NUL_BODY="/tmp/${CHANGE_ID}.nul-response.json"
NUL_CODE="$(curl --silent --show-error --output "$NUL_BODY" --write-out '%{http_code}' "${A[@]}" \
  -X POST "$BASE_URL/chat/task-threads/$SMOKE_TASK_ID/team/messages" \
  --data-binary "@/tmp/${CHANGE_ID}.nul-payload.json")"
assert_json_4xx "$NUL_BODY" "$NUL_CODE"
```

隔离 MySQL 8.0.21 probe 已在代码验收执行；生产 smoke 的只读 SQL 也必须显示 exact 命中，case/space/NUL/padding 为 0：

```sql
SET @task='<SMOKE_TASK_ID>', @agent='<REGISTERED_CANONICAL_AGENT_ID>';
SELECT
  SUM(BINARY task_id=BINARY @task AND OCTET_LENGTH(task_id)=OCTET_LENGTH(@task)) AS exact_task,
  SUM(BINARY task_id=BINARY UPPER(@task) AND OCTET_LENGTH(task_id)=OCTET_LENGTH(UPPER(@task))) AS case_task,
  SUM(BINARY task_id=BINARY CONCAT(@task,' ') AND OCTET_LENGTH(task_id)=OCTET_LENGTH(CONCAT(@task,' '))) AS space_task,
  SUM(BINARY task_id=BINARY CONCAT(@task,CHAR(0)) AND OCTET_LENGTH(task_id)=OCTET_LENGTH(CONCAT(@task,CHAR(0)))) AS nul_task
FROM agent_task_thread;

SELECT
  SUM(BINARY agent_id=BINARY @agent AND OCTET_LENGTH(agent_id)=OCTET_LENGTH(@agent)) AS exact_member,
  SUM(BINARY agent_id=BINARY UPPER(@agent) AND OCTET_LENGTH(agent_id)=OCTET_LENGTH(UPPER(@agent))) AS case_member,
  SUM(BINARY agent_id=BINARY CONCAT(@agent,' ') AND OCTET_LENGTH(agent_id)=OCTET_LENGTH(CONCAT(@agent,' '))) AS space_member,
  SUM(BINARY agent_id=BINARY CONCAT(@agent,CHAR(0)) AND OCTET_LENGTH(agent_id)=OCTET_LENGTH(CONCAT(@agent,CHAR(0)))) AS nul_member
FROM agent_task_member
WHERE BINARY task_id=BINARY @task AND OCTET_LENGTH(task_id)=OCTET_LENGTH(@task);
```

### 8.5 B09 audit 与 codex-ws-agent

```sql
SELECT report_sha256, manifest_row_count, seal_status, approved_operator, sealed_at
FROM agent_task_backfill_manifest_batch ORDER BY id DESC LIMIT 5;
SELECT report_sha256, COUNT(*) AS rows_persisted
FROM agent_task_backfill_manifest GROUP BY report_sha256 ORDER BY MAX(id) DESC LIMIT 5;
SELECT run_id, report_sha256, operator, manifest_row_count, issue_row_count,
       member_insert_count, work_item_insert_count, run_status, completed_at
FROM agent_task_backfill_run ORDER BY id DESC LIMIT 5;
SELECT issue_code, COUNT(*), MAX(occurrence_count)
FROM agent_task_backfill_issue GROUP BY issue_code ORDER BY issue_code;
SELECT trigger_name, event_object_table, action_timing, event_manipulation
FROM information_schema.triggers
WHERE trigger_schema=DATABASE() AND trigger_name LIKE 'trg_task_backfill_%'
ORDER BY trigger_name;
-- 必须为 12 个 exact trigger；最新 approved batch SEALED，apply run SUCCEEDED。
```

受限 B09 operator 必须实测 direct INSERT batch/manifest/issue/run 均 permission denied，仅 approve/apply routine `EXECUTE` 可用。

```bash
cd "$AGENT_APP_DIR"
PATH=/home/isp/apps/node/bin:$PATH node agent-client.mjs --validate
/home/isp/bin/codex_ws_agent_start.sh status

: "${CODEX_PROFILES_FILE:=/home/isp/apps/codex-ws-agent/codex-profiles.conf}"
: "${EXPECTED_MODELS_FILE:?TSV: profileId<TAB>expected codexModel for every enabled Agent}"
python3 - "$CODEX_PROFILES_FILE" "$EXPECTED_MODELS_FILE" <<'PY'
import configparser, pathlib, sys
cfg=configparser.ConfigParser(interpolation=None)
cfg.optionxform=str
cfg.read(sys.argv[1], encoding='utf-8')
expected={}
for line in pathlib.Path(sys.argv[2]).read_text().splitlines():
    if not line or line.startswith('#'): continue
    profile, model=line.split('\t',1)
    if not profile or not model: raise SystemExit('blank expected profile/model')
    expected[profile]=model
seen={}
default_model=cfg.get('default','codexModel',fallback='').strip()
for section in cfg.sections():
    if not section.startswith('agent.'): continue
    if cfg.get(section,'enabled',fallback='true').strip().lower() == 'false': continue
    profile=cfg.get(section,'profileId',fallback=section[6:]).strip()
    model=cfg.get(section,'codexModel',fallback=default_model).strip()
    if not model: raise SystemExit(f'{profile}: blank codexModel')
    seen[profile]=model
if seen != expected: raise SystemExit(f'per-Agent codexModel mismatch: actual={seen!r} expected={expected!r}')
print('per-Agent codexModel OK', seen)
PY

: "${WORKSPACE_POLICY_ID:?}"
: "${WORKSPACE_TASK_ID:?known retained archived smoke fixture}"
: "${WORKSPACE_AGENT_ID:?}"
: "${WORKSPACE_ROLE:=coder}"
/home/isp/bin/codex_ws_agent.sh workspace inspect \
  --policy "$WORKSPACE_POLICY_ID" --task "$WORKSPACE_TASK_ID" \
  --agent "$WORKSPACE_AGENT_ID" --role "$WORKSPACE_ROLE" \
  | tee "/tmp/${CHANGE_ID}.workspace-inspect.json"
rg -q 'archived' "/tmp/${CHANGE_ID}.workspace-inspect.json"
rg -q 'quarantinePath' "/tmp/${CHANGE_ID}.workspace-inspect.json"

git --git-dir='<POLICY_REPOSITORY_PATH>' worktree list --porcelain \
  | tee "/tmp/${CHANGE_ID}.worktree-list.txt"
rg -q '<EXPECTED_QUARANTINE_ABSOLUTE_PATH>' "/tmp/${CHANGE_ID}.worktree-list.txt"
```

不得为了 smoke 运行 `git worktree remove/prune`、移动 quarantine 或编辑 archive metadata。

## 9. 恢复写入与观察

只有全部 schema/data 校验、API/agent smoke 和双人签字通过后才恢复写入。观察 initializer、identity、legacy assign/report、task-thread ACL、B09 run/issue、agent reconnect/ledger quarantine、磁盘/inode、MySQL lock wait/deadlock/metadata lock。

## 10. 获批完整灾难恢复：DROP + CREATE 后恢复旧栈

### 10.1 适用边界与强门禁

- scoped UNIQUE 已允许跨 scope 同 task ID 后，**不得**只回退旧 JAR或重建 global unique。
- 完整恢复会用维护窗口前 dump 替换当前生产 schema，丢弃 dump 时点之后的业务数据；只能在灾难恢复审批后执行。
- 绝不能把 `$DUMP` 重放到未清空的 `$DB_NAME`。固定顺序是：停服务/停写 → 保存失败现场 → 校验旧 dump → `DROP DATABASE` → 按原 charset/collation `CREATE DATABASE` → restore。
- 每个危险块都再次调用 `require_full_restore_approval` 并断言精确变量/路径。

```bash
# 函数与全部 prerequisite 已在第 3.4 节、任何迁移之前定义和验证。
declare -F require_full_restore_approval >/dev/null || die 'pre-migration full-restore gate is unavailable'
assert_rollback_prerequisites
```


### 10.2 再次停服务/停写，并保存当前失败现场

完整恢复时磁盘可能已变化；在任何失败现场 dump/tar 前，必须重新运行第 1 节相同的全部文件系统门禁逻辑。未通过则保持服务停止并升级存储，不得跳过现场保存或覆盖旧备份。

```bash
require_full_restore_approval
run_disk_gate pre-full-restore

require_full_restore_approval
if ! /home/isp/bin/codex_ws_agent_start.sh stop; then
  die 'agent stop failed before full restore'
fi
assert_agent_stopped
stop_api_exact
assert_no_modifying_transactions pre-full-restore

require_full_restore_approval
FAILURE_DIR="$BACKUP_DIR/${CHANGE_ID}.failed-state.$(date -u +%Y%m%dT%H%M%SZ)"
[[ "$FAILURE_DIR" == "$BACKUP_DIR"/* && ! -e "$FAILURE_DIR" ]] || die 'unsafe failure evidence path'
install -d -m 0700 "$FAILURE_DIR"

sha256sum "$CURRENT_JAR" > "$FAILURE_DIR/current-failed.jar.sha256"
install -m 0600 "$CURRENT_JAR" "$FAILURE_DIR/current-failed.jar"
if [[ -d "$API_DEPLOY_DIR/logs" ]]; then
  tar --xattrs --acls -C "$API_DEPLOY_DIR" -czf "$FAILURE_DIR/api-logs.tgz" logs
fi
tar --xattrs --acls -C /home/isp/apps -czf "$FAILURE_DIR/codex-ws-agent.failed.tgz" codex-ws-agent
sha256sum "$FAILURE_DIR"/*.tgz "$FAILURE_DIR/current-failed.jar" \
  > "$FAILURE_DIR/failed-files.sha256"

FAILED_DB_DUMP="$FAILURE_DIR/${DB_NAME}.failed.sql.gz"
"${MYSQLDUMP[@]}" --single-transaction --quick --routines --triggers --events --hex-blob \
  --set-gtid-purged=OFF --no-tablespaces --add-drop-table \
  "$DB_NAME" | gzip -1 > "$FAILED_DB_DUMP.tmp"
[[ -s "$FAILED_DB_DUMP.tmp" ]] || die 'failed-state database dump is empty'
mv "$FAILED_DB_DUMP.tmp" "$FAILED_DB_DUMP"
gzip -t "$FAILED_DB_DUMP"
sha256sum "$FAILED_DB_DUMP" > "$FAILED_DB_DUMP.sha256"
```

### 10.3 校验原完整备份和 agent tar

```bash
require_full_restore_approval
sha256sum -c "$DUMP.sha256"
gzip -t "$DUMP"
gzip -cd "$DUMP" | awk '/agent_task_meta/ {found=1} END {exit found ? 0 : 1}' \
  || die 'approved dump content check failed'
sha256sum -c "$ROLLBACK_JAR.sha256"
sha256sum -c "$AGENT_BACKUP_TAR.sha256"

python3 - "$AGENT_BACKUP_TAR" <<'PY'
import pathlib, sys, tarfile
archive=pathlib.Path(sys.argv[1])
with tarfile.open(archive, 'r:gz') as tf:
    members=tf.getmembers()
    if not members:
        raise SystemExit('empty agent backup')
    for member in members:
        p=pathlib.PurePosixPath(member.name)
        if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0] != 'codex-ws-agent':
            raise SystemExit(f'unsafe agent tar member: {member.name!r}')
PY

IFS=$'\t' read -r ORIGINAL_DB_CHARSET ORIGINAL_DB_COLLATION < "$SCHEMA_META"
[[ "$ORIGINAL_DB_CHARSET" =~ ^[A-Za-z0-9_]+$ ]] || die 'unsafe restore charset'
[[ "$ORIGINAL_DB_COLLATION" =~ ^[A-Za-z0-9_]+$ ]] || die 'unsafe restore collation'
```

### 10.4 明确 DROP + CREATE 生产 schema，再恢复完整 dump

这是唯一允许的完整数据库恢复路径。门禁、schema 名和原 charset/collation 任一断言失败都禁止 `DROP`。

```bash
require_full_restore_approval
[[ "$DB_NAME" != mysql && "$DB_NAME" != information_schema && "$DB_NAME" != performance_schema && "$DB_NAME" != sys ]] \
  || die 'refusing to replace a system schema'
"${MYSQL[@]}" -e "DROP DATABASE \`$DB_NAME\`; CREATE DATABASE \`$DB_NAME\` CHARACTER SET $ORIGINAL_DB_CHARSET COLLATE $ORIGINAL_DB_COLLATION;"

require_full_restore_approval
RESTORED_EMPTY_COUNT="$("${MYSQL[@]}" --batch --raw --skip-column-names -e \
  "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$DB_NAME';")"
[[ "$RESTORED_EMPTY_COUNT" == 0 ]] || die 'production schema was not empty before restore'
gzip -cd "$DUMP" | "${MYSQL[@]}" "$DB_NAME"
```

### 10.5 核验 restore checksum、schema、行数和关键表

```bash
require_full_restore_approval
POST_ROW_COUNTS="$FAILURE_DIR/post-restore-row-counts.tsv"
exact_row_counts "$POST_ROW_COUNTS"
cmp -s "$PRE_ROW_COUNTS" "$POST_ROW_COUNTS" \
  || { diff -u "$PRE_ROW_COUNTS" "$POST_ROW_COUNTS" >&2 || true; die 'restored row counts differ'; }

POST_SCHEMA_DUMP="$FAILURE_DIR/post-restore-schema.sql"
"${MYSQLDUMP[@]}" --no-data --routines --triggers --events --skip-comments \
  --set-gtid-purged=OFF --no-tablespaces "$DB_NAME" > "$POST_SCHEMA_DUMP"
cmp -s "$PRE_SCHEMA_DUMP" "$POST_SCHEMA_DUMP" \
  || { diff -u "$PRE_SCHEMA_DUMP" "$POST_SCHEMA_DUMP" >&2 || true; die 'restored schema/routines/triggers/events differ'; }
sha256sum "$DUMP" "$PRE_ROW_COUNTS" "$POST_ROW_COUNTS" \
  "$PRE_SCHEMA_DUMP" "$POST_SCHEMA_DUMP" \
  > "$FAILURE_DIR/restore-verification.sha256"

POST_SCHEMA_META="$("${MYSQL[@]}" --batch --raw --skip-column-names -e "
SELECT default_character_set_name, default_collation_name
FROM information_schema.schemata WHERE schema_name='$DB_NAME';")"
[[ "$POST_SCHEMA_META" == "$ORIGINAL_DB_CHARSET"$'\t'"$ORIGINAL_DB_COLLATION" ]] \
  || die "restored schema charset/collation differs: $POST_SCHEMA_META"

POST_CRITICAL_ROW_COUNTS="$FAILURE_DIR/post-restore-critical-row-counts.tsv"
capture_critical_table_counts "$DB_NAME" "$POST_CRITICAL_ROW_COUNTS"
cmp -s "$PRE_CRITICAL_ROW_COUNTS" "$POST_CRITICAL_ROW_COUNTS" \
  || { diff -u "$PRE_CRITICAL_ROW_COUNTS" "$POST_CRITICAL_ROW_COUNTS" >&2 || true; \
       die 'restored critical exact row counts/presence differ'; }

RESTORE_CHECK_SQL="$FAILURE_DIR/restore-check-table.sql"
RESTORE_CHECK_FILE="$FAILURE_DIR/restore-check-table.tsv"
write_present_check_sql "$RESTORE_CHECK_SQL"
"${MYSQL[@]}" "$DB_NAME" --batch --raw --column-names < "$RESTORE_CHECK_SQL" \
  | tee "$RESTORE_CHECK_FILE"
verify_present_check_output "$RESTORE_CHECK_FILE"
sha256sum "$PRE_CRITICAL_ROW_COUNTS" "$POST_CRITICAL_ROW_COUNTS" \
  "$CRITICAL_TABLE_EXPECTATIONS" "$RESTORE_CHECK_FILE" \
  >> "$FAILURE_DIR/restore-verification.sha256"
```

`cmp` 与 `CHECK TABLE` 任一失败都保持停写。不得自动删除差异行。

### 10.6 恢复 B09 definer/operator 的系统库状态

业务 dump 已含当时业务 schema 内的 routines/triggers/events，但不会恢复 `mysql` 系统库账户。第 3.3 节生成的两个精确 SQL 文件先 `DROP USER IF EXISTS` 对应**单一明确账户**，再在变更前存在时重建原 `CREATE USER` 和全部原 grants；变更前不存在时只撤销/删除本次新增账户。禁止使用通配账户名。

```bash
require_full_restore_approval
DEFINER_RESTORE_SQL="$ACCOUNT_EVIDENCE_DIR/b09-definer.restore.sql"
OPERATOR_RESTORE_SQL="$ACCOUNT_EVIDENCE_DIR/b09-operator.restore.sql"
sha256sum -c "$ACCOUNT_EVIDENCE_SHA"
for f in "$DEFINER_RESTORE_SQL" "$OPERATOR_RESTORE_SQL"; do
  [[ "$f" == "$ACCOUNT_EVIDENCE_DIR"/* && -f "$f" && "$(stat -c '%a' "$f")" == 600 ]] \
    || die "unsafe account restore SQL: $f"
done
[[ "$(sed -n '1p' "$DEFINER_RESTORE_SQL")" == "DROP USER IF EXISTS 'cyf_b09_definer'@'localhost';" ]] \
  || die 'definer restore SQL targets the wrong account'
[[ "$(sed -n '1p' "$OPERATOR_RESTORE_SQL")" == "DROP USER IF EXISTS '$B09_OPERATOR_USER'@'$B09_OPERATOR_HOST';" ]] \
  || die 'operator restore SQL targets the wrong account'

require_full_restore_approval
"${MYSQL[@]}" < "$DEFINER_RESTORE_SQL"
"${MYSQL[@]}" < "$OPERATOR_RESTORE_SQL"

verify_mysql_account_snapshot() {
  local user="$1" host="$2" stem="$3" expected_create expected_grants
  local actual_create actual_grants exists
  expected_create="$ACCOUNT_EVIDENCE_DIR/$stem.show-create.tsv"
  expected_grants="$ACCOUNT_EVIDENCE_DIR/$stem.show-grants.tsv"
  actual_create="$FAILURE_DIR/$stem.post-restore.show-create.tsv"
  actual_grants="$FAILURE_DIR/$stem.post-restore.show-grants.tsv"
  exists="$("${MYSQL[@]}" --batch --raw --skip-column-names -e \
    "SELECT COUNT(*) FROM mysql.user WHERE User='$user' AND Host='$host';")"
  [[ "$exists" == 0 || "$exists" == 1 ]] || die "ambiguous restored account state for $user@$host"
  if [[ -s "$expected_create" ]]; then
    [[ "$exists" == 1 ]] || die "required restored account is missing: $user@$host"
    "${MYSQL[@]}" --batch --raw --skip-column-names \
      -e "SHOW CREATE USER '$user'@'$host';" > "$actual_create"
    "${MYSQL[@]}" --batch --raw --skip-column-names \
      -e "SHOW GRANTS FOR '$user'@'$host';" > "$actual_grants"
    cmp -s "$expected_create" "$actual_create" || die "restored CREATE USER differs for $user@$host"
    cmp -s "$expected_grants" "$actual_grants" || die "restored grants differ for $user@$host"
  else
    [[ "$exists" == 0 ]] || die "account should have been revoked/dropped: $user@$host"
    : > "$actual_create"
    : > "$actual_grants"
  fi
}

verify_mysql_account_snapshot cyf_b09_definer localhost b09-definer
verify_mysql_account_snapshot "$B09_OPERATOR_USER" "$B09_OPERATOR_HOST" b09-operator
```

`verify_mysql_account_snapshot` 对存在状态、`SHOW CREATE USER` 和全部 `SHOW GRANTS` 做 byte-for-byte 比较；若变更前不存在账户，则强断言恢复后仍不存在。旧 dump 若包含 B09 routines，其 definer 用户必须恢复到原锁定/授权状态；旧状态无该账户时，精确 `DROP USER IF EXISTS` 撤销本次新增系统对象。

### 10.7 恢复旧 JAR 与旧 codex-ws-agent tar/config

先从迁移前 checksum 锁定的参数文件重新加载 JVM/app argv，并重建 fail-closed Auth curl 数组；不得继续使用可能在维护窗口中被改写的内存数组。

```bash
require_full_restore_approval
load_rollback_runtime_context
sha256sum -c "$ROLLBACK_JAR.sha256"
install -m 0644 "$ROLLBACK_JAR" "$CURRENT_JAR.tmp"
mv "$CURRENT_JAR.tmp" "$CURRENT_JAR"
[[ "$(sha256sum "$CURRENT_JAR" | awk '{print $1}')" == "$(awk '{print $1}' "$ROLLBACK_JAR.sha256")" ]] \
  || die 'restored JAR checksum mismatch'

require_full_restore_approval
FAILED_AGENT_DIR="$FAILURE_DIR/codex-ws-agent.directory"
[[ ! -e "$FAILED_AGENT_DIR" ]] || die 'failed agent directory evidence already exists'
mv "$AGENT_APP_DIR" "$FAILED_AGENT_DIR"
tar --xattrs --acls -C /home/isp/apps -xzf "$AGENT_BACKUP_TAR"
[[ -f "$AGENT_APP_DIR/agent-client.mjs" ]] || die 'restored agent entrypoint missing'
PATH=/home/isp/apps/node/bin:$PATH node "$AGENT_APP_DIR/agent-client.mjs" --validate
```

### 10.8 启动旧版本并执行 fail-closed smoke

```bash
require_full_restore_approval
start_api_exact
if ! /home/isp/bin/codex_ws_agent_start.sh start; then
  die 'old codex-ws-agent start command failed'
fi
assert_one_agent_writer

mapfile -t restored_api < <(api_pids)
(( ${#restored_api[@]} == 1 )) || die 'old API did not start as one exact process'
[[ -n "$(ss -H -ltn "sport = :$API_PORT")" ]] || die 'old API port is not listening'
RESTORE_ACTUATOR="$FAILURE_DIR/old-api-actuator.json"
curl --fail --silent --show-error "$BASE_URL/actuator" > "$RESTORE_ACTUATOR"
python3 - "$RESTORE_ACTUATOR" <<'PY'
import json, pathlib, sys
obj=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
if not isinstance(obj,dict):
    raise SystemExit('old API actuator did not return a JSON object')
PY
/home/isp/bin/codex_ws_agent_start.sh status

sha256sum -c "$OLD_SMOKE_PREFLIGHT_RESPONSE.sha256"
OLD_IDENTITY_RESPONSE="$FAILURE_DIR/old-api-identity.json"
curl --fail --silent --show-error "${A[@]}" \
  "$BASE_URL/agent/$OLD_SMOKE_AGENT_ID" > "$OLD_IDENTITY_RESPONSE"
python3 - "$OLD_IDENTITY_RESPONSE" "$OLD_SMOKE_AGENT_ID" <<'PY'
import json, pathlib, sys
obj=json.loads(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))
if not isinstance(obj,dict) or obj.get('status') != 200 or obj.get('code') != 'E0':
    raise SystemExit(f'old API identity smoke failed: {obj!r}')
data=obj.get('data')
if not isinstance(data,dict) or data.get('agentId') != sys.argv[2]:
    raise SystemExit('old API identity returned the wrong Agent')
PY

POST_SMOKE_ROW_COUNTS="$FAILURE_DIR/post-old-smoke-row-counts.tsv"
exact_row_counts "$POST_SMOKE_ROW_COUNTS"
cmp -s "$PRE_ROW_COUNTS" "$POST_SMOKE_ROW_COUNTS" \
  || die 'read-only old-version smoke unexpectedly changed restored row counts'
```

旧 API/agent health、identity read、日志和恢复行数全部通过，且 DBA/Reviewer 对 restore checksum、账户/routine/grant 状态签字后，才可按旧版本变更单恢复写流量。失败时保持停写并升级；不要再次把 dump 重放到当前 schema。

## 11. 失败决策摘要

- 任何 HEAD、SHA、磁盘、停写、事务、dump、restore drill、schema、identity、B09 或 smoke 断言失败：保持停写并升级，不得跳过。
- 未恢复写入时，可在完整灾难恢复审批后执行第 10 节；它必须替换整个 schema 和旧应用/agent，不能只回滚 JAR。
- 已恢复写入或已有跨 scope 同 task ID 时默认 roll-forward；若选择第 10 节，必须明确接受 dump 时点后的数据替换。
- A08/B09 partial apply 失败要保留 run/audit 证据，不手工删除失败记录。
