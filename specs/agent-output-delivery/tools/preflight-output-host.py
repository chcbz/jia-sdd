#!/usr/bin/env python3
"""Read-only, bounded CYF host metadata probe; never run services or export credentials."""
import hashlib
import json
import os
from pathlib import Path
import re
import socket
import stat
import time


ROOTS = (
    "/var/lib/cyf-api-flow", "/var/lib/cyf-web-flow",
    "/home/isp/hosts/cyf/api", "/home/isp/hosts/cyf/web/kit",
    "/home/isp/apps", "/etc/cyf",
)
HELPERS = (
    "/usr/local/sbin/cyf-api-flow-deploy",
    "/usr/local/sbin/cyf-web-flow-deploy",
)
BINARIES = (
    "/home/isp/apps/mysql/bin/mysql", "/home/isp/apps/mysql/mysql.sock",
    "/home/isp/apps/nginx/sbin/nginx", "/home/isp/apps/minio/minio",
    "/home/isp/apps/clamav/sbin/clamd", "/usr/sbin/clamd",
)


def metadata(name, hash_small_regular=False):
    result = {"path": name}
    try:
        info = os.lstat(name)
        result.update(exists=True, mode=oct(stat.S_IMODE(info.st_mode)),
                      uid=info.st_uid, gid=info.st_gid, size=info.st_size,
                      symlink=stat.S_ISLNK(info.st_mode),
                      regular=stat.S_ISREG(info.st_mode))
        if hash_small_regular and stat.S_ISREG(info.st_mode) and info.st_size <= 1024 * 1024:
            fd = os.open(name, os.O_RDONLY | os.O_NOFOLLOW)
            with os.fdopen(fd, "rb") as stream:
                data = stream.read(1024 * 1024 + 1)
                observed = os.fstat(stream.fileno())
            if len(data) <= 1024 * 1024 and (info.st_dev, info.st_ino, info.st_mtime_ns) == (
                    observed.st_dev, observed.st_ino, observed.st_mtime_ns):
                result["sha256"] = hashlib.sha256(data).hexdigest()
            else:
                result["hashStatus"] = "changed_or_oversize"
    except FileNotFoundError:
        result["exists"] = False
    except OSError:
        result["status"] = "unreadable"
    return result


def disk(name):
    item = metadata(name)
    if item.get("exists"):
        try:
            info = os.statvfs(name)
            item.update(availableBytes=info.f_bavail * info.f_frsize,
                        totalBytes=info.f_blocks * info.f_frsize)
        except OSError:
            item["diskStatus"] = "unreadable"
    return item


def local_port(port):
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=0.5):
            return {"port": port, "tcpConnect": True}
    except OSError:
        return {"port": port, "tcpConnect": False}


def allowed_jar(arg):
    roots = ("/home/isp/hosts/cyf/api/", "/var/lib/cyf-api-flow/")
    if not re.fullmatch(r"/[A-Za-z0-9_./-]+\.jar", arg):
        return False
    if any(part in (".", "..") for part in arg.split("/")):
        return False
    return os.path.normpath(arg) == arg and arg.startswith(roots)


def api_processes():
    results = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdecimal():
            continue
        try:
            with (entry / "comm").open("rb") as stream:
                if stream.read(17).rstrip(b"\n") != b"java":
                    continue
            with (entry / "cmdline").open("rb") as stream:
                parts = stream.read(65537)
            if len(parts) > 65536:
                continue
            args = [x.decode("utf-8", errors="replace") for x in parts.split(b"\0") if x]
            if not args or Path(args[0]).name != "java":
                continue
            # Do not export the command line or arbitrary JVM/property values.
            jars = [arg for i, arg in enumerate(args) if i > 0 and args[i - 1] == "-jar"
                    and allowed_jar(arg)]
            if not jars:
                continue
            ticks = (entry / "stat").read_text().split(") ", 1)[1].split()[19]
            results.append({"pid": int(entry.name), "startTicks": ticks,
                            "jars": [metadata(jar) for jar in jars]})
        except (OSError, IndexError, ValueError):
            continue
    return results


def main():
    started = time.time()
    result = {
        "observedAtEpoch": int(started), "uid": os.getuid(), "readOnly": True,
        "directories": [disk(path) for path in ROOTS],
        "helpers": [metadata(path, True) for path in HELPERS],
        "binaries": [metadata(path) for path in BINARIES],
        "loopbackPorts": [local_port(port) for port in (10018, 3306, 6379, 5672, 9000, 3310)],
        "apiProcesses": api_processes(),
        "limits": ["No configuration file contents or process environments were read.",
                   "Bounded command lines were inspected in memory; only allowlisted CYF jar paths are exported.",
                   "TCP availability does not identify a service or establish readiness.",
                   "No SQL, application mutations, installation, restart or build was performed.",
                   "No schema, backup, storage policy, scanner signature or functional gate is closed."],
    }
    result["elapsedSeconds"] = round(time.time() - started, 3)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
