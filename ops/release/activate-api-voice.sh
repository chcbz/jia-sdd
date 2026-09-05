#!/bin/bash -p
set -Eeuo pipefail
IFS=$'\n\t'
umask 077
export PATH=/usr/sbin:/usr/bin:/sbin:/bin
export LC_ALL=C

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
source "$SCRIPT_DIR/common.sh"
source "$SCRIPT_DIR/lib/api-host-transaction.sh"

INPUT_FILE="$SCRIPT_DIR/jvc-oai-r1-input.json"; CONFIG=''; AUDIO=''; TRANSCRIPT_SHA=''; EXECUTE=0
while (($#)); do
  case "$1" in
    --input) (($#>=2)) || die "--input requires path"; INPUT_FILE="$2"; shift 2 ;;
    --config) (($#>=2)) || die "--config requires path"; CONFIG="$2"; shift 2 ;;
    --audio-fixture) (($#>=2)) || die "--audio-fixture requires path"; AUDIO="$2"; shift 2 ;;
    --expected-transcript-sha256) (($#>=2)) || die "--expected-transcript-sha256 requires digest"; TRANSCRIPT_SHA="$2"; shift 2 ;;
    --execute) EXECUTE=1; shift ;;
    --dry-run) EXECUTE=0; shift ;;
    --help|-h) printf 'Usage: %s --input FILE --config FILE --audio-fixture FILE --expected-transcript-sha256 SHA [--execute]\n' "$0"; exit 0 ;;
    *) die "unknown activation option: $1" ;;
  esac
done
host_load_input "$INPUT_FILE"; host_require_execute_approval
[[ -n "$CONFIG" && -n "$AUDIO" ]] || die "config and audio fixture are required"
require_sha256 "expected transcript SHA" "$TRANSCRIPT_SHA"
[[ ! -L "$CONFIG" && ! -L "$AUDIO" ]] || die "voice inputs must not be symlinks"
CONFIG="$(normalize_absolute_path 'voice config' "$CONFIG")"; AUDIO="$(normalize_absolute_path 'audio fixture' "$AUDIO")"
if host_offline; then CONFIG_EXPECTED="600:$(id -u):$(id -g):1"; else CONFIG_EXPECTED=600:0:0:1; fi
if host_offline; then CONFIG_UID="$(id -u)"; CONFIG_GID="$(id -g)"; else CONFIG_UID=0; CONFIG_GID=0; fi
[[ -f "$CONFIG" && ! -L "$CONFIG" && "$(stat -Lc '%a:%u:%g:%h' "$CONFIG")" == "$CONFIG_EXPECTED" ]] \
  || die "voice config candidate must be 0600 trusted regular nlink1"
[[ -f "$AUDIO" && ! -L "$AUDIO" && "$(stat -Lc %h "$AUDIO")" == 1 ]] || die "audio fixture is unsafe"
VOICE_ENCODED="$(host_parse_voice_config "$CONFIG" all)" || die "voice config validation failed"
VOICE_VALUES=()
while IFS= read -r encoded; do
  [[ -n "$encoded" ]] || continue
  assignment="$(printf '%s' "$encoded" | base64 -d)" || die "voice config decode failed"
  VOICE_VALUES+=("$assignment")
done <<< "$VOICE_ENCODED"
unset VOICE_ENCODED encoded assignment
if (( EXECUTE == 0 )); then
  printf 'DRY_RUN=PASS\nCOMPONENT=api-voice-activation\nCONFIG=VALID_REDACTED\nSMOKE=NOT_PERFORMED\n'
  exit 0
fi

host_prepare_transaction_dirs; host_acquire_release_lock; host_validate_live_jar
host_validate_boot_jar "$LIVE_JAR" || die "live JAR is not a valid Spring Boot artifact"
VOICE_LIVE="$(host_path /opt/cyf/service/api/.voice-runtime.env)"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"; CHANGE_ID="$CYF_RELEASE_APPROVAL_ID"
STAGE="$(dirname -- "$VOICE_LIVE")/.voice-runtime.stage-${CHANGE_ID}"
RESTORE="$(dirname -- "$VOICE_LIVE")/.voice-runtime.restore-${CHANGE_ID}"
BACKUP_DIR="$BACKUP_ROOT/voice-${STAMP}-${CHANGE_ID}"; RECORD="$RECORD_ROOT/voice-activation-${STAMP}-${CHANGE_ID}.json"
mkdir -m 0750 -- "$BACKUP_DIR"; if ! host_offline; then chown root:isp "$BACKUP_DIR"; fi
host_fsync_dir "$BACKUP_ROOT"
CONFIG_SHA="$(host_sha_regular "$CONFIG")"; PREVIOUS_SHA=ABSENT; BACKUP_CONFIG="$BACKUP_DIR/voice-runtime.env"
if [[ -e "$VOICE_LIVE" ]]; then
  [[ -f "$VOICE_LIVE" && ! -L "$VOICE_LIVE" && "$(stat -Lc '%a:%u:%g:%h' "$VOICE_LIVE")" == "$CONFIG_EXPECTED" ]] \
    || die "existing voice config is unsafe"
  PREVIOUS_SHA="$(host_sha_regular "$VOICE_LIVE")"
  host_copy_exclusive "$VOICE_LIVE" "$BACKUP_CONFIG" 0400 "$PREVIOUS_SHA" "$CONFIG_UID" "$CONFIG_GID"
else
  BACKUP_CONFIG=ABSENT
fi
host_copy_exclusive "$CONFIG" "$STAGE" 0600 "$CONFIG_SHA" "$CONFIG_UID" "$CONFIG_GID"
host_record_init "$RECORD" activation "$CHANGE_ID" "$API_HEAD" "$API_TREE" "$BACKUP_CONFIG" "$PREVIOUS_SHA" "$CONFIG_SHA"
PHASE=PREPARED; SMOKE_DIR=''
activation_failure() {
  local rc=$?; trap - EXIT; set +e
  [[ -z "$SMOKE_DIR" || ! -e "$SMOKE_DIR" ]] || rm -rf -- "$SMOKE_DIR"
  case "$PHASE" in
    PREPARED)
      host_record_state "$RECORD" ABORTED_BEFORE_STOP 2>/dev/null || true
      host_finalize_record "$RECORD" 2>/dev/null || true
      ;;
    STOP_RECORDING)
      if ! host_record_state "$RECORD" ABORTED_BEFORE_STOP 2>/dev/null; then
        host_record_state "$RECORD" FAILED_MANUAL_RECOVERY_REQUIRED 2>/dev/null || true
      fi
      host_finalize_record "$RECORD" 2>/dev/null || true
      ;;
    STOP_ATTEMPTED|STOPPED|CANDIDATE_INSTALLED|STARTED_PENDING_SMOKE)
      restore_ok=0
      if host_call_lifecycle stop >/dev/null 2>&1; then
        if [[ "$BACKUP_CONFIG" == ABSENT ]]; then
          host_remove_durable "$VOICE_LIVE" && restore_ok=1
        elif host_copy_exclusive "$BACKUP_CONFIG" "$RESTORE" 0600 "$PREVIOUS_SHA" "$CONFIG_UID" "$CONFIG_GID" \
            && host_replace_durable "$RESTORE" "$VOICE_LIVE"; then
          restore_ok=1
        fi
      fi
      if (( restore_ok == 1 )) && host_call_lifecycle start >/dev/null 2>&1; then
        if ! host_record_state "$RECORD" ROLLED_BACK_HEALTHY 2>/dev/null; then
          host_record_state "$RECORD" FAILED_MANUAL_RECOVERY_REQUIRED 2>/dev/null || true
        fi
      else
        host_record_state "$RECORD" FAILED_MANUAL_RECOVERY_REQUIRED 2>/dev/null || true
      fi
      host_finalize_record "$RECORD" 2>/dev/null || true
      ;;
    STARTED_HEALTHY|COMMITTING)
      host_record_state "$RECORD" FAILED_MANUAL_RECOVERY_REQUIRED 2>/dev/null || true; host_finalize_record "$RECORD" 2>/dev/null || true
      ;;
    COMMITTED)
      host_finalize_record "$RECORD" 2>/dev/null || true
      ;;
  esac
  exit "$rc"
}
trap activation_failure EXIT
PHASE=STOP_RECORDING
host_record_state "$RECORD" STOP_ATTEMPTED
PHASE=STOP_ATTEMPTED
host_call_lifecycle stop; PHASE=STOPPED; host_record_state "$RECORD" STOPPED
host_replace_durable "$STAGE" "$VOICE_LIVE"; PHASE=CANDIDATE_INSTALLED; host_record_state "$RECORD" CANDIDATE_INSTALLED
host_call_lifecycle start
PHASE=STARTED_PENDING_SMOKE

