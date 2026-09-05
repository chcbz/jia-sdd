#!/usr/bin/python3
"""Bounded, fail-closed Juyi Hall service health monitor (Python 3.6 stdlib)."""

import argparse
import copy
import datetime
import errno
import fcntl
import hashlib
import json
import os
import re
import socket
import ssl
import stat
import subprocess
import sys
import tempfile
import time
from urllib import error as urlerror
from urllib import request as urlrequest

SCHEMA_VERSION = 1
CONFIG_PATH = "/etc/cyf-juyiting-health.json"
STATE_DIR = "/var/lib/cyf-juyiting-health"
STATE_PATH = STATE_DIR + "/state.json"
LOCK_PATH = STATE_DIR + "/monitor.lock"
MAINTENANCE_PATH = STATE_DIR + "/maintenance"
CANONICAL = "/usr/local/sbin/cyf-api-kit"
CANONICAL_SHA256 = "56537824cd33f6333f199ea1cebda90b127b39c079e08daad6d164607f788ef5"
MAIL_PYTHON = "/usr/bin/python3"
MAIL_HELPER = "/root/.local/bin/cyf-task-email"
MAIL_HELPER_SHA256 = "ddc540f1d450880af5bb707751cf6cd68b6492e58cb702436b19580867d3ae99"
MAIL_ENV = "/root/.config/cyf-task-monitor/email.env"
WEB_URL = "https://kit.chaoyoufan.cn/juyiting"
API_URL = "https://api.chaoyoufan.cn/agent/map"
USER_AGENT = "CYF-HealthMonitor/1.0"
EXPECTED_RUNTIME_IDENTITY = "cyf-api(987:1000)"
FAILURE_THRESHOLD = 3
HEALTHY_RESET_THRESHOLD = 3
MAX_RECOVERY_ATTEMPTS = 2
COOLDOWN_SECONDS = 30 * 60
STARTUP_GRACE_SECONDS = 25 * 60
MIN_MEMORY_BYTES = 1024 * 1024 * 1024
MIN_DISK_BYTES = 5 * 1024 * 1024 * 1024
MAX_STATE_BYTES = 128 * 1024
MAX_HTTP_BODY = 256 * 1024
MAX_OUTBOX = 24
MAX_NOTICE_IDS = 64
COMPONENTS = ("local_api", "web", "public_api", "mysql", "redis", "agent")
FIXED_ENV = {
    "PATH": "/usr/sbin:/usr/bin:/sbin:/bin",
    "HOME": "/root",
    "LC_ALL": "C",
    "LANG": "C",
    "USER": "root",
    "LOGNAME": "root",
}


class MonitorError(Exception):
    """A bounded, user-safe monitor failure."""


class BusyError(MonitorError):
    """Another monitor process holds the singleton lock."""


def utc_text(epoch):
    return datetime.datetime.utcfromtimestamp(int(epoch)).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_label(value, fallback="error"):
    text = str(value or fallback).lower()
    text = re.sub(r"[^a-z0-9_.:-]+", "_", text).strip("_")
    return (text or fallback)[:80]


def json_no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise MonitorError("duplicate_json_key")
        result[key] = value
    return result


def read_json_fd(fd, maximum):
    chunks = []
    total = 0
    while True:
        data = os.read(fd, min(65536, maximum + 1 - total))
        if not data:
            break
        chunks.append(data)
        total += len(data)
        if total > maximum:
            raise MonitorError("file_too_large")
    try:
        return json.loads(b"".join(chunks).decode("utf-8"), object_pairs_hook=json_no_duplicates)
    except MonitorError:
        raise
    except (UnicodeDecodeError, ValueError):
        raise MonitorError("invalid_json")


def validate_parent_chain(path, expected_uid=0):
    current = os.path.abspath(os.path.dirname(path))
    while True:
        try:
            info = os.lstat(current)
        except OSError:
            raise MonitorError("missing_parent")
        if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
            raise MonitorError("unsafe_parent_type")
        if info.st_uid != expected_uid or stat.S_IMODE(info.st_mode) & 0o022:
            raise MonitorError("unsafe_parent_permissions")
        if current == "/":
            break
        current = os.path.dirname(current)


def validate_regular(path, expected_mode=None, expected_uid=0, maximum=None,
                     validate_parents=True, require_executable=False):
    if validate_parents:
        validate_parent_chain(path, expected_uid)
    try:
        info = os.lstat(path)
    except OSError:
        raise MonitorError("missing_file")
    if not stat.S_ISREG(info.st_mode) or stat.S_ISLNK(info.st_mode):
        raise MonitorError("unsafe_file_type")
    if info.st_uid != expected_uid or info.st_nlink != 1:
        raise MonitorError("unsafe_file_identity")
    mode = stat.S_IMODE(info.st_mode)
    if expected_mode is not None and mode != expected_mode:
        raise MonitorError("unsafe_file_mode")
    if mode & 0o022:
        raise MonitorError("writable_trusted_file")
    if maximum is not None and info.st_size > maximum:
        raise MonitorError("file_too_large")
    if require_executable and not mode & 0o100:
        raise MonitorError("file_not_executable")
    return info


def validate_directory(path, expected_mode=0o700, expected_uid=0, validate_parents=True):
    if validate_parents:
        validate_parent_chain(path, expected_uid)
    try:
        info = os.lstat(path)
    except OSError:
        raise MonitorError("missing_directory")
    if not stat.S_ISDIR(info.st_mode) or stat.S_ISLNK(info.st_mode):
        raise MonitorError("unsafe_directory_type")
    if info.st_uid != expected_uid or stat.S_IMODE(info.st_mode) != expected_mode:
        raise MonitorError("unsafe_directory_permissions")
    return info


