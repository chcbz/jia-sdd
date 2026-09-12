#!/usr/bin/env python3
import fcntl
import os
import time
from pathlib import Path

counter = Path("/tmp/od06-synthetic-codex-r3.invocations.log")
counter.parent.mkdir(parents=True, exist_ok=True)
with counter.open("a", encoding="utf-8") as stream:
    fcntl.flock(stream.fileno(), fcntl.LOCK_EX)
    stream.write(f"{int(time.time() * 1000)} pid={os.getpid()}\n")
    stream.flush()
    os.fsync(stream.fileno())
    fcntl.flock(stream.fileno(), fcntl.LOCK_UN)
os.execv("/tmp/od06-synthetic-codex-r2.py", ["/tmp/od06-synthetic-codex-r2.py", *os.sys.argv[1:]])