TOKEN=''
for assignment in "${VOICE_VALUES[@]}"; do
  [[ "${assignment%%=*}" == CYF_VOICE_SMOKE_BEARER_TOKEN ]] && TOKEN="${assignment#*=}"
done
[[ -n "$TOKEN" ]] || die "smoke credential was not parsed"
CURL=/usr/bin/curl
if host_offline; then CURL="${CYF_RELEASE_FAKE_CURL:-}"; [[ -x "$CURL" ]] || die "offline fake curl is missing"; fi
SMOKE_DIR="$(mktemp -d "$BACKUP_DIR/.smoke.XXXXXX")"; chmod 0700 "$SMOKE_DIR"
STT_REQUEST_ID="host-stt-${STAMP}-${CHANGE_ID}"
TTS_REQUEST_ID="host-tts-${STAMP}-${CHANGE_ID}"
[[ "$STT_REQUEST_ID" != "$TTS_REQUEST_ID" ]] || die "voice smoke request IDs must be independent"
STT_BODY="$SMOKE_DIR/stt.json"
STT_CODE="$(printf 'Authorization: Bearer %s\n' "$TOKEN" | host_loopback_curl "$CURL" --header @- --silent --show-error \
  --output "$STT_BODY" --write-out '%{http_code}' --request POST \
  --form "audio=@$AUDIO" --form "requestId=$STT_REQUEST_ID" --form 'language=zh-CN' \
  http://127.0.0.1:10018/chat/speech/transcriptions)"