def sha256_file(path):
    digest = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            chunk = stream.read(65536)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def load_config(path=CONFIG_PATH, expected_uid=0, validate_parents=True):
    validate_regular(path, expected_mode=0o600, expected_uid=expected_uid,
                     maximum=8192, validate_parents=validate_parents)
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        fd = os.open(path, flags)
    except OSError:
        raise MonitorError("config_open_failed")
    try:
        info = os.fstat(fd)
        if not stat.S_ISREG(info.st_mode) or info.st_uid != expected_uid \
                or stat.S_IMODE(info.st_mode) != 0o600 or info.st_nlink != 1:
            raise MonitorError("config_identity_changed")
        config = read_json_fd(fd, 8192)
    finally:
        os.close(fd)
    if not isinstance(config, dict):
        raise MonitorError("config_not_object")
    allowed = {"schema_version", "web_marker", "email_enabled", "reminder_interval_seconds"}
    if set(config) != allowed:
        raise MonitorError("config_keys_invalid")
    if config.get("schema_version") != SCHEMA_VERSION:
        raise MonitorError("config_schema_invalid")
    marker = config.get("web_marker")
    if not isinstance(marker, str) or not 1 <= len(marker) <= 128 \
            or any(ord(char) < 0x20 for char in marker):
        raise MonitorError("web_marker_invalid")
    if not isinstance(config.get("email_enabled"), bool):
        raise MonitorError("email_enabled_invalid")
    reminder = config.get("reminder_interval_seconds")
    if isinstance(reminder, bool) or not isinstance(reminder, int) \
            or reminder < 21600 or reminder > 604800:
        raise MonitorError("reminder_interval_invalid")
    return config


def initial_state(now):
    return {
        "schema_version": SCHEMA_VERSION,
        "initialized_at": int(now),
        "updated_at": int(now),
        "sequence": 0,
        "component_streaks": {name: 0 for name in COMPONENTS},
        "all_healthy_streak": 0,
        "api_healthy_streak": 0,
        "incident": None,
        "recovery": {
            "attempts": 0,
            "circuit_latched": False,
            "last_attempt_at": None,
            "in_flight": None,
            "last_result": None,
            "last_success_at": None,
        },
        "outbox": [],
        "notice_ids": [],
        "last_snapshot": None,
    }


def _is_int(value, minimum=0):
    return isinstance(value, int) and not isinstance(value, bool) and value >= minimum


def validate_state(data):
    expected = {
        "schema_version", "initialized_at", "updated_at", "sequence",
        "component_streaks", "all_healthy_streak", "api_healthy_streak",
        "incident", "recovery", "outbox", "notice_ids", "last_snapshot",
    }
    if not isinstance(data, dict) or set(data) != expected:
        raise MonitorError("state_keys_invalid")
    if data.get("schema_version") != SCHEMA_VERSION:
        raise MonitorError("state_schema_invalid")
    for key in ("initialized_at", "updated_at", "sequence", "all_healthy_streak", "api_healthy_streak"):
        if not _is_int(data.get(key)):
            raise MonitorError("state_counter_invalid")
    streaks = data.get("component_streaks")
    if not isinstance(streaks, dict) or set(streaks) != set(COMPONENTS):
        raise MonitorError("state_streaks_invalid")
    if any(not _is_int(value) for value in streaks.values()):
        raise MonitorError("state_streak_invalid")
    incident = data.get("incident")
    if incident is not None:
        if not isinstance(incident, dict) or set(incident) != {"id", "opened_at", "components", "last_reminder_slot"}:
            raise MonitorError("state_incident_invalid")
        if not isinstance(incident["id"], str) or len(incident["id"]) > 80 \
                or not _is_int(incident["opened_at"]) \
                or not isinstance(incident["components"], list) \
                or any(item not in COMPONENTS for item in incident["components"]) \
                or not _is_int(incident["last_reminder_slot"]):
            raise MonitorError("state_incident_fields_invalid")
    recovery = data.get("recovery")
    recovery_keys = {"attempts", "circuit_latched", "last_attempt_at", "in_flight",
                     "last_result", "last_success_at"}
    if not isinstance(recovery, dict) or set(recovery) != recovery_keys:
        raise MonitorError("state_recovery_invalid")
    if not _is_int(recovery["attempts"]) or recovery["attempts"] > MAX_RECOVERY_ATTEMPTS \
            or not isinstance(recovery["circuit_latched"], bool):
        raise MonitorError("state_recovery_fields_invalid")
    for key in ("last_attempt_at", "last_success_at"):
        if recovery[key] is not None and not _is_int(recovery[key]):
            raise MonitorError("state_recovery_time_invalid")
    if recovery["in_flight"] is not None:
        flight = recovery["in_flight"]
        if not isinstance(flight, dict) or set(flight) != {"action", "attempt", "at"} \
                or flight["action"] not in ("start", "restart") \
                or not _is_int(flight["attempt"], 1) or not _is_int(flight["at"]):
            raise MonitorError("state_in_flight_invalid")
    if recovery["last_result"] is not None:
        result = recovery["last_result"]
        if not isinstance(result, dict) or set(result) != {"at", "action", "attempt", "classification"} \
                or result["action"] not in ("start", "restart") \
                or not _is_int(result["at"]) or not _is_int(result["attempt"], 1) \
                or not isinstance(result["classification"], str) or len(result["classification"]) > 80:
            raise MonitorError("state_recovery_result_invalid")
    outbox = data.get("outbox")
    if not isinstance(outbox, list) or len(outbox) > MAX_OUTBOX:
        raise MonitorError("state_outbox_invalid")
    notice_keys = {"id", "event", "subject", "body", "created_at", "attempts", "next_attempt_at", "last_error"}
    for item in outbox:
        if not isinstance(item, dict) or set(item) != notice_keys:
            raise MonitorError("state_notice_invalid")
        if any(not isinstance(item[key], str) or len(item[key]) > limit for key, limit in
               (("id", 128), ("event", 40), ("subject", 160), ("body", 2000), ("last_error", 80))):
            raise MonitorError("state_notice_text_invalid")
        if not _is_int(item["created_at"]) or not _is_int(item["attempts"]) \
                or not _is_int(item["next_attempt_at"]):
            raise MonitorError("state_notice_counter_invalid")
    ids = data.get("notice_ids")
    if not isinstance(ids, list) or len(ids) > MAX_NOTICE_IDS \
            or any(not isinstance(item, str) or len(item) > 128 for item in ids):
        raise MonitorError("state_notice_ids_invalid")
    snapshot = data["last_snapshot"]
    if snapshot is not None:
        if not isinstance(snapshot, dict) or set(snapshot) != {"at", "maintenance", "overall_healthy", "checks", "recovery"}:
            raise MonitorError("state_snapshot_invalid")
        if not _is_int(snapshot["at"]) or not isinstance(snapshot["maintenance"], bool) \
                or not isinstance(snapshot["overall_healthy"], bool):
            raise MonitorError("state_snapshot_fields_invalid")
        checks = snapshot["checks"]
        allowed_checks = set(COMPONENTS) | {"local_api_post_recovery"}
        if not isinstance(checks, dict) or not set(COMPONENTS).issubset(set(checks)) \
                or not set(checks).issubset(allowed_checks):
            raise MonitorError("state_snapshot_checks_invalid")
        allowed_result = {"healthy", "classification", "http_status", "pid", "elapsed_seconds",
                          "returncode", "content_type"}
        for result in checks.values():
            if not isinstance(result, dict) or not {"healthy", "classification"}.issubset(set(result)) \
                    or not set(result).issubset(allowed_result) \
                    or not isinstance(result["healthy"], bool) \
                    or not isinstance(result["classification"], str) \
                    or len(result["classification"]) > 80:
                raise MonitorError("state_snapshot_result_invalid")
            for key in ("http_status", "pid", "elapsed_seconds", "returncode"):
                if key in result and (not isinstance(result[key], int) or isinstance(result[key], bool)):
                    raise MonitorError("state_snapshot_number_invalid")
            if "content_type" in result and (not isinstance(result["content_type"], str)
                                             or len(result["content_type"]) > 80):
                raise MonitorError("state_snapshot_content_type_invalid")
        recovery_snapshot = snapshot["recovery"]
        allowed_recovery = {"decision", "result", "resource_preflight"}
        if not isinstance(recovery_snapshot, dict) or set(recovery_snapshot) - allowed_recovery \
                or not {"decision", "result"}.issubset(set(recovery_snapshot)) \
                or any(not isinstance(value, str) or len(value) > 80
                       for value in recovery_snapshot.values()):
            raise MonitorError("state_snapshot_recovery_invalid")
    return data