[[ "$STT_CODE" == 200 ]] || die "authenticated STT smoke failed"
/usr/bin/python3 -I -B - "$STT_BODY" "$TRANSCRIPT_SHA" "$STT_REQUEST_ID" <<'PY'
import hashlib, json, sys
with open(sys.argv[1], 'r', encoding='utf-8') as stream: data=json.load(stream)
payload=data.get('data',{})
value=payload.get('text')
if (not isinstance(value,str) or hashlib.sha256(value.encode('utf-8')).hexdigest()!=sys.argv[2]
        or payload.get('requestId') != sys.argv[3]):
    raise SystemExit('STT transcript assertion failed')
PY
TTS_BODY="$SMOKE_DIR/tts.bin"; TTS_HEADERS="$SMOKE_DIR/tts.headers"; TTS_REQUEST="$SMOKE_DIR/tts-request.json"
/usr/bin/python3 -I -B - "$TTS_REQUEST" "$TTS_REQUEST_ID" <<'PY'
import json, os, sys
fd=os.open(sys.argv[1], os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0), 0o600)
with os.fdopen(fd,'w',encoding='utf-8') as stream:
    json.dump({'requestId':sys.argv[2], 'text':'聚义厅语音验收',
               'voice':'juyiting-default', 'format':'mp3'}, stream, sort_keys=True)
    stream.write('\n'); stream.flush(); os.fsync(stream.fileno())
PY
TTS_CODE="$(printf 'Authorization: Bearer %s\n' "$TOKEN" | host_loopback_curl "$CURL" --header @- --silent --show-error \
  --dump-header "$TTS_HEADERS" --output "$TTS_BODY" --write-out '%{http_code}' --request POST \
  --header 'Content-Type: application/json' --data "@$TTS_REQUEST" \
  http://127.0.0.1:10018/chat/speech/synthesis)"
[[ "$TTS_CODE" == 200 && -s "$TTS_BODY" ]] || die "authenticated TTS smoke failed"
/usr/bin/python3 -I -B - "$TTS_HEADERS" "$TTS_BODY" "$TTS_REQUEST_ID" <<'PY'
from pathlib import Path
import re, sys
headers=Path(sys.argv[1]).read_text(encoding='iso-8859-1').replace('\r\n','\n').splitlines()
body=Path(sys.argv[2]).read_bytes(); expected=sys.argv[3]
values={}
for line in headers:
    if ':' not in line: continue
    name,value=line.split(':',1); values.setdefault(name.strip().lower(),[]).append(value.strip())
if values.get('content-type') != ['audio/mpeg']:
    raise SystemExit('TTS MIME assertion failed')
if values.get('x-voice-request-id') != [expected]:
    raise SystemExit('TTS request ID response assertion failed')
if values.get('cache-control') != ['no-store']:
    raise SystemExit('TTS cache-control assertion failed')
if values.get('content-length') != [str(len(body))]:
    raise SystemExit('TTS content-length assertion failed')
if len(body) < 4 or not (body.startswith(b'ID3') or (body[0] == 0xff and body[1] & 0xe0 == 0xe0)):
    raise SystemExit('TTS MP3 body assertion failed')
PY
rm -rf -- "$SMOKE_DIR"; SMOKE_DIR=''
PHASE=STARTED_HEALTHY
host_record_state "$RECORD" STARTED_HEALTHY
PHASE=COMMITTING; host_record_state "$RECORD" COMMITTED
PHASE=COMMITTED; host_finalize_record "$RECORD"
trap - EXIT
printf 'ACTIVATE_API_VOICE=PASS\nSTATUS=COMMITTED\nSTT=AUTHENTICATED_PASS\nTTS=AUTHENTICATED_PASS\nRECORD=%s\n' "$RECORD"