class StateStore(object):
    def __init__(self, state_dir=STATE_DIR, expected_uid=0, validate_parents=True):
        self.state_dir = state_dir
        self.state_path = os.path.join(state_dir, "state.json")
        self.lock_path = os.path.join(state_dir, "monitor.lock")
        self.maintenance_path = os.path.join(state_dir, "maintenance")
        self.expected_uid = expected_uid
        self.validate_parents = validate_parents
        self.lock_fd = None

    def prepare_init(self):
        if self.validate_parents:
            validate_parent_chain(self.state_dir, self.expected_uid)
        try:
            os.mkdir(self.state_dir, 0o700)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise MonitorError("state_directory_create_failed")
        validate_directory(self.state_dir, 0o700, self.expected_uid, self.validate_parents)
        if os.path.lexists(self.lock_path):
            validate_regular(self.lock_path, 0o600, self.expected_uid, 4096, False)
        else:
            flags = os.O_RDWR | os.O_CREAT | os.O_EXCL
            if hasattr(os, "O_NOFOLLOW"):
                flags |= os.O_NOFOLLOW
            fd = os.open(self.lock_path, flags, 0o600)
            try:
                os.fchmod(fd, 0o600)
            finally:
                os.close(fd)
            validate_regular(self.lock_path, 0o600, self.expected_uid, 4096, False)

    def acquire(self):
        validate_directory(self.state_dir, 0o700, self.expected_uid, self.validate_parents)
        validate_regular(self.lock_path, 0o600, self.expected_uid, 4096, False)
        flags = os.O_RDWR
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        self.lock_fd = os.open(self.lock_path, flags)
        info = os.fstat(self.lock_fd)
        path_info = os.lstat(self.lock_path)
        if (info.st_dev, info.st_ino) != (path_info.st_dev, path_info.st_ino) \
                or info.st_uid != self.expected_uid or info.st_nlink != 1 \
                or stat.S_IMODE(info.st_mode) != 0o600:
            self.release()
            raise MonitorError("lock_identity_changed")
        try:
            fcntl.flock(self.lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError as exc:
            self.release()
            if exc.errno in (errno.EACCES, errno.EAGAIN):
                raise BusyError("monitor_lock_busy")
            raise MonitorError("monitor_lock_failed")

    def release(self):
        if self.lock_fd is not None:
            try:
                os.close(self.lock_fd)
            finally:
                self.lock_fd = None

    def read(self):
        validate_regular(self.state_path, 0o600, self.expected_uid, MAX_STATE_BYTES, False)
        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            fd = os.open(self.state_path, flags)
        except OSError:
            raise MonitorError("state_open_failed")
        try:
            info = os.fstat(fd)
            if info.st_uid != self.expected_uid or info.st_nlink != 1 \
                    or stat.S_IMODE(info.st_mode) != 0o600 or not stat.S_ISREG(info.st_mode):
                raise MonitorError("state_identity_changed")
            data = read_json_fd(fd, MAX_STATE_BYTES)
        finally:
            os.close(fd)
        return validate_state(data)

    def write(self, data):
        validate_directory(self.state_dir, 0o700, self.expected_uid, self.validate_parents)
        validate_state(data)
        payload = (json.dumps(data, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        if len(payload) > MAX_STATE_BYTES:
            raise MonitorError("state_serialized_too_large")
        fd = None
        temporary = None
        try:
            fd, temporary = tempfile.mkstemp(prefix=".state.", dir=self.state_dir)
            os.fchmod(fd, 0o600)
            if os.geteuid() == 0:
                os.fchown(fd, self.expected_uid, -1)
            written = 0
            while written < len(payload):
                written += os.write(fd, payload[written:])
            os.fsync(fd)
            os.close(fd)
            fd = None
            os.replace(temporary, self.state_path)
            temporary = None
            directory_fd = os.open(self.state_dir, os.O_RDONLY)
            try:
                os.fsync(directory_fd)
            finally:
                os.close(directory_fd)
        finally:
            if fd is not None:
                os.close(fd)
            if temporary is not None:
                try:
                    os.unlink(temporary)
                except OSError:
                    pass

    def maintenance(self):
        if not os.path.lexists(self.maintenance_path):
            return False
        validate_regular(self.maintenance_path, 0o600, self.expected_uid, 4096, False)
        return True

    def pause(self, now):
        if os.path.lexists(self.maintenance_path):
            validate_regular(self.maintenance_path, 0o600, self.expected_uid, 4096, False)
            return
        payload = ("maintenance paused at %s\n" % utc_text(now)).encode("ascii")
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = os.open(self.maintenance_path, flags, 0o600)
        try:
            os.write(fd, payload)
            os.fsync(fd)
        finally:
            os.close(fd)

    def resume(self):
        if not os.path.lexists(self.maintenance_path):
            return
        validate_regular(self.maintenance_path, 0o600, self.expected_uid, 4096, False)
        os.unlink(self.maintenance_path)
        directory_fd = os.open(self.state_dir, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)


class NoRedirect(urlrequest.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def parse_elapsed(value):
    if not isinstance(value, str) or not re.match(r"^(?:\d+-)?\d{1,2}:\d{2}(?::\d{2})?$", value):
        return None
    days = 0
    rest = value
    if "-" in rest:
        day_text, rest = rest.split("-", 1)
        days = int(day_text)
    parts = [int(item) for item in rest.split(":")]
    if len(parts) == 2:
        hours, minutes, seconds = 0, parts[0], parts[1]
    else:
        hours, minutes, seconds = parts
    if minutes >= 60 or seconds >= 60:
        return None
    return days * 86400 + hours * 3600 + minutes * 60 + seconds


def parse_canonical_status(returncode, stdout):
    if not isinstance(stdout, str) or len(stdout) > 65536:
        return {"healthy": False, "classification": "canonical_output_invalid", "recovery_safe": False}
    fields = {}
    for line in stdout.splitlines():
        if re.match(r"^[A-Z0-9_]+=", line):
            key, value = line.split("=", 1)
            if key in fields or len(key) > 64 or len(value) > 256:
                return {"healthy": False, "classification": "canonical_output_invalid", "recovery_safe": False}
            fields[key] = value
    pid = fields.get("PID")
    pid_value = int(pid) if pid and pid.isdigit() and int(pid) > 1 else None
    elapsed = None
    if pid_value is not None:
        pattern = r"^\s*%d\s+\d+\s+\S+\s+\S+\s+\d+\s+\S+\s+\d{4}\s+(\S+)\s+" % pid_value
        for line in stdout.splitlines():
            match = re.match(pattern, line)
            if match:
                elapsed = parse_elapsed(match.group(1))
                break
    common = {
        "pid": pid_value,
        "elapsed_seconds": elapsed,
        "returncode": int(returncode),
        "recovery_safe": False,
    }
    if returncode == 0:
        trusted = fields.get("STATUS") == "RUNNING" \
            and fields.get("ARTIFACT_ATTESTATION") == "MATCH" \
            and fields.get("PORT_10018") == "LISTENING_BY_PID" \
            and fields.get("RUNTIME_IDENTITY") == EXPECTED_RUNTIME_IDENTITY \
            and fields.get("HEALTH") == "UP" and pid_value is not None
        common.update({"healthy": trusted,
                       "classification": "up" if trusted else "canonical_up_invalid"})
        return common
    if returncode == 3:
        stopped = fields.get("STATUS") == "STOPPED" and fields.get("PORT_10018") == "NOT_LISTENING"
        common.update({"healthy": False,
                       "classification": "stopped" if stopped else "stopped_transient_or_invalid",
                       "recovery_safe": stopped})
        return common
    if returncode == 4:
        trusted_not_ready = fields.get("STATUS") == "RUNNING" \
            and fields.get("ARTIFACT_ATTESTATION") == "MATCH" \
            and fields.get("PORT_10018") == "LISTENING_BY_PID" \
            and fields.get("RUNTIME_IDENTITY") == EXPECTED_RUNTIME_IDENTITY \
            and fields.get("HEALTH") == "NOT_READY" \
            and pid_value is not None and elapsed is not None
        common.update({"healthy": False,
                       "classification": "not_ready_trusted" if trusted_not_ready else "not_ready_identity_incomplete",
                       "recovery_safe": trusted_not_ready})
        return common
    if returncode == 1:
        common.update({"healthy": False, "classification": "canonical_busy_or_error"})
        return common
    if returncode == 5:
        common.update({"healthy": False, "classification": "canonical_unsafe_identity_or_listener"})
        return common
    common.update({"healthy": False, "classification": "canonical_returncode_unknown"})
    return common


class Effects(object):
    def _run(self, argv, timeout):
        process = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, cwd="/", env=dict(FIXED_ENV),
                                   universal_newlines=True)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            process.communicate()
            return {"returncode": 124, "classification": "timeout", "stdout": "", "stderr": ""}
        return {"returncode": process.returncode, "classification": "completed",
                "stdout": stdout[:65537], "stderr": stderr[:4097]}

    def _trusted_canonical(self):
        try:
            validate_regular(CANONICAL, 0o755, 0, 1024 * 1024, True, True)
            return sha256_file(CANONICAL) == CANONICAL_SHA256
        except (MonitorError, OSError):
            return False

    def canonical_status(self):
        if not self._trusted_canonical():
            return {"healthy": False, "classification": "canonical_file_untrusted",
                    "recovery_safe": False, "returncode": None, "pid": None,
                    "elapsed_seconds": None}
        result = self._run([CANONICAL, "status"], 15)
        if result["classification"] == "timeout":
            return {"healthy": False, "classification": "canonical_status_timeout",
                    "recovery_safe": False, "returncode": 124, "pid": None,
                    "elapsed_seconds": None}
        return parse_canonical_status(result["returncode"], result["stdout"])

    def recover(self, action):
        if action not in ("start", "restart") or not self._trusted_canonical():
            return {"returncode": 126, "classification": "canonical_file_untrusted"}
        result = self._run([CANONICAL, action], None)
        return {"returncode": result["returncode"],
                "classification": "exit_%d" % result["returncode"]}

    def _http(self, url):
        req = urlrequest.Request(url, headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/json",
            "Accept-Encoding": "identity",
            "Cache-Control": "no-cache",
        })
        opener = urlrequest.build_opener(NoRedirect(), urlrequest.HTTPSHandler(context=ssl.create_default_context()))
        try:
            response = opener.open(req, timeout=8)
        except urlerror.HTTPError as exc:
            response = exc
        try:
            status_code = int(response.getcode())
            content_type = (response.headers.get("Content-Type") or "").split(";", 1)[0].strip().lower()
            body = response.read(MAX_HTTP_BODY + 1)
            if len(body) > MAX_HTTP_BODY:
                return status_code, content_type, None, "body_too_large"
            return status_code, content_type, body, "completed"
        finally:
            response.close()

    def web(self, marker):
        try:
            status_code, content_type, body, classification = self._http(WEB_URL)
            healthy = classification == "completed" and status_code == 200 \
                and content_type == "text/html" and marker.encode("utf-8") in body
            return {"healthy": healthy, "classification": "web_ok" if healthy else "web_invalid",
                    "http_status": status_code, "content_type": content_type[:80]}
        except Exception as exc:
            return {"healthy": False, "classification": "web_%s" % safe_label(type(exc).__name__)}

    def public_api(self):
        try:
            status_code, content_type, body, classification = self._http(API_URL)
            valid = False
            if classification == "completed" and status_code in (401, 403) \
                    and content_type in ("application/json", "application/problem+json"):
                try:
                    payload = json.loads(body.decode("utf-8"), object_pairs_hook=json_no_duplicates)
                except (UnicodeDecodeError, ValueError, MonitorError):
                    payload = None
                if isinstance(payload, dict):
                    values = []
                    for key in ("code", "status", "error", "message", "msg", "detail"):
                        if key in payload and isinstance(payload[key], (str, int)) and not isinstance(payload[key], bool):
                            values.append(str(payload[key]).lower())
                    joined = " ".join(values)
                    markers = ("401", "403", "unauthorized", "forbidden", "authentication",
                               "access denied", "未认证", "未授权", "登录", "token")
                    valid = any(marker in joined for marker in markers)
            return {"healthy": valid,
                    "classification": "auth_boundary_ok" if valid else "auth_boundary_invalid",
                    "http_status": status_code, "content_type": content_type[:80]}
        except Exception as exc:
            return {"healthy": False, "classification": "public_api_%s" % safe_label(type(exc).__name__)}

    def mysql(self):
        try:
            sock = socket.create_connection(("127.0.0.1", 3306), timeout=3)
            try:
                sock.settimeout(3)
                data = sock.recv(64)
            finally:
                sock.close()
            healthy = bool(data)
            return {"healthy": healthy, "classification": "mysql_reachable" if healthy else "mysql_no_handshake"}
        except Exception as exc:
            return {"healthy": False, "classification": "mysql_%s" % safe_label(type(exc).__name__)}

    def redis(self):
        try:
            sock = socket.create_connection(("127.0.0.1", 6379), timeout=3)
            try:
                sock.settimeout(3)
                sock.sendall(b"PING\r\n")
                data = sock.recv(128)
            finally:
                sock.close()
            healthy = data.startswith((b"+PONG", b"-NOAUTH", b"-NOPERM"))
            return {"healthy": healthy,
                    "classification": "redis_reachable" if healthy else "redis_unexpected_reply"}
        except Exception as exc:
            return {"healthy": False, "classification": "redis_%s" % safe_label(type(exc).__name__)}

    def agent(self):
        try:
            result = self._run(["/usr/bin/systemctl", "is-active", "codex-ws-agent.service"], 5)
            active = result["returncode"] == 0 and result["stdout"].strip() == "active"
            return {"healthy": active, "classification": "agent_active" if active else "agent_inactive"}
        except Exception as exc:
            return {"healthy": False, "classification": "agent_%s" % safe_label(type(exc).__name__)}

    def resources(self):
        try:
            available = None
            with open("/proc/meminfo", "r") as stream:
                for line in stream:
                    if line.startswith("MemAvailable:"):
                        available = int(line.split()[1]) * 1024
                        break
            disk = os.statvfs("/opt/cyf/service/api").f_bavail * os.statvfs("/opt/cyf/service/api").f_frsize
            healthy = available is not None and available >= MIN_MEMORY_BYTES and disk >= MIN_DISK_BYTES
            return {"healthy": healthy,
                    "classification": "resources_ok" if healthy else "resources_below_canonical_minimum"}
        except Exception as exc:
            return {"healthy": False, "classification": "resources_%s" % safe_label(type(exc).__name__)}

    def send_email(self, subject, body):
        try:
            validate_regular(MAIL_PYTHON, 0o755, 0, 1024 * 1024, True, True)
            validate_regular(MAIL_HELPER, 0o700, 0, 1024 * 1024, True, False)
            validate_regular(MAIL_ENV, 0o600, 0, 8192, True, False)
            if sha256_file(MAIL_HELPER) != MAIL_HELPER_SHA256:
                return False, "mail_helper_hash_mismatch"
            result = self._run([MAIL_PYTHON, "-I", MAIL_HELPER, subject[:160], body[:2000]], 30)
            return result["returncode"] == 0, "helper_accepted" if result["returncode"] == 0 else "helper_failed"
        except Exception as exc:
            return False, "mail_%s" % safe_label(type(exc).__name__)


def sanitized_result(result):
    clean = {
        "healthy": bool(result.get("healthy")),
        "classification": safe_label(result.get("classification")),
    }
    for key in ("http_status", "pid", "elapsed_seconds", "returncode"):
        value = result.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            clean[key] = value
    if isinstance(result.get("content_type"), str):
        clean["content_type"] = safe_label(result["content_type"], "unknown")
    return clean


def notice_body(event, now, incident_id, components, extra=""):
    component_text = ",".join(sorted(components)) if components else "none"
    lines = [
        "CYF Juyi Hall health monitor event: %s" % event,
        "time_utc=%s" % utc_text(now),
        "incident=%s" % (incident_id or "none"),
        "components=%s" % component_text,
    ]
    if extra:
        lines.append(extra[:500])
    lines.append("SMTP helper acceptance does not prove inbox delivery.")
    return "\n".join(lines)


def enqueue_notice(state, notice_id, event, subject, body, now):
    if notice_id in state["notice_ids"]:
        return False
    state["notice_ids"].append(notice_id)
    state["notice_ids"] = state["notice_ids"][-MAX_NOTICE_IDS:]
    item = {
        "id": notice_id[:128], "event": event[:40], "subject": subject[:160],
        "body": body[:2000], "created_at": int(now), "attempts": 0,
        "next_attempt_at": int(now), "last_error": "",
    }
    if len(state["outbox"]) >= MAX_OUTBOX:
        for index, pending in enumerate(state["outbox"]):
            if pending["event"] == "reminder":
                state["outbox"].pop(index)
                break
    if len(state["outbox"]) >= MAX_OUTBOX:
        digest = next((pending for pending in state["outbox"] if pending["event"] == "digest"), None)
        if digest is None:
            replaced = state["outbox"].pop(0)
            digest = {
                "id": "outbox-digest", "event": "digest",
                "subject": "CYF health monitor pending event digest",
                "body": "coalesced_count=2 latest=%s,%s" % (replaced["event"], event),
                "created_at": int(now), "attempts": 0, "next_attempt_at": int(now),
                "last_error": "",
            }
            state["outbox"].insert(0, digest)
        else:
            match = re.search(r"coalesced_count=(\d+)", digest["body"])
            count = int(match.group(1)) + 1 if match else 2
            digest["body"] = "coalesced_count=%d latest=%s" % (count, event[:40])
            digest["next_attempt_at"] = min(digest["next_attempt_at"], int(now))
        return True
    state["outbox"].append(item)
    return True


def flush_outbox(state, effects, config, now, limit=2):
    if not config["email_enabled"]:
        return 0
    delivered = 0
    examined = 0
    index = 0
    while index < len(state["outbox"]) and examined < limit:
        item = state["outbox"][index]
        if item["next_attempt_at"] > now:
            index += 1
            continue
        examined += 1
        accepted, classification = effects.send_email(item["subject"], item["body"])
        if accepted:
            state["outbox"].pop(index)
            delivered += 1
            continue
        item["attempts"] += 1
        delay = min(21600, 300 * (2 ** min(item["attempts"], 6)))
        item["next_attempt_at"] = int(now + delay)
        item["last_error"] = safe_label(classification)
        index += 1
    return delivered


class Monitor(object):
    def __init__(self, effects, persist, clock=None):
        self.effects = effects
        self.persist = persist
        self.clock = clock or time.time

    def _probe(self, function, fallback):
        try:
            result = function()
            if not isinstance(result, dict) or "healthy" not in result or "classification" not in result:
                raise MonitorError("probe_shape_invalid")
            return result
        except Exception as exc:
            return {"healthy": False, "classification": "%s_%s" % (fallback, safe_label(type(exc).__name__))}

    def check_once(self, state, config, maintenance=False):
        now = int(self.clock())
        status = self._probe(self.effects.canonical_status, "canonical")
        results = {
            "local_api": status,
            "web": self._probe(lambda: self.effects.web(config["web_marker"]), "web"),
            "public_api": self._probe(self.effects.public_api, "public_api"),
            "mysql": self._probe(self.effects.mysql, "mysql"),
            "redis": self._probe(self.effects.redis, "redis"),
            "agent": self._probe(self.effects.agent, "agent"),
        }
        for name in COMPONENTS:
            if results[name]["healthy"]:
                state["component_streaks"][name] = 0
            else:
                state["component_streaks"][name] += 1
        all_healthy = all(results[name]["healthy"] for name in COMPONENTS)
        state["all_healthy_streak"] = state["all_healthy_streak"] + 1 if all_healthy else 0
        if status["healthy"]:
            state["api_healthy_streak"] += 1
        else:
            state["api_healthy_streak"] = 0
        if state["api_healthy_streak"] >= HEALTHY_RESET_THRESHOLD:
            state["recovery"].update({
                "attempts": 0, "circuit_latched": False, "last_attempt_at": None,
                "in_flight": None, "last_result": None,
            })
        confirmed = sorted(name for name in COMPONENTS
                           if state["component_streaks"][name] >= FAILURE_THRESHOLD)
        if state["incident"] is None and confirmed:
            state["sequence"] += 1
            incident_id = "I%06d-%d" % (state["sequence"], now)
            state["incident"] = {"id": incident_id, "opened_at": now,
                                 "components": confirmed, "last_reminder_slot": 0}
            enqueue_notice(state, "incident:%s:confirmed" % incident_id, "incident_confirmed",
                           "CYF Juyi Hall incident confirmed",
                           notice_body("incident_confirmed", now, incident_id, confirmed), now)
        elif state["incident"] is not None:
            state["incident"]["components"] = confirmed or state["incident"]["components"]
            if state["all_healthy_streak"] >= HEALTHY_RESET_THRESHOLD:
                incident = state["incident"]
                enqueue_notice(state, "incident:%s:resolved" % incident["id"], "resolved",
                               "CYF Juyi Hall incident resolved",
                               notice_body("resolved_after_three_healthy_checks", now,
                                           incident["id"], incident["components"]), now)
                state["incident"] = None
            else:
                incident = state["incident"]
                slot = max(0, (now - incident["opened_at"]) // config["reminder_interval_seconds"])
                if slot > incident["last_reminder_slot"]:
                    incident["last_reminder_slot"] = slot
                    enqueue_notice(state, "incident:%s:reminder:%d" % (incident["id"], slot),
                                   "reminder", "CYF Juyi Hall incident reminder",
                                   notice_body("restrained_reminder", now, incident["id"],
                                               incident["components"]), now)
        state["last_snapshot"] = {
            "at": now, "maintenance": bool(maintenance), "overall_healthy": all_healthy,
            "checks": {name: sanitized_result(results[name]) for name in COMPONENTS},
            "recovery": {"decision": "none", "result": "not_attempted"},
        }
        state["updated_at"] = now
        self.persist(state)

        decision = self._recovery_decision(state, status, results, maintenance, now)
        state["last_snapshot"]["recovery"]["decision"] = decision["classification"]
        action = decision.get("action")
        pre_recovery_mail_accepted = 0
        if action:
            resources = self._probe(self.effects.resources, "resources")
            state["last_snapshot"]["recovery"]["resource_preflight"] = safe_label(resources["classification"])
            if not resources["healthy"]:
                incident_id = state["incident"]["id"] if state["incident"] else "unconfirmed"
                slot = now // COOLDOWN_SECONDS
                enqueue_notice(state, "incident:%s:resources:%d" % (incident_id, slot),
                               "recovery_deferred", "CYF API recovery deferred by resources",
                               notice_body("recovery_deferred_resources", now, incident_id,
                                           ["local_api"], "canonical minimum resources not met"), now)
                state["last_snapshot"]["recovery"]["decision"] = "resources_blocked"
                action = None
        if action:
            recovery = state["recovery"]
            attempt = recovery["attempts"] + 1
            recovery["attempts"] = attempt
            recovery["last_attempt_at"] = now
            recovery["in_flight"] = {"action": action, "attempt": attempt, "at": now}
            incident_id = state["incident"]["id"] if state["incident"] else "unconfirmed"
            enqueue_notice(state, "incident:%s:recovery:%d:attempted" % (incident_id, attempt),
                           "recovery_attempted", "CYF API recovery attempted",
                           notice_body("recovery_attempted", now, incident_id, ["local_api"],
                                       "action=%s attempt=%d" % (action, attempt)), now)
            state["updated_at"] = now
            self.persist(state)  # durable attempt fence before canonical lifecycle command
            pre_recovery_mail_accepted = flush_outbox(state, self.effects, config, now, 2)
            self.persist(state)  # delivery outcome is durable before the long canonical wait
            try:
                command_result = self.effects.recover(action)
                if not isinstance(command_result, dict) or not isinstance(command_result.get("returncode"), int):
                    raise MonitorError("recovery_result_invalid")
            except Exception as exc:
                command_result = {"returncode": 126,
                                  "classification": "recovery_%s" % safe_label(type(exc).__name__)}
            fresh = self._probe(self.effects.canonical_status, "canonical_post_recovery")
            success = command_result.get("returncode") == 0 and fresh.get("healthy") is True
            classification = "success_health_up" if success else "failed_fresh_health_not_up"
            recovery["in_flight"] = None
            recovery["last_result"] = {"at": now, "action": action, "attempt": attempt,
                                       "classification": classification}
            if success:
                recovery["last_success_at"] = now
                state["api_healthy_streak"] = 1
                state["component_streaks"]["local_api"] = 0
            if recovery["attempts"] >= MAX_RECOVERY_ATTEMPTS:
                recovery["circuit_latched"] = True
            state["last_snapshot"]["checks"]["local_api_post_recovery"] = sanitized_result(fresh)
            state["last_snapshot"]["recovery"]["result"] = classification
            enqueue_notice(state, "incident:%s:recovery:%d:result" % (incident_id, attempt),
                           "recovery_result", "CYF API recovery result",
                           notice_body("recovery_result", now, incident_id, ["local_api"],
                                       "action=%s attempt=%d result=%s" %
                                       (action, attempt, classification)), now)
            self.persist(state)
        delivered = pre_recovery_mail_accepted + flush_outbox(state, self.effects, config, now, 2)
        state["updated_at"] = now
        self.persist(state)
        return {"healthy": all_healthy, "maintenance": bool(maintenance),
                "recovery": state["last_snapshot"]["recovery"],
                "mail_accepted": delivered, "mail_pending": len(state["outbox"])}

    def _recovery_decision(self, state, status, results, maintenance, now):
        if maintenance:
            return {"classification": "maintenance_paused"}
        if status.get("healthy"):
            return {"classification": "local_api_up"}
        if state["component_streaks"]["local_api"] < FAILURE_THRESHOLD:
            return {"classification": "failure_threshold_not_met"}
        if not results["mysql"]["healthy"] or not results["redis"]["healthy"]:
            return {"classification": "dependencies_unreachable"}
        recovery = state["recovery"]
        if recovery["circuit_latched"] or recovery["attempts"] >= MAX_RECOVERY_ATTEMPTS:
            recovery["circuit_latched"] = True
            return {"classification": "circuit_latched"}
        if recovery["last_attempt_at"] is not None \
                and now - recovery["last_attempt_at"] < COOLDOWN_SECONDS:
            return {"classification": "cooldown"}
        if status.get("classification") == "stopped" and status.get("recovery_safe"):
            return {"classification": "start_permitted", "action": "start"}
        if status.get("classification") == "not_ready_trusted" and status.get("recovery_safe"):
            age = status.get("elapsed_seconds")
            if age is None and recovery["last_attempt_at"] is not None:
                age = now - recovery["last_attempt_at"]
            if age is not None and age >= STARTUP_GRACE_SECONDS:
                return {"classification": "restart_permitted", "action": "restart"}
            return {"classification": "startup_grace"}
        return {"classification": "identity_or_status_not_recovery_safe"}


def public_status(state, maintenance):
    recovery = state["recovery"]
    return {
        "initialized_at": utc_text(state["initialized_at"]),
        "updated_at": utc_text(state["updated_at"]),
        "maintenance": bool(maintenance),
        "incident": copy.deepcopy(state["incident"]),
        "recovery": {
            "attempts": recovery["attempts"],
            "circuit_latched": recovery["circuit_latched"],
            "last_attempt_at": utc_text(recovery["last_attempt_at"]) if recovery["last_attempt_at"] is not None else None,
            "in_flight": copy.deepcopy(recovery["in_flight"]),
            "last_result": copy.deepcopy(recovery["last_result"]),
        },
        "mail_pending": len(state["outbox"]),
        "last_snapshot": copy.deepcopy(state["last_snapshot"]),
    }


def require_root():
    if os.geteuid() != 0:
        raise MonitorError("root_required")


def parser():
    result = argparse.ArgumentParser(
        description="Bounded Juyi Hall service health monitor; cron uses --check-once.",
        epilog=("Examples: --init (explicit first state); --check-once (probe/write/recover); "
                "--status (stored snapshot only); --pause/--resume; --reset-circuit; "
                "--notify-test (explicit helper delivery test)."))
    actions = result.add_mutually_exclusive_group(required=True)
    actions.add_argument("--init", action="store_true", help="initialize absent state only; no probes/recovery/mail")
    actions.add_argument("--check-once", action="store_true", help="run one bounded check and optional API-only recovery")
    actions.add_argument("--status", action="store_true", help="read stored snapshot only; never repair or probe")
    actions.add_argument("--pause", action="store_true", help="create the trusted maintenance marker")
    actions.add_argument("--resume", action="store_true", help="remove a trusted maintenance marker")
    actions.add_argument("--reset-circuit", action="store_true", help="explicitly reset API attempt/circuit fence")
    actions.add_argument("--notify-test", action="store_true", help="explicitly enqueue and try one test email; no probes")
    return result


def main(argv=None):
    args = parser().parse_args(argv)
    os.umask(0o077)
    store = StateStore()
    try:
        require_root()
        config = load_config()
        if args.init:
            store.prepare_init()
        store.acquire()
        if args.init:
            if os.path.lexists(store.state_path):
                raise MonitorError("state_already_initialized")
            state = initial_state(time.time())
            store.write(state)
            print(json.dumps({"status": "initialized", "state": store.state_path}, sort_keys=True))
            return 0
        state = store.read()
        maintenance = store.maintenance()
        now = int(time.time())
        if args.status:
            print(json.dumps(public_status(state, maintenance), sort_keys=True, separators=(",", ":")))
            return 0
        if args.pause:
            store.pause(now)
            print(json.dumps({"status": "maintenance_paused"}, sort_keys=True))
            return 0
        if args.resume:
            store.resume()
            print(json.dumps({"status": "maintenance_resumed"}, sort_keys=True))
            return 0
        if args.reset_circuit:
            state["recovery"].update({"attempts": 0, "circuit_latched": False,
                                      "last_attempt_at": None, "in_flight": None,
                                      "last_result": None})
            state["updated_at"] = now
            store.write(state)
            print(json.dumps({"status": "circuit_reset"}, sort_keys=True))
            return 0
        effects = Effects()
        if args.notify_test:
            notice_id = "notify-test:%d" % now
            enqueue_notice(state, notice_id, "notify_test", "CYF health monitor test",
                           notice_body("explicit_notify_test", now, None, []), now)
            store.write(state)
            accepted = flush_outbox(state, effects, config, now, 1)
            state["updated_at"] = now
            store.write(state)
            print(json.dumps({"status": "notify_test_processed", "helper_accepted": accepted,
                              "mail_pending": len(state["outbox"])}, sort_keys=True))
            return 0 if accepted else 1
        monitor = Monitor(effects, store.write)
        summary = monitor.check_once(state, config, maintenance)
        print(json.dumps(summary, sort_keys=True, separators=(",", ":")))
        return 0 if summary["healthy"] else 1
    except BusyError:
        print(json.dumps({"status": "deferred", "reason": "monitor_lock_busy"}, sort_keys=True))
        return 75
    except MonitorError as exc:
        print(json.dumps({"status": "fail_closed", "reason": safe_label(str(exc))}, sort_keys=True),
              file=sys.stderr)
        return 2
    except Exception as exc:
        print(json.dumps({"status": "fail_closed", "reason": "unexpected_%s" % safe_label(type(exc).__name__)},
                         sort_keys=True), file=sys.stderr)
        return 2
    finally:
        store.release()


if __name__ == "__main__":
    sys.exit(main())
